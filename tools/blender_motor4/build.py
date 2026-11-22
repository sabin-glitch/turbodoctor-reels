"""Builds the 4-cylinder common-rail diesel in section, animates one full 720 deg cycle (1 frame = 1 deg of crank),
creates the section variants and the shot cameras, saves out/motor4.blend.

  /home/claude/vbpy/bin/python build.py
"""
import sys, os, time, math, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import bpy
from mathutils import Vector, Matrix
from lib import *
from dims import *
import mats, scene, anim
import parts_core as pc, parts_head as ph, parts_fuel as pf, parts_drive as pd, parts_fx as px

OUT = os.path.join(HERE, 'out'); os.makedirs(OUT, exist_ok=True)
NF = 720
FR = list(range(NF))
T0 = time.time()


def log(*a):
    print('[%6.1fs]' % (time.time() - T0), *a, flush=True)


REG = {}          # name -> kind ('house', 'comp', 'mov', 'fx')
SECM = {}         # name -> (sec material Y, sec material X)


def reg(ob, kind, secY=None, secX=None, sm=True, ang=35):
    c = {'house': 'housing', 'comp': 'comp', 'mov': 'mov', 'fx': 'fx'}[kind]
    move_to(ob, bpy.data.collections[c])
    REG[ob.name] = kind
    SECM[ob.name] = (secY, secX)
    if sm and ob.type == 'MESH':
        smooth(ob, ang)
    return ob


def mark_bores(blk, M):
    me = blk.data; me.materials.append(M['bore']); bi = len(me.materials) - 1
    for p in me.polygons:
        for cx in CX:
            d = Vector((p.center.x - cx, p.center.y, 0)); r = d.length
            if abs(r - RB) < 0.6 and p.center.z > 96 and r > 1e-6 and Vector((p.normal.x, p.normal.y, 0)).dot(-d.normalized()) > 0.85:
                p.material_index = bi


