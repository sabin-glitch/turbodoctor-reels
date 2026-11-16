# Episodul 9: motorina care nu unge (Bosch, Delphi, Denso: lubrifierea si cel mult 7% biodiesel; biodieselul degradat; uleiul de incalzire,
# uleiul vegetal; aerul din sistem). Momentele din ep9/vo/cues.json (provizorii).
import math, json, os
import numpy as np
import icomp as IC, ifx as F, ikit as K, iser as S, i2d as D
import fxlib as X
from icomp import Shot
from fxlib import seg

E = S.Ep(9); N = E.n; EP = E.ep; W, L, LE = E.W, E.L, E.LE; TOTAL = E.TOTAL
GLOB = S.glob(E)
AMBER = np.array([1.0, 0.75, 0.5]); GUM = np.array([0.40, 0.25, 0.10]); AIR = np.array([0.86, 0.93, 1.0]); RED = np.array([1.0, 0.32, 0.2])
FJ = json.load(open('/home/claude/w/inj/out/filter.json'))
TJ = json.load(open(os.path.join(IC.HERE, 'blend', 'tank.json')))

def sym2(icon, text, small=None, cls='warn'):
    s = '<small>%s</small>' % small if small else ''
    return '<div class="sym %s"><div class="ic">%s</div><div class="tx">%s%s</div></div>' % (cls, D.ICON2[icon], text, s)

B7 = ('<div style="display:flex;flex-direction:column;align-items:center"><div style="display:flex;width:150px;height:150px;border:8px solid #fff;border-radius:14px;'
      'align-items:center;justify-content:center;font:400 84px/1 Anton;color:#fff;background:rgba(8,12,17,.92)">B7</div>'
      '<div class="lb grey" style="margin-top:14px">PE POMPĂ</div></div>')

SPR = dict(S.spr_common(N), **{
 'tag_gap': K.lb('ÎNTRE AC ȘI CORPUL DUZEI', 'grey', 'Vedere la microscop'),
 'l_film': K.lb('PELICULA DE MOTORINĂ', 'lp'),
 'l_only': K.lb('SINGURUL LUBRIFIANT', 'lp big', 'Pelicula de motorină dintre piese'),
 'c_pump': K.lb('POMPA DE ÎNALTĂ PRESIUNE', 'lp'),
 'c_inj': K.lb('INJECTOARELE', 'lp'),
 'g_req': K.lb('CE CER PRODUCĂTORII DE INJECȚIE', 'grey'),
 'c_lube': K.chk('MOTORINĂ CARE UNGE SUFICIENT'),
 'c_b7': K.chk('CEL MULT 7% BIODIESEL'),
 'b7': B7,
 'l_bio': K.lb('BIODIESEL VECHI SAU PROST'),
 'l_acid': K.lb('ACIZI ȘI DEPUNERI', 'bad'),
 'l_clog': K.lb('FILTRUL SE ÎNFUNDĂ', 'bad'),
 'l_stick': K.lb('PIESELE SE LIPESC', 'bad big'),
 'c_heat': sym2('barrel', 'ULEI DE ÎNCĂLZIRE'),
 'x_heat': K.chk('NU UNGE DESTUL', False),
 'c_veg': sym2('oil', 'ULEI VEGETAL'),
 'x_visc': K.chk('PREA VÂSCOS', False),
 'x_dep': K.chk('LASĂ DEPUNERI', False),
 'l_empty': K.lb('REZERVOR GOL', 'bad'),
 'l_air': K.lb('AERUL ÎMPIEDICĂ UNGEREA', 'bad big'),
 'l_nofilm': K.lb('FĂRĂ PELICULĂ', 'bad'),
 'l_metal': K.lb('METAL PE METAL', 'bad big'),
 'l_noz': K.lb('DUZELE SE LIPESC', 'bad big'),
 'l_valve': K.lb('SUPAPELE CEDEAZĂ', 'bad big'),
 'c_std': K.chk('MOTORINĂ STANDARD'),
 'c_station': K.chk('DE LA BENZINĂRII SERIOASE'),
 'c_mix': K.chk('FĂRĂ AMESTECURI'),
 'c_last': K.chk('NU MERGI PÂNĂ LA ULTIMA PICĂTURĂ'),
})

