# Rezervorul de motorina al masinii, in sectiune (planul y = 0, jumatatea din fata scoasa): motorina, apa adunata pe fund
# (apa e mai grea decat motorina), picaturi de condens pe tavan si pe peretii de deasupra motorinei, modulul pompei cu sorbul jos.
#   venv_bpy/bin/python tank.py   -> blend/tank.blend + blend/tank.json
import sys, os, json, math
sys.path.insert(0, '/home/claude/w/inj'); sys.path.insert(0, '/home/claude/w/serinj')
import bpy, bmesh, numpy as np
import kit as K, imats as IM
from micro_lin import sec_lin

OUT = '/home/claude/w/serinj/blend/'; os.makedirs(OUT, exist_ok=True)
K.init(empty=True); M = IM.make_all()
LX, LY, LZ, T = 520.0, 300.0, 240.0, 5.0       # exterior, perete
ZW, ZF = T + 14.0, T + 96.0                     # varful apei, nivelul motorinei
rng = np.random.default_rng(7)

secT = sec_lin('secTank', 0x3a3f47, 22.0, 1.0, 0.3)
tankM = IM.metal('tankHDPE', 0x2a2d33, 0.55, metal=0.0, coat=0.15)

def mark_front(o, y0=0.0, tol=0.05):
    me = o.data
    for p in me.polygons:
        if p.normal.y < -0.9 and abs(p.center.y - y0) < tol: p.material_index = 1
    me.update()

def cut_front(o, y0=0.0):
    c = K.box('cutter', (LX * 3, 1000.0, LZ * 4), c=(0, y0 - 500.0, LZ / 2))
    K.boolean(o, c, 'DIFFERENCE')

# ---------- carcasa
outer = K.box('t_shell', (LX, LY, LZ), c=(0, 0, LZ / 2), mat=[tankM, secT], bev=34.0, seg=5)
inner = K.box('t_in', (LX - 2 * T, LY - 2 * T, LZ - 2 * T), c=(0, 0, LZ / 2), bev=29.0, seg=5)
K.boolean(outer, inner, 'DIFFERENCE')
cut_front(outer); mark_front(outer); K.shade(outer, 30)

# ---------- lichide: forma interioara taiata intre doua cote (fata din fata retrasa putin, ca la filtru)
def liquid(name, z0, z1, mat, shrink=0.35, yf=0.3):
    o = K.box(name, (LX - 2 * T - 2 * shrink, LY - 2 * T - 2 * shrink, LZ - 2 * T - 2 * shrink), c=(0, 0, LZ / 2), mat=mat, bev=29.0 - shrink, seg=5)
    slab = K.box(name + '_s', (LX * 2, LY, z1 - z0), c=(0, yf + LY / 2, (z0 + z1) / 2))
    K.boolean(o, slab, 'INTERSECT'); o.visible_shadow = False
    return o
water = liquid('t_water', T + 0.2, ZW, M['water'])
fuel = liquid('t_fuel', ZW, ZF, M['fuelLP'])

# ---------- picaturile de condens (pe tavan si pe peretii de deasupra motorinei)
bm = bmesh.new(); drops = []
def drop(c, r, n):
    """picatura turtita spre perete (n = normala peretelui, spre interior)"""
    m = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=r)
    vs = m['verts']; n = np.asarray(n, float)
    for v in vs:
        p = np.array(v.co); d = p @ n
        p = p - n * d * 0.55                      # turtita
        if d < 0: p = p - n * d * 0.4             # spatele lipit de perete
        v.co = (p + np.asarray(c)).tolist()
    drops.append((list(c), r))
zt = LZ - T
for k in range(150):                              # tavan
    x = rng.uniform(-LX / 2 + 40, LX / 2 - 40); y = rng.uniform(14, LY / 2 - 30); r = rng.uniform(2.6, 6.5)
    if abs(x - 95) < 58 and abs(y - 70) < 58: continue            # modulul pompei
    drop((x, y, zt - r * 0.35), r, (0, 0, -1))