# ------------------------------------------------------------------------------------------- build
def build_all():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.unit_settings.system = 'NONE'
    M = mats.build()
    for n in ('housing', 'comp', 'mov', 'fx', 'var_L', 'var_D', 'var_E', 'var_F'):
        coll(n)
    # ---- block group
    blk = pc.build_block(); set_mats(blk, M['iron']); mark_bores(blk, M); reg(blk, 'house', 'iron_sec', 'iron_secX', ang=40)
    for c in pc.build_caps(): set_mats(c, M['iron']); reg(c, 'house', 'iron_sec', 'iron_secX')
    for s in pc.build_shells(): set_mats(s, M['shell']); reg(s, 'house', 'steel_sec', 'steel_secX')
    g = pc.build_gasket(); set_mats(g, M['gasket']); reg(g, 'house', 'steel_sec', 'steel_secX')
    pan = pc.build_pan(); set_mats(pan, M['pan']); reg(pan, 'house', 'pan_sec', 'pan_secX')
    pool = pc.build_oil_pool(); set_mats(pool, M['oil']); pool['a'] = 1.0; pool['p'] = 0.0; reg(pool, 'house')
    log('block')
    # ---- head group
    hd = ph.build_head(); set_mats(hd, M['alu']); reg(hd, 'house', 'alu_sec', 'alu_secX', ang=40)
    seats, guides, seals, washers = ph.build_seats_guides()
    for o in seats: set_mats(o, M['steel']); reg(o, 'house', 'steel_sec', 'steel_secX')
    for o in guides: set_mats(o, M['steel']); reg(o, 'house', 'steel_sec', 'steel_secX')
    for o in seals: set_mats(o, M['plastic']); reg(o, 'comp')
    for o in washers: set_mats(o, M['steel']); reg(o, 'comp')
    for o in ph.build_cam_caps(): set_mats(o, M['alu']); reg(o, 'house', 'alu_sec', 'alu_secX')
    for o in ph.build_head_bolts(): set_mats(o, M['bolt']); reg(o, 'house', 'steel_sec', 'steel_secX')
    cv = ph.build_cover(); set_mats(cv, M['plastic']); reg(cv, 'house', 'plastic_sec', 'plastic_secX')
    log('head')
    # ---- crank train
    crank = pc.build_crank(); set_mats(crank, M['steel']); reg(crank, 'mov', 'steel_sec', 'steel_secX', ang=40)
    fw = pc.build_flywheel(); set_mats(fw, M['steel']); reg(fw, 'mov', 'mov_sec', 'mov_secX')
    for i in range(4):
        reg(pc.build_piston(f'piston{i + 1}'), 'mov', 'piston_sec', 'piston_secX', ang=40)
        reg(pc.build_rod(f'rod{i + 1}'), 'mov', 'mov_sec', 'mov_secX')
    log('crank train')
    # ---- valvetrain
    VT = []
    for (i, kind, x, y) in ph.valves():
        sy = -1 if kind == 'I' else 1
        tag = f'{kind}{i + 1}{"a" if x < CX[i] else "b"}'
        v = ph.build_valve('valve_' + tag, kind); v.location = (x, y, Z_VFACE); reg(v, 'mov', 'mov_sec', 'mov_secX')
        lift = LIFT_I if kind == 'I' else LIFT_E
        s = spring('spring_' + tag, Z_SSEAT + 1.2, Z_RET, Z_RET - lift, 10.2, 1.75, 6.0)
        s.location = (x, y, 0); set_mats(s, M['spring']); reg(s, 'mov', 'mov_sec', 'mov_secX')
        f = ph.build_follower('follower_' + tag)
        if sy < 0:
            f.data.transform(Matrix.Scale(-1, 4, Vector((0, 1, 0)))); f.data.flip_normals()
        f.location = (x, sy * Y_HLA, Z_PIV); reg(f, 'mov', 'mov_sec', 'mov_secX')
        h = ph.build_hla('hla_' + tag); h.data.transform(Matrix.Translation((x, sy * Y_HLA, 0))); reg(h, 'comp')
        VT.append((i, kind, x, y, sy, tag))
    log('valvetrain')
    # ---- belt layout first (phases of the toothed wheels)
    lay = pd.belt_layout()
    log('belt teeth', lay['n'], 'length %.1f' % lay['total'], 'tensioner', lay['T'])
    rc = N_CRANK * BELT_P / TAU
    # belt offset s0 so that a belt tooth sits in a crank-sprocket groove at theta = 0
    ph_c = pd.phase_for(lay, (0.0, 0.0), rc, N_CRANK)          # sprocket rotation that would align (teeth at 0)
    s0 = -ph_c * rc                                            # instead slide the belt by the opposite amount
    lay['s0'] = s0
    def wheel_phase(c, r, n):
        # phase of a wheel with teeth centred at angle 0 so that it meshes with the belt displaced by s0
        segs, tot, nn = lay['segs'], lay['total'], lay['n']
        pb = tot / nn; best = (1e9, 0)
        for k in range(nn):
            (py, pz), _ = pd.path_eval(segs, tot, (k + 0.5) * pb + s0)
            d = abs(math.hypot(py - c[0], pz - c[1]) - r)
            if d < best[0]: best = (d, math.atan2(pz - c[1], py - c[0]))
        return best[1] - math.pi / n
    ph_cam = wheel_phase((Y_CAM, Z_CAM), N_CAM * BELT_P / TAU, N_CAM)
    ph_hp = wheel_phase((Y_HPP, Z_HPP), N_HPP * BELT_P / TAU, N_HPP)
    ph_wp = wheel_phase((Y_WP, Z_WP), N_WP * BELT_P / TAU, N_WP)
    # ---- camshafts (sprocket phase applied by rotating only the sprocket part: rebuild with rotation)
    cams = {}
    for sy in (-1, 1):
        cm = ph.build_camshaft('camshaft_' + ('intake' if sy < 0 else 'exhaust'), sy)
        cm.location = (0, sy * Y_CAM, Z_CAM)
        reg(cm, 'mov', 'mov_sec', 'mov_secX', ang=40)
        cams[sy] = cm
    # rotate the exhaust sprocket teeth: vertices with x < X_HF - 2 (the sprocket region) rotated by ph_cam
    me = cams[1].data
    R = Matrix.Rotation(ph_cam, 4, 'X')
    for v in me.vertices:
        if v.co.x < X_HF - 2.0:
            v.co = R @ v.co
    log('camshafts')
    # ---- fuel system
    for i, cx in enumerate(CX):
        inj = pf.build_injector(f'injector{i + 1}')
        inj.rotation_euler = (0, 0, math.pi); inj.location = (cx, 0, Z_TIP); reg(inj, 'comp')
        gp = pf.build_glow_plug(f'glowplug{i + 1}')
        gp.rotation_euler = (GP_ANG, 0, 0); gp.location = (cx + GP_TIP[0], GP_TIP[1], GP_TIP[2]); gp['g'] = 0.0; reg(gp, 'comp')
    for o in pf.build_risers(): reg(o, 'comp')
    reg(pf.build_leakoff(), 'comp')
    for o in pf.build_clamps(): reg(o, 'comp')
    rail, rfuel, sens, drv = pf.build_rail()
    reg(rail, 'house', 'rail_sec', 'steel_secX'); rfuel['a'] = 1.0; rfuel['p'] = 1.0; reg(rfuel, 'house')
    reg(sens, 'comp'); reg(drv, 'comp')
    reg(pd.build_hp_line(), 'comp')
    log('fuel system')
    # ---- belt drive
    belt = pd.build_belt(lay); reg(belt, 'mov', sm=False)
    idl = pd.build_idlers(lay)
    reg(idl['tensioner'], 'mov', 'mov_sec', 'mov_secX'); reg(idl['idler'], 'mov', 'mov_sec', 'mov_secX'); reg(idl['tens_arm'], 'comp')
    wpp, wph = pd.build_wpump(lay)
    wpp.data.transform(Matrix.Rotation(ph_wp, 4, 'X')); wpp.location = (0, Y_WP, Z_WP)
    reg(wpp, 'mov', 'mov_sec', 'mov_secX'); reg(wph, 'comp')
    # ---- HP pump
    HP = pd.build_hp_pump()
    me = HP['shaft'].data; R = Matrix.Rotation(ph_hp, 4, 'X')
    for v in me.vertices:
        if v.co.x < X_BF - 1.0: v.co = R @ v.co
    for k in ('shaft', 'tappet', 'spring', 'ball', 'ivalve', 'fuel_ch'):
        reg(HP[k], 'mov', 'mov_sec', 'mov_secX')
    for k in ('housing', 'barrel', 'ofit', 'meun', 'nipple', 'fuel_lp', 'fuel_hp', 'fuel_in'):
        reg(HP[k], 'comp', 'alu_sec' if k == 'housing' else 'steel_sec', 'alu_secX' if k == 'housing' else 'steel_secX')
    for k in ('fuel_lp', 'fuel_hp', 'fuel_in'):
        HP[k]['a'] = 1.0; HP[k]['p'] = 0.0 if k != 'fuel_hp' else 1.0
        SECM[HP[k].name] = (None, None)
    HP['fuel_ch']['a'] = 1.0; HP['fuel_ch']['p'] = 0.0; SECM[HP['fuel_ch'].name] = (None, None)
    log('hp pump')
    # ---- oil pump + chain
    OP = pd.build_oil_pump()
    reg(OP['rotor'], 'mov', 'mov_sec', 'mov_secX')
    for v in OP['vanes']: reg(v, 'mov', 'mov_sec', 'mov_secX')
    for k in ('housing', 'pickup', 'outpipe'):
        reg(OP[k], 'comp', 'alu_sec' if k == 'housing' else 'steel_sec', 'alu_secX' if k == 'housing' else 'steel_secX')
    OP['oil_s']['a'] = 1.0; OP['oil_s']['p'] = 0.0; OP['oil_p']['a'] = 1.0; OP['oil_p']['p'] = 1.0
    reg(OP['oil_s'], 'comp'); reg(OP['oil_p'], 'comp')
    chl = pd.chain_layout()
    rch = N_CHS * CHAIN_P / TAU
    # chain offset so that a roller sits in a crank chain-sprocket groove
    segs, tot, nn = chl['segs'], chl['total'], chl['n']
    pcn = tot / nn; best = (1e9, 0)
    for k in range(nn):
        (py, pz), _ = pd.path_eval(segs, tot, k * pcn)
        d = abs(math.hypot(py, pz) - rch)
        if d < best[0]: best = (d, math.atan2(pz, py))
    g_ang = math.pi / N_CHS                                       # first groove angle of the crank sprocket
    dpsi = ((g_ang - best[1]) + math.pi / N_CHS) % (TAU / N_CHS) - math.pi / N_CHS
    chl['s0'] = dpsi * rch
    # pump sprocket phase (rotate its teeth so a groove meets a roller)
    best = (1e9, 0)
    for k in range(nn):
        (py, pz), _ = pd.path_eval(segs, tot, k * pcn + chl['s0'])
        d = abs(math.hypot(py, pz - Z_OP) - rch)
        if d < best[0]: best = (d, math.atan2(pz - Z_OP, py))
    ph_op = best[1] - math.pi / N_CHS
    me = OP['rotor'].data; R = Matrix.Rotation(ph_op, 4, 'X')
    for v in me.vertices:
        if v.co.x < X_CHAIN + 4.0 and math.hypot(v.co.y, v.co.z) > 12.5: v.co = R @ v.co
    ch = pd.build_chain(chl); reg(ch, 'mov', sm=False)
    log('oil pump + chain')
    # ---- effects
    for i in range(4):
        g, b = px.build_gas(i); reg(g, 'fx', sm=False); reg(b, 'fx', sm=False)
        reg(px.build_spray(i), 'fx', sm=False)
    for o in px.build_port_gas(): reg(o, 'fx', sm=False)
    log('effects')
    stray = [o.name for o in sc.collection.objects if o.type == 'MESH']
    if stray:
        log('WARNING stray meshes removed:', stray[:20])
        for n in stray: remove(bpy.data.objects[n])
    return dict(lay=lay, chl=chl, VT=VT, HP=HP, OP=OP)