# ------------------------------------------------------------------ acul in ghidaj: pelicula de motorina (deschiderea) si acul care se lipeste
def guide_paths(r=1.43, z0=52.0, z1=21.0):
    return [F.IPath([list(F.PR(r, z0)), list(F.PR(r, z1))], None, 1.0, smooth=0, step=0.5),
            F.IPath([list(F.PLf(r, z0)), list(F.PLf(r, z1))], None, 1.0, smooth=0, step=0.5)]
GPATHS = guide_paths()

def fx_film_guide(t_on):
    def f(C):
        a = float(seg(C.t, t_on, t_on + 0.6))
        if a <= 0.01: return
        for p, s in zip(GPATHS, (61, 62)):
            F.flow(C, p, 34, 9.0, AMBER, 0.32, lat=0.0, seed=s, mode='add', shape='g', shade=0, a=0.55 * a)
    return f

def fx_stuck(t_on):
    def f(C):
        a = float(seg(C.t, t_on, t_on + 0.25))
        if a <= 0.01: return
        pu = 0.75 + 0.25 * math.sin(C.t * 9)
        p0 = C.P(F.PLf(1.43, 39.0)); p1 = C.P(F.PR(1.43, 22.0))
        x0, y0, x1, y1 = p0[0] / C.k - 44, p0[1] / C.k, p1[0] / C.k + 44, p1[1] / C.k
        D.rbox(C, x0, y0, x1 - x0, y1 - y0, (255, 75, 75), a * pu, th=6, fill=(255, 75, 75, 40), r=18)
    return f

def shake_at(ta, dur=0.7, amp=3.0):
    def sh(t):
        e = float(seg(t, ta, ta + 0.06)) * (1 - float(seg(t, ta + dur * 0.6, ta + dur)))
        return (amp * e * math.sin(t * 61.0), 0.7 * amp * e * math.sin(t * 47.0 + 0.4))
    return sh

# ------------------------------------------------------------------ vederea micro: pelicula, aerul, metal pe metal
def gap_path(lat=0.6):
    gp = F.IPath([[0, -0.1, 26], [0, -0.1, -26]], None, 1.0, smooth=0, step=0.25)
    gp.L = np.tile(np.array([lat, 0, 0]), (gp.n, 1)); return gp
GP = gap_path(); GPA = gap_path(0.5)

def fx_film(a=0.45, t_off=None):
    def f(C):
        k = 1.0 if t_off is None else 1 - float(seg(C.t, t_off - 0.2, t_off + 0.6))
        if k > 0.01: F.flow(C, GP, 30, 13.0, AMBER, 0.12, lat=0.9, seed=5, mode='add', shape='g', shade=0, a=a * k)
    return f

def fx_air(t_on, t_off):
    def f(C):
        k = 1 - float(seg(C.t, t_off - 0.2, t_off + 0.5))
        if k > 0.01: F.flow(C, GPA, 9, 6.0, AIR, 0.9, lat=0.45, seed=9, t0=t_on, mode='over', shape='d', shade=0.75, a=0.95 * k, sz_var=0.45)
    return f

RM = X.rnd(55, 40, 4)
def fx_grind(t_on):
    """metal pe metal (jocul inchis): scantei pe linia de contact si fulgi de metal"""
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

def ov_micro3(C):
    F.spr(C, 'tag_gap', 540, 400, L(3) + 0.1, LE(3) + 0.2, anchor='tc')
    F.label(C, 'l_only', [0.0, -0.1, 6.0], (90, 640), L(3) + 0.3, LE(3) + 0.2)
    F.spr(C, 'c_pump', 540, 1060, W(3, 'pompei') - 0.1, LE(3) + 0.2, anchor='tc')
    F.spr(C, 'c_inj', 540, 1150, W(3, 'injectoarelor') - 0.1, LE(3) + 0.2, anchor='tc')

def ov_micro8(C):
    F.spr(C, 'l_air', 540, 420, W(7, 'impiedica') - 0.2, LE(7) + 0.3, anchor='tc')
    F.label(C, 'l_nofilm', [0.0, -0.1, 6.0], (90, 640), W(8, 'pelicula') - 0.1, W(8, 'freaca') + 0.2)
    F.spr(C, 'l_metal', 540, 1150, W(8, 'metal') - 0.1, W(8, 'duzele') + 0.1, anchor='tc')

