# Episodul 13: tachetul pompei CP4
import math
import numpy as np
import pser as S, ifx as F, i2d as D, ikit as K, pdraw as P, fxlib as X
from icomp import Shot
from fxlib import seg, ease
E = S.Ep(13); W, L, LE = E.W, E.L, E.LE; TOTAL = E.TOTAL; GLOB = S.glob(E)
RED = (255, 75, 75); GREEN = (61, 220, 132); YEL = (255, 210, 31); GREY = (150, 162, 175)
FILM_Y = S.pf_tint(S.LPY, which='hp')
H0 = S.H0
P_CAM = np.array([0.0, -7.0, H0 - 18.0]); P_ROL = S.P_roller(H0); P_TAP = S.P_tappet(H0); P_PIS = np.array([2.2, -2.4, H0 + 20.0])
ROL_PX = (490, 727); ROL_RT = (512, 727); CON_PX = (491, 797)                   # rola si contactul cu cama, pe placile pc (px la 1080)
D.ICON2.setdefault('knock', '<svg width="80" height="80" viewBox="0 0 64 64"><path d="M12 50 L32 30" stroke="#FFB224" stroke-width="7" stroke-linecap="round"/>'
                   '<rect x="26" y="10" width="26" height="15" rx="3" transform="rotate(45 39 17.5)" fill="none" stroke="#FFB224" stroke-width="5"/>'
                   '<path d="M44 40a9 9 0 0 1 0 12M51 35a16 16 0 0 1 0 22" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round"/></svg>')

def kbz(P3, z, tx, ty, cam='pc', st='fuel'): return S.kb_on(cam, st, P3, z, tx, ty)
def ring_px(C, p, R, t_in, t_out, col=RED, th=6):
    t = C.t; z = C.shot.kbat(t)[0]; x, y = S.pk(C, [p])[0]
    D.arc(C, x, y, R * z, 0, 360, col, th, F.pop(t, t_in, t_out) * (0.75 + 0.25 * math.sin(t * 7.0)))

# ------------------------------------------------------------------ tachetul vazut de sus (desen 2D): rotund in locas, cu rola deasupra camei; cama trece de sus in jos
ANG = list(range(-15, 95, 5))
TT = {a: E.add(P.tappet_top(a, 620, uid='tt%d' % i)) for i, a in enumerate(ANG)}
TT_BAD = E.add(P.tappet_top(90, 620, bad=True, uid='ttb'))
TCX, TTOP = 540, 440; TCY = TTOP + 310
l_cama = E.lb('CAMA', 'grey')
def top_view(C, ang, bad, t_in, t_out):
    t = C.t; a = F.pop(t, t_in, t_out)
    if a <= 0.003: return
    k = min(ANG, key=lambda v: abs(v - ang))
    F.spr(C, TT_BAD if (bad and k == 90) else TT[k], TCX, TTOP, t_in, t_out, anchor='tc')
    for x in (172, 908): S.arrow2(C, (x, 520), (x, 1010), YEL, 8, a, head=24)
    F.spr(C, l_cama, 908, 450, t_in + 0.1, t_out, anchor='tc')
hd_top = lambda t0, t1: S.hd(E, 'TACHETUL, VĂZUT DE SUS', t0, t1, 'grey big')

# ------------------------------------------------------------------ carligul: rola se rostogoleste pe cama; tachetul se rasuceste un sfert de tura; rola alunecata de-a latul face pilitura
# (coperta, la 1,85 s: titlul sus, rola rasucita pe cama, cu scantei si fulgi argintii)
T_T = 0.75; T_R = 1.45
KBH = kbz(P_ROL, 1.35, 540, 1000)
l_h1 = E.lb('ROLA SE ROSTOGOLEȘTE PE CAMĂ', 'grey big'); l_h2 = E.lb('TACHETUL SE RĂSUCEȘTE', 'bad big'); l_h3 = E.lb('ROLA ALUNECĂ: CAMA FACE PILITURĂ', 'bad big')
def ov_hook(C):
    t = C.t; te = E.T_S + 0.1
    F.spr(C, l_h1, 540, 1640, 0.05, T_T, anchor='tc'); F.spr(C, l_h2, 540, 1640, T_T, T_R, anchor='tc'); F.spr(C, l_h3, 540, 1640, T_R - 0.05, te, anchor='tc')
    ring_px(C, ROL_PX if t < T_R else ROL_RT, 96, T_T - 0.05, te)
