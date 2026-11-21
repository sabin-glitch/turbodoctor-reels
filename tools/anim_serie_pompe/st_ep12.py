# Episodul 12: regulatorul de debit blocat
import math
import numpy as np
import pser as S, ifx as F, i2d as D, ikit as K, pdraw as P, fxlib as X
from icomp import Shot
from fxlib import seg, ease
E = S.Ep(12); W, L, LE = E.W, E.L, E.LE; TOTAL = E.TOTAL; GLOB = S.glob(E)
RED = (255, 75, 75); GREEN = (61, 220, 132); GLINT = (255, 240, 170)
RP, RT = S.mj('reg')                   # punctele si traseele regulatorului (mm)
FILM_Y = S.pf_tint(S.LPY, which='hp')  # pelicula marita, in galbenul motorinei din aceasta serie
KB_RG = (0.76, 0, -170)                # regulatorul intreg in sectiune (rg, rgf), intre insigna si subtitrare
KB_RZ = (0.58, 0, -40)                 # pistonasul, ferestrele si sita, de aproape (rgz)

def fuel_in(C, t0=None, t1=None, n=10, a=1.0, sp=150.0, stop=False):
    """motorina prin regulator: din afara, prin sita si ferestre, apoi in jos spre pompa (stop = se opreste in pistonas)"""
    for i, nm in enumerate(('stop_R', 'stop_L') if stop else ('in_R', 'in_L')):
        S.flow3(C, RT[nm], n, sp, GLINT, 4.6, t0=t0, t1=t1, a=a, seed=3 + i, glow=0.5, lat=3.0)

# ------------------------------------------------------------------ carligul: pistonasul se misca intruna, apoi se agata; acul presiunii din rampa o ia razna
# (coperta, la 2,25 s: regulatorul in sectiune, cercul rosu pe pistonas, acul in rosu)
T_K = 1.3
def ph_hook(t): return min(t, T_K)                       # la 0,3 dintr-o cursa pistonasul ramane aproape deschis
l_rp = E.lb('PRESIUNEA DIN RAMPĂ', 'grey'); l_st = E.lb('PISTONAȘUL SE AGAȚĂ', 'bad big'); l_mv = E.lb('PISTONAȘUL DOZEAZĂ MOTORINA', 'lp')
def ov_hook(C):
    t = C.t; te = E.T_S + 0.1
    fuel_in(C, n=9)
    k = float(seg(t, T_K, T_K + 0.5))
    v = 0.5 + 0.03 * math.sin(t * 7.0) + k * (0.38 + 0.07 * math.sin(t * 23.0))
    S.gauge(C, 790, 1450, 112, v, F.pop(t, 0.05, te), red=(0.8, 1.0), green=(0.38, 0.62)); F.spr(C, l_rp, 790, 1582, 0.1, te, anchor='tc')
    x, y = S.p3(C, [RP['gap']])[0]
    D.arc(C, x, y, 54, 0, 360, RED, 6, F.pop(t, T_K, te)); S.sparks2(C, x, y, t, T_K - 0.05, T_K + 0.5, n=12, L=26.0, R=30.0)
    F.spr(C, l_mv, 540, 1700, 0.1, T_K - 0.05, anchor='tc'); F.spr(C, l_st, 540, 1694, T_K + 0.08, te, anchor='tc')
HOOK = [Shot('rg', 0.0, E.T_S, st='regmove', kb=[(0.0, 0.85, -110, 250), (E.T_S, 0.88, -112, 254)], tr=None, phase=ph_hook, ov=ov_hook, shake=S.shake_at(T_K, 0.7, 5.0))]

SIGNS = S.symptoms(E, 2, [(E.sym('idle', 'RALANTI NEREGULAT'), 'ralanti'), (E.sym('power', 'PUTERE CARE VINE ȘI PLEACĂ'), 'putere'),
                          (E.sym('stall', 'MOTORUL SE OPREȘTE', 'Când ridici piciorul'), 'motor'),
                          (E.sym('ecu', 'ERORI DE PRESIUNE ÎN RAMPĂ', cls='warn'), 'erori')], cam='rgf', st='regfull', kb=KB_RG, y0=690, dy=140)

