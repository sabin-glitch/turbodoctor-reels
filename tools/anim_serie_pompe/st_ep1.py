# Episodul 1: aerul ramas dupa schimbul de filtru. Filtrul nou, montat gol, e plin de aer; pompa porneste fara pelicula de motorina,
# cama, rola si pistonul lucreaza metal pe metal, iar pilitura pleaca prin toata instalatia. Momentele: ep1/vo/cues.json.
import math, json, os
import numpy as np
import icomp as IC, ifx as F, ikit as K, pser as S, i2d as D
import fxlib as X
from icomp import Shot
from fxlib import seg

E = S.Ep(1); N = E.n; EP = E.ep; W, L, LE = E.W, E.L, E.LE; TOTAL = E.TOTAL
GLOB = S.glob(E)
STOP_CRANK = ('<div class="stop" style="max-width:940px"><div class="ic">%s</div><div>MOTORUL NU SE PORNEȘTE'
              '<small>ca să tragă singur motorina</small></div></div>') % K.ICON['stop']

SPR = dict(S.spr_common(N), **{
 # semnele
 's_crank': K.sym('start', 'DEMARORUL ÎNVÂRTE MULT'),
 's_hard': K.sym('engine', 'MOTORUL PORNEȘTE GREU'),
 's_stall': K.sym('stall', 'SE OPREȘTE', 'După câteva secunde'),
 # pompa nu are ulei
 'l_nooil': K.lb('POMPA NU ARE ULEI', 'grey big'),
 'l_lube': K.lb('UNSĂ ȘI RĂCITĂ DE MOTORINĂ', 'lp big'),
 'l_fuel': K.lb('MOTORINĂ', 'lp'),
 # filtrul gol
 'l_newf': K.lb('FILTRU NOU, MONTAT GOL', 'grey'),
 'l_air': K.lb('PLIN DE AER', 'bad big'),
 'sys': D.sys_svg(),
 'h_filter_w': D.sys_hl(['filter'], **S.WHITE_HL), 'h_pump': D.sys_hl(['pump']), 'h_reg': D.sys_hl(['reg']), 'h_rail': D.sys_hl(['rail']),
 'h_inj': D.sys_hl(['inj']), 'h_ret': D.sys_hl(['ret']), 'h_tank': D.sys_hl(['tank']), 'h_lp': D.sys_hl(['lp']),
 'h_epump_g': D.sys_hl(['epump'], **S.GREEN_HL), 'h_filter_g': D.sys_hl(['filter'], **S.GREEN_HL), 'h_lp_g': D.sys_hl(['lp'], **S.GREEN_HL),
 'l_airfirst': K.lb('ÎN POMPĂ AJUNGE ÎNTÂI AERUL', 'bad big', 'Nu motorina'),
 # metal pe metal
 'l_nofilm': K.lb('FĂRĂ PELICULA DE MOTORINĂ', 'bad'),
 'l_cam': K.lb('CAMA'), 'l_roller': K.lb('ROLA'), 'l_plunger': K.lb('PISTONUL'),
 'l_metal': K.lb('METAL PE METAL', 'bad big'),
 'l_scratch': K.lb('SUPRAFEȚELE SE ZGÂRIE', 'bad big'),
 # pilitura
 'l_filings': K.lb('PILITURĂ FINĂ', 'bad big', 'Se desprinde din zgârieturi'),
 'l_starts': K.lb('MOTORUL PORNEȘTE PÂNĂ LA URMĂ', 'grey'),
 'l_wear': K.lb('UZURA A ÎNCEPUT', 'bad big', 'Merge mai departe la fiecare drum'),
 'l_goes': K.lb('PILITURA PLEACĂ ODATĂ CU MOTORINA', 'bad'),
 'l_ret': K.lb('PRIN RETUR, ÎN REZERVOR', 'bad'),
 'l_again': K.lb('ȘI DIN NOU SPRE POMPĂ', 'bad big'),
 # cum eviti
 'g_avoid': K.lb('CUM EVIȚI', 'good big'),
 'c_fill': K.chk('INSTALAȚIA SE UMPLE'),
 'c_bleed': K.chk('SE AERISEȘTE ÎNAINTE DE PORNIRE'),
 'c_proc': K.chk('DUPĂ PROCEDURA MAȘINII'),
 'st_crank': STOP_CRANK,
 # ce facem noi
 'g_noi': K.lb('CE FACEM NOI LA TURBO DOCTOR', 'big'),
 'l_apart': K.lb('POMPA DESFĂCUTĂ', 'grey'),
 'l_mic': K.lb('VERIFICATĂ LA MICROSCOP', 'grey'),
 'l_found': K.lb('PILITURĂ ȘI ZGÂRIETURI', 'bad'),
 'l_recond': K.lb('RECONDIȚIONATĂ CU PIESE NOI', 'good big'),
 'l_bench': K.lb('TESTATĂ PE BANC', 'good big'),
 'sheet': K.panel('FIȘA DE TEST', 440, 344),
 'c_flow': K.chk('DEBIT'), 'c_press': K.chk('PRESIUNE'), 'c_seal': K.chk('ETANȘEITATE'),
 'l_injst': K.lb('INJECTOARELE, VERIFICATE PE STAND', 'good', 'La ele a ajuns aceeași pilitură'),
})

