# Episodul 2: apa din motorina. Planurile pe voce (ep2/vo/cues.json).
import os, json, math
import numpy as np
import icomp as IC, ifx as F, ikit as K
import fxlib as X
from icomp import Shot
from fxlib import seg, win, ease
from ifx import PR, PLf, PTS, HP, LP

EP = 'ep2'; N = 2
Q = IC.Cues(os.path.join(IC.HERE, EP, 'vo', 'cues.json')); W = Q.W; L = Q.L; LE = Q.LE
TOTAL = json.load(open(os.path.join(IC.HERE, EP, 'vo', 'timeline.json')))['total']
GLOB = K.make_glob(EP, N)
WATER = np.array([0.18, 0.61, 1.0]); RUSTC = np.array([0.62, 0.30, 0.12]); RUSTD = np.array([0.42, 0.20, 0.08])
TJ = json.load(open(os.path.join(IC.HERE, 'blend', 'tank.json'))); TD = TJ['dims']
FJ = json.load(open('/home/claude/w/inj/out/filter.json'))

def scr(cam, st, P, kb=(1.0, 0, 0)):
    J = json.load(open(IC.find_plate('%s__%s' % (cam, st)) + '.json')); c = X.Cam(J, 1080, 1920); c.set2d(*kb)
    x, y, z = c.proj(np.asarray(P, float).reshape(-1, 3)); return float(x[0]), float(y[0])

BALL = np.array([0, 0, 137.222])

SPR = {
 'badge': K.badge_html(N),
 'l_src': '<div class="lb src">SURSA: <b>BOSCH</b></div>',
 'l_water': K.lb('APĂ ÎN MOTORINĂ', 'water'),
 'l_second': K.lb('A DOUA CAUZĂ', 'bad big'),
 'l_after': K.lb('DUPĂ MOTORINA MURDARĂ', 'grey'),
 'l_metal': K.lb('TOTUL E METAL', 'grey'),
 'l_rust': K.lb('RUGINĂ', 'bad'),
 'l_flake': K.lb('SE DESPRINDE ȘI MACINĂ', 'bad'),
 'l_fill': K.lb('UMPLE JOCUL', 'bad'),
 'l_block': K.lb('PIESELE SE BLOCHEAZĂ', 'bad big'),
 'l_oil': K.lb('MOTORINA UNGE', 'good'),
 'l_nooil': K.lb('APA NU UNGE', 'bad'),
 'l_contact': K.lb('METAL PE METAL', 'bad'),
 'l_lub': K.lb('SINGURUL LUBRIFIANT', 'lp'),
 'l_cond': K.lb('CONDENS', 'water', 'Pe pereții rezervorului'),
 'l_bottom': K.lb('APA SE ADUNĂ PE FUND', 'water', 'E mai grea decât motorina'),
 's_station': K.sym('fuel', 'BENZINĂRII CU REZERVOARE', 'Prost întreținute'),
 'l_sep': K.lb('SEPARĂ APA', 'water'),
 'l_cup': K.lb('PAHARUL DE APĂ', 'water'),
 'l_nodrain': K.lb('NESCURSĂ LA TIMP', 'bad'),
 'l_pass': K.lb('SPRE POMPĂ ȘI INJECTOARE', 'bad'),
 's_start': K.sym('start', 'PORNIRE GREA'),
 's_idle': K.sym('idle', 'MERS NEREGULAT'),
 's_pwr': K.sym('power', 'PUTERE MAI MICĂ'),
 's_smoke': K.sym('smoke', 'FUM'),
 'l_fuel': K.chk('MOTORINĂ DE LA BENZINĂRII SERIOASE'),
 'l_ft': K.lb('FILTRUL SCHIMBAT LA TIMP', 'good'),
 's_wlamp': K.sym('water', 'MARTORUL DE APĂ', 'Aprins în bord', 'warn'),
 'l_drain': K.lb('APA SCURSĂ DIN FILTRU', 'good'),
}

