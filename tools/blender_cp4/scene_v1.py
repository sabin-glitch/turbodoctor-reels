# Proba Blender: pompa Bosch CP4.1 in sectiune (aceeasi geometrie ca animatia "Amorsare filtru motorina").
# Rulare: venv/bin/python scene.py still <frame> [scale%] [samples]   |   venv/bin/python scene.py anim [start end]
import bpy, json, math, sys, os
import numpy as np
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'src')
FPS = 30
DUR = 6.0
NF = int(DUR * FPS)

# ---------------------------------------------------------------- utilitare
def rnd(x):
    v = math.sin(x * 12.9898 + 4.1414) * 43758.5453
    return v - math.floor(v)
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease(x): x = clamp(x); return x * x * (3 - 2 * x)
def lerp(a, b, k): return a + (b - a) * k
def W(p):  # reperul pompei (three.js, mm, Y sus) -> lume Blender (m, Z sus)
    return Vector((p[0], -p[2], p[1])) * 0.001

for o in list(bpy.data.objects): bpy.data.objects.remove(o)
scn = bpy.context.scene
scn.render.fps = FPS
scn.frame_start, scn.frame_end = 0, NF - 1

# ---------------------------------------------------------------- materiale
def srgb(h):
    c = [((h >> 16) & 255) / 255, ((h >> 8) & 255) / 255, (h & 255) / 255]
    return [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c] + [1]

def pbr(name, col, metal, rough, bump=None, aniso=0.0, coat=0.0, wave=None, emis=None):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; N = nt.nodes; L = nt.links
    b = N['Principled BSDF']
    b.inputs['Base Color'].default_value = srgb(col)
    b.inputs['Metallic'].default_value = metal
    b.inputs['Roughness'].default_value = rough
    if aniso: b.inputs['Anisotropic'].default_value = aniso
    if coat: b.inputs['Coat Weight'].default_value = coat
    tc = N.new('ShaderNodeTexCoord')
    hgt = None
    if bump:  # (scara, amplitudine, variatie de asperitate)
        nz = N.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = bump[0]; nz.inputs['Detail'].default_value = 8
        L.new(tc.outputs['Object'], nz.inputs['Vector'])
        hgt = nz.outputs['Fac']
        if len(bump) > 2:
            mr = N.new('ShaderNodeMapRange'); mr.inputs['To Min'].default_value = rough - bump[2] / 2; mr.inputs['To Max'].default_value = rough + bump[2] / 2
            L.new(nz.outputs['Fac'], mr.inputs['Value']); L.new(mr.outputs['Result'], b.inputs['Roughness'])
    if wave:  # urme de frezare pe fetele de sectiune
        wv = N.new('ShaderNodeTexWave'); wv.wave_type = 'RINGS'; wv.inputs['Scale'].default_value = wave[0]
        wv.inputs['Distortion'].default_value = 0.6; wv.inputs['Detail'].default_value = 2
        mp = N.new('ShaderNodeMapping'); mp.inputs['Location'].default_value = (60, 0, 0)
        L.new(tc.outputs['Object'], mp.inputs['Vector']); L.new(mp.outputs['Vector'], wv.inputs['Vector'])
        if hgt is not None:
            ad = N.new('ShaderNodeMath'); ad.operation = 'MULTIPLY_ADD'; ad.inputs[1].default_value = wave[1]
            L.new(wv.outputs['Fac'], ad.inputs[0]); L.new(hgt, ad.inputs[2]); hgt = ad.outputs[0]
        else: hgt = wv.outputs['Fac']
    if hgt is not None:
        bp = N.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = (bump[1] if bump else 0.2); bp.inputs['Distance'].default_value = 0.05
        L.new(hgt, bp.inputs['Height']); L.new(bp.outputs['Normal'], b.inputs['Normal'])
    if emis:
        b.inputs['Emission Color'].default_value = srgb(emis); b.inputs['Emission Strength'].default_value = 0.0
    return m

