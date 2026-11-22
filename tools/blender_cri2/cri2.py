"""Bosch CRI2 solenoid-valve injector (ball valve, 0445110 type), built in Blender in section.
Units: 1 BU = 1 mm, nozzle tip at z = 0, axis = Z, high-pressure inlet on +X, section plane y = 0 (back half kept).
Proportions reconstructed from Bosch exploded views and Bosch patents; movements are exaggerated for the animation.

  python cri2.py build                 -> out/cri2.blend
  python cri2.py render <cam> <layer> [scale]   -> out/<cam>_<layer>.png
  python cri2.py info                  -> out/info.json (cameras, anchors, paths in pixels)
"""
import bpy, bmesh, math, json, os, sys
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
os.makedirs(OUT, exist_ok=True)
SEG = 128

# exaggerated strokes (mm)
LIFT_NEEDLE = 2.5
LIFT_ARM = 0.6

# --------------------------------------------------------------------------- mesh helpers
def mesh_obj(name, verts, faces, coll=None):
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.validate()
    bm = bmesh.new(); bm.from_mesh(me)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me)
    (coll or bpy.context.scene.collection).objects.link(ob)
    return ob


def revolve(name, prof, segs=SEG, coll=None):
    """prof: closed polygon of (r, z), r >= 0 (points with r=0 sit on the axis)."""
    verts, faces, idx = [], [], []
    for r, z in prof:
        if r < 1e-9:
            idx.append([len(verts)] * segs); verts.append((0.0, 0.0, z))
        else:
            b = len(verts)
            for k in range(segs):
                a = 2 * math.pi * (k + 0.5) / segs
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
    return mesh_obj(name, verts, faces, coll)


def frame_of(d):
    d = Vector(d).normalized()
    t = Vector((1, 0, 0)) if abs(d.x) < 0.9 else Vector((0, 1, 0))
    u = d.cross(t).normalized(); v = d.cross(u)
    return u, v, d


def cyl(name, p0, p1, r, segs=48, coll=None, r1=None):
    p0, p1 = Vector(p0), Vector(p1); r1 = r if r1 is None else r1
    u, v, d = frame_of(p1 - p0)
    verts, faces = [], []
    for p, rr in ((p0, r), (p1, r1)):
        for k in range(segs):
            a = 2 * math.pi * (k + 0.5) / segs
            verts.append(tuple(p + (u * math.cos(a) + v * math.sin(a)) * rr))
    c0 = len(verts); verts.append(tuple(p0)); c1 = len(verts); verts.append(tuple(p1))
    for k in range(segs):
        k2 = (k + 1) % segs
        faces.append([k, k2, segs + k2, segs + k])
        faces.append([c0, k2, k]); faces.append([c1, segs + k, segs + k2])
    return mesh_obj(name, verts, faces, coll)


def box(name, x0, x1, y0, y1, z0, z1, coll=None):
    v = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    f = [[0, 3, 2, 1], [4, 5, 6, 7], [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7]]
    return mesh_obj(name, v, f, coll)


def prism(name, n, apothem, z0, z1, rot=0.0, coll=None):
    R = apothem / math.cos(math.pi / n)
    v = []
    for z in (z0, z1):
        for k in range(n):
            a = rot + 2 * math.pi * k / n
            v.append((R * math.cos(a), R * math.sin(a), z))
    v.append((0, 0, z0)); v.append((0, 0, z1)); c0, c1 = 2 * n, 2 * n + 1
    f = []
    for k in range(n):
        k2 = (k + 1) % n
        f.append([k, k2, n + k2, n + k]); f.append([c0, k2, k]); f.append([c1, n + k, n + k2])
    return mesh_obj(name, v, f, coll)


def torus(name, center, axis, R, r, seg=64, seg2=16, coll=None):
    u, v, d = frame_of(axis); c = Vector(center)
    verts, faces = [], []
    for i in range(seg):
        a = 2 * math.pi * (i + 0.5) / seg
        ring_c = c + (u * math.cos(a) + v * math.sin(a)) * R
        radial = (u * math.cos(a) + v * math.sin(a))
        for j in range(seg2):
            b = 2 * math.pi * j / seg2
            verts.append(tuple(ring_c + radial * (r * math.cos(b)) + d * (r * math.sin(b))))
    for i in range(seg):
        i2 = (i + 1) % seg
        for j in range(seg2):
            j2 = (j + 1) % seg2
            faces.append([i * seg2 + j, i2 * seg2 + j, i2 * seg2 + j2, i * seg2 + j2])
    return mesh_obj(name, verts, faces, coll)


def helix(name, z0, z1, rm, rw, turns, coll=None, flat_ends=True):
    """coil spring along Z as a swept tube (mesh)."""
    n = int(turns * 64); ring = 16
    pts = []
    for i in range(n + 1):
        t = i / n; a = 2 * math.pi * turns * t
        zt = t
        pts.append(Vector((rm * math.cos(a), rm * math.sin(a), z0 + (z1 - z0) * zt)))
    verts, faces = [], []
    for i, p in enumerate(pts):
        tg = (pts[min(i + 1, n)] - pts[max(i - 1, 0)]).normalized()
        u = Vector((p.x, p.y, 0)).normalized(); v = tg.cross(u).normalized(); u = v.cross(tg).normalized()
        for j in range(ring):
            b = 2 * math.pi * j / ring
            verts.append(tuple(p + (u * math.cos(b) + v * math.sin(b)) * rw))
    for i in range(n):
        for j in range(ring):
            j2 = (j + 1) % ring
            faces.append([i * ring + j, (i + 1) * ring + j, (i + 1) * ring + j2, i * ring + j2])
    faces.append(list(range(ring))[::-1]); faces.append([n * ring + j for j in range(ring)])
    return mesh_obj(name, verts, faces, coll)


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


def dup(ob, name):
    o2 = ob.copy(); o2.data = ob.data.copy(); o2.name = name
    bpy.context.scene.collection.objects.link(o2)
    return o2


def smooth(ob, ang=32):
    me = ob.data
    for p in me.polygons: p.use_smooth = True
    try:
        me.set_sharp_from_angle(angle=math.radians(ang))
    except Exception:
        pass


# --------------------------------------------------------------------------- materials
def _p(nt, typ, **kw):
    n = nt.nodes.new(typ)
    for k, v in kw.items(): setattr(n, k, v)
    return n


def mat_metal(name, col, rough, metal=1.0, aniso=0.0, coat=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; m.use_fake_user = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*col, 1); b.inputs['Metallic'].default_value = metal
    b.inputs['Roughness'].default_value = rough
    if aniso: b.inputs['Anisotropic'].default_value = aniso
    if coat: b.inputs['Coat Weight'].default_value = coat
    return m


