# Episodul 17: pompa la mana a doua
import math
import numpy as np
import pser as S, ifx as F, i2d as D, ikit as K, pdraw as P, fxlib as X
from icomp import Shot
from fxlib import seg, ease
E = S.Ep(17); W, L, LE = E.W, E.L, E.LE; TOTAL = E.TOTAL; GLOB = S.glob(E)
RED = (255, 75, 75); GREEN = (61, 220, 132)
LENS_W = (0.5, 0, 10)                  # cama si rola in sectiune, intr-o lupa (placile pc)

# ------------------------------------------------------------------ carligul: raftul cu zece pompe la fel; una, in lupa, e roasa pe dinauntru
# (coperta, la 2,25 s: raftul, cercul rosu pe o pompa si lupa cu cama roasa)
P_OPEN = (432, 925)                    # pompa aleasa, pe placa sh
T_H = 1.15
l_h1 = E.lb('POMPE FOLOSITE, DE LA DEZMEMBRĂRI', 'grey'); l_h2 = E.lb('UNA E ROASĂ PE DINĂUNTRU', 'bad big')
def ov_hook(C):
    t = C.t; te = E.T_S + 0.1
    x, y = S.pk(C, [P_OPEN])[0]
    D.arc(C, x, y, 88, 0, 360, RED, 6, F.pop(t, T_H, te))
    F.lens(C, 'pc', 'dam', 806, 1420, 190, T_H + 0.05, te, kb=LENS_W, src=('px', x + 58, y + 62), ring=RED)
    F.spr(C, l_h1, 540, 1640, 0.1, T_H, anchor='tc'); F.spr(C, l_h2, 540, 1634, T_H + 0.15, te, anchor='tc')
HOOK = [Shot('sh', 0.0, E.T_S, st='shelf', kb=[(0.0, 0.84, 0, 171), (E.T_S, 0.87, 0, 176)], tr=None, phase=False, ov=ov_hook)]

# ------------------------------------------------------------------ semnele: o vreme merge, apoi vin pornirea grea, lipsa de putere, erorile; uneori urmeaza injectoarele
SIGNS = S.symptoms(E, 2, [(E.sym('start', 'PORNIRE GREA'), 'pornirea'), (E.sym('power', 'PIERDERE DE PUTERE'), 'pierderea'),
                          (E.sym('ecu', 'ERORI DE PRESIUNE'), 'erorile'), (E.sym('warn', 'UNEORI URMEAZĂ INJECTOARELE', cls='warn'), 'uneori')],
                   cam='pw', st='fuel', kb=S.KB_PW, fx=[S.fx_fuel()], y0=690, dy=140, phase=None)
SIGNS.ov = S.ovs(SIGNS.ov, S.tl(E, [('DUPĂ MONTAREA UNEI POMPE FOLOSITE', 'grey', W(2, 'dupa') - 0.1), ('O VREME, MAȘINA MERGE', 'good big', W(2, 'masina') - 0.15)], W(2, 'apoi') + 0.2))

# ------------------------------------------------------------------ nu se poate judeca din ochi: uzura e inauntru; pe dinafara, una buna si una roasa arata la fel
T_3B = W(3, 'uzura') - 0.15; T_3C = W(3, 'dinafara') - 0.45
KB_2 = (1.06, 0, -57)                  # cele doua pompe de pe polita de sus (placa sh2, care trebuie sa acopere cadrul)
P2A = (270, 1000); P2B = (810, 1000)   # centrele lor pe placa sh2
l_q = E.lb('?', 'big'); l_cam = E.lb('CAMA', 'grey'); l_pl = E.lb('PISTOANELE', 'grey'); l_vl = E.lb('SUPAPELE', 'grey')
def ov_two(C):
    te = T_3B + 0.1
    for i, p in enumerate((P2A, P2B)):
        x, y = S.pk(C, [p])[0]; F.spr(C, l_q, x, y - 392, L(3) + 0.25 + 0.2 * i, te, anchor='tc')
