# Episodul 12: defectele electrice (bobina: intrerupta, scurtcircuit, izolatie pierduta fata de corp; teancul piezo: scurtcircuit,
# capacitate pierduta, nu se schimba separat; rare fata de cele hidraulice; mufa si cablajul). Momentele din ep12/vo/cues.json (provizorii).
import math, json, os
import numpy as np
import icomp as IC, ifx as F, ikit as K, iser as S, i2d as D
import fxlib as X
from icomp import Shot
from fxlib import seg

E = S.Ep(12); N = E.n; EP = E.ep; W, L, LE = E.W, E.L, E.LE; TOTAL = E.TOTAL
GLOB = S.glob(E)
ELEC = np.array([0.45, 0.78, 1.0]); ELEC8 = (115, 200, 255)
CONN = np.array(F.J['pts']['conn_el'], float)

def sym2(icon, text, small=None, cls='warn'):
    s = '<small>%s</small>' % small if small else ''
    return '<div class="sym %s"><div class="ic">%s</div><div class="tx">%s%s</div></div>' % (cls, D.ICON2[icon], text, s)

def stack_svg(n=64, w=300, h=700):
    g = [f'<rect x="0" y="0" width="{w}" height="{h}" rx="10" fill="#2a2f36"/>', f'<rect x="0" y="0" width="22" height="{h}" rx="6" fill="#cfd6de"/>',
         f'<rect x="{w - 22}" y="0" width="22" height="{h}" rx="6" fill="#cfd6de"/>']
    lh = (h - 40) / n
    for i in range(n):
        y = 20 + i * lh
        g.append(f'<rect x="26" y="{y:.1f}" width="{w - 52}" height="{lh * 0.72:.1f}" fill="{"#e2d3ac" if i % 2 else "#d4c296"}"/>')
        g.append(f'<rect x="{26 if i % 2 else 40}" y="{y + lh * 0.72:.1f}" width="{w - 66}" height="{lh * 0.28:.1f}" fill="#9a7b44"/>')
    return f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">{"".join(g)}</svg>'

STOP_SEP = '<div class="stop"><div class="ic">%s</div><div>NU SE SCHIMBĂ SEPARAT</div></div>' % K.ICON['stop']

SPR = dict(S.spr_common(N), **{
 'g_em': K.lb('INJECTORUL ELECTROMAGNETIC', 'grey'),
 'l_coil': K.lb('BOBINA', ''), 'l_arm': K.lb('ANCORA', ''), 'l_valve': K.lb('SUPAPA DE COMANDĂ', 'hp'),
 'x_open': K.chk('BOBINĂ ÎNTRERUPTĂ', False),
 'x_short': K.chk('SCURTCIRCUIT', False),
 'x_iso': K.chk('IZOLAȚIE PIERDUTĂ FAȚĂ DE CORP', False),
 'g_piezo': K.lb('INJECTORUL PIEZO', 'grey'),
 'stack': stack_svg(),
 'l_layers': K.lb('SUTE DE STRATURI', '', 'ceramice'),
 'l_short2': K.lb('SCURTCIRCUIT', 'bad'),
 'st_sep': STOP_SEP,
 'c_elec': sym2('plug', 'DEFECTELE ELECTRICE', 'Rare', 'warn'),
 'c_hyd': sym2('drop', 'DEFECTELE HIDRAULICE', 'Mai dese', 'bad'),
 'l_plug': K.lb('MUFA', ''), 'l_wire': K.lb('CABLAJUL', ''),
 'g_before': K.lb('ÎNAINTE SĂ SCHIMBI INJECTOARE', 'grey'),
 'c_plugs': K.chk('VERIFICĂ MUFELE'),
 'c_wires': K.chk('ȘI CABLAJUL'),
})