# ------------------------------------------------------------------------------------------- animation
def animate(S):
    lay, chl, VT, HP, OP = S['lay'], S['chl'], S['VT'], S['HP'], S['OP']
    ob = bpy.data.objects
    th = [float(f) for f in FR]
    rad = [math.radians(t) for t in th]
    anim.keys(ob['crankshaft'], 'rotation_euler', 0, FR, rad)
    anim.keys(ob['flywheel'], 'rotation_euler', 0, FR, rad)
    for i, cx in enumerate(CX):
        p = ob[f'piston{i + 1}']; r = ob[f'rod{i + 1}']
        zp = [piston_z(t, i) for t in th]
        cp = [crankpin(t, i) for t in th]
        p.location = (cx, 0, zp[0]); anim.keys(p, 'location', 2, FR, zp)
        r.location = (cx, cp[0][0], cp[0][1])
        anim.keys(r, 'location', 1, FR, [c[0] for c in cp]); anim.keys(r, 'location', 2, FR, [c[1] for c in cp])
        anim.keys(r, 'rotation_euler', 0, FR, [math.atan2(c[0], z - c[1]) for c, z in zip(cp, zp)])
    for (i, kind, x, y, sy, tag) in VT:
        lifts = [valve_lift(cyc(t, i), kind) for t in th]
        L = LIFT_I if kind == 'I' else LIFT_E
        anim.keys(ob['valve_' + tag], 'location', 2, FR, [Z_VFACE - l for l in lifts])
        sp = ob['spring_' + tag]
        anim.keys(sp.data.shape_keys, 'key_blocks["comp"].value', -1, FR, [l / L for l in lifts])
        anim.keys(ob['follower_' + tag], 'rotation_euler', 0, FR, [sy * ph.follower_angle(l) for l in lifts])
    for sy in (-1, 1):
        anim.keys(ob['camshaft_' + ('intake' if sy < 0 else 'exhaust')], 'rotation_euler', 0, FR, [ph.cam_alpha(t, sy) for t in th])
    # belt + pulleys
    rc = N_CRANK * BELT_P / TAU
    s_belt = [lay['s0'] + r_ * rc for r_ in rad]
    kv = [pd.belt_key_values(lay, s) for s in s_belt]
    bk = ob['belt'].data.shape_keys
    for k in range(1, pd.K_KEYS):
        anim.keys(bk, f'key_blocks["o{k}"].value', -1, FR, [v[k - 1] for v in kv])
    anim.keys(ob['wp_pulley'], 'rotation_euler', 0, FR, [r_ * rc / (N_WP * BELT_P / TAU) for r_ in rad])
    anim.keys(ob['tensioner'], 'rotation_euler', 0, FR, [-r_ * rc / (pd.R_TENS + pd.BELT_OUT) for r_ in rad])
    anim.keys(ob['idler'], 'rotation_euler', 0, FR, [-r_ * rc / (pd.R_IDL + pd.BELT_OUT) for r_ in rad])
    # HP pump (shaft at engine speed)
    beta = [r_ + pd.HP_PHASE for r_ in rad]
    anim.keys(HP['shaft'], 'rotation_euler', 0, FR, beta)
    lifts = [pd.hp_lift(b) for b in beta]
    zr0 = pd.HP_R0 + pd.HP_RR
    anim.keys(HP['tappet'], 'location', 2, FR, [Z_HPP + zr0 + l for l in lifts])
    Lf = HP['spring']['Lf']
    anim.keys(HP['spring'], 'scale', 2, FR, [(Lf - l) / Lf for l in lifts])
    def stroke_phase(b):
        return (2 * b) % TAU          # 0..pi: plunger rising (delivery), pi..2pi: falling (suction)
    def sm(x):
        x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)
    pvals, ball, ival, chs = [], [], [], []
    for b, l in zip(beta, lifts):
        ps = stroke_phase(b)
        if ps < math.pi: p = sm((ps - 0.05) / 0.35)
        else: p = 1 - sm((ps - math.pi) / 0.3)
        pvals.append(p)
        ball.append(0.9 * (sm((ps - 0.45) / 0.15) * (1 - sm((ps - math.pi + 0.15) / 0.12))) if ps < math.pi else 0.0)
        ival.append(-0.7 * (sm((ps - math.pi - 0.15) / 0.2) * (1 - sm((ps - TAU + 0.35) / 0.2))) if ps >= math.pi else 0.0)
        chs.append(max(0.4, 9.0 - l))
    anim.keys(HP['fuel_ch'], '["p"]', -1, FR, pvals)
    anim.keys(HP['fuel_ch'], 'scale', 2, FR, chs)
    anim.keys(HP['ball'], 'location', 1, FR, [Y_HPP + 8.4 + v for v in ball])
    anim.keys(HP['ivalve'], 'location', 2, FR, [Z_HPP + pd.Z_CH_TOP + 0.2 + v for v in ival])
    # oil pump rotor + vanes, chain
    anim.keys(OP['rotor'], 'rotation_euler', 0, FR, rad)
    for k, v in enumerate(OP['vanes']):
        psis = [r_ + TAU * k / pd.OP_NV for r_ in rad]
        tips = [pd.vane_tip(ps) for ps in psis]
        anim.keys(v, 'location', 1, FR, [t * math.cos(ps) for t, ps in zip(tips, psis)])
        anim.keys(v, 'location', 2, FR, [Z_OP + t * math.sin(ps) for t, ps in zip(tips, psis)])
        anim.keys(v, 'rotation_euler', 0, FR, [ps - math.pi / 2 for ps in psis])
    rch = N_CHS * CHAIN_P / TAU
    kv = [pd.chain_key_values(chl, chl['s0'] + r_ * rch) for r_ in rad]
    ck = ob['chain'].data.shape_keys
    for k in range(1, pd.K_KEYS):
        anim.keys(ck, f'key_blocks["o{k}"].value', -1, FR, [v[k - 1] for v in kv])
    # effects
    for i, cx in enumerate(CX):
        g = ob[f'gas{i}']
        b = ob[f'gasbowl{i}']; sp = ob[f'spray{i}']
        zp = [piston_z(t, i) for t in th]
        crown = [z + CH for z in zp]
        anim.keys(g, 'location', 2, FR, crown)
        anim.keys(g, 'scale', 2, FR, [max(0.2, Z_HD - c) for c in crown])
        anim.keys(b, 'location', 2, FR, zp)
        st = [px.gas_state(cyc(t, i)) for t in th]
        for o in (g, b):
            for j in range(3):
                anim.keys(o, '["col"]', j, FR, [s[0][j] for s in st])
            anim.keys(o, '["e"]', -1, FR, [s[1] for s in st])
            anim.keys(o, '["a"]', -1, FR, [s[2] for s in st])
        ss = [px.spray_state(cyc(t, i)) for t in th]
        for j in range(3):
            anim.keys(sp, 'scale', j, FR, [max(0.001, s[0]) for s in ss])
        anim.keys(sp, '["a"]', -1, FR, [s[1] for s in ss])
    for o in [o for o in bpy.data.collections['fx'].objects if o.name.startswith('pgas_')]:
        i = int(o['cyl']); kind = o['kind']
        st = [px.port_state(kind, cyc(t, i)) for t in th]
        for j in range(3):
            anim.keys(o, '["col"]', j, FR, [s[0][j] for s in st])
        anim.keys(o, '["e"]', -1, FR, [s[1] for s in st])
        anim.keys(o, '["a"]', -1, FR, [s[2] for s in st])
    log('animation keys')