def ov_in(C):
    te = T_3C + 0.1
    S.lab_parts(C, [(l_cam, 'cam', (1040, 1090), W(3, 'cama') - 0.2, 'tr'), (l_pl, 'plunger', (44, 590), W(3, 'pistoane') - 0.2),
                    (l_vl, S.P_BALL, (1040, 500), W(3, 'supape') - 0.2, 'tr')], te)
l_ok = E.lb('BUNĂ', 'good big'); l_bad = E.lb('ROASĂ', 'bad big')
def ov_pair(C):
    te = L(4) + 0.1; ta = W(3, 'una') - 0.2; tb = W(3, 'una', 2) - 0.2
    xa, ya = S.pk(C, [P2A])[0]; xb, yb = S.pk(C, [P2B])[0]
    F.lens(C, 'pc', 'fuel', xa, ya + 22, 162, ta, te, kb=LENS_W, ring=GREEN, tag='ok17')
    F.lens(C, 'pc', 'damf', xb, yb + 22, 162, tb, te, kb=LENS_W, ring=RED, tag='bad17')
    F.spr(C, l_ok, xa, ya + 198, ta + 0.2, te, anchor='tc'); F.spr(C, l_bad, xb, yb + 198, tb + 0.2, te, anchor='tc')
INSIDE = [
 Shot('sh2', L(3), T_3B, st='shelf', kb=[(L(3),) + KB_2, (T_3B, 1.1, 0, -96)], phase=False, tr=('xf', 0.3),
      ov=S.ovs(ov_two, S.bl(E, [('NU SE POATE JUDECA DIN OCHI', 'bad big', L(3) + 0.2)], T_3B))),
 Shot('pw', T_3B, T_3C, st='fuel', kb=[(T_3B,) + S.KB_PW, (T_3C, 1.05, 0, 46)], tr=('xf', 0.3), fx=[S.fx_fuel()],
      ov=S.ovs(ov_in, S.bl(E, [('UZURA E ÎNĂUNTRU', 'bad big', T_3B + 0.15)], T_3C))),
 Shot('sh2', T_3C, L(4), st='shelf', kb=[(T_3C, 1.1, 0, -96), (L(4), 1.12, 0, -100)], phase=False, tr=('xf', 0.3),
      ov=S.ovs(ov_pair, S.tl(E, [('PE DINAFARĂ, ARATĂ LA FEL', 'big', T_3C + 0.2)], L(4)))),
]

# ------------------------------------------------------------------ fara poveste: nu stii kilometrii, motorina, de ce a ajuns masina la dezmembrat
KB_Z = (1.0, 0, 0)                     # pompa de pe raft in stanga, eticheta de carton in dreapta (placa shz acopera cadrul)
tags = [E.add(P.tag(430, nq=k)) for k in range(4)]
T_Q = [W(4, 'fara') - 0.3, W(4, 'kilometri') - 0.25, W(4, 'motorina') - 0.25, W(4, 'ajuns') - 0.5]
def ov_tag(C):
    te = L(5) + 0.1
    for k in range(4):
        F.spr(C, tags[k], 612, 566, T_Q[k], (T_Q[k + 1] + 0.25) if k < 3 else te)
STORY = [Shot('shz', L(4), L(5), st='shelf', kb=[(L(4),) + KB_Z, (L(5), 1.04, 0, 0)], phase=False, tr=('xf', 0.3),
              ov=S.ovs(ov_tag, S.bl(E, [('O POMPĂ DE LA DEZMEMBRĂRI', 'grey', L(4) + 0.15), ('VINE FĂRĂ POVESTE', 'bad big', W(4, 'fara') - 0.2)], L(5))))]

# ------------------------------------------------------------------ luni de zile pe raft, cu racordurile deschise: praf, umezeala, motorina veche care lasa depuneri
T_5B = W(5, 'inauntru') - 0.15
PORTS = [(175, 895), (270, 852)]       # cele doua racorduri deschise, pe placa shz
DUSTP = [[(-20, 1060), (80, 980), (165, 905)], [(20, 620), (120, 760), (200, 830), (262, 850)], [(-10, 860), (80, 880), (165, 893)]]
l_port = E.lb('RACORD DESCHIS', 'bad')
def ov_ports(C):
    t = C.t; te = T_5B + 0.1; tp = W(5, 'racordurile') - 0.2
    for i, pth in enumerate(DUSTP): S.flowp(C, pth, 8, 90.0, S.DUST2, 7.5, t0=tp + 0.2, seed=21 + i, lat=9.0, dark=0.9)
    for i, p in enumerate(PORTS):
        x, y = S.pk(C, [p])[0]; D.arc(C, x, y, 36, 0, 360, RED, 6, F.pop(t, tp + 0.12 * i, te))
    x, y = S.pk(C, [PORTS[0]])[0]; F.label(C, l_port, ('px', x - 26, y + 26), (44, 1030), tp + 0.1, te)