def mat_section(name, col, line, ang=45.0, period=1.6, width=0.16, dots=False):
    """matte cut face with hatching (x/z on the cut plane, mm)."""
    m = bpy.data.materials.new(name); m.use_nodes = True; m.use_fake_user = True
    nt = m.node_tree; b = nt.nodes['Principled BSDF']
    b.inputs['Metallic'].default_value = 0.5; b.inputs['Roughness'].default_value = 0.6
    tc = _p(nt, 'ShaderNodeTexCoord'); sx = _p(nt, 'ShaderNodeSeparateXYZ')
    nt.links.new(tc.outputs['Object'], sx.inputs[0])
    if not dots:
        ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        m1 = _p(nt, 'ShaderNodeMath', operation='MULTIPLY'); m1.inputs[1].default_value = ca / period
        m2 = _p(nt, 'ShaderNodeMath', operation='MULTIPLY'); m2.inputs[1].default_value = sa / period
        nt.links.new(sx.outputs['X'], m1.inputs[0]); nt.links.new(sx.outputs['Z'], m2.inputs[0])
        ad = _p(nt, 'ShaderNodeMath', operation='ADD'); nt.links.new(m1.outputs[0], ad.inputs[0]); nt.links.new(m2.outputs[0], ad.inputs[1])
        fr = _p(nt, 'ShaderNodeMath', operation='FRACT'); nt.links.new(ad.outputs[0], fr.inputs[0])
        lt = _p(nt, 'ShaderNodeMath', operation='LESS_THAN'); lt.inputs[1].default_value = width
        nt.links.new(fr.outputs[0], lt.inputs[0]); fac = lt.outputs[0]
    else:   # wire cross-sections for the coil
        p = period
        fx = _p(nt, 'ShaderNodeMath', operation='MULTIPLY'); fx.inputs[1].default_value = 1 / p
        fz = _p(nt, 'ShaderNodeMath', operation='MULTIPLY'); fz.inputs[1].default_value = 1 / p
        nt.links.new(sx.outputs['X'], fx.inputs[0]); nt.links.new(sx.outputs['Z'], fz.inputs[0])
        def centred(src):
            f = _p(nt, 'ShaderNodeMath', operation='FRACT'); nt.links.new(src, f.inputs[0])
            s = _p(nt, 'ShaderNodeMath', operation='SUBTRACT'); s.inputs[1].default_value = 0.5; nt.links.new(f.outputs[0], s.inputs[0])
            q = _p(nt, 'ShaderNodeMath', operation='MULTIPLY'); nt.links.new(s.outputs[0], q.inputs[0]); nt.links.new(s.outputs[0], q.inputs[1])
            return q.outputs[0]
        a1 = _p(nt, 'ShaderNodeMath', operation='ADD'); nt.links.new(centred(fx.outputs[0]), a1.inputs[0]); nt.links.new(centred(fz.outputs[0]), a1.inputs[1])
        gt = _p(nt, 'ShaderNodeMath', operation='GREATER_THAN'); gt.inputs[1].default_value = 0.16
        nt.links.new(a1.outputs[0], gt.inputs[0]); fac = gt.outputs[0]
    mx = _p(nt, 'ShaderNodeMix', data_type='RGBA')
    mx.inputs[6].default_value = (*col, 1); mx.inputs[7].default_value = (*line, 1)
    nt.links.new(fac, mx.inputs[0]); nt.links.new(mx.outputs[2], b.inputs['Base Color'])
    return m


def mat_plastic(name, col, rough=0.45):
    m = bpy.data.materials.new(name); m.use_nodes = True; m.use_fake_user = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*col, 1); b.inputs['Roughness'].default_value = rough
    b.inputs['Metallic'].default_value = 0.0
    return m