# ------------------------------------------------------------------ bobina ridica ancora: campul, ancora, supapa
CL = F.PLf(6.0, 152.0); CR = F.PR(6.0, 152.0)
def fx_coil(t_on, t_off=1e9, t_flick=None):
    """bobina sub tensiune: stralucire si inele de camp (2D in jurul infasurarilor)"""
    def f(C):
        t = C.t
        e = float(seg(t, t_on, t_on + 0.2)) * (1 - float(seg(t, t_off, t_off + 0.15)))
        if t_flick is not None and t > t_flick: e *= 0.0 if int(t * 13) % 3 else 0.6
        if e <= 0.01: return
        for P in (CL, CR):
            F.glow(C, np.asarray(P, float), 110 * C.k, ELEC, 0.45 * e)
            x, y = C.P(P); x, y = x / C.k, y / C.k
            for k in range(3):
                ph = (t * 0.9 + k / 3.0) % 1.0
                D.arc(C, x, y, 60 + 140 * ph, 0, 360, ELEC8, th=4, a=0.55 * e * (1 - ph))
    return f

def fx_valve_flow(t_open):
    def f(C):
        if C.t > t_open: F.flow(C, 'cc_R', 30, 9.0, np.array([1.0, 0.75, 0.3]), 0.12, lat=0.6, seed=47, t0=t_open, mode='add', shape='g', shade=0, a=0.6)
    return f

def ov_em(C):
    F.spr(C, 'g_em', 540, 390, L(3) - 0.05, LE(3) + 0.3, anchor='tc')
    F.label(C, 'l_coil', F.PLf(6.4, 153.0), (60, 520), W(3, 'bobina') - 0.1, LE(3) + 0.3)
    F.label(C, 'l_arm', F.PLf(3.4, 146.6), (60, 860), W(3, 'ancora') - 0.1, LE(3) + 0.3)
    F.label(C, 'l_valve', F.PLf(0.62, 137.2), (60, 1060), W(3, 'supapa') - 0.1, LE(3) + 0.3)

# ------------------------------------------------------------------ defectele bobinei
def fx_faults(C):
    t = C.t
    # 1 intrerupta: un X rosu pe infasurarea din dreapta
    a1 = F.pop(t, W(4, 'intrerupe') - 0.05, LE(4) + 0.3, 0.15, 0.25)
    if a1 > 0.003:
        x, y = C.P(CR); x, y = x / C.k, y / C.k
        D.line2(C, [(x - 40, y - 40), (x + 40, y + 40)], (255, 75, 75), 12, a1); D.line2(C, [(x + 40, y - 40), (x - 40, y + 40)], (255, 75, 75), 12, a1)
    # 2 scurtcircuit: scantei intre spire, pe infasurarea din stanga
    ts = W(4, 'scurtcircuit') - 0.05
    if t > ts:
        for i in range(4): F.sparks(C, np.asarray(CL, float) + F.EZ * (1.2 * i - 1.8), ts + 0.32 * i, n=22, life=0.3, speed=9.0, size=0.12, seed=170 + i)
        F.glow(C, np.asarray(CL, float), 90 * C.k, np.array([1.0, 0.35, 0.25]), 0.35 * F.pop(t, ts, LE(4) + 0.3))
    # 3 izolatia pierduta: arc electric de la bobina la corp
    ti = W(4, 'izolatia') - 0.05
    ai = F.pop(t, ti, LE(4) + 0.3, 0.1, 0.25)
    if ai > 0.003:
        x0, y0 = C.P(CR); x1, y1 = C.P(F.PR(10.6, 150.5)); x0, y0, x1, y1 = x0 / C.k, y0 / C.k, x1 / C.k, y1 / C.k
        rr = np.random.RandomState(int(t * 20)).rand(8)
        pts = [(x0 + (x1 - x0) * k / 7 + (0 if k in (0, 7) else 16 * (rr[k] - 0.5)), y0 + (y1 - y0) * k / 7 + (0 if k in (0, 7) else 22 * (rr[k] - 0.5))) for k in range(8)]
        D.line2(C, pts, (230, 245, 255), 5, ai * (0.6 + 0.4 * rr[0]))
        F.glow(C, np.asarray(F.PR(10.6, 150.5), float), 70 * C.k, ELEC, 0.5 * ai)

