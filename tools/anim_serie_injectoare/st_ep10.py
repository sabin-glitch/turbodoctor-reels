# Episodul 10: pilitura de la pompa (buletinele tehnice ale constructorilor: metal in pompa = pompa, rampa, toate injectoarele, tevile, filtrul;
# rezervorul si conductele golite si spalate; injectoarele nu se curata si nu se refolosesc). Momentele din ep10/vo/cues.json (provizorii).
import math, json, os
import numpy as np
import icomp as IC, ifx as F, ikit as K, iser as S, i2d as D
import fxlib as X
from icomp import Shot
from fxlib import seg

E = S.Ep(10); N = E.n; EP = E.ep; W, L, LE = E.W, E.L, E.LE; TOTAL = E.TOTAL
GLOB = S.glob(E)
METAL = np.array([0.86, 0.88, 0.92]); METAL2 = (225, 230, 238)

GREEN_HL = dict(col='#3ddc84', fill='rgba(61,220,132,.22)')
STOP_REUSE = ('<div class="stop" style="max-width:940px"><div class="ic">%s</div><div>CURĂȚAREA ȘI REFOLOSIREA<br>INJECTOARELOR'
              '<small>Niciun buletin al constructorilor nu le permite</small></div></div>') % K.ICON['stop']

SPR = dict(S.spr_common(N), **{
 'tag_pump': K.lb('ÎN POMPA DE ÎNALTĂ PRESIUNE', 'grey', 'Vedere la microscop'),
 'l_grind': K.lb('POMPA SE MACINĂ', 'bad big'),
 'sys': D.sys_svg(),
 'h_pump': D.sys_hl(['pump']), 'h_rail': D.sys_hl(['rail']), 'h_inj': D.sys_hl(['inj']), 'h_pipes': D.sys_hl(['hp', 'lp']),
 'h_filter': D.sys_hl(['filter']),
 'h_pump_new': D.sys_hl(['pump'], **GREEN_HL), 'h_inj_new': D.sys_hl(['inj'], **GREEN_HL),
 'l_fil': K.lb('PILITURA PLEACĂ PRIN RAMPĂ', 'bad', 'În toate injectoarele'),
 'l_valve': K.lb('SUPAPA DE COMANDĂ', 'hp'),
 'l_ball': K.lb('ZONA BILEI', 'bad big'),
 'g_doc': K.lb('BULETINELE TEHNICE ALE CONSTRUCTORILOR', 'grey'),
 'chip_metal': '<div class="lb bad big">DACĂ GĂSEȘTI METAL ÎN POMPĂ</div>',
 'g_repl': '<div class="lb bad big">SE SCHIMBĂ</div>',
 'g_tank': K.lb('REZERVORUL ȘI CONDUCTELE', 'grey'),
 'c_drain': K.chk('SE GOLESC'),
 'c_wash': K.chk('SE SPALĂ'),
 'st_reuse': STOP_REUSE,
 'g_alone': K.lb('POMPA SCHIMBATĂ SINGURĂ', 'grey'),
 'l_new': '<div class="lb good big">INJECTOARE NOI</div>',
 'l_dead': '<div class="lb bad big">INJECTOARE NOI, DISTRUSE</div>',
 'l_left': K.lb('DE PILITURA RĂMASĂ', 'bad'),
})

# ------------------------------------------------------------------ micro: pompa care se macina
def gap_path(lat=0.6):
    gp = F.IPath([[0, -0.1, 26], [0, -0.1, -26]], None, 1.0, smooth=0, step=0.25)
    gp.L = np.tile(np.array([lat, 0, 0]), (gp.n, 1)); return gp
GP = gap_path()

