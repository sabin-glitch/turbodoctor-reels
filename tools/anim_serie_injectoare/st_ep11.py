# Episodul 11: injectorul fara cod si reconditionarea fara standard (codul de corectie; testul Bosch din 2013: 70% picate).
# Momentele din ep11/vo/cues.json (provizorii). Codul de pe ecran e un exemplu, nu un cod real.
import math, json, os
import numpy as np
import icomp as IC, ifx as F, ikit as K, iser as S, i2d as D
import fxlib as X
from icomp import Shot
from fxlib import seg

E = S.Ep(11); N = E.n; EP = E.ep; W, L, LE = E.W, E.L, E.LE; TOTAL = E.TOTAL
GLOB = S.glob(E)
CODE = 'A7K2 9QF4'

def sym2(icon, text, small=None, cls='warn'):
    s = '<small>%s</small>' % small if small else ''
    return '<div class="sym %s"><div class="ic">%s</div><div class="tx">%s%s</div></div>' % (cls, D.ICON2[icon], text, s)

def inj_svg(body, dark):
    return (f'<svg width="64" height="150" viewBox="0 0 64 150"><rect x="16" y="6" width="32" height="26" rx="5" fill="{dark}"/>'
            f'<rect x="12" y="30" width="40" height="40" rx="6" fill="{body}"/><rect x="50" y="40" width="12" height="10" rx="3" fill="{body}"/>'
            f'<rect x="20" y="70" width="24" height="36" rx="4" fill="{body}"/><rect x="20" y="104" width="24" height="22" fill="{dark}"/>'
            f'<path d="M26 126h12l-3 18h-6z" fill="{body}"/></svg>')

SPR = dict(S.spr_common(N), **{
 'l_code': K.lb('COD DE CORECȚIE', '', 'Scris pe corpul injectorului'),
 'ic_ecu': '<div style="width:120px;height:120px;display:flex;align-items:center;justify-content:center;border-radius:20px;background:rgba(255,255,255,.05)">'
           + D.ICON2['ecu'].replace('width="80" height="80"', 'width="96" height="96"') + '</div>',
 'c_mount': K.chk('INTRODUS LA MONTAJ'),
 'g_qty': K.lb('CÂT DĂ FIECARE INJECTOR', 'grey'),
 'l_nocode': K.lb('FĂRĂ COD', 'bad'),
 'l_bad': K.lb('MOTORUL MERGE PROST', 'bad big'),
 'g_risk': K.lb('AL DOILEA RISC', 'grey', 'Recondiționarea fără standard'),
 'x_bench': sym2('bench', 'FĂRĂ STAND DE TESTARE', None, 'bad'),
 'x_parts': sym2('part', 'FĂRĂ PIESE BUNE', None, 'bad'),
 'g_bosch': K.lb('BOSCH A TESTAT INJECTOARE RECONDIȚIONATE', 'grey', 'În afara rețelei autorizate'),
 'y2013': '<div class="lb num">2013</div>',
 'i_g': inj_svg('#9aa7b5', '#4b5563'), 'i_r': inj_svg('#ff4b4b', '#8b1d1d'),
 'l_fail': '<div class="lb bad big">AU PICAT TESTELE</div>',
 'c_bench': K.chk('TESTAT PE STAND'),
 'c_parts': K.chk('CU PIESE BUNE'),
 'c_code': K.chk('CODAT ÎN CALCULATOR LA MONTAJ'),
})