# ------------------------------------------------------------------ pompa nu comprima tot ce primeste: la intrare sta regulatorul, o supapa electrica
T_3B = W(3, 'la') - 0.15; T_3C = W(3, 'o') - 0.1
KB_ZM = S.kb_on('pw', 'fuel', S.P_ZME, 1.5, 600, 800)
l_coil = E.lb('BOBINA', 'grey'); l_plug = E.lb('MUFA', 'grey')
def ov_zme(C):
    x, y = S.p3(C, [S.P_ZME])[0]; z = C.shot.kbat(C.t)[0]
    D.arc(C, x, y, 96 * z, 0, 360, (255, 210, 31), 7, F.pop(C.t, W(3, 'regulatorul') - 0.35, T_3C + 0.1))
def ov_el(C):
    te = L(4) + 0.1
    fuel_in(C, n=9)
    S.lab3(C, [(l_coil, RP['coil'], (1040, 640), T_3C + 0.3, 'tr'), (l_plug, RP['conn'], (1040, 470), T_3C + 0.55, 'tr')], te)
INLET = [
 S.pump(E, 'pw', L(3), T_3C, kb=[(L(3),) + S.KB_PW, (T_3B, 1.04, 0, 46), (T_3B + 1.0,) + KB_ZM, (T_3C, KB_ZM[0] * 1.03, KB_ZM[1], KB_ZM[2])], ov=ov_zme,
        labs=[('NU COMPRIMĂ TOT CE PRIMEȘTE', 'lp big', L(3) + 0.2), ('LA INTRARE: REGULATORUL DE DEBIT', 'big', T_3B + 0.15)]),
 Shot('rg', T_3C, L(4), st='regmove', kb=[(T_3C,) + KB_RG, (L(4), 0.79, 0, -176)], tr=('xf', 0.3), ov=S.ovs(ov_el,
      S.bl(E, [('O SUPAPĂ ELECTRICĂ', 'big', T_3C + 0.15), ('TRECE DOAR CÂT CERE CALCULATORUL', 'lp big', W(3, 'trece') - 0.2)], L(4)))),
]

# ------------------------------------------------------------------ inauntru, un pistonas cu joc foarte mic se misca tot timpul
l_sp = E.lb('PISTONAȘUL', 'lp'); l_gap = E.lb('JOC FOARTE MIC', 'lp'); l_mesh = E.lb('SITA', 'grey'); l_spr = E.lb('ARCUL', 'grey')
def ov_spool(C):
    te = L(5) + 0.1
    fuel_in(C, n=12)
    S.lab3(C, [(l_sp, RP['spoolL'], (44, 700), W(4, 'pistonas') - 0.2), (l_gap, RP['gap'], (1040, 640), W(4, 'joc') - 0.2, 'tr'),
               (l_mesh, RP['mesh'], (1040, 1060), L(4) + 0.5, 'tr'), (l_spr, RP['spring'], (44, 1080), L(4) + 0.7)], te)
SPOOL = [Shot('rgz', L(4), L(5), st='regmove', kb=[(L(4),) + KB_RZ, (L(5), 0.6, 0, -42)], tr=('xf', 0.3),
              ov=S.ovs(ov_spool, S.bl(E, [('SE MIȘCĂ TOT TIMPUL CÂT MERGE MOTORUL', 'lp', W(4, 'se') - 0.2)], L(5))))]

# ------------------------------------------------------------------ aici se opreste prima murdarie: o particula, putina rugina, un strat de lac; pistonasul se agata
T_5B = W(5, 'particula') - 0.26; T_5C = W(5, 'pistonasul') - 0.2; T_GR = W(5, 'particula') - 0.35; T_ST = T_5C + 0.6
def ov_dirt(C):
    fuel_in(C, n=12)
    for i, nm in enumerate(('stop_R', 'stop_L')):
        S.flow3(C, RT[nm], 10, 90.0, S.DUST2, 7.5, t0=L(5) + 0.1, seed=31 + i, lat=5.0, dark=0.9)
