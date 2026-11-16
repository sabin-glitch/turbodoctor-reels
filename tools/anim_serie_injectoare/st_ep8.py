# Episodul 8: AdBlue in rezervorul de motorina (GM TechLink, ADAC). Uree + apa, coroziune si cristale albe, tot sistemul de alimentare.
# Momentele din ep8/vo/cues.json (provizorii).
import math, json, os
import numpy as np
import icomp as IC, ifx as F, ikit as K, iser as S, i2d as D
import fxlib as X
from icomp import Shot
from fxlib import seg

E = S.Ep(8); N = E.n; EP = E.ep; W, L, LE = E.W, E.L, E.LE; TOTAL = E.TOTAL
GLOB = S.glob(E)
ADB = np.array([0.75, 0.94, 1.0]); CRYST = np.array([0.95, 0.97, 1.0]); CRY2 = (240, 246, 255)

SPR = dict(S.spr_common(N), **{
 'l_adb': K.lb('ADBLUE ÎN REZERVOR', 'water'),
 'g_urea': K.lb('32,5% UREE', 'grey'),
 'g_water': K.lb('RESTUL: APĂ', 'water'),
 'l_corr': K.lb('COROZIUNE', 'bad'),
 'l_cryst': K.lb('CRISTALE ALBE', 'bad'),
 'sys': D.sys_svg(),
 'h_pump': D.sys_hl(['pump']), 'h_inj': D.sys_hl(['inj']),
 'h_all': D.sys_hl(['pump', 'inj', 'rail', 'hp', 'lp', 'filter', 'tank']),
 'l_gap': K.lb('JOCURI DE CÂȚIVA MICRONI', 'bad'),
 'chip_on': '<div class="lb bad big">DACĂ MOTORUL A FOST PORNIT</div>',
 'q_gm': '<div class="quote sm red"><q>„ÎNLOCUIREA ÎNTREGULUI SISTEM DE ALIMENTARE”</q><small>General Motors, dacă motorul a fost pornit</small></div>',
 'x_key': K.chk('NU PUI CONTACTUL', False),
 'c_drain': K.chk('REZERVORUL SE GOLEȘTE'),
 'c_wash': K.chk('ȘI SE SPALĂ'),
})

# ------------------------------------------------------------------ rezervorul cu AdBlue: picaturi si diagrama compozitiei
RD = X.rnd(81, 20, 3)
def fx_adb_drops(t_on, n=12):
    def f(C):
        t = C.t
        for i in range(n):
            ta = t_on + i * 0.3
            if t < ta: continue
            u = t - ta; x = -215 + 30 * RD[i, 0]; z = 168 - 0.5 * 900 * u * u
            if z < 101:
                tz = math.sqrt(2 * (168 - 101) / 900.0); zz = 101 - 60 * (u - tz)           # trece prin motorina si coboara spre fund
                if zz < 22:
                    du = (22 - zz) / 60.0                                                   # ajunsa la fund: se intinde in stratul de AdBlue
                    if du < 0.6: F.glow(C, np.array([x, 90, 12.0]), (50 + 160 * du) * C.k, ADB, 0.5 * (1 - du / 0.6))
                    continue
                F.dots3(C, np.array([x, 90, zz]), 8.5, ADB, 0.95, shade=0.6, ztest=False); continue
            F.dots3(C, np.array([x, 90, z]), 9.5, ADB, 1.0, shade=0.6, ztest=False)
        e = float(seg(t, W(3, 'apa'), W(3, 'apa') + 0.5)) * (1 - float(seg(t, LE(3), LE(3) + 0.6)))
        if e > 0.01:
            for k in range(9): F.glow(C, np.array([-232 + 58 * k, 90, 10.0]), 110 * C.k, ADB, 0.2 * e * (0.8 + 0.2 * math.sin(t * 4 + k)))
    return f

def ov_comp(C):
    t = C.t; tp = W(3, 'uree') - 0.1; te = LE(3) + 0.35
    a = F.pop(t, tp, te, 0.3, 0.3)
    if a > 0.003:
        D.rbox(C, 150, 360, 780, 330, (70, 80, 92), a, th=2, fill=(8, 12, 17, 225), r=18)
        D.text(C, 'UREE DIZOLVATĂ ÎN APĂ', 540, 525, 52, (232, 237, 243), a * (1 - float(seg(t, W(3, '32') - 0.35, W(3, '32') - 0.1))), 'anton')
        pr = float(seg(t, W(3, '32') - 0.2, W(3, '32') + 1.0))
        D.pie(C, 330, 525, 125, [0.325, 0.675], [(240, 244, 248), (47, 155, 255)], pr, a, hole=0.56)
        D.text(C, '32,5%', 330, 525, 50, (255, 255, 255), a * float(seg(t, W(3, '32') - 0.1, W(3, '32') + 0.3)), 'anton')
        F.spr(C, 'g_urea', 500, 440, W(3, '32') - 0.1, te)
        F.spr(C, 'g_water', 500, 540, W(3, 'restul') - 0.1, te)
    F.label(C, 'l_adb', TJ_W, (1040, 1150), W(3, 'adblue') - 0.1, LE(3) + 0.3, anchor='tr')
TJ = json.load(open(os.path.join(IC.HERE, 'blend', 'tank.json'))); TJ_W = np.array(TJ['pts']['water'], float) + np.array([120, 0, 0])