# ------------------------------------------------------------------------------------------- section variants
FLUID_MATS = ('fuel_lp', 'fuel_hp', 'fuel_var', 'oil')


def cut_copy(ob, axis, value, keep, coll_name, suffix):
    """copy `ob` (sharing its animation), cut in the object's local space with a world-space half-space.
    Fluid volumes are cut 0.3 mm behind the plane, so the cut faces of the parts inside them stay in front."""
    if any(m and m.name in FLUID_MATS for m in ob.data.materials):
        value = value + 0.3 * keep
    o2 = ob.copy(); o2.data = ob.data.copy(); o2.name = ob.name + suffix
    bpy.data.collections[coll_name].objects.link(o2)
    if o2.data.shape_keys:
        # booleans cannot keep shape keys: cut copies of shape-keyed objects are not supported -> skip
        bpy.data.objects.remove(o2, do_unlink=True); return None
    big = 5000.0
    lo, hi = [-big] * 3, [big] * 3
    i = 'xyz'.index(axis)
    if keep > 0: hi[i] = value
    else: lo[i] = value
    c = box('cutter', lo[0], hi[0], lo[1], hi[1], lo[2], hi[2])     # world space: the boolean modifier applies the relative transform
    bpy.context.view_layer.update()
    Mw = ob.matrix_world.copy()
    apply_bool(o2, c); remove(c)
    if len(o2.data.polygons) == 0:
        bpy.data.objects.remove(o2, do_unlink=True); return None
    secY, secX = SECM.get(ob.name, (None, None))
    sec = secY if axis == 'y' else secX
    if sec:
        sm_ = mats.M[sec]
        me = o2.data
        if sm_.name not in [m.name for m in me.materials if m]: me.materials.append(sm_)
        mi = [m.name if m else '' for m in me.materials].index(sm_.name)
        R3 = Mw.to_3x3()
        for p in me.polygons:
            cw = Mw @ p.center; nw = (R3 @ p.normal).normalized()
            if abs(cw[i] - value) < 0.05 and nw[i] * (-keep) > 0.97:
                p.material_index = mi
    return o2


