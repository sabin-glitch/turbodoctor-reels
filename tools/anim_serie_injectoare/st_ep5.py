# Episodul 5: saiba de etansare. Gazele scapa pe langa injector, umplu putul cu calamina („black death”), injectorul se blocheaza.
# Momentele din ep5/vo/cues.json (provizorii pana vine vocea).
import math
import numpy as np
import icomp as IC, ifx as F, ikit as K, iser as S, i2d as D
import fxlib as X
from icomp import Shot
from fxlib import seg
from ifx import PR, PLf

E = S.Ep(5); N = E.n; EP = E.ep; W, L, LE = E.W, E.L, E.LE; TOTAL = E.TOTAL
GLOB = S.glob(E)
COPPER = np.array([1.0, 0.55, 0.25]); SMOKE = np.array([0.70, 0.66, 0.62]); HOTG = np.array([1.0, 0.5, 0.15])

SPR = dict(S.spr_common(N), **{
 'l_washer': K.lb('ȘAIBA DE CUPRU', 'lp'),
 'l_head': K.lb('CHIULASA', 'grey'),
 'c_seal': K.chk('ȚINE GAZELE ÎN CILINDRU'),
 'x_miss': K.chk('LIPSEȘTE', False),
 'x_reuse': K.chk('REFOLOSITĂ', False),
 'x_wrong': K.chk('NEPOTRIVITĂ', False),
 'x_clamp': K.chk('CLEMA STRÂNSĂ GREȘIT', False),
 'l_gas': K.lb('GAZELE SCAPĂ', 'bad', 'Pe lângă injector'),
 'l_soot': K.lb('CALAMINĂ FOARTE TARE', 'bad'),
 'q_black': '<div class="quote red"><q>„MOARTEA NEAGRĂ”</q><small>„Black death”, cum îi spune Mercedes-Benz</small></div>',
 'l_stuck': K.lb('BLOCAT ÎN CHIULASĂ', 'bad big'),
 's_soot': K.sym('smoke', 'FUNINGINE', 'În jurul injectorului'),
 's_idle': K.sym('idle', 'MERS NEREGULAT'),
 's_stuck': K.sym('warn', 'NU MAI IESE', 'La demontare', 'warn'),
 'c_new': K.chk('ȘAIBĂ NOUĂ'),
 'c_seat': K.chk('SCAUNUL CURĂȚAT'),
 'c_torque': K.chk('CUPLUL ȘI UNGHIUL DIN FABRICĂ'),
})

# ------------------------------------------------------------------ traseul gazelor pe langa injector (pe ambele fete de sectiune)
GAS_RZ = [(2.4, -1.5), (3.64, 2.6), (3.64, 21.4), (4.25, 22.5), (4.61, 23.2), (4.61, 25.1), (6.0, 26.1), (8.2, 26.6), (9.0, 27.6), (9.0, 40.0), (9.0, 57.0),
          (8.95, 60.0), (8.95, 90.0)]
GAS_R = F.IPath([PR(r, z) for r, z in GAS_RZ], 'R', 0.12, smooth=4, step=0.1)
GAS_L = F.IPath([PLf(r, z) for r, z in GAS_RZ], 'L', 0.12, smooth=4, step=0.1)
WASH_R, WASH_L = PR(6.0, 26.1), PLf(6.0, 26.1)

def fx_washer_glow(t_on, t_off, a=0.45):
    def f(C):
        e = float(seg(C.t, t_on, t_on + 0.4)) * (1 - float(seg(C.t, t_off - 0.4, t_off)))
        if e <= 0: return
        k = 0.75 + 0.25 * math.sin(C.t * 5.0)
        for P in (WASH_R, WASH_L): F.glow(C, P, 70 * C.k, COPPER, a * e * k)
    return f

def fx_gas(t_on, t_off=None, n=70, a=1.0, P=None):
    """gazele urca pe langa injector; P = impulsuri de ardere (pulsatia la fiecare ardere)"""
    def f(C):
        k = a
        if P is not None:
            e = 0.0
            for ton, toff in P:
                d = C.t - (ton + 0.12)
                if 0 <= d < 0.6: e = max(e, math.exp(-d / 0.22))
            k *= 0.35 + 0.65 * e
        for i, pth in enumerate((GAS_R, GAS_L)):
            F.flow(C, pth, n, 26.0, SMOKE, 0.3, lat=0.8, seed=71 + i, t0=t_on, t1=t_off, mode='over', shape='d', shade=0.45, a=min(1.0, k), sz_var=0.6)
            F.flow(C, pth, 28, 30.0, HOTG, 0.17, lat=0.7, seed=81 + i, t0=t_on, t1=t_off, mode='add', shape='g', shade=0, a=0.95 * min(1.0, k), glow=0.45)
    return f

