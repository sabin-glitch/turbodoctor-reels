# Episodul 13: uzura normala (Bosch: sistemul proiectat pentru 300.000 km la autoturisme; Delphi: durata medie in service 130-160.000 km;
# cavitatie la scaunul supapei si la duza, arcuri slabite, returul creste, preinjectiile se pierd; duza care curge poate topi pistonul).
# Momentele din ep13/vo/cues.json (provizorii).
import math, json, os
import numpy as np
import icomp as IC, ifx as F, ikit as K, iser as S, i2d as D
import fxlib as X
from icomp import Shot
from fxlib import seg, ease

E = S.Ep(13); N = E.n; EP = E.ep; W, L, LE = E.W, E.L, E.LE; TOTAL = E.TOTAL
GLOB = S.glob(E)
SD = json.load(open(os.path.join(IC.HERE, 'blend', 'seat_dmg.json')))
HOT = np.array([1.0, 0.42, 0.12])

SPR = dict(S.spr_common(N), **{
 'g_bosch': K.lb('BOSCH PROIECTEAZĂ SISTEMUL DE INJECȚIE PENTRU', 'grey'),
 'ic_odo': '<div style="width:110px;height:110px;display:flex;align-items:center;justify-content:center">'
           + D.ICON2['odo'].replace('width="80" height="80"', 'width="100" height="100"') + '</div>',
 'c_cars': K.lb('LA AUTOTURISME', ''),
 'g_delphi': K.lb('DELPHI: DURATA MEDIE ÎN SERVICE', 'grey'),
 'l_cav': K.lb('CAVITAȚIE', 'bad big', 'La scaunul supapei'),
 'l_noz': K.lb('ȘI LA DUZĂ', 'bad big'),
 'l_spring': K.lb('ARCURILE SLĂBESC', 'bad big'),
 'l_ret': K.lb('RETURUL CREȘTE', 'bad'),
 'l_pilot': K.lb('PREINJECȚIILE SE PIERD', 'bad'),
 's_start': K.sym('start', 'PORNIRE GREA'), 's_idle': K.sym('idle', 'RALANTI NEREGULAT'), 's_smoke': K.sym('smoke', 'FUM'),
 'l_drip': K.lb('O DUZĂ CARE CURGE', 'bad'),
 'l_melt': K.lb('POATE TOPI PISTONUL', 'bad big'),
 'g_km': K.lb('LA KILOMETRAJ MARE', 'grey'),
 'c_ret': K.chk('TEST DE RETUR'),
 'c_bench': K.chk('VERIFICARE PE STAND'),
 'g_before': K.lb('ÎNAINTE SĂ CEDEZE UN INJECTOR', 'good'),
})