def world_range(ob, axis):
    i = 'xyz'.index(axis)
    Mw = ob.matrix_world
    vals = [(Mw @ Vector(c))[i] for c in ob.bound_box]
    return min(vals), max(vals)


KEEP_WHOLE_E = None


def make_variants():
    bpy.context.scene.frame_set(0)
    bpy.context.view_layer.update()
    VAR = {'L': [], 'D': [], 'E': [], 'F': []}
    # L: housings cut at y = 0 (keep y >= 0)
    for n, k in list(REG.items()):
        ob = bpy.data.objects[n]
        if k == 'house':
            lo, hi = world_range(ob, 'y')
            if lo >= -0.01: VAR['L'].append(n); continue
            if hi <= 0.0: continue
            o2 = cut_copy(ob, 'y', 0.0, +1, 'var_L', '_L')
            if o2: VAR['L'].append(o2.name)
        elif k in ('comp', 'mov') or (k == 'fx' and not n.startswith('pgas_')):
            VAR['L'].append(n)
    log('variant L', len(VAR['L']))
    # D: L + pistons and gases cut at y = 0
    swap = {}
    for i in range(4):
        for n in (f'piston{i + 1}', f'gas{i}', f'gasbowl{i}'):
            o2 = cut_copy(bpy.data.objects[n], 'y', 0.0, +1, 'var_D', '_D')
            if o2: swap[n] = o2.name
    VAR['D'] = [swap.get(n, n) for n in VAR['L']]
    log('variant D')
    # transverse variants: E on the whole engine, F (front section) applied on top of the L section
    Lmap = {}
    for n in VAR['L']:
        if n.endswith('_L'): Lmap[n[:-2]] = n
    def transverse(name, xv, keep_whole, on_L):
        out = []
        for n, k in list(REG.items()):
            if k == 'fx' and n.startswith('spray'):
                i = int(n[5:])
                if CX[i] - 32.0 >= xv or abs(CX[i] - xv) < 20.0: out.append(n)
                continue
            if k == 'fx' and n.startswith('pgas_') and on_L: continue
            src = n
            if on_L and k == 'house':
                if n in Lmap: src = Lmap[n]
                elif n not in VAR['L']: continue          # housing entirely removed by the L cut
            ob = bpy.data.objects[src]
            lo, hi = world_range(ob, 'x')
            if hi <= xv: continue
            if lo >= xv or n in keep_whole: out.append(src); continue
            o2 = cut_copy(ob, 'x', xv, +1, 'var_' + name, '_' + name)
            if o2:
                SECM[o2.name] = SECM.get(n, (None, None)); out.append(o2.name)
            elif ob.data.shape_keys: out.append(src)
        return out
    for n in list(Lmap.values()):
        orig = n[:-2]; SECM[n] = SECM.get(orig, (None, None))
    kw = set()
    for (i, kind, x, y) in ph.valves():
        if abs(x - X_T) < 0.01:
            tag = f'{kind}{i + 1}{"a" if x < CX[i] else "b"}'
            kw |= {'valve_' + tag, 'spring_' + tag, 'follower_' + tag, 'hla_' + tag}
            for nm in list(REG):
                if nm.startswith(('seal_', 'swash_')) and nm.endswith(f'{kind}{i}_{x:.0f}'): kw.add(nm)
    VAR['E'] = transverse('E', X_T, kw, False)
    log('variant E', len(VAR['E']))
    VAR['F'] = transverse('F', X_FRONT, set(), True)
    log('variant F', len(VAR['F']))
    return VAR


