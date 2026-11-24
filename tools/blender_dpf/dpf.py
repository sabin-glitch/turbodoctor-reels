"""Turbo Doctor - close-coupled oxidation catalyst (DOC) + diesel particulate filter (DPF) in one housing, in Blender.

Units: 1 BU = 1 mm. Canister axis = Z, gases flow downwards (inlet from the turbocharger at the top, outlet at the bottom).
Section plane y = 0: the back half (y >= 0) stays, the camera looks from the -Y side.
DPF inlet face at z = 0. All sensors, pipes and hoses sit in the back half (y > 0), so they stay whole in the section.

  python dpf.py build                          -> out/dpf.blend
  python dpf.py info                           -> out/info.json (camera, crops, anchors, paths, lattice)
  python dpf.py queue [prefix ...]             -> renders every job not yet on disk (out/<job>.png)
  python dpf.py render <job> [samples] [pct] [out]
  python dpf.py prev <tier> <crop|''> <vis> <pct> <spp> <out> [hold]
  python dpf.py look <view> <up> <field> <size> <spp> <out> [vis] [tgt] [dist]
"""
import bpy, math, json, os, sys, time
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from kit import *
from kit import _p

OUT = os.environ.get('DPF_OUT', os.path.join(HERE, 'out'))
os.makedirs(OUT, exist_ok=True)

# --------------------------------------------------------------------------- dimensions (mm)
R_B = 72.0                       # brick radius (144 mm, 5.66")
MAT_T = 5.0                      # support mat
SH_T = 1.5                       # stainless shell
R_SI = R_B + MAT_T               # shell inner radius
R_SO = R_SI + SH_T
DPF_Z0, DPF_Z1 = -178.0, 0.0     # filter brick (7")
DOC_Z0, DOC_Z1 = 20.0, 96.0      # catalyst brick (3"), 20 mm gap to the filter
SH_Z0, SH_Z1 = -186.0, 104.0     # cylindrical part of the shell
R_IN, R_OUT = 32.0, 30.0         # inlet / outlet pipe outer radius
IN_Z, IN_R = 166.0, 55.0         # inlet elbow: starts at z, bend radius
IN_PZ = IN_Z + IN_R              # inlet pipe axis height (221)
IN_X0 = -100.0                   # inlet flange face
OUT_Z, OUT_R = -250.0, 50.0      # outlet elbow
OUT_PZ = OUT_Z - OUT_R           # outlet pipe axis height (-300)
OUT_X1 = 103.0                   # outlet flange face

# DPF: silicon carbide, square segments cemented together, 200 cpsi class (31 cells/cm2, wall 0.38 mm)
DPF_P, DPF_W, DPF_NSEG, DPF_SEAM, DPF_PLUG = 34.3 / 19, 0.38, 19, 1.6, 6.0
# DOC: cordierite flow-through monolith, 400 cpsi class
DOC_P, DOC_W = 1.27, 0.17

# revolved body: the necks are a little thinner than the elbow tubes, so the two surfaces never coincide in the booleans
OUTER = [(0.0, -247.5), (29.2, -247.5), (29.2, -245.8), (33.0, -241.5), (38.0, -237.0), (72.0, -197.5), (76.6, -191.0), (78.5, -186.0),
         (78.5, 104.0), (76.6, 109.0), (72.0, 115.5), (40.0, 155.0), (34.5, 160.5), (31.2, 165.3), (31.2, 167.0), (0.0, 167.0)]
INNER = [(0.0, -251.0), (27.7, -251.0), (27.7, -245.4), (31.4, -241.0), (36.5, -236.4), (70.6, -196.8), (75.1, -190.5), (77.0, -185.6),
         (77.0, 103.6), (75.1, 108.5), (70.6, 114.8), (38.6, 154.2), (33.0, 159.8), (29.6, 164.9), (29.6, 168.5), (0.0, 168.5)]


def r_prof(prof, z):
    for (r0, z0), (r1, z1) in zip(prof[1:-1], prof[2:-1]):
        if z0 <= z <= z1:
            return r0 + (r1 - r0) * (z - z0) / max(1e-9, z1 - z0)
    return 0.0


def inlet_path(z_start, x_end, n=16):
    pts = [(0.0, 0.0, z_start), (0.0, 0.0, IN_Z)]
    for k in range(1, n + 1):
        th = (PI / 2) * k / n
        pts.append((-IN_R + IN_R * math.cos(th), 0.0, IN_Z + IN_R * math.sin(th)))
    pts.append((x_end, 0.0, IN_PZ))
    return pts


def outlet_path(z_start, x_end, n=16):
    pts = [(0.0, 0.0, z_start), (0.0, 0.0, OUT_Z)]
    for k in range(1, n + 1):
        th = (PI / 2) * k / n
        pts.append((OUT_R - OUT_R * math.cos(th), 0.0, OUT_Z - OUT_R * math.sin(th)))
    pts.append((x_end, 0.0, OUT_PZ))
    return pts


def _dist_poly(p, pts):
    p = Vector(p); best = 1e9
    for a, b in zip(pts, pts[1:]):
        a, b = Vector(a), Vector(b); ab = b - a
        t = max(0.0, min(1.0, (p - a).dot(ab) / max(1e-9, ab.length_squared)))
        best = min(best, (p - (a + ab * t)).length)
    return best


_IN_C = inlet_path(150.0, IN_X0 - 6.0); _OUT_C = outlet_path(-236.0, OUT_X1 + 6.0)


def inside_cavity(p, tol=0.0):
    r = math.hypot(p[0], p[1])
    if INNER[1][1] <= p[2] <= INNER[-2][1] and r < r_prof(INNER, p[2]) + tol: return True
    if _dist_poly(p, _IN_C) < R_IN - SH_T + tol: return True
    if _dist_poly(p, _OUT_C) < R_OUT - SH_T + tol: return True
    return False


# ---- sensor ports: (point on the outer wall, outward direction)
def _cone_x(z, y, sign):
    return sign * math.sqrt(max(0.0, r_prof(OUTER, z) ** 2 - y * y))


Y_S = 12.0                                    # plane of the temperature sensors
Y_P = 14.0                                    # plane of the pressure pipes / lambda probe
T1_P = (_cone_x(128.0, Y_S, -1), Y_S, 128.0); T1_D = (-1.0, 0.0, 0.0)                  # before the catalyst
T2_P = (_cone_x(10.0, Y_S, -1), Y_S, 10.0); T2_D = (-1.0, 0.0, 0.0)                     # between catalyst and filter
T3_P = (_cone_x(-215.0, Y_S, -1), Y_S, -215.0); T3_D = (-math.cos(math.radians(24)), 0.0, -math.sin(math.radians(24)))   # after the filter
_LA = math.radians(45.0)
_LC = Vector((-IN_R + IN_R * math.cos(_LA), 0.0, IN_Z + IN_R * math.sin(_LA)))
LAM_D = (math.cos(_LA), 0.0, math.sin(_LA))
LAM_P = tuple(_LC + Vector(LAM_D) * math.sqrt(R_IN ** 2 - Y_P ** 2) + Vector((0.0, Y_P, 0.0)))
P1_P = (_cone_x(10.0, Y_P, 1), Y_P, 10.0)       # pressure tap before the filter (in the gap)
P2_P = (_cone_x(-216.0, Y_P, 1), Y_P, -216.0)   # pressure tap after the filter (outlet cone)
PX1, PX2 = 104.0, 124.0                       # vertical runs of the two pressure pipes
PIPE_TOP = 92.0
PORT_X1, PORT_X2, PORT_Z = 112.0, 132.0, 150.0  # sensor ports (pointing down)
SENS_C = (122.0, Y_P, 193.0)                  # differential pressure sensor body centre


def arc_pts(c, r, a0, a1, n, plane='xz', y=0.0):
    pts = []
    for k in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * k / n)
        pts.append((c[0] + r * math.cos(a), y, c[1] + r * math.sin(a)))
    return pts


def p1_path():
    """pressure pipe from the tap before the filter: out of the boss, bend, straight up."""
    return [(P1_P[0] - 3.0, Y_P, 10.0), (PX1 - 12.0, Y_P, 10.0)] + arc_pts((PX1 - 12.0, 22.0), 12.0, -90, 0, 10, y=Y_P)[1:] + [(PX1, Y_P, PIPE_TOP)]


def p2_path():
    return [(P2_P[0] - 3.0, Y_P, -216.0), (PX2 - 12.0, Y_P, -216.0)] + arc_pts((PX2 - 12.0, -204.0), 12.0, -90, 0, 10, y=Y_P)[1:] + [(PX2, Y_P, PIPE_TOP)]


def bez(P0, P1, P2, P3, n):
    out = []
    for k in range(n + 1):
        t = k / n; u = 1 - t
        out.append(tuple(u ** 3 * Vector(P0) + 3 * u * u * t * Vector(P1) + 3 * u * t * t * Vector(P2) + t ** 3 * Vector(P3)))
    return out


def hose1_path(): return bez((PX1, Y_P, PIPE_TOP - 14.0), (PX1, Y_P, 118.0), (PORT_X1, Y_P, 124.0), (PORT_X1, Y_P, PORT_Z + 10.0), 24)
def hose2_path(): return bez((PX2, Y_P, PIPE_TOP - 14.0), (PX2, Y_P, 118.0), (PORT_X2, Y_P, 124.0), (PORT_X2, Y_P, PORT_Z + 10.0), 24)


