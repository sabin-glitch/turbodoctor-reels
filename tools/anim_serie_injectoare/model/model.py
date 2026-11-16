# Injector common rail cu electromagnet (tip Bosch CRI), in sectiune: geometrie din profile de revolutie + canale forate.
# Reper: axa injectorului = Z, varful duzei la z = 0, conectorul sus. Unitati: mm (obiectele stau sub ROOT cu scara 0.001).
# Sectiune: se scoate o pana de WEDGE grade centrata pe directia -Y (spre camera). Piesele mobile de pe axa raman intregi (ac, tija, bila).
# Rulare: python model.py [iesire.blend]    (variabile: WEDGE=120 | 0 pentru injectorul intreg)
import bpy, bmesh, math, json, os, sys
import numpy as np
from mathutils import Vector, Matrix
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import kit as K, imats

WEDGE = float(os.environ.get('WEDGE', '120'))       # unghiul penei (pozitia fetelor de sectiune si a canalelor)
CUT = os.environ.get('CUT', '1') == '1'             # 0 = injectorul intreg, netaiat
aR = math.radians(-90 + WEDGE / 2); aL = math.radians(-90 - WEDGE / 2)
uR = np.array([math.cos(aR), math.sin(aR), 0.0]); uL = np.array([math.cos(aL), math.sin(aL), 0.0])
EZ = np.array([0.0, 0.0, 1.0])
LIFT_N = 0.30      # ridicarea acului (mm; in realitate ~0,2-0,3)
LIFT_V = 0.32      # ridicarea armaturii / bilei (mm; in realitate ~0,05: marita ca sa se vada)
META = {'wedge': WEDGE, 'aR': aR, 'aL': aL, 'uR': uR.tolist(), 'uL': uL.tolist(), 'lift_n': LIFT_N, 'lift_v': LIFT_V, 'pts': {}, 'paths': {}}

def PR(rad, z): return uR * rad + EZ * z          # punct in planul fetei din dreapta
def PL(rad, z): return uL * rad + EZ * z          # punct in planul fetei din stanga

# ------------------------------------------------------------------ taierea penei
def wedge_prism(eps=0.0, name='WEDGE'):
    """prisma penei scoase (cu fetele impinse cu eps in material)"""
    nR = np.array([math.sin(aR), -math.cos(aR)]); nL = np.array([-math.sin(aL), math.cos(aL)])     # normalele spre pana
    A = -eps * (nR + nL) / max(1e-6, 1 + float(nR @ nL))
    R = 600.0
    pts = [A, A + uR[:2] * R, A + np.array([0, -R * 1.6]), A + uL[:2] * R]
    bm = bmesh.new()
    vb = [bm.verts.new((p[0], p[1], -200.0)) for p in pts]; vt = [bm.verts.new((p[0], p[1], 500.0)) for p in pts]
    n = len(pts)
    bm.faces.new(list(reversed(vb))); bm.faces.new(vt)
    for i in range(n): bm.faces.new([vb[i], vb[(i + 1) % n], vt[(i + 1) % n], vt[i]])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = K.bm_to_mesh(bm, name, smooth=False)
    return K.obj(name, me)

def mark_section(o, tol=2e-3):
    """fetele aflate pe cele doua plane de taiere primesc materialul 1"""
    me = o.data
    co = np.zeros(len(me.vertices) * 3, np.float64); me.vertices.foreach_get('co', co); co = co.reshape(-1, 3)
    mw = np.array(o.matrix_local, np.float64) if o.parent is K.ROOT else np.eye(4)
    co = co @ mw[:3, :3].T + mw[:3, 3]
    def on(u):
        cr = co[:, 0] * u[1] - co[:, 1] * u[0]; dt = co[:, 0] * u[0] + co[:, 1] * u[1]
        return (np.abs(cr) < tol) & (dt > -tol)
    oR = on(uR); oL = on(uL)
    mi = np.zeros(len(me.polygons), np.int32); me.polygons.foreach_get('material_index', mi)
    for p in me.polygons:
        vs = list(p.vertices)
        if oR[vs].all() or oL[vs].all(): mi[p.index] = 1
    me.polygons.foreach_set('material_index', mi)
    sm = (mi != 1); me.polygons.foreach_set('use_smooth', sm)
    me.update()

def manifold(o):
    bm = bmesh.new(); bm.from_mesh(o.data)
    bad = sum(1 for e in bm.edges if len(e.link_faces) != 2); n = len(bm.faces); v = bm.calc_volume(signed=True); bm.free()
    return bad, n, round(v, 1)