# ------------------------------------------------------------------ kilometrii: Bosch 300.000, Delphi 130-160.000
def ov_km(C):
    t = C.t
    F.spr(C, 'g_bosch', 540, 390, L(3) - 0.05, LE(3) + 0.3, anchor='tc')
    a = F.pop(t, L(3) - 0.05, L(4) + 0.1)
    if a > 0.003:
        D.rbox(C, 140, 500, 800, 230, (255, 210, 31), a, th=3, fill=(8, 12, 17, 238), r=20)
        F.spr(C, 'ic_odo', 170, 560, L(3) - 0.05, L(4) + 0.1, popk=1.0, slide=(0, 0))
        v = 300000 * float(ease(float(seg(t, L(3) + 0.2, W(3, 'kilometri') + 0.1))))
        D.text(C, D.fmt_km(v), 760, 615, 128, (255, 255, 255), a, 'anton', anchor='rm')
        D.text(C, 'KM', 790, 640, 60, (255, 210, 31), a, 'anton', anchor='lm')
    F.spr(C, 'c_cars', 540, 770, W(3, 'autoturisme') - 0.1, L(4) + 0.1, anchor='tc')
    # scala: proiectat 300.000 (Bosch) si media in service 130-160.000 (Delphi)
    F.spr(C, 'g_delphi', 540, 390, L(4) - 0.05, LE(4) + 0.35, anchor='tc')
    a4 = F.pop(t, L(4) - 0.1, LE(4) + 0.35)
    if a4 <= 0.003: return
    x0, x1, y, kmax = 120, 960, 800, 320000.0
    def XK(km): return x0 + (x1 - x0) * km / kmax
    D.line2(C, [(x0, y), (x1, y)], (150, 160, 172), 8, a4)
    for km in range(0, 300001, 50000):
        D.line2(C, [(XK(km), y - 16), (XK(km), y + 16)], (150, 160, 172), 4, a4)
        if km % 100000 == 0: D.text(C, D.fmt_km(km), XK(km), y + 52, 26, (182, 194, 207), a4, 'mont9')
    D.dots2(C, np.array([[XK(300000), y]]), 18, (61, 220, 132), a4, glow=0.6)
    D.text(C, 'PROIECTAT · BOSCH', XK(300000), y - 120, 28, (61, 220, 132), a4, 'mont9', anchor='rm')
    D.text(C, '300.000', XK(300000), y - 70, 54, (61, 220, 132), a4, 'anton', anchor='rm')
    pb = float(seg(t, W(4, '130') - 0.1, W(4, '160') + 0.3))
    ab = a4 * float(seg(t, W(4, '130') - 0.15, W(4, '130') + 0.1))
    if ab > 0.003:
        xa, xb = XK(130000), XK(130000 + 30000 * max(pb, 0.02))
        D.rbox(C, xa, y - 26, xb - xa, 52, (255, 178, 36), ab, th=2, fill=(255, 178, 36, 235), r=8)
        D.text(C, 'MEDIA ÎN SERVICE · DELPHI', XK(145000), y + 130, 28, (255, 178, 36), ab, 'mont9')
        D.text(C, '130–160.000 KM', XK(145000), y + 180, 54, (255, 178, 36), ab * float(seg(t, W(4, '160') - 0.1, W(4, '160') + 0.2)), 'anton')

# ------------------------------------------------------------------ cavitatia la scaun, duza, arcurile
PITS = [np.array(p[0], float) for p in SD['pits']]
def fx_cav(t_on):
    def f(C):
        t = C.t
        if t < t_on: return
        for i in range(0, len(PITS), 2):
            per = 0.55 + 0.1 * (i % 3); u = ((t - t_on) + i * 0.13) % per / per
            p = PITS[i] + F.EZ * 0.012
            if u < 0.7: F.dots3(C, p, 0.02 + 0.035 * u / 0.7, np.array([0.85, 0.93, 1.0]), 0.85, shape='r', shade=0.0, ztest=False)
            else: F.glow(C, p, 40 * C.k * (1 - (u - 0.7) / 0.3), np.array([0.8, 0.92, 1.0]), 0.6 * (1 - (u - 0.7) / 0.3))
    return f

SPRING = [np.array([0, 0, z], float) for z in np.linspace(156.0, 166.0, 6)]
def fx_spring(t_on):
    def f(C):
        e = float(seg(C.t, t_on, t_on + 0.3))
        if e <= 0.01: return
        for p in SPRING: F.glow(C, p, 95 * C.k, np.array([1.0, 0.35, 0.25]), 0.45 * e * (0.7 + 0.3 * math.sin(C.t * 8)))
    return f

