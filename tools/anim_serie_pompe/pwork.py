# Statiile atelierului pentru seria pompelor (desene schematice ale mele, nu utilajele reale din atelier):
#   mic   = pompa desfacuta, sub microscopul stereo           -> blend/wk_mic.blend   (din pump.blend)
#   usb   = baia cu ultrasunete, cu piesele in cos            -> blend/wk_usb.blend   (din pump.blend)
#   bench = bancul de proba pentru pompe, cu pompa montata    -> blend/wk_bench.blend (din pump.blend)
#   inj   = standul de injectoare                             -> blend/wk_inj.blend   (din aux.blend)
#   venv_bpy/bin/python pwork.py mic usb bench inj
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, '/home/claude/w/inj')
import bpy, numpy as np
import kit as K, imats, irig
import pshots as S, pkin
from kit import srgb
PI = math.pi
H0 = pkin.state(S.PHI0)['h']          # inaltimea tachetului in placile fixe

def tree(o, v):
    o.hide_render = v
    for c in o.children_recursive:
        c.hide_render = True if c.name.startswith(('d_', 'x_')) or any(p.name.startswith(('d_', 'x_')) for p in parents(c)) else v
def parents(o):
    r = []
    while o.parent is not None: o = o.parent; r.append(o)
    return r

def mats():
    M = {}; mt = imats.metal
    M['paint'] = mt('wkPaint', 0x1f5a94, 0.42, metal=0.25, coat=0.5, bump=(2.5, 0.03, 0.08))
    M['paintD'] = mt('wkPaintD', 0x262b33, 0.5, metal=0.3, coat=0.3, bump=(3, 0.03, 0.08))
    M['inox'] = mt('wkInox', 0xcdd2d8, 0.26, bump=(2.0, 0.03, 0.1))
    M['inoxD'] = mt('wkInoxD', 0x8d949c, 0.34, bump=(2.0, 0.04, 0.1))
    M['black'] = mt('wkBlack', 0x15171a, 0.55, metal=0.0, coat=0.15, bump=(8, 0.05))
    M['white'] = mt('wkWhite', 0xe7eaee, 0.38, metal=0.0, coat=0.35)
    M['mat'] = mt('wkMat', 0x1d4a48, 0.85, metal=0.0, bump=(14, 0.08))
    M['top'] = mt('wkTop', 0x4a5059, 0.5, metal=0.5, bump=(2.0, 0.04, 0.12))
    M['yellow'] = mt('wkYellow', 0xffd21f, 0.45, metal=0.0, coat=0.3)
    M['red'] = mt('wkRed', 0xe5302a, 0.45, metal=0.0, coat=0.3)
    M['dial'] = mt('wkDial', 0xf4f4f0, 0.6, metal=0.0)
    M['glass'] = imats.liquid('wkGlass', 0xcfe8f4, 0.16, emit=0.5)
    M['bath'] = imats.liquid('wkBath', 0x7fd0ea, 0.26, emit=0.7)
    M['fuel'] = imats.liquid('wkFuel', imats.C_LP, 0.9)
    def emis(name, col, s):
        m, N, L, b = imats._new(name); b.inputs['Base Color'].default_value = [0, 0, 0, 1]
        b.inputs['Emission Color'].default_value = srgb(col); b.inputs['Emission Strength'].default_value = s; b.inputs['Roughness'].default_value = 0.3
        return m
    M['screen'] = emis('wkScreen', 0x0d2c4a, 1.2); M['scrA'] = emis('wkScrA', 0x35d0ff, 2.2); M['scrB'] = emis('wkScrB', 0xffd21f, 2.2); M['scrG'] = emis('wkScrG', 0x3ddc84, 2.2)
    M['led'] = emis('wkLed', 0xffffff, 6.0)
    for m in M.values(): m.use_fake_user = True
    return M

def table(M, sx, sy, c=(0, 0), mat_on=True, name='wkTable'):
    g = K.empty(name)
    K.box(name + '.top', (sx, sy, 36), c=(c[0], c[1], -18), mat=M['top'], bev=5, parent=g)
    if mat_on: K.box(name + '.mat', (sx - 40, sy - 40, 3), c=(c[0], c[1], 1.5), mat=M['mat'], bev=1, parent=g)
    return g