# ------------------------------------------------------------------------------------------- shots
def uniform(th0, span, n):
    return [th0 + span * k / n for k in range(n)]


def warped(th0, cyl_i, base=10.0, slow=1.8, c0=688.0, c1=770.0, ramp=18.0):
    """crank angles for one 720-deg loop with slow motion around the firing TDC of cylinder cyl_i."""
    def v(th):
        c = cyc(th, cyl_i)
        d = c if c < 540 else c - 720          # -180..540, 0 = firing TDC
        a, b_ = c0 - 720, c1 - 720
        if d < a - ramp or d > b_ + ramp: return base
        if a <= d <= b_: return slow
        t = (a - d) / ramp if d < a else (d - b_) / ramp
        t = t * t * (3 - 2 * t)
        return slow + (base - slow) * t
    th, out = th0, []
    while th < th0 + 720.0 - 1e-6:
        out.append(th); th += v(th)
    scale = 720.0 / (th - th0)
    return [th0 + (t - th0) * scale for t in out]


SHOTS = {
    'A_motor':      dict(var='L', thetas=uniform(0.0, 720.0, 72), glow=0.0, floor=False,
                         cam=((-28.0, 0.0, 150.0), 18.0, 15.0, 3200.0), fit=((-290, -150, -160), (250, 120, 455)), region=(40, 1040, 300, 1500)),
    'B_pompa_inalta': dict(var='F', thetas=uniform(0.0, 720.0, 72), glow=0.0, floor=False,
                         cam=((X_FRONT, Y_HPP, Z_HPP + 45.0), 80.0, 8.0, 1600.0), fit=((X_FRONT, -152, 166), (X_FRONT, -70, 324)), region=(90, 990, 360, 1440)),
    'C_pompa_ulei': dict(var='F', thetas=uniform(0.0, 360.0, 60), glow=0.0, floor=False,
                         cam=((X_FRONT, 0.0, Z_OP + 5.0), 62.0, 14.0, 1600.0), fit=((X_FRONT, -60, -150), (X_FRONT, 52, -42)), region=(90, 990, 420, 1400)),
    'D_cilindru':   dict(var='D', thetas=warped(FIRE[1] + 200.0, 1, base=13.0, slow=2.2), glow=1.0, floor=False,
                         cam=((CX[1], 0.0, 285.0), 20.0, 3.0, 1800.0), fit=((CX[1] - 46, -20, 160), (CX[1] + 46, 12, 400)), region=(60, 1020, 230, 1610)),
    'E_supape':     dict(var='E', thetas=uniform(0.0, 720.0, 72), glow=0.0, floor=False,
                         cam=((X_T, 0.0, 220.0), 76.0, 8.0, 2600.0), fit=((X_T, -105, -70), (X_T, 105, 445)), region=(60, 1020, 230, 1640)),
}