RM = X.rnd(57, 40, 4)
def fx_grind(t_on):
    def f(C):
        t = C.t
        if t < t_on: return
        for i in range(10):
            ta = t_on + (i * 0.31) % 1.4
            per = 1.1 + 0.4 * RM[i, 3]; tk = ta + per * math.floor(max(0.0, t - ta) / per)
            side = -0.1 if i % 2 else 0.1; z = 17 - 34 * RM[i, 0]
            F.sparks(C, np.array([side, -0.15, z]), tk, n=18, life=0.32, speed=6.5, size=0.13, seed=140 + i + int(tk * 10))
        F.flow(C, GP, 24, 10.0, METAL, 0.18, lat=0.3, seed=29, t0=t_on, mode='over', shape='d', shade=0.8, sz_var=0.6)
    return f

def shake_at(ta, dur=0.9, amp=4.0):
    def sh(t):
        e = float(seg(t, ta, ta + 0.08)) * (1 - float(seg(t, ta + dur * 0.6, ta + dur)))
        return (amp * e * math.sin(t * 57.0), 0.75 * amp * e * math.sin(t * 43.0 + 0.7))
    return sh

def ov_micro(C):
    F.spr(C, 'tag_pump', 540, 400, L(3) + 0.1, W(3, 'pilitura'), anchor='tc')
    F.spr(C, 'l_grind', 540, 1150, W(3, 'macina') - 0.1, W(3, 'pilitura'), anchor='tc')

# ------------------------------------------------------------------ schema: pilitura pleaca spre injectoare
SP = D.sys_paths()
def ov_sys3(C):
    t = C.t; t0 = W(3, 'pilitura') - 0.15
    F.spr(C, 'sys', D.SYS_X, D.SYS_Y, t0, L(4) + 0.2, popk=1.0, slide=(0, 0))
    a = F.pop(t, t0, L(4) + 0.2)
    D.flow2(C, SP['inj'], 80, 260.0, METAL2, 4.0, t0=W(3, 'pilitura'), a=a, seed=3, glow=0.5)
    F.spr(C, 'h_pump', D.SYS_X, D.SYS_Y, t0, L(4) + 0.2, popk=1.0, slide=(0, 0))
    F.spr(C, 'h_rail', D.SYS_X, D.SYS_Y, W(3, 'rampa') - 0.1, L(4) + 0.2, popk=1.0, slide=(0, 0))
    F.spr(C, 'h_inj', D.SYS_X, D.SYS_Y, W(3, 'injectoarele') - 0.1, L(4) + 0.2, popk=1.0, slide=(0, 0))
    F.spr(C, 'l_fil', 540, 390, W(3, 'pilitura') - 0.05, LE(3) + 0.35, anchor='tc')
    px, py = D.sys_pt('pump')
    for i in range(4):                                         # scantei la pompa
        ph = (t * 1.7 + i * 0.25) % 1.0
        if ph < 0.35: D.dots2(C, np.array([[px + 60 * math.cos(i * 1.9 + t), py + 50 * math.sin(i * 2.3 + t)]]), 5.0 * (1 - ph / 0.35), (255, 200, 120), a, glow=0.8)

# ------------------------------------------------------------------ supapa de comanda: pilitura se depune la bila
RS = X.rnd(77, 24, 4)
def fx_valve_metal(t_on):
    def f(C):
        t = C.t
        F.flow(C, 'cc_R', 18, 3.0, METAL, 0.06, lat=0.6, seed=43, t0=t_on - 1.0, mode='over', shape='d', shade=0.85, sz_var=0.5)
        for i in range(14):
            ta = t_on + i * 0.17
            if t < ta: continue
            a = 2 * math.pi * RS[i, 0]; uu = np.array([math.cos(a), math.sin(a), 0.0])
            if uu[1] < -0.3: uu[1] = -uu[1]
            p = uu * (0.56 + 0.05 * RS[i, 1]) + F.EZ * (136.62 + 0.05 * RS[i, 2])
            F.dots3(C, p, 0.03 + 0.02 * RS[i, 3], METAL, 1.0, shade=0.9, ztest=False)
            F.dots3(C, p, 0.06, np.array([1.0, 0.3, 0.25]), 0.7 * (0.55 + 0.45 * math.sin((t - ta) * 10)), shape='r', shade=0, ztest=False)
            if i % 3 == 0: F.sparks(C, p, ta + 0.05, n=12, life=0.28, speed=0.8, size=0.01, seed=95 + i)
    return f

