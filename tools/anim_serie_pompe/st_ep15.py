# Episodul 15: greselile de montaj
import math
import numpy as np
import pser as S, ifx as F, i2d as D, ikit as K, pdraw as P, fxlib as X
from icomp import Shot
from fxlib import seg, ease
E = S.Ep(15); W, L, LE = E.W, E.L, E.LE; TOTAL = E.TOTAL; GLOB = S.glob(E)
RED = (255, 75, 75); GREEN = (61, 220, 132)
FILM_Y = S.pf_tint(S.LPY, which='hp')
PX_CROP = (60, 100, 1060, 1400)                     # pompa intreaga (placa px:full) ca sprite
PORTS = [(790, 425), (522, 238)]                    # racordul lateral si cel de sus, pe placa px:full

def px_at(cx, cy, sc, p):
    """un punct de pe placa px:full -> cadru, pentru sprite-ul centrat in (cx, cy), la scara sc"""
    x0, y0, x1, y1 = PX_CROP
    return (cx + (p[0] - (x0 + x1) / 2.0) * sc, cy + (p[1] - (y0 + y1) / 2.0) * sc)
DU = X.rnd(13, 24, 4)
def dust_fall(C, targets, t0, a=1.0, n=12, y_top=440, per=1.1, r=5.0):
    """fire de praf care cad, unul dupa altul, in racordurile deschise"""
    t = C.t
    if t < t0 or a <= 0.003: return
    for i in range(n):
        tx, ty = targets[i % len(targets)]
        ph = ((t - t0) / per + DU[i, 0]) % 1.0
        x = tx + (DU[i, 1] - 0.5) * 120 * (1.0 - ph); y = y_top + (ty - y_top) * ph * ph
        S.grain2(C, x, y, r * (0.7 + 0.6 * DU[i, 2]), a * min(1.0, ph * 6.0) * (1.0 - float(seg(ph, 0.92, 1.0))), seed=i)
def num_hd(n, text, t0, t1): return S.hd(E, '%d. %s' % (n, text), t0, t1, 'bad big')

# ------------------------------------------------------------------ carligul: pompa noua, cu racordurile deschise, in care cade praful; apoi pornita fara motorina
# (coperta, la 1,85 s: titlul sus, pompa in sectiune, goala, cu scantei)
T_HB = 1.25; SC_H = 0.62; CX_H, CY_H = 540, 1150
l_ha = E.lb('POMPĂ NOUĂ, RACORDURI DESCHISE', 'grey big'); l_hb = E.lb('PORNITĂ FĂRĂ MOTORINĂ', 'bad big')
def ov_hookA(C):
    t = C.t; te = T_HB + 0.3; a = F.pop(t, -1.0, te)
    S.plate_spr(C, 'px', 'full', CX_H, CY_H, SC_H, a, crop=PX_CROP, tag='h15')
    dust_fall(C, [px_at(CX_H, CY_H, SC_H, p) for p in PORTS], -0.6, a, n=14, y_top=640, per=0.9, r=7.5)
    F.spr(C, l_ha, 540, 1640, 0.1, te, anchor='tc')
def ov_hookB(C):
    F.spr(C, l_hb, 540, 1640, T_HB - 0.05, E.T_S + 0.1, anchor='tc')
HOOK = [S.plain(E, 0.0, T_HB, ov_hookA, tr=None),
        Shot('pw', T_HB, E.T_S, st='dry', kb=[(T_HB, 0.85, 0, 200), (E.T_S, 0.88, 0, 196)], tr=('xf', 0.25), fx=[S.fx_dry(T_HB - 0.4)], ov=ov_hookB)]

# ------------------------------------------------------------------ semnele, imediat dupa montare: porneste greu sau deloc, pierde motorina pe la racorduri, erorile de presiune revin in cateva zile
SIG = S.symptoms(E, 2, [(E.sym('start', 'PORNEȘTE GREU SAU DELOC'), 'porneste'), (E.sym('drop', 'PIERDE MOTORINĂ', 'Pe la racorduri', cls='warn'), 'pierde'),
                        (E.sym('ecu', 'ERORILE DE PRESIUNE REVIN', 'În câteva zile'), 'erorile')], cam='px', st='full', kb=(0.9, 0, 40))
SIG.ov = S.ovs(SIG.ov, S.tl(E, [('IMEDIAT DUPĂ MONTARE', 'big', L(2) + 0.1)], W(2, 'porneste') + 0.4))
SIGNS = [SIG]

