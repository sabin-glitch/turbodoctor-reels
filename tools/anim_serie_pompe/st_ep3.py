# Episodul 3: benzina pusa din greseala
import math
import numpy as np
import pser as S, ifx as F, i2d as D
from icomp import Shot
from fxlib import seg, ease
E = S.Ep(3); W, L, LE = E.W, E.L, E.LE; TOTAL = E.TOTAL; GLOB = S.glob(E)
MIXT = S.pf_tint(S.MIX)                                  # amestecul verde-galbui, peste tot unde apare dupa alimentare
FILM_Y = S.pf_tint(S.LPY, which='hp')                    # pelicula marita, in galbenul motorinei din aceasta serie
bh = S.scr('pc', 'fuel', S.P_contact(S.H0), (1.05, 0, 0))

# ------------------------------------------------------------------ carligul: suvoiul verde intra in rezervor; in pompa, contactul incepe sa scanteieze
T_H = 2.2                       # coperta se ia la 1,85 s: rezervorul cu suvoiul verde
l_benz = E.lb('BENZINĂ', 'bad big')
def ov_hook(C):
    p = S.pk(C, [(232, 880)])[0]; F.spr(C, l_benz, p[0], p[1], 0.35, T_H + 0.1)
HOOK = [
 S.tank(E, 0.0, T_H, kb=[(0.0, 0.8, 170, 330), (T_H, 0.83, 164, 322)], tr=None, pf=S.pf_tint(S.MIX, 0.5, 1.6), ov=S.ovs(S.tank_in(0.1), S.tank_nozzle(E, -1.0, T_H + 0.1), ov_hook)),
 S.pump(E, 'pc', T_H, E.T_S, pf=MIXT, fx=[S.fx_fuel(col=S.MIXS, n=60, a=0.6), S.fx_dry(T_H + 0.2)], tr=('flash', 0.3), shake=S.shake_at(T_H + 0.2, 0.7, 3.0)),
]
SIGNS = S.symptoms(E, 2, [(E.sym('engine', 'SUNĂ ALTFEL', 'Imediat după alimentare'), 'suna'), (E.sym('idle', 'MERGE NEREGULAT'), 'merge'), (E.sym('power', 'PIERDE PUTERE'), 'pierde'),
                          (E.sym('stall', 'SE POATE OPRI'), 'poate')], cam='tank', st='dry', kb=(1.0, 0, -20), y0=690, dy=140, pf=MIXT)

# ------------------------------------------------------------------ pelicula de motorina; benzina o spala
T_3 = W(3, 'pompa') - 0.2; T_4F = W(4, 'motorina') - 0.15; T_4P = W(4, 'de') - 0.12; T_5M = W(5, 'din') - 0.12; T_5S = W(5, 'iar') - 0.15
l_cam = E.lb('CAMA', 'grey'); l_rol = E.lb('ROLA', 'grey'); l_pis = E.lb('PISTONUL', 'grey')
def ov_parts(C):
    S.lab_parts(C, [(l_cam, 'cam', (1040, 1050), W(4, 'cama') - 0.15, 'tr'), (l_rol, 'roller', (44, 690), W(4, 'rola') - 0.15),
                    (l_pis, np.array([0.0, -3.2, S.hC(C) + 26.0]), (1040, 404), W(4, 'pistoane') - 0.15, 'tr')], L(5) + 0.3)
