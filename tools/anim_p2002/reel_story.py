# Reelul „Eroarea P2002”: planurile filmului DPF EA288, puse in ordinea si in timpul vocii (vo/cues.json).
# Fiecare plan are timpul lui din reel (t0, t1), iar evenimentele (treceri intre stari, particule, etichete) sunt legate de cuvinte.
#   python reel_story.py            -> hud_reel_data.js (textele de pe ecran, pe cadre) + rezumatul planurilor
import os, json, math, unicodedata
import numpy as np
import fxlib as X, shots as S, layout as L, gas as G
import story as ST
from fxlib import seg, ease, hexc, ramp, flow

HERE = os.path.dirname(os.path.abspath(__file__))
CUES = os.environ.get('P2002_CUES', os.path.join(HERE, 'reel_vo', 'cues.json'))
C = json.load(open(CUES, encoding='utf8'))
FPS = S.FPS

def norm(s):
    s = unicodedata.normalize('NFD', s.lower()); return ''.join(c for c in s if unicodedata.category(c) != 'Mn' and c.isalnum())
def _w(i, word, occ=0):
    n = norm(word); k = 0
    for w in C['words']:
        if w['win'] == i and norm(w['text']) == n:
            if k == occ: return w
            k += 1
    raise KeyError((i, word, occ))
W = lambda i, word, occ=0: _w(i, word, occ)['s']          # inceputul cuvantului
WE = lambda i, word, occ=0: _w(i, word, occ)['e']         # sfarsitul cuvantului
LS = lambda i: C['lines'][i]['start']
LE = lambda i: C['lines'][i]['end']
SEND = round(C['end'], 3)

# ---------------------------------------------------------------- taieturile (in golurile dintre randuri)
CUT = 0.30
T1 = LS(2) - CUT; T2 = LS(3) - CUT; T3 = LS(4) - CUT; T4 = LS(5) - CUT
T5 = W(6, 'calculează') - 0.35
T7 = LS(7) - CUT; T8 = LS(8) - CUT; T9 = LS(9) - CUT; T10 = LS(10) - CUT
T6 = LS(11) - CUT; T16 = W(11, 'Sau', 1) - 0.25
T11 = LS(12) - CUT; T12 = LS(13) - CUT; T13 = LS(14) - CUT
T14 = W(14, 'sau') - 0.20; T15 = W(14, 'arde') - 0.20; T17 = LS(15) - CUT
# hook
HB1 = 0.12; HP = W(0, 'P2002') - 0.03; HEF = W(0, 'eficiență') - 0.03; HQ = W(0, 'Ce') - 0.03
HM = W(0, 'de', 1) - 0.03; HV = W(0, '2.0') - 0.03; HG = W(0, 'gama') - 0.03
HEND = LE(0) + 0.22                       # titlurile din hook ies; de aici incepe raspunsul
ANS = LS(1) - 0.12                        # subtitrarile si titlul raspunsului

class RShot:
    """un plan al reelului; u = timpul local al planului (secunde, in timpul reelului)"""
    def __init__(s, id, t0, t1, cam, states, kind='plate', loop=None, fx=None, dim=None, grade=None, kb=None, lu=None, xf=True):
        s.id, s.t0, s.t1, s.cam, s.states, s.kind = id, round(t0, 4), round(t1, 4), cam, states, kind
        s.loop, s.fx, s.dim, s.grade, s.kb, s.xf = loop, fx, dim, grade, kb, xf
        s.lu = lu if lu is not None else (lambda u: u)            # timpul buclei (piesele in miscare)
        s._cam = None
    def layers(s, u):
        w = [1.0] + [0.0] * (len(s.states) - 1)
        for i in range(1, len(s.states)):
            a = float(seg(u, *s.states[i][1])); w[i] = a
            for j in range(i): w[j] *= (1 - a)
        return [(st[0], wi) for st, wi in zip(s.states, w)]

def pw(anch):
    """harta liniara pe bucati timp local -> u al efectului; in afara ancorelor continua cu panta 1"""
    xs = [a[0] for a in anch]; us = [a[1] for a in anch]
    def f(u):
        if u <= xs[0]: return us[0] + (u - xs[0])
        if u >= xs[-1]: return us[-1] + (u - xs[-1])
        return float(np.interp(u, xs, us))
    return f

