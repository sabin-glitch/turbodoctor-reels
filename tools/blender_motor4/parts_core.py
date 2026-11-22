"""Block, crankshaft, con-rods, pistons, oil pan (whole solids; sections are cut later)."""
import math, bpy
from mathutils import Vector, Matrix
from lib import *
from dims import *
import mats


def gear_profile(n, r_pitch, depth, frac_top=0.38, frac_root=0.5, rounding=4):
    """simple trapezoid-ish tooth outline (y,z) around the origin, teeth start at angle 0 (tooth centred at 0)."""
    pts = []
    ra, rr = r_pitch + depth * 0.45, r_pitch - depth * 0.55
    for k in range(n):
        a0 = TAU * k / n
        p = TAU / n
        for t, r in ((-0.5, rr), (-0.5 + (1 - frac_root) / 2 * 0.0 + 0.12, rr), (-frac_top / 2 - 0.05, r_pitch), (-frac_top / 2, ra),
                     (frac_top / 2, ra), (frac_top / 2 + 0.05, r_pitch), (0.5 - 0.12, rr)):
            a = a0 + t * p
            pts.append((r * math.cos(a), r * math.sin(a)))
    return pts


def sprocket(name, n, r_pitch, x0, x1, depth=4.0, hub=None, bore=None, flange=None):
    """toothed wheel in the YZ plane between x0..x1 (axis X)."""
    ob = extrude(name, gear_profile(n, r_pitch, depth), x0, x1, 'YZ')
    if flange:
        for xa, xb in flange:
            f = cyl(name + '_fl', (xa, 0, 0), (xb, 0, 0), r_pitch + depth * 0.45 + 2.5, segs=96)
            apply_bool(ob, f, 'UNION'); remove(f)
    if hub:
        h = cyl(name + '_hub', (hub[0], 0, 0), (hub[1], 0, 0), hub[2], segs=64)
        apply_bool(ob, h, 'UNION'); remove(h)
    if bore:
        b = cyl(name + '_bore', (min(x0, x1) - 30, 0, 0), (max(x0, x1) + 30, 0, 0), bore, segs=48)
        apply_bool(ob, b); remove(b)
    return ob


# ======================================================================== block
def build_block():
    prof = [(-Y_BU, Z_BD), (Y_BU, Z_BD), (Y_BU, 150), (Y_BL, 96), (Y_BL, Z_PAN + 6), (Y_BL + 5, Z_PAN + 6), (Y_BL + 5, Z_PAN),
            (-Y_BL - 5, Z_PAN), (-Y_BL - 5, Z_PAN + 6), (-Y_BL, Z_PAN + 6), (-Y_BL, 96), (-Y_BU, 150)]
    blk = extrude('block', prof, X_BF, X_BR, 'YZ')
    bevel(blk, 3.0, 3, 35)
    # cylinder barrels hanging into the crankcase
    cuts = []
    # crankcase bays between bulkheads (bulkheads 22 wide at the mains)
    cav = [(-96, Z_PAN - 5), (96, Z_PAN - 5), (96, 84), (60, 124), (-60, 124), (-96, 84)]
    edges = [X_BF + 10] + sum([[m - 11, m + 11] for m in MAINS], []) + [X_BR - 10]
    for k in range(0, len(edges), 2):
        cuts.append(extrude(f'bay{k}', cav, edges[k], edges[k + 1], 'YZ'))
    bool_many(blk, cuts)
    for i, cx in enumerate(CX):
        bar = cyl(f'barrel{i}', (cx, 0, 104), (cx, 0, 130), 47.5, segs=96)
        apply_bool(blk, bar, 'UNION'); remove(bar)
    # cap seats: lower half of every bulkhead is the separate bearing cap
    seats = [box(f'capseat{k}', m - 11.5, m + 11.5, -58, 58, Z_PAN - 5, 0.0) for k, m in enumerate(MAINS)]
    bool_many(blk, seats)
    # main bearing bores (upper halves)
    mb = cyl('mb', (X_BF - 5, 0, 0), (X_BR + 5, 0, 0), 29.0, segs=96)
    apply_bool(blk, mb); remove(mb)
    # water jacket: scalloped ring around the siamesed bores
    jo = [cyl(f'jo{i}', (cx, 0, 142), (cx, 0, 230.0), 57.0, segs=96) for i, cx in enumerate(CX)]
    jo = union(jo, 'jacket')
    ji = [cyl(f'ji{i}', (cx, 0, 130), (cx, 0, 240), 46.5, segs=96) for i, cx in enumerate(CX)]
    bool_many(jo, ji)
    apply_bool(blk, jo); remove(jo)
    # bores
    bores = [cyl(f'bore{i}', (cx, 0, 95), (cx, 0, Z_BD + 5), RB, segs=128) for i, cx in enumerate(CX)]
    bool_many(blk, bores)
    # front seal bore for the crank nose, rear seal
    for xa, xb, r in ((X_BF - 5, X_BF + 12, 24.0), (X_BR - 12, X_BR + 5, 46.0)):
        c = cyl('seal', (xa, 0, 0), (xb, 0, 0), r, segs=64); apply_bool(blk, c); remove(c)
    # head bolt holes (visible on the deck)
    hb = [cyl(f'hb{k}', (m, s * 63.0, 120), (m, s * 63.0, Z_BD + 2), 6.0, segs=24) for k, m in enumerate(MAINS) for s in (-1, 1)]
    bool_many(blk, hb)
    # piston-cooling jet bosses: small holes at the bottom of the barrels (exhaust side)
    return blk