# ------------------------------------------------------------------ micro: coroziune si cristale pe pereti
RC = X.rnd(83, 120, 4)
def fx_cryst(t_on, k_max=1.0):
    def f(C):
        n = int(np.clip((C.t - t_on) * 30, 0, 90) * k_max)
        if n <= 0: return
        side = np.where(np.arange(n) % 2 == 0, -1.0, 1.0)
        P = np.stack([side * (1.5 - 0.1 - 0.35 * RC[:n, 2]), -0.12 + 0 * side, 20 - RC[:n, 0] * 40], -1)
        F.dots3(C, P, 0.12 + 0.16 * RC[:n, 1], CRYST, 1.0, shade=0.35, ztest=False)
    return f

def fx_gap(a=0.45):
    gp = F.IPath([[0, -0.1, 26], [0, -0.1, -26]], None, 1.0, smooth=0, step=0.25)
    gp.L = np.tile(np.array([0.6, 0, 0]), (gp.n, 1))
    return lambda C: F.flow(C, gp, 30, 13.0, np.array([1.0, 0.75, 0.5]), 0.12, lat=0.9, seed=5, mode='add', shape='g', shade=0, a=a)

def ov_micro(C):
    F.label(C, 'l_corr', [-1.2, -0.1, 8.0], (90, 640), W(4, 'corodeaza') - 0.1, LE(4) + 0.3)
    F.label(C, 'l_cryst', [1.25, -0.1, -6.0], (1040, 1150), W(4, 'cristale') - 0.1, LE(4) + 0.3, anchor='tr')

# ------------------------------------------------------------------ schema: cristalele ajung in pompa si injectoare; GM: tot sistemul
SP = D.sys_paths()
LP_INJ = [D.Poly(np.vstack([SP['lp'].p, p.p[1:]])) for p in SP['inj']]
def ov_sys(C):
    t = C.t; t0 = L(5) - 0.1; te = L(7) + 0.2
    F.spr(C, 'sys', D.SYS_X, D.SYS_Y, t0, te, popk=1.0, slide=(0, 0))
    a = F.pop(t, t0, te)
    D.flow2(C, LP_INJ, 80, 300.0, CRY2, 4.5, t0=t0 + 0.2, a=a, seed=4, glow=0.35)
    F.spr(C, 'h_pump', D.SYS_X, D.SYS_Y, W(5, 'pompa') - 0.1, L(6), popk=1.0, slide=(0, 0))
    F.spr(C, 'h_inj', D.SYS_X, D.SYS_Y, W(5, 'injectoare') - 0.1, L(6), popk=1.0, slide=(0, 0))
    F.spr(C, 'l_gap', 540, 390, W(5, 'jocurile') - 0.1, LE(5) + 0.3, anchor='tc')
    F.spr(C, 'chip_on', 540, 390, L(6) - 0.05, W(6, 'general') - 0.05, anchor='tc')
    F.spr(C, 'h_all', D.SYS_X, D.SYS_Y, W(6, 'inlocuirea') - 0.1, te, popk=1.0, slide=(0, 0))
    F.spr(C, 'q_gm', 540, 352, W(6, 'general') - 0.1, LE(6) + 0.35, anchor='tc')

def ov_do(C):
    for k, (sid, w) in enumerate((('x_key', 'contactul'), ('c_drain', 'goleste'), ('c_wash', 'spala'))):
        F.spr(C, sid, 540, 400 + 88 * k, W(7, w) - 0.1, LE(7) + 0.3, anchor='tc')

def fx_wash(t_on):
    def f(C):
        e = float(seg(C.t, t_on, t_on + 0.4)) * (1 - float(seg(C.t, t_on + 2.0, t_on + 2.8)))
        if e <= 0: return
        for k in range(5):
            F.glow(C, np.array([-180 + 90 * k, 90, 30 + 10 * math.sin(C.t * 3 + k)]), 140 * C.k, np.array([0.55, 0.85, 1.0]), 0.3 * e)
    return f

# ------------------------------------------------------------------ planuri
SHOTS = S.opening(E, 'upper', S.BALL, fx_dive=[S.fx_parts(('hp_in', 'hp_down'), 36, 32.0, CRYST, 0.3, shade=0.4)]) + [
 Shot('tank', L(3), L(4), st='adb', tr=('xf', 0.3), kb=[(L(3), 1.0, 0, 40), (L(4), 1.05, 0, 30)], fx=[fx_adb_drops(L(3) + 0.1)], ov=ov_comp),
 Shot('microf', L(4), L(5), st='mclean', seq=[('mrust1', W(4, 'corodeaza') - 0.1, W(4, 'corodeaza') + 0.9)], tr=('xf', 0.3),
      kb=[(L(4), 1.0, 0, 0), (L(5), 1.06, 0, 0)], fx=[fx_gap(), fx_cryst(W(4, 'cristale') - 0.4)], ov=ov_micro),
 Shot('blank', L(5), L(7), st='none', tr=('xf', 0.3), ov=ov_sys),
 Shot('tank', L(7), L(E.OUT), st='adb', seq=[('empty', W(7, 'goleste') - 0.1, W(7, 'goleste') + 1.1)], tr=('xf', 0.3),
      kb=[(L(7), 1.0, 0, 40), (L(E.OUT), 1.05, 0, 30)], fx=[fx_wash(W(7, 'spala') - 0.2)], ov=ov_do),
 S.ending(E),
]