def volume(o):
    bm = bmesh.new(); bm.from_mesh(o.data); v = bm.calc_volume(signed=True); bm.free(); return v

def in_wedge(o, eps=0.0):
    """cate varfuri ale piesei sunt in pana scoasa"""
    me = o.data; co = np.zeros(len(me.vertices) * 3, np.float64); me.vertices.foreach_get('co', co); co = co.reshape(-1, 3)
    bpy.context.view_layer.update()
    mw = np.array(K.ROOT.matrix_world.inverted() @ o.matrix_world, np.float64)
    co = co @ mw[:3, :3].T + mw[:3, 3]
    nR = np.array([math.sin(aR), -math.cos(aR)]); nL = np.array([-math.sin(aL), math.cos(aL)])
    return int(((co[:, :2] @ nR > -eps + 1e-4) & (co[:, :2] @ nL > -eps + 1e-4)).sum())

def cut(o, eps=0.0, mark=True):
    """scoate pana din piesa. Verifica rezultatul (volumul trebuie sa scada); daca solverul exact nu scoate nimic, incearca altul."""
    if not CUT: return o
    if in_wedge(o, eps) == 0:
        if mark: mark_section(o)
        return o
    v0 = volume(o); keep = o.data.copy(); ok = False
    for solver in ('EXACT', 'MANIFOLD', 'FLOAT'):
        K.boolean(o, wedge_prism(eps), 'DIFFERENCE', solver=solver)
        v1 = volume(o)
        if v1 < v0 * 0.995 and in_wedge(o, eps) == 0: ok = True; break
        print('  !! taiere esuata cu', solver, o.name, round(v0, 3), round(v1, 3), flush=True)
        old = o.data; o.data = keep.copy(); bpy.data.meshes.remove(old)
    bpy.data.meshes.remove(keep)
    if not ok: print('  !!!! PIESA NETAIATA', o.name, flush=True)
    if mark: mark_section(o)
    return o

def finish(o, sharp=32):
    """netezire cu muchii ascutite; fetele de sectiune raman plane"""
    me = o.data
    mi = np.zeros(len(me.polygons), np.int32); me.polygons.foreach_get('material_index', mi)
    me.polygons.foreach_set('use_smooth', np.ones(len(me.polygons), dtype=bool))
    me.set_sharp_from_angle(angle=math.radians(sharp)); me.update()
    return o

def rev(name, prof, mat, sec=None, seg=96, sharp=32):
    """corp de revolutie intreg in jurul axei Z; materialele [exterior, sectiune]"""
    mats = [mat] if sec is None else [mat, sec]
    return K.lathe(name, prof, seg=seg, mat=mats, sharp=sharp)

def drill(targets, a, b, r, seg=28, ext=0.0):
    """gaura cilindrica intre punctele a, b (mm) in toate piesele din targets"""
    a = np.asarray(a, float); b = np.asarray(b, float); d = (b - a) / np.linalg.norm(b - a)
    a2 = a - d * ext; b2 = b + d * ext
    for t in targets:
        c = K.rod('drill', a2, b2, r, seg=seg)
        bpy.context.view_layer.update()
        K.boolean(t, c, 'DIFFERENCE')
        if os.environ.get('DBG'): print('  drill', t.name, manifold(t), flush=True)

def thread(r_maj, r_min, z0, z1, pitch=1.0, up=True):
    """profil in dinti de fierastrau (filet desenat ca santuri inelare)"""
    n = max(1, int(round(abs(z1 - z0) / pitch))); p = (z1 - z0) / n; out = []
    for i in range(n):
        out += [(r_maj, z0 + p * i), (r_maj, z0 + p * (i + 0.35)), (r_min, z0 + p * (i + 0.6)), (r_min, z0 + p * (i + 0.85))]
    out.append((r_maj, z1))
    return out

def helix(name, r, wire, z0, z1, turns, mat, seg=14, per=36, ends=1.0):
    """arc elicoidal cu capete inchise (spire lipite la capete)"""
    L = (z1 - z0) - 2 * wire; act = turns - 2 * ends; pa = (L - 2 * ends * 2 * wire) / max(act, 1e-6)
    def h(k):
        if k < ends: return k * 2 * wire
        if k > turns - ends: return L - (turns - k) * 2 * wire
        return ends * 2 * wire + (k - ends) * pa
    n = int(turns * per) + 1
    P = [(r * math.cos(2 * math.pi * turns * i / (n - 1)), r * math.sin(2 * math.pi * turns * i / (n - 1)), z0 + wire + h(turns * i / (n - 1))) for i in range(n)]
    me = K.tube_mesh(name, np.array(P), wire, seg=seg, caps=True)
    return K.obj(name, me, mat)