# ------------------------------------------------------------------ ce cer producatorii: motorina care unge, cel mult 7% biodiesel
RW = np.random.RandomState(19).rand(70, 4)
def ov_spec(C):
    t = C.t; a = F.pop(t, L(4) - 0.1, L(5) + 0.2, 0.4, 0.3)
    if a > 0.003:
        P = np.stack([(RW[:, 0] * 1080 + 30 * np.sin(t * 0.7 + RW[:, 3] * 6)) % 1080, (RW[:, 1] * 1920 - t * (40 + 50 * RW[:, 2])) % 1920], -1)
        D.dots2(C, P, 3.0 + 5.0 * RW[:, 2], (255, 192, 42), 0.35 * a, glow=0.6)
    # cine cere: pozitia comuna a producatorilor de echipamente de injectie (2009), pana apar cerintele
    ac = F.pop(t, L(4) + 0.05, W(4, 'unge') + 0.1, 0.3, 0.3)
    if ac > 0.003:
        D.rbox(C, 170, 600, 740, 470, (110, 120, 132), ac, th=2, fill=(8, 12, 17, 225), r=18)
        D.text(C, 'POZIȚIA COMUNĂ · 2009', 540, 648, 28, (182, 194, 207), ac, 'mont9')
        for k, nm in enumerate(('BOSCH', 'DELPHI', 'DENSO', 'SIEMENS VDO', 'STANADYNE')):
            an = ac * float(seg(t, W(4, 'echipamente') - 0.1 + 0.14 * k, W(4, 'echipamente') + 0.12 + 0.14 * k))
            D.text(C, nm, 540, 716 + 60 * k, 60, (255, 255, 255), an, 'anton')
        D.text(C, 'Cerințe pentru motorină', 540, 1034, 26, (150, 160, 172), ac, 'mont')
    F.spr(C, 'g_req', 540, 400, L(4) - 0.05, LE(4) + 0.3, anchor='tc')
    F.spr(C, 'c_lube', 540, 500, W(4, 'unge') - 0.1, LE(4) + 0.3, anchor='tc')
    ap = a * float(seg(t, W(4, 'cel') - 0.2, W(4, 'cel') + 0.1))
    if ap > 0.003:
        pr = float(seg(t, W(4, 'cel') - 0.1, W(4, '7') + 0.5))
        D.pie(C, 450, 830, 175, [0.07, 0.93], [(61, 220, 132), (255, 192, 42)], pr, ap, hole=0.6)
        D.text(C, '7%', 450, 830, 92, (61, 220, 132), ap * float(seg(t, W(4, '7') - 0.1, W(4, '7') + 0.25)), 'anton')
    F.spr(C, 'b7', 860, 700, W(4, 'biodiesel') - 0.1, LE(4) + 0.3, anchor='tc')
    F.spr(C, 'c_b7', 540, 1060, W(4, '7') - 0.1, LE(4) + 0.3, anchor='tc')

# ------------------------------------------------------------------ biodieselul degradat: acizi si depuneri, filtrul se infunda
RG = X.rnd(91, 420, 4)
PIN = F.IPath(FJ['paths']['in'][1:], 'L', 3.0, smooth=6, step=0.5)
def fx_gum(t_on, t_clog):
    def f(C):
        t = C.t
        F.flow(C, PIN, 40, 70.0, AMBER, 0.9, lat=0.7, seed=12, mode='add', shape='g', shade=0, a=0.5)
        F.flow(C, PIN, 24, 60.0, GUM, 1.5, lat=0.7, seed=19, t0=t_on, mode='over', shape='d', shade=0.5, sz_var=0.6)
        e = float(seg(t, t_clog - 0.6, t_clog + 1.6))
        n = int(420 * e)
        if n <= 0: return
        side = (np.arange(n) % 2 == 0)[:, None]
        U = np.where(side, F.UR[None, :], F.UL[None, :]); Nn = np.where(side, F.NR[None, :], F.NL[None, :])
        P = U * (25.6 + RG[:n, 0:1] * 8.0) + F.EZ[None, :] * (48.0 + RG[:n, 1:2] * 90.0) + Nn * 0.5
        big = RG[:n, 3] > 0.82
        F.dots3(C, P, np.where(big, 1.7 + RG[:n, 2] * 1.1, 0.8 + RG[:n, 2] * 0.7), GUM, np.where(big, 1.0, 0.6), shade=0.5)
    return f