def liquid(name, col, dens=0.06):
    m = bpy.data.materials.new(name); m.use_nodes = True
    N = m.node_tree.nodes; L = m.node_tree.links
    b = N['Principled BSDF']
    b.inputs['Base Color'].default_value = [1, 1, 1, 1]
    b.inputs['Roughness'].default_value = 0.02
    b.inputs['IOR'].default_value = 1.46
    b.inputs['Transmission Weight'].default_value = 1.0
    va = N.new('ShaderNodeVolumeAbsorption'); va.inputs['Color'].default_value = srgb(col); va.inputs['Density'].default_value = dens
    L.new(va.outputs['Volume'], N['Material Output'].inputs['Volume'])
    tr = N.new('ShaderNodeBsdfTransparent'); mx = N.new('ShaderNodeMixShader'); mx.name = 'FADE'
    mx.inputs['Fac'].default_value = 1.0
    L.new(tr.outputs[0], mx.inputs[1]); L.new(b.outputs[0], mx.inputs[2]); L.new(mx.outputs[0], N['Material Output'].inputs['Surface'])
    return m

MAT = {
    'castAlu':    pbr('castAlu', 0xb9bcc0, 1, 0.55, bump=(1.6, 0.35, 0.25)),
    'machAlu':    pbr('machAlu', 0xd8dadd, 1, 0.22, bump=(40, 0.04), aniso=0.4),
    'secAlu':     pbr('secAlu', 0xd2d5d9, 1, 0.30, bump=(30, 0.05, 0.1), wave=(0.45, 0.25)),
    'steelHead':  pbr('steelHead', 0x9a9fa6, 1, 0.38, bump=(6, 0.12, 0.15)),
    'steel':      pbr('steel', 0xb7bcc2, 1, 0.30),
    'steelPol':   pbr('steelPol', 0xdfe2e6, 1, 0.12),
    'steelDark':  pbr('steelDark', 0x4a4e55, 1, 0.4),
    'secSteel':   pbr('secSteel', 0xa4a9b0, 1, 0.28, bump=(30, 0.05, 0.1), wave=(0.6, 0.25)),
    'secTap':     pbr('secTap', 0x7d828a, 1, 0.3, wave=(0.9, 0.2)),
    'secBronze':  pbr('secBronze', 0xc9a066, 1, 0.3),
    'zincW':      pbr('zincW', 0xc9ced6, 1, 0.32, bump=(3, 0.06, 0.12)),
    'bronze':     pbr('bronze', 0xc08f4e, 1, 0.3),
    'sealBrown':  pbr('sealBrown', 0x4a2a1a, 0, 0.55),
    'plasticGrey': pbr('plasticGrey', 0x3a3d42, 0, 0.5, coat=0.2),
    'markDark':   pbr('markDark', 0x222428, 0.6, 0.4),
    'dlc':        pbr('dlc', 0x2e3035, 1, 0.22, coat=0.5),
    'scored':     pbr('scored', 0x6e5a48, 1, 0.65, bump=(14, 0.9, 0.4)),
    'fuel':       liquid('fuel', 0x2f8cff, 0.035),
    'fuelCh':     liquid('fuelCh', 0x2f8cff, 0.05),
    'fuelHP':     liquid('fuelHP', 0xff6a3d, 0.06),
}
MAT['rollerPol'] = pbr('rollerPol', 0xdfe2e6, 1, 0.12, emis=0xff6a10)

# ---------------------------------------------------------------- geometria din animatia existenta
GJ = json.load(open(os.path.join(SRC, 'geo.json')))
GB = open(os.path.join(SRC, 'geo.bin'), 'rb').read()

ROOT = bpy.data.objects.new('CP4', None)
scn.collection.objects.link(ROOT)
ROOT.rotation_euler = (math.pi / 2, 0, 0)
ROOT.scale = (0.001, 0.001, 0.001)

def empty(name, parent=ROOT):
    e = bpy.data.objects.new(name, None); scn.collection.objects.link(e); e.parent = parent; return e

def mk_mesh(name, pos, nrm, idx):
    me = bpy.data.meshes.new(name)
    nv = len(pos); nl = len(idx); nt = nl // 3
    me.vertices.add(nv); me.vertices.foreach_set('co', pos.astype(np.float32).ravel())
    me.loops.add(nl); me.loops.foreach_set('vertex_index', idx.astype(np.int32))
    me.polygons.add(nt); me.polygons.foreach_set('loop_start', np.arange(0, nl, 3, dtype=np.int32))
    me.update(); me.validate(clean_customdata=False)
    me.polygons.foreach_set('use_smooth', np.ones(nt, dtype=bool))
    if nrm is not None:
        n = nrm / np.maximum(1e-9, np.linalg.norm(nrm, axis=1))[:, None]
        if len(me.vertices) == nv: me.normals_split_custom_set_from_vertices(n.tolist())
    return me

