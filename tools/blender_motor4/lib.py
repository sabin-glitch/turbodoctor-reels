"""Mesh, material and scene helpers for the 4-cylinder engine model (Blender 5.3, Cycles).
Units: 1 BU = 1 mm. Z up. Crankshaft axis = X. Cylinder 1 at -X (timing belt end).
Helpers follow the conventions of the CRI2 injector model (sursa/injector-cri2-blender/cri2.py).
"""
import bpy, bmesh, math
from mathutils import Vector, Matrix

TAU = 2 * math.pi


# --------------------------------------------------------------------------- collections / objects
def coll(name, parent=None):
    c = bpy.data.collections.get(name)
    if c is None:
        c = bpy.data.collections.new(name)
        (parent or bpy.context.scene.collection).children.link(c)
    return c


def move_to(ob, c):
    for cc in list(ob.users_collection):
        cc.objects.unlink(ob)
    c.objects.link(ob)
    return ob


def mesh_obj(name, verts, faces, c=None, clean=True):
    me = bpy.data.meshes.new(name)
    me.from_pydata([tuple(v) for v in verts], [], faces)
    me.validate()
    if clean:
        bm = bmesh.new(); bm.from_mesh(me)
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me)
    (c or bpy.context.scene.collection).objects.link(ob)
    return ob


def remove(ob):
    me = ob.data if ob.type == 'MESH' else None
    bpy.data.objects.remove(ob, do_unlink=True)
    if me is not None and me.users == 0:
        bpy.data.meshes.remove(me)


def dup(ob, name, c=None):
    o2 = ob.copy(); o2.data = ob.data.copy(); o2.name = name
    (c or ob.users_collection[0]).objects.link(o2)
    return o2


def apply_xform(ob):
    """bake object transform into mesh"""
    ob.data.transform(ob.matrix_world)
    ob.matrix_world = Matrix.Identity(4)
    return ob


def place(ob, loc=(0, 0, 0), rot=None):
    M = Matrix.Translation(Vector(loc))
    if rot is not None:
        M = M @ rot
    ob.data.transform(M)
    return ob


def join(obs, name):
    """join meshes (keeps materials); the result gets exactly `name`."""
    obs = [o for o in obs if o is not None]
    c = obs[0].users_collection[0]
    bm = bmesh.new()
    mats = []
    for o in obs:
        me = o.data.copy(); me.transform(o.matrix_world)
        mi_map = []
        for m in o.data.materials:
            if m not in mats: mats.append(m)
            mi_map.append(mats.index(m))
        if mi_map:
            for p in me.polygons:
                p.material_index = mi_map[p.material_index] if p.material_index < len(mi_map) else 0
        bm.from_mesh(me); bpy.data.meshes.remove(me)
    for o in obs: remove(o)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for m in mats: me.materials.append(m)
    ob = bpy.data.objects.new(name, me)
    c.objects.link(ob)
    return ob


# --------------------------------------------------------------------------- primitives
def frame_of(d):
    d = Vector(d).normalized()
    t = Vector((1, 0, 0)) if abs(d.x) < 0.9 else Vector((0, 1, 0))
    u = d.cross(t).normalized(); v = d.cross(u)
    return u, v, d


def revolve(name, prof, segs=64, c=None, axis='Z', center=(0, 0, 0), phase=0.5):
    """prof: closed polygon of (r, h), r >= 0; revolved around `axis` through `center`."""
    verts, faces, idx = [], [], []
    for r, z in prof:
        if r < 1e-9:
            idx.append([len(verts)] * segs); verts.append((0.0, 0.0, z))
        else:
            b = len(verts)
            for k in range(segs):
                a = TAU * (k + phase) / segs
                verts.append((r * math.cos(a), r * math.sin(a), z))
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
    ob = mesh_obj(name, verts, faces, c)
    R = Matrix.Identity(4)
    if axis == 'X': R = Matrix.Rotation(math.pi / 2, 4, 'Y')
    elif axis == 'Y': R = Matrix.Rotation(-math.pi / 2, 4, 'X')
    ob.data.transform(Matrix.Translation(Vector(center)) @ R)
    return ob


