"""Timing belt drive (with tooth-accurate sliding via shape keys), coolant pump, tensioner, idler,
HP pump Bosch CP4.1-type (single plunger, double cam, roller tappet) and the vane oil pump with its chain."""
import math, bpy, bmesh
from mathutils import Vector, Matrix
from lib import *
from dims import *
import mats
from parts_core import sprocket, gear_profile, convex_hull

BELT_IN, BELT_OUT, BELT_TOOTH = 0.8, 1.7, 2.9     # pitch line -> land (inside), back (outside), tooth tip (inside)
K_KEYS = 8


# ======================================================================== belt path
def tangent(ca, ra, cb, rb):
    """signed radii (+ CCW around the pulley = pulley inside the loop). Returns (pa, pb, t)."""
    d = (cb[0] - ca[0], cb[1] - ca[1]); D = math.hypot(*d); phi = math.atan2(d[1], d[0])
    k = (ra - rb) / D
    best = None
    for sg in (1, -1):
        mu = phi + sg * math.acos(max(-1, min(1, k)))
        m = (math.cos(mu), math.sin(mu))
        pa = (ca[0] + ra * m[0], ca[1] + ra * m[1]); pb = (cb[0] + rb * m[0], cb[1] + rb * m[1])
        t = (-m[1], m[0])
        if (pb[0] - pa[0]) * t[0] + (pb[1] - pa[1]) * t[1] > 0:
            # right normal of t must be m: right normal = (t1, -t0)
            if abs(t[1] - m[0]) < 1e-6 and abs(-t[0] - m[1]) < 1e-6:
                best = (pa, pb, t)
    return best


def loop_path(pulleys, step=0.5):
    """pulleys: list of (centre(y,z), signed radius). Returns list of samples (pos(y,z), tangent) at ~step spacing and length."""
    n = len(pulleys)
    tans = [tangent(pulleys[i][0], pulleys[i][1], pulleys[(i + 1) % n][0], pulleys[(i + 1) % n][1]) for i in range(n)]
    segs = []   # ('L', p0, p1) or ('A', c, r, a0, a1, dir)
    for i in range(n):
        c, r = pulleys[i]
        pin = tans[(i - 1) % n][1]; pout = tans[i][0]
        a0 = math.atan2(pin[1] - c[1], pin[0] - c[0]); a1 = math.atan2(pout[1] - c[1], pout[0] - c[0])
        if r > 0:
            while a1 < a0: a1 += TAU
        else:
            while a1 > a0: a1 -= TAU
        segs.append(('A', c, abs(r), a0, a1))
        segs.append(('L', pout, tans[i][1]))
    total = 0.0
    for s in segs:
        total += abs(s[4] - s[3]) * s[2] if s[0] == 'A' else math.hypot(s[2][0] - s[1][0], s[2][1] - s[1][1])
    return segs, total


def path_eval(segs, total, u):
    """position (y,z) and unit tangent at arc length u (mod total)"""
    u = u % total
    for s in segs:
        if s[0] == 'A':
            L = abs(s[4] - s[3]) * s[2]
            if u <= L:
                a = s[3] + (s[4] - s[3]) * (u / L if L > 0 else 0)
                sg = 1 if s[4] > s[3] else -1
                p = (s[1][0] + s[2] * math.cos(a), s[1][1] + s[2] * math.sin(a))
                t = (-math.sin(a) * sg, math.cos(a) * sg)
                return p, t
            u -= L
        else:
            L = math.hypot(s[2][0] - s[1][0], s[2][1] - s[1][1])
            if u <= L:
                f = u / L
                p = (s[1][0] + (s[2][0] - s[1][0]) * f, s[1][1] + (s[2][1] - s[1][1]) * f)
                return p, ((s[2][0] - s[1][0]) / L, (s[2][1] - s[1][1]) / L)
            u -= L
    s = segs[-1]
    return s[2], (1, 0)


R_TENS, R_IDL = 29.0, 25.0


def belt_layout():
    rc, rk, rh, rw = N_CRANK * BELT_P / TAU, N_CAM * BELT_P / TAU, N_HPP * BELT_P / TAU, N_WP * BELT_P / TAU
    C, W, K, H = (0.0, 0.0), (Y_WP, Z_WP), (Y_CAM, Z_CAM), (Y_HPP, Z_HPP)
    I = (-76.0, 94.0)
    base = (-62.0, 312.0); dirv = (0.62, -0.785)     # tensioner slides towards the belt
    def build(s):
        T = (base[0] + dirv[0] * s, base[1] + dirv[1] * s)
        P = [(C, rc), (W, rw), (K, rk), (T, -(R_TENS + BELT_OUT)), (H, rh), (I, -(R_IDL + BELT_OUT))]
        segs, tot = loop_path(P)
        return P, segs, tot, T
    # choose an integer number of teeth near the nominal length, solve tensioner travel
    P, segs, tot, T = build(0.0)
    n_teeth = round(tot / BELT_P)
    target = n_teeth * BELT_P
    lo, hi = -25.0, 25.0
    f = lambda s: build(s)[2] - target
    flo, fhi = f(lo), f(hi)
    if flo * fhi > 0:
        n_teeth = round(build(0.0)[2] / BELT_P) - 1; target = n_teeth * BELT_P
    for _ in range(60):
        mid = (lo + hi) / 2
        if (f(lo) - 0) * (f(mid)) <= 0: hi = mid
        else: lo = mid
    P, segs, tot, T = build((lo + hi) / 2)
    return dict(P=P, segs=segs, total=tot, n=n_teeth, T=T, I=I)