def part(name, parent=ROOT, over=None):
    g = empty(name, parent)
    for p in GJ:
        if p['n'] != name: continue
        o, v = p['o'], p['v']; b = p['b']
        pq = np.frombuffer(GB, np.uint16, v * 3, o).reshape(-1, 3).astype(np.float64)
        pos = np.array(b[:3]) + pq * np.array(b[3:])
        o2 = o + ((v * 6 + 3) & ~3)
        if p.get('h'): nq = np.frombuffer(GB, np.int16, v * 4, o2).reshape(-1, 4)[:, :3] / 32767.0; o3 = o2 + v * 8
        else: nq = np.frombuffer(GB, np.int8, v * 4, o2).reshape(-1, 4)[:, :3] / 127.0; o3 = o2 + v * 4
        idx = np.frombuffer(GB, np.uint16 if p['w'] == 2 else np.uint32, p['i'], o3)
        me = mk_mesh(name + '.' + p['m'], pos, nq, idx)
        mat = (over or {}).get(p['m']) or MAT[p['m']]
        me.materials.append(mat)
        ob = bpy.data.objects.new(me.name, me); scn.collection.objects.link(ob); ob.parent = g
    return g

for n in ['cp4c.housing', 'cp4c.flange', 'cp4c.head', 'cp4c.bushes', 'cp4c.seal', 'cp4c.hbolts', 'cp4c.fscrews', 'cp4.zme', 'cp4.ports']:
    part(n)
shaft = part('cp4.shaft')
shaftDam = part('cp4c.shaftDam')
tap = empty('tap')
part('cp4c.tappet', tap)
roller = part('cp4.roller', tap, over={'steelPol': MAT['rollerPol']})
plunger = part('cp4.plunger')
inValve = part('cp4.inValve'); inSpring = part('cp4.inSpring'); outBall = part('cp4.outBall'); outSpring = part('cp4.outSpring')
inSpring.location.y = 86.0; outBall.location.y = 81.6; outSpring.location.y = 81.6
fLP = part('cp4c.fuelLP'); fCol = part('cp4c.fuelCol'); fCh = part('cp4c.fuelCh'); fOut = part('cp4c.fuelOut'); fIn = part('cp4c.fuelIn')
for f in (fLP, fCol, fCh, fOut, fIn):
    for c in f.children: c.visible_shadow = False

# ---------------------------------------------------------------- arcul pistonului (doua forme, pozitia e liniara in h)
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
HA, HB = 18.0, 40.0
PA, n_, rad_ = spring_pts(HA + 12.9, 53)
PB, _, _ = spring_pts(HB + 12.9, 53)
faces = [(i * rad_ + j, i * rad_ + (j + 1) % rad_, (i + 1) * rad_ + (j + 1) % rad_, (i + 1) * rad_ + j) for i in range(n_ - 1) for j in range(rad_)]
sme = bpy.data.meshes.new('spring'); sme.from_pydata(PA, [], faces); sme.shade_smooth(); sme.materials.append(MAT['steel'])
spring = bpy.data.objects.new('spring', sme); scn.collection.objects.link(spring); spring.parent = ROOT
spring.shape_key_add(name='A'); kb = spring.shape_key_add(name='B'); kb.slider_min, kb.slider_max = -10, 10
for i, p in enumerate(PB): kb.data[i].co = p

# ---------------------------------------------------------------- cinematica (aceeasi ca in animatia three.js)
Rb, LIFT, RRr = 14.5, 6.5, 5.5
NT = 360
aa = np.linspace(0, 2 * np.pi, 1440, endpoint=False)
camR = Rb + LIFT * (0.5 + 0.5 * np.cos(2 * aa))
hPar = np.zeros(NT + 1); hCross = np.zeros(NT + 1)
for i in range(NT + 1):
    ph = i / NT * math.pi; px = camR * np.cos(aa + ph); py = camR * np.sin(aa + ph)
    m = np.abs(px) < RRr; hPar[i] = np.max(py[m] + np.sqrt(RRr * RRr - px[m] ** 2)); hCross[i] = py.max() + RRr
def look(tb, ph):
    u = (ph / math.pi) % 1.0; x = u * NT; i = int(math.floor(x)); f = x - i
    return tb[i] * (1 - f) + tb[min(NT, i + 1)] * f

