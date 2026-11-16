# Piese comune pentru episoadele 3–13: deschiderea (injectorul intreg -> sectiune -> apropiere), finalul (jeturi bune),
# planul cu simptomele, eticheta de previzualizare (cat timp vocea e provizorie), utilitare de etichete.
import os, json, math
import numpy as np, cv2
import icomp as IC, ifx as F, ikit as K
import fxlib as X
from icomp import Shot
from fxlib import seg

BALL = np.array([0, 0, 137.222]); TIP = np.array([0, 0, 0.6]); COIL = np.array([0, 0, 152.0])
SAC = np.array([0, 0, 1.45]); HOLES = [np.array(d, float) for d in F.J['hole_dirs']]
FIRST = {3: 'depunerile', 4: 'calamina', 5: 'saiba', 6: 'murdaria', 7: 'benzina', 8: 'adblue', 9: 'motorina', 10: 'pilitura',
         11: 'injectorul', 12: 'defectele', 13: 'uzura'}

class Ep:
    def __init__(s, n):
        s.n = n; s.ep = 'ep%d' % n
        s.Q = IC.Cues(os.path.join(IC.HERE, s.ep, 'vo', 'cues.json'))
        tl = json.load(open(os.path.join(IC.HERE, s.ep, 'vo', 'timeline.json')))
        s.TOTAL = tl['total']; s.PROV = bool(tl.get('provisional'))
        s.W, s.L, s.LE = s.Q.W, s.Q.L, s.Q.LE
        s.NL = len(s.Q.lines); s.OUT = s.NL - 3          # primul rand din final
        s.T_C = s.W(1, 'cauza'); s.T_N = s.W(1, FIRST[n])

def scr(cam, st, P, kb=(1.0, 0, 0)):
    J = json.load(open(IC.find_plate('%s__%s' % (cam, st)) + '.json')); c = X.Cam(J, 1080, 1920); c.set2d(*kb)
    x, y, z = c.proj(np.asarray(P, float).reshape(-1, 3)); return float(x[0]), float(y[0])

def spr_common(n):
    return {'badge': K.badge_html(n), 'prev': '<div class="lb bad">PREVIZUALIZARE · VOCEA URMEAZĂ</div>'}

def glob(E):
    g0 = K.make_glob(E.ep, E.n)
    def g(t, img):
        img = g0(t, img)
        if E.PROV:
            s = IC.sprite(E.ep, 'prev'); k = IC.W / 1080.0
            if k != 1.0: s = cv2.resize(s, (max(1, int(s.shape[1] * k)), max(1, int(s.shape[0] * k))), interpolation=cv2.INTER_AREA)
            IC.blit(img, s, (540 - s.shape[1] / 2 / k) * k, 1600 * k, 0.85)
        return img
    return g

# ------------------------------------------------------------------ fluxuri
def fx_fuel(t_on=None, paths=('hp_all',), n=110, speed=38.0, size=0.11, a=0.55):
    def f(C):
        for i, pn in enumerate(paths):
            F.flow(C, pn, n, speed, np.array([1.0, 0.72, 0.45]), size, lat=0.8, seed=11 + i, t0=t_on, mode='add', shape='g', shade=0, a=a)
    return f

def fx_parts(paths, n, speed, col, size, t_on=None, t1=None, shape='d', shade=0.55, mode='over', seed=30, sz_var=0.45, glow=0.0, a=1.0, lat=0.7):
    def f(C):
        for i, pn in enumerate(paths):
            F.flow(C, pn, n, speed, np.asarray(col, float), size, lat=lat, seed=seed + i, t0=t_on, t1=t1, mode=mode, shape=shape, shade=shade, sz_var=sz_var, glow=glow, a=a)
    return f

def fx_glow_pts(pts, r_px, col, t_on, t_off=None, a=0.35, puls=0.0):
    def f(C):
        e = float(seg(C.t, t_on, t_on + 0.5)) * (1 - (float(seg(C.t, t_off, t_off + 0.5)) if t_off else 0.0))
        if e <= 0: return
        for p in pts:
            F.glow(C, np.asarray(p, float), r_px * C.k, np.asarray(col, float), a * e * (1 - puls + puls * (0.5 + 0.5 * math.sin(C.t * 7))))
    return f

def hole_exit(i, k=1.0): return SAC + HOLES[i] * 1.78 * k

