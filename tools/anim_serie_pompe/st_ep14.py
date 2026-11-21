# Episodul 14: uzura normala si garniturile imbatranite
import math
import numpy as np
import pser as S, ifx as F, i2d as D, ikit as K, pdraw as P, fxlib as X
from icomp import Shot
from fxlib import seg, ease
E = S.Ep(14); W, L, LE = E.W, E.L, E.LE; TOTAL = E.TOTAL; GLOB = S.glob(E)
RED = (255, 75, 75); GREEN = (61, 220, 132); YEL = (255, 210, 31)
G_R = [(466, 500), (471, 566), (471, 800), (482, 850)]          # motorina care scapa pe langa piston (placa ph), dreapta si stanga
G_L = [(406, 500), (401, 566), (401, 800), (390, 850)]
KB_P = (1.6, 168, 384)                                            # pistonul din capul pompei, de aproape (ca in episodul 5)
def leak(C, a=1.0, n=16, sp=200.0, t0=None, r=4.4):
    S.flowp(C, G_R, n, sp, S.HP2, r, t0=t0, a=a, seed=7, lat=1.5, glow=0.6)
    S.flowp(C, G_L, n, sp, S.HP2, r, t0=t0, a=a, seed=8, lat=1.5, glow=0.6)

# ------------------------------------------------------------------ jocul marit, in vederea marita (placa micro: banda de motorina dintre doua blocuri hasurate, x 526..553)
GX0, GX1 = 526.0, 553.0
def gap_w(t, t0, t1, d1=70.0): return d1 * float(ease(seg(t, t0, t1))) if t1 > t0 else d1
def pf_gap(dfun):
    """blocul din dreapta se departeaza cu d px (la 1080): jocul dintre piston si cilindru creste; golul se umple cu motorina"""
    def f(rgba, t):
        d = dfun(t)
        if d < 0.5: return rgba
        k = rgba.shape[1] / 1080.0; xc = int(540 * k); di = int(round(d * k)); w = rgba.shape[1]
        out = rgba.copy(); out[:, xc + di:] = rgba[:, xc:w - di]; out[:, xc:xc + di] = rgba[:, xc - 1:xc]
        return out
    return f
def gap_flow(C, d, n=14, sp=240.0, a=1.0, t0=None, seed=3):
    xm = (GX0 + GX1 + d) / 2.0; hw = (GX1 - GX0 + d) / 2.0
    S.flowp(C, [(xm, -60), (xm, 1980)], n, sp, (255, 214, 150), 6.5, t0=t0, a=a, seed=seed, lat=max(hw - 10.0, 1.0), glow=0.7)
l_joc = E.lb('JOC', 'grey')
def gap_dim(C, d, a, y=1000):
    if a <= 0.003: return
    (x0, yy), (x1, _) = S.pk(C, [(GX0, y), (GX1 + d, y)]); xm = (x0 + x1) / 2
    S.arrow2(C, (xm, yy), (x0 - 26, yy), RED, 7, a, head=18); S.arrow2(C, (xm, yy), (x1 + 26, yy), RED, 7, a, head=18)
    if a > 0.5: F.spr(C, l_joc, xm, yy + 22, -1.0, 1e9, anchor='tc')

# ------------------------------------------------------------------ carligul: kilometrajul se invarte; in capul pompei, pistonul urca si motorina portocalie scapa pe langa el
# (coperta, la 1,85 s: titlul sus, pompa cu scaparea, kilometrajul jos)
T_H = 1.2; KM0, KM1 = 87412, 412886; NO = 36
ODO = [E.add(P.odo(int(KM0 + (KM1 - KM0) * float(ease(i / (NO - 1.0)))))) for i in range(NO)]
l_h1 = E.lb('KILOMETRII SE ADUNĂ, AN DUPĂ AN', 'grey'); l_h2 = E.lb('MOTORINA SCAPĂ PE LÂNGĂ PISTON', 'bad big')
def ov_hook(C):
    t = C.t; te = E.T_S + 0.1
    leak(C, a=0.35 + 0.65 * float(seg(t, 0.3, 1.3)), n=20, r=6.0)
    i = int(round((NO - 1) * float(seg(t, 0.1, 1.75))))
    F.spr(C, ODO[i], 540, 1440, -1.0, te, anchor='tc')
    x, y = S.pk(C, [(436, 690)])[0]; D.arc(C, x, y, 96, 0, 360, RED, 6, F.pop(t, T_H, te))
    F.spr(C, l_h1, 540, 1660, 0.1, T_H, anchor='tc'); F.spr(C, l_h2, 540, 1654, T_H + 0.12, te, anchor='tc')
