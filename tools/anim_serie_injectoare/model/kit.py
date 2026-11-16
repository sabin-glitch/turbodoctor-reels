# Kit de modelare pentru Blender (bpy): solide din profile, tevi, SDF -> mesh (piese turnate), booleene, materiale.
# Unitati: milimetri in toate functiile; obiectele stau sub ROOT (scara 0.001), deci scena e in metri.
import bpy, bmesh, math
import numpy as np
from mathutils import Vector, Matrix

scn = None
ROOT = None

def init(empty=True):
    global scn, ROOT
    if empty:
        bpy.ops.wm.read_factory_settings(use_empty=True)
    scn = bpy.context.scene
    ROOT = bpy.data.objects.get('ROOT')
    if ROOT is None:
        ROOT = bpy.data.objects.new('ROOT', None)
        scn.collection.objects.link(ROOT)
        ROOT.scale = (0.001, 0.001, 0.001)
    return scn, ROOT

def W(p):
    """punct in mm (reperul ansamblului) -> lume (m)"""
    return Vector((p[0], p[1], p[2])) * 0.001

# ------------------------------------------------------------------ obiecte / mesh
def mesh_np(name, V, F, smooth=True, sharp=None):
    me = bpy.data.meshes.new(name)
    V = np.asarray(V, np.float32).reshape(-1, 3)
    F = np.asarray(F, np.int32)
    k = F.shape[1]
    me.vertices.add(len(V)); me.vertices.foreach_set('co', V.ravel())
    me.loops.add(F.size); me.loops.foreach_set('vertex_index', F.ravel())
    me.polygons.add(len(F)); me.polygons.foreach_set('loop_start', np.arange(0, F.size, k, dtype=np.int32))
    me.update(); me.validate()
    if smooth:
        me.polygons.foreach_set('use_smooth', np.ones(len(me.polygons), dtype=bool))
        if sharp is not None:
            me.set_sharp_from_angle(angle=math.radians(sharp))
    me.update()
    return me

def obj(name, me, mat=None, parent=None, loc=None, rot=None, scale=None):
    o = bpy.data.objects.new(name, me)
    scn.collection.objects.link(o)
    o.parent = parent if parent is not None else ROOT
    if loc is not None: o.location = loc
    if rot is not None: o.rotation_euler = rot
    if scale is not None: o.scale = scale
    if mat is not None and me is not None:
        if isinstance(mat, (list, tuple)):
            for m in mat: me.materials.append(m)
        else:
            me.materials.append(mat)
    return o

def empty(name, parent=None, loc=None, rot=None):
    o = bpy.data.objects.new(name, None)
    scn.collection.objects.link(o)
    o.parent = parent if parent is not None else ROOT
    if loc is not None: o.location = loc
    if rot is not None: o.rotation_euler = rot
    return o

def bm_to_mesh(bm, name, smooth=True, sharp=30):
    me = bpy.data.meshes.new(name)
    bm.normal_update()
    bm.to_mesh(me); bm.free()
    if smooth:
        me.polygons.foreach_set('use_smooth', np.ones(len(me.polygons), dtype=bool))
        if sharp is not None: me.set_sharp_from_angle(angle=math.radians(sharp))
    me.update()
    return me

def clean(me, dist=1e-4):
    bm = bmesh.new(); bm.from_mesh(me)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=dist)
    bmesh.ops.dissolve_degenerate(bm, edges=bm.edges, dist=dist)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free(); me.update()
    return me

def apply_mods(o):
    """aplica toti modificatorii (inlocuieste mesh-ul cu cel evaluat)"""
    dg = bpy.context.evaluated_depsgraph_get()
    dg.update()
    ev = o.evaluated_get(dg)
    me = bpy.data.meshes.new_from_object(ev, preserve_all_data_layers=True, depsgraph=dg)
    old = o.data
    o.modifiers.clear()
    o.data = me
    me.name = old.name
    if old.users == 0: bpy.data.meshes.remove(old)
    return o

def bevel(o, w=1.0, seg=2, angle=35, apply=True, harden=True):
    m = o.modifiers.new('bev', 'BEVEL')
    m.width = w; m.segments = seg; m.limit_method = 'ANGLE'; m.angle_limit = math.radians(angle)
    m.harden_normals = False
    if apply: apply_mods(o)
    return o