# ------------------------------------------------------------------ 1. pompa pornita goala; producatorii: nu are voie sa mearga fara motorina; instalatia se umple si se aeriseste inainte de prima pornire
T_3B = W(3, 'producatorii') - 0.15; T_3C = W(3, 'instalatia') - 0.15
stp = E.stop('NU ARE VOIE SĂ MEARGĂ FĂRĂ MOTORINĂ', 'Scriu producătorii pompelor')
def ov_stop(C): F.spr(C, stp, 540, 880, T_3B + 0.15, T_3C + 0.1, anchor='tc')
DRY = [
 S.pump(E, 'pc', L(3), T_3B, st='dry', fx=[S.fx_dry(L(3) + 0.2)], ov=num_hd(1, 'POMPA PORNITĂ GOALĂ', L(3) + 0.1, T_3C + 0.1),
        labs=[('MERGE FĂRĂ MOTORINĂ', 'bad big', W(3, 'pornita') - 0.1)]),
 Shot('pw', T_3B, T_3C, st='dry', kb=[(T_3B,) + S.KB_PW, (T_3C, 1.04, 0, 40)], tr=('xf', 0.3), dim=lambda t: 0.35 * F.pop(t, T_3B, T_3C + 0.2),
      ov=S.ovs(num_hd(1, 'POMPA PORNITĂ GOALĂ', L(3) + 0.1, T_3C + 0.1), ov_stop)),
 S.sysm(E, T_3C, L(4), hl=[(['lp', 'filter'], S.YEL_HL, W(3, 'umple') - 0.2), (['pump'], S.GREEN_HL, W(3, 'inainte') - 0.2)],
        flows=[('lp', S.AIR2, 8, 170.0, 7.0, T_3C + 0.1, W(3, 'aeriseste') + 0.5, True), ('lp', S.LP2, 14, 210.0, 4.5, W(3, 'umple') - 0.1)],
        labs=[('INSTALAȚIA SE UMPLE ȘI SE AERISEȘTE', 'good', T_3C + 0.1), ('ÎNAINTE DE PRIMA PORNIRE', 'good big', W(3, 'inainte') - 0.15)]),
]

# ------------------------------------------------------------------ 2. murdaria: pompa lasata cu racordurile deschise pe un banc prafuit; particule mai mici de 0,1 mm pot da defecte
T_4B = W(4, 'particule') - 0.15; SC_B = 0.52; CX_B, CY_B = 540, 790
BENCH = E.add('<svg width="900" height="70" viewBox="0 0 900 70"><rect x="0" y="8" width="900" height="34" rx="8" fill="#6b5640" stroke="#9c8162" stroke-width="4"/>'
              '<rect x="40" y="42" width="40" height="28" fill="#3d3226"/><rect x="820" y="42" width="40" height="28" fill="#3d3226"/></svg>')
BD = X.rnd(57, 40, 3)
def ov_bench(C):
    t = C.t; te = T_4B + 0.1; a = F.pop(t, L(4) - 0.1, te)
    F.spr(C, BENCH, 90, 1120, L(4) - 0.1, te)
    S.plate_spr(C, 'px', 'full', CX_B, CY_B, SC_B, a, crop=PX_CROP, tag='b15')
    for i in range(40):                                                      # praful de pe banc
        S.grain2(C, 110 + 860 * BD[i, 0], 1126 + 4 * BD[i, 1], 2.5 + 3.5 * BD[i, 2], a * 0.9, seed=40 + i)
    dust_fall(C, [px_at(CX_B, CY_B, SC_B, p) for p in PORTS], W(4, 'racordurile') - 0.6, a, n=12, y_top=440, per=1.0, r=6.5)
    for p in PORTS:
        x, y = px_at(CX_B, CY_B, SC_B, p); D.arc(C, x, y, 34, 0, 360, RED, 5, F.pop(t, W(4, 'racordurile') - 0.1, te) * (0.75 + 0.25 * math.sin(t * 7.0)))
