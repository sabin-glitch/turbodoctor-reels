# Motorul 2.0 TDI (simplificat, dar la scara): bloc, chiulasa, capac, baie; cilindrul 1 in sectiune (plan X = SEC_X).
import bpy, bmesh, math, json, os
import numpy as np
from mathutils import Vector, Matrix
import kit as K
from kit import S
from mats import MAT
import layout as L

SX = L.SEC_X
XB = 90.0          # de aici pana la SX piesele sunt modelate fin (zona sectiunii)
XMIN = -216.0

def two_piece(name, f, ymin, ymax, zmin, zmax, mat, secmat, v_main=1.7, v_bay=0.85, xmin=XMIN, planar=None):
    a = K.sdf_obj(name + '.a', f, (xmin, ymin, zmin), (XB, ymax, zmax), v_main, mat, planar=planar)
    b = K.sdf_obj(name + '.b', f, (XB, ymin, zmin), (SX, ymax, zmax), v_bay, [mat, secmat], sec=[(0, SX)])
    return a, b

def f_block():
    body = S.su(16.0,
                S.box((-20, 0, -6), (182, 124, 86), 14),
                S.box((-20, 0, 160), (180, L.BLOCK_Y, 86), 12))
    ribs = [S.box((xr, -L.BLOCK_Y - 1, 152), (5, 7, 76), 3) for xr in (88, 0, -88, -172)]
    ribs += [S.box((xr, L.BLOCK_Y + 1, 152), (5, 7, 76), 3) for xr in (88, 0, -88, -172)]
    ribs += [S.box((-20, -L.BLOCK_Y - 1, 112), (172, 6, 5), 3), S.box((-20, -L.BLOCK_Y - 1, 196), (172, 5, 4), 2.5)]
    bell = S.i(S.cyl(0, (-207, 0, 6), 186, 8, 3), S.plane((0, 0, 1), 224))
    rail = S.box((-20, 0, -88), (184, 132, 7), 4)
    bosses = [S.cyl(1, (55, -124, 58), 14, 9, 3), S.cyl(1, (-150, -124, 62), 15, 9, 3), S.cyl(1, (-150, -124, -20), 15, 9, 3),
              S.cyl(1, (30, -112, 120), 13, 9, 3), S.cyl(1, (40, -124, 45), 12, 9, 3), S.cyl(1, (60, -112, 200), 10, 8, 3)]
    f = S.su(7.0, body, *ribs, bell, rail, *bosses)
    f = S.i(f, S.plane((0, 0, 1), L.DECK))
    # goluri vizibile in sectiune (cilindrul 1)
    bore = S.cyl(2, (SX, 0, 150), L.BORE / 2, 95)
    room = S.su(10.0, S.cyl(0, (SX, 0, 0), 92, 40), S.box((SX, 0, -62), (40, 104, 40), 8))
    jacket = S.d(S.cyl(2, (SX, 0, 170), 57.5, 60, 4), S.cyl(2, (SX, 0, 170), 47.5, 80))
    gal = S.cyl(0, (SX, -86, 96), 5.5, 60)
    f = S.d(f, S.u(bore, room, jacket, gal))
    return f

