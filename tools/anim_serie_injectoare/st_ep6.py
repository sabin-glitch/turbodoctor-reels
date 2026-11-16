# Episodul 6: murdaria si greselile de la montaj (Denso, Delphi, Bosch). Momentele din ep6/vo/cues.json (provizorii).
import math
import numpy as np
import cv2
import icomp as IC, ifx as F, ikit as K, iser as S, i2d as D
import fxlib as X
from icomp import Shot
from fxlib import seg
from ifx import PR, PLf

E = S.Ep(6); N = E.n; EP = E.ep; W, L, LE = E.W, E.L, E.LE; TOTAL = E.TOTAL
GLOB = S.glob(E)
DIRT = np.array([0.48, 0.36, 0.22]); DIRT2 = np.array([0.30, 0.24, 0.18]); AIR = np.array([0.88, 0.94, 1.0])
INLET = np.array(F.J['pts']['inlet']); CD = np.array(F.J['uR']) * math.cos(math.radians(32)) + F.EZ * math.sin(math.radians(32))

def sym2(icon, text, small=None, cls='warn'):
    s = '<small>%s</small>' % small if small else ''
    return '<div class="sym %s"><div class="ic">%s</div><div class="tx">%s%s</div></div>' % (cls, D.ICON2[icon], text, s)

_STEEL = '<linearGradient id="sg" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#eef2f6"/><stop offset=".5" stop-color="#b8c1cb"/><stop offset="1" stop-color="#6f7a86"/></linearGradient>'
def pipe_svg(used):
    cone = ('<path d="M540 80 L596 88 L605 82 L607 92 Q618 105 607 118 L605 128 L596 122 L540 130 Z" fill="url(#sg)" stroke="#4a535d" stroke-width="2.5"/>'
            '<path d="M586 90 L592 101 L587 112" fill="none" stroke="#ff4b4b" stroke-width="3"/>'
            '<g fill="#d7dde4" stroke="#6f7a86" stroke-width="1.5"><path d="M632 94 l10 -5 l3 9 z"/><path d="M646 112 l11 2 l-5 8 z"/><path d="M660 98 l8 4 l-7 5 z"/></g>') if used else \
           '<path d="M540 80 L610 94 Q622 105 610 116 L540 130 Z" fill="url(#sg)" stroke="#4a535d" stroke-width="2.5"/>'
    return ('<svg width="860" height="258" viewBox="0 0 700 210"><defs>' + _STEEL + '</defs>'
            '<rect x="30" y="80" width="512" height="50" fill="url(#sg)" stroke="#4a535d" stroke-width="2.5"/>' + cone +
            '<rect x="30" y="98" width="586" height="14" fill="#1a1310"/><rect x="30" y="101.5" width="586" height="7" fill="#ff5a26" opacity=".85"/>'
            '<path d="M360 60 L372 48 H458 L470 60 V150 L458 162 H372 L360 150 Z" fill="#aeb7c1" stroke="#4a535d" stroke-width="2.5"/>'
            '<path d="M395 50V160M435 50V160" stroke="#7d8894" stroke-width="2"/></svg>')

SPR = dict(S.spr_common(N), **{
 'l_dirt': K.lb('MURDĂRIE INTRATĂ LA MONTAJ', 'bad'),
 'q_denso': '<div class="quote mid red"><q>„POATE DEFECTA INJECTORUL IMEDIAT”</q><small>Denso, despre murdăria intrată în sistem la montaj</small></div>',
 'l_valve': K.lb('SUPAPA DE COMANDĂ', 'grey'),
 'c_caps': K.chk('CAPACE PE RACORDURI'),
 'c_clean': K.chk('LOC DE MUNCĂ CURAT'),
 'p_pipe': K.panel('ȚEAVA DE ÎNALTĂ PRESIUNE', 900, 600),
 'pipe_new': pipe_svg(False), 'pipe_used': pipe_svg(True),
 'g_new': K.lb('NOUĂ', 'good'),
 'g_used': K.lb('REFOLOSITĂ', 'bad'),
 'g_cone': K.lb('CONUL SE DEFORMEAZĂ', 'bad'),
 'g_chips': K.lb('AȘCHII', 'bad', 'Pleacă spre injector'),
 'x_reuse': K.chk('NU SE REFOLOSESC', False),
 's_torque': sym2('wrench', 'CUPLURILE DE STRÂNGERE'),
 's_ret': sym2('ret', 'RETURUL LIBER'),
 's_air': sym2('air', 'AERISIREA', 'După reparație'),
 'l_air': K.lb('AERUL ÎMPIEDICĂ UNGEREA', 'bad'),
 'b3a': '<div class="tag3"><div class="t">BOSCH · TREI CAUZE CHEIE</div><div class="r on"><i>1</i>PARTICULELE DIN MOTORINĂ</div><div class="r on"><i>2</i>APA DIN MOTORINĂ</div><div class="r"><i>3</i>MONTAJUL GREȘIT</div></div>',
 'b3b': '<div class="tag3"><div class="t">BOSCH · TREI CAUZE CHEIE</div><div class="r on"><i>1</i>PARTICULELE DIN MOTORINĂ</div><div class="r on"><i>2</i>APA DIN MOTORINĂ</div><div class="r hot"><i>3</i>MONTAJUL GREȘIT</div></div>',
 'c_srv': K.chk('MONTAT ÎN SERVICE'),
 'c_lab': K.chk('CURĂȚENIE DE LABORATOR'),
 'c_pipes': K.chk('ȚEVI NOI'),
 'c_tq': K.chk('CUPLURI DUPĂ FABRICANT'),
})

