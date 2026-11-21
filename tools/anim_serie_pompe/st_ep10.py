# Episodul 10: pompa de alimentare din rezervor, slabita
import math
import numpy as np
import pser as S, ifx as F, i2d as D, ikit as K, pdraw as P, fxlib as X
from icomp import Shot
from fxlib import seg, ease
E = S.Ep(10); W, L, LE = E.W, E.L, E.LE; TOTAL = E.TOTAL; GLOB = S.glob(E)

KB_TM = (0.76, 30, -80)          # modulul pompei electrice, intreg, intre insigna si subtitrare
def tank_flow(C, t0=None, a=1.0, n=14, sp=260.0):
    """motorina urca din sorb, prin modul, pe conducta spre motor"""
    S.flowp(C, S.TANK_OUT, n, sp, S.LP2, 5.0, t0=t0, a=a, seed=5, glow=0.3, lat=2.0)

# ------------------------------------------------------------------ carligul: rezervorul cu pompa electrica; manometrul de pe conducta coboara (coperta: acul jos, eticheta rosie)
l_ep = E.lb('POMPA ELECTRICĂ DIN REZERVOR', 'lp'); l_drop = E.lb('DĂ TOT MAI PUȚINĂ PRESIUNE', 'bad big'); l_feed = E.lb('ALIMENTARE', 'grey')
def ov_hook(C):
    t = C.t; te = E.T_S + 0.1
    v = 0.8 - 0.56 * float(ease(seg(t, 0.35, 1.5))) + 0.015 * math.sin(t * 9.0)
    tank_flow(C, a=1.0 - 0.6 * float(seg(t, 0.4, 1.6)), n=16)
    S.gauge(C, 832, 838, 92, v, F.pop(t, 0.0, te), green=(0.6, 1.0)); F.spr(C, l_feed, 600, 800, 0.1, te, anchor='tr')
    F.spr(C, l_ep, 540, 1470, 0.1, 1.0, anchor='tc'); F.spr(C, l_drop, 540, 1462, 1.12, te, anchor='tc')
HOOK = [S.tank(E, 0.0, E.T_S, kb=[(0.0, 0.9, 0, 260), (E.T_S, 0.93, 0, 262)], tr=None, ov=ov_hook)]

SIGNS = S.symptoms(E, 2, [(E.sym('start', 'PORNIRE GREA'), 'pornire'), (E.sym('power', 'LIPSĂ DE PUTERE', 'La accelerare'), 'lipsa'),
                          (E.sym('warn', 'BÂZÂIT DIN ZONA REZERVORULUI', 'Uneori, mai puternic', cls='warn'), 'bazait')], cam='tm', st='tmfuel', kb=KB_TM)

# ------------------------------------------------------------------ pompa de inalta presiune nu trage singura: primeste motorina, sub presiune, de la pompa electrica din rezervor
T_3B = W(3, 'pompa', 2) - 0.42
l_mot = E.lb('MOTORAȘUL', 'grey'); l_sock = E.lb('SITA', 'grey'); l_float = E.lb('PLUTITORUL', 'grey')
def ov_parts(C):
    te = L(4) + 0.12
    for sid, pt, box, an, dt in ((l_mot, (665, 1250), (1052, 800), 'tr', 0.25), (l_sock, (700, 1486), (1052, 1060), 'tr', 0.55), (l_float, (90, 930), (36, 690), None, 0.85)):
        x, y = S.pk(C, [pt])[0]
        if an: F.label(C, sid, ('px', x, y), box, T_3B + dt, te, anchor=an)
        else: F.label(C, sid, ('px', x, y), box, T_3B + dt, te)
FEED = [
 S.sysm(E, L(3), T_3B, hl=[(['pump'], S.YEL_HL, L(3) + 0.3), (['epump', 'tank'], S.GREEN_HL, W(3, 'primeste') - 0.2)], flows=[('lp', S.LP2, 16, 210.0, 5.0, W(3, 'primeste') - 0.25)],
        labs=[('POMPA DE ÎNALTĂ PRESIUNE NU TRAGE SINGURĂ', 'lp', L(3) + 0.25), ('PRIMEȘTE MOTORINA SUB PRESIUNE', 'lp big', W(3, 'primeste') - 0.2)]),
 Shot('tm', T_3B, L(4), st='tmfuel', kb=[(T_3B,) + KB_TM, (L(4), 0.79, 30, -84)], phase=False, tr=('xf', 0.3),
      ov=S.ovs(ov_parts, S.bl(E, [('POMPA ELECTRICĂ DIN REZERVOR', 'lp big', T_3B + 0.15)], L(4)))),
]

