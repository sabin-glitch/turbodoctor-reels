# Episodul 7: AdBlue pus in rezervorul de motorina
import math
import numpy as np
import pser as S, ifx as F, i2d as D, ikit as K, pdraw as P, fxlib as X
from icomp import Shot
from fxlib import seg, ease
E = S.Ep(7); W, L, LE = E.W, E.L, E.LE; TOTAL = E.TOTAL; GLOB = S.glob(E)
ADB_T = S.pf_tint(S.ADB); ADB2 = S.ADB2                  # lichidul bleu, peste tot unde a ajuns AdBlue
fl_h = E.add(P.filler(700)); fl_s = E.add(P.filler(640)); fl_ok = E.add(P.filler(640, hl='adblue')); can_r = E.add(P.adblue_can(300, rot=118)); can_b = E.add(P.adblue_can(380)); can_u = E.add(P.adblue_can(210))
l_mot = E.lb('MOTORINĂ', 'lp'); l_adb = E.lb('ADBLUE', 'water')

# ------------------------------------------------------------------ carligul: cele doua busoane, bidonul de AdBlue varsat in cel negru; apoi pompa, cu lichid bleu si cristale albe
# (coperta, la 1,85 s: bidonul si busoanele)
T_H = 2.05; FX0, FY0 = 190, 800                          # busonul negru la (409, 997), cel albastru la (704, 1014)
def ov_hook(C):
    te = T_H + 0.12
    F.spr(C, fl_h, FX0, FY0, -1.0, te); F.spr(C, can_r, 153, 666, -1.0, te)
    D.flow2(C, [D.Poly([(380, 900), (394, 950), (409, 1000)])], 8, 240.0, ADB2, 10.0, t0=-1.0, a=F.pop(C.t, -1.0, te), seed=5, glow=0.35, lat=4.0)
    F.spr(C, l_mot, 409, 1204, 0.3, te, anchor='tc'); F.spr(C, l_adb, 704, 1204, 0.5, te, anchor='tc')
CRY_PC = [S.P_CAM, S.P_roller(S.H0), S.P_tappet(S.H0), np.array([0.0, -22.0, 7.0]), np.array([0.0, -32.0, -3.0]), S.P_SHAFT, F.PR(24.0, -14.0), F.PR(20.0, 16.0)]
l_cry = E.lb('CRISTALE ALBE', 'bad big')
def ov_hook2(C):
    F.label(C, l_cry, S.P_CAM, (540, 1150), T_H + 0.35, E.T_S + 0.1)
HOOK = [
 S.plain(E, 0.0, T_H, ov_hook, tr=None),
 S.pump(E, 'pc', T_H, E.T_S, st='fuel', phase=False, pf=ADB_T, tr=('flash', 0.25), kb=[(T_H, 1.0, 0, 30), (E.T_S, 1.05, 0, 30)],
        fx=[S.fx_fuel(col=S.ADBS, a=0.4), S.fx_blotch(CRY_PC, S.CRY3, T_H + 0.05, T_H + 0.75, R=2.6, n=14, soft=False, spark=0.5)], ov=ov_hook2),
]

SIGNS = S.symptoms(E, 2, [(E.lb('DACĂ MOTORUL A FOST PORNIT', 'grey'), 'daca'), (E.sym('idle', 'MERS NEREGULAT'), 'mers'), (E.sym('stall', 'OPRIRI'), 'opriri'),
                          (E.sym('start', 'NU MAI PORNEȘTE', 'Până la urmă'), 'un')], cam='tank', st='adb', kb=(1.0, 0, -20), y0=650, dy=140)

# ------------------------------------------------------------------ ce este AdBlue si unde ii e locul
T_3L = W(3, 'Locul') - 0.12
def ov_what(C):
    t = C.t; te = L(4) + 0.1
    F.spr(C, can_b, 350, 470, L(3) + 0.05, T_3L + 0.2)
    F.spr(C, can_u, 585, 420, T_3L + 0.1, te); F.spr(C, fl_s, 220, 760, T_3L + 0.1, te)
    tb = W(3, 'buson') - 0.2
    F.spr(C, fl_ok, 220, 760, tb, te, popk=1.0, slide=(0, 0))
    S.arrow2(C, (690, 706), (690, 852), (61, 220, 132), 10, F.pop(t, tb, te), prog=float(seg(t, tb, tb + 0.35)))
