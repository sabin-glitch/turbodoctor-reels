"""Modelling kit for the Turbo Doctor Blender models (mesh helpers, booleans, materials).
Taken from tools/blender_turbo_lagare/turbo.py (same conventions: 1 BU = 1 mm, MANIFOLD booleans)."""
import bpy, bmesh, math
from mathutils import Vector, Matrix

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


def rot_from_x(axis):
    """4x4 rotation taking +X to the unit vector `axis`."""
    return Vector((1.0, 0.0, 0.0)).rotation_difference(Vector(axis).normalized()).to_matrix().to_4x4()


def revolve_z(name, prof, segs=96):
    """prof: (r, z) polygon revolved around the Z axis."""
    ob = revolve_x(name, [(z, r) for (r, z) in prof], segs=segs)
    ob.data.transform(Matrix.Rotation(-PI / 2, 4, 'Y'))
    return ob


def hexbolt(name, base, axis, af=10.0, h=6.0, shank=None):
    """bolt head (+washer) standing on `base`, head pointing along `axis`; optional shank (length, radius) the other way."""
    parts = bolt_head(name, (0.0, 0.0, 0.0), +1, af=af, h=h)
    if shank:
        L, r = shank
        s = cyl(name + '_s', (-L, 0.0, 0.0), (0.5, 0.0, 0.0), r, segs=32)
        apply_bool(parts[0], s, 'UNION'); bpy.data.objects.remove(s, do_unlink=True)
    M = Matrix.Translation(Vector(base)) @ rot_from_x(axis)
    for o in parts: o.data.transform(M)
    return parts


def stadium2(A, B, rr, n=16):
    """2D stadium between points A and B (tuples), radius rr."""
    A = Vector(A); B = Vector(B); d = (B - A).normalized(); nr = Vector((-d.y, d.x)); pts = []
    for k in range(n + 1):
        a = -PI / 2 + PI * k / n; pts.append(tuple(B + (d * math.cos(a) + nr * math.sin(a)) * rr))
    for k in range(n + 1):
        a = PI / 2 + PI * k / n; pts.append(tuple(A + (d * math.cos(a) + nr * math.sin(a)) * rr))
    return pts



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