DRIP = [[(330, 300), (380, 560), (470, 760), (520, 900)]]
l_dust = E.lb('PRAF', 'bad'); l_wet = E.lb('UMEZEALĂ', 'water')
def ov_dirt(C):
    te = L(6) + 0.1
    F.spr(C, l_dust, 250, 560, W(5, 'praf') - 0.15, te, anchor='tc'); F.spr(C, l_wet, 800, 560, W(5, 'umezeala') - 0.15, te, anchor='tc')
SHELFLIFE = [
 Shot('shz', L(5), T_5B, st='shelf', kb=[(L(5), 1.04, 0, 0), (L(5) + 1.2, 1.12, 60, 0), (T_5B, 1.15, 62, 0)], phase=False, tr=None,
      ov=S.ovs(ov_ports, S.bl(E, [('LUNI DE ZILE PE UN RAFT', 'grey', L(5) + 0.15), ('CU RACORDURILE DESCHISE', 'bad big', W(5, 'racordurile') - 0.2)], T_5B))),
 Shot('pc', T_5B, L(6), st='dry', seq=[('lacd', W(5, 'invecheste') - 0.3, W(5, 'depuneri') + 0.4)], kb=[(T_5B, 1.0, 0, 0), (L(6), 1.07, 0, 0)], phase=False, tr=('xf', 0.3),
      fx=[S.fx_grit(('bath_R', 'cam_Ldn', 'cam_Lup'), T_5B - 1.0, n=30, speed=5.0, size=0.85), S.fx_drops(('bath_R', 'cam_Ldn'), W(5, 'umezeala') - 1.6, n=7, speed=5.0, size=1.0)],
      ov=S.ovs(ov_dirt, S.bl(E, [('ÎNĂUNTRU INTRĂ PRAF ȘI UMEZEALĂ', 'bad', T_5B + 0.2), ('MOTORINA VECHE LASĂ DEPUNERI', 'bad big', W(5, 'motorina') - 0.15)], L(6)))),
]

# ------------------------------------------------------------------ daca e deja roasa, face pilitura in masina ta; pilitura ajunge in injectoare, rampa, rezervor
T_6B = W(6, 'iar') - 0.1
FILINGS = [
 Shot('pm', L(6), T_6B, st='damf', kb=[(L(6), 1.04, 0, 0), (T_6B, 1.1, 0, 0)], phase=False, tr=('xf', 0.3),
      fx=[S.fx_dry(L(6), rate=8.0, amp=0.7, size=0.2, speed=30.0), S.fx_flakes(L(6) + 0.1)],
      ov=S.bl(E, [('DACĂ E DEJA ROASĂ', 'bad', L(6) + 0.15), ('FACE PILITURĂ ÎN MAȘINA TA', 'bad big', W(6, 'face') - 0.2)], T_6B)),
 S.sysm(E, T_6B, L(7), hl=[(['pump'], None, T_6B + 0.1), (['inj'], None, W(6, 'injectoare') - 0.2), (['rail'], None, W(6, 'rampa') - 0.2), (['tank'], None, W(6, 'rezervor') - 0.2)],
        flows=[('to_rail', S.METAL2, 12, 170.0, 4.5, T_6B + 0.2), ('rail_inj', S.METAL2, 16, 170.0, 4.5, W(6, 'injectoare') - 0.5),
               ('ret', S.METAL2, 12, 150.0, 4.0, W(6, 'rampa') - 0.2), ('tank', S.METAL2, 20, 150.0, 4.0, W(6, 'rezervor') - 0.4)],
        labs=[('PILITURA PLEACĂ DIN POMPĂ', 'bad', T_6B + 0.2), ('INJECTOARE, RAMPĂ, REZERVOR', 'bad big', W(6, 'injectoare') - 0.2)]),
]