def boolean(o, cutter, op='DIFFERENCE', solver='EXACT', apply=True, remove_cutter=True):
    m = o.modifiers.new('bool', 'BOOLEAN')
    m.operation = op; m.object = cutter
    try: m.solver = solver
    except Exception: m.solver = 'EXACT'
    try: m.material_mode = 'TRANSFER'
    except Exception: pass
    if apply:
        apply_mods(o)
        if remove_cutter:
            cm = cutter.data
            bpy.data.objects.remove(cutter)
            if cm and cm.users == 0: bpy.data.meshes.remove(cm)
    return o

def join(objs, name=None):
    """uneste mai multe obiecte intr-unul (pastreaza materialele)"""
    objs = [o for o in objs if o is not None]
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join()
    r = bpy.context.view_layer.objects.active
    if name: r.name = name; r.data.name = name
    return r

def shade(o, sharp=30):
    me = o.data
    me.polygons.foreach_set('use_smooth', np.ones(len(me.polygons), dtype=bool))
    if sharp is not None: me.set_sharp_from_angle(angle=math.radians(sharp))
    me.update(); return o

def set_mat_all(o, mat):
    o.data.materials.clear(); o.data.materials.append(mat)

# ------------------------------------------------------------------ primitive
def box(name, size, c=(0, 0, 0), mat=None, bev=0.0, seg=2, parent=None):
    sx, sy, sz = size
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.x *= sx; v.co.y *= sy; v.co.z *= sz
    me = bm_to_mesh(bm, name, smooth=bev > 0)
    o = obj(name, me, mat, parent, loc=c)
    if bev > 0: bevel(o, bev, seg)
    return o

def cyl(name, r, h, c=(0, 0, 0), axis='Z', mat=None, seg=48, r2=None, bev=0.0, bseg=2, parent=None, caps=True):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=caps, cap_tris=False, segments=seg, radius1=r, radius2=(r if r2 is None else r2), depth=h)
    me = bm_to_mesh(bm, name, smooth=True, sharp=40)
    rot = {'Z': (0, 0, 0), 'X': (0, math.pi / 2, 0), 'Y': (-math.pi / 2, 0, 0)}[axis]
    o = obj(name, me, mat, parent, loc=c, rot=rot)
    if bev > 0: bevel(o, bev, bseg, angle=40)
    return o

def rod(name, a, b, r, mat=None, seg=24, r2=None, parent=None, bev=0.0):
    a = Vector(a); b = Vector(b); d = b - a
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=seg, radius1=r, radius2=(r if r2 is None else r2), depth=d.length)
    me = bm_to_mesh(bm, name, smooth=True, sharp=40)
    o = obj(name, me, mat, parent, loc=(a + b) / 2)
    o.rotation_mode = 'QUATERNION'
    o.rotation_quaternion = d.to_track_quat('Z', 'Y')
    if bev > 0: bevel(o, bev, 2, angle=40)
    return o

def lathe(name, prof, seg=64, mat=None, parent=None, loc=None, rot=None, axis='Z', sharp=30, closed=True, deg=360.0, a0=0.0):
    """corp de revolutie: prof = [(r, z), ...] (contur inchis daca closed). axa locala Z."""
    P = np.asarray(prof, np.float32)
    n = len(P)
    full = abs(deg - 360.0) < 1e-6
    ns = seg if full else seg + 1
    ang = np.radians(a0) + np.radians(deg) * np.arange(ns) / seg
    ca, sa = np.cos(ang), np.sin(ang)
    V = np.zeros((ns, n, 3), np.float32)
    V[:, :, 0] = ca[:, None] * P[None, :, 0]
    V[:, :, 1] = sa[:, None] * P[None, :, 0]
    V[:, :, 2] = P[None, :, 1]
    F = []
    m = n if closed else n - 1
    for i in range(seg if not full else ns):
        i2 = (i + 1) % ns if full else i + 1
        for j in range(m):
            j2 = (j + 1) % n
            F.append((i * n + j, i2 * n + j, i2 * n + j2, i * n + j2))
    V = V.reshape(-1, 3)
    if not full and closed:
        # capace la capetele sectorului
        me = bpy.data.meshes.new(name)
        faces = [tuple(f) for f in F]
        faces.append(tuple(range(0, n)))
        faces.append(tuple(reversed(range((ns - 1) * n, ns * n))))
        me.from_pydata(V.tolist(), [], faces); me.update()
    else:
        me = mesh_np(name, V, np.array(F, np.int32), smooth=False)
    clean(me, 1e-5)
    me.polygons.foreach_set('use_smooth', np.ones(len(me.polygons), dtype=bool))
    if sharp is not None: me.set_sharp_from_angle(angle=math.radians(sharp))
    me.update()
    r = {'Z': (0, 0, 0), 'X': (0, math.pi / 2, 0), 'Y': (-math.pi / 2, 0, 0)}[axis] if rot is None else rot
    return obj(name, me, mat, parent, loc=loc, rot=r)

