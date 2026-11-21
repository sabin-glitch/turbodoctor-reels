# Doua piese in sectiune pentru seria pompelor (desene schematice, cu jocurile marite ca sa se vada):
#   blend/qc.blend  - cupla rapida de pe conducta de joasa presiune: stutul cu guler intrat in cupla, doua garnituri (bune sau imbatranite), furtunul
#   blend/hpe.blend - capatul conductei de inalta presiune: conul conductei asezat in scaunul racordului, strans de piulita olandeza (con bun sau deformat)
#   venv_bpy/bin/python pconn.py
# Reper: axa Z, aceeasi pana ca la injector (spre -Y). Motorina urca (de jos, de la rezervor, in sus, spre pompa).
import bpy, math, json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, '/home/claude/w/inj')
import kit as K, imats, irig
from model import rev, cut, finish, thread, group, PR, PL, uR, uL, EZ, aR, aL, WEDGE

def ring(c, rr, rz, step=15, notch=None):
    """profilul unei garnituri: elipsa in jurul lui c = (r, z); notch = adancimea crapaturii de pe partea dinspre ax (0..1)"""
    out = []
    for a in range(0, 360, step):
        if notch and a == 180: out += [(c[0] - rr * 0.985, c[1] + 0.16), (c[0] - rr * (1 - 2 * notch), c[1]), (c[0] - rr * 0.985, c[1] - 0.16)]; continue
        out.append((c[0] + rr * math.cos(math.radians(a)), c[1] + rz * math.sin(math.radians(a))))
    return out

def save(name, META, groups):
    out = os.path.join(HERE, 'blend', name + '.blend')
    for g in groups: print(' ', g, len(bpy.data.objects[g].children))
    META.update(wedge=WEDGE, uR=uR.tolist(), uL=uL.tolist())
    json.dump(META, open(out.replace('.blend', '.json'), 'w'), indent=1)
    irig.setup_world(0.3); irig.setup_camera(); irig.setup_render(1080, 1920, 32, 0.0)
    bpy.ops.wm.save_as_mainfile(filepath=out, compress=True)
    print('SAVED', out, len(bpy.data.objects), 'obiecte', flush=True)