# ------------------------------------------------------------------ murdaria pe traseul de inalta presiune si la supapa
def fx_dirt(t_on, t_off=None, n=60, size=0.42, speed=40.0):
    def f(C):
        F.flow(C, 'hp_in', n, speed, DIRT, size, lat=0.75, seed=31, t0=t_on, t1=t_off, mode='over', shape='d', shade=0.6, sz_var=0.7)
        F.flow(C, 'hp_down', n, speed, DIRT2, size * 0.9, lat=0.75, seed=32, t0=None if t_on is None else t_on + 0.6, t1=t_off, mode='over', shape='d', shade=0.6, sz_var=0.7)
    return f

RS = X.rnd(66, 40, 4)
def fx_valve_hit(t_on):
    """particulele urca prin orificiul de iesire si se prind intre bila si scaun, cu scantei"""
    def f(C):
        t = C.t
        F.flow(C, 'cc_R', 14, 3.0, DIRT, 0.07, lat=0.6, seed=41, t0=t_on - 0.8, mode='over', shape='d', shade=0.7, sz_var=0.5)
        for i in range(6):
            ta = t_on + i * 0.28
            if t < ta: continue
            a = 2 * math.pi * RS[i, 0]; uu = np.array([math.cos(a), math.sin(a), 0.0])
            if uu[1] < -0.3: uu[1] = -uu[1]
            p = uu * (0.56 + 0.05 * RS[i, 1]) + F.EZ * (136.62 + 0.05 * RS[i, 2])
            F.dots3(C, p, 0.035 + 0.02 * RS[i, 3], np.array([0.40, 0.31, 0.22]), 1.0, shade=0.9, ztest=False)
            F.dots3(C, p, 0.07, np.array([1.0, 0.3, 0.25]), 0.85 * (0.55 + 0.45 * math.sin((t - ta) * 10)), shape='r', shade=0, ztest=False)
            F.sparks(C, p, ta + 0.05, n=14, life=0.3, speed=0.8, size=0.01, seed=90 + i)
    return f

def ov_dirt(C):
    F.label(C, 'l_dirt', np.array(F.J['pts']['inlet_mid']), (1040, 1150), W(3, 'murdaria') - 0.1, W(3, 'poate') - 0.1, anchor='tr')

def ov_denso(C):
    F.spr(C, 'q_denso', 540, 400, W(3, 'poate') - 0.3, LE(3) + 0.4, anchor='tc')
    F.label(C, 'l_valve', S.BALL + np.array([0.55, 0, 0.1]) + F.NR * 0.02, (1040, 1150), W(3, 'defecta') - 0.1, LE(3) + 0.3, anchor='tr')