HOOK = [Shot('pc', 0.0, T_T, st='fuel', kb=[(0.0,) + KBH, (T_T, KBH[0] * 1.02, KBH[1], KBH[2])], phase=lambda t: t - T_T, fx=[S.fx_fuel()], tr=None, ov=ov_hook),
        Shot('pc', T_T, T_R, st='rotturn', kb=[(T_T, KBH[0] * 1.02, KBH[1], KBH[2]), (T_R, KBH[0] * 1.04, KBH[1], KBH[2])], phase=lambda t: min(0.999, max(0.0, (t - T_T) / (T_R - T_T))),
             fx=[S.fx_fuel(a=0.35)], tr=None, ov=ov_hook),
        Shot('pc', T_R, E.T_S, st='rotdam', kb=[(T_R, KBH[0] * 1.04, KBH[1], KBH[2]), (E.T_S, KBH[0] * 1.08, KBH[1], KBH[2])], phase=lambda t: (t - T_R) * 0.6 + 1.0,
             fx=[S.fx_dry(T_R - 0.05), S.fx_flakes(T_R, n=110)], tr=None, ov=ov_hook)]

# ------------------------------------------------------------------ semnele (din ancheta NHTSA): martorul de motor, pornire grea, pierdere de putere, zgomot de bataie mai tare, apoi avarie sau motor oprit in mers
SIGNS = S.symptoms(E, 2, [(E.sym('engine', 'MARTORUL DE MOTOR'), 'martorul'), (E.sym('start', 'PORNIRE GREA'), 'pornire'), (E.sym('power', 'PIERDERE DE PUTERE'), 'pierdere'),
                          (E.sym('knock', 'ZGOMOT DE BĂTAIE MAI TARE'), 'zgomot'), (E.sym('stall', 'AVARIE SAU MOTOR OPRIT', 'În mers'), 'avarie')],
                   cam='pw', st='fuel', kb=S.KB_PW, fx=[S.fx_fuel()], phase=None, y0=630, dy=126)

# ------------------------------------------------------------------ pompa CP4: pe arbore e o cama, pe cama calca o rola tinuta intr-un tachet, care impinge pistonul
T_3B = W(3, 'pe') - 0.2
KB3 = kbz(P_ROL, 1.1, 540, 820)
labs3 = [(E.lb('ARBORELE CU CAMĂ', 'lp'), P_CAM, (1040, 1110), W(3, 'arborele') - 0.1), (E.lb('ROLA', 'lp'), P_ROL, (1040, 880), W(3, 'rola') - 0.1),
         (E.lb('TACHETUL', 'lp'), P_TAP, (1040, 700), W(3, 'tachet') - 0.1), (E.lb('PISTONUL', 'lp'), P_PIS, (1040, 520), W(3, 'pistonul') - 0.1)]
def ov_parts(C):
    for sid, p3, box, ti in labs3: F.label(C, sid, p3, box, ti, L(4) + 0.1, anchor='tr')
CP4 = [
 S.pump(E, 'pw', L(3), T_3B, st='fuel', labs=[('POMPA CP4', 'big', W(3, 'cp4') - 0.1), ('PE FOARTE MULTE DIESELE MODERNE', 'grey', W(3, 'foarte') - 0.1)]),
 Shot('pc', T_3B, L(4), st='fuel', kb=[(T_3B,) + KB3, (L(4), 1.14, KB3[1], KB3[2] + 10)], fx=[S.fx_fuel()], tr=('xf', 0.3), ov=ov_parts),
]

# ------------------------------------------------------------------ cat timp rola sta dreapta se rostogoleste pe cama, pe o pelicula de motorina; dar tachetul e rotund si se poate rasuci in locas
T_4F = W(4, 'pe', 2) - 0.25; T_4T = W(4, 'numai') - 0.15
KB4 = kbz(P_ROL, 1.5, 540, 880)
T_WOB = W(4, 'rasuci') - 0.15
def wob(t): return 13.0 * math.sin(2 * math.pi * (t - T_WOB) / 1.3) * float(seg(t, T_WOB, T_WOB + 0.3)) * (1.0 - float(seg(t, L(5) - 0.5, L(5))))
def ov_top4(C):
    t = C.t; te = L(5) + 0.1
    top_view(C, wob(t), False, T_4T, te)
    D.arc(C, TCX, TCY, 214, 0, 360, YEL, 6, F.pop(t, W(4, 'rotund') - 0.1, W(4, 'poate') - 0.2) * (0.7 + 0.3 * math.sin(t * 7.0)))