def fit_camera(co, pts, region):
    """adjust lens + shift so that the projections of pts fill `region` (x0, x1, y0, y1 in px of 1080x1920)."""
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene; cd = co.data
    P = [Vector(p) for p in pts]
    x0, x1, y0, y1 = region
    cd.lens = 50.0; cd.shift_x = 0.0; cd.shift_y = 0.0
    def meas():
        bpy.context.view_layer.update()
        pr = [world_to_camera_view(sc, co, p) for p in P]
        xs = [v.x * 1080 for v in pr]; ys = [(1 - v.y) * 1920 for v in pr]
        return min(xs), max(xs), min(ys), max(ys)
    for _ in range(12):
        m = meas()
        k = min((x1 - x0) / max(m[1] - m[0], 1e-3), (y1 - y0) / max(m[3] - m[2], 1e-3))
        cd.lens *= k
        for attr, idx, goal in (('shift_x', 0, (x0 + x1) / 2), ('shift_y', 1, (y0 + y1) / 2)):
            m = meas(); c0 = ((m[0] + m[1]) / 2, (m[2] + m[3]) / 2)[idx]
            setattr(cd, attr, getattr(cd, attr) + 0.01)
            m = meas(); c1 = ((m[0] + m[1]) / 2, (m[2] + m[3]) / 2)[idx]
            setattr(cd, attr, getattr(cd, attr) - 0.01)
            if abs(c1 - c0) > 1e-6:
                setattr(cd, attr, getattr(cd, attr) + (goal - c0) / ((c1 - c0) / 0.01))
    m = meas()
    log('fit', co.name, 'lens %.1f shift %.3f %.3f' % (cd.lens, cd.shift_x, cd.shift_y), [round(v) for v in m])
    return co


def bbox_pts(a, b):
    return [(x, y, z) for x in (a[0], b[0]) for y in (a[1], b[1]) for z in (a[2], b[2])]