# ------------------------------------------------------------------ curbe si tevi
def catmull(pts, n_per=12, closed=False):
    """interpolare Catmull-Rom centripeta simplificata prin puncte (N,3) -> (M,3)"""
    P = np.asarray(pts, np.float64)
    if len(P) < 3: return np.linspace(P[0], P[-1], n_per + 1)
    if closed:
        Q = np.vstack([P[-1], P, P[0], P[1]])
    else:
        Q = np.vstack([2 * P[0] - P[1], P, 2 * P[-1] - P[-2]])
    out = []
    ns = len(Q) - 3
    for i in range(ns):
        p0, p1, p2, p3 = Q[i], Q[i + 1], Q[i + 2], Q[i + 3]
        t = np.linspace(0, 1, n_per, endpoint=False)[:, None]
        out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    if not closed: out.append(P[-1][None, :])
    return np.vstack(out)

def fillet_path(pts, r, n=8):
    """polilinie cu colturi rotunjite (raza r): pentru tevi indoite ca in realitate"""
    P = [np.asarray(p, np.float64) for p in pts]
    out = [P[0]]
    for i in range(1, len(P) - 1):
        a, p, b = P[i - 1], P[i], P[i + 1]
        d1 = a - p; d2 = b - p; l1 = np.linalg.norm(d1); l2 = np.linalg.norm(d2); d1 /= l1; d2 /= l2
        th = math.acos(max(-1.0, min(1.0, float(d1 @ d2))))
        if th > math.pi - 1e-3:
            out.append(p); continue
        rr = r[i] if isinstance(r, (list, tuple)) else r
        t = rr / math.tan(th / 2); tm = min(l1, l2) * 0.49
        if t > tm: t = tm; rr = t * math.tan(th / 2)
        p1 = p + d1 * t; p2 = p + d2 * t
        bis = (d1 + d2); bis /= np.linalg.norm(bis)
        c = p + bis * (rr / math.sin(th / 2))
        v1 = p1 - c; v2 = p2 - c
        ax = np.cross(v1, v2); ax /= np.linalg.norm(ax)
        tot = math.acos(max(-1.0, min(1.0, float(v1 @ v2) / (rr * rr))))
        for k in range(n + 1):
            a_ = tot * k / n
            v = v1 * math.cos(a_) + np.cross(ax, v1) * math.sin(a_) + ax * (ax @ v1) * (1 - math.cos(a_))
            out.append(c + v)
    out.append(P[-1])
    return np.array(out)

