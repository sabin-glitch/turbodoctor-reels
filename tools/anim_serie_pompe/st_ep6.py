# Episodul 6: apa din motorina
import math
import numpy as np
import pser as S, ifx as F, i2d as D, ikit as K, pdraw as P, fxlib as X
from icomp import Shot
from fxlib import seg, ease
E = S.Ep(6); W, L, LE = E.W, E.L, E.LE; TOTAL = E.TOTAL; GLOB = S.glob(E)
BLUE = (70, 160, 245); FILM_Y = S.pf_tint(S.LPY, which='hp')

# ------------------------------------------------------------------ carligul: paharul separatorului, cu apa albastra la fund; apoi pompa, cu rugina pe arbore, pe rola si pe piston
# (coperta, la 2,25 s: pompa ruginita, cu paharul cu apa intr-o lupa)
T_H = 1.3
l_apa = E.lb('APĂ', 'water big'); l_rug = E.lb('RUGINĂ', 'bad big')
def ov_h1(C):
    x, y = S.pk(C, [(650, 1660)])[0]
    F.label(C, l_apa, ('px', x, y), (760, 1040), 0.3, T_H + 0.1)
def ov_h2(C):
    te = E.T_S + 0.1
    F.lens(C, 'filter', 'fwlo', 848, 1030, 150, T_H + 0.1, te, kb=(0.7, 0, -476), ring=BLUE)
    F.spr(C, l_apa, 848, 1194, T_H + 0.25, te, anchor='tc')
    x, y = S.pk(C, [(330, 960)])[0]
    F.label(C, l_rug, ('px', x, y), (48, 1150), T_H + 0.5, te)
HOOK = [
 Shot('filter', 0.0, T_H, st='fwlo', kb=[(0.0, 0.8, 0, -640), (T_H, 0.84, 0, -664)], tr=None, phase=False, fx=[S.fx_sep(-3.0)], ov=ov_h1),
 S.pump(E, 'pc', T_H, E.T_S, st='fuel', seq=[('rust', T_H + 0.05, T_H + 0.65)], phase=False, tr=('xf', 0.25), kb=[(T_H, 1.0, 0, 30), (E.T_S, 1.05, 0, 30)],
        fx=[S.fx_drops(('bath_R', 'cam_Ldn'), n=10, speed=10.0)], ov=ov_h2),
]

SIGNS = S.symptoms(E, 2, [(E.sym('water', 'MARTOR DE APĂ', 'Acolo unde există', cls='warn'), 'martorul'), (E.sym('start', 'PORNIRE GREA'), 'pornire'),
                          (E.sym('idle', 'MERS NEREGULAT'), 'mers'), (E.sym('fuel', 'DUPĂ ALIMENTARE', 'Sau după ce a stat mult', cls='warn'), 'mai')],
                   cam='filter', st='fwlo', kb=(0.6, 0, -60), fx=[S.fx_sep(L(2) - 3.0)], y0=690, dy=140)

# ------------------------------------------------------------------ apa vine odata cu motorina sau se aduna din condens; e mai grea si se asaza la fund
T_3C = W(3, 'sau') - 0.15; T_3W = W(3, 'condens') + 0.3
SINK = [(182, 1000), (192, 1070), (222, 1136), (300, 1160), (520, 1163), (860, 1163)]
l_wat = E.lb('APĂ', 'water'); l_mot = E.lb('MOTORINĂ', 'lp'); l_cond = E.lb('CONDENS', 'water')
def ov_tank(C):
    S.flowp(C, SINK, 12, 110.0, BLUE, 8.0, t0=L(3) + 0.9, t1=T_3C + 0.6, seed=4, lat=3.0, glow=0.2, dark=0.5)
    te = L(4) + 0.12
    x, y = S.pk(C, [(338, 806)])[0]; F.label(C, l_cond, ('px', x, y), (120, 520), W(3, 'condens') - 0.1, te)
    x, y = S.pk(C, [(300, 1066)])[0]; F.spr(C, l_mot, x, y, W(3, 'decat') - 0.1, te, anchor='cc')
    x, y = S.pk(C, [(250, 1163)])[0]; F.label(C, l_wat, ('px', x, y), (96, 1112), W(3, 'E') - 0.05, te, side='r')