def tooth_h(fr):
    """inner surface offset (negative = inside) along one pitch (fraction 0..1, tooth centred at 0.5)."""
    pts = [(0.0, -BELT_IN), (0.24, -BELT_IN), (0.32, -1.7), (0.38, -BELT_TOOTH + 0.25), (0.42, -BELT_TOOTH), (0.58, -BELT_TOOTH),
           (0.62, -BELT_TOOTH + 0.25), (0.68, -1.7), (0.76, -BELT_IN), (1.0, -BELT_IN)]
    for k in range(len(pts) - 1):
        if pts[k][0] <= fr <= pts[k + 1][0]:
            a, b = pts[k], pts[k + 1]
            return a[1] + (b[1] - a[1]) * (fr - a[0]) / (b[0] - a[0])
    return -BELT_IN


FR = [0.0, 0.12, 0.24, 0.32, 0.38, 0.42, 0.5, 0.58, 0.62, 0.68, 0.76, 0.88]


def belt_verts(lay, offset):
    segs, tot, n = lay['segs'], lay['total'], lay['n']
    pb = tot / n
    V = []
    hw = BELT_W / 2
    for k in range(n):
        for fr in FR:
            w = (k + fr) * pb
            (py, pz), (ty, tz) = path_eval(segs, tot, w + offset)
            my, mz = tz, -ty          # right normal = outward for the CCW loop
            hin = tooth_h(fr)
            for (xo, h) in ((-hw, hin), (hw, hin), (hw, BELT_OUT), (-hw, BELT_OUT)):
                V.append((X_BELT + xo, py + my * h, pz + mz * h))
    return V


def build_belt(lay):
    n = lay['n']; ns = n * len(FR)
    V0 = belt_verts(lay, 0.0)
    F = []
    for j in range(ns):
        j2 = (j + 1) % ns
        for c in range(4):
            c2 = (c + 1) % 4
            F.append([j * 4 + c, j2 * 4 + c, j2 * 4 + c2, j * 4 + c2])
    ob = mesh_obj('belt', V0, F, clean=False)
    me = ob.data
    for p in me.polygons: p.use_smooth = False
    ob.shape_key_add(name='Basis')
    pb = lay['total'] / n
    for k in range(1, K_KEYS):
        sk = ob.shape_key_add(name=f'o{k}')
        V = belt_verts(lay, pb * k / K_KEYS)
        for i, v in enumerate(V): sk.data[i].co = v
    set_mats(ob, mats.M['belt'])
    return ob


def belt_key_values(lay, s):
    """shape key values for a belt displacement s (mm)"""
    pb = lay['total'] / lay['n']
    q = (s % pb) / pb * K_KEYS
    k = int(math.floor(q)) % K_KEYS; f = q - math.floor(q)
    vals = [0.0] * K_KEYS          # index 0 = basis (offset 0)
    vals[k] += 1 - f; vals[(k + 1) % K_KEYS] += f
    return vals[1:]                # values for keys o1..o7 (basis implied)


def phase_for(lay, centre, r_abs, n_teeth):
    """pulley rotation (rad) at zero belt offset so that a groove sits under a belt tooth on the wrap."""
    segs, tot, n = lay['segs'], lay['total'], lay['n']
    pb = tot / n
    # find belt tooth (fraction 0.5) closest to the pulley
    best = (1e9, 0)
    for k in range(n):
        (py, pz), _ = path_eval(segs, tot, (k + 0.5) * pb)
        d = abs(math.hypot(py - centre[0], pz - centre[1]) - r_abs)
        if d < best[0]: best = (d, math.atan2(pz - centre[1], py - centre[0]))
    # sprocket teeth are centred at angle 0 (+Y) -> groove centred at half a pitch: rotate so a groove is at the tooth angle
    return best[1] - math.pi / n_teeth