def frames(P):
    """repere cu transport paralel de-a lungul polilinii P -> (T, N, B)"""
    P = np.asarray(P, np.float64)
    T = np.zeros_like(P)
    T[1:-1] = P[2:] - P[:-2]; T[0] = P[1] - P[0]; T[-1] = P[-1] - P[-2]
    T /= np.maximum(1e-12, np.linalg.norm(T, axis=1))[:, None]
    N = np.zeros_like(P); B = np.zeros_like(P)
    up = np.array([0, 0, 1.0]) if abs(T[0][2]) < 0.9 else np.array([1.0, 0, 0])
    n = np.cross(up, T[0]); n /= np.linalg.norm(n)
    N[0] = n; B[0] = np.cross(T[0], n)
    for i in range(1, len(P)):
        v = np.cross(T[i - 1], T[i]); s = np.linalg.norm(v)
        if s < 1e-9:
            N[i] = N[i - 1]
        else:
            v /= s; a = math.atan2(s, float(T[i - 1] @ T[i]))
            n = N[i - 1]
            N[i] = n * math.cos(a) + np.cross(v, n) * math.sin(a) + v * (v @ n) * (1 - math.cos(a))
        N[i] -= T[i] * (N[i] @ T[i]); N[i] /= np.linalg.norm(N[i])
        B[i] = np.cross(T[i], N[i])
    return T, N, B

def tube_mesh(name, P, r, seg=24, caps=True, r_in=None, squash=None):
    """teava de-a lungul polilinii P (M,3); r scalar sau (M,). r_in -> perete gros (teava goala)"""
    P = np.asarray(P, np.float64); M = len(P)
    R = np.full(M, r, np.float64) if np.isscalar(r) else np.asarray(r, np.float64)
    T, N, B = frames(P)
    ang = 2 * np.pi * np.arange(seg) / seg
    ca, sa = np.cos(ang), np.sin(ang)
    sq = (1.0, 1.0) if squash is None else squash
    def ring(rad):
        return P[:, None, :] + (N[:, None, :] * (ca[None, :, None] * sq[0]) + B[:, None, :] * (sa[None, :, None] * sq[1])) * rad[:, None, None]
    Vo = ring(R).reshape(-1, 3)
    F = []
    for i in range(M - 1):
        for j in range(seg):
            j2 = (j + 1) % seg
            F.append((i * seg + j, i * seg + j2, (i + 1) * seg + j2, (i + 1) * seg + j))
    V = Vo
    if r_in is not None:
        Ri = np.full(M, r_in, np.float64) if np.isscalar(r_in) else np.asarray(r_in, np.float64)
        Vi = ring(Ri).reshape(-1, 3); o = M * seg
        V = np.vstack([Vo, Vi])
        for i in range(M - 1):
            for j in range(seg):
                j2 = (j + 1) % seg
                F.append((o + i * seg + j, o + (i + 1) * seg + j, o + (i + 1) * seg + j2, o + i * seg + j2))
        for e in (0, M - 1):
            for j in range(seg):
                j2 = (j + 1) % seg
                q = (e * seg + j, e * seg + j2, o + e * seg + j2, o + e * seg + j)
                F.append(q if e == M - 1 else q[::-1])
        me = mesh_np(name, V, np.array(F, np.int32), smooth=True, sharp=50)
    else:
        me = bpy.data.meshes.new(name)
        faces = [tuple(f) for f in F]
        if caps:
            faces.append(tuple(reversed(range(0, seg))))
            faces.append(tuple(range((M - 1) * seg, M * seg)))
        me.from_pydata(V.tolist(), [], faces); me.update()
        me.polygons.foreach_set('use_smooth', np.ones(len(me.polygons), dtype=bool))
        me.set_sharp_from_angle(angle=math.radians(50)); me.update()
    return me

def tube(name, pts, r, mat=None, seg=24, fillet=None, smooth_n=0, caps=True, r_in=None, parent=None, squash=None):
    if fillet: P = fillet_path(pts, fillet)
    elif smooth_n: P = catmull(pts, smooth_n)
    else: P = np.asarray(pts, np.float64)
    me = tube_mesh(name, P, r, seg, caps, r_in, squash)
    return obj(name, me, mat, parent)

def path_len(P):
    P = np.asarray(P, np.float64)
    d = np.linalg.norm(P[1:] - P[:-1], axis=1)
    return np.concatenate([[0], np.cumsum(d)])

def resample(P, n):
    P = np.asarray(P, np.float64); s = path_len(P)
    u = np.linspace(0, s[-1], n)
    return np.stack([np.interp(u, s, P[:, k]) for k in range(3)], axis=1)