HOOK = [Shot('ph', 0.0, E.T_S, st='fuel', kb=[(0.0, 0.95, 40, 250), (E.T_S, 0.98, 40, 252)], tr=None, ov=ov_hook)]

# ------------------------------------------------------------------ semnele vin incet: pornire tot mai grea (mai ales la cald), putere mai mica la turatii mari, urme umede pe pompa
SIGNS = S.symptoms(E, 2, [(E.sym('start', 'PORNIRE TOT MAI GREA', 'Mai ales cu motorul cald'), 'pornire'), (E.sym('power', 'PUTERE MAI MICĂ', 'La turații mari'), 'putere'),
                          (E.sym('drop', 'URME UMEDE DE MOTORINĂ', 'Pe pompă', cls='warn'), 'urme')], cam='pw', st='wear', kb=S.KB_PW)
SIGNS.ov = S.ovs(SIGNS.ov, S.tl(E, [('SEMNELE VIN ÎNCET', 'big', L(2) + 0.1)], W(2, 'pornire') + 0.6))

# ------------------------------------------------------------------ milioane de curse la fiecare mie de kilometri, la peste 2.000 de bari
KB_PL = S.kb_on('pw', 'fuel', S.P_plunger(S.H0), 1.45, 540, 880)
l_pis = E.lb('PISTONUL', 'lp'); l_2000 = E.lb('PESTE 2.000 BAR', 'num hp')
def ov_strokes(C):
    te = L(4) + 0.12; h = S.hC(C)
    F.label(C, l_pis, S.P_plunger(h), (44, 760), L(3) + 0.3, te)
    F.label(C, l_2000, S.P_CHAMBER, (1040, 560), W(3, 'peste') - 0.25, te, anchor='tr')
STROKES = [S.pump(E, 'pw', L(3), L(4), kb=[(L(3),) + KB_PL, (L(4), KB_PL[0] * 1.04, KB_PL[1], KB_PL[2])], phase=lambda t: 2.6 * t, ov=ov_strokes,
                  labs=[('MILIOANE DE CURSE', 'lp big', W(3, 'milioane') - 0.15), ('LA FIECARE 1.000 DE KILOMETRI', 'lp', W(3, 'fiecare') - 0.15)])]

# ------------------------------------------------------------------ cu timpul, jocul dintre piston si cilindru creste; o parte din motorina scapa inapoi, in loc sa ajunga in rampa
T_4B = W(4, 'parte') - 0.3; T_G0 = W(4, 'creste') - 0.7; T_G1 = W(4, 'creste') + 0.7
D4 = lambda t: gap_w(t, T_G0, T_G1)
def ov_grow(C):
    t = C.t; d = D4(t)
    gap_flow(C, d, n=16, sp=200.0, a=float(seg(t, T_G0, T_G1)))
    gap_dim(C, d, F.pop(t, T_G0 - 0.2, T_4B + 0.1))
l_pr = E.lb('PRESIUNE ÎN RAMPĂ', 'hp')
def ov_back(C):
    t = C.t; te = L(5) + 0.12
    leak(C, n=18, sp=210.0)
    a = F.pop(t, T_4B + 0.3, te); v = 0.84 - 0.42 * float(ease(seg(t, W(4, 'loc') - 0.6, L(5) - 0.4))) + 0.01 * math.sin(t * 9.0)
    S.gauge(C, 836, 800, 118, v, a, green=(0.62, 1.0)); F.spr(C, l_pr, 836, 940, T_4B + 0.3, te, anchor='tc')