# ------------------------------------------------------------------ capacul rosu pe racordul de intrare
def ov_caps(C):
    t = C.t; ta = W(4, 'capace') - 0.35
    e = float(seg(t, ta, ta + 0.45)); a = F.pop(t, ta, None, 0.15)
    if a > 0.003:
        k = C.k; slide = 30.0 * (1 - e * e * (3 - 2 * e))
        p1 = INLET + CD * (1.5 + slide); p0 = INLET - CD * (9.0 - slide)
        (x1, y1), (x0, y0) = C.P(p1), C.P(p0)
        x1, y1, x0, y0 = x1 / k, y1 / k, x0 / k, y0 / k
        dx, dy = x1 - x0, y1 - y0; Ln = math.hypot(dx, dy) + 1e-6; nx, ny = -dy / Ln, dx / Ln
        rp = 0.5 * Ln * 9.6 / 10.5
        quad = [(x0 + nx * rp, y0 + ny * rp), (x1 + nx * rp, y1 + ny * rp), (x1 - nx * rp, y1 - ny * rp), (x0 - nx * rp, y0 - ny * rp)]
        xs = [q[0] for q in quad]; ys = [q[1] for q in quad]
        def draw(buf, P, kk):
            pts = np.array([P(*q) for q in quad], np.int32)
            cv2.fillConvexPoly(buf, pts, (226, 52, 52, 255), cv2.LINE_AA, shift=4)
            cv2.polylines(buf, [pts], True, (120, 20, 20, 255), max(1, int(3 * kk)), cv2.LINE_AA, shift=4)
            q2 = [(x1 + nx * rp - dx * 0.18, y1 + ny * rp - dy * 0.18), (x1 - nx * rp - dx * 0.18, y1 - ny * rp - dy * 0.18)]
            cv2.line(buf, P(*q2[0]), P(*q2[1]), (255, 120, 120, 255), max(1, int(3 * kk)), cv2.LINE_AA, shift=4)
        D.canvas(C, min(xs) - 6, min(ys) - 6, max(xs) - min(xs) + 12, max(ys) - min(ys) + 12, draw, a)
    F.spr(C, 'c_caps', 540, 400, W(4, 'capace') - 0.1, LE(4) + 0.3, anchor='tc')
    F.spr(C, 'c_clean', 540, 490, W(4, 'locul') - 0.1, LE(4) + 0.3, anchor='tc')

# ------------------------------------------------------------------ teava: noua si refolosita, aschiile pornesc spre injector
RC = X.rnd(77, 30, 3)
def ov_pipe(C):
    t = C.t; tp = L(5) - 0.05; te = LE(5) + 0.35
    a = F.pop(t, tp, te, 0.3, 0.3)
    if a <= 0.003: return
    F.spr(C, 'p_pipe', 90, 520, tp, te)
    F.spr(C, 'pipe_new', 120, 590, tp + 0.1, te, popk=1.0, slide=(0, 0))
    F.spr(C, 'g_new', 150, 800, tp + 0.2, te)
    tu = W(5, 'refolosesc') - 0.2
    F.spr(C, 'pipe_used', 120, 850, tu, te, popk=1.0, slide=(0, 0))
    F.spr(C, 'g_used', 150, 1060, tu + 0.1, te)
    F.spr(C, 'x_reuse', 540, 420, tu, te, anchor='tc')
    tc = W(5, 'conul') - 0.1
    D.rbox(C, 120 + 652, 850 + 88, 126, 86, (255, 75, 75), a * float(seg(t, tc, tc + 0.3)), th=5, r=12)
    F.spr(C, 'g_cone', 520, 1060, tc, te)
    tch = W(5, 'aschii') - 0.15
    if t > tch:
        u = t - tch; P = []
        for i in range(10):
            s = (u * (40 + 30 * RC[i, 0]) + RC[i, 1] * 25) % 90
            P.append((120 + 790 + s, 850 + 129 + (RC[i, 2] - 0.5) * 18 + math.sin(s * 0.08 + i) * 4))
        D.dots2(C, P, 5.5, (215, 221, 228), a * float(seg(t, tch, tch + 0.3)))
        F.spr(C, 'g_chips', 640, 1150, tch, te)

# ------------------------------------------------------------------ cupluri, retur, aerisire; aerul in joc (vederea micro)
def ov_three(C):
    F.spr(C, 's_torque', 220, 400, W(6, 'cuplurile') - 0.1, W(6, 'aerul') - 0.25)
    F.spr(C, 's_ret', 220, 540, W(6, 'returul') - 0.1, W(6, 'aerul') - 0.25)
    F.spr(C, 's_air', 220, 680, W(6, 'aerisirea') - 0.1, W(6, 'aerul') - 0.25)

def fx_bubbles(t_on):
    gp = F.IPath([[0, -0.1, 26], [0, -0.1, -26]], None, 1.0, smooth=0, step=0.25)
    gp.L = np.tile(np.array([0.5, 0, 0]), (gp.n, 1))
    def f(C):
        F.flow(C, gp, 26, 13.0, np.array([1.0, 0.75, 0.5]), 0.12, lat=0.9, seed=5, mode='add', shape='g', shade=0, a=0.4)
        F.flow(C, gp, 9, 6.0, AIR, 0.9, lat=0.45, seed=9, t0=t_on, mode='over', shape='d', shade=0.75, a=0.95, sz_var=0.45)
    return f