# ------------------------------------------------------------------ planuri standard
def opening(E, dive_cam='upper', dive_pt=BALL, dive_kb=((1.12, 0, 60), (1.0, 0, 20)), fx_hook=(), fx_dive=(), dive_st='shut', zmax=3.4):
    W, L = E.W, E.L
    bh = scr('hero', 'shut', dive_pt, (1.07, 0, -30))
    return [
        Shot('hero', 0.0, E.T_N, st='full', wipe=('shut', E.T_C - 0.05, E.T_C + 0.85, 60),
             kb=[(0.0, 1.0, 0, 0), (E.T_N, 1.07, 0, -30)], fx=[fx_fuel(E.T_C + 0.2)] + list(fx_hook), tr=None),
        Shot(dive_cam, E.T_N, L(3), st=dive_st, tr=('dive', 0.75, bh, zmax),
             kb=[(E.T_N,) + tuple(dive_kb[0]), (L(3),) + tuple(dive_kb[1])], fx=[fx_fuel(E.T_N - 3.0, ('hp_in', 'hp_down'), 90, 32.0)] + list(fx_dive)),
    ]

def ending(E):
    t0 = E.L(E.OUT); P = K.inj_pulses(t0 - 0.2, E.TOTAL + 1, 0.7, 0.16)
    return Shot('chamberz', t0, E.TOTAL + 1, st='shut', kb=[(t0, 1.0, 0, -60), (E.TOTAL, 1.1, 0, -80)],
                fx=[lambda C: K.spray_pulses(C, P, kind='good', L=14.0, life=0.42)])

def symptoms(E, i, cards, kind='bad', smoke=True, y0=760, dy=140, extra_fx=()):
    """planul cu camera de ardere si cardurile de simptome; cards = [(sprite, cuvant[, n])]"""
    W, L, LE = E.W, E.L, E.LE
    P = K.inj_pulses(L(i) - 0.5, L(i + 1) + 0.3, 0.62, 0.17)
    fx = [lambda C: K.spray_pulses(C, P, kind=kind, L=13.0, life=0.42)]
    if smoke: fx.append(lambda C: F.smoke(C, np.array([0, -7.0, -5.0]), L(i) - 0.5, n=90, rise=(0, 0, 2.5), spread=12.0, size=2.8, a=0.4))
    def ov(C):
        for k, cd in enumerate(cards):
            sid, w = cd[0], cd[1]; nn = cd[2] if len(cd) > 2 else 1
            F.spr(C, sid, 220, y0 + k * dy, W(i, w, nn) - 0.1, LE(i) + 0.3)
    t1 = W(i, cards[0][1]) - 0.1
    return Shot('chamberz', L(i), L(i + 1), st='shut', kb=[(L(i), 1.0, 0, -140), (L(i + 1), 1.05, 0, -150)], fx=fx + list(extra_fx), ov=ov,
                dim=lambda t: 0.25 * F.pop(t, t1, LE(i) + 0.3))

def bars(C, x, y, w, h, vals, cols, prog, a=1.0, labels=None):
    """bare verticale simple (ex. cantitati pe cilindri); vals 0..1"""
    n = len(vals); gw = w / n
    for k, v in enumerate(vals):
        hh = h * v * prog
        c = np.asarray(cols[k], np.float32); c = c / 255.0 if c.max() > 1.0 else c
        F.rect(C, x + k * gw + gw * 0.18, y + h - hh, gw * 0.64, hh, c, a)

def kb_on(cam, st, P, z, tx=540, ty=960):
    """Ken Burns (zoom, dx, dy) care pune punctul 3D P la (tx, ty) pe ecran, cu zoom z"""
    x, y = scr(cam, st, P)
    dx, dy = tx - (x - 540) * z - 540, ty - (y - 960) * z - 960
    mx, my = 540 * (z - 1), 960 * (z - 1)                 # placa trebuie sa acopere tot cadrul
    return (z, float(np.clip(dx, -mx, mx)), float(np.clip(dy, -my, my)))

def comb_flash(P, t_c=-4.0, r=240, col=(1.0, 0.5, 0.15), a=0.55, delay=0.1, tau=0.16):
    """fulgerul arderii dupa fiecare injectie (P = lista de impulsuri (ton, toff))"""
    def f(C):
        e = 0.0
        for ton, toff in P:
            d = C.t - (ton + delay)
            if 0 <= d < 1.0: e = max(e, math.exp(-d / tau) * min(1.0, d / 0.04))
        if e > 0.01: F.glow(C, np.array([0, 0, t_c]), r * C.k, np.asarray(col, float), a * e)
    return f
