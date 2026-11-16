# Episodul 4: calamina din gaurile duzei. Momentele din ep4/vo/cues.json.
import math
import numpy as np
import icomp as IC, ifx as F, ikit as K, iser as S
import fxlib as X
from icomp import Shot
from fxlib import seg
from ifx import PR, PLf

E = S.Ep(4); N = E.n; EP = E.ep; W, L, LE = E.W, E.L, E.LE; TOTAL = E.TOTAL
GLOB = S.glob(E)
HOT = np.array([1.0, 0.42, 0.1]); COKE = np.array([0.09, 0.075, 0.065]); COKE2 = np.array([0.22, 0.16, 0.11]); DET = np.array([0.3, 1.0, 0.55])
SAC = S.SAC; EZ = F.EZ

SPR = dict(S.spr_common(N), **{
 'l_hole': '<div class="dim">0,1 mm<small>GAURA DUZEI</small></div>',
 'l_hot': K.lb('VÂRF FIERBINTE', 'hp'),
 'l_coke': K.lb('CALAMINĂ', 'bad', 'În găuri și în jurul lor'),
 'p_temp': K.panel('DEPUNERILE ȘI TEMPERATURA VÂRFULUI', 820, 380),
 'g_300': K.lb('~300 °C', 'hp'),
 'g_fast': K.lb('CRESC MULT MAI REPEDE', 'bad'),
 's_off': K.sym('stop', 'MOTOR OPRIT', 'Căldura rămâne', 'warn'),
 'l_bake': K.lb('MOTORINA SE COACE', 'bad'),
 'l_in': K.lb('DEPUNEREA DIN GAURĂ', 'bad', 'Ea fură puterea'),
 'l_out': K.lb('CRUSTA DE AFARĂ', 'grey'),
 'l_jet': K.lb('JETUL SE STRICĂ', 'bad'),
 's_smoke': K.sym('smoke', 'FUM'),
 's_pwr': K.sym('power', 'PUTERE MAI MICĂ'),
 's_fuel': K.sym('fuel', 'CONSUM MAI MARE'),
 's_dpf': K.sym('warn', 'PROBLEME REPETATE', 'Cu filtrul de particule'),
 'c_det': K.chk('MOTORINĂ CU ADITIVI DETERGENȚI'),
 'p_bar': K.panel('PUTEREA PIERDUTĂ', 820, 230),
 'g_back': K.lb('PESTE TREI SFERTURI, RECUPERATĂ', 'good'),
 'g_tank': K.lb('CAM ÎNTR-UN PLIN', 'grey'),
})

# ------------------------------------------------------------------ calamina in gaurile 0 si 4 (pe planele de taiere) si in jurul iesirilor
def hole_frame(i):
    d = S.HOLES[i]; u = np.array([d[0], d[1], 0.0]); u /= np.linalg.norm(u)
    perp = np.cross(np.cross(u, EZ), d); perp /= np.linalg.norm(perp)
    nrm = F.NR if i == 0 else F.NL
    return d, perp, nrm
RC = X.rnd(123, 400, 5)
def coke_pts(k_in, k_out):
    """k_in, k_out = 0..1, cat de mult a crescut depunerea in gaura / afara"""
    P = []; Sz = []; Col = []
    for j, i in enumerate((0, 4)):
        d, perp, nrm = hole_frame(i)
        n_in = int(110 * k_in)
        for q in range(n_in):
            r = RC[j * 200 + q]; s = 0.75 + 1.05 * r[0]; side = 1 if r[1] > 0.5 else -1
            P.append(SAC + d * s + perp * side * (0.05 - 0.022 * r[2] * k_in) + nrm * 0.014); Sz.append(0.012 + 0.016 * r[3]); Col.append(COKE)
        n_out = int(80 * k_out)
        for q in range(n_out):
            r = RC[j * 200 + 110 + q]; a = r[0] * 2 * math.pi; rr = 0.06 + 0.16 * r[1]
            P.append(SAC + d * (1.78 + 0.02 * r[2]) + perp * rr * math.cos(a) * 1.0 + EZ * 0.0 + nrm * 0.014 + d * rr * 0.25 * math.sin(a)); Sz.append(0.018 + 0.03 * r[3]); Col.append(COKE2 if q % 3 else COKE)
    return np.array(P), np.array(Sz), np.array(Col)

def fx_coke(curve):
    """curve(t) -> (k_in, k_out)"""
    def f(C):
        ki, ko = curve(C.t)
        if ki <= 0.001 and ko <= 0.001: return
        P, Sz, Col = coke_pts(ki, ko)
        if len(P) == 0: return
        for col in (COKE, COKE2):
            m = np.all(Col == col, axis=1)
            if m.any(): F.dots3(C, P[m], Sz[m], col, 1.0, shade=0.6, ztest=False)
    return f