def build_idlers(lay):
    M = mats.M
    T, I = lay['T'], lay['I']
    out = {}
    for name, c, r in (('tensioner', T, R_TENS), ('idler', I, R_IDL)):
        pr = revolve(name, [(6.0, X_BELT - 14.5), (r - 1.0, X_BELT - 14.5), (r, X_BELT - 13.5), (r, X_BELT + 13.5), (r - 1.0, X_BELT + 14.5),
                            (6.0, X_BELT + 14.5)], segs=96, axis='X')
        hub = revolve(name + 'h', [(6.0, X_BELT - 16), (14.0, X_BELT - 16), (14.0, X_BELT + 15), (6.0, X_BELT + 15)], segs=48, axis='X')
        holes = [cyl('ih', (X_BELT - 20, 0.6 * r * math.cos(a), 0.6 * r * math.sin(a)), (X_BELT + 20, 0.6 * r * math.cos(a), 0.6 * r * math.sin(a)), r * 0.16, segs=24)
                 for a in [TAU * k / 6 for k in range(6)]]
        bool_many(pr, holes)
        set_mats(pr, M['pulley']); set_mats(hub, M['steel'])
        ob = join([pr, hub], name)
        ob.location = (0, c[0], c[1])
        out[name] = ob
    # static parts: tensioner arm/base plate + bolts
    arm = rbox('tens_arm', -18, 18, -12, 12, X_BELT + 15, X_BELT + 22, 10)
    arm.data.transform(Matrix.Rotation(math.pi / 2, 4, 'Y'))
    arm.data.transform(Matrix.Translation((0, T[0], T[1])))
    set_mats(arm, M['iron'])
    out['tens_arm'] = arm
    return out


def build_wpump(lay):
    """coolant pump: pulley (rotating) + housing (static)."""
    M = mats.M
    rw = N_WP * BELT_P / TAU
    pul = sprocket('wp_pulley', N_WP, rw, X_BELT - 14.0, X_BELT + 14.0, depth=3.4, flange=[(X_BELT - 16, X_BELT - 14), (X_BELT + 14, X_BELT + 16)],
                   hub=(X_BELT - 18, X_BELT + 20, 15.0))
    set_mats(pul, M['steel'])
    hs = revolve('wp_house', [(10.0, X_BELT + 16), (24.0, X_BELT + 16), (32.0, X_BELT + 20), (36.0, X_BF - 0.5), (10.0, X_BF - 0.5)], segs=64, axis='X')
    hs.data.transform(Matrix.Translation((0, Y_WP, Z_WP)))
    set_mats(hs, M['alu'])
    return pul, hs


# ======================================================================== HP pump (CP4.1 type)
HP_R0, HP_RR, HP_H = 13.0, 7.0, 7.0      # cam base radius, roller radius, plunger stroke
HP_PL = 3.25                             # plunger radius (6.5 mm)
Z_BAR0, Z_BAR1 = 68.0, 96.0              # barrel (local z)
Z_CH_TOP = 90.0                          # pumping chamber top
HP_PHASE = 0.0


def hp_lift(beta):
    """plunger lift (mm) for pump shaft angle beta (rad); two strokes per revolution."""
    return HP_H * (1 - math.cos(2 * beta)) / 2


def hp_cam_profile(n_dir=360, n_s=720):
    pts = []
    for s in range(n_s):
        b = TAU * s / n_s
        d = HP_R0 + HP_RR + hp_lift(b)
        # roller centre fixed at +Z in the world; seen from the cam frame (rotated by -b)
        pts.append((d * math.sin(b), d * math.cos(b)))
    prof = []
    R2 = HP_RR ** 2
    for j in range(n_dir):
        psi = TAU * (j + 0.5) / n_dir
        ux, uy = math.cos(psi), math.sin(psi)
        best = 1e9
        for (cy_, cz_) in pts:
            proj = cy_ * ux + cz_ * uy
            if proj <= 0: continue
            perp2 = cy_ * cy_ + cz_ * cz_ - proj * proj
            if perp2 > R2: continue
            t = proj - math.sqrt(R2 - perp2)
            best = min(best, t)
        prof.append((best * ux, best * uy))
    return prof


