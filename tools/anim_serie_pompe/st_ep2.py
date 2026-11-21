# Episodul 2: rezervorul golit si mersul pe ultimii litri
import math
import numpy as np
import pser as S, ifx as F, i2d as D
from icomp import Shot
from fxlib import seg, ease
E = S.Ep(2); W, L, LE = E.W, E.L, E.LE; TOTAL = E.TOTAL; GLOB = S.glob(E)

# ------------------------------------------------------------------ carligul: acul pe rosu, apoi rezervorul in care motorina fuge intr-o parte
T_H = 1.35
fuel_ic = E.sym('fuel', 'REZERVĂ', cls='warn')
def ov_gauge(C):
    t = C.t; v = 0.3 - 0.29 * float(ease(seg(t, 0.1, 0.9))) + 0.012 * math.sin(t * 23) * float(seg(t, 0.9, 1.1))
    S.gauge(C, 540, 1050, 275, v, 1.0, red=(0.0, 0.14), th=14)
    D.text(C, '0', 296, 1200, 60, a=1.0, font='mont'); D.text(C, '1/2', 540, 845, 48, a=0.9, font='mont'); D.text(C, '1', 786, 1200, 60, a=1.0, font='mont')
    F.spr(C, fuel_ic, 540, 1150, 0.55, T_H + 0.2, anchor='tc', scale=0.62)
def air_tank(t_on, t_off=None, n=16):
    def ov(C): S.flowp(C, S.TANK_OUT, n, 150.0, S.AIR2, 9.0, t0=t_on, t1=t_off, ring=True, lat=5.0, seed=4, dark=0.6)
    return ov
HOOK = [
 S.plain(E, 0.0, T_H, ov_gauge, tr=None),
 Shot('tank', T_H, E.T_S, st='dry', wipe=('empty', T_H - 0.6, T_H + 1.0, 14, 'drop', (S.TANK_TOP, 1128), S.slosh(T_H - 0.3, 0.1, 1.3)), tr=('flash', 0.3),
      kb=[(T_H, 1.12, 0, -30), (E.T_S, 1.2, -40, -60)], ov=air_tank(T_H + 0.1), phase=False),
]
SIGNS = S.symptoms(E, 2, [(E.sym('idle', 'SE ÎNEACĂ ÎN VIRAJE', 'Sau în rampă'), 'ineaca'), (E.sym('stall', 'SE OPREȘTE'), 'opreste'), (E.sym('start', 'PORNEȘTE GREU', 'După alimentare'), 'porneste')],
                   cam='tank', st='empty', kb=(1.0, 0, -20))

# ------------------------------------------------------------------ pompa e unsa de motorina; rezervorul se goleste si intra aer
T_3 = W(3, 'cat') - 0.2; T_4S = W(4, 'aerul') - 0.25; T_4P = W(4, 'iar') - 0.2; T_D0 = W(4, 'pelicula'); T_D1 = T_D0 + 0.9
l_film = E.lb('PELICULA DE MOTORINĂ', 'lp')
def ov_film(C):
    S.lab_parts(C, [(l_film, 'contact', (44, 640), W(3, 'piesele') - 0.3)], L(4) + 0.1)
bh = S.scr('pw', 'fuel', S.P_contact(S.H0), (1.04, 0, 40))
EXPL = [
 S.pump(E, 'pw', L(3), T_3, labs=[('UNSĂ ȘI RĂCITĂ DE MOTORINĂ', 'lp big', W(3, 'unsa'))]),
 S.pump(E, 'pc', T_3, L(4), labs=[('PIESELE EI NU SE ATING', 'good big', W(3, 'nu'))], fx=[S.fx_fuel(n=60, a=0.6)], ov=ov_film, tr=('dive', 0.7, bh, 2.6, 'full')),
 Shot('tank', L(4), T_4S, st='dry', wipe=('empty', W(4, 'goleste') - 0.5, W(4, 'in') + 0.5, 14, 'drop', (S.TANK_TOP, 1128), S.slosh(L(4), 0.05, 1.9)),
      kb=[(L(4), 1.0, 0, -20), (T_4S, 1.1, -30, -40)], phase=False,
      ov=S.ovs(air_tank(W(4, 'intra') - 0.2), S.bl(E, [('REZERVORUL SE GOLEȘTE', 'grey', L(4) + 0.3), ('ÎN CONDUCTĂ INTRĂ AER', 'bad big', W(4, 'intra') - 0.2)], T_4S, y=1200))),
 S.sysm(E, T_4S, T_4P, hl=[(['tank', 'epump'], S.WHITE_HL, T_4S), (['filter'], S.WHITE_HL, T_4S + 0.5), (['pump'], None, W(4, 'pompa') - 0.2)],
        flows=[('lp', S.AIR2, 26, 240.0, 7.5, T_4S, None, True)], labs=[('AERUL AJUNGE ÎN POMPĂ', 'bad big', T_4S + 0.1)]),
 S.pump(E, 'pc', T_4P, L(5), seq=[('dry', T_D0, T_D1)], labs=[('PELICULA DINTRE PIESE DISPARE', 'bad big', T_D0 - 0.2)],
        fx=[S.fx_fuel(t_off=T_D0, n=60, a=0.6), S.fx_bubbles(T_4P - 1.0, T_D0 + 0.4), S.fx_dry(T_D1 - 0.2)], shake=S.shake_at(T_D1, 0.9, 3.0)),
]

