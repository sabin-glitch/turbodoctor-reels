# Episodul 16: pompa schimbata fara curatarea instalatiei
import math
import numpy as np
import pser as S, ifx as F, i2d as D, ikit as K, pdraw as P, fxlib as X
from icomp import Shot
from fxlib import seg, ease
E = S.Ep(16); W, L, LE = E.W, E.L, E.LE; TOTAL = E.TOTAL; GLOB = S.glob(E)
RED = (255, 75, 75); GREEN = (61, 220, 132); SILVER = (236, 241, 248)

def filings(C, names, n, speed, r, a, t_move=None, t_gone=None, seed=1, lat=5.0, acc=0.9):
    """pilitura ramasa pe traseele schemei: sta pe loc si sclipeste pana la t_move, apoi porneste; la t_gone dispare (piesa schimbata sau curatata)"""
    if t_gone is not None: a = a * (1.0 - float(seg(C.t, t_gone, t_gone + 0.5)))
    if a <= 0.003: return
    polys = []
    for nm in names:
        p = S.SP[nm]; polys += p if isinstance(p, list) else [p]
    rng = np.random.RandomState(seed); u0 = rng.rand(n); which = rng.randint(0, len(polys), n); sv = 1 + (rng.rand(n) - 0.5) * 0.5
    off = (rng.rand(n) - 0.5) * 2 * lat; ph = rng.rand(n) * 6.283
    dt = 0.0 if t_move is None else max(C.t - t_move, 0.0); d = (dt - acc / 2) if dt > acc else dt * dt / (2 * acc)
    pts = []
    for i in range(n):
        p = polys[which[i]]; s = (u0[i] * p.len + d * speed * sv[i]) % p.len
        q = p.at([s])[0]
        j = min(int(np.searchsorted(p.cum, s)), len(p.p) - 1); j0 = max(j - 1, 0)
        dv = p.p[j] - p.p[j0]; nv = np.array([-dv[1], dv[0]]) / (np.linalg.norm(dv) + 1e-9)
        pts.append(q + nv * off[i])
    D.dots2(C, np.array(pts), r * (0.8 + 0.35 * np.sin(C.t * 5.0 + ph)), S.METAL2, a, 0.55)

# ------------------------------------------------------------------ carligul: pompa noua, stralucitoare; in conducte, in injectoare si in rezervor, pilitura veche sclipeste si porneste la drum
# (coperta, la 1,85 s: pompa noua in stanga, trei lupe cu pilitura in dreapta)
T_GO = 1.45; R_L = 136
BALL = np.array([539.0, 1123.0]); R_B = 50.0                      # bila supapei de comanda, pe placa valve:shut
VR = X.rnd(53, 16, 4); HR = X.rnd(29, 40, 3)
SEAT = np.array([BALL + (R_B + 2 + 6 * VR[i, 1]) * np.array([math.sin(math.radians(-50 + 100 * VR[i, 0])), math.cos(math.radians(-50 + 100 * VR[i, 0]))]) for i in range(14)])
LENSES = [  # placa, starea, incadrarea lupei, centrul lupei, eticheta, fulgii (pe placa), viteza dupa T_GO, dreptunghiul in care se intorc
 ('microf', 'mclean', (1.0, 0, 0), (812, 846), 'CONDUCTE ȘI RAMPĂ', np.c_[486 + 108 * HR[:14, 0], 830 + 260 * HR[:14, 1]], (0.0, 150.0), (480, 820, 600, 1100)),
 ('valve', 'shut', (1.5, 2, -300), (812, 1124), 'INJECTOARE', np.r_[SEAT[:9], np.c_[520 + 38 * HR[14:20, 0], 1186 + 60 * HR[14:20, 1]]], (0.0, -30.0), (518, 1184, 560, 1250)),
 ('tank', 'dry', (0.9, 108, -144), (812, 1402), 'REZERVOR', np.c_[285 + 270 * HR[20:36, 0], 1160 + 14 * HR[20:36, 1]], (70.0, 0.0), (280, 1100, 560, 1200)),
]
l_new = E.lb('POMPĂ NOUĂ', 'good big'); l_old = E.lb('PILITURA VECHE E TOT ACOLO', 'bad big'); l_len = [E.lb(x[4], 'bad') for x in LENSES]
def lens_flakes(C, c, kb, P0, vel, box, a, r=4.8, seed=0, n_fix=0):
    """fulgi care sclipesc intr-o lupa: P0 pe placa; dupa T_GO pornesc cu viteza vel (primii n_fix raman pe loc)"""
    t = C.t; dt = max(t - T_GO, 0.0); d = (dt - 0.4) if dt > 0.8 else dt * dt / 1.6
    Q = np.array(P0, float); mv = np.arange(len(Q)) >= n_fix
    Q[mv] = Q[mv] + np.array(vel) * d
    Q[mv, 0] = box[0] + (Q[mv, 0] - box[0]) % (box[2] - box[0]); Q[mv, 1] = box[1] + (Q[mv, 1] - box[1]) % (box[3] - box[1])
    Sx = (Q - np.array([540.0, 960.0])) * kb[0] + np.array([kb[1] + c[0], kb[2] + c[1]])
    keep = np.hypot(Sx[:, 0] - c[0], Sx[:, 1] - c[1]) < R_L - 12
    if not keep.any(): return
    rr = r * (0.75 + 0.4 * np.sin(t * 6.0 + np.arange(len(Q)) * 1.7 + seed))
    D.dots2(C, Sx[keep], rr[keep], SILVER, a, 0.6)