def spline(pts, n=10):
    """Catmull-Rom through the points."""
    P = [Vector(p) for p in pts]; P = [P[0] * 2 - P[1]] + P + [P[-1] * 2 - P[-2]]
    out = []
    for i in range(1, len(P) - 2):
        for k in range(n):
            t = k / n; t2 = t * t; t3 = t2 * t
            out.append(tuple(0.5 * ((2 * P[i]) + (-P[i - 1] + P[i + 1]) * t + (2 * P[i - 1] - 5 * P[i] + 4 * P[i + 1] - P[i + 2]) * t2 +
                                    (-P[i - 1] + 3 * P[i] - 3 * P[i + 1] + P[i + 2]) * t3)))
    out.append(tuple(P[-2]))
    return out


def along(p, d, s): return tuple(Vector(p) + Vector(d).normalized() * s)


T_LEN = 64.0          # rigid length of a temperature sensor outside the wall
L_LEN = 70.0          # lambda probe
T1_CAB = [along(T1_P, T1_D, T_LEN - 2), along(T1_P, T1_D, T_LEN + 16), (-164.0, 13.0, 112.0), (-172.0, 15.0, 84.0), (-172.0, 16.0, 58.0)]
T2_CAB = [along(T2_P, T2_D, T_LEN - 2), along(T2_P, T2_D, T_LEN + 16), (-177.0, 13.0, -6.0), (-185.0, 15.0, -34.0), (-185.0, 16.0, -62.0)]
T3_CAB = [along(T3_P, T3_D, T_LEN - 2), along(T3_P, T3_D, T_LEN + 16), (-150.0, 13.0, -262.0), (-166.0, 15.0, -284.0), (-168.0, 16.0, -312.0)]
LAM_CAB = [along(LAM_P, LAM_D, L_LEN - 2), along(LAM_P, LAM_D, L_LEN + 18), (62.0, 15.0, 303.0), (30.0, 16.0, 315.0), (-10.0, 17.0, 314.0), (-44.0, 18.0, 302.0)]


# --------------------------------------------------------------------------- honeycomb bricks (direct mesh, half brick y >= 0)
class Quads:
    def __init__(self): self.V = []; self.F = []

    def add(self, p0, p1, p2, p3, n):
        a = (p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2]); b = (p2[0] - p0[0], p2[1] - p0[1], p2[2] - p0[2])
        cx = a[1] * b[2] - a[2] * b[1]; cy = a[2] * b[0] - a[0] * b[2]; cz = a[0] * b[1] - a[1] * b[0]
        q = (p0, p1, p2, p3) if (cx * n[0] + cy * n[1] + cz * n[2]) >= 0 else (p3, p2, p1, p0)
        i = len(self.V); self.V.extend(q); self.F.append((i, i + 1, i + 2, i + 3))

    def obj(self, name):
        if not self.F: return None
        me = bpy.data.meshes.new(name); me.from_pydata(self.V, [], self.F); me.update()
        ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
        return ob