# ------------------------------------------------------------------ codul de pe corp si introducerea lui in calculator
BODY = np.array([0, 0, 112.0])
def ov_code(C):
    t = C.t; a = F.pop(t, W(3, 'cod') - 0.15, LE(3) + 0.3)
    if a > 0.003:
        bx, by = C.P(BODY); bx, by = bx / C.k, by / C.k
        ae = a * float(seg(t, W(3, 'cod') - 0.15, W(3, 'scris') + 0.2))
        D.text(C, CODE, bx, by, 17, (52, 56, 62), ae * 0.9, 'mont9', shadow=False)        # gravat pe corp
        D.rbox(C, bx - 72, by - 17, 144, 34, (255, 210, 31), a, th=3, r=8)
        D.line2(C, [(bx + 72, by), (650, by)], (255, 210, 31), 3, a)
        D.rbox(C, 650, by - 95, 390, 190, (255, 210, 31), a, th=3, fill=(8, 12, 17, 232), r=14)
        D.text(C, 'COD DE CORECȚIE', 845, by - 55, 28, (182, 194, 207), a, 'mont9')
        D.text(C, CODE, 845, by + 8, 58, (255, 255, 255), a, 'mont9')
        D.text(C, 'exemplu', 845, by + 62, 24, (150, 160, 172), a, 'mont')
    # calculatorul: codul se scrie litera cu litera
    ae = F.pop(t, W(3, 'calculator') - 0.2, LE(3) + 0.3)
    if ae > 0.003:
        D.rbox(C, 80, 1040, 920, 200, (61, 220, 132), ae, th=3, fill=(8, 12, 17, 236), r=16)
        F.spr(C, 'ic_ecu', 110, 1080, W(3, 'calculator') - 0.2, LE(3) + 0.3, popk=1.0, slide=(0, 0))
        D.text(C, 'CALCULATORUL MOTORULUI · INJECTOR 1', 260, 1095, 26, (182, 194, 207), ae, 'mont9', anchor='lm')
        n = int(len(CODE) * float(seg(t, W(3, 'calculator'), W(3, 'montaj') + 0.1)) + 0.5)
        cur = '_' if (n < len(CODE) and int(t * 4) % 2 == 0) else ''
        D.text(C, CODE[:n] + cur, 260, 1165, 62, (255, 255, 255), ae, 'mont9', anchor='lm')
    F.spr(C, 'c_mount', 1000, 950, W(3, 'montaj') - 0.05, LE(3) + 0.3, anchor='tr')

# ------------------------------------------------------------------ fara cod: cantitati diferite pe cilindri
VALS = [0.71, 0.69, 0.47, 0.72]
def ov_qty(C):
    t = C.t; a = F.pop(t, L(4) - 0.1, LE(4) + 0.35)
    if a <= 0.003: return
    x0, y0, w, h = 150, 470, 780, 380
    D.rbox(C, x0 - 40, y0 - 90, w + 80, h + 160, (70, 80, 92), a, th=2, fill=(8, 12, 17, 225), r=18)
    F.spr(C, 'g_qty', 540, y0 - 70, L(4) - 0.1, LE(4) + 0.35, anchor='tc')
    pr = float(seg(t, L(4), W(4, 'stie') + 0.4))
    cols = [(61, 220, 132), (61, 220, 132), (255, 75, 75), (61, 220, 132)]
    S.bars(C, x0, y0, w, h, VALS, cols, pr, a)
    ty = y0 + h - h * 0.70
    for k in range(13): D.line2(C, [(x0 + k * 62, ty), (x0 + k * 62 + 34, ty)], (232, 237, 243), 4, a * 0.85)
    D.text(C, 'CERUT', x0 + w - 4, ty - 24, 26, (232, 237, 243), a, 'mont9', anchor='rm')
    for k in range(4): D.text(C, 'CIL. %d' % (k + 1), x0 + w / 8 + k * w / 4, y0 + h + 34, 28, (182, 194, 207), a, 'mont9')
    F.spr(C, 'l_nocode', x0 + w / 8 + 2 * w / 4, y0 + h * (1 - VALS[2]) - 70, W(4, 'acel') - 0.1, LE(4) + 0.35, anchor='tc')
    F.spr(C, 'l_bad', 540, 1060, W(4, 'motorul') - 0.1, LE(4) + 0.35, anchor='tc')

