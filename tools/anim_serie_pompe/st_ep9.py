# Episodul 9: filtrul infundat si motorina inghetata
import math
import numpy as np
import pser as S, ifx as F, i2d as D, ikit as K, pdraw as P, fxlib as X
from icomp import Shot
from fxlib import seg, ease
E = S.Ep(9); W, L, LE = E.W, E.L, E.LE; TOTAL = E.TOTAL; GLOB = S.glob(E)

PF_DARK = S.pf_paper(col=(0.15, 0.115, 0.085), w=0.93)            # hartia filtrului, neagra de murdarie
def fx_clog(t_on=None, t_off=None, n_out=22, n_in=5, sp=1.0, a=0.55):
    """motorina la un filtru incarcat: se aduna in jurul hartiei, dar prin ea si prin tubul central trece putina"""
    def f(C):
        col = np.array([1.0, 0.86, 0.5])
        for i, (pn, v, m) in enumerate((('flt_outR', 13.0, n_out), ('flt_outL', 13.0, n_out), ('flt_inR', 4.0 * sp, n_in), ('flt_inL', 4.0 * sp, n_in), ('flt_core', 22.0 * sp, n_in), ('flt_coreL', 22.0 * sp, n_in))):
            F.flow(C, pn, m, v, col, 1.5, lat=0.9, seed=21 + i, t0=t_on, t1=t_off, mode='add', shape='g', shade=0, a=a)
    return f

# ------------------------------------------------------------------ carligul: paiul strans, apoi filtrul cu hartia neagra (coperta: filtrul, cu etichete)
T_H = 1.05
straw = E.add(P.straw(900)); l_much = E.lb('MOTORINĂ', 'lp'); l_none = E.lb('APROAPE NIMIC', 'bad')
def ov_straw(C):
    te = T_H + 0.12
    F.spr(C, straw, 90, 770, 0.0, te); F.spr(C, l_much, 250, 1100, 0.15, te, anchor='tc'); F.spr(C, l_none, 800, 1100, 0.45, te, anchor='tc')
l_black = E.lb('HÂRTIA ÎNFUNDATĂ', 'bad'); l_out = E.lb('SPRE POMPĂ: PREA PUȚIN', 'bad')
def ov_hookf(C):
    te = E.T_S + 0.1
    F.label(C, l_black, F.PLf(-30.0, 60.0), (30, 1030), T_H + 0.1, te)
    F.label(C, l_out, F.PR(5.5, 150.0), (1050, 760), T_H + 0.25, te, anchor='tr')
HOOK = [S.plain(E, 0.0, T_H, ov_straw, tr=None),
        Shot('fl', T_H, E.T_S, st='ffull', kb=[(T_H, 0.66, 0, 240), (E.T_S, 0.69, 0, 240)], pf=PF_DARK, fx=[fx_clog()], ov=ov_hookf, tr=('xf', 0.25), phase=False)]

SIGNS = S.symptoms(E, 2, [(E.sym('power', 'NU MAI TRAGE', 'La depășire sau în rampă'), 'trage'), (E.sym('warn', 'INTRĂ ÎN AVARIE'), 'avarie'), (E.sym('stall', 'SE OPREȘTE'), 'opreste'),
                          (E.sym('cold', 'IARNA, LA GER', 'Se oprește la scurt timp după pornire', cls='warn'), 'iarna')],
                   cam='fl', st='ffull', fx=[fx_clog()], y0=690, dy=140, pf=PF_DARK)

# ------------------------------------------------------------------ pompa comprima doar ce primeste, iar tot ce primeste trece prin filtru
T_3B = W(3, 'iar') - 0.1
FEED = [
 S.pump(E, 'pw', L(3), T_3B, labs=[('POMPA COMPRIMĂ DOAR CE PRIMEȘTE', 'hp big', L(3) + 0.25)]),
 S.sysm(E, T_3B, L(4), hl=[(['filter'], S.YEL_HL, T_3B + 0.2)], flows=[('lp', S.LP2, 16, 210.0, 5.0, None)],
        labs=[('TOT CE PRIMEȘTE TRECE PRIN FILTRU', 'lp big', T_3B + 0.15)]),
]