def cyl(name, p0, p1, r, segs=48, c=None, r1=None, phase=0.5):
    p0, p1 = Vector(p0), Vector(p1); r1 = r if r1 is None else r1
    u, v, d = frame_of(p1 - p0)
    verts, faces = [], []
    for p, rr in ((p0, r), (p1, r1)):
        for k in range(segs):
            a = TAU * (k + phase) / segs
            verts.append(tuple(p + (u * math.cos(a) + v * math.sin(a)) * rr))
    c0 = len(verts); verts.append(tuple(p0)); c1 = len(verts); verts.append(tuple(p1))
    for k in range(segs):
        k2 = (k + 1) % segs
        faces.append([k, k2, segs + k2, segs + k])
        faces.append([c0, k2, k]); faces.append([c1, segs + k, segs + k2])
    return mesh_obj(name, verts, faces, c)


def box(name, x0, x1, y0, y1, z0, z1, c=None):
    v = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    f = [[0, 3, 2, 1], [4, 5, 6, 7], [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7]]
    return mesh_obj(name, v, f, c)


def extrude(name, poly, d0, d1, plane='YZ', c=None):
    """prism from a simple 2D polygon (u, v) between depths d0..d1 along the plane normal.
    plane 'YZ': (u,v)=(y,z), depth=x ; 'XZ': (u,v)=(x,z), depth=y ; 'XY': (u,v)=(x,y), depth=z"""
    def P(u, v, d):
        if plane == 'YZ': return (d, u, v)
        if plane == 'XZ': return (u, d, v)
        return (u, v, d)
    # make polygon CCW
    area = sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1] for i in range(len(poly)))
    if area < 0: poly = poly[::-1]
    n = len(poly)
    bm = bmesh.new()
    vb = [bm.verts.new(P(u, v, d0)) for u, v in poly]
    vt = [bm.verts.new(P(u, v, d1)) for u, v in poly]
    bm.faces.new(vb[::-1]); bm.faces.new(vt)
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new([vb[i], vb[j], vt[j], vt[i]])
    bmesh.ops.triangulate(bm, faces=[f for f in bm.faces if len(f.verts) > 4])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me)
    (c or bpy.context.scene.collection).objects.link(ob)
    return ob


def arc_pts(cx, cy, r, a0, a1, n):
    return [(cx + r * math.cos(a0 + (a1 - a0) * k / n), cy + r * math.sin(a0 + (a1 - a0) * k / n)) for k in range(n + 1)]


def rounded_rect(u0, u1, v0, v1, r, n=6):
    r = min(r, (u1 - u0) / 2 - 1e-3, (v1 - v0) / 2 - 1e-3)
    pts = []
    pts += arc_pts(u1 - r, v0 + r, r, -math.pi / 2, 0, n)
    pts += arc_pts(u1 - r, v1 - r, r, 0, math.pi / 2, n)
    pts += arc_pts(u0 + r, v1 - r, r, math.pi / 2, math.pi, n)
    pts += arc_pts(u0 + r, v0 + r, r, math.pi, 1.5 * math.pi, n)
    return pts


def rbox(name, x0, x1, y0, y1, z0, z1, r, n=5, c=None):
    """box with rounded vertical (Z) edges"""
    return extrude(name, rounded_rect(x0, x1, y0, y1, r, n), z0, z1, 'XY', c)


def rmf_frames(pts):
    """rotation-minimizing frames along a polyline"""
    T = []
    for i in range(len(pts)):
        a = pts[max(i - 1, 0)]; b = pts[min(i + 1, len(pts) - 1)]
        T.append((b - a).normalized())
    u, v, _ = frame_of(T[0])
    U = [u]
    for i in range(1, len(pts)):
        uu = U[-1] - T[i] * U[-1].dot(T[i])
        U.append(uu.normalized())
    return T, U