# ------------------------------------------------------------------ cupla rapida
BARB = []
for z0 in (-44.0, -39.0, -34.0): BARB += [(4.4, z0), (5.3, z0 + 3.4), (4.4, z0 + 3.4)]
def build_qc():
    K.init(empty=True); M = imats.make_all(); META = {'pts': {}, 'paths': {}}; P = META['pts']
    M['qbody'] = imats.metal('qbody', 0x2b2e34, 0.45, metal=0.0, coat=0.15, bevel=0.2); M['secQ'] = imats.sec('secQ', 0x69707b, 1.5, 1.0, 0.2, metal=0.0, rough=0.7)
    M['oring'] = imats.metal('oring', 0x2f9a5c, 0.55, metal=0.0); M['secOring'] = imats.sec('secOring', 0x2f9a5c, 1.0, 1.0, 0.0, k=0.95, metal=0.0, rough=0.7, plain=True)
    M['oringOld'] = imats.metal('oringOld', 0x5a4326, 0.8, metal=0.0, bump=(9, 0.5)); M['secOringOld'] = imats.sec('secOringOld', 0x7b5b33, 1.0, 1.0, 0.0, k=0.95, metal=0.0, rough=0.85, plain=True)
    M['clip'] = imats.metal('clip', 0x7f9fc9, 0.45, metal=0.0, coat=0.2); M['secClip'] = imats.sec('secClip', 0x7f9fc9, 1.0, 1.0, 0.0, k=0.8, metal=0.0, rough=0.6, plain=True)
    M['spacer'] = imats.metal('spacer', 0x9aa0a8, 0.55, metal=0.0); M['secSpacer'] = imats.sec('secSpacer', 0xa9afb7, 1.0, 1.0, 0.0, k=0.8, metal=0.0, rough=0.7, plain=True)
    BODY = [(3.0, -46.0), (4.4, -46.0)] + BARB + [(4.4, -13.0), (8.5, -11.0), (8.5, 24.0), (6.3, 24.0), (6.3, 11.5), (6.1, 11.5), (6.1, 1.5), (4.1, 1.5), (4.1, -4.0), (3.0, -4.0)]
    SPIG = [(3.0, -2.0), (3.6, -2.0), (4.0, -1.2), (4.0, 15.5), (5.5, 16.2), (5.5, 18.2), (4.0, 18.9), (4.0, 96.0), (3.0, 96.0)]
    HOSE = [(4.42, -96.0), (7.4, -96.0), (7.4, -15.0), (4.42, -15.0), (4.42, -30.58)] + [(r + 0.02, z) for r, z in reversed(BARB)]
    HOSE = HOSE[:-1] + [(4.42, -44.0)]
    SPAC = [(4.15, 5.0), (6.05, 5.0), (6.05, 7.0), (4.15, 7.0)]
    BUSH = [(4.15, 9.8), (6.05, 9.8), (6.05, 11.5), (6.25, 11.5), (6.25, 13.2), (4.15, 13.2)]
    CLIP = [(4.2, 18.7), (6.25, 18.7), (6.25, 24.05), (7.7, 24.05), (7.7, 25.8), (4.2, 25.8)]
    O1, O2 = (5.05, 3.5), (5.05, 8.4)
    body = rev('q_body', BODY, M['qbody'], M['secQ'], seg=120); cut(body); finish(body)
    spig = rev('q_spig', SPIG, M['zinc'], M['secMagNut'], seg=96); cut(spig); finish(spig)
    hose = rev('q_hose', HOSE, M['rubber'], M['secRubber'], seg=96); cut(hose); finish(hose)
    spac = rev('q_spacer', SPAC, M['spacer'], M['secSpacer'], seg=96); cut(spac)
    bush = rev('q_bush', BUSH, M['spacer'], M['secSpacer'], seg=96); cut(bush)
    clip = rev('q_clip', CLIP, M['clip'], M['secClip'], seg=96); cut(clip); finish(clip)
    og = [rev('q_o%d' % i, ring(c, 1.06, 1.06), M['oring'], M['secOring'], seg=96) for i, c in enumerate((O1, O2))]
    ob = [rev('q_ob%d' % i, ring((c[0] + 0.2, c[1] - 0.25), 0.76, 0.86, notch=n), M['oringOld'], M['secOringOld'], seg=96) for i, (c, n) in enumerate(((O1, 0.34), (O2, 0.5)))]
    for o in og + ob: cut(o); finish(o, 60)
    E = 0.06
    FUEL = [(0, -96.0), (4.36, -96.0), (4.36, -46.05), (2.95, -46.05), (2.95, -3.95), (4.05, -3.95), (4.05, -2.05), (2.95, -2.05), (2.95, 96.0), (0, 96.0)]
    fuel = rev('q_fuel', FUEL, M['fuelLP'], seg=64); cut(fuel, eps=E, mark=False); fuel.visible_shadow = False
    group('Q_BODY', [body, spig, hose, spac, bush, clip]); group('Q_OK', og); gb = group('Q_BAD', ob); group('Q_FUEL', [fuel])
    for o in ob: o.hide_render = True
    # cupla intreaga (nesectionata)
    W = [rev('qw_body', [(0, -46.0), (4.4, -46.0)] + BARB + [(4.4, -13.0), (8.5, -11.0), (8.5, 24.0), (0, 24.0)], M['qbody'], seg=120), rev('qw_spig', [(0, 15.0), (4.0, 15.0), (4.0, 96.0), (0, 96.0)], M['zinc'], seg=96),
         rev('qw_hose', [(0, -96.0), (7.4, -96.0), (7.4, -15.0), (0, -15.0)], M['rubber'], seg=96), rev('qw_clip', [(0, 24.05), (7.7, 24.05), (7.7, 25.8), (0, 25.8)], M['clip'], seg=96)]
    for o in W: finish(o); o.hide_render = True
    group('Q_FULL', W)
    P['o1'] = PR(O1[0], O1[1]).tolist(); P['o2'] = PR(O2[0], O2[1]).tolist(); P['o1L'] = PL(O1[0], O1[1]).tolist(); P['o2L'] = PL(O2[0], O2[1]).tolist()
    P['mouth'] = PR(4.1, 25.8).tolist(); P['mouthL'] = PL(4.1, 25.8).tolist(); P['body'] = PR(8.5, 6.0).tolist(); P['bodyL'] = PL(8.5, 6.0).tolist(); P['clip'] = PR(7.7, 25.0).tolist()
    P['spig'] = PR(4.0, 40.0).tolist(); P['spigL'] = PL(4.0, 40.0).tolist(); P['hose'] = PR(7.4, -30.0).tolist(); P['hoseL'] = PL(7.4, -30.0).tolist(); P['bead'] = PR(5.5, 17.2).tolist(); P['tip'] = [0, 0, -3.0]
    PT = META['paths']
    for nm, PP in (('air_R', PR), ('air_L', PL)):
        PT[nm] = [PP(11.5, 37.0).tolist(), PP(5.4, 29.0).tolist(), PP(4.12, 25.6).tolist(), PP(4.12, 19.3).tolist(), PP(5.9, 18.6).tolist(), PP(5.9, 15.9).tolist(), PP(4.1, 14.6).tolist(), PP(4.22, 8.4).tolist(),
                  PP(4.22, 3.5).tolist(), PP(4.06, 0.0).tolist(), PP(4.06, -2.5).tolist(), PP(3.3, -3.2).tolist(), PP(1.9, -2.4).tolist(), PP(1.6, 3.0).tolist(), PP(1.6, 96.0).tolist()]
        PT[nm.replace('air', 'in')] = PT[nm][:11]                       # doar pana la varful stutului
    PT['flow'] = [[0, 0, -96.0], [0, 0, 96.0]]
    save('qc', META, ['Q_BODY', 'Q_OK', 'Q_BAD', 'Q_FUEL', 'Q_FULL'])

