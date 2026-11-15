# Modulul de tratare a gazelor: catalizator de oxidare + filtru de particule (DPF), in sectiune (sfert decupat).
import bpy, bmesh, math
import numpy as np
from mathutils import Vector, Matrix
import kit as K
from kit import S
from mats import MAT
import layout as L

def mod_empty():
    e = K.empty('MOD')
    e.matrix_basis = Matrix(((L.MX[0], L.MY[0], L.MD[0], L.M0[0]),
                             (L.MX[1], L.MY[1], L.MD[1], L.M0[1]),
                             (L.MX[2], L.MY[2], L.MD[2], L.M0[2]),
                             (0, 0, 0, 1)))
    return e

def boxes_np(boxes):
    """lista de (x0,x1,y0,y1,z0,z1) -> (V, F) cu cate 8 varfuri si 6 fete patrate pe cutie"""
    B = np.asarray(boxes, np.float32).reshape(-1, 6)
    n = len(B)
    V = np.zeros((n, 8, 3), np.float32)
    for k, (ix, iy, iz) in enumerate([(0, 2, 4), (1, 2, 4), (1, 3, 4), (0, 3, 4), (0, 2, 5), (1, 2, 5), (1, 3, 5), (0, 3, 5)]):
        V[:, k, 0] = B[:, ix]; V[:, k, 1] = B[:, iy]; V[:, k, 2] = B[:, iz]
    q = np.array([(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)], np.int32)
    F = (q[None, :, :] + (8 * np.arange(n, dtype=np.int32))[:, None, None]).reshape(-1, 4)
    return V.reshape(-1, 3), F

def boxes_obj(name, boxes, mat, parent, key=None):
    V, F = boxes_np(boxes)
    me = K.mesh_np(name, V, F, smooth=False)
    o = K.obj(name, me, mat, parent)
    if key is not None:
        V2, _ = boxes_np(key)
        o.shape_key_add(name='Basis')
        kb = o.shape_key_add(name='K'); kb.slider_min = 0.0; kb.slider_max = 1.0
        kb.data.foreach_set('co', V2.ravel())
    return o

def honeycomb(R, z0, z1, p, w, skin=1.2):
    """peretii unui monolit cu celule patrate; sfertul (x>0, y>0) lipseste; planele de taiere trec prin mijlocul celulelor"""
    Ri = R - skin * 0.6
    B = []
    kmax = int(R / p) + 2
    for k in range(-kmax, kmax + 1):
        x = (k + 0.5) * p
        if abs(x) >= Ri - 0.3: continue
        c = math.sqrt(Ri * Ri - x * x)
        B.append((x - w / 2, x + w / 2, -c, (0.0 if x > 0 else c), z0, z1))      # perete in planul x = const
        B.append((-c, (0.0 if x > 0 else c), x - w / 2, x + w / 2, z0, z1))      # perete in planul y = const
    return B

def cells(R, p, skin=1.2):
    """celulele intregi ramase: (i, j, x0, x1, y0, y1) cu limitele interioare"""
    Ri = R - skin
    out = []
    kmax = int(R / p) + 2
    for i in range(-kmax, kmax + 1):
        for j in range(-kmax, kmax + 1):
            if i > 0 and j > 0: continue
            if i == 0 and j == 0: continue
            cx, cy = i * p, j * p
            if math.hypot(abs(cx) + p / 2, abs(cy) + p / 2) > Ri: continue
            x0, x1, y0, y1 = cx - p / 2, cx + p / 2, cy - p / 2, cy + p / 2
            if j == 0 and i > 0: y1 = 0.0
            if i == 0 and j > 0: x1 = 0.0
            out.append((i, j, x0, x1, y0, y1))
    return out

