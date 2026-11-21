# Episodul 11: aerul tras pe la racorduri
import math
import numpy as np
import pser as S, ifx as F, i2d as D, ikit as K, pdraw as P, fxlib as X
from icomp import Shot
from fxlib import seg, ease
E = S.Ep(11); W, L, LE = E.W, E.L, E.LE; TOTAL = E.TOTAL; GLOB = S.glob(E)
RED = (255, 75, 75); GREEN = (61, 220, 132); AIR = (235, 244, 255); YEL = (255, 210, 31)
PQ, PA = S.mj('qc')                                   # cupla rapida: puncte si trasee (mm); motorina urca din furtun spre pompa
FILM_Y = S.pf_tint(S.LPY, which='hp')

def air_in(C, n=7, sp=120.0, r=9.0, t0=None, a=1.0):
    """bulele de aer care intra pe la gura cuplei, coboara pe langa inelele crapate si urca apoi cu motorina spre pompa"""
    for k, nm in enumerate(('air_R', 'air_L')):
        S.flow3(C, PA[nm], n, sp, AIR, r, t0=t0, a=a, seed=21 + k, ring=True, jit=0.15)
def fuel_up(C, n=16, sp=190.0, a=0.6):
    S.flow3(C, PA['flow'], n, sp, S.LP2, 5.0, a=a, seed=5, glow=0.4, lat=22.0)
def tube_bubbles(C, y, a, n=12, sp=240.0, x0=70, x1=1010, r=16.0, t0=None, seed=3, lat=36.0):
    D.flow2(C, [D.Poly([(x0, y), (x1, y)])], n, sp, AIR, r, t0=t0, a=a, seed=seed, jit=0.3, lat=lat, ring=True)
    D.flow2(C, [D.Poly([(x0, y), (x1, y)])], n, sp, (255, 255, 255), r * 0.28, t0=t0, a=0.7 * a, seed=seed, jit=0.3, lat=lat)

# ------------------------------------------------------------------ carligul: bule in conducta transparenta; in sectiune, aerul intra pe langa inelul crapat al cuplei
# (coperta, la 1,85 s: titlul sus, cupla in sectiune cu bulele care intra si inelele crapate incercuite)
T_HB = 1.5; KB_H = (0.7, 0, 160)
TUBE = E.add(P.tube(960, 1.0))
l_hb = E.lb('BULE ÎN CONDUCTA DE MOTORINĂ', 'bad big')
def ov_hookA(C):
    t = C.t; a = F.pop(t, -1.0, T_HB + 0.3)
    F.spr(C, TUBE, 540, 880, -1.0, T_HB + 0.3, anchor='tc')
    tube_bubbles(C, 980, a, n=10, sp=300.0)
    F.spr(C, l_hb, 540, 1150, 0.15, T_HB + 0.3, anchor='tc')
l_hc = E.lb('GARNITURĂ CRĂPATĂ', 'bad'); l_hd = E.lb('AERUL INTRĂ PE LA RACORD', 'bad big')
def rings_o(C, t_in, t_out, R=30.0, names=('o1', 'o2')):
    z = C.shot.kbat(C.t)[0]; a = F.pop(C.t, t_in, t_out)
    for nm in names:
        x, y = S.p3(C, [PQ[nm]])[0]
        D.arc(C, x, y, R * z / 0.7, 0, 360, RED, 5, a * (0.75 + 0.25 * math.sin(C.t * 7.0)))
def ov_hookB(C):
    te = E.T_S + 0.1
    fuel_up(C); air_in(C, n=8, sp=150.0)
    rings_o(C, T_HB - 0.05, te)
    F.spr(C, l_hc, 540, 1560, T_HB - 0.05, te, anchor='tc'); F.spr(C, l_hd, 540, 1650, T_HB + 0.05, te, anchor='tc')     # pline la coperta (1,85 s)
HOOK = [S.plain(E, 0.0, T_HB, ov_hookA, tr=None),
        Shot('qsz', T_HB, E.T_S, st='qbad', kb=[(T_HB,) + KB_H, (E.T_S, 0.72, 0, 156)], phase=False, tr=('xf', 0.3), ov=ov_hookB)]