EXPL = [
 S.film(E, L(3), T_3, pf=FILM_Y, flow=((255, 236, 150), None), sides=('METAL', 'METAL'), t_sides=W(3, 'piese') - 0.2,
        labs=[('MOTORINA E ULEIOASĂ', 'lp', L(3) + 0.25), ('PELICULA DE MOTORINĂ', 'lp big', W(3, 'pelicula') - 0.3), ('ȚINE PIESELE DESPĂRȚITE', 'good big', W(3, 'tine') - 0.15)]),
 S.pump(E, 'pw', T_3, L(4), labs=[('POMPA SE BAZEAZĂ PE PELICULĂ', 'lp big', T_3 + 0.25), ('NU ARE ALT LUBRIFIANT', 'bad big', W(3, 'nu') - 0.2)]),
 S.tank(E, L(4), T_4F, kb=[(L(4), 0.8, 170, 0), (T_4F, 0.83, 164, -6)], pf=S.pf_tint(S.MIX, L(4) + 0.5, W(4, 'cu') + 0.2),
        ov=S.ovs(S.tank_in(L(4) - 0.1, W(4, 'cu') + 0.3), S.tank_nozzle(E, L(4) - 0.5, T_4F + 0.2)),
        labs=[('BENZINA E UN SOLVENT', 'bad big', L(4) + 0.2), ('SE AMESTECĂ ÎN MOTORINĂ', 'bad', W(4, 'amestecata') - 0.1)]),
 S.film(E, T_4F, T_4P, seq=[('mdry', W(4, 'spala') - 0.1, W(4, 'pelicula') + 0.25)], pf=S.pfs(FILM_Y, S.pf_tint(S.MIX, T_4F - 0.3, T_4F + 0.5)),
        flow=(S.MIX2, None, W(4, 'spala') + 0.2), sides=('METAL', 'METAL'), t_sides=T_4F,
        labs=[('BENZINA SUBȚIAZĂ MOTORINA', 'bad', T_4F + 0.15), ('ȘI SPALĂ PELICULA', 'bad big', W(4, 'spala') - 0.15)]),
 S.pump(E, 'pc', T_4P, T_5M, pf=MIXT, ov=ov_parts, kb=[(T_4P, 1.0, 0, 0), (T_5M, 1.07, 0, 0)],
        labs=[('PIESELE RĂMÂN FĂRĂ PELICULĂ', 'bad big', T_4P + 0.2), ('METAL PE METAL', 'bad big', W(5, 'metal') - 0.25)],
        fx=[S.fx_fuel(col=S.MIXS, n=50, a=0.5), S.fx_dry(W(5, 'lucreze') - 0.2)], shake=S.shake_at(W(5, 'metal') - 0.2, 1.3, 2.5)),
 Shot('pm', T_5M, T_5S, st='fuel', seq=[('damf', T_5M + 0.3, T_5M + 1.3)], pf=S.pf_tint(S.MIX, rmin=0.62), tr=('dive', 0.6, bh, 2.4, 'full'), kb=[(T_5M, 1.0, 0, 0), (T_5S, 1.06, 0, 0)],
      fx=[S.fx_dry(T_5M - 0.2, rate=9.0, amp=0.75, size=0.2, speed=30.0), S.fx_flakes(W(5, 'pilitura') - 0.45)], phase=False,
      ov=S.bl(E, [('SUPRAFEȚELE SE ZGÂRIE', 'bad big', T_5M + 0.1), ('PILITURĂ', 'bad big', W(5, 'pilitura') - 0.15)], T_5S), shake=S.shake_at(T_5M, T_5S - T_5M + 0.4, 2.0)),
 S.sysm(E, T_5S, L(6), hl=[(['pump'], None, T_5S), (['rail'], None, W(5, 'toata') - 0.1), (['inj'], None, W(5, 'instalatia') - 0.1)],
        flows=[('to_rail', S.METAL2, 12, 170.0, 4.5, T_5S + 0.2), ('rail_inj', S.METAL2, 16, 170.0, 4.5, T_5S + 0.9), ('ret', S.METAL2, 12, 150.0, 4.0, T_5S + 1.5)],
        labs=[('PILITURĂ ÎN TOATĂ INSTALAȚIA', 'bad big', T_5S + 0.15)]),
]

# ------------------------------------------------------------------ intrebarea care hotaraste paguba: a fost pornit motorul?
T_6 = W(6, 'la') - 0.15; T_7 = W(7, 'daca', 2) - 0.15
l_one = E.lb('UN SINGUR LUCRU CONTEAZĂ', 'grey big')
q_key = E.add('<div class="stat y" style="padding:20px 46px 28px"><div style="zoom:2.1;height:62px;margin-top:-8px">%s</div>'
              '<span style="font-size:54px;line-height:1.12;margin-top:0">A FOST PORNIT<br>MOTORUL?</span></div>' % D.ICON2['key'])
def ov_q(C):
    F.spr(C, l_one, 540, 470, W(6, 'conteaza') - 0.2, T_6 + 0.1, anchor='tc')
    F.spr(C, q_key, 540, 590, W(6, 'daca') - 0.15, T_6 + 0.1, anchor='tc')
