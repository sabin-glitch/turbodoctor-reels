# Episodul 7: benzina pusa din greseala (ADAC, RAC). Pelicula de ungere spalata in pompa, metal pe metal, pilitura in tot sistemul.
# Momentele din ep7/vo/cues.json (provizorii).
import math, json, os
import numpy as np
import icomp as IC, ifx as F, ikit as K, iser as S, i2d as D
import fxlib as X
from icomp import Shot
from fxlib import seg

E = S.Ep(7); N = E.n; EP = E.ep; W, L, LE = E.W, E.L, E.LE; TOTAL = E.TOTAL
GLOB = S.glob(E)
PETROL = np.array([0.72, 0.95, 0.32]); METAL = (225, 230, 238)
TJ = json.load(open(os.path.join(IC.HERE, 'blend', 'tank.json')))

def sym2(icon, text, small=None, cls='warn'):
    s = '<small>%s</small>' % small if small else ''
    return '<div class="sym %s"><div class="ic">%s</div><div class="tx">%s%s</div></div>' % (cls, D.ICON2[icon], text, s)
def stop(icon_svg, text, small=None):
    s = '<small>%s</small>' % small if small else ''
    return '<div class="stop"><div class="ic">%s</div><div>%s%s</div></div>' % (icon_svg, text, s)
DROP_B = D.ICON2['drop'].replace('#ffc02a', '#b8f04f')

SPR = dict(S.spr_common(N), **{
 'tag_pump': K.lb('ÎN POMPA DE ÎNALTĂ PRESIUNE', 'grey', 'Vedere la microscop'),
 'l_film': K.lb('PELICULA DE UNGERE', 'lp'),
 'l_benz': K.lb('BENZINA O SPALĂ', 'bad'),
 'l_metal': K.lb('METAL PE METAL', 'bad big'),
 'sys': D.sys_svg(),
 'h_pump': D.sys_hl(['pump']), 'h_inj': D.sys_hl(['inj']), 'h_rail': D.sys_hl(['rail']), 'h_pipes': D.sys_hl(['hp', 'lp']),
 'h_filter': D.sys_hl(['filter']), 'h_tank': D.sys_hl(['tank']),
 'l_fil': K.lb('PILITURĂ ÎN TOT SISTEMUL', 'bad', 'Până în injectoare'),
 'chip_run': '<div class="lb bad big">DACĂ MOTORUL A MERS</div>',
 'g_repl': K.lb('REPARAȚIA POATE CUPRINDE', 'grey'),
 'q_adac': '<div class="quote mid red"><q>ȘI CANTITĂȚILE MICI POT FACE RĂU</q><small>Avertismentul ADAC despre benzina pusă în rezervorul de motorină</small></div>',
 'x_key': K.chk('NU PUI CONTACTUL', False),
 'x_start': K.chk('NU PORNEȘTI MOTORUL', False),
 'c_tow': K.chk('CHEMI TRACTAREA'),
 'c_drain': K.chk('REZERVORUL SE GOLEȘTE'),
 'st_winter': stop(K.ICON['cold'], 'IARNA, NU AMESTECA', 'Motorina cu benzină'),
 'd_dies': '<div style="text-align:center">' + D.ICON2['drop'].replace('width="80" height="80"', 'width="150" height="150"') + '<div class="lb lp" style="margin-top:8px">MOTORINĂ</div></div>',
 'd_benz': '<div style="text-align:center">' + DROP_B.replace('width="80" height="80"', 'width="150" height="150"') + '<div class="lb" style="margin-top:8px;border-color:#b8f04f">BENZINĂ</div></div>',
})

# ------------------------------------------------------------------ vederea micro: motorina, apoi benzina care spala pelicula
def gap_path():
    gp = F.IPath([[0, -0.1, 26], [0, -0.1, -26]], None, 1.0, smooth=0, step=0.25)
    gp.L = np.tile(np.array([0.6, 0, 0]), (gp.n, 1)); return gp
GP = gap_path()

def fx_gap(t_benz=None, t_dry=None):
    def f(C):
        t = C.t
        ka = 1.0 if t_dry is None else 1 - float(seg(t, t_dry - 0.2, t_dry + 0.8))
        if ka > 0.01: F.flow(C, GP, 30, 13.0, np.array([1.0, 0.75, 0.5]), 0.12, lat=0.9, seed=5, mode='add', shape='g', shade=0, a=0.45 * ka)
        if t_benz is not None and t > t_benz - 0.3:
            kb = float(seg(t, t_benz - 0.3, t_benz + 0.3)) * (1 - float(seg(t, (t_dry or 1e9) + 0.8, (t_dry or 1e9) + 1.6)))
            if kb > 0.01: F.flow(C, GP, 26, 20.0, PETROL, 0.32, lat=0.95, seed=17, t0=t_benz - 0.3, mode='over', shape='d', shade=0.45, a=0.95 * kb, glow=0.35, sz_var=0.5)
    return f