# ------------------------------------------------------------------ SDF vectorizat (numpy) -> mesh (marching cubes)
class S:
    @staticmethod
    def sphere(c, r):
        c = np.asarray(c, np.float32)
        return lambda P: np.linalg.norm(P - c, axis=1) - r
    @staticmethod
    def box(c, h, r=0.0):
        c = np.asarray(c, np.float32); h = np.asarray(h, np.float32)
        def f(P):
            q = np.abs(P - c) - (h - r)
            return np.linalg.norm(np.maximum(q, 0), axis=1) + np.minimum(q.max(axis=1), 0) - r
        return f
    @staticmethod
    def cyl(ax, c, r, hh, rd=0.0):
        c = np.asarray(c, np.float32); i, j = (ax + 1) % 3, (ax + 2) % 3
        def f(P):
            dr = np.hypot(P[:, i] - c[i], P[:, j] - c[j]) - r + rd
            dh = np.abs(P[:, ax] - c[ax]) - hh + rd
            return np.minimum(np.maximum(dr, dh), 0) + np.hypot(np.maximum(dr, 0), np.maximum(dh, 0)) - rd
        return f
    @staticmethod
    def capsule(a, b, r, r2=None):
        a = np.asarray(a, np.float32); b = np.asarray(b, np.float32); ba = b - a; bb = float(ba @ ba)
        def f(P):
            pa = P - a
            h = np.clip((pa @ ba) / bb, 0, 1)
            d = np.linalg.norm(pa - ba[None, :] * h[:, None], axis=1)
            return d - (r if r2 is None else r + (r2 - r) * h)
        return f
    @staticmethod
    def cone(a, b, r1, r2, rd=0.0):
        """trunchi de con cu capete plane intre a (r1) si b (r2)"""
        a = np.asarray(a, np.float32); b = np.asarray(b, np.float32); ba = b - a; l = float(np.linalg.norm(ba)); d = ba / l
        def f(P):
            q = P - a
            h = q @ d
            rad = np.linalg.norm(q - d[None, :] * h[:, None], axis=1)
            rr = r1 + (r2 - r1) * np.clip(h / l, 0, 1)
            dr = rad - rr + rd; dh = np.maximum(-h, h - l) + rd
            return np.minimum(np.maximum(dr, dh), 0) + np.hypot(np.maximum(dr, 0), np.maximum(dh, 0)) - rd
        return f
    @staticmethod
    def torus(ax, c, R, r):
        c = np.asarray(c, np.float32); i, j = (ax + 1) % 3, (ax + 2) % 3
        return lambda P: np.hypot(np.hypot(P[:, i] - c[i], P[:, j] - c[j]) - R, P[:, ax] - c[ax]) - r
    @staticmethod
    def plane(n, d):
        n = np.asarray(n, np.float32)
        return lambda P: P @ n - d
    @staticmethod
    def path(P, r):
        """teava (reuniune de capsule) de-a lungul polilinii; r scalar sau per punct"""
        P = np.asarray(P, np.float32); R = np.full(len(P), r, np.float32) if np.isscalar(r) else np.asarray(r, np.float32)
        def f(X):
            m = np.full(len(X), 1e9, np.float32)
            for k in range(len(P) - 1):
                a, b = P[k], P[k + 1]; ba = b - a; bb = float(ba @ ba)
                if bb < 1e-9: continue
                pa = X - a; h = np.clip((pa @ ba) / bb, 0, 1)
                d = np.linalg.norm(pa - ba[None, :] * h[:, None], axis=1) - (R[k] + (R[k + 1] - R[k]) * h)
                m = np.minimum(m, d)
            return m
        return f
    @staticmethod
    def u(*f):
        def g(P):
            m = f[0](P)
            for h in f[1:]: m = np.minimum(m, h(P))
            return m
        return g
    @staticmethod
    def i(*f):
        def g(P):
            m = f[0](P)
            for h in f[1:]: m = np.maximum(m, h(P))
            return m
        return g
    @staticmethod
    def d(a, b):
        return lambda P: np.maximum(a(P), -b(P))
    @staticmethod
    def su(k, *f):
        def g(P):
            m = f[0](P)
            for fn in f[1:]:
                v = fn(P); h = np.maximum(k - np.abs(m - v), 0) / k
                m = np.minimum(m, v) - h * h * k * 0.25
            return m
        return g
    @staticmethod
    def sd(k, a, b):
        def g(P):
            m = a(P); v = -b(P); h = np.maximum(k - np.abs(m - v), 0) / k
            return np.maximum(m, v) + h * h * k * 0.25
        return g
    @staticmethod
    def si(k, a, b):
        def g(P):
            m = a(P); v = b(P); h = np.maximum(k - np.abs(m - v), 0) / k
            return np.maximum(m, v) + h * h * k * 0.25
        return g
    @staticmethod
    def round(f, r):
        return lambda P: f(P) - r
    @staticmethod
    def shell(f, t):
        return lambda P: np.abs(f(P)) - t