def build_hp_pump():
    """returns dict of objects in WORLD coordinates (pump shaft at (Y_HPP, Z_HPP)); moving objects have origin set so that
    shaft rotates about X through its origin; tappet group translates in Z."""
    M = mats.M
    O = {}
    xc = X_HPC
    T = Matrix.Translation((0, Y_HPP, Z_HPP))
    # ---- shaft + cam + sprocket (rotating; origin on the shaft axis)
    sh = cyl('hp_shaft', (X_BELT - 18, 0, 0), (xc + 24, 0, 0), 9.5, segs=64)
    cam = extrude('hp_cam', hp_cam_profile(), xc - 7.0, xc + 7.0, 'YZ')
    spr = sprocket('hp_spr', N_HPP, N_HPP * BELT_P / TAU, X_BELT - 14.0, X_BELT + 14.0, depth=3.4,
                   flange=[(X_BELT - 16, X_BELT - 14), (X_BELT + 14, X_BELT + 16)], hub=(X_BELT - 18, X_BELT + 20, 16.0))
    shaft = union([sh, cam, spr], 'hp_shaft')
    set_mats(shaft, M['steel'])
    shaft.location = (0, Y_HPP, Z_HPP)
    O['shaft'] = shaft
    # ---- tappet group (roller + shoe + plunger + spring plate), local origin = roller centre at zero lift
    zr0 = HP_R0 + HP_RR
    rol = cyl('hp_roller', (xc - 6.0, 0, 0), (xc + 6.0, 0, 0), HP_RR, segs=64)
    axl = cyl('hp_axle', (xc - 8.5, 0, 0), (xc + 8.5, 0, 0), 2.8, segs=24)
    tap = revolve('hp_tappet', [(9.6, -3.0), (11.95, -3.0), (11.95, 16.0), (0.0, 16.0), (0.0, 9.0), (9.6, 9.0)], segs=64)
    tap.data.transform(Matrix.Translation((xc, 0, 0)))
    slot = box('slot', xc - 6.4, xc + 6.4, -12.5, 12.5, -4.0, 8.0)
    apply_bool(tap, slot); remove(slot)
    shoe = box('hp_shoe', xc - 8.6, xc + 8.6, -9.0, 9.0, -1.0, 9.0)
    rc = cyl('rc', (xc - 7.0, 0, 0), (xc + 7.0, 0, 0), HP_RR + 0.4, segs=48); apply_bool(shoe, rc); remove(rc)
    sl2 = box('sl2', xc - 6.3, xc + 6.3, -12, 12, -6, 3); apply_bool(shoe, sl2); remove(sl2)
    plg = cyl('hp_plunger', (xc, 0, 15.0), (xc, 0, 61.0), HP_PL, segs=40)
    plate = revolve('hp_splate', [(3.3, 16.0), (10.4, 16.0), (10.4, 17.6), (3.3, 17.6)], segs=48)
    plate.data.transform(Matrix.Translation((xc, 0, 0)))
    for o, mk in ((rol, 'steel'), (axl, 'steel'), (tap, 'steel'), (shoe, 'follower'), (plg, 'steel'), (plate, 'steel')):
        set_mats(o, M[mk])
    tg = join([rol, axl, tap, shoe, plg, plate], 'hp_tappet')
    tg.location = (0, Y_HPP, Z_HPP + zr0)
    O['tappet'] = tg
    # ---- plunger spring: hangs from the barrel bottom (object origin), compressed by scaling Z
    z_plate0 = zr0 + 17.6
    Lf = Z_BAR0 - z_plate0
    hv, hf = helix_verts(-Lf, 0.0, 8.6, 1.7, 6.5)
    spv = mesh_obj('hp_spring', hv, hf, clean=True)
    set_mats(spv, M['spring'])
    spv.location = (xc, Y_HPP, Z_HPP + Z_BAR0)
    spv['Lf'] = Lf
    O['spring'] = spv
    # ---- housing (aluminium): shaft body + tappet tower + front flange
    body = cyl('hp_body', (X_BF - 0.5, 0, 0), (xc + 26.0, 0, 0), 29.0, segs=96)
    tw = rbox('hp_tower', xc - 17.0, xc + 17.0, -19.0, 19.0, 0.0, Z_BAR0, 6.0)
    fl = extrude('hp_flange', rounded_rect(-40.0, 40.0, -38.0, 38.0, 8.0), X_BF - 0.5, X_BF + 7.5, 'YZ')
    br = box('hp_bracket', X_BF - 0.5, X_BF + 7.5, 0.0, Y_HPP * -1 - 72.0, -45.0, 40.0)   # plate towards the block side
    hous = union([body, tw, fl, br], 'hp_housing')
    bevel(hous, 1.5, 2, 35)
    cuts = [cyl('camch', (xc - 9.5, 0, 0), (xc + 9.5, 0, 0), 24.5, segs=96),
            cyl('tbore', (xc, 0, 10.0), (xc, 0, Z_BAR0 + 1), 12.2, segs=64),
            cyl('sbore', (X_BF - 5, 0, 0), (xc + 20, 0, 0), 9.7, segs=48)]
    for a in (0.6, 2.2, 3.8, 5.4):
        cuts.append(cyl('fh', (X_BF - 2, 31 * math.cos(a), 31 * math.sin(a)), (X_BF + 10, 31 * math.cos(a), 31 * math.sin(a)), 4.2, segs=20))
    bool_many(hous, cuts)
    # metering unit boss (side, -Y) + inlet nipple
    set_mats(hous, M['alu'])
    hous.data.transform(T)
    O['housing'] = hous
    # ---- barrel / pump head (steel) with pumping chamber, inlet valve (top) and outlet valve (+Y)
    bar = rbox('hp_barrel', xc - 15.0, xc + 15.0, -15.0, 15.0, Z_BAR0, Z_BAR1, 5.0)
    bevel(bar, 1.2, 2, 35)
    outb = cyl('outb', (xc, 0, 84.0), (xc, 27.0, 84.0), 7.5, segs=48)
    inb = cyl('inb', (xc, 0, Z_BAR1), (xc, 0, Z_BAR1 + 9.0), 9.0, segs=48)
    bar = union([bar, outb, inb], 'hp_barrel')
    cuts = [cyl('pb', (xc, 0, Z_BAR0 - 1), (xc, 0, Z_CH_TOP), HP_PL + 0.03, segs=40),
            cyl('ich', (xc, 0, Z_CH_TOP), (xc, 0, Z_CH_TOP + 3.0), 4.2, segs=40),      # inlet valve chamber
            cyl('ich2', (xc, 0, Z_CH_TOP + 3.0), (xc, 0, Z_BAR1 + 9.5), 1.8, segs=24),
            cyl('och', (xc, 0, 84.0), (xc, 6.0, 84.0), 1.2, segs=20),
            cyl('ovb', (xc, 6.0, 84.0), (xc, 14.0, 84.0), 2.6, segs=24),
            cyl('oout', (xc, 14.0, 84.0), (xc, 28.0, 84.0), 1.3, segs=20)]
    bool_many(bar, cuts)
    set_mats(bar, M['steel'])
    bar.data.transform(T)
    O['barrel'] = bar
    # outlet fitting (hex) + inlet valve parts + outlet ball
    of = hexnut('hp_ofit', (xc, 27.0, 84.0), (xc, 38.0, 84.0), 17.0); of.data.transform(T); set_mats(of, M['steel'])
    O['ofit'] = of
    ball = sphere('hp_ball', (xc, 8.4, 84.0), 2.0, 24, 12); set_mats(ball, M['steel'])
    ball.data.transform(Matrix.Translation((-xc, -8.4, -84.0)))
    ball.location = (xc, Y_HPP + 8.4, Z_HPP + 84.0)
    O['ball'] = ball
    ivd = revolve('hp_inlet_valve', [(0.0, 0.0), (3.9, 0.0), (3.9, 0.9), (1.2, 0.9), (1.2, 5.0), (0.0, 5.0)], segs=40)
    set_mats(ivd, M['steel'])
    ivd.location = (xc, Y_HPP, Z_HPP + Z_CH_TOP + 0.2)
    O['ivalve'] = ivd
    # metering unit (solenoid) on the -Y side + connector + LP inlet
    mu = cyl('hp_meun', (xc, -19.0, 46.0), (xc, -40.0, 46.0), 11.0, segs=48)
    mu2 = cyl('mu2', (xc, -40.0, 46.0), (xc, -44.0, 46.0), 8.0, segs=40)
    muc = box('muc', xc - 6, xc + 6, -42, -30, 55, 68); bevel(muc, 1.0, 2, 35)
    meun = union([mu, mu2], 'hp_meun'); set_mats(meun, M['steel'])
    set_mats(muc, M['plastic'])
    meun = join([meun, muc], 'hp_meun'); meun.data.transform(T)
    O['meun'] = meun
    nip = cyl('hp_nip', (xc + 18.0, -10.0, 30.0), (xc + 18.0, -30.0, 30.0), 4.5, segs=32)
    nip.data.transform(T); set_mats(nip, M['steel']); O['nipple'] = nip
    # ---- fuel volumes
    fl_ch = cyl('hpf_chamber', (xc + 0.2, 0, 0), (xc + 9.3, 0, 0), 24.3, segs=96)        # cam chamber (LP)
    ct = cyl('ct', (xc - 1, 0, 0), (xc + 10, 0, 0), 9.6, segs=48); apply_bool(fl_ch, ct); remove(ct)
    tb = cyl('hpf_tb', (xc, 0, 10.2), (xc, 0, Z_BAR0 + 0.5), 12.1, segs=64)
    lp = union([fl_ch, tb], 'hp_fuel_lp')
    lp.data.transform(T); set_mats(lp, M['fuel_lp']); O['fuel_lp'] = lp
    # pumping chamber column (scaled in z): unit height, top fixed at chamber top
    pc = cyl('hp_fuel_ch', (xc, 0, -1.0), (xc, 0, 0.0), HP_PL - 0.02, segs=40)
    pc.location = (0, Y_HPP, Z_HPP + Z_CH_TOP)
    set_mats(pc, M['fuel_var']); O['fuel_ch'] = pc
    hp_out = union([cyl('o1', (xc, 0, 84.0), (xc, 6.0, 84.0), 1.15, segs=20), cyl('o2', (xc, 6.0, 84.0), (xc, 14.0, 84.0), 2.55, segs=24),
                    cyl('o3', (xc, 14.0, 84.0), (xc, 28.0, 84.0), 1.25, segs=20)], 'hp_fuel_hp')
    hp_out.data.transform(T); set_mats(hp_out, M['fuel_hp']); O['fuel_hp'] = hp_out
    lp_in = union([cyl('i1', (xc, 0, Z_CH_TOP + 0.1), (xc, 0, Z_CH_TOP + 2.9), 4.15, segs=40),
                   cyl('i2', (xc, 0, Z_CH_TOP + 2.9), (xc, 0, Z_BAR1 + 9.4), 1.75, segs=24)], 'hp_fuel_in')
    lp_in.data.transform(T); set_mats(lp_in, M['fuel_lp']); O['fuel_in'] = lp_in
    return O


