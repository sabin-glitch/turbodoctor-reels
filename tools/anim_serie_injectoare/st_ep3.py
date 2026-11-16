# Episodul 3: depunerile din interior (pelicula de lac pe ac si pe pistonul de comanda). Momentele din ep3/vo/cues.json.
import math
import numpy as np
import icomp as IC, ifx as F, ikit as K, iser as S
import fxlib as X
from icomp import Shot
from fxlib import seg
from ifx import PR, PLf

E = S.Ep(3); N = E.n; EP = E.ep; W, L, LE = E.W, E.L, E.LE; TOTAL = E.TOTAL
GLOB = S.glob(E)
AMB = np.array([1.0, 0.68, 0.18]); NA = np.array([1.0, 0.95, 0.75]); ADD = np.array([0.35, 0.9, 0.5]); DET = np.array([0.3, 1.0, 0.55])

SPR = dict(S.spr_common(N), **{
 'l_needle': K.lb('ACUL', 'grey'),
 'l_piston': K.lb('PISTONUL DE COMANDĂ', 'grey'),
 'l_film': K.lb('PELICULĂ CA UN LAC', 'bad', 'Se depune în timp'),
 'l_na': K.lb('URME DE SODIU', 'bad'),
 'l_add': K.lb('ADITIVI', 'lp'),
 'l_ppm': K.lb('CÂTEVA PĂRȚI LA UN MILION', 'bad big'),
 'l_gap': '<div class="dim">CÂȚIVA MICRONI<small>JOCUL DINTRE PIESE</small></div>',
 'l_force': K.lb('FORȚE MICI', 'grey'),
 'l_brake': K.lb('PELICULA LE FRÂNEAZĂ', 'bad'),
 'p_lag': K.panel('COMANDA ȘI MIȘCAREA ACULUI', 820, 380),
 'g_cmd': K.lb('COMANDA', 'grey'),
 'g_late': K.lb('ACUL: MAI TÂRZIU', 'bad'),
 'l_stuck': K.lb('SAU RĂMÂNE LIPIT', 'bad big'),
 's_cold': K.sym('cold', 'PORNIRE GREA LA RECE', 'Sau imposibilă'),
 's_idle': K.sym('idle', 'MERS NEREGULAT'),
 's_pwr': K.sym('power', 'PIERDERE DE PUTERE'),
 'l_elec': K.lb('TESTELE ELECTRICE', 'grey'),
 'c_coil': K.chk('BOBINA: BUNĂ'),
 'c_res': K.chk('REZISTENȚA: BUNĂ'),
 'c_inj': K.chk('INJECȚIA: NU E CUM TREBUIE', False),
 'c_det': K.chk('MOTORINĂ CU ADITIVI DETERGENȚI'),
 'c_st': K.chk('DE LA BENZINĂRII SERIOASE'),
 'l_clean': K.lb('LE POT CHIAR CURĂȚA', 'good'),
})

# ------------------------------------------------------------------ pelicula (stralucire chihlimbar pe ac si pe piston)
NEEDLE_Z = np.linspace(8.0, 32.0, 13); PIST_Z = np.linspace(119.0, 130.5, 8)
def fx_film(t_on, a=0.42, r=24):
    def f(C):
        e = float(seg(C.t, t_on, t_on + 1.2))
        if e <= 0: return
        for z in NEEDLE_Z:
            for P in (PR(1.44, z), PLf(1.44, z)): F.glow(C, P, r * C.k, AMB, a * e)
        for z in PIST_Z:
            for P in (PR(2.12, z), PLf(2.12, z)): F.glow(C, P, r * C.k, AMB, a * e)
    return f

def fx_sodium(t_react, t_stick):
    """sodiul si aditivii plutesc in joc, reactioneaza si se lipesc pe pereti (scena micro)"""
    gp = F.IPath([[0, -0.1, 26], [0, -0.1, -26]], None, 1.0, smooth=0, step=0.25)
    gp.L = np.tile(np.array([0.7, 0, 0]), (gp.n, 1))
    r = X.rnd(91, 80, 4)
    def f(C):
        t = C.t
        F.flow(C, gp, 30, 13.0, np.array([1.0, 0.75, 0.5]), 0.12, lat=0.9, seed=5, mode='add', shape='g', shade=0, a=0.45)
        if t < t_stick + 0.8:
            k = 1 - float(seg(t, t_stick, t_stick + 0.8))
            F.flow(C, gp, 9, 9.0, NA, 0.3, lat=0.6, seed=6, mode='over', shape='d', shade=0.4, a=k)
            F.flow(C, gp, 9, 7.5, ADD, 0.34, lat=0.6, seed=7, mode='over', shape='d', shade=0.4, a=k)
        n = int(np.clip((t - t_react) * 22, 0, 80))
        if n > 0:
            side = np.where(np.arange(n) % 2 == 0, -1.0, 1.0)
            P = np.stack([side * (1.5 - 0.12), -0.12 + 0 * side, 21 - r[:n, 0] * 42], -1)
            F.dots3(C, P, 0.13 + 0.1 * r[:n, 1], AMB, 0.95, shade=0.5, ztest=False)
    return f

