# Senzorul de presiune diferentiala cu furtunase, sondele de temperatura, sonda lambda, furtunurile de racire, joja, cablajul.
import bpy, bmesh, math
import numpy as np
from mathutils import Vector
import kit as K
from kit import S, pbr
from mats import MAT
import layout as L

def probe(name, p, n, hex_r=8.0, body_r=3.4, body_len=20.0, cable=None, cable_r=2.1, boss_r=9.0):
    """sonda insurubata intr-un mamelon sudat: p = punctul de pe tabla, n = normala spre exterior"""
    p = np.asarray(p, np.float64); n = L.nrm(n)
    K.rod(name + '.boss', p - n * 3, p + n * 7, boss_r, MAT['inoxS'], seg=24, bev=0.8)
    K.rod(name + '.hex', p + n * 7, p + n * 14, hex_r, MAT['zincW'], seg=6, bev=0.6)
    K.rod(name + '.body', p + n * 14, p + n * (14 + body_len), body_r, MAT['steel'], seg=16)
    K.rod(name + '.crimp', p + n * (12 + body_len), p + n * (20 + body_len), body_r + 1.0, MAT['steelDark'], seg=16)
    if cable is not None:
        pts = [tuple(p + n * (18 + body_len)), tuple(p + n * (40 + body_len))] + [tuple(c) for c in cable]
        K.tube(name + '.cable', pts, cable_r, MAT['wire'], seg=10, smooth_n=8)
    return p + n * (14 + body_len / 2)

def lambda_probe(name, p, n, cable):
    p = np.asarray(p, np.float64); n = L.nrm(n)
    K.rod(name + '.boss', p - n * 3, p + n * 8, 12.0, MAT['inoxS'], seg=28, bev=0.8)
    K.rod(name + '.hex', p + n * 8, p + n * 17, 11.5, MAT['zincW'], seg=6, bev=0.7)
    K.rod(name + '.body', p + n * 17, p + n * 46, 8.2, MAT['steel'], seg=24, bev=0.8)
    K.rod(name + '.cap', p + n * 46, p + n * 60, 6.6, MAT['steelDark'], seg=24, bev=1.0)
    K.rod(name + '.boot', p + n * 58, p + n * 72, 4.6, MAT['rubber'], seg=16, r2=3.2)
    pts = [tuple(p + n * 70), tuple(p + n * 92)] + [tuple(c) for c in cable]
    K.tube(name + '.cable', pts, 2.8, MAT['wire'], seg=10, smooth_n=8)
    return p + n * 34