def honeycomb(name, R, z0, z1, pitch, wall, nseg=0, seam=0.0, plug=0.0, hole_depth=9.0, skin=2.2, rec=0.3):
    """returns {'wall','in','out','plug','seam','dark'} objects + lattice info. Cut row (y = 0) goes through cell centres."""
    h = (pitch - wall) / 2
    if nseg:
        Pseg = nseg * pitch + seam; k0 = int(math.ceil(R / Pseg)) + 1
        xs = [k * Pseg + seam / 2 + (i + 0.5) * pitch for k in range(-k0, k0) for i in range(nseg)]
        ys = [m * Pseg + (j - nseg // 2) * pitch for m in range(0, k0 + 1) for j in range(nseg)]
        ys = [y for y in ys if y > -1e-6]
    else:
        n = int(R / pitch) + 2
        xs = [(i + 0.5) * pitch for i in range(-n, n)]; ys = [j * pitch for j in range(0, n + 1)]
    xs = [x for x in xs if abs(x) - h < R]; ys = [y for y in ys if y - h < R]

    def intervals(cs, lo, hi):
        out = []; cur = lo
        for n_, c in enumerate(cs):
            a, b = max(c - h, lo), min(c + h, hi)
            if b <= a: continue
            if a > cur + 1e-9: out.append((cur, a, 's' if a - cur > wall * 1.6 else 'w', -1))
            out.append((a, b, 'h', n_)); cur = b
        if hi > cur + 1e-9: out.append((cur, hi, 'w', -1))
        return out
    XI = intervals(xs, -R, R); YI = intervals(ys, 0.0, R)

    def valid(ix, iy): return math.hypot(abs(xs[ix]) + h, abs(ys[iy]) + h) <= R - skin
    def inlet(ix, iy): return (ix + iy) % 2 == 0

    Q = {k: Quads() for k in ('wall', 'in', 'out', 'plug', 'seam', 'dark')}
    UP, DN, FR, BK, LF, RT = (0, 0, 1), (0, 0, -1), (0, -1, 0), (0, 1, 0), (-1, 0, 0), (1, 0, 0)
    # ---- end faces
    for (xa, xb, kx, ix) in XI:
        for (ya, yb, ky, iy) in YI:
            if max(math.hypot(xa, ya), math.hypot(xa, yb), math.hypot(xb, ya), math.hypot(xb, yb)) > R: continue
            cell = kx == 'h' and ky == 'h' and valid(ix, iy)
            for (zf, s) in ((z1, 1), (z0, -1)):
                nrm = UP if s > 0 else DN
                if not cell:
                    key = 'seam' if (kx == 's' or ky == 's' or (kx == 'h' and ky == 'h')) else 'wall'
                    Q[key].add((xa, ya, zf), (xb, ya, zf), (xb, yb, zf), (xa, yb, zf), nrm); continue
                is_in = inlet(ix, iy) or plug == 0
                opened = True if plug == 0 else (is_in == (s > 0))
                ck = 'in' if is_in else 'out'
                if opened:
                    if iy == 0: continue                       # the cut trough itself is open here
                    zb = zf - s * hole_depth
                    Q[ck].add((xa, ya, zf), (xa, yb, zf), (xa, yb, zb), (xa, ya, zb), RT)
                    Q[ck].add((xb, ya, zf), (xb, yb, zf), (xb, yb, zb), (xb, ya, zb), LF)
                    Q[ck].add((xa, ya, zf), (xb, ya, zf), (xb, ya, zb), (xa, ya, zb), BK)
                    Q[ck].add((xa, yb, zf), (xb, yb, zf), (xb, yb, zb), (xa, yb, zb), FR)
                    Q['dark'].add((xa, ya, zb), (xb, ya, zb), (xb, yb, zb), (xa, yb, zb), nrm)
                else:
                    zb = zf - s * rec
                    Q['plug'].add((xa, ya, zb), (xb, ya, zb), (xb, yb, zb), (xa, yb, zb), nrm)
                    Q['wall'].add((xa, ya, zf), (xa, yb, zf), (xa, yb, zb), (xa, ya, zb), RT)
                    Q['wall'].add((xb, ya, zf), (xb, yb, zf), (xb, yb, zb), (xb, ya, zb), LF)
                    if iy > 0: Q['wall'].add((xa, ya, zf), (xb, ya, zf), (xb, ya, zb), (xa, ya, zb), BK)
                    Q['wall'].add((xa, yb, zf), (xb, yb, zf), (xb, yb, zb), (xa, yb, zb), FR)
    # ---- cut face (y = 0)
    cells = []
    for (xa, xb, kx, ix) in XI:
        cell = kx == 'h' and valid(ix, 0)
        if not cell:
            key = 'seam' if (kx != 'w' or abs((xa + xb) / 2) > R - skin) else 'wall'
            Q[key].add((xa, 0, z0), (xb, 0, z0), (xb, 0, z1), (xa, 0, z1), FR); continue
        is_in = inlet(ix, 0) or plug == 0
        ck = 'in' if is_in else 'out'
        if plug == 0: ta, tb = z0, z1
        elif is_in:
            ta, tb = z0 + plug, z1
            Q['plug'].add((xa, 0, z0 + rec), (xb, 0, z0 + rec), (xb, 0, ta), (xa, 0, ta), FR)
            Q['plug'].add((xa, 0, ta), (xb, 0, ta), (xb, h, ta), (xa, h, ta), UP)
        else:
            ta, tb = z0, z1 - plug
            Q['plug'].add((xa, 0, tb), (xb, 0, tb), (xb, 0, z1 - rec), (xa, 0, z1 - rec), FR)
            Q['plug'].add((xa, 0, tb), (xb, 0, tb), (xb, h, tb), (xa, h, tb), DN)
        Q[ck].add((xa, 0, ta), (xa, h, ta), (xa, h, tb), (xa, 0, tb), RT)
        Q[ck].add((xb, 0, ta), (xb, h, ta), (xb, h, tb), (xb, 0, tb), LF)
        Q[ck].add((xa, h, ta), (xb, h, ta), (xb, h, tb), (xa, h, tb), FR)
        cells.append([round(xa, 4), round(xb, 4), 1 if is_in else 0])
    # ---- outer skin + skin rings on the end faces
    N = 96
    for k in range(N):
        a0, a1 = PI * k / N, PI * (k + 1) / N
        c0, s0, c1, s1 = math.cos(a0), math.sin(a0), math.cos(a1), math.sin(a1)
        Q['seam'].add((R * c0, R * s0, z0), (R * c1, R * s1, z0), (R * c1, R * s1, z1), (R * c0, R * s0, z1), ((c0 + c1), (s0 + s1), 0))
        ri = R - skin - 0.25
        for (zf, nrm) in ((z1 + 0.02, UP), (z0 - 0.02, DN)):
            Q['seam'].add((ri * c0, ri * s0, zf), (R * c0, R * s0, zf), (R * c1, R * s1, zf), (ri * c1, ri * s1, zf), nrm)
    obs = {k: q.obj(f'{name}_{k}') for k, q in Q.items()}
    info = {'pitch': pitch, 'wall': wall, 'h': h, 'cells': cells, 'z0': z0, 'z1': z1, 'plug': plug,
            'seams_x': [round((a + b) / 2, 3) for (a, b, k, i) in XI if k == 's']}
    return {k: o for k, o in obs.items() if o is not None}, info


# --------------------------------------------------------------------------- shell
def convex_hull(pts):
    pts = sorted(set((round(x, 5), round(y, 5)) for x, y in pts))
    def cross(o, a, b): return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def circle(cx, cy, r, n=40): return [(cx + r * math.cos(2 * PI * k / n), cy + r * math.sin(2 * PI * k / n)) for k in range(n)]


def torus_z(name, z, R, r, seg=128, seg2=14):
    ob = torus_x(name, z, R, r, seg, seg2); ob.data.transform(Matrix.Rotation(-PI / 2, 4, 'Y')); return ob


BOSSES = [   # name, point, direction, boss radius, boss height, hole radius
    ('t1', T1_P, T1_D, 9.5, 10.0, 3.3), ('t2', T2_P, T2_D, 9.5, 10.0, 3.3), ('t3', T3_P, T3_D, 9.5, 10.0, 3.3),
    ('lam', LAM_P, LAM_D, 13.0, 12.0, 6.6), ('p1', P1_P, (1, 0, 0), 8.0, 9.0, 2.6), ('p2', P2_P, (1, 0, 0), 8.0, 9.0, 2.6)]


def build_shell():
    body = revolve_z('shell', OUTER, segs=144)
    pin = inlet_path(156.0, IN_X0 + 1.0); pout = outlet_path(-240.0, OUT_X1 - 1.0)
    adds = [sweep('in_o', pin, [R_IN] * len(pin), segs=72), sweep('out_o', pout, [R_OUT] * len(pout), segs=72)]
    # V-band flange towards the turbocharger
    vf = revolve_x('vband', [(IN_X0, 29.0), (IN_X0, 44.0), (IN_X0 + 1.6, 44.0), (IN_X0 + 8.5, 34.5), (IN_X0 + 8.5, 29.0)], segs=96)
    vf.data.transform(Matrix.Translation((0.0, 0.0, IN_PZ))); adds.append(vf)
    # two-bolt outlet flange
    hull = convex_hull(circle(0.0, OUT_PZ, 41.0, 64) + circle(48.0, OUT_PZ, 13.0, 32) + circle(-48.0, OUT_PZ, 13.0, 32))
    adds.append(extrude('oflange', hull, 'x', OUT_X1 - 9.0, OUT_X1))
    for (nm, p, d, rb, hb, rh) in BOSSES:
        adds.append(cyl('boss_' + nm, along(p, d, -5.0), along(p, d, hb), rb, segs=48))
    for a_ in adds:
        apply_bool(body, a_, 'UNION'); bpy.data.objects.remove(a_, do_unlink=True)
    cav = revolve_z('cav', INNER, segs=144)
    for c_ in (sweep('in_i', _IN_C, [R_IN - SH_T] * len(_IN_C), segs=72), sweep('out_i', _OUT_C, [R_OUT - SH_T] * len(_OUT_C), segs=72)):
        apply_bool(cav, c_, 'UNION'); bpy.data.objects.remove(c_, do_unlink=True)
    cuts = [cav]
    for (nm, p, d, rb, hb, rh) in BOSSES:
        cuts.append(cyl('hole_' + nm, along(p, d, -14.0), along(p, d, hb + 2.0), rh, segs=32))
    for sy in (-1, 1):
        cuts.append(cyl(f'ofh{sy}', (OUT_X1 - 12.0, sy * 48.0, OUT_PZ), (OUT_X1 + 2.0, sy * 48.0, OUT_PZ), 5.6, segs=32))
    bool_many(body, cuts)
    return body


def build_welds():
    W = [torus_z('weld_top', SH_Z1 + 0.5, R_SO + 0.45, 1.5), torus_z('weld_bot', SH_Z0 - 0.5, R_SO + 0.45, 1.5),
         torus_z('weld_n1', 165.0, R_IN + 0.55, 1.25, seg=96), torus_z('weld_n2', -246.5, R_OUT + 0.55, 1.25, seg=96)]
    wf = torus_x('weld_vb', IN_X0 + 9.0, R_IN + 0.6, 1.3, seg=96); wf.data.transform(Matrix.Translation((0, 0, IN_PZ))); W.append(wf)
    wo = torus_x('weld_of', OUT_X1 - 9.4, R_OUT + 0.6, 1.4, seg=96); wo.data.transform(Matrix.Translation((0, 0, OUT_PZ))); W.append(wo)
    return W


def build_front_details():
    """things on the front half only (leave with it when the section opens): seam weld, type plate."""
    D = []
    a = math.radians(-118.0)                                    # longitudinal seam of the rolled shell
    D.append(cyl('weld_seam', (R_SO * math.cos(a), R_SO * math.sin(a), SH_Z0 + 2.0), (R_SO * math.cos(a), R_SO * math.sin(a), SH_Z1 - 2.0), 1.5, segs=14))
    # stamped type plate, spot-welded on the shell
    a0, a1 = math.radians(-97.0), math.radians(-66.0); n = 12; V = []; F = []
    for k in range(n + 1):
        an = a0 + (a1 - a0) * k / n
        for (rr, zz) in ((R_SO - 0.2, -96.0), (R_SO + 0.7, -96.0), (R_SO + 0.7, -70.0), (R_SO - 0.2, -70.0)):
            V.append((rr * math.cos(an), rr * math.sin(an), zz))
    for k in range(n):
        b = k * 4; c = b + 4
        for j in range(4):
            j2 = (j + 1) % 4; F.append([b + j, c + j, c + j2, b + j2])
    F.append([0, 1, 2, 3]); F.append([n * 4 + 3, n * 4 + 2, n * 4 + 1, n * 4])
    D.append(mesh_obj('type_plate', V, F))
    return D


# --------------------------------------------------------------------------- sensors
def place(ob, p, d):
    ob.data.transform(Matrix.Translation(Vector(p)) @ rot_from_x(d)); return ob


def connector(name, p, tangent, L=26.0, a=6.5, b=5.5):
    obs = []
    body = extrude(name, rrect(0, 0, a, b, 1.6), 'x', 0.0, L)
    lock = box(name + '_lock', L * 0.35, L * 0.8, -a * 0.55, a * 0.55, b - 0.2, b + 1.6)
    boot = revolve_x(name + '_boot', [(-7.0, 0.0), (-7.0, 3.0), (0.5, 4.6), (0.5, 0.0)], segs=24)
    for o in (body, lock, boot):
        place(o, p, tangent); obs.append(o)
    return obs


def temp_sensor(name, p, d, cab):
    """exhaust gas temperature sensor: probe in the gas, union nut on the welded boss, steel tube, crimp, braided lead, plug."""
    O = []
    O.append(place(revolve_x(name + '_probe', [(-46.0, 0.0), (-45.2, 1.25), (-44.0, 1.6), (-10.0, 1.6), (-9.0, 2.9), (12.0, 2.9), (12.0, 0.0)], segs=32), p, d))
    nut = prism_x(name + '_nut', 6, 8.5, 10.0, 21.0, rot=0.3)
    ch = revolve_x(name + '_nc', [(9.9, 0.0), (9.9, 8.3), (11.0, 9.9), (20.0, 9.9), (21.1, 8.6), (21.1, 0.0)], segs=48)
    apply_bool(nut, ch, 'INTERSECT'); bpy.data.objects.remove(ch, do_unlink=True)
    O.append(place(nut, p, d))
    O.append(place(revolve_x(name + '_tube', [(21.0, 0.0), (21.0, 5.2), (24.0, 5.2), (25.0, 3.1), (46.0, 3.1), (46.0, 0.0)], segs=32), p, d))
    O.append(place(revolve_x(name + '_crimp', [(46.0, 0.0), (46.0, 4.3), (51.0, 4.3), (51.6, 3.7), (53.0, 3.7), (53.6, 4.3), (62.0, 4.3), (T_LEN, 3.4), (T_LEN, 0.0)], segs=32), p, d))
    pts = spline(cab, 10)
    O.append(sweep(name + '_cable', pts, [2.35] * len(pts), segs=20))
    tg = Vector(pts[-1]) - Vector(pts[-2])
    O += connector(name + '_conn', pts[-1], tg)
    return O


def lambda_probe(name, p, d, cab):
    O = []
    O.append(place(revolve_x(name + '_tip', [(-24.0, 0.0), (-24.0, 4.6), (-22.6, 5.9), (-2.0, 5.9), (-2.0, 6.4), (14.0, 6.4), (14.0, 0.0)], segs=40), p, d))
    hx = prism_x(name + '_hex', 6, 11.0, 12.0, 21.0, rot=0.2)
    ch = revolve_x(name + '_hc', [(11.9, 0.0), (11.9, 11.0), (13.0, 12.7), (20.0, 12.7), (21.1, 11.2), (21.1, 0.0)], segs=48)
    apply_bool(hx, ch, 'INTERSECT'); bpy.data.objects.remove(ch, do_unlink=True)
    O.append(place(hx, p, d))
    O.append(place(revolve_x(name + '_body', [(21.0, 0.0), (21.0, 10.3), (39.0, 10.3), (40.2, 9.2), (41.4, 9.2), (42.0, 10.0), (44.0, 10.0), (45.0, 8.9), (47.5, 7.7),
                                              (58.0, 7.7), (58.0, 0.0)], segs=48), p, d))
    O.append(place(revolve_x(name + '_grommet', [(58.0, 0.0), (58.0, 6.9), (60.0, 7.2), (66.0, 6.4), (L_LEN, 4.4), (L_LEN, 0.0)], segs=40), p, d))
    pts = spline(cab, 10)
    O.append(sweep(name + '_cable', pts, [3.3] * len(pts), segs=20))
    tg = Vector(pts[-1]) - Vector(pts[-2])
    O += connector(name + '_conn', pts[-1], tg, L=34.0, a=8.5, b=7.0)
    return O


def ring_z(name, x, y, z0, z1, r0, r1, segs=32):
    ob = revolve_z(name, [(r0, z0), (r1, z0), (r1, z1), (r0, z1)], segs=segs); ob.data.transform(Matrix.Translation((x, y, 0.0))); return ob


def build_dp_sensor():
    """differential pressure sensor on a bracket with a heat shield, two rubber hoses, two steel pipes to the taps."""
    O = []
    cx, cy, cz = SENS_C
    body = extrude('dps_body', rrect(cx, cz, 24.0, 21.0, 5.0), 'y', cy - 13.0, cy + 13.0)
    O.append(body)
    O.append(extrude('dps_lid', rrect(cx - 2.0, cz, 18.0, 16.5, 4.0), 'y', cy - 14.0, cy - 12.6))
    for i, px in enumerate((PORT_X1, PORT_X2)):
        prt = revolve_z(f'dps_port{i}', [(0.0, PORT_Z), (2.0, PORT_Z), (3.3, PORT_Z + 1.0), (4.3, PORT_Z + 5.0), (3.5, PORT_Z + 5.2), (3.5, PORT_Z + 7.0), (4.3, PORT_Z + 11.0),
                                          (3.5, PORT_Z + 11.2), (3.5, cz - 21.0 - 4.0), (5.6, cz - 21.0 - 3.0), (5.6, cz - 20.0), (0.0, cz - 20.0)], segs=32)
        prt.data.transform(Matrix.Translation((px, cy, 0.0))); O.append(prt)
    sock = extrude('dps_sock', rrect(cy, cz + 1.0, 8.5, 10.5, 2.6), 'x', cx + 23.0, cx + 45.0)
    bool_many(sock, [extrude('dps_sock_c', rrect(cy, cz + 1.0, 6.9, 8.9, 1.8), 'x', cx + 30.0, cx + 46.0)])
    O.append(sock)
    for k in (-1, 0, 1):
        O.append(cyl(f'dps_pin{k}', (cx + 29.0, cy, cz + 1.0 + k * 4.6), (cx + 42.0, cy, cz + 1.0 + k * 4.6), 0.6, segs=10))
    O.append(box('dps_latch', cx + 31.0, cx + 39.0, cy - 3.0, cy + 3.0, cz + 11.2, cz + 13.4))
    lug = extrude('dps_lug', stadium2((cx, cz + 20.0), (cx, cz + 32.0), 8.5), 'y', cy - 5.0, cy + 5.0)
    bool_many(lug, [cyl('dps_lug_h', (cx, cy - 7.0, cz + 32.0), (cx, cy + 7.0, cz + 32.0), 3.3, segs=24)])
    O.append(lug)
    O += hexbolt('dps_bolt', (cx, cy - 5.0, cz + 32.0), (0.0, -1.0, 0.0), af=10.0, h=4.6)
    O.append(cyl('dps_spacer', (cx, cy + 5.0, cz + 32.0), (cx, cy + 14.2, cz + 32.0), 6.0, segs=32))
    # bracket + heat shield
    yb = cy + 14.0
    O.append(extrude('brk_dps', [(152.0, 238.0), (96.0, 238.0), (96.0, 160.0), (73.2, 112.0), (73.2, 86.0), (86.0, 86.0), (86.0, 106.0), (110.0, 150.0), (152.0, 150.0)], 'y', yb, yb + 2.0))
    O.append(box('shield_a', 87.0, 88.2, 0.8, yb + 2.0, 150.0, 242.0))
    O.append(box('shield_b', 87.0, 99.0, 0.8, yb + 2.0, 242.0, 243.2))
    # steel pipes with union nuts and a hose bead
    for i, (pp, tap) in enumerate(((p1_path(), P1_P), (p2_path(), P2_P))):
        O.append(sweep(f'ppipe{i}', pp, [4.0] * len(pp), segs=28))
        nut = prism_x(f'pnut{i}', 6, 7.0, tap[0] + 9.0, tap[0] + 18.0, rot=0.3); nut.data.transform(Matrix.Translation((0.0, tap[1], tap[2]))); O.append(nut)
        px = (PX1, PX2)[i]
        O.append(ring_z(f'pbead{i}', px, Y_P, PIPE_TOP - 5.5, PIPE_TOP - 3.5, 0.0, 4.9, segs=28))
        O.append(ring_z(f'pclip{i}', px, Y_P, -76.0, -64.0, 3.9, 6.2))
    O.append(box('brk_clip', 74.6, 131.0, Y_P + 5.6, Y_P + 7.4, -77.0, -63.0))
    # rubber hoses + spring clamps
    for i, hp in enumerate((hose1_path(), hose2_path())):
        O.append(sweep(f'hose{i}', hp, [5.6] * len(hp), segs=28))
        px, qx = (PX1, PX2)[i], (PORT_X1, PORT_X2)[i]
        for j, (x_, z_) in enumerate(((px, PIPE_TOP - 9.5), (qx, PORT_Z + 4.5))):
            O.append(ring_z(f'hclamp{i}{j}', x_, Y_P, z_ - 3.5, z_ + 3.5, 5.3, 6.6))
            O.append(box(f'hclamp_e{i}{j}', x_ + 5.6, x_ + 10.0, Y_P - 2.2, Y_P + 2.2, z_ - 3.5, z_ + 3.5))
    return O


def build_back_bracket():
    pl = extrude('brk_back', [(-67.5, -86.0), (-124.0, -94.0), (-135.0, -106.0), (-135.0, -124.0), (-124.0, -136.0), (-67.5, -142.0)], 'y', 36.0, 39.0)
    bool_many(pl, [cyl('bb_h', (-117.0, 34.0, -115.0), (-117.0, 41.0, -115.0), 5.4, segs=32)])
    return [pl]


# --------------------------------------------------------------------------- materials
def _mat(name):
    m = bpy.data.materials.new(name); m.use_nodes = True; m.use_fake_user = True
    return m, m.node_tree, m.node_tree.nodes['Principled BSDF']


def mat_surf(name, col, rough, metal=0.0, bump=0.0, bscale=1.0, bdist=0.05, detail=6.0, tint2=None, tscale=0.05, tlo=0.40, thi=0.66, bevel=0.0,
             zbands=None, rvar=0.0, stretch=None, coat=0.0, grain=None):
    """principled surface with object-space noise bump, large-scale tint and optional heat-tint bands along Z."""
    m, nt, b = _mat(name)
    b.inputs['Base Color'].default_value = (*col, 1); b.inputs['Metallic'].default_value = metal; b.inputs['Roughness'].default_value = rough
    if coat: b.inputs['Coat Weight'].default_value = coat
    tc = _p(nt, 'ShaderNodeTexCoord'); csrc = None
    vec = tc.outputs['Object']
    if stretch is not None:
        mp = _p(nt, 'ShaderNodeMapping'); mp.inputs['Scale'].default_value = stretch; nt.links.new(tc.outputs['Object'], mp.inputs['Vector']); vec = mp.outputs['Vector']
    if bump or rvar:
        nz = _p(nt, 'ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = bscale; nz.inputs['Detail'].default_value = detail
        nt.links.new(vec, nz.inputs['Vector'])
        if bump:
            bp = _p(nt, 'ShaderNodeBump'); bp.inputs['Strength'].default_value = bump; bp.inputs['Distance'].default_value = bdist
            nt.links.new(nz.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
        if rvar:
            rr = _p(nt, 'ShaderNodeMapRange'); rr.inputs[3].default_value = max(0.02, rough - rvar); rr.inputs[4].default_value = min(1.0, rough + rvar)
            nt.links.new(nz.outputs['Fac'], rr.inputs[0]); nt.links.new(rr.outputs[0], b.inputs['Roughness'])
    if tint2 is not None:
        nz2 = _p(nt, 'ShaderNodeTexNoise'); nz2.inputs['Scale'].default_value = tscale; nz2.inputs['Detail'].default_value = 4.0
        nt.links.new(tc.outputs['Object'], nz2.inputs['Vector'])
        mx = _p(nt, 'ShaderNodeMix', data_type='RGBA'); mx.inputs[6].default_value = (*col, 1); mx.inputs[7].default_value = (*tint2, 1)
        mr = _p(nt, 'ShaderNodeMapRange'); mr.inputs[1].default_value = tlo; mr.inputs[2].default_value = thi
        nt.links.new(nz2.outputs['Fac'], mr.inputs[0]); nt.links.new(mr.outputs[0], mx.inputs[0]); csrc = mx.outputs[2]
    if zbands:
        sx = _p(nt, 'ShaderNodeSeparateXYZ'); nt.links.new(tc.outputs['Object'], sx.inputs[0])
        for (zc, wdt, c2, k) in zbands:
            sb = _p(nt, 'ShaderNodeMath', operation='SUBTRACT'); nt.links.new(sx.outputs['Z'], sb.inputs[0]); sb.inputs[1].default_value = zc
            ab = _p(nt, 'ShaderNodeMath', operation='ABSOLUTE'); nt.links.new(sb.outputs[0], ab.inputs[0])
            mr = _p(nt, 'ShaderNodeMapRange'); mr.interpolation_type = 'SMOOTHSTEP'
            mr.inputs[1].default_value = wdt; mr.inputs[2].default_value = 0.0; mr.inputs[3].default_value = 0.0; mr.inputs[4].default_value = k
            nt.links.new(ab.outputs[0], mr.inputs[0])
            mx = _p(nt, 'ShaderNodeMix', data_type='RGBA'); mx.inputs[7].default_value = (*c2, 1)
            if csrc is None: mx.inputs[6].default_value = (*col, 1)
            else: nt.links.new(csrc, mx.inputs[6])
            nt.links.new(mr.outputs[0], mx.inputs[0]); csrc = mx.outputs[2]
    if grain is not None:                      # fine speckle (porous ceramic): (colour 2, scale, lo, hi)
        g2, gs, glo, ghi = grain
        nz3 = _p(nt, 'ShaderNodeTexNoise'); nz3.inputs['Scale'].default_value = gs; nz3.inputs['Detail'].default_value = 2.0
        nt.links.new(tc.outputs['Object'], nz3.inputs['Vector'])
        mr = _p(nt, 'ShaderNodeMapRange'); mr.inputs[1].default_value = glo; mr.inputs[2].default_value = ghi
        nt.links.new(nz3.outputs['Fac'], mr.inputs[0])
        mx = _p(nt, 'ShaderNodeMix', data_type='RGBA'); mx.inputs[7].default_value = (*g2, 1)
        if csrc is None: mx.inputs[6].default_value = (*col, 1)
        else: nt.links.new(csrc, mx.inputs[6])
        nt.links.new(mr.outputs[0], mx.inputs[0]); csrc = mx.outputs[2]
    if csrc is not None: nt.links.new(csrc, b.inputs['Base Color'])
    if bevel: add_bevel(m, bevel)
    return m


M = {}


def mats():
    if M: return M
    straw, blue = (0.50, 0.40, 0.24), (0.30, 0.31, 0.40)
    bands = [(SH_Z1 + 3, 34.0, straw, 0.55), (SH_Z0 - 3, 34.0, straw, 0.50), (150.0, 30.0, blue, 0.35), (-232.0, 26.0, blue, 0.28)]
    M['ss'] = mat_surf('ss', (0.62, 0.62, 0.60), 0.34, 1.0, bump=0.10, bscale=0.9, bdist=0.04, tint2=(0.52, 0.50, 0.45), tscale=0.03, bevel=0.3,
                       zbands=bands, rvar=0.07, stretch=(1.0, 1.0, 0.08))
    M['ss_pipe'] = mat_surf('ss_pipe', (0.52, 0.50, 0.47), 0.36, 1.0, bump=0.10, bscale=1.2, bdist=0.04, tint2=(0.36, 0.33, 0.36), tscale=0.04, bevel=0.3, rvar=0.06)
    M['ss_in'] = mat_surf('ss_in', (0.235, 0.225, 0.215), 0.55, 0.85, bump=0.22, bscale=1.5, bdist=0.05, tint2=(0.17, 0.16, 0.15), tscale=0.035, tlo=0.3, thi=0.8)
    M['ss_in2'] = mat_surf('ss_in2', (0.46, 0.45, 0.43), 0.42, 1.0, bump=0.12, bscale=1.5, bdist=0.04, tint2=(0.36, 0.33, 0.29), tscale=0.03, tlo=0.3, thi=0.8)
    M['ss_cut'] = mat_surf('ss_cut', (0.82, 0.83, 0.85), 0.55, 0.25)
    M['flange'] = mat_surf('flange', (0.36, 0.36, 0.37), 0.42, 1.0, bump=0.2, bscale=2.0, bdist=0.04, tint2=(0.30, 0.26, 0.23), tscale=0.05, bevel=0.5)
    M['flange_cut'] = mat_section('flange_cut', (0.30, 0.31, 0.33), (0.13, 0.13, 0.15), 45, 2.2, axes='XZ')
    M['weld'] = mat_surf('weld', (0.30, 0.28, 0.27), 0.46, 1.0, bump=0.9, bscale=1.6, bdist=0.35, detail=3.0, tint2=(0.36, 0.30, 0.20), tscale=0.2)
    M['mat'] = mat_surf('mat', (0.83, 0.81, 0.74), 1.0, 0.0, bump=0.7, bscale=3.0, bdist=0.25, detail=8.0, tint2=(0.70, 0.66, 0.56), tscale=0.6, tlo=0.35, thi=0.75)
    M['doc'] = mat_surf('doc', (0.70, 0.66, 0.56), 0.92, 0.0, bump=0.5, bscale=14.0, bdist=0.03, tint2=(0.62, 0.57, 0.47), tscale=0.08, grain=((0.56, 0.52, 0.43), 24.0, 0.42, 0.72))
    M['doc_ch'] = mat_surf('doc_ch', (0.56, 0.52, 0.44), 0.95, 0.0, bump=0.5, bscale=14.0, bdist=0.03, grain=((0.44, 0.40, 0.33), 24.0, 0.42, 0.72))
    sic, sic2 = (0.105, 0.110, 0.112), (0.045, 0.048, 0.050)
    M['dpf'] = mat_surf('dpf', sic, 0.84, 0.0, bump=0.9, bscale=18.0, bdist=0.05, tint2=(0.085, 0.09, 0.092), tscale=0.08, grain=(sic2, 26.0, 0.40, 0.70))
    M['dpf_in'] = mat_surf('dpf_in', (0.082, 0.086, 0.088), 0.9, 0.0, bump=0.9, bscale=18.0, bdist=0.05, grain=(sic2, 26.0, 0.40, 0.70))
    M['dpf_out'] = mat_surf('dpf_out', (0.082, 0.086, 0.088), 0.9, 0.0, bump=0.9, bscale=18.0, bdist=0.05, grain=(sic2, 26.0, 0.40, 0.70))
    M['plug'] = mat_surf('plug', (0.30, 0.30, 0.29), 0.95, 0.0, bump=0.8, bscale=9.0, bdist=0.06, grain=((0.20, 0.20, 0.19), 14.0, 0.40, 0.72))
    M['cement'] = mat_surf('cement', (0.50, 0.49, 0.45), 0.95, 0.0, bump=0.7, bscale=6.0, bdist=0.06, tint2=(0.42, 0.41, 0.38), tscale=0.3, grain=((0.38, 0.37, 0.34), 10.0, 0.42, 0.74))
    M['cement_doc'] = mat_surf('cement_doc', (0.74, 0.71, 0.62), 0.95, 0.0, bump=0.4, bscale=6.0, bdist=0.04)
    M['dark'] = mat_surf('dark', (0.006, 0.006, 0.006), 1.0, 0.0)
    M['probe'] = mat_surf('probe', (0.70, 0.70, 0.70), 0.26, 1.0, bevel=0.2, tint2=(0.55, 0.47, 0.36), tscale=0.06)
    M['zinc'] = mat_surf('zinc', (0.72, 0.70, 0.62), 0.30, 1.0, bevel=0.35, rvar=0.05, bscale=3.0)
    M['steel_dk'] = mat_surf('steel_dk', (0.26, 0.26, 0.28), 0.40, 1.0, bevel=0.25)
    M['braid'] = mat_surf('braid', (0.74, 0.73, 0.68), 0.88, 0.0, bump=0.9, bscale=5.0, bdist=0.18, detail=1.0, tint2=(0.60, 0.59, 0.54), tscale=1.2)
    M['sleeve'] = mat_surf('sleeve', (0.03, 0.03, 0.033), 0.62, 0.0, bump=0.6, bscale=4.0, bdist=0.12, detail=1.0)
    M['rubber'] = mat_surf('rubber', (0.022, 0.022, 0.024), 0.58, 0.0, bump=0.15, bscale=1.2, bdist=0.05, bevel=0.3)
    M['plastic'] = mat_surf('plastic', (0.035, 0.035, 0.04), 0.40, 0.0, bump=0.12, bscale=10.0, bdist=0.02, bevel=0.45)
    M['plastic_gy'] = mat_surf('plastic_gy', (0.30, 0.31, 0.33), 0.45, 0.0, bevel=0.3)
    M['grommet'] = mat_surf('grommet', (0.09, 0.045, 0.03), 0.55, 0.0, bevel=0.3)
    M['pipe'] = mat_surf('pipe', (0.66, 0.66, 0.65), 0.27, 1.0, tint2=(0.52, 0.45, 0.34), tscale=0.04, rvar=0.05, bscale=2.0)
    M['brk'] = mat_surf('brk', (0.58, 0.58, 0.54), 0.38, 1.0, bump=0.08, bscale=2.0, bdist=0.03, bevel=0.35, tint2=(0.50, 0.47, 0.38), tscale=0.06)
    M['shield'] = mat_surf('shield', (0.76, 0.76, 0.74), 0.24, 1.0, bump=0.05, bscale=0.6, bdist=0.05, bevel=0.2)
    M['clamp'] = mat_surf('clamp', (0.22, 0.22, 0.24), 0.34, 1.0, bevel=0.2)
    M['brass'] = mat_surf('brass', (0.78, 0.60, 0.30), 0.3, 1.0)
    for nm, col in (('idR', (1, 0, 0)), ('idG', (0, 1, 0)), ('idB', (0, 0, 1)), ('idW', (1, 1, 1))):
        M[nm] = mat_emit_white(nm, col)
    return M


def mat_of(name):
    n = name
    if n.startswith(('t1_', 't2_', 't3_')):
        if '_probe' in n or '_tube' in n: return 'probe'
        if '_nut' in n: return 'zinc'
        if '_crimp' in n: return 'steel_dk'
        if '_cable' in n: return 'braid'
        if '_lock' in n: return 'plastic_gy'
        if '_boot' in n: return 'rubber'
        return 'plastic'
    if n.startswith('lam_'):
        if '_tip' in n or '_body' in n: return 'probe'
        if '_hex' in n: return 'zinc'
        if '_grommet' in n: return 'grommet'
        if '_cable' in n: return 'sleeve'
        if '_lock' in n: return 'plastic_gy'
        if '_boot' in n: return 'rubber'
        return 'plastic'
    if n.startswith('dps_pin'): return 'brass'
    if n.startswith('dps_bolt') or n.startswith('dps_spacer'): return 'zinc'
    if n.startswith('dps_'): return 'plastic'
    if n.startswith('brk_') or n in ('fbracket',): return 'brk'
    if n.startswith('shield'): return 'shield'
    if n.startswith('ppipe') or n.startswith('pbead'): return 'pipe'
    if n.startswith('pnut'): return 'zinc'
    if n.startswith('pclip') or n.startswith('hclamp'): return 'clamp'
    if n.startswith('hose'): return 'rubber'
    if n.startswith('weld'): return 'weld'
    if n == 'type_plate': return 'shield'
    return 'ss'


def set_simple(ob, key, ang=34):
    ob.data.materials.clear(); ob.data.materials.append(mats()[key]); smooth(ob, ang)


def shell_mats(ob, cut=True):
    """slot 0 shell outside, 1 section (y = 0), 2 inside before the filter (sooty), 3 pipes / cones (darker heat tint), 4 flange plate, 5 flange section,
    6 inside after the filter (clean)."""
    mm = mats(); me = ob.data
    me.materials.clear()
    for k in ('ss', 'ss_cut', 'ss_in', 'ss_pipe', 'flange', 'flange_cut', 'ss_in2'): me.materials.append(mm[k])
    for p in me.polygons:
        c, n = p.center, p.normal
        fl = c.x > OUT_X1 - 9.6 or c.x < IN_X0 + 8.8
        if cut and abs(c.y) < 2e-3 and n.y < -0.98:
            p.material_index = 5 if fl else 1; continue
        q = c + n * 0.7
        if inside_cavity(q, -0.15): p.material_index = 2 if c.z > DPF_Z0 + 20.0 else 6
        elif fl: p.material_index = 4
        elif c.z > SH_Z1 + 3.0 or c.z < SH_Z0 - 3.0: p.material_index = 3
        else: p.material_index = 0
    smooth(ob, 40)


# --------------------------------------------------------------------------- scene assembly
def build():
    t0 = time.time()
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene; sc.unit_settings.system = 'NONE'
    mm = mats()
    cols = {k: new_coll(k) for k in ('shell', 'mats', 'doc', 'dpf', 'acc', 'front')}
    print('shell...', flush=True)
    sh = build_shell()
    fr = dup(sh, 'shell_front'); cut_plane(fr, 'y-'); shell_mats(fr, cut=False); move_to(fr, cols['front'])
    cut_plane(sh, 'y+'); shell_mats(sh); move_to(sh, cols['shell'])
    for w in build_welds():
        f2 = dup(w, w.name + '_f'); cut_plane(f2, 'y-'); set_simple(f2, 'weld', 60); move_to(f2, cols['front'])
        cut_plane(w, 'y+'); set_simple(w, 'weld', 60); move_to(w, cols['shell'])
    for ob in build_front_details():
        set_simple(ob, mat_of(ob.name)); move_to(ob, cols['front'])
    print('mats + bricks...', time.time() - t0, flush=True)
    for nm, (z0, z1) in (('mat_dpf', (DPF_Z0, DPF_Z1)), ('mat_doc', (DOC_Z0, DOC_Z1))):
        o = revolve_z(nm, [(R_B + 0.05, z0 + 3.0), (R_SI - 0.05, z0 + 3.0), (R_SI - 0.05, z1 - 3.0), (R_B + 0.05, z1 - 3.0)], segs=144)
        cut_plane(o, 'y+'); set_simple(o, 'mat'); move_to(o, cols['mats'])
    lat = {}
    D, lat['dpf'] = honeycomb('dpf', R_B, DPF_Z0, DPF_Z1, DPF_P, DPF_W, nseg=DPF_NSEG, seam=DPF_SEAM, plug=DPF_PLUG)
    for k, ob in D.items():
        ob.data.materials.append(mm[{'wall': 'dpf', 'in': 'dpf_in', 'out': 'dpf_out', 'plug': 'plug', 'seam': 'cement', 'dark': 'dark'}[k]]); move_to(ob, cols['dpf'])
    C, lat['doc'] = honeycomb('doc', R_B, DOC_Z0, DOC_Z1, DOC_P, DOC_W, skin=1.4)
    for k, ob in C.items():
        ob.data.materials.append(mm[{'wall': 'doc', 'in': 'doc_ch', 'out': 'doc_ch', 'plug': 'plug', 'seam': 'cement_doc', 'dark': 'dark'}[k]]); move_to(ob, cols['doc'])
    print('sensors...', time.time() - t0, flush=True)
    A = temp_sensor('t1', T1_P, T1_D, T1_CAB) + temp_sensor('t2', T2_P, T2_D, T2_CAB) + temp_sensor('t3', T3_P, T3_D, T3_CAB)
    A += lambda_probe('lam', LAM_P, LAM_D, LAM_CAB) + build_dp_sensor() + build_back_bracket()
    for ob in A:
        set_simple(ob, mat_of(ob.name)); move_to(ob, cols['acc'])
    for ob in list(sc.collection.objects):
        if ob.type == 'MESH': print('  stray', ob.name); bpy.data.objects.remove(ob, do_unlink=True)
    world_and_lights(); make_cameras()
    r = sc.render; r.engine = 'CYCLES'; r.resolution_percentage = 100; r.film_transparent = True
    cy = sc.cycles; cy.device = 'CPU'; cy.samples = 64; cy.use_adaptive_sampling = True; cy.adaptive_threshold = 0.02
    cy.use_denoising = True; cy.denoiser = 'OPENIMAGEDENOISE'
    cy.max_bounces = 8; cy.glossy_bounces = 4; cy.diffuse_bounces = 3; cy.transmission_bounces = 2; cy.transparent_max_bounces = 4
    cy.caustics_reflective = False; cy.caustics_refractive = False
    sc.view_settings.view_transform = 'AgX'
    try: sc.view_settings.look = 'AgX - Medium High Contrast'
    except Exception: pass
    r.image_settings.file_format = 'PNG'; r.image_settings.color_mode = 'RGBA'; r.image_settings.color_depth = '16'
    json.dump(lat, open(os.path.join(OUT, 'lattice.json'), 'w'))
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, 'dpf.blend'))
    nf = sum(len(o.data.polygons) for o in bpy.data.objects if o.type == 'MESH')
    print('saved', len(bpy.data.objects), 'objects,', nf, 'faces in %.0fs' % (time.time() - t0))


# --------------------------------------------------------------------------- light + cameras
CAM = {'main': dict(yaw=-12.0, pitch=15.0, dist=2600.0, tgt=(2.0, 0.0, -15.0), field=720.0)}


def cam_dir(yaw, pitch):
    y, p = math.radians(yaw), math.radians(pitch)
    return Vector((math.sin(y) * math.cos(p), math.cos(y) * math.cos(p), -math.sin(p)))


def world_and_lights(yaw=CAM['main']['yaw']):
    sc = bpy.context.scene
    w = bpy.data.worlds.new('studio'); sc.world = w; w.use_nodes = True
    nt = w.node_tree; bg = nt.nodes['Background']
    tc = _p(nt, 'ShaderNodeTexCoord'); sx = _p(nt, 'ShaderNodeSeparateXYZ'); nt.links.new(tc.outputs['Generated'], sx.inputs[0])
    az = _p(nt, 'ShaderNodeMath', operation='ARCTAN2'); nt.links.new(sx.outputs['Y'], az.inputs[0]); nt.links.new(sx.outputs['X'], az.inputs[1])
    el = sx.outputs['Z']
    def mr(src, a0, a1, b0=0.0, b1=1.0):
        m = _p(nt, 'ShaderNodeMapRange'); m.clamp = True
        m.inputs[1].default_value = a0; m.inputs[2].default_value = a1; m.inputs[3].default_value = b0; m.inputs[4].default_value = b1
        nt.links.new(src, m.inputs[0]); return m.outputs[0]
    def mul(a_, b_):
        m = _p(nt, 'ShaderNodeMath', operation='MULTIPLY'); nt.links.new(a_, m.inputs[0])
        if isinstance(b_, float): m.inputs[1].default_value = b_
        else: nt.links.new(b_, m.inputs[1])
        return m.outputs[0]
    def add(a_, b_):
        m = _p(nt, 'ShaderNodeMath', operation='ADD'); nt.links.new(a_, m.inputs[0]); nt.links.new(b_, m.inputs[1]); return m.outputs[0]
    d = cam_dir(yaw, 0)
    cam_back = math.atan2(-d.y, -d.x)          # azimuth of the camera position seen from the object
    def box_light(center, half, e0, e1, gain):
        dd = _p(nt, 'ShaderNodeMath', operation='SUBTRACT'); nt.links.new(az.outputs[0], dd.inputs[0]); dd.inputs[1].default_value = center
        wr = _p(nt, 'ShaderNodeMath', operation='WRAP'); nt.links.new(dd.outputs[0], wr.inputs[0]); wr.inputs[1].default_value = PI; wr.inputs[2].default_value = -PI
        ab = _p(nt, 'ShaderNodeMath', operation='ABSOLUTE'); nt.links.new(wr.outputs[0], ab.inputs[0])
        h = mr(ab.outputs[0], half, half * 0.55, 0.0, 1.0)
        v = mul(mr(el, e0, e0 + 0.08), mr(el, e1, e1 - 0.08))
        return mul(mul(h, v), gain)
    L = box_light(cam_back, math.radians(13), -0.35, 0.70, 2.6)
    L = add(L, box_light(cam_back + math.radians(68), math.radians(9), -0.25, 0.75, 2.0))
    L = add(L, box_light(cam_back - math.radians(72), math.radians(8), -0.25, 0.75, 1.7))
    L = add(L, box_light(cam_back + math.radians(180), math.radians(25), -0.10, 0.60, 0.9))
    L = add(L, mul(mr(el, 0.80, 0.95), 1.5))
    base = mr(el, -0.6, 0.9, 0.02, 0.20)
    tot = add(L, base)
    nt.links.new(tot, bg.inputs['Color']); bg.inputs['Strength'].default_value = 1.0
    for name, rot, en, ang in (('key', (math.radians(50), 0, math.radians(-34)), 2.5, 9),
                               ('rim', (math.radians(66), 0, math.radians(150)), 1.6, 6),
                               ('fill', (math.radians(80), 0, math.radians(32)), 0.75, 30),
                               ('fill_r', (math.radians(62), 0, math.radians(60)), 1.0, 14),
                               ('low', (math.radians(80), 0, math.radians(-8)), 0.9, 16)):
        ld = bpy.data.lights.new(name, 'SUN'); ld.energy = en; ld.angle = math.radians(ang)
        lo = bpy.data.objects.new(name, ld); lo.rotation_euler = rot; sc.collection.objects.link(lo)


def make_cameras():
    sc = bpy.context.scene
    for name, spec in CAM.items():
        cd = bpy.data.cameras.new('cam_' + name); cd.sensor_fit = 'HORIZONTAL'; cd.sensor_width = 36.0; cd.sensor_height = 36.0
        cd.clip_start = 10.0; cd.clip_end = 9000.0
        co = bpy.data.objects.new('cam_' + name, cd); sc.collection.objects.link(co)
        d = cam_dir(spec['yaw'], spec['pitch']); tgt = Vector(spec['tgt'])
        co.location = tgt - d * spec['dist']
        co.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
        cd.lens = 36.0 * spec['dist'] / spec['field']


# --------------------------------------------------------------------------- rendering
BASE = 2160               # T1 plate size (square); tiers multiply it
SEC = ['shell', 'mats', 'doc', 'dpf', 'acc']


def setup_layer(vis, hold=(), vt='AgX'):
    sc = bpy.context.scene
    for c in bpy.data.collections:
        c.hide_render = not (c.name in vis or c.name in hold)
        for ob in c.objects:
            ob.is_holdout = c.name in hold
    sc.view_settings.view_transform = vt
    if vt == 'Standard': sc.view_settings.look = 'None'


def set_crop(tier, crop):
    """crop = (x0, y0, x1, y1) in pixels of the tier-size image (y down)."""
    sc = bpy.context.scene; r = sc.render; S = BASE * tier
    r.resolution_x = S; r.resolution_y = S
    if crop:
        x0, y0, x1, y1 = crop
        r.use_border = True; r.use_crop_to_border = True
        r.border_min_x = x0 / S; r.border_max_x = x1 / S; r.border_min_y = 1 - y1 / S; r.border_max_y = 1 - y0 / S
    else:
        r.use_border = False


def crops():
    p = os.path.join(OUT, 'crops.json')
    return json.load(open(p)) if os.path.exists(p) else {}


TIERS = {'T1': 1, 'T2': 2, 'T8': 8, 'TA': 24, 'TB': 24}      # TA / TB: macro plates at the filter inlet / outlet end


def job_list():
    C = crops(); J = []
    J.append(('T1_sec', dict(tier=1, vis=SEC, samples=72)))
    J.append(('T1_front', dict(tier=1, vis=['front'], hold=SEC, samples=64)))
    for tn in ('T2', 'T8', 'TA', 'TB'):
        if tn in C: J.append((f'{tn}_sec', dict(tier=TIERS[tn], crop=C[tn], vis=SEC, samples=64 if tn in ('T2', 'T8') else 80)))
    for tn in ('T1', 'T2', 'T8', 'TA', 'TB'):
        if tn != 'T1' and tn not in C: continue
        cr = C.get(tn) if tn != 'T1' else None
        for k in ('A', 'B') + (('C', 'D') if tn in ('T1', 'T2') else ()):
            vis = {'A': ['dpf', 'doc', 'mats'], 'B': ['dpf'], 'C': ['acc'], 'D': ['acc']}[k]
            J.append((f'{tn}_id{k}', dict(tier=TIERS[tn], crop=cr, vis=vis, hold=[c for c in SEC if c not in vis], vt='Standard', samples=10, denoise=False, ids=k)))
    return J


_DP = ('dps_', 'hose', 'hclamp', 'ppipe', 'pbead', 'pnut')
IDS = {   # mask plates: pure R / G / B emission per group, everything else is a holdout
    'A': {'idR': lambda c, n: c == 'dpf', 'idG': lambda c, n: c == 'doc', 'idB': lambda c, n: c == 'mats'},
    'B': {'idR': lambda c, n: n.endswith('_in'), 'idG': lambda c, n: n.endswith('_out'), 'idB': lambda c, n: n.endswith('_plug')},
    'C': {'idR': lambda c, n: n.startswith(('t1_', 't2_', 't3_')), 'idG': lambda c, n: n.startswith('lam_'), 'idB': lambda c, n: n.startswith(_DP)},
    'D': {'idR': lambda c, n: n.startswith(('ppipe', 'pbead', 'pnut')), 'idG': lambda c, n: n.startswith(('hose', 'hclamp')), 'idB': lambda c, n: n.startswith('dps_')},
}


def render_job(name, spec, samples=None, pct=100, out=None):
    sc = bpy.context.scene
    sc.camera = bpy.data.objects['cam_main']
    setup_layer(spec['vis'], spec.get('hold', ()), spec.get('vt', 'AgX'))
    set_crop(spec.get('tier', 1), spec.get('crop'))
    sc.render.resolution_percentage = spec.get('pct', pct)
    sc.cycles.samples = samples or spec.get('samples', 64)
    sc.cycles.use_denoising = spec.get('denoise', True)
    ids = spec.get('ids')
    if ids:
        for c in spec['vis']:
            for ob in bpy.data.collections[c].objects:
                key = next((k for k, f in IDS[ids].items() if f(c, ob.name)), None)
                if key is None: ob.is_holdout = True
                else:
                    ob.data.materials.clear(); ob.data.materials.append(bpy.data.materials[key])
    sc.render.filepath = out or os.path.join(OUT, name + '.png')
    t = time.time()
    bpy.ops.render.render(write_still=True)
    print(f'DONE {name} {time.time() - t:.0f}s', flush=True)
    return True


def open_blend():
    bpy.ops.wm.open_mainfile(filepath=os.path.join(OUT, 'dpf.blend'))


def queue(only=None):
    for name, spec in job_list():
        if only and not any(name.startswith(o) or name.endswith(o) for o in only): continue
        if os.path.exists(os.path.join(OUT, name + '.png')): continue
        open_blend()        # fresh state per job (materials / holdouts)
        render_job(name, spec)


# --------------------------------------------------------------------------- projections for the compositor
def project(pts, size=BASE):
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene; co = bpy.data.objects['cam_main']
    sc.render.resolution_x = size; sc.render.resolution_y = size
    out = []
    for p in pts:
        v = world_to_camera_view(sc, co, Vector(p)); out.append([v.x * size, (1 - v.y) * size, v.z])
    return out


def info():
    open_blend()
    S1 = BASE
    def bbox(pts, tier, pad):
        q = project(pts, S1)
        xs = [p[0] * tier for p in q]; ys = [p[1] * tier for p in q]
        return [int(max(0, min(xs) - pad)), int(max(0, min(ys) - pad)), int(min(S1 * tier, max(xs) + pad)), int(min(S1 * tier, max(ys) + pad))]
    def boxpts(x0, x1, z0, z1, y0=0.0, y1=0.0): return [(x, y, z) for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)]
    C = {}
    C['T2'] = bbox(boxpts(-196.0, 176.0, -338.0, 322.0, 0.0, 60.0), 2, 20)
    xm = 9.5 * DPF_P + DPF_SEAM / 2                                             # macro centre: middle of the first segment right of the centre seam
    C['T8'] = bbox(boxpts(xm - 36.0, xm + 36.0, -52.0, 34.0, 0.0, 30.0), 8, 16)   # around the filter inlet face (zoom path to the macro)
    C['TA'] = bbox(boxpts(xm - 13.6, xm + 13.6, -24.0, 9.0, 0.0, 4.0), 24, 8)    # filter inlet end (wide enough for the 16:9 layout too)
    C['TB'] = bbox(boxpts(xm - 13.6, xm + 13.6, DPF_Z0 - 12.0, DPF_Z0 + 22.0, 0.0, 4.0), 24, 8)   # filter outlet end
    json.dump(C, open(os.path.join(OUT, 'crops.json'), 'w'), indent=1)
    A = {   # 3D anchors (mm)
        'inlet': (IN_X0 - 2.0, 0.0, IN_PZ), 'outlet': (OUT_X1 + 2.0, 0.0, OUT_PZ), 'vband': (IN_X0 + 2.0, 0.0, IN_PZ + 40.0),
        'doc': (-30.0, 0.0, 60.0), 'doc_top': (20.0, 30.0, DOC_Z1), 'dpf': (30.0, 0.0, -95.0), 'dpf_top': (-20.0, 30.0, 0.0),
        'mat_doc': (R_B + 2.5, 0.0, 70.0), 'mat_dpf': (-(R_B + 2.5), 0.0, -120.0), 'shell': (R_SO, 0.0, -40.0), 'shell_l': (-R_SO, 0.0, -60.0),
        'gap': (0.0, 20.0, 10.0), 'cone_in': (40.0, 0.0, 140.0), 'cone_out': (-30.0, 0.0, -222.0), 'seam': (0.0, 0.0, -60.0),
        't1': along(T1_P, T1_D, 16.0), 't2': along(T2_P, T2_D, 16.0), 't3': along(T3_P, T3_D, 16.0), 'lam': along(LAM_P, LAM_D, 30.0),
        't1_tip': along(T1_P, T1_D, -40.0), 't2_tip': along(T2_P, T2_D, -40.0), 't3_tip': along(T3_P, T3_D, -40.0), 'lam_tip': along(LAM_P, LAM_D, -18.0),
        'p1': (P1_P[0] + 13.0, Y_P, 10.0), 'p2': (P2_P[0] + 13.0, Y_P, -216.0), 'pipe1': (PX1, Y_P, 50.0), 'pipe2': (PX2, Y_P, -120.0),
        'hose1': hose1_path()[12], 'hose2': hose2_path()[12], 'dps': (SENS_C[0], SENS_C[1] - 13.0, SENS_C[2]), 'dps_sock': (SENS_C[0] + 40.0, SENS_C[1], SENS_C[2] + 1.0),
        'shield': (87.0, 6.0, 226.0), 'brk': (-126.0, 36.0, -115.0), 'plug_in': (0.0, 0.0, -3.0), 'plug_out': (0.0, 0.0, DPF_Z0 + 3.0),
    }
    res = {'crops': C, 'base': S1, 'tiers': TIERS, 'anch': {k: project([p], S1)[0] for k, p in A.items()}}
    res['paths3d'] = {'p1': p1_path(), 'p2': p2_path(), 'hose1': hose1_path(), 'hose2': hose2_path(),
                      'in_c': inlet_path(SH_Z1 + 8.0, IN_X0 - 30.0), 'out_c': outlet_path(SH_Z0 - 8.0, OUT_X1 + 30.0)}
    res['cab'] = {'t1': T1_CAB + [along(T1_P, T1_D, -46.0), along(T1_P, T1_D, 10.0)], 't2': T2_CAB + [along(T2_P, T2_D, -46.0), along(T2_P, T2_D, 10.0)],
                  't3': T3_CAB + [along(T3_P, T3_D, -46.0), along(T3_P, T3_D, 10.0)], 'lam': LAM_CAB + [along(LAM_P, LAM_D, -24.0), along(LAM_P, LAM_D, 12.0)]}
    co = bpy.data.objects['cam_main']
    res['M'] = [list(r) for r in co.matrix_world.inverted()]
    res['lens'] = co.data.lens; res['sensor'] = co.data.sensor_width
    res['dims'] = dict(R_B=R_B, R_SI=R_SI, R_SO=R_SO, DPF_Z0=DPF_Z0, DPF_Z1=DPF_Z1, DOC_Z0=DOC_Z0, DOC_Z1=DOC_Z1, SH_Z0=SH_Z0, SH_Z1=SH_Z1,
                       R_IN=R_IN, R_OUT=R_OUT, IN_Z=IN_Z, IN_R=IN_R, IN_PZ=IN_PZ, IN_X0=IN_X0, OUT_Z=OUT_Z, OUT_R=OUT_R, OUT_PZ=OUT_PZ, OUT_X1=OUT_X1,
                       Y_P=Y_P, Y_S=Y_S, PX1=PX1, PX2=PX2, PIPE_TOP=PIPE_TOP, PORT_X1=PORT_X1, PORT_X2=PORT_X2, PORT_Z=PORT_Z, SENS_C=SENS_C,
                       DPF_P=DPF_P, DPF_W=DPF_W, DPF_SEAM=DPF_SEAM, DPF_PLUG=DPF_PLUG, DOC_P=DOC_P, DOC_W=DOC_W, XM=xm,
                       OUTER=OUTER, INNER=INNER, T1_P=T1_P, T2_P=T2_P, T3_P=T3_P, LAM_P=LAM_P, P1_P=P1_P, P2_P=P2_P, T1_D=T1_D, T2_D=T2_D, T3_D=T3_D, LAM_D=LAM_D)
    res['lattice'] = json.load(open(os.path.join(OUT, 'lattice.json')))
    json.dump(res, open(os.path.join(OUT, 'info.json'), 'w'))
    print('crops', C)


def look(view, up, field, size, spp, out, vis='shell,mats,doc,dpf,acc,front', tgt='2,0,-15', dist='2600'):
    """render from an arbitrary direction (view = direction the camera looks along, up = screen-up vector)."""
    open_blend()
    sc = bpy.context.scene
    d = Vector([float(v) for v in view.split(',')]).normalized(); u = Vector([float(v) for v in up.split(',')]).normalized()
    t = Vector([float(v) for v in tgt.split(',')]); D = float(dist)
    cd = bpy.data.cameras.new('cam_look'); cd.sensor_fit = 'HORIZONTAL'; cd.sensor_width = 36.0; cd.clip_start = 10.0; cd.clip_end = 9000.0
    co = bpy.data.objects.new('cam_look', cd); sc.collection.objects.link(co)
    co.location = t - d * D
    zc = -d; xc = u.cross(zc).normalized(); yc = zc.cross(xc)
    co.rotation_euler = Matrix((xc, yc, zc)).transposed().to_euler()
    cd.lens = 36.0 * D / float(field)
    sc.camera = co
    setup_layer(vis.split(','), (), 'AgX')
    try: sc.view_settings.look = 'AgX - Medium High Contrast'
    except Exception: pass
    r = sc.render; r.resolution_x = int(size); r.resolution_y = int(size); r.use_border = False; r.resolution_percentage = 100
    r.film_transparent = False
    sc.cycles.samples = int(spp); sc.cycles.use_denoising = True
    r.filepath = out
    t0 = time.time(); bpy.ops.render.render(write_still=True); print('look done %.0fs' % (time.time() - t0))


def prev(tier, crop, vis, pct, spp, out, hold=''):
    open_blend()
    spec = dict(tier=int(tier), crop=[int(v) for v in crop.split(',')] if crop else None, vis=vis.split(','), hold=hold.split(',') if hold else [])
    render_job('prev', spec, int(spp), int(pct), out)


if __name__ == '__main__':
    a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    if a[0] == 'build': build()
    elif a[0] == 'render':
        open_blend(); J = dict(job_list())
        render_job(a[1], J[a[1]], int(a[2]) if len(a) > 2 else None, int(a[3]) if len(a) > 3 else 100, a[4] if len(a) > 4 else None)
    elif a[0] == 'queue': queue(only=a[1:] or None)
    elif a[0] == 'info': info()
    elif a[0] == 'prev': prev(*a[1:])
    elif a[0] == 'look': look(*a[1:])
