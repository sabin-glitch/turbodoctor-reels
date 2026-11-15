# Regia cadrelor refacute cu Blender in reelul "Un banal schimb de filtru de motorina..." (hook 0-173 si pompa in sectiune 2180-3038).
# Pentru fiecare cadru al reelului scrie: timpul animatiei U (din vo/uframes.json, ca etichetele si panoul sa ramana pe voce),
# camera, starea pompei pentru pagina three.js (particule + HUD) si reteta de compunere a randarilor Blender.
#   python3 director.py [--moves]   -> director.json (+ moves.json: cadrele intregi pentru miscarile de camera, daca se cer)
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
REEL = os.environ.get('REEL', '/home/claude/reels/amorsare_filtru')
U = json.load(open(os.path.join(REEL, 'vo/uframes.json')))
MOVES = '--moves' in sys.argv

NL, LR = 38, 90                 # ca in reel_scene.py: cadre pe o jumatate de tura a camei, cadre pentru rotirea tachetului
HOOK = (0, 173)                 # hook: prim-plan, tachetul se roteste din primul cadru
CP = (2180, 3038)               # pompa in sectiune
F_ROT = 2740                    # cadrul la care incepe rotirea tachetului ("Tachetul se roteste in alezaj")
F_CUT1 = 2658                   # planul larg -> prim-plan ("Se blocheaza si freaca de cama")
F_CUT2 = None                   # (optional) prim-plan -> planul larg; None = prim-planul ramane pana la capat, peste stampila "POMPA DISTRUSA"
N_MOVE = 24                     # cadre pentru o miscare de camera (centrata pe taietura), daca e randata
DAM0, DAM1 = 51, 58             # cama trece din intreaga in taiata intre aceste cadre ale rotirii
CHIP0 = 30                      # pilitura incepe sa se desprinda la acest cadru al rotirii
H0, H1 = 2559, 2646             # rola se incinge ("filmul de ungere dispare" ... inainte de prim-plan)

SH = {  # c in reperul pompei (mm); oy = decalajul efectiv pe verticala (pagina primeste oy + 10, modul vo scade 10)
    'W': dict(c=[0, 34, 0], az=44.0, el=13.5, d=620.0, oy=160.0),
    'C': dict(c=[0, 24, 0], az=47.0, el=14.5, d=410.0, oy=140.0),
}
clamp = lambda x, a=0.0, b=1.0: max(a, min(b, x))
def ease(x): x = clamp(x); return x * x * (3 - 2 * x)
lerp = lambda a, b, k: a + (b - a) * k
def mix(A, B, k): return dict(c=[lerp(A['c'][i], B['c'][i], k) for i in range(3)], az=lerp(A['az'], B['az'], k), el=lerp(A['el'], B['el'], k),
                              d=math.exp(lerp(math.log(A['d']), math.log(B['d']), k)), oy=lerp(A['oy'], B['oy'], k))