def fx_gapflow(t_slow):
    gp = F.IPath([[0, -0.1, 26], [0, -0.1, -26]], None, 1.0, smooth=0, step=0.25)
    gp.L = np.tile(np.array([0.5, 0, 0]), (gp.n, 1))
    def f(C):
        fast = C.t < t_slow
        F.flow(C, gp, 30, 15.0 if fast else 3.0, np.array([1.0, 0.75, 0.5]), 0.13, lat=0.9, seed=5, mode='add', shape='g', shade=0, a=0.5)
    return f

def fx_clean(t_on):
    gp = F.IPath([[0, -0.1, 26], [0, -0.1, -26]], None, 1.0, smooth=0, step=0.25)
    gp.L = np.tile(np.array([0.6, 0, 0]), (gp.n, 1))
    def f(C):
        F.flow(C, gp, 28, 13.0, np.array([1.0, 0.75, 0.5]), 0.12, lat=0.9, seed=5, mode='add', shape='g', shade=0, a=0.45)
        F.flow(C, gp, 16, 10.0, DET, 0.3, lat=0.7, seed=8, t0=t_on, mode='add', shape='g', shade=0, a=0.9, glow=0.4)
    return f

def fx_coil(t_on, t_off):
    def f(C):
        if C.t < t_on or C.t > t_off: return
        ph = (C.t - t_on) % 0.62
        a = 0.45 if ph < 0.2 else 0.0
        for P in (PR(6.0, 152.0), PLf(6.0, 152.0)): F.glow(C, P, 70 * C.k, np.array([0.45, 0.75, 1.0]), a)
    return f

P_LAG = K.inj_pulses(L(6) - 0.4, W(6, 'ramane') - 0.2, 0.7, 0.16)

# ------------------------------------------------------------------ etichete
def ov_hero(C):
    F.label(C, 'l_needle', PR(1.42, 22.0), (640, 1060), W(3, 'ac') - 0.05, LE(3) + 0.2)
    F.label(C, 'l_piston', PR(2.14, 125.0), (560, 520), W(3, 'pistonul') - 0.05, LE(3) + 0.2)
    F.spr(C, 'l_film', 540, 1150, W(3, 'pelicula') - 0.1, LE(3) + 0.2, anchor='tc')

def ov_sodium(C):
    F.label(C, 'l_na', [0.0, -0.1, 9.0], (90, 430), W(4, 'sodiu') - 0.05, LE(4) + 0.2)
    F.label(C, 'l_add', [0.0, -0.1, -1.0], (640, 640), W(4, 'aditivi') - 0.05, LE(4) + 0.2)
    F.spr(C, 'l_ppm', 540, 1080, W(4, 'teste') - 0.1, LE(4) + 0.3, anchor='tc')

def ov_brake(C):
    t = C.t; a = F.pop(t, W(5, 'jocurile') - 0.1, W(5, 'fortele') + 0.6, 0.25, 0.25)
    if a > 0.003:                                   # cota peste joc, de la perete de metal la perete de metal
        x0, y0 = C.P([-1.5, -0.1, 2.0]); x1, y1 = C.P([1.5, -0.1, 2.0])
        F.bracket(C, (x0 / C.k, y0 / C.k), (x1 / C.k, y1 / C.k), a, th=4.0, tick=18)
    xg, yg = C.P([0, -0.1, 2.0])
    F.label(C, 'l_gap', ('px', xg / C.k, yg / C.k + 20), (110, 640), W(5, 'jocurile'), W(5, 'fortele') + 0.6)
    F.label(C, 'l_force', [-5.0, -0.1, 7.0], (560, 430), W(5, 'fortele') - 0.05, LE(5) + 0.2)
    F.label(C, 'l_brake', [-1.0, -0.1, -4.0], (90, 1150), W(5, 'franeaza') - 0.1, LE(5) + 0.3)