# ------------------------------------------------------------------ ultimii litri: motorina putina se incalzeste; apa si murdaria de pe fund
T_5P = W(5, 'iar') - 0.2; T_6S = W(6, 'ele') - 0.2
def ov_warm(C):
    a = F.pop(C.t, W(5, 'putina') - 0.3, T_5P + 0.1)
    v = 0.25 + 0.6 * float(ease(seg(C.t, W(5, 'incalzeste') - 0.3, W(5, 'repede') + 0.6)))
    S.thermo(C, 930, 1120, 330, v, a)
LOW = ('empty', 0.0, 0.1, 14, 'drop', (S.TANK_TOP, 1108), S.slosh(L(5), 0.02, 2.3))
def dirt(t_on, t_go=None):
    def ov(C):
        e = F.pop(C.t, t_on, None)
        r = np.random.RandomState(8).rand(46, 3); x = 130 + 830 * r[:, 0]; y = 1166 + 10 * r[:, 1]
        if t_go is not None:
            u = np.clip((C.t - t_go) / 1.6 - 0.5 * r[:, 2], 0, 1); x = x + (S.TANK_SORB[0] - x) * u * u; y = y + (S.TANK_SORB[1] + 6 - y) * u
        D.dots2(C, np.array(S.pk(C, list(zip(x, y)))), 3.2 * C.shot.kbat(C.t)[0], (58, 44, 30), e)
        if t_go is not None: S.flowp(C, S.TANK_OUT[1:], 12, 170.0, (70, 54, 36), 4.5, t0=t_go + 1.0, lat=4.0, seed=9)
    return ov
LITRES = [
 Shot('tank', L(5), T_5P, st='dry', wipe=LOW, kb=[(L(5), 1.0, 0, -20), (T_5P, 1.06, 0, -30)], phase=False,
      pf=S.pf_tint((0.95, 0.52, 0.18), W(5, 'incalzeste') - 0.3, W(5, 'repede') + 0.8, w=0.55),
      ov=S.ovs(ov_warm, S.bl(E, [('MERSUL PE ULTIMII LITRI', 'grey', L(5) + 0.3), ('PUȚINA MOTORINĂ SE ÎNCĂLZEȘTE REPEDE', 'bad', W(5, 'putina') - 0.2)], T_5P, y=1200))),
 S.pump(E, 'pc', T_5P, L(6), labs=[('MOTORINA CALDĂ E MAI SUBȚIRE', 'bad big', T_5P + 0.2, 'Unge mai slab')], fx=[S.fx_fuel(n=30, a=0.3)], pf=S.pf_tint((0.99, 0.84, 0.46), w=0.8)),
 Shot('tank', L(6), T_6S, st='cond', wipe=('empty', W(6, 'cu') - 0.4, W(6, 'jos') + 0.3, 14, 'drop', (S.TANK_TOP, 1118), None),
      kb=[(L(6), 1.5, -200, -250), (W(6, 'cu') - 0.3, 1.5, -200, -250), (T_6S, 1.25, -90, -130)], phase=False,
      ov=S.ovs(dirt(L(6) + 0.2, W(6, 'ele') - 0.6), S.bl(E, [('APĂ ȘI IMPURITĂȚI PE FUND', 'water big', W(6, 'apa') - 0.4), ('CU NIVELUL JOS, AJUNG LA SORB', 'bad', W(6, 'cu') - 0.1)], T_6S, y=1200))),
 S.sysm(E, T_6S, L(7), hl=[(['tank', 'epump'], S.WHITE_HL, T_6S), (['filter'], None, W(6, 'filtru') - 0.2), (['pump'], None, W(6, 'pompa') - 0.2)],
        flows=[('tank', (120, 96, 66), 14, 150.0, 5.5, T_6S), ('lp', (120, 96, 66), 16, 150.0, 5.5, T_6S + 0.3), ('lp', S.WATER2, 8, 150.0, 6.0, T_6S + 0.4)],
        labs=[('SPRE FILTRU ȘI SPRE POMPĂ', 'bad big', T_6S + 0.2)]),
]