def open_pump():
    bpy.ops.wm.open_mainfile(filepath=os.path.join(HERE, 'blend', 'pump.blend')); K.init(empty=False)
    D = bpy.data.objects
    for n in ['CUT', 'FULL', 'fCh', 'fCol', 'fIn', 'fLP', 'fOut', 'cp4.ports', 'cp4.zme', 'inSpring', 'inValve', 'outBall', 'outSpring', 'shaftDam',
              'shaft', 'tap', 'plunger', 'spring']: tree(D[n], True)
    return D

def hold(name, names, loc, rot, D, show=True, parent=None):
    """pune obiectele `names` sub un suport nou (pozitie si rotatie in reperul scenei, mm) si le arata"""
    h = K.empty(name, parent, loc, rot)
    for n in names:
        o = D[n]; o.parent = h
        if show: tree(o, False)
    return h

def spring_span(D):
    """intinderea arcului (y local) in pozitia placilor fixe"""
    sp = D['spring']; sp.data.shape_keys.key_blocks['B'].value = (H0 - pkin.HA) / (pkin.HB - pkin.HA)
    dg = bpy.context.evaluated_depsgraph_get(); dg.update(); ev = sp.evaluated_get(dg); me = ev.to_mesh()
    ys = [v.co.y for v in me.vertices]; rs = [math.hypot(v.co.x, v.co.z) for v in me.vertices]; ev.to_mesh_clear()
    return min(ys), max(ys), max(rs)

def save(name):
    irig.setup_world(0.3); irig.setup_camera(); irig.setup_render(1080, 1920, 32, 0.0)
    bp = os.path.join(HERE, 'blend', name + '.blend')
    bpy.ops.wm.save_as_mainfile(filepath=bp, compress=True); print('SAVED', bp, len(bpy.data.objects), 'objects', flush=True)

# ------------------------------------------------------------------ microscopul
def microscope(M, x, y, z0, parent):
    """microscop stereo: talpa, coloana, bloc de focalizare, corp cu obiectiv si lumina inelara, doua oculare. (x, y) = axa optica"""
    g = K.empty('wkMic', parent)
    K.box('mic.base', (200, 250, 20), c=(x, y + 38, z0 + 10), mat=M['white'], bev=6, parent=g)
    K.cyl('mic.stage', 50, 3, c=(x, y, z0 + 21.5), mat=M['black'], parent=g)
    K.cyl('mic.col', 15, 300, c=(x, y + 132, z0 + 20 + 150), mat=M['inox'], parent=g)
    K.cyl('mic.colcap', 17, 8, c=(x, y + 132, z0 + 324), mat=M['black'], parent=g)
    K.box('mic.block', (66, 84, 98), c=(x, y + 112, z0 + 212), mat=M['white'], bev=7, parent=g)
    for s in (-1, 1):
        K.cyl('mic.knob%d' % s, 21, 22, c=(x + s * 44, y + 112, z0 + 205), axis='X', mat=M['black'], bev=2, parent=g)
        K.cyl('mic.knobs%d' % s, 13, 12, c=(x + s * 60, y + 112, z0 + 205), axis='X', mat=M['inoxD'], bev=1.5, parent=g)
    K.box('mic.arm', (52, 96, 40), c=(x, y + 40, z0 + 228), mat=M['white'], bev=7, parent=g)
    K.cyl('mic.body', 37, 92, c=(x, y, z0 + 210), mat=M['white'], bev=5, parent=g)
    K.cyl('mic.zoom', 15, 92, c=(x, y, z0 + 214), axis='X', mat=M['black'], bev=2, parent=g)
    K.cyl('mic.obj', 27, 34, c=(x, y, z0 + 148), mat=M['black'], bev=2, parent=g)
    K.lathe('mic.ring', [(29, 0), (46, 0), (46, 15), (29, 15)], mat=M['black'], parent=g, loc=(x, y, z0 + 118))
    K.lathe('mic.led', [(32, -0.6), (43, -0.6), (43, 0.4), (32, 0.4)], mat=M['led'], parent=g, loc=(x, y, z0 + 118))
    K.box('mic.prism', (92, 62, 52), c=(x, y - 4, z0 + 276), mat=M['white'], bev=9, parent=g)
    for s in (-1, 1):
        a = (x + s * 20, y - 14, z0 + 292); b = (x + s * 27, y - 62, z0 + 352); c = (x + s * 28.4, y - 71.6, z0 + 364)
        K.rod('mic.eye%d' % s, a, b, 13.5, mat=M['black'], parent=g); K.rod('mic.cup%d' % s, b, c, 17, mat=M['black'], r2=18.5, parent=g)
    return g

