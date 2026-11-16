# Filtrul de motorina cu separator de apa, in sectiune. Reper: axa Z, fundul paharului la z = 0. Aceeasi pana (WEDGE grade, spre -Y) ca la injector.
# Rulare: python filter.py   ->  out/filter.blend + out/filter.json
import bpy, bmesh, math, json, os, sys
import numpy as np
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import kit as K, imats
import model as MD
from model import rev, cut, finish, drill, thread, group, PR, PL, uR, uL, EZ, aR, aL, WEDGE

META = {'pts': {}, 'paths': {}}

def star_prism(name, n, r_out, r_in, z0, z1, mat):
    pts = []
    for k in range(n):
        a = 2 * math.pi * k / n; b = a + math.pi / n
        pts.append((r_out * math.cos(a), r_out * math.sin(a))); pts.append((r_in * math.cos(b), r_in * math.sin(b)))
    bm = bmesh.new()
    vb = [bm.verts.new((x, y, z0)) for x, y in pts]; vt = [bm.verts.new((x, y, z1)) for x, y in pts]
    m = len(pts)
    bm.faces.new(list(reversed(vb))); bm.faces.new(vt)
    for i in range(m): bm.faces.new([vb[i], vb[(i + 1) % m], vt[(i + 1) % m], vt[i]])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = K.bm_to_mesh(bm, name, smooth=False)
    return K.obj(name, me, mat)