GROW = [
 None,
 S.pump(E, 'ph', T_4B, L(5), kb=[(T_4B,) + KB_P, (L(5), KB_P[0] * 1.04, KB_P[1], KB_P[2])], fx=[], ov=ov_back,
        labs=[('O PARTE DIN MOTORINĂ SCAPĂ ÎNAPOI', 'bad', T_4B + 0.15), ('ÎN LOC SĂ AJUNGĂ ÎN RAMPĂ', 'bad big', W(4, 'loc') - 0.3)]),
]
l_ps = E.lb('PISTON', 'grey'); l_cy = E.lb('CILINDRU', 'grey')
def sides(t0, t1):
    def ov(C):
        for sid, x in ((l_ps, 236), (l_cy, 844)): F.spr(C, sid, x, 700, t0, t1, anchor='tc')
    return ov
GROW[0] = Shot('micro', L(4), T_4B, st='mclean', pf=pf_gap(D4), kb=[(L(4), 1.0, 0, 0), (T_4B, 1.04, 0, 0)], phase=False, tr=('xf', 0.3),
               ov=S.ovs(ov_grow, S.hd(E, 'VEDERE MĂRITĂ', L(4) + 0.05, T_4B + 0.1, 'grey'), sides(L(4) + 0.4, T_4B + 0.1),
                        S.bl(E, [('CU TIMPUL', 'grey', L(4) + 0.1), ('JOCUL DINTRE PISTON ȘI CILINDRU CREȘTE', 'bad', W(4, 'jocul') - 0.2)], T_4B)))

# ------------------------------------------------------------------ la cald, motorina e mai subtire si scapa si mai usor; la demaror, pompa uzata nu mai strange presiunea de pornire
T_5B = W(5, 'aceea') - 0.35; T_CR = W(5, 'demaror') - 0.1; V_ST = 0.6
def ov_hot(C):
    t = C.t; te = T_5B + 0.1; d = 70.0
    gap_flow(C, d, n=14, sp=200.0 + 220.0 * float(seg(t, W(5, 'subtire') - 0.3, W(5, 'scapa'))), seed=3)
    gap_flow(C, d, n=12, sp=380.0, a=float(seg(t, W(5, 'scapa') - 0.3, W(5, 'usor'))), seed=9)
    S.thermo(C, 150, 1180, 300, 0.15 + 0.75 * float(ease(seg(t, L(5) + 0.1, L(5) + 1.3))), F.pop(t, L(5), te))
l_ok = E.lb('POMPĂ BUNĂ', 'good'); l_bad = E.lb('POMPĂ UZATĂ', 'bad'); l_st = E.lb('PORNIRE', 'lp')
def tick(C, cx, cy, R, v, a):
    ang = 150.0 + v * 240.0
    D.arc(C, cx, cy, R + 18, ang - 2.5, ang + 2.5, YEL, 16, a)
def ov_crank(C):
    t = C.t; te = L(6) + 0.12; a = F.pop(t, T_5B, te)
    for x, sid, tag in ((270, l_ok, 'ok14'), (810, l_bad, 'bad14')):
        S.plate_spr(C, 'px', 'full', x, 760, 0.4, a, crop=(120, 220, 1080, 1400), tag=tag)
        F.spr(C, sid, x, 470, T_5B + 0.1, te, anchor='tc')
    vg = 0.04 + 0.74 * float(ease(seg(t, T_CR, T_CR + 1.4))) + 0.008 * math.sin(t * 11.0)
    vb = 0.04 + 0.36 * float(ease(seg(t, T_CR, T_CR + 1.6))) + 0.03 * math.sin(t * 13.0) * float(seg(t, T_CR + 0.4, T_CR + 1.0))
    for x, v in ((270, vg), (810, vb)):
        S.gauge(C, x, 1062, 100, v, a, green=(V_ST, 1.0)); tick(C, x, 1062, 100, V_ST, a)
    F.spr(C, l_st, 540, 1062, T_5B + 0.3, te, anchor='cc')
    D.arc(C, 810, 1062, 128, 0, 360, RED, 6, F.pop(t, W(5, 'presiunea') - 0.1, te))