def ov_air(C):
    F.spr(C, 'l_air', 540, 420, W(6, 'impiedica') - 0.2, LE(6) + 0.3, anchor='tc')

def ov_bosch(C):
    t = C.t
    F.spr(C, 'b3a', 540, 560, W(7, 'trei') - 0.2, W(7, 'montajul') + 0.25, anchor='tc', popk=1.0)
    F.spr(C, 'b3b', 540, 560, W(7, 'montajul') - 0.05, LE(7) + 0.35, anchor='tc', popk=1.0, slide=(0, 0))

def ov_fix(C):
    for k, (sid, w) in enumerate((('c_srv', 'service'), ('c_lab', 'curatenie'), ('c_pipes', 'tevi'), ('c_tq', 'cupluri'))):
        F.spr(C, sid, 540, 420 + 90 * k, W(8, w) - 0.1, LE(8) + 0.3, anchor='tc')

# ------------------------------------------------------------------ planuri
INP = S.scr('hero', 'shut', INLET, (1.07, 0, -30))
KBU = S.kb_on('upper', 'shut', np.array(F.J['pts']['inlet_mid']), 1.0)
SHOTS = S.opening(E, 'upper', np.array(F.J['pts']['inlet_mid']), dive_kb=((1.1, 0, 40), (1.0, 0, 20)),
                  fx_dive=[fx_dirt(E.T_N - 0.6, None, 40)]) + [
 Shot('upper', L(3), W(3, 'defecta') - 0.25, st='shut', kb=[(L(3), 1.0, 0, 20), (W(3, 'defecta'), 1.12, -40, 40)], fx=[S.fx_fuel(L(3) - 3), fx_dirt(L(3) - 2.0)],
      ov=[ov_dirt, ov_denso], dim=lambda t: 0.3 * F.pop(t, W(3, 'poate') - 0.3, LE(3) + 0.4)),
 Shot('valve', W(3, 'defecta') - 0.25, L(4), st='shut', tr=('xf', 0.25), kb=[(W(3, 'defecta'), 1.0, 0, -60), (L(4), 1.06, 0, -70)],
      fx=[fx_valve_hit(W(3, 'defecta'))], ov=ov_denso, dim=lambda t: 0.3 * F.pop(t, W(3, 'poate') - 0.3, LE(3) + 0.4)),
 Shot('hero', L(4), L(5), st='full', kb=[(L(4), 1.25, -40, 160), (L(5), 1.32, -60, 175)], ov=ov_caps),
 Shot('upper', L(5), L(6), st='shut', kb=[(L(5), 1.0, 0, 20), (L(6), 1.04, 0, 20)], fx=[S.fx_fuel(L(5) - 3)], ov=ov_pipe,
      dim=lambda t: 0.6 * F.pop(t, L(5) - 0.05, LE(5) + 0.35, 0.3, 0.3)),
 Shot('upper', L(6), W(6, 'aerul') - 0.2, st='shut', kb=[(L(6), 1.0, 0, 20), (W(6, 'aerul'), 1.05, 0, 30)], fx=[S.fx_fuel(L(6) - 3)], ov=ov_three,
      dim=lambda t: 0.25 * F.pop(t, W(6, 'cuplurile') - 0.1, W(6, 'aerul'))),
 Shot('microf', W(6, 'aerul') - 0.2, L(7), st='mclean', tr=('xf', 0.3), kb=[(W(6, 'aerul'), 1.0, 0, 0), (L(7), 1.05, 0, 0)], fx=[fx_bubbles(W(6, 'aerul') - 0.6)], ov=ov_air),
 Shot('hero', L(7), L(8), st='shut', kb=[(L(7), 1.0, 0, 0), (L(8), 1.04, 0, -10)], fx=[S.fx_fuel(L(7) - 3)], ov=ov_bosch,
      dim=lambda t: 0.45 * F.pop(t, W(7, 'trei') - 0.2, LE(7) + 0.35)),
 Shot('upper', L(8), L(E.OUT), st='shut', kb=[(L(8), 1.0, 0, 20), (L(E.OUT), 1.05, 0, 30)], fx=[S.fx_fuel(L(8) - 3)], ov=ov_fix,
      dim=lambda t: 0.2 * F.pop(t, W(8, 'service') - 0.1, LE(8) + 0.3)),
 S.ending(E),
]