RM = X.rnd(55, 40, 4)
def fx_grind(t_on):
    """metal pe metal: scantei pe pereti si fulgi de metal desprinsi"""
    def f(C):
        t = C.t
        if t < t_on: return
        for i in range(8):
            ta = t_on + (i * 0.37) % 1.6 + 1.6 * int(i * 0.37 / 1.6)
            per = 1.3 + 0.4 * RM[i, 3]; tk = ta + per * math.floor(max(0.0, t - ta) / per)
            side = -0.1 if i % 2 else 0.1; z = 16 - 32 * RM[i, 0]
            F.sparks(C, np.array([side, -0.15, z]), tk, n=16, life=0.3, speed=6.0, size=0.12, seed=110 + i + int(tk * 10))
        F.flow(C, GP, 18, 9.0, np.array([0.88, 0.9, 0.94]), 0.16, lat=0.3, seed=23, t0=t_on + 0.2, mode='over', shape='d', shade=0.8, sz_var=0.6)
    return f

def ov_micro(C):
    F.spr(C, 'tag_pump', 540, 400, W(3, 'pompa') - 0.15, W(4, 'pilitura') - 0.1, anchor='tc')
    F.label(C, 'l_film', [0.0, -0.1, 6.0], (90, 640), W(3, 'pelicula') - 0.1, W(3, 'pompa') - 0.15)
    F.label(C, 'l_benz', [0.4, -0.1, -5.0], (1040, 1150), W(3, 'spala') - 0.1, LE(3) + 0.2, anchor='tr')
    F.spr(C, 'l_metal', 540, 1150, W(4, 'metal') - 0.1, W(4, 'pilitura') - 0.1, anchor='tc')

def shake4(t):
    ta = W(4, 'metal') - 0.1
    e = float(seg(t, ta, ta + 0.1)) * (1 - float(seg(t, ta + 0.9, ta + 1.3)))
    return (4.0 * e * math.sin(t * 57.0), 3.0 * e * math.sin(t * 43.0 + 0.7))

# ------------------------------------------------------------------ schema: pilitura pleaca din pompa spre injectoare, apoi tot ce se schimba
SP = D.sys_paths()
def ov_sys(C):
    t = C.t; t0 = W(4, 'pilitura') - 0.15
    F.spr(C, 'sys', D.SYS_X, D.SYS_Y, t0, L(6) + 0.2, popk=1.0, slide=(0, 0))
    a = F.pop(t, t0, L(6) + 0.2)
    D.flow2(C, SP['inj'], 70, 260.0, METAL, 4.0, t0=W(4, 'pilitura'), a=a, seed=3, glow=0.5)
    F.spr(C, 'h_inj', D.SYS_X, D.SYS_Y, W(4, 'injectoare') - 0.1, W(4, 'injectoare') + 1.2, popk=1.0, slide=(0, 0))
    F.spr(C, 'l_fil', 540, 400, W(4, 'pilitura') - 0.1, LE(4) + 0.3, anchor='tc')
    # reparatia: componentele se aprind una cate una
    F.spr(C, 'chip_run', 540, 380, L(5) - 0.05, LE(5) + 0.4, anchor='tc')
    for sid, w in (('h_pump', 'pompa'), ('h_inj', 'injectoarele'), ('h_rail', 'rampa'), ('h_pipes', 'tevile'), ('h_filter', 'filtrul'), ('h_tank', 'rezervorul')):
        F.spr(C, sid, D.SYS_X, D.SYS_Y, W(5, w) - 0.1, LE(5) + 0.4, popk=1.0, slide=(0, 0))

# ------------------------------------------------------------------ rezervorul: picaturi de benzina; ce faci; iarna
RD = X.rnd(71, 20, 3)
def fx_petrol_drops(t_on):
    def f(C):
        t = C.t
        for i in range(9):
            ta = t_on + i * 0.36
            if t < ta: continue
            u = t - ta; x = -212 + 22 * RD[i, 0]; y = 90; z = 168 - 0.5 * 900 * u * u
            if z < 101:
                tz = math.sqrt(2 * (168 - 101) / 900.0); du = u - tz
                if du < 0.5: F.glow(C, np.array([x, y, 101.0]), (60 + 120 * du) * C.k, PETROL, 0.45 * (1 - du / 0.5))
                continue
            F.dots3(C, np.array([x, y, z]), 4.5, PETROL, 1.0, shade=0.6, ztest=False)
    return f

