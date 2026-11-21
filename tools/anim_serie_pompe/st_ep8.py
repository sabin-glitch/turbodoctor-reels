# Episodul 8: motorina imbatranita si bacteriile din rezervor
import math
import numpy as np
import pser as S, ifx as F, i2d as D, ikit as K, pdraw as P, fxlib as X
from icomp import Shot
from fxlib import seg, ease
E = S.Ep(8); W, L, LE = E.W, E.L, E.LE; TOTAL = E.TOTAL; GLOB = S.glob(E)
RED = (255, 75, 75); GREEN = (61, 220, 132); WATER = (70, 160, 245); GLINT = (255, 226, 140)
RP, RT = S.mj('reg')
FILM_Y = S.pf_tint(S.LPY, which='hp')
LACC = (0.36, 0.2, 0.07)                          # lacul: maro inchis
SLUDGE = (0.12, 0.11, 0.06)                       # namolul din filtru
OLD_T = S.pf_tint(S.OLD, w=0.75)                  # motorina veche, maronie (pe placile cu motorina galbena)
IFACE = 1162.0                                    # limita apa / motorina pe placa tank:cond

def tint_t(c0, c1, t0, t1, which='hp'):
    """lichidul din placa trece de la culoarea c0 la c1 intre t0 si t1"""
    c0 = np.asarray(c0, np.float32); c1 = np.asarray(c1, np.float32)
    def f(rgba, t):
        u = float(seg(t, t0, t1)); return S.pf_tint(tuple(c0 + (c1 - c0) * u), which=which)(rgba, t)
    return f
COL = X.rnd(81, 44, 4)
def colonies(C, g, a=1.0):
    """colonii de bacterii si ciuperci pe limita dintre apa si motorina (placa tank:cond): pete verzui-negre care cresc (g = 0..1)"""
    if a <= 0.003 or g <= 0.003: return
    z = C.shot.kbat(C.t)[0]
    gi = np.clip(g * 1.7 - COL[:, 3] * 0.7, 0, 1)
    keep = gi > 0.02
    if not keep.any(): return
    xs = 130 + 820 * COL[keep, 0]; ys = IFACE + (COL[keep, 1] - 0.5) * 12
    Q = np.array(S.pk(C, list(zip(xs, ys)))); r = (5.0 + 9.0 * COL[keep, 2]) * gi[keep] * z
    D.dots2(C, Q, r * 1.25, (24, 30, 18), a * 0.9, 0.0)
    D.dots2(C, Q, r, (52, 66, 34), a, 0.0)
    D.dots2(C, Q + np.c_[-0.3 * r, -0.3 * r], r * 0.4, (104, 126, 58), a * 0.8, 0.0)

# ------------------------------------------------------------------ carligul: trec lunile; in rezervor motorina se inchide la culoare si la limita cu apa creste namolul; in pompa, pistonul ramane lipit sus
# (coperta, la 2,25 s: titlul pe trei randuri sus, calendarul si lupa cu pistonul lipit, rezervorul cu namol jos)
MONTHS = ['NOI', 'DEC', 'IAN', 'FEB', 'MAR', 'APR']
CAL = [E.add(P.calendar(m, 260, n_cross=28 if i < len(MONTHS) - 1 else 12)) for i, m in enumerate(MONTHS)]
l_h1 = E.lb('LUNI DE STAT', 'grey big'); l_h2 = E.lb('PISTONUL RĂMÂNE LIPIT', 'bad big')
KB_H = (0.8, 0, 380)
def ov_hook(C):
    t = C.t; te = E.T_S + 0.1
    i = min(len(MONTHS) - 1, int(max(t - 0.1, 0.0) / 0.3))
    F.spr(C, CAL[i], 80, 790, -1.0, te)
    colonies(C, float(seg(t, 0.7, 2.0)))
    F.lens(C, 'ph', 'stuckp', 790, 950, 165, 0.45, te, kb=(0.42, 46, 4), ring=RED, tag='h8')
    F.spr(C, l_h1, 540, 1600, 0.15, 1.3, anchor='tc'); F.spr(C, l_h2, 540, 1600, 1.4, te, anchor='tc')