def ov_hook(C):
    t = C.t; te = E.T_S + 0.1
    S.plate_spr(C, 'px', 'full', 292, 1010, 0.5, F.pop(t, -1.0, te), crop=(120, 220, 1080, 1400), tag='new16')
    S.sparks2(C, 178, 800, t, 0.12, 0.7, n=10, L=34.0, R=46.0, col=(255, 255, 255))
    F.spr(C, l_new, 292, 1336, 0.15, te, anchor='tc')
    for i, (cam, st, kb, c, tx, P0, vel, box) in enumerate(LENSES):
        ti = 0.3 + 0.2 * i
        F.lens(C, cam, st, c[0], c[1], R_L, ti, te, kb=kb, ring=RED, tag='h16')
        lens_flakes(C, c, kb, P0, vel, box, F.pop(t, ti + 0.2, te), seed=i, n_fix=9 if i == 1 else 0)
    for i, x in enumerate(LENSES): F.spr(C, l_len[i], x[3][0], x[3][1] + R_L - 30, 0.45 + 0.2 * i, te, anchor='tc')
    F.spr(C, l_old, 540, 1600, 0.9, te, anchor='tc')
HOOK = [S.plain(E, 0.0, E.T_S, ov_hook, tr=None)]

# ------------------------------------------------------------------ semnele: merge bine o vreme, apoi erorile de presiune se intorc si injectoarele cedeaza unul cate unul
SIGNS = S.symptoms(E, 2, [(E.sym('odo', 'MERGE BINE O VREME', 'După pompa schimbată', cls='good'), 'merge'), (E.sym('ecu', 'ERORILE DE PRESIUNE SE ÎNTORC'), 'erorile'),
                          (E.sym('warn', 'INJECTOARELE CEDEAZĂ', 'Unul câte unul'), 'injectoarele')], cam='pw', st='fuel', kb=S.KB_PW, fx=[S.fx_fuel()], phase=None)

# ------------------------------------------------------------------ o pompa roasa nu-si tine pilitura: o trimite in rampa, in injectoare si, prin retur, in rezervor
T_3B = W(3, 'trimite') - 0.3
SPREAD = [
 Shot('pm', L(3), T_3B, st='damf', kb=[(L(3), 1.04, 0, 0), (T_3B, 1.1, 0, 0)], phase=False, tr=('xf', 0.3),
      fx=[S.fx_dry(L(3), rate=8.0, amp=0.7, size=0.2, speed=30.0), S.fx_flakes(L(3) + 0.1)],
      ov=S.bl(E, [('O POMPĂ ROASĂ PE DINĂUNTRU', 'bad', L(3) + 0.15), ('NU-ȘI ȚINE PILITURA PENTRU EA', 'bad big', W(3, 'nu') - 0.15)], T_3B)),
 S.sysm(E, T_3B, L(4), hl=[(['pump'], None, T_3B + 0.1), (['rail'], None, W(3, 'rampa') - 0.2), (['inj'], None, W(3, 'injectoare') - 0.2), (['tank'], None, W(3, 'rezervor') - 0.2)],
        flows=[('lp', S.LP2, 14, 210.0, 4.5, None), ('to_rail', S.METAL2, 12, 170.0, 4.5, T_3B + 0.2), ('rail_inj', S.METAL2, 16, 170.0, 4.5, W(3, 'injectoare') - 0.5),
               ('ret', S.METAL2, 16, 230.0, 4.0, W(3, 'injectoare') + 0.1), ('tank', S.METAL2, 20, 150.0, 4.0, W(3, 'rezervor') - 0.5)],
        labs=[('PILITURA PLEACĂ ODATĂ CU MOTORINA', 'bad', T_3B + 0.2), ('RAMPĂ, INJECTOARE, RETUR, REZERVOR', 'bad', W(3, 'in') - 0.1)]),
]

