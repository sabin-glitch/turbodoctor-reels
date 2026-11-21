# Pompa Bosch CP4.1 pentru seria „De ce se strica pompele de inalta presiune”: geometria precalculata a animatiei „Amorsare filtru”
# (src/geo.bin + geo.json), cu materialele si culorile seriei injectoarelor (joasa presiune galben, inalta presiune portocaliu-rosu).
#   venv_bpy/bin/python pmodel.py        -> blend/pump.blend  (grupuri: CUT = sectiunea, FULL = pompa intreaga, piese mobile, lichide)
import sys, os, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, '/home/claude/w/inj')
import bpy, bmesh, numpy as np
from mathutils import Vector
import kit as K, imats, irig
import pkin
from kit import srgb

K.init(empty=True)
scn = K.scn; ROOT = K.ROOT
CP4 = K.empty('CP4'); CP4.rotation_euler = (math.pi / 2, 0, 0)

SEC_K, SEC_M, SEC_R, HATCH, SEC_TONE = imats.SEC_K, imats.SEC_M, imats.SEC_R, imats.HATCH, imats.SEC_TONE
def sec3(name, col, period, strength, sign, k=None, plain=False):
    """fata de sectiune cu hasura in reperul pompei: fract((x + sign*y + z) / perioada); planul cu normala +x e mai inchis"""
    m, N, L, b = imats._new(name)
    base = srgb(imats.dim(col, SEC_K if k is None else k))
    b.inputs['Base Color'].default_value = base; b.inputs['Metallic'].default_value = SEC_M; b.inputs['Roughness'].default_value = SEC_R
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

M = {}
M['castAlu'] = imats.metal('castAlu', 0xb9bcc0, 0.55, bump=(1.6, 0.35, 0.25))
M['machAlu'] = imats.metal('machAlu', 0xd8dadd, 0.24, bump=(40, 0.04), aniso=0.3)
M['steelHead'] = imats.metal('steelHead', 0x9a9fa6, 0.38, bump=(6, 0.12, 0.15))
M['steel'] = imats.metal('steel', 0xb7bcc2, 0.30)
M['steelPol'] = imats.metal('steelPol', 0xdfe2e6, 0.13)
M['steelDark'] = imats.metal('steelDark', 0x4a4e55, 0.4)
M['zincW'] = imats.metal('zincW', 0xc9ced6, 0.32, bump=(3, 0.06, 0.12))
M['bronze'] = imats.metal('bronze', 0xc08f4e, 0.3)
M['sealBrown'] = imats.metal('sealBrown', 0x4a2a1a, 0.55, metal=0.0)
M['plasticGrey'] = imats.metal('plasticGrey', 0x3a3d42, 0.5, metal=0.0, coat=0.2)
M['markDark'] = imats.metal('markDark', 0x222428, 0.4, metal=0.6)
M['dlc'] = imats.metal('dlc', 0x2e3035, 0.22, coat=0.5)
M['scored'] = imats.metal('scored', 0x6e5a48, 0.65, bump=(14, 0.9, 0.4))
M['secAlu'] = sec3('secAlu', 0xd9dbde, 2.6, 0.2, 1)
M['secSteel'] = sec3('secSteel', 0x9aa0a8, 2.0, 0.25, -1)
M['secTap'] = sec3('secTap', 0x5d626a, 1.4, 0.3, 1)
M['secBronze'] = sec3('secBronze', 0xc79a58, 1.0, 0.0, 1, plain=True)
M['fuel'] = imats.liquid('fuelLP', imats.C_LP, 0.9)
M['fuelCh'] = imats.liquid('fuelCh', imats.C_LP, 0.92)
M['fuelHP'] = imats.liquid('fuelHP', imats.C_HP, 0.93)
M['rollerPol'] = imats.metal('rollerPol', 0xdfe2e6, 0.13)
_b = M['rollerPol'].node_tree.nodes['Principled BSDF']; _b.inputs['Emission Color'].default_value = srgb(0xff6a10); _b.inputs['Emission Strength'].default_value = 0.0
M['rust'] = imats.damage('rust', 0x5a2a12, 0xc9652a, rough=0.9, scale=0.45, stretch=(1, 1, 1), thr=0.6, soft=0.2, bump=0.9, metal=0.15)
# lacul (motorina imbatranita): pelicula subtire, lucioasa, maro-chihlimbarie, aproape uniforma (nu pete, ca rugina)
M['lac'] = imats.damage('lac', 0x2e1705, 0x6a3a0c, rough=0.2, scale=0.16, stretch=(1, 1, 1), thr=1.0, soft=0.3, bump=0.12, metal=0.3)
_b = M['lac'].node_tree.nodes['Principled BSDF']; _b.inputs['Coat Weight'].default_value = 0.7; _b.inputs['Coat Roughness'].default_value = 0.08
_c = M['lac'].node_tree.nodes['COVER']; _c.inputs['From Min'].default_value = 0.2; _c.inputs['From Max'].default_value = 0.62; _c.inputs['To Min'].default_value = 0.74; _c.inputs['To Max'].default_value = 0.97
# uzura: benzi mate, gri, cu rizuri pe directia de rulare (otel sters, nu ruginit)
M['wear'] = imats.damage('wear', 0x2f3237, 0x8b9097, rough=0.62, scale=0.9, stretch=(1, 0.08, 1), thr=0.6, bump=1.0, metal=0.85)
for m in M.values(): m.use_fake_user = True