def build():
    K.init(empty=True)
    M = imats.make_all(); P = META['pts']; O = {}
    # ---------- capul filtrului (aluminiu) cu racorduri
    head_p = [(7.0, 138.0), (11.0, 138.0)] + thread(11.0, 10.4, 138.4, 148.6, 1.5) + [(11.0, 149.0), (11.0, 152.0), (20.0, 152.0), (20.0, 158.0), (36.0, 158.0), (36.0, 152.0), (44.0, 152.0), (45.0, 153.0),
              (45.0, 171.0), (43.0, 173.0), (0, 173.0), (0, 166.0), (7.0, 166.0)]
    head = rev('fhead', head_p, M['castAlu'], M['secAlu'], seg=120)
    for u, z, nm in ((uL, 155.5, 'in'), (uR, 162.0, 'out')):
        boss = K.rod('boss', u * 40.0 + EZ * z, u * 66.0 + EZ * z, 9.5, mat=[M['castAlu'], M['secAlu']], seg=48)
        bpy.context.view_layer.update(); K.boolean(head, boss, 'UNION')
    drill([head], uL * 30.0 + EZ * 155.5, uL * 67.0 + EZ * 155.5, 4.2)          # intrare: din racord in camera inelara
    drill([head], uR * 0.0 + EZ * 162.0, uR * 67.0 + EZ * 162.0, 4.2)           # iesire: din teava centrala spre racord
    cut(head); finish(head)
    P['in'] = (uL * 66.0 + EZ * 155.5).tolist(); P['out'] = (uR * 66.0 + EZ * 162.0).tolist(); P['head'] = [0, 0, 165.0]
    # ---------- carcasa (tabla), placa de sus cu gauri, garnitura
    can_p = [(30.0, 30.0), (33.0, 30.0), (38.0, 34.0), (40.0, 38.0), (40.0, 147.0), (41.6, 148.0), (41.6, 151.2), (38.6, 151.2), (38.6, 148.6), (39.0, 148.0), (39.0, 38.6), (37.4, 35.0), (32.6, 31.2), (30.0, 31.2)]
    can = rev('can', can_p, M['canPaint'], M['secCan'], seg=120); cut(can); finish(can)
    plate = rev('fplate', [(11.1, 146.6), (38.6, 146.6), (38.6, 149.6), (11.1, 149.6)], M['steel'], M['secScrew'], seg=96)
    for k in range(6):
        az = aR + k * math.pi / 3; u = np.array([math.cos(az), math.sin(az), 0.0])
        drill([plate], u * 28.0 + EZ * 145.0, u * 28.0 + EZ * 151.0, 3.6, seg=20)
    cut(plate); finish(plate)
    gasket = rev('fgasket', [(33.6, 149.6), (37.6, 149.6), (37.6, 152.3), (33.6, 152.3)], M['rubber'], M['secRubber'], seg=96); cut(gasket)
    # ---------- elementul filtrant: hartie plisata, capace, teava centrala
    paper = star_prism('paper', 44, 34.0, 25.0, 46.0, 140.0, [M['paper'], M['secPaper']])
    hole = K.lathe('ph', [(0, 40.0), (14.0, 40.0), (14.0, 146.0), (0, 146.0)], seg=64, sharp=None)
    bpy.context.view_layer.update(); K.boolean(paper, hole, 'DIFFERENCE')
    cut(paper); paper.data.polygons.foreach_set('use_smooth', np.zeros(len(paper.data.polygons), dtype=bool)); paper.data.update()
    cap_t = rev('capT', [(12.0, 140.0), (35.6, 140.0), (35.6, 136.5), (36.6, 136.5), (36.6, 142.0), (12.0, 142.0)], M['plasticG'], M['secPlastic'], seg=96); cut(cap_t)
    cap_b = rev('capB', [(0, 44.0), (36.6, 44.0), (36.6, 49.5), (35.6, 49.5), (35.6, 46.0), (0, 46.0)], M['plasticG'], M['secPlastic'], seg=96); cut(cap_b)
    tube = rev('ftube', [(12.6, 46.0), (13.8, 46.0), (13.8, 140.0), (12.6, 140.0)], M['steel'], M['secScrew'], seg=64)
    for zc in np.arange(54.0, 136.0, 9.0):
        for k in range(6):
            az = aR + k * math.pi / 3 + (0.5 if int(zc / 9) % 2 else 0.0) * math.pi / 3; u = np.array([math.cos(az), math.sin(az), 0.0])
            drill([tube], u * 11.0 + EZ * zc, u * 15.5 + EZ * zc, 1.7, seg=12)
    cut(tube); finish(tube)
    seal_t = rev('fseal', [(11.1, 142.0), (14.0, 142.0), (14.0, 146.6), (11.1, 146.6)], M['rubber'], M['secRubber'], seg=64); cut(seal_t)
    dirt = K.lathe('f_dirt', [(34.4, 47.0), (34.4, 139.0)], seg=96, mat=M['dirt'], sharp=None, closed=False, deg=360.0 - WEDGE, a0=math.degrees(aR)); dirt.hide_render = True; dirt.visible_shadow = False
    # ---------- paharul separatorului de apa (transparent), robinet de golire, senzor de apa
    bowl_p = [(29.0, 34.0), (29.0, 26.0), (33.0, 26.0), (33.0, 6.0), (30.0, 2.0), (6.0, 0.0), (6.0, 2.4), (29.0, 4.2), (30.6, 7.0), (30.6, 23.6), (26.6, 23.6), (26.6, 34.0)]
    bowl = rev('bowl', bowl_p, M['bowl'], M['secBowl'], seg=120); cut(bowl); finish(bowl)
    neck = rev('fneck', [(26.6, 34.2), (29.9, 34.2), (29.9, 30.0), (30.0, 30.0), (30.0, 36.0), (26.6, 36.0)], M['steel'], M['secScrew'], seg=96); cut(neck)
    drain = rev('drain', [(0, -9.0), (7.5, -9.0), (9.0, -7.5), (9.0, -2.0), (5.9, -1.0), (5.9, 3.6), (0, 3.6)], M['plastic'], M['secPlastic'], seg=48); cut(drain); finish(drain)
    sens = rev('wsensor', [(0, -6.0), (4.2, -6.0), (4.2, 5.0), (0, 5.0)], M['plasticG'], M['secPlastic'], seg=32)
    sens.location = Vector(uL * 19.0); bpy.context.view_layer.update()
    pins = []
    for s in (-1, 1):
        side = np.cross(uL, EZ)
        pn = K.rod('wpin', uL * 19.0 + side * 1.6 * s + EZ * 4.0, uL * 19.0 + side * 1.6 * s + EZ * 12.5, 0.6, mat=M['brass'], seg=12); pins.append(pn)
    P['bowl'] = [0, 0, 16.0]; P['sensor'] = (uL * 19.0 + EZ * 12.5).tolist(); P['drain'] = [0, 0, -6.0]; P['paper'] = PR(30.0, 95.0).tolist(); P['can'] = PR(40.0, 95.0).tolist()
    # ---------- lichide: motorina (fata retrasa cu eps) si apa (in pahar si in partea de jos)
    E = 0.06
    def fl(o):
        cut(o, eps=E, mark=False); o.visible_shadow = False; return o
    fuel_p = [(0, 4.4), (29.0, 4.4), (30.5, 7.0), (30.5, 23.7), (26.5, 23.7), (26.5, 36.0), (32.4, 31.4), (37.3, 35.2), (38.9, 38.8), (38.9, 146.5), (0, 146.5)]
    fuel = fl(rev('f_fuel', fuel_p, M['fuelLP'], seg=96))
    f_ctr = fl(rev('f_ctr', [(0, 146.4), (6.9, 146.4), (6.9, 165.9), (0, 165.9)], M['fuelLP'], seg=48))
    f_top = fl(rev('f_top', [(20.1, 149.7), (33.5, 149.7), (33.5, 152.0), (35.9, 152.0), (35.9, 157.9), (20.1, 157.9)], M['fuelLP'], seg=96))
    f_in = fl(K.rod('f_in', uL * 30.0 + EZ * 155.5, uL * 66.0 + EZ * 155.5, 4.1, mat=M['fuelLP'], seg=28))
    f_out = fl(K.rod('f_out', uR * 0.5 + EZ * 162.0, uR * 66.0 + EZ * 162.0, 4.1, mat=M['fuelLP'], seg=28))
    holes = []
    for k in (0, 4):      # gaurile din placa aflate in planele fetelor
        az = aR + k * math.pi / 3; u = np.array([math.cos(az), math.sin(az), 0.0])
        holes.append(fl(K.rod('f_ph', u * 28.0 + EZ * 146.4, u * 28.0 + EZ * 149.8, 3.5, mat=M['fuelLP'], seg=20)))
    water_p = [(0, 4.45), (29.0, 4.45), (30.45, 7.05), (30.45, 23.65), (26.45, 23.65), (26.45, 36.0), (32.35, 31.45), (37.25, 35.25), (38.85, 38.85), (38.85, 100.0), (0, 100.0)]
    water = fl(rev('f_water', water_p, M['water'], seg=96)); water.hide_render = True
    O['FILTER'] = group('FILTER', [head, can, plate, gasket, paper, cap_t, cap_b, tube, seal_t, bowl, neck, drain, sens] + pins)
    O['F_FUEL'] = group('F_FUEL', [fuel, f_ctr, f_top, f_in, f_out] + holes)
    O['F_WATER'] = group('F_WATER', [water]); O['F_DIRT'] = group('F_DIRT', [dirt])
    # trasee (mm)
    PT = META['paths']
    PT['in'] = [(uL * 66 + EZ * 155.5).tolist(), (uL * 34 + EZ * 155.5).tolist(), (uL * 28 + EZ * 154.0).tolist(), (uL * 28 + EZ * 147.0).tolist(), (uL * 36.8 + EZ * 138.0).tolist(), (uL * 36.8 + EZ * 60.0).tolist()]
    PT['down_R'] = [(uR * 28 + EZ * 154.0).tolist(), (uR * 28 + EZ * 147.0).tolist(), (uR * 36.8 + EZ * 138.0).tolist(), (uR * 36.8 + EZ * 60.0).tolist()]
    PT['up'] = [[0, 0, 60.0], [0, 0, 140.0], [0, 0, 160.0], (uR * 6 + EZ * 162).tolist(), (uR * 66 + EZ * 162).tolist()]
    META['wedge'] = WEDGE; META['uR'] = uR.tolist(); META['uL'] = uL.tolist()
    return O

if __name__ == '__main__':
    out = os.path.join(HERE, 'out', 'filter.blend')
    build()
    json.dump(META, open(out.replace('.blend', '.json'), 'w'), indent=1)
    bpy.ops.wm.save_as_mainfile(filepath=out)
    print('SAVED', out, flush=True)