def clock(nodes):
    acc = [0.0]
    for i in range(1, len(nodes)): acc.append(acc[-1] + (nodes[i][0] - nodes[i - 1][0]) * (nodes[i][1] + nodes[i - 1][1]) / 2)
    def f(t):
        if t <= nodes[0][0]: return (t - nodes[0][0]) * nodes[0][1]
        for i in range(1, len(nodes)):
            if t <= nodes[i][0]:
                dt = t - nodes[i - 1][0]; T_ = nodes[i][0] - nodes[i - 1][0]; v0, v1 = nodes[i - 1][1], nodes[i][1]
                return acc[i - 1] + v0 * dt + (v1 - v0) * dt * dt / (2 * T_)
        return acc[-1] + (t - nodes[-1][0]) * nodes[-1][1]
    return f

# cronologia probei (secunde): 0-2.2 pompare normala | 1.4-2.6 intra aerul | 2.4 rola se blocheaza, se incinge |
# 3.0-4.2 tachetul se roteste 90 grade | 4.0+ rola taie cama, pilitura
CAMc = clock([[0, 4.2], [3.0, 4.2], [4.4, 2.8], [DUR, 2.6]])
SPINc = clock([[0, 15.0], [2.3, 15.0], [3.0, 0], [DUR, 0]])
T_FUEL, T_HEAT, T_ROT, T_DAM, T_CHIP, T_SPARK = 1.4, 2.4, 3.0, 4.15, 3.9, 2.7

def state(t):
    phi = -CAMc(t)
    fuel = 1 - ease((t - T_FUEL) / 1.2)
    heat = ease((t - T_HEAT) / 1.2) * (0.8 + 0.2 * math.sin(t * 23))
    rot = ease((t - T_ROT) / 1.2)
    dam = 1 if t > T_DAM else 0
    h = lerp(look(hPar, phi), look(hCross, phi), rot)
    v = look(hPar, phi + 0.02) - look(hPar, phi - 0.02); up = clamp(v * 4, -1, 1)
    return dict(phi=phi, spin=SPINc(t), rot=rot, dam=dam, fuel=fuel, heat=heat, h=h, up=up)

# ---------------------------------------------------------------- particule: scantei si pilitura
def shard_mesh(name, seed):
    import random; R = random.Random(seed)
    P = [(R.uniform(-1, 1) * 1.1, R.uniform(-1, 1) * 0.35, R.uniform(-1, 1) * 0.6) for _ in range(7)]
    import bmesh
    bm = bmesh.new()
    for p in P: bm.verts.new(p)
    bmesh.ops.convex_hull(bm, input=bm.verts)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); return me
MAT['chip'] = pbr('chip', 0xd5d9de, 1, 0.18)
mspark = bpy.data.materials.new('spark'); mspark.use_nodes = True
Nn = mspark.node_tree.nodes; Ll = mspark.node_tree.links
for nd in list(Nn):
    if nd.type != 'OUTPUT_MATERIAL': Nn.remove(nd)
em = Nn.new('ShaderNodeEmission'); em.inputs['Color'].default_value = (1.0, 0.45, 0.08, 1); em.inputs['Strength'].default_value = 60
Ll.new(em.outputs[0], Nn['Material Output'].inputs['Surface'])
sph = bpy.data.meshes.new('sparkM')
import bmesh
bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=8, v_segments=6, radius=0.22); bm.to_mesh(sph); bm.free(); sph.materials.append(mspark)

NCH, NSP = 70, 46
chips = []
for i in range(NCH):
    me = shard_mesh('chip%d' % i, i); me.materials.append(MAT['chip'])
    ob = bpy.data.objects.new('chip%d' % i, me); scn.collection.objects.link(ob); ob.parent = ROOT
    s = 0.35 + rnd(i * 3.7) * 0.6; ob['s'] = s; chips.append(ob)
sparks = []
for i in range(NSP):
    ob = bpy.data.objects.new('spark%d' % i, sph); scn.collection.objects.link(ob); ob.parent = ROOT
    ob.visible_shadow = False; sparks.append(ob)

glow = bpy.data.lights.new('glow', 'POINT'); glow.color = (1.0, 0.42, 0.1); glow.shadow_soft_size = 0.002
glowO = bpy.data.objects.new('glow', glow); scn.collection.objects.link(glowO)