def ov_adac(C):
    F.spr(C, 'q_adac', 540, 390, W(6, 'adac') - 0.1, LE(6) + 0.35, anchor='tc')

def ov_do(C):
    for k, (sid, w) in enumerate((('x_key', 'contactul'), ('x_start', 'pornesti'), ('c_tow', 'tractarea'), ('c_drain', 'goleste'))):
        F.spr(C, sid, 540, 380 + 86 * k, W(7, w) - 0.1, LE(7) + 0.3, anchor='tc')

RW = np.random.RandomState(12).rand(90, 4)
def ov_winter(C):
    t = C.t; a = F.pop(t, L(8) - 0.1, L(E.OUT) + 0.2, 0.4, 0.3)
    if a > 0.003:
        P = np.stack([(RW[:, 0] * 1180 - 50 + 40 * np.sin(t * 0.8 + RW[:, 3] * 6)) % 1080, (RW[:, 1] * 1920 + t * (70 + 60 * RW[:, 2])) % 1920], -1)
        D.dots2(C, P, 3.0 + 4.0 * RW[:, 2], (235, 245, 255), 0.75 * a)
    F.spr(C, 'st_winter', 540, 520, W(8, 'iarna') - 0.15, LE(8) + 0.35, anchor='tc')
    F.spr(C, 'd_dies', 320, 860, W(8, 'motorina') - 0.1, LE(8) + 0.35, anchor='tc')
    F.spr(C, 'd_benz', 760, 860, W(8, 'benzina') - 0.1, LE(8) + 0.35, anchor='tc')
    D.text(C, '+', 540, 950, 110, (232, 237, 243), a * float(seg(t, W(8, 'benzina') - 0.1, W(8, 'benzina') + 0.2)), 'anton')
    ax = a * float(seg(t, W(8, 'benzina') + 0.25, W(8, 'benzina') + 0.5))
    if ax > 0:
        D.line2(C, [(230, 840), (850, 1150)], (255, 75, 75), 16, ax); D.line2(C, [(850, 840), (230, 1150)], (255, 75, 75), 16, ax)

# ------------------------------------------------------------------ planuri
GUIDE = S.scr('hero', 'shut', [0, 0, 22.0], (1.07, 0, -30))
SHOTS = S.opening(E, 'microf', np.array([0, 0, 22.0]), dive_kb=((1.0, 0, 0), (1.0, 0, 0)), dive_st='mclean', zmax=3.0,
                  fx_dive=[fx_gap()]) + [
 Shot('microf', L(3), L(4), st='mclean', seq=[('mdry0', W(3, 'spala') - 0.1, W(3, 'pelicula') + 0.6)], kb=[(L(3), 1.0, 0, 0), (L(4), 1.05, 0, 0)],
      fx=[fx_gap(W(3, 'benzina') - 0.2, W(3, 'spala'))], ov=ov_micro),
 Shot('microf', L(4), W(4, 'pilitura') - 0.1, st='mdry0', seq=[('mdry', W(4, 'metal') - 0.22, W(4, 'metal') + 0.06)], kb=[(L(4), 1.05, 0, 0), (W(4, 'pilitura'), 1.12, 0, 0)], shake=shake4,
      fx=[fx_grind(W(4, 'metal') - 0.2)], ov=ov_micro),
 Shot('blank', W(4, 'pilitura') - 0.1, L(6), st='none', tr=('xf', 0.3), ov=ov_sys),
 Shot('tank', L(6), L(8), st='dry', seq=[('empty', W(7, 'goleste') - 0.1, W(7, 'goleste') + 1.2)], tr=('xf', 0.3),
      kb=[(L(6), 1.0, 0, 0), (L(8), 1.06, 0, -10)], fx=[fx_petrol_drops(W(6, 'cantitatile') - 0.4)], ov=[ov_adac, ov_do],
      dim=lambda t: 0.3 * F.pop(t, W(6, 'adac') - 0.1, LE(6) + 0.35)),
 Shot('blank', L(8), L(E.OUT), st='none', tr=('xf', 0.3), ov=ov_winter),
 S.ending(E),
]