# ------------------------------------------------------------------ semnele: porneste greu dupa o noapte de stat, ezita la accelerare; in conducta transparenta se vad bule
T_2B = W(2, 'in') - 0.1
SIGNS = [S.symptoms(E, 2, [(E.sym('start', 'PORNEȘTE GREU', 'După o noapte de stat'), 'porneste'), (E.sym('power', 'EZITĂ LA ACCELERARE'), 'ezita')],
                    cam='fl', st='ffull', fx=[S.fx_flt_air(L(2))], t1=T_2B)]
TUBE_B = E.add(P.tube(1000, 1.0))
l_flt2 = E.lb('FILTRU', 'grey')
def ov_tube(C):
    t = C.t; te = L(3) + 0.1; a = F.pop(t, T_2B - 0.1, te)
    S.plate_spr(C, 'fl', 'ffull', 540, 648, 0.42, a, crop=(150, 250, 930, 1500), tag='flt11')
    F.spr(C, l_flt2, 790, 648, T_2B + 0.1, te, anchor='cl')
    F.spr(C, TUBE_B, 540, 900, T_2B - 0.1, te, anchor='tc')
    tube_bubbles(C, 1004, a, n=9, sp=200.0, x0=60, x1=1020, r=18.0, lat=40.0)
    D.arc(C, 540, 1004, 150, 0, 360, RED, 5, F.pop(t, W(2, 'vad') - 0.1, te) * (0.75 + 0.25 * math.sin(t * 7.0)))
SIGNS += [S.plain(E, T_2B, L(3), S.ovs(ov_tube, S.bl(E, [('ÎN CONDUCTA TRANSPARENTĂ', 'lp', T_2B + 0.1, 'Lângă filtru, acolo unde există'),
                                                       ('SE VĂD BULE', 'bad big', W(2, 'vad') - 0.15)], L(3))))]

# ------------------------------------------------------------------ intre rezervor si pompa: conducte, cuple rapide, carcasa filtrului si, la unele masini, para de amorsare;
# la multe motoare partea asta lucreaza in depresiune: pompa trage motorina spre ea
X0, Y0 = 40, 460
def fp(x, y): return (X0 + x, Y0 + y)
LPS = E.add(P.lpside(1000))
CHAIN = [fp(300, 760), fp(300, 80)]
HOSES = [(130, 172), (208, 242), (430, 468), (586, 612), (648, 690)]
T_TANK = W(3, 'rezervor') - 0.1; T_PUMP = W(3, 'pompa') - 0.1; T_FUEL = W(3, 'motorina') - 0.2; T_HOSE = W(3, 'conducte') - 0.1
T_CPL = W(3, 'cuple') - 0.1; T_FLT = W(3, 'carcasa') - 0.1; T_BULB = W(3, 'para') - 0.15
T_DEP = W(4, 'partea') - 0.15; T_PULL = W(4, 'trage') - 0.15; T_4B = W(4, 'garnitura') - 0.4
l_pmp = E.lb('POMPA', 'grey', 'De înaltă presiune'); l_tnk = E.lb('REZERVOR', 'grey'); l_hos = E.lb('CONDUCTE', 'bad'); l_cpl = E.lb('CUPLĂ RAPIDĂ', 'bad')
l_flt = E.lb('CARCASA FILTRULUI', 'bad'); l_blb = E.lb('PARĂ DE AMORSARE', 'bad', 'La unele mașini'); l_dep = E.lb('DEPRESIUNE', 'bad')
WEAK = [  # (centrul pe desen, raza inelului, momentul, eticheta, y-ul etichetei)
 ((300, 190), 46, T_CPL, l_cpl, 650), ((300, 353), 96, T_FLT, l_flt, 813), ((300, 528), 72, T_BULB, l_blb, 988), ((300, 630), 46, T_CPL + 0.2, l_cpl, 1090)]