l_pis = E.lb('PISTON', 'grey'); l_cil = E.lb('CILINDRU', 'grey')
GX0, GX1 = 526.0, 553.0                             # peretii jocului pe placa micro
GLINT = (255, 226, 160); GR = X.rnd(71, 10, 3)
T_HITS = (W(4, 'pot') + 0.1, W(4, 'defecte') - 0.1, W(4, 'defecte') + 0.3)
def ov_grit(C):
    """motorina licare prin joc; din T_4B intra granule de praf, se freaca de pereti, iar la fiecare lovitura sar scantei"""
    t = C.t; z = C.shot.kbat(t)[0]
    S.flowp(C, [(539.5, -40), (539.5, 1960)], 14, 200.0, GLINT, 3.2, lat=9.0, seed=6, glow=0.3, a=0.8)
    if t < T_4B + 0.1: return
    for i in range(10):
        y = -60 + ((t - T_4B) * (150.0 + 60.0 * GR[i, 0]) + 2040 * GR[i, 1]) % 2040
        x = 539.5 + (GR[i, 2] - 0.5) * 9.0 + 3.0 * math.sin(t * 5.0 + i)
        X_, Y_ = S.pk(C, [(x, y)])[0]
        S.grain2(C, X_, Y_, 8.5 * z, F.pop(t, T_4B + 0.1 + 0.08 * i, 1e9), seed=30 + i)
    for k, th in enumerate(T_HITS):
        wall = GX0 if k % 2 == 0 else GX1; yh = 700 + 260 * k
        X_, Y_ = S.pk(C, [(wall, yh)])[0]
        S.sparks2(C, X_, Y_, t, th, th + 0.45, n=14, L=34.0, R=26.0, seed=50 + k)
def ov_sides(C):
    F.spr(C, l_pis, 236, 700, T_4B + 0.3, L(5) + 0.1, anchor='tc'); F.spr(C, l_cil, 844, 700, T_4B + 0.3, L(5) + 0.1, anchor='tc')
DIRT = [
 S.plain(E, L(4), T_4B, S.ovs(ov_bench, num_hd(2, 'MURDĂRIA', L(4) + 0.1, L(5) + 0.1),
                             S.bl(E, [('POMPĂ CU RACORDURILE DESCHISE', 'bad', W(4, 'pompa') - 0.1), ('PE UN BANC PRĂFUIT', 'bad big', W(4, 'banc') - 0.1)], T_4B))),
 Shot('micro', T_4B, L(5), st='mclean', seq=[('mscored', W(4, 'defecte') - 0.1, W(4, 'defecte') + 0.5)], pf=FILM_Y, kb=[(T_4B, 1.5, 0, 0), (L(5), 1.6, 0, 0)], phase=False, tr=('xf', 0.3),
      ov=S.ovs(ov_grit, num_hd(2, 'MURDĂRIA', L(4) + 0.1, L(5) + 0.1), ov_sides,
               S.bl(E, [('PARTICULE MAI MICI DE 0,1 MM', 'bad big', T_4B + 0.1), ('POT DA DEFECTE', 'bad big', W(4, 'pot') - 0.1)], L(5)))),
]

# ------------------------------------------------------------------ 3. conductele de inalta presiune refolosite: capatul deformat etanseaza mai greu; din filet se pot desprinde aschii fine
T_5B = W(5, 'capatul') - 0.15; T_5C = W(5, 'iar') - 0.15
KB_HZ = (1.1, -54, -80)
LEAK_L = [(500, 1102), (470, 1070), (440, 1030), (410, 985), (380, 940), (330, 890), (270, 875)]
LEAK_R = [(580, 1102), (612, 1070), (642, 1030), (672, 985), (702, 940), (760, 890), (830, 875)]
CHIP_L = [(262, 872), (330, 890), (380, 940), (410, 985), (440, 1030), (470, 1070), (505, 1104), (532, 1150), (540, 1230), (540, 1980)]   # din filet, pe langa con, in conducta
CHIP_R = [(1080 - x, y) for (x, y) in CHIP_L]
def hp_down(C, n=14, a=0.7, x=540): S.flowp(C, [(x, -40), (x, 1980)], n, 260.0, S.HP2, 4.5, lat=28.0, seed=4, glow=0.45, a=a)
def ov_hc(C): hp_down(C, n=16, a=0.75, x=537)
def ov_seat(C):
    t = C.t; te = T_5C + 0.1
    hp_down(C)
    for k, pth in enumerate((LEAK_L, LEAK_R)):
        S.flowp(C, pth, 8, 70.0, S.HP2, 6.5, t0=W(5, 'etanseaza') - 0.2, seed=11 + k, glow=0.7, a=1.0)
    for (x, y) in ((438, 1035), (640, 1035)):
        X_, Y_ = S.pk(C, [(x, y)])[0]; D.arc(C, X_, Y_, 52, 0, 360, RED, 5, F.pop(t, W(5, 'deformat') + 0.2, te) * (0.75 + 0.25 * math.sin(t * 7.0)))