VPT = S.BALL + np.array([0.55, 0, 0.1]) + F.NR * 0.02
def ov_valve(C):
    F.label(C, 'l_valve', VPT, (1040, 1150), W(4, 'supapa') - 0.1, W(4, 'zona') - 0.1, anchor='tr')
    F.label(C, 'l_ball', VPT, (1040, 1150), W(4, 'zona') - 0.1, LE(4) + 0.3, anchor='tr')

# ------------------------------------------------------------------ buletinele: ce se schimba
def ov_sys5(C):
    t = C.t; t0 = L(5) - 0.1; te = L(6) + 0.2
    F.spr(C, 'sys', D.SYS_X, D.SYS_Y, t0, te, popk=1.0, slide=(0, 0))
    a = F.pop(t, t0, te)
    D.flow2(C, SP['inj'], 60, 120.0, METAL2, 3.5, a=0.7 * a, seed=5, glow=0.3)
    F.spr(C, 'g_doc', 540, 390, L(5) - 0.05, W(5, 'daca') - 0.05, anchor='tc')
    F.spr(C, 'chip_metal', 540, 380, W(5, 'daca') - 0.05, W(5, 'schimba') - 0.05, anchor='tc')
    F.spr(C, 'g_repl', 540, 380, W(5, 'schimba') - 0.05, te, anchor='tc')
    for sid, w, n in (('h_pump', 'pompa', 2), ('h_rail', 'rampa', 1), ('h_inj', 'injectoarele', 1), ('h_pipes', 'tevile', 1), ('h_filter', 'filtrul', 1)):
        F.spr(C, sid, D.SYS_X, D.SYS_Y, W(5, w, n) - 0.1, te, popk=1.0, slide=(0, 0))

# ------------------------------------------------------------------ rezervorul se goleste si se spala; injectoarele nu se refolosesc
def fx_wash(t_on):
    def f(C):
        e = float(seg(C.t, t_on, t_on + 0.4)) * (1 - float(seg(C.t, t_on + 1.8, t_on + 2.6)))
        if e <= 0: return
        for k in range(5):
            F.glow(C, np.array([-180 + 90 * k, 90, 30 + 10 * math.sin(C.t * 3 + k)]), 140 * C.k, np.array([0.55, 0.85, 1.0]), 0.3 * e)
    return f

def ov_tank(C):
    F.spr(C, 'g_tank', 540, 390, L(6) - 0.05, W(6, 'iar') + 0.1, anchor='tc')
    F.spr(C, 'c_drain', 540, 478, W(6, 'golesc') - 0.1, W(6, 'iar') + 0.1, anchor='tc')
    F.spr(C, 'c_wash', 540, 566, W(6, 'spala') - 0.1, W(6, 'iar') + 0.1, anchor='tc')

def ov_reuse(C):
    t = C.t
    F.spr(C, 'st_reuse', 540, 1060, W(6, 'niciun') - 0.1, L(7) + 0.2, anchor='tc')
    ax = F.pop(t, W(6, 'refolosirea') - 0.1, L(7) + 0.2, 0.15, 0.25)
    if ax > 0.003:
        pr = float(seg(t, W(6, 'refolosirea') - 0.1, W(6, 'refolosirea') + 0.35))
        D.line2(C, [(330, 420), (750, 980)], (255, 75, 75), 22, ax, prog=pr)
        D.line2(C, [(750, 420), (330, 980)], (255, 75, 75), 22, ax, prog=float(seg(t, W(6, 'refolosirea') + 0.1, W(6, 'refolosirea') + 0.45)))