def fx_heat(t_on, t_off=None, k=1.0):
    def f(C):
        e = float(seg(C.t, t_on, t_on + 1.0)) * (1 - (float(seg(C.t, t_off, t_off + 1.2)) if t_off else 0.0)) * k
        if e <= 0: return
        F.glow(C, np.array([0, 0, 0.9]), 260 * C.k, HOT, 0.32 * e * (0.85 + 0.15 * math.sin(C.t * 3)))
        for i in (0, 4): F.glow(C, S.hole_exit(i), 90 * C.k, np.array([1.0, 0.6, 0.2]), 0.3 * e)
    return f

def fx_bake(t_on):
    def f(C):
        for i in (0, 4):
            F.smoke(C, S.hole_exit(i) + S.HOLES[i] * 0.1, t_on, n=40, rise=(0, 0, 0.6), spread=0.25, size=0.18, col=(0.55, 0.5, 0.45), a=0.35, life=1.8, seed=40 + i)
    return f

def ramp(pts):
    xs = [p[0] for p in pts]
    def g(t):
        return float(np.interp(t, xs, [p[1] for p in pts])), float(np.interp(t, xs, [p[2] for p in pts]))
    return g

T4 = W(4, 'calamina'); T5 = W(5, 'repede'); T6 = L(6); T9 = W(9, 'detergentii')
COKE_CURVE = ramp([(0, 0, 0), (W(4, 'lasa') - 0.2, 0, 0), (LE(4), 0.35, 0.3), (T5, 0.5, 0.45), (LE(5) + 0.2, 0.75, 0.65), (LE(6), 0.95, 0.85),
                   (T9 - 0.2, 1.0, 1.0), (LE(9), 0.18, 0.5), (TOTAL, 0.18, 0.5)])
P_DOWN = K.inj_pulses(L(3) + 0.2, LE(3) + 0.2, 0.62, 0.17)
P_BAD = K.inj_pulses(W(7, 'jetul') - 0.1, L(8) + 0.2, 0.62, 0.17)

# ------------------------------------------------------------------ etichete
def ov_hole(C):
    F.label(C, 'l_hole', S.hole_exit(0) + S.HOLES[0] * 0.05, (600, 470), W(3, 'zecime') - 0.2, LE(3) + 0.3)

def ov_hot(C):
    F.label(C, 'l_hot', np.array([0.7, 0, 0.6]) + F.NR * 0.01, (560, 440), W(4, 'fierbinte') - 0.1, LE(4) + 0.2)
    F.label(C, 'l_coke', S.hole_exit(4) + F.NL * 0.014, (90, 1080), T4 - 0.05, LE(4) + 0.2)

def ov_temp(C):
    t = C.t; tp = L(5) - 0.1; te = LE(5) + 0.3
    a = F.pop(t, tp, te, 0.3, 0.3)
    if a > 0.003:
        F.spr(C, 'p_temp', 130, 560, tp, te)
        xs = np.linspace(0, 1, 160)
        ys = 0.08 + 0.12 * xs + 0.8 * np.clip((xs - 0.5) / 0.5, 0, 1) ** 1.6
        F.graph(C, 170, 650, 740, 250, [(xs, ys, (255, 90, 38), 6)], float(seg(t, tp + 0.2, tp + 2.0)), a)
        x3 = 170 + 0.5 * 740
        F.rect(C, x3 - 1.5, 650, 3, 250, (1.0, 0.824, 0.122), a * float(seg(t, W(5, '300') - 0.1, W(5, '300') + 0.3)))
        F.spr(C, 'g_300', x3 - 60, 910, W(5, '300') - 0.1, te)
        F.spr(C, 'g_fast', 520, 610, T5 - 0.15, te)

def ov_off(C):
    F.spr(C, 's_off', 220, 360, L(6) - 0.05, LE(6) + 0.3)
    F.label(C, 'l_bake', S.hole_exit(0) + F.NR * 0.014, (560, 1080), W(6, 'coace') - 0.1, LE(6) + 0.3)

def ov_inside(C):
    d, perp, nrm = hole_frame(0)
    F.label(C, 'l_in', SAC + d * 1.3 + nrm * 0.014, (420, 430), W(7, 'puterea') - 0.05, W(7, 'jetul') - 0.1)
    F.label(C, 'l_out', SAC + d * 1.85 + perp * 0.14 + nrm * 0.014, (520, 1060), W(7, 'crusta') - 0.05, W(7, 'jetul') - 0.1)
    F.spr(C, 'l_jet', 540, 1100, W(7, 'jetul') + 0.1, LE(7) + 0.3, anchor='tc')