HOOK = [Shot('tank', 0.0, E.T_S, st='cond', kb=[(0.0,) + KB_H, (E.T_S, 0.83, 0, 376)], phase=False, tr=None, pf=S.pf_tint(S.OLD, 0.3, 1.8, w=0.8), ov=ov_hook)]

# ------------------------------------------------------------------ semnele: la masinile care stau, motorul nu porneste sau porneste si se opreste; filtrul, plin de namol inchis la culoare
T_2B = W(2, 'iar') - 0.1
SIG = S.symptoms(E, 2, [(E.sym('start', 'NU PORNEȘTE', 'După luni de pauză'), 'nu'), (E.sym('stall', 'PORNEȘTE ȘI SE OPREȘTE'), 'porneste', 2)],
                 cam='pw', st='stuckp', kb=S.KB_PW, phase=None, t1=T_2B)
SIG.ov = S.ovs(SIG.ov, S.tl(E, [('LA MAȘINILE CARE STAU', 'big', L(2) + 0.1)], W(2, 'nu') + 0.4))
SIGNS = [SIG,
         Shot('fl', T_2B, L(3), st='ffull', kb=[(T_2B,) + S.KB_FL, (L(3), 0.94, 0, 66)], phase=False, tr=('xf', 0.3),
              pf=S.pfs(OLD_T, S.pf_paper(col=SLUDGE, t0=T_2B + 0.2, t1=W(2, 'namol') + 0.3, w=0.95)),
              ov=S.bl(E, [('FILTRUL, PLIN DE NĂMOL', 'bad big', W(2, 'filtrul') - 0.1), ('ÎNCHIS LA CULOARE', 'bad', W(2, 'inchis') - 0.1)], L(3)))]

# ------------------------------------------------------------------ motorina de azi are pana la 7% biodiesel; biodieselul unge bine, dar imbatraneste: cu aerul si cu caldura se oxideaza
T_3B = W(3, 'biodieselul') - 0.15; T_3C = W(3, 'cu') - 0.15
dsp = E.add(P.dispenser(400, plate='B7'))
b7 = E.add('<div class="stat y" style="padding:12px 34px 16px"><span style="font-size:30px;margin-top:0;color:#b6c2cf">PÂNĂ LA</span><b style="font-size:150px">7%</b><span style="font-size:36px">BIODIESEL</span></div>')
def ov_b7(C):
    F.spr(C, dsp, 60, 560, L(3) + 0.1, T_3B + 0.1)
    F.spr(C, b7, 770, 700, W(3, 'pana') - 0.2, T_3B + 0.1, anchor='tc')
l_air = E.lb('AER', 'grey'); l_heat = E.lb('CĂLDURĂ', 'bad')
def ov_ox(C):
    t = C.t; te = L(4) + 0.1; ta = W(3, 'aerul') - 0.15; th = W(3, 'caldura') - 0.15
    x, y = S.pk(C, [(24, 730)])[0]
    for k in range(3):
        S.arrow2(C, (x + 60 + 70 * k, y - 200), (x + 90 + 70 * k, y - 40), (232, 242, 255), th=8, a=F.pop(t, ta + 0.1 * k, te), prog=float(seg(t, ta + 0.1 * k, ta + 0.5 + 0.1 * k)), head=20)
    F.spr(C, l_air, x + 150, y - 230, ta, te, anchor='bc')
    S.thermo(C, 930, 560, 300, 0.25 + 0.65 * float(ease(seg(t, th, th + 1.2))), F.pop(t, th - 0.1, te))
    F.spr(C, l_heat, 930, 880, th, te, anchor='tc')