def build():
    O = {}
    MOD = mod_empty(); O['MOD'] = MOD
    T = L.SHELL_T
    # ---------------- carcasa din tabla (cu flansa si colier intre catalizator si filtru), sfert decupat
    r1, r2, ze = L.SHELL_R1, L.SHELL_R2, L.MOD_END
    prof = [(r1, -12), (r1, 97), (84, 97), (84, 104), (r2, 104), (r2, ze),
            (r2 - T, ze), (r2 - T, 100.5), (r1 - T, 100.5), (r1 - T, -12)]
    shell = K.lathe('mod.shell', prof, seg=96, mat=[MAT['inoxHeat'], MAT['inoxS']], parent=MOD, sharp=30)
    cut = K.box('cut', (220, 220, 286 - 2), c=(110, 110, (286 + 2) / 2), parent=MOD)
    cut.data.materials.append(MAT['inoxS'])
    K.boolean(shell, cut, solver='EXACT')
    K.shade(shell, 30)
    O['shell'] = shell
    # ---------------- vata de etansare (izolatia dintre ceramica si tabla)
    for nm, R, z0, z1, ro in (('mod.mat1', L.CAT_R, L.CAT_Z0 + 3, L.CAT_Z1 - 3, r1 - T), ('mod.mat2', L.DPF_R, L.DPF_Z0 + 4, L.DPF_Z1 - 4, r2 - T)):
        K.lathe(nm, [(R, z0), (ro, z0), (ro, z1), (R, z1)], seg=64, mat=MAT['mat'], parent=MOD, deg=270, a0=90, sharp=30)
    # ---------------- catalizatorul de oxidare (celule drepte, fine)
    B = honeycomb(L.CAT_R, L.CAT_Z0, L.CAT_Z1, L.CAT_P, L.CAT_W)
    O['cat'] = boxes_obj('mod.cat', B, MAT['ceramicCat'], MOD)
    K.lathe('mod.catskin', [(L.CAT_R - 1.0, L.CAT_Z0), (L.CAT_R, L.CAT_Z0), (L.CAT_R, L.CAT_Z1), (L.CAT_R - 1.0, L.CAT_Z1)], seg=64,
            mat=MAT['ceramicCat'], parent=MOD, deg=270, a0=90)
    # ---------------- filtrul de particule (canale infundate alternativ)
    p, w = L.DPF_P, L.DPF_W; z0, z1 = L.DPF_Z0, L.DPF_Z1; pl = L.DPF_PLUG
    B = honeycomb(L.DPF_R, z0, z1, p, w)
    CE = cells(L.DPF_R, p)
    for (i, j, x0, x1, y0, y1) in CE:
        if (i + j) % 2 == 0: B.append((x0, x1, y0, y1, z1 - pl, z1))    # canal de intrare: dop la iesire
        else: B.append((x0, x1, y0, y1, z0, z0 + pl))                     # canal de iesire: dop la intrare
    O['dpf'] = boxes_obj('mod.dpf', B, MAT['ceramic'], MOD)
    K.lathe('mod.dpfskin', [(L.DPF_R - 1.2, z0), (L.DPF_R, z0), (L.DPF_R, z1), (L.DPF_R - 1.2, z1)], seg=64,
            mat=MAT['ceramic'], parent=MOD, deg=270, a0=90)
    # ---------------- funinginea din canalele de intrare vizibile pe fetele taiate (grosime animata)
    hw = w / 2
    S0, S1, A0, A1, G0, G1 = [], [], [], [], [], []
    vis = [c for c in CE if (c[1] == 0 and c[0] > 0) or (c[0] == 0 and c[1] > 0)]
    O['vis_cells'] = vis
    for (i, j, x0, x1, y0, y1) in vis:
        if (i + j) % 2: continue
        a0, a1, b0, b1 = x0 + hw, x1 - (hw if j == 0 else 0), y0 + hw, y1 - (hw if i == 0 else 0)
        zt, zb = z0 + 0.5, z1 - pl
        e = 0.03; t = 1.25
        if j == 0:   # fata y = 0: pereti laterali la x = a0, a1 si fundul la y = b0
            S0 += [(a0, a0 + e, b0, b1, zt, zb), (a1 - e, a1, b0, b1, zt, zb), (a0, a1, b0, b0 + e, zt, zb)]
            S1 += [(a0, a0 + t, b0, b1, zt, zb), (a1 - t, a1, b0, b1, zt, zb), (a0, a1, b0, b0 + t, zt, zb)]
        else:        # fata x = 0
            S0 += [(a0, a1, b0, b0 + e, zt, zb), (a0, a1, b1 - e, b1, zt, zb), (a0, a0 + e, b0, b1, zt, zb)]
            S1 += [(a0, a1, b0, b0 + t, zt, zb), (a0, a1, b1 - t, b1, zt, zb), (a0, a0 + t, b0, b1, zt, zb)]
        # cenusa: dop deschis la culoare care creste de la capatul infundat
        A0.append((a0, a1, b0, b1, zb - 0.05, zb)); A1.append((a0, a1, b0, b1, zb - 62.0, zb))
        # crusta de la lichidul de racire: pe gura canalului
        G0.append((a0, a1, b0, b1, zt - 0.4, zt - 0.35)); G1.append((a0, a1, b0, b1, zt - 0.4, zt + 16.0))
    O['soot'] = boxes_obj('mod.soot', S0, MAT['soot'], MOD, key=S1)
    O['ash'] = boxes_obj('mod.ash', A0, MAT['ash'], MOD, key=A1)
    O['glaze'] = boxes_obj('mod.glaze', G0, MAT['glaze'], MOD, key=G1)
    # crusta si pe fata de intrare a monolitului (peste capetele peretilor)
    Bg = [(b[0] - 0.25, b[1] + 0.25, b[2] - 0.0, b[3], z0 - 0.9, z0 + 0.05) if abs(b[1] - b[0]) < w * 1.5 else
          (b[0], b[1], b[2] - 0.25, b[3] + 0.25, z0 - 0.9, z0 + 0.05) for b in honeycomb(L.DPF_R, z0, z1, p, w)]
    O['glazeTop'] = boxes_obj('mod.glazeTop', Bg, MAT['glaze'], MOD)
    # ---------------- colierul dintre cele doua jumatati
    K.lathe('mod.vband', [(84.3, 96.0), (88.6, 98.2), (88.6, 102.8), (84.3, 105.0)], seg=72, mat=MAT['clamp'], parent=MOD, deg=270, a0=90, sharp=25)
    a = math.radians(205)
    c = Vector((92 * math.cos(a), 92 * math.sin(a), 100.5)); tdir = Vector((-math.sin(a), math.cos(a), 0))
    K.rod('mod.vbolt', c - tdir * 26, c + tdir * 26, 3.2, MAT['zincW'], parent=MOD)
    for s in (-1, 1):
        K.rod('mod.vtrun', c + tdir * 14 * s - Vector((0, 0, 7)), c + tdir * 14 * s + Vector((0, 0, 7)), 5.0, MAT['clamp'], parent=MOD, bev=0.8)
    K.rod('mod.vnut', c + tdir * 21, c + tdir * 29, 6.0, MAT['zincW'], seg=6, parent=MOD)
    # ---------------- palnia de intrare (de la turbina) si palnia de iesire: tabla ambutisata, din SDF
    top = L.mw(0, 0, -12); apex = L.mw(0, 0, -60)
    f0 = np.array([L.TURB_OUT_X, L.TURBO_Y, L.TURBO_Z]); f1 = np.array([-138.0, -221.0, 262.0])
    fin = S.su(16.0, S.cone(top + L.MD * 2, apex, L.SHELL_R1, 36.0, rd=10.0), S.capsule(f0 + np.array([14.0, 0, 0]), f1, 30.0, 36.0))
    fin = S.i(fin, S.plane((1, 0, 0), f0[0]))                 # fata flansei catre turbina
    fin = S.i(fin, S.plane(tuple(L.MD), float(L.MD @ top)))   # se opreste la gulerul carcasei
    O['funnel_in'] = K.sdf_obj('mod.funnelIn', fin, (-245, -310, 190), (-40, -140, 305), 1.25, MAT['inoxHeat'])
    K.cyl('mod.flangeIn', 39.0, 7.0, c=(f0[0] - 3.5, f0[1], f0[2]), axis='X', mat=MAT['inoxS'], seg=64, bev=1.0)
    end = L.mw(0, 0, L.MOD_END); ap2 = L.mw(0, 0, L.MOD_END + 50)
    path = [L.mw(0, 0, L.MOD_END + 30), (-192.5, -241.5, -128), (-194, -247, -152), (-193, -263, -173), (-190.5, -292, -187), (-188, -332, -193)]
    fout = S.su(18.0, S.cone(end - L.MD * 2, ap2, L.SHELL_R2, 38.0, rd=10.0), S.path(K.catmull(path, 6), 30.0))
    fout = S.i(fout, S.plane(tuple(-L.MD), float(-L.MD @ end)))
    fout = S.i(fout, S.plane((0, -1, 0), 330.0))
    O['funnel_out'] = K.sdf_obj('mod.funnelOut', fout, (-285, -334, -230), (-95, -150, -76), 1.25, MAT['inoxHeat'])
    return O