STARTED = [
 S.tank(E, L(6), T_6, pf=MIXT, ov=ov_q, kb=[(L(6), 1.0, 0, 70), (T_6, 1.05, 0, 80)], dim=lambda t: 0.3 * F.pop(t, L(6) + 0.2, T_6 + 0.2)),
 S.sysm(E, T_6, L(7), hl=[(['tank'], S.WHITE_HL, T_6), (['epump'], S.YEL_HL, W(6, 'pompa') - 0.2), (['pump'], None, W(6, 'uneori') - 0.2)],
        flows=[('tank', S.MIX2, 14, 150.0, 5.5, T_6), ('lp', S.MIX2, 24, 210.0, 6.5, W(6, 'porneste') - 0.2)],
        labs=[('POMPA ELECTRICĂ PORNEȘTE DE LA CONTACT', 'bad', W(6, 'pompa') - 0.25), ('UNEORI, DE LA DESCHIDEREA PORTIEREI', 'bad', W(6, 'uneori') - 0.1)]),
 S.tank(E, L(7), T_7, pf=MIXT, wipe=('empty', W(7, 'golirea') - 0.3, W(7, 'rezervorului') + 0.7, 14, 'drop', (S.TANK_TOP, S.TANK_BOT), None),
        ov=S.hd(E, 'DACĂ NU AI PORNIT MOTORUL', L(7) + 0.05, T_7 + 0.1, 'good big'), labs=[('DE OBICEI AJUNGE GOLIREA REZERVORULUI', 'good', W(7, 'de') - 0.1)]),
 S.sysm(E, T_7, L(8), hl=[(['pump'], None, W(7, 'pompa') - 0.15), (['inj'], None, W(7, 'injectoarele') - 0.15), (['rail'], None, W(7, 'rampa') - 0.15), (['hp'], None, W(7, 'conductele') - 0.15)],
        flows=[('lp', S.MIX2, 20, 210.0, 6.0, None), ('to_rail', S.METAL2, 10, 170.0, 4.5, W(7, 'pompa') - 0.1), ('rail_inj', S.METAL2, 14, 170.0, 4.5, W(7, 'injectoarele') - 0.2)],
        labs=[('DACĂ MOTORUL A MERS', 'bad big', T_7 + 0.1)]),
]

# ------------------------------------------------------------------ cum eviti paguba
c_key = E.sym('key', 'NU PUNE CONTACTUL', 'Și nu porni motorul'); c_tow = E.sym('tow', 'MAȘINA SE TRACTEAZĂ', cls='good'); c_drn = E.sym('drain', 'REZERVORUL SE GOLEȘTE', cls='good')
def ov_avoid(C):
    te = L(9) + 0.1; tk = W(8, 'nu') - 0.1
    F.spr(C, c_key, 220, 850, tk, te); S.xmark(C, 290, 918, 46, F.pop(C.t, tk + 0.35, te), th=12)
    F.spr(C, c_tow, 220, 990, W(8, 'masina') - 0.1, te); F.spr(C, c_drn, 220, 1130, W(8, 'rezervorul') - 0.1, te)
AVOID = S.avoid(E, 'tank', 'dry', L(8), L(9), [], head='CUM EVIȚI PAGUBA', kb=[(L(8), 0.74, 0, -290), (L(9), 0.76, 0, -294)], pf=MIXT, dim=0, ov=ov_avoid,
                wipe=('empty', W(8, 'rezervorul') - 0.1, W(8, 'goleste') + 0.9, 14, 'drop', (S.TANK_TOP, S.TANK_BOT), None))

# ------------------------------------------------------------------ ce facem noi
T_9 = W(9, 'o') - 0.15; T_10 = L(10) - 0.1; T_10I = W(10, 'iar') - 0.1
bar = E.add('<div class="stat y" style="padding:12px 34px 16px"><span style="font-size:30px;margin-top:0;color:#b6c2cf">PÂNĂ LA</span><b style="font-size:118px">2.400</b><span style="font-size:36px">BAR</span></div>')
def ov_bar(C): F.spr(C, bar, 850, 470, W(10, 'pana') - 0.25, L(E.OUT) + 0.2, anchor='tc')
NOI = [
 S.wk_mic(E, L(9), T_9, labs=[('DACĂ MOTORUL A MERS CU BENZINĂ', 'grey', W(9, 'daca') - 0.1), ('DESFACEM POMPA', 'grey', W(9, 'desfacem') - 0.1), ('CĂUTĂM PILITURA LA MICROSCOP', 'good big', W(9, 'cautam') - 0.1)],
          lens=(W(9, 'pilitura') - 0.2, T_9)),
 S.wk_bench(E, T_9, T_10, labs=[('O POMPĂ CURATĂ: DOAR TESTUL PE BANC', 'good', W(9, 'curata') - 0.3)],
            rows=[('DEBIT', W(9, 'trece')), ('PRESIUNE', W(9, 'prin')), ('ETANȘEITATE', W(9, 'banc') - 0.1)]),
 S.wk_mic(E, T_10, T_10I, labs=[('POMPA ZGÂRIATĂ', 'bad', W(10, 'zgariata') - 0.2), ('RECONDIȚIONATĂ CU PIESE NOI', 'good big', W(10, 'reconditionam') - 0.1)],
          lens=(T_10 + 0.2, W(10, 'cu') - 0.2), t_new=W(10, 'cu') - 0.15),
 S.wk_inj(E, T_10I, L(E.OUT), labs=[('INJECTOARELE, VERIFICATE PE STAND', 'good big', W(10, 'injectoarele') - 0.1)], ov=ov_bar),
]

SHOTS = S.opening(E, HOOK) + [SIGNS] + EXPL + STARTED + [AVOID] + NOI + [S.ending(E)]
SPR = E.SPR