RY = -150.0          # planurile urca in cadru: subiectul sta deasupra subtitrarilor (y 1290-1530)
def KB(dur, z0, z1, p0=(0, 0), p1=(0, 0), rz=1.0, rx=0.0, ry=RY):
    """miscarea 2D a filmului (zoom z0->z1, deplasare p0->p1) + asezarea reelului (rz, rx, ry)"""
    def f(u):
        e = min(max(u / dur, 0.0), 1.0 + 0.4 / dur)
        return (z0 + (z1 - z0) * e) * rz, p0[0] + (p1[0] - p0[0]) * e + rx, p0[1] + (p1[1] - p0[1]) * e + ry
    return f

# ---------------------------------------------------------------- hook + raspuns: motorul intreg (rotire, apoi cadrul fix)
PUNCH = [(HP, 0.085, 20.0), (HQ, 0.04, 9.0), (HM, 0.04, 9.0), (HV, 0.055, 12.0)]       # (moment, zoom, tremur px)
HK0 = (0.86, 0.0, 200.0); HK1 = (0.90, 0.0, 200.0)                                      # hook: motorul mai mic si mai jos, sub titluri
AK0 = (1.20, 18.0, -226.0); AK1 = (1.265, 20.0, -236.0)                                 # raspuns: filtrul, racitorul si supapa EGR
def kb_hero(u):
    if u < HEND - 0.15:
        e = u / (HEND - 0.15); z, dx, dy = [HK0[i] + (HK1[i] - HK0[i]) * e for i in range(3)]
    else:
        a = float(seg(u, HEND - 0.15, HEND + 0.95)); e = min(max((u - HEND - 0.95) / (T1 - HEND - 0.95), 0.0), 1.1)
        tg = [AK0[i] + (AK1[i] - AK0[i]) * e for i in range(3)]
        z, dx, dy = [HK1[i] + (tg[i] - HK1[i]) * a for i in range(3)]
    for (tp, pa, sh) in PUNCH:
        d = u - tp
        if -0.02 <= d < 0.8:
            k = math.exp(-max(d, 0.0) * 6.5) * (min(max((d + 0.02) / 0.07, 0.0), 1.0) if d < 0.05 else 1.0)
            z += pa * k; dx += sh * math.exp(-max(d, 0) * 9) * math.sin(d * 75); dy += sh * math.exp(-max(d, 0) * 9) * math.cos(d * 61)
    return z, dx, dy

# ---------------------------------------------------------------- efecte cu momentele din reel
gas = ST.gas; signal = ST.signal; puffs = ST.puffs
C_EXH, C_EXH2, C_EGR, C_AIR = ST.C_EXH, ST.C_EXH2, ST.C_EGR, ST.C_AIR

def fx_route_r(um):
    return lambda u, cam, cv, k: ST.fx_route(um(u), cam, cv, k)

def fx_egr_r(c):
    return lambda u, cam, cv, k: ST.fx_egr(u + c, cam, cv, k)

def fx_dpf_r(c):
    return lambda u, cam, cv, k: ST.fx_dpf(u + c, cam, cv, k)

def fx_dps_r(t1, t2):
    def f(u, cam, cv, k):
        gas(cv, cam, G.EXH, u, 2000, 330, size=1.7, seed=1, colf=ST.exh_col, a=0.55)
        signal(cv, cam, G.DPS1, u, 30, 85, ST.C_P1, seed=41, a=float(seg(u, t1, t1 + 0.6)), size=1.7)
        signal(cv, cam, G.DPS2, u, 52, 85, ST.C_P2, seed=42, a=float(seg(u, t2, t2 + 0.6)), size=1.7)
    return f

def fx_clog_r(a, b):
    CL = lambda x: float(seg(x, a, b))
    def f(u, cam, cv, k):
        g = CL(u)
        ST.cool_gas(u, cam, cv, flow=1.0 - 0.8 * g, dist=95.0 * ST._integ(lambda x: 1.0 - 0.62 * CL(x), u), g=g)
        ST.cool_clog(cam, cv, g)
    return f

def fx_coolcrack_r(tl):
    def f(u, cam, cv, k):
        ST.cool_gas(u, cam, cv, flow=0.45, dist=52.0 * u + 400.0, g=0.5)
        ST.cool_clog(cam, cv, 0.5, hole=(ST.CRK, 7.0))
        ST.cool_leak(u, cam, cv, tl)
    return f

