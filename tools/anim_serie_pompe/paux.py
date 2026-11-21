# Piesele din jurul pompei pentru seria pompelor: filtrul de motorina al masinii (in sectiune), modulul pompei electrice din rezervor,
# injectorul, rampa, racordul rapid si piulita olandeza. Geometria vine din animatia „Amorsare filtru” (src/geo.bin).
#   venv_bpy/bin/python paux.py   -> blend/aux.blend  (grupuri: FLT, TM, INJ, RAIL, QUICK, UNUT; lichide fltOut, fltCore, fltAll, tmFuel)
import sys, os, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, '/home/claude/w/inj')
import bpy, numpy as np
import kit as K, imats, irig
import pgeo as G
from kit import srgb

K.init(empty=True); scn = K.scn
M = {}
MT = imats.metal
M['brass'] = MT('brass', 0xc8a24e, 0.3)
M['coatBlack'] = MT('coatBlack', 0x1b2028, 0.34, metal=0.4, coat=0.5, bump=(2.0, 0.04, 0.1))
M['zincW'] = MT('zincW', 0xc9ced6, 0.32, bump=(3, 0.06, 0.12))
M['zinc'] = MT('zinc', 0xb9bec6, 0.34, bump=(3, 0.06, 0.12))
M['plasticBlack'] = MT('plasticBlack', 0x17181b, 0.45, metal=0.0, coat=0.2, bump=(6, 0.05))
M['plasticCap'] = MT('plasticCap', 0x2c3038, 0.5, metal=0.0)
M['paper'] = MT('paper', 0xe6dcc2, 0.92, metal=0.0, bump=(3.5, 0.5))
M['sealGreen'] = MT('sealGreen', 0x2f9a58, 0.6, metal=0.0)
M['steelPol'] = MT('steelPol', 0xdfe2e6, 0.13)
M['steel'] = MT('steel', 0xb7bcc2, 0.30)
M['steelDark'] = MT('steelDark', 0x4a4e55, 0.4)
M['plasticNat'] = MT('plasticNat', 0xd9d6c8, 0.5, metal=0.0, coat=0.15)
M['mesh'] = MT('mesh', 0x9aa0a6, 0.6, metal=0.6, bump=(30, 0.5))
M['wireBrown'] = MT('wireBrown', 0x6b4a2a, 0.5, metal=0.0)
M['wireRed'] = MT('wireRed', 0xb3261e, 0.5, metal=0.0)
M['floatBlack'] = MT('floatBlack', 0x18191b, 0.7, metal=0.0, bump=(8, 0.3))
M['copper'] = MT('copper', 0xc8794a, 0.3)
M['railSteel'] = MT('railSteel', 0x8e949c, 0.4, bump=(4, 0.1, 0.15))
M['clipBlue'] = MT('clipBlue', 0x1e6fd6, 0.45, metal=0.0, coat=0.2)
M['secCoat'] = G.sec3('secCoat', 0x9aa0a8, 2.0, 0.25, -1)
M['secPlastic'] = G.sec3('secPlastic', 0x3d4148, 1.6, 0.0, 1, k=0.9, plain=True, metal=0.0, rough=0.7)
M['secPaper'] = G.sec3('secPaper', 0xefe5cb, 1.5, 0.18, 1, k=0.8, metal=0.0, rough=0.9)
M['secNat'] = G.sec3('secNat', 0xcfccbd, 2.2, 0.16, -1, k=0.75, metal=0.0, rough=0.6)
M['fuel'] = imats.liquid('fuelLP', imats.C_LP, 0.9)
M['fuelCore'] = imats.liquid('fuelCore', imats.C_LP, 0.9)
for m in M.values(): m.use_fake_user = True

def grp(name, loc=(0, 0, 0)):
    e = K.empty(name); e.rotation_euler = (math.pi / 2, 0, 0); e.location = loc; return e

FLT = grp('FLT')
for n in ['flt.body', 'flt.lid', 'flt.screws', 'flt.cart']: G.part(n, FLT, M)
fo = G.part('flt.fuelOut', FLT, M, oname='fltOut'); fc = G.part('flt.fuelCore', FLT, M, over={'fuel': M['fuelCore']}, oname='fltCore'); fa = G.part('flt.fuelAll', FLT, M, oname='fltAll')
TM = grp('TM')
for n in ['tm.flange', 'tm.rods', 'tm.springs', 'tm.pot', 'tm.pump', 'tm.plumbing', 'tm.sender']: G.part(n, TM, M)
tf = G.part('tm.fuelPot', TM, M, oname='tmFuel')
INJ = grp('INJ'); G.part('inj', INJ, M)
RAIL = grp('RAIL'); G.part('rail', RAIL, M)
QUICK = grp('QUICK'); G.part('quick', QUICK, M)
UNUT = grp('UNUT'); G.part('unut', UNUT, M)
for f in (fo, fc, fa, tf):
    for c in f.children: c.visible_shadow = False
for g in (fa, TM, INJ, RAIL, QUICK, UNUT):
    g.hide_render = True
    for c in g.children_recursive: c.hide_render = True

irig.setup_world(0.3); irig.setup_camera(); irig.setup_render(1080, 1920, 32, 0.0)
bp = os.path.join(HERE, 'blend', 'aux.blend')
bpy.ops.wm.save_as_mainfile(filepath=bp); bpy.ops.file.pack_all(); bpy.ops.wm.save_as_mainfile(filepath=bp, compress=True)
print('SAVED', bp, len(bpy.data.objects), 'objects')