def build_caps():
    obs = []
    for k, m in enumerate(MAINS):
        prof = [(-56, 0), (56, 0), (56, -14), (46, -36), (-46, -36), (-56, -14)]
        cp = extrude(f'cap{k}', prof, m - 11, m + 11, 'YZ')
        bevel(cp, 2.0, 2, 35)
        b = cyl('capbore', (m - 20, 0, 0), (m + 20, 0, 0), 29.0, segs=96); apply_bool(cp, b); remove(b)
        for s in (-1, 1):
            bh = cyl('bh', (m, s * 41, -36.2), (m, s * 41, -45.0), 8.5, segs=6, phase=0.0)   # bolt heads (hex)
            bs = cyl('bs', (m, s * 41, -36.5), (m, s * 41, -34.0), 9.0, segs=48)
            apply_bool(cp, bh, 'UNION'); remove(bh); apply_bool(cp, bs, 'UNION'); remove(bs)
        obs.append(cp)
    return obs


def build_shells():
    """main bearing shells (copper) in block + caps"""
    obs = []
    for k, m in enumerate(MAINS):
        s = revolve(f'mshell{k}', [(27.05, -10.5), (29.0, -10.5), (29.0, 10.5), (27.05, 10.5)], segs=96, axis='X', center=(m, 0, 0))
        obs.append(s)
    return obs


def build_gasket():
    g = box('gasket', X_HF + 2, X_HR - 2, -Y_BU + 1, Y_BU - 1, Z_BD, Z_HD)
    holes = [cyl(f'gh{i}', (cx, 0, Z_BD - 1), (cx, 0, Z_HD + 1), RB + 1.0, segs=128) for i, cx in enumerate(CX)]
    holes += [cyl(f'gbh{k}', (m, s * 63.0, Z_BD - 1), (m, s * 63.0, Z_HD + 1), 6.5, segs=24) for k, m in enumerate(MAINS) for s in (-1, 1)]
    bool_many(g, holes)
    # beads around bores
    for i, cx in enumerate(CX):
        t = torus(f'bead{i}', (cx, 0, Z_HD - 0.2), (0, 0, 1), RB + 4.0, 0.9, seg=128, seg2=10)
        apply_bool(g, t, 'UNION'); remove(t)
    return g


def build_pan():
    outer = [(-Y_BL - 5, Z_PAN), (Y_BL + 5, Z_PAN), (Y_BL + 5, Z_PAN - 6), (Y_BL - 4, Z_PAN - 14), (Y_BL - 10, Z_PANB + 8), (Y_BL - 22, Z_PANB),
             (-Y_BL + 22, Z_PANB), (-Y_BL + 10, Z_PANB + 8), (-Y_BL + 4, Z_PAN - 14), (-Y_BL - 5, Z_PAN - 6)]
    pan = extrude('pan', outer, X_BF, X_BR, 'YZ')
    bevel(pan, 6.0, 4, 30)
    t = 3.5
    inner = [(-Y_BL + t - 4, Z_PAN + 1), (Y_BL - t + 4, Z_PAN + 1), (Y_BL - 4 - t, Z_PAN - 14), (Y_BL - 10 - t, Z_PANB + 8 + t), (Y_BL - 22, Z_PANB + t),
             (-Y_BL + 22, Z_PANB + t), (-Y_BL + 10 + t, Z_PANB + 8 + t), (-Y_BL + 4 + t, Z_PAN - 14)]
    cav = extrude('pancav', inner, X_BF + t, X_BR - t, 'YZ')
    bevel(cav, 5.0, 3, 30)
    apply_bool(pan, cav); remove(cav)
    # drain plug
    dp = cyl('drain', (60, 30, Z_PANB - 7), (60, 30, Z_PANB + 2), 9.0, segs=6, phase=0.0)
    apply_bool(pan, dp, 'UNION'); remove(dp)
    return pan