TANK = [
 S.tank(E, L(3), L(4), st='dry', seq=[('cond', T_3C, T_3W + 0.3)], wipe=('cond', W(3, 'odata') + 0.4, T_3C - 0.1, 8, 'up', (1206, 1146), None),
        kb=[(L(3), 0.8, 170, 0), (T_3C - 0.25, 0.83, 164, -6), (T_3W, 1.0, 0, -110), (L(4), 1.05, 0, -120)],
        fx=[S.fx_tank_cond(T_3C + 0.2, W(3, 'condens') - 0.3)],
        ov=S.ovs(S.tank_in(L(3) - 0.1, T_3C - 0.2, col=S.LP2, n=44), S.tank_in(L(3) + 0.5, T_3C - 0.4, col=BLUE, n=6, r=9.0, speed=300.0),
                 S.tank_nozzle(E, L(3) - 0.5, T_3C + 0.05, col='#3b4652', dark='#1a2129'), ov_tank),
        labs=[('APA VINE ODATĂ CU MOTORINA', 'water', L(3) + 0.2), ('SAU SE ADUNĂ DIN CONDENS', 'water', T_3C + 0.1), ('E MAI GREA: SE AȘAZĂ LA FUND', 'water big', W(3, 'E') - 0.1)]),
]

# ------------------------------------------------------------------ separatorul din filtru opreste apa; plin sau cu filtrul depasit, apa trece spre pompa
T_4S = W(4, 'apa') - 0.15
l_bowl = E.lb('SEPARATORUL', 'water', 'Aici se adună apa')
def ov_filt(C):
    x, y = S.pk(C, [(690, 1650)])[0]
    F.label(C, l_bowl, ('px', x, y), (752, 930), W(4, 'separator') - 0.1, W(4, 'daca') + 0.1)
FILT = [
 Shot('filter', L(4), T_4S, st='fwlo', seq=[('fwhi', W(4, 'daca') - 0.1, W(4, 'depasit') + 0.4)], kb=[(L(4), 0.66, 0, -400), (T_4S, 0.69, 0, -418)], phase=False, tr=('xf', 0.3),
      fx=[S.fx_sep(L(4) - 2.0, W(4, 'depasit') - 0.2)],
      ov=S.ovs(ov_filt, S.bl(E, [('FILTRUL ARE UN SEPARATOR DE APĂ', 'good', L(4) + 0.25), ('SEPARATOR PLIN SAU FILTRU DEPĂȘIT', 'bad', W(4, 'daca') - 0.1)], T_4S))),
 S.sysm(E, T_4S, L(5), hl=[(['filter'], S.WATER_HL, T_4S), (['pump'], S.WATER_HL, W(4, 'spre') - 0.15)],
        flows=[('lp_f', S.LP2, 10, 200.0, 5.0, None), ('lp_p', BLUE, 9, 190.0, 6.0, T_4S + 0.1), (['lp_p'], S.LP2, 6, 190.0, 5.0, None)],
        labs=[('APA TRECE MAI DEPARTE', 'bad big', T_4S + 0.1), ('SPRE POMPĂ', 'bad big', W(4, 'spre') - 0.15)]),
]

# ------------------------------------------------------------------ apa nu unge: unde ia locul motorinei, pelicula se rupe
T_5F = W(5, 'ajunge') - 0.05; T_5B = W(5, 'rupe') - 0.3
bh = S.scr('pc', 'fuel', S.P_contact(S.H0), (1.06, 0, 0))
l_wf = E.lb('APĂ', 'water big'); l_mf = E.lb('MOTORINĂ', 'lp')
def ov_film(C):
    t = C.t
    u = float(seg(t, T_5F + 0.45, W(5, 'pelicula') - 0.1)); yf = -120 + 2160 * u
    if t < T_5B + 0.2:
        F.label(C, l_wf, ('px', 560, min(max(yf - 260, 470), 780)), (700, 520), T_5F + 0.9, T_5B + 0.2)
        F.label(C, l_mf, ('px', 520, 1090), (120, 1040), T_5F + 0.3, W(5, 'motorinei') + 0.3, anchor='tl')
    S.sparks2(C, 540, 800, t, T_5B + 0.35, n=18, L=44.0, R=360.0)
WET = [
 S.pump(E, 'pc', L(5), T_5F, kb=[(L(5), 1.0, 0, 0), (T_5F, 1.06, 0, 0)], fx=[S.fx_fuel(a=0.4), S.fx_drops(('bath_R', 'cam_Ldn', 'cam_Lup'), L(5) - 2.0, n=12, speed=16.0, size=1.0)],
        labs=[('APA NU UNGE', 'bad big', L(5) + 0.1)]),
 S.film(E, T_5F, L(6), seq=[('mdry', T_5B, T_5B + 0.5)], pf=S.pfs(FILM_Y, S.pf_front(S.WATER, T_5F + 0.45, W(5, 'pelicula') - 0.1)),
        flow=((255, 236, 150), None, W(5, 'motorinei')), sides=('CAMA', 'ROLA'), t_sides=T_5F + 0.3, tr=('dive', 0.6, bh, 2.6, 'full'), ov=ov_film,
        shake=S.shake_at(T_5B + 0.3, 1.6, 2.5),
        labs=[('APA IA LOCUL MOTORINEI', 'water', T_5F + 0.5), ('PELICULA DINTRE PIESE SE RUPE', 'bad big', W(5, 'pelicula') - 0.15), ('UZURA SE ACCELEREAZĂ', 'bad big', W(5, 'iar') - 0.1)]),
]