def mat_copper_coil(name):
    m = mat_metal(name, (0.93, 0.52, 0.32), 0.32)
    nt = m.node_tree; b = nt.nodes['Principled BSDF']
    tc = _p(nt, 'ShaderNodeTexCoord'); w = _p(nt, 'ShaderNodeTexWave', wave_type='BANDS', bands_direction='Z')
    w.inputs['Scale'].default_value = 0.0;
    sx = _p(nt, 'ShaderNodeSeparateXYZ'); nt.links.new(tc.outputs['Object'], sx.inputs[0])
    mu = _p(nt, 'ShaderNodeMath', operation='MULTIPLY'); mu.inputs[1].default_value = 2 * math.pi / 0.32
    nt.links.new(sx.outputs['Z'], mu.inputs[0])
    si = _p(nt, 'ShaderNodeMath', operation='SINE'); nt.links.new(mu.outputs[0], si.inputs[0])
    bp = _p(nt, 'ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.35; bp.inputs['Distance'].default_value = 0.05
    nt.links.new(si.outputs[0], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    return m


def mat_fuel(name):
    """graphic liquid: black glossy base + white emission (tinted later in compositing)."""
    m = bpy.data.materials.new(name); m.use_nodes = True; m.use_fake_user = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (0, 0, 0, 1); b.inputs['Roughness'].default_value = 0.18
    b.inputs['Emission Color'].default_value = (1, 1, 1, 1); b.inputs['Emission Strength'].default_value = 0.78
    b.inputs['Coat Weight'].default_value = 0.0
    return m


MATS = {}


def mats():
    if MATS: return MATS
    steel = (0.70, 0.72, 0.75)
    MATS.update(
        body=(mat_metal('steel_body', steel, 0.30), mat_section('sec_body', (0.30, 0.31, 0.33), (0.13, 0.14, 0.16), 45, 2.6)),
        nut=(mat_metal('steel_nut', (0.64, 0.66, 0.70), 0.26), mat_section('sec_nut', (0.27, 0.28, 0.30), (0.12, 0.13, 0.15), -45, 2.0)),
        nozzle=(mat_metal('steel_nozzle', (0.58, 0.60, 0.64), 0.24), mat_section('sec_nozzle', (0.33, 0.34, 0.37), (0.14, 0.15, 0.17), -45, 1.2)),
        valve=(mat_metal('steel_valve', (0.80, 0.81, 0.83), 0.20), mat_section('sec_valve', (0.36, 0.37, 0.40), (0.15, 0.16, 0.18), -45, 0.9)),
        core=(mat_metal('iron_core', (0.40, 0.41, 0.43), 0.42), mat_section('sec_core', (0.23, 0.24, 0.26), (0.10, 0.10, 0.12), 45, 1.4)),
        magnut=(mat_metal('steel_magnut', (0.66, 0.67, 0.70), 0.34), mat_section('sec_magnut', (0.28, 0.29, 0.31), (0.12, 0.13, 0.15), -45, 2.2)),
        coil=(mat_copper_coil('copper_coil'), mat_section('sec_coil', (0.55, 0.28, 0.14), (0.20, 0.09, 0.04), 0, 0.42, dots=True)),
        plastic=(mat_plastic('plastic_black', (0.025, 0.026, 0.03), 0.42), mat_section('sec_plastic', (0.10, 0.10, 0.11), (0.05, 0.05, 0.06), 45, 1.8)),
        washer=(mat_metal('copper_washer', (0.90, 0.48, 0.30), 0.30), mat_section('sec_washer', (0.50, 0.25, 0.13), (0.22, 0.10, 0.05), 45, 0.8)),
        polish=(mat_metal('steel_polished', (0.93, 0.94, 0.96), 0.14), None),
        armature=(mat_metal('iron_armature', (0.58, 0.59, 0.62), 0.30), None),
        spring=(mat_metal('steel_spring', (0.42, 0.44, 0.47), 0.28), None),
        filt=(mat_metal('steel_filter', (0.76, 0.77, 0.80), 0.24), None),
        pin=(mat_metal('tin_pin', (0.85, 0.83, 0.78), 0.25), None),
        wire=(mat_metal('copper_wire', (0.95, 0.55, 0.33), 0.25), mat_section('sec_wire', (0.62, 0.32, 0.16), (0.62, 0.32, 0.16), 0, 5.0)),
        fuel=(mat_fuel('fuel_white'), None),
        head=(mat_metal('alu_head', (0.42, 0.43, 0.44), 0.62), mat_section('sec_head', (0.34, 0.35, 0.36), (0.15, 0.16, 0.17), 45, 3.2)),
        clamp=(mat_metal('steel_clamp', (0.36, 0.37, 0.40), 0.36), mat_section('sec_clamp', (0.22, 0.23, 0.25), (0.10, 0.10, 0.12), -45, 1.6)),
        glow=(mat_metal('steel_glow', (0.55, 0.56, 0.60), 0.30), mat_section('sec_glow', (0.30, 0.31, 0.33), (0.13, 0.14, 0.15), -45, 1.0)),
    )
    return MATS


def set_mats(ob, key, cut_side=-1):
    """slot 0 = surface, slot 1 = section; faces on the cut plane facing the camera side get slot 1."""
    surf, sec = mats()[key]
    ob.data.materials.clear(); ob.data.materials.append(surf)
    if sec is not None:
        ob.data.materials.append(sec)
        for p in ob.data.polygons:
            if abs(p.center.y) < 2e-3 and p.normal.y * cut_side > 0.98:
                p.material_index = 1
    smooth(ob)


# --------------------------------------------------------------------------- geometry (full solids)
HP_X = 5.6           # x of the vertical high-pressure bores
LP_X = -5.6          # x of the leak-off bore
Z_IN = 96.0          # height of the high-pressure inlet
Z_THR = 115.2        # height of the inlet throttle


def build_parts():
    P = {}   # name -> (object, material key, group)  group: static / g1 / g2 / sprN / sprA
    # ---- nozzle body
    noz = [(0.0, 0.0), (0.9, 0.12), (1.65, 0.55), (2.35, 1.35), (2.95, 2.55), (3.35, 4.0), (3.5, 5.6), (3.5, 26.2), (3.65, 27.0),
           (6.6, 27.0), (7.0, 27.4), (7.0, 43.6), (6.7, 44.0),
           (2.0, 44.0), (2.0, 30.2), (3.1, 29.8), (3.1, 27.6), (1.8, 27.0), (1.8, 2.6), (0.45, 1.15), (0.45, 0.6), (0.0, 0.35)]
    nb = revolve('nozzle_body', noz)
    cut = [cyl('feed', (HP_X, 0, 44.6), (3.1, 0, 29.2), 0.8)]
    for k in range(8):                                  # 8 spray holes, 150 deg cone
        a = 2 * math.pi * k / 8
        d = Vector((math.sin(math.radians(75)) * math.cos(a), math.sin(math.radians(75)) * math.sin(a), -math.cos(math.radians(75))))
        p0 = Vector((0.15 * math.cos(a), 0.15 * math.sin(a), 0.95))
        cut.append(cyl(f'hole{k}', p0, p0 + d * 2.2, 0.17, segs=24))
    bool_many(nb, cut)
    P['nozzle_body'] = (nb, 'nozzle', 'static')
    # ---- nozzle nut + sealing washer
    nn = revolve('nozzle_nut', [(3.7, 24.0), (8.2, 24.0), (8.75, 24.5), (8.75, 61.5), (8.4, 62.0), (7.05, 62.0), (7.05, 27.0), (3.7, 27.0)])
    P['nozzle_nut'] = (nn, 'nut', 'static')
    P['washer'] = (revolve('washer', [(3.6, 22.2), (6.4, 22.2), (6.4, 24.0), (3.6, 24.0)]), 'washer', 'static')
    # ---- injector body (holder)
    bd = revolve('body', [(4.25, 44.0), (7.0, 44.0), (7.0, 62.0), (8.5, 62.6), (8.5, 112.0), (8.0, 112.5), (8.0, 121.5),
                          (7.2, 121.5), (7.2, 119.5), (4.0, 119.5), (4.0, 108.0), (2.35, 108.0), (2.35, 62.0), (4.25, 62.0)])
    boss = cyl('boss', (6.0, 0, Z_IN), (21.0, 0, Z_IN), 6.2, segs=96)
    apply_bool(bd, boss, 'UNION'); bpy.data.objects.remove(boss, do_unlink=True)
    cham = cyl('cham', (20.2, 0, Z_IN), (21.3, 0, Z_IN), 6.25, r1=5.2, segs=96)   # outer chamfer of the inlet
    cuts = [cham,
            cyl('in_bore', (21.5, 0, Z_IN), (9.0, 0, Z_IN), 2.0, segs=48),
            cyl('in_cone', (21.3, 0, Z_IN), (19.9, 0, Z_IN), 3.4, r1=2.0, segs=48),
            cyl('in_link', (9.2, 0, Z_IN), (HP_X - 0.3, 0, Z_IN), 1.0, segs=32),
            cyl('hp_down', (HP_X, 0, 43.5), (HP_X, 0, Z_IN + 0.8), 0.8, segs=32),
            cyl('hp_up', (HP_X, 0, Z_IN - 0.5), (HP_X, 0, Z_THR + 0.45), 0.7, segs=32),
            cyl('hp_thr', (HP_X + 0.4, 0, Z_THR), (3.85, 0, Z_THR), 0.45, segs=32),
            cyl('lp_up', (LP_X, 0, 59.4), (LP_X, 0, 119.9), 0.6, segs=32),
            cyl('lp_link', (-4.0, 0, 60.0), (LP_X - 0.5, 0, 60.0), 0.5, segs=32)]
    for k in range(6):   # thread grooves on the inlet boss
        cuts.append(torus(f'thr{k}', (13.6 + k * 1.15, 0, Z_IN), (1, 0, 0), 6.23, 0.32, seg=90, seg2=12))
    bool_many(bd, cuts)
    P['body'] = (bd, 'body', 'static')
    # ---- edge filter (rod filter) in the inlet
    ef = cyl('edge_filter', (10.6, 0, Z_IN), (20.4, 0, Z_IN), 1.55, segs=64)
    fl = []
    for k in range(4):
        a = math.pi / 4 + k * math.pi / 2
        ux, uz = math.cos(a), math.sin(a)
        fl.append(box(f'flat{k}', 11.4, 19.6, -0.35, 0.35, -0.35, 0.35))
        fl[-1].matrix_world = Matrix.Translation((0, 0, Z_IN)) @ Matrix.Rotation(a, 4, 'X') @ Matrix.Translation((0, 0, 1.55))
    bool_many(ef, fl)
    P['edge_filter'] = (ef, 'filt', 'static_full')
    # ---- valve piece (control chamber, inlet/outlet throttles, ball seat)
    vp = revolve('valve_piece', [(2.15, 108.0), (3.98, 108.0), (3.98, 114.2), (3.2, 114.4), (3.2, 116.0), (3.98, 116.2), (3.98, 119.5),
                                 (0.85, 119.5), (0.3, 119.0), (0.3, 116.5), (2.15, 116.5)])
    bool_many(vp, [cyl('thr_in', (3.4, 0, Z_THR), (2.0, 0, Z_THR), 0.25, segs=24)])
    P['valve_piece'] = (vp, 'valve', 'static')
    # ---- magnet nut (hex)
    mn = revolve('magnet_nut', [(8.05, 112.0), (11.5, 112.0), (12.4, 112.9), (12.4, 136.6), (11.5, 138.0), (4.5, 138.0), (4.5, 136.0),
                                (7.6, 136.0), (7.6, 124.4), (7.2, 124.4), (7.2, 121.5), (8.05, 121.5)])
    hx = prism('hex', 6, 11.0, 100, 150, rot=math.pi / 6)
    apply_bool(mn, hx, 'INTERSECT'); bpy.data.objects.remove(hx, do_unlink=True)
    bool_many(mn, [cyl('wire_hole', (-5.0, 0, 134.0), (-5.0, 0, 139.0), 0.5, segs=16)])
    P['magnet_nut'] = (mn, 'magnut', 'static')
    # ---- magnet core + coil
    co = revolve('core', [(2.0, 124.4), (3.4, 124.4), (3.4, 134.6), (6.0, 134.6), (6.0, 124.4), (7.6, 124.4), (7.6, 136.0), (2.0, 136.0)])
    bool_many(co, [cyl('wh1', (-5.0, 0, 134.0), (-5.0, 0, 136.5), 0.5, segs=16)])
    P['core'] = (co, 'core', 'static')
    P['coil'] = (revolve('coil', [(3.55, 124.6), (5.85, 124.6), (5.85, 134.4), (3.55, 134.4)]), 'coil', 'coil')
    # ---- top cap with electrical connector (plastic) and return nipple
    cap = revolve('cap', [(2.0, 138.0), (11.0, 138.0), (11.0, 146.5), (10.0, 148.0), (4.2, 148.0), (4.2, 157.0), (3.6, 157.6), (1.6, 157.6), (1.6, 148.0), (2.0, 148.0)])
    plug = box('plug', -25.0, -6.0, -6.5, 6.5, 139.0, 149.5)
    apply_bool(cap, plug, 'UNION'); bpy.data.objects.remove(plug, do_unlink=True)
    bool_many(cap, [box('socket', -26.0, -13.0, -4.6, 4.6, 141.0, 147.6),
                    torus('oring_g', (0, 0, 152.5), (0, 0, 1), 4.23, 0.55, seg=90, seg2=12)])
    P['cap'] = (cap, 'plastic', 'static')
    P['oring'] = (torus('oring', (0, 0, 152.5), (0, 0, 1), 4.25, 0.5, seg=96, seg2=16), 'plastic', 'static_full')
    P['pin_a'] = (box('pin_a', -22.5, -12.0, 1.6, 2.4, 143.9, 144.7), 'pin', 'static_full')
    lead = cyl('lead1', (-5.0, 0, 134.3), (-5.0, 0, 144.3), 0.34, segs=16)
    apply_bool(lead, cyl('lead2', (-5.0, 0, 144.3), (-12.4, 0, 144.3), 0.34, segs=16), 'UNION')
    bpy.data.objects.remove(bpy.data.objects['lead2'], do_unlink=True)
    P['lead'] = (lead, 'wire', 'static')
    # ---- moving group 2: needle, pressure pin with spring seat, valve-control plunger
    P['needle'] = (revolve('needle', [(0.0, 1.30), (0.55, 1.42), (1.01, 1.75), (1.4, 2.3), (1.4, 27.2), (1.98, 28.6), (1.98, 44.3), (1.7, 44.5), (0.0, 44.5)]), 'polish', 'g2')
    P['pressure_pin'] = (revolve('pressure_pin', [(0.0, 44.5), (3.4, 44.5), (3.6, 44.7), (3.6, 46.0), (1.5, 46.0), (1.5, 48.5), (0.0, 48.5)]), 'polish', 'g2')
    P['plunger'] = (revolve('plunger', [(0.0, 48.5), (2.1, 48.5), (2.14, 48.8), (2.14, 52.0), (1.9, 52.4), (1.9, 105.6), (2.14, 106.0), (2.14, 112.8), (2.0, 113.0), (0.0, 113.0)]), 'polish', 'g2')
    P['nozzle_spring'] = (helix('nozzle_spring', 46.3, 61.7, 3.15, 0.62, 6.5), 'spring', 'spr_noz')
    # ---- moving group 1: armature (plate + bolt), ball guide, ball
    P['armature'] = (revolve('armature', [(0.0, 120.85), (1.25, 120.85), (1.25, 122.1), (6.8, 122.1), (7.0, 122.3), (7.0, 123.4), (6.8, 123.6),
                                          (1.25, 123.6), (1.25, 131.0), (0.0, 131.0)]), 'armature', 'g1')
    P['ball_guide'] = (revolve('ball_guide', [(0.0, 120.45), (0.9, 120.45), (0.9, 120.85), (0.0, 120.85)]), 'polish', 'g1')
    bs = bpy.data.meshes.new('ball'); bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=64, v_segments=32, radius=0.75)
    bm.to_mesh(bs); bm.free(); ball = bpy.data.objects.new('ball', bs); bpy.context.scene.collection.objects.link(ball)
    ball.location = (0, 0, 119.74)
    P['ball'] = (ball, 'polish', 'g1')
    P['arm_spring'] = (helix('arm_spring', 131.2, 135.8, 1.45, 0.28, 5.0), 'spring', 'spr_arm')
    return P


def build_fuel():
    """cavity volumes (full), grouped by pressure region."""
    F = {'hp': [], 'ctrl': [], 'lp': [], 'sac': []}
    F['hp'] += [cyl('f_in', (21.3, 0, Z_IN), (9.0, 0, Z_IN), 1.98, segs=48), cyl('f_in_cone', (21.3, 0, Z_IN), (19.9, 0, Z_IN), 3.35, r1=1.98, segs=48),
                cyl('f_link', (9.2, 0, Z_IN), (HP_X, 0, Z_IN), 0.98, segs=32),
                cyl('f_down', (HP_X, 0, 44.0), (HP_X, 0, Z_IN + 0.78), 0.78, segs=32), cyl('f_up', (HP_X, 0, Z_IN), (HP_X, 0, Z_THR + 0.43), 0.68, segs=32),
                cyl('f_thr', (HP_X, 0, Z_THR), (3.9, 0, Z_THR), 0.43, segs=24),
                revolve('f_groove', [(3.22, 114.42), (3.97, 114.25), (3.97, 116.15), (3.22, 116.0)]),
                cyl('f_ithr', (3.25, 0, Z_THR), (2.1, 0, Z_THR), 0.24, segs=24),
                cyl('f_feed', (HP_X, 0, 44.1), (3.1, 0, 29.2), 0.78),
                revolve('f_pch', [(0.0, 27.62), (3.08, 27.62), (3.08, 29.78), (1.98, 30.18), (0.0, 30.18)]),
                revolve('f_ann', [(0.0, 1.76), (1.0, 1.76), (1.78, 2.6), (1.78, 27.0), (3.0, 27.62), (0.0, 27.62)])]
    F['ctrl'] += [revolve('f_cc', [(0.0, 113.0), (2.14, 113.0), (2.14, 116.5), (0.0, 116.5)]),
                  revolve('f_oth', [(0.0, 116.5), (0.29, 116.5), (0.29, 119.0), (0.84, 119.48), (0.0, 119.48)])]
    F['lp'] += [revolve('f_arm', [(0.0, 119.5), (3.98, 119.5), (3.98, 119.52), (7.19, 119.52), (7.19, 124.39), (2.0, 124.39), (2.0, 136.0),
                                  (4.49, 136.0), (4.49, 138.0), (1.99, 138.0), (1.99, 148.0), (1.59, 148.0), (1.59, 157.5), (0.0, 157.5)]),
                cyl('f_lp_up', (LP_X, 0, 59.5), (LP_X, 0, 119.6), 0.58, segs=32), cyl('f_lp_link', (-4.1, 0, 60.0), (LP_X, 0, 60.0), 0.48, segs=24),
                revolve('f_spring', [(0.0, 44.02), (4.24, 44.02), (4.24, 62.0), (2.34, 62.0), (2.34, 108.0), (0.0, 108.0)])]
    F['sac'] += [revolve('f_sac', [(0.0, 0.36), (0.44, 0.6), (0.44, 1.15), (1.0, 1.75), (0.0, 1.75)])]
    for k in range(8):
        a = 2 * math.pi * k / 8
        d = Vector((math.sin(math.radians(75)) * math.cos(a), math.sin(math.radians(75)) * math.sin(a), -math.cos(math.radians(75))))
        p0 = Vector((0.15 * math.cos(a), 0.15 * math.sin(a), 0.95))
        F['sac'].append(cyl(f'f_hole{k}', p0, p0 + d * 1.75, 0.165, segs=24))
    return F


def build_head():
    """cylinder head section around the injector: stepped bore (seat for the sealing washer at z=22.2), nozzle hole,
    coolant jackets, inclined glow plug, clamp (claw) on the nozzle-nut shoulder with its bolt. Clearances exaggerated."""
    H = {}
    hb = box('head_block', -48, 48, -30, 30, 3.5, 58.0)
    u = Vector((-math.sin(math.radians(18)), 0, math.cos(math.radians(18)))); A = Vector((-15.0, 0, 1.5))
    cuts = [revolve('h_bore', [(0.0, 22.2), (10.5, 22.2), (10.5, 70.0), (0.0, 70.0)]),
            revolve('h_noz', [(0.0, -2.0), (4.3, -2.0), (4.3, 22.3), (0.0, 22.3)]),
            cyl('h_glow', tuple(A - u * 3), tuple(A + u * 70), 2.7),
            cyl('h_bolt', (24.0, 0, 33.5), (24.0, 0, 60.0), 3.05),
            box('h_jacket1', -46, -36, -20, 20, 12, 44), box('h_jacket2', 34, 46, -20, 20, 16, 46),
            box('h_jacket3', -31, -24, -20, 20, 40, 50)]
    bool_many(hb, cuts)
    H['head_block'] = (hb, 'head', 'head')
    gp = cyl('glow_plug', tuple(A), tuple(A + u * 6), 1.1)
    for nm, a0, a1, r in (('gp_body', 6, 58, 2.45), ('gp_hex', 58, 63, 4.0)):
        o = cyl(nm, tuple(A + u * a0), tuple(A + u * a1), r)
        apply_bool(gp, o, 'UNION'); bpy.data.objects.remove(o, do_unlink=True)
    H['glow_plug'] = (gp, 'glow', 'head')
    cl_ = box('clamp', -14.0, 30.0, -7.0, 7.0, 62.0, 68.0)
    bool_many(cl_, [cyl('clamp_hole', (0, 0, 60), (0, 0, 70), 8.55, segs=96), cyl('clamp_slot', (24.0, 0, 60), (24.0, 0, 70), 3.1)])
    H['clamp'] = (cl_, 'clamp', 'clamp')
    bolt = revolve('clamp_bolt', [(0.0, 34.0), (2.9, 34.0), (3.0, 34.3), (3.0, 68.0), (4.8, 68.0), (4.8, 72.6), (4.4, 73.0), (0.0, 73.0)], segs=64)
    bolt.location = (24.0, 0, 0)
    H['clamp_bolt'] = (bolt, 'clamp', 'clamp')
    return H


def cut_half(ob, keep='back', eps=0.0):
    """keep='back' -> y >= -eps ; keep='front' -> y <= 0"""
    if keep == 'back':
        c = box('cutter', -100, 100, -100, -eps, -50, 220)
    else:
        c = box('cutter', -100, 100, 0.0, 100, -50, 220)
    apply_bool(ob, c); bpy.data.objects.remove(c, do_unlink=True)


# --------------------------------------------------------------------------- scene
def new_coll(name):
    c = bpy.data.collections.new(name); bpy.context.scene.collection.children.link(c); return c


def move_to(ob, coll):
    for c in list(ob.users_collection): c.objects.unlink(ob)
    coll.objects.link(ob)


def world_and_lights():
    """studio environment: dark floor-to-sky gradient + tall soft boxes placed by azimuth around the camera,
    so polished cylinders show long bright bands instead of reflecting black."""
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
    cam_back = math.atan2(-math.cos(math.radians(YAW)), -math.sin(math.radians(YAW)))   # azimuth behind the camera
    def box_light(center, half, e0, e1, gain):
        d = _p(nt, 'ShaderNodeMath', operation='SUBTRACT'); nt.links.new(az.outputs[0], d.inputs[0]); d.inputs[1].default_value = center
        wr = _p(nt, 'ShaderNodeMath', operation='WRAP'); nt.links.new(d.outputs[0], wr.inputs[0]); wr.inputs[1].default_value = math.pi; wr.inputs[2].default_value = -math.pi
        ab = _p(nt, 'ShaderNodeMath', operation='ABSOLUTE'); nt.links.new(wr.outputs[0], ab.inputs[0])
        h = mr(ab.outputs[0], half, half * 0.55, 0.0, 1.0)            # soft edges
        v = mul(mr(el, e0, e0 + 0.08), mr(el, e1, e1 - 0.08))
        return mul(mul(h, v), gain)
    L = box_light(cam_back, math.radians(13), -0.35, 0.70, 3.0)
    L = add(L, box_light(cam_back + math.radians(68), math.radians(9), -0.25, 0.75, 2.2))
    L = add(L, box_light(cam_back - math.radians(72), math.radians(8), -0.25, 0.75, 1.8))
    L = add(L, box_light(cam_back + math.radians(180), math.radians(25), -0.10, 0.60, 0.9))
    L = add(L, mul(mr(el, 0.80, 0.95), 1.6))                                # overhead panel
    base = mr(el, -0.6, 0.9, 0.02, 0.20)
    tot = add(L, base)
    nt.links.new(tot, bg.inputs['Color']); bg.inputs['Strength'].default_value = 1.0
    for name, rot, en, ang in (('key', (math.radians(50), 0, math.radians(-30)), 2.6, 10),
                               ('rim', (math.radians(68), 0, math.radians(150)), 2.0, 6),
                               ('fill', (math.radians(78), 0, math.radians(35)), 0.6, 30)):
        ld = bpy.data.lights.new(name, 'SUN'); ld.energy = en; ld.angle = math.radians(ang)
        lo = bpy.data.objects.new(name, ld); lo.rotation_euler = rot; sc.collection.objects.link(lo)


CAMS = {
    # name: (target region z0, z1, x centre, screen top px, screen bottom px)
    'full': dict(z0=-24.0, z1=158.0, xc=0.0, top=150, bot=1330),
    'valve': dict(z0=104.0, z1=141.0, xc=0.0, top=210, bot=1300),
    'nozzle': dict(z0=-11.0, z1=32.0, xc=0.0, top=210, bot=1300),
    'head': dict(z0=-12.0, z1=66.0, xc=0.0, top=210, bot=1300),
    'guide': dict(z0=14.0, z1=60.0, xc=0.0, top=210, bot=1300),
}
YAW, PITCH, DIST = 24.0, 9.0, 620.0


def cam_basis():
    yaw, pit = math.radians(YAW), math.radians(PITCH)
    d = Vector((math.sin(yaw) * math.cos(pit), math.cos(yaw) * math.cos(pit), -math.sin(pit)))   # view direction
    return d


def make_camera(name):
    sc = bpy.context.scene
    cd = bpy.data.cameras.new(name); cd.sensor_fit = 'VERTICAL'; cd.sensor_height = 24.0; cd.sensor_width = 24.0 * 1080 / 1920
    co = bpy.data.objects.new(name, cd); sc.collection.objects.link(co)
    d = cam_basis(); tgt = Vector((0, 0, 67.0))
    co.location = tgt - d * DIST
    co.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    return co


def fit_camera(co, spec):
    """lens + shift so that the axis range [z0, z1] spans screen rows top..bot and its middle sits at x = 540."""
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene; cd = co.data
    A = Vector((spec['xc'], 0, spec['z1'])); B = Vector((spec['xc'], 0, spec['z0'])); M = (A + B) / 2
    def meas():
        bpy.context.view_layer.update()
        a = world_to_camera_view(sc, co, A); b = world_to_camera_view(sc, co, B); m = world_to_camera_view(sc, co, M)
        return (1 - a.y) * 1920, (1 - b.y) * 1920, m.x * 1080
    cd.lens = 60.0; cd.shift_x = 0.0; cd.shift_y = 0.0
    for _ in range(12):
        ya, yb, xm = meas()
        cd.lens *= (spec['bot'] - spec['top']) / (yb - ya)
        for attr, idx, goal in (('shift_y', 0, spec['top']), ('shift_x', 2, 540.0)):
            v0 = meas()[idx]; setattr(cd, attr, getattr(cd, attr) + 0.01); v1 = meas()[idx]; setattr(cd, attr, getattr(cd, attr) - 0.01)
            setattr(cd, attr, getattr(cd, attr) + (goal - v0) / ((v1 - v0) / 0.01))
    print(co.name, 'lens %.1f shift %.3f %.3f' % (cd.lens, cd.shift_x, cd.shift_y), [round(v, 1) for v in meas()])
    return co


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.unit_settings.system = 'NONE'
    P = build_parts(); F = build_fuel(); P.update(build_head())
    C = {k: new_coll(k) for k in ('static', 'coil', 'static_full', 'g1', 'g2', 'spr_noz', 'spr_arm', 'front', 'fuel_hp', 'fuel_ctrl', 'fuel_lp', 'fuel_sac', 'head', 'clamp')}
    for name, (ob, mk, grp) in P.items():
        if grp in ('static', 'coil'):
            fr = dup(ob, name + '_front'); cut_half(fr, 'front'); set_mats(fr, mk, cut_side=+1); move_to(fr, C['front'])
            cut_half(ob, 'back'); set_mats(ob, mk, cut_side=-1)
        elif grp in ('head', 'clamp'):
            cut_half(ob, 'back'); set_mats(ob, mk, cut_side=-1)
        else:
            set_mats(ob, mk)
        move_to(ob, C[grp])
    for reg, obs in F.items():
        for ob in obs:
            cut_half(ob, 'back', eps=0.03)
            ob.data.materials.clear(); ob.data.materials.append(mats()['fuel'][0])
            for p in ob.data.polygons: p.use_smooth = True
            move_to(ob, C['fuel_' + reg])
    world_and_lights()
    sc.render.resolution_x = 1080; sc.render.resolution_y = 1920
    for cname, spec in CAMS.items():
        fit_camera(make_camera('cam_' + cname), spec)
    r = sc.render; r.engine = 'CYCLES'; r.resolution_x = 1080; r.resolution_y = 1920; r.resolution_percentage = 100
    r.film_transparent = True
    cy = sc.cycles; cy.device = 'CPU'; cy.samples = 64; cy.use_adaptive_sampling = True; cy.adaptive_threshold = 0.02
    cy.use_denoising = True; cy.denoiser = 'OPENIMAGEDENOISE'
    cy.max_bounces = 8; cy.glossy_bounces = 4; cy.diffuse_bounces = 2; cy.transmission_bounces = 2; cy.transparent_max_bounces = 4
    cy.caustics_reflective = False; cy.caustics_refractive = False
    sc.view_settings.view_transform = 'AgX'
    try:
        sc.view_settings.look = 'AgX - Medium High Contrast'
    except Exception:
        try: sc.view_settings.look = 'Medium High Contrast'
        except Exception: pass
    r.image_settings.file_format = 'PNG'; r.image_settings.color_mode = 'RGBA'; r.image_settings.color_depth = '16'
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, 'cri2.blend'))
    print('saved', len(bpy.data.objects), 'objects')