def f_head():
    body = S.box((-20, 0, 300), (180, L.HEAD_Y, 72), 8)
    pads = [S.box((x, -L.HEAD_Y - 2, L.PORT_Z), (31, 6, 25), 4) for x in L.CYL_X] + [S.box((x, L.HEAD_Y + 2, L.PORT_Z), (31, 6, 25), 4) for x in L.CYL_X]
    f = S.su(5.0, body, *pads)
    f = S.i(f, S.plane((0, 0, -1), -L.DECK))
    f = S.i(f, S.plane((0, 0, 1), L.HEAD_TOP))
    cam = S.box((SX, 0, 366), (45, 99, 19), 5)
    exh = S.path(K.catmull([(SX, -25, 232), (SX, -25.5, 252), (SX, -35, 277), (SX, -62, 296), (SX, -94, 301), (SX, -130, 302)], 8), 13.5)
    inl = S.path(K.catmull([(SX, 25, 232), (SX, 25.5, 252), (SX, 35, 277), (SX, 62, 296), (SX, 94, 301), (SX, 130, 302)], 8), 14.0)
    seats = S.u(S.cone((SX, -25, 236), (SX, -25, 244), 15.0, 13.0), S.cone((SX, 25, 236), (SX, 25, 244), 15.0, 13.5))
    pockets = S.u(S.cyl(2, (SX, -25, 334), 14.5, 20, 2), S.cyl(2, (SX, 25, 334), 14.5, 20, 2))
    stems = S.u(S.cyl(2, (SX, -25, 300), 3.6, 60), S.cyl(2, (SX, 25, 300), 3.6, 60))
    inj = S.u(S.cyl(2, (SX, 0, 300), 9.9, 60), S.cyl(2, (SX, 0, 246), 4.6, 12))
    water = S.u(S.box((SX, -72, 260), (30, 14, 8), 6), S.box((SX, 72, 260), (30, 14, 8), 6),
                S.box((SX, -82, 330), (30, 12, 9), 6), S.box((SX, 82, 330), (30, 12, 9), 6))
    f = S.d(f, S.u(cam, exh, inl, seats, pockets, stems, inj, water))
    return f

def f_cover():
    body = S.su(9.0, S.box((-20, 0, 396), (180, 110, 28), 15),
                S.box((-40, -52, 414), (130, 26, 14), 9),
                S.box((-40, 52, 414), (130, 26, 14), 9),
                S.cyl(2, (-78, 0, 428), 25, 9, 3))
    f = S.i(body, S.plane((0, 0, -1), -(L.HEAD_TOP + 0.6)))
    f = S.d(f, S.box((SX, 0, 392), (62, 99, 23), 10))
    return f

def f_pan():
    body = S.su(12.0, S.box((-20, 0, -112), (180, 128, 17), 7),
                S.box((-20, 0, -160), (180, 112, 48), 24))
    ribs = [S.box((x, -113, -162), (4, 7, 38), 3) for x in (-150, -100, -50, 0, 50)]
    f = S.su(6.0, body, *ribs, S.cyl(1, (-64, -116, -188), 13, 8, 3))
    f = S.i(f, S.plane((0, 0, 1), -95.5))
    f = S.d(f, S.box((SX, 0, -148), (62, 102, 52), 18))
    return f

def geo_part(name, parent, MATMAP, GJ, GB):
    out = []
    for p in GJ:
        if p['n'] != name: continue
        o, v = p['o'], p['v']; b = p['b']
        pq = np.frombuffer(GB, np.uint16, v * 3, o).reshape(-1, 3).astype(np.float64)
        pos = np.array(b[:3]) + pq * np.array(b[3:])
        o2 = o + ((v * 6 + 3) & ~3)
        if p.get('h'): nq = np.frombuffer(GB, np.int16, v * 4, o2).reshape(-1, 4)[:, :3] / 32767.0; o3 = o2 + v * 8
        else: nq = np.frombuffer(GB, np.int8, v * 4, o2).reshape(-1, 4)[:, :3] / 127.0; o3 = o2 + v * 4
        idx = np.frombuffer(GB, np.uint16 if p['w'] == 2 else np.uint32, p['i'], o3).reshape(-1, 3)
        # three.js (Y sus) -> Blender (Z sus)
        P = np.stack([pos[:, 0], -pos[:, 2], pos[:, 1]], axis=1)
        me = K.mesh_np(name + '.' + p['m'], P, idx.astype(np.int32), smooth=True, sharp=40)
        ob = K.obj(me.name, me, MATMAP.get(p['m'], MAT['steel']), parent)
        out.append(ob)
    return out

def helix(name, r, wire, turns, length, mat, parent, per=28, rad=10):
    n = int(turns * per) + 1
    k = np.linspace(0, turns, n); a = k * 2 * np.pi
    z = wire / 2 + (length - wire) * k / turns
    P = np.stack([r * np.cos(a), r * np.sin(a), z], axis=1)
    me = K.tube_mesh(name, P, wire / 2, seg=rad, caps=True)
    return K.obj(name, me, mat, parent)