# ---------------------------------------------------------------- camera, lumini, fundal
cam = bpy.data.cameras.new('cam'); camO = bpy.data.objects.new('cam', cam); scn.collection.objects.link(camO); scn.camera = camO
cam.sensor_fit = 'VERTICAL'; cam.sensor_height = 24.0
cam.dof.use_dof = True; cam.dof.aperture_blades = 7; cam.dof.aperture_ratio = 1.0
focus = bpy.data.objects.new('focus', None); scn.collection.objects.link(focus); cam.dof.focus_object = focus

SH = [  # t, tinta (reper pompa, mm), azimut, elevatie, distanta (mm), focala (mm), f-stop
    (0.0, (2, 30, 4), 54, 17, 470, 42, 2.8),
    (2.6, (3, 24, 4), 46, 16, 400, 46, 2.4),
    (4.2, (5, 17, 6), 38, 17, 300, 52, 2.0),
    (DUR, (5, 16, 6), 34, 18, 285, 54, 2.0),
]
def shot(t):
    i = 0
    while i < len(SH) - 2 and t >= SH[i + 1][0]: i += 1
    a, b = SH[i], SH[i + 1]; k = ease((t - a[0]) / (b[0] - a[0]))
    c = [lerp(a[1][j], b[1][j], k) for j in range(3)]
    return c, lerp(a[2], b[2], k), lerp(a[3], b[3], k), math.exp(lerp(math.log(a[4]), math.log(b[4]), k)), lerp(a[5], b[5], k), lerp(a[6], b[6], k)

def area(name, loc, target, size, energy, col=(1, 1, 1), shape='RECTANGLE', sy=None):
    l = bpy.data.lights.new(name, 'AREA'); l.energy = energy; l.color = col; l.shape = shape; l.size = size; l.size_y = sy or size
    o = bpy.data.objects.new(name, l); scn.collection.objects.link(o); o.location = loc
    d = (Vector(target) - Vector(loc)); o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler(); return o
C0 = W((0, 20, 0))
area('key', C0 + Vector((0.55, -0.35, 0.55)), C0, 0.35, 55, (1.0, 0.97, 0.93), sy=0.2)
area('fill', C0 + Vector((0.2, -0.7, 0.05)), C0, 0.5, 5, (0.85, 0.9, 1.0))
area('rim', C0 + Vector((-0.45, 0.45, 0.35)), C0, 0.08, 45, (0.8, 0.88, 1.0), sy=0.6)
area('top', C0 + Vector((0.05, 0.0, 0.8)), C0, 0.3, 12)

world = bpy.data.worlds.new('W'); scn.world = world; world.use_nodes = True
WN = world.node_tree.nodes; WL = world.node_tree.links
bg = WN['Background']
env = WN.new('ShaderNodeTexEnvironment')
env.image = bpy.data.images.load(os.path.join(SRC, 'studio.exr'))
WL.new(env.outputs['Color'], bg.inputs['Color']); bg.inputs['Strength'].default_value = 0.22
lp = WN.new('ShaderNodeLightPath'); bg2 = WN.new('ShaderNodeBackground'); bg2.inputs['Color'].default_value = srgb(0x15181c); bg2.inputs['Strength'].default_value = 1.0
mxw = WN.new('ShaderNodeMixShader')
WL.new(lp.outputs['Is Camera Ray'], mxw.inputs['Fac']); WL.new(bg.outputs[0], mxw.inputs[1]); WL.new(bg2.outputs[0], mxw.inputs[2])
WL.new(mxw.outputs[0], WN['World Output'].inputs['Surface'])

# perete de fundal intunecat, putin texturat, pentru umbre moi si profunzime
bpy.ops.mesh.primitive_plane_add(size=3, location=W((0, 0, 0)) + Vector((-0.6, 0.6, 0)), rotation=(math.pi / 2, 0, math.radians(45)))
wall = bpy.context.active_object; wall.name = 'wall'
wm = pbr('wall', 0x101215, 0, 0.8, bump=(0.4, 0.2)); wall.data.materials.append(wm)