# ------------------------------------------------------------------ pe scurt: pompa noua singura, pilitura ramasa omoara injectoarele noi
def ov_sys7(C):
    t = C.t; t0 = L(7) - 0.1; te = L(E.OUT) + 0.2
    F.spr(C, 'sys', D.SYS_X, D.SYS_Y, t0, te, popk=1.0, slide=(0, 0))
    a = F.pop(t, t0, te)
    D.flow2(C, SP['rail_inj'], 60, 140.0, METAL2, 4.0, a=a, seed=8, glow=0.5)
    F.spr(C, 'h_pump_new', D.SYS_X, D.SYS_Y, W(7, 'pompa') - 0.1, te, popk=1.0, slide=(0, 0))
    F.spr(C, 'g_alone', 540, 390, W(7, 'pompa') - 0.1, W(7, 'injectoare') - 0.05, anchor='tc')
    F.spr(C, 'h_inj_new', D.SYS_X, D.SYS_Y, W(7, 'injectoare') - 0.1, W(7, 'distruse') + 0.15, popk=1.0, slide=(0, 0))
    F.spr(C, 'h_inj', D.SYS_X, D.SYS_Y, W(7, 'distruse') - 0.1, te, popk=1.0, slide=(0, 0))
    F.spr(C, 'l_new', 540, 380, W(7, 'injectoare') - 0.05, W(7, 'distruse') - 0.05, anchor='tc')
    F.spr(C, 'l_dead', 540, 380, W(7, 'distruse') - 0.05, te, anchor='tc')
    F.spr(C, 'l_left', 1040, 1180, W(7, 'pilitura') - 0.1, te, anchor='tr')

# ------------------------------------------------------------------ planuri
SHOTS = S.opening(E, 'upper', S.BALL, fx_dive=[S.fx_parts(('hp_in', 'hp_down'), 40, 32.0, METAL, 0.3, shade=0.85, glow=0.3)]) + [
 Shot('microf', L(3), W(3, 'pilitura') - 0.1, st='mdry', tr=('xf', 0.3), kb=[(L(3), 1.04, 0, 0), (W(3, 'pilitura'), 1.12, 0, 0)],
      shake=shake_at(W(3, 'macina') - 0.1, 1.0, 4.0), fx=[fx_grind(L(3) + 0.3)], ov=ov_micro),
 Shot('blank', W(3, 'pilitura') - 0.1, L(4), st='none', tr=('xf', 0.3), ov=ov_sys3),
 Shot('valve', L(4), L(5), st='shut', tr=('xf', 0.3),
      kb=[(L(4), 1.0, 0, -60), (W(4, 'zona') - 0.2, 1.0, 0, -60), (L(5), ) + S.kb_on('valve', 'shut', S.BALL, 1.45)],
      fx=[fx_valve_metal(L(4) + 0.2)], ov=ov_valve),
 Shot('blank', L(5), L(6), st='none', tr=('xf', 0.3), ov=ov_sys5),
 Shot('tank', L(6), W(6, 'iar') - 0.1, st='dry', seq=[('empty', W(6, 'golesc') - 0.1, W(6, 'golesc') + 1.0)], tr=('xf', 0.3),
      kb=[(L(6), 1.0, 0, 40), (W(6, 'iar'), 1.05, 0, 30)], fx=[fx_wash(W(6, 'spala') - 0.2)], ov=ov_tank),
 Shot('hero', W(6, 'iar') - 0.1, L(7), st='full', tr=('xf', 0.3), kb=[(W(6, 'iar'), 1.0, 0, 0), (L(7), 1.04, 0, -10)], ov=ov_reuse,
      dim=lambda t: 0.35 * F.pop(t, W(6, 'niciun') - 0.1, L(7) + 0.3)),
 Shot('blank', L(7), L(E.OUT), st='none', tr=('xf', 0.3), ov=ov_sys7),
 S.ending(E),
]