# ------------------------------------------------------------------ apoi vine rugina: apa si acizii din motorina ataca metalul (carcasa, arborele, supapele)
HSG = [F.PR(27.2 * math.cos(math.radians(a)), 27.2 * math.sin(math.radians(a))) for a in (-62, -38, -14, 10, 34)] + [F.PLf(-27.2 * math.cos(math.radians(a)), 27.2 * math.sin(math.radians(a))) for a in (-55, -25, 5)]
VLV = [S.P_INVALVE, S.P_BALL, F.PR(8.0, 86.5)]
l_hsg = E.lb('CARCASA', 'bad'); l_shf = E.lb('ARBORELE', 'bad'); l_vlv = E.lb('SUPAPELE', 'bad')
def ov_rust(C):
    te = L(7) + 0.12
    F.label(C, l_hsg, F.PR(27.2 * math.cos(math.radians(-14)), 27.2 * math.sin(math.radians(-14))), (760, 1060), W(6, 'carcasa') - 0.1, te)
    F.label(C, l_shf, S.P_SHAFT, (60, 1040), W(6, 'arborele') - 0.1, te)
    F.label(C, l_vlv, S.P_BALL, (720, 420), W(6, 'supapele') - 0.1, te)
RUST = [
 S.pump(E, 'pw', L(6), L(7), st='fuel', seq=[('rust', W(6, 'vine') - 0.1, W(6, 'combina') + 0.3)], phase=False, kb=[(L(6),) + S.KB_PW, (L(7), 1.09, 0, 40)],
        fx=[S.fx_fuel(a=0.3), S.fx_drops(('bath_R', 'cam_Ldn'), n=9, speed=7.0, size=1.0),
            S.fx_blotch(HSG, (0.5, 0.2, 0.07), W(6, 'ataca') - 0.3, W(6, 'carcasa') + 0.7, R=4.2, n=16, a=0.75, seed=9),
            S.fx_blotch(HSG, S.RUST3, W(6, 'ataca') - 0.1, W(6, 'carcasa') + 0.9, R=2.6, n=26, soft=False, sq=0.9),
            S.fx_blotch(VLV, S.RUST3, W(6, 'arborele') + 0.2, W(6, 'supapele') + 0.7, R=2.3, n=16, soft=False)],
        ov=ov_rust, labs=[('APOI VINE RUGINA', 'bad big', L(6) + 0.2), ('APA ȘI ACIZII DIN MOTORINĂ ATACĂ METALUL', 'bad', W(6, 'Apa') - 0.1)]),
]

# ------------------------------------------------------------------ rugina desprinsa devine praf abraziv si merge spre regulator si spre injectoare
T_7S = W(7, 'care') - 0.12
DUSTR = [
 S.pump(E, 'pc', L(7), T_7S, st='rust', phase=False, kb=[(L(7), 1.02, 0, 0), (T_7S, 1.09, 0, 0)],
        fx=[S.fx_fuel(a=0.3), S.fx_grit(('bath_R', 'cam_Ldn', 'cam_Lup'), L(7) - 2.0, n=20, speed=13.0, size=0.62, col=S.RUST3), S.fx_flakes(L(7) + 0.2, n=50, size=0.2)],
        labs=[('RUGINA SE DESPRINDE', 'bad big', L(7) + 0.15), ('DEVINE PRAF ABRAZIV', 'bad big', W(7, 'praf') - 0.2)]),
 S.sysm(E, T_7S, L(8), hl=[(['pump'], S.RUST_HL, T_7S), (['reg'], None, W(7, 'regulator') - 0.2), (['rail'], S.RUST_HL, W(7, 'regulator') + 0.2), (['inj'], None, W(7, 'injectoare') - 0.25)],
        flows=[('reg', S.RUST2, 5, 120.0, 5.0, T_7S + 0.1), ('to_rail', S.RUST2, 14, 170.0, 5.0, T_7S + 0.2), ('rail_inj', S.RUST2, 18, 170.0, 5.0, W(7, 'spre', 2) - 0.5)],
        labs=[('PRAFUL DE RUGINĂ MERGE MAI DEPARTE', 'bad', T_7S + 0.1), ('SPRE REGULATOR ȘI INJECTOARE', 'bad big', W(7, 'regulator') - 0.25)]),
]