def ov_filter(C):
    F.spr(C, 'l_bio', 540, 380, L(5) - 0.05, W(5, 'filtrele') + 0.3, anchor='tc')
    F.label(C, 'l_acid', list(F.PR(36.2, 118.0)), (620, 540), W(5, 'acizi') - 0.1, LE(5) + 0.3)
    F.label(C, 'l_clog', FJ['pts']['paper'], (600, 1130), W(5, 'filtrele') - 0.1, LE(5) + 0.3)

# ------------------------------------------------------------------ uleiul de incalzire, uleiul vegetal; rezervorul gol
def ov_oils(C):
    F.spr(C, 'c_heat', 540, 400, L(6) - 0.05, LE(6) + 0.3, anchor='tc')
    F.spr(C, 'x_heat', 540, 560, W(6, 'nu') - 0.1, LE(6) + 0.3, anchor='tc')
    F.spr(C, 'c_veg', 540, 690, W(6, 'uleiul', 2) - 0.1, LE(6) + 0.3, anchor='tc')
    F.spr(C, 'x_visc', 540, 850, W(6, 'vascos') - 0.1, LE(6) + 0.3, anchor='tc')
    F.spr(C, 'x_dep', 540, 940, W(6, 'depuneri') - 0.1, LE(6) + 0.3, anchor='tc')
    F.label(C, 'l_empty', TJ['pts']['fuel'], (480, 1120), W(7, 'fara') - 0.1, W(7, 'aerul') + 0.1)

# ------------------------------------------------------------------ cum eviti: lista si indicatorul de combustibil
def ov_do(C):
    t = C.t
    for k, (sid, w) in enumerate((('c_std', 'standard'), ('c_station', 'benzinarii'), ('c_mix', 'amestecuri'), ('c_last', 'mergi'))):
        F.spr(C, sid, 540, 390 + 88 * k, W(9, w) - 0.15, LE(9) + 0.35, anchor='tc')
    a = F.pop(t, W(9, 'mergi') - 0.2, LE(9) + 0.35)
    if a <= 0.003: return
    cx, cy, R = 540, 1110, 165
    D.rbox(C, cx - R - 40, cy - R - 40, 2 * R + 80, R + 110, (70, 80, 92), a, th=2, fill=(8, 12, 17, 215), r=18)
    D.arc(C, cx, cy, R, 200, 340, (205, 212, 220), th=10, a=a)
    D.arc(C, cx, cy, R, 200, 228, (255, 75, 75), th=16, a=a)
    D.text(C, 'E', cx + (R - 42) * math.cos(math.radians(204)), cy + (R - 42) * math.sin(math.radians(204)), 40, (255, 120, 120), a, 'anton')
    D.text(C, 'F', cx + (R - 42) * math.cos(math.radians(336)), cy + (R - 42) * math.sin(math.radians(336)), 40, (232, 237, 243), a, 'anton')
    u = float(seg(t, W(9, 'nu') - 0.1, W(9, 'picatura') + 0.2))
    th = math.radians(318 - 112 * u)
    D.line2(C, [(cx, cy), (cx + (R - 18) * math.cos(th), cy + (R - 18) * math.sin(th))], (255, 210, 31), 9, a)
    D.dots2(C, np.array([[cx, cy]]), 15, (255, 210, 31), a)
    al = a * float(seg(t, W(9, 'picatura'), W(9, 'picatura') + 0.2)) * (0.6 + 0.4 * math.sin(t * 10))
    if al > 0.003: D.text(C, 'REZERVĂ', cx, cy + 40, 40, (255, 75, 75), al, 'anton')