# ---------------------------------------------------------------- animatie pe cadre (cheie la fiecare cadru -> motion blur corect)
def key_all():
    rp = MAT['rollerPol'].node_tree.nodes['Principled BSDF']
    for f in range(NF + 1):
        t = f / FPS; S = state(t); h = S['h']
        shaft.rotation_euler = (0, 0, S['phi']); shaftDam.rotation_euler = (0, 0, S['phi'])
        shaft.scale = (1, 1, 1) if S['dam'] < 0.5 else (0, 0, 0); shaftDam.scale = (0, 0, 0) if S['dam'] < 0.5 else (1, 1, 1)
        tap.location = (0, h, 0); tap.rotation_euler = (0, S['rot'] * math.pi / 2, 0); roller.rotation_euler = (0, 0, S['spin'])
        plunger.location = (0, h, 0)
        kbB = spring.data.shape_keys.key_blocks['B']; kbB.value = (h - HA) / (HB - HA)
        up = S['up']; fuel = S['fuel']
        il = clamp(-up) * 1.1 * fuel + clamp(-up) * 0.4 * (1 - fuel)
        inValve.location = (0, 84.2 - il, 0); inSpring.scale = (1, (4.4 - il) / 4.4, 1)
        ol = clamp(up) * 0.9 * fuel; outBall.location = (15.66 + ol, 81.6, 0)
        outSpring.location = (outBall.location.x + 1.5, 81.6, 0); outSpring.scale = ((28 - outSpring.location.x) / 10.8, 1, 1)
        top = h + 50.4; fCol.location = (0, top, 0); fCol.scale = (1, max(0.05, 79 - top), 1)
        for ob in (shaft, shaftDam, tap, roller, plunger, inValve, inSpring, outBall, outSpring, fCol):
            ob.keyframe_insert('location', frame=f); ob.keyframe_insert('rotation_euler', frame=f); ob.keyframe_insert('scale', frame=f)
        kbB.keyframe_insert('value', frame=f)
        for nm, k in (('fuel', fuel), ('fuelCh', fuel), ('fuelHP', fuel)):
            mx = MAT[nm].node_tree.nodes['FADE']; mx.inputs['Fac'].default_value = 0.08 + 0.92 * k; mx.inputs['Fac'].keyframe_insert('default_value', frame=f)
        rp.inputs['Emission Strength'].default_value = 6.0 * S['heat'] ** 1.5; rp.inputs['Emission Strength'].keyframe_insert('default_value', frame=f)
        cy = h - 5.5
        glow.energy = 0.35 * S['heat']; glowO.location = W((4, cy, 4)); glow.keyframe_insert('energy', frame=f); glowO.keyframe_insert('location', frame=f)
        # scantei: fiecare cu nasterea ei, 0.35 s de viata, aruncate tangential din punctul de contact
        for i, ob in enumerate(sparks):
            tb = T_SPARK + i * (DUR - T_SPARK - 0.3) / NSP + rnd(i * 2.9) * 0.08; age = t - tb; life = 0.28 + rnd(i * 5.1) * 0.15
            if age < 0 or age > life or S['heat'] < 0.05:
                ob.scale = (0, 0, 0)
                ob.location = (2, cy, 3)
            else:
                v = 120 + rnd(i * 4.1) * 220; upv = (rnd(i * 6.7) - 0.3) * 120; zz = (rnd(i * 8.9) - 0.5) * 140
                ob.location = (2 + v * age, cy + 1 + upv * age - 900 * age * age, 2 + zz * age); k = 1 - age / life
                ob.scale = (0.6 + 0.6 * k,) * 3
            ob.keyframe_insert('location', frame=f); ob.keyframe_insert('scale', frame=f)
        # pilitura: se desprinde la contact si e purtata in carcasa, in jurul camei
        c1 = t - T_CHIP
        for i, ob in enumerate(chips):
            b = i * 0.03
            if c1 < b:
                ob.scale = (0, 0, 0); ob.location = (0, cy, 0)
            else:
                age = c1 - b; r = 21.8 + rnd(i * 2.1) * 4.6; a0 = math.pi / 2 - 0.25 - rnd(i * 9.7) * 0.2; w = 0.5 + rnd(i * 5.3) * 0.9
                ang = a0 - min(age, 6) * w * 0.9; sink = clamp(age / 3); rr = lerp(r, 23 + rnd(i * 3.9) * 3.2, sink)
                z = (rnd(i * 6.1) * 11.5) * (1 if i % 3 else -1) + (0.6 if i % 3 else 0)
                ob.location = (rr * math.cos(ang), rr * math.sin(ang), z); s = ob['s']; ob.scale = (s, s, s)
                ob.rotation_euler = (age * (2 + rnd(i) * 5), age * (1 + rnd(i * 2) * 4), rnd(i * 3) * 6)
            ob.keyframe_insert('location', frame=f); ob.keyframe_insert('scale', frame=f); ob.keyframe_insert('rotation_euler', frame=f)
        # camera
        c, az, el, d, lens, fst = shot(t)
        A, E = math.radians(az), math.radians(el)
        cp = (c[0] + d * math.sin(A) * math.cos(E), c[1] + d * math.sin(E), c[2] + d * math.cos(A) * math.cos(E))
        camO.location = W(cp); camO.rotation_euler = (W(c) - W(cp)).to_track_quat('-Z', 'Y').to_euler()
        focus.location = W((c[0], min(c[1], cy + 4), c[2] + 4))
        cam.lens = lens; cam.dof.aperture_fstop = fst
        camO.keyframe_insert('location', frame=f); camO.keyframe_insert('rotation_euler', frame=f); focus.keyframe_insert('location', frame=f)
        cam.keyframe_insert('lens', frame=f); cam.dof.keyframe_insert('aperture_fstop', frame=f)
    # interpolare liniara: cadrele sunt deja calculate
    for ad in [o.animation_data for o in bpy.data.objects] + [m.node_tree.animation_data for m in bpy.data.materials if m.node_tree] + \
              [spring.data.shape_keys.animation_data, cam.animation_data, glow.animation_data]:
        if not ad or not ad.action: continue
        try:
            fcs = ad.action.fcurves
        except AttributeError:
            fcs = [fc for l in ad.action.layers for s in l.strips for cb in s.channelbags for fc in cb.fcurves]
        for fc in fcs:
            for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'