ANCHORS = {
    'bloc': (-120.0, 0.0, 60.0), 'chiulasa': (-120.0, 0.0, 262.0), 'arbore_cotit': (-44.0, 0.0, 0.0), 'piston': (CX[1], 0.0, 150.0),
    'biela': (CX[1], 0.0, 80.0), 'supapa_admisie': (CX[1] - VX, -VY, 300.0), 'supapa_evacuare': (CX[1] - VX, VY, 300.0),
    'arc_supapa': (CX[1] - VX, -VY, 302.0), 'culbutor_rola': (CX[1] - VX, -Y_CAM, Z_ROLL), 'ax_came_admisie': (CX[1], -Y_CAM, Z_CAM),
    'ax_came_evacuare': (CX[1], Y_CAM, Z_CAM), 'element_hidraulic': (CX[1] - VX, -Y_HLA, Z_PIV - 15), 'injector': (CX[1], 0.0, Z_TIP + 90.0),
    'duza_injector': (CX[1], 0.0, Z_TIP), 'bujie_incandescenta': (CX[1], GP_TIP[1] - 20 * math.sin(GP_ANG), GP_TIP[2] + 20 * math.cos(GP_ANG)),
    'varf_bujie': (CX[1], GP_TIP[1], GP_TIP[2]), 'rampa': (0.0, 0.0, Z_RAIL + R_RAIL), 'senzor_presiune_rampa': (-215.0, 0.0, Z_RAIL),
    'regulator_presiune': (205.0, 0.0, Z_RAIL), 'conducta_injector': (CX[1] + X_RISER, 0.0, 380.0), 'pompa_inalta_presiune': (-200.0, Y_HPP, Z_HPP),
    'curea_distributie': (X_BELT, -120.0, 300.0), 'intinzator': (X_BELT, -60.0, 309.0), 'pompa_apa': (X_BELT, Y_WP, Z_WP),
    'pompa_ulei': (X_FRONT, 0.0, Z_OP), 'sorb_ulei': (X_FRONT, -6.0, Z_PANB + 12.0), 'baie_ulei': (0.0, 0.0, -120.0), 'volanta': (230.0, 0.0, 120.0),
    'lant_pompa_ulei': (X_CHAIN, 22.0, -46.0), 'camera_ardere': (CX[1], 0.0, 236.0), 'cama_pompa': (X_FRONT, Y_HPP, Z_HPP + 16.0),
    'piston_pompa': (X_FRONT, Y_HPP, Z_HPP + 75.0), 'supapa_iesire_pompa': (X_FRONT, Y_HPP + 10.0, Z_HPP + 84.0), 'dozator': (X_FRONT, Y_HPP - 40.0, Z_HPP + 46.0),
    'rotor_palete': (X_FRONT, 0.0, Z_OP), 'iesire_ulei': (X_FRONT, -60.0, Z_OP + 45.0),
}


def make_shots(VAR):
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene
    sc.render.resolution_x, sc.render.resolution_y = 1080, 1920
    scene.render_settings(samples=8, pct=100)
    base_layer = sc.view_layers[0]; base_layer.name = 'ALL'
    # floor shadow catcher
    fl = box('floor_shadow', -2500, 2500, -2500, 2500, Z_PANB - 1.6, Z_PANB - 0.6)
    fl.is_shadow_catcher = True
    set_mats(fl, mats.M['pan'])
    info = {}
    for name, S in SHOTS.items():
        tgt, yaw, pit, dist = S['cam']
        co = scene.camera('CAM_' + name, tgt, yaw, pit, dist, 50.0)
        fit_camera(co, bbox_pts(*S['fit']), S['region'])
        c = coll('SHOT_' + name)
        for n in VAR[S['var']]:
            ob = bpy.data.objects.get(n)
            if ob and ob.name not in c.objects: c.objects.link(ob)
        if S.get('floor'): c.objects.link(fl)
        bpy.context.view_layer.update()
        def px(p):
            v = world_to_camera_view(sc, co, Vector(p)); return [round(v.x * 1080, 1), round((1 - v.y) * 1920, 1), round(v.z, 1)]
        info[name] = dict(anch={k: px(p) for k, p in ANCHORS.items()}, lens=co.data.lens, shift=[co.data.shift_x, co.data.shift_y],
                          matrix=[list(r) for r in co.matrix_world], thetas=S['thetas'])
        log('shot', name, 'objects', len(c.objects), 'frames', len(S['thetas']), 'lens %.1f' % co.data.lens)
    if fl.name in sc.collection.objects: sc.collection.objects.unlink(fl)
    for name in SHOTS:
        vl = sc.view_layers.get(name) or sc.view_layers.new(name)
        for lc in vl.layer_collection.children:
            lc.exclude = (lc.name != 'SHOT_' + name)
    for lc in base_layer.layer_collection.children:
        lc.exclude = not lc.name.startswith(('housing', 'comp', 'mov', 'fx'))
    base_layer.use = False
    sc['shots'] = json.dumps({k: {kk: vv for kk, vv in v.items() if kk not in ('cam', 'fit', 'region')} for k, v in SHOTS.items()})
    json.dump(info, open(os.path.join(OUT, 'info.json'), 'w'), indent=1)
    sc.frame_start, sc.frame_end = 0, NF - 1
    sc.render.fps = 30


def main():
    S = build_all()
    animate(S)
    VAR = make_variants()
    make_shots(VAR)
    for ob in bpy.data.objects:
        if ob.type == 'MESH':
            for p in ob.data.polygons: pass
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, 'motor4.blend'), compress=True)
    log('saved', len(bpy.data.objects), 'objects')


if __name__ == '__main__':
    main()
