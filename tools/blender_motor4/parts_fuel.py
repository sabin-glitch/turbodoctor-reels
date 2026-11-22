"""Injectors (Bosch CRI2 exterior, same profiles as the CRI2 section model), glow plugs, rail with sensor and pressure
regulator, HP risers, leak-off line, injector clamps."""
import math, bpy
from mathutils import Vector, Matrix
from lib import *
from dims import *
import mats


def build_injector(name):
    """local frame: nozzle tip at origin, axis +Z, HP inlet towards +X (rotate 180 deg about Z when placing)."""
    M = mats.M
    noz = revolve(name + 'noz', [(0.0, 0.0), (0.9, 0.12), (1.65, 0.55), (2.35, 1.35), (2.95, 2.55), (3.35, 4.0), (3.5, 5.6), (3.5, 22.3),
                                 (0.0, 22.3)], segs=48)
    holes = []
    for k in range(8):
        a = TAU * k / 8
        d = Vector((math.sin(math.radians(75)) * math.cos(a), math.sin(math.radians(75)) * math.sin(a), -math.cos(math.radians(75))))
        p0 = Vector((0.15 * math.cos(a), 0.15 * math.sin(a), 0.95))
        holes.append(cyl(f'h{k}', p0, p0 + d * 2.4, 0.2, segs=12))
    bool_many(noz, holes)
    set_mats(noz, M['inj_nut'])
    wsh = revolve(name + 'wsh', [(3.6, 22.2), (6.4, 22.2), (6.4, 24.0), (3.6, 24.0)], segs=48); set_mats(wsh, M['copper'])
    nut = revolve(name + 'nut', [(3.55, 22.3), (3.7, 24.0), (8.2, 24.0), (8.75, 24.5), (8.75, 61.5), (8.4, 62.0), (0.0, 62.0), (0.0, 22.3)], segs=64)
    set_mats(nut, M['inj_nut'])
    bd = revolve(name + 'bd', [(0.0, 62.0), (7.0, 62.0), (8.5, 62.6), (8.5, 112.0), (8.0, 112.5), (8.0, 121.5), (0.0, 121.5)], segs=64)
    boss = cyl('boss', (6.0, 0, 96.0), (21.0, 0, 96.0), 6.2, segs=64)
    apply_bool(bd, boss, 'UNION'); remove(boss)
    cuts = [cyl('cham', (20.2, 0, 96.0), (21.3, 0, 96.0), 6.25, r1=5.2, segs=64), cyl('ib', (21.5, 0, 96.0), (16.0, 0, 96.0), 2.0, segs=24),
            cyl('ic', (21.3, 0, 96.0), (19.9, 0, 96.0), 3.4, r1=2.0, segs=32)]
    for k in range(5):
        cuts.append(torus(f'thr{k}', (14.2 + k * 1.15, 0, 96.0), (1, 0, 0), 6.23, 0.32, seg=64, seg2=8))
    bool_many(bd, cuts)
    set_mats(bd, M['inj_body'])
    mn = revolve(name + 'mn', [(0.0, 112.0), (11.5, 112.0), (12.4, 112.9), (12.4, 136.6), (11.5, 138.0), (0.0, 138.0)], segs=64)
    from lib import extrude as _ex
    hexo = _ex('hex', [(11.0 / math.cos(math.pi / 6) * math.cos(math.pi / 6 + k * math.pi / 3), 11.0 / math.cos(math.pi / 6) * math.sin(math.pi / 6 + k * math.pi / 3)) for k in range(6)], 100, 150, 'XY')
    apply_bool(mn, hexo, 'INTERSECT'); remove(hexo)
    set_mats(mn, M['inj_nut'])
    cap = revolve(name + 'cap', [(0.0, 138.0), (11.0, 138.0), (11.0, 146.5), (10.0, 148.0), (4.2, 148.0), (4.2, 157.0), (3.6, 157.6), (0.0, 157.6)], segs=64)
    plug = box('plug', -25.0, -6.0, -6.5, 6.5, 139.0, 149.5); bevel(plug, 1.0, 2, 35)
    apply_bool(cap, plug, 'UNION'); remove(plug)
    sock = box('sock', -26.0, -13.0, -4.6, 4.6, 141.0, 147.6); apply_bool(cap, sock); remove(sock)
    set_mats(cap, M['plastic'])
    # mating connector with wires
    con = box(name + 'con', -33.0, -14.0, -5.6, 5.6, 140.0, 148.6); bevel(con, 1.2, 2, 35)
    latch = box('latch', -30.0, -18.0, -3.0, 3.0, 148.6, 150.4); apply_bool(con, latch, 'UNION'); remove(latch)
    set_mats(con, M['plastic'])
    w1 = tube(name + 'w', [(-33, 0, 144.3), (-40, 0, 144.3), (-46, 0, 150), (-48, 0, 162)], 2.3, segs=12)
    set_mats(w1, M['plastic'])
    return join([noz, wsh, nut, bd, mn, cap, con, w1], name)