OXID = [
 S.plain(E, L(3), T_3B, S.ovs(ov_b7, S.tl(E, [('MOTORINA DE AZI', 'big', L(3) + 0.1)], T_3B))),
 S.film(E, T_3B, T_3C, st='mclean', pf=tint_t(S.LPY, S.OLD, W(3, 'imbatraneste'), W(3, 'imbatraneste') + 1.0), kb=[(T_3B, 1.0, 0, 0), (T_3C, 1.06, 0, 0)],
        flow=((255, 236, 150), None, W(3, 'imbatraneste') + 0.4), sides=('PISTON', 'CILINDRU'),
        labs=[('BIODIESELUL UNGE BINE', 'good big', T_3B + 0.1), ('DAR ÎMBĂTRÂNEȘTE', 'bad big', W(3, 'dar') - 0.1)]),
 S.tank(E, T_3C, L(4), st='dry', kb=[(T_3C, 0.85, 0, 120), (L(4), 0.88, 0, 116)], pf=S.pf_tint(S.OLD, W(3, 'aerul'), W(3, 'oxideaza') + 0.4, w=0.8), ov=ov_ox,
        labs=[('CU AERUL ȘI CU CĂLDURA', 'bad', T_3C + 0.1), ('SE OXIDEAZĂ', 'bad big', W(3, 'oxideaza') - 0.15)], y=384),
]

# ------------------------------------------------------------------ din oxidare: acizi, care ataca metalul, si rasini lipicioase, care se depun ca un lac pe piesele calde
T_4P = W(4, 'piesele') - 0.2
LACQ = [
 S.film(E, L(4), T_4P, st='mclean', seq=[('mrust1', W(4, 'ataca') - 0.2, W(4, 'metalul') + 0.4), ('mlac1', W(4, 'depun') - 0.2, W(4, 'depun') + 0.4), ('mlac2', W(4, 'lac') - 0.15, W(4, 'lac') + 0.45)],
        pf=S.pf_tint(S.OLD, which='hp', w=0.85), kb=[(L(4), 1.04, 0, 0), (T_4P, 1.12, 0, 0)], sides=('PISTON', 'CILINDRU'),
        labs=[('DIN OXIDARE: ACIZI', 'bad big', L(4) + 0.1), ('CARE ATACĂ METALUL', 'bad big', W(4, 'care') - 0.1), ('ȘI RĂȘINI LIPICIOASE', 'bad big', W(4, 'si') - 0.1),
              ('SE DEPUN CA UN LAC', 'bad big', W(4, 'se') - 0.1)]),
 S.pump(E, 'pw', T_4P, L(5), st='stuckp', kb=[(T_4P, 1.0, 0, 46), (L(5), 1.06, 0, 30)], fx=[], labs=[('PE PIESELE CALDE', 'bad big', T_4P + 0.12)]),
]