# ------------------------------------------------------------------ capatul conductei de inalta presiune
def build_hpe():
    K.init(empty=True); M = imats.make_all(); META = {'pts': {}, 'paths': {}}; P = META['pts']
    seat = lambda z: 1.2 + (z + 4.5) * 0.6                     # raza scaunului conic la inaltimea z (-4.5 .. 0)
    STUB = [(1.2, -34.0), (14.0, -34.0), (14.0, -15.0), (12.6, -13.6), (7.0, -13.6)] + thread(6.95, 6.15, -12.6, -0.7, 1.5) + [(6.5, 0.0), (seat(0.0), 0.0), (1.2, -4.5)]
    PIPE = [(1.1, -3.9), (seat(-3.9), -3.9), (seat(-0.4), -0.4), (4.3, 0.35), (4.3, 1.6), (3.0, 3.6), (3.0, 96.0), (1.1, 96.0)]
    # conul refolosit: turtit si cu un prag inelar acolo unde a mai fost strans, nu mai calca pe tot scaunul
    PBAD = [(1.1, -3.9), (1.45, -3.9), (1.95, -3.25), (1.95, -2.55), (2.65, -2.2), (2.85, -1.45), (3.35, -1.2), (seat(-0.4) - 0.05, -0.4), (4.42, 0.2), (4.42, 1.5), (3.0, 3.6), (3.0, 96.0), (1.1, 96.0)]
    NUT = [(7.05, -12.2), (11.2, -12.2), (11.2, 7.6), (9.8, 9.0), (3.18, 9.0), (3.18, 3.62), (4.48, 1.62), (7.05, 1.62)] + [(r + 0.1, z) for r, z in reversed(thread(6.95, 6.15, -12.2, 1.2, 1.5))][1:-1]
    stub = rev('h_stub', STUB, M['body'], M['secBody'], seg=120); cut(stub); finish(stub)
    nut = rev('h_nut', NUT, M['nut'], M['secNut'], seg=6 * 16)
    hx = K.cyl('hx', 12.2, 60.0, c=(0, 0, 0), seg=6); hx.rotation_euler = (0, 0, math.radians(30)); K.boolean(nut, hx, op='INTERSECT')
    cut(nut); finish(nut)
    pipe = rev('h_pipe', PIPE, M['steelGnd'], M['secNozzle'], seg=96); cut(pipe); finish(pipe)
    bad = rev('h_pipeBad', PBAD, M['steelGnd'], M['secNozzle'], seg=96); cut(bad); finish(bad); bad.hide_render = True
    E = 0.05
    FUEL = [(0, -34.0), (1.15, -34.0), (1.15, -4.5), (seat(-3.95) - 0.03, -3.95), (1.05, -3.95), (1.05, 96.0), (0, 96.0)]
    fuel = rev('h_fuel', FUEL, M['fuelHP'], seg=48); cut(fuel, eps=E, mark=False); fuel.visible_shadow = False
    group('H_BODY', [stub, nut]); group('H_OK', [pipe]); group('H_BAD', [bad]); group('H_FUEL', [fuel])
    P['seat'] = PR(seat(-2.2), -2.2).tolist(); P['seatL'] = PL(seat(-2.2), -2.2).tolist(); P['nut'] = PR(11.2, -2.0).tolist(); P['nutL'] = PL(11.2, -2.0).tolist()
    P['thread'] = PR(7.0, -7.0).tolist(); P['threadL'] = PL(7.0, -7.0).tolist(); P['pipe'] = PR(3.0, 30.0).tolist(); P['pipeL'] = PL(3.0, 30.0).tolist(); P['stub'] = PR(14.0, -24.0).tolist(); P['head'] = PR(4.3, 1.0).tolist()
    PT = META['paths']
    for nm, PP in (('leak_R', PR), ('leak_L', PL)):                    # pe unde scapa motorina cand conul nu mai etanseaza: pe langa con, prin filet, afara
        PT[nm] = [PP(1.0, -6.0).tolist(), PP(1.7, -3.6).tolist(), PP(3.6, -0.3).tolist(), PP(5.6, 0.75).tolist(), PP(6.75, 0.6).tolist(), PP(6.75, -12.4).tolist(), PP(8.2, -13.2).tolist(), PP(12.4, -13.3).tolist(), PP(14.3, -16.0).tolist(), PP(14.3, -40.0).tolist()]
        PT[nm.replace('leak', 'chip')] = [PP(6.6, -9.0).tolist(), PP(6.6, 0.4).tolist(), PP(5.0, 0.7).tolist(), PP(3.6, -0.5).tolist(), PP(1.7, -3.7).tolist(), PP(0.5, -4.6).tolist(), PP(0.3, 6.0).tolist(), PP(0.3, 96.0).tolist()]
    PT['flow'] = [[0, 0, -34.0], [0, 0, 96.0]]
    save('hpe', META, ['H_BODY', 'H_OK', 'H_BAD', 'H_FUEL'])

if __name__ == '__main__':
    which = sys.argv[1:] or ['qc', 'hpe']
    if 'qc' in which: build_qc()
    if 'hpe' in which: build_hpe()