# ------------------------------------------------------------------ picaturi de apa in motorina
def fx_water(t_on, n=26, n_flow=90, paths=('hp_all',), size=0.58, speed=22.0):
    def f(C):
        for i, pn in enumerate(paths):
            F.flow(C, pn, n_flow, speed * 1.6, np.array([1.0, 0.72, 0.45]), size * 0.3, lat=0.8, seed=11 + i, t0=t_on, mode='add', shape='g', shade=0, a=0.5)
            F.flow(C, pn, n, speed, WATER, size, lat=0.7, seed=27 + i, t0=t_on, mode='over', shape='d', shade=0.55, sz_var=0.45)
            F.flow(C, pn, n, speed, np.array([0.85, 0.95, 1.0]), size * 0.35, lat=0.7, seed=27 + i, t0=t_on, mode='add', shape='g', shade=0, a=0.6, sz_var=0.45)
    return f

def fx_needle_rust(t_w, t_r):
    """picaturi de apa care se aseaza pe ac si se fac rugina"""
    r = X.rnd(33, 26, 4)
    def f(C):
        t = C.t
        for i in range(26):
            ta = t_w + i * 0.05
            if t < ta: continue
            z = 9.0 + r[i, 0] * 14.0; side = 1 if i % 2 else -1
            p = (F.UR if side > 0 else F.UL) * (1.46 + 0.05 * r[i, 1]) + F.EZ * z + (F.NR if side > 0 else F.NL) * 0.02
            k = float(seg(t, t_r, t_r + 0.9)); col = WATER * (1 - k) + RUSTC * k
            F.dots3(C, p, 0.10 + 0.07 * r[i, 2], col, float(seg(t, ta, ta + 0.25)), shade=0.6, ztest=False)
    return f

def fx_flakes(t_on, t_grind):
    """bucati de rugina care se desprind de pe pereti si macina (scena micro, 1 unitate = 1 micron)"""
    gp = F.IPath([[0, -0.1, 170], [0, -0.1, -170]], None, 1.0, smooth=0, step=1.0)
    gp.L = np.tile(np.array([0.45, 0, 0]), (gp.n, 1))
    def f(C):
        t = C.t
        F.flow(C, gp, 24, 40.0, np.array([1.0, 0.75, 0.5]), 0.22, lat=0.9, seed=5, t0=t_on - 3, mode='add', shape='g', shade=0, a=0.45)
        F.flow(C, gp, 12, 30.0, RUSTC, 1.3, lat=0.5, seed=9, t0=t_on, mode='over', shape='d', shade=0.7, sz_var=0.5)
        for i, tb in enumerate(np.arange(t_grind, t_grind + 3.0, 0.3)):
            zz = 90 - (i * 41) % 180
            F.sparks(C, np.array([0.75 if i % 2 else -0.75, -0.2, zz]), tb, n=16, life=0.26, speed=24.0, size=0.42, seed=70 + i)
    return f

def fx_dry_contact(t_on, t_off):
    def f(C):
        for i, tb in enumerate(np.arange(t_on, t_off, 0.24)):
            zz = 100 - (i * 53) % 200
            F.sparks(C, np.array([1.5 if i % 2 else -1.5, -0.2, zz]), tb, n=22, life=0.3, speed=30.0, size=0.5, seed=110 + i)
    return f

def fx_tank(t_cond, t_fall):
    T, ZW, ZF, LZ = TD['T'], TD['ZW'], TD['ZF'], TD['LZ']
    r = X.rnd(55, 14, 5)
    def f(C):
        t = C.t
        for i in range(14):                      # picaturi care cad din tavan, trec prin motorina si se aduna jos
            ta = t_fall + i * 0.42
            if t < ta: continue
            x = -200 + r[i, 0] * 260; y = 40 + r[i, 1] * 90; z0 = LZ - T - 6
            u = t - ta; zf = z0 - 0.5 * 2600 * u * u
            if zf < ZF:
                tf = math.sqrt(2 * (z0 - ZF) / 2600); zf = ZF - 34 * (u - tf)
            if zf < ZW + 3:
                continue
            F.dots3(C, np.array([x, y, zf]), 5.0 + 2.0 * r[i, 2], WATER, 1.0, shade=0.6, ztest=False)
            F.dots3(C, np.array([x - 1.5, y - 2, zf + 1.5]), 1.8, np.array([0.9, 0.97, 1.0]), 0.8, mode='add', shape='g', shade=0, ztest=False)
        a = float(seg(t, t_cond, t_cond + 1.0)) * (0.5 + 0.5 * math.sin(t * 2.2) ** 2)
        F.glow(C, np.array([0, 60, (T + ZW) / 2]), 260 * C.k, WATER, 0.18 * a)
    return f