# ------------------------------------------------------------------ cum eviti: filtrul la timp, separatorul golit, benzinarii cunoscute
T_DR = W(8, 'goleste') + 0.25
l_drn = E.lb('ȘURUBUL DE GOLIRE', 'water')
def ov_drain(C):
    x, y = S.pk(C, [(540, 1836)])[0]
    F.label(C, l_drn, ('px', x + 16, y - 6), (630, 880), W(8, 'goleste') - 0.05, L(9) + 0.1)
AVOID = S.avoid(E, 'filter', 'fwlo', L(8), L(9), [('SCHIMBĂ FILTRUL LA TIMP', W(8, 'schimba')), ('GOLEȘTE SEPARATORUL DE APĂ', W(8, 'goleste')), ('ALIMENTEAZĂ LA BENZINĂRII CUNOSCUTE', W(8, 'alimenteaza'))],
                kb=[(L(8), 0.8, 0, -700), (L(9), 0.83, 0, -726)], seq=[('shut', T_DR + 0.5, T_DR + 2.6)], fx=[S.fx_sep(L(8) - 3.0, water=False), S.fx_drain(T_DR, 3.4, z1=-24.0, n=22, size=1.6)], ov=ov_drain, dim=0)

# ------------------------------------------------------------------ ce facem noi
T_9U = W(9, 'curatam') - 0.12; T_9N = W(9, 'si', 2) - 0.1; T_10I = W(10, 'iar') - 0.1
RKB = (1.25, 250, 0)                       # arborele (ruginit sau curat) in lupa
def ov_mic(C):
    F.lens(C, 'pc', 'rustd', 770, 650, 200, W(9, 'cautam') - 0.2, T_9U + 0.12, kb=RKB, src=S.WM_OBJ, ring=(196, 96, 42))
l_cor = E.lb('PIESĂ CORODATĂ', 'bad'); l_newp = E.lb('PIESĂ NOUĂ', 'good')
def ov_parts(C):
    te = L(10) + 0.12; t1 = W(9, 'inlocuim') - 0.2; t2 = W(9, 'piese', 2) - 0.25
    F.lens(C, 'pc', 'rustd', 262, 660, 158, t1, te, kb=RKB, src=S.WM_OBJ, ring=(255, 75, 75))
    F.lens(C, 'pc', 'dry', 818, 660, 158, t2, te, kb=RKB, src=S.WM_OBJ, ring=(61, 220, 132))
    F.spr(C, l_cor, 262, 832, t1 + 0.2, te, anchor='tc'); F.spr(C, l_newp, 818, 832, t2 + 0.2, te, anchor='tc')
NOI = [
 S.wk(E, 'wm', L(9), T_9U, [('DESFACEM POMPA', 'good big', W(9, 'desfacem') - 0.2), ('CĂUTĂM URMELE DE RUGINĂ, LA MICROSCOP', 'good', W(9, 'cautam') - 0.15)], st='wkdam', ov=ov_mic),
 S.wk_usb(E, T_9U, T_9N, labs=[('CURĂȚĂM PIESELE CU ULTRASUNETE', 'good', T_9U + 0.15)], t_dip=W(9, 'ultrasunete') - 0.6),
 S.wk(E, 'wm', T_9N, L(10), [('PIESELE CORODATE: ÎNLOCUITE CU NOI', 'good', T_9N + 0.15)], st='wkdam', seq=[('wk', W(9, 'piese', 2) - 0.2, W(9, 'piese', 2) + 0.4)], ov=ov_parts),
 S.wk_bench(E, L(10), T_10I, labs=[('TESTĂM POMPA PE BANC', 'good big', W(10, 'testam') - 0.15), ('INCLUSIV LA ETANȘEITATE', 'good big', W(10, 'inclusiv') - 0.15)],
            rows=[('DEBIT', W(10, 'testam') + 0.1), ('PRESIUNE', W(10, 'testam') + 0.5), ('ETANȘEITATE', W(10, 'etanseitate') - 0.1)], t_sheet=L(10) + 0.1),
 S.wk_inj(E, T_10I, L(E.OUT), labs=[('DACĂ APA A AJUNS ȘI LA INJECTOARE', 'bad', T_10I + 0.15), ('LE VERIFICĂM ȘI PE ELE', 'good big', W(10, 'le') - 0.1)]),
]

SHOTS = S.opening(E, HOOK) + [SIGNS] + TANK + FILT + WET + RUST + DUSTR + [AVOID] + NOI + [S.ending(E)]
SPR = E.SPR