def mk_mic():
    D = open_pump(); M = mats()
    table(M, 440, 440, (5, 20))
    mx, my = -45, 70
    microscope(M, mx, my, 3, None)
    zs = 3 + 23 + 12 + 12.5            # axa arborelui: masa, talpa cu placa, reazeme, fusul
    hold('hShaft', ['shaft', 'shaftDam'], (mx, my, zs), (PI / 2, 0, PI / 2), D); tree(D['shaftDam'], True)
    for yl in (-18.0, 27.0):
        K.box('wkVb%d' % int(yl), (12, 42, 12), c=(mx - yl, my, 3 + 23 + 6), mat=D['shaft'].children[0].data.materials[0] if False else M['inoxD'], bev=1)
    # piesele din fata: tachetul (cu rola in sus), pistonul si arcul culcate, corpul si capul pompei
    hold('hTap', ['tap'], (-125, -105, 3 + 19.5 + H0), (-PI / 2, 0, PI / 2), D)
    hold('hPl', ['plunger'], (-78 - H0, -118, 3 + 10.4), (0, 0, -PI / 2), D)
    y0, y1, r = spring_span(D)
    hold('hSp', ['spring'], (38 - y0, -118, 3 + r), (0, 0, -PI / 2), D)
    hold('hBody', ['cp4.housing', 'cp4.flange', 'cp4.fscrews', 'cp4.seal', 'cp4c.bushes'], (128, 62, 3 + 66.5), (PI / 2, 0, 0.5), D)
    hold('hHead', ['cp4.head', 'cp4.hbolts'], (118, -80, 3 - 41), (PI / 2, 0, -0.4), D)
    save('wk_mic')

# ------------------------------------------------------------------ baia cu ultrasunete
def mk_usb():
    D = open_pump(); M = mats()
    table(M, 400, 270, (0, 0), mat_on=False)
    g = K.empty('wkUsb')
    body = K.box('usb.body', (340, 210, 170), c=(0, 0, 85), mat=M['inox'], bev=7, parent=g)
    cut = K.box('usb.cut', (304, 174, 140), c=(0, 0, 112), parent=g); K.boolean(body, cut); K.shade(body, 40)
    K.box('usb.liq', (302, 172, 96), c=(0, 0, 90), mat=M['bath'], parent=g).visible_shadow = False
    # tabloul din fata: afisaj si doua butoane
    K.box('usb.panel', (150, 4, 62), c=(-70, -106.5, 62), mat=M['black'], bev=1, parent=g)
    K.box('usb.disp', (56, 2, 24), c=(-104, -109, 68), mat=M['scrA'], parent=g)
    for i, x in enumerate((-52, -22)):
        K.cyl('usb.knob%d' % i, 11, 12, c=(x, -113, 66), axis='Y', mat=M['inoxD'], bev=1.5, parent=g)
        K.box('usb.kn%d' % i, (2.2, 2, 9), c=(x, -119.6, 70), mat=M['yellow'], parent=g)
    K.box('usb.led', (8, 2, 8), c=(-124, -109, 44), mat=M['scrG'], parent=g)
    K.cyl('usb.drain', 9, 26, c=(170 + 12, 40, 34), axis='X', mat=M['inoxD'], parent=g)
    K.cyl('usb.tap', 5, 30, c=(170 + 20, 40, 52), mat=M['black'], parent=g)
    for s in (-1, 1): K.box('usb.foot%d' % s, (30, 180, 8), c=(s * 135, 0, 0), mat=M['black'], bev=2, parent=g)
    # cosul din sarma
    b = K.empty('usb.basket', g); zb = 52; zt = 152; bx, by = 138, 72
    for s in (-1, 1):
        K.rod('bk.l%d' % s, (-bx, s * by, zt), (bx, s * by, zt), 2.2, mat=M['inoxD'], parent=b)
        K.rod('bk.w%d' % s, (s * bx, -by, zt), (s * bx, by, zt), 2.2, mat=M['inoxD'], parent=b)
        for t in (-1, 1): K.rod('bk.c%d%d' % (s, t), (s * bx, t * by, zb), (s * bx, t * by, zt), 2.0, mat=M['inoxD'], parent=b)
        K.tube('bk.h%d' % s, [(s * bx, -34, zt), (s * (bx + 6), -34, zt + 34), (s * (bx + 6), 34, zt + 34), (s * bx, 34, zt)], 2.4, mat=M['inoxD'], fillet=10, parent=b)
    for i in range(15):
        x = -bx + i * (2 * bx / 14); K.rod('bk.x%d' % i, (x, -by, zb), (x, by, zb), 1.2, mat=M['inoxD'], seg=8, parent=b)
    for i in range(9):
        y = -by + i * (2 * by / 8); K.rod('bk.y%d' % i, (-bx, y, zb), (bx, y, zb), 1.2, mat=M['inoxD'], seg=8, parent=b)
    # piesele in cos: arborele culcat, tachetul, pistonul, arcul
    hold('hShaft', ['shaft', 'shaftDam'], (-58, 26, zb + 1.2 + 21), (PI / 2, 0, PI / 2), D, parent=b); tree(D['shaftDam'], True)
    hold('hTap', ['tap'], (70, 30, zb + 1.2 + 19.5 + H0), (-PI / 2, 0, PI / 2), D, parent=b)
    hold('hPl', ['plunger'], (-78 - H0, -36, zb + 1.2 + 10.4), (0, 0, -PI / 2), D, parent=b)
    y0, y1, r = spring_span(D)
    hold('hSp', ['spring'], (30 - y0, -36, zb + 1.2 + r), (0, 0, -PI / 2), D, parent=b)
    save('wk_usb')