# ------------------------------------------------------------------ fulgii au de la cativa microni la cateva sute; cei mai mici ajung in injectoare si se aseaza pe supapa de comanda
T_4B = W(4, 'cei') - 0.12; T_SET = W(4, 'se') - 0.2
V_IN = [(1075, 1475), (930, 1560), (820, 1645), (735, 1585), (668, 1528), (590, 1500), (545, 1440), (539, 1380), (539, 1195)]      # din conducta de inalta presiune, prin camera de comanda, pana sub bila (placa valve:shut)
def ov_sizes(C):
    for i, (n, r, sp) in enumerate(((30, 2.4, 190.0), (11, 5.5, 160.0), (5, 11.5, 130.0))):
        S.flowp(C, [(540, -60), (540, 1980)], n, sp, S.METAL2, r, lat=52.0 - r, seed=11 + i, glow=0.5, dark=0.55)
l_ball = E.lb('BILA SUPAPEI', 'grey')
def ov_valve(C):
    t = C.t; z = C.shot.kbat(t)[0]; te = L(5) + 0.1
    S.flowp(C, V_IN, 22, 230.0, S.METAL2, 4.2, t0=T_4B - 1.6, lat=13.0, seed=5, glow=0.5, dark=0.5)
    bx, by = S.pk(C, [tuple(BALL)])[0]
    F.label(C, l_ball, ('px', bx + 42 * z, by - 12 * z), (1040, 640), T_4B + 0.5, te, anchor='tr')
    for i in range(14):
        ta = T_SET + i * 0.13
        if t < ta: continue
        x, y = S.pk(C, [tuple(SEAT[i])])[0]
        D.dots2(C, np.array([[x, y]]), (4.0 + 3.0 * VR[i, 2]) * z, S.METAL2, 1.0, 0.5)
        D.arc(C, x, y, 11 * z, 0, 360, RED, 3, 0.7 * (0.55 + 0.45 * math.sin((t - ta) * 10)))
        if i % 3 == 0: S.sparks2(C, x, y, t, ta, ta + 0.4, n=8, L=16.0, R=20.0)
FLAKES = [
 S.film(E, L(4), T_4B, st='mclean', head='ÎN CONDUCTA DE INJECȚIE, MĂRIT', sides=None, ov=ov_sizes, kb=[(L(4), 1.7, 0, 0), (T_4B, 1.85, 0, 0)],
        labs=[('FULGI DE METAL', 'bad big', L(4) + 0.15), ('DE LA CÂȚIVA MICRONI LA CÂTEVA SUTE', 'bad', W(4, 'de', 2) - 0.15)]),
 Shot('valve', T_4B, L(5), st='shut', kb=[(T_4B, 1.3, 0, -280), (L(5), 1.4, 0, -384)], phase=False, tr=('xf', 0.3),
      ov=S.ovs(ov_valve, S.tl(E, [('CEI MAI MICI AJUNG ÎN INJECTOARE', 'bad', T_4B + 0.15), ('SE AȘAZĂ PE SUPAPA DE COMANDĂ', 'bad big', T_SET)], L(5)))),
]

# ------------------------------------------------------------------ se schimba doar pompa: pilitura ramasa in conducte, in rampa si in rezervor porneste din nou, spre injectoare si spre pompa noua
T_MV = W(5, 'porneste')
def ov_again(C):
    a = F.pop(C.t, L(5) - 0.1, L(6) + 0.2)
    filings(C, ['to_rail'], 16, 170.0, 4.6, a, T_MV, seed=3)
    filings(C, ['rail_inj'], 18, 170.0, 4.6, a, T_MV, seed=4)
    filings(C, ['ret'], 12, 170.0, 4.2, a, T_MV, seed=5)
    filings(C, ['tank'], 22, 110.0, 4.2, a, T_MV, seed=6, lat=9.0)
    S.sys_flow(C, ['lp'], 12, 150.0, S.METAL2, 4.2, a, t0=T_MV + 0.5, seed=8, glow=0.55)
AGAIN = [S.sysm(E, L(5), L(6), hl=[(['pump'], S.GREEN_HL, W(5, 'pompa') - 0.3, W(5, 'pompa', 2) - 0.1), (['inj'], None, W(5, 'spre') - 0.15), (['pump'], None, W(5, 'pompa', 2) - 0.2)],
               flows=[('lp', S.LP2, 14, 210.0, 4.5, T_MV), ('to_rail', S.HP2, 10, 170.0, 4.5, T_MV + 0.2)], ov=ov_again,
               labs=[('SE SCHIMBĂ DOAR POMPA', 'big', L(5) + 0.15), ('PILITURA A RĂMAS ÎN INSTALAȚIE', 'bad big', W(5, 'pilitura') - 0.15), ('PORNEȘTE DIN NOU LA DRUM', 'bad big', T_MV - 0.1),
                     ('SPRE INJECTOARE ȘI SPRE POMPA NOUĂ', 'bad', W(5, 'spre') - 0.15)])]