def sphere(name, c, r, mat, seg=48):
    bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=seg // 2, radius=r)
    me = K.bm_to_mesh(bm, name, smooth=True, sharp=None)
    return K.obj(name, me, mat, loc=c)

def group(name, objs):
    e = K.empty(name)
    for o in objs:
        o.parent = e
    return e

# ------------------------------------------------------------------ constructia
def build():
    K.init(empty=True)
    M = imats.make_all()
    P = META['pts']; O = {}

    # ---------- duza
    dome = [(1.7 * math.sin(math.radians(a)), 1.7 - 1.7 * math.cos(math.radians(a))) for a in range(0, 61, 3)]
    sac = [(0.55 * math.cos(math.radians(a)), 1.55 - 0.55 * math.sin(math.radians(a))) for a in range(0, 91, 6)]
    z_seat_top = 1.55 + (1.75 - 0.55) / math.tan(math.radians(30))
    noz = dome + [(3.5, 6.2), (3.5, 22.0), (4.3, 22.6), (4.5, 22.9), (4.5, 30.3), (4.7, 30.5), (6.95, 30.5), (7.15, 30.7), (7.15, 39.8), (6.95, 40.0),
                  (2.25, 40.0), (2.0, 39.75), (2.0, 29.6), (3.1, 28.7), (3.1, 26.0), (1.75, 24.4), (1.75, z_seat_top)] + sac
    nozzle = rev('nozzle', noz, M['nozzle'], M['secNozzle'], seg=160, sharp=40)
    HOLES = [math.radians(-30 + 60 * k) for k in range(6)]
    hole_dir = []
    for az in HOLES:
        u = np.array([math.cos(az), math.sin(az), 0.0]); d = u * math.sin(math.radians(75)) - EZ * math.cos(math.radians(75))
        a = np.array([0, 0, 1.45]) + d * 0.2; b = np.array([0, 0, 1.45]) + d * 2.6
        drill([nozzle], a, b, 0.13, seg=16); hole_dir.append(d.tolist())
    drill([nozzle], PR(5.9, 40.6), PR(2.9, 27.3), 0.7)          # canalul inclinat spre camera de presiune
    cut(nozzle); finish(nozzle)
    META['hole_dirs'] = hole_dir; META['hole_az'] = HOLES
    P['tip'] = [0, 0, 0]; P['sac'] = [0, 0, 1.45]; P['seat'] = [0, 0, 2.42]; P['pch'] = [0, 0, 27.3]; P['guide'] = [0, 0, 35.0]

    # ---------- acul (intreg)
    ndl = [(0, 1.72), (0.32, 1.72), (1.05, 2.416), (1.42, 3.142), (1.42, 24.2), (1.985, 25.4)]
    for zg in (32.0, 34.5, 37.0): ndl += [(1.985, zg - 0.25), (1.88, zg - 0.2), (1.88, zg + 0.2), (1.985, zg + 0.25)]
    ndl += [(1.985, 40.8), (1.3, 40.8), (1.3, 42.6), (0, 42.6)]
    needle = rev('needle', ndl, M['steelPol'], seg=96)
    pin = rev('ppin', [(0, 42.6), (2.9, 42.6), (2.9, 43.8), (1.1, 43.8), (1.1, 47.0), (0, 47.0)], M['steel'], seg=64)
    plg = [(0, 47.0), (1.1, 47.0), (1.1, 56.2), (2.14, 57.6)]
    for zg in (122.0, 124.5, 127.0): plg += [(2.14, zg - 0.3), (2.0, zg - 0.22), (2.0, zg + 0.22), (2.14, zg + 0.3)]
    plg += [(2.14, 130.8), (1.95, 131.0), (0, 131.0)]
    plunger = rev('plunger', plg, M['steelGnd'], seg=72)
    spring = helix('nspring', 2.32, 0.45, 43.8, 57.0, 6.5, M['steel'])
    O['NEEDLE'] = group('NEEDLE', [needle, pin, plunger])
    P['needle_top'] = [0, 0, 42.6]; P['spring'] = [0, 0, 50.0]; P['plunger_mid'] = [0, 0, 90.0]

    # ---------- piulita duzei, saiba de cupru
    nutp = [(4.62, 27.0), (6.4, 27.0), (8.6, 29.2), (8.6, 57.6), (8.2, 58.0), (7.66, 58.0), (7.66, 42.0), (7.22, 42.0), (7.22, 30.5), (4.62, 30.5)]
    nut = rev('nut', nutp, M['nut'], M['secNut']); cut(nut); finish(nut)
    washer = rev('washer', [(4.62, 25.2), (7.4, 25.2), (7.4, 26.98), (4.62, 26.98)], M['copper'], M['secCopper']); cut(washer); finish(washer)
    P['washer'] = [0, 0, 26.0]

    # ---------- corpul
    body_p = [(3.3, 40.0), (7.15, 40.0), (7.15, 42.2)] + thread(7.6, 7.25, 42.4, 57.4) + [(7.6, 57.5), (8.5, 58.5), (8.5, 99.5), (7.9, 100.2), (7.9, 105.8), (8.5, 106.5),
              (8.5, 115.5), (11.0, 118.5), (11.0, 139.3)] + thread(10.25, 9.9, 139.6, 146.6) + [(9.9, 146.9), (9.9, 147.6),
              (7.8, 147.6), (7.8, 139.0), (7.55, 139.0), (7.55, 133.5), (4.45, 133.5), (4.45, 132.5), (5.3, 132.5), (5.3, 127.5), (4.45, 127.5), (4.45, 117.5),
              (2.4, 117.5), (2.4, 57.0), (3.3, 57.0)]
    body = rev('body', body_p, M['body'], M['secBody'], seg=120)
    # racordul de inalta presiune (in planul fetei din dreapta)
    TH = math.radians(32)
    c0 = PR(5.0, 130.0); cd = uR * math.cos(TH) + EZ * math.sin(TH)
    conn_p = [(0, 2.0), (8.2, 2.0), (8.2, 12.2), (7.0, 13.4), (7.0, 15.0)] + thread(7.0, 6.55, 15.2, 28.6, 1.3) + [(6.3, 29.3), (6.3, 30.0), (3.2, 30.0), (1.5, 27.6), (0, 27.6)]
    conn = K.lathe('conn', conn_p, seg=72, mat=[M['body'], M['secBody']], sharp=32)
    zq = Vector(cd).to_track_quat('Z', 'Y')
    conn.rotation_mode = 'QUATERNION'; conn.rotation_quaternion = zq; conn.location = Vector(c0)
    bpy.context.view_layer.update()
    # corpul si racordul raman piese separate vizual, dar unite geometric (o singura fata de sectiune)
    trim = K.lathe('trim', [(0, 100.0), (10.6, 100.0), (10.6, 175.0), (0, 175.0)], seg=96, sharp=None)
    bpy.context.view_layer.update()
    K.boolean(conn, trim, 'DIFFERENCE')
    if os.environ.get('DBG'): print('  conn', manifold(conn), 'body', manifold(body), flush=True)
    K.boolean(body, conn, 'UNION')
    if os.environ.get('DBG'): print('  union', manifold(body), flush=True)
    drill([body], c0 - cd * 0.2, c0 + cd * 28.2, 1.5)                                   # alezajul racordului
    drill([body], PR(5.9, 39.0), PR(5.9, 129.0), 0.8)                                   # canalul de inalta presiune spre duza
    drill([body], PL(6.6, 60.0), PL(6.6, 134.0), 0.6)                                   # canalul de scapari (retur)
    drill([body], PL(6.6, 61.0), PL(3.0, 54.0), 0.6)
    cut(body); finish(body)
    if os.environ.get('DBG'): print('  body cut', manifold(body), flush=True)
    P['inlet'] = (c0 + cd * 30).tolist(); P['inlet_mid'] = (c0 + cd * 16).tolist(); P['ann'] = PR(4.9, 130.0).tolist(); P['hp_mid'] = PR(5.9, 85.0).tolist()
    P['body_mid'] = [0, 0, 85.0]; P['leak_mid'] = PL(6.6, 95.0).tolist()
    META['conn'] = {'c0': c0.tolist(), 'd': cd.tolist()}
    # filtrul-tija din racord (intreg)
    ef = K.rod('edgefilter', c0 + cd * 16.5, c0 + cd * 25.5, 1.43, mat=M['steelDark'], seg=32)
    for k in range(4):
        a = k * math.pi / 2 + math.pi / 4
        side = (np.cross(cd, EZ)); side /= np.linalg.norm(side); up = np.cross(side, cd)
        off = (side * math.cos(a) + up * math.sin(a)) * 1.62
        c = K.rod('g', c0 + cd * 16.0 + off, c0 + cd * 26.0 + off, 0.52, seg=16)
        bpy.context.view_layer.update(); K.boolean(ef, c, 'DIFFERENCE')
    finish(ef)
    P['edgefilter'] = (c0 + cd * 21).tolist()

    # ---------- grupul supapei: piesa supapei, inel de etansare, bila, surub de strangere
    z_ball = 136.02 + 0.85 / math.sin(math.radians(45))
    vp = [(2.15, 118.0), (4.4, 118.0), (4.4, 133.5), (7.5, 133.5), (7.5, 138.6), (1.6, 138.6), (1.6, 137.62), (0.38, 136.4), (0.38, 133.3), (2.15, 132.4)]
    valve = rev('valve', vp, M['steelGnd'], M['secValve'], seg=96)
    drill([valve], PR(4.6, 130.5), PR(1.9, 131.85), 0.3, seg=16)                         # droselul de alimentare (Z)
    drill([valve], PL(6.6, 132.0), PL(6.6, 140.0), 0.6)
    cut(valve); finish(valve)
    seal = rev('hpseal', [(2.45, 117.5), (4.4, 117.5), (4.4, 118.0), (2.45, 118.0)], M['seal'], M['secSeal'], seg=64); cut(seal)
    ball = sphere('ball', (0, 0, z_ball), 0.85, M['ball'])
    screw = rev('screw', [(3.4, 138.8), (3.6, 138.6), (7.75, 138.6), (7.75, 145.0), (3.6, 145.0), (3.4, 144.8)], M['steel'], M['secScrew'], seg=96)
    drill([screw], PL(6.6, 138.0), PL(6.6, 146.0), 0.6)
    cut(screw); finish(screw)
    P['ball'] = [0, 0, z_ball]; P['cc'] = [0, 0, 131.7]; P['athr'] = [0, 0, 134.8]; P['zthr'] = PR(3.3, 131.2).tolist(); P['valve'] = [0, 0, 126.0]

    # ---------- armatura (disc taiat + tija intreaga), arcul supapei
    arm_pin = rev('armpin', [(0, z_ball + 0.87), (0.75, z_ball + 0.87), (0.75, 151.6), (1.6, 151.6), (1.6, 152.4), (0, 152.4)], M['steelPol'], seg=48)
    arm = rev('armplate', [(0.78, 145.6), (6.9, 145.6), (6.9, 147.2), (0.78, 147.2)], M['steel'], M['secArm'], seg=96)
    for az in (aR, aL, aR + math.pi * 2 / 3, aR + math.pi / 3, aR + math.pi):
        u = np.array([math.cos(az), math.sin(az), 0.0])
        drill([arm], u * 4.2 + EZ * 145.0, u * 4.2 + EZ * 148.0, 0.75, seg=20)
    cut(arm); finish(arm)
    O['ARM'] = group('ARM', [arm_pin, arm])
    O['BALL'] = group('BALL', [ball])
    vspring = helix('vspring', 1.32, 0.3, 152.4, 160.8, 7.0, M['steel'], seg=10, per=28)
    P['arm'] = [0, 0, 146.4]

    # ---------- electromagnetul: miez, bobina, carcasa bobinei, piulita, capac din plastic cu conector si stut de retur
    core_p = [(2.0, 147.6), (4.2, 147.6), (4.2, 156.5), (7.9, 156.5), (7.9, 147.6), (9.6, 147.6), (9.6, 158.0), (8.0, 158.0), (8.0, 163.0), (1.2, 163.0), (1.2, 161.0), (2.0, 161.0)]
    core = rev('core', core_p, M['steelDark'], M['secCore']); cut(core); finish(core)
    coil = rev('coil', [(4.42, 147.95), (7.68, 147.95), (7.68, 156.2), (4.42, 156.2)], M['copper'], M['secCoil'], seg=96); cut(coil)
    bob = rev('bobbin', [(4.22, 147.7), (4.4, 147.7), (4.4, 156.22), (7.7, 156.22), (7.7, 147.7), (7.88, 147.7), (7.88, 156.47), (4.22, 156.47)], M['plasticG'], M['secPlastic'], seg=96); cut(bob)
    mn_p = [(10.3, 139.4), (12.4, 139.4), (12.6, 139.6), (12.6, 159.6), (12.4, 159.8), (8.1, 159.8), (8.1, 158.05), (9.66, 158.05), (9.66, 147.65), (10.3, 147.65)]
    magnut = rev('magnut', mn_p, M['zinc'], M['secMagNut'], seg=120)
    hexp = K.lathe('hex', [(0, 142.5), (13.9, 142.5), (13.9, 157.0), (0, 157.0)], seg=6, sharp=None)
    ring_lo = K.lathe('rlo', [(0, 139.0), (12.6, 139.0), (12.6, 142.6), (0, 142.6)], seg=96, sharp=None)
    ring_hi = K.lathe('rhi', [(0, 156.9), (12.6, 156.9), (12.6, 160.2), (0, 160.2)], seg=96, sharp=None)
    bpy.context.view_layer.update()
    K.boolean(hexp, ring_lo, 'UNION'); K.boolean(hexp, ring_hi, 'UNION')
    K.boolean(magnut, hexp, 'INTERSECT')
    cut(magnut); finish(magnut)
    cap_p = [(8.05, 159.85), (9.4, 159.85), (9.4, 169.6), (8.2, 171.5), (3.4, 171.5), (3.4, 175.2), (2.7, 175.9), (2.7, 177.0), (2.45, 177.25), (2.45, 177.9), (2.7, 178.15), (2.7, 179.2), (2.4, 179.5),
             (1.2, 179.5), (1.2, 163.05), (8.05, 163.05)]
    cap = rev('cap', cap_p, M['plastic'], M['secPlastic'], seg=96)
    # conectorul electric (in spate-stanga, nu atinge planele de taiere)
    az = math.radians(140); u = np.array([math.cos(az), math.sin(az), 0.0]); tilt = math.radians(24)
    cdir = u * math.cos(tilt) + EZ * math.sin(tilt)
    cb = K.box('connbox', (13.0, 10.0, 21.0), mat=M['plastic'], bev=1.6, seg=3)
    q = Vector(cdir).to_track_quat('Z', 'Y'); cb.rotation_mode = 'QUATERNION'; cb.rotation_quaternion = q; cb.location = Vector(u * 15.5 + EZ * 169.5)
    hole = K.box('connhole', (10.2, 7.2, 12.0)); hole.rotation_mode = 'QUATERNION'; hole.rotation_quaternion = q; hole.location = Vector(u * 15.5 + EZ * 169.5 + cdir * 6.0)
    bpy.context.view_layer.update(); K.boolean(cb, hole, 'DIFFERENCE')
    for s in (-1, 1):
        side = np.cross(cdir, EZ); side /= np.linalg.norm(side)
        pn = K.box('cpin', (0.8, 2.2, 7.0), mat=M['brass']); pn.rotation_mode = 'QUATERNION'; pn.rotation_quaternion = q
        pn.location = Vector(u * 15.5 + EZ * 169.5 + cdir * 4.0 + side * 2.4 * s)
    cut(cap); finish(cap)
    P['coil'] = [0, 0, 152.0]; P['conn_el'] = (u * 15.5 + EZ * 169.5 + cdir * 10).tolist(); P['ret'] = [0, 0, 179.5]; P['top'] = [0, 0, 180.0]

    # ---------- motorina (volume): inalta presiune / camera de comanda / sac / joasa presiune
    E = 0.03
    def fl(o):
        cut(o, eps=E, mark=False); o.visible_shadow = False; return o
    f_in = fl(K.rod('f_inlet', c0 - cd * 0.5, c0 + cd * 27.7, 1.47, mat=M['fuelHP'], seg=28))
    f_ann = fl(rev('f_ann', [(4.47, 127.55), (5.27, 127.55), (5.27, 132.45), (4.47, 132.45)], M['fuelHP'], seg=72))
    f_hp = fl(K.rod('f_hp', PR(5.9, 39.9), PR(5.9, 128.6), 0.78, mat=M['fuelHP'], seg=24))
    f_nzin = fl(K.rod('f_nzin', PR(5.9, 40.3), PR(2.95, 27.5), 0.68, mat=M['fuelHP'], seg=24))
    f_nz = fl(rev('f_nz', [(0, 2.47), (1.07, 2.47), (1.73, 3.64), (1.73, 24.38), (3.08, 26.02), (3.08, 28.68), (1.98, 29.5), (0, 29.5)], M['fuelHP'], seg=72))
    f_z = fl(K.rod('f_z', PR(4.5, 130.55), PR(2.05, 131.78), 0.28, mat=M['fuelHP'], seg=16))
    f_cc = fl(rev('f_cc', [(0, 130.2), (2.13, 130.2), (2.13, 132.4), (0.36, 133.3), (0.36, 136.4), (0.57, 136.6), (0, 136.6)], M['fuelCC'], seg=64))
    sacp = [(0, 1.03)] + [(0.53 * math.cos(math.radians(a)), 1.55 - 0.52 * math.sin(math.radians(a))) for a in range(90, -1, -6)] + [(1.04, 2.44), (0, 2.44)]
    f_sac = fl(rev('f_sac', sacp, M['fuelSac'], seg=48))
    sac_objs = [f_sac]
    for d in hole_dir:
        d = np.array(d); h = K.rod('f_hole', np.array([0, 0, 1.45]) + d * 0.3, np.array([0, 0, 1.45]) + d * 1.78, 0.115, mat=M['fuelSac'], seg=12)
        if CUT and (d[0] * uR[1] - d[1] * uR[0]) > 1e-3 and (d[0] * uL[1] - d[1] * uL[0]) < -1e-3:
            bpy.data.objects.remove(h); continue                      # jetul din pana scoasa
        sac_objs.append(fl(h))
    f_spr = fl(rev('f_spr', [(0, 40.05), (3.27, 40.05), (3.27, 56.97), (2.38, 56.97), (2.38, 117.45), (0, 117.45)], M['fuelLP'], seg=72))
    f_arm = fl(rev('f_arm', [(0, 136.68), (0.63, 136.68), (1.58, 137.64), (1.58, 138.62), (3.38, 138.62), (3.38, 145.02), (7.77, 145.02), (7.77, 147.58), (1.98, 147.58),
                             (1.98, 160.98), (1.18, 160.98), (1.18, 179.3), (0, 179.3)], M['fuelLP'], seg=72))
    f_leak = fl(K.rod('f_leak', PL(6.6, 60.2), PL(6.6, 145.0), 0.58, mat=M['fuelLP'], seg=20))
    f_leak2 = fl(K.rod('f_leak2', PL(6.6, 61.0), PL(3.2, 54.4), 0.58, mat=M['fuelLP'], seg=20))
    O['FUEL_HP'] = group('FUEL_HP', [f_in, f_ann, f_hp, f_nzin, f_nz, f_z]); O['FUEL_CC'] = group('FUEL_CC', [f_cc]); O['FUEL_SAC'] = group('FUEL_SAC', sac_objs)
    O['FUEL_LP'] = group('FUEL_LP', [f_spr, f_arm, f_leak, f_leak2])
    O['STATIC'] = group('STATIC', [nozzle, nut, washer, body, ef, valve, seal, screw, core, coil, bob, magnut, cap, cb, spring, vspring] +
                        [o for o in bpy.data.objects if o.name.startswith('cpin')])

    # ---------- straturi de uzura / rugina (suprafete subtiri peste piese; ascunse in starea curata)
    def skin(name, prof, mat, cutw=False, seg=96):
        if cutw and CUT:
            o = K.lathe(name, prof, seg=seg, mat=mat, sharp=None, closed=False, deg=360.0 - WEDGE, a0=math.degrees(aR))
        else:
            o = K.lathe(name, prof, seg=seg, mat=mat, sharp=None, closed=False)
        o.visible_shadow = False; o.hide_render = True
        return o
    g = 0.012
    d_nseat = skin('d_nseat', [(0.56, 1.56 + g), (1.75 - g, z_seat_top), (1.75 - g, 6.5)], M['eroded'], cutw=True)                     # scaunul din duza
    d_ntip = skin('d_ntip', [(0.33, 1.72 - g), (1.05 + g, 2.416 - g), (1.42 + g, 3.142), (1.42 + g, 6.5)], M['eroded'])                  # varful acului
    d_nguide = skin('d_nguide', [(1.985 + g, 25.5), (1.985 + g, 40.7)], M['scored'])                                                 # ghidajul acului
    d_nshaft = skin('d_nshaft', [(1.42 + g, 6.5), (1.42 + g, 24.2)], M['rust'])                                                      # tija acului (rugina)
    d_bguide = skin('d_bguide', [(2.0 - g, 29.7), (2.0 - g, 39.7)], M['scored'], cutw=True)                                          # alezajul de ghidare din duza
    d_vseat = skin('d_vseat', [(0.38 + g, 136.42), (1.6 - g, 137.62 + g * 0.5)], M['eroded'], cutw=True)                              # scaunul bilei
    d_ball = sphere('d_ball', (0, 0, z_ball), 0.85 + g, M['eroded']); d_ball.visible_shadow = False; d_ball.hide_render = True
    d_pguide = skin('d_pguide', [(2.14 + g, 118.5), (2.14 + g, 130.7)], M['scored'])                                                 # ghidajul tijei de comanda
    for o in (d_ntip, d_nguide, d_nshaft, d_pguide): o.parent = O['NEEDLE']
    d_ball.parent = O['BALL']
    O['DMG'] = group('DMG', [d_nseat, d_bguide, d_vseat])
    META['dmg'] = ['d_nseat', 'd_ntip', 'd_nguide', 'd_nshaft', 'd_bguide', 'd_vseat', 'd_ball', 'd_pguide']

    # ---------- motorul din jur: chiulasa, piston, camasa cilindrului (pentru cadrele cu camera de ardere)
    DECK = 2.6
    head_p = [(3.78, DECK), (52.0, DECK), (52.0, 96.0), (9.4, 96.0), (9.4, 25.2), (4.72, 25.2), (4.72, 22.4), (3.78, 21.6)]
    head = rev('head', head_p, M['castAlu'], M['secAlu'], seg=120); cut(head); finish(head)
    TDC = 1.7
    def piston_prof(top):
        b = [(0, -2.2), (3.0, -2.6), (7.0, -6.0), (11.0, -11.5), (14.5, -13.6), (18.5, -13.2), (21.6, -10.6), (22.9, -7.0), (22.4, -3.2), (21.4, -0.6), (21.6, 0.0)]
        p = [(r, z + top) for r, z in b] + [(40.3, top), (40.4, top - 0.4)]
        for zr in (-6.0, -10.5, -15.5): p += [(40.4, top + zr + 1.1), (37.2, top + zr + 1.1), (37.2, top + zr - 1.1), (40.4, top + zr - 1.1)]
        p += [(40.4, top - 52.0), (34.0, top - 52.0), (34.0, top - 26.0), (30.0, top - 21.0), (0, top - 21.0)]
        return p
    piston = rev('piston', piston_prof(TDC), M['pistonAlu'], M['secPiston'], seg=120); cut(piston); finish(piston)
    rings = []
    for zr in (-6.0, -10.5, -15.5):
        rg = rev('ring', [(37.4, TDC + zr - 0.95), (40.46, TDC + zr - 0.95), (40.46, TDC + zr + 0.95), (37.4, TDC + zr + 0.95)], M['steelDark'], M['secIron'], seg=120); cut(rg); rings.append(rg)
    liner = rev('liner', [(40.5, DECK - 1.2), (52.0, DECK - 1.2), (52.0, -80.0), (40.5, -80.0)], M['iron'], M['secIron'], seg=120); cut(liner); finish(liner)
    gasket = rev('gasket', [(41.2, DECK - 1.2), (52.0, DECK - 1.2), (52.0, DECK), (41.2, DECK)], M['steelDark'], M['secScrew'], seg=120); cut(gasket)
    O['PISTON'] = group('PISTON', [piston] + rings)
    O['ENGINE'] = group('ENGINE', [head, liner, gasket])
    META['engine'] = {'deck': DECK, 'tdc': TDC, 'bore': 40.5}
    P['bowl_lip'] = [0, 0, TDC - 3.0]

    # ---------- trasee pentru particule (mm)
    PT = META['paths']
    PT['hp_in'] = [(c0 + cd * s).tolist() for s in (30, 22, 12, 3)] + [PR(5.3, 130.4).tolist()]
    PT['hp_down'] = [PR(5.6, 129.5).tolist(), PR(5.9, 127.0).tolist(), PR(5.9, 100.0).tolist(), PR(5.9, 60.0).tolist(), PR(5.9, 41.0).tolist(), PR(4.6, 34.5).tolist(), PR(2.95, 27.6).tolist()]
    PT['nz_down_R'] = [PR(2.7, 27.3).tolist(), PR(1.6, 24.0).tolist(), PR(1.58, 14.0).tolist(), PR(1.58, 5.0).tolist(), PR(1.25, 3.0).tolist(), PR(0.8, 2.1).tolist(), PR(0.35, 1.5).tolist()]
    PT['nz_down_L'] = [PL(2.7, 27.3).tolist(), PL(1.6, 24.0).tolist(), PL(1.58, 14.0).tolist(), PL(1.58, 5.0).tolist(), PL(1.25, 3.0).tolist(), PL(0.8, 2.1).tolist(), PL(0.35, 1.5).tolist()]
    PT['z_in'] = [PR(5.0, 130.3).tolist(), PR(4.5, 130.55).tolist(), PR(2.1, 131.75).tolist(), PR(1.0, 131.9).tolist()]
    PT['a_out'] = [[0, 0, 131.8], [0, 0, 133.4], [0, 0, 136.3]]
    return O

if __name__ == '__main__':
    out = sys.argv[-1] if sys.argv[-1].endswith('.blend') else os.path.join(HERE, 'out', 'inj_cut.blend' if CUT else 'inj_full.blend')
    O = build()
    json.dump(META, open(out.replace('.blend', '.json'), 'w'), indent=1)
    bpy.ops.wm.save_as_mainfile(filepath=out)
    n = sum(len(o.data.polygons) for o in bpy.data.objects if o.type == 'MESH')
    print('SAVED', out, 'poligoane', n, flush=True)
