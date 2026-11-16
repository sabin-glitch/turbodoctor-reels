# Galeria de evacuare, turbosuflanta (carcase, rotor), conducte de aer si de ulei.
import bpy, bmesh, math
import numpy as np
from mathutils import Vector
import kit as K
from kit import S
from mats import MAT
import layout as L

TY, TZ = L.TURBO_Y, L.TURBO_Z

def wheel(name, parent, x_dir, n_blades, R, L_ax, r_hub0, r_tip0, wrap, mat, splitter=False):
    """rotor radial-axial: butuc + palete. x_dir = +1: gura (partea axiala) spre +X."""
    nm, ns = 16, 5
    phi = np.linspace(0, np.pi / 2, nm)
    xh = L_ax * (1 - np.sin(phi)); rh = r_hub0 + (R - r_hub0) * (1 - np.cos(phi))
    xs = L_ax * 0.26 + (L_ax * 0.74) * (1 - np.sin(phi)); rs = r_tip0 + (R - r_tip0) * (1 - np.cos(phi))
    # butuc (corp de revolutie)
    prof = [(0.02, -4.0)] + [(float(rh[i]), float(xh[i])) for i in range(nm - 1, -1, -1)] + [(r_hub0 * 0.75, L_ax + 5.0), (0.02, L_ax + 7.0)]
    hub = K.lathe(name + '.hub', prof, seg=48, mat=mat, parent=parent, axis='X', sharp=40)
    if x_dir < 0: hub.rotation_euler = (0, -math.pi / 2, 0)
    V = []; F = []
    def blade(th0, m0=0):
        base = len(V)
        for i in range(m0, nm):
            m = i / (nm - 1)
            th = th0 + wrap * (1 - m) ** 1.4
            for j in range(ns):
                s = j / (ns - 1)
                x = xh[i] + (xs[i] - xh[i]) * s; r = rh[i] + (rs[i] - rh[i]) * s
                V.append((x * x_dir, r * math.cos(th), r * math.sin(th)))
        nmm = nm - m0
        for i in range(nmm - 1):
            for j in range(ns - 1):
                a = base + i * ns + j
                F.append((a, a + 1, a + ns + 1, a + ns))
    for b in range(n_blades):
        blade(2 * math.pi * b / n_blades)
        if splitter: blade(2 * math.pi * (b + 0.5) / n_blades, m0=5)
    me = K.mesh_np(name + '.blades', np.array(V, np.float32), np.array(F, np.int32), smooth=True)
    o = K.obj(name + '.blades', me, mat, parent)
    sol = o.modifiers.new('sol', 'SOLIDIFY'); sol.thickness = 1.1; sol.offset = 0.0
    K.apply_mods(o); K.shade(o, 40)
    return o