def ov_fix(C):
    t = C.t
    F.spr(C, 'c_det', 540, 420, W(9, 'motorina') - 0.1, LE(9) + 0.3, anchor='tc')
    tp = W(9, 'teste') - 0.1; a = F.pop(t, tp, LE(9) + 0.3, 0.3, 0.3)
    if a > 0.003:
        F.spr(C, 'p_bar', 130, 860, tp, LE(9) + 0.3)
        F.rect(C, 175, 950, 730, 60, (0.235, 0.259, 0.298), a)
        F.rect(C, 175, 950, 730 * 0.78 * float(seg(t, W(9, 'recuperat') - 0.2, W(9, 'recuperat') + 1.2)), 60, (0.239, 0.863, 0.518), a)
        F.spr(C, 'g_back', 175, 1030, W(9, 'sferturi') - 0.2, LE(9) + 0.3)
        F.spr(C, 'g_tank', 175, 1110, W(9, 'plin') - 0.1, LE(9) + 0.3)

def fx_det(t_on):
    def f(C):
        F.flow(C, 'nz_R', 30, 7.0, DET, 0.05, lat=0.8, seed=61, t0=t_on, mode='add', shape='g', shade=0, a=0.8, glow=0.3)
        F.flow(C, 'nz_L', 30, 7.0, DET, 0.05, lat=0.8, seed=62, t0=t_on, mode='add', shape='g', shade=0, a=0.8, glow=0.3)
    return f

# ------------------------------------------------------------------ planuri
TIPKB = (1.0, 0, -330)
HX, HY = S.scr('tip', 'shut', S.hole_exit(0) - S.HOLES[0] * 0.45, (1.0, 0, 0)); ZH = 2.3
DXH, DYH = -(HX - 540) * ZH, -(HY - 960) * ZH - 80
TIPPT = S.scr('tipw', 'shut', [0, 0, 1.0], TIPKB)
SHOTS = S.opening(E, 'tipw', S.TIP, dive_kb=((1.12, 0, -330), (1.0, 0, -330)), zmax=3.6,
                  fx_hook=[fx_heat(E.T_N, None, 0.6)], fx_dive=[fx_heat(E.T_N, None, 1.0)]) + [
 Shot('tip', L(3), L(4), st='shut', seq=[('open', P_DOWN[0][0] - 0.05, P_DOWN[0][0] + 0.05)], tr=('dive', 0.6, TIPPT, 3.0),
      kb=[(L(3), 1.0, 0, -300), (L(4), 1.04, 0, -300)], fx=[lambda C: K.spray_pulses(C, P_DOWN, kind='good', L=5.0, life=0.35, szk=0.45)], ov=ov_hole),
 Shot('tip', L(4), L(6), st='shut', kb=[(L(4), 1.04, 0, -300), (L(6), 1.1, 0, -320)], fx=[fx_heat(L(4)), fx_coke(COKE_CURVE)], ov=[ov_hot, ov_temp],
      dim=lambda t: 0.5 * F.pop(t, L(5) - 0.1, LE(5) + 0.3, 0.3, 0.3)),
 Shot('tip', L(6), L(7), st='shut', tr=('xf', 0.25), kb=[(L(6), 1.1, 0, -320), (L(7), 1.14, 0, -330)], fx=[fx_heat(L(6) - 1.0), fx_coke(COKE_CURVE), fx_bake(W(6, 'coace') - 0.3)], ov=ov_off),
 Shot('tip', L(7), L(8), st='shut', tr=('xf', 0.3), kb=[(L(7), 1.0, 0, -300), (W(7, 'puterea') + 0.2, ZH, DXH, DYH), (W(7, 'jetul') - 0.2, ZH, DXH, DYH), (L(8), 1.0, 0, -300)],
      fx=[fx_coke(COKE_CURVE), lambda C: K.spray_pulses(C, P_BAD, kind='bad', L=5.0, life=0.35, szk=0.45)], ov=ov_inside),
 S.symptoms(E, 8, [('s_smoke', 'fum'), ('s_pwr', 'putere'), ('s_fuel', 'consum'), ('s_dpf', 'probleme')], y0=700, dy=135),
 Shot('tip', L(9), L(E.OUT), st='shut', kb=[(L(9), 1.0, 0, -300), (L(E.OUT), 1.05, 0, -310)], fx=[fx_coke(COKE_CURVE), fx_det(T9 - 0.3)], ov=ov_fix,
      dim=lambda t: 0.45 * F.pop(t, W(9, 'teste') - 0.1, LE(9) + 0.3, 0.3, 0.3)),
 S.ending(E),
]