# ------------------------------------------------------------------ carligul: filtrul gol, apoi pompa care merge uscata
T_H = 1.3
HOOK = [
 Shot('fl', 0.0, T_H, st='fempty', kb=[(0.0, 0.9, 0, 66), (T_H, 0.96, 0, 40)], fx=[S.fx_flt_air()], tr=None, phase=False),
 Shot('pc', T_H, E.T_S, st='dry', kb=[(T_H, 1.0, 0, 0), (E.T_S, 1.06, 0, 0)], fx=[S.fx_dry(T_H - 0.05, rate=12.0, amp=1.35, n=26)], tr=('flash', 0.3),
      shake=S.shake_at(T_H, 1.7, 3.0)),
]

# ------------------------------------------------------------------ semnele
SIGNS = S.symptoms(E, 2, [('s_crank', 'demarorul'), ('s_hard', 'porneste'), ('s_stall', 'opreste')], fx=[S.fx_flt_air()])

# ------------------------------------------------------------------ pompa nu are ulei: e unsa de motorina
T_P = W(3, 'piesele') - 0.25
def ov_nooil(C):
    F.spr(C, 'l_nooil', 540, 372, W(3, 'nu') - 0.1, T_P + 0.1, anchor='tc')
def ov_lube(C):
    F.spr(C, 'l_lube', 540, 1186, W(3, 'unse') - 0.1, LE(3) + 0.3, anchor='tc')
    F.label(C, 'l_fuel', S.P_LPBATH, (1040, 1060), W(3, 'motorina') - 0.1, LE(3) + 0.3, anchor='tr')

# ------------------------------------------------------------------ filtrul nou, plin de aer; aerul ajunge primul in pompa
T_M4 = W(4, 'daca') - 0.15
def ov_newf(C):
    F.spr(C, 'l_newf', 540, 372, W(4, 'nou') - 0.1, T_M4 + 0.1, anchor='tc')
    F.label(C, 'l_air', F.PR(27.0, 96.0), (1040, 640), W(4, 'plin') - 0.1, T_M4 + 0.1, anchor='tr')

def P2(x, y): return (D.SYS_X + x, D.SYS_Y + y)
AIR_UP = D.Poly([P2(155, 470), P2(155, 410), P2(155, 358), P2(155, 262)])
def ov_sys4(C):
    t = C.t; t0 = T_M4; te = L(5) + 0.2
    a = S.sysmap(C, t0, te, [('h_filter_w', t0 + 0.1), ('h_pump', W(4, 'pompa') - 0.1)])
    S.sys_flow(C, ['lp_f'], 16, 70.0, S.LP2, 5.0, a, t0=t0 + 0.3, seed=4, glow=0.4)                       # motorina vine din urma
    D.flow2(C, [AIR_UP], 16, 105.0, S.AIR2, 9.0, t0=t0 + 0.3, a=a, seed=7, ring=True, jit=0.3, lat=9.0)    # aerul din filtru, inainte
    px, py = D.sys_pt('pump')
    ap = a * float(seg(t, W(4, 'ajunge'), W(4, 'ajunge') + 0.6))
    if ap > 0.003:
        r = X.rnd(17, 9, 4)
        for i in range(9):
            ph = (t * 0.5 + r[i, 0]) % 1.0
            D.dots2(C, np.array([[px - 60 + 120 * r[i, 1], py + 50 - 110 * ph]]), 7.0 + 5.0 * r[i, 2], S.AIR2, ap * math.sin(ph * math.pi), ring=True)
    F.spr(C, 'l_airfirst', 540, 384, W(4, 'ajunge') - 0.1, te, anchor='tc')

