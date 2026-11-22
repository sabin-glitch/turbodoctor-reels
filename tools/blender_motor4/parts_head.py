"""Cylinder head, valvetrain (roller finger followers + HLA), camshafts with envelope-generated lobes, cover."""
import math, bpy
from mathutils import Vector, Matrix
from lib import *
from dims import *
import mats
from parts_core import sprocket, gear_profile

L_PAD = Y_HLA - VY      # 46: pivot -> valve contact
L_ROL = Y_HLA - Y_CAM   # 26: pivot -> roller
H_ROL = Z_ROLL - Z_PIV  # 5.5


def valves():
    """(i, kind, x, y) for every valve"""
    out = []
    for i, cx in enumerate(CX):
        for sx in (-1, 1):
            out.append((i, 'I', cx + sx * VX, -VY))
            out.append((i, 'E', cx + sx * VX, VY))
    return out


def port_path(x, sy):
    """centre line from the valve seat up and out to the side face (sy=-1 intake, +1 exhaust)"""
    return bezier((x, sy * VY, Z_VFACE - 1.0), (x, sy * VY, Z_HD + 26.0), (x, sy * (VY + 16), Z_HD + 38.0), (x, sy * (Y_H + 3.0), Z_HD + 40.0), n=28)


def port_radii(n, r0=11.2, r1=10.0, r2=11.5):
    out = []
    for k in range(n + 1):
        t = k / n
        out.append(r0 + (r1 - r0) * min(1, t / 0.45) if t < 0.45 else r1 + (r2 - r1) * (t - 0.45) / 0.55)
    return out


def gp_point(d):
    return Vector((GP_TIP[0], GP_TIP[1], GP_TIP[2])) + Vector(GP_DIR) * d