def frame(f):
    hook = HOOK[0] <= f <= HOOK[1]
    a = f if hook else f - F_ROT                  # indicele de faza al camei (un cadru = pi/NL)
    u = U[f] - 60.5
    R = dict(f=f, U=U[f], hook=hook, a=a)
    # ---- camera
    cam, mv = 'C', None
    if not hook:
        cam = 'W' if (f < F_CUT1 or (F_CUT2 is not None and f >= F_CUT2)) else 'C'
        if MOVES:
            for fc, A, B, nm in [(F_CUT1, 'W', 'C', 'T1')] + ([(F_CUT2, 'C', 'W', 'T2')] if F_CUT2 is not None else []):
                i = f - (fc - N_MOVE // 2)
                if 0 <= i < N_MOVE: mv = (nm, i, mix(SH[A], SH[B], ease((i + 0.5) / N_MOVE)))
    shot = mv[2] if mv else SH[cam]
    R['cam'] = cam; R['shot'] = shot
    R['panel'] = 1.0 if (cam == 'W' and not hook) else 0.0     # panoul "Bosch CP4 - sectiune" doar in planul larg: in prim-plan acoperea supapele din capul hidraulic
    # ---- starea pompei
    rot = ease(a / LR) if a >= 0 else 0.0
    bk = ease((u - 4.2) / 1.0) * (1 - ease((u - 9) / 3) * 0.6)     # bulele de aer din carcasa, ca in pagina (si in hook)
    if hook: fuel, heat, sk = 0.0, 1.0, 1.0
    else:
        fuel = 1 - ease((u - 4.4) / 2.2)
        heat = ease((f - H0) / (H1 - H0))
        sk = ease((u - 6.2) / 1.2)
    c1 = (a - CHIP0) / 30 * 0.9
    wd = clamp((a - DAM0) / (DAM1 - DAM0))       # ponderea camei taiate
    R['st'] = dict(phi=-math.pi * a / NL, spin=0, rot=rot, dam=1 if wd >= 0.5 else 0, fuel=fuel, heat=heat * (0.8 + 0.2 * math.sin(f * 23 / 30)), bk=bk, sk=sk, c1=c1, tp=U[f])
    R['add'] = bool(heat > 0.03 or sk > 0)        # scantei / stralucire de randat
    # ---- reteta Blender
    k = a % NL
    if mv: R['bl'] = dict(full='moves/%s_%03d.png' % (mv[0], mv[1])); R['move'] = dict(name=mv[0], i=mv[1], sname='HOT' if mv[0] == 'T1' else 'CROSS', k=a)
    else:
        if a < 0:
            if cam == 'W':
                w = {'FUEL': fuel, 'AIR': (1 - fuel) * (1 - heat), 'HOT': (1 - fuel) * heat}
                lay = [[s, k, round(v, 4)] for s, v in w.items() if v > 0.002]
                tot = sum(x[2] for x in lay); lay = [[s, kk, v / tot] for s, kk, v in lay]
                plates = [[s, v] for s, kk, v in lay]
            else: lay = [['HOT', k, 1.0]]; plates = [['HOT', 1.0]]
        elif a < LR:
            assert cam == 'C'
            lay = [['ROT0', a, 1 - wd]] if wd <= 0 else ([['ROT1', a, 1.0]] if wd >= 1 else [['ROT0', a, 1 - wd], ['ROT1', a, wd]]); plates = [['HOT', 1.0]]
        else: lay = [['CROSS', k, 1.0]]; plates = [['HOT', 1.0]]
        R['bl'] = dict(cam=cam, plates=plates, r1=lay, r2=a % (2 * NL))
    return R

D = [frame(f) for f in list(range(HOOK[0], HOOK[1] + 1)) + list(range(CP[0], CP[1] + 1))]
json.dump(dict(NL=NL, LR=LR, SH=SH, frames=D), open(os.path.join(HERE, 'director.json'), 'w'))
mv = [dict(out='moves/%s_%03d.png' % (r['move']['name'], r['move']['i']), shot=r['shot'], sname=r['move']['sname'], k=r['move']['k']) for r in D if 'move' in r]
json.dump(mv, open(os.path.join(HERE, 'moves.json'), 'w'))
need = {}
for r in D:
    b = r['bl']
    if 'full' in b: continue
    for s, k, v in b['r1']: need.setdefault((b['cam'], s), set()).add(k)
    need.setdefault((b['cam'], 'R2'), set()).add(b['r2'])
    for s, v in b['plates']: need.setdefault((b['cam'], 'plate ' + s), set()).add(0)
print(len(D), 'cadre;', len(mv), 'cadre de miscare;', sum(1 for r in D if r['add']), 'cu scantei/stralucire')
for kk in sorted(need): print(' ', kk, len(need[kk]), 'cadre', min(need[kk]), '..', max(need[kk]))
for f in (0, 173, 2180, 2657, 2658, 2740, 2961, 2962, 3038):
    r = next(x for x in D if x['f'] == f); s = r['st']
    print(f, 'U %.2f' % r['U'], r['cam'], 'a', r['a'], 'fuel %.2f heat %.2f rot %.2f bk %.2f sk %.2f c1 %.2f' % (s['fuel'], s['heat'], s['rot'], s['bk'], s['sk'], s['c1']), r['bl'])