def build_oil_pool():
    """static oil in the sump (cut later with the pan)."""
    t = 3.6
    zl = -118.0
    inner = [(-Y_BL + 10 + t, zl), (Y_BL - 10 - t, zl), (Y_BL - 10 - t, Z_PANB + 8 + t), (Y_BL - 22, Z_PANB + t),
             (-Y_BL + 22, Z_PANB + t), (-Y_BL + 10 + t, Z_PANB + 8 + t)]
    pool = extrude('oil_pool', inner, X_BF + t + 0.2, X_BR - t - 0.2, 'YZ')
    return pool


# ======================================================================== crankshaft
def web_solid(name, x0, x1, s):
    """crank web between a main journal and a rod journal on side s (+1: throw at +Z), with counterweight."""
    hull = []
    # convex hull of circle(0,0,36) and circle(0, s*RC, 31)
    r0, r1 = 37.0, 31.0
    c1 = (0.0, s * RC)
    for k in range(48):
        a = TAU * k / 48
        hull.append((r0 * math.cos(a), r0 * math.sin(a)))
        hull.append((c1[0] + r1 * math.cos(a), c1[1] + r1 * math.sin(a)))
    hull = convex_hull(hull)
    w = extrude(name, hull, x0, x1, 'YZ')
    # counterweight: sector opposite to the throw
    R = 79.0; half = math.radians(64)
    base = -s * math.pi / 2 + 0.0
    cw = [(0.0, 0.0)]
    for k in range(25):
        a = (-half + 2 * half * k / 24) + (math.pi / 2 if s < 0 else -math.pi / 2)
        cw.append((R * math.cos(a), R * math.sin(a)))
    cwo = extrude(name + '_cw', cw, x0, x1, 'YZ')
    bevel(cwo, 4.0, 3, 30)
    apply_bool(w, cwo, 'UNION'); remove(cwo)
    bevel(w, 2.2, 2, 35)
    return w


def convex_hull(pts):
    pts = sorted(set((round(p[0], 6), round(p[1], 6)) for p in pts))
    def cross(o, a, b): return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0: lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0: upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def build_crank():
    parts = []
    # main journals
    for k, m in enumerate(MAINS):
        parts.append(cyl(f'mj{k}', (m - 13, 0, 0), (m + 13, 0, 0), 27.0, segs=96))
    for i, cx in enumerate(CX):
        s = THROW[i]
        parts.append(cyl(f'rj{i}', (cx - 12, 0, s * RC), (cx + 12, 0, s * RC), 24.0, segs=96))
        parts.append(web_solid(f'web{i}a', cx - 31.0, cx - 12.0, s))
        parts.append(web_solid(f'web{i}b', cx + 12.0, cx + 31.0, s))
    # nose: shaft, oil-pump chain sprocket, belt sprocket, damper pulley
    parts.append(cyl('nose', (X_DAMP - 14, 0, 0), (MAINS[0] - 13, 0, 0), 20.0, segs=64))
    parts.append(sprocket('ch_spr', N_CHS, N_CHS * CHAIN_P / TAU, X_CHAIN - 4.5, X_CHAIN + 4.5, depth=5.0))
    rp = N_CRANK * BELT_P / TAU
    parts.append(sprocket('belt_spr', N_CRANK, rp, X_BELT - 14.0, X_BELT + 14.0, depth=3.4, flange=[(X_BELT - 16, X_BELT - 14), (X_BELT + 14, X_BELT + 16)]))
    # damper pulley (poly-V)
    dpp = revolve('damper', [(20, X_DAMP - 14), (70, X_DAMP - 14), (75, X_DAMP - 11)] +
                  sum([[(75, X_DAMP - 11 + 2.4 * k + 1.2), (72.5, X_DAMP - 11 + 2.4 * k + 2.4)] for k in range(8)], []) +
                  [(75, X_DAMP + 9), (75, X_DAMP + 12), (68, X_DAMP + 14), (40, X_DAMP + 14), (40, X_DAMP + 20), (20, X_DAMP + 20)],
                  segs=128, axis='X')
    parts.append(dpp)
    # rear flange
    parts.append(cyl('flange', (MAINS[-1] + 13, 0, 0), (X_BR + 10, 0, 0), 46.0, segs=96))
    crank = union(parts, 'crankshaft')
    # oil holes in the journals
    holes = []
    for k, m in enumerate(MAINS):
        holes.append(cyl(f'oh{k}', (m, -30, 0), (m, 30, 0), 3.0, segs=16))
    for i, cx in enumerate(CX):
        s = THROW[i]
        holes.append(cyl(f'ohr{i}', (cx, 0, s * RC - 26 * s), (cx, 0, s * RC + 26 * s), 3.0, segs=16))
    bool_many(crank, holes)
    return crank


