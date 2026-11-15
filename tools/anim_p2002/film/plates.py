# Randeaza cadrele fixe (cu adancime), straturile in bucla si orbita de inceput. Sare peste ce exista deja.
import sys, os, json, math, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import bpy, numpy as np
import film as F, rig, layout as L, shots as S
import OpenEXR

OUT = os.environ.get('DPF_PL', os.path.join(HERE, 'pl')); os.makedirs(OUT, exist_ok=True)
W = int(os.environ.get('PW', S.W)); H = int(os.environ.get('PH', S.H)); SPP = int(os.environ.get('SPP', '40'))
F.load(W, H, SPP)
D = F.D; scn = F.scn; cy = scn.cycles
MOVING = ['CRANK', 'ROD', 'PISTON', 'VEX', 'VIN', 'VEX.SPR', 'VIN.SPR', 'VEX.CAM', 'VIN.CAM']
soot_b = bpy.data.materials['soot'].node_tree.nodes['Principled BSDF']

def set_cam(name, pos=None):
    c = S.CAMS[name]
    rig.aim(F.cam, tuple(pos if pos is not None else c['pos']), tuple(c['tgt']), lens=c['lens'], fstop=c.get('fstop'),
            focus_mm=tuple(c['focus']) if 'focus' in c else None)

def apply(st):
    for g in ('exh', 'egr', 'int'): F.ghost(g, 1 if g in st.get('ghost', ()) else 0)
    F.key('mod.soot', st.get('soot', 0.35)); F.key('mod.ash', st.get('ash', 0.0)); F.key('mod.glaze', st.get('glaze', 0.0))
    F.show('mod.soot', st.get('soot', 0.35) > 0.01)
    F.show('mod.ash', st.get('ash', 0.0) > 0); F.show('mod.glaze', st.get('glaze', 0.0) > 0)
    F.show('mod.glazeTop', st.get('glazeTop', False)); F.show('egr.crack', st.get('egr_crack', False)); F.show('dps.crack', st.get('dps_crack', False))
    F.pose(math.radians(st.get('th', 60)))
    F.flap('egrv.FLAP', math.radians(st.get('egrv', 35))); F.flap('exf.FLAP', math.radians(st.get('exf', 75)))
    F.rotor(math.radians(st.get('rot', 0)))
    soot_b.inputs['Emission Strength'].default_value = st.get('glow', 0.0)
    if st.get('glow_col') is not None: soot_b.inputs['Emission Color'].default_value = (*st['glow_col'], 1.0)
    for n in MOVING: F.show(n, not st.get('no_eng', False))
    F.show('ROTOR', not st.get('no_rotor', False))

def ghost_objs(st):
    act = set(st.get('ghost', ())); out = []
    for o in D:
        if o.type != 'MESH': continue
        if any(s.material is not None and s.material.get('ghost') in act for s in o.material_slots): out.append(o)
    return out

def read_z(path):
    f = OpenEXR.File(path)
    for p in f.parts:
        for k, v in p.channels.items():
            if 'Depth' in k: return np.asarray(v.pixels, np.float32)

def zpass(base, st, extra_hide=()):
    """adancimea primei suprafete opace (piesele transparente sunt ascunse), camera fara profunzime de camp"""
    hid = [o for o in ghost_objs(st) if not o.hide_render] + [o for o in extra_hide if not o.hide_render]
    for o in hid: o.hide_render = True
    old = (cy.samples, cy.use_denoising, F.cam.data.dof.use_dof, cy.max_bounces)
    cy.samples = 1; cy.use_denoising = False; F.cam.data.dof.use_dof = False; cy.max_bounces = 0
    R = scn.render; s = R.image_settings
    bpy.ops.render.render(write_still=False)
    s.media_type = 'MULTI_LAYER_IMAGE'; s.file_format = 'OPEN_EXR_MULTILAYER'; s.color_depth = '32'; s.exr_codec = 'ZIP'
    tmp = base + '.tmp.exr'
    bpy.data.images['Render Result'].save_render(tmp, scene=scn)
    s.media_type = 'IMAGE'; s.file_format = 'PNG'; s.color_mode = 'RGBA'; s.color_depth = '8'
    z = read_z(tmp); os.remove(tmp)
    z = np.where(z > 1e6, 1e6, z).astype(np.float32)
    np.save(base + '.z.npy', z)
    cy.samples, cy.use_denoising, F.cam.data.dof.use_dof, cy.max_bounces = old
    for o in hid: o.hide_render = False

def hq(on=True):
    try:
        cy.denoising_prefilter = 'ACCURATE' if on else 'FAST'; cy.denoising_quality = 'HIGH' if on else 'FAST'
    except Exception: pass