HOT = [
 Shot('micro', L(5), T_5B, st='mclean', pf=pf_gap(lambda t: 70.0), kb=[(L(5), 1.04, 0, 0), (T_5B, 1.08, 0, 0)], phase=False, tr=('xf', 0.3),
      ov=S.ovs(ov_hot, S.hd(E, 'VEDERE MĂRITĂ', L(5) + 0.05, T_5B + 0.1, 'grey'), sides(L(5) + 0.2, T_5B + 0.1),
               S.bl(E, [('LA CALD, MOTORINA E MAI SUBȚIRE', 'lp', L(5) + 0.1), ('ȘI SCAPĂ ȘI MAI UȘOR', 'bad big', W(5, 'scapa') - 0.2)], T_5B))),
 S.plain(E, T_5B, L(6), S.ovs(ov_crank, S.hd(E, 'LA DEMAROR', T_5B + 0.05, L(6) + 0.1, 'big'),
                              S.bl(E, [('POMPA UZATĂ NU MAI STRÂNGE', 'bad big', W(5, 'pompa') - 0.15), ('PRESIUNEA DE PORNIRE', 'bad big', W(5, 'presiunea') - 0.15)], L(6)))),
]

# ------------------------------------------------------------------ imbatranesc si garniturile: se intaresc, crapa si lasa motorina sa iasa pe la ax sau pe la capace (placa px)
SEAL = (365.0, 975.0); SRX, SRY = 54.0, 102.0
T_6B = W(6, 'se') - 0.15; T_OUT6 = W(6, 'capace') - 1.0
KB_S = (1.8, 315, -127); KB_W = (0.85, -56, 22)
def pf_hard(t0, t1):
    """simeringul axului se intareste: cauciucul maro se inchide spre cenusiu-negru"""
    def f(rgba, t):
        e = float(seg(t, t0, t1))
        if e <= 0.003: return rgba
        k = rgba.shape[1] / 1080.0; x0, x1 = int((SEAL[0] - 70) * k), int((SEAL[0] + 70) * k); y0, y1 = int((SEAL[1] - 120) * k), int((SEAL[1] + 120) * k)
        sub = rgba[y0:y1, x0:x1]; al = np.maximum(sub[..., 3:4], 1e-4); c = np.clip(sub[..., :3] / al, 0, 1)
        yy, xx = np.mgrid[y0:y1, x0:x1] / k; ell = ((xx - SEAL[0]) / (SRX + 10)) ** 2 + ((yy - SEAL[1]) / (SRY + 12)) ** 2 < 1.0
        m = (np.clip((c[..., 0] - c[..., 2] - 0.06) / 0.08, 0, 1) * ell)[..., None] * e
        new = np.array([0.13, 0.11, 0.1], np.float32) * (0.6 + 0.9 * c.max(-1, keepdims=True))
        out = rgba.copy(); out[y0:y1, x0:x1, :3] = (c * (1 - m) + new * m) * sub[..., 3:4]
        return out
    return f
CRACKS = []
for i, deg in enumerate((-50.0, -14.0, 22.0, 56.0)):
    k = 6.0 if i % 2 else -6.0
    CRACKS.append([(SEAL[0] + SRX * rr * math.cos(math.radians(deg + dk)), SEAL[1] + SRY * rr * math.sin(math.radians(deg + dk))) for rr, dk in ((0.8, 0.0), (0.93, k), (1.07, k * 0.3))])
DRIP_S = [(392, 1072), (396, 1130), (400, 1190), (404, 1250)]
DRIP_C = [(420, 612), (424, 660), (432, 700), (440, 760), (446, 840)]
l_ax = E.lb('AX', 'bad'); l_cap = E.lb('CAPAC', 'bad')
def wet(C, pts, a):
    if a <= 0.003: return
    z = C.shot.kbat(C.t)[0]; Q = S.pk(C, pts)
    D.line2(C, Q, (255, 200, 60), 12 * z, 0.4 * a); D.line2(C, Q, (255, 236, 160), 3 * z, 0.5 * a)