def ov_chips(C):
    t = C.t
    hp_down(C)
    for k, pth in enumerate((LEAK_L, LEAK_R)): S.flowp(C, pth, 8, 70.0, S.HP2, 6.5, seed=11 + k, glow=0.7, a=1.0)
    for k, pth in enumerate((CHIP_L, CHIP_R)): S.flowp(C, pth, 9, 150.0, S.METAL2, 7.5, t0=T_5C + 0.2, seed=21 + k, glow=0.3, dark=1.0, jit=0.1)
PIPES = [
 Shot('hc', L(5), T_5B, st='hok', kb=[(L(5), 0.8, 0, -80), (T_5B, 0.84, 0, -90)], phase=False, tr=('xf', 0.3),
      ov=S.ovs(ov_hc, num_hd(3, 'CONDUCTELE REFOLOSITE', L(5) + 0.1, L(6) + 0.1),
               S.bl(E, [('CONDUCTE DE ÎNALTĂ PRESIUNE', 'hp', L(5) + 0.6), ('REFOLOSITE', 'bad big', W(5, 'refolosite') - 0.1)], T_5B))),
 Shot('hcz', T_5B, T_5C, st='hok', seq=[('hbad', W(5, 'deformat') - 0.2, W(5, 'deformat') + 0.4)], kb=[(T_5B,) + KB_HZ, (T_5C, 1.14, -54, -84)], phase=False, tr=('xf', 0.3),
      ov=S.ovs(ov_seat, num_hd(3, 'CONDUCTELE REFOLOSITE', L(5) + 0.1, L(6) + 0.1),
               S.bl(E, [('CAPĂTUL S-A DEFORMAT', 'bad big', T_5B + 0.1), ('LA PRIMA STRÂNGERE', 'bad', W(5, 'la') - 0.1), ('ETANȘEAZĂ MAI GREU', 'bad big', W(5, 'etanseaza') - 0.1)], T_5C))),
 Shot('hcz', T_5C, L(6), st='hbad', kb=[(T_5C, 1.14, -54, -84), (L(6), 1.18, -54, -90)], phase=False, tr=None,
      ov=S.ovs(ov_chips, num_hd(3, 'CONDUCTELE REFOLOSITE', L(5) + 0.1, L(6) + 0.1), S.bl(E, [('AȘCHII FINE DIN FILET', 'bad big', W(5, 'filet') - 0.15)], L(6)))),
]

# ------------------------------------------------------------------ 4. calculatorul: dupa o pompa sau un regulator nou, multe masini cer adaptare cu testerul (desen ilustrativ)
NT = 14
TST = [E.add(P.tester(i / (NT - 1.0), 440, done=(i == NT - 1))) for i in range(NT)]
T_AD0 = W(6, 'multe') - 0.1; T_AD1 = L(7) - 0.5
def ov_tester(C):
    t = C.t; te = L(7) + 0.1; i = int(round((NT - 1) * float(seg(t, T_AD0, T_AD1))))
    F.spr(C, TST[i], 540, 446, L(6) + 0.15, te, anchor='tc')
    D.text(C, 'DESEN ILUSTRATIV', 540, 1138, 20, (125, 136, 148), F.pop(t, L(6) + 0.3, te), font='mont7', anchor='mm', shadow=False)
ECU = [S.plain(E, L(6), L(7), S.ovs(ov_tester, num_hd(4, 'ADAPTAREA ÎN CALCULATOR', L(6) + 0.1, L(7) + 0.1),
                                    S.bl(E, [('DUPĂ O POMPĂ SAU UN REGULATOR NOU', 'grey', W(6, 'dupa') - 0.1), ('MULTE MAȘINI CER ADAPTARE', 'bad big', W(6, 'multe') - 0.1),
                                             ('CU TESTERUL', 'bad big', W(6, 'testerul') - 0.15)], L(7))))]

# ------------------------------------------------------------------ cum eviti: montaj curat, dopuri pe racorduri pana in ultima clipa, procedura de umplere a masinii
KB_AV = (0.48, 0, -150)
def ov_caps(C):
    t = C.t; z = C.shot.kbat(t)[0]; a = F.pop(t, W(7, 'dopuri') - 0.1, L(8) + 0.1)
    if a <= 0.003: return
    for (x, y), dx in zip(PORTS, (14, 0)):
        X_, Y_ = S.pk(C, [(x + dx, y - (8 if dx == 0 else 0))])[0]
        D.dots2(C, np.array([[X_, Y_]]), 60 * z, (255, 196, 30), a, 0.0)
        D.dots2(C, np.array([[X_ - 14 * z, Y_ - 14 * z]]), 18 * z, (255, 236, 150), a * 0.8, 0.0)
        D.arc(C, X_, Y_, 60 * z, 0, 360, (150, 100, 10), 4, a)
