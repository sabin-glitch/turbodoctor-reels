# Geometria precalculata (src/geo.bin + geo.json, din animatia „Amorsare filtru”) -> obiecte Blender; fete de sectiune cu hasura.
import os, json, math
import bpy, bmesh, numpy as np
import kit as K, imats
from kit import srgb
HERE = os.path.dirname(os.path.abspath(__file__))
GJ = json.load(open(os.path.join(HERE, 'src', 'geo.json'))); GB = open(os.path.join(HERE, 'src', 'geo.bin'), 'rb').read()
SEC_K, SEC_M, SEC_R, HATCH, SEC_TONE = imats.SEC_K, imats.SEC_M, imats.SEC_R, imats.HATCH, imats.SEC_TONE

def sec3(name, col, period, strength, sign, k=None, plain=False, metal=None, rough=None):
    """fata de sectiune cu hasura in reperul piesei: fract((x + sign*y + z) / perioada); planul cu normala +x e mai inchis"""
    m, N, L, b = imats._new(name)
    base = srgb(imats.dim(col, SEC_K if k is None else k))
    b.inputs['Base Color'].default_value = base; b.inputs['Metallic'].default_value = SEC_M if metal is None else metal
    b.inputs['Roughness'].default_value = SEC_R if rough is None else rough
    tc = N.new('ShaderNodeTexCoord')
    sx = N.new('ShaderNodeSeparateXYZ'); L.new(tc.outputs['Object'], sx.inputs[0])
    a1 = N.new('ShaderNodeMath'); a1.operation = 'MULTIPLY_ADD'; a1.inputs[1].default_value = sign
    L.new(sx.outputs['Y'], a1.inputs[0]); L.new(sx.outputs['X'], a1.inputs[2])
    a2 = N.new('ShaderNodeMath'); a2.operation = 'ADD'; L.new(a1.outputs[0], a2.inputs[0]); L.new(sx.outputs['Z'], a2.inputs[1])
    a3 = N.new('ShaderNodeMath'); a3.operation = 'DIVIDE'; a3.inputs[1].default_value = period; L.new(a2.outputs[0], a3.inputs[0])
    a4 = N.new('ShaderNodeMath'); a4.operation = 'FRACT'; L.new(a3.outputs[0], a4.inputs[0])
    a5 = N.new('ShaderNodeMath'); a5.operation = 'SUBTRACT'; a5.inputs[1].default_value = 0.5; L.new(a4.outputs[0], a5.inputs[0])
    a6 = N.new('ShaderNodeMath'); a6.operation = 'ABSOLUTE'; L.new(a5.outputs[0], a6.inputs[0])
    mrh = N.new('ShaderNodeMapRange'); mrh.interpolation_type = 'SMOOTHSTEP'
    mrh.inputs['From Min'].default_value = 0.22; mrh.inputs['From Max'].default_value = 0.28
    mrh.inputs['To Min'].default_value = 1.0 - (0.0 if plain else strength * HATCH); mrh.inputs['To Max'].default_value = 1.0
    L.new(a6.outputs[0], mrh.inputs['Value'])
    sn = N.new('ShaderNodeSeparateXYZ'); L.new(tc.outputs['Normal'], sn.inputs[0])
    tn = N.new('ShaderNodeMapRange'); tn.inputs['From Min'].default_value = 0.0; tn.inputs['From Max'].default_value = 1.0
    tn.inputs['To Min'].default_value = 1.0; tn.inputs['To Max'].default_value = 1.0 - SEC_TONE
    L.new(sn.outputs['X'], tn.inputs['Value'])
    mt = N.new('ShaderNodeMath'); mt.operation = 'MULTIPLY'; L.new(mrh.outputs['Result'], mt.inputs[0]); L.new(tn.outputs['Result'], mt.inputs[1])
    vs = N.new('ShaderNodeVectorMath'); vs.operation = 'SCALE'; vs.inputs[0].default_value = base[:3]
    L.new(mt.outputs[0], vs.inputs['Scale']); L.new(vs.outputs['Vector'], b.inputs['Base Color'])
    return m

def mk_mesh(name, pos, nrm, idx):
    me = bpy.data.meshes.new(name); nv = len(pos); nl = len(idx); nt = nl // 3
    me.vertices.add(nv); me.vertices.foreach_set('co', pos.astype(np.float32).ravel())
    me.loops.add(nl); me.loops.foreach_set('vertex_index', idx.astype(np.int32))
    me.polygons.add(nt); me.polygons.foreach_set('loop_start', np.arange(0, nl, 3, dtype=np.int32))
    me.update(); me.validate(clean_customdata=False)
    me.polygons.foreach_set('use_smooth', np.ones(nt, dtype=bool))
    if nrm is not None and len(me.vertices) == nv:
        n = nrm / np.maximum(1e-9, np.linalg.norm(nrm, axis=1))[:, None]; me.normals_split_custom_set_from_vertices(n.tolist())
    return me

def part(name, parent, M, over=None, oname=None):
    """piesa `name` din geo.bin ca un gol cu cate un mesh pe material; M = materialele dupa nume"""
    g = K.empty(oname or name, parent)
    for p in GJ:
        if p['n'] != name: continue
        o, v, b = p['o'], p['v'], p['b']
        pq = np.frombuffer(GB, np.uint16, v * 3, o).reshape(-1, 3).astype(np.float64)
        pos = np.array(b[:3]) + pq * np.array(b[3:])
        o2 = o + ((v * 6 + 3) & ~3)
        if p.get('h'): nq = np.frombuffer(GB, np.int16, v * 4, o2).reshape(-1, 4)[:, :3] / 32767.0; o3 = o2 + v * 8
        else: nq = np.frombuffer(GB, np.int8, v * 4, o2).reshape(-1, 4)[:, :3] / 127.0; o3 = o2 + v * 4
        idx = np.frombuffer(GB, np.uint16 if p['w'] == 2 else np.uint32, p['i'], o3)
        me = mk_mesh((oname or name) + '.' + p['m'], pos, nq, idx)
        me.materials.append((over or {}).get(p['m']) or M[p['m']])
        ob = bpy.data.objects.new(me.name, me); K.scn.collection.objects.link(ob); ob.parent = g
    return g

def skin(src_names, name, mat, off=0.05, parent=None):
    """piele subtire peste piese (rugina, lacuri, uzura): copie a mesh-ului, umflata cu off mm; ascunsa implicit"""
    g = K.empty(name, parent)
    for sn in src_names:
        so = bpy.data.objects[sn]; me = so.data.copy(); me.name = name + '.' + sn
        bm = bmesh.new(); bm.from_mesh(me)
        for v in bm.verts: v.co += v.normal * off
        bm.to_mesh(me); bm.free(); me.materials.clear(); me.materials.append(mat)
        ob = bpy.data.objects.new(me.name, me); K.scn.collection.objects.link(ob); ob.parent = g; ob.visible_shadow = False
    g.hide_render = True
    for c in g.children: c.hide_render = True
    return g