def build_glow_plug(name):
    """local: tip at origin, axis +Z (object z = distance from the tip; used by the glow shader)."""
    M = mats.M
    sh = revolve(name + 'sh', [(0.0, 0.0), (1.1, 0.12), (1.7, 0.6), (2.0, 1.5), (2.0, 30.0), (2.7, 30.4), (0.0, 30.4)], segs=40)
    set_mats(sh, M['glow'])
    bd = revolve(name + 'bd', [(0.0, 30.0), (2.7, 30.0), (4.0, 30.6), (4.0, 33.0), (5.0, 34.0), (5.0, 54.6), (0.0, 54.6)], segs=48)
    thr = [torus(f't{k}', (0, 0, 35.0 + k * 1.0), (0, 0, 1), 5.05, 0.33, seg=48, seg2=8) for k in range(19)]
    bool_many(bd, thr)
    set_mats(bd, M['gp_body'])
    hx = extrude(name + 'hx', [(5.0 / math.cos(math.pi / 6) * math.cos(k * math.pi / 3), 5.0 / math.cos(math.pi / 6) * math.sin(k * math.pi / 3)) for k in range(6)], 54.6, 63.0, 'XY')
    bevel(hx, 0.5, 1, 35)
    set_mats(hx, M['zinc'])
    st = revolve(name + 'st', [(0.0, 63.0), (3.4, 63.0), (3.4, 66.0), (2.0, 66.2), (2.0, 74.0), (0.0, 74.0)], segs=32)
    set_mats(st, M['plastic'])
    boot = revolve(name + 'boot', [(0.0, 64.5), (5.6, 64.5), (6.0, 66.0), (6.0, 78.0), (3.5, 82.0), (0.0, 82.0)], segs=40)
    set_mats(boot, M['plastic'])
    wire = tube(name + 'wire', [(0, 0, 81), (0, 0, 88), (0, -4, 96), (0, -12, 101)], 2.0, segs=12)
    set_mats(wire, M['plastic'])
    return join([sh, bd, hx, st, boot, wire], name)