def ov_lp(C):
    t = C.t; te = T_4B + 0.1; a = F.pop(t, L(3) - 0.1, te)
    if a <= 0.003: return
    F.spr(C, LPS, X0, Y0, L(3) - 0.1, te)
    sp = 150.0 + 90.0 * float(seg(t, T_PULL, T_PULL + 0.6))
    D.flow2(C, [D.Poly(CHAIN)], 22, sp, S.LP2, 5.0, t0=T_FUEL, a=0.95 * a, seed=4, glow=0.45, lat=3.0)
    lo = 1.0 - 0.6 * float(seg(t, T_DEP - 0.2, T_DEP + 0.3))                 # etichetele punctelor slabe se sting cand vine depresiunea; inelele raman
    F.spr(C, l_pmp, 470, fp(0, 80)[1], T_PUMP, T_DEP, anchor='cl'); D.line2(C, [fp(420, 80), (462, fp(0, 80)[1])], (182, 194, 207), 3, a * F.pop(t, T_PUMP, T_DEP))
    F.spr(C, l_tnk, 400, fp(0, 736)[1], T_TANK, te, anchor='cl')
    ah = F.pop(t, T_HOSE, te) * lo
    for y0, y1 in HOSES: D.line2(C, [fp(300, y0 + 4), fp(300, y1 - 4)], RED, 12, ah * (0.55 + 0.3 * math.sin(t * 6.0)))
    F.spr(C, l_hos, 470, fp(0, 449)[1] - 6, T_HOSE, T_DEP, anchor='cl'); D.line2(C, [fp(318, 449), (462, fp(0, 449)[1] - 6)], RED, 3, F.pop(t, T_HOSE, T_DEP))
    for (cx, cy), R, ti, sid, yl in WEAK:
        x, y = fp(cx, cy); ar = F.pop(t, ti, te)
        D.arc(C, x, y, R, 0, 360, RED, 6, ar * (0.8 + 0.2 * math.sin(t * 6.0 + cy)) * (0.55 + 0.45 * lo))
        F.spr(C, sid, 470, yl, ti, T_DEP, anchor='cl'); D.line2(C, [(x + R, y), (462, yl)], RED, 3, F.pop(t, ti, T_DEP))
    ag = F.pop(t, W(4, 'depresiune') - 0.2, te)                               # vacuumetrul: acul coboara sub zero
    if ag > 0.003:
        v = 0.62 - 0.42 * float(ease(seg(t, W(4, 'depresiune'), W(4, 'depresiune') + 1.0)))
        S.gauge(C, 800, 800, 118, v, ag, red=(0.0, 0.3))
        D.text(C, '0', 800 + 150 * math.cos(math.radians(150 + 0.62 * 240)), 800 + 150 * math.sin(math.radians(150 + 0.62 * 240)), 30, (232, 237, 243), ag, font='mont', anchor='mm')
        F.spr(C, l_dep, 800, 948, W(4, 'depresiune') - 0.1, te, anchor='tc')
    S.arrow2(C, (176, 1170), (176, 590), S.LP2, th=12, a=a * F.pop(t, T_PULL, te), prog=float(seg(t, T_PULL, T_PULL + 0.8)), head=30)
    D.arc(C, fp(300, 80)[0], fp(300, 80)[1], 118, 0, 360, (232, 242, 255), 5, F.pop(t, T_PULL, te) * (0.6 + 0.4 * math.sin(t * 8.0)))
LPSIDE = [S.plain(E, L(3), T_4B, S.ovs(ov_lp, S.tl(E, [('DE LA REZERVOR LA POMPĂ', 'big', L(3) + 0.1), ('LA MULTE MOTOARE', 'grey big', L(4) + 0.05),
                                                       ('PARTEA ASTA LUCREAZĂ ÎN DEPRESIUNE', 'bad', T_DEP), ('POMPA TRAGE MOTORINA SPRE EA', 'big', T_PULL)], T_4B)))]

# ------------------------------------------------------------------ o garnitura imbatranita sau o cupla crapata nu lasa motorina sa iasa; lasa aerul sa intre (cupla in sectiune)
T_AIR = W(4, 'lasa', 2) - 0.2; KB_Q = (0.7, 0, 0)
def ov_q4(C):
    t = C.t; te = L(5) + 0.1
    fuel_up(C)
    rings_o(C, T_4B + 0.2, te)
    air_in(C, n=9, sp=150.0, t0=T_AIR)
    pr = float(seg(t, T_AIR, T_AIR + 0.5)); aa = F.pop(t, T_AIR, te)
    for nm, sx in (('mouth', 1), ('mouthL', -1)):
        x, y = S.p3(C, [PQ[nm]])[0]
        S.arrow2(C, (x + sx * 130, y - 84), (x + sx * 22, y - 12), AIR, th=9, a=aa, prog=pr, head=24)