# --------------------------------------------------------------------------- render layers
LAYERS = {
    # layer: (visible collections, holdout collections, view transform)
    'plate':   (['static', 'coil', 'static_full'], [], 'AgX'),
    'coil':    (['coil'], ['static', 'static_full'], 'Standard'),
    'g1':      (['g1'], ['static', 'coil', 'static_full'], 'AgX'),
    'g2':      (['g2'], ['static', 'coil', 'static_full'], 'AgX'),
    'spr_noz': (['spr_noz'], ['static', 'coil', 'static_full'], 'AgX'),
    'spr_arm': (['spr_arm'], ['static', 'coil', 'static_full'], 'AgX'),
    'fuel_hp': (['fuel_hp'], ['static', 'coil', 'static_full'], 'Standard'),
    'fuel_ctrl': (['fuel_ctrl'], ['static', 'coil', 'static_full'], 'Standard'),
    'fuel_lp': (['fuel_lp'], ['static', 'coil', 'static_full'], 'Standard'),
    'fuel_sac': (['fuel_sac'], ['static', 'coil', 'static_full'], 'Standard'),
    'front':   (['front'], [], 'AgX'),
    'all':     (['static', 'coil', 'static_full', 'g1', 'g2', 'spr_noz', 'spr_arm'], [], 'AgX'),
    'ext':     (['static', 'coil', 'front', 'static_full', 'g1', 'g2', 'spr_noz', 'spr_arm'], [], 'AgX'),
    'headblk': (['head'], [], 'AgX'),
    'clamp':   (['clamp'], [], 'AgX'),
}