def fx_valve_r(a):
    """supapa ramane intepenita aproape inchisa incepand cu momentul a"""
    def f(u, cam, cv, k):
        op = 1.0 - float(seg(u, a, a + 0.5)); thr = 0.12 + 0.88 * op
        ec = lambda sf, r: ramp(sf, [0, G.G_COOL0, G.G_COOL1, 1], [C_EXH2, C_EXH2, C_EGR, C_EGR])
        af = lambda sf, r: np.where(sf > G.G_VALVE, (r[:, 6] < thr) * 1.0, 1.0)
        gas(cv, cam, G.EGR, u, 1500, 260, size=1.5, seed=3, colf=ec, af=af)
        gas(cv, cam, G.AIR, u, 520, 330, C_AIR, 1.5, seed=4, af=lambda sf, r: (r[:, 6] > 0.42 * op) * 1.0)
        sh = 0.06 + 0.5 * op
        cc = lambda sf, r: np.where((r[:, 5] < sh)[:, None], C_EGR[None, :], C_AIR[None, :])
        gas(cv, cam, G.CHG, u, 900, 360, size=1.5, seed=5, colf=cc, swirl=0.02)
        ST.valve_dep(cam, cv, float(seg(u, a + 0.1, a + 0.7)))
    return f

def fx_leak_r(tl):
    def f(u, cam, cv, k):
        if ST.F_CRACK is None: ST.F_CRACK = G._frac(G.DPS1, ST.HCP - ST.HCD * 6.0)
        lk = float(seg(u, tl, tl + 0.7))
        signal(cv, cam, G.DPS1, u, 26, 85, ST.C_P1, seed=41, cut=(ST.F_CRACK, 1 - 0.85 * lk))
        signal(cv, cam, G.DPS2, u, 46, 85, ST.C_P2, seed=42)
        if lk > 0:
            puffs(cv, cam, ST.HCP, ST.HCD, u, 46, 0.9, 70, 0.45, hexc(0xffa860), 1.6, 9.0, a=0.34 * lk, seed=43, t0=tl, mode='over', shape='g', drag=1.6, col1=hexc(0xb8b2ac))
            puffs(cv, cam, ST.HCP, ST.HCD, u, 30, 0.5, 120, 0.3, ST.C_P1, 0.7, 0.3, a=0.9 * lk, seed=44, t0=tl, mode='add', shape='g', drag=1.0)
    return f

def fx_maf_r(tl):
    def f(u, cam, cv, k):
        if ST.F_LEAK is None: ST.F_LEAK = G._frac(G.CHG, (99.8, -148.8, 354.0))
        lk = float(seg(u, tl, tl + 0.7)); FL = ST.F_LEAK
        gas(cv, cam, G.AIR, u, 620, 300, C_AIR, 1.7, seed=4)
        gas(cv, cam, G.CHG, u, 900, 360, C_AIR, 1.6, seed=5, swirl=0.02, af=lambda sf, r: np.where(sf > FL, (r[:, 6] > 0.5 * lk) * 1.0, 1.0))
        if lk > 0:
            puffs(cv, cam, ST.LEAKP, ST.LEAKD, u, 90, 1.0, 110, 0.4, C_AIR, 2.5, 12.0, a=0.26 * lk, seed=73, t0=tl, mode='add', shape='g', drag=0.7, ztest=False)
            puffs(cv, cam, ST.LEAKP, ST.LEAKD, u, 140, 0.6, 200, 0.16, hexc(0xcdeaff), 1.5, 0.9, a=1.0 * lk, seed=74, t0=tl, mode='add', shape='g', drag=0.3, ztest=False)
    return f

def fx_inj_r(c):
    return lambda u, cam, cv, k: ST.fx_inj(u + c, cam, cv, k)

