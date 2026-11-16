# Episodul 1: particulele din motorina. Planurile pe voce (ep1/vo/cues.json).
import os, json, math
import numpy as np
import icomp as IC, ifx as F, ikit as K
import fxlib as X
from icomp import Shot
from fxlib import seg, win, ease
from ifx import PR, PLf, PTS, HP, LP

EP = 'ep1'; N = 1
Q = IC.Cues(os.path.join(IC.HERE, EP, 'vo', 'cues.json')); W = Q.W; L = Q.L; LE = Q.LE
TOTAL = json.load(open(os.path.join(IC.HERE, EP, 'vo', 'timeline.json')))['total']
SD = json.load(open(os.path.join(IC.HERE, 'blend', 'seat_dmg.json')))
GLOB = K.make_glob(EP, N)

def scr(cam, st, P, kb=(1.0, 0, 0)):
    J = json.load(open(IC.find_plate('%s__%s' % (cam, st)) + '.json')); c = X.Cam(J, 1080, 1920); c.set2d(*kb)
    x, y, z = c.proj(np.asarray(P, float).reshape(-1, 3)); return float(x[0]), float(y[0])

BALL = np.array([0, 0, 137.222]); TIP = np.array([0, 0, 0.6]); RING = np.array([0.0, -0.601, 136.621])

SPR = {
 'badge': K.badge_html(N),
 'l_grit': K.lb('PARTICULE DURE', 'bad'),
 'l_src': '<div class="lb src">SURSA: <b>BOSCH</b></div>',
 'l_dirty': K.lb('MOTORINĂ MURDARĂ', 'bad'),
 'l_fail': K.lb('CEDEAZĂ ÎNAINTE DE VREME', 'bad big'),
 'l_gap': '<div class="dim">1–4 µm<small>JOCUL DINTRE PIESE</small></div>',
 'l_hair': K.lb('FIR DE PĂR', '', '50–70 microni'),
 'l_few': K.lb('CÂȚIVA MICRONI', 'bad', 'Nu le vezi cu ochiul liber'),
 'l_scr': K.lb('ZGÂRIETURI', 'bad'),
 'l_valve': K.lb('SUPAPA DE COMANDĂ', 'hp'),
 'l_ball': K.lb('BILĂ DE 1 <span class="u">mm</span>'),
 'l_lift': K.lb('SE RIDICĂ', 'lp'),
 'l_open': K.lb('ACUL DESCHIDE', 'hp'),
 'l_stop': K.lb('INJECȚIA SE OPREȘTE', 'grey'),
 'l_trap': K.lb('PRINSE ÎNTRE BILĂ ȘI SCAUN', 'bad'),
 'l_pits': K.lb('ADÂNCITURI', 'bad'),
 'l_chan': K.lb('CANAL SĂPAT', 'bad'),
 'l_leak': K.lb('NU MAI ETANȘEAZĂ', 'bad'),
 'l_ret': K.lb('RETURUL CREȘTE', 'lp'),
 'p_rate': K.panel('DEBITUL DE INJECȚIE', 820, 380),
 'g_norm': K.lb('NORMAL', 'grey'),
 'g_bad': K.lb('UZAT: MAI MULT, MAI TÂRZIU', 'bad'),
 'l_noz': K.lb('DUZA ERODATĂ', 'bad'),
 'l_jet': K.lb('JET STRICAT', 'bad'),
 's_cel': K.sym('engine', 'MARTORUL DE MOTOR', 'Aprins în bord'),
 's_pwr': K.sym('power', 'PIERDERE DE PUTERE'),
 's_stall': K.sym('stall', 'SE OPREȘTE ÎN MERS', 'Uneori'),
 'l_fq': K.lb('FILTRU DE CALITATE', 'good'),
 'l_fi': K.lb('SCHIMBAT LA INTERVAL', 'good', 'Din cartea service'),
 'l_fuel': K.chk('MOTORINĂ DE LA BENZINĂRII SERIOASE'),
 'l_caught': K.lb('PARTICULELE RĂMÂN ÎN FILTRU', 'good'),
}

# ------------------------------------------------------------------ particule
def fx_hp(t_on, n_grit=60, n_flow=90, paths=('hp_all',), grit_size=0.32, speed=24.0, glow=0.0):
    def f(C):
        for i, pn in enumerate(paths):
            F.flow(C, pn, n_flow, speed * 1.6, np.array([1.0, 0.72, 0.45]), grit_size * 0.35, lat=0.8, seed=11 + i, t0=t_on, mode='add', shape='g', shade=0, a=0.55)
            F.grit(C, pn, n_grit, speed, size=grit_size, seed=17 + i, t0=t_on, lat=0.75)
    return f