def render(cam, layer, pct=100, samples=None, out=None):
    bpy.ops.wm.open_mainfile(filepath=os.path.join(OUT, 'cri2.blend'))
    sc = bpy.context.scene; sc.camera = bpy.data.objects['cam_' + cam]
    vis, hold, vt = LAYERS[layer]
    for c in bpy.data.collections:
        on = c.name in vis or c.name in hold
        c.hide_render = not on
        for ob in c.objects:
            ob.is_holdout = c.name in hold
    sc.view_settings.view_transform = vt
    if vt == 'Standard':
        sc.view_settings.look = 'None'
    if layer == 'coil':
        bpy.context.view_layer.material_override = bpy.data.materials['fuel_white']
    sc.render.resolution_percentage = pct
    if samples: sc.cycles.samples = samples
    elif layer.startswith('fuel'): sc.cycles.samples = 24
    elif layer in ('g1', 'g2', 'spr_noz', 'spr_arm'): sc.cycles.samples = 48
    sc.render.filepath = out or os.path.join(OUT, f'{cam}_{layer}.png')
    bpy.ops.render.render(write_still=True)


# --------------------------------------------------------------------------- projections for the compositor
ANCH = {
    'inlet': (21.0, 0, Z_IN + 6.2), 'filter': (15.5, 0, Z_IN), 'hp_bore': (HP_X, 0, 75.0), 'coil': (-5.85, 0, 129.5),
    'armature': (-7.0, 0, 122.9), 'ball': (0.0, 0, 119.74), 'outlet_thr': (0.0, 0, 117.8), 'ctrl_ch': (0.0, 0, 114.7),
    'inlet_thr': (2.7, 0, Z_THR), 'valve_piece': (-3.98, 0, 110.0), 'plunger': (-1.9, 0, 85.0), 'spring': (-3.8, 0, 54.0),
    'needle': (-1.98, 0, 36.0), 'needle_tip': (0.0, 0, 1.6), 'pressure_ch': (-3.1, 0, 28.7), 'nozzle': (-3.5, 0, 12.0),
    'nut': (-8.75, 0, 45.0), 'washer': (-6.4, 0, 23.1), 'return': (0.0, 0, 157.6), 'connector': (-25.0, 0, 147.0),
    'leak': (LP_X, 0, 90.0), 'core': (-7.6, 0, 132.5), 'magnet_nut': (-11.0, 0, 125.0), 'armature_ch': (6.6, 0, 121.0),
    'seat': (1.01, 0, 1.75), 'sac': (0.0, 0, 0.9), 'body': (-8.5, 0, 100.0), 'tip': (0.0, 0, 0.0),
    'g1_ref': (0.0, 0, 120.0), 'g2_ref': (0.0, 0, 60.0), 'spr_noz_top': (0.0, 0, 61.7), 'spr_noz_bot': (0.0, 0, 46.3),
    'spr_arm_top': (0.0, 0, 135.8), 'spr_arm_bot': (0.0, 0, 131.2),
    'plunger_top': (0.0, 0, 113.0), 'shoulder_l': (-1.7, 0, 27.9), 'shoulder_r': (1.7, 0, 27.9), 'gap_arm': (0.0, 0, 124.0),
    'coilL0': (-5.85, 0, 124.6), 'coilL1': (-3.55, 0, 124.6), 'coilL2': (-3.55, 0, 134.4), 'coilL3': (-5.85, 0, 134.4),
    'coilR0': (3.55, 0, 124.6), 'coilR1': (5.85, 0, 124.6), 'coilR2': (5.85, 0, 134.4), 'coilR3': (3.55, 0, 134.4),
    'cc_right': (2.15, 0, 114.7), 'oth_top': (0.0, 0, 119.0), 'spring_mid': (3.15, 0, 54.0),
}