def fx_regen_r(a, tc):
    """regenerare (jar de la momentul a), fisura la momentul tc"""
    Z0, Z1, P6 = ST.Z0, ST.Z1, ST.P6
    def f(u, cam, cv, k):
        kk = float(seg(u, a, a + 0.9))
        ST.dpf_gas(cv, cam, u, soot_k=0.85, n=520, clean=hexc(0xffc070))
        r, face, ch, side, zc = ST._dpf_tab(170, 15)
        life = 0.8; age = ((u / life + r[:, 4]) % 1.0)
        P = ST._dpf_pos(face, ch * P6 + side * 2.0 * (1 - age * 0.6), -0.3 - r[:, 8] * 1.0, zc - age * 9)
        x, y, zz = cam.proj(P)
        cv.dots(x, y, zz, cam.px(1.1 * (1 - age * 0.5), zz), hexc(0xffc45a), kk * (1 - age) * 0.8, 'add', 'g', zbias=0.0012)
        kc = float(seg(u, tc, tc + 0.55))
        if kc > 0:
            m = 1500; q = X.rnd(16, m, 6)
            for fc in (0, 1):
                aa = 0.3 + q[:, 0] * 64.7
                s_ = aa if fc == 0 else -aa
                zj = Z0 + 61.0 + 1.5 * np.sin(s_ * 0.19 + 0.6) + 0.8 * np.sin(s_ * 0.83 + 1.0) + 0.45 * np.sign(np.sin(s_ * 2.9)) + (q[:, 1] - 0.5) * 0.5
                P = ST._dpf_pos(np.full(m, fc), aa, np.full(m, -0.05), zj)
                x, y, zz = cam.proj(P)
                p = 0.5 + 0.5 * q[:, 0] * (1 if fc == 0 else -1)
                grow = np.clip((kc * 1.15 - p) / 0.08, 0, 1)
                cv.dots(x, y, zz, cam.px(0.3 + 0.22 * q[:, 3], zz), hexc(0x050505), grow, 'over', 'd', ztest=False)
                cv.dots(x, y, zz, cam.px(1.25, zz), hexc(0xff6a1c), grow * 0.07 * (1 - 0.7 * float(seg(u, tc + 0.8, tc + 1.8))), 'add', 'g', ztest=False)
            ks = float(seg(u, tc + 0.5, tc + 1.1))
            r, face, ch, side, zc = ST._dpf_tab(300, 17)
            zcr = Z0 + 61.0; Dz = (Z1 + 14.0) - zcr
            d = ((r[:, 4] + u * 0.85 * (0.8 + 0.4 * r[:, 5])) % 1.0) * Dz
            P = ST._dpf_pos(face, (ch + side) * P6 + (r[:, 6] - 0.5) * 2.6, -0.35 - r[:, 8] * 1.4, zcr + d)
            x, y, zz = cam.proj(P)
            cv.dots(x, y, zz, cam.px(0.8 * (0.7 + 0.6 * r[:, 9]), zz), ST.C_SOOT, ks * np.clip(d / 6.0, 0, 1) * 0.95, 'over', 'd', zbias=0.0012)
    return f

def fx_oil_r(c):
    return lambda u, cam, cv, k: ST.fx_oil(u + c, cam, cv, k)

def fx_turbo_r(c):
    return lambda u, cam, cv, k: ST.fx_turbo(u + c, cam, cv, k)

def fx_ash_r(c):
    return lambda u, cam, cv, k: ST.fx_ash(u + c, cam, cv, k)

DIM = lambda a, b, lvl=0.8: (lambda u: lvl * float(seg(u, a, b)))

# ---------------------------------------------------------------- planurile
def L_(t, t0): return t - t0          # moment absolut -> timp local

d01 = T2 - T1
um01 = pw([(L_(W(2, 'ies'), T1) - 0.10, 0.55), (L_(W(2, 'turbină'), T1), 1.75), (L_(W(2, 'catalizator'), T1), 2.38), (L_(W(2, 'filtrul'), T1), 3.2)])
c02 = 0.5 - (L_(W(3, 'o'), T2) - 0.05)                    # gazele recirculate pornesc pe „o parte”
c03 = 0.15 - (L_(W(4, 'gazele'), T3) - 0.15)              # gazele intra in canale pe „gazele”
a07 = L_(W(7, 'Se'), T7) - 0.10; b07 = L_(W(7, 'gaze', 1), T7) + 0.45
a09 = L_(W(9, 'fisurat'), T9) - 0.20; l09 = L_(W(9, 'pierde'), T9) - 0.15
a10 = L_(W(10, 'Înțepenită'), T10) - 0.10
a06 = L_(W(11, 'crăpat'), T6) - 0.15
l16 = L_(W(11, 'pierdut'), T16) - 0.15
c11 = 4.3 - (L_(W(12, 'picură'), T11) - 0.10)             # injectorul incepe sa picure pe „picură”
a12 = L_(W(13, 'regenerează'), T12) - 0.10; k12 = L_(W(13, 'crapă'), T12) - 0.10
c13 = 0.35; c14 = 0.5
a15 = L_(W(14, 'lasă'), T15) - 0.10; c15 = 0.4 - a15