# ------------------------------------------------------------------ lacul umple jocurile de cativa microni; pistoanele si regulatorul se misca tot mai greu si pot ramane intepenite
T_5B = W(5, 'pistoanele') - 0.15; T_5C = W(5, 'regulatorul') - 0.15; T_5D = W(5, 'pot') - 0.15; T_STOP = W(5, 'si', 2) - 0.05
LR = X.rnd(23, 60, 3)
GX0, GX1 = 526.0, 553.0                            # peretii jocului pe placa micro (banda de motorina dintre piston si cilindru)
def ov_fill(C):
    """lacul creste din ambii pereti ai jocului spre mijloc, pana ramane doar un fir de motorina; licaririle se rarefiaza"""
    t = C.t; z = C.shot.kbat(t)[0]; u = float(ease(seg(t, W(5, 'umple') - 0.3, W(5, 'microni') + 0.4))); wl = 11.5 * u
    S.flowp(C, [(539.5, -40), (539.5, 1960)], 14, 200.0 * (1.0 - 0.75 * u), GLINT, 3.2, lat=max(1.5, 11.0 - wl), seed=6, glow=0.3, a=0.85 * (1.0 - 0.7 * u))
    if wl < 0.3: return
    for wall, sg in ((GX0, 1.0), (GX1, -1.0)):
        (xa, ya), (xb, yb) = S.pk(C, [(wall + sg * wl / 2.0, -60), (wall + sg * wl / 2.0, 1980)])
        D.line2(C, [(xa, ya), (xb, yb)], (122, 68, 24), wl * z, 1.0)
        (xe, ye), (xf, yf) = S.pk(C, [(wall + sg * wl, -60), (wall + sg * wl, 1980)])
        D.line2(C, [(xe, ye), (xf, yf)], (70, 38, 12), 3.0, 0.9)
    Q = []; R = []
    for i in range(60):
        wall, sg = (GX0, 1.0) if i % 2 == 0 else (GX1, -1.0)
        Q.append(S.pk(C, [(wall + sg * wl * LR[i, 0], -40 + 2000 * LR[i, 1])])[0]); R.append((1.2 + 1.8 * LR[i, 2]) * z)
    D.dots2(C, np.array(Q), np.array(R), (60, 32, 10), 0.8, 0.0)
l_pis = E.lb('PISTON', 'grey'); l_cil = E.lb('CILINDRU', 'grey'); hid_m = E.lb('VEDERE MĂRITĂ', 'grey')
def ov_mic(C):
    te = T_5B + 0.1
    F.spr(C, hid_m, 540, 372, L(5) + 0.05, te, anchor='tc')
    F.spr(C, l_pis, 236, 700, L(5) + 0.3, te, anchor='tc'); F.spr(C, l_cil, 844, 700, L(5) + 0.3, te, anchor='tc')
KB_PH = (1.2, 100, -180)
l_gol = E.lb('CAMA SE ÎNVÂRTE ÎN GOL', 'grey')
def ov_ph(C):
    t = C.t; te = T_5C + 0.1; x, y = S.pk(C, [(430, 1232)])[0]; z = C.shot.kbat(t)[0]
    D.arc(C, x, y, 64 * z / 1.2, 0, 360, RED, 6, F.pop(t, T_5B + 0.4, te) * (0.75 + 0.25 * math.sin(t * 7.0)))
    F.label(C, l_gol, ('px', x + 70, y), (1040, 1000), T_5B + 0.5, te, anchor='tr')
def ph_slow(t):
    u = min(max(t - T_5C, 0.0), T_STOP - T_5C); D_ = T_STOP - T_5C; return 0.2 + 1.1 * (u - u * u / (2 * D_))
def ov_reg(C):
    t = C.t; k = 1.0 - float(seg(t, T_5C, T_STOP))
    for i, nm in enumerate(('in_R', 'in_L')):
        S.flow3(C, RT[nm], 10, 40.0 + 120.0 * k, GLINT, 4.6, a=0.3 + 0.7 * k, seed=3 + i, glow=0.5, lat=3.0)
    if t > T_STOP - 0.1:
        x, y = S.p3(C, [RP['gap']])[0]
        D.arc(C, x, y, 58, 0, 360, RED, 6, F.pop(t, T_STOP - 0.1, T_5D + 0.1))
P_PW = (530, 640)
def ov_stuck(C):
    t = C.t; te = L(6) + 0.1; x, y = S.pk(C, [P_PW])[0]
    D.arc(C, x, y, 118, 0, 360, RED, 7, F.pop(t, W(5, 'ramane') - 0.1, te))
    S.sparks2(C, x, y + 110, t, W(5, 'ramane'), W(5, 'ramane') + 0.5, n=10, L=26.0, R=30.0)