# ======================================================================== head
def build_head():
    h = rbox('head', X_HF, X_HR, -Y_H, Y_H, Z_HD, Z_CAM, 9.0)
    bevel(h, 2.0, 2, 35)
    ch = rbox('vch', X_HF + 7, X_HR - 7, -Y_H + 6, Y_H - 6, Z_SSEAT, Z_CAM + 6, 6.0)
    apply_bool(h, ch); remove(ch)
    # bosses inside the valve chamber
    bos = []
    for (i, kind, x, y) in valves():
        sy = -1 if kind == 'I' else 1
        bos.append(cyl('gb', (x, y, Z_SSEAT - 2), (x, y, Z_SSEAT), 9.0, segs=48))
        bos.append(cyl('hlab', (x, sy * Y_HLA, Z_SSEAT - 2), (x, sy * Y_HLA, Z_PIV - 7.0), 9.5, segs=48))
    for i, cx in enumerate(CX):
        bos.append(cyl('injb', (cx, 0, Z_SSEAT - 2), (cx, 0, Z_TIP + 61.0), 13.5, segs=64))
        p0, p1 = gp_point(20.0), gp_point(54.0)
        bos.append(cyl('gpb', p0, p1, 9.0, segs=48))
    for m in (MAINS[1], MAINS[3]):   # injector clamp bolt bosses
        bos.append(cyl('clb', (m, 0, Z_SSEAT - 2), (m, 0, Z_TIP + 62.6), 8.0, segs=40))
    for m in MAINS:
        for sy in (-1, 1):
            bos.append(box('tower', m - 10, m + 10, min(sy * 20, sy * 54), max(sy * 20, sy * 54), Z_SSEAT - 2, Z_CAM))
    hb = union(bos, 'bosses')
    apply_bool(h, hb, 'UNION'); remove(hb)
    # water jacket core: slab minus inflated obstacles
    jk = box('jk', X_HF + 9, X_HR - 9, -Y_H + 8, Y_H - 8, Z_HD + 9.0, Z_SSEAT - 8.0)
    obst = []
    for (i, kind, x, y) in valves():
        sy = -1 if kind == 'I' else 1
        pp = port_path(x, sy)
        obst.append(tube('po', pp, [r + 3.5 for r in port_radii(len(pp) - 1)], segs=32))
        obst.append(cyl('gbo', (x, y, Z_HD), (x, y, Z_SSEAT), 9.0, segs=32))
    for i, cx in enumerate(CX):
        obst.append(cyl('injo', (cx, 0, Z_HD - 1), (cx, 0, Z_SSEAT), 13.5, segs=48))
        obst.append(cyl('gpo', gp_point(-2), gp_point(60), 9.0, segs=32))
    for m in MAINS:
        for sy in (-1, 1):
            obst.append(cyl('bo', (m, sy * 63, Z_HD - 1), (m, sy * 63, Z_SSEAT), 10.5, segs=32))
    ob = union(obst, 'obst')
    apply_bool(jk, ob); remove(ob)
    apply_bool(h, jk); remove(jk)
    # cavities: ports, seat pockets, guide bores, injector wells, glow plug wells, HLA bores, cam journal bores, bolt holes, gear chamber
    cut = []
    for (i, kind, x, y) in valves():
        sy = -1 if kind == 'I' else 1
        rv = R_VI if kind == 'I' else R_VE
        pp = port_path(x, sy)
        cut.append(tube('port', pp, port_radii(len(pp) - 1), segs=40))
        cut.append(cyl('pocket', (x, y, Z_HD - 1), (x, y, Z_HD + 7.0), rv + 1.6, segs=64))
        cut.append(cyl('gbore', (x, y, Z_HD + 20), (x, y, Z_SSEAT + 1), 6.0, segs=32))
        cut.append(cyl('hla', (x, sy * Y_HLA, Z_PIV - 30), (x, sy * Y_HLA, Z_CAM), 6.6, segs=32))
    for i, cx in enumerate(CX):
        cut.append(cyl('w1', (cx, 0, Z_HD - 1), (cx, 0, Z_TIP + 22.2), 4.4, segs=40))
        cut.append(cyl('w2', (cx, 0, Z_TIP + 22.2), (cx, 0, Z_TIP + 24.2), 7.0, segs=48))
        cut.append(cyl('w3', (cx, 0, Z_TIP + 24.2), (cx, 0, Z_CAM + 10), 9.6, segs=64))
        cut.append(cyl('g1', gp_point(-3), gp_point(28.5), 2.7, segs=32))
        cut.append(cyl('g2', gp_point(28.0), gp_point(55.0), 5.2, segs=40))
        cut.append(cyl('g3', gp_point(54.5), gp_point(95.0), 7.6, segs=40))
    for sy in (-1, 1):
        cut.append(cyl('jbore', (X_HF - 5, sy * Y_CAM, Z_CAM), (X_HR + 5, sy * Y_CAM, Z_CAM), R_JOUR + 0.15, segs=64))
    for m in MAINS:
        for sy in (-1, 1):
            cut.append(cyl('bh', (m, sy * 63, Z_HD - 1), (m, sy * 63, Z_SSEAT + 1), 6.2, segs=24))
            cut.append(cyl('bcb', (m, sy * 63, Z_SSEAT - 3.0), (m, sy * 63, Z_SSEAT + 1), 9.2, segs=32))
    cut.append(box('gearch', X_GEAR - 9, X_GEAR + 9, -62, 62, Z_CAM - 45, Z_CAM + 6))
    cut.append(cyl('camseal', (X_HF - 5, Y_CAM, Z_CAM), (X_GEAR, Y_CAM, Z_CAM), 16.5, segs=48))
    cu = union(cut, 'cuts')
    apply_bool(h, cu); remove(cu)
    return h