def ov_seal(C):
    t = C.t; te = L(7) + 0.12
    x, y = S.pk(C, [SEAL])[0]; z = C.shot.kbat(t)[0]
    D.arc(C, x, y, 118 * z, 0, 360, RED, 6, F.pop(t, W(6, 'garniturile') - 0.2, T_OUT6))
    pr = float(seg(t, W(6, 'crapa') - 0.15, W(6, 'crapa') + 0.6))
    for pts in CRACKS: D.line2(C, S.pk(C, pts), (236, 228, 214), 2.6 * z, F.pop(t, W(6, 'crapa') - 0.2, te), prog=pr)
    ws = float(seg(t, W(6, 'lasa') - 0.2, W(6, 'lasa') + 1.2)); wet(C, DRIP_S[:1 + int(ws * 3.99)], ws)
    S.flowp(C, DRIP_S, 5, 60.0, (255, 210, 80), 6.0, t0=W(6, 'lasa'), seed=4, lat=2.0, glow=0.6)
    wc = float(seg(t, W(6, 'capace') - 0.5, W(6, 'capace') + 0.8)); wet(C, DRIP_C[:1 + int(wc * 4.99)], wc)
    S.flowp(C, DRIP_C, 5, 60.0, (255, 210, 80), 6.0, t0=W(6, 'capace') - 0.2, seed=5, lat=2.0, glow=0.6)
    xa, ya = S.pk(C, [(400, 1040)])[0]; F.label(C, l_ax, ('px', xa, ya), (44, 1060), W(6, 'ax') - 0.2, te)
    xc, yc = S.pk(C, [(470, 606)])[0]; F.label(C, l_cap, ('px', xc, yc), (1040, 560), W(6, 'capace') - 0.2, te, anchor='tr')
SEALS = [Shot('px', L(6), L(7), st='full', kb=[(L(6),) + KB_S, (T_OUT6, KB_S[0] * 1.04, KB_S[1], KB_S[2]), (T_OUT6 + 0.9,) + KB_W, (L(7), KB_W[0] * 1.02, KB_W[1], KB_W[2])],
              phase=False, tr=('xf', 0.3), pf=pf_hard(W(6, 'intaresc') - 0.3, W(6, 'intaresc') + 0.6), ov=S.ovs(ov_seal,
              S.bl(E, [('ÎMBĂTRÂNESC ȘI GARNITURILE', 'lp', L(6) + 0.1), ('SE ÎNTĂRESC ȘI CRAPĂ', 'bad big', T_6B), ('MOTORINA IESE PE LA AX', 'bad big', W(6, 'lasa') - 0.15),
                       ('SAU PE LA CAPACE', 'bad big', W(6, 'sau') - 0.15)], L(7))))]

# ------------------------------------------------------------------ uzura normala nu vine peste noapte si, de obicei, nu umple instalatia de pilitura
T_7B = W(7, 'si') - 0.1
SLOW = [
 Shot('pm', L(7), T_7B, st='wear', kb=[(L(7), 1.04, 0, 0), (T_7B, 1.1, 0, 0)], phase=False, tr=('xf', 0.3),
      ov=S.bl(E, [('UZURA NORMALĂ', 'lp big', L(7) + 0.1), ('NU VINE PESTE NOAPTE', 'lp big', W(7, 'nu') - 0.15)], T_7B)),
 S.sysm(E, T_7B, L(8), hl=[(['pump'], S.YEL_HL, T_7B + 0.2)], flows=[('lp', S.LP2, 16, 210.0, 5.0, None), ('to_rail', S.HP2, 12, 170.0, 5.0, None), ('rail_inj', S.HP2, 16, 170.0, 5.0, None)],
        labs=[('DE OBICEI', 'big', T_7B + 0.15), ('NU UMPLE INSTALAȚIA DE PILITURĂ', 'good big', W(7, 'nu', 2) - 0.15)]),
]

# ------------------------------------------------------------------ cum eviti surprizele: filtre la timp, motorina curata, verificare la primele semne
AVOID = S.avoid(E, 'pw', 'wear', L(8), L(9), [('FILTRE SCHIMBATE LA TIMP', W(8, 'filtre')), ('MOTORINĂ CURATĂ', W(8, 'motorina')), ('VERIFICARE LA PRIMELE SEMNE', W(8, 'verificare'))],
                kb=[(L(8),) + S.KB_PW, (L(9), S.KB_PW[0] * 1.04, S.KB_PW[1], S.KB_PW[2])], head='CUM EVIȚI SURPRIZELE')