def tube(name, pts, r, segs=24, c=None, cap=True, r_out=None):
    """swept circle along polyline pts (list of Vector-able). r can be a float or list per point."""
    pts = [Vector(p) for p in pts]
    T, U = rmf_frames(pts)
    rs = r if isinstance(r, (list, tuple)) else [r] * len(pts)
    verts, faces = [], []
    for i, p in enumerate(pts):
        u = U[i]; v = T[i].cross(u)
        for k in range(segs):
            a = TAU * (k + 0.5) / segs
            verts.append(tuple(p + (u * math.cos(a) + v * math.sin(a)) * rs[i]))
    n = len(pts)
    for i in range(n - 1):
        for k in range(segs):
            k2 = (k + 1) % segs
            faces.append([i * segs + k, (i + 1) * segs + k, (i + 1) * segs + k2, i * segs + k2])
    if cap:
        c0 = len(verts); verts.append(tuple(pts[0])); c1 = len(verts); verts.append(tuple(pts[-1]))
        for k in range(segs):
            k2 = (k + 1) % segs
            faces.append([c0, k2, k]); faces.append([c1, (n - 1) * segs + k, (n - 1) * segs + k2])
    return mesh_obj(name, verts, faces, c)


def bezier(p0, p1, p2, p3, n=24):
    p0, p1, p2, p3 = map(Vector, (p0, p1, p2, p3))
    out = []
    for i in range(n + 1):
        t = i / n
        out.append((1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1 + 3 * (1 - t) * t * t * p2 + t ** 3 * p3)
    return out


def fillet_path(pts, rad, n=8):
    """polyline with rounded corners (radius rad)"""
    pts = [Vector(p) for p in pts]
    out = [pts[0]]
    for i in range(1, len(pts) - 1):
        a, b, cc = pts[i - 1], pts[i], pts[i + 1]
        d1 = (a - b).normalized(); d2 = (cc - b).normalized()
        ang = math.acos(max(-1, min(1, d1.dot(d2))))
        if ang > math.pi - 1e-3:
            out.append(b); continue
        t = rad / math.tan(ang / 2)
        t = min(t, (a - b).length * 0.49, (cc - b).length * 0.49)
        q0 = b + d1 * t; q1 = b + d2 * t
        for k in range(n + 1):
            s = k / n
            out.append((1 - s) ** 2 * q0 + 2 * (1 - s) * s * b + s * s * q1)
    out.append(pts[-1])
    return out


def torus(name, center, axis, R, r, seg=64, seg2=16, c=None):
    u, v, d = frame_of(axis); cc = Vector(center)
    verts, faces = [], []
    for i in range(seg):
        a = TAU * (i + 0.5) / seg
        radial = (u * math.cos(a) + v * math.sin(a))
        ring_c = cc + radial * R
        for j in range(seg2):
            b = TAU * j / seg2
            verts.append(tuple(ring_c + radial * (r * math.cos(b)) + d * (r * math.sin(b))))
    for i in range(seg):
        i2 = (i + 1) % seg
        for j in range(seg2):
            j2 = (j + 1) % seg2
            faces.append([i * seg2 + j, i2 * seg2 + j, i2 * seg2 + j2, i * seg2 + j2])
    return mesh_obj(name, verts, faces, c)


def sphere(name, center, r, u=32, v=16, c=None):
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=u, v_segments=v, radius=r)
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me); (c or bpy.context.scene.collection).objects.link(ob)
    me.transform(Matrix.Translation(Vector(center)))
    return ob