def build_seats_guides():
    seats, guides, seals, washers = [], [], [], []
    for (i, kind, x, y) in valves():
        rv = R_VI if kind == 'I' else R_VE
        # seat insert: ring with a 45 deg face matching the valve
        prof = [(rv - 2.7, Z_HD + 7.0), (rv + 1.6, Z_HD + 7.0), (rv + 1.6, Z_HD), (rv + 0.4, Z_HD), (rv + 0.05, Z_VFACE + 1.45 + 0.05),
                (rv - 2.55, Z_VFACE + 4.05), (rv - 2.7, Z_VFACE + 4.4)]
        s = revolve(f'seat_{kind}{i}_{x:.0f}', prof, segs=64); s.data.transform(Matrix.Translation((x, y, 0)))
        seats.append(s)
        g = revolve(f'guide_{kind}{i}_{x:.0f}', [(R_STEM + 0.05, Z_HD + 24.0), (5.9, Z_HD + 24.0), (5.9, Z_SSEAT + 10.0), (R_STEM + 0.05, Z_SSEAT + 10.0)], segs=40)
        g.data.transform(Matrix.Translation((x, y, 0))); guides.append(g)
        sl = revolve(f'seal_{kind}{i}_{x:.0f}', [(R_STEM + 0.05, Z_SSEAT + 9.0), (6.6, Z_SSEAT + 9.0), (6.6, Z_SSEAT + 15.0), (5.0, Z_SSEAT + 17.5), (R_STEM + 0.05, Z_SSEAT + 17.5)], segs=40)
        sl.data.transform(Matrix.Translation((x, y, 0))); seals.append(sl)
        w = revolve(f'swash_{kind}{i}_{x:.0f}', [(6.2, Z_SSEAT), (13.2, Z_SSEAT), (13.2, Z_SSEAT + 1.2), (6.2, Z_SSEAT + 1.2)], segs=48)
        w.data.transform(Matrix.Translation((x, y, 0))); washers.append(w)
    return seats, guides, seals, washers


def build_valve(name, kind):
    """local: valve face centre at origin, stem along +Z; includes retainer + keepers."""
    R = R_VI if kind == 'I' else R_VE
    prof = [(0.0, 0.0), (R - 0.5, 0.0), (R, 0.5), (R, 1.45), (R - 2.6, 4.05), (R - 4.6, 5.2), (7.0, 7.4), (4.6, 11.0), (3.6, 15.0),
            (R_STEM, 21.0), (R_STEM, V_LEN - 8.6), (R_STEM - 0.55, V_LEN - 8.1), (R_STEM - 0.55, V_LEN - 6.9), (R_STEM, V_LEN - 6.4),
            (R_STEM, V_LEN - 5.6), (R_STEM - 0.55, V_LEN - 5.1), (R_STEM - 0.55, V_LEN - 3.9), (R_STEM, V_LEN - 3.4),
            (R_STEM, V_LEN - 0.5), (R_STEM - 0.5, V_LEN), (0.0, V_LEN)]
    v = revolve(name, prof, segs=48)
    # heat tint on the exhaust valve head
    if kind == 'E':
        set_mats(v, mats.M['valve'], extra=[(mats.M['valve_hot'], lambda p: p.center.z < 9.0)])
    else:
        set_mats(v, mats.M['valve'])
    zr = Z_RET - Z_VFACE
    ret = revolve(name + '_ret', [(5.4, zr), (13.4, zr), (13.4, zr + 1.6), (11.0, zr + 2.6), (7.2, zr + 5.6), (5.4, zr + 5.6)], segs=48)
    kp = revolve(name + '_kp', [(R_STEM - 0.5, zr + 0.6), (5.35, zr + 0.6), (7.1, zr + 5.8), (R_STEM - 0.5, zr + 5.8)], segs=40)
    set_mats(ret, mats.M['steel']); set_mats(kp, mats.M['bolt'])
    return join([v, ret, kp], name)


def build_follower(name):
    """exhaust-side canonical follower (pivot at origin, valve pad toward -Y). Mirror for intake."""
    side = [(7.5, -3.0), (6.5, 3.5), (2.0, 6.0), (-14.0, 7.5), (-20.0, 11.5), (-32.0, 11.5), (-38.0, 6.5), (-49.0, 4.2), (-51.5, 1.0),
            (-50.5, -3.8), (-41.0, -4.8), (-26.0, -5.5), (-8.0, -6.2), (3.0, -6.8)]
    plates = []
    for sx in (-1, 1):
        pl = extrude(name + 'pl', side, sx * 4.4, sx * 6.2, 'YZ')
        plates.append(pl)
    pad = extrude(name + 'pad', [(-51.0, -2.7), (-40.0, -2.7), (-40.0, 1.5), (-51.0, 1.5)], -6.2, 6.2, 'YZ')
    sock = extrude(name + 'sock', [(-6.0, -6.6), (7.0, -6.6), (7.0, 3.0), (-6.0, 3.0)], -6.2, 6.2, 'YZ')
    body = union(plates + [pad, sock], name)
    bevel(body, 0.8, 2, 35)
    cup = sphere(name + 'cup', (0, 0, 0), 4.1, 32, 16); apply_bool(body, cup); remove(cup)
    set_mats(body, mats.M['follower'])
    roller = cyl(name + 'rl', (-4.2, -L_ROL, H_ROL), (4.2, -L_ROL, H_ROL), R_ROLL, segs=64)
    set_mats(roller, mats.M['steel'])
    axle = cyl(name + 'ax', (-6.6, -L_ROL, H_ROL), (6.6, -L_ROL, H_ROL), 2.6, segs=24)
    set_mats(axle, mats.M['steel'])
    return join([body, roller, axle], name)