# ------------------------------------------------------------------ pompa electrica se uzeaza: sita se infunda, contactele se incing; presiunea si debitul scad
T_4B = W(4, 'ori') - 0.12; T_4C = W(4, 'nu') - 0.25
SLUDGE = S.pfs(S.pf_cryst(n=190, seed=5, box=(392, 1296, 812, 1452), r=(9.0, 22.0), col=(0.2, 0.13, 0.07), edge=(26, 17, 9), t0=W(4, 'infunda') - 0.3, t1=T_4B - 0.2, liq=True),
               S.pf_cryst(n=60, seed=6, box=(300, 1180, 900, 1320), r=(6.0, 13.0), col=(0.24, 0.16, 0.09), edge=(30, 20, 10), t0=W(4, 'infunda') - 0.1, t1=T_4B - 0.2, only_liq=True))
DIRT = [[(140, 1500), (330, 1440), (470, 1400)], [(960, 1480), (850, 1430), (740, 1400)], [(590, 1620), (600, 1500), (600, 1420)]]
l_sock2 = E.lb('SITA', 'bad')
def ov_sock(C):
    te = T_4B + 0.12
    for i, pth in enumerate(DIRT): S.flowp(C, pth, 7, 70.0, S.DUST2, 5.0, t0=W(4, 'infunda') - 0.6, seed=11 + i, lat=6.0, dark=0.9)
    x, y = S.pk(C, [(470, 1376)])[0]; F.label(C, l_sock2, ('px', x, y), (50, 940), W(4, 'sita') - 0.25, te)
plug = E.add(P.plug(320)); l_plug = E.lb('MUFA POMPEI', 'grey'); l_pd = E.lb('PRESIUNE', 'grey')
def ov_plug(C):
    t = C.t; te = L(5) + 0.12; a = F.pop(t, T_4B + 0.15, te)
    F.spr(C, plug, 40, 500, T_4B + 0.15, te); F.spr(C, l_plug, 200, 742, T_4B + 0.3, te, anchor='tc')
    x, y = S.pk(C, [(560, 300)])[0]; S.dash2(C, (330, 560), (x - 30, y + 6), (232, 237, 243), 4, a, n=7)
    ag = F.pop(t, T_4C, te); v = 0.8 - 0.55 * float(ease(seg(t, T_4C + 0.2, L(5) - 0.5))) + 0.015 * math.sin(t * 8.0)
    S.gauge(C, 880, 600, 104, v, ag, green=(0.6, 1.0)); F.spr(C, l_pd, 880, 724, T_4C, te, anchor='tc')
WEAK = [
 Shot('tmz', L(4), T_4B, st='tmfuel', kb=[(L(4), 0.8, 0, -200), (T_4B, 0.84, 0, -216)], phase=False, tr=('xf', 0.3), pf=SLUDGE,
      ov=S.ovs(ov_sock, S.bl(E, [('POMPA ELECTRICĂ SE UZEAZĂ ȘI EA', 'bad', L(4) + 0.15), ('SITA SE ÎNFUNDĂ CU MURDĂRIE', 'bad big', W(4, 'infunda') - 0.25)], T_4B))),
 Shot('tm', T_4B, L(5), st='tmfuel', kb=[(T_4B,) + KB_TM, (L(5), 0.79, 30, -84)], phase=False, tr=('xf', 0.3),
      ov=S.ovs(ov_plug, S.bl(E, [('CONTACTELE SE ÎNCING', 'bad big', T_4B + 0.2), ('PRESIUNE ȘI DEBIT MAI MICI', 'bad big', T_4C + 0.1)], L(5)))),
]

# ------------------------------------------------------------------ pompa de inalta presiune ramane cu prea putina motorina; piesele ei se uzeaza mai repede
T_5B = W(5, 'iar') - 0.1
HUNGRY = [
 S.sysm(E, L(5), T_5B, hl=[(['epump'], None, L(5) + 0.1), (['pump'], None, W(5, 'ramane') - 0.2), (['rail'], None, W(5, 'presiunea') - 0.2)],
        flows=[('lp', S.LP2, 4, 80.0, 5.0, None)],
        labs=[('PREA PUȚINĂ MOTORINĂ LA POMPĂ', 'bad big', L(5) + 0.2), ('NU MAI ȚINE PRESIUNEA ÎN RAMPĂ', 'bad big', W(5, 'nu') - 0.1)]),
 Shot('pc', T_5B, L(6), st='fuel', seq=[('wear', W(5, 'se') - 0.2, W(5, 'repede') + 0.3)], kb=[(T_5B, 1.0, 0, 0), (L(6), 1.08, 0, 0)], phase=False, tr=('xf', 0.3),
      fx=[S.fx_fuel(n=12, a=0.4, speed=9.0)],
      ov=S.bl(E, [('UNSE ȘI RĂCITE TOT DE MOTORINĂ', 'lp', T_5B + 0.15), ('SE UZEAZĂ MAI REPEDE', 'bad big', W(5, 'se') - 0.2)], L(6))),
]