def ov_grain(C):
    t = C.t; yg = 300 + 620 * float(ease(seg(t, T_GR, T_GR + 0.85))); a = F.pop(t, T_GR, W(5, 'rugina') - 0.25)
    S.grain2(C, 540 + 14 * math.sin(t * 3.0) * (1 - float(seg(t, T_GR + 0.6, T_GR + 0.85))), yg, 58, a, seed=5)
    S.sparks2(C, 540, 920, t, T_GR + 0.85, T_GR + 1.5, n=10, L=30.0, R=44.0)
def ph_stick(t):
    u = min(max(t - T_5C, 0.0), 0.6); return 0.28 + u - u * u / 1.2          # incetineste si ramane pe loc dupa 0,6 s
l_stick = E.lb('PISTONAȘUL SE AGAȚĂ', 'bad big')
def ov_stick(C):
    t = C.t; te = L(6) + 0.1
    fuel_in(C, n=10, a=1.0 - 0.5 * float(seg(t, T_5C, T_ST)))
    x, y = S.p3(C, [RP['gap']])[0]
    D.arc(C, x, y, 58, 0, 360, RED, 6, F.pop(t, T_ST - 0.1, te)); S.sparks2(C, x, y, t, T_ST - 0.1, T_ST + 0.5, n=12, L=26.0, R=30.0)
    F.spr(C, l_stick, 540, 1186, T_ST - 0.15, te, anchor='tc')
DIRT = [
 Shot('rgz', L(5), T_5B, st='regmove', kb=[(L(5), 0.6, 0, -42), (T_5B, 0.62, 0, -44)], tr=None,
      ov=S.ovs(ov_dirt, S.bl(E, [('AICI SE OPREȘTE PRIMA MURDĂRIE', 'bad big', L(5) + 0.15)], T_5B))),
 S.film(E, T_5B, T_5C, seq=[('mrust1', W(5, 'rugina') - 0.3, W(5, 'rugina') + 0.5), ('mlac2', W(5, 'strat') - 0.2, W(5, 'lac') + 0.5)], pf=FILM_Y,
        flow=((255, 236, 150), None), sides=('BUCȘA', 'PISTONAȘUL'), ov=ov_grain,
        labs=[('O PARTICULĂ TRECUTĂ DE FILTRU', 'bad', T_GR), ('PUȚINĂ RUGINĂ', 'bad big', W(5, 'putina') - 0.15), ('UN STRAT DE LAC, DE CÂȚIVA MICRONI', 'bad', W(5, 'un') - 0.15)]),
 Shot('rgz', T_5C, L(6), st='regmove', kb=[(T_5C, 0.6, 0, -42), (L(6), 0.63, 0, -44)], tr=('xf', 0.3), phase=ph_stick, ov=ov_stick, shake=S.shake_at(T_ST - 0.1, 0.7, 5.0)),
]

# ------------------------------------------------------------------ ramas prea deschis: presiunea urca peste cea ceruta; ramas prea inchis: pompa ramane fara motorina
T_6A = W(6, 'lasa') - 0.1; T_6B = W(6, 'ramas', 2) - 0.12; T_6C = W(6, 'lasa', 2) - 0.1
gp = E.panel('PRESIUNEA DIN RAMPĂ', 880, 600)
_u = np.linspace(0, 1, 60); _s = lambda a, b, x: np.clip((x - a) / (b - a), 0, 1) ** 2 * (3 - 2 * np.clip((x - a) / (b - a), 0, 1))
REQ = 0.46 + 0.0 * _u
HI = 0.46 + 0.4 * _s(0.18, 0.7, _u) + 0.02 * np.sin(_u * 40.0) * _s(0.3, 0.6, _u)
LO = 0.46 - 0.36 * _s(0.18, 0.7, _u) + 0.02 * np.sin(_u * 40.0) * _s(0.3, 0.6, _u)
def graph(curve, t_in, t_out, tag_v):
    def ov(C):
        P.graph_panel(C, gp, 540, 470, 880, 600, [(_u, REQ, GREEN, 6), (_u, curve, RED, 6)], t_in, t_out + 0.12, t_in + 0.25, dur=1.3, xlab='TIMP', ylab='PRESIUNE',
                      tags=[('CERUTĂ', GREEN, 0.3, 0.5), ('REALĂ', (255, 120, 120), 0.99, tag_v)])
    return ov
