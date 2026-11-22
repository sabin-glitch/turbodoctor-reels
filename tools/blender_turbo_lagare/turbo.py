"""Turbo Doctor - passenger-car diesel VNT turbocharger in Blender, in section, two bearing systems.

Units: 1 BU = 1 mm. Shaft axis = X (compressor at -X, turbine at +X), Z up.
Section plane y = 0: the back half (y >= 0) stays, the camera looks from the -Y side.
Variant A = two full-floating bushings (rotate at ~1/2 shaft speed, Garrett), circlips, separate thrust bearing.
Variant B = one-piece semi-floating bearing held by an anti-rotation pin (does not rotate), same thrust bearing.
Clearances are exaggerated so the oil films can be seen (inner 0.4 mm, outer 0.8 mm A / 0.5 mm B).

  python turbo.py build                         -> out/turbo.blend
  python turbo.py render <job> [samples] [pct]  -> out/<job>.png   (jobs in JOBS)
  python turbo.py queue [first] [last]          -> renders every job not yet on disk
  python turbo.py info                          -> out/info.json (camera projections, crops, anchors)
"""
import bpy, bmesh, math, json, os, sys, time
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get('TURBO_OUT', os.path.join(HERE, 'out'))
os.makedirs(OUT, exist_ok=True)
SEG = 128
PI = math.pi

# --------------------------------------------------------------------------- mesh helpers
def mesh_obj(name, verts, faces, coll=None):
    me = bpy.data.meshes.new(name)
    me.from_pydata([tuple(map(float, v)) for v in verts], [], faces)
    me.validate()
    bm = bmesh.new(); bm.from_mesh(me)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me)
    (coll or bpy.context.scene.collection).objects.link(ob)
    return ob


def revolve_x(name, prof, segs=SEG, coll=None):
    """prof: closed polygon of (x, r); revolved around the X axis (y = r cos a, z = r sin a)."""
    verts, faces, idx = [], [], []
    for x, r in prof:
        if r < 1e-9:
            idx.append([len(verts)] * segs); verts.append((x, 0.0, 0.0))
        else:
            b = len(verts)
            for k in range(segs):
                a = 2 * PI * (k + 0.5) / segs
                verts.append((x, r * math.cos(a), r * math.sin(a)))
            idx.append([b + k for k in range(segs)])
    n = len(prof)
    for i in range(n):
        j = (i + 1) % n
        for k in range(segs):
            k2 = (k + 1) % segs
            q = []
            for v in (idx[i][k], idx[j][k], idx[j][k2], idx[i][k2]):
                if v not in q: q.append(v)
            if len(q) >= 3: faces.append(q)
    return mesh_obj(name, verts, faces, coll)


def ring(name, x0, x1, r0, r1, segs=SEG):
    return revolve_x(name, [(x0, r0), (x1, r0), (x1, r1), (x0, r1)], segs)


def frame_of(d):
    d = Vector(d).normalized()
    t = Vector((1, 0, 0)) if abs(d.x) < 0.9 else Vector((0, 1, 0))
    u = d.cross(t).normalized(); v = d.cross(u)
    return u, v, d


def cyl(name, p0, p1, r, segs=48, r1=None):
    p0, p1 = Vector(p0), Vector(p1); r1 = r if r1 is None else r1
    u, v, d = frame_of(p1 - p0)
    verts, faces = [], []
    for p, rr in ((p0, r), (p1, r1)):
        for k in range(segs):
            a = 2 * PI * (k + 0.5) / segs
            verts.append(tuple(p + (u * math.cos(a) + v * math.sin(a)) * rr))
    c0 = len(verts); verts.append(tuple(p0)); c1 = len(verts); verts.append(tuple(p1))
    for k in range(segs):
        k2 = (k + 1) % segs
        faces.append([k, k2, segs + k2, segs + k])
        faces.append([c0, k2, k]); faces.append([c1, segs + k, segs + k2])
    return mesh_obj(name, verts, faces)


def box(name, x0, x1, y0, y1, z0, z1):
    v = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    f = [[0, 3, 2, 1], [4, 5, 6, 7], [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7]]
    return mesh_obj(name, v, f)


def extrude(name, pts2, axis, a0, a1):
    """closed 2D polygon extruded along an axis. axis 'z': pts=(x,y); 'x': pts=(y,z); 'y': pts=(x,z)."""
    n = len(pts2)
    def P(p, a):
        if axis == 'z': return (p[0], p[1], a)
        if axis == 'x': return (a, p[0], p[1])
        return (p[0], a, p[1])
    verts = [P(p, a0) for p in pts2] + [P(p, a1) for p in pts2]
    faces = [list(range(n))[::-1], [n + i for i in range(n)]]
    for i in range(n):
        j = (i + 1) % n
        faces.append([i, j, n + j, n + i])
    return mesh_obj(name, verts, faces)