def spray(P, kind='good', Ls=7.0):
    return lambda C: K.spray_pulses(C, P, kind=kind, L=Ls, life=0.3, szk=0.7)

P3 = K.inj_pulses(L(3) - 0.3, L(4) + 0.3, 0.62, 0.15)
P45 = K.inj_pulses(L(4) - 0.3, L(6) + 0.3, 0.62, 0.15)
P6 = [(t, t + 0.15) for t in np.cumsum([L(6) - 0.3] + [0.5, 0.9, 0.45, 1.1, 0.55, 0.8, 0.6])]          # ardere neregulata
P8 = K.inj_pulses(L(8) - 0.3, L(E.OUT) + 0.3, 0.62, 0.15)

# ------------------------------------------------------------------ etichete
def ov_seal(C):
    F.label(C, 'l_washer', WASH_R, (1040, 1150), W(3, 'saiba') - 0.05, LE(3) + 0.2, anchor='tr')
    F.label(C, 'l_head', PR(16.0, 30.0), (720, 700), W(3, 'chiulasa') - 0.05, LE(3) + 0.2)
    F.spr(C, 'c_seal', 540, 420, W(3, 'tine') - 0.1, LE(3) + 0.3, anchor='tc')

def ov_leak(C):
    ys = (400, 488, 576, 664)
    for (sid, w), y in zip((('x_miss', 'lipseste'), ('x_reuse', 'refolosita'), ('x_wrong', 'nepotrivita'), ('x_clamp', 'clema')), ys):
        F.spr(C, sid, 540, y, W(4, w) - 0.1, LE(4) + 0.3, anchor='tc')
    F.label(C, 'l_gas', PR(9.0, 34.0), (1040, 1150), W(4, 'scapa') - 0.1, LE(4) + 0.3, anchor='tr')

def ov_soot(C):
    F.label(C, 'l_soot', PR(9.0, 30.0), (1040, 1150), W(5, 'calamina') - 0.05, W(5, 'mercedes') - 0.15, anchor='tr')
    F.spr(C, 'q_black', 540, 400, W(5, 'mercedes') - 0.15, LE(5) + 0.4, anchor='tc')

def ov_stuck(C):
    t = C.t; ta = W(6, 'blocheaza') - 0.1
    a = F.pop(t, ta, LE(6) + 0.3, 0.2, 0.3)
    if a > 0.003:
        x, y = S.scr('well', 'soot2', [0, 0, 50.0], KB6)
        lift = 26 * float(seg(t, ta, ta + 0.35)) * (1 - float(seg(t, ta + 0.5, ta + 0.8)))
        D.line2(C, [(x, y + 40 - lift), (x, y - 120 - lift)], (255, 255, 255), 9, a)
        D.line2(C, [(x - 34, y - 86 - lift), (x, y - 124 - lift), (x + 34, y - 86 - lift)], (255, 255, 255), 9, a)
        ax = float(seg(t, ta + 0.55, ta + 0.8))
        if ax > 0:
            D.line2(C, [(x - 46, y - 96), (x + 46, y - 4)], (255, 75, 75), 12, a * ax)
            D.line2(C, [(x + 46, y - 96), (x - 46, y - 4)], (255, 75, 75), 12, a * ax)
    F.label(C, 'l_stuck', PR(9.0, 40.0), (1040, 1150), ta + 0.5, LE(6) + 0.3, anchor='tr')

def ov_fix(C):
    t = C.t
    F.spr(C, 'c_new', 540, 400, W(8, 'saiba') - 0.1, LE(8) + 0.3, anchor='tc')
    F.spr(C, 'c_seat', 540, 490, W(8, 'scaunul') - 0.1, LE(8) + 0.3, anchor='tc')
    F.spr(C, 'c_torque', 540, 580, W(8, 'cuplul') - 0.1, LE(8) + 0.3, anchor='tc')
    # cadranul de strangere: arcul galben = cuplul, prelungirea verde = unghiul
    ta = W(8, 'strangere') - 0.1; a = F.pop(t, ta, LE(8) + 0.3, 0.3, 0.3)
    if a > 0.003:
        cx, cy, R = 820, 1060, 118
        D.rbox(C, cx - 175, cy - 170, 350, 300, (70, 80, 92), a, th=2, fill=(8, 12, 17, 215), r=18)
        D.arc(C, cx, cy, R, 135, 405, (60, 68, 78), 20, a)
        e1 = float(seg(t, W(8, 'cuplul') - 0.1, W(8, 'cuplul') + 0.8)); e2 = float(seg(t, W(8, 'unghiul') - 0.1, W(8, 'unghiul') + 0.7))
        D.arc(C, cx, cy, R, 135, 135 + 180 * e1, (255, 210, 31), 20, a)
        D.arc(C, cx, cy, R, 315, 315 + 75 * e2, (61, 220, 132), 20, a)
        D.text(C, 'CUPLU', cx, cy - 12, 40, (255, 210, 31), a * float(seg(t, W(8, 'cuplul') - 0.1, W(8, 'cuplul') + 0.3)), 'anton')
        D.text(C, '+ UNGHI', cx, cy + 40, 36, (61, 220, 132), a * e2, 'anton')
        D.text(C, 'STRÂNGEREA CLEMEI', cx, cy + 112, 22, (182, 194, 207), a, 'mont', shadow=False)