STICK = [
 Shot('micro', L(5), T_5B, st='mclean', pf=FILM_Y, kb=[(L(5), 2.2, 0, 0), (T_5B, 2.3, 0, 0)], phase=False, tr=('xf', 0.3),
      ov=S.ovs(ov_fill, ov_mic, S.bl(E, [('LACUL UMPLE JOCURILE', 'bad big', L(5) + 0.1), ('DE CÂȚIVA MICRONI', 'bad', W(5, 'de') - 0.1)], T_5B))),
 Shot('ph', T_5B, T_5C, st='stuckp', kb=[(T_5B,) + KB_PH, (T_5C, 1.24, 100, -186)], tr=('xf', 0.3), pf=OLD_T,
      ov=S.ovs(ov_ph, S.bl(E, [('PISTOANELE POMPEI', 'bad big', T_5B + 0.1)], T_5C))),
 Shot('rgz', T_5C, T_5D, st='regmove', kb=[(T_5C, 0.58, 0, -40), (T_5D, 0.61, 0, -43)], tr=('xf', 0.3), phase=ph_slow,
      ov=S.ovs(ov_reg, S.bl(E, [('ȘI REGULATORUL DE DEBIT', 'bad', T_5C + 0.1), ('SE MIȘCĂ TOT MAI GREU', 'bad big', W(5, 'misca') - 0.15)], T_5D))),
 S.pump(E, 'pw', T_5D, L(6), st='stuckp', kb=[(T_5D, 1.0, 0, 46), (L(6), 1.05, 0, 34)], fx=[], ov=ov_stuck, shake=S.shake_at(W(5, 'ramane'), 0.7, 5.0),
        labs=[('ȘI POT RĂMÂNE ÎNȚEPENITE', 'bad big', T_5D + 0.1)]),
]

# ------------------------------------------------------------------ apa in rezervor: la limita dintre apa si motorina cresc bacterii si ciuperci; namolul lor infunda filtrul si lasa pompa fara motorina
T_6B = W(6, 'ele') - 0.15; T_6C = W(6, 'lasa') - 0.15
T_Z0 = W(6, 'limita') - 0.3; T_Z1 = W(6, 'limita') + 0.9
def ov_bio(C):
    t = C.t; z = C.shot.kbat(t)[0]
    aw = F.pop(t, W(6, 'apa') - 0.2, T_Z0 + 0.4)
    if aw > 0.003:
        Q = S.pk(C, [(110, 1173), (972, 1173)]); D.line2(C, Q, WATER, 10 * z, aw * (0.6 + 0.4 * math.sin(t * 7.0)))
    colonies(C, float(seg(t, W(6, 'cresc') - 0.2, W(6, 'ciuperci') + 0.4)))
BIO = [
 Shot('tank', L(6), T_6B, st='cond', kb=[(L(6), 0.85, 0, 120), (T_Z0, 0.86, 0, 118), (T_Z1, 1.7, 0, -216), (T_6B, 1.76, 0, -230)], phase=False, tr=('xf', 0.3), pf=OLD_T,
      ov=S.ovs(ov_bio, S.tl(E, [('DACĂ S-A ADUNAT ȘI APĂ', 'big', L(6) + 0.1), ('LA LIMITA DINTRE APĂ ȘI MOTORINĂ', '', W(6, 'la') - 0.1),
                                ('CRESC BACTERII ȘI CIUPERCI', 'bad big', W(6, 'cresc') - 0.15)], T_6B))),
 Shot('fl', T_6B, T_6C, st='ffull', kb=[(T_6B,) + S.KB_FL, (T_6C, 0.95, 0, 66)], phase=False, tr=('xf', 0.3),
      pf=S.pfs(OLD_T, S.pf_paper(col=SLUDGE, t0=T_6B + 0.2, t1=W(6, 'filtrul') + 0.4, w=0.95)),
      ov=S.bl(E, [('ELE FAC UN NĂMOL', 'bad big', T_6B + 0.1), ('CARE ÎNFUNDĂ FILTRUL', 'bad big', W(6, 'care') - 0.1)], T_6C)),
 S.pump(E, 'pw', T_6C, L(7), st='dry', fx=[S.fx_dry(T_6C + 0.3)], labs=[('ȘI LASĂ POMPA FĂRĂ MOTORINĂ', 'bad big', T_6C + 0.1)]),
]