# ------------------------------------------------------------------ metal pe metal
T_D0 = W(5, 'pelicula') - 0.1; T_D1 = T_D0 + 1.0
def ov_metal(C):
    te = L(6) + 0.2; tm = W(5, 'metal') - 0.1
    F.spr(C, 'l_nofilm', 540, 1190, T_D0, tm, anchor='tc')
    S.lab_parts(C, [('l_cam', 'cam', (1040, 1050), W(5, 'cama') - 0.1, 'tr'), ('l_roller', 'roller', (44, 690), W(5, 'rola') - 0.1),
                    ('l_plunger', np.array([0.0, -3.2, S.hC(C) + 26.0]), (1040, 404), W(5, 'pistonul') - 0.1, 'tr')], te)
    F.spr(C, 'l_metal', 540, 1180, tm, W(5, 'suprafetele') - 0.1, anchor='tc')
    F.spr(C, 'l_scratch', 540, 1180, W(5, 'suprafetele') - 0.1, te, anchor='tc')

# ------------------------------------------------------------------ pilitura fina; uzura a inceput
T_W = W(6, 'motorul') - 0.2
def ov_filings(C):
    F.spr(C, 'l_filings', 540, 1150, W(6, 'pilitura') - 0.1, T_W + 0.1, anchor='tc')
def ov_wear(C):
    F.spr(C, 'l_starts', 540, 1190, W(6, 'porneste') - 0.1, W(6, 'uzura') - 0.1, anchor='tc')
    F.spr(C, 'l_wear', 540, 1150, W(6, 'uzura') - 0.1, L(7) + 0.2, anchor='tc')

# ------------------------------------------------------------------ pilitura pleaca prin instalatie
PUMP_REG = D.Poly([P2(155, 262), P2(155, 334)])
def ov_sys7(C):
    t = C.t; t0 = L(7) - 0.1; te = L(8) + 0.2
    tr, ta, ti = W(7, 'regulatorul') - 0.1, W(7, 'rampa') - 0.1, W(7, 'injectoare') - 0.1
    tq, tk, tp = W(7, 'retur') - 0.1, W(7, 'rezervor') - 0.1, W(7, 'spre') - 0.1
    a = S.sysmap(C, t0, te, [('h_pump', t0 + 0.1), ('h_reg', tr), ('h_rail', ta), ('h_inj', ti), ('h_ret', tq), ('h_tank', tk), ('h_lp', tp)])
    S.sys_flow(C, ['lp'], 22, 80.0, S.LP2, 4.0, 0.55 * a, seed=2, glow=0.2)                                    # motorina, tot timpul
    D.flow2(C, [PUMP_REG], 10, 70.0, S.METAL2, 4.2, t0=tr - 0.3, a=a, seed=3, glow=0.6, lat=10.0)
    S.sys_flow(C, ['inj'], 90, 380.0, S.METAL2, 4.2, a, t0=ta - 1.15, seed=5, glow=0.6)                        # pompa -> rampa -> injectoare
    S.sys_flow(C, ['ret', 'ret_p'], 60, 520.0, S.METAL2, 4.0, a, t0=tq - 0.2, seed=6, glow=0.6)                # returul
    S.sys_flow(C, ['tank'], 26, 150.0, S.METAL2, 4.0, a, t0=tk + 0.1, seed=8, glow=0.6, lat=10.0)              # pe fundul rezervorului
    S.sys_flow(C, ['lp'], 26, 230.0, S.METAL2, 4.0, a, t0=tp - 0.4, seed=9, glow=0.6)                          # din nou spre pompa
    px, py = D.sys_pt('pump')
    for i in range(4):                                                                                           # pompa care se roade
        ph = (t * 1.7 + i * 0.25) % 1.0
        if ph < 0.35: D.dots2(C, np.array([[px + 60 * math.cos(i * 1.9 + t), py + 50 * math.sin(i * 2.3 + t)]]), 5.0 * (1 - ph / 0.35), (255, 200, 120), a, glow=0.8)
    F.spr(C, 'l_goes', 540, 396, t0 + 0.1, tq, anchor='tc')
    F.spr(C, 'l_ret', 540, 396, tq, W(7, 'din') - 0.1, anchor='tc')
    F.spr(C, 'l_again', 540, 390, W(7, 'din') - 0.1, te, anchor='tc')