SHOTS = [
    RShot('hero', 0.0, T1, 'heroB', [('solid', None)], kind='hero', kb=kb_hero, xf=False),
    RShot('s01', T1, T2, 'route', [('solid', None), ('ghostNR', (0.12, 0.95))], loop=('rotor', 12, 30, 0), fx=fx_route_r(um01),
          kb=KB(d01, 1.0, 1.05, (0, 0), (10, -14), ry=-30)),
    RShot('s02', T2, T3, 'routeC', [('ghostNR', None)], loop=('rotor', 12, 30, 0), fx=fx_egr_r(c02), kb=KB(T3 - T2, 1.0, 1.045)),
    RShot('s03', T3, T4, 'dpf', [('soot0', None), ('soot1', (L_(W(4, 'funinginea'), T3) - 0.9, T4 - T3 + 0.2))], fx=fx_dpf_r(c03),
          kb=KB(T4 - T3, 1.0, 1.06, (0, 0), (0, -20), ry=-90)),
    RShot('s04', T4, T5, 'dps', [('gexh', None)], fx=fx_dps_r(L_(W(5, 'presiunea'), T4) - 0.05, L_(W(5, 'după'), T4) - 0.45),
          kb=KB(T5 - T4, 1.0, 1.0, (0, 0), (12, 0), ry=-80)),
    RShot('s05', T5, T7, 'heroB', [('solid', None)], dim=DIM(0.0, 0.7, 0.86), kb=KB(T7 - T5, 1.04, 1.0, ry=-60)),
    # --- cauzele, in ordinea reelului: racitorul de gaze, supapa EGR, senzorul, aerul; apoi injectia si uleiul
    RShot('s07', T7, T8, 'cool', [('solid', None)], fx=fx_clog_r(a07, b07), kb=KB(T8 - T7, 1.0, 1.07, (0, 0), (0, -16))),
    RShot('s08', T8, T9, 'routeC', [('ghostNR', None)], loop=('rotor', 12, 30, 0), fx=ST.fx_thin, kb=KB(T9 - T8, 1.045, 1.085)),
    RShot('s09', T9, T10, 'cool', [('solid', None), ('ecrack', (a09, a09 + 0.5))], fx=fx_coolcrack_r(l09),
          kb=KB(T10 - T9, 1.07, 1.12, (0, -16), (0, -26))),
    RShot('s10', T10, T6, 'egrvB', [('vopen', None), ('vclosed', (a10, a10 + 0.5))], fx=fx_valve_r(a10), kb=KB(T6 - T10, 1.0, 1.05, ry=-300)),
    RShot('s06', T6, T16, 'dpsC', [('solid', None), ('crack', (a06, a06 + 0.6))], fx=fx_leak_r(a06 + 0.3), kb=KB(T16 - T6, 1.0, 1.06, ry=-190)),
    RShot('s16', T16, T11, 'mafG', [('gint', None)], fx=fx_maf_r(l16), kb=KB(T11 - T16, 1.0, 1.05, ry=-90)),
    RShot('s11', T11, T12, 'inj', [('noeng', None)], loop=('engine', 60, 30, 45), fx=fx_inj_r(c11), lu=lambda u: u + c11,
          kb=KB(T12 - T11, 1.0, 1.05, (0, -110), (0, -110)), grade=(0.80, 1.22)),
    RShot('s12', T12, T13, 'dpf', [('soot1', None), ('regen2', (a12, a12 + 0.9))], fx=fx_regen_r(a12, k12), kb=KB(T13 - T12, 1.03, 1.08)),
    RShot('s13', T13, T14, 'sec', [('noeng', None)], loop=('engine', 60, 30, 45), fx=fx_oil_r(c13), lu=lambda u: u + c13,
          kb=KB(T14 - T13, 1.0, 1.03, ry=-230), grade=(0.80, 1.22)),
    RShot('s14', T14, T15, 'turboG', [('gturbo', None)], loop=('rotor', 12, 30, 0), fx=fx_turbo_r(c14), kb=KB(T15 - T14, 1.0, 1.03)),
    RShot('s15', T15, T17, 'dpf', [('sootM', None), ('ash', (a15, a15 + 2.4))], fx=fx_ash_r(c15), kb=KB(T17 - T15, 1.1, 1.16, (0, -150), (0, -170), ry=-90)),
    RShot('s17', T17, SEND, 'heroB', [('solid', None)], dim=DIM(0.0, 0.8, 0.84), kb=KB(SEND - T17, 1.0, 1.04, ry=-60)),
]
TOTAL = SEND
BY = {s.id: s for s in SHOTS}

# ============================================================== textele de pe ecran (HUD), in timpul reelului
ORANGE = '#ff9238'; RED = '#ff5a4d'; BLUE = '#58b6ff'; PINK = '#ff6fb5'; GREEN = '#3fd68a'; AMBER = '#f0b23e'; GREY = '#c9d0d8'
SUBG = '#8fe0b6'; SUBR = '#ff8377'
dp = ST.dp; Z0, Z1 = ST.Z0, ST.Z1; CC = ST.CC; TUBX = ST.TUBX; SX = ST.SX; MISC = ST.MISC
mw = L.mw