WHAT = [S.plain(E, L(3), L(4), S.ovs(ov_what, S.bl(E, [('ADBLUE: UREE DIZOLVATĂ ÎN APĂ', 'water big', L(3) + 0.2), ('LOCUL LUI: REZERVORUL CU BUȘON ALBASTRU', 'water', T_3L + 0.1),
                                                     ('DE ACOLO AJUNGE ÎN EVACUARE, NU ÎN MOTOR', 'grey', W(3, 'de') - 0.1)], L(4))))]

# ------------------------------------------------------------------ turnat in motorina: nu se amesteca, coboara la fund, exact de unde trage pompa electrica
T_4C = W(4, 'E') - 0.2; T_4W = W(4, 'greu') + 0.3; T_4S = W(4, 'exact') - 0.1
SINK = [(182, 1000), (192, 1070), (222, 1136), (300, 1160), (520, 1163), (700, 1163)]
l_sorb = E.lb('SORBUL', 'bad')
def ov_tank(C):
    t = C.t; te = L(5) + 0.12
    x, y = S.pk(C, [(24, 730)])[0]
    F.spr(C, can_r, x - 237, y - 258, L(4) - 0.6, T_4C + 0.1, slide=(-20, -26))
    S.flowp(C, SINK, 14, 110.0, ADB2, 8.0, t0=L(4) + 0.5, t1=T_4W + 2.0, seed=4, lat=3.0, glow=0.25, dark=0.5)
    S.flowp(C, S.TANK_OUT, 12, 170.0, ADB2, 6.5, t0=W(4, 'trage') - 0.3, seed=9, lat=2.0, glow=0.3, dark=0.6)
    x, y = S.pk(C, [(300, 1066)])[0]; F.spr(C, l_mot, x, y, W(4, 'greu') - 0.1, te, anchor='cc')
    x, y = S.pk(C, [(250, 1166)])[0]; F.label(C, l_adb, ('px', x, y), (96, 1112), W(4, 'coboara') - 0.1, te, side='r')
    x, y = S.pk(C, [(700, 1152)])[0]; F.label(C, l_sorb, ('px', x, y), (800, 1112), T_4S, te, side='l')
TANK = [
 S.tank(E, L(4), L(5), st='dry', seq=[('adb', T_4W, T_4W + 0.6)], wipe=('adb', W(4, 'nu') - 0.2, T_4W, 8, 'up', (1206, 1140), None),
        kb=[(L(4), 0.8, 170, 0), (T_4C, 0.83, 164, -6), (T_4W, 1.0, 0, -110), (L(5), 1.05, 0, -120)],
        ov=S.ovs(S.tank_in(L(4) - 0.1, T_4C - 0.1, col=ADB2, n=34, r=8.5), ov_tank),
        labs=[('TURNAT DIN GREȘEALĂ ÎN MOTORINĂ', 'bad', L(4) + 0.2), ('NU SE AMESTECĂ CU EA', 'water big', W(4, 'nu') - 0.15), ('E MAI GREU: COBOARĂ LA FUND', 'water big', T_4C + 0.1),
              ('EXACT DE UNDE TRAGE POMPA ELECTRICĂ', 'bad', T_4S)]),
]

# ------------------------------------------------------------------ contact pus: pompa electrica il trimite spre filtru si spre pompa de inalta presiune
SEND = [
 S.sysm(E, L(5), L(6), hl=[(['epump'], S.YEL_HL, W(5, 'pompa') - 0.2), (['filter'], S.WATER_HL, W(5, 'filtru') - 0.2), (['pump'], None, W(5, 'pompa', 2) - 0.2)],
        flows=[('tank', ADB2, 14, 150.0, 5.5, L(5) + 0.2), ('lp_f', ADB2, 9, 200.0, 6.0, W(5, 'trimite') - 0.3), ('lp_p', ADB2, 10, 200.0, 6.0, W(5, 'filtru'))],
        labs=[('CONTACT PUS', 'bad big', L(5) + 0.1), ('POMPA ELECTRICĂ ÎL TRIMITE SPRE FILTRU', 'bad', W(5, 'pompa') - 0.2), ('ȘI SPRE POMPA DE ÎNALTĂ PRESIUNE', 'bad', W(5, 'si') - 0.1),
              ('AICI AR TREBUI SĂ AJUNGĂ DOAR MOTORINĂ', 'grey', W(5, 'unde') - 0.1)]),
]