AIRIN = [Shot('qsz', T_4B, L(5), st='qbad', kb=[(T_4B,) + KB_Q, (L(5), 0.72, 0, -6)], phase=False, tr=('xf', 0.3),
              ov=S.ovs(ov_q4, S.tl(E, [('O GARNITURĂ ÎMBĂTRÂNITĂ', 'bad', T_4B + 0.1), ('SAU O CUPLĂ CRĂPATĂ', 'bad', W(4, 'sau') - 0.1),
                                       ('NU LASĂ MOTORINA SĂ IASĂ', 'lp', W(4, 'nu') - 0.1), ('LASĂ AERUL SĂ INTRE', 'bad big', T_AIR)], L(5))))]

# ------------------------------------------------------------------ bulele ajung in pompa; unde e o bula nu e pelicula; aerul impiedica ungerea corecta a pieselor
T_5B = W(5, 'unde') - 0.15; T_5C = W(5, 'aerul') - 0.15
BUB = X.rnd(17, 4, 3)          # bulele turtite in pelicula: cel mult doua intregi pe ecran, intre titlu si etichete
def capsule(C, x, y, w, h, a):
    """o bula turtita intre doua piese: gol inchis la culoare, cu margine alba"""
    r = w / 2.0; n = max(2, int((h - w) / (r * 0.6)) + 2)
    ys = np.linspace(y - (h - w) / 2.0, y + (h - w) / 2.0, n)
    D.dots2(C, np.c_[np.full(n, x), ys], r, (52, 64, 78), a * 0.92, 0.0)
    D.arc(C, x, ys[0], r, 180, 360, AIR, 4, a); D.arc(C, x, ys[-1], r, 0, 180, AIR, 4, a)
    D.line2(C, [(x - r, ys[0]), (x - r, ys[-1])], AIR, 4, a); D.line2(C, [(x + r, ys[0]), (x + r, ys[-1])], AIR, 4, a)
def ov_film(C):
    t = C.t; z = C.shot.kbat(C.t)[0]; a = F.pop(t, T_5B + 0.1, T_5C + 0.1)
    xl, _ = S.pk(C, [(464, 960)])[0]; xr, _ = S.pk(C, [(615, 960)])[0]; xc = (xl + xr) / 2.0; w = (xr - xl) + 10
    for i in range(4):
        h = w * (1.15 + 0.25 * BUB[i, 2]); y = 160 + ((i / 4.0 + 0.04 * BUB[i, 0]) * 1800 + (t - T_5B) * 190) % 1800
        ay = a * float(np.clip((y - h / 2 - 450) / 70.0, 0, 1) * np.clip((1170 - y - h / 2) / 70.0, 0, 1))      # nu intra sub titlu si sub etichete
        if ay > 0.003:
            capsule(C, xc, y, w, h, ay)
            for sx in (xl, xr): S.sparks2(C, sx, y, t, T_5B + 0.3, None, n=7, a=ay, L=24.0, R=28.0, seed=31 + i + int(sx))
l_cam = E.lb('CAMA', 'grey'); l_rol = E.lb('ROLA', 'grey')
def ov_cam(C):
    t = C.t; h = S.hC(C)
    for k in range(3):
        ta = T_5C + 0.5 + 0.8 * k
        if t > ta:
            x, y = S.p3(C, [S.P_contact(h)])[0]
            S.sparks2(C, x, y, t, ta, ta + 0.45, n=10, L=30.0, R=36.0, seed=40 + k)
