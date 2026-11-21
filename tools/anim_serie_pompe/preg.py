# Regulatorul de debit al pompei (unitatea de dozare), in sectiune: bobina, armatura, pistonasul in bucsa lui, arcul, sita de la intrare.
# Desen schematic, cu cursa pistonasului marita ca sa se vada. Reper: axa Z, varful (iesirea spre pompa) la z = 0, bobina sus. Aceeasi pana ca la injector (spre -Y).
#   venv_bpy/bin/python preg.py   ->  blend/reg.blend + blend/reg.json
# Piesele mobile stau sub golul R_MOVE (location z = s, 0 = inchis ... 4.4 = deschis); lichidul si arcul se intind din starea placii (pshots.reg_fn).
import bpy, bmesh, math, json, os, sys
import numpy as np
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, '/home/claude/w/inj')
import kit as K, imats, irig
from model import rev, cut, finish, drill, thread, helix, group, PR, PL, uR, uL, EZ, aR, aL, WEDGE

META = {'pts': {}, 'paths': {}}
ZP = 8.9            # inaltimea ferestrelor din bucsa

UB_A = math.radians(24)                                     # mufa pleaca spre dreapta, putin spre spate
def connector(M, pre):
    ub = np.array([math.cos(UB_A), math.sin(UB_A), 0.0])
    conn = K.box(pre + 'conn', (17.0, 12.0, 9.6), c=tuple(ub * 15.0 + EZ * 58.2), mat=M['plastic'], bev=1.4); conn.rotation_euler = (0, 0, UB_A)
    lip = K.box(pre + 'lip', (3.2, 14.2, 11.8), c=tuple(ub * 23.2 + EZ * 58.2), mat=M['plastic'], bev=0.9); lip.rotation_euler = (0, 0, UB_A)
    return conn, lip

def mesh_mat(name, cells=64, mz=1.35, wire=0.17):
    """plasa sitei: fire deschise si ochiuri inchise, desenate din unghi si inaltime"""
    m = imats.metal(name, 0xd2d7de, 0.4, metal=0.9)
    N = m.node_tree.nodes; L = m.node_tree.links; b = N['Principled BSDF']
    tc = N.new('ShaderNodeTexCoord'); sx = N.new('ShaderNodeSeparateXYZ'); L.new(tc.outputs['Object'], sx.inputs[0])
    at = N.new('ShaderNodeMath'); at.operation = 'ARCTAN2'; L.new(sx.outputs['Y'], at.inputs[0]); L.new(sx.outputs['X'], at.inputs[1])
    def band(src, mult):
        a = N.new('ShaderNodeMath'); a.operation = 'MULTIPLY'; a.inputs[1].default_value = mult; L.new(src, a.inputs[0])
        f = N.new('ShaderNodeMath'); f.operation = 'FRACT'; L.new(a.outputs[0], f.inputs[0])
        d = N.new('ShaderNodeMath'); d.operation = 'SUBTRACT'; d.inputs[1].default_value = 0.5; L.new(f.outputs[0], d.inputs[0])
        ab = N.new('ShaderNodeMath'); ab.operation = 'ABSOLUTE'; L.new(d.outputs[0], ab.inputs[0]); return ab.outputs[0]
    u = band(at.outputs[0], cells / (2 * math.pi)); v = band(sx.outputs['Z'], mz)
    mx = N.new('ShaderNodeMath'); mx.operation = 'MAXIMUM'; L.new(u, mx.inputs[0]); L.new(v, mx.inputs[1])
    mr = N.new('ShaderNodeMapRange'); mr.interpolation_type = 'SMOOTHSTEP'
    mr.inputs['From Min'].default_value = 0.5 - wire - 0.035; mr.inputs['From Max'].default_value = 0.5 - wire + 0.035
    L.new(mx.outputs[0], mr.inputs['Value'])
    mc = N.new('ShaderNodeMix'); mc.data_type = 'RGBA'
    mc.inputs[6].default_value = K.srgb(0x3d3524); mc.inputs[7].default_value = K.srgb(0xd2d7de)
    L.new(mr.outputs['Result'], mc.inputs[0]); L.new(mc.outputs[2], b.inputs['Base Color'])
    L.new(mr.outputs['Result'], b.inputs['Metallic'])
    return m