# ------------------------------------------------------------------ la ralanti trece destul; la accelerare debitul e strangulat si presiunea din rampa cade
T_4B = W(4, 'accelerare') - 0.36; T_4C = W(4, 'si') - 0.1
l_dem = E.lb('MOTORUL CERE', 'grey')
def ov_idle(C):
    t = C.t; te = T_4B + 0.12; a = F.pop(t, L(4) + 0.3, te)
    v = 0.16 + 0.03 * math.sin(t * 5.0) + 0.5 * float(ease(seg(t, T_4B - 0.45, T_4B + 0.2)))
    S.gauge(C, 868, 610, 112, v, a, red=None, green=(0.0, 0.3)); F.spr(C, l_dem, 868, 742, L(4) + 0.3, te, anchor='tc')
gp = E.panel('PRESIUNEA DIN RAMPĂ', 880, 600)
_u = np.linspace(0, 1, 60); _s = lambda a, b, x: np.clip((x - a) / (b - a), 0, 1) ** 2 * (3 - 2 * np.clip((x - a) / (b - a), 0, 1))
REQ = 0.22 + 0.62 * _s(0.28, 0.46, _u); REAL = 0.22 + 0.62 * _s(0.28, 0.46, _u) * (1.0 - 0.6 * _s(0.4, 0.78, _u))
CURVES = [(_u, REQ, (61, 220, 132), 6), (_u, REAL, (255, 75, 75), 6)]
def ov_graph(C):
    P.graph_panel(C, gp, 540, 470, 880, 600, CURVES, T_4C - 0.05, L(5) + 0.12, T_4C + 0.15, dur=1.2, xlab='TIMP', ylab='PRESIUNE',
                  tags=[('CERUTĂ', (61, 220, 132), 0.99, 0.87), ('REALĂ', (255, 120, 120), 0.99, 0.2), ('ACCELERARE', (182, 194, 207), 0.33, 0.03)])
STARVE = [
 Shot('fl', L(4), T_4B, st='ffull', kb=[(L(4), 0.86, -120, 66), (T_4B, 0.9, -120, 62)], pf=PF_DARK, phase=False, tr=('xf', 0.3), fx=[fx_clog(n_in=13, sp=1.5)],
      ov=S.ovs(ov_idle, S.bl(E, [('UN FILTRU ÎNCĂRCAT', 'bad', L(4) + 0.15), ('LA RALANTI TRECE DESTULĂ MOTORINĂ', 'good', W(4, 'lasa') - 0.1)], T_4B))),
 S.sysm(E, T_4B, T_4C, hl=[(['filter'], None, T_4B + 0.15), (['pump'], None, W(4, 'debitul') - 0.2)],
        flows=[('lp_f', S.LP2, 12, 210.0, 5.0, None), ('lp_p', S.RED2, 3, 70.0, 5.0, None)],
        labs=[('LA ACCELERARE, MOTORUL CERE MULT', 'lp', T_4B + 0.15), ('DEBITUL E STRANGULAT', 'bad big', W(4, 'debitul') - 0.15)]),
 S.plain(E, T_4C, L(5), S.ovs(ov_graph, S.bl(E, [('PRESIUNEA DIN RAMPĂ CADE', 'bad big', W(4, 'presiunea') - 0.1)], L(5)))),
]

# ------------------------------------------------------------------ iarna: de pe la -7 grade apar cristale de parafina, care la ger astupa filtrul
T_5M = W(5, 'minus') - 0.25; T_5K = W(5, 'cristale') - 0.5; T_5A = W(5, 'ele') - 0.4
WAX = (1.0, 0.98, 0.9); WAXE = (150, 126, 70); WAXP = (0.95, 0.86, 0.56)
l_m7 = E.lb('−7 °C', 'num water')
PF_WIN = S.pfs(S.pf_tint((0.9, 0.8, 0.46), t0=T_5K - 0.3, t1=T_5K + 2.2, w=0.55),                      # motorina se tulbura
               S.pf_cryst(n=210, seed=7, box=(110, 230, 970, 1720), r=(7.0, 14.0), col=WAX, t0=T_5K, t1=T_5K + 2.4, only_liq=True, edge=WAXE),
               S.pf_cryst(n=190, seed=9, box=(160, 380, 262, 1640), r=(8.0, 17.0), col=WAXP, t0=T_5A, t1=L(6) - 0.5, liq=True, edge=WAXE),
               S.pf_cryst(n=190, seed=11, box=(814, 380, 916, 1640), r=(8.0, 17.0), col=WAXP, t0=T_5A, t1=L(6) - 0.5, liq=True, edge=WAXE))