BUBBLES = [
 S.pump(E, 'pw', L(5), T_5B, st='fuel', fx=[S.fx_fuel(), S.fx_bubbles(L(5) + 0.1)],
        labs=[('BULELE AJUNG ÎN POMPĂ', 'bad big', L(5) + 0.1), ('ODATĂ CU MOTORINA', 'bad', W(5, 'odata') - 0.1)]),
 S.film(E, T_5B, T_5C, st='mclean', pf=FILM_Y, kb=[(T_5B, 1.2, 0, 0), (T_5C, 1.27, 0, 0)], ov=ov_film,
        labs=[('UNDE E O BULĂ', 'bad big', T_5B + 0.1), ('NU E PELICULĂ', 'bad big', W(5, 'nu') - 0.1)]),
 S.pump(E, 'pc', T_5C, L(6), st='fuel', fx=[S.fx_fuel(), S.fx_bubbles(T_5C - 0.3)], ov=ov_cam,
        labs=[('AERUL ÎMPIEDICĂ UNGEREA', 'bad big', T_5C + 0.1), ('CORECTĂ A PIESELOR', 'bad', W(5, 'corecta') - 0.1)]),
]

# ------------------------------------------------------------------ nu e o pana bruska, ca la filtrul montat gol: e o uzura marunta, la fiecare pornire, care se aduna in luni de zile
T_6B = W(6, 'e', 2) - 0.12; T_6C = W(6, 'care') - 0.15
gp = E.panel('UZURA POMPEI', 880, 600)
_u = np.linspace(0, 1, 240); _s = lambda a, b, x: np.clip((x - a) / (b - a), 0, 1) ** 2 * (3 - 2 * np.clip((x - a) / (b - a), 0, 1))
SUDDEN = 0.05 + 0.85 * _s(0.12, 0.17, _u)
STEPS = 0.05 + 0.04 * (np.floor(_u / 0.05) + _s(0.0, 0.25, (_u % 0.05) / 0.05))
def graph(curves, tags, t_in, t_out, t_draw, dur=1.2):
    def ov(C):
        P.graph_panel(C, gp, 540, 470, 880, 600, curves, t_in, t_out + 0.12, t_draw, dur=dur, xlab='TIMP', ylab='UZURĂ', tags=tags)
    return ov
TUBE_F = [E.add(P.tube(1000, 0.18 + 0.82 * i / 15.0)) for i in range(16)]
L_PN = [E.lb('PORNIREA %d' % k, 'grey big') for k in (1, 2, 3)]
def ov_refill(C):
    """trei porniri la rand: la fiecare, coloana de motorina se reface incet, cu bulele impinse in fata ei"""
    t = C.t; te = T_6C + 0.1; a = F.pop(t, T_6B - 0.1, te); per = (T_6C - T_6B) / 3.0
    k = min(2, int(max(t - T_6B, 0.0) / per)); u = float(ease(seg(t - T_6B - k * per, 0.12 * per, 0.85 * per)))
    i = int(round(15 * u)); F.spr(C, TUBE_F[i], 540, 760, T_6B - 0.1, te, anchor='tc')
    xf = 40 + 44 + 872 * (0.18 + 0.82 * i / 15.0) * 1000 / 960.0
    if u < 0.999:
        Q = np.array([[xf - 34 - 74 * m, 864 + 34 * math.sin(m * 2.1)] for m in range(4) if xf - 34 - 74 * m > 90])
        if len(Q): D.dots2(C, Q, 15.0, AIR, a, ring=True)
    F.spr(C, L_PN[k], 540, 1010, T_6B + k * per, T_6B + (k + 1) * per - 0.05 if k < 2 else te, anchor='tc')
STEADY = [
 S.plain(E, L(6), T_6B, S.ovs(graph([(_u, SUDDEN, RED, 6)], [('FILTRU MONTAT GOL', (255, 120, 120), 0.62, 0.95)], L(6) - 0.1, T_6B, W(6, 'filtru') - 0.3, dur=0.9),
                              S.bl(E, [('NU E O PANĂ BRUSCĂ', 'big', L(6) + 0.1), ('CA LA UN FILTRU MONTAT GOL', 'bad', W(6, 'ca') - 0.1)], T_6B, y=1150))),
 S.plain(E, T_6B, T_6C, S.ovs(ov_refill, S.bl(E, [('O UZURĂ MĂRUNTĂ', 'bad big', T_6B + 0.1), ('LA FIECARE PORNIRE', 'bad big', W(6, 'fiecare') - 0.15)], T_6C))),
 S.plain(E, T_6C, L(7), S.ovs(graph([(_u, SUDDEN, (120, 70, 74), 4), (_u, STEPS, YEL, 6)], [('FILTRU MONTAT GOL', (150, 96, 100), 0.62, 0.95), ('AER PE LA RACORDURI', YEL, 0.97, 0.38)], T_6C - 0.1, L(7), T_6C + 0.15, dur=1.6),
                              S.bl(E, [('SE ADUNĂ ÎN LUNI DE ZILE', 'bad big', T_6C + 0.1)], L(7), y=1150))),
]