# ------------------------------------------------------------------ returul creste, preinjectiile se pierd
def ov_ret(C):
    t = C.t; a = F.pop(t, L(6) - 0.1, L(7) + 0.2)
    if a <= 0.003: return
    # tubul de retur
    tx, ty, tw, th = 200, 470, 120, 360
    D.rbox(C, tx, ty, tw, th, (205, 212, 220), a, th=4, r=14)
    v = 0.3 + 0.48 * float(seg(t, W(6, 'returul') + 0.1, W(6, 'creste') + 0.5))
    col = (255, 178, 36) if v < 0.55 else (255, 75, 75)
    D.rbox(C, tx + 10, ty + 10 + (th - 20) * (1 - v), tw - 20, (th - 20) * v, col, a, th=1, fill=(*col, 230), r=8)
    for k in range(1, 6): D.line2(C, [(tx + tw - 34, ty + th * k / 6), (tx + tw - 10, ty + th * k / 6)], (205, 212, 220), 3, a)
    F.spr(C, 'l_ret', tx + tw + 40, ty + 40, W(6, 'returul') - 0.1, L(7) + 0.2)
    # trasa injectiilor: preinjectie mica + injectia principala; preinjectiile dispar
    bx0, by = 120, 1170; kp = 1 - float(seg(t, W(6, 'preinjectiile') + 0.1, W(6, 'pierd') + 0.3))
    pts = [(bx0, by)]
    for c in range(3):
        x = bx0 + 40 + c * 280
        hp = 70 * kp
        pts += [(x, by), (x, by - hp), (x + 36, by - hp), (x + 36, by), (x + 90, by), (x + 90, by - 230), (x + 200, by - 230), (x + 200, by)]
    pts.append((bx0 + 860, by))
    D.line2(C, pts, (255, 210, 31), 6, a)
    if kp < 0.98:
        for c in range(3):
            x = bx0 + 58 + c * 280
            ax = a * (1 - kp)
            D.line2(C, [(x - 22, by - 92), (x + 22, by - 48)], (255, 75, 75), 7, ax); D.line2(C, [(x + 22, by - 92), (x - 22, by - 48)], (255, 75, 75), 7, ax)
    F.spr(C, 'l_pilot', 540, 860, W(6, 'preinjectiile') - 0.1, L(7) + 0.2, anchor='tc')

# ------------------------------------------------------------------ duza care curge topeste pistonul
RP = X.rnd(97, 20, 4)
def fx_melt(t_on):
    def f(C):
        t = C.t
        for i in range(6):                                   # picaturi care cad din varful duzei pe piston
            ta = t_on + i * 0.45
            if t < ta: continue
            u = (t - ta) % 2.7
            if u < 0.5: F.dots3(C, np.array([0.0, -1.0, 0.4 - 0.3 * u]), 0.25 + 0.35 * u, np.array([1.0, 0.75, 0.3]), 1.0, shade=0.5, ztest=False)
            elif u < 0.9: F.dots3(C, np.array([0.0, -1.0, 0.25 - 2.0 * (u - 0.5)]), 0.4, np.array([1.0, 0.75, 0.3]), 1.0, shade=0.5, ztest=False)
        e = float(seg(t, t_on + 0.6, t_on + 2.2))
        if e <= 0.01: return
        pu = 0.8 + 0.2 * math.sin(t * 7)
        for P, r in ((np.array([0, -1.0, -0.6]), 150), (F.PR(7.0, -6.0), 130), (F.PLf(7.0, -6.0), 130), (F.PR(13.0, -11.0), 110), (F.PLf(13.0, -11.0), 110)):
            F.glow(C, np.asarray(P, float), r * C.k, HOT, 0.42 * e * pu)
        F.smoke(C, np.array([0, -2.0, -2.0]), t_on + 1.0, n=60, rise=(0, 0, 6.0), spread=8.0, size=3.5, a=0.3)
    return f

def ov_melt(C):
    F.label(C, 'l_drip', [0, -1.0, 0.6], (620, 560), W(7, 'duza') - 0.1, LE(7) + 0.3)
    F.spr(C, 'l_melt', 540, 1150, W(7, 'topi') - 0.1, LE(7) + 0.3, anchor='tc')