# ------------------------------------------------------------------ de aceea producatorii cer mult mai mult: rampa, conducte, injectoare si filtru noi, rezervor golit si curatat
T_6P = W(6, 'pompa') - 0.2; T_6R = W(6, 'rampa') - 0.2; T_6C = W(6, 'conducte') - 0.2; T_6I = W(6, 'injectoare') - 0.2; T_6F = W(6, 'filtru') - 0.2; T_6T = W(6, 'rezervor') - 0.2
def ov_makers(C):
    a = F.pop(C.t, L(6) - 0.1, L(7) + 0.2)
    filings(C, ['to_rail'], 16, 0.0, 4.6, a, t_gone=T_6R + 0.1, seed=3)
    filings(C, ['rail_inj'], 18, 0.0, 4.6, a, t_gone=T_6I, seed=4)
    filings(C, ['ret'], 12, 0.0, 4.2, a, t_gone=T_6I + 0.3, seed=5)
    filings(C, ['tank'], 22, 0.0, 4.2, a, t_gone=W(6, 'golit') - 0.1, seed=6, lat=9.0)
MAKERS = [S.sysm(E, L(6), L(7), hl=[(['pump'], S.GREEN_HL, T_6P), (['rail'], S.GREEN_HL, T_6R), (['hp'], S.GREEN_HL, T_6C), (['inj'], S.GREEN_HL, T_6I), (['filter'], S.GREEN_HL, T_6F),
                                    (['tank'], S.GREEN_HL, T_6T)], ov=ov_makers,
                 labs=[('PRODUCĂTORII CER MULT MAI MULT', 'big', W(6, 'producatorii') - 0.15), ('RAMPĂ, CONDUCTE, INJECTOARE, FILTRU', 'good', W(6, 'si') - 0.1),
                       ('REZERVOR GOLIT ȘI CURĂȚAT', 'good big', T_6T)])]

# ------------------------------------------------------------------ cum eviti: cere sa vezi regulatorul de debit si filtrul vechi; pilitura pe ele = se curata toata instalatia
T_7A = W(7, 'si') - 0.15; T_7B = W(7, 'daca') - 0.12
KB_RS = (0.62, 0, -430)                # sita regulatorului, deasupra cardurilor
KB_F = (0.6, 0, -264)                  # hartia filtrului, deasupra cardurilor
FLK_R = S.pfs(S.pf_cryst(n=110, seed=7, box=(250, 830, 850, 1270), r=(8.0, 19.0), col=(0.5, 0.53, 0.58), edge=(20, 23, 28), amin=0.8))
FLK_F = S.pfs(S.pf_cryst(n=120, seed=9, box=(310, 560, 770, 1290), r=(7.0, 16.0), col=(0.5, 0.53, 0.58), edge=(20, 23, 28), amin=0.8))
hd_ev = S.hd(E, 'CUM EVIȚI', L(7), L(8) + 0.1, 'good big')
cds = S.cards(E, [('CERE SĂ VEZI REGULATORUL DE DEBIT', W(7, 'cere')), ('ȘI FILTRUL VECHI', W(7, 'filtrul')), ('PILITURĂ PE ELE: SE CURĂȚĂ TOT', W(7, 'trebuie')),
                  ('DOAR POMPA SCHIMBATĂ', W(7, 'nu') - 0.1, False)], L(8) + 0.1)
l_fil = E.lb('PILITURĂ', 'bad')
def ov_r(C): F.label(C, l_fil, ('px',) + tuple(S.pk(C, [(720, 1010)])[0]), (1040, 520), W(7, 'regulatorul') - 0.1, T_7A + 0.1, anchor='tr')
def ov_f(C): F.label(C, l_fil, ('px',) + tuple(S.pk(C, [(700, 820)])[0]), (1040, 560), T_7A + 0.4, L(8) + 0.1, anchor='tr')
AVOID = [
 Shot('rgs', L(7), T_7A, st='regfull', kb=[(L(7),) + KB_RS, (T_7A, 0.64, 0, -412)], phase=False, tr=('xf', 0.3), pf=FLK_R, ov=S.ovs(hd_ev, cds, ov_r),
      dim=lambda t: 0.1 * F.pop(t, W(7, 'cere') - 0.2, T_7A + 0.3)),
 Shot('fl', T_7A, L(8), st='ffull', kb=[(T_7A,) + KB_F, (L(8), 0.64, 0, -270)], phase=False, tr=('xf', 0.3), pf=FLK_F, ov=S.ovs(hd_ev, cds, ov_f),
      dim=lambda t: 0.1 + 0.12 * F.pop(t, T_7B, L(8) + 0.3)),
]