# titluri: (plan de inceput, plan de sfarsit, rand mic, titlu, culoarea randului mic)
TITLES = [
    (ANS, T1, 'P2002 · EFICIENȚĂ FILTRU DE PARTICULE', 'De cele mai multe ori, filtrul nu are nimic', ORANGE),
    (T1, T2, 'TRASEUL GAZELOR', 'De la motor până la filtru', ORANGE),
    (T2, T3, 'TRASEUL GAZELOR', 'O parte se întoarce prin EGR', ORANGE),
    (T3, T4, 'ÎN FILTRU', 'Gazele trec, funinginea rămâne', ORANGE),
    (T4, T5, 'CUM JUDECĂ CALCULATORUL', 'Măsoară presiunea pe filtru', ORANGE),
    (T5, T7, 'CUM JUDECĂ CALCULATORUL', 'Compară cu ce a calculat', ORANGE),
    (T7, T10, 'CAUZA 1 · CEA MAI DEASĂ', 'Răcitorul de gaze', RED),
    (T10, T6, 'CAUZA 2', 'Supapa EGR', RED),
    (T6, T16, 'CAUZA 3', 'Furtunașele senzorului', RED),
    (T16, T11, 'CAUZA 4', 'Aerul și debitmetrul', RED),
    (T11, T13, 'CAUZA 5', 'Injecția', RED),
    (T13, T17, 'CAUZA 6', 'Uleiul ars', RED),
    (T17, SEND + 1, 'ÎNAINTE DE A SCHIMBA FILTRUL', 'Se caută cauza', ORANGE),
]
# pastila de sub titlu
CHIPS = [
    (W(8, 'deși') - 0.10, T11, 'FILTRUL E BUN', GREEN),
    (W(12, 'chiar') - 0.05, T17, 'FILTRUL E VICTIMA', AMBER),
]
# widgetul calculat / masurat (chei absolute; intre cauze revine la „se potrivesc”)
RS = 0.45
ECU = dict(on=T7 + 0.15, off=T17, calc=[[0.0, 0.5]], meas=[
    [T7, 0.5], [W(7, 'puține') - 0.10, 0.5], [WE(7, 'calculatorul'), 0.42],
    [W(8, 'iese') - 0.10, 0.42], [W(8, 'Apare') - 0.20, 0.395], [W(8, 'Apare') + 0.40, 0.26],
    [T10, 0.26], [T10 + RS, 0.5], [W(10, 'Efectul') - 0.15, 0.5], [W(10, 'același') + 0.15, 0.28],
    [T6, 0.28], [T6 + RS, 0.5], [W(11, 'crăpat') + 0.45, 0.5], [W(11, 'înfundat') + 0.35, 0.2],
    [T16, 0.2], [T16 + RS, 0.5], [W(11, 'pierdut') + 0.50, 0.5], [W(11, 'debitmetru') + 0.25, 0.25],
    [T11, 0.25], [T11 + RS, 0.5], [W(12, 'face') - 0.10, 0.5], [WE(12, 'calcul'), 0.82],
    [W(13, 'regenerează') + 0.3, 0.82], [W(13, 'fierbinte') + 0.5, 0.66], [W(13, 'crapă') + 0.15, 0.66], [W(13, 'crapă') + 0.95, 0.12],
    [T13, 0.12], [T13 + RS, 0.5], [T14, 0.6], [T15 + 0.3, 0.68], [W(14, 'cenușa', 1) + 0.7, 0.86]])
# schema calculat / masurat (planul s05)
INFO = dict(t0=T5, t1=T7, pA=T5 + 0.15, gA0=W(6, 'câtă') - 0.05, gA1=W(6, 'trebui') + 0.45, pB=W(6, 'Dacă') - 0.40,
            gB0=W(6, 'măsoară') - 0.05, gB1=W(6, 'mult') + 0.25, vB=0.15, cmp=W(6, 'mult') + 0.05, fault=W(6, 'dă') - 0.12)
# lista de la final (planul s17)
FINAL = dict(t0=T17, i0=T17 + 0.45, di=0.50, fin2=W(15, 'Eroarea') - 0.15,
             items=['Răcitorul de gaze (EGR)', 'Supapa EGR', 'Senzorul de presiune și furtunașele', 'Debitmetrul și admisia', 'Injectoarele', 'Consumul de ulei și turbina'],
             a='Eroarea arată spre filtru.', b='Cauza se găsește la diagnoză.')
# cardul cu martorul din hook
LAMP = dict(on=-0.5, off=HEND + 0.02, y=1420)