def plate(camn, stn):
    base = os.path.join(OUT, '%s__%s' % (camn, stn))
    if os.path.exists(base + '.z.npy') and os.path.exists(base + '.png'): return
    st = S.STATES[stn]; set_cam(camn); apply(st)
    scn.render.resolution_x, scn.render.resolution_y = W, H; cy.samples = SPP; hq(True)
    t = time.time(); F.render(base, exr=False); t1 = time.time() - t
    zpass(base, st)
    print('PLATE %s__%s beauty %.1fs total %.1fs' % (camn, stn, t1, time.time() - t), flush=True)

# ------------------------------------------------------------- straturi in bucla
HOLD = None
def hold_mat():
    global HOLD
    if HOLD is None:
        HOLD = bpy.data.materials.new('HOLD'); HOLD.use_nodes = True
        N = HOLD.node_tree.nodes; Lk = HOLD.node_tree.links
        for n in list(N):
            if n.type != 'OUTPUT_MATERIAL': N.remove(n)
        out = [n for n in N if n.type == 'OUTPUT_MATERIAL'][0]
        h = N.new('ShaderNodeHoldout'); Lk.new(h.outputs[0], out.inputs['Surface'])
    return HOLD

def loop(lp):
    camn, stn, kind, n = lp['cam'], lp['state'], lp['kind'], lp['n']
    lw, lh = W * 2 // 3, H * 2 // 3
    names = MOVING if kind == 'engine' else ['ROTOR']
    base0 = os.path.join(OUT, 'loop_%s_%s' % (camn, kind))
    if os.path.exists(base0 + '_%03d.z.npy' % (n - 1)): return
    st = dict(S.STATES[stn]); st.pop('no_eng', None) if kind == 'engine' else st.pop('no_rotor', None)
    set_cam(camn); apply(st)
    mov = set()
    for nm in names:
        mov.add(D[nm]); mov.update(D[nm].children_recursive)
    gh = set(ghost_objs(st)) - mov
    saved = []; hm = hold_mat()
    for o in D:
        if o.type != 'MESH' or o in mov or o.hide_render: continue
        if o in gh: o.hide_render = True; saved.append((o, None)); continue
        saved.append((o, [s.material for s in o.material_slots]))
        for s in o.material_slots: s.material = hm
    scn.render.resolution_x, scn.render.resolution_y = lw, lh; cy.samples = int(os.environ.get('LSPP', '16')); hq(False)
    t = time.time()
    for k in range(n):
        if kind == 'engine': F.pose(math.radians(k * 720.0 / n))
        else: F.rotor(math.radians(k * 120.0 / n))
        base = base0 + '_%03d' % k
        F.render(base, exr=False); zpass(base, {})
    print('LOOP %s %s %d cadre %.1fs' % (camn, kind, n, time.time() - t), flush=True)
    for o, mats in saved:
        if mats is None: o.hide_render = False
        else:
            for s, m in zip(o.material_slots, mats): s.material = m
    scn.render.resolution_x, scn.render.resolution_y = W, H

def orbit():
    ow, oh = int(os.environ.get('OW', '900')), int(os.environ.get('OH', '1600'))
    od = os.path.join(OUT, 'orbit'); os.makedirs(od, exist_ok=True)
    apply(S.STATES['solid'])
    scn.render.resolution_x, scn.render.resolution_y = ow, oh; cy.samples = int(os.environ.get('OSPP', '16')); hq(False)
    c = S.CAMS['heroB']
    ks = list(range(S.ORBIT_N))
    if os.environ.get('OREV'): ks.reverse()
    for k in ks:
        base = os.path.join(od, '%04d' % k)
        if os.path.exists(base + '.png'): continue
        u = k / (S.ORBIT_N - 1); e = u * u * (3 - 2 * u); e = 0.5 * u + 0.5 * e
        a = S.ORB_A0 + (S.ORB_A1 - S.ORB_A0) * e
        rig.aim(F.cam, tuple(S.orb(a, R=1640 - 80 * e)), tuple(c['tgt']), lens=c['lens'], fstop=c['fstop'], focus_mm=tuple(c['focus']))
        t = time.time(); F.render(base, exr=False)
        if k % 10 == 0: print('ORBIT %d %.1fs' % (k, time.time() - t), flush=True)
    scn.render.resolution_x, scn.render.resolution_y = W, H

if __name__ == '__main__':
    what = os.environ.get('WHAT', 'plates,loops,orbit').split(',')
    only = os.environ.get('ONLY', '')
    if 'plates' in what:
        for camn, stn in S.PLATES:
            if only and ('%s__%s' % (camn, stn)) not in only.split(','): continue
            plate(camn, stn)
    if 'loops' in what:
        for lp in S.LOOPS:
            if only and ('%s_%s' % (lp['cam'], lp['kind'])) not in only.split(','): continue
            loop(lp)
    if 'orbit' in what: orbit()
    print('DONE', flush=True)