# ------------------------------------------------------------------ cum eviti: instalatia se umple si se aeriseste; motorul nu se porneste ca sa traga singur
T_F0 = W(8, 'umple') - 0.25; T_F1 = W(8, 'inainte'); T_M8 = W(8, 'motorul') - 0.2
def ov_fill(C):
    te = T_M8 + 0.1
    F.spr(C, 'g_avoid', 540, 372, L(8) - 0.05, te, anchor='tc')
    F.spr(C, 'c_fill', 540, 1010, W(8, 'umple') - 0.1, te, anchor='tc')
    F.spr(C, 'c_bleed', 540, 1096, W(8, 'aeriseste') - 0.1, te, anchor='tc')
    F.spr(C, 'c_proc', 540, 1182, W(8, 'procedura') - 0.1, te, anchor='tc')

def ov_sys8(C):
    t = C.t; t0 = T_M8; te = L(9) + 0.2
    a = S.sysmap(C, t0, te, [('h_epump_g', t0 + 0.2), ('h_lp_g', t0 + 0.5), ('h_filter_g', t0 + 0.9)])
    S.sys_flow(C, ['lp'], 34, 120.0, S.LP2, 5.0, a, t0=t0 + 0.3, seed=12, glow=0.45)
    F.spr(C, 'st_crank', 540, 380, W(8, 'nu') - 0.15, te, anchor='tc')

# ------------------------------------------------------------------ ce facem noi: microscopul, piesele noi, bancul, standul de injectoare
T_B = L(10) - 0.1; T_I = W(10, 'iar') - 0.2; T_NEW = W(9, 'reconditionam') - 0.1
LENS_KB = (1.6, -128, 128)               # cama zgariata de sub rola, in lupa
def ov_mic(C):
    te = T_B + 0.15
    F.spr(C, 'g_noi', 540, 372, L(9) - 0.05, te, anchor='tc')
    F.spr(C, 'l_apart', 540, 1196, W(9, 'desfacem') - 0.1, W(9, 'microscop') - 0.3, anchor='tc')
    F.lens(C, 'pc', 'dam', 770, 650, 200, W(9, 'microscop') - 0.3, T_NEW + 0.1, kb=LENS_KB, src=S.WM_OBJ)
    F.spr(C, 'l_mic', 540, 1196, W(9, 'microscop') - 0.3, W(9, 'pilitura') - 0.1, anchor='tc')
    F.spr(C, 'l_found', 540, 1196, W(9, 'pilitura') - 0.1, T_NEW + 0.1, anchor='tc')
    F.spr(C, 'l_recond', 540, 1180, T_NEW + 0.1, te, anchor='tc')

def ov_bench(C):
    te = T_I + 0.15
    F.spr(C, 'g_noi', 540, 372, L(9) - 0.05, te, anchor='tc')
    F.spr(C, 'l_bench', 540, 1186, W(10, 'banc') - 0.25, te, anchor='tc')
    S.test_sheet(C, 800, 470, W(10, 'debit') - 0.45, te, [('c_flow', W(10, 'debit') - 0.1), ('c_press', W(10, 'presiune') - 0.1), ('c_seal', W(10, 'etanseitate') - 0.1)])

def ov_injst(C):
    te = L(E.OUT) + 0.2
    F.spr(C, 'g_noi', 540, 372, L(9) - 0.05, te, anchor='tc')
    F.spr(C, 'l_injst', 540, 1160, W(10, 'verificam') - 0.2, te, anchor='tc')