# ------------------------------------------------------------------ coroziv pentru otel si aluminiu; cand se usuca, lasa cristale albe; depunerile raman pe piese
T_6B = W(6, 'iar') - 0.12; T_6C = W(6, 'Depunerile') - 0.1
l_inj = E.lb('INJECTOARELE', 'bad')
def ov_dep(C):
    te = L(7) + 0.12; ti = W(6, 'injectoarele') - 0.25
    F.lens(C, 'ij', 'inj', 850, 560, 150, ti, te, kb=(0.9, 0, 396), ring=(255, 75, 75), pf=S.pf_cryst(n=40, seed=9, box=(430, 340, 650, 700), r=(7.0, 15.0)), tag='cry')
    F.spr(C, l_inj, 850, 726, ti + 0.15, te, anchor='tc')
CORR = [
 S.pump(E, 'pc', L(6), T_6B, st='fuel', seq=[('rust', L(6) + 0.2, L(6) + 4.4)], phase=False, pf=ADB_T, kb=[(L(6), 1.0, 0, 0), (T_6B, 1.06, 0, 0)], fx=[S.fx_fuel(col=S.ADBS, a=0.4)],
        labs=[('ADBLUE E COROZIV', 'bad big', L(6) + 0.15), ('PENTRU OȚEL ȘI ALUMINIU', 'bad big', W(6, 'pentru') - 0.1)]),
 Shot('fl', T_6B, T_6C, st='ffull', seq=[('fempty', T_6B + 0.15, T_6B + 1.2)], kb=[(T_6B,) + S.KB_FL, (T_6C, 0.94, 0, 62)], phase=False, tr=('xf', 0.3),
      pf=S.pfs(ADB_T, S.pf_paper(col=(0.4, 0.35, 0.3), t0=T_6B - 1.0, t1=T_6B, w=0.78), S.pf_cryst(n=170, seed=4, box=(300, 330, 800, 1330), r=(6.0, 16.0), t0=W(6, 'lasa') - 0.5, t1=W(6, 'sarea') + 0.2)),
      ov=S.ovs(S.tl(E, [('FILTRUL DE MOTORINĂ', 'grey', T_6B + 0.1)], T_6C),
               S.bl(E, [('CÂND SE USUCĂ', 'grey big', T_6B + 0.15), ('LASĂ CRISTALE ALBE, CA SAREA', 'bad big', W(6, 'lasa') - 0.1)], T_6C))),
 S.pump(E, 'pc', T_6C, L(7), st='dry', seq=[('rustd', T_6C - 4.0, T_6C + 10.0)], phase=False, kb=[(T_6C, 1.0, 0, 0), (L(7), 1.07, 0, 0)], fx=[],
        pf=S.pf_cryst(n=130, seed=5, box=(30, 560, 720, 1140), r=(6.0, 15.0), t0=T_6C - 0.6, t1=T_6C + 2.6), ov=ov_dep,
        labs=[('DEPUNERILE RĂMÂN PE PIESE', 'bad big', T_6C + 0.15), ('POMPA ȘI INJECTOARELE AU DE SUFERIT', 'bad', W(6, 'iar', 2) - 0.1)]),
]

# ------------------------------------------------------------------ daca motorul a mers: inlocuirea instalatiei, de la rezervor pana la injectoare
T_7R = W(7, 'de', 2) - 0.1
ALL = [
 S.sysm(E, L(7), L(8), hl=[(['tank', 'epump'], None, T_7R + 0.1), (['filter', 'lp'], None, T_7R + 0.4), (['pump', 'reg'], None, T_7R + 0.7), (['rail', 'hp'], None, T_7R + 1.0),
                           (['inj'], None, W(7, 'injectoare') - 0.2)],
        flows=[('lp', ADB2, 16, 200.0, 5.5, None), ('to_rail', ADB2, 12, 170.0, 5.0, L(7) + 0.2), ('rail_inj', ADB2, 16, 170.0, 5.0, L(7) + 0.8)],
        labs=[('DACĂ MOTORUL A MERS', 'bad big', L(7) + 0.1), ('PRODUCĂTORII CER DE OBICEI ÎNLOCUIREA', 'bad', W(7, 'producatorii') - 0.1), ('DE LA REZERVOR PÂNĂ LA INJECTOARE', 'bad big', T_7R)]),
]