def build():
    O = {}
    # ---------------- galeria + carcasa turbinei (fonta, o singura piesa turnata)
    parts = []
    for xi in L.CYL_X:
        parts.append(S.box((xi, -L.HEAD_Y - 9, L.PORT_Z), (27, 5.5, 23), 4))
        parts.append(S.capsule((xi, -L.HEAD_Y - 6, L.PORT_Z), (xi * 0.80, -162, 300), 15.5))
    parts.append(S.capsule((112, -163, 300), (-112, -163, 300), 18.5))
    parts.append(S.path(K.catmull([(10, -162, 300), (7, -180, 311), (5, -202, 319), (4, -222, 314)], 6), 21.0))
    volute = S.torus(0, (L.TURB_X, TY, TZ), 45, 25)
    core = S.cyl(0, (L.TURB_X - 1, TY, TZ), 50, 23, 6)
    neck = S.cyl(0, (-30, TY, TZ), 31.5, 18, 3)
    fl = S.cyl(0, (L.TURB_OUT_X + 5, TY, TZ), 38.5, 4.5, 1.5)
    boss = S.cyl(0, (24, -258, 242), 9, 9, 3)
    f = S.su(11.0, *parts, volute, core, neck, boss)
    f = S.su(3.0, f, fl)
    f = S.i(f, S.plane((0, 1, 0), -L.HEAD_Y - 3.6))
    O['manifold'] = K.sdf_obj('trb.manifold', f, (-152, -292, 190), (152, -L.HEAD_Y - 3.6, 348), 1.2, MAT['castIron'])
    for xi in L.CYL_X:
        for (dx, dz) in ((20, 15), (-20, -15)):
            K.cyl('trb.nut', 6.6, 7, c=(xi + dx, -L.HEAD_Y - 18, L.PORT_Z + dz), axis='Y', mat=MAT['zinc'], seg=6, bev=0.7)
            K.cyl('trb.stud', 3.2, 12, c=(xi + dx, -L.HEAD_Y - 20, L.PORT_Z + dz), axis='Y', mat=MAT['zinc'], seg=12)
    # colierul dintre turbina si palnia catalizatorului
    K.lathe('trb.vband', [(38.8, -6.5), (43.5, -4.4), (43.5, 4.4), (38.8, 6.5)], seg=64, mat=MAT['clamp'], axis='X', loc=(L.TURB_OUT_X, TY, TZ), sharp=25)
    K.rod('trb.vbolt', (L.TURB_OUT_X, TY - 22, TZ + 47), (L.TURB_OUT_X, TY + 22, TZ + 47), 3.0, MAT['zincW'])
    K.rod('trb.vnut', (L.TURB_OUT_X, TY + 18, TZ + 47), (L.TURB_OUT_X, TY + 26, TZ + 47), 5.6, MAT['zincW'], seg=6)
    # ---------------- carcasa centrala (lagarele) cu racordurile de ulei
    ch = S.su(6.0, S.cyl(0, (50, TY, TZ), 26, 22, 5), S.cyl(0, (73, TY, TZ), 42, 5, 2.5), S.cyl(0, (30, TY, TZ), 36, 4, 2),
              S.cyl(2, (50, TY, TZ + 29), 9, 8, 2), S.box((50, TY, TZ - 30), (13, 11, 6), 3))
    O['chra'] = K.sdf_obj('trb.chra', ch, (22, TY - 46, TZ - 40), (82, TY + 46, TZ + 42), 0.9, MAT['blockIron'])
    K.tube('trb.oilfeed', [(60, -118, 200), (60, -140, 212), (56, -182, 296), (50, TY, TZ + 44), (50, TY, TZ + 36)], 3.2, MAT['steel'], seg=14, fillet=14)
    K.cyl('trb.banjo', 7.5, 7, c=(50, TY, TZ + 40), axis='Z', mat=MAT['zincW'], seg=6, bev=0.6)
    K.cyl('trb.banjo2', 7.0, 8, c=(60, -116, 200), axis='Y', mat=MAT['zincW'], seg=6, bev=0.6)
    K.tube('trb.oilret', [(50, TY, TZ - 34), (50, TY + 4, TZ - 62), (54, -168, 118), (55, -134, 60), (55, -122, 58)], 8.0, MAT['steel'], seg=20, fillet=24)
    K.box('trb.oilfl', (30, 26, 4), c=(50, TY, TZ - 37), mat=MAT['steel'], bev=1.0)
    # ---------------- carcasa compresorului (aluminiu)
    cx = L.COMP_X
    comp = S.su(9.0, S.torus(0, (cx, TY, TZ), 50, 21), S.cyl(0, (cx - 4, TY, TZ), 56, 15, 6), S.cyl(0, (cx + 28, TY, TZ), 30, 15, 3),
                S.path(K.catmull([(cx, TY + 50, TZ + 4), (cx - 2, TY + 57, TZ + 42), (cx - 4, TY + 62, TZ + 79)], 6), 20.5))
    comp = S.su(3.0, comp, S.cyl(0, (L.COMP_IN_X - 3, TY, TZ), 32.5, 3, 1.2))
    comp = S.i(comp, S.plane((1, 0, 0), L.COMP_IN_X), S.plane((0, 0, 1), TZ + 79))
    O['comp'] = K.sdf_obj('trb.comp', comp, (cx - 30, TY - 78, TZ - 78), (L.COMP_IN_X, TY + 90, TZ + 79), 1.0, MAT['castAluG'])
    # ---------------- rotorul (se vede cand carcasele devin transparente)
    RT = K.empty('ROTOR', loc=(0, TY, TZ)); O['ROTOR'] = RT
    cw = K.empty('rot.cw', parent=RT, loc=(cx - 12, 0, 0))
    wheel('rot.comp', cw, +1, 6, 38.0, 30.0, 8.0, 25.0, 0.95, MAT['machAlu'], splitter=True)
    tw = K.empty('rot.tw', parent=RT, loc=(L.TURB_X + 14, 0, 0))
    wheel('rot.turb', tw, -1, 9, 33.0, 28.0, 8.0, 26.0, -0.8, MAT['steelDark'])
    K.cyl('rot.shaft', 4.5, 96, c=(52, 0, 0), axis='X', mat=MAT['steelPol'], seg=24, parent=RT)
    # ---------------- actuatorul geometriei variabile
    K.box('trb.act', (46, 40, 52), c=(118, -278, 322), mat=MAT['plasticBlack'], bev=4.0, seg=3)
    K.cyl('trb.actcap', 20, 10, c=(118, -278, 352), axis='Z', mat=MAT['plasticBlack'], seg=40, bev=2)
    K.box('trb.actcon', (18, 16, 26), c=(146, -282, 330), mat=MAT['connGrey'], bev=2.0)
    K.box('trb.actbr', (60, 6, 36), c=(110, -254, 318), mat=MAT['steel'], bev=1.0)
    K.rod('trb.actrod', (100, -292, 300), (26, -266, 244), 2.6, MAT['zincW'], seg=12)
    K.box('trb.lever', (8, 26, 8), c=(24, -262, 243), mat=MAT['steelDark'], bev=1.5)
    # ---------------- aer: tubulatura de la filtru, amestecatorul EGR, teava de presiune catre admisie
    mix = S.su(7.0, S.cyl(0, (172, TY, TZ), 33.5, 26, 3), S.capsule((184, -228, 232), (186, -218, 256), 20.0),
               S.cyl(0, (L.COMP_IN_X + 3.5, TY, TZ), 37, 3.5, 1.2))
    mix = S.i(mix, S.plane((-1, 0, 0), -(L.COMP_IN_X + 0.4)), S.plane((1, 0, 0), 198.0))
    O['mixer'] = K.sdf_obj('air.mixer', mix, (L.COMP_IN_X + 0.4, TY - 44, 208), (198, TY + 44, TZ + 44), 0.9, MAT['castAluG'])
    duct = K.catmull([(198, TY, TZ), (232, -217, 268), (284, -236, 284), (334, -268, 308), (372, -300, 331)], 10)
    O['duct'] = K.tube('air.duct', duct, 30.5, MAT['plasticBlackG'], seg=40, r_in=28.2)
    K.tube('air.ductring', [duct[-1] - (duct[-1] - duct[-2]) * 2.2, duct[-1]], 33.0, MAT['plasticBlackG'], seg=40, r_in=28.2)
    K.tube('air.clamp1', [(199, TY, TZ), (210, TY - 1.5, TZ + 0.6)], 31.6, MAT['clamp'], seg=40, r_in=30.4)
    # debitmetrul (pe tubulatura de aer)
    d0 = duct[len(duct) * 2 // 3]; d1 = duct[len(duct) * 2 // 3 + 3]; dd = (d1 - d0) / np.linalg.norm(d1 - d0)
    K.tube('air.maf', [d0, d0 + dd * 30], 34.0, MAT['plasticGrey'], seg=40, r_in=28.2)
    up = np.array([0, 0, 1.0]); up = up - dd * (up @ dd); up /= np.linalg.norm(up)
    K.rod('air.mafs', d0 + dd * 15 + up * 30, d0 + dd * 15 + up * 56, 11.0, MAT['plasticBlack'], seg=24, bev=1.5)
    K.box('air.mafc', (16, 24, 14), c=tuple(d0 + dd * 15 + up * 60), mat=MAT['connGrey'], bev=2.0)
    O['maf_pos'] = (d0 + dd * 15 + up * 40).tolist()
    cp = K.catmull([(cx - 4, TY + 62, TZ + 79), (cx - 5, -142, 392), (cx - 6, -108, 447), (cx - 6, -40, 471), (cx - 6, 40, 471), (cx - 6, 122, 452), (cx - 6, 160, 410), (cx - 6, 168, 378)], 10)
    O['charge'] = K.tube('air.charge', cp, 22.5, MAT['plasticBlackG'], seg=36, r_in=20.0)
    K.tube('air.clamp2', [cp[1], cp[3]], 23.6, MAT['clamp'], seg=36, r_in=22.6)
    O['paths'] = {'duct': duct.tolist(), 'charge': cp.tolist()}
    return O
