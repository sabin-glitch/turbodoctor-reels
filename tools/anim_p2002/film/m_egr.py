# EGR de joasa presiune: priza de dupa filtru, racitorul (in sectiune), supapa EGR, teava de evacuare cu clapeta.
import bpy, bmesh, math
import numpy as np
from mathutils import Vector, Matrix
import kit as K
from kit import S
from mats import MAT
import layout as L

def unit_frame(name, c, axis, toward):
    """reper local: z = axa tevii, y = spre camera (bisectoarea decuparii), x = axul clapetei"""
    z = L.nrm(axis); t = np.asarray(toward, np.float64)
    y = L.nrm(t - z * (t @ z)); x = np.cross(y, z)
    e = K.empty(name)
    e.matrix_basis = Matrix(((x[0], y[0], z[0], c[0]), (x[1], y[1], z[1], c[1]), (x[2], y[2], z[2], c[2]), (0, 0, 0, 1)))
    return e, x, y, z

def flap_unit(name, c, axis, toward, r, blen, mat_body, motor=(40, 50, 44), wall=5.0):
    """corp de clapeta cu motoras: teava scurta cu sfert decupat, clapeta fluture pe ax, carcasa actuatorului."""
    U, x, y, z = unit_frame(name, c, axis, toward)
    h = blen / 2
    prof = [(r, -h), (r + wall + 4, -h), (r + wall + 4, -h + 4), (r + wall, -h + 6), (r + wall, h - 6), (r + wall + 4, h - 4), (r + wall + 4, h), (r, h)]
    body = K.lathe(name + '.body', prof, seg=64, mat=[mat_body, MAT['machAlu']], parent=U, sharp=30)
    cut = K.lathe('cutw', [(0.02, -h + 5), (r + wall + 12, -h + 5), (r + wall + 12, h - 5), (0.02, h - 5)], seg=16, mat=MAT['machAlu'], parent=U, deg=90, a0=45)
    K.boolean(body, cut, solver='EXACT'); K.shade(body, 30)
    # lagarele axului + carcasa actuatorului (pe partea +x)
    K.cyl(name + '.boss1', 7.5, 12, c=(r + wall + 4, 0, 0), axis='X', mat=mat_body, seg=24, parent=U, bev=1.0)
    K.cyl(name + '.boss2', 7.5, 10, c=(-(r + wall + 3), 0, 0), axis='X', mat=mat_body, seg=24, parent=U, bev=1.0)
    mx = r + wall + 10 + motor[0] / 2
    K.box(name + '.motor', motor, c=(mx, 0, 4), mat=MAT['plasticBlack'], bev=5.0, seg=3, parent=U)
    K.cyl(name + '.motcan', 15, motor[0] * 0.9, c=(mx, -6, -motor[2] / 2 - 9), axis='X', mat=MAT['plasticBlack'], seg=32, bev=2.0, parent=U)
    K.box(name + '.conn', (20, 18, 22), c=(mx + 4, motor[1] / 2 + 8, 6), mat=MAT['connGrey'], bev=2.5, parent=U)
    for (dy, dz) in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        K.cyl(name + '.scr', 2.6, 3, c=(mx + motor[0] / 2 + 0.5, dy * (motor[1] / 2 - 6), 4 + dz * (motor[2] / 2 - 6)), axis='X', mat=MAT['zincW'], seg=6, parent=U)
    # clapeta (se roteste in jurul axului local x)
    F = K.empty(name + '.FLAP', parent=U)
    K.cyl(name + '.disc', r - 0.8, 1.8, c=(0, 0, 0), axis='Z', mat=MAT['steel'], seg=64, parent=F, bev=0.4)
    K.cyl(name + '.shaft', 3.2, 2 * r + wall * 2 + 26, c=(6, 0, 0), axis='X', mat=MAT['steelPol'], seg=20, parent=F)
    for s in (-1, 1):
        K.cyl(name + '.fscr', 2.2, 1.6, c=(s * r * 0.45, 0, 1.6), axis='Z', mat=MAT['zincW'], seg=6, parent=F)
    return U, F