def sdf_mesh(name, f, bmin, bmax, voxel, sec=None):
    """evalueaza SDF-ul pe o grila si extrage suprafata (marching cubes). Intoarce bpy mesh (in mm).
    Limitele grilei taie piesa cu fete plane; sec = [(axa, valoare), ...] -> fetele de pe acele limite primesc materialul 1."""
    from skimage import measure
    bmin = np.asarray(bmin, np.float64); bmax = np.asarray(bmax, np.float64)
    n = np.maximum(2, np.round((bmax - bmin) / voxel).astype(int) + 1)
    sp = (bmax - bmin) / (n - 1)
    xs = (bmin[0] + sp[0] * np.arange(n[0])).astype(np.float32)
    ys = (bmin[1] + sp[1] * np.arange(n[1])).astype(np.float32)
    zs = (bmin[2] + sp[2] * np.arange(n[2])).astype(np.float32)
    vol = np.empty((n[0], n[1], n[2]), np.float32)
    Y, Z = np.meshgrid(ys, zs, indexing='ij')
    yz = np.stack([Y.ravel(), Z.ravel()], axis=1)
    slab = max(1, int(1_500_000 // max(1, len(yz))))
    for i0 in range(0, n[0], slab):
        i1 = min(n[0], i0 + slab)
        P = np.empty(((i1 - i0) * len(yz), 3), np.float32)
        P[:, 0] = np.repeat(xs[i0:i1], len(yz)); P[:, 1] = np.tile(yz[:, 0], i1 - i0); P[:, 2] = np.tile(yz[:, 1], i1 - i0)
        vol[i0:i1] = f(P).reshape(i1 - i0, n[1], n[2])
    e = 0.004 * float(sp.min())
    vol[0, :, :] = np.maximum(vol[0, :, :], e); vol[-1, :, :] = np.maximum(vol[-1, :, :], e)
    vol[:, 0, :] = np.maximum(vol[:, 0, :], e); vol[:, -1, :] = np.maximum(vol[:, -1, :], e)
    vol[:, :, 0] = np.maximum(vol[:, :, 0], e); vol[:, :, -1] = np.maximum(vol[:, :, -1], e)
    V, F, Nn, _ = measure.marching_cubes(vol, 0.0, spacing=tuple(float(x) for x in sp))
    V = V + bmin[None, :].astype(np.float32)
    me = mesh_np(name, V, F.astype(np.int32), smooth=True)
    if sec:
        co = np.zeros(len(me.vertices) * 3, np.float32); me.vertices.foreach_get('co', co); co = co.reshape(-1, 3)
        lv = np.zeros(len(me.loops), np.int32); me.loops.foreach_get('vertex_index', lv); lv = lv.reshape(-1, 3)
        mi = np.zeros(len(me.polygons), np.int32)
        for (ax, val) in sec:
            tol = 0.45 * float(sp[ax])
            on = np.abs(co[:, ax] - val) < tol
            mi[on[lv].all(axis=1)] = 1
        me.polygons.foreach_set('material_index', mi)
    return me

def sdf_obj(name, f, bmin, bmax, voxel, mat=None, parent=None, decimate=None, planar=None, sec=None, sharp=55):
    me = sdf_mesh(name, f, bmin, bmax, voxel, sec=sec)
    o = obj(name, me, mat, parent)
    if planar is not None:
        m = o.modifiers.new('dis', 'DECIMATE'); m.decimate_type = 'DISSOLVE'; m.angle_limit = math.radians(planar)
        try: m.delimit = {'MATERIAL'}
        except Exception: pass
        apply_mods(o)
        o.modifiers.new('tri', 'TRIANGULATE'); apply_mods(o)
    if decimate is not None:
        m = o.modifiers.new('dec', 'DECIMATE'); m.ratio = decimate
        apply_mods(o)
    shade(o, sharp)
    return o

# ------------------------------------------------------------------ materiale
def srgb(h, a=1.0):
    c = [((h >> 16) & 255) / 255, ((h >> 8) & 255) / 255, (h & 255) / 255]
    return [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c] + [a]

GHOSTS = {}   # grup -> lista de (material)

def pbr(name, col, metal=0.0, rough=0.5, bump=None, aniso=0.0, coat=0.0, emis=None, emis_str=0.0, mix=None, spec=None,
        ghost=None, alpha=None, transmission=0.0, ior=None, sss=None, vcol=False):
    """material Principled. bump=(scara, tarie[, variatie asperitate]); mix=(culoare2, scara zgomot, contrast) pete de culoare;
    ghost='grup' -> alfa comandat pe cadru (transparenta de tip raze X)."""
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; N = nt.nodes; L = nt.links
    b = N['Principled BSDF']
    b.inputs['Base Color'].default_value = srgb(col)
    b.inputs['Metallic'].default_value = metal
    b.inputs['Roughness'].default_value = rough
    if aniso: b.inputs['Anisotropic'].default_value = aniso
    if coat: b.inputs['Coat Weight'].default_value = coat
    if spec is not None: b.inputs['Specular IOR Level'].default_value = spec
    if transmission: b.inputs['Transmission Weight'].default_value = transmission
    if ior: b.inputs['IOR'].default_value = ior
    tc = N.new('ShaderNodeTexCoord')
    if mix:
        nz = N.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = mix[1]; nz.inputs['Detail'].default_value = 5
        L.new(tc.outputs['Object'], nz.inputs['Vector'])
        cr = N.new('ShaderNodeValToRGB')
        c = mix[2] if len(mix) > 2 else 0.25
        cr.color_ramp.elements[0].position = 0.5 - c; cr.color_ramp.elements[0].color = srgb(col)
        cr.color_ramp.elements[1].position = 0.5 + c; cr.color_ramp.elements[1].color = srgb(mix[0])
        L.new(nz.outputs['Fac'], cr.inputs['Fac']); L.new(cr.outputs['Color'], b.inputs['Base Color'])
    if bump:
        nz = N.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = bump[0]; nz.inputs['Detail'].default_value = 6
        L.new(tc.outputs['Object'], nz.inputs['Vector'])
        if len(bump) > 2:
            mr = N.new('ShaderNodeMapRange'); mr.inputs['To Min'].default_value = max(0.02, rough - bump[2] / 2); mr.inputs['To Max'].default_value = min(1.0, rough + bump[2] / 2)
            L.new(nz.outputs['Fac'], mr.inputs['Value']); L.new(mr.outputs['Result'], b.inputs['Roughness'])
        bp = N.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = bump[1]; bp.inputs['Distance'].default_value = 0.05
        L.new(nz.outputs['Fac'], bp.inputs['Height']); L.new(bp.outputs['Normal'], b.inputs['Normal'])
    if emis is not None:
        b.inputs['Emission Color'].default_value = srgb(emis); b.inputs['Emission Strength'].default_value = emis_str
    if alpha is not None:
        b.inputs['Alpha'].default_value = alpha
    if ghost:
        v = N.new('ShaderNodeValue'); v.name = 'GHOST'; v.outputs[0].default_value = 1.0
        L.new(v.outputs[0], b.inputs['Alpha'])
        GHOSTS.setdefault(ghost, []).append(m)
        m['ghost'] = ghost
    try:
        m.cycles.emission_sampling = 'NONE'
    except Exception: pass
    return m

def set_ghost(group, alpha):
    for m in bpy.data.materials:
        if m.get('ghost') == group and m.node_tree:
            n = m.node_tree.nodes.get('GHOST')
            if n: n.outputs[0].default_value = alpha