def helix_verts(z0, z1, rm, rw, turns, ring=12, per_turn=48, flat=0.75):
    """coil spring along Z (closed ends: `flat` dead turns at each end)."""
    n = int(turns * per_turn)
    pts = []
    tot = turns
    for i in range(n + 1):
        t = i / n * tot
        # pitch profile: dead coils at both ends
        if t < flat: zz = 0.0 + (t / flat) * 0.0
        if True:
            act = tot - 2 * flat
            if t <= flat: s = 0.0
            elif t >= tot - flat: s = 1.0
            else: s = (t - flat) / act
            zz = s
        pts.append((t, zz))
    # coordinates; ends: wire resting -> z from z0+rw to z1-rw
    out = []
    zlo, zhi = z0 + rw, z1 - rw
    for t, s in pts:
        a = TAU * t
        dz = 0.0
        if t <= flat: dz = (t / flat) * 2 * rw * 0.5
        elif t >= tot - flat: dz = -((tot - t) / flat) * 2 * rw * 0.5
        zz = zlo + (zhi - zlo) * s
        if t <= flat: zz = zlo + (t / flat) * rw
        if t >= tot - flat: zz = zhi - ((tot - t) / flat) * rw
        out.append(Vector((rm * math.cos(a), rm * math.sin(a), zz)))
    verts, faces = [], []
    for i, p in enumerate(out):
        tg = (out[min(i + 1, n)] - out[max(i - 1, 0)]).normalized()
        u = Vector((p.x, p.y, 0)).normalized(); v = tg.cross(u).normalized(); u = v.cross(tg).normalized()
        for j in range(ring):
            b = TAU * j / ring
            verts.append(tuple(p + (u * math.cos(b) + v * math.sin(b)) * rw))
    for i in range(n):
        for j in range(ring):
            j2 = (j + 1) % ring
            faces.append([i * ring + j, (i + 1) * ring + j, (i + 1) * ring + j2, i * ring + j2])
    faces.append(list(range(ring))[::-1]); faces.append([n * ring + j for j in range(ring)])
    return verts, faces


def spring(name, z0, z1_free, z1_comp, rm, rw, turns, c=None, flat=0.8):
    """spring with a shape key 'comp' (top at z1_comp); basis top at z1_free. Bottom fixed at z0."""
    v0, f = helix_verts(z0, z1_free, rm, rw, turns, flat=flat)
    ob = mesh_obj(name, v0, f, c, clean=False)
    v1, _ = helix_verts(z0, z1_comp, rm, rw, turns, flat=flat)
    ob.shape_key_add(name='Basis')
    k = ob.shape_key_add(name='comp')
    for i, p in enumerate(v1):
        k.data[i].co = p
    return ob


# --------------------------------------------------------------------------- booleans / normals
def apply_bool(ob, cutter, op='DIFFERENCE'):
    m = ob.modifiers.new('b', 'BOOLEAN'); m.operation = op; m.object = cutter; m.solver = 'MANIFOLD'
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(ob.evaluated_get(dg))
    ob.modifiers.clear(); old = ob.data; ob.data = me; bpy.data.meshes.remove(old)
    return ob


def bool_many(ob, cutters, op='DIFFERENCE', keep=False):
    if not cutters: return ob
    if len(cutters) > 3:
        # union cutters first (faster, fewer passes)
        base = cutters[0]
        for c2 in cutters[1:]:
            apply_bool(base, c2, 'UNION')
        apply_bool(ob, base, op)
    else:
        for c2 in cutters:
            apply_bool(ob, c2, op)
    if not keep:
        for c2 in cutters:
            if c2.name in bpy.data.objects:
                remove(c2)
    return ob


def union(obs, name=None):
    base = obs[0]
    for o in obs[1:]:
        apply_bool(base, o, 'UNION'); remove(o)
    if name: base.name = name; base.data.name = name
    return base


def smooth(ob, ang=35):
    me = ob.data
    for p in me.polygons: p.use_smooth = True
    try:
        me.set_sharp_from_angle(angle=math.radians(ang))
    except Exception:
        pass
    return ob


def bevel(ob, width=1.0, seg=2, ang=40, apply=True):
    m = ob.modifiers.new('bev', 'BEVEL'); m.width = width; m.segments = seg
    m.limit_method = 'ANGLE'; m.angle_limit = math.radians(ang)
    m.harden_normals = False
    try: m.miter_outer = 'MITER_ARC'
    except Exception: pass
    if apply:
        dg = bpy.context.evaluated_depsgraph_get()
        me = bpy.data.meshes.new_from_object(ob.evaluated_get(dg))
        ob.modifiers.clear(); old = ob.data; ob.data = me; bpy.data.meshes.remove(old)
    return ob


def wnormals(ob):
    m = ob.modifiers.new('wn', 'WEIGHTED_NORMAL'); m.keep_sharp = True
    return ob


# --------------------------------------------------------------------------- materials
def srgb(h):
    c = [((h >> 16) & 255) / 255, ((h >> 8) & 255) / 255, (h & 255) / 255]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c)