# ------------------------------------------------------------------ ce facem noi: odata cu pompa curatam injectoarele, rampa si conductele; injectoarele pe stand, pana la 2.400 de bari;
# recomandam si curatarea rezervorului si a traseului; pompa reconditionata ajunge intr-o instalatie curata
T_8B = W(8, 'iar') - 0.1; T_9B = W(9, 'asa') - 0.12
bar = E.add('<div class="stat y" style="padding:12px 34px 16px"><span style="font-size:30px;margin-top:0;color:#b6c2cf">PÂNĂ LA</span><b style="font-size:118px">2.400</b><span style="font-size:36px">BAR</span></div>')
def ov_bar(C): F.spr(C, bar, 850, 470, W(8, 'pana') - 0.25, L(9) + 0.2, anchor='tc')
TK = X.rnd(91, 30, 3)
T_CL0 = W(9, 'curatarea') - 0.1; T_CL1 = W(9, 'traseu') + 0.2
def ov_tank(C):
    t = C.t; z = C.shot.kbat(t)[0]
    xs = 150 + 780 * TK[:, 0]; ys = 1163 + 11 * TK[:, 1]
    al = 1.0 - np.clip((t - (T_CL0 + (T_CL1 - T_CL0) * (xs - 150) / 780.0)) / 0.35, 0, 1)
    keep = al > 0.02
    if keep.any():
        Q = np.array(S.pk(C, list(zip(xs[keep], ys[keep]))))
        D.dots2(C, Q, (4.0 + 3.5 * TK[keep, 2]) * z * al[keep] * (0.8 + 0.3 * np.sin(t * 6.0 + xs[keep])), S.METAL2, 1.0, 0.55)
    u = float(seg(t, T_CL0, T_CL1))
    if 0.0 < u < 1.0:
        x, y = S.pk(C, [(150 + 780 * u, 1166)])[0]
        D.dots2(C, np.array([[x, y], [x, y - 22 * z]]), np.array([13.0, 8.0]) * z, (200, 240, 255), 0.8, 0.9)
hid = E.lb('CE FACEM NOI LA TURBO DOCTOR', 'big')
ALLC = ['tank', 'epump', 'filter', 'lp', 'pump', 'reg', 'hp', 'rail', 'inj']
def ov_clean(C): F.spr(C, hid, 540, 372, E.T_NOI - 0.05, L(E.OUT) + 0.2, anchor='tc')
NOI = [
 S.wk_usb(E, L(8), T_8B, labs=[('ODATĂ CU POMPA', 'good big', W(8, 'odata') - 0.15), ('CURĂȚĂM INJECTOARELE, RAMPA, CONDUCTELE', 'good', W(8, 'curatam') - 0.15)], t_dip=W(8, 'curatam') - 0.3),
 S.wk_inj(E, T_8B, L(9), labs=[('INJECTOARELE: TESTATE PE STAND', 'good big', T_8B + 0.15)], ov=ov_bar),
 S.wk(E, 'tank', L(9), T_9B, [('RECOMANDĂM: REZERVOR ȘI TRASEU CURĂȚATE', 'good', L(9) + 0.15)], st='dry', kb=[(L(9), 1.0, 0, -20), (T_9B, 1.06, 0, -30)], ov=ov_tank, y=1200),
 S.sysm(E, T_9B, L(E.OUT), hl=[(ALLC, S.GREEN_HL, T_9B + 0.25)], flows=[('lp', S.LP2, 16, 210.0, 5.0, None), ('to_rail', S.HP2, 12, 170.0, 5.0, None), ('rail_inj', S.HP2, 16, 170.0, 5.0, None)],
        ov=S.ovs(ov_clean, S.tl(E, [('POMPA RECONDIȚIONATĂ', 'good big', T_9B + 0.15), ('ÎNTR-O INSTALAȚIE CURATĂ', 'good big', W(9, 'instalatie') - 0.4)], L(E.OUT), y=452))),
]

SHOTS = S.opening(E, HOOK) + [SIGNS] + SPREAD + FLAKES + AGAIN + MAKERS + AVOID + NOI + [S.ending(E)]
SPR = E.SPR