def fx_filter_sep(t_on, t_out):
    pup = F.IPath(FJ['paths']['up'], None, 2.0, smooth=6, step=0.5)
    pin = F.IPath(FJ['paths']['in'][1:], 'L', 3.0, smooth=6, step=0.5)   # fara primul segment: racordul de intrare nu e modelat
    r = X.rnd(81, 30, 4)
    def f(C):
        t = C.t
        F.flow(C, pin, 40, 70.0, np.array([1.0, 0.85, 0.5]), 0.9, lat=0.7, seed=12, mode='add', shape='g', shade=0, a=0.5)
        F.flow(C, pin, 12, 60.0, WATER, 2.2, lat=0.7, seed=13, mode='over', shape='d', shade=0.55, t1=t_out + 0.5)
        for i in range(30):                      # picaturile coboara printre straturi spre pahar
            ta = t_on + (i * 0.23) % 6.0 + int(i * 0.23 / 6.0) * 6.0
            u = (t - ta) % 3.2
            if t < ta: continue
            z = 60 - 14 * u; rr = 12 + r[i, 0] * 15
            if z < 18: continue
            P = (F.UR if i % 2 else F.UL) * rr + F.EZ * z + (F.NR if i % 2 else F.NL) * 0.6
            F.dots3(C, P, 1.6 + r[i, 1] * 1.0, WATER, 1.0, shade=0.55)
        if t > t_out:
            F.flow(C, pup, 30, 70.0, WATER, 2.0, lat=0.6, seed=14, t0=t_out, mode='over', shape='d', shade=0.55)
            F.flow(C, pup, 50, 90.0, np.array([1.0, 0.85, 0.5]), 0.9, lat=0.6, seed=15, mode='add', shape='g', shade=0, a=0.5)
    return f

def fx_drain(t_on):
    pd = F.IPath([[0.0, 0, 6.0], [0.0, 0, -9.0], [0.0, 0, -70.0]], None, 1.5, smooth=4, step=0.5)
    def f(C):
        F.flow(C, pd, 40, 42.0, WATER, 2.2, lat=0.5, seed=16, t0=t_on, t1=t_on + 4.0, mode='over', shape='d', shade=0.55, ztest=False)
    return f

PULSES_S = K.inj_pulses(L(8) - 0.5, L(9) + 0.3, 0.62, 0.17)
PULSES_E = K.inj_pulses(L(10) - 0.2, TOTAL + 1, 0.7, 0.16)

# ------------------------------------------------------------------ etichete
def ov_hero(C):
    F.spr(C, 'l_src', 1036, 214, W(2, 'bosch') - 0.1, LE(2) + 0.2, anchor='tr')
    F.label(C, 'l_water', PR(5.9, 96.0), (650, 760), W(2, 'apa') - 0.05, LE(2) + 0.2)
    F.label(C, 'l_second', PR(5.9, 72.0), (520, 1000), W(2, 'doua') - 0.1, LE(2) + 0.2, anchor='tc', side='r')
    F.spr(C, 'l_after', 540, 1170, W(2, 'imediat') - 0.1, LE(2) + 0.2, anchor='tc')

def ov_needle(C):
    F.label(C, 'l_metal', PR(1.42, 30.0), (620, 420), W(3, 'metal') - 0.1, LE(3) + 0.3)
    F.label(C, 'l_rust', PR(1.48, 15.0), (90, 1050), W(3, 'rugina') - 0.05, LE(3) + 0.3)

def ov_rust(C):
    F.label(C, 'l_flake', [0.0, -0.1, 40.0], (430, 420), W(4, 'desprinde') - 0.1, W(4, 'umple') - 0.1)
    F.label(C, 'l_fill', [0.0, -0.1, -30.0], (90, 1060), W(4, 'umple') - 0.05, LE(4) + 0.3)
    F.spr(C, 'l_block', 540, 700, W(4, 'blocheaza') - 0.1, LE(4) + 0.3, anchor='tc')