# ------------------------------------------------------------------ cum eviti: nu o monta netestata; testul pe banc costa mult mai putin decat paguba
AVOID = S.avoid(E, 'shz', 'shelf', L(7), L(8), [('NU O MONTA NETESTATĂ', W(7, 'nu') - 0.05, False), ('ÎNTÂI, UN TEST PE BANC', W(7, 'test')), ('MULT MAI IEFTIN DECÂT PAGUBA', W(7, 'mult'))],
                kb=[(L(7), 1.0, 0, 0), (L(8), 1.05, 0, 0)])

# ------------------------------------------------------------------ ce facem noi: testam si pompa adusa de tine, sau o reconditionam pe a ta
T_8B = W(8, 'sau') - 0.12; T_9U = W(9, 'curatam') - 0.12; T_9N = W(9, 'inlocuim') - 0.12; T_9T = W(9, 'si') - 0.1; T_G = W(9, 'garantie') - 0.3
l_wr = E.lb('PIESĂ UZATĂ', 'bad'); l_newp = E.lb('PIESĂ NOUĂ', 'good')
def ov_parts(C):
    te = T_9T + 0.12; t1 = T_9N + 0.15; t2 = W(9, 'piese', 2) - 0.25
    F.lens(C, 'pc', 'dam', 262, 660, 158, t1, te, kb=S.LENS_KB, src=S.WM_OBJ, ring=RED)
    F.lens(C, 'pc', 'dry', 818, 660, 158, t2, te, kb=S.LENS_KB, src=S.WM_OBJ, ring=GREEN)
    F.spr(C, l_wr, 262, 832, t1 + 0.2, te, anchor='tc'); F.spr(C, l_newp, 818, 832, t2 + 0.2, te, anchor='tc')
gar = S.seal(E, '12', 'LUNI GARANȚIE')
def ov_gar(C): F.spr(C, gar, 250, 600, T_G + 0.2, L(E.OUT) + 0.2, anchor='tc')
NOI = [
 S.wk_bench(E, L(8), T_8B, labs=[('TESTĂM ȘI POMPA ADUSĂ DE TINE', 'good big', W(8, 'testam') - 0.15)],
            rows=[('DEBIT', W(8, 'testam') + 0.5), ('PRESIUNE', W(8, 'testam') + 0.95)], t_sheet=W(8, 'testam') + 0.1, kb=[(L(8), 1.0, 0, 0), (T_8B, 1.05, 0, 0)]),
 S.wk(E, 'wm', T_8B, T_9U, [('SAU O RECONDIȚIONĂM PE A TA', 'good big', T_8B + 0.15), ('O DESFACEM', 'good big', W(9, 'desfacem') - 0.12)], st='wkdam'),
 S.wk_usb(E, T_9U, T_9N, labs=[('O CURĂȚĂM CU ULTRASUNETE', 'good big', T_9U + 0.12)], t_dip=W(9, 'ultrasunete') - 0.6),
 S.wk(E, 'wm', T_9N, T_9T, [('PIESELE UZATE: ÎNLOCUITE CU NOI', 'good', T_9N + 0.15)], st='wkdam', seq=[('wk', W(9, 'piese', 2) - 0.2, W(9, 'piese', 2) + 0.4)], ov=ov_parts),
 S.wk_bench(E, T_9T, L(E.OUT), labs=[('O TESTĂM PE BANC', 'good big', T_9T + 0.12), ('FIȘĂ DE TEST ȘI GARANȚIE', 'good big', W(9, 'fisa') - 0.2)],
            rows=[('DEBIT', W(9, 'testam') + 0.2), ('PRESIUNE', W(9, 'testam') + 0.6)], t_sheet=W(9, 'testam') - 0.1, ov=ov_gar),
]

SHOTS = S.opening(E, HOOK) + [SIGNS] + INSIDE + STORY + SHELFLIFE + FILINGS + [AVOID] + NOI + [S.ending(E)]
SPR = E.SPR