def fx_clean_seat(t_on):
    def f(C):
        e = float(seg(C.t, t_on, t_on + 0.3)) * (1 - float(seg(C.t, t_on + 1.4, t_on + 2.0)))
        if e <= 0: return
        for k, P in enumerate((PR(5.2, 25.25), PR(7.0, 25.25), PLf(6.0, 25.25))):
            F.glow(C, P, (40 + 18 * math.sin(C.t * 9 + k)) * C.k, np.array([0.6, 1.0, 0.75]), 0.5 * e)
    return f

# ------------------------------------------------------------------ planuri
WP = [0, 0, 27.0]
KB3a = S.kb_on('well', 'shut', WP, 1.0, ty=1000); KB3b = S.kb_on('well', 'shut', WP, 1.28, ty=980)
KB4 = S.kb_on('well', 'shut', WP, 1.32, ty=1000); KB5 = S.kb_on('well', 'shut', [0, 0, 32.0], 1.4, ty=980)
KB6 = S.kb_on('well', 'shut', [0, 0, 36.0], 1.1, ty=1000); KB8a = S.kb_on('well', 'shut', WP, 1.2, ty=1020); KB8b = S.kb_on('well', 'shut', WP, 1.3, ty=1020)

def shake6(t):
    ta = W(6, 'blocheaza') - 0.1
    e = float(seg(t, ta, ta + 0.1)) * (1 - float(seg(t, ta + 0.6, ta + 0.9)))
    return (5.0 * e * math.sin(t * 61.0), 3.0 * e * math.sin(t * 47.0 + 1.3))

SHOTS = S.opening(E, 'well', np.array(WP), dive_kb=(S.kb_on('well', 'shut', WP, 1.1, ty=1000), KB3a), zmax=3.4,
                  fx_dive=[fx_washer_glow(E.T_N - 0.2, L(3) + 1.0)]) + [
 Shot('well', L(3), L(4), st='shut', kb=[(L(3),) + KB3a, (L(4),) + KB3b],
      fx=[spray(P3), S.comb_flash(P3), fx_washer_glow(W(3, 'saiba') - 0.1, LE(3) + 0.3)], ov=ov_seal),
 Shot('well', L(4), L(5), st='shut', seq=[('nowasher', W(4, 'lipseste') - 0.1, W(4, 'lipseste') + 0.5)], tr=('xf', 0.25),
      kb=[(L(4),) + KB3b, (L(5),) + KB4], fx=[spray(P45), S.comb_flash(P45), fx_gas(W(4, 'gazele') - 0.1, None, 60, 1.0, P45)], ov=ov_leak,
      dim=lambda t: 0.2 * F.pop(t, W(4, 'lipseste') - 0.1, LE(4) + 0.3)),
 Shot('well', L(5), L(6), st='nowasher', seq=[('soot1', W(5, 'lasa') - 0.1, W(5, 'lasa') + 0.9), ('soot2', W(5, 'tare') - 0.1, W(5, 'mercedes'))], tr=('xf', 0.2),
      kb=[(L(5),) + KB4, (L(6),) + KB5], fx=[spray(P45), S.comb_flash(P45), fx_gas(L(5) - 1.0, None, 80, 1.0, P45)], ov=ov_soot,
      dim=lambda t: 0.35 * F.pop(t, W(5, 'mercedes') - 0.15, LE(5) + 0.4, 0.3, 0.3)),
 Shot('well', L(6), L(7), st='soot2', tr=('xf', 0.25), kb=[(L(6),) + KB6, (L(7),) + KB6], shake=shake6,
      fx=[spray(P6, 'bad'), S.comb_flash(P6, a=0.4), fx_gas(L(6) - 2.0, None, 40, 0.6, P6)], ov=ov_stuck),
 S.symptoms(E, 7, [('s_soot', 'funingine'), ('s_idle', 'mers'), ('s_stuck', 'demontare')]),
 Shot('well', L(8), L(E.OUT), st='soot2', seq=[('shut', W(8, 'saiba') - 0.15, W(8, 'saiba') + 0.6)], kb=[(L(8),) + KB8a, (L(E.OUT),) + KB8b],
      fx=[spray(P8), S.comb_flash(P8, a=0.35), fx_washer_glow(W(8, 'saiba'), W(8, 'scaunul') + 0.6, 0.55), fx_clean_seat(W(8, 'scaunul') - 0.1)], ov=ov_fix),
 S.ending(E),
]