def ov_win(C):
    t = C.t; te = L(6) + 0.12; a = F.pop(t, L(5) + 0.25, te)
    v = 0.62 - 0.5 * float(ease(seg(t, L(5) + 0.4, T_5M + 0.5)))
    S.thermo(C, 944, 900, 330, v, a); F.spr(C, l_m7, 944, 480, T_5M + 0.2, te, anchor='tc')
def fx_win(C):
    k = 1.0 - 0.85 * float(seg(C.t, T_5A, L(6) - 0.6))
    fx_clog(n_out=16, n_in=max(1, int(round(12 * k))), sp=0.5 + k, a=0.5)(C)
WINTER = [
 Shot('flz', L(5), L(6), st='ffull', kb=[(L(5), 0.92, -40, 40), (L(6), 0.97, -40, 40)], phase=False, tr=('xf', 0.3), pf=PF_WIN, fx=[fx_win], ov=S.ovs(ov_win, S.bl(E, [
      ('IARNA, FRIGUL FACE ACELAȘI LUCRU', 'water', L(5) + 0.2), ('DE PE LA −7 °C: CRISTALE DE PARAFINĂ', 'water', T_5M + 0.1), ('LA GER PUTERNIC, ASTUPĂ FILTRUL', 'bad big', W(5, 'iar', 2) - 0.1)], L(6)))),
]

# ------------------------------------------------------------------ pompa infometata: motorina o unge si o raceste; la debit mic, piese mai calde si pelicula mai subtire
T_6B = W(6, 'motorina') - 0.1; T_6C = W(6, 'asa') - 0.1
l_flow = E.lb('DEBIT', 'lp'); l_temp = E.lb('TEMPERATURĂ', 'bad')
def ov_hot(C):
    t = C.t; te = L(7) + 0.12
    a = F.pop(t, L(6) + 0.3, te); v = 0.78 - 0.56 * float(ease(seg(t, L(6) + 0.5, L(6) + 2.2))) + 0.02 * math.sin(t * 6.0)
    S.gauge(C, 868, 560, 104, v, a, red=(0.0, 0.3)); F.spr(C, l_flow, 868, 684, L(6) + 0.3, te, anchor='tc')
    a2 = F.pop(t, T_6C - 0.1, te); h = 0.28 + 0.56 * float(ease(seg(t, T_6C, L(7) - 0.8)))
    S.thermo(C, 150, 980, 300, h, a2); F.spr(C, l_temp, 40, 1036, T_6C - 0.1, te)
HUNGRY = [
 S.pump(E, 'pc', L(6), L(7), fx=[S.fx_fuel(n=12, a=0.4, speed=9.0)], ov=ov_hot, kb=[(L(6), 1.0, 0, 0), (L(7), 1.08, 0, 0)],
        labs=[('POMPA ÎNFOMETATĂ PIERDE PRESIUNE', 'bad', L(6) + 0.15), ('MOTORINA O UNGE ȘI O RĂCEȘTE', 'lp big', T_6B), ('DEBIT MIC: PIESE MAI CALDE', 'bad big', T_6C + 0.1, 'Și o peliculă de motorină mai subțire')]),
]