# ------------------------------------------------------------------ bancul de proba pentru pompe
def gauge(M, c, r, parent, name='wkGauge', ang=0.6):
    """manometru cu cadran, cu fata spre -Y; ang = pozitia acului (0..1)"""
    g = K.empty(name, parent, loc=c)
    K.cyl(name + '.bezel', r, 26, c=(0, 0, 0), axis='Y', mat=M['black'], bev=3, parent=g)
    K.cyl(name + '.face', r - 6, 2, c=(0, -13.2, 0), axis='Y', mat=M['dial'], parent=g)
    for i in range(11):
        a = math.radians(225 - 270 * i / 10); rr = r - 14
        t = K.box(name + '.t%d' % i, (2.4 if i % 5 else 3.6, 1.2, 9 if i % 5 else 13), c=(rr * math.cos(a), -14.4, rr * math.sin(a)), mat=M['black'] if i < 8 else M['red'], parent=g)
        t.rotation_euler = (0, -(a - PI / 2), 0)
    a = math.radians(225 - 270 * ang); L = r - 20
    n = K.box(name + '.needle', (3.2, 1.6, L), c=(L / 2 * math.cos(a), -16, L / 2 * math.sin(a)), mat=M['red'], parent=g); n.rotation_euler = (0, -(a - PI / 2), 0)
    K.cyl(name + '.hub', 6, 5, c=(0, -16.5, 0), axis='Y', mat=M['black'], parent=g)
    return g

def monitor(M, c, w, h, parent, name='wkMon'):
    """monitor cu fata spre -Y: ecran luminos cu cateva bare si o curba din puncte"""
    g = K.empty(name, parent, loc=c)
    K.box(name + '.case', (w + 16, 16, h + 16), c=(0, 0, 0), mat=M['black'], bev=3, parent=g)
    K.box(name + '.scr', (w, 2, h), c=(0, -8.6, 0), mat=M['screen'], parent=g)
    for i in range(5):
        hh = h * (0.22 + 0.11 * i); K.box(name + '.b%d' % i, (w * 0.07, 1.2, hh), c=(-w * 0.38 + i * w * 0.11, -10, -h * 0.42 + hh / 2), mat=M['scrA'], parent=g)
    for i in range(3): K.box(name + '.r%d' % i, (w * 0.3, 1.2, h * 0.07), c=(w * 0.28, -10, h * 0.3 - i * h * 0.16), mat=M['scrB'] if i == 0 else M['scrG'], parent=g)
    return g