# ------------------------------------------------------------------ planuri
GUIDE = S.scr('needle', 'shut', [0, 0, 36.0], (1.25, 0, 280))
SHOTS = S.opening(E, 'needle', np.array([0, 0, 36.0]), dive_kb=((1.0, 0, 120), (1.25, 0, 280)), zmax=3.0,
                  fx_dive=[fx_film_guide(E.T_N + 0.6)]) + [
 Shot('microf', L(3), L(4), st='mclean', tr=('dive', 0.7, GUIDE, 3.0), kb=[(L(3), 1.0, 0, 0), (L(4), 1.06, 0, 0)],
      fx=[fx_film(0.5)], ov=ov_micro3),
 Shot('blank', L(4), L(5), st='none', tr=('xf', 0.3), ov=ov_spec),
 Shot('filter', L(5), W(5, 'piesele') - 0.1, st='shut', tr=('xf', 0.3), kb=[(L(5), 0.6, 0, -60), (W(5, 'piesele'), 0.64, 0, -60)],
      fx=[fx_gum(L(5) + 0.1, W(5, 'filtrele'))], ov=ov_filter),
 Shot('microf', W(5, 'piesele') - 0.1, L(6), st='mlac1', seq=[('mlac2', W(5, 'lipesc') - 0.1, W(5, 'lipesc') + 0.7)], tr=('xf', 0.25),
      kb=[(W(5, 'piesele'), 1.0, 0, 0), (L(6), 1.05, 0, 0)], fx=[fx_film(0.3)],
      ov=lambda C: F.spr(C, 'l_stick', 540, 1150, W(5, 'piesele') - 0.05, L(6) + 0.2, anchor='tc')),
 Shot('tank', L(6), W(7, 'aerul') - 0.2, st='dry', seq=[('empty', W(7, 'ramai') - 0.1, W(7, 'motorina') + 0.5)], tr=('xf', 0.3),
      kb=[(L(6), 1.0, 0, 40), (W(7, 'aerul'), 1.06, 0, 30)], ov=ov_oils,
      dim=lambda t: 0.6 * (1 - float(seg(t, L(7) - 0.35, L(7) + 0.15)))),
 Shot('microf', W(7, 'aerul') - 0.2, W(8, 'duzele') - 0.1, st='mclean',
      seq=[('mdry0', L(8) - 0.1, W(8, 'pelicula') + 0.5), ('mdry', W(8, 'freaca') - 0.22, W(8, 'freaca') + 0.06)], tr=('xf', 0.3),
      kb=[(W(7, 'aerul'), 1.0, 0, 0), (W(8, 'duzele'), 1.1, 0, 0)], shake=shake_at(W(8, 'freaca') - 0.1, 1.2, 4.0),
      fx=[fx_film(0.45, L(8)), fx_air(W(7, 'aerul') - 3.6, L(8) + 0.3), fx_grind(W(8, 'freaca') - 0.1)], ov=ov_micro8),
 Shot('needle', W(8, 'duzele') - 0.1, W(8, 'supapele') - 0.1, st='shut', tr=('xf', 0.2), kb=[(W(8, 'duzele'), 1.15, 0, 230), (W(8, 'supapele'), 1.2, 0, 250)],
      shake=shake_at(W(8, 'lipesc') - 0.05, 0.6, 3.0), fx=[fx_stuck(W(8, 'duzele') - 0.1)],
      ov=lambda C: F.spr(C, 'l_noz', 540, 1150, W(8, 'duzele') - 0.05, W(8, 'supapele') + 0.1, anchor='tc')),
 Shot('seattop', W(8, 'supapele') - 0.1, L(9), st='tclean', seq=[('tpits', W(8, 'cedeaza') - 0.2, W(8, 'cedeaza') + 0.3)], tr=('xf', 0.2),
      kb=[(W(8, 'supapele'), 1.0, 0, 0), (L(9), 1.1, 0, 0)], shake=shake_at(W(8, 'cedeaza') - 0.05, 0.6, 3.0),
      ov=lambda C: F.spr(C, 'l_valve', 540, 1150, W(8, 'supapele') - 0.05, L(9) + 0.2, anchor='tc')),
 Shot('tank', L(9), L(E.OUT), st='dry', tr=('xf', 0.3), kb=[(L(9), 1.0, 0, 40), (L(E.OUT), 1.05, 0, 30)], ov=ov_do,
      dim=lambda t: 0.5),
 S.ending(E),
]