P4 = K.inj_pulses(L(4) - 0.5, L(5) + 0.3, 0.62, 0.17)

# ------------------------------------------------------------------ reconditionarea fara standard
def ov_risk(C):
    F.spr(C, 'g_risk', 540, 390, L(5) - 0.05, LE(5) + 0.3, anchor='tc')
    F.spr(C, 'x_bench', 540, 560, W(5, 'stand') - 0.15, LE(5) + 0.3, anchor='tc')
    F.spr(C, 'x_parts', 540, 720, W(5, 'piese') - 0.15, LE(5) + 0.3, anchor='tc')

# ------------------------------------------------------------------ testul Bosch: 7 din 10 picate
RED_ORDER = [3, 0, 7, 5, 9, 2, 6]
def ov_bosch(C):
    t = C.t
    F.spr(C, 'g_bosch', 540, 380, L(6) - 0.05, LE(6) + 0.35, anchor='tc')
    F.spr(C, 'y2013', 540, 500, W(6, '2013') - 0.1, LE(6) + 0.35, anchor='tc')
    t70 = W(6, '70') - 0.15
    for k in range(10):
        x = 540 + (k % 5 - 2) * 150; y = 600 + (k // 5) * 190
        F.spr(C, 'i_g', x, y, W(6, 'injectoare') - 0.1 + 0.05 * k, LE(6) + 0.35, anchor='tc')
        if k in RED_ORDER:
            F.spr(C, 'i_r', x, y, t70 + 0.11 * RED_ORDER.index(k), LE(6) + 0.35, anchor='tc', popk=1.0, slide=(0, 0))
    a = F.pop(t, t70, LE(6) + 0.35)
    if a > 0.003:
        v = int(round(70 * float(seg(t, t70, t70 + 0.9))))
        D.text(C, '%d%%' % v, 540, 1060, 170, (255, 75, 75), a, 'anton')
    F.spr(C, 'l_fail', 540, 1160, W(6, 'picat') - 0.1, LE(6) + 0.35, anchor='tc')

# ------------------------------------------------------------------ cum eviti
def ov_do(C):
    for k, (sid, w) in enumerate((('c_bench', 'testat'), ('c_parts', 'piese'), ('c_code', 'codat'))):
        F.spr(C, sid, 540, 400 + 88 * k, W(7, w) - 0.15, LE(7) + 0.35, anchor='tc')

# ------------------------------------------------------------------ planuri
SHOTS = S.opening(E) + [
 Shot('hero', L(3), L(4), st='full', tr=('xf', 0.3), kb=[(L(3), 1.0, 0, 0), (L(4), 1.1, 0, 20)], ov=ov_code,
      dim=lambda t: 0.25 * F.pop(t, W(3, 'calculator') - 0.2, LE(3) + 0.3)),
 Shot('chamberz', L(4), L(5), st='shut', tr=('xf', 0.3), kb=[(L(4), 1.0, 0, -140), (L(5), 1.05, 0, -150)],
      fx=[lambda C: K.spray_pulses(C, P4, kind='bad', L=13.0, life=0.42)], ov=ov_qty, dim=lambda t: 0.3),
 Shot('hero', L(5), L(6), st='shut', tr=('xf', 0.3), kb=[(L(5), 1.0, 0, 0), (L(6), 1.05, 0, -20)], ov=ov_risk,
      dim=lambda t: 0.4 * F.pop(t, L(5) - 0.1, L(6) + 0.3)),
 Shot('blank', L(6), L(7), st='none', tr=('xf', 0.3), ov=ov_bosch),
 Shot('hero', L(7), L(E.OUT), st='full', tr=('xf', 0.3), kb=[(L(7), 1.0, 0, 0), (L(E.OUT), 1.05, 0, -20)], ov=ov_do,
      dim=lambda t: 0.3 * F.pop(t, L(7) - 0.1, L(E.OUT) + 0.3)),
 S.ending(E),
]
