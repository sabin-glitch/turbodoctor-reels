# Scaunul bilei deteriorat: adancituri pe inelul de contact, apoi canalul format prin unirea lor. Scrie blend/inj_dmg.blend + seat_dmg.json
#   venv_bpy/bin/python seatdmg.py
import sys, os, json, math
sys.path.insert(0, '/home/claude/w/inj')
import bpy, bmesh, numpy as np
from mathutils import Vector
import kit as K

OUT = '/home/claude/w/serinj/blend/'; os.makedirs(OUT, exist_ok=True)
bpy.ops.wm.open_mainfile(filepath='/home/claude/w/inj/out/inj_cut.blend'); K.init(empty=False)
D = bpy.data.objects; M = bpy.data.materials
aR, aL = math.radians(-30), math.radians(-150)
R0, Z0 = 0.601, 136.621                      # inelul de contact bila / scaun
NV = np.array([-1.0, 1.0]) / math.sqrt(2)    # normala conului spre gol, in (r, z)
TV = np.array([1.0, 1.0]) / math.sqrt(2)     # directia conului (in sus, spre exterior)

def cone_pt(s, th, depth):
    """punct pe con la distanta s de inelul de contact (de-a lungul generatoarei), azimut th, impins cu depth spre gol"""
    rz = np.array([R0, Z0]) + TV * s + NV * depth
    return Vector((rz[0] * math.cos(th), rz[0] * math.sin(th), rz[1]))

def ball(name, c, r, seg=20):
    bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=max(8, seg // 2), radius=r)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(o); o.parent = K.ROOT; o.location = c
    me.materials.append(M['eroded'])
    return o

def carve(src, name, cutters):
    o = src.copy(); o.data = src.data.copy(); o.name = name; o.data.name = name
    bpy.context.scene.collection.objects.link(o); o.parent = src.parent
    bpy.context.view_layer.update()
    for c in cutters:
        K.boolean(o, c, 'DIFFERENCE', solver='EXACT')
    o.hide_render = True
    return o

rng = np.random.default_rng(11)
# adancituri: pe toata partea ramasa a inelului (azimut de la -30 la 210 de grade), mai dese langa fetele de sectiune
pits = []
ths = list(np.linspace(math.radians(-29), math.radians(209), 26)) + [aR + 0.01, aL - 0.01, aR + 0.06, aL - 0.06]
for th in ths:
    th = th + rng.uniform(-0.05, 0.05)
    s = rng.uniform(-0.05, 0.05); r = rng.uniform(0.018, 0.04)
    pits.append((s, th, r))
valve = D['valve']
pit_c = [ball('pc%02d' % i, cone_pt(s, th, r * 0.45), r) for i, (s, th, r) in enumerate(pits)]
vp = carve(valve, 'valve_pits', pit_c)
# canalul: adanciturile de la azimut 90 (in spate, cu fata spre camera de sus) se unesc intr-un sant de-a lungul generatoarei
pit_c2 = [ball('pd%02d' % i, cone_pt(s, th, r * 0.45), r) for i, (s, th, r) in enumerate(pits)]
TH_C = math.radians(90)
ch = []
for k, s in enumerate(np.linspace(-0.26, 0.42, 30)):
    w = 0.034 + 0.012 * math.sin(k * 1.7) + 0.008 * rng.random()
    ch.append(ball('ch%02d' % k, cone_pt(s, TH_C + 0.02 * math.sin(k * 0.9), w * 0.35), w, seg=16))
vc = carve(valve, 'valve_chan', pit_c2 + ch)
# motorina din alezajul de sub bila, fara „capacul” din con (pentru vederea de sus, cu bila scoasa)
fcc = D['f_cc']; low = fcc.copy(); low.data = fcc.data.copy(); low.name = 'f_cc_low'; bpy.context.scene.collection.objects.link(low); low.parent = fcc.parent
cutc = K.cyl('cc_cut', 3.0, 7.4, c=(0, 0, 132.68), mat=None, seg=48)
bpy.context.view_layer.update(); K.boolean(low, cutc, 'INTERSECT', solver='EXACT'); low.hide_render = True
# traseul motorinei prin canal (pentru particule), mm
path = [list(cone_pt(s, TH_C, 0.0)) for s in np.linspace(-0.3, 0.5, 12)]
json.dump({'chan_path': path, 'ring': [R0, Z0], 'pits': [[list(cone_pt(s, th, 0.0)), r] for (s, th, r) in pits]}, open(OUT + 'seat_dmg.json', 'w'), indent=1)
bpy.ops.wm.save_as_mainfile(filepath=OUT + 'inj_dmg.blend')
print('SAVED inj_dmg', len(vp.data.polygons), len(vc.data.polygons), flush=True)