def ov_lag(C):
    t = C.t; tp = L(6) - 0.1; te = W(6, 'ramane') - 0.15
    a = F.pop(t, tp, te, 0.3, 0.3)
    if a > 0.003:
        F.spr(C, 'p_lag', 130, 640, tp, te)
        xs = np.linspace(0, 1, 160)
        cmd = 0.8 * ((xs > 0.12) & (xs < 0.5))
        def lift(x, a0, a1, h):
            u = np.clip((x - a0) / (a1 - a0), 0, 1); return h * np.sin(np.pi * u) ** 0.5 * ((x >= a0) & (x <= a1))
        late = lift(xs, 0.34, 0.72, 0.55)
        pr = float(seg(t, tp + 0.2, tp + 2.0))
        F.graph(C, 170, 730, 740, 250, [(xs, cmd, (232, 237, 243), 5), (xs, late, (255, 75, 75), 6)], pr, a)
        F.spr(C, 'g_cmd', 180, 990, tp + 0.3, te)
        F.spr(C, 'g_late', 410, 990, W(6, 'tarziu') - 0.1, te)
    F.spr(C, 'l_stuck', 540, 1110, W(6, 'ramane') - 0.1, LE(6) + 0.3, anchor='tc')

def ov_elec(C):
    F.label(C, 'l_elec', PR(6.0, 152.0), (90, 430), W(8, 'testele') - 0.05, LE(8) + 0.3)
    F.spr(C, 'c_coil', 540, 960, W(8, 'electrice') - 0.05, LE(8) + 0.3, anchor='tc')
    F.spr(C, 'c_res', 540, 1050, W(8, 'bune') - 0.1, LE(8) + 0.3, anchor='tc')
    F.spr(C, 'c_inj', 540, 1140, W(8, 'dar') - 0.05, LE(8) + 0.3, anchor='tc')

def ov_clean(C):
    F.spr(C, 'c_det', 540, 420, W(9, 'motorina') - 0.1, LE(9) + 0.3, anchor='tc')
    F.spr(C, 'c_st', 540, 510, W(9, 'benzinarii') - 0.1, LE(9) + 0.3, anchor='tc')
    F.spr(C, 'l_clean', 540, 1120, W(9, 'curata') - 0.1, LE(9) + 0.3, anchor='tc')

# ------------------------------------------------------------------ planuri
BALLH = S.scr('hero', 'shut', [0, 0, 22.0], (1.0, 0, 70))
SHOTS = S.opening(E, 'upper', S.BALL, fx_hook=[fx_film(E.T_N, 0.35, 16)], fx_dive=[fx_film(E.T_N, 0.4, 30)]) + [
 Shot('hero', L(3), L(4), st='shut', kb=[(L(3), 0.95, 0, 60), (L(4), 1.0, 0, 70)], fx=[S.fx_fuel(L(3) - 4), fx_film(W(3, 'depune') - 0.2, 0.5, 18)], ov=ov_hero),
 Shot('microf', L(4), L(5), st='mclean', seq=[('mlac1', W(4, 'reactioneaza') - 0.1, W(4, 'reactioneaza') + 1.4)], tr=('dive', 0.7, BALLH, 3.0),
      kb=[(L(4), 1.0, 0, 0), (L(5), 1.06, 0, 0)], fx=[fx_sodium(W(4, 'reactioneaza'), W(4, 'aditivi') + 0.4)], ov=ov_sodium),
 Shot('microf', L(5), L(6), st='mlac1', seq=[('mlac2', W(5, 'pelicula') - 0.15, W(5, 'pelicula') + 0.6)], tr=('xf', 0.25),
      kb=[(L(5), 1.06, 0, 0), (L(6), 1.14, 0, 0)], fx=[fx_gapflow(W(5, 'franeaza'))], ov=ov_brake),
 Shot('tipw', L(6), L(7), st='shut', kb=[(L(6), 1.0, 0, -330), (L(7), 1.04, 0, -340)],
      fx=[lambda C: [F.spray(C, a + 0.12, b + 0.12, 'weak', L=16.0, life=0.4) for a, b in P_LAG if a - 0.05 <= C.t <= min(b + 0.8, W(6, 'ramane') - 0.05)]], ov=ov_lag,
      dim=lambda t: 0.5 * F.pop(t, L(6) - 0.1, W(6, 'ramane') - 0.15, 0.3, 0.3)),
 S.symptoms(E, 7, [('s_cold', 'pornire'), ('s_idle', 'mers'), ('s_pwr', 'pierdere')], kind='weak'),
 Shot('upper', L(8), L(9), st='shut', kb=[(L(8), 1.0, 0, 20), (L(9), 1.05, 0, 30)], fx=[S.fx_fuel(L(8) - 3, ('hp_in', 'hp_down'), 90, 32.0), fx_coil(L(8), LE(8) + 0.4), fx_film(L(8) - 1, 0.45, 30)], ov=ov_elec),
 Shot('microf', L(9), L(E.OUT), st='mlac2', seq=[('mlac1', W(9, 'previn') - 0.1, W(9, 'previn') + 0.8), ('mclean', W(9, 'curata') - 0.1, W(9, 'curata') + 0.8)],
      kb=[(L(9), 1.0, 0, 0), (L(E.OUT), 1.05, 0, 0)], fx=[fx_clean(W(9, 'detergenti') - 0.2)], ov=ov_clean),
 S.ending(E),
]