# ------------------------------------------------------------------ urmarea
T_7A = W(7, 'suprafete') - 0.3; T_7B = W(7, 'presiune') - 0.3
def ov_rail(C):
    a = F.pop(C.t, T_7B + 0.2, L(8) + 0.1); v = 0.78 - 0.5 * float(ease(seg(C.t, T_7B + 0.3, L(8) - 0.3)))
    S.gauge(C, 800, 1050, 86, v, a, red=(0.0, 0.3), th=8, nt=7)
AFTER = [
 S.pump(E, 'pc', L(7), T_7A, st='dry', labs=[('POMPA RĂMASĂ FĂRĂ UNGERE', 'bad big', L(7) + 0.3)], fx=[S.fx_dry(L(7) - 0.2)], shake=S.shake_at(L(7), T_7A - L(7), 2.0)),
 Shot('pm', T_7A, T_7B, st='dry', seq=[('dam', T_7A + 0.3, T_7A + 1.3)], tr=('dive', 0.6, S.scr('pc', 'dry', S.P_contact(S.H0), (1.05, 0, 0)), 2.4, 'full'),
      kb=[(T_7A, 1.0, 0, 0), (T_7B, 1.06, 0, 0)], fx=[S.fx_dry(T_7A - 0.2, rate=9.0, amp=0.75, size=0.2, speed=30.0), S.fx_flakes(W(7, 'pilitura') - 0.3)], phase=False,
      ov=S.bl(E, [('SUPRAFEȚE ZGÂRIATE', 'bad big', T_7A + 0.1), ('PILITURĂ', 'bad big', W(7, 'pilitura') - 0.1)], T_7B), shake=S.shake_at(T_7A, T_7B - T_7A + 0.4, 2.0)),
 S.sysm(E, T_7B, L(8), hl=[(['pump'], None, T_7B), (['rail'], None, T_7B + 0.3)], flows=[('to_rail', S.HP2, 10, 120.0, 5.0, None)],
        labs=[('PRESIUNE TOT MAI MICĂ ÎN RAMPĂ', 'bad big', T_7B + 0.1)], ov=ov_rail),
]

# ------------------------------------------------------------------ cum eviti: un sfert de rezervor
YQ = 1084
l_q = E.lb('MINIM UN SFERT', 'good big')
def ov_quarter(C):
    a = F.pop(C.t, W(8, 'rezervorul') - 0.2, L(9) + 0.1)
    p = S.pk(C, [(112, YQ), (978, YQ)]); S.dash2(C, p[0], p[1], S.GREEN2, 6, a, n=16)
    F.spr(C, l_q, 540, S.pk(C, [(540, YQ - 150)])[0][1], W(8, 'sub') - 0.2, W(8, 'iar') + 0.2, anchor='tc')
AVOID = S.avoid(E, 'tank', 'dry', L(8), L(9), [('REZERVORUL, MINIM UN SFERT', W(8, 'iar') + 0.2), ('AERISIRE ÎNAINTE DE PORNIRE', W(8, 'instalatia')), ('NU SE INSISTĂ LA DEMAROR', W(8, 'nu', 2), False)],
                kb=[(L(8), 1.0, 0, -150), (L(9), 1.04, 0, -160)], wipe=('empty', 0.0, 0.1, 14, 'drop', (S.TANK_TOP, YQ), None), ov=ov_quarter, dim=0)

# ------------------------------------------------------------------ ce facem noi
T_10 = L(10) - 0.1; T_G = W(10, 'cu', 2) - 0.25
gar = S.seal(E, '12', 'LUNI GARANȚIE')
def ov_gar(C): F.spr(C, gar, 850, 470, T_G + 0.25, L(E.OUT) + 0.2, anchor='tc')
NOI = [
 S.wk_bench(E, L(9), T_10, labs=[('POMPA, TESTATĂ PE BANC', 'good big', W(9, 'testam'))], rows=[('DEBIT', W(9, 'debitul')), ('PRESIUNE', W(9, 'presiunea'))]),
 S.wk_mic(E, T_10, T_G, labs=[('POMPA DESFĂCUTĂ', 'grey', W(10, 'desfacem')), ('VERIFICATĂ LA MICROSCOP', 'grey', W(10, 'verificam')), ('RECONDIȚIONATĂ CU PIESE NOI', 'good big', W(10, 'reconditionam'))],
          lens=(W(10, 'microscop') - 0.3, W(10, 'reconditionam')), t_new=W(10, 'reconditionam') - 0.1),
 S.wk(E, 'px', T_G, L(E.OUT), st='full', labs=[('POMPA PLEACĂ TESTATĂ', 'good big', T_G + 0.2)], kb=[(T_G, 0.68, -150, 20), (L(E.OUT), 0.72, -150, 14)], ov=ov_gar),
]

SHOTS = S.opening(E, HOOK) + [SIGNS] + EXPL + LITRES + AFTER + [AVOID] + NOI + [S.ending(E)]
SPR = E.SPR