def hexnut(name, p0, p1, af):
    p0, p1 = Vector(p0), Vector(p1)
    u, v, d = frame_of(p1 - p0)
    R = af / 2 / math.cos(math.pi / 6)
    verts = []
    for p in (p0, p1):
        for k in range(6):
            a = k * math.pi / 3 + math.pi / 6
            verts.append(tuple(p + (u * math.cos(a) + v * math.sin(a)) * R))
    verts.append(tuple(p0)); verts.append(tuple(p1))
    faces = []
    for k in range(6):
        k2 = (k + 1) % 6
        faces.append([k, k2, 6 + k2, 6 + k]); faces.append([12, k2, k]); faces.append([13, 6 + k, 6 + k2])
    ob = mesh_obj(name, verts, faces)
    bevel(ob, 0.6, 1, 35)
    return ob


def build_hp_line():
    """pump outlet -> rail inlet boss."""
    p0 = (X_HPC, Y_HPP + 38.0, Z_HPP + 84.0)
    pts = fillet_path([p0, (X_HPC, Y_HPP + 48.0, Z_HPP + 84.0), (X_HPC, -88.0, Z_HPP + 110.0), (X_HPC, -88.0, Z_RAIL), (-178.0, -50.0, Z_RAIL),
                       (-178.0, -R_RAIL - 12.0, Z_RAIL)], 12.0, n=10)
    t = tube('hp_pipe', pts, 3.0, segs=20)
    n = hexnut('hpn', (-178.0, -R_RAIL - 21.0, Z_RAIL), (-178.0, -R_RAIL - 9.0, Z_RAIL), 17.0)
    set_mats(t, mats.M['line']); set_mats(n, mats.M['steel'])
    return join([t, n], 'hp_pipe')