END = None        # „pana la sfarsitul planului”
# etichete: plan -> (text, punct 3D mm, x, y text, aliniere, t_on absolut, t_off absolut sau END, culoare, [sub-randuri (t absolut, text, culoare)])
LABELS = {
 'hero': [('Filtru de particule', tuple(mw(30, 30, 120)), 56, 404, 'l', W(1, 'filtrul') - 0.10, END, GREEN, [(0, 'DE CELE MAI MULTE ORI, BUN', SUBG)]),
          ('Supapă EGR', (176, -240, 206), 640, 742, 'l', W(1, 'EGR') - 0.10, END, RED, [(0, 'A DOUA CAUZĂ', SUBR)]),
          ('Răcitor de gaze', (-52, -274, 34), 410, 1128, 'l', W(1, 'răcitorul') - 0.10, END, RED, [(0, 'CAUZA CEA MAI DEASĂ', SUBR)])],
 's01': [('Turbină', (4, -212, 266), 700, 400, 'l', W(2, 'turbină') - 0.05, END, ORANGE),
         ('Catalizator de oxidare', tuple(mw(34, 34, 47)), 330, 640, 'l', W(2, 'catalizator') - 0.05, END, ORANGE),
         ('Filtru de particule (DPF)', tuple(mw(36, 36, 215)), 60, 1190, 'l', W(2, 'filtrul') - 0.05, END, ORANGE)],
 's02': [('Răcitor de gaze', (-20, -296, 30), 440, 1040, 'l', W(3, 'răcitorul') - 0.05, END, AMBER),
         ('Supapă EGR', (176, -262, 206), 956, 392, 'r', W(3, 'supapa') - 0.05, END, AMBER)],
 's03': [('Canal de intrare', tuple(dp(0, 12, -1, Z0 + 40)), 330, 470, 'l', W(4, 'gazele') - 0.05, END, ORANGE),
         ('Dop', tuple(dp(0, 18, -1, Z0 + 5)), 790, 430, 'l', W(4, 'trec') + 0.10, END, GREY),
         ('Perete poros', tuple(dp(0, 39, 0, Z0 + 95)), 700, 1110, 'l', W(4, 'pereții') - 0.05, END, GREY),
         ('Funingine', tuple(dp(1, 10.2, -1, Z0 + 110)), 250, 1150, 'l', W(4, 'funinginea') - 0.05, END, GREY)],
 's04': [('Senzor de presiune', (-266, -212, 318), 50, 392, 'l', W(5, 'Măsoară') - 0.05, END, GREY),
         ('Înainte de filtru', tuple(MISC['dps_b1']), 50, 730, 'l', W(5, 'înainte') - 0.05, END, ORANGE, [(0, 'PRESIUNE MAI MARE', ORANGE)]),
         ('După filtru', tuple(MISC['dps_b2']), 50, 1140, 'l', W(5, 'după') - 0.05, END, BLUE, [(0, 'PRESIUNE MAI MICĂ', BLUE)])],
 's07': [('Gaze recirculate', (CC[0] + 19.5, CC[1] - 18.5, CC[2] + 30), 660, 470, 'l', T7 + 0.55, END, AMBER),
         ('Antigel', (CC[0] + 13.0, CC[1] - 19.5, CC[2] - 24), 720, 1100, 'l', T7 + 1.15, END, PINK),
         ('Depuneri', (CC[0] + TUBX[0] + 2.2, CC[1] - 19.5 + 1.2, CC[2] + 4), 60, 680, 'l', W(7, 'depuneri') - 0.05, END, RED)],
 's08': [('Debit EGR mic', (95, -280, 151), 600, 820, 'l', T8 + 0.5, END, AMBER)],
 's09': [('Fisură', tuple(ST.CRK), 500, 640, 'l', W(9, 'fisurat') + 0.10, END, RED, [(0, 'ÎN RĂCITOR', SUBR), (W(9, 'pierde') - 0.05, 'PIERDE ANTIGEL ÎN GAZE', PINK)])],
 's10': [('Gaze recirculate', (168, -249, 183), 520, 1150, 'l', T10 + 0.8, END, AMBER),
         ('Supapă EGR', (176 + 14, -240 - 22, 206 + 6), 40, 700, 'l', W(10, 'supapa') - 0.05, END, AMBER,
          [(0, '', SUBR), (W(10, 'Înțepenită') - 0.05, 'ÎNȚEPENITĂ DE DEPUNERI', SUBR), (W(10, 'nu') - 0.05, 'NU SE DESCHIDE CÂT I SE CERE', SUBR)])],
 's06': [('Furtunaș crăpat', tuple(ST.HCP), 50, 700, 'l', W(11, 'crăpat') + 0.05, END, RED, [(0, 'SENZORUL CITEȘTE MAI PUȚIN', SUBR)])],
 's16': [('Aer pierdut', tuple(ST.LEAKP), 380, 440, 'l', W(11, 'pierdut') - 0.05, END, RED),
         ('Debitmetru', tuple(S.META['turbo']['maf_pos']), 640, 560, 'l', W(11, 'debitmetru') - 0.05, END, BLUE, [(0, 'MĂSOARĂ GREȘIT', SUBR)])],
 's11': [('Evacuare', (SX - 6, -34, 274), 50, 420, 'l', T11 + 0.8, END, ORANGE),
         ('Admisie', (SX - 6, 34, 274), 860, 470, 'l', T11 + 1.3, END, BLUE),
         ('Injector', (SX, 5.5, 262), 650, 620, 'l', W(12, 'injector') - 0.05, END, GREY),
         ('Motorină în plus', (SX, 2, L.DECK - 10), 650, 1150, 'l', W(12, 'picură') + 0.15, END, RED)],
 's12': [('Funinginea arde', tuple(dp(0, 24, -1, Z0 + 70)), 700, 520, 'l', W(13, 'regenerează') + 0.2, W(13, 'până') + 0.1, ORANGE),
         ('Fisură', tuple(dp(0, 30, -0.05, Z0 + 61.0)), 60, 500, 'l', W(13, 'crapă') + 0.25, END, RED, [(0, 'FUNINGINEA TRECE NEFILTRATĂ', SUBR)])],
 's13': [('Segmenți uzați', (SX, -40.5, 176), 60, 1090, 'l', T13 + 0.75, END, AMBER)],
 's14': [('Etanșarea axului', (24, -212, 272), 430, 560, 'l', T14 + 0.30, END, AMBER)],
 's15': [('Cenușă', tuple(dp(0, 24, -1, Z1 - 30)), 560, 880, 'l', W(14, 'cenușă') - 0.05, END, GREY, [(0, '', GREY), (W(14, 'nu') - 0.05, 'NU ARDE LA REGENERARE', SUBR)])],
}