ROLL = [
 Shot('pc', L(4), T_4F, st='fuel', kb=[(L(4),) + KB4, (T_4F, 1.56, KB4[1], KB4[2])], fx=[S.fx_fuel()], tr=('xf', 0.3),
      ov=S.ovs(lambda C: ring_px(C, ROL_PX, 80, W(4, 'rola') - 0.1, T_4F + 0.1, col=GREEN),
               S.bl(E, [('ROLA STĂ DREAPTĂ', 'good big', W(4, 'rola') - 0.1), ('SE ROSTOGOLEȘTE PE CAMĂ', 'good big', W(4, 'rostogoleste') - 0.1)], T_4F))),
 S.film(E, T_4F, T_4T, pf=FILM_Y, flow=((255, 236, 150), None), labs=[('PE O PELICULĂ DE MOTORINĂ', 'lp big', W(4, 'pelicula') - 0.15)], kb=[(T_4F, 1.0, 0, 0), (T_4T, 1.05, 0, 0)]),
 S.plain(E, T_4T, L(5), S.ovs(ov_top4, hd_top(T_4T + 0.05, L(5) + 0.1),
                              S.bl(E, [('TACHETUL E ROTUND', 'big', W(4, 'tachetul') - 0.1), ('SE POATE RĂSUCI ÎN LOCAȘUL LUI', 'bad big', W(4, 'poate') - 0.25)], L(5)))),
]

# ------------------------------------------------------------------ cand ungerea slabeste (aer, benzina, motorina care nu unge), rola se poate intoarce cu un sfert de tura
T_5T = W(5, 'rola') - 0.2
T_A0 = W(5, 'intoarce') - 0.05; T_A1 = W(5, 'tura') + 0.1
LUB = S.symptoms(E, 5, [(E.sym('air', 'AER ÎN INSTALAȚIE'), 'aerului'), (E.sym('fuel', 'BENZINĂ ÎN MOTORINĂ'), 'benzinei'), (E.sym('drop', 'MOTORINĂ CARE NU UNGE'), 'motorine')],
                 cam='microf', st='mclean', kb=(1.0, 0, 0), t1=T_5T, seq=[('mdry', W(5, 'slabeste') - 0.1, W(5, 'slabeste') + 0.7)], pf=FILM_Y, dimk=0.25)
LUB.ov = S.ovs(LUB.ov, S.tl(E, [('UNGEREA SLĂBEȘTE', 'bad big', L(5) + 0.1)], T_5T),
               lambda C: S.flowp(C, [(540, -40), (540, 1960)], 30, 260.0, (255, 236, 150), 4.5, lat=52.0, seed=6, glow=0.3, a=0.8 * (1.0 - float(seg(C.t, W(5, 'slabeste') - 0.1, W(5, 'slabeste') + 0.5)))))
l_90 = E.lb('90°', 'bad big')
def ov_top5(C):
    t = C.t; te = L(6) + 0.1; u = float(ease(seg(t, T_A0, T_A1))); ang = 90.0 * u
    top_view(C, ang, u >= 1.0, T_5T, te)
    if u > 0.01:
        D.arc(C, TCX, TCY, 262, -90.0, -90.0 + ang, RED, 8, F.pop(t, T_A0, te))
        F.spr(C, l_90, TCX + 205, TTOP + 18, T_A1 - 0.25, te, anchor='tc')
TURN = [LUB,
        S.plain(E, T_5T, L(6), S.ovs(ov_top5, hd_top(T_5T + 0.05, L(6) + 0.1),
                                     S.bl(E, [('ROLA SE POATE ÎNTOARCE', 'bad', T_5T + 0.12), ('CU UN SFERT DE TURĂ', 'bad big', W(5, 'sfert') - 0.25)], L(6))))]