# ------------------------------------------------------------------ cum eviti paguba
c_key = E.sym('key', 'NU PUNE CONTACTUL', 'Dacă ai greșit rezervorul'); c_tow = E.sym('tow', 'MAȘINA SE TRACTEAZĂ', cls='good'); c_drn = E.sym('drain', 'REZERVORUL SE GOLEȘTE', 'Și se curăță', cls='good')
def ov_avoid(C):
    te = L(9) + 0.1; tk = W(8, 'nu') - 0.1
    F.spr(C, c_key, 220, 850, tk, te); S.xmark(C, 290, 918, 46, F.pop(C.t, tk + 0.35, te), th=12)
    F.spr(C, c_tow, 220, 990, W(8, 'masina') - 0.1, te); F.spr(C, c_drn, 220, 1130, W(8, 'rezervorul', 2) - 0.1, te)
AVOID = S.avoid(E, 'tank', 'adb', L(8), L(9), [], head='CUM EVIȚI PAGUBA', kb=[(L(8), 0.74, 0, -290), (L(9), 0.76, 0, -294)], dim=0, ov=ov_avoid,
                wipe=('empty', W(8, 'goleste') - 0.3, W(8, 'goleste') + 1.0, 14, 'drop', (S.TANK_TOP, S.TANK_BOT), None))

# ------------------------------------------------------------------ ce facem noi
T_10U = W(10, 'ce', 3) - 0.12; T_10B = W(10, 'si', 2) - 0.1
RKB = (1.25, 250, 0)                                     # arborele, in lupa
tr_ok = E.add(P.tray('SE RECONDIȚIONEAZĂ')); tr_no = E.add(P.tray('SE ÎNLOCUIEȘTE', '#ff4b4b', bad=True))
def ov_mic(C):
    F.lens(C, 'pc', 'rustd', 770, 650, 200, W(9, 'microscop') - 0.4, L(10) + 0.12, kb=RKB, src=S.WM_OBJ, ring=(196, 96, 42),
           pf=S.pf_cryst(n=26, seed=7, box=(170, 800, 520, 1130), r=(7.0, 15.0)), tag='cry')
def ov_trays(C):
    te = T_10U + 0.12
    F.spr(C, tr_ok, 60, 520, W(10, 'reconditiona') - 0.35, te); F.spr(C, tr_no, 560, 520, W(10, 'inlocuit') - 0.35, te)
NOI = [
 S.wk(E, 'wm', L(9), L(10), [('DESFACEM POMPA ȘI INJECTOARELE', 'good', W(9, 'desfacem') - 0.2), ('LA MICROSCOP: CÂT A ÎNAINTAT COROZIUNEA', 'good', W(9, 'la', 2) - 0.15)], st='wkdam', ov=ov_mic),
 S.wk(E, 'wm', L(10), T_10U, [('ÎȚI SPUNEM CE SE MAI POATE RECONDIȚIONA', 'good', L(10) + 0.15), ('ȘI CE TREBUIE ÎNLOCUIT', 'good big', W(10, 'si') - 0.1),
                              ('HOTĂRÂREA O LUĂM ÎMPREUNĂ', 'good big', W(10, 'hotararea') - 0.15)], st='wkdam', ov=ov_trays),
 S.wk_usb(E, T_10U, T_10B, labs=[('CE SE SALVEAZĂ: CURĂȚAT CU ULTRASUNETE', 'good', T_10U + 0.15)], t_dip=W(10, 'ultrasunete') - 0.6),
 S.wk_bench(E, T_10B, L(E.OUT), labs=[('ȘI TESTAT PE BANC', 'good big', T_10B + 0.15)],
            rows=[('DEBIT', T_10B + 0.35), ('PRESIUNE', T_10B + 0.65), ('ETANȘEITATE', T_10B + 0.95)], t_sheet=T_10B + 0.1),
]

SHOTS = S.opening(E, HOOK) + [SIGNS] + WHAT + TANK + SEND + CORR + ALL + [AVOID] + NOI + [S.ending(E)]
SPR = E.SPR