yb = LY / 2 - T
for k in range(130):                              # peretele din spate, deasupra motorinei
    x = rng.uniform(-LX / 2 + 36, LX / 2 - 36); z = rng.uniform(ZF + 14, zt - 30); r = rng.uniform(2.4, 6.0) * (0.75 + 0.5 * (z - ZF) / (zt - ZF))
    if abs(x - 95) < 52: continue
    drop((x, yb - r * 0.35, z), r, (0, -1, 0))
for sx in (-1, 1):                                # peretii laterali
    xw = sx * (LX / 2 - T)
    for k in range(40):
        y = rng.uniform(14, LY / 2 - 30); z = rng.uniform(ZF + 14, zt - 30); r = rng.uniform(2.4, 5.5)
        drop((xw - sx * r * 0.35, y, z), r, (-sx, 0, 0))
for k in range(18):                               # picaturi cazute pe fundul de apa (inca rotunde)
    x = rng.uniform(-LX / 2 + 50, LX / 2 - 50); y = rng.uniform(20, LY / 2 - 40); r = rng.uniform(3, 6)
me = K.bm_to_mesh(bm, 't_drops', smooth=True, sharp=None)
dro = K.obj('t_drops', me, M['water']); dro.visible_shadow = False

# ---------- modulul pompei, sorbul, conducta de umplere
plast = IM.metal('pumpPl', 0x6f7680, 0.45, metal=0.0, coat=0.2)
pump = K.cyl('t_pump', 42.0, LZ - 52.0, c=(95, 70, 52 + (LZ - 52) / 2), mat=plast, seg=48)
flange = K.cyl('t_flange', 74.0, 12.0, c=(95, 70, LZ + 4.0), mat=plast, seg=64, bev=2.0)
sock = K.cyl('t_sock', 34.0, 16.0, c=(95, 70, T + 11.0), mat=IM.metal('sock', 0xd9d4c4, 0.8, metal=0.0), seg=40, bev=3.0)
stem = K.cyl('t_stem', 9.0, 34.0, c=(95, 70, T + 34.0), mat=plast, seg=24)
fline = K.tube('t_fline', [(115, 70, LZ + 10), (115, 70, LZ + 60), (200, 70, LZ + 70), (330, 70, LZ + 70)], 7.0, mat=IM.metal('hose', 0x1d1f23, 0.5, metal=0.0), seg=20, fillet=25)
neck = K.tube('t_neck', [(-LX / 2 + 30, 90, LZ - 70), (-LX / 2 - 30, 90, LZ - 40), (-LX / 2 - 80, 90, LZ + 40), (-LX / 2 - 110, 90, LZ + 120)], 24.0, mat=tankM, seg=40, fillet=40)
cap = K.cyl('t_cap', 30.0, 18.0, c=(-LX / 2 - 110, 90, LZ + 128), mat=IM.metal('capM', 0x2b2e34, 0.4, metal=0.0), seg=40, bev=3.0)

def group(name, objs):
    e = K.empty(name)
    for o in objs: o.parent = e
    return e
group('TANK', [outer, pump, flange, sock, stem, fline, neck, cap]); group('T_FUEL', [fuel])
group('T_WATER', [water]); group('T_DROPS', [dro])
META = {'pts': {'water': [0, 70, (T + ZW) / 2], 'fuel': [0, 70, (ZW + ZF) / 2], 'ceil': [-120, 60, zt - 4], 'wall': [-150, yb - 3, ZF + 60],
                'sock': [95, 70, T + 11.0], 'neck': [-LX / 2 - 100, 90, LZ + 110], 'pump': [95, 70, 150]},
        'dims': {'LX': LX, 'LY': LY, 'LZ': LZ, 'T': T, 'ZW': ZW, 'ZF': ZF}, 'drops': drops}
json.dump(META, open(OUT + 'tank.json', 'w'))
bpy.ops.wm.save_as_mainfile(filepath=OUT + 'tank.blend')
print('SAVED', OUT + 'tank.blend', len(drops), flush=True)