# ------------------------------------------------------------------ din clipa aceea nu se mai rostogoleste: aluneca de-a latul pe cama si taie un sant in mijlocul ei
T_6B = W(6, 'aluneca') - 0.15; T_6C = W(6, 'sant') - 0.35
KB6 = kbz(P_ROL, 1.5, 540, 860)
KB6Z = kbz(S.P_contact(H0), 1.8, 540, 760)
SLIDE = [
 Shot('pc', L(6), T_6B, st='rotturn', kb=[(L(6),) + KB6, (T_6B, 1.54, KB6[1], KB6[2])], phase=lambda t: min(0.999, max(0.0, (t - L(6) - 0.2) / 1.1)), fx=[S.fx_fuel(a=0.3)], tr=('xf', 0.3),
      ov=S.ovs(lambda C: ring_px(C, ROL_PX, 80, W(6, 'nu') - 0.2, T_6B + 0.1),
               S.bl(E, [('DIN CLIPA ACEEA', 'grey', L(6) + 0.1), ('NU SE MAI ROSTOGOLEȘTE', 'bad big', W(6, 'nu') - 0.1)], T_6B))),
 Shot('pc', T_6B, T_6C, st='rotdam', kb=[(T_6B, 1.54, KB6[1], KB6[2]), (T_6C, 1.6, KB6[1], KB6[2])], fx=[S.fx_dry(T_6B), S.fx_flakes(T_6B + 0.3, n=90)], tr=('xf', 0.25),
      ov=S.bl(E, [('ALUNECĂ DE-A LATUL PE CAMĂ', 'bad big', T_6B + 0.1)], T_6C)),
 Shot('pc', T_6C, L(7), st='rotdam', kb=[(T_6C,) + KB6Z, (L(7), 1.86, KB6Z[1], KB6Z[2])], fx=[S.fx_dry(T_6C), S.fx_flakes(T_6C, n=90)], tr=('xf', 0.25),
      ov=S.ovs(lambda C: ring_px(C, (491, 840), 70, W(6, 'sant') - 0.1, L(7) + 0.1),
               S.bl(E, [('UN ȘANȚ ÎN MIJLOCUL CAMEI', 'bad big', W(6, 'sant') - 0.15)], L(7)))),
]

# ------------------------------------------------------------------ metalul ros pleaca in fulgi fini in toata instalatia, pana in injectoare si in rezervor
T_7B = W(7, 'toata') - 0.3
KB7 = kbz(P_ROL, 1.15, 540, 820)
SPREAD = [
 Shot('pc', L(7), T_7B, st='rotdam', kb=[(L(7),) + KB7, (T_7B, 1.2, KB7[1], KB7[2])], fx=[S.fx_dry(L(7) - 0.2, rate=8.0, amp=0.7), S.fx_flakes(L(7), n=140, fall=34.0)], tr=('xf', 0.3),
      ov=S.bl(E, [('METALUL ROS', 'bad big', L(7) + 0.15), ('PLEACĂ ÎN FULGI FINI', 'bad big', W(7, 'fulgi') - 0.2)], T_7B)),
 S.sysm(E, T_7B, L(8), hl=[(['pump'], None, T_7B + 0.1), (['rail'], None, T_7B + 0.6), (['inj'], None, W(7, 'injectoare') - 0.2), (['tank'], None, W(7, 'rezervor') - 0.2)],
        flows=[('lp', S.LP2, 14, 210.0, 4.5, None), ('to_rail', S.METAL2, 12, 170.0, 4.5, T_7B + 0.2), ('rail_inj', S.METAL2, 16, 170.0, 4.5, W(7, 'injectoare') - 0.6),
               ('ret', S.METAL2, 16, 230.0, 4.0, W(7, 'injectoare')), ('tank', S.METAL2, 20, 150.0, 4.0, W(7, 'rezervor') - 0.5)],
        labs=[('ÎN TOATĂ INSTALAȚIA', 'bad big', T_7B + 0.2), ('PÂNĂ ÎN INJECTOARE ȘI ÎN REZERVOR', 'bad', W(7, 'pana') - 0.1)]),
]