# ======================================================================== oil pump (vane type) + chain
OP_RR = 17.0          # rotor radius
OP_RING = 23.5        # stator ring inner radius
OP_E = 3.5            # eccentricity (+Y)
OP_NV = 7
OP_VL = 10.0          # vane radial length
OP_VT = 2.8           # vane thickness
OP_W = 14.0           # rotor width (x)
OP_HR = 34.0          # housing radius


def vane_tip(psi):
    """distance from rotor centre to the ring along direction psi"""
    ey, ez = OP_E, 0.0
    uy, uz = math.cos(psi), math.sin(psi)
    b = ey * uy + ez * uz
    return b + math.sqrt(OP_RING ** 2 - (ey * ey + ez * ez - b * b))


def pickup_profile(z_in, Zp, ro=9.0, rb=30.0, th=1.6):
    """(r, z) profiles of the oil pick-up: wall (neck + bell), screen, oil inside. Neck top at the boss underside z_in."""
    zt, zn = z_in, z_in - 2.0            # neck top / neck bottom (outer)
    zs, zr = Zp + 10.0, Zp + 6.0         # bell shoulder (outer) / rim bottom
    dr, dz = rb - ro, zs - zn
    L = math.hypot(dr, dz)
    nr, nz = -dz / L, dr / L             # outward normal of the bell top
    pr, pz = ro - th * nr, zn - th * nz  # a point of the inner top surface
    zi = lambda r: pz + (r - pr) * dz / dr
    wall = [(ro - th, zt), (ro, zt), (ro, zn), (rb, zs), (rb, zr), (rb - th, zr), (rb - th, zi(rb - th)), (ro - th, zi(ro - th))]
    screen = [(0.0, zr + 0.2), (rb - th + 0.2, zr + 0.2), (rb - th + 0.2, zr + 1.0), (0.0, zr + 1.0)]
    g = 0.2
    oil = [(0.0, zt - 0.2), (ro - th - g, zt - 0.2), (ro - th - g, zi(ro - th - g) - 0.3), (rb - th - g, zi(rb - th - g) - 0.3),
           (rb - th - g, zr + 1.2), (0.0, zr + 1.2)]
    return dict(wall=wall, screen=screen, oil=oil)