def build(src):
    O = {}
    # ---------------- piesele mari turnate
    two_piece('eng.block', f_block(), -146, 146, -98, L.DECK, MAT['blockIron'], MAT['secIron'])
    two_piece('eng.head', f_head(), -128, 128, L.DECK, L.HEAD_TOP, MAT['headAlu'], MAT['secAlu'])
    two_piece('eng.cover', f_cover(), -116, 116, L.HEAD_TOP + 0.6, 442, MAT['plasticBlack'], MAT['secDark'])
    two_piece('eng.pan', f_pan(), -134, 134, -212, -95.5, MAT['castAlu'], MAT['secAlu'])
    # garnitura de chiulasa
    g = K.box('eng.gasket', (332, 2 * L.BLOCK_Y + 4, 1.6), c=(-34, 0, L.DECK), mat=MAT['gasket'])
    c = K.cyl('cutg', 41.5, 10, c=(SX, 0, L.DECK), mat=MAT['gasket'], seg=64)
    K.boolean(g, c)
    # dopuri de turnare pe spatele blocului, busonul de ulei, capacul de umplere
    for x in (44, -44, -132):
        K.cyl('eng.plug', 17, 5, c=(x, -L.BLOCK_Y - 1.5, 150), axis='Y', mat=MAT['zincW'], seg=40, bev=1.5)
    K.cyl('eng.drain', 9, 9, c=(-64, -127, -188), axis='Y', mat=MAT['zincW'], seg=6, bev=0.8)
    cap = K.lathe('eng.oilcap', [(0.01, 0), (26, 0), (29, 3), (29, 12), (25, 16), (0.01, 16)], seg=48, mat=MAT['plasticBlack'], loc=(-78, 0, 436))
    for i in range(12):
        a = i * math.pi / 6
        K.box('eng.oilcap.r', (5, 3.2, 12), c=(-78 + 29 * math.cos(a), 29 * math.sin(a), 443), mat=MAT['plasticBlack'], bev=1.0).rotation_euler = (0, 0, a)
    # baia de ulei: uleiul vizibil in sectiune
    K.box('eng.oil', (SX - 96, 196, 42), c=((SX + 96) / 2 - 0.3, 0, -178), mat=MAT['oilLiq'], bev=3.0)

    # ---------------- arborele cotit (portiunea cilindrului 1): se roteste in jurul axei X
    CR = K.empty('CRANK'); O['CRANK'] = CR
    r = L.STROKE / 2
    web = S.su(6.0,
               S.i(S.capsule((111.5, 0, -4), (111.5, 0, r), 31.0), S.cyl(0, (111.5, 0, 0), 200, 7.5, 2)),
               S.i(S.cyl(0, (111.5, 0, 0), 78, 7.5, 2), S.plane((0, 0, 1), -14.0), S.plane((0, 0.94, 0.34), 30.0), S.plane((0, -0.94, 0.34), 30.0)))
    K.sdf_obj('crank.web', web, (100, -84, -84), (123, 84, 84), 0.9, MAT['steelDark'], parent=CR)
    K.cyl('crank.main', 27, 44, c=(84, 0, 0), axis='X', mat=MAT['steelPol'], seg=64, bev=1.2, parent=CR)
    K.cyl('crank.pin', 24, 28, c=(SX, 0, r), axis='X', mat=MAT['steelPol'], seg=64, bev=1.2, parent=CR)
    K.cyl('crank.oilh', 3, 2, c=(SX, 0, r + 24), axis='Z', mat=MAT['crack'], seg=16, parent=CR)

    # ---------------- biela (origine in centrul capului mare, +Z spre bolt)
    RD = K.empty('ROD'); O['ROD'] = RD
    R = L.ROD
    rod = S.su(7.0, S.cyl(0, (0, 0, 0), 34, 11, 2), S.cyl(0, (0, 0, R), 18.5, 11, 2), S.box((0, 0, R / 2), (7.0, 11.5, R / 2 - 18), 3))
    rod = S.d(rod, S.u(S.cyl(0, (0, 0, 0), 24.2, 30), S.cyl(0, (0, 0, R), 13.1, 30),
                       S.box((9.5, 0, R / 2 + 4), (4.5, 6.0, R / 2 - 44), 3), S.box((-9.5, 0, R / 2 + 4), (4.5, 6.0, R / 2 - 44), 3)))
    K.sdf_obj('rod.body', rod, (-12.5, -36, -36), (12.5, 36, R + 20), 0.8, MAT['steelDark'], parent=RD)
    for s in (-1, 1):
        K.cyl('rod.bolt', 4.2, 6, c=(0, 29 * s, -20), axis='Z', mat=MAT['zincW'], seg=6, parent=RD)

    # ---------------- pistonul (jumatate, ca sa se vada camera de ardere din capul pistonului)
    PS = K.empty('PISTON'); O['PISTON'] = PS
    prof = [(40.25, -28), (40.25, 22.6), (37.2, 22.6), (37.2, 26), (40.25, 26), (40.25, 29.6), (37.2, 29.6), (37.2, 32), (40.25, 32),
            (40.25, 35.4), (37.2, 35.4), (37.2, 38), (40.25, 38), (40.25, 44), (39.4, 45), (27.5, 45), (26.6, 43.5), (29.6, 37.0),
            (28.6, 32.4), (24.0, 30.2), (14.0, 31.4), (0.02, 38.6), (0.02, 24.5), (20, 24.5), (31, 14), (34.2, -28)]
    K.lathe('piston.body', prof, seg=96, mat=MAT['machAlu'], parent=PS, deg=180, a0=90, sharp=28)
    for (z0, z1, m) in ((35.6, 37.8, 'steelDark'), (29.8, 31.8, 'steelDark'), (22.9, 25.7, 'steel')):
        K.lathe('piston.ring', [(37.4, z0), (40.55, z0), (40.55, z1), (37.4, z1)], seg=96, mat=MAT[m], parent=PS, deg=180, a0=90, sharp=28)
    K.lathe('piston.pin', [(8, -31), (13, -31), (13, 31), (8, 31)], seg=48, mat=MAT['steelPol'], parent=PS, axis='X', sharp=30)

    # ---------------- supape, arcuri, came
    vprof = [(0.02, 0), (12.6, 0), (13.4, 1.2), (13.4, 2.4), (6.2, 9.5), (3.4, 20), (3.0, 34), (3.0, 112), (0.02, 112)]
    for nm, y in (('VEX', -25.0), ('VIN', 25.0)):
        V = K.empty(nm, loc=(SX, y, L.DECK + 0.6)); O[nm] = V
        K.lathe(nm + '.valve', vprof, seg=48, mat=MAT['steel'], parent=V, sharp=30)
        K.lathe(nm + '.ret', [(3.0, 100), (12.5, 100), (12.5, 103), (6, 106), (3.0, 106)], seg=40, mat=MAT['steelDark'], parent=V, sharp=30)
        SP = K.empty(nm + '.SPR', loc=(SX, y, 315.5)); O[nm + '.SPR'] = SP
        helix(nm + '.spring', 9.6, 2.6, 5.5, 22.0 + 0.0, MAT['steelPol'], SP)
        C = K.empty(nm + '.CAM', loc=(SX, y, 363.0)); O[nm + '.CAM'] = C
        K.cyl(nm + '.shaft', 10.0, 86, c=(-20, 0, 0), axis='X', mat=MAT['steel'], seg=40, parent=C)
        lobe = S.su(3.0, S.cyl(0, (0, 0, 0), 13.0, 8, 1.5), S.cyl(0, (0, 0, -12.0), 8.0, 8, 1.5), S.cyl(0, (0, 0, -6.0), 10.6, 8, 1.5))
        K.sdf_obj(nm + '.lobe', lobe, (-9.5, -16, -22), (9.5, 16, 15), 0.6, MAT['steelPol'], parent=C)
    # ---------------- injectorul cilindrului 1 (modelul din filmul cu amorsarea)
    GJ = json.load(open(os.path.join(src, 'geo.json'))); GB = open(os.path.join(src, 'geo.bin'), 'rb').read()
    INJ = K.empty('INJ', loc=(SX, 0, L.DECK - 2.2)); O['INJ'] = INJ
    mm = {'steelPol': MAT['steelPol'], 'copper': MAT['copper'], 'steelDark': MAT['steelDark'], 'zincW': MAT['zincW'], 'steel': MAT['steel'],
          'plasticBlack': MAT['plasticGrey'], 'brass': MAT['brass']}
    geo_part('inj', INJ, mm, GJ, GB)
    return O