AVOID = [S.avoid(E, 'px', 'full', L(7), L(8), [('MONTAJ CURAT', W(7, 'monteaza')), ('DOPURI PE RACORDURI', W(7, 'dopuri')), ('PROCEDURA DE UMPLERE A MAȘINII', W(7, 'procedura'))],
                 kb=[(L(7),) + KB_AV, (L(8), 0.5, 0, -154)], ov=ov_caps)]

# ------------------------------------------------------------------ ce facem noi: fiecare pompa reconditionata pleaca testata pe banc, cu fisa de test, cu piesele inlocuite si cu 12 luni garantie;
# o pompa montata in alta parte care nu face presiune: o verificam pe banc si afli daca problema e la pompa sau in alta parte
T_8B = W(8, 'piesele') - 0.3; T_9B = W(9, 'verificam') - 0.3
tr_old = E.add(P.tray('PIESELE ÎNLOCUITE', '#b6c2cf', bad=True)); gar = S.seal(E, '12', 'LUNI GARANȚIE')
def ov_parts(C):
    F.spr(C, tr_old, 50, 462, T_8B + 0.15, L(9) + 0.12)
    F.spr(C, gar, 800, 456, W(8, 'garantie') - 0.25, L(9) + 0.12, anchor='tc')
hid = E.lb('CE FACEM NOI LA TURBO DOCTOR', 'big'); l_rp = E.lb('PRESIUNE ÎN RAMPĂ', 'grey')
def ov_other(C):
    t = C.t; te = T_9B + 0.1; a = F.pop(t, L(9) - 0.1, te)
    F.spr(C, hid, 540, 372, E.T_NOI - 0.05, L(E.OUT) + 0.2, anchor='tc')
    S.plate_spr(C, 'px', 'full', 300, 790, 0.46, a, crop=PX_CROP, tag='o15')
    v = 0.62 - 0.45 * float(ease(seg(t, W(9, 'nu') - 0.2, W(9, 'nu') + 0.8)))
    S.gauge(C, 800, 800, 140, v, F.pop(t, L(9) + 0.2, te), red=(0.0, 0.25))
    F.spr(C, l_rp, 800, 970, L(9) + 0.3, te, anchor='tc')
    D.arc(C, 800, 800, 168, 0, 360, RED, 6, F.pop(t, W(9, 'nu') - 0.1, te))
NOI = [
 S.wk_bench(E, L(8), T_8B, labs=[('FIECARE POMPĂ RECONDIȚIONATĂ', 'good', W(8, 'fiecare') - 0.1), ('TESTATĂ PE BANC', 'good big', W(8, 'testata') - 0.1)],
            rows=[('DEBIT', W(8, 'testata')), ('PRESIUNE', W(8, 'banc'))], t_sheet=W(8, 'fisa') - 0.6),
 S.wk(E, 'wm', T_8B, L(9), [('CU PIESELE ÎNLOCUITE', 'good big', T_8B + 0.12), ('ȘI 12 LUNI GARANȚIE', 'good big', W(8, 'garantie') - 0.15)], ov=ov_parts),
 S.plain(E, L(9), T_9B, S.ovs(ov_other, S.bl(E, [('O POMPĂ MONTATĂ ÎN ALTĂ PARTE', 'grey', W(9, 'pompa') - 0.15), ('NU FACE PRESIUNE', 'bad big', W(9, 'nu') - 0.1)], T_9B))),
 S.wk_bench(E, T_9B, L(E.OUT), labs=[('O VERIFICĂM PE BANC', 'good big', T_9B + 0.12), ('AFLI UNDE E PROBLEMA', 'good big', W(9, 'afli') - 0.1)],
            rows=[('PRESIUNE', W(9, 'banc') - 0.1), ('DEBIT', W(9, 'banc') + 0.2)], t_sheet=W(9, 'banc') - 0.5),
]

SHOTS = S.opening(E, HOOK) + SIGNS + DRY + DIRT + PIPES + ECU + AVOID + NOI + [S.ending(E)]
SPR = E.SPR