GJ = json.load(open(os.path.join(HERE, 'src', 'geo.json'))); GB = open(os.path.join(HERE, 'src', 'geo.bin'), 'rb').read()
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

def part(name, parent=None, over=None, oname=None):
    g = K.empty(oname or name, parent or CP4)
    for p in GJ:
        if p['n'] != name: continue
        o, v = p['o'], p['v']; b = p['b']
        pq = np.frombuffer(GB, np.uint16, v * 3, o).reshape(-1, 3).astype(np.float64)
        pos = np.array(b[:3]) + pq * np.array(b[3:])
        o2 = o + ((v * 6 + 3) & ~3)
        if p.get('h'): nq = np.frombuffer(GB, np.int16, v * 4, o2).reshape(-1, 4)[:, :3] / 32767.0; o3 = o2 + v * 8
        else: nq = np.frombuffer(GB, np.int8, v * 4, o2).reshape(-1, 4)[:, :3] / 127.0; o3 = o2 + v * 4
        idx = np.frombuffer(GB, np.uint16 if p['w'] == 2 else np.uint32, p['i'], o3)
        me = mk_mesh((oname or name) + '.' + p['m'], pos, nq, idx)
        me.materials.append((over or {}).get(p['m']) or M[p['m']])
        ob = bpy.data.objects.new(me.name, me); scn.collection.objects.link(ob); ob.parent = g
    return g

def skin(src_names, name, mat, off=0.05, parent=None):
    """piele subtire peste piese (rugina, lacuri, uzura): copie a mesh-ului, umflata cu off mm, cu material cu alfa in pete; ascunsa implicit"""
    g = K.empty(name, parent or CP4)
    for sn in src_names:
        so = bpy.data.objects[sn]; me = so.data.copy(); me.name = name + '.' + sn
        bm = bmesh.new(); bm.from_mesh(me)
        for v in bm.verts: v.co += v.normal * off
        bm.to_mesh(me); bm.free(); me.materials.clear(); me.materials.append(mat)
        ob = bpy.data.objects.new(me.name, me); scn.collection.objects.link(ob); ob.parent = g; ob.visible_shadow = False
    g.hide_render = True
    for c in g.children: c.hide_render = True
    return g

CUT = K.empty('CUT', CP4); FULL = K.empty('FULL', CP4)
for n in ['cp4c.housing', 'cp4c.flange', 'cp4c.head', 'cp4c.bushes', 'cp4c.seal', 'cp4c.hbolts', 'cp4c.fscrews']: part(n, CUT)
for n in ['cp4.zme', 'cp4.ports']: part(n, CP4)
for n in ['cp4.housing', 'cp4.flange', 'cp4.head', 'cp4.hbolts', 'cp4.fscrews', 'cp4.seal']: part(n, FULL)
shaft = part('cp4.shaft', oname='shaft'); shaftDam = part('cp4c.shaftDam', oname='shaftDam')
tap = K.empty('tap', CP4); part('cp4c.tappet', tap, oname='tappet')
roller = part('cp4.roller', tap, over={'steelPol': M['rollerPol']}, oname='roller')
plunger = part('cp4.plunger', oname='plunger')
inValve = part('cp4.inValve', oname='inValve'); inSpring = part('cp4.inSpring', oname='inSpring')
outBall = part('cp4.outBall', oname='outBall'); outSpring = part('cp4.outSpring', oname='outSpring')
inSpring.location.y = 86.0; outBall.location.y = 81.6; outSpring.location.y = 81.6
fLP = part('cp4c.fuelLP', oname='fLP'); fCol = part('cp4c.fuelCol', oname='fCol'); fCh = part('cp4c.fuelCh', oname='fCh')
fOut = part('cp4c.fuelOut', oname='fOut'); fIn = part('cp4c.fuelIn', oname='fIn')
for f in (fLP, fCol, fCh, fOut, fIn):
    for c in f.children: c.visible_shadow = False