def build_hla(name):
    b = revolve(name, [(0.0, Z_PIV - 30.0), (6.5, Z_PIV - 30.0), (6.5, Z_PIV - 6.0), (5.0, Z_PIV - 5.0), (3.2, Z_PIV - 3.2), (0.0, Z_PIV - 3.2)], segs=48)
    ball = sphere(name + 'b', (0, 0, Z_PIV), 4.0, 32, 16)
    apply_bool(b, ball, 'UNION'); remove(ball)
    set_mats(b, mats.M['steel'])
    return b


# ======================================================================== camshafts (lobes from the follower envelope)
def follower_angle(lift):
    return math.asin(max(-0.99, min(0.99, lift / L_PAD)))


def roller_centre(lift, sy):
    """world (y, z) of the roller axle for a given valve lift; sy=+1 exhaust side, -1 intake side."""
    phi = follower_angle(lift)
    # canonical (exhaust) offset from pivot: (-L_ROL, H_ROL), rotated by +phi about X; intake mirrored
    y0, z0 = -L_ROL, H_ROL
    yr = y0 * math.cos(phi) - z0 * math.sin(phi)
    zr = y0 * math.sin(phi) + z0 * math.cos(phi)
    return (sy * Y_HLA + sy * yr, Z_PIV + zr)


def cam_alpha(theta, sy):
    """camshaft rotation about +X (rad); exhaust driven by the belt (+theta/2), intake via spur gears (-theta/2)."""
    return math.radians(theta / 2.0) * (1 if sy > 0 else -1)


def lobe_polygon(i, kind, n_dir=360, n_s=1440):
    sy = -1 if kind == 'I' else 1
    cyc0 = []
    pts = []
    for s in range(n_s):
        th = 720.0 * s / n_s
        L = valve_lift(cyc(th, i), kind)
        yr, zr = roller_centre(L, sy)
        dy, dz = yr - sy * Y_CAM, zr - Z_CAM
        a = -cam_alpha(th, sy)
        ca, sa = math.cos(a), math.sin(a)
        pts.append((dy * ca - dz * sa, dy * sa + dz * ca))
    prof = []
    R2 = R_ROLL * R_ROLL
    for j in range(n_dir):
        psi = TAU * (j + 0.5) / n_dir
        ux, uy = math.cos(psi), math.sin(psi)
        best = 1e9
        for (cy_, cz_) in pts:
            proj = cy_ * ux + cz_ * uy
            if proj <= 0: continue
            perp2 = (cy_ * cy_ + cz_ * cz_) - proj * proj
            if perp2 > R2: continue
            t = proj - math.sqrt(R2 - perp2)
            if t < best: best = t
        prof.append((best * ux, best * uy))
    return prof