def _n(nt, typ, **kw):
    n = nt.nodes.new(typ)
    for k, v in kw.items(): setattr(n, k, v)
    return n


def new_mat(name):
    m = bpy.data.materials.get(name)
    if m: return m, False
    m = bpy.data.materials.new(name)
    try: m.use_nodes = True
    except Exception: pass
    m.use_fake_user = True
    return m, True


def noise_bump(nt, b, scale, strength, dist=0.15, detail=6.0, rough_var=None, rough=None, coord='Object'):
    tc = nt.nodes.get('tc') or _n(nt, 'ShaderNodeTexCoord', name='tc')
    nz = _n(nt, 'ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = scale; nz.inputs['Detail'].default_value = detail
    nz.inputs['Roughness'].default_value = 0.62
    nt.links.new(tc.outputs[coord], nz.inputs['Vector'])
    bp = _n(nt, 'ShaderNodeBump'); bp.inputs['Strength'].default_value = strength; bp.inputs['Distance'].default_value = dist
    nt.links.new(nz.outputs['Fac'], bp.inputs['Height'])
    nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    if rough_var:
        mr = _n(nt, 'ShaderNodeMapRange'); mr.inputs['To Min'].default_value = rough - rough_var / 2; mr.inputs['To Max'].default_value = rough + rough_var / 2
        nt.links.new(nz.outputs['Fac'], mr.inputs['Value']); nt.links.new(mr.outputs['Result'], b.inputs['Roughness'])
    return bp


def mat_metal(name, col, rough, metal=1.0, aniso=0.0, bump=None, coat=0.0, bevel_r=0.0, spec=0.5):
    """bump = (scale, strength[, rough_var])"""
    m, new = new_mat(name)
    if not new: return m
    nt = m.node_tree; b = nt.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*col, 1); b.inputs['Metallic'].default_value = metal
    b.inputs['Roughness'].default_value = rough
    if aniso: b.inputs['Anisotropic'].default_value = aniso
    if coat: b.inputs['Coat Weight'].default_value = coat
    bp = None
    if bump:
        bp = noise_bump(nt, b, bump[0], bump[1], rough_var=bump[2] if len(bump) > 2 else None, rough=rough)
    if bevel_r:
        bv = _n(nt, 'ShaderNodeBevel'); bv.samples = 4; bv.inputs['Radius'].default_value = bevel_r
        if bp is not None:
            nt.links.new(bv.outputs['Normal'], bp.inputs['Normal'])
        else:
            nt.links.new(bv.outputs['Normal'], b.inputs['Normal'])
    return m


def mat_plastic(name, col, rough=0.45, bump=None):
    m, new = new_mat(name)
    if not new: return m
    nt = m.node_tree; b = nt.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*col, 1); b.inputs['Roughness'].default_value = rough
    b.inputs['Metallic'].default_value = 0.0
    if bump: noise_bump(nt, b, bump[0], bump[1])
    return m