def ov_faults(C):
    for k, (sid, w) in enumerate((('x_open', 'intrerupe'), ('x_short', 'scurtcircuit'), ('x_iso', 'izolatia'))):
        F.spr(C, sid, 540, 1010 + 86 * k, W(4, w) - 0.1, LE(4) + 0.3, anchor='tc')

# ------------------------------------------------------------------ teancul piezo
SX, SY, SW, SH = 130, 470, 300, 700
def ov_piezo(C):
    t = C.t; a = F.pop(t, L(5) - 0.1, LE(5) + 0.35)
    F.spr(C, 'g_piezo', 540, 380, L(5) - 0.05, LE(5) + 0.35, anchor='tc')
    F.spr(C, 'stack', SX, SY, L(5) + 0.1, LE(5) + 0.35, popk=1.0, slide=(0, 0))
    if a > 0.003:                                              # acolada si eticheta pe teanc
        ab = a * float(seg(t, W(5, 'sute') - 0.1, W(5, 'sute') + 0.3))
        D.line2(C, [(SX + SW + 20, SY + 10), (SX + SW + 40, SY + 10), (SX + SW + 40, SY + SH - 10), (SX + SW + 20, SY + SH - 10)], (255, 210, 31), 4, ab)
    F.spr(C, 'l_layers', SX + SW + 60, SY + SH / 2 - 30, W(5, 'sute') - 0.1, W(5, 'scurtcircuit') - 0.1)
    ts = W(5, 'scurtcircuit') - 0.05
    a2 = F.pop(t, ts, LE(5) + 0.35, 0.1, 0.25)
    if a2 > 0.003:                                             # scurtcircuit intre doua straturi
        yy = SY + 0.58 * SH; fl = 0.65 + 0.35 * math.sin(t * 31) * math.sin(t * 17)
        D.line2(C, [(SX + 26, yy), (SX + SW - 26, yy)], (255, 90, 70), 9, a2 * fl)
        rr = np.random.RandomState(int(t * 24)).rand(12, 2)
        D.dots2(C, np.stack([SX + 30 + rr[:, 0] * (SW - 60), yy + (rr[:, 1] - 0.5) * 30], -1), 4.0, (255, 220, 160), a2 * fl, glow=0.9)
    F.spr(C, 'l_short2', SX + SW + 60, SY + 0.58 * SH - 30, W(5, 'scurtcircuit') - 0.1, LE(5) + 0.35)
    tc = W(5, 'capacitatea') - 0.2
    ac = F.pop(t, tc, LE(5) + 0.35)
    if ac > 0.003:                                             # capacitatea scade
        gx, gy, gw, gh = 850, 470, 120, 330
        v = 1.0 - 0.62 * float(seg(t, tc + 0.2, tc + 1.4))
        D.rbox(C, gx, gy, gw, gh, (205, 212, 220), ac, th=4, r=10)
        col = (61, 220, 132) if v > 0.75 else ((255, 178, 36) if v > 0.5 else (255, 75, 75))
        D.rbox(C, gx + 10, gy + 10 + (gh - 20) * (1 - v), gw - 20, (gh - 20) * v, col, ac, th=1, fill=(*col, 235), r=6)
        D.text(C, 'CAPACITATE', gx + gw / 2, gy + gh + 34, 28, (232, 237, 243), ac, 'mont9')
    F.spr(C, 'st_sep', 540, 1180, W(5, 'nu') - 0.1, LE(5) + 0.35, anchor='tc')