def build_oil_pump():
    M = mats.M
    O = {}
    xr = X_OPR
    T = Matrix.Translation((0, 0, Z_OP))
    # rotor + shaft + sprocket (rotating, origin on the shaft axis)
    rot = cyl('op_rotor', (xr - OP_W / 2, 0, 0), (xr + OP_W / 2, 0, 0), OP_RR, segs=96)
    slots = []
    for k in range(OP_NV):
        a = TAU * k / OP_NV
        sl = box('sl', xr - OP_W, xr + OP_W, -OP_VT / 2 - 0.1, OP_VT / 2 + 0.1, OP_RR - OP_VL - 0.5, OP_RR + 5)
        sl.data.transform(Matrix.Rotation(a - math.pi / 2, 4, 'X'))
        slots.append(sl)
    bool_many(rot, slots)
    shf = cyl('op_shaft', (X_CHAIN - 7.0, 0, 0), (xr + OP_W / 2 + 6.0, 0, 0), 7.0, segs=48)
    spr = sprocket('op_spr', N_CHS, N_CHS * CHAIN_P / TAU, X_CHAIN - 3.5, X_CHAIN + 3.5, depth=4.6, hub=(X_CHAIN - 7.5, X_CHAIN + 6, 12.0))
    rotor = union([rot, shf, spr], 'op_rotor')
    set_mats(rotor, M['steel'])
    rotor.location = (0, 0, Z_OP)
    O['rotor'] = rotor
    vanes = []
    for k in range(OP_NV):
        v = box(f'op_vane{k}', xr - OP_W / 2 + 0.3, xr + OP_W / 2 - 0.3, -OP_VT / 2, OP_VT / 2, -OP_VL, 0.0)
        bevel(v, 0.35, 1, 35)
        set_mats(v, M['follower'])
        vanes.append(v)
    O['vanes'] = vanes
    # housing (body + mounting ears), eccentric ring bore, shaft bore, inlet (down), outlet (up-left)
    body = cyl('op_body', (X_CHAIN + 6.5, 0, 0), (xr + OP_W / 2 + 9.0, 0, 0), OP_HR, segs=96)
    ears = box('ears', X_CHAIN + 6.5, xr + OP_W / 2 + 9.0, -44, 44, -8, 8)
    boss_i = cyl('bi', (xr, -6.0, -20.0), (xr, -6.0, -OP_HR - 6.0), 10.5, segs=48)
    boss_o = cyl('bo', (xr, -12.0, 14.0), (xr, -34.0, 30.0), 9.0, segs=48)
    hous = union([body, ears, boss_i, boss_o], 'op_housing')
    bevel(hous, 1.2, 2, 35)
    cuts = [cyl('ring', (xr - OP_W / 2 - 0.2, OP_E, 0), (xr + OP_W / 2 + 0.2, OP_E, 0), OP_RING, segs=128),
            cyl('sb', (X_CHAIN, 0, 0), (xr + OP_W / 2 + 4, 0, 0), 7.3, segs=48),
            cyl('inl', (xr, -6.0, -12.0), (xr, -6.0, -OP_HR - 8.0), 7.2, segs=48),
            cyl('outl', (xr, -8.0, 12.0), (xr, -36.0, 31.0), 6.0, segs=48)]
    cuts += [cyl('ob', (X_CHAIN + 4, 38 * s, 0), (xr + OP_W / 2 + 12, 38 * s, 0), 3.0, segs=20) for s in (-1, 1)]
    bool_many(hous, cuts)
    for s in (-1, 1):
        bh = cyl('obh', (X_CHAIN + 6.5, 38 * s, 0), (X_CHAIN + 1.5, 38 * s, 0), 6.0, segs=6, phase=0.0)
        apply_bool(hous, bh, 'UNION'); remove(bh)
    set_mats(hous, M['alu'])
    hous.data.transform(T)
    O['housing'] = hous
    # pick-up (sorb): short neck under the inlet boss, flat bell, mesh screen (world coordinates).
    # The profile must not cross itself (the old one did, which broke the section cut).
    z_in = Z_OP - OP_HR - 6.0            # underside of the inlet boss
    Zp = Z_PANB
    PK = pickup_profile(z_in, Zp)
    pin = revolve('op_pickup', PK['wall'], segs=64)
    scr = revolve('op_screen', PK['screen'], segs=64)
    pin = union([pin, scr], 'op_pickup')
    pin.data.transform(Matrix.Translation((xr + 0.02, -6.0, 0)))      # axis 0.02 mm off the section plane
    set_mats(pin, M['pan'])
    O['pickup'] = pin
    # outlet pipe: from the housing up the crankcase side wall to the main gallery
    po = fillet_path([(xr, -34.0, Z_OP + 31.0), (xr, -66.0, Z_OP + 52.0), (xr, -86.0, Z_OP + 60.0), (xr, -86.0, 30.0)], 12.0)
    op = tube('op_outpipe', po, 8.0, segs=32)
    poe = [Vector(po[0]) + (Vector(po[0]) - Vector(po[1])).normalized() * 1.0] + [Vector(p) for p in po] + [Vector(po[-1]) + (Vector(po[-1]) - Vector(po[-2])).normalized() * 1.0]
    oin = tube('opin', poe, 6.4, segs=24)
    apply_bool(op, oin); remove(oin)
    set_mats(op, M['steel'])
    O['outpipe'] = op
    # ---- oil volumes: crescent split into suction (bottom, p=0) and pressure (top, p=1) halves
    cres = cyl('cres', (xr - OP_W / 2 + 0.2, OP_E, 0), (xr + OP_W / 2 - 0.2, OP_E, 0), OP_RING - 0.1, segs=128)
    rc = cyl('rc', (xr - OP_W, 0, 0), (xr + OP_W, 0, 0), OP_RR + 0.1, segs=96); apply_bool(cres, rc); remove(rc)
    top = dup(cres, 'op_oil_p')
    c1 = box('cl', xr - 50, xr + 50, -60, 60, -60, 0.0); apply_bool(top, c1); remove(c1)
    c2 = box('ch', xr - 50, xr + 50, -60, 60, 0.0, 60); apply_bool(cres, c2); remove(c2)
    suc = union([cres, cyl('ins', (xr, -6.0, -12.0), (xr, -6.0, -OP_HR - 7.8), 7.0, segs=40)], 'op_oil_s')
    ous = union([top, cyl('ous', (xr, -8.0, 12.0), (xr, -35.5, 30.7), 5.8, segs=40)], 'op_oil_p')
    suc.data.transform(T); ous.data.transform(T)
    pick = revolve('op_oil_pick', PK['oil'], segs=64)                  # the bell is under the oil level: full of oil
    pick.data.transform(Matrix.Translation((xr + 0.02, -6.0, 0)))
    suc = union([suc, pick], 'op_oil_s')
    pipe_oil = tube('op_oil_pipe', po, 6.2, segs=24)
    ous = union([ous, pipe_oil], 'op_oil_p')
    set_mats(suc, M['oil']); set_mats(ous, M['oil'])
    O['oil_s'] = suc; O['oil_p'] = ous
    return O