def mat_section(name, col, line, ang=45.0, period=2.6, width=0.16, axis='Y', metal=0.45, rough=0.62):
    """matte cut face with hatching. axis = normal of the cut plane ('Y' -> hatch in x/z, 'X' -> hatch in y/z)."""
    m, new = new_mat(name)
    if not new: return m
    nt = m.node_tree; b = nt.nodes['Principled BSDF']
    b.inputs['Metallic'].default_value = metal; b.inputs['Roughness'].default_value = rough
    tc = _n(nt, 'ShaderNodeTexCoord'); sx = _n(nt, 'ShaderNodeSeparateXYZ')
    nt.links.new(tc.outputs['Object'], sx.inputs[0])
    ua, va = ('X', 'Z') if axis == 'Y' else (('Y', 'Z') if axis == 'X' else ('X', 'Y'))
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    m1 = _n(nt, 'ShaderNodeMath', operation='MULTIPLY'); m1.inputs[1].default_value = ca / period
    m2 = _n(nt, 'ShaderNodeMath', operation='MULTIPLY'); m2.inputs[1].default_value = sa / period
    nt.links.new(sx.outputs[ua], m1.inputs[0]); nt.links.new(sx.outputs[va], m2.inputs[0])
    ad = _n(nt, 'ShaderNodeMath', operation='ADD'); nt.links.new(m1.outputs[0], ad.inputs[0]); nt.links.new(m2.outputs[0], ad.inputs[1])
    fr = _n(nt, 'ShaderNodeMath', operation='FRACT'); nt.links.new(ad.outputs[0], fr.inputs[0])
    # anti-aliased line: smoothstep on distance to line centre
    s5 = _n(nt, 'ShaderNodeMath', operation='SUBTRACT'); s5.inputs[1].default_value = 0.5; nt.links.new(fr.outputs[0], s5.inputs[0])
    ab = _n(nt, 'ShaderNodeMath', operation='ABSOLUTE'); nt.links.new(s5.outputs[0], ab.inputs[0])
    mr = _n(nt, 'ShaderNodeMapRange', interpolation_type='SMOOTHSTEP')
    mr.inputs['From Min'].default_value = 0.5 - width; mr.inputs['From Max'].default_value = 0.5 - width * 0.55
    nt.links.new(ab.outputs[0], mr.inputs['Value'])
    mx = _n(nt, 'ShaderNodeMix', data_type='RGBA')
    mx.inputs[6].default_value = (*col, 1); mx.inputs[7].default_value = (*line, 1)
    nt.links.new(mr.outputs['Result'], mx.inputs[0]); nt.links.new(mx.outputs[2], b.inputs['Base Color'])
    return m


def obj_attr(nt, name):
    a = _n(nt, 'ShaderNodeAttribute'); a.attribute_type = 'OBJECT'; a.attribute_name = name
    return a


def mat_glow_fluid(name, col_a, col_b, emit=0.8, alpha=0.92, base_dark=True, prop='p', rough=0.2):
    """'graphic' liquid (Sabin's convention): dark glossy base + emission, colour mixes col_a->col_b
    by object custom property `prop` (0..1); alpha by object property 'a' (multiplied)."""
    m, new = new_mat(name)
    if not new: return m
    nt = m.node_tree; N = nt.nodes; L = nt.links
    b = N['Principled BSDF']; out = N['Material Output']
    b.inputs['Base Color'].default_value = (0.0, 0.0, 0.0, 1) if base_dark else (*col_a, 1)
    b.inputs['Roughness'].default_value = rough
    b.inputs['Emission Strength'].default_value = emit
    at = obj_attr(nt, prop)
    mx = _n(nt, 'ShaderNodeMix', data_type='RGBA'); mx.clamp_factor = True
    mx.inputs[6].default_value = (*col_a, 1); mx.inputs[7].default_value = (*col_b, 1)
    L.new(at.outputs['Fac'], mx.inputs[0])
    L.new(mx.outputs[2], b.inputs['Emission Color'])
    aa = obj_attr(nt, 'a')
    mul = _n(nt, 'ShaderNodeMath', operation='MULTIPLY'); mul.inputs[1].default_value = alpha
    L.new(aa.outputs['Fac'], mul.inputs[0])
    tr = _n(nt, 'ShaderNodeBsdfTransparent')
    ms = _n(nt, 'ShaderNodeMixShader')
    L.new(mul.outputs[0], ms.inputs[0]); L.new(tr.outputs[0], ms.inputs[1]); L.new(b.outputs[0], ms.inputs[2])
    L.new(ms.outputs[0], out.inputs['Surface'])
    return m