def build_camshaft(name, sy):
    parts = []
    xa = X_GEAR - 7.0 if sy < 0 else X_BELT - 18.0
    parts.append(cyl(name + 'core', (xa, 0, 0), (X_HR - 8, 0, 0), 11.0, segs=64))
    for m in MAINS:
        parts.append(cyl(name + 'j', (m - 9.5, 0, 0), (m + 9.5, 0, 0), R_JOUR, segs=96))
    kind = 'I' if sy < 0 else 'E'
    for i, cx in enumerate(CX):
        prof = lobe_polygon(i, kind)
        for sx in (-1, 1):
            x = cx + sx * VX
            lb = extrude(name + f'lobe{i}{sx}', prof, x - 6.8, x + 6.8, 'YZ')
            parts.append(lb)
    # spur gear coupling the shafts (intake = mirrored + half tooth)
    rp = Y_CAM
    g = extrude(name + 'gear', gear_profile(N_GEAR, rp, 4.4, frac_top=0.42), X_GEAR - 6.0, X_GEAR + 6.0, 'YZ')
    if sy < 0:   # exhaust gear has a tooth at angle pi (pointing -Y); intake: half a tooth rotated -> gap facing the exhaust gear
        g.data.transform(Matrix.Rotation(math.pi / N_GEAR, 4, 'X'))
    parts.append(g)
    parts.append(cyl(name + 'ghub', (X_GEAR - 9.0, 0, 0), (X_GEAR + 9.0, 0, 0), 16.0, segs=64))
    if sy > 0:
        rpb = N_CAM * BELT_P / TAU
        parts.append(sprocket(name + 'spr', N_CAM, rpb, X_BELT - 14.0, X_BELT + 14.0, depth=3.4, flange=[(X_BELT - 16, X_BELT - 14), (X_BELT + 14, X_BELT + 16)]))
        parts.append(cyl(name + 'shub', (X_BELT - 18.0, 0, 0), (X_BELT + 20.0, 0, 0), 22.0, segs=64))
    cam = union(parts, name)
    # lighten the big sprocket with windows
    if sy > 0:
        wins = []
        for k in range(5):
            a = TAU * k / 5 + 0.3
            c = cyl('win', (X_BELT - 20, 44 * math.cos(a), 44 * math.sin(a)), (X_BELT + 20, 44 * math.cos(a), 44 * math.sin(a)), 11.0, segs=40)
            wins.append(c)
        bool_many(cam, wins)
    set_mats(cam, mats.M['steel'])
    return cam


def build_cam_caps():
    caps = []
    for m in MAINS:
        for sy in (-1, 1):
            c = box('ccap', m - 9.5, m + 9.5, min(sy * 21, sy * 55), max(sy * 21, sy * 55), Z_CAM, Z_CAM + 16.0)
            bevel(c, 2.0, 2, 35)
            b = cyl('ccb', (m - 15, sy * Y_CAM, Z_CAM), (m + 15, sy * Y_CAM, Z_CAM), R_JOUR + 0.15, segs=64)
            apply_bool(c, b); remove(b)
            for yy in (sy * 25.5, sy * 50.5):
                bh = cyl('cbh', (m, yy, Z_CAM + 16.0), (m, yy, Z_CAM + 21.5), 5.2, segs=6, phase=0.0)
                apply_bool(c, bh, 'UNION'); remove(bh)
            caps.append(c)
    return caps


def build_head_bolts():
    out = []
    for m in MAINS:
        for sy in (-1, 1):
            b = cyl('hbolt', (m, sy * 63, Z_SSEAT - 3.0), (m, sy * 63, Z_SSEAT + 8.5), 8.4, segs=12, phase=0.0)
            w = cyl('hbw', (m, sy * 63, Z_SSEAT - 3.0), (m, sy * 63, Z_SSEAT - 1.2), 9.0, segs=32)
            apply_bool(b, w, 'UNION'); remove(w)
            out.append(b)
    return out


def build_cover():
    zt = Z_CAM + 48.0
    o = rbox('cover', X_HF - 3, X_HR + 3, -Y_H - 2, Y_H + 2, Z_CAM, zt, 12.0)
    bevel(o, 9.0, 4, 30)
    i_ = rbox('covi', X_HF + 1, X_HR - 1, -Y_H + 2, Y_H - 2, Z_CAM - 5, zt - 3.5, 9.0)
    bevel(i_, 6.0, 3, 30)
    apply_bool(o, i_); remove(i_)
    # ribs on top
    for k in range(-3, 4):
        r = box('rib', -190, 180, k * 16 - 1.2, k * 16 + 1.2, zt - 1, zt + 2.2)
        apply_bool(o, r, 'UNION'); remove(r)
    holes = [cyl('ch', (cx + X_RISER, 0, zt - 10), (cx + X_RISER, 0, zt + 10), 6.5, segs=32) for cx in CX]
    bool_many(o, holes)
    return o