def stadium(cx, cy, hx, hy, n=24):
    """rounded rectangle (half sizes hx >= hy), ends are half circles."""
    r = hy; L = hx - r; pts = []
    for k in range(n + 1):
        a = -PI / 2 + PI * k / n; pts.append((cx + L + r * math.cos(a), cy + r * math.sin(a)))
    for k in range(n + 1):
        a = PI / 2 + PI * k / n; pts.append((cx - L + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def rrect(cx, cy, hx, hy, r, n=8):
    pts = []
    for (sx, sy, a0) in ((1, 1, 0), (-1, 1, 90), (-1, -1, 180), (1, -1, 270)):
        ox, oy = cx + sx * (hx - r), cy + sy * (hy - r)
        for k in range(n + 1):
            a = math.radians(a0 + 90 * k / n); pts.append((ox + r * math.cos(a), oy + r * math.sin(a)))
    return pts


def torus_x(name, x, R, r, seg=96, seg2=16):
    verts, faces = [], []
    for i in range(seg):
        a = 2 * PI * (i + 0.5) / seg
        for j in range(seg2):
            b = 2 * PI * j / seg2
            rr = R + r * math.cos(b)
            verts.append((x + r * math.sin(b), rr * math.cos(a), rr * math.sin(a)))
    for i in range(seg):
        i2 = (i + 1) % seg
        for j in range(seg2):
            j2 = (j + 1) % seg2
            faces.append([i * seg2 + j, i2 * seg2 + j, i2 * seg2 + j2, i * seg2 + j2])
    return mesh_obj(name, verts, faces)


def prism_x(name, n, apothem, x0, x1, rot=0.0):
    R = apothem / math.cos(PI / n)
    v = []
    for x in (x0, x1):
        for k in range(n):
            a = rot + 2 * PI * k / n
            v.append((x, R * math.cos(a), R * math.sin(a)))
    v.append((x0, 0, 0)); v.append((x1, 0, 0)); c0, c1 = 2 * n, 2 * n + 1
    f = []
    for k in range(n):
        k2 = (k + 1) % n
        f.append([k, k2, n + k2, n + k]); f.append([c0, k2, k]); f.append([c1, n + k, n + k2])
    return mesh_obj(name, v, f)


def sweep(name, pts, rads, segs=64, caps=True):
    """tube with circular sections along a polyline (parallel-transport frames)."""
    P = [Vector(p) for p in pts]; n = len(P)
    T = []
    for i in range(n):
        a = P[min(i + 1, n - 1)] - P[max(i - 1, 0)]; T.append(a.normalized())
    u0, v0, _ = frame_of(T[0]); U = [u0]
    for i in range(1, n):
        u = U[-1] - T[i] * U[-1].dot(T[i]); U.append(u.normalized())
    verts, faces = [], []
    for i in range(n):
        u = U[i]; v = T[i].cross(u)
        for k in range(segs):
            a = 2 * PI * (k + 0.5) / segs
            verts.append(tuple(P[i] + (u * math.cos(a) + v * math.sin(a)) * rads[i]))
    for i in range(n - 1):
        for k in range(segs):
            k2 = (k + 1) % segs
            faces.append([i * segs + k, i * segs + k2, (i + 1) * segs + k2, (i + 1) * segs + k])
    if caps:
        c0 = len(verts); verts.append(tuple(P[0])); c1 = len(verts); verts.append(tuple(P[-1]))
        for k in range(segs):
            k2 = (k + 1) % segs
            faces.append([c0, k2, k]); faces.append([c1, (n - 1) * segs + k, (n - 1) * segs + k2])
    return mesh_obj(name, verts, faces)


def apply_bool(ob, cutter, op='DIFFERENCE'):
    m = ob.modifiers.new('b', 'BOOLEAN'); m.operation = op; m.object = cutter; m.solver = 'MANIFOLD'
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(ob.evaluated_get(dg))
    ob.modifiers.clear(); old = ob.data; ob.data = me; bpy.data.meshes.remove(old)


def bool_many(ob, cutters, op='DIFFERENCE'):
    for c in cutters:
        apply_bool(ob, c, op)
    for c in cutters:
        bpy.data.objects.remove(c, do_unlink=True)
    return ob


def union(name, obs):
    base = obs[0]; base.name = name
    return bool_many(base, obs[1:], 'UNION')


def dup(ob, name):
    o2 = ob.copy(); o2.data = ob.data.copy(); o2.name = name
    bpy.context.scene.collection.objects.link(o2)
    return o2


def smooth(ob, ang=34):
    me = ob.data
    for p in me.polygons: p.use_smooth = True
    try:
        me.set_sharp_from_angle(angle=math.radians(ang))
    except Exception:
        pass


def rot_x(ob, ang):
    ob.data.transform(Matrix.Rotation(ang, 4, 'X'))


# --------------------------------------------------------------------------- blades
def sheet_solid(name, A, B):
    """A, B: [ns][nt] lists of 3D points (two faces of a thin blade) -> closed solid."""
    ns, nt = len(A), len(A[0])
    verts = [p for row in A for p in row] + [p for row in B for p in row]
    off = ns * nt
    ia = lambda i, j: i * nt + j
    ib = lambda i, j: off + i * nt + j
    f = []
    for i in range(ns - 1):
        for j in range(nt - 1):
            f.append([ia(i, j), ia(i + 1, j), ia(i + 1, j + 1), ia(i, j + 1)])
            f.append([ib(i, j), ib(i, j + 1), ib(i + 1, j + 1), ib(i + 1, j)])
    for j in range(nt - 1):
        f.append([ia(0, j), ia(0, j + 1), ib(0, j + 1), ib(0, j)])
        f.append([ia(ns - 1, j), ib(ns - 1, j), ib(ns - 1, j + 1), ia(ns - 1, j + 1)])
    for i in range(ns - 1):
        f.append([ia(i, 0), ib(i, 0), ib(i + 1, 0), ia(i + 1, 0)])
        f.append([ia(i, nt - 1), ia(i + 1, nt - 1), ib(i + 1, nt - 1), ib(i, nt - 1)])
    return mesh_obj(name, verts, f)


def blade(name, hub, shr, theta, thick, t0, phi, ns=9, nt=34, s0=-0.06):
    """hub(t), shr(t) -> (x, r); theta(t, s) -> rad; thick(s, tt) -> mm; blade from t0..1, rotated by phi."""
    A, B = [], []
    for i in range(ns):
        s = s0 + (1 - s0) * i / (ns - 1)
        ra, rb = [], []
        for j in range(nt):
            tt = j / (nt - 1); t = t0 + (1 - t0) * tt
            hx, hr = hub(t); sx, sr = shr(t)
            x = hx + (sx - hx) * s; r = hr + (sr - hr) * s
            th = theta(t, s) + phi; dt = thick(max(s, 0.0), tt) / (2 * r)
            ra.append((x, r * math.cos(th - dt), r * math.sin(th - dt)))
            rb.append((x, r * math.cos(th + dt), r * math.sin(th + dt)))
        A.append(ra); B.append(rb)
    return sheet_solid(name, A, B)


def edge_profile(tt, le=0.10, te_k=0.45):
    return (0.28 + 0.72 * min(1.0, (tt / le) ** 0.5)) * (1 - te_k * tt ** 4)


# compressor wheel meridional lines (x, r)
def c_hub(t): return (-66.0 + 25.5 * math.sin(t * PI / 2), 25.0 - 19.0 * math.cos(t * PI / 2))
def c_shr(t): return (-66.0 + 21.5 * math.sin(t * PI / 2), 25.0 - 7.0 * math.cos(t * PI / 2))
def c_theta(t, s): return -(1.0 * (1 - (1 - t) ** 3) + 0.22 * t ** 3) - 0.05 * s * (1 - t)
# turbine wheel meridional lines
def t_hub(t): return (66.0 - 27.4 * math.cos(t * PI / 2), 21.5 - 15.0 * math.sin(t * PI / 2))
def t_shr(t): return (66.0 - 20.5 * math.cos(t * PI / 2), 21.5 - 3.0 * math.sin(t * PI / 2))
def t_theta(t, s):
    u = max(0.0, (t - 0.34) / 0.66)
    return -0.78 * u ** 2.1 * (0.85 + 0.15 * s)


def build_compressor_wheel():
    prof = [(-67.6, 0.0), (-67.6, 4.3), (-67.0, 5.3)]
    for k in range(0, 29):
        prof.append(c_hub(k / 28))
    prof += [(-40.1, 25.0), (-39.7, 24.5), (-39.5, 23.6), (-39.5, 8.0), (-39.3, 6.6), (-39.3, 0.0)]
    hub = revolve_x('cw_hub', prof, segs=160)
    parts = [hub]
    for k in range(6):
        ph = 2 * PI * k / 6
        parts.append(blade(f'cw_main{k}', c_hub, c_shr, c_theta, lambda s, tt: (1.35 * (1 - s) + 0.62 * s) * edge_profile(tt), 0.0, ph, nt=40))
        parts.append(blade(f'cw_spl{k}', c_hub, c_shr, c_theta, lambda s, tt: (1.25 * (1 - s) + 0.58 * s) * edge_profile(tt, 0.14), 0.36, ph + PI / 6, nt=28))
    ob = join(parts, 'compressor_wheel')
    return ob


def build_turbine_wheel():
    prof = [(37.8, 0.0), (37.8, 20.9), (38.05, 21.45)]
    for k in range(0, 29):
        x, r = t_hub(k / 28); prof.append((x + 0.6 * (1 - k / 28) ** 3, r))
    prof += [(66.6, 6.2), (67.9, 4.9), (68.6, 2.8), (68.8, 0.0)]
    hub = revolve_x('tw_hub', prof, segs=160)
    # scallops in the back disc between the blades
    cut = []
    for k in range(10):
        a = 2 * PI * (k + 0.5) / 10 + 0.02
        cut.append(cyl(f'tw_sc{k}', (37.0, 27.2 * math.cos(a), 27.2 * math.sin(a)), (40.2, 27.2 * math.cos(a), 27.2 * math.sin(a)), 8.6, segs=48))
    bool_many(hub, cut)
    parts = [hub]
    for k in range(10):
        ph = 2 * PI * k / 10
        parts.append(blade(f'tw_b{k}', lambda t: (t_hub(t)[0] + 0.6 * (1 - t) ** 3, t_hub(t)[1]), t_shr, t_theta,
                           lambda s, tt: (1.45 * (1 - s) + 0.78 * s) * edge_profile(tt, 0.06, 0.3), 0.0, ph, nt=40))
    return join(parts, 'turbine_wheel')


def join(obs, name):
    bpy.ops.object.select_all(action='DESELECT')
    for o in obs: o.select_set(True)
    bpy.context.view_layer.objects.active = obs[0]
    bpy.ops.object.join(); ob = bpy.context.view_layer.objects.active; ob.name = name; ob.data.name = name
    return ob


# --------------------------------------------------------------------------- parts
def build_rotor():
    R = {}
    shaft = revolve_x('shaft', [(-73.5, 0.0), (-73.5, 2.1), (-73.0, 2.5), (-58.0, 2.5), (-57.6, 3.0), (-24.3, 3.0), (-24.0, 3.7), (-23.6, 4.0),
                                (-9.2, 4.0), (-8.6, 3.8), (8.6, 3.8), (9.2, 4.0), (23.9, 4.0), (24.35, 4.6), (24.55, 7.6), (24.9, 8.0),
                                (27.9, 8.0), (27.9, 7.0), (29.3, 7.0), (29.3, 8.0), (32.6, 8.0), (32.6, 7.3), (33.6, 7.3), (33.6, 8.0),
                                (37.4, 8.0), (38.0, 8.9), (38.0, 0.0)], segs=160)
    R['shaft'] = shaft
    R['compressor_wheel'] = build_compressor_wheel()
    nut = prism_x('nut', 6, 4.0, -72.6, -67.6, rot=PI / 6)
    ch = revolve_x('nut_ch', [(-72.6, 0), (-72.6, 3.9), (-72.0, 4.75), (-68.2, 4.75), (-67.6, 3.9), (-67.6, 0)], segs=96)
    apply_bool(nut, ch, 'INTERSECT'); bpy.data.objects.remove(ch, do_unlink=True)
    R['nut'] = nut
    R['turbine_wheel'] = build_turbine_wheel()
    return R


def build_rotor_cut():
    """rotating but axisymmetric -> can be shown in section"""
    C = {}
    C['collar'] = revolve_x('collar', [(-31.2, 3.0), (-31.2, 8.2), (-30.9, 8.5), (-29.3, 8.5), (-29.0, 8.2), (-29.0, 4.6), (-25.8, 4.6),
                                       (-25.8, 8.2), (-25.5, 8.5), (-24.3, 8.5), (-24.0, 8.2), (-24.0, 3.0)])
    C['flinger'] = revolve_x('flinger', [(-39.5, 3.0), (-39.5, 5.0), (-37.0, 5.0), (-37.0, 4.2), (-36.0, 4.2), (-36.0, 5.0), (-33.0, 5.0),
                                         (-33.0, 7.6), (-32.6, 8.0), (-31.6, 8.0), (-31.2, 7.6), (-31.2, 3.0)])
    return C


GAL_Z = 12.5          # oil gallery height
FEED_X = 16.0         # journal centres at +-16


def build_chra(var):
    body = revolve_x('chra_' + var, [(-26.0, 0.0), (-26.0, 30.0), (-21.5, 30.0), (-20.5, 28.6), (-19.5, 21.5), (19.0, 21.5), (20.6, 23.2),
                                     (22.4, 31.2), (23.5, 34.5), (31.0, 34.5), (31.0, 0.0)], segs=160)
    adds = [cyl('in_boss', (0, 0, 14.0), (0, 0, 29.0), 9.5, segs=96),
            cyl('in_boss_base', (0, 0, 12.0), (0, 0, 23.0), 11.5, r1=9.5, segs=96),
            extrude('dr_neck', rrect(0, 0, 15.0, 11.0, 4.0), 'z', -31.5, -14.0),
            extrude('dr_flange', stadium(0, 0, 21.5, 12.0), 'z', -36.0, -31.5)]
    for a in adds:
        apply_bool(body, a, 'UNION'); bpy.data.objects.remove(a, do_unlink=True)
    cut = [cyl('gal', (-26.3, 0, GAL_Z), (FEED_X + 1.6, 0, GAL_Z), 2.0, segs=40),
           cyl('in_bore', (0, 0, 29.3), (0, 0, GAL_Z - 0.5), 3.0, segs=48),
           cyl('in_cb', (0, 0, 29.3), (0, 0, 27.6), 5.2, segs=48),
           box('drain_cav', -23.5, 24.0, -15.5, 15.5, -29.0, -11.0),
           extrude('drain_out', rrect(0, 0, 12.0, 8.0, 3.0), 'z', -36.3, -28.0),
           cyl('dbolt1', (16.5, 0, -36.3), (16.5, 0, -30.0), 3.3, segs=32), cyl('dbolt2', (-16.5, 0, -36.3), (-16.5, 0, -30.0), 3.3, segs=32),
           ring('t_end', 22.2, 26.0, 0.0, 12.0) if False else revolve_x('t_end', [(22.1, 0.0), (22.1, 12.0), (26.0, 12.0), (26.0, 0.0)]),
           box('t_end_dn', 22.2, 26.0, -9.0, 9.0, -14.0, 0.5),
           revolve_x('t_wall', [(25.9, 0.0), (25.9, 8.2), (31.1, 8.2), (31.1, 0.0)]),
           revolve_x('c_cb', [(-26.1, 0.0), (-26.1, 9.5), (-22.2, 9.5), (-22.2, 0.0)]),
           box('c_cb_dn', -26.1, -22.4, -7.0, 7.0, -14.0, 0.5)]
    for sx in (-1, 1):
        cut.append(cyl(f'feed{sx}', (sx * FEED_X, 0, GAL_Z + 0.5), (sx * FEED_X, 0, 5.0), 1.2, segs=32))
    if var == 'A':
        cut += [revolve_x('boreA', [(-22.25, 0.0), (-22.25, 7.05), (22.25, 7.05), (22.25, 0.0)]),
                revolve_x('midA', [(-9.8, 0.0), (-9.8, 9.0), (9.8, 9.0), (9.8, 0.0)]),
                box('winA', -7.5, 7.5, -6.0, 6.0, -12.0, -5.0)]
        for x0, x1 in ((9.95, 10.8), (21.2, 22.05)):
            for sx in (-1, 1):
                a, b = sorted((sx * x0, sx * x1))
                cut.append(revolve_x(f'grv{a:.1f}', [(a, 0.0), (a, 7.95), (b, 7.95), (b, 0.0)]))
    else:
        cut += [revolve_x('boreB', [(-22.25, 0.0), (-22.25, 6.75), (22.25, 6.75), (22.25, 0.0)]),
                box('slotB1', 4.5, 9.5, -3.0, 3.0, -12.0, -5.0), box('slotB2', -9.5, -4.5, -3.0, 3.0, -12.0, -5.0)]
    bool_many(body, cut)
    if var == 'B':
        col = extrude('pin_col', rrect(0, 0, 3.6, 3.6, 1.2), 'z', -19.0, -9.5)
        apply_bool(body, col, 'UNION'); bpy.data.objects.remove(col, do_unlink=True)
        bool_many(body, [cyl('pin_hole', (0, 0, -19.5), (0, 0, -5.0), 1.25, segs=32)])
    return body


def build_internals(var):
    I = {}
    if var == 'A':
        for sx, nm in ((1, 'bush_t'), (-1, 'bush_c')):
            a, b = sorted((sx * 11.0, sx * 21.0))
            bu = revolve_x(nm, [(a, 4.7), (a + 0.3, 4.4), (b - 0.3, 4.4), (b, 4.7), (b, 5.95), (b - 0.3, 6.25), (a + 0.3, 6.25), (a, 5.95)])
            cut = []
            for k in range(4):
                an = PI / 4 + k * PI / 2
                cut.append(cyl(f'{nm}_h{k}', (sx * FEED_X, 3.8 * math.cos(an), 3.8 * math.sin(an)),
                               (sx * FEED_X, 6.7 * math.cos(an), 6.7 * math.sin(an)), 0.9, segs=24))
            bool_many(bu, cut)
            I[nm] = bu
        k = 0
        for x0, x1 in ((10.0, 10.75), (21.25, 22.0)):
            for sx in (-1, 1):
                a, b = sorted((sx * x0, sx * x1))
                I[f'clip{k}'] = revolve_x(f'clip{k}', [(a, 5.55), (b, 5.55), (b, 7.9), (a, 7.9)]); k += 1
    else:
        pr = [(-21.0, 4.75), (-21.0, 5.95), (-20.7, 6.25), (-17.0, 6.25), (-17.0, 5.85), (-15.0, 5.85), (-15.0, 6.25), (-11.0, 6.25),
              (-10.7, 6.0), (10.7, 6.0), (11.0, 6.25), (15.0, 6.25), (15.0, 5.85), (17.0, 5.85), (17.0, 6.25), (20.7, 6.25), (21.0, 5.95),
              (21.0, 4.75), (20.7, 4.4), (11.3, 4.4), (11.0, 4.6), (10.6, 5.0), (-10.6, 5.0), (-11.0, 4.6), (-11.3, 4.4), (-20.7, 4.4)]
        be = revolve_x('bearing_sf', pr)
        cut = []
        for sx in (-1, 1):
            for k in range(4):
                an = k * PI / 2
                cut.append(cyl(f'sf_h{sx}{k}', (sx * FEED_X, 3.8 * math.cos(an), 3.8 * math.sin(an)), (sx * FEED_X, 6.6 * math.cos(an), 6.6 * math.sin(an)), 0.85, segs=24))
            cut.append(cyl(f'sf_d{sx}', (sx * 7.0, 0, -4.4), (sx * 7.0, 0, -6.6), 0.8, segs=24))
        cut.append(cyl('sf_pin', (0, 0, -4.4), (0, 0, -6.6), 1.3, segs=32))
        bool_many(be, cut)
        I['bearing_sf'] = be
        I['pin'] = cyl('pin', (0, 0, -18.5), (0, 0, -5.15), 1.22, segs=40)
    # thrust bearing (bronze), oil deflector, piston rings
    tp = revolve_x('thrust_plate', [(-28.8, 5.0), (-28.8, 13.5), (-26.0, 13.5), (-26.0, 5.0)])
    lobe = extrude('tp_lobe', rrect(0, 12.0, 7.0, 4.6, 2.0), 'x', -28.8, -26.0)
    apply_bool(tp, lobe, 'UNION'); bpy.data.objects.remove(lobe, do_unlink=True)
    bool_many(tp, [cyl('tp_h1', (-25.9, 0, GAL_Z), (-27.4, 0, GAL_Z), 1.4, segs=24), cyl('tp_h2', (-27.4, 0, GAL_Z), (-27.4, 0, 4.0), 0.85, segs=24)])
    for k in range(6):       # shallow pad grooves on both faces
        an = PI / 6 + k * PI / 3
        for xa, xb in ((-28.95, -28.65), (-26.15, -25.85)):
            g = box(f'tpg{k}{xa}', xa, xb, -0.7, 0.7, 5.2, 11.0); rot_x(g, an - PI / 2)
            apply_bool(tp, g); bpy.data.objects.remove(g, do_unlink=True)
    I['thrust_plate'] = tp
    I['deflector'] = revolve_x('deflector', [(-29.6, 9.2), (-29.6, 17.5), (-28.8, 17.5), (-28.8, 9.2)])
    I['ring_t'] = revolve_x('ring_t', [(28.15, 7.15), (29.05, 7.15), (29.05, 8.15), (28.15, 8.15)])
    I['ring_c'] = revolve_x('ring_c', [(-36.9, 4.35), (-36.1, 4.35), (-36.1, 5.55), (-36.9, 5.55)])
    return I


def build_backplate():
    bp = revolve_x('backplate', [(-39.0, 5.6), (-33.6, 5.6), (-33.6, 10.2), (-29.6, 10.2), (-29.6, 17.6), (-26.0, 17.6), (-26.0, 30.6),
                                 (-29.0, 30.6), (-29.0, 46.0), (-36.6, 46.0), (-36.6, 40.3), (-39.0, 40.3)], segs=160)
    return bp


def comp_volute(r_of, segs_c=56):
    """centre-line of the compressor volute; returns (pts, rads) from phi0..phi1 (deg)."""
    def P(phi):
        r = r_of(phi); a = math.radians(phi)
        Rc = 37.5 + 0.6 * r; xv = -40.0 - r
        return (xv, Rc * math.cos(a), Rc * math.sin(a)), r
    return P


def build_comp_housing():
    core = revolve_x('comp_housing', [(-99.0, 0.0), (-99.0, 23.2), (-98.2, 24.2), (-74.0, 24.2), (-68.0, 27.0), (-60.0, 33.5), (-50.0, 37.5),
                                      (-42.0, 40.0), (-40.0, 49.5), (-29.0, 49.5), (-29.0, 0.0)], segs=160)
    rv = lambda phi: 2.6 + 10.2 * (phi / 360.0) ** 0.9
    VP = comp_volute(rv)
    def path(phi0, phi1, n, extra=0.0):
        pts, rs = [], []
        for i in range(n + 1):
            ph = phi0 + (phi1 - phi0) * i / n; p, r = VP(ph); pts.append(p); rs.append(r + extra)
        return pts, rs
    # outlet duct (tangential at phi = 360, the +Y side, going up)
    p_end, r_end = VP(360.0)
    p_b, _ = VP(359.0); tg = (Vector(p_end) - Vector(p_b)).normalized()
    duct = [tuple(Vector(p_end) + tg * d) for d in (0.0, 8.0, 16.0, 24.0, 32.0, 40.0, 48.0)]
    dr = [r_end + 0.5 * i / 6 for i in range(7)]
    shells = []
    pts, rs = path(10.0, 300.0, 70, 3.6); shells.append(sweep('cv_sh1', pts, rs))
    pts, rs = path(290.0, 360.0, 20, 3.6); pts += duct[1:]; rs += [r + 3.4 for r in dr[1:]]; shells.append(sweep('cv_sh2', pts, rs))
    for s in shells:
        apply_bool(core, s, 'UNION'); bpy.data.objects.remove(s, do_unlink=True)
    bead = sweep('cv_bead', [tuple(Vector(duct[-1]) - tg * 7.5), tuple(Vector(duct[-1]) - tg * 5.0)], [r_end + 0.5 + 4.9] * 2)
    apply_bool(core, bead, 'UNION'); bpy.data.objects.remove(bead, do_unlink=True)
    inbead = torus_x('in_bead', -93.5, 24.2, 1.5)
    apply_bool(core, inbead, 'UNION'); bpy.data.objects.remove(inbead, do_unlink=True)
    # cavities
    cav = [(-100.0, 0.0), (-100.0, 21.4), (-80.0, 20.6), (-72.0, 19.0), (-66.6, 18.45)]
    for k in range(0, 21):
        s = k / 20; cav.append((-66.0 + 21.5 * math.sin(s * PI / 2), 25.0 - 7.0 * math.cos(s * PI / 2) + 0.4))
    cav += [(-44.8, 26.3), (-44.8, 38.5), (-39.05, 38.5), (-39.05, 40.35), (-36.65, 40.35), (-36.65, 46.05), (-28.9, 46.05), (-28.9, 0.0)]
    cuts = [revolve_x('cv_cav', cav, segs=160)]
    pts, rs = path(8.0, 300.0, 70); cuts.append(sweep('cv_p1', pts, rs))
    pts, rs = path(290.0, 360.0, 20); pts += [tuple(Vector(duct[-1]) + tg * 2.0)]; rs += [dr[-1]]
    pts = pts[:-1] + duct[1:] + [tuple(Vector(duct[-1]) + tg * 2.0)]; rs = rs[:-1] + dr[1:] + [dr[-1]]
    cuts.append(sweep('cv_p2', pts, rs))
    # bolt bosses for the backplate clamp (6) at r = 47.5
    bool_many(core, cuts)
    return core, {'outlet_end': tuple(duct[-1]), 'outlet_dir': tuple(tg), 'VP': VP}


def build_turbine_housing():
    core = revolve_x('turbine_housing', [(31.0, 0.0), (31.0, 41.5), (36.0, 41.5), (38.5, 38.5), (45.0, 33.0), (52.0, 29.0), (60.0, 27.4),
                                         (72.0, 26.4), (79.0, 26.4), (79.0, 42.0), (86.0, 42.0), (86.0, 0.0)], segs=160)
    rv = lambda phi: 13.0 - 10.0 * (max(phi, 0.0) / 340.0) ** 0.85
    def VP(phi):
        r = rv(phi); a = math.radians(phi)
        Rc = 33.0 + 0.85 * r; xv = 43.0 + 0.6 * r
        return (xv, Rc * math.cos(a), Rc * math.sin(a)), r
    def path(phi0, phi1, n, extra=0.0):
        pts, rs = [], []
        for i in range(n + 1):
            ph = phi0 + (phi1 - phi0) * i / n; p, r = VP(ph); pts.append(p); rs.append(r + extra)
        return pts, rs
    p0, r0 = VP(0.0); p1, _ = VP(1.0); tg = (Vector(p1) - Vector(p0)).normalized()     # flow direction at the inlet (+Z)
    inlet = [tuple(Vector(p0) - tg * d) for d in (46.0, 38.0, 30.0, 22.0, 14.0, 6.0)]
    ir = [r0 + 1.0 - 1.0 * i / 5 for i in range(6)]
    shells = []
    pts, rs = path(0.0, 70.0, 20, 4.5); shells.append(sweep('tv_sh1', inlet + pts, [r + 4.5 for r in ir] + rs))
    pts, rs = path(60.0, 345.0, 70, 4.5); shells.append(sweep('tv_sh2', pts, rs))
    fl = extrude('t_in_flange', rrect(Vector(p0).x, Vector(p0).y, 31.0, 27.0, 6.0), 'z', -56.0, -47.0)
    shells.append(fl)
    for s in shells:
        apply_bool(core, s, 'UNION'); bpy.data.objects.remove(s, do_unlink=True)
    cav = [(30.9, 0.0), (30.9, 36.0), (36.8, 36.0), (36.8, 33.3), (45.5, 33.3), (45.5, 21.85)]
    for k in range(1, 21):
        s = k / 20; cav.append((66.0 - 20.5 * math.cos(s * PI / 2), 21.5 - 3.0 * math.sin(s * PI / 2) + 0.35))
    cav += [(70.0, 19.0), (79.0, 23.0), (86.1, 23.5), (86.1, 0.0)]
    cuts = [revolve_x('tv_cav', cav, segs=160)]
    pts, rs = path(-2.0, 70.0, 22); cuts.append(sweep('tv_p1', [tuple(Vector(p0) - tg * d) for d in (60.0, 46.0, 38.0, 30.0, 22.0, 14.0, 6.0)] + pts,
                                                     [ir[0]] + ir + rs))
    pts, rs = path(60.0, 345.0, 70); cuts.append(sweep('tv_p2', pts, rs))
    fx, fy = Vector(p0).x, Vector(p0).y
    for sx in (-1, 1):
        for sy in (-1, 1):
            cuts.append(cyl(f'tib{sx}{sy}', (fx + sx * 23.0, fy + sy * 19.0, -57.0), (fx + sx * 23.0, fy + sy * 19.0, -46.0), 3.6, segs=32))
    for k in range(3):
        a = PI / 2 + 2 * PI * k / 3 + PI / 3
        cuts.append(cyl(f'tob{k}', (78.0, 35.5 * math.cos(a), 35.5 * math.sin(a)), (86.5, 35.5 * math.cos(a), 35.5 * math.sin(a)), 3.6, segs=32))
    bool_many(core, cuts)
    return core, {'inlet_start': tuple(Vector(p0) - tg * 52.0), 'inlet_dir': tuple(tg), 'VP': VP}


def build_vnt():
    V = {}
    V['nozzle_ring'] = revolve_x('nozzle_ring', [(36.8, 22.8), (36.8, 33.0), (38.5, 33.0), (38.5, 22.8)], segs=160)
    V['unison'] = revolve_x('unison', [(33.6, 30.6), (33.6, 34.6), (35.8, 34.6), (35.8, 30.6)], segs=160)
    vanes = []
    c = 10.5; tc = 0.24; alpha = math.radians(24.0); Rp = 28.6
    for k in range(11):
        ph = 2 * PI * (k + 0.25) / 11
        rh = Vector((math.cos(ph), math.sin(ph))); th = Vector((-math.sin(ph), math.cos(ph)))
        d = th * math.cos(alpha) - rh * math.sin(alpha); n = Vector((-d.y, d.x))
        P = rh * Rp; top, bot = [], []
        for i in range(25):
            xi = (1 - math.cos(PI * i / 24)) / 2
            yt = 5 * tc * c * (0.2969 * math.sqrt(xi) - 0.126 * xi - 0.3516 * xi ** 2 + 0.2843 * xi ** 3 - 0.1036 * xi ** 4)
            camber = 0.04 * c * 4 * xi * (1 - xi)
            q = P + d * (c * (xi - 0.38))
            top.append(q + n * (camber + yt)); bot.append(q + n * (camber - yt))
        poly = [(p.x, p.y) for p in top] + [(p.x, p.y) for p in reversed(bot[1:-1])]
        vanes.append(extrude(f'vane{k}', poly, 'x', 38.5, 45.45))
        vanes.append(cyl(f'vpin{k}', (33.4, P.x, P.y), (38.6, P.x, P.y), 1.3, segs=24))
    V['vanes'] = join(vanes, 'vanes')
    V['heat_shield'] = revolve_x('heat_shield', [(31.8, 9.0), (32.4, 12.0), (34.4, 16.0), (35.9, 18.6), (36.0, 29.8), (36.75, 29.8), (36.75, 18.2),
                                                 (35.2, 15.4), (33.2, 11.5), (32.6, 9.0)], segs=160)
    return V


def bolt_head(name, p, axis_dir, af=10.0, h=6.0, washer=True):
    """hex bolt head + washer standing on point p, pointing along +/-X (axis_dir = +1 / -1)."""
    x0 = p[0]; x1 = x0 + axis_dir * h
    hx = prism_x(name, 6, af / 2, min(x0, x1), max(x0, x1), rot=0.3)
    ch = revolve_x(name + '_c', [(min(x0, x1), 0), (min(x0, x1), af * 0.55), (max(x0, x1) - 0.8, af * 0.62), (max(x0, x1), af * 0.5), (max(x0, x1), 0)] if axis_dir > 0 else
                   [(min(x0, x1), 0), (min(x0, x1), af * 0.5), (min(x0, x1) + 0.8, af * 0.62), (max(x0, x1), af * 0.55), (max(x0, x1), 0)], segs=48)
    apply_bool(hx, ch, 'INTERSECT'); bpy.data.objects.remove(ch, do_unlink=True)
    hx.data.transform(Matrix.Translation((0, p[1], p[2])))
    obs = [hx]
    if washer:
        w = revolve_x(name + '_w', [(x0 - 0.0, 3.2), (x0 + axis_dir * 1.6, 3.2), (x0 + axis_dir * 1.6, af * 0.85), (x0, af * 0.85)] if axis_dir > 0 else
                      [(x0 + axis_dir * 1.6, 3.2), (x0, 3.2), (x0, af * 0.85), (x0 + axis_dir * 1.6, af * 0.85)], segs=48)
        w.data.transform(Matrix.Translation((0, p[1], p[2])))
        hx.data.transform(Matrix.Translation((axis_dir * 1.6, 0, 0)))
        obs.append(w)
    return obs


def build_hardware():
    H = []
    # turbine-side clamp: 6 bolts with plates over the CHRA flange (heads towards -X)
    for k in range(6):
        a = 2 * PI * (k + 0.25) / 6
        y, z = 38.6 * math.cos(a), 38.6 * math.sin(a)
        pl = extrude(f'cplate{k}', rrect(0, 0, 4.2, 6.5, 1.5), 'x', 21.0, 24.0)
        pl.data.transform(Matrix.Rotation(a - PI / 2, 4, 'X') @ Matrix.Translation((0, 0, 35.5)))
        H.append(pl)
        H += bolt_head(f'tb{k}', (21.0, y, z), -1, af=10.0, h=5.5)
    # compressor housing clamp: 6 bolts on the back rim (heads towards +X)
    for k in range(6):
        a = 2 * PI * (k + 0.25) / 6
        H += bolt_head(f'cb{k}', (-29.0, 47.0 * math.cos(a), 47.0 * math.sin(a)), +1, af=8.0, h=4.5)
    # oil inlet + drain flange bolts
    # oil feed: banjo-style fitting (hex) + steel pipe from the engine
    hexz = [(7.0 / math.cos(PI / 6) * math.cos(PI / 6 + k * PI / 3), 7.0 / math.cos(PI / 6) * math.sin(PI / 6 + k * PI / 3)) for k in range(6)]
    fit = extrude('oil_fitting', hexz, 'z', 29.0, 37.0)
    ch = cyl('fit_ch', (0, 0, 28.9), (0, 0, 37.1), 7.9, segs=64)
    apply_bool(fit, ch, 'INTERSECT'); bpy.data.objects.remove(ch, do_unlink=True)
    bool_many(fit, [cyl('fit_bore', (0, 0, 28.0), (0, 0, 38.0), 3.0, segs=48)])
    H.append(fit)
    pipe = cyl('oil_pipe', (0, 0, 36.5), (0, 0, 72.0), 4.2, segs=64)
    bool_many(pipe, [cyl('pipe_bore', (0, 0, 35.0), (0, 0, 73.0), 3.0, segs=48)])
    H.append(pipe)
    nutp = extrude('pipe_nut', [(6.0 / math.cos(PI / 6) * math.cos(k * PI / 3), 6.0 / math.cos(PI / 6) * math.sin(k * PI / 3)) for k in range(6)], 'z', 37.0, 43.0)
    bool_many(nutp, [cyl('pn_bore', (0, 0, 36.0), (0, 0, 44.0), 4.25, segs=48)])
    H.append(nutp)
    # oil drain: gasket + tube
    dt = cyl('drain_tube', (0, 0, -36.0), (0, 0, -66.0), 9.2, segs=72)
    bool_many(dt, [cyl('dt_bore', (0, 0, -35.0), (0, 0, -67.0), 7.7, segs=72)])
    H.append(dt)
    dfl = extrude('drain_fl2', stadium(0, 0, 21.5, 12.0), 'z', -40.0, -36.0)
    bool_many(dfl, [cyl('dfl_b', (0, 0, -41.0), (0, 0, -35.0), 7.7, segs=72),
                    cyl('dfl_h1', (16.5, 0, -41.0), (16.5, 0, -35.0), 3.3, segs=32), cyl('dfl_h2', (-16.5, 0, -41.0), (-16.5, 0, -35.0), 3.3, segs=32)])
    H.append(dfl)
    return H


def build_actuator():
    """pneumatic VNT actuator on a bracket, rod to the vane lever (all in front of the section plane)."""
    A = []
    cx, cy, cz = -18.0, -44.0, -58.0
    can = revolve_x('act_can', [(cx - 16.0, 0.0), (cx - 16.0, 21.0), (cx - 13.0, 25.0), (cx + 7.0, 25.5), (cx + 9.5, 27.5), (cx + 11.0, 27.5),
                                (cx + 11.0, 25.0), (cx + 14.0, 23.0), (cx + 16.0, 12.0), (cx + 16.0, 0.0)], segs=96)
    can.data.transform(Matrix.Translation((0, cy, cz)))
    nip = cyl('act_nip', (cx - 4.0, cy - 20.0, cz + 10.0), (cx - 4.0, cy - 33.0, cz + 18.0), 2.6, segs=24)
    A += [can, nip]
    rod_p0 = Vector((cx + 16.0, cy, cz)); lever_p = Vector((34.0, -33.0, -40.0))
    A.append(cyl('act_rod', rod_p0, lever_p + Vector((-1.5, 0, 0)), 2.0, segs=24))
    A.append(cyl('act_rod_end', lever_p + Vector((-4.0, 0, 0)), lever_p + Vector((1.5, 0, 0)), 3.4, segs=24))
    lev = box('act_lever', 32.5, 35.5, -36.0, -30.0, -41.0, -24.0); A.append(lev)
    A.append(cyl('act_pivot', (31.0, -33.0, -26.5), (37.5, -33.0, -26.5), 3.2, segs=32))
    br = box('act_bracket', -14.0, -2.0, -2.0, 2.0, 0.0, 31.0)
    br.data.transform(Matrix.Translation((0, -16.0, -16.0)) @ Matrix.Rotation(math.radians(135.0), 4, 'X'))
    A.append(br)
    return A


# --------------------------------------------------------------------------- oil volumes (white emission, tinted in the compositor)
def build_oil(var):
    O = {'feed': [], 'outer': [], 'inner': [], 'thrust': [], 'holes': []}
    O['feed'] += [cyl('o_in', (0, 0, 72.0), (0, 0, GAL_Z), 2.94, segs=40), cyl('o_gal', (-26.0, 0, GAL_Z), (FEED_X + 1.5, 0, GAL_Z), 1.94, segs=40),
                  cyl('o_tp1', (-26.0, 0, GAL_Z), (-27.4, 0, GAL_Z), 1.34, segs=24), cyl('o_tp2', (-27.4, 0, GAL_Z), (-27.4, 0, 4.7), 0.8, segs=24)]
    zb = 6.4 if var == 'A' else 6.1
    for sx in (-1, 1):
        O['feed'].append(cyl(f'o_feed{sx}', (sx * FEED_X, 0, GAL_Z), (sx * FEED_X, 0, zb), 1.14, segs=32))
    for sx in (-1, 1):
        a, b = sorted((sx * 11.0, sx * 21.0))
        O['inner'].append(revolve_x(f'o_inner{sx}', [(a + 0.3, 4.02), (b - 0.3, 4.02), (b - 0.3, 4.38), (a + 0.3, 4.38)]))
        if var == 'A':
            O['outer'].append(revolve_x(f'o_outer{sx}', [(a + 0.3, 6.27), (b - 0.3, 6.27), (b - 0.3, 7.03), (a + 0.3, 7.03)]))
        else:
            O['outer'].append(revolve_x(f'o_outer{sx}', [(a + 0.3, 6.27), (b - 0.3, 6.27), (b - 0.3, 6.73), (a + 0.3, 6.73)]))
            g0, g1 = sorted((sx * 15.0, sx * 17.0))
            O['outer'].append(revolve_x(f'o_groove{sx}', [(g0 + 0.02, 5.87), (g1 - 0.02, 5.87), (g1 - 0.02, 6.3), (g0 + 0.02, 6.3)]))
            for k in (0, 1, 2, 3):
                an = k * PI / 2
                O['holes'].append(cyl(f'o_sfh{sx}{k}', (sx * FEED_X, 4.38 * math.cos(an), 4.38 * math.sin(an)), (sx * FEED_X, 5.9 * math.cos(an), 5.9 * math.sin(an)), 0.82, segs=24))
    O['thrust'] += [revolve_x('o_th1', [(-29.0, 4.62), (-28.82, 4.62), (-28.82, 8.45), (-29.0, 8.45)]),
                    revolve_x('o_th2', [(-25.98, 5.02), (-25.82, 5.02), (-25.82, 8.45), (-25.98, 8.45)]),
                    revolve_x('o_th3', [(-28.8, 4.62), (-26.0, 4.62), (-26.0, 4.98), (-28.8, 4.98)])]
    return O


# --------------------------------------------------------------------------- materials
def _p(nt, typ, **kw):
    n = nt.nodes.new(typ)
    for k, v in kw.items(): setattr(n, k, v)
    return n


def add_bevel(m, radius=0.22):
    nt = m.node_tree; b = nt.nodes['Principled BSDF']
    bv = _p(nt, 'ShaderNodeBevel'); bv.samples = 6; bv.inputs['Radius'].default_value = radius
    if b.inputs['Normal'].is_linked:
        src = b.inputs['Normal'].links[0].from_socket; nt.links.new(src, bv.inputs['Normal'])
    nt.links.new(bv.outputs['Normal'], b.inputs['Normal'])


def mat_metal(name, col, rough, metal=1.0, aniso=0.0, bevel=0.22, noise=0.0, nscale=0.6, tint2=None, grad=None):
    m = bpy.data.materials.new(name); m.use_nodes = True; m.use_fake_user = True
    nt = m.node_tree; b = nt.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*col, 1); b.inputs['Metallic'].default_value = metal
    b.inputs['Roughness'].default_value = rough
    if aniso: b.inputs['Anisotropic'].default_value = aniso
    tc = _p(nt, 'ShaderNodeTexCoord')
    if noise:
        nz = _p(nt, 'ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = nscale; nz.inputs['Detail'].default_value = 8.0
        nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
        bp = _p(nt, 'ShaderNodeBump'); bp.inputs['Strength'].default_value = noise; bp.inputs['Distance'].default_value = 0.08
        nt.links.new(nz.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
        rr = _p(nt, 'ShaderNodeMapRange'); rr.inputs[3].default_value = rough * 0.85; rr.inputs[4].default_value = min(1.0, rough * 1.25)
        nt.links.new(nz.outputs['Fac'], rr.inputs[0]); nt.links.new(rr.outputs[0], b.inputs['Roughness'])
        if tint2 is not None:
            nz2 = _p(nt, 'ShaderNodeTexNoise'); nz2.inputs['Scale'].default_value = nscale * 0.18; nz2.inputs['Detail'].default_value = 3.0
            nt.links.new(tc.outputs['Object'], nz2.inputs['Vector'])
            mx = _p(nt, 'ShaderNodeMix', data_type='RGBA'); mx.inputs[6].default_value = (*col, 1); mx.inputs[7].default_value = (*tint2, 1)
            mr = _p(nt, 'ShaderNodeMapRange'); mr.inputs[1].default_value = 0.42; mr.inputs[2].default_value = 0.68
            nt.links.new(nz2.outputs['Fac'], mr.inputs[0]); nt.links.new(mr.outputs[0], mx.inputs[0])
            nt.links.new(mx.outputs[2], b.inputs['Base Color'])
    if grad is not None:          # colour along X (heat tint towards the turbine)
        x0, x1, c1 = grad
        sx = _p(nt, 'ShaderNodeSeparateXYZ'); nt.links.new(tc.outputs['Object'], sx.inputs[0])
        mr = _p(nt, 'ShaderNodeMapRange'); mr.inputs[1].default_value = x0; mr.inputs[2].default_value = x1
        nt.links.new(sx.outputs['X'], mr.inputs[0])
        mx = _p(nt, 'ShaderNodeMix', data_type='RGBA'); mx.inputs[6].default_value = (*col, 1); mx.inputs[7].default_value = (*c1, 1)
        nt.links.new(mr.outputs[0], mx.inputs[0]); nt.links.new(mx.outputs[2], b.inputs['Base Color'])
    if bevel: add_bevel(m, bevel)
    return m


def mat_section(name, col, line, ang=45.0, period=1.6, width=0.18, axes='XZ'):
    """matte cut face with hatching in object coordinates (mm)."""
    m = bpy.data.materials.new(name); m.use_nodes = True; m.use_fake_user = True
    nt = m.node_tree; b = nt.nodes['Principled BSDF']
    b.inputs['Metallic'].default_value = 0.45; b.inputs['Roughness'].default_value = 0.62
    tc = _p(nt, 'ShaderNodeTexCoord'); sx = _p(nt, 'ShaderNodeSeparateXYZ')
    nt.links.new(tc.outputs['Object'], sx.inputs[0])
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    m1 = _p(nt, 'ShaderNodeMath', operation='MULTIPLY'); m1.inputs[1].default_value = ca / period
    m2 = _p(nt, 'ShaderNodeMath', operation='MULTIPLY'); m2.inputs[1].default_value = sa / period
    nt.links.new(sx.outputs[axes[0]], m1.inputs[0]); nt.links.new(sx.outputs[axes[1]], m2.inputs[0])
    ad = _p(nt, 'ShaderNodeMath', operation='ADD'); nt.links.new(m1.outputs[0], ad.inputs[0]); nt.links.new(m2.outputs[0], ad.inputs[1])
    fr = _p(nt, 'ShaderNodeMath', operation='FRACT'); nt.links.new(ad.outputs[0], fr.inputs[0])
    lt = _p(nt, 'ShaderNodeMath', operation='LESS_THAN'); lt.inputs[1].default_value = width
    nt.links.new(fr.outputs[0], lt.inputs[0])
    mx = _p(nt, 'ShaderNodeMix', data_type='RGBA')
    mx.inputs[6].default_value = (*col, 1); mx.inputs[7].default_value = (*line, 1)
    nt.links.new(lt.outputs[0], mx.inputs[0]); nt.links.new(mx.outputs[2], b.inputs['Base Color'])
    return m


def mat_emit_white(name='oil_white', col=(1, 1, 1)):
    m = bpy.data.materials.new(name); m.use_nodes = True; m.use_fake_user = True
    nt = m.node_tree; nt.nodes.clear()
    em = _p(nt, 'ShaderNodeEmission'); em.inputs['Color'].default_value = (*col, 1); em.inputs['Strength'].default_value = 1.0
    out = _p(nt, 'ShaderNodeOutputMaterial'); nt.links.new(em.outputs[0], out.inputs['Surface'])
    return m


MATS = {}
SURF = {   # key: (surface colour, rough, kwargs) ; section: (colour, line, angle, period)
    'alu_cast': ((0.62, 0.63, 0.64), 0.46, dict(noise=0.25, nscale=0.9), ((0.27, 0.28, 0.29), (0.12, 0.13, 0.14), 45, 2.8)),
    'alu_mach': ((0.80, 0.81, 0.83), 0.30, dict(noise=0.05), ((0.32, 0.33, 0.35), (0.14, 0.15, 0.16), -45, 2.2)),
    'iron':     ((0.30, 0.30, 0.31), 0.55, dict(noise=0.35, nscale=1.1, tint2=(0.33, 0.29, 0.25)), ((0.22, 0.22, 0.23), (0.09, 0.09, 0.10), 45, 2.0)),
    'th_steel': ((0.17, 0.16, 0.155), 0.55, dict(noise=0.5, nscale=1.0, tint2=(0.24, 0.17, 0.12)), ((0.21, 0.19, 0.18), (0.08, 0.07, 0.07), -45, 2.6)),
    'bronze':   ((0.80, 0.52, 0.27), 0.30, dict(noise=0.04), ((0.46, 0.29, 0.14), (0.20, 0.12, 0.05), -45, 0.9)),
    'steel':    ((0.68, 0.69, 0.72), 0.26, dict(), ((0.30, 0.31, 0.33), (0.13, 0.13, 0.15), 45, 1.1)),
    'steel_dk': ((0.30, 0.31, 0.33), 0.38, dict(), ((0.20, 0.20, 0.22), (0.08, 0.08, 0.09), -45, 0.7)),
    'sheet':    ((0.52, 0.50, 0.47), 0.40, dict(noise=0.08, tint2=(0.45, 0.36, 0.30)), ((0.26, 0.25, 0.24), (0.10, 0.10, 0.10), 0, 0.5)),
    'vnt':      ((0.26, 0.24, 0.22), 0.45, dict(noise=0.15), ((0.20, 0.19, 0.18), (0.08, 0.07, 0.07), 45, 1.0)),
    'black':    ((0.035, 0.036, 0.04), 0.42, dict(noise=0.05), ((0.07, 0.07, 0.08), (0.03, 0.03, 0.03), 45, 2.0)),
    'zinc':     ((0.70, 0.70, 0.66), 0.30, dict(), None),
    'zinc_cut': ((0.72, 0.71, 0.66), 0.30, dict(), ((0.32, 0.32, 0.30), (0.14, 0.14, 0.13), -45, 1.0)),
}


def mats():
    if MATS: return MATS
    for k, (col, rough, kw, sec) in SURF.items():
        s = mat_metal('m_' + k, col, rough, **kw)
        MATS[k] = (s, mat_section('s_' + k, *sec) if sec else None, mat_section('t_' + k, *sec, axes='YZ') if sec else None)
    MATS['wheel_c'] = (mat_metal('m_wheel_c', (0.86, 0.87, 0.89), 0.20, aniso=0.35, bevel=0.12), None, None)
    MATS['wheel_t'] = (mat_metal('m_wheel_t', (0.44, 0.41, 0.38), 0.34, bevel=0.12, noise=0.06, tint2=(0.42, 0.33, 0.26)), None, None)
    MATS['shaft'] = (mat_metal('m_shaft', (0.92, 0.93, 0.95), 0.10, bevel=0.1, grad=(22.0, 37.0, (0.55, 0.42, 0.30))),
                     mat_section('s_shaft', (0.38, 0.39, 0.42), (0.15, 0.16, 0.18), 45, 0.9),
                     mat_section('t_shaft', (0.58, 0.60, 0.64), (0.22, 0.23, 0.26), -20, 0.75, width=0.22, axes='YZ'))
    MATS['oil'] = (mat_emit_white(), None, None)
    for zk, col in (('feed', (1, 0, 0)), ('outer', (0, 1, 0)), ('inner', (0, 0, 1)), ('thrust', (1, 0, 0)), ('holes', (0, 1, 0))):
        MATS['oil_' + zk] = (mat_emit_white('oil_' + zk, col), None, None)
    return MATS


def set_mats(ob, key, cut='y', side=-1, at=0.0):
    """slot 0 surface, slot 1 section (faces lying on the cut plane, facing the camera side)."""
    surf, sec_y, sec_x = mats()[key]
    sec = sec_y if cut == 'y' else sec_x
    ob.data.materials.clear(); ob.data.materials.append(surf)
    if sec is not None and cut:
        ob.data.materials.append(sec)
        for p in ob.data.polygons:
            if cut == 'y' and abs(p.center.y - at) < 2e-3 and p.normal.y * side > 0.98: p.material_index = 1
            if cut == 'x' and abs(p.center.x - at) < 2e-3 and p.normal.x * side > 0.98: p.material_index = 1
    smooth(ob)


def cut_plane(ob, keep, at=0.0, eps=0.0):
    """keep: 'y+' (y >= at), 'y-' (y <= at), 'x+' (x >= at)."""
    B = 400.0
    if keep == 'y+': c = box('cutter', -B, B, -B, at - eps, -B, B)
    elif keep == 'y-': c = box('cutter', -B, B, at, B, -B, B)
    else: c = box('cutter', -B, at - eps, -B, B, -B, B)
    apply_bool(ob, c); bpy.data.objects.remove(c, do_unlink=True)
    return len(ob.data.polygons) > 0


# --------------------------------------------------------------------------- scene assembly
def new_coll(name):
    c = bpy.data.collections.new(name); bpy.context.scene.collection.children.link(c); return c


def move_to(ob, coll):
    for c in list(ob.users_collection): c.objects.unlink(ob)
    coll.objects.link(ob)


MAT_OF = {
    'comp_housing': 'alu_cast', 'backplate': 'alu_mach', 'chra_A': 'iron', 'chra_B': 'iron', 'turbine_housing': 'th_steel',
    'nozzle_ring': 'vnt', 'unison': 'vnt', 'vanes': 'vnt', 'heat_shield': 'sheet', 'bush_t': 'bronze', 'bush_c': 'bronze',
    'bearing_sf': 'bronze', 'pin': 'steel', 'thrust_plate': 'bronze', 'deflector': 'sheet', 'ring_t': 'steel_dk', 'ring_c': 'steel_dk',
    'collar': 'steel', 'flinger': 'steel', 'shaft': 'shaft', 'compressor_wheel': 'wheel_c', 'turbine_wheel': 'wheel_t', 'nut': 'zinc',
}


def mat_key(name):
    if name in MAT_OF: return MAT_OF[name]
    if name.startswith('clip'): return 'steel_dk'
    if name.startswith('act_'): return 'black' if name in ('act_can', 'act_nip') else 'steel_dk'
    if name.startswith(('tb', 'cb')): return 'zinc'
    if name.startswith('cplate'): return 'steel_dk'
    if name in ('oil_fitting', 'pipe_nut'): return 'zinc_cut'
    if name in ('oil_pipe', 'drain_tube', 'drain_fl2'): return 'steel'
    return 'steel'


def build():
    t0 = time.time()
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene; sc.unit_settings.system = 'NONE'
    mats()
    print('rotor...', flush=True)
    R = build_rotor(); RC = build_rotor_cut()
    print('chra...', time.time() - t0, flush=True)
    CH = {v: build_chra(v) for v in 'AB'}
    IN = {v: build_internals(v) for v in 'AB'}
    print('housings...', time.time() - t0, flush=True)
    comp, cinfo = build_comp_housing(); turb, tinfo = build_turbine_housing()
    bp = build_backplate(); V = build_vnt()
    print('hardware...', time.time() - t0, flush=True)
    HW = build_hardware(); ACT = build_actuator()
    OIL = {v: build_oil(v) for v in 'AB'}
    cols = {k: new_coll(k) for k in ('shared', 'front', 'chra_A', 'chra_B', 'int_A', 'int_B', 'rotor', 'rotor_c', 'rotor_t', 'rotor_cut',
                                      'oilA_feed', 'oilA_outer', 'oilA_inner', 'oilA_thrust', 'oilB_feed', 'oilB_outer', 'oilB_inner', 'oilB_thrust', 'oilB_holes',
                                      'trA_static', 'trA_bush', 'trA_shaft', 'trA_oil_feed', 'trA_oil_outer', 'trA_oil_inner', 'trA_oil_holes',
                                      'trB_static', 'trB_shaft', 'trB_oil_feed', 'trB_oil_outer', 'trB_oil_inner', 'trB_oil_holes',
                                      'trP_static', 'trP_shaft', 'trP_oil_outer', 'trP_oil_inner')}
    print('section cuts...', time.time() - t0, flush=True)
    # ---- transverse copies first (from the full solids)
    XT = FEED_X               # land of the turbine-side bearing (A bushing middle / B land)
    XP = 0.0                  # semi-floating bearing middle (pin)
    def tr_copy(ob, key, coll, at, nm=None):
        o = dup(ob, (nm or ob.name) + '_tr' + coll)
        if cut_plane(o, 'x+', at):
            set_mats(o, key, cut='x', side=-1, at=at); move_to(o, cols[coll]); return o
        bpy.data.objects.remove(o, do_unlink=True); return None
    tr_copy(CH['A'], 'iron', 'trA_static', XT)
    for nm in ('clip0', 'clip1', 'clip2', 'clip3'):
        tr_copy(IN['A'][nm], 'steel_dk', 'trA_static', XT)
    tr_copy(IN['A']['bush_t'], 'bronze', 'trA_bush', XT)
    tr_copy(R['shaft'], 'shaft', 'trA_shaft', XT)
    tr_copy(CH['B'], 'iron', 'trB_static', XT); tr_copy(IN['B']['bearing_sf'], 'bronze', 'trB_static', XT)
    tr_copy(R['shaft'], 'shaft', 'trB_shaft', XT)
    tr_copy(CH['B'], 'iron', 'trP_static', XP, 'chraP'); tr_copy(IN['B']['bearing_sf'], 'bronze', 'trP_static', XP, 'bearP')
    tr_copy(IN['B']['pin'], 'steel', 'trP_static', XP, 'pinP')
    tr_copy(R['shaft'], 'shaft', 'trP_shaft', XP, 'shaftP')
    oilm = mats()['oil'][0]
    for var, coll_pref, at in (('A', 'trA_oil_', XT), ('B', 'trB_oil_', XT)):
        for zone in ('feed', 'outer', 'inner', 'holes'):
            for ob in OIL[var][zone]:
                o = dup(ob, ob.name + '_' + coll_pref + zone)
                if cut_plane(o, 'x+', at + 0.02):
                    o.data.materials.clear(); o.data.materials.append(oilm); move_to(o, cols[coll_pref + zone])
                else: bpy.data.objects.remove(o, do_unlink=True)
    # oil inside the rotating A bushing holes (rotates with the bushing)
    for k in range(4):
        an = PI / 4 + k * PI / 2
        o = cyl(f'o_bh{k}', (XT, 4.38 * math.cos(an), 4.38 * math.sin(an)), (XT, 6.27 * math.cos(an), 6.27 * math.sin(an)), 0.86, segs=24)
        cut_plane(o, 'x+', XT + 0.02); o.data.materials.clear(); o.data.materials.append(oilm); move_to(o, cols['trA_oil_holes'])
    for zone in ('outer', 'inner'):
        for ob in OIL['B'][zone]:
            o = dup(ob, ob.name + '_P' + zone)
            if cut_plane(o, 'x+', XP + 0.02):
                o.data.materials.clear(); o.data.materials.append(oilm); move_to(o, cols['trP_oil_' + zone])
            else: bpy.data.objects.remove(o, do_unlink=True)
    # B pin section: the inner relief / outer relief around the middle are oil too
    for nm, r0, r1 in (('o_relief_in', 4.42, 4.98), ('o_relief_out', 6.02, 6.73)):
        o = revolve_x(nm, [(XP + 0.02, r0), (2.0, r0), (2.0, r1), (XP + 0.02, r1)])
        o.data.materials.clear(); o.data.materials.append(oilm); move_to(o, cols['trP_oil_outer' if 'out' in nm else 'trP_oil_inner'])
    # ---- main section (y = 0)
    def split(ob, key, back_coll, front=True):
        if front:
            fr = dup(ob, ob.name + '_front')
            if cut_plane(fr, 'y-'):
                set_mats(fr, key, cut=None); move_to(fr, cols['front'])
            else: bpy.data.objects.remove(fr, do_unlink=True)
        if cut_plane(ob, 'y+'):
            set_mats(ob, key, cut='y', side=-1); move_to(ob, cols[back_coll])
        else: bpy.data.objects.remove(ob, do_unlink=True)
    for ob, key in ((comp, 'alu_cast'), (turb, 'th_steel'), (bp, 'alu_mach'), (V['nozzle_ring'], 'vnt'), (V['unison'], 'vnt'),
                    (V['vanes'], 'vnt'), (V['heat_shield'], 'sheet')):
        split(ob, key, 'shared')
    for ob in HW + ACT:
        split(ob, mat_key(ob.name), 'shared')
    split(CH['A'], 'iron', 'chra_A', front=True)
    split(CH['B'], 'iron', 'chra_B', front=False)
    for v in 'AB':
        for nm, ob in IN[v].items():
            split(ob, mat_key(nm), 'int_' + v, front=False)
    for nm, ob in RC.items():
        split(ob, 'steel', 'rotor_cut', front=False)
    for nm, ob in R.items():
        set_mats(ob, mat_key(nm), cut=None)
        move_to(ob, cols['rotor_c' if nm in ('compressor_wheel', 'nut') else 'rotor_t' if nm == 'turbine_wheel' else 'rotor'])
    for v in 'AB':
        for zone, obs in OIL[v].items():
            for ob in obs:
                if cut_plane(ob, 'y+', 0.0, eps=0.03):
                    ob.data.materials.clear(); ob.data.materials.append(oilm); move_to(ob, cols[f'oil{v}_{zone}'])
                    for p in ob.data.polygons: p.use_smooth = True
                else: bpy.data.objects.remove(ob, do_unlink=True)
    for ob in list(sc.collection.objects):
        if ob.type == 'MESH': print('  stray', ob.name); bpy.data.objects.remove(ob, do_unlink=True)
    print('lights/cameras...', time.time() - t0, flush=True)
    world_and_lights()
    make_cameras()
    r = sc.render; r.engine = 'CYCLES'; r.resolution_percentage = 100; r.film_transparent = True
    cy = sc.cycles; cy.device = 'CPU'; cy.samples = 64; cy.use_adaptive_sampling = True; cy.adaptive_threshold = 0.02
    cy.use_denoising = True; cy.denoiser = 'OPENIMAGEDENOISE'
    cy.max_bounces = 8; cy.glossy_bounces = 4; cy.diffuse_bounces = 2; cy.transmission_bounces = 2; cy.transparent_max_bounces = 4
    cy.caustics_reflective = False; cy.caustics_refractive = False
    sc.view_settings.view_transform = 'AgX'
    try: sc.view_settings.look = 'AgX - Medium High Contrast'
    except Exception: pass
    r.image_settings.file_format = 'PNG'; r.image_settings.color_mode = 'RGBA'; r.image_settings.color_depth = '16'
    json.dump({'comp_outlet_end': cinfo['outlet_end'], 'comp_outlet_dir': cinfo['outlet_dir'],
               'turb_inlet_start': tinfo['inlet_start'], 'turb_inlet_dir': tinfo['inlet_dir']}, open(os.path.join(OUT, 'geo.json'), 'w'), indent=1)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, 'turbo.blend'))
    print('saved', len(bpy.data.objects), 'objects in %.0fs' % (time.time() - t0))


# --------------------------------------------------------------------------- light + cameras
CAM = {   # yaw (deg, +: camera on the compressor side), pitch, distance, target, sensor-fit square size at target (mm)
    'main': dict(yaw=22.0, pitch=11.0, dist=760.0, tgt=(-6.0, 0.0, -1.0), field=236.0),
    'hero': dict(yaw=40.0, pitch=17.0, dist=760.0, tgt=(-6.0, 0.0, -2.0), field=250.0),
    'trA': dict(trans=FEED_X, dist=180.0, field=58.0),
    'trP': dict(trans=0.0, dist=180.0, field=58.0),
}


def cam_dir(yaw, pitch):
    y, p = math.radians(yaw), math.radians(pitch)
    return Vector((math.sin(y) * math.cos(p), math.cos(y) * math.cos(p), -math.sin(p)))


def world_and_lights(yaw=22.0):
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
    for name, rot, en, ang in (('key', (math.radians(48), 0, math.radians(-38)), 2.4, 10),
                               ('rim', (math.radians(66), 0, math.radians(150)), 1.8, 6),
                               ('fill', (math.radians(78), 0, math.radians(35)), 0.55, 30),
                               ('fill_r', (math.radians(60), 0, math.radians(60)), 1.1, 14)):
        ld = bpy.data.lights.new(name, 'SUN'); ld.energy = en; ld.angle = math.radians(ang)
        lo = bpy.data.objects.new(name, ld); lo.rotation_euler = rot; sc.collection.objects.link(lo)


def make_cameras():
    sc = bpy.context.scene
    for name, spec in CAM.items():
        cd = bpy.data.cameras.new('cam_' + name); cd.sensor_fit = 'HORIZONTAL'; cd.sensor_width = 36.0; cd.sensor_height = 36.0
        cd.clip_start = 1.0; cd.clip_end = 5000.0
        co = bpy.data.objects.new('cam_' + name, cd); sc.collection.objects.link(co)
        if 'trans' in spec:
            x = spec['trans']; co.location = (x - spec['dist'], 0.0, 0.0)
            d = Vector((1, 0, 0)); co.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
            cd.lens = 36.0 * spec['dist'] / spec['field']
        else:
            d = cam_dir(spec['yaw'], spec['pitch']); tgt = Vector(spec['tgt'])
            co.location = tgt - d * spec['dist']
            co.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
            cd.lens = 36.0 * spec['dist'] / spec['field']


# --------------------------------------------------------------------------- rendering
BASE = 2160               # T1 plate size (square); tiers multiply it
ROT_STEP = 6.0            # deg per loop frame
NC, NT = 10, 6            # loop lengths (compressor 6+6 blades -> 60 deg period, turbine 10 blades -> 36 deg)
SOLID = ['shared', 'chra_A', 'chra_B', 'int_A', 'int_B', 'rotor', 'rotor_c', 'rotor_t', 'rotor_cut', 'front']


def setup_layer(vis, hold=(), vt='AgX', override=None):
    sc = bpy.context.scene
    for c in bpy.data.collections:
        c.hide_render = not (c.name in vis or c.name in hold)
        for ob in c.objects:
            ob.is_holdout = c.name in hold
    sc.view_settings.view_transform = vt
    if vt == 'Standard': sc.view_settings.look = 'None'
    bpy.context.view_layer.material_override = bpy.data.materials[override] if override else None


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


def var_layers(v):
    other = 'B' if v == 'A' else 'A'
    return ['shared', 'chra_' + v, 'int_' + v, 'rotor', 'rotor_c', 'rotor_t', 'rotor_cut']


def crops():
    p = os.path.join(OUT, 'crops.json')
    return json.load(open(p)) if os.path.exists(p) else {}


def job_list():
    C = crops(); J = []
    J.append(('T1_A', dict(cam='main', tier=1, vis=var_layers('A'))))
    J.append(('T1_front', dict(cam='main', tier=1, vis=['front'], hold=var_layers('A'), samples=40)))
    for v in 'AB':
        if 'T2' in C: J.append((f'T2_{v}', dict(cam='main', tier=2, crop=C['T2'], vis=var_layers(v))))
        if 'T3' in C: J.append((f'T3_{v}', dict(cam='main', tier=4, crop=C['T3'], vis=var_layers(v))))
    for v in 'AB':
        zones = ['feed', 'outer', 'inner', 'thrust'] + (['holes'] if v == 'B' else [])
        for tier, key in ((1, None), (2, 'T2'), (4, 'T3')):
            if key and key not in C: continue
            tn = {1: 'T1', 2: 'T2', 4: 'T3'}[tier]
            J.append((f'oil{v}_{tn}_rgb', dict(cam='main', tier=tier, crop=C.get(key) if key else None, vis=[f'oil{v}_feed', f'oil{v}_outer', f'oil{v}_inner'],
                                               hold=var_layers(v), vt='Standard', samples=12, denoise=False, oilrgb=True)))
            J.append((f'oil{v}_{tn}_th', dict(cam='main', tier=tier, crop=C.get(key) if key else None, vis=[f'oil{v}_thrust'] + ([f'oil{v}_holes'] if v == 'B' else []),
                                              hold=var_layers(v), vt='Standard', samples=12, denoise=False, oilrgb=True)))
    if 'LC' in C:
        for k in range(NC): J.append((f'LC_{k:02d}', dict(cam='main', tier=2, crop=C['LC'], vis=var_layers('A'), rot_c=k * ROT_STEP, samples=16, mblur=True)))
    if 'LT' in C:
        for k in range(NT): J.append((f'LT_{k:02d}', dict(cam='main', tier=2, crop=C['LT'], vis=var_layers('A'), rot_t=k * ROT_STEP, samples=16, mblur=True)))
    # transverse views (straight down the axis)
    for nm, cam, st, shaft, extra in (('trA', 'trA', 'trA_static', 'trA_shaft', ['trA_bush']), ('trB', 'trA', 'trB_static', 'trB_shaft', []),
                                      ('trP', 'trP', 'trP_static', 'trP_shaft', [])):
        J.append((f'{nm}_static', dict(cam=cam, tier=1.2, vis=[st], samples=20, pct=70, upscale=True)))
        J.append((f'{nm}_shaft', dict(cam=cam, tier=1.2, vis=[shaft], samples=32)))
        for e in extra: J.append((f'{nm}_bush', dict(cam=cam, tier=1.2, vis=[e], samples=32)))
    for nm, pref in (('trA', 'trA_oil_'), ('trB', 'trB_oil_'), ('trP', 'trP_oil_')):
        for z in ('feed', 'outer', 'inner', 'holes'):
            J.append((f'{nm}_oil_{z}', dict(cam='trA' if nm != 'trP' else 'trP', tier=1.2, vis=[pref + z],
                                             hold=[{'trA': 'trA_static', 'trB': 'trB_static', 'trP': 'trP_static'}[nm]] + (['trA_bush'] if nm == 'trA' and z != 'holes' else []),
                                             vt='Standard', samples=12, denoise=False)))
    return J


def render_job(name, spec, samples=None, pct=100, out=None):
    sc = bpy.context.scene
    sc.camera = bpy.data.objects['cam_' + spec['cam']]
    missing = [v for v in spec['vis'] if v not in bpy.data.collections]
    if missing or not any(len(bpy.data.collections[v].objects) for v in spec['vis'] if v in bpy.data.collections):
        print('skip (empty)', name); return False
    setup_layer(spec['vis'], spec.get('hold', ()), spec.get('vt', 'AgX'))
    tier = spec.get('tier', 1)
    if isinstance(tier, float):
        S = int(BASE * tier); sc.render.resolution_x = S; sc.render.resolution_y = S; sc.render.use_border = False
    else:
        set_crop(tier, spec.get('crop'))
    pct = spec.get('pct', pct)
    sc.render.resolution_percentage = pct
    sc.cycles.samples = samples or spec.get('samples', 64)
    sc.cycles.use_denoising = spec.get('denoise', True)
    if spec.get('oilrgb'):
        # each zone keeps its own pure colour: R / G / B channels
        for c in spec['vis']:
            zone = c.split('_')[-1]
            for ob in bpy.data.collections[c].objects:
                ob.data.materials.clear(); ob.data.materials.append(bpy.data.materials['oil_' + zone])
    cw = bpy.data.objects['compressor_wheel']; nut = bpy.data.objects['nut']; tw = bpy.data.objects['turbine_wheel']
    for ob in (cw, nut, tw):
        ob.animation_data_clear(); ob.rotation_euler = (0, 0, 0)
    sc.render.use_motion_blur = bool(spec.get('mblur'))
    if spec.get('mblur'):
        sc.render.motion_blur_shutter = 0.5
        sc.frame_set(10)
        for obs, ang in (((cw, nut), spec.get('rot_c', 0.0)), ((tw,), spec.get('rot_t', 0.0))):
            for ob in obs:
                bpy.context.preferences.edit.keyframe_new_interpolation_type = 'LINEAR'
                for f, a in ((9, ang - ROT_STEP), (10, ang), (11, ang + ROT_STEP)):
                    ob.rotation_euler = (math.radians(a), 0, 0); ob.keyframe_insert('rotation_euler', index=0, frame=f)
        sc.frame_set(10)
    sc.render.filepath = out or os.path.join(OUT, name + '.png')
    t = time.time()
    bpy.ops.render.render(write_still=True)
    if spec.get('upscale') and pct != 100:      # back to the full plate size (same camera), with OpenCV
        import subprocess
        subprocess.run(['python3', '-c', 'import cv2,sys; a=cv2.imread(sys.argv[1],-1); cv2.imwrite(sys.argv[1], cv2.resize(a,(int(sys.argv[2]),)*2, interpolation=cv2.INTER_LANCZOS4))',
                        sc.render.filepath, str(sc.render.resolution_x)], check=True)
    print(f'DONE {name} {time.time() - t:.0f}s', flush=True)
    return True


def open_blend():
    bpy.ops.wm.open_mainfile(filepath=os.path.join(OUT, 'turbo.blend'))


def queue(first=None, last=None, only=None):
    open_blend()
    for name, spec in job_list():
        if only and not any(name.startswith(o) for o in only): continue
        if os.path.exists(os.path.join(OUT, name + '.png')): continue
        open_blend()        # fresh state per job (materials / overrides)
        render_job(name, spec)


# --------------------------------------------------------------------------- projections for the compositor
def project(cam_name, pts, size):
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene; co = bpy.data.objects['cam_' + cam_name]
    sc.render.resolution_x = size; sc.render.resolution_y = size
    out = []
    for p in pts:
        v = world_to_camera_view(sc, co, Vector(p)); out.append([v.x * size, (1 - v.y) * size, v.z])
    return out


def info():
    """crops (tier pixels) + anchors / paths (T1 pixels of the main camera; transverse cameras in their own pixels)."""
    open_blend()
    S1 = BASE
    def bbox(pts, tier, pad):
        q = project('main', pts, S1)
        xs = [p[0] * tier for p in q]; ys = [p[1] * tier for p in q]
        return [int(max(0, min(xs) - pad)), int(max(0, min(ys) - pad)), int(min(S1 * tier, max(xs) + pad)), int(min(S1 * tier, max(ys) + pad))]
    def cloud(x0, x1, r, ylo=-1.0, n=24):
        pts = []
        for x in (x0, x1):
            for k in range(n):
                a = 2 * PI * k / n; y = r * math.cos(a); z = r * math.sin(a)
                if y >= ylo * r: pts.append((x, y, z))
        return pts
    C = {}
    C['T2'] = bbox(cloud(-42.0, 40.0, 36.0, 0.0) + [(0, 0, 52.0), (0, 0, -62.0), (-20, 12, -40), (20, 12, -40), (-18, 9, 32), (18, 9, 32)], 2, 30)
    C['T3'] = bbox(cloud(-33.0, 27.0, 13.0, 0.0) + [(0, 0, 16.0), (0, 0, -12.0)], 4, 30)
    C['LC'] = bbox(cloud(-74.0, -37.5, 27.5) + cloud(-56.0, -56.0, 27.5), 2, 24)
    C['LT'] = bbox(cloud(36.5, 70.0, 23.0) + cloud(46.0, 46.0, 23.0), 2, 24)
    json.dump(C, open(os.path.join(OUT, 'crops.json'), 'w'), indent=1)
    geo = json.load(open(os.path.join(OUT, 'geo.json')))
    A = {   # 3D anchors (mm)
        'comp_wheel': (-55.0, 0.0, 14.0), 'comp_nut': (-70.0, 0.0, 0.0), 'comp_housing': (-62.0, 0.0, -30.0), 'comp_inlet': (-96.0, 0.0, 0.0),
        'comp_outlet': tuple(geo['comp_outlet_end']), 'diffuser': (-42.0, 0.0, 31.0), 'volute_c_top': (-44.0, 0.0, 41.5), 'volute_c_bot': (-50.0, 0.0, -45.0),
        'backplate': (-36.0, 0.0, 22.0), 'chra': (0.0, 0.0, -20.5), 'chra_top': (0.0, 0.0, 21.5), 'oil_in': (0.0, 0.0, 31.0), 'oil_in_bore': (0.0, 0.0, 22.0),
        'gallery': (6.0, 0.0, GAL_Z), 'feed_t': (FEED_X, 0.0, 9.0), 'feed_c': (-FEED_X, 0.0, 9.0), 'drain': (0.0, 0.0, -34.0), 'drain_cav': (0.0, 0.0, -20.0),
        'bush_t': (FEED_X, 0.0, 5.3), 'bush_c': (-FEED_X, 0.0, 5.3), 'bush_t_bot': (FEED_X, 0.0, -5.3), 'bush_c_bot': (-FEED_X, 0.0, -5.3),
        'outer_t': (FEED_X, 0.0, 6.65), 'inner_t': (FEED_X, 0.0, 4.2), 'outer_c': (-FEED_X, 0.0, 6.65), 'inner_c': (-FEED_X, 0.0, 4.2),
        'outer_t_b': (FEED_X, 0.0, 6.5), 'sf_mid': (0.0, 0.0, 5.6), 'pin': (0.0, 0.0, -8.0), 'pin_low': (0.0, 0.0, -16.0),
        'shaft': (0.0, 0.0, 0.0), 'shaft_t': (FEED_X, 0.0, 0.0), 'shaft_c': (-FEED_X, 0.0, 0.0), 'shaft_top': (0.0, 0.0, 3.8),
        'thrust': (-27.4, 0.0, 9.5), 'thrust_low': (-27.4, 0.0, -9.5), 'collar': (-24.9, 0.0, 7.0), 'flinger': (-32.0, 0.0, 7.0), 'ring_c': (-36.5, 0.0, 5.0),
        'ring_t': (28.6, 0.0, 7.6), 'heat_shield': (34.0, 0.0, 15.0), 'turb_wheel': (52.0, 0.0, 12.0), 'turb_housing': (60.0, 0.0, 40.0),
        'vanes': (42.0, 0.0, 27.5), 'vanes_bot': (42.0, 0.0, -27.5), 'turb_outlet': (86.0, 0.0, 0.0), 'turb_inlet': tuple(geo['turb_inlet_start']),
        'volute_t_top': (48.0, 0.0, 44.0), 'volute_t_bot': (46.0, 0.0, -38.0), 'clip_t': (21.6, 0.0, 6.8), 'deflector': (-29.2, 0.0, 15.0),
    }
    res = {'crops': C, 'base': S1, 'anch': {k: project('main', [p], S1)[0] for k, p in A.items()}}
    # paths (3D polylines)
    P = {}
    P['air_in'] = [(-112.0, 0.0, z) for z in (0.0,)] + [(-90.0, 0.0, 0.0)]
    P['oil_in'] = [(0.0, 0.0, 34.0), (0.0, 0.0, GAL_Z)]
    P['gal_c'] = [(0.0, 0.0, GAL_Z), (-27.4, 0.0, GAL_Z), (-27.4, 0.0, 5.0)]
    P['gal_t'] = [(0.0, 0.0, GAL_Z), (FEED_X, 0.0, GAL_Z), (FEED_X, 0.0, 6.6)]
    P['gal_c2'] = [(-FEED_X, 0.0, GAL_Z), (-FEED_X, 0.0, 6.6)]
    res['paths3d'] = P
    res['paths'] = {k: project('main', v, S1) for k, v in P.items()}
    # helper: arbitrary point projection table for the compositor (grid on the section plane)
    res['M'] = [list(r) for r in (bpy.data.objects['cam_main'].matrix_world.inverted())]
    cd = bpy.data.objects['cam_main'].data
    res['lens'] = cd.lens; res['sensor'] = cd.sensor_width
    for tn in ('trA', 'trP'):
        co = bpy.data.objects['cam_' + tn]; St = int(BASE * 1.2)
        res[tn] = {'size': St, 'lens': co.data.lens, 'center': project(tn, [(CAM[tn]['trans'], 0, 0)], St)[0],
                   'px_per_mm': project(tn, [(CAM[tn]['trans'], 10.0, 0)], St)[0][0] - project(tn, [(CAM[tn]['trans'], 0, 0)], St)[0][0],
                   'up_per_mm': project(tn, [(CAM[tn]['trans'], 0, 10.0)], St)[0][1] - project(tn, [(CAM[tn]['trans'], 0, 0)], St)[0][1]}
    json.dump(res, open(os.path.join(OUT, 'info.json'), 'w'), indent=1)
    print('crops', C)


def prev(cam, tier, crop, vis, pct, spp, out, hold=''):
    open_blend()
    spec = dict(cam=cam, tier=int(tier) if tier.isdigit() else float(tier), crop=[int(v) for v in crop.split(',')] if crop else None,
                vis=vis.split(','), hold=hold.split(',') if hold else [])
    render_job('prev', spec, int(spp), int(pct), out)


if __name__ == '__main__':
    a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    if a[0] == 'build': build()
    elif a[0] == 'render':
        open_blend(); J = dict(job_list())
        render_job(a[1], J[a[1]], int(a[2]) if len(a) > 2 else None, int(a[3]) if len(a) > 3 else 100,
                   a[4] if len(a) > 4 else None)
    elif a[0] == 'queue':
        queue(only=a[1:] or None)
    elif a[0] == 'info': info()
    elif a[0] == 'prev': prev(*a[1:])