def build_flywheel():
    x0 = X_BR + 10
    fw = revolve('flywheel', [(30, 0), (120, 0), (124, 3), (124, 16), (120, 22), (60, 22), (60, 30), (30, 30)], segs=160, axis='X', center=(x0, 0, 0))
    ring = sprocket('ringgear', 132, 133.0, x0 + 4, x0 + 16, depth=4.5)
    apply_bool(fw, ring, 'UNION'); remove(ring)
    for k in range(8):
        a = TAU * k / 8 + 0.2
        b = cyl('fwb', (x0 + 29, 40 * math.cos(a), 40 * math.sin(a)), (x0 + 35, 40 * math.cos(a), 40 * math.sin(a)), 6.0, segs=6, phase=0.0)
        apply_bool(fw, b, 'UNION'); remove(b)
    for k in range(6):
        a = TAU * k / 6
        h = cyl('fwh', (x0 - 1, 90 * math.cos(a), 90 * math.sin(a)), (x0 + 25, 90 * math.cos(a), 90 * math.sin(a)), 9.0, segs=32)
        apply_bool(fw, h); remove(h)
    return fw


# ======================================================================== con-rod
def build_rod(name):
    """local frame: big end centre at origin, small end at +Z ROD; thickness along X."""
    out = []
    # outline (y,z): big end boss r=33, small end boss r=17.5, concave tapered shank (cubic bezier flanks)
    def bz(p0, p1, p2, p3, n=20):
        return [((1-t)**3*p0[0]+3*(1-t)**2*t*p1[0]+3*(1-t)*t*t*p2[0]+t**3*p3[0], (1-t)**3*p0[1]+3*(1-t)**2*t*p1[1]+3*(1-t)*t*t*p2[1]+t**3*p3[1]) for t in [k/n for k in range(n+1)]]
    rb, rs = 33.0, 17.5
    a_b, a_s = math.radians(36), math.radians(-12)
    pb = (rb*math.cos(a_b), rb*math.sin(a_b)); ps = (rs*math.cos(a_s), ROD + rs*math.sin(a_s))
    right = bz(pb, (19.0, 42.0), (11.5, 96.0), ps)
    outline = right[:-1]
    outline += [(rs*math.cos(a), ROD + rs*math.sin(a)) for a in [a_s + (math.pi - 2*a_s)*k/40 for k in range(41)]][:-1]
    left = [(-x, z) for x, z in reversed(right)]
    outline += left[:-1]
    outline += [(rb*math.cos(a), rb*math.sin(a)) for a in [math.pi - a_b + (math.pi + 2*a_b)*k/48 for k in range(49)]][:-1]
    rod = extrude(name, outline, -11.0, 11.0, 'YZ')
    # bolt bosses on both sides of the big end
    for sy in (-1, 1):
        bb = box(name + 'bb', -11, 11, sy*23.0, sy*36.0, -17.0, 14.0)
        bevel(bb, 2.0, 2, 30)
        apply_bool(rod, bb, 'UNION'); remove(bb)
    # side recesses (I-beam) on both faces
    for sx in (-1, 1):
        pk = extrude(name + 'pk', [(-7.5, 40), (7.5, 40), (5.5, 118), (-5.5, 118)], sx * 11.5, sx * 5.0, 'YZ')
        bevel(pk, 2.0, 2, 30)
        apply_bool(rod, pk); remove(pk)
    # trapezoid small end: chamfer the top
    for sy in (-1, 1):
        ch = box(name + 'ch', -14, 14, -30, 30, 0, 30)
        ch.data.transform(Matrix.Translation((sy * 11.0, 0, ROD + 6)) @ Matrix.Rotation(sy * math.radians(14), 4, 'Y') @ Matrix.Translation((sy * 14, 0, 0)))
        apply_bool(rod, ch); remove(ch)
    bevel(rod, 1.2, 2, 35)
    # bores
    b1 = cyl(name + 'b1', (-20, 0, 0), (20, 0, 0), 25.6, segs=96); apply_bool(rod, b1); remove(b1)
    b2 = cyl(name + 'b2', (-20, 0, ROD), (20, 0, ROD), 15.2, segs=64); apply_bool(rod, b2); remove(b2)
    # bolts (heads under the cap)
    for sy in (-1, 1):
        bh = cyl(name + 'bh', (0, sy * 29.5, -16.5), (0, sy * 29.5, -23.0), 6.0, segs=12, phase=0.0)
        apply_bool(rod, bh, 'UNION'); remove(bh)
    # split line groove
    gr = box(name + 'gr', -12, 12, -40, -27.6, -0.25, 0.25); g2 = box(name + 'gr2', -12, 12, 27.6, 40, -0.25, 0.25)
    bool_many(rod, [gr, g2])
    set_mats(rod, mats.M['forged'])
    shell = revolve(name + '_shell', [(24.05, -10.8), (25.6, -10.8), (25.6, 10.8), (24.05, 10.8)], segs=96, axis='X')
    bush = revolve(name + '_bush', [(14.05, -10.0), (15.2, -10.0), (15.2, 10.0), (14.05, 10.0)], segs=64, axis='X', center=(0, 0, ROD))
    set_mats(shell, mats.M['shell']); set_mats(bush, mats.M['shell'])
    return join([rod, shell, bush], name)