# ------------------------------------------------------------------ cum eviti: tot ce tine pelicula intreaga; filtru schimbat si aerisit, rezervor care nu ajunge la fund, niciodata benzina
T_8B = W(8, 'filtru') - 0.25; T_8C = W(8, 'rezervor') - 0.25; T_8D = W(8, 'niciodata') - 0.25
ITEMS = [('FILTRU SCHIMBAT ȘI AERISIT CORECT', W(8, 'filtru')), ('REZERVOR CARE NU AJUNGE LA FUND', W(8, 'rezervor')), ('NICIODATĂ BENZINĂ', W(8, 'niciodata'))]
hd_ev = S.hd(E, 'CUM EVIȚI', L(8), L(9) + 0.1, 'good big')
DISP = E.add(P.dispenser(380, plate='BENZINĂ', top='BENZINĂ', col='#3ddc84'))
def ov_benz(C):
    t = C.t; te = L(9) + 0.1; a = F.pop(t, T_8D + 0.35, te)
    F.spr(C, DISP, 540, 440, T_8D - 0.1, te, anchor='tc')
    if a > 0.003:
        for (x0, y0), (x1, y1) in (((380, 500), (700, 920)), ((700, 500), (380, 920))):
            D.line2(C, [(x0, y0), (x1, y1)], (20, 10, 10), 34, a * 0.6); D.line2(C, [(x0, y0), (x1, y1)], RED, 24, a)
AVOID = [
 S.film(E, L(8), T_8B, pf=FILM_Y, flow=((255, 236, 150), None), head=None, labs=[('TOT CE ȚINE PELICULA ÎNTREAGĂ', 'good big', W(8, 'tot') - 0.1)], ov=hd_ev,
        kb=[(L(8), 1.0, 0, 0), (T_8B, 1.05, 0, 0)]),
 S.avoid(E, 'fl', 'ffull', T_8B, T_8C, ITEMS, kb=[(T_8B, 0.52, 0, -205), (T_8C, 0.54, 0, -210)]),
 S.avoid(E, 'tank', 'dry', T_8C, T_8D, ITEMS, kb=[(T_8C, 0.85, 0, -170), (T_8D, 0.87, 0, -172)]),
 S.avoid(E, 'blank', 'none', T_8D, L(9), ITEMS, dim=0, ov=ov_benz),
]

# ------------------------------------------------------------------ ce facem noi: reconditionam pompele CP4; pilitura la microscop; verificam cama, rola si tachetul; piese noi; banc; injectoarele pe stand
T_9B = W(9, 'cautam') - 0.25; T_9C = W(9, 'verificam') - 0.2; T_10B = W(10, 'iar') - 0.15; T_10C = W(10, 'verificam') - 0.2
chk9 = [(E.chk('CAMA'), P_CAM, (1040, 1100), W(9, 'cama') - 0.1), (E.chk('ROLA'), P_ROL, (1040, 900), W(9, 'rola') - 0.1), (E.chk('TACHETUL'), P_TAP, (1040, 700), W(9, 'tachetul') - 0.1)]
def ov_chk(C):
    for sid, p3, box, ti in chk9: F.label(C, sid, p3, box, ti, L(10) + 0.1, anchor='tr')
NOI = [
 S.wk(E, 'wm', L(9), T_9B, [('RECONDIȚIONĂM POMPELE CP4', 'good big', W(9, 'reconditionam') - 0.15)], st='wkdam'),
 S.wk_mic(E, T_9B, T_9C, labs=[('CĂUTĂM PILITURA, LA MICROSCOP', 'good big', T_9B + 0.12)], lens=(T_9B + 0.3, T_9C + 0.1), lens_src=('pc', 'rotdam', S.LENS_KB)),
 S.wk(E, 'pc', T_9C, L(10), [('VERIFICĂM', 'good big', T_9C + 0.12)], st='rotdam', kb=[(T_9C,) + KB3, (L(10), 1.14, KB3[1], KB3[2] + 10)], ov=ov_chk),
 S.wk_mic(E, L(10), T_10B, labs=[('PIESELE ROASE', 'bad big', L(10) + 0.12), ('SE ÎNLOCUIESC CU PIESE NOI', 'good big', W(10, 'inlocuiesc') - 0.15)], t_new=W(10, 'piese') - 0.15),
 S.wk_bench(E, T_10B, T_10C, labs=[('POMPA E TESTATĂ PE BANC', 'good big', T_10B + 0.12)], rows=[('DEBIT', W(10, 'testata')), ('PRESIUNE', W(10, 'banc'))], t_sheet=T_10B + 0.2),
 S.wk_inj(E, T_10C, L(E.OUT), labs=[('VERIFICĂM PE STAND ȘI INJECTOARELE', 'good', T_10C + 0.12), ('LA CARE AU AJUNS FULGII', 'bad big', W(10, 'la') - 0.1)]),
]

SHOTS = S.opening(E, HOOK) + [SIGNS] + CP4 + ROLL + TURN + SLIDE + SPREAD + AVOID + NOI + [S.ending(E)]
SPR = E.SPR