key_all()

# ---------------------------------------------------------------- randare
R = scn.render
scn.render.engine = 'CYCLES'
cy_ = scn.cycles
cy_.device = 'CPU'; cy_.samples = 96; cy_.use_adaptive_sampling = True; cy_.adaptive_threshold = 0.03
R.use_persistent_data = True
cy_.use_denoising = True; cy_.denoiser = 'OPENIMAGEDENOISE'
cy_.max_bounces = 6; cy_.glossy_bounces = 3; cy_.transmission_bounces = 6; cy_.volume_bounces = 1; cy_.diffuse_bounces = 2
cy_.caustics_reflective = False; cy_.caustics_refractive = False; cy_.blur_glossy = 1.0
R.resolution_x, R.resolution_y = 1080, 1920
R.use_motion_blur = True; R.motion_blur_shutter = 0.5
scn.view_settings.view_transform = 'AgX'
try: scn.view_settings.look = 'AgX - Medium High Contrast'
except Exception: pass
R.image_settings.file_format = 'PNG'
R.film_transparent = False

if __name__ == '__main__':
    args = sys.argv[1:]
    mode = args[0] if args else 'save'
    os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
    if mode == 'still':
        fr = int(args[1]); wx = int(args[2]) if len(args) > 2 else 540; R.resolution_x, R.resolution_y = wx, wx * 16 // 9
        if len(args) > 3: cy_.samples = int(args[3])
        scn.frame_set(fr); R.filepath = os.path.join(HERE, 'out', 'still_%03d.png' % fr)
        bpy.ops.render.render(write_still=True)
    elif mode == 'anim':
        a, b = (int(args[1]), int(args[2])) if len(args) > 2 else (0, NF - 1)
        step = int(args[3]) if len(args) > 3 else 1; off = int(args[4]) if len(args) > 4 else 0
        wx = int(os.environ.get('WX', '720')); R.resolution_x, R.resolution_y = wx, wx * 16 // 9; cy_.samples = int(os.environ.get('SPP', '32'))
        for fr in range(a + off, b + 1, step):
            fp = os.path.join(HERE, 'frames', 'f%04d.png' % fr)
            if os.path.exists(fp): continue
            scn.frame_set(fr); R.filepath = fp; bpy.ops.render.render(write_still=True)
    elif mode == 'save':   # fisier .blend de sine statator (HDRI impachetat), gata de randat pe un calculator cu placa video
        R.resolution_x, R.resolution_y = 1080, 1920; cy_.samples = 64
        R.filepath = '//cadre/f'
        scn.frame_set(150)
        bp = os.path.join(HERE, 'out', 'cp4_proba.blend')
        bpy.ops.wm.save_as_mainfile(filepath=bp)
        bpy.ops.file.pack_all()
        bpy.ops.wm.save_as_mainfile(filepath=bp, compress=True)