def build():
    O = {}
    MAT['yellow'] = pbr('yellow', 0xe2a614, 0.0, 0.4, coat=0.3)
    # ---------------- senzorul de presiune diferentiala (pe suport, sus langa carcasa)
    D = L.DPS
    K.box('dps.bracket', (3.0, 40, 96), c=(D[0] + 10.5, D[1], D[2] - 22), mat=MAT['steel'], bev=0.8)
    K.box('dps.foot', (26, 34, 3.0), c=(D[0] + 22, D[1], D[2] - 69), mat=MAT['steel'], bev=0.8)
    K.rod('dps.fbolt', (D[0] + 26, D[1], D[2] - 74), (D[0] + 26, D[1], D[2] - 62), 5.5, MAT['zincW'], seg=6)
    body = K.box('dps.body', (17, 46, 30), c=(D[0], D[1], D[2]), mat=MAT['plasticBlack'], bev=3.0, seg=3)
    K.cyl('dps.dome', 13.5, 5, c=(D[0] - 9.5, D[1], D[2]), axis='X', mat=MAT['plasticBlack'], seg=40, bev=1.5)
    K.box('dps.conn', (15, 21, 22), c=(D[0], D[1], D[2] + 25), mat=MAT['connGrey'], bev=3.0, seg=3)
    K.box('dps.lock', (17, 10, 6), c=(D[0], D[1], D[2] + 31), mat=MAT['plasticGrey'], bev=1.5)
    K.rod('dps.screw', (D[0] + 6, D[1], D[2] - 6), (D[0] + 14, D[1], D[2] - 6), 4.6, MAT['zincW'], seg=6)
    nip = []
    for s in (-1, 1):
        a = np.array([D[0], D[1] + s * 12.0, D[2] - 15.0]); b = a - np.array([0, 0, 15.0])
        K.rod('dps.nip', a, b, 3.4, MAT['plasticBlack'], seg=16)
        K.lathe('dps.barb', [(3.4, -1.6), (4.4, 0), (3.4, 1.6)], seg=16, mat=MAT['plasticBlack'], loc=tuple(b + np.array([0, 0, 3.0])))
        nip.append(b)
    # tevi de otel sudate pe carcasa + furtunase de cauciuc pana la senzor
    PH = 122.0
    b1 = L.mpol(L.SHELL_R2, PH, 113.0); n1 = L.mdir(PH)            # priza dinaintea filtrului
    b2 = L.mpol(L.SHELL_R2, PH - 14, L.MOD_END - 9.0); n2 = L.mdir(PH - 14)   # priza de dupa filtru
    for nm, b, n in (('dps.boss1', b1, n1), ('dps.boss2', b2, n2)):
        K.rod(nm, b - n * 2, b + n * 8, 6.5, MAT['inoxS'], seg=20, bev=0.8)
        K.rod(nm + 'n', b + n * 8, b + n * 14, 6.2, MAT['zincW'], seg=6)
    t1 = [tuple(b1 + n1 * 14), tuple(b1 + n1 * 30), tuple(b1 + n1 * 34 - L.MD * 40), tuple(nip[0] + np.array([4.0, -4.0, -82.0])), tuple(nip[0] + np.array([0, 0, -52.0]))]
    t2 = [tuple(b2 + n2 * 14), tuple(b2 + n2 * 30), tuple(b2 + n2 * 36 - L.MD * 60), tuple(L.mpol(L.SHELL_R2 + 40, PH + 6, 60.0)), tuple(nip[1] + np.array([-6.0, 6.0, -92.0])), tuple(nip[1] + np.array([0, 0, -56.0]))]
    K.tube('dps.tube1', t1, 3.1, MAT['steel'], seg=14, fillet=16)
    K.tube('dps.tube2', t2, 3.1, MAT['steel'], seg=14, fillet=16)
    h1 = [tuple(nip[0] + np.array([0, 0, -58.0])), tuple(nip[0] + np.array([0.5, -1.5, -36.0])), tuple(nip[0] + np.array([0, -1.0, -16.0])), tuple(nip[0] + np.array([0, 0, 5.0]))]
    h2 = [tuple(nip[1] + np.array([0, 0, -62.0])), tuple(nip[1] + np.array([-1.0, 1.5, -38.0])), tuple(nip[1] + np.array([0, 1.0, -16.0])), tuple(nip[1] + np.array([0, 0, 5.0]))]
    H1 = K.catmull(h1, 10); H2 = K.catmull(h2, 10)
    K.obj('dps.hose1', K.tube_mesh('dps.hose1', H1, 5.4, seg=20), MAT['rubberHose'])
    K.obj('dps.hose2', K.tube_mesh('dps.hose2', H2, 5.4, seg=20), MAT['rubberHose'])
    for nm, H in (('dps.cl1', H1), ('dps.cl2', H2)):
        K.tube(nm + 'a', [tuple(H[2]), tuple(H[4])], 6.1, MAT['clamp'], seg=20, r_in=5.3)
    # fisura in furtun (apare in capitolul cu senzorul)
    k = len(H1) // 2; c = H1[k]; d = L.nrm(H1[k + 1] - H1[k - 1])
    side = L.nrm(np.cross(d, np.array([1.0, 0, 0]))); out = L.nrm(np.cross(side, d))
    out = np.array([0.35, -0.93, 0.0]); out = L.nrm(out - d * (out @ d)); side = np.cross(d, out)
    cr = [tuple(c + out * 5.45 + d * (-7 + 2.0 * i) + side * (1.3 * math.sin(i * 1.9))) for i in range(8)]
    O['hose_crack'] = K.tube('dps.crack', cr, 0.55, MAT['crack'], seg=8)
    O['hose_crack_pos'] = (c + out * 6.0).tolist(); O['hose_crack_dir'] = out.tolist()
    O['dps_pos'] = D.tolist(); O['dps_b1'] = b1.tolist(); O['dps_b2'] = b2.tolist()
    O['dps_tube1'] = np.vstack([np.array(t1[::-1]), H1[1:]]).tolist(); O['dps_tube2'] = np.vstack([np.array(t2[::-1]), H2[1:]]).tolist()
    # ---------------- sonde de temperatura si sonda lambda, cu cabluri catre cablajul motorului
    hz = 396.0
    O['egt1'] = probe('egt1', (-86.0, -238.0, 284.5), (0.0, -0.78, 0.62), cable=[(-92, -250, 350), (-100, -190, 392), (-104, -132, hz)]).tolist()
    O['lam'] = lambda_probe('lam', (-104.0, -214.0, 296.5), (0.05, 0.1, 1.0), cable=[(-112, -196, 384), (-118, -140, hz + 4), (-122, -128, hz)]).tolist()
    pe = L.mpol(L.SHELL_R2, -42.0, 111.0); ne = L.mdir(-42.0)
    O['egt2'] = probe('egt2', pe, ne, cable=[tuple(pe + ne * 70 + np.array([0, 0, 60])), (-40, -235, 330), (-52, -150, 392), (-56, -130, hz)]).tolist()
    pe = L.mpol(L.SHELL_R2, -42.0, L.MOD_END - 8.0); ne = L.mdir(-42.0)
    O['egt3'] = probe('egt3', pe, ne, cable=[tuple(pe + ne * 60 + np.array([0, 0, 40])), (-88, -300, 60), (-96, -292, 200), (-150, -262, 345), (-170, -150, 394), (-172, -130, hz)]).tolist()
    # cablajul (tub riflat) pe marginea din spate a chiulasei
    hp = K.catmull([(-240, -122, hz - 6), (-180, -127, hz), (-60, -128, hz), (60, -127, hz), (118, -124, hz - 4)], 12)
    t = path_t = np.linspace(0, 1, len(hp))
    hr = 8.0 + 0.55 * np.sin(np.arange(len(hp)) * 2.4)
    K.obj('harness', K.tube_mesh('harness', K.resample(hp, 260), 8.0 + 0.6 * np.sin(np.arange(260) * 1.9), seg=16), MAT['plasticBlack'])
    for x in (-150, -20, 90):
        K.box('harness.clip', (10, 8, 22), c=(x, -121, hz - 4), mat=MAT['plasticGrey'], bev=1.5)
    # ---------------- lichidul de racire: teava rigida pe bloc + furtunurile racitorului EGR
    C = L.COOL_C; hx = L.COOL_S[0] / 2
    a = (C[0] + hx + 20, C[1] + 22, C[2] + 50); b = (C[0] + hx + 20, C[1] + 22, C[2] - 50)
    ha = K.catmull([a, (a[0] + 22, a[1] + 3, a[2] + 6), (22, -192, 98), (30, -146, 117), (30, -124, 120)], 10)
    hb = K.catmull([b, (b[0] + 24, b[1] + 5, b[2] + 5), (30, -184, 6), (40, -146, 38), (40, -126, 45)], 10)
    K.obj('cool.hoseA', K.tube_mesh('cool.hoseA', ha, 10.5, seg=24), MAT['rubberHose'])
    K.obj('cool.hoseB', K.tube_mesh('cool.hoseB', hb, 10.5, seg=24), MAT['rubberHose'])
    for nm, H in (('cool.clA', ha), ('cool.clB', hb)):
        K.tube(nm + '1', [tuple(H[1]), tuple(H[3])], 11.4, MAT['clamp'], seg=24, r_in=10.4)
        K.tube(nm + '2', [tuple(H[-4]), tuple(H[-2])], 11.4, MAT['clamp'], seg=24, r_in=10.4)
    K.tube('cool.pipe', [(30, -122, 120), (-40, -122, 120), (-120, -122, 120), (-150, -122, 70), (-150, -122, 62)], 8.5, MAT['steel'], seg=20, fillet=22)
    O['hoseA'] = ha.tolist(); O['hoseB'] = hb.tolist()
    # ---------------- joja de ulei
    dp = K.catmull([(-64, -131, -98), (-64, -134, -30), (-70, -137, 110), (-84, -141, 300), (-97, -152, 436)], 10)
    K.obj('dip.tube', K.tube_mesh('dip.tube', dp, 4.0, seg=14), MAT['steel'])
    top = dp[-1]; dd = L.nrm(dp[-1] - dp[-2])
    K.rod('dip.plug', top, top + dd * 14, 6.0, MAT['yellow'], seg=20, bev=1.0)
    ring = [tuple(top + dd * 26 + np.array([12 * math.cos(t), 0.0, 12 * math.sin(t)])) for t in np.linspace(0, 2 * np.pi, 33)]
    K.obj('dip.ring', K.tube_mesh('dip.ring', np.array(ring), 2.6, seg=12), MAT['yellow'])
    return O