# ------------------------------------------------------------------ cum eviti: testul de retur si standul
LV = [0.31, 0.29, 0.74, 0.33]
def ov_do(C):
    t = C.t
    F.spr(C, 'g_km', 540, 390, W(8, 'kilometraj') - 0.15, LE(8) + 0.35, anchor='tc')
    F.spr(C, 'c_ret', 540, 478, W(8, 'test') - 0.1, LE(8) + 0.35, anchor='tc')
    F.spr(C, 'c_bench', 540, 566, W(8, 'verificare') - 0.1, LE(8) + 0.35, anchor='tc')
    a = F.pop(t, W(8, 'retur') - 0.2, LE(8) + 0.35)
    if a > 0.003:
        pr = float(seg(t, W(8, 'retur'), W(8, 'retur') + 1.6))
        for k in range(4):
            x = 300 + k * 140; y0, h = 700, 330
            D.rbox(C, x, y0, 80, h, (205, 212, 220), a, th=4, r=12)
            v = LV[k] * pr; col = (255, 75, 75) if k == 2 and v > 0.45 else (255, 192, 42)
            if v > 0.01: D.rbox(C, x + 8, y0 + 8 + (h - 16) * (1 - v), 64, (h - 16) * v, col, a, th=1, fill=(*col, 230), r=6)
            D.text(C, 'INJ. %d' % (k + 1), x + 40, y0 + h + 34, 26, (182, 194, 207), a, 'mont9')
    F.spr(C, 'g_before', 540, 1130, W(8, 'inainte') - 0.1, LE(8) + 0.35, anchor='tc')

# ------------------------------------------------------------------ planuri
PIT8 = PITS[8]
SYM = S.symptoms(E, 7, [('s_start', 'pornire'), ('s_idle', 'ralanti'), ('s_smoke', 'fum')])
SYM.t1 = W(7, 'iar') - 0.1
SHOTS = S.opening(E) + [
 Shot('hero', L(3), L(5), st='full', tr=('xf', 0.3), kb=[(L(3), 1.0, 0, 0), (L(5), 1.06, 0, -20)], ov=ov_km, dim=lambda t: 0.62),
 Shot('seattop', L(5), W(5, 'duza') - 0.15, st='tclean', seq=[('tpits', W(5, 'cavitatia') - 0.1, W(5, 'scaunul') + 0.2)], tr=('xf', 0.3),
      kb=[(L(5), 1.0, 0, 0), (W(5, 'duza'), 1.1, 0, 0)], fx=[fx_cav(W(5, 'cavitatia') - 0.3)],
      ov=lambda C: F.spr(C, 'l_cav', 540, 1130, W(5, 'cavitatia') - 0.1, W(5, 'duza'), anchor='tc')),
 Shot('tipw', W(5, 'duza') - 0.15, W(5, 'arcurile') - 0.15, st='worn', tr=('xf', 0.2), kb=[(W(5, 'duza'), 1.0, 0, -330), (W(5, 'arcurile'), 1.04, 0, -340)],
      ov=lambda C: F.spr(C, 'l_noz', 540, 1130, W(5, 'duza') - 0.1, W(5, 'arcurile'), anchor='tc')),
 Shot('upper', W(5, 'arcurile') - 0.15, L(6), st='shut', tr=('xf', 0.2), kb=[(W(5, 'arcurile'), 1.1, 0, 160), (L(6), 1.16, 0, 190)],
      fx=[fx_spring(W(5, 'arcurile') - 0.1)], ov=lambda C: F.spr(C, 'l_spring', 540, 440, W(5, 'arcurile') - 0.1, L(6) + 0.2, anchor='tc')),
 Shot('blank', L(6), L(7), st='none', tr=('xf', 0.25), ov=ov_ret),
 SYM,
 Shot('chamber', W(7, 'iar') - 0.1, L(8), st='shut', tr=('xf', 0.3), kb=[(W(7, 'iar'), 1.0, 0, -80), (L(8), 1.08, 0, -100)],
      fx=[fx_melt(W(7, 'duza') - 0.2)], ov=ov_melt),
 Shot('hero', L(8), L(E.OUT), st='full', tr=('xf', 0.3), kb=[(L(8), 1.0, 0, 0), (L(E.OUT), 1.04, 0, -20)], ov=ov_do,
      dim=lambda t: 0.62 * F.pop(t, L(8) - 0.1, L(E.OUT) + 0.3)),
 S.ending(E),
]