# ------------------------------------------------------------------ cum eviti: filtru nou la interval, inainte de iarna; pe ger, motorina de iarna, fara benzina in ea
bk = E.add(P.book(290)); l_old = E.lb('VECHI', 'bad'); l_new = E.lb('NOU', 'good')
c1 = E.chk('SCHIMBĂ FILTRUL LA INTERVAL'); c2 = E.chk('DE PREFERAT ÎNAINTE DE IARNĂ'); c3 = E.chk('PE GER: MOTORINĂ DE IARNĂ'); c4 = E.stop('NU TURNA BENZINĂ ÎN EA')
CROP = (228, 186, 868, 1462)
def ov_avoid(C):
    t = C.t; te = L(8) + 0.1; tn = W(7, 'schimba') - 0.1
    S.plate_spr(C, 'fl', 'ffull', 196, 634, 0.31, F.pop(t, L(7) + 0.1, te), crop=CROP, pf=PF_DARK, tag='old9')
    S.plate_spr(C, 'fl', 'ffull', 470, 634, 0.31, F.pop(t, tn + 0.3, te), crop=CROP, tag='new')
    S.xmark(C, 196, 634, 66, F.pop(t, tn + 0.1, te), th=15)
    S.arrow2(C, (300, 634), (366, 634), (61, 220, 132), 10, F.pop(t, tn + 0.2, te), prog=float(seg(t, tn + 0.2, tn + 0.5)))
    F.spr(C, l_old, 196, 842, L(7) + 0.3, te, anchor='tc'); F.spr(C, l_new, 470, 842, tn + 0.4, te, anchor='tc')
    F.spr(C, bk, 676, 446, W(7, 'interval') - 0.5, te)
    F.spr(C, c1, 540, 926, tn, te, anchor='tc'); F.spr(C, c2, 540, 1010, W(7, 'preferat') - 0.25, te, anchor='tc')
    F.spr(C, c3, 540, 1094, W(7, 'alimenteaza') - 0.15, te, anchor='tc'); F.spr(C, c4, 540, 1178, W(7, 'nu') - 0.15, te, anchor='tc')
AVOID = S.plain(E, L(7), L(8), S.ovs(S.hd(E, 'CUM EVIȚI', L(7), L(8) + 0.1, 'good big'), ov_avoid))

# ------------------------------------------------------------------ ce facem noi: pompa acuzata pe nedrept se vede pe banc, cu alimentarea bancului
T_9B = W(9, 'daca', 2) - 0.12
v_ok = E.lb('POMPA E BUNĂ', 'good big', 'Problema e la filtru sau la alimentare'); v_no = E.lb('SE RECONDIȚIONEAZĂ', 'bad big', 'O desfacem și înlocuim piesele uzate')
def ov_ok(C): F.spr(C, v_ok, 540, 1150, W(9, 'pompa') - 0.15, T_9B + 0.12, anchor='tc')
pn = E.panel('FIȘA DE TEST', 440, 260); n1 = E.chk('DEBIT', False); n2 = E.chk('PRESIUNE', False)
def ov_no(C):
    te = L(E.OUT) + 0.12
    S.test_sheet(C, 800, 470, T_9B + 0.1, te, [(n1, W(9, 'nu') - 0.1), (n2, W(9, 'le') - 0.1)], title=pn)
    F.spr(C, v_no, 540, 1150, W(9, 'desfacem') - 0.25, te, anchor='tc')
NOI = [
 S.wk_bench(E, L(8), L(9), labs=[('POMPA SE VERIFICĂ PE BANC', 'good big', W(8, 'pompa') - 0.1), ('CU ALIMENTAREA BANCULUI, NU A MAȘINII', 'good', W(8, 'testam') - 0.15)],
            kb=[(L(8), 1.0, 0, 0), (L(9), 1.04, 0, 0)]),
 S.wk_bench(E, L(9), T_9B, rows=[('DEBIT', W(9, 'debitul') - 0.05), ('PRESIUNE', W(9, 'presiunea') - 0.05)], t_sheet=L(9) + 0.05, ov=ov_ok,
            kb=[(L(9), 1.04, 0, 0), (T_9B, 1.07, 0, 0)], tr=('xf', 0.2)),
 S.wk(E, 'wm', T_9B, L(E.OUT), [], st='wk', ov=ov_no),
]

SHOTS = S.opening(E, HOOK) + [SIGNS] + FEED + STARVE + WINTER + HUNGRY + [AVOID] + NOI + [S.ending(E)]
SPR = E.SPR