# ---------------------------------------------------------------- chain (crank sprocket z=0 -> pump sprocket z=Z_OP), shape-key sliding
def chain_layout():
    r = N_CHS * CHAIN_P / TAU
    P = [((0.0, 0.0), r), ((0.0, Z_OP), r)]
    segs, tot = loop_path(P)
    n = round(tot / CHAIN_P)
    return dict(segs=segs, total=tot, n=n, r=r)


def chain_verts(lay, offset):
    segs, tot, n = lay['segs'], lay['total'], lay['n']
    pc = tot / n
    piv = []
    for k in range(n):
        (py, pz), _ = path_eval(segs, tot, k * pc + offset)
        piv.append((py, pz))
    V = []
    rr = 2.6
    for k in range(n):
        a = piv[k]; b = piv[(k + 1) % n]
        # roller (12-gon) at a
        for j in range(12):
            t = TAU * j / 12
            for x in (X_CHAIN - 3.4, X_CHAIN + 3.4):
                V.append((x, a[0] + rr * math.cos(t), a[1] + rr * math.sin(t)))
        # two side plates (boxes) a->b
        dy, dz = b[0] - a[0], b[1] - a[1]; L = math.hypot(dy, dz) or 1.0
        ty, tz = dy / L, dz / L; ny, nz = -tz, ty
        hw = 3.2
        for xs in ((X_CHAIN - 5.0, X_CHAIN - 3.6), (X_CHAIN + 3.6, X_CHAIN + 5.0)):
            for x in xs:
                for (s, h) in ((-3.0, -hw), (L + 3.0, -hw), (L + 3.0, hw), (-3.0, hw)):
                    V.append((x, a[0] + ty * s + ny * h, a[1] + tz * s + nz * h))
    return V


def chain_faces(n):
    F = []
    per = 24 + 16
    for k in range(n):
        b = k * per
        for j in range(12):
            j2 = (j + 1) % 12
            F.append([b + j * 2, b + j2 * 2, b + j2 * 2 + 1, b + j * 2 + 1])
        F.append([b + j * 2 for j in range(12)][::-1]); F.append([b + j * 2 + 1 for j in range(12)])
        for pl in range(2):
            c = b + 24 + pl * 8
            v0 = [c + 0, c + 1, c + 2, c + 3]; v1 = [c + 4, c + 5, c + 6, c + 7]
            F.append(v0[::-1]); F.append(v1)
            for q in range(4):
                q2 = (q + 1) % 4
                F.append([v0[q], v0[q2], v1[q2], v1[q]])
    return F


def build_chain(lay):
    V0 = chain_verts(lay, 0.0)
    ob = mesh_obj('chain', V0, chain_faces(lay['n']), clean=False)
    ob.shape_key_add(name='Basis')
    pc = lay['total'] / lay['n']
    for k in range(1, K_KEYS):
        sk = ob.shape_key_add(name=f'o{k}')
        for i, v in enumerate(chain_verts(lay, pc * k / K_KEYS)): sk.data[i].co = v
    set_mats(ob, mats.M['steel'])
    return ob


def chain_key_values(lay, s):
    pc = lay['total'] / lay['n']
    q = (s % pc) / pc * K_KEYS
    k = int(math.floor(q)) % K_KEYS; f = q - math.floor(q)
    vals = [0.0] * K_KEYS
    vals[k] += 1 - f; vals[(k + 1) % K_KEYS] += f
    return vals[1:]