# ======================================================================== piston
BOWL = [(0.0, 40.6), (4.5, 38.6), (9.0, 35.0), (13.5, 32.8), (18.0, 32.6), (21.8, 34.0), (24.2, 37.0), (24.5, 40.5), (23.4, 43.4),
        (21.8, 45.4), (21.4, 46.6), (21.9, 47.9)]


def build_piston(name, cut_gallery=True):
    R = RB - 0.08
    prof = list(BOWL) + [(R - 0.25, CH), (R - 0.25, CH - 6.5), (R, CH - 7.0), (R, -SKIRT + 1.0), (R - 1.0, -SKIRT),
                         (R - 5.0, -SKIRT), (R - 5.0, -2.0), (R - 8.0, 12.0), (R - 12.0, 20.0), (22.0, 25.5), (0.0, 27.0)]
    p = revolve(name, prof, segs=128)
    # ring grooves
    grooves = []
    for z0, z1, d in ((CH - 9.6, CH - 7.1, 3.6), (CH - 15.6, CH - 13.6, 3.4), (CH - 22.6, CH - 19.6, 3.4)):
        grooves.append(revolve(name + 'g', [(R - d, z0), (R + 2, z0), (R + 2, z1), (R - d, z1)], segs=128))
    bool_many(p, grooves)
    # oil drain holes in the oil ring groove (cosmetic): skip
    # cooling gallery (visible when the piston is cut)
    if cut_gallery:
        gal = revolve(name + 'gal', [(26.5, 30.0), (33.0, 30.5), (33.5, 36.0), (27.0, 37.5)], segs=96)
        apply_bool(p, gal); remove(gal)
    # pin bosses and pin bore along X
    for sx in (-1, 1):
        bs = cyl(name + 'boss', (sx * 12.0, 0, 0), (sx * (R - 4.0), 0, 0), 19.0, segs=64)
        apply_bool(p, bs, 'UNION'); remove(bs)
    pb = cyl(name + 'pb', (-RB - 2, 0, 0), (RB + 2, 0, 0), 14.05, segs=64); apply_bool(p, pb); remove(pb)
    # skirt recess around the pin bosses (modern short skirt): cut flats on the +-X sides below the rings
    for sx in (-1, 1):
        fl = box(name + 'fl', sx * (R - 3.2), sx * (R + 5.0), -30, 30, -SKIRT - 2, CH - 26.0)
        apply_bool(p, fl); remove(fl)
    set_mats(p, mats.M['piston'])
    # rings
    rings = []
    for k, (z0, z1, d) in enumerate(((CH - 9.6, CH - 7.1, 3.6), (CH - 15.6, CH - 13.6, 3.4), (CH - 22.6, CH - 19.6, 3.4))):
        rg = revolve(name + f'r{k}', [(R - d + 0.2, z0 + 0.05), (R + 0.02, z0 + 0.05), (R + 0.02, z1 - 0.05), (R - d + 0.2, z1 - 0.05)], segs=128)
        set_mats(rg, mats.M['ring']); rings.append(rg)
    pin = revolve(name + 'pin', [(8.0, -RB + 4.5), (14.0, -RB + 4.5), (14.0, RB - 4.5), (8.0, RB - 4.5)], segs=64, axis='X')
    set_mats(pin, mats.M['steel'])
    return join([p] + rings + [pin], name)