def fx_micro(t_on, t_hit):
    gp = F.IPath([[0, -0.1, 170], [0, -0.1, -170]], None, 1.0, smooth=0, step=1.0)
    gp.L = np.tile(np.array([1.0, 0, 0]), (gp.n, 1))
    def f(C):
        t = C.t
        F.flow(C, gp, 30, 46.0, np.array([1.0, 0.75, 0.5]), 0.25, lat=0.9, seed=5, t0=t_on - 3, mode='add', shape='g', shade=0, a=0.5)
        F.grit(C, gp, 9, 38.0, size=1.15, seed=8, t0=t_on, lat=0.25, sz_var=0.35)
        # scantei pe marginile jocului, unde particulele freaca
        for i, tb in enumerate(np.arange(t_hit, t_hit + 3.4, 0.33)):
            zz = 80 - (i * 37) % 160
            F.sparks(C, np.array([1.5 if i % 2 else -1.5, -0.2, zz]), tb, n=18, life=0.28, speed=26.0, size=0.45, seed=60 + i)
    return f

def fx_valve_open(t_open, t_close=None):
    def f(C):
        F.flow(C, 'z_in', 26, 9.0, np.array([1.0, 0.7, 0.4]), 0.09, lat=0.7, seed=3, mode='add', shape='g', shade=0, a=0.6)
        if C.t > t_open - 0.1:
            for pn, sd in (('cc_R', 31), ('ret_L', 32), ('ret_R', 33)):
                F.flow(C, pn, 70, 22.0, LP, 0.11, lat=0.8, seed=sd, t0=t_open, t1=t_close, mode='add', shape='g', shade=0, a=0.8, glow=0.25)
    return f

def fx_seat_trap(t0):
    def f(C):
        t = C.t
        # particule care urca prin orificiul de iesire si se opresc intre bila si scaun (pe fetele de sectiune, la conturul bilei)
        r = X.rnd(71, 12, 8)
        for i in range(12):
            ta = t0 + i * 0.19; u = (t - ta) / 0.6
            if u < 0: continue
            side = 1 if i % 2 else -1
            uu = F.UR if side > 0 else F.UL; nrm = F.NR if side > 0 else F.NL
            rr = 0.56 + 0.05 * r[i, 1]; zz = 136.60 + 0.05 * r[i, 2]
            if u < 1:
                e = u * u * (3 - 2 * u)
                p = uu * (0.12 + (rr - 0.12) * e) + F.EZ * (135.2 + (zz - 135.2) * e) + nrm * 0.03
            else:
                p = uu * rr + F.EZ * zz + nrm * 0.03
            sz = 0.03 + 0.025 * r[i, 3]
            F.dots3(C, p, sz, np.array([0.40, 0.33, 0.26]), 1.0, shade=0.9, ztest=False)
            if u >= 1:
                F.dots3(C, p, sz * 1.9, np.array([1.0, 0.3, 0.25]), 0.9 * (0.55 + 0.45 * math.sin((t - ta) * 10)), shape='r', shade=0, ztest=False)
                F.sparks(C, p, ta + 0.6, n=16, life=0.3, speed=0.8, size=0.01, seed=90 + i)
    return f

UR = F.UR