# arcul pistonului (doua forme; pozitia spirelor e liniara in cursa tachetului)
SR, SW, STURNS = 8.3, 2.0, 5.5
def spring_pts(y0, y1, perTurn=40, radial=14):
    r = SW / 2; ne = 1.0; L = max(y1 - y0 - SW, STURNS * SW * 0.98)
    act = STURNS - 2 * ne; pa = (L - 2 * ne * SW) / act
    def hAt(k):
        if k < ne: return k * SW
        if k > STURNS - ne: return L - (STURNS - k) * SW
        return ne * SW + (k - ne) * pa
    n = int(round(STURNS * perTurn)) + 1; P = []
    for i in range(n):
        k = i / (n - 1) * STURNS; a = k * 2 * math.pi; ca, sa = math.cos(a), math.sin(a); y = y0 + r + hAt(k)
        dk = 0.01; dy = (hAt(min(STURNS, k + dk)) - hAt(max(0, k - dk))) / (2 * dk) / (2 * math.pi)
        t = Vector((-SR * sa, dy, SR * ca)).normalized(); nr = Vector((ca, 0, sa)); bb = t.cross(nr)
        for j in range(radial):
            ph = j / radial * 2 * math.pi; d = nr * math.cos(ph) + bb * math.sin(ph)
            P.append((SR * ca + d.x * r, y + d.y * r, SR * sa + d.z * r))
    return P, n, radial
PA, n_, rad_ = spring_pts(pkin.HA + 12.9, 53); PB, _, _ = spring_pts(pkin.HB + 12.9, 53)
faces = [(i * rad_ + j, i * rad_ + (j + 1) % rad_, (i + 1) * rad_ + (j + 1) % rad_, (i + 1) * rad_ + j) for i in range(n_ - 1) for j in range(rad_)]
sme = bpy.data.meshes.new('spring'); sme.from_pydata(PA, [], faces); sme.shade_smooth(); sme.materials.append(M['steel'])
spring = bpy.data.objects.new('spring', sme); scn.collection.objects.link(spring); spring.parent = CP4
spring.shape_key_add(name='A'); kb = spring.shape_key_add(name='B'); kb.slider_min, kb.slider_max = -10, 10
for i, p in enumerate(PB): kb.data[i].co = p

# piei de uzura / rugina / lacuri (ascunse; starile le arata)
skin(['shaft.steelPol', 'shaft.steel'], 'd_rust_shaft', M['rust'], parent=shaft)
skin(['roller.steelPol'], 'd_rust_roller', M['rust'], parent=roller)
skin(['plunger.steelPol', 'plunger.steel'], 'd_rust_plunger', M['rust'], parent=plunger)
skin(['shaft.steelPol', 'shaft.steel'], 'd_lac_shaft', M['lac'], parent=shaft)
skin(['roller.steelPol'], 'd_lac_roller', M['lac'], parent=roller)
skin(['plunger.steelPol', 'plunger.steel'], 'd_lac_plunger', M['lac'], parent=plunger)
skin(['shaft.steelPol'], 'd_wear_shaft', M['wear'], parent=shaft)
skin(['roller.steelPol'], 'd_wear_roller', M['wear'], parent=roller)
skin(['plunger.steelPol'], 'd_wear_plunger', M['wear'], parent=plunger)

irig.setup_world(0.3); irig.setup_camera(); irig.setup_render(1080, 1920, 32, 0.0)
os.makedirs(os.path.join(HERE, 'blend'), exist_ok=True)
bp = os.path.join(HERE, 'blend', 'pump.blend')
bpy.ops.wm.save_as_mainfile(filepath=bp); bpy.ops.file.pack_all(); bpy.ops.wm.save_as_mainfile(filepath=bp, compress=True)
print('SAVED', bp, len(bpy.data.objects), 'objects')