# ------------------------------------------------------------------ cum eviti: masina care sta mult se lasa cu rezervorul plin, cu motorina proaspata; la repunerea in mers, filtru nou
T_7B = W(7, 'iar') - 0.1
ITEMS = [('REZERVORUL PLIN', W(7, 'rezervorul')), ('MOTORINĂ PROASPĂTĂ', W(7, 'proaspata')), ('FILTRU NOU LA REPUNEREA ÎN MERS', W(7, 'repunerea'))]
AVOID = [S.avoid(E, 'tank', 'dry', L(7), T_7B, ITEMS, kb=[(L(7), 0.85, 0, -200), (T_7B, 0.87, 0, -204)],
                 ov=S.ovs(S.tank_nozzle(E, W(7, 'rezervorul') - 0.3, T_7B + 0.1, col='#3b4652', dark='#1a2129'), S.tank_in(W(7, 'rezervorul'), T_7B, col=S.LP2))),
         S.avoid(E, 'fl', 'ffull', T_7B, L(8), ITEMS, kb=[(T_7B, 0.55, 0, -170), (L(8), 0.57, 0, -174)])]

# ------------------------------------------------------------------ ce facem noi: pompa intepenita de depuneri nu e neaparat pierduta; o desfacem, ultrasunete, garnituri si piese corodate noi;
# o testam pe banc; la fel procedam cu injectoarele, care sufera de aceleasi depuneri
T_8B = W(8, 'desfacem') - 0.4; T_8C = W(8, 'schimbam') - 0.15; T_9B = W(9, 'la') - 0.15
st_set = E.add(P.seals(480))
def ov_set(C): F.spr(C, st_set, 780, 440, T_8C + 0.2, L(9) + 0.12, anchor='tc')
NOI = [
 S.wk(E, 'wm', L(8), T_8B, [('O POMPĂ ÎNȚEPENITĂ DE DEPUNERI', 'grey', W(8, 'pompa') - 0.15), ('NU E NEAPĂRAT PIERDUTĂ', 'good big', W(8, 'nu') - 0.1)], st='wkdam'),
 S.wk_usb(E, T_8B, T_8C, labs=[('O DESFACEM', 'good big', T_8B + 0.1), ('CURĂȚĂM PIESELE CU ULTRASUNETE', 'good', W(8, 'curatam') - 0.1)], t_dip=W(8, 'curatam') - 0.3),
 S.wk(E, 'wm', T_8C, L(9), [('SCHIMBĂM GARNITURILE', 'good big', T_8C + 0.12), ('ȘI PIESELE CORODATE', 'good', W(8, 'piesele', 2) - 0.12)], st='wkdam',
      seq=[('wk', W(8, 'piesele', 2) - 0.1, W(8, 'piesele', 2) + 0.5)], ov=ov_set),
 S.wk_bench(E, L(9), T_9B, labs=[('O TESTĂM PE BANC', 'good big', W(9, 'testam') - 0.15)], rows=[('DEBIT', W(9, 'testam') + 0.2), ('PRESIUNE', W(9, 'banc'))],
            t_sheet=W(9, 'testam') - 0.1),
 S.wk_inj(E, T_9B, L(E.OUT), labs=[('LA FEL PROCEDĂM CU INJECTOARELE', 'good big', T_9B + 0.12), ('CARE SUFERĂ DE ACELEAȘI DEPUNERI', 'grey', W(9, 'sufera') - 0.15)]),
]

SHOTS = S.opening(E, HOOK) + SIGNS + OXID + LACQ + STICK + BIO + AVOID + NOI + [S.ending(E)]
SPR = E.SPR