def holes_dirs():
    out = []
    for k in range(8):
        a = 2 * math.pi * k / 8
        d = (math.sin(math.radians(75)) * math.cos(a), math.sin(math.radians(75)) * math.sin(a), -math.cos(math.radians(75)))
        p0 = (0.15 * math.cos(a) + d[0] * 1.75, 0.15 * math.sin(a) + d[1] * 1.75, 0.95 + d[2] * 1.75)
        out.append((p0, d))
    return out


PATHS = {
    'hp_main': [(21.0, 0, Z_IN), (HP_X, 0, Z_IN), (HP_X, 0, 44.1), (3.1, 0, 29.2), (2.4, 0, 28.6), (1.6, 0, 26.0), (1.6, 2.0, 2.4), (1.1, 0, 1.9)],
    'hp_ctrl': [(HP_X, 0, Z_IN), (HP_X, 0, Z_THR), (3.6, 0, Z_THR), (2.15, 0, Z_THR), (0.9, 0, 115.0)],
    'ctrl_out': [(0.0, 0, 113.6), (0.0, 0, 116.5), (0.0, 0, 119.3), (0.9, 0, 119.9), (2.6, 0, 120.4), (4.6, 0, 121.0), (7.05, 0, 121.6), (7.05, 0, 123.9), (3.0, 0, 124.1),
                 (1.6, 0, 124.4), (1.6, 0, 135.5), (1.2, 0, 140.0), (0.0, 0, 147.0), (0.0, 0, 157.6)],
    'leak': [(-3.8, 0, 58.0), (-4.2, 0, 60.0), (LP_X, 0, 60.0), (LP_X, 0, 119.4), (LP_X, 0, 121.0), (-7.05, 0, 121.6), (-7.05, 0, 123.9), (-3.0, 0, 124.1), (-1.6, 0, 124.4)],
    'fluxL': [(-2.7, 0, 124.2), (-2.7, 0, 130.0), (-2.9, 0, 135.2), (-4.7, 0, 135.4), (-6.5, 0, 135.2), (-6.8, 0, 130.0), (-6.8, 0, 124.2),
              (-6.4, 0, 122.85), (-4.5, 0, 122.85), (-2.7, 0, 122.85), (-2.7, 0, 124.2)],
    'fluxR': [(2.7, 0, 124.2), (2.7, 0, 130.0), (2.9, 0, 135.2), (4.7, 0, 135.4), (6.5, 0, 135.2), (6.8, 0, 130.0), (6.8, 0, 124.2),
              (6.4, 0, 122.85), (4.5, 0, 122.85), (2.7, 0, 122.85), (2.7, 0, 124.2)],
}