def export_hud(path):
    Wd, Hd = S.W, S.H
    out = dict(fps=FPS, total=TOTAL, W=Wd, H=Hd, hook_end=HEND, ans=ANS,
               shots=[dict(id=s.id, t0=s.t0, t1=s.t1) for s in SHOTS],
               titles=[dict(on=a, off=b, k=k, t=t, col=c) for (a, b, k, t, c) in TITLES],
               chips=[dict(on=a, off=b, text=t, col=c) for (a, b, t, c) in CHIPS],
               ecu=ECU, info=INFO, final=FINAL, lamp=LAMP, labels=[])
    for s in SHOTS:
        if s.id not in LABELS: continue
        cam = X.Cam(ST.cam_J(s.cam), Wd, Hd)
        for lab in LABELS[s.id]:
            (txt, p3, tx, ty, al, a, b, col) = lab[:8]; sub = lab[8] if len(lab) > 8 else None
            if b is None: b = s.t1
            f0 = int(math.floor(a * FPS)) - 1; f1 = int(math.ceil(b * FPS)) + 14
            ax = []; ay = []
            for f in range(f0, f1):
                u = f / FPS - s.t0
                cam.set2d(*s.kb(u))
                x, y, z = cam.proj(np.array(p3, np.float64)); ax.append(round(float(x[0]), 1)); ay.append(round(float(y[0]), 1))
            out['labels'].append(dict(shot=s.id, text=txt, ax=ax, ay=ay, f0=f0, tx=tx, ty=ty, al=al, on=a, off=b, col=col, sub=sub))
    open(path, 'w', encoding='utf8').write('window.TL = ' + json.dumps(out, ensure_ascii=False) + ';\n')
    return out

if __name__ == '__main__':
    o = export_hud(os.path.join(HERE, 'hud_reel_data.js'))
    for s in SHOTS: print('%-5s %7.2f - %7.2f  (%.2f s)  %s' % (s.id, s.t0, s.t1, s.t1 - s.t0, s.cam))
    print('hook', dict(B1=HB1, P=round(HP, 2), EF=round(HEF, 2), Q=round(HQ, 2), M=round(HM, 2), V=round(HV, 2), G=round(HG, 2), END=round(HEND, 2), ANS=round(ANS, 2)))
    for l in o['labels']: print(l['shot'], l['text'], '| punct', round(l['ax'][2]), round(l['ay'][2]), '-> text', l['tx'], l['ty'], '| %.2f - %.2f' % (l['on'], l['off']))
    print('total', TOTAL, 'cadre', int(TOTAL * FPS) + 1)