def mk_bench():
    D = open_pump(); M = mats()
    table(M, 380, 520, (0, 110), mat_on=False)
    ZP = 150.0
    hold('hPump', ['FULL', 'cp4.ports', 'cp4.zme', 'shaft'], (0, 0, ZP), (PI / 2, 0, PI), D)
    g = K.empty('wkBench')
    K.box('bn.drive', (250, 240, 262), c=(0, 222, 131), mat=M['paint'], bev=9, parent=g)
    K.box('bn.vent', (150, 3, 54), c=(0, 101, 42), mat=M['paintD'], parent=g)
    for i in range(6): K.box('bn.vs%d' % i, (140, 2, 3), c=(0, 99.4, 22 + i * 8), mat=M['black'], parent=g)
    K.cyl('bn.bell', 66, 64, c=(0, 67, ZP), axis='Y', mat=M['paintD'], bev=3, parent=g)
    K.cyl('bn.bellf', 74, 10, c=(0, 39.6, ZP), axis='Y', mat=M['inoxD'], bev=2, parent=g)
    K.box('bn.ped', (130, 58, ZP - 60), c=(0, 67, (ZP - 60) / 2), mat=M['paintD'], bev=4, parent=g)
    K.box('bn.stripe', (252, 4, 16), c=(0, 100.6, 236), mat=M['yellow'], parent=g)
    # turnul cu aparate: manometru si monitor
    K.box('bn.tower', (250, 50, 216), c=(0, 317, 370), mat=M['paint'], bev=8, parent=g)
    gauge(M, (-64, 280, 388), 50, g, ang=0.62)
    monitor(M, (54, 284, 390), 116, 84, g)
    K.box('bn.estop', (40, 6, 40), c=(-64, 290, 300), mat=M['yellow'], bev=2, parent=g)
    K.cyl('bn.estopb', 13, 14, c=(-64, 282, 300), axis='Y', mat=M['red'], bev=3, parent=g)
    # rampa de proba, pe doua suporturi, cu senzor si supapa
    zr = 296.0; yr = 150.0
    K.cyl('bn.rail', 13, 250, c=(10, yr, zr), axis='X', mat=M['inoxD'], bev=2, parent=g)
    for i, x in enumerate((-70, -20, 30, 80)):
        K.cyl('bn.rs%d' % i, 7.5, 16, c=(x, yr, zr + 19), mat=M['inoxD'], bev=1, parent=g); K.cyl('bn.rc%d' % i, 9, 9, c=(x, yr, zr + 30), mat=M['yellow'] if i else M['inox'], seg=6, parent=g)
    K.cyl('bn.sens', 10, 30, c=(150, yr, zr), axis='X', mat=M['inox'], seg=6, parent=g); K.box('bn.splug', (22, 20, 18), c=(174, yr, zr), mat=M['black'], bev=3, parent=g)
    K.cyl('bn.pcv', 11, 26, c=(-128, yr, zr), axis='X', mat=M['inox'], seg=6, parent=g)
    for i, x in enumerate((-95, 115)): K.box('bn.rb%d' % i, (14, 30, zr - 262), c=(x, yr, 262 + (zr - 262) / 2 - 6), mat=M['paintD'], bev=2, parent=g)
    # conducta de inalta presiune: de la racordul din capul pompei (in stanga, dupa rotire) pana la rampa
    hp = (-53.0, 0.0, ZP + 81.6)
    K.tube('bn.hp', [hp, (-86, 0, hp[2]), (-86, 0, 338), (-86, yr, 338), (-70, yr, 338), (-70, yr, zr + 34)], 3.3, mat=M['inox'], fillet=14, parent=g)
    K.cyl('bn.hpn', 8, 13, c=(-60, 0, hp[2]), axis='X', mat=M['inox'], seg=6, parent=g)
    # alimentarea si returul (furtunuri), cu un filtru al bancului
    K.tube('bn.lp1', [(-12, -70, ZP + 26), (-12, -100, ZP + 26), (120, -100, ZP + 26), (120, -100, 118)], 6.5, mat=M['black'], fillet=22, parent=g)
    K.tube('bn.lp2', [(14, -70, ZP + 10), (14, -112, ZP + 10), (14, -112, 6)], 6.5, mat=M['black'], fillet=22, parent=g)
    K.cyl('bn.flt', 30, 104, c=(120, -100, 58), mat=M['inox'], bev=4, parent=g); K.cyl('bn.fltc', 32, 16, c=(120, -100, 112), mat=M['paintD'], bev=3, parent=g)
    K.cyl('bn.grom', 12, 6, c=(14, -112, 3), mat=M['black'], parent=g)
    # cablul regulatorului de debit
    K.tube('bn.cab', [(-67, -28, ZP + 30), (-100, -28, ZP + 30), (-120, 20, 60), (-120, 96, 60)], 2.6, mat=M['black'], smooth_n=10, parent=g)
    save('wk_bench')