def info():
    from bpy_extras.object_utils import world_to_camera_view
    bpy.ops.wm.open_mainfile(filepath=os.path.join(OUT, 'cri2.blend'))
    sc = bpy.context.scene; res = {}
    for cname in CAMS:
        co = bpy.data.objects['cam_' + cname]
        def px(p):
            v = world_to_camera_view(sc, co, Vector(p)); return [round(v.x * 1080, 2), round((1 - v.y) * 1920, 2), round(v.z, 3)]
        d = {'anch': {k: px(p) for k, p in ANCH.items()},
             'paths': {k: [px(p) for p in pts] for k, pts in PATHS.items()},
             'holes': [[px(p0), px((p0[0] + dd[0] * 20, p0[1] + dd[1] * 20, p0[2] + dd[2] * 20)), dd] for p0, dd in holes_dirs()],
             'lens': co.data.lens, 'shift': [co.data.shift_x, co.data.shift_y],
             'M': [list(r) for r in co.matrix_world.inverted()], 'sensor_h': co.data.sensor_height}
        # pixel motion per mm of lift for the moving groups
        for g, ref in (('g1', ANCH['g1_ref']), ('g2', ANCH['g2_ref'])):
            a = px(ref); b = px((ref[0], ref[1], ref[2] + 1.0))
            d['dpx_' + g] = [b[0] - a[0], b[1] - a[1]]
        # world points along the axis for mapping between cameras
        d['axis'] = [px((x, 0, z)) for z in (-10, 0, 30, 60, 110, 120, 140) for x in (-8, 8)]
        res[cname] = d
    res['lift'] = {'needle': LIFT_NEEDLE, 'arm': LIFT_ARM}
    json.dump(res, open(os.path.join(OUT, 'info.json'), 'w'), indent=1)
    print('info written')