def whole(M):
    """regulatorul intreg (nesectionat), pentru cadrele cu sita vazuta din afara"""
    sl = [(2.2, 0.0), (6.2, 0.0), (7.0, 0.8), (7.0, 5.0), (6.4, 5.0), (6.4, 15.4), (7.0, 15.4), (7.0, 19.0), (5.8, 19.0), (5.8, 21.6), (7.0, 21.6), (7.0, 25.0), (12.0, 25.0), (12.0, 31.0), (0, 31.0), (0, 2.0), (2.2, 2.0)]
    P = [rev('w_sleeve', sl, M['body'], seg=120), rev('w_mesh', [(7.05, 5.7), (7.45, 5.7), (7.45, 14.7), (7.05, 14.7)], M['mesh'], seg=128),
         rev('w_ringA', [(6.42, 5.02), (7.7, 5.02), (7.7, 5.9), (6.42, 5.9)], M['brass'], seg=96), rev('w_ringB', [(6.42, 14.5), (7.7, 14.5), (7.7, 15.38), (6.42, 15.38)], M['brass'], seg=96),
         rev('w_oring', [(7.05 + 1.25 * math.cos(math.radians(a)), 20.3 + 1.25 * math.sin(math.radians(a))) for a in range(0, 360, 15)], M['rubber'], seg=96),
         rev('w_can', [(0, 31.0), (13.2, 31.0), (13.2, 52.0), (12.7, 52.5), (0, 52.5)], M['zinc'], seg=120),
         rev('w_cap', [(0, 52.5), (10.4, 52.5), (10.4, 62.2), (8.8, 64.0), (0, 64.0)], M['plastic'], seg=96)]
    for o in P: finish(o)
    P += list(connector(M, 'w_'))
    g = group('R_FULL', P)
    for o in P: o.hide_render = True
    return g