# ------------------------------------------------------------------ cum eviti: garnituri noi la schimbul de filtru; cuplele si furtunurile crapate se inlocuiesc, nu se carpesc cu coliere
T_7B = W(7, 'iar') - 0.1
ITEMS = [('GARNITURI NOI LA FILTRU', W(7, 'garnituri')), ('CUPLE ȘI FURTUNURI CRĂPATE: NOI', W(7, 'cuplele')), ('NU SE CÂRPESC CU COLIERE', W(7, 'nu') - 0.05, False)]
l_new = E.lb('GARNITURI NOI', 'good')
def ov_new(C):
    F.label(C, l_new, PQ['o2'], (1040, 560), W(7, 'garnituri') + 0.1, T_7B + 0.1, anchor='tr')
AVOID = [S.avoid(E, 'qsz', 'qok', L(7), T_7B, ITEMS, kb=[(L(7), 0.6, 0, -330), (T_7B, 0.62, 0, -336)], ov=ov_new),
         S.avoid(E, 'qsf', 'qfull', T_7B, L(8), ITEMS, kb=[(T_7B, 0.75, 0, -250), (L(8), 0.78, 0, -258)])]

# ------------------------------------------------------------------ ce facem noi: daca a lucrat mult cu aer, o desfacem si o verificam la microscop; schimbam piesele zgariate si garniturile;
# o testam pe banc la presiune si la etanseitate; pleaca cu fisa de test, ca sa stii sigur ca nu pompa trage aer
T_8B = W(8, 'schimbam') - 0.12; T_9B = W(9, 'pleaca') - 0.15
st_set = E.add(P.seals(480))
def ov_set(C): F.spr(C, st_set, 780, 440, W(8, 'garniturile') - 0.2, L(9) + 0.12, anchor='tc')
NOI = [
 S.wk_mic(E, L(8), T_8B, labs=[('DACĂ A LUCRAT MULT CU AER', 'grey', W(8, 'daca') - 0.1), ('O DESFACEM', 'good big', W(8, 'desfacem') - 0.12),
                               ('O VERIFICĂM LA MICROSCOP', 'good big', W(8, 'verificam') - 0.12)], lens=(W(8, 'microscop') - 0.2, T_8B + 0.1)),
 S.wk(E, 'wm', T_8B, L(9), [('SCHIMBĂM PIESELE ZGÂRIATE', 'good', T_8B + 0.12), ('ȘI GARNITURILE', 'good big', W(8, 'garniturile') - 0.12)], st='wkdam',
      seq=[('wk', W(8, 'piesele') - 0.1, W(8, 'piesele') + 0.5)], ov=ov_set),
 S.wk_bench(E, L(9), T_9B, labs=[('O TESTĂM PE BANC', 'good big', W(9, 'testam') - 0.15)],
            rows=[('PRESIUNE', W(9, 'presiune') - 0.05), ('ETANȘEITATE', W(9, 'etanseitate') - 0.05)], t_sheet=W(9, 'testam') + 0.2),
 S.wk_bench(E, T_9B, L(E.OUT), labs=[('PLEACĂ CU FIȘA DE TEST', 'good big', T_9B + 0.12), ('SIGUR NU POMPA TRAGE AER', 'good big', W(9, 'sigur') - 0.15)],
            rows=[('PRESIUNE', L(9)), ('ETANȘEITATE', L(9))], t_sheet=L(9), kb=[(T_9B, 1.04, 0, 0), (L(E.OUT), 1.1, 0, 0)]),
]

SHOTS = S.opening(E, HOOK) + SIGNS + LPSIDE + AIRIN + BUBBLES + STEADY + AVOID + NOI + [S.ending(E)]
SPR = E.SPR