# ------------------------------------------------------------------ greseala scumpa: se schimba pompa de inalta presiune, iar defectul ramane
l_new = E.lb('POMPĂ NOUĂ', 'good'); l_rem = E.lb('DEFECTUL A RĂMAS', 'bad big'); l_guilty = E.lb('VINOVATA: POMPA DIN REZERVOR', 'bad')
def ov_mist(C):
    t = C.t; te = L(7) + 0.1; tp = W(6, 'schimba') - 0.3; tg = W(6, 'pentru') - 0.2
    S.plate_spr(C, 'pw', 'full', 290, 700, 0.42, F.pop(t, L(6) + 0.25, te), crop=(60, 380, 1040, 1500), tag='new10')      # pompa e pe ecran de la inceput, nu doar de la „schimba”
    F.spr(C, l_new, 290, 944, tp + 0.25, te, anchor='tc')
    F.spr(C, l_rem, 540, 1024, W(6, 'defectul') - 0.12, te, anchor='tc')
    S.plate_spr(C, 'tm', 'tmfuel', 812, 690, 0.36, F.pop(t, tg, te), crop=(180, 250, 920, 1540), tag='tm10')
    S.arrow2(C, (506, 700), (640, 700), (255, 75, 75), 11, F.pop(t, tg + 0.1, te), prog=float(seg(t, tg + 0.1, tg + 0.45)))
    D.arc(C, 812, 690, 236, 0, 360, (255, 75, 75), 7, F.pop(t, W(6, 'vinovata') - 0.15, te))
    F.spr(C, l_guilty, 540, 1112, W(6, 'vinovata') - 0.15, te, anchor='tc')
MISTAKE = S.plain(E, L(6), L(7), S.ovs(S.hd(E, 'O GREȘEALĂ SCUMPĂ', L(6) + 0.15, L(7) + 0.1, 'bad big'), ov_mist))

# ------------------------------------------------------------------ cum eviti: nu cu rezervorul aproape gol (motorina raceste pompa electrica), filtrul schimbat la timp
AVOID = S.avoid(E, 'tank', 'dry', L(7), L(8), [('NU MERGE CU REZERVORUL APROAPE GOL', W(7, 'nu') - 0.05, False), ('MOTORINA RĂCEȘTE POMPA ELECTRICĂ', W(7, 'pentru')), ('SCHIMBĂ FILTRUL LA TIMP', W(7, 'schimba'))],
                kb=[(L(7), 1.0, 0, -150), (L(8), 1.04, 0, -160)], wipe=('empty', 0.0, 0.1, 14, 'drop', (S.TANK_TOP, 1118), None), dim=0)

# ------------------------------------------------------------------ ce facem noi: testul pe banc desparte cele doua pompe
T_8B = W(8, 'daca') - 0.1; T_G = W(9, 'cu') - 0.3
v_ok = E.lb('NU O SCHIMBI DEGEABA', 'good big')
def ov_ok(C): F.spr(C, v_ok, 540, 1186, W(8, 'nu') - 0.12, L(9) + 0.12, anchor='tc')
gar = S.seal(E, '12', 'LUNI GARANȚIE')
def ov_gar(C): F.spr(C, gar, 850, 470, T_G + 0.25, L(E.OUT) + 0.2, anchor='tc')
NOI = [
 S.wk_bench(E, L(8), T_8B, labs=[('TESTUL PE BANC DESPARTE CELE DOUĂ POMPE', 'good', W(8, 'testul') - 0.1)], kb=[(L(8), 1.0, 0, 0), (T_8B, 1.03, 0, 0)]),
 S.wk_bench(E, T_8B, L(9), rows=[('DEBIT', W(8, 'debitul') - 0.05), ('PRESIUNE', W(8, 'presiunea') - 0.05)], t_sheet=T_8B + 0.15, ov=ov_ok,
            kb=[(T_8B, 1.03, 0, 0), (L(9), 1.07, 0, 0)], tr=('xf', 0.2)),
 S.wk_mic(E, L(9), L(E.OUT), labs=[('DACĂ S-A UZAT, O RECONDIȚIONĂM', 'good big', W(9, 'uzat') - 0.3)], lens=(L(9) + 0.35, T_G + 0.1), lens_src=('pc', 'wear', (0.8, -64, 64)), ov=ov_gar),
]

SHOTS = S.opening(E, HOOK) + [SIGNS] + FEED + WEAK + HUNGRY + [MISTAKE, AVOID] + NOI + [S.ending(E)]
SPR = E.SPR