def ov_lube(C):
    F.label(C, 'l_oil', [0.0, -0.1, 40.0], (600, 420), W(5, 'motorina') - 0.1, W(5, 'apa') - 0.1)
    F.label(C, 'l_nooil', [0.0, -0.1, 30.0], (600, 420), W(5, 'apa'), W(5, 'iar') - 0.1)
    F.label(C, 'l_contact', [1.5, -0.1, -50.0], (90, 1060), W(5, 'unge') - 0.05, W(5, 'iar') - 0.1)
    F.label(C, 'l_lub', [0.0, -0.1, 30.0], (560, 420), W(5, 'iar'), LE(5) + 0.3)

def ov_tank(C):
    F.label(C, 'l_cond', TJ['pts']['wall'], (90, 560), W(6, 'condensul') - 0.05, W(6, 'filtrul') + 0.2)
    F.label(C, 'l_bottom', TJ['pts']['water'], (500, 1212), W(6, 'rezervor') - 0.05, W(6, 'filtrul') + 0.2)
    F.spr(C, 's_station', 540, 380, W(6, 'benzinarii') - 0.1, W(6, 'filtrul') + 0.2, anchor='tc')

def ov_filter7(C):
    F.label(C, 'l_cup', FJ['pts']['bowl'], (610, 1130), W(6, 'filtrul') + 0.2, W(7, 'daca') + 0.2)
    F.label(C, 'l_sep', [26.0, -15.0, 70.0], (600, 520), W(7, 'separa') - 0.05, W(7, 'daca') + 0.2)
    F.label(C, 'l_nodrain', FJ['pts']['bowl'], (560, 1130), W(7, 'scursa') - 0.05, LE(7) + 0.3)
    F.label(C, 'l_pass', [40.0, -20.0, 162.0], (520, 380), W(7, 'trece') - 0.05, LE(7) + 0.3, anchor='tc')

def ov_sym(C):
    F.spr(C, 's_start', 220, 760, W(8, 'pornire') - 0.1, LE(8) + 0.3)
    F.spr(C, 's_idle', 220, 900, W(8, 'mers') - 0.1, LE(8) + 0.3)
    F.spr(C, 's_pwr', 220, 1040, W(8, 'putere') - 0.1, LE(8) + 0.3)
    F.spr(C, 's_smoke', 220, 1180, W(8, 'fum') - 0.1, LE(8) + 0.3)

def ov_filter9(C):
    F.spr(C, 'l_fuel', 540, 1180, W(9, 'motorina') - 0.1, W(9, 'martorul') - 0.1, anchor='tc')
    F.label(C, 'l_ft', [-28.0, -16.0, 120.0], (70, 420), W(9, 'filtrul') - 0.05, LE(9) + 0.3)
    F.spr(C, 's_wlamp', 540, 1040, W(9, 'martorul') - 0.1, LE(9) + 0.3, anchor='tc')
    F.label(C, 'l_drain', FJ['pts']['drain'], (470, 1180), W(9, 'apa', 2) - 0.05, LE(9) + 0.3)

# ------------------------------------------------------------------ planuri
T_CAUZA = W(0, 'cauza'); T_APA = W(0, 'apa')
BALL_HERO = scr('hero', 'shut', BALL, (1.07, 0, -30))
GUIDE_NEEDLE = scr('needle', 'shut', [0, 0, 15.0], (1.3, 0, -200))
T_FILT = W(6, 'filtrul')

def shake(t0, t1, amp=10.0):
    def g(t):
        if t < t0 or t > t1: return 0.0
        return amp * math.sin(t * 61.0) * (1 - (t - t0) / (t1 - t0))
    return g
SHK = shake(W(4, 'blocheaza'), W(4, 'blocheaza') + 0.6)