QUEUE = [('full', 'plate'), ('full', 'fuel_hp'), ('full', 'fuel_ctrl'), ('full', 'fuel_lp'), ('full', 'fuel_sac'),
         ('full', 'g1'), ('full', 'g2'), ('full', 'spr_noz'), ('full', 'spr_arm'), ('full', 'coil'), ('full', 'front'),
         ('valve', 'plate'), ('valve', 'fuel_hp'), ('valve', 'fuel_ctrl'), ('valve', 'fuel_lp'), ('valve', 'g1'), ('valve', 'g2'), ('valve', 'spr_arm'), ('valve', 'coil'),
         ('nozzle', 'plate'), ('nozzle', 'fuel_hp'), ('nozzle', 'fuel_sac'), ('nozzle', 'fuel_lp'), ('nozzle', 'g2'),
         ('full', 'ext'),
         ('head', 'headblk'), ('head', 'clamp'), ('head', 'plate'), ('head', 'fuel_hp'), ('head', 'fuel_lp'), ('head', 'fuel_sac'), ('head', 'g2'),
         ('head', 'spr_noz'), ('full', 'headblk'), ('full', 'clamp'),
         ('guide', 'plate'), ('guide', 'fuel_hp'), ('guide', 'fuel_lp'), ('guide', 'fuel_sac'), ('guide', 'g2'), ('guide', 'spr_noz')]


def queue():
    import time
    for cam, layer in QUEUE:
        f = os.path.join(OUT, f'{cam}_{layer}.png')
        if os.path.exists(f): continue
        t = time.time(); render(cam, layer)
        print(f'DONE {cam}_{layer} {time.time() - t:.0f}s', flush=True)


if __name__ == '__main__':
    a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    if a[0] == 'build': build()
    elif a[0] == 'render':
        render(a[1], a[2], int(a[3]) if len(a) > 3 else 100, int(a[4]) if len(a) > 4 else None, a[5] if len(a) > 5 else None)
    elif a[0] == 'info': info()
    elif a[0] == 'queue': queue()