def mat_gas(name, emit_scale=1.0):
    """fake volume for cylinder gases, mostly additive (glow) with a slight darkening for smoke.
    object props: 'col' rgb, 'e' emission strength, 'a' opacity."""
    m, new = new_mat(name)
    if not new: return m
    nt = m.node_tree; N = nt.nodes; L = nt.links
    for n in list(N):
        if n.type != 'OUTPUT_MATERIAL': N.remove(n)
    out = N['Material Output']
    col = obj_attr(nt, 'col'); e = obj_attr(nt, 'e'); a = obj_attr(nt, 'a')
    lw = _n(nt, 'ShaderNodeLayerWeight'); lw.inputs['Blend'].default_value = 0.5
    inv = _n(nt, 'ShaderNodeMath', operation='SUBTRACT'); inv.inputs[0].default_value = 1.0
    L.new(lw.outputs['Facing'], inv.inputs[1])
    pw = _n(nt, 'ShaderNodeMath', operation='POWER'); pw.inputs[1].default_value = 1.5; L.new(inv.outputs[0], pw.inputs[0])
    tc = _n(nt, 'ShaderNodeTexCoord'); nz = _n(nt, 'ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 0.05
    nz.inputs['Detail'].default_value = 4.0; nz.inputs['Distortion'].default_value = 0.6
    L.new(tc.outputs['Object'], nz.inputs['Vector'])
    mr = _n(nt, 'ShaderNodeMapRange'); mr.inputs['From Min'].default_value = 0.32; mr.inputs['From Max'].default_value = 0.72
    mr.inputs['To Min'].default_value = 0.3; mr.inputs['To Max'].default_value = 1.0
    L.new(nz.outputs['Fac'], mr.inputs['Value'])
    k = _n(nt, 'ShaderNodeMath', operation='MULTIPLY'); L.new(pw.outputs[0], k.inputs[0]); L.new(mr.outputs['Result'], k.inputs[1])
    # emission (additive)
    em = _n(nt, 'ShaderNodeEmission'); L.new(col.outputs['Color'], em.inputs['Color'])
    es = _n(nt, 'ShaderNodeMath', operation='MULTIPLY'); L.new(e.outputs['Fac'], es.inputs[0]); L.new(k.outputs[0], es.inputs[1])
    es2 = _n(nt, 'ShaderNodeMath', operation='MULTIPLY'); es2.inputs[1].default_value = emit_scale; L.new(es.outputs[0], es2.inputs[0])
    L.new(es2.outputs[0], em.inputs['Strength'])
    # transmission: slight darkening proportional to opacity
    ka = _n(nt, 'ShaderNodeMath', operation='MULTIPLY'); L.new(k.outputs[0], ka.inputs[0]); L.new(a.outputs['Fac'], ka.inputs[1])
    tv = _n(nt, 'ShaderNodeMath', operation='MULTIPLY_ADD'); tv.inputs[1].default_value = -0.55; tv.inputs[2].default_value = 1.0
    L.new(ka.outputs[0], tv.inputs[0])
    tr = _n(nt, 'ShaderNodeBsdfTransparent'); cm = _n(nt, 'ShaderNodeCombineColor')
    for ch in ('Red', 'Green', 'Blue'): L.new(tv.outputs[0], cm.inputs[ch])
    L.new(cm.outputs[0], tr.inputs['Color'])
    ad = _n(nt, 'ShaderNodeAddShader'); L.new(tr.outputs[0], ad.inputs[0]); L.new(em.outputs[0], ad.inputs[1])
    L.new(ad.outputs[0], out.inputs['Surface'])
    return m


def set_mats(ob, surf, sec=None, plane=None, extra=None):
    """slot 0 = surface; slot 1 = section; faces lying on a cut plane get the section material.
    plane: list of (axis, value, sign) e.g. [('y', 0.0, -1)] = faces at y=0 with normal pointing -y."""
    me = ob.data
    me.materials.clear(); me.materials.append(surf)
    if sec is not None and plane:
        me.materials.append(sec)
        ai = {'x': 0, 'y': 1, 'z': 2}
        for p in me.polygons:
            for ax, val, sg in plane:
                i = ai[ax]
                if abs(p.center[i] - val) < 0.02 and p.normal[i] * sg > 0.97:
                    p.material_index = 1
                    break
    if extra:
        for mat, test in extra:
            me.materials.append(mat); mi = len(me.materials) - 1
            for p in me.polygons:
                if p.material_index == 0 and test(p):
                    p.material_index = mi
    return ob


def set_prop(ob, key, val):
    ob[key] = val


def key_prop(ob, key, val, frame):
    ob[key] = val
    ob.keyframe_insert(data_path=f'["{key}"]', frame=frame)