def fx_chan(t_on):
    cp = F.IPath(SD['chan_path'], None, 0.012, smooth=6, step=0.005)
    def f(C):
        F.flow(C, cp, 160, 1.1, np.array([1.0, 0.55, 0.25]), 0.016, lat=0.5, seed=4, t0=t_on, mode='add', shape='g', shade=0, a=1.0, glow=0.5, ztest=False, tail=2, tail_dt=0.03)
        F.glow(C, cp.P[len(cp.P) // 2], 90 * C.k, HP, 0.3 * float(seg(C.t, t_on, t_on + 0.5)))
    return f

def fx_leak(t_on):
    def f(C):
        for pn, sd in (('ret_L', 32), ('ret_R', 33)):
            F.flow(C, pn, 40, 12.0, LP, 0.1, lat=0.7, seed=sd, t0=t_on, mode='add', shape='g', shade=0, a=0.8, glow=0.3)
        F.glow(C, RING, 70 * C.k, np.array([1.0, 0.3, 0.2]), 0.35 * (0.6 + 0.4 * math.sin(C.t * 9)) * float(seg(C.t, t_on, t_on + 0.4)))
    return f

def fx_nozzle_grit(t_on):
    def f(C):
        for pn, sd in (('nz_R', 51), ('nz_L', 52)):
            F.grit(C, pn, 26, 9.0, size=0.11, seed=sd, t0=t_on, lat=0.9)
    return f

PULSES_A = K.inj_pulses(59.0, 62.3, 0.62, 0.17)
PULSES_B = K.inj_pulses(62.37, 64.4, 0.62, 0.17)
PULSES_C = K.inj_pulses(63.9, 71.2, 0.62, 0.17)
PULSES_E = K.inj_pulses(78.0, TOTAL + 1, 0.7, 0.16)

def fx_filter(t_on):
    FJ = json.load(open('/home/claude/w/inj/out/filter.json'))
    pin = F.IPath(FJ['paths']['in'], 'L', 3.0, smooth=6, step=0.5)
    pup = F.IPath(FJ['paths']['up'], None, 2.0, smooth=6, step=0.5)
    def f(C):
        F.grit(C, pin, 50, 70.0, size=1.6, seed=9, t0=t_on, lat=0.8, ends=(True, False))
        F.flow(C, pup, 60, 90.0, np.array([1.0, 0.85, 0.5]), 0.9, lat=0.6, seed=10, mode='add', shape='g', shade=0, a=0.55)
        # particulele oprite pe hartie (se aduna)
        n = int(np.clip((C.t - t_on) * 14, 0, 70)); r = X.rnd(12, 70, 6)
        if n > 0:
            th = F.aL + 0.02; z = 62 + r[:n, 0] * 70
            P = np.stack([np.cos(th) * 31.5 + 0 * z, np.sin(th) * 31.5 + 0 * z, z], -1) + F.NL[None, :] * 0.5
            F.dots3(C, P, 1.0 + r[:n, 1] * 1.1, np.array([0.11, 0.09, 0.07]), 1.0, shade=0.8)
    return f

# ------------------------------------------------------------------ etichete
def ov_hero(C):
    F.spr(C, 'l_src', 1036, 214, W(2, 'bosch') - 0.1, LE(2) + 0.2, anchor='tr')
    F.label(C, 'l_dirty', PR(5.9, 98.0), (650, 760), W(2, 'motorina'), LE(2) + 0.2)
    F.label(C, 'l_fail', BALL, (560, 1120), W(2, 'cedeaza') - 0.1, LE(2) + 0.2, anchor='tc', side='r')

def ov_micro(C):
    xg, yg = C.P([0, 0, -40.0])
    F.label(C, 'l_gap', ('px', xg / C.k, yg / C.k), (150, 1120), W(3, '1'), W(3, 'un') + 0.2)
    F.label(C, 'l_hair', [-60.0, -70.0, 60.0], (90, 420), W(3, 'par') - 0.05, LE(3) + 0.3)

def ov_micro2(C):
    F.label(C, 'l_few', [0, -0.1, 30.0], (610, 470), W(4, 'nu') - 0.1, LE(4) + 0.2)
    F.label(C, 'l_scr', [1.6, -0.1, -60.0], (640, 1080), W(4, 'fac') - 0.1, LE(4) + 0.2)

def ov_valve(C):
    F.label(C, 'l_valve', [-0.62, 0, 136.62], (80, 520), W(5, 'supapa') - 0.05, W(5, 'acul') - 0.1)
    F.label(C, 'l_ball', BALL + np.array([0, -0.4, 0.5]), (640, 640), W(5, 'bila') - 0.05, W(5, 'acul') - 0.1)
    F.label(C, 'l_lift', BALL + np.array([0, 0, 1.2]), (650, 470), W(5, 'ridica') - 0.05, W(5, 'acul') + 0.4)

def ov_tip(C):
    F.label(C, 'l_open', [0, 0, 3.2], (90, 560), W(5, 'acul'), W(5, 'cand', 2) + 0.1)
    F.label(C, 'l_stop', [0, 0, 2.6], (560, 520), W(5, 'injectia') - 0.1, LE(5) + 0.4)

def ov_seat(C):
    F.label(C, 'l_trap', F.UR * 0.58 + F.EZ * 136.62 + F.NR * 0.03, (420, 470), W(6, 'prinse') - 0.05, 45.1)

def ov_top(C):
    pit = np.array(SD['pits'][8][0])
    F.label(C, 'l_pits', pit, (620, 430), W(6, 'adancituri') - 0.05, W(6, 'unesc') + 0.6)
    cm = np.array(SD['chan_path'][6])
    F.label(C, 'l_chan', cm, (90, 430), W(6, 'canal') - 0.15, LE(6) + 0.4)

def ov_leak(C):
    F.label(C, 'l_leak', RING + np.array([0, 0, 0.05]), (90, 1010), W(7, 'etanseaza') - 0.2, W(7, 'iar') + 0.1)
    F.label(C, 'l_ret', PLf(1.4, 152.0), (90, 420), W(7, 'returul') - 0.05, W(7, 'iar') + 0.1)
    t = C.t; tp = W(7, 'injectorul') - 0.1
    a = F.pop(t, tp, LE(7) + 0.4, 0.3, 0.3)
    if a > 0.003:
        F.spr(C, 'p_rate', 130, 700, tp, LE(7) + 0.4)
        xs = np.linspace(0, 1, 160)
        def pulse(x, a0, a1, h):
            u = np.clip((x - a0) / (a1 - a0), 0, 1); return h * np.sin(np.pi * u) ** 0.6 * ((x >= a0) & (x <= a1))
        y1 = pulse(xs, 0.12, 0.55, 0.62); y2 = pulse(xs, 0.12, 0.74, 0.86)
        pr = float(seg(t, tp + 0.2, tp + 2.2))
        F.graph(C, 170, 790, 740, 250, [(xs, y1, (232, 237, 243), 5), (xs, y2, (255, 75, 75), 6)], pr, a)
        F.spr(C, 'g_norm', 180, 1086 - 40, tp + 0.4, LE(7) + 0.4)
        F.spr(C, 'g_bad', 370, 1086 - 40, W(7, 'multa') - 0.1, LE(7) + 0.4)

def ov_noz(C):
    F.label(C, 'l_noz', [0, 0, 1.6], (90, 600), W(8, 'duza') - 0.1, LE(8) + 0.3)
    F.label(C, 'l_jet', [9.0, -6.0, -2.2], (600, 1080), W(8, 'jetul') + 0.15, LE(8) + 0.3)

def ov_sym(C):
    F.spr(C, 's_cel', 220, 860, W(9, 'martorul') - 0.1, LE(9) + 0.3)
    F.spr(C, 's_pwr', 220, 1000, W(9, 'pierdere') - 0.1, LE(9) + 0.3)
    F.spr(C, 's_stall', 220, 1140, W(9, 'motorul') - 0.1, LE(9) + 0.3)

def ov_filter(C):
    F.label(C, 'l_fq', [25.98, -15.0, 105.0], (600, 520), W(10, 'filtru') - 0.05, LE(10) + 0.3)
    F.label(C, 'l_fi', [-28.0, -16.0, 120.0], (70, 380), W(10, 'schimbat') - 0.05, LE(10) + 0.3)
    F.spr(C, 'l_fuel', 540, 1150, W(10, 'motorina') - 0.1, LE(10) + 0.3, anchor='tc')

# ------------------------------------------------------------------ planuri
T_CAUZA = W(0, 'cauza'); T_PART = W(0, 'particulele')
BALL_HERO = scr('hero', 'shut', BALL, (1.07, 0, -30))
GUIDE_NEEDLE = scr('needle', 'shut', [0, 0, 36.0], (1.3, 0, 300))

SHOTS = [
 Shot('hero', 0.0, T_PART, st='full', wipe=('shut', T_CAUZA - 0.05, T_CAUZA + 0.85, 60),
      kb=[(0.0, 1.0, 0, 0), (T_PART, 1.07, 0, -30)], fx=[fx_hp(T_CAUZA + 0.2, 70, 110)], tr=None),
 Shot('upper', T_PART, L(2), st='shut', tr=('dive', 0.75, BALL_HERO, 3.4),
      kb=[(T_PART, 1.12, 0, 60), (L(2), 1.0, 0, 20)], fx=[fx_hp(T_PART - 3.0, 70, 90, ('hp_in', 'hp_down'), 0.42, 20.0)]),
 Shot('hero', L(2), L(3), st='shut', kb=[(L(2), 0.95, 0, 60), (L(3), 1.0, 0, 70)], fx=[fx_hp(L(2) - 5, 80, 110)], ov=ov_hero,
      spot=lambda t, C: (C.P(BALL)[0], C.P(BALL)[1], 90 * C.k, float(seg(t, W(2, 'cedeaza') - 0.1, W(2, 'cedeaza') + 0.3)))),
 Shot('needle', L(3), W(3, 'jocuri') - 0.1, st='shut', kb=[(L(3), 1.0, 0, 120), (W(3, 'jocuri') - 0.1, 1.3, 0, 300)],
      fx=[fx_nozzle_grit(L(3) - 4)]),
 Shot('micro', W(3, 'jocuri') - 0.1, L(4), st='mclean', seq=[('mhair', W(3, 'un') - 0.05, W(3, 'un') + 0.5)],
      tr=('dive', 0.7, GUIDE_NEEDLE, 3.0), kb=[(W(3, 'jocuri'), 1.0, 0, -40), (L(4), 1.03, 0, -40)], fx=[fx_micro(L(4) + 0.5, 99)], ov=ov_micro),
 Shot('microz', L(4), L(5), st='mclean', seq=[('mscored', W(4, 'microni') - 0.2, W(4, 'fac') + 0.3)], tr=('xf', 0.35),
      kb=[(L(4), 1.0, 0, 0), (L(5), 1.08, 0, 0)], fx=[fx_micro(L(4) + 0.2, W(4, 'vezi'))], ov=ov_micro2),
 Shot('valve', L(5), W(5, 'acul') - 0.05, st='shut', seq=[('vopen', W(5, 'ridica') - 0.05, W(5, 'ridica') + 0.25)],
      kb=[(L(5), 1.0, 0, -60), (W(5, 'acul'), 1.06, 0, -70)], fx=[fx_valve_open(W(5, 'ridica'))], ov=ov_valve),
 Shot('tipw', W(5, 'acul') - 0.05, L(6), st='open', seq=[('shut', W(5, 'inchide') - 0.05, W(5, 'inchide') + 0.2)],
      kb=[(W(5, 'acul'), 1.0, 0, -330), (L(6), 1.04, 0, -340)],
      fx=[lambda C: F.spray(C, W(5, 'acul') + 0.05, W(5, 'inchide') + 0.1, 'good', L=20.0, life=0.45)], ov=ov_tip),
 Shot('seat', L(6), W(6, 'lasa'), st='clean', kb=[(L(6), 1.0, 0, 0), (W(6, 'lasa'), 1.08, 0, 30)], fx=[fx_seat_trap(L(6) + 0.2)], ov=ov_seat),
 Shot('seattop', W(6, 'lasa'), L(7), st='tclean', seq=[('tpits', W(6, 'adancituri') - 0.1, W(6, 'adancituri') + 0.35), ('tchan', W(6, 'unesc') - 0.1, W(6, 'unesc') + 0.45)],
      kb=[(W(6, 'lasa'), 1.0, 0, 0), (L(7), 1.1, 0, 0)], fx=[fx_chan(W(6, 'presiune'))], ov=ov_top),
 Shot('valve', L(7), L(8), st='shut', kb=[(L(7), 1.0, 0, -60), (L(8), 1.04, 0, -60)], fx=[fx_leak(L(7) + 0.2)], ov=ov_leak,
      dim=lambda t: 0.55 * F.pop(t, W(7, 'injectorul') - 0.1, LE(7) + 0.4, 0.3, 0.3)),
 Shot('tipw', L(8), L(9), st='worn', kb=[(L(8), 1.0, 0, -330), (L(9), 1.05, 0, -340)],
      fx=[fx_nozzle_grit(L(8) - 3), lambda C: K.spray_pulses(C, PULSES_A, kind='good', L=20.0, life=0.45),
          lambda C: K.spray_pulses(C, PULSES_B, kind='bad', L=20.0, life=0.45)], ov=ov_noz),
 Shot('chamberz', L(9), L(10), st='shut', kb=[(L(9), 1.0, 0, -140), (L(10), 1.05, 0, -150)],
      fx=[lambda C: K.spray_pulses(C, PULSES_C, kind='bad', L=13.0, life=0.42),
          lambda C: F.smoke(C, np.array([0, -7.0, -5.0]), L(9) - 1.0, n=80, rise=(0, 0, 2.5), spread=12.0, size=2.6, a=0.38)], ov=ov_sym,
      dim=lambda t: 0.25 * F.pop(t, W(9, 'martorul') - 0.1, LE(9) + 0.3)),
 Shot('filter', L(10), L(11), st='fdirty', seq=[('shut', W(10, 'schimbat') - 0.05, W(10, 'schimbat') + 0.5)],
      kb=[(L(10), 0.6, 0, -60), (L(11), 0.63, 0, -60)], fx=[fx_filter(L(10) - 1.0)], ov=ov_filter),
 Shot('chamberz', L(11), TOTAL + 1, st='shut', kb=[(L(11), 1.0, 0, -60), (TOTAL, 1.1, 0, -80)],
      fx=[lambda C: K.spray_pulses(C, PULSES_E, kind='good', L=14.0, life=0.42)]),
]