# ------------------------------------------------------------------ ce facem noi: debitul la presiune mare si etanseitatea, pe banc; uneori garnituri noi; pistoane si supape noi; fisa de test si garantia
T_9B = W(9, 'uneori') - 0.15; T_10B = W(10, 'si') - 0.1; T_G = W(10, 'garantie') - 0.3
gp = E.panel('DEBITUL LA PRESIUNE MARE', 880, 560)
_u = np.linspace(0, 1, 60); REF = 0.82 - 0.12 * _u ** 2; WORN = 0.78 - 0.5 * _u ** 1.6
def ov_graph(C):
    P.graph_panel(C, gp, 540, 440, 880, 560, [(_u, REF, GREEN, 6), (_u, WORN, RED, 6)], W(9, 'masuram') - 0.3, T_9B + 0.12, W(9, 'masuram') + 0.1, dur=1.4,
                  tags=[('REFERINȚĂ', GREEN, 0.06, 0.92), ('POMPA UZATĂ', (255, 120, 120), 0.6, 0.2)])
st_set = E.add(P.seals(480))
def ov_set(C): F.spr(C, st_set, 780, 440, T_9B + 0.2, L(10) + 0.12, anchor='tc')
l_wr = E.lb('PIESĂ UZATĂ', 'bad'); l_nw = E.lb('PIESĂ NOUĂ', 'good'); KB_LW = (0.8, -64, 64)
def ov_parts(C):
    te = T_10B + 0.12; t1 = W(10, 'pistoanele') + 0.1; t2 = W(10, 'piese') - 0.25
    F.lens(C, 'pc', 'wear', 262, 660, 158, t1, te, kb=KB_LW, src=S.WM_OBJ, ring=RED)
    F.lens(C, 'pc', 'dry', 818, 660, 158, t2, te, kb=KB_LW, src=S.WM_OBJ, ring=GREEN)
    F.spr(C, l_wr, 262, 832, t1 + 0.2, te, anchor='tc'); F.spr(C, l_nw, 818, 832, t2 + 0.2, te, anchor='tc')
gar = S.seal(E, '12', 'LUNI GARANȚIE', 'Fără limită de kilometri')
def ov_gar(C): F.spr(C, gar, 250, 600, T_G + 0.2, L(E.OUT) + 0.2, anchor='tc')
NOI = [
 S.wk(E, 'wb', L(9), T_9B, [('MĂSURĂM DEBITUL LA PRESIUNE MARE', 'good', W(9, 'masuram') - 0.15), ('ȘI ETANȘEITATEA', 'good big', W(9, 'verificam') - 0.15)], ov=ov_graph),
 S.wk(E, 'wm', T_9B, L(10), [('UNEORI AJUNG GARNITURI NOI', 'good big', T_9B + 0.15)], ov=ov_set),
 S.wk(E, 'wm', L(10), T_10B, [('PISTOANE SAU SUPAPE UZATE', 'bad', W(10, 'pistoanele') - 0.2), ('ÎNLOCUITE CU PIESE NOI', 'good big', W(10, 'inlocuim') - 0.15)], st='wkdam',
      seq=[('wk', W(10, 'piese') - 0.2, W(10, 'piese') + 0.4)], ov=ov_parts),
 S.wk_bench(E, T_10B, L(E.OUT), labs=[('O TESTĂM DIN NOU', 'good big', T_10B + 0.12), ('FIȘĂ DE TEST ȘI GARANȚIE', 'good big', W(10, 'primesti') - 0.15)],
            rows=[('DEBIT', W(10, 'testam') + 0.2), ('PRESIUNE', W(10, 'testam') + 0.6), ('ETANȘEITATE', W(10, 'pompa') + 0.4)], t_sheet=W(10, 'testam') - 0.1, ov=ov_gar),
]

SHOTS = S.opening(E, HOOK) + [SIGNS] + STROKES + GROW + HOT + SEALS + SLOW + [AVOID] + NOI + [S.ending(E)]
SPR = E.SPR