def build():
    K.init(empty=True)
    M = imats.make_all(); P = META['pts']
    M['mesh'] = mesh_mat('mesh'); M['secMesh'] = imats.sec('secMesh', 0x8d939b, 0.5, 1.0, 0.3)
    M['spool'] = imats.metal('spool', 0xa9bcd6, 0.2, metal=1.0); M['secSpool'] = imats.sec('secSpool', 0x7f9cc4, 1.0, -1.0, 0.26)
    # ---------- bucsa (corpul supapei) cu flansa
    sl = [(2.2, 0.0), (6.2, 0.0), (7.0, 0.8), (7.0, 5.0), (6.4, 5.0), (6.4, 15.4), (7.0, 15.4), (7.0, 19.0), (5.8, 19.0), (5.8, 21.6), (7.0, 21.6), (7.0, 25.0),
          (12.0, 25.0), (12.0, 31.0), (5.2, 31.0), (5.2, 29.0), (3.0, 29.0), (3.0, 2.0), (2.2, 2.0)]
    sleeve = rev('r_sleeve', sl, M['body'], M['secBody'], seg=120)
    for k in range(3):
        az = aR + k * 2 * math.pi / 3; u = np.array([math.cos(az), math.sin(az), 0.0])
        drill([sleeve], u * 2.0 + EZ * ZP, u * 8.0 + EZ * ZP, 1.3, seg=20)
    cut(sleeve); finish(sleeve)
    # ---------- sita de la intrare (plasa fina intre doua inele) si garnitura
    mesh = rev('r_mesh', [(7.05, 5.7), (7.45, 5.7), (7.45, 14.7), (7.05, 14.7)], M['mesh'], M['secMesh'], seg=96); cut(mesh); finish(mesh)
    ring_a = rev('r_ringA', [(6.42, 5.02), (7.7, 5.02), (7.7, 5.9), (6.42, 5.9)], M['brass'], M['secCopper'], seg=96); cut(ring_a)
    ring_b = rev('r_ringB', [(6.42, 14.5), (7.7, 14.5), (7.7, 15.38), (6.42, 15.38)], M['brass'], M['secCopper'], seg=96); cut(ring_b)
    oring = rev('r_oring', [(7.05 + 1.25 * math.cos(math.radians(a)), 20.3 + 1.25 * math.sin(math.radians(a))) for a in range(0, 360, 15)], M['rubber'], M['secRubber'], seg=96); cut(oring)
    # ---------- pistonasul (pahar cu gura in jos), tija si armatura: piesele mobile
    sp = [(1.9, 6.0), (2.95, 6.0), (2.95, 12.0), (2.75, 12.2), (2.75, 14.0), (2.95, 14.2), (2.95, 21.0), (0, 21.0), (0, 19.0), (1.9, 19.0)]
    spool = rev('r_spool', sp, M['spool'], M['secSpool'], seg=96); cut(spool); finish(spool)
    pin = rev('r_pin', [(0, 21.0), (1.0, 21.0), (1.0, 33.4), (0, 33.4)], M['steelGnd'], seg=48)
    arm = rev('r_arm', [(0, 33.4), (4.0, 33.4), (4.42, 33.8), (4.42, 43.0), (4.0, 43.4), (0, 43.4)], M['steelGnd'], seg=72)
    move = group('R_MOVE', [spool, pin, arm])
    spring = helix('r_spring', 1.32, 0.27, 2.1, 19.0, 9.0, M['steel'])
    # ---------- electromagnetul: polul de jos, tubul armaturii, carcasa bobinei, bobina, carcasa de tabla, dopul de sus, mufa
    pole = rev('r_pole', [(1.25, 29.05), (5.15, 29.05), (5.15, 31.0), (11.45, 31.0), (11.45, 32.9), (1.25, 32.9)], M['steelDark'], M['secCore'], seg=96); cut(pole); finish(pole)
    tubec = rev('r_tube', [(4.6, 32.9), (5.15, 32.9), (5.15, 48.6), (4.6, 48.6)], M['zinc'], M['secMagNut'], seg=72); cut(tubec)
    bob = rev('r_bob', [(5.2, 32.95), (11.4, 32.95), (11.4, 34.0), (5.9, 34.0), (5.9, 46.0), (11.4, 46.0), (11.4, 47.0), (5.2, 47.0)], M['plasticG'], M['secPlastic'], seg=96); cut(bob)
    coil = rev('r_coil', [(5.95, 34.05), (11.35, 34.05), (11.35, 45.95), (5.95, 45.95)], M['copper'], M['secCoil'], seg=96); cut(coil)
    plug = rev('r_plug', [(0, 48.6), (5.15, 48.6), (5.15, 47.05), (11.45, 47.05), (11.45, 50.95), (0, 50.95)], M['steelDark'], M['secCore'], seg=96); cut(plug); finish(plug)
    can = rev('r_can', [(11.5, 31.0), (13.2, 31.0), (13.2, 52.0), (12.7, 52.5), (0, 52.5), (0, 51.0), (11.5, 51.0)], M['zinc'], M['secMagNut'], seg=120); cut(can); finish(can)
    CAPP = [(0, 52.5), (10.4, 52.5), (10.4, 62.2), (8.8, 64.0), (0, 64.0)]
    cap = rev('r_cap', CAPP, M['plastic'], M['secPlastic'], seg=96); cut(cap); finish(cap)
    conn, lip = connector(M, 'r_')
    # ---------- motorina (joasa presiune): inelul de sub sita, ferestrele, golul de sub pistonas si interiorul lui
    E = 0.06
    def fl(o):
        cut(o, eps=E, mark=False); o.visible_shadow = False; return o
    f_ring = fl(rev('r_fRing', [(6.45, 5.95), (7.0, 5.95), (7.0, 14.45), (6.45, 14.45)], M['fuelLP'], seg=96))
    ports = []
    for k in (0, 2):                                   # ferestrele aflate in planele fetelor
        az = aR + k * 2 * math.pi / 3; u = np.array([math.cos(az), math.sin(az), 0.0])
        ports.append(fl(K.rod('r_fPort', u * 3.02 + EZ * ZP, u * 6.5 + EZ * ZP, 1.25, mat=M['fuelLP'], seg=20)))
    f_bore = fl(rev('r_fBore', [(0, 0.0), (2.15, 0.0), (2.15, 2.0), (1.85, 2.0), (1.85, 18.9), (0, 18.9)], M['fuelLP'], seg=64))
    f_under = fl(rev('r_fUnder', [(1.9, 2.02), (2.95, 2.02), (2.95, 5.98), (1.9, 5.98)], M['fuelLP'], seg=64))
    group('R_BODY', [sleeve, mesh, ring_a, ring_b, oring, spring, pole, tubec, bob, coil, plug, can, cap, conn, lip])
    group('R_FUEL', [f_ring, f_bore, f_under] + ports)
    whole(M)
    # ---------- puncte si trasee (mm)
    P['tip'] = [0, 0, 0]; P['spool'] = PR(2.95, 16.5).tolist(); P['spoolL'] = PL(2.95, 16.5).tolist(); P['rim'] = PR(2.95, 6.0).tolist(); P['port'] = PR(4.8, ZP).tolist(); P['portL'] = PL(4.8, ZP).tolist()
    P['mesh'] = PR(7.45, 10.0).tolist(); P['meshL'] = PL(7.45, 10.0).tolist(); P['spring'] = [0, 0, 11.0]; P['coil'] = PR(8.6, 40.0).tolist(); P['coilL'] = PL(8.6, 40.0).tolist()
    P['arm'] = [0, 0, 38.5]; P['conn'] = [15.0 * math.cos(UB_A), 15.0 * math.sin(UB_A), 58.2]; P['oring'] = PR(8.3, 20.3).tolist(); P['gap'] = PR(2.98, 17.5).tolist(); P['gapL'] = PL(2.98, 17.5).tolist()
    PT = META['paths']
    for nm, PP in (('in_R', PR), ('in_L', PL)):
        PT[nm] = [PP(17.0, 11.5).tolist(), PP(9.0, 9.6).tolist(), PP(6.6, ZP).tolist(), PP(3.3, ZP).tolist(), PP(2.3, 6.6).tolist(), PP(1.2, 3.6).tolist(), [0, 0, 0.6], [0, 0, -9.0]]
        PT[nm.replace('in', 'stop')] = [PP(17.0, 11.5).tolist(), PP(9.0, 9.6).tolist(), PP(6.6, ZP).tolist(), PP(3.4, ZP).tolist()]
    PT['gap_R'] = [PR(2.98, 21.0).tolist(), PR(2.98, 6.0).tolist()]; PT['gap_L'] = [PL(2.98, 21.0).tolist(), PL(2.98, 6.0).tolist()]
    META['wedge'] = WEDGE; META['uR'] = uR.tolist(); META['uL'] = uL.tolist(); META['zp'] = ZP; META['stroke'] = 4.4

if __name__ == '__main__':
    out = os.path.join(HERE, 'blend', 'reg.blend')
    build()
    for g in ('R_BODY', 'R_MOVE', 'R_FUEL'): print(g, len(bpy.data.objects[g].children))
    json.dump(META, open(out.replace('.blend', '.json'), 'w'), indent=1)
    irig.setup_world(0.3); irig.setup_camera(); irig.setup_render(1080, 1920, 32, 0.0)
    bpy.ops.wm.save_as_mainfile(filepath=out, compress=True)
    print('SAVED', out, len(bpy.data.objects), 'obiecte', flush=True)