def build_rail():
    """rail body (cut in the section) + fuel inside + sensor and pressure-regulating valve (whole)."""
    M = mats.M
    x0, x1 = -192.0, 182.0
    body = cyl('rail', (x0, 0, Z_RAIL), (x1, 0, Z_RAIL), R_RAIL, segs=64)
    ends = []
    for xa, xb in ((x0 - 1, x0 + 14), (x1 - 14, x1 + 1)):
        e = extrude('rhex', [(13.0 / math.cos(math.pi / 6) * math.cos(k * math.pi / 3 + math.pi / 6), 13.0 / math.cos(math.pi / 6) * math.sin(k * math.pi / 3 + math.pi / 6)) for k in range(6)], xa, xb, 'YZ')
        e.data.transform(Matrix.Translation((0, 0, Z_RAIL)))
        ends.append(e)
    bos = []
    for cx in CX:
        x = cx + X_RISER
        bos.append(cyl('ob', (x, 0, Z_RAIL), (x, 0, Z_RAIL - R_RAIL - 12.0), 7.0, segs=40))
    bos.append(cyl('inb', (-178.0, 0, Z_RAIL), (-178.0, -R_RAIL - 12.0, Z_RAIL), 7.0, segs=40))
    for xm in (-88.0, 88.0):   # mounting lugs
        lug = box('lug', xm - 9, xm + 9, -6, 6, Z_RAIL - 26, Z_RAIL); bevel(lug, 2.0, 2, 35)
        bos.append(lug)
    rb = union([body] + ends + bos, 'rail')
    cuts = [cyl('rbore', (x0 - 5, 0, Z_RAIL), (x1 + 5, 0, Z_RAIL), 4.8, segs=40)]
    for cx in CX:
        x = cx + X_RISER
        cuts.append(cyl('od', (x, 0, Z_RAIL), (x, 0, Z_RAIL - R_RAIL - 13.0), 1.6, segs=16))
    cuts.append(cyl('id', (-178.0, 0, Z_RAIL), (-178.0, -R_RAIL - 13.0, Z_RAIL), 1.6, segs=16))
    for xm in (-88.0, 88.0):
        cuts.append(cyl('lh', (xm, -8, Z_RAIL - 19), (xm, 8, Z_RAIL - 19), 4.2, segs=24))
    bool_many(rb, cuts)
    set_mats(rb, M['rail'])
    # fuel in the rail (high pressure)
    fu = [cyl('fu', (x0 - 0.5, 0, Z_RAIL), (x1 + 0.5, 0, Z_RAIL), 4.75, segs=40)]
    for cx in CX:
        x = cx + X_RISER
        fu.append(cyl('fud', (x, 0, Z_RAIL), (x, 0, Z_RAIL - R_RAIL - 12.9), 1.55, segs=16))
    fu.append(cyl('fui', (-178.0, 0, Z_RAIL), (-178.0, -R_RAIL - 12.9, Z_RAIL), 1.55, segs=16))
    fuel = union(fu, 'rail_fuel')
    set_mats(fuel, M['fuel_hp'])
    # pressure sensor (front end)
    s1 = cyl('sns', (x0 - 1, 0, Z_RAIL), (x0 - 14, 0, Z_RAIL), 9.5, segs=48)
    s2 = extrude('snh', [(11.0 / math.cos(math.pi / 6) * math.cos(k * math.pi / 3), 11.0 / math.cos(math.pi / 6) * math.sin(k * math.pi / 3)) for k in range(6)], x0 - 14, x0 - 22, 'YZ')
    s2.data.transform(Matrix.Translation((0, 0, Z_RAIL)))
    sn = union([s1, s2], 'rail_sensor'); set_mats(sn, M['steel'])
    s3 = cyl('snc', (x0 - 22, 0, Z_RAIL), (x0 - 40, 0, Z_RAIL), 10.5, segs=48)
    sk = box('snk', x0 - 41, x0 - 30, -6, 6, Z_RAIL + 6, Z_RAIL + 17); apply_bool(s3, sk, 'UNION'); remove(sk)
    set_mats(s3, M['plastic'])
    sensor = join([sn, s3], 'rail_sensor')
    # pressure regulating valve (rear end)
    d1 = extrude('drh', [(13.0 / math.cos(math.pi / 6) * math.cos(k * math.pi / 3), 13.0 / math.cos(math.pi / 6) * math.sin(k * math.pi / 3)) for k in range(6)], x1 + 1, x1 + 9, 'YZ')
    d1.data.transform(Matrix.Translation((0, 0, Z_RAIL)))
    d2 = cyl('drb', (x1 + 9, 0, Z_RAIL), (x1 + 36, 0, Z_RAIL), 14.5, segs=64)
    d1 = union([d1, d2], 'rail_drv'); set_mats(d1, M['steel'])
    d3 = cyl('drc', (x1 + 36, 0, Z_RAIL), (x1 + 46, 0, Z_RAIL), 12.0, segs=48)
    dk = box('drk', x1 + 34, x1 + 47, -6, 6, Z_RAIL + 10, Z_RAIL + 22); apply_bool(d3, dk, 'UNION'); remove(dk)
    set_mats(d3, M['plastic'])
    drv = join([d1, d3], 'rail_drv')
    return rb, fuel, sensor, drv


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