def ov_open(C): fuel_in(C, n=22, sp=210.0)
def ov_shut(C): fuel_in(C, n=10, sp=110.0, stop=True)
STUCK = [
 Shot('rgz', L(6), T_6A, st='regopen', kb=[(L(6), 0.6, 0, -42), (T_6A, 0.62, 0, -44)], phase=False, tr=('xf', 0.3),
      ov=S.ovs(ov_open, S.bl(E, [('RĂMAS PREA DESCHIS', 'bad big', L(6) + 0.12)], T_6A))),
 S.plain(E, T_6A, T_6B, S.ovs(graph(HI, T_6A, T_6B, 0.97), S.bl(E, [('PRESIUNEA URCĂ PESTE CEA CERUTĂ', 'bad big', W(6, 'presiunea') - 0.1)], T_6B, y=1150))),
 Shot('rgz', T_6B, T_6C, st='regshut', kb=[(T_6B, 0.6, 0, -42), (T_6C, 0.62, 0, -44)], phase=False, tr=('xf', 0.3),
      ov=S.ovs(ov_shut, S.bl(E, [('RĂMAS PREA ÎNCHIS', 'bad big', T_6B + 0.12)], T_6C))),
 S.plain(E, T_6C, L(7), S.ovs(graph(LO, T_6C, L(7), 0.2), S.bl(E, [('POMPA RĂMÂNE FĂRĂ MOTORINĂ', 'bad big', T_6C + 0.2), ('TRAGE SLAB SAU NU MAI PORNEȘTE', 'bad big', W(6, 'iar') - 0.1)], L(7), y=1150))),
]

# ------------------------------------------------------------------ regulatorul e si martorul pompei: pilitura pe sita lui = pompa se roade pe dinauntru
T_7B = W(7, 'daca') - 0.12
KB_RS = (0.8, 0, -260)
FLK = S.pfs(S.pf_cryst(n=95, seed=7, box=(250, 800, 850, 1270), r=(8.0, 19.0), col=(0.52, 0.55, 0.6), edge=(22, 25, 31), amin=0.8, t0=W(7, 'sita') - 0.3, t1=W(7, 'pilitura') + 0.5))
FIL_IN = [[(30, 760), (190, 900), (330, 1000)], [(1050, 800), (900, 930), (760, 1010)], [(40, 1250), (200, 1160), (330, 1090)], [(1050, 1260), (880, 1160), (760, 1090)]]
def ov_mesh(C):
    t = C.t; te = L(8) + 0.1
    for i, pth in enumerate(FIL_IN): S.flowp(C, pth, 6, 120.0, S.METAL2, 4.6, t0=T_7B + 0.2, seed=41 + i, lat=10.0, glow=0.5, dark=0.6)
    F.lens(C, 'pc', 'damf', 866, 566, 150, W(7, 'pompa') - 0.15, te, kb=(0.5, 0, 10), ring=RED)
WITNESS = [
 Shot('rgf', L(7), T_7B, st='regfull', kb=[(L(7),) + KB_RG, (T_7B, 0.79, 0, -176)], phase=False, tr=('xf', 0.3),
      ov=S.bl(E, [('REGULATORUL: MARTORUL POMPEI', 'big', L(7) + 0.2)], T_7B)),
 Shot('rgs', T_7B, L(8), st='regfull', kb=[(T_7B,) + KB_RS, (L(8), 0.84, 0, -268)], phase=False, tr=('xf', 0.3), pf=FLK,
      ov=S.ovs(ov_mesh, S.bl(E, [('PILITURĂ PE SITA REGULATORULUI', 'bad big', W(7, 'sita') - 0.3), ('POMPA SE ROADE PE DINĂUNTRU', 'bad big', W(7, 'pompa') - 0.15)], L(8)))),
]