# ------------------------------------------------------------------ rare fata de cele hidraulice; mufa si cablajul
def ov_rare(C):
    t = C.t; te = W(6, 'iar') + 0.1
    F.spr(C, 'c_elec', 540, 470, L(6) - 0.05, te, anchor='tc')
    D.text(C, 'RARE', 540, 700, 130, (255, 210, 31), F.pop(t, W(6, 'rare') - 0.1, te), 'anton')
    F.spr(C, 'c_hyd', 540, 820, W(6, 'hidraulice') - 0.15, te, anchor='tc')
    D.text(C, 'MAI DESE', 540, 1050, 130, (255, 75, 75), F.pop(t, W(6, 'hidraulice') - 0.05, te), 'anton')

def cable_pts(C):
    x, y = C.P(CONN); x, y = x / C.k, y / C.k
    return [(x - 30, y - 6), (x - 150, y + 30), (x - 310, y + 10), (x - 470, y + 90), (-60, y + 170)]

def ov_plug(C):
    t = C.t; a = F.pop(t, W(6, 'iar') - 0.2, None, 0.3)
    if a > 0.003:
        P = cable_pts(C)
        D.line2(C, P, (30, 33, 38), 30, a); D.line2(C, P, (70, 76, 84), 18, a)
        ah = a * float(seg(t, W(6, 'cablaj') - 0.1, W(6, 'cablaj') + 0.3)) * (0.7 + 0.3 * math.sin(t * 6))
        D.line2(C, P, (255, 210, 31), 6, ah)
    F.label(C, 'l_plug', CONN, (600, 520), W(6, 'mufa') - 0.1, None)
    F.spr(C, 'l_wire', 90, 790, W(6, 'cablaj') - 0.1, None)
    F.spr(C, 'g_before', 540, 1010, W(7, 'inainte') - 0.1, L(E.OUT) + 0.3, anchor='tc')
    F.spr(C, 'c_plugs', 540, 1096, W(7, 'mufele') - 0.1, L(E.OUT) + 0.3, anchor='tc')
    F.spr(C, 'c_wires', 540, 1182, W(7, 'cablajul') - 0.1, L(E.OUT) + 0.3, anchor='tc')

# ------------------------------------------------------------------ planuri
KB_COIL = S.kb_on('upper', 'shut', np.array([0, 0, 150.0]), 1.45, ty=700)
KB_CONN = S.kb_on('hero', 'full', CONN, 1.5, ty=560)
SHOTS = S.opening(E, 'upper', S.COIL, dive_kb=((1.0, 0, 120), (1.0, 0, 100)), fx_dive=[fx_coil(E.T_N + 0.3)]) + [
 Shot('upper', L(3), L(4), st='shut', seq=[('vopen', W(3, 'ridica') - 0.05, W(3, 'ridica') + 0.2)], tr=('xf', 0.3),
      kb=[(L(3), 1.0, 0, 100), (L(4), 1.05, 0, 110)], fx=[fx_coil(W(3, 'bobina') - 0.1, W(3, 'supapa') + 1.4), fx_valve_flow(W(3, 'ridica'))], ov=ov_em),
 Shot('upper', L(4), L(5), st='shut', tr=('xf', 0.3), kb=[(L(4), 1.2, KB_COIL[1] * 0.6, KB_COIL[2] * 0.6), (L(5), ) + KB_COIL],
      fx=[fx_coil(L(4) - 0.3, W(4, 'intrerupe') + 0.1), fx_faults], ov=ov_faults),
 Shot('blank', L(5), L(6), st='none', tr=('xf', 0.3), ov=ov_piezo),
 Shot('hero', L(6), W(6, 'iar') - 0.1, st='shut', tr=('xf', 0.3), kb=[(L(6), 1.0, 0, 0), (W(6, 'iar'), 1.04, 0, 0)], ov=ov_rare, dim=lambda t: 0.62),
 Shot('hero', W(6, 'iar') - 0.1, L(E.OUT), st='full', tr=('xf', 0.3), kb=[(W(6, 'iar'), 1.3, KB_CONN[1] * 0.8, KB_CONN[2] * 0.8), (L(7), ) + KB_CONN, (L(E.OUT), ) + KB_CONN],
      ov=ov_plug),
 S.ending(E),
]