def build_risers():
    M = mats.M
    out = []
    for i, cx in enumerate(CX):
        x = cx + X_RISER
        pts = fillet_path([(x, 0, Z_RAIL - R_RAIL - 12.0), (x, 0, Z_INLET), (cx - 22.0, 0, Z_INLET)], 8.0, n=10)
        t = tube(f'riser{i}', pts, 3.0, segs=20)
        n1 = hexnut(f'rn1{i}', (cx - 23.0, 0, Z_INLET), (cx - 12.5, 0, Z_INLET), 17.0)
        n2 = hexnut(f'rn2{i}', (x, 0, Z_RAIL - R_RAIL - 21.0), (x, 0, Z_RAIL - R_RAIL - 9.0), 17.0)
        set_mats(t, M['line']); set_mats(n1, M['steel']); set_mats(n2, M['steel'])
        out.append(join([t, n1, n2], f'hp_line{i}'))
    return out


def build_leakoff():
    M = mats.M
    zt = Z_TIP + 157.6
    parts = []
    for cx in CX:
        parts.append(cyl('lt', (cx, 0, zt - 6.0), (cx, 0, zt + 6.5), 4.6, segs=32))
        parts.append(cyl('lt2', (cx - 9, 0, zt + 3.5), (cx + 9, 0, zt + 3.5), 3.6, segs=24))
    pts = [(CX[0] - 9, 0, zt + 3.5), (CX[-1] + 9, 0, zt + 3.5)]
    parts.append(tube('lh', pts, 2.6, segs=16))
    tail = fillet_path([(CX[-1] + 9, 0, zt + 3.5), (CX[-1] + 40, 0, zt + 3.5), (CX[-1] + 52, 0, zt - 30)], 10.0)
    parts.append(tube('ltail', tail, 2.6, segs=16))
    lo = union(parts, 'leakoff')
    set_mats(lo, M['plastic'])
    return lo


def build_clamps():
    """one clamp bridges two injectors (cyl 1-2 and 3-4), bolt in the middle (as on the EA288)."""
    M = mats.M
    out = []
    z0 = Z_TIP + 62.6
    for (a, b, xm) in ((CX[0], CX[1], MAINS[1]), (CX[2], CX[3], MAINS[3])):
        bar = box('clamp', a, b, -5.0, 5.0, z0, z0 + 9.0)
        rings = [cyl('fo', (c, 0, z0), (c, 0, z0 + 9.0), 12.0, segs=64) for c in (a, b)]
        bar = union([bar] + rings, 'clamp')
        bevel(bar, 1.2, 2, 35)
        forks = [cyl('fk', (c, 0, z0 - 2), (c, 0, z0 + 12), 8.7, segs=64) for c in (a, b)]
        bool_many(bar, forks)
        bh = cyl('cbh', (xm, 0, z0 + 9.0), (xm, 0, z0 + 15.5), 7.0, segs=6, phase=0.0)
        wa = cyl('cbw', (xm, 0, z0 + 9.0), (xm, 0, z0 + 10.4), 8.0, segs=32)
        apply_bool(bar, bh, 'UNION'); remove(bh); apply_bool(bar, wa, 'UNION'); remove(wa)
        set_mats(bar, M['forged'])
        out.append(bar)
    return out