# ------------------------------------------------------------------ cum eviti: filtru la timp, motorina curata; un regulator nou pe o pompa care face pilitura nu rezolva nimic
T_8B = W(8, 'iar') - 0.1
hd_ev = S.hd(E, 'CUM EVIȚI', L(8), L(9) + 0.1, 'good big')
cds = S.cards(E, [('FILTRU SCHIMBAT LA TIMP', W(8, 'filtru')), ('MOTORINĂ CURATĂ', W(8, 'motorina')), ('REGULATOR NOU PE O POMPĂ ROASĂ', W(8, 'nu') - 0.1, False)], L(9) + 0.1)
l_newr = E.lb('REGULATOR NOU', 'good')
def ov_newr(C):
    te = L(9) + 0.1; t0 = W(8, 'regulator') - 0.2
    F.lens(C, 'rgf', 'regfull', 800, 640, 170, t0, te, kb=(0.31, -16, 2), ring=GREEN); F.spr(C, l_newr, 800, 826, t0 + 0.2, te, anchor='tc')
AVOID = [
 Shot('rgf', L(8), T_8B, st='regfull', kb=[(L(8), 0.79, 0, -176), (T_8B, 0.82, 0, -180)], phase=False, tr=('xf', 0.3), ov=S.ovs(hd_ev, cds),
      dim=lambda t: 0.24 * F.pop(t, W(8, 'filtru') - 0.2, T_8B + 0.3)),
 Shot('pm', T_8B, L(9), st='damf', kb=[(T_8B, 1.0, 0, -60), (L(9), 1.06, 0, -64)], phase=False, tr=('xf', 0.3),
      fx=[S.fx_dry(T_8B, rate=8.0, amp=0.7, size=0.2, speed=30.0), S.fx_flakes(T_8B + 0.1)], ov=S.ovs(hd_ev, cds, ov_newr), dim=lambda t: 0.2),
]

# ------------------------------------------------------------------ ce facem noi: nu schimbam regulatorul pe ghicite; desfacem, cautam pilitura, testam pe banc
T_9B = W(9, 'desfacem') - 0.12; T_9C = W(9, 'si') - 0.1; T_10B = W(10, 'daca', 2) - 0.12
v_ok = E.lb('POMPĂ SĂNĂTOASĂ: REGULATOR NOU', 'good big'); v_no = E.lb('DACĂ NU: O RECONDIȚIONĂM ÎNTREAGĂ', 'good big')
def ov_verdict(C):
    te = L(E.OUT) + 0.12
    F.spr(C, v_ok, 540, 1196, W(10, 'pompa') - 0.2, T_10B, anchor='tc'); F.spr(C, v_no, 540, 1196, T_10B + 0.1, te, anchor='tc')
    F.lens(C, 'rgf', 'regfull', 250, 640, 160, W(10, 'ajunge') - 0.2, T_10B + 0.1, kb=(0.29, -15, 2), ring=GREEN)
NOI = [
 S.wk(E, 'wm', L(9), T_9B, [('NU SCHIMBĂM REGULATORUL PE GHICITE', 'good', W(9, 'nu') - 0.15)], st='wkdam'),
 S.wk_mic(E, T_9B, T_9C, labs=[('DESFACEM POMPA', 'good big', T_9B + 0.12), ('CĂUTĂM PILITURA, LA MICROSCOP', 'good big', W(9, 'cautam') - 0.15)],
          lens=(W(9, 'cautam') - 0.1, T_9C + 0.1), tr=None),
 S.wk_bench(E, T_9C, L(10), labs=[('TESTĂM TOTUL PE BANC', 'good big', T_9C + 0.15)], rows=[('DEBIT', W(9, 'debit') - 0.1), ('PRESIUNE', W(9, 'presiune') - 0.1)], t_sheet=W(9, 'testam') + 0.2),
 S.wk(E, 'px', L(10), L(E.OUT), st='full', kb=[(L(10), 0.7, 0, 20), (L(E.OUT), 0.74, 0, 14)], ov=ov_verdict),
]

SHOTS = S.opening(E, HOOK) + [SIGNS] + INLET + SPOOL + DIRT + STUCK + WITNESS + AVOID + NOI + [S.ending(E)]
SPR = E.SPR