# ------------------------------------------------------------------ planuri
bh = S.scr('pw', 'fuel', S.P_contact(S.H0), (1.04, 0, 40))
SHOTS = S.opening(E, HOOK) + [
 SIGNS,
 Shot('pw', L(3), T_P, st='fuel', tr=('xf', 0.3), kb=[(L(3), 1.0, 0, 46), (T_P, 1.04, 0, 40)], fx=[S.fx_fuel()], ov=ov_nooil),
 Shot('pc', T_P, L(4), st='fuel', tr=('dive', 0.75, bh, 2.6, 'full'), kb=[(T_P, 1.0, 0, 0), (L(4), 1.05, 0, 0)], fx=[S.fx_fuel(n=60, a=0.6)], ov=ov_lube),
 Shot('fl', L(4), T_M4, st='fempty', tr=('xf', 0.3), kb=[(L(4), 0.9, 0, 66), (T_M4, 0.94, 0, 56)], fx=[S.fx_flt_air()], ov=ov_newf, phase=False),
 S.sys_shot(E, T_M4, L(5), ov_sys4),
 Shot('pc', L(5), L(6), st='fuel', seq=[('dry', T_D0, T_D1)], tr=('xf', 0.3), kb=[(L(5), 1.0, 0, 0), (L(6), 1.07, 0, 0)],
      fx=[S.fx_fuel(t_off=T_D0, n=60, a=0.6), S.fx_bubbles(L(5) - 0.8, T_D0 + 0.3), S.fx_dry(T_D1 - 0.3)], ov=ov_metal,
      shake=S.shakes(S.shake_at(W(5, 'metal') - 0.1, 1.0, 2.5), S.shake_at(W(5, 'zgarie') - 0.1, 1.0, 4.0))),
 Shot('pm', L(6), T_W, st='dry', seq=[('dam', L(6) + 0.5, L(6) + 2.2)], tr=('dive', 0.6, S.scr('pc', 'dry', S.P_contact(S.H0), (1.07, 0, 0)), 2.4, 'full'), kb=[(L(6), 1.0, 0, 0), (T_W, 1.06, 0, 0)],
      fx=[S.fx_dry(L(6) - 0.2, rate=9.0, amp=0.75, size=0.2, speed=30.0), S.fx_flakes(L(6) + 0.2)], ov=ov_filings, phase=False,
      shake=S.shake_at(L(6), T_W - L(6) + 0.5, 2.0)),
 Shot('pc', T_W, L(7), st='fuel', tr=('xf', 0.35), kb=[(T_W, 1.04, 0, 0), (L(7), 1.0, 0, 0)],
      fx=[S.fx_fuel(n=36, a=0.3), S.fx_filings(T_W - 1.5)], ov=ov_wear),
 S.sys_shot(E, L(7), L(8), ov_sys7),
 Shot('fl', L(8), T_M8, st='fempty', wipe=('ffull', T_F0, T_F1, 26, 'up', (1440, 330)), tr=('xf', 0.3), kb=[(L(8), 0.9, 0, 66), (T_M8, 0.93, 0, 60)],
      fx=[S.fx_flt_air(t_off=T_F1 - 0.6), S.fx_flt_fuel(T_F1 - 0.4)], ov=ov_fill, phase=False),
 S.sys_shot(E, T_M8, L(9), ov_sys8),
 Shot('wm', L(9), T_B, st='wkdam', seq=[('wk', T_NEW, T_NEW + 0.5)], tr=('xf', 0.35), kb=[(L(9), 1.0, 0, 0), (T_B, 1.06, 0, 0)], ov=ov_mic, phase=False),
 Shot('wb', T_B, T_I, st='wk', tr=('xf', 0.35), kb=[(T_B, 1.0, 0, 0), (T_I, 1.05, 0, 0)], ov=ov_bench, phase=False),
 Shot('wi', T_I, L(E.OUT), st='wk', tr=('xf', 0.35), kb=[(T_I, 1.0, 0, 0), (L(E.OUT), 1.06, 0, 0)], fx=[S.fx_spray(T_I + 0.4)], ov=ov_injst, phase=False),
 S.ending(E),
]