def build():
    O = {}
    C = L.COOL_C; SZ = L.COOL_S
    hx, hy, hz = SZ[0] / 2, SZ[1] / 2, SZ[2] / 2
    CO = K.empty('COOL', loc=tuple(C)); O['COOL'] = CO
    # ---------------- carcasa racitorului (inox), cu fereastra taiata in fata
    shell = K.box('egr.shell', (SZ[0], SZ[1], SZ[2]), mat=[MAT['inoxEgr'], MAT['inoxS']], bev=7.0, seg=4, parent=CO)
    inner = K.box('cuti', (SZ[0] - 4.4, SZ[1] - 4.4, SZ[2] + 10), mat=MAT['inoxS'], bev=5.0, seg=4, parent=CO)
    K.boolean(shell, inner, solver='EXACT')
    YC = -19.5; ZW = 50.0
    def window(mat=None):
        return K.box('cutw', (SZ[0] + 30, 60, 2 * ZW), c=(0, YC - 30, 0), mat=mat or MAT['inoxS'], parent=CO)
    K.boolean(shell, window(), solver='EXACT'); K.shade(shell, 30)
    # placile tubulare (capetele fasciculului)
    for s in (-1, 1):
        K.box('egr.sheet', (SZ[0] - 4.6, SZ[1] - 4.6, 3.0), c=(0, 0, s * (hz - 6)), mat=MAT['inoxS'], parent=CO)
    # ---------------- fasciculul de tevi (gazele trec prin tevi, lichidul de racire pe langa ele)
    r = L.COOL_TUBE_R; p = L.COOL_PITCH
    xs = [(-1.5 + i) * p for i in range(4)]; ys = [(-2.5 + j) * p for j in range(6)]
    tubes = []
    for x in xs:
        for y in ys:
            me = K.tube_mesh('t', [(x, y, -hz + 6), (x, y, hz - 6)], r, seg=20, r_in=r - 0.7)
            tubes.append(K.obj('t', me, [MAT['inoxS'], MAT['secDark']], CO))
    tb = K.join(tubes, 'egr.tubes')
    K.boolean(tb, window(), solver='EXACT'); K.shade(tb, 40)
    O['tubes'] = tb; O['tube_xy'] = [(x, y) for x in xs for y in ys]
    # lichidul de racire dintre tevi (roz), taiat de aceeasi fereastra
    cool = K.box('egr.coolant', (SZ[0] - 4.8, SZ[1] - 4.8, SZ[2] - 15), mat=MAT['coolant'], parent=CO)
    cyls = []
    for x in xs:
        for y in ys:
            cyls.append(K.cyl('c', r + 0.05, SZ[2], c=(x, y, 0), seg=20, parent=CO))
    cj = K.join(cyls, 'cutc'); cj.data.materials.append(MAT['coolant'])
    K.boolean(cool, cj, solver='EXACT')
    K.boolean(cool, window(MAT['coolant']), solver='EXACT')
    O['coolant'] = cool
    # fisura din peretele unei tevi (apare doar in capitolul cu racitorul)
    xc = xs[1]
    pts = [(xc + (r - 0.72) * math.cos(math.radians(a)), YC + (r - 0.72) * math.sin(math.radians(a)), z)
           for (a, z) in ((62, -3), (74, 2), (66, 6), (82, 10), (72, 15), (88, 19), (78, 24))]
    O['crack'] = K.tube('egr.crack', pts, 0.42, MAT['crack'], seg=8, parent=CO)
    O['crack_pos'] = (C + np.array([xc + 1.2, YC + r - 1.0, 10.0])).tolist()
    # stuturile pentru furtunurile de lichid de racire
    for nm, z in (('egr.spigA', 50.0), ('egr.spigB', -50.0)):
        K.cyl(nm, 8.0, 24, c=(hx + 10, 22, z), axis='X', mat=MAT['inoxS'], seg=28, parent=CO)
        K.lathe(nm + 'b', [(8.0, -2), (9.6, 0), (8.0, 2)], seg=28, mat=MAT['inoxS'], parent=CO, axis='X', loc=(hx + 18, 22, z))
    # urechi de prindere
    for s in (-1, 1):
        K.box('egr.tab', (4, 22, 26), c=(-hx - 1.0, s * 24, s * 40), mat=MAT['inoxS'], bev=1.0, parent=CO)
    # ---------------- difuzoarele si tevile de gaze (din SDF, tabla ambutisata)
    take = [(-188.0, -243.0, -112.0), (-150.0, -247.0, -108.0), (-112.0, -251.0, -104.0), (-78.0, -252.0, -96.0), (C[0], C[1], C[2] - hz - 16), (C[0], C[1], C[2] - hz - 4)]
    fin = S.su(22.0, S.box((C[0], C[1], C[2] - hz + 1), (hx - 0.5, hy - 0.5, 7), 6), S.path(K.catmull(take, 6), 17.0))
    fin = S.i(fin, S.plane((0, 0, 1), C[2] - hz + 2.5))
    O['take'] = K.sdf_obj('egr.take', fin, (-196, -300, -132), (C[0] + hx + 4, -204, C[2] - hz + 2.5), 1.1, MAT['inoxEgr'])
    up = [(C[0], C[1], C[2] + hz + 2), (C[0], C[1], C[2] + hz + 20), (-34.0, -258.0, 136.0), (4.0, -264.0, 150.0), (40.0, -264.0, 151.0)]
    fo = S.su(22.0, S.box((C[0], C[1], C[2] + hz - 1), (hx - 0.5, hy - 0.5, 7), 6), S.path(K.catmull(up, 6), 16.5))
    fo = S.i(fo, S.plane((0, 0, -1), -(C[2] + hz - 2.5)), S.plane((1, 0, 0), 40.0))
    O['egr_up'] = K.sdf_obj('egr.up', fo, (C[0] - hx - 4, -300, C[2] + hz - 2.5), (40, -204, 172), 1.1, MAT['inoxEgr'])
    VC = np.array([176.0, -240.0, 206.0]); VA = L.nrm([17.0, 20.0, 52.0])
    p1 = VC - VA * 22; p2 = VC + VA * 22
    pipe = K.fillet_path([(40.0, -264.0, 151.0), (132.0, -264.0, 151.0), tuple(p1 - VA * 30), tuple(p1)], 30, 8)
    O['egr_pipe'] = K.tube('egr.pipe', pipe, 16.5, MAT['inoxEgr'], seg=32, r_in=15.2)
    K.tube('egr.pipe2', [tuple(p2), tuple(p2 + VA * 12)], 16.5, MAT['inoxEgr'], seg=32, r_in=15.2)
    # ---------------- supapa EGR (clapeta cu motoras) si clapeta de evacuare
    U, F = flap_unit('egrv', VC, VA, (0.55, -0.82, 0.1), 16.0, 44.0, MAT['castAlu'], motor=(36, 46, 40))
    O['EGRV'] = U; O['EGRV_FLAP'] = F
    # teava de evacuare: racord flexibil + clapeta de evacuare
    e0 = np.array([-188.0, -330.0, -193.0]); e1 = np.array([-186.4, -372.0, -197.0]); e2 = np.array([-184.2, -446.0, -202.0])
    e3 = np.array([-183.6, -478.0, -203.6]); e4 = np.array([-182.8, -522.0, -205.6]); e5 = np.array([-181.5, -610.0, -209.0])
    K.tube('exh.p1', [tuple(e0), tuple(e1)], 30.0, MAT['inox'], seg=40, r_in=28.4)
    n = 90; t = np.linspace(0, 1, n)
    P = e1[None, :] + (e2 - e1)[None, :] * t[:, None]
    rr = 33.0 + 2.4 * np.sin(t * 2 * np.pi * 15); rr[:3] = 31.5; rr[-3:] = 31.5
    O['flex'] = K.obj('exh.flex', K.tube_mesh('exh.flex', P, rr, seg=40, caps=False), MAT['flex'])
    K.tube('exh.p2', [tuple(e2), tuple(e3)], 30.0, MAT['inox'], seg=40, r_in=28.4)
    K.tube('exh.p3', [tuple(e4), tuple(e5)], 30.0, MAT['inox'], seg=40, r_in=28.4)
    FC = (e3 + e4) / 2; FA = L.nrm(e4 - e3)
    U2, F2 = flap_unit('exf', FC, FA, (0.75, -0.2, 0.62), 28.6, 44.0, MAT['castAlu'], motor=(40, 52, 44))
    O['EXF'] = U2; O['EXF_FLAP'] = F2
    O['paths'] = {
        'take': K.catmull(take, 8).tolist(),
        'cool_in': [C[0], C[1], C[2] - hz + 6], 'cool_out': [C[0], C[1], C[2] + hz - 6],
        'up': K.catmull(up, 8).tolist(), 'pipe': np.asarray(pipe).tolist(), 'v1': p1.tolist(), 'v2': p2.tolist(),
        'vend': (p2 + VA * 30).tolist(),
        'exh': [e0.tolist(), e1.tolist(), e2.tolist(), e3.tolist(), e4.tolist(), e5.tolist()],
    }
    O['VC'] = VC.tolist(); O['FC'] = FC.tolist()
    return O