# ------------------------------------------------------------------ standul de injectoare
def mk_inj():
    bpy.ops.wm.open_mainfile(filepath=os.path.join(HERE, 'blend', 'aux.blend')); K.init(empty=False)
    D = bpy.data.objects; M = mats()
    for n in S.AUXG: tree(D[n], True)
    table(M, 320, 330, (0, 40), mat_on=False)
    ZI = 262.0                                   # varful duzei
    D['INJ'].location = (0, 0, ZI); tree(D['INJ'], False)
    g = K.empty('wkInj')
    K.box('ij.cab', (250, 230, 112), c=(0, 45, 56), mat=M['paint'], bev=8, parent=g)
    K.box('ij.stripe', (252, 4, 12), c=(0, -70.6, 96), mat=M['yellow'], parent=g)
    K.box('ij.col', (44, 44, 440), c=(0, 128, 112 + 220), mat=M['paintD'], bev=4, parent=g)
    K.box('ij.arm', (44, 150, 34), c=(0, 62, 520), mat=M['paintD'], bev=4, parent=g)
    K.box('ij.clampb', (52, 96, 30), c=(0, 80, ZI + 96), mat=M['paintD'], bev=3, parent=g)
    K.box('ij.clamp', (76, 44, 30), c=(0, 0, ZI + 96), mat=M['inoxD'], bev=3, parent=g)
    for s in (-1, 1): K.cyl('ij.cs%d' % s, 5, 36, c=(s * 28, -4, ZI + 96), axis='Y', mat=M['black'], seg=6, parent=g)
    # camera de pulverizare (sticla) si paharul gradat de dedesubt
    K.lathe('ij.cham', [(46, 0), (46, 128)], mat=M['glass'], parent=g, loc=(0, 0, ZI - 122), closed=False).visible_shadow = False
    K.cyl('ij.chtop', 50, 8, c=(0, 0, ZI + 10), mat=M['inoxD'], bev=2, parent=g)
    K.lathe('ij.fun', [(47, 0), (50, 0), (12, -30), (9, -30)], mat=M['inoxD'], parent=g, loc=(0, 0, ZI - 122))
    K.lathe('ij.glass', [(17, 0), (17, 40)], mat=M['glass'], parent=g, loc=(0, 0, 113), closed=False).visible_shadow = False
    K.cyl('ij.gfuel', 14.6, 15, c=(0, 0, 113 + 8), mat=M['fuel'], parent=g).visible_shadow = False
    K.cyl('ij.gbase', 22, 5, c=(0, 0, 114), mat=M['black'], parent=g)
    # conducta de inalta presiune, manometrul si monitorul
    K.tube('ij.hp', [(34, 0, ZI + 128), (62, 0, ZI + 156), (62, 0, 470), (62, 128, 470), (62, 128, 404)], 3.2, mat=M['inox'], fillet=16, parent=g)
    K.box('ij.pumpb', (62, 50, 66), c=(52, 128, 372), mat=M['paint'], bev=5, parent=g)
    gauge(M, (-78, 108, 420), 40, g, name='ijGauge', ang=0.7)
    K.box('ij.gb', (24, 30, 24), c=(-40, 122, 420), mat=M['paintD'], bev=3, parent=g)
    monitor(M, (-66, -62, 136), 84, 52, g, name='ijMon')
    save('wk_inj')

if __name__ == '__main__':
    for a in sys.argv[1:]:
        if a in ('mic', 'usb', 'bench', 'inj'): globals()['mk_' + a]()