SHOTS = [
 Shot('hero', 0.0, T_APA, st='full', wipe=('shut', T_CAUZA - 0.05, T_CAUZA + 0.85, 60),
      kb=[(0.0, 1.0, 0, 0), (T_APA, 1.07, 0, -30)], fx=[fx_water(T_CAUZA + 0.2, 30, 100)], tr=None),
 Shot('upper', T_APA, L(2), st='shut', tr=('dive', 0.75, BALL_HERO, 3.4),
      kb=[(T_APA, 1.12, 0, 60), (L(2), 1.0, 0, 20)], fx=[fx_water(T_APA - 3.0, 22, 90, ('hp_in', 'hp_down'), 0.5, 18.0)]),
 Shot('hero', L(2), L(3), st='shut', kb=[(L(2), 0.95, 0, 60), (L(3), 1.0, 0, 70)], fx=[fx_water(L(2) - 5, 30, 110)], ov=ov_hero),
 Shot('needle', L(3), L(4), st='shut', seq=[('nrust', W(3, 'rugina') - 0.1, W(3, 'rugina') + 0.8)],
      kb=[(L(3), 1.0, 0, 0), (L(4), 1.3, 0, -200)], fx=[fx_needle_rust(L(3) + 0.3, W(3, 'rugina') - 0.1)], ov=ov_needle,
      spot=lambda t, C: (C.P(PR(0.0, 15.0))[0], C.P(PR(0.0, 15.0))[1], 230 * C.k, 0.8 * float(seg(t, W(3, 'rugina') - 0.1, W(3, 'rugina') + 0.4)))),
 Shot('microz', L(4), L(5), st='mrust1', seq=[('mrust2', W(4, 'umple') - 0.1, W(4, 'umple') + 0.6)], tr=('dive', 0.7, GUIDE_NEEDLE, 3.0),
      kb=[(L(4), 1.0, 0, 0), (L(5), 1.08, 0, 0)], fx=[fx_flakes(L(4), W(4, 'macina') - 0.1)], ov=ov_rust,
      shake=lambda t: (SHK(t), 0.6 * SHK(t + 0.05))),
 Shot('microz', L(5), L(6), st='mclean', seq=[('mwater', W(5, 'apa') - 0.1, W(5, 'apa') + 0.4), ('mclean', W(5, 'iar') - 0.1, W(5, 'iar') + 0.4)],
      kb=[(L(5), 1.0, 0, 0), (L(6), 1.06, 0, 0)], fx=[fx_dry_contact(W(5, 'unge') - 0.1, W(5, 'iar') - 0.1)], ov=ov_lube),
 Shot('tank', L(6), T_FILT, st='dry', seq=[('cond', W(6, 'condensul') - 0.1, W(6, 'condensul') + 1.0)],
      kb=[(L(6), 1.0, 0, 0), (T_FILT, 1.06, 0, -10)], fx=[fx_tank(W(6, 'condensul'), W(6, 'formeaza') - 0.2)], ov=ov_tank),
 Shot('filter', T_FILT, L(8), st='fwlo', seq=[('fwhi', W(7, 'scursa') - 0.1, W(7, 'trece') + 0.2)],
      kb=[(T_FILT, 0.6, 0, -60), (L(8), 0.64, 0, -60)], fx=[fx_filter_sep(T_FILT + 0.3, W(7, 'trece'))], ov=ov_filter7),
 Shot('chamberz', L(8), L(9), st='shut', kb=[(L(8), 1.0, 0, -140), (L(9), 1.05, 0, -150)],
      fx=[lambda C: K.spray_pulses(C, PULSES_S, kind='bad', L=13.0, life=0.42),
          lambda C: F.smoke(C, np.array([0, -7.0, -5.0]), L(8) - 0.5, n=90, rise=(0, 0, 2.5), spread=12.0, size=2.8, a=0.4)], ov=ov_sym,
      dim=lambda t: 0.25 * F.pop(t, W(8, 'pornire') - 0.1, LE(8) + 0.3)),
 Shot('filter', L(9), L(10), st='fwlo', seq=[('shut', W(9, 'apa', 2) + 0.4, W(9, 'apa', 2) + 2.2)],
      kb=[(L(9), 0.6, 0, -60), (L(10), 0.63, 0, -60)], fx=[fx_drain(W(9, 'apa', 2) - 0.1)], ov=ov_filter9),
 Shot('chamberz', L(10), TOTAL + 1, st='shut', kb=[(L(10), 1.0, 0, -60), (TOTAL, 1.1, 0, -80)],
      fx=[lambda C: K.spray_pulses(C, PULSES_E, kind='good', L=14.0, life=0.42)]),
]
