# Povestea filmului: planuri, treceri intre stari, particule. Timpul local al planului = u (secunde).
import math
import numpy as np
import fxlib as X, shots as S, gas as G, layout as L
from fxlib import hexc, ramp, seg, win, flow, ease

C_EXH = hexc(0xff7216); C_EXH2 = hexc(0xffa64a); C_EGR = hexc(0xf6c98c); C_AIR = hexc(0x45b0ff)
C_SOOT = hexc(0x0c0c0d); C_COOL = hexc(0xff4fa6); C_STEAM = hexc(0xf1f5ff); C_OIL = hexc(0xe0991c); C_FUEL = hexc(0xf0e68a)
C_FIRE = hexc(0xff8a1e); C_ASH = hexc(0xd9d2c3); C_OK = hexc(0x35d07f); C_BAD = hexc(0xff4338)

def lighten(c, f):
    c = np.asarray(c, np.float64); return c + (1 - c) * f

class Shot:
    def __init__(s, id, t0, t1, cam, states, kind='plate', zoom=(1.0, 1.05), pan=((0, 0), (0, 0)), loop=None, fx=None, dim=None, xf=True, ease=False, grade=None):
        s.id, s.t0, s.t1, s.cam, s.states, s.kind = id, t0, t1, cam, states, kind
        s.zoom, s.pan, s.loop, s.fx, s.dim, s.xf, s.ease = zoom, pan, loop, fx, dim, xf, ease
        s.grade = grade                                  # (castig, gama) aplicate imaginii randate, inainte de particule
        s._cam = None
    def layers(s, u):
        w = [1.0] + [0.0] * (len(s.states) - 1)
        for i in range(1, len(s.states)):
            a = float(seg(u, *s.states[i][1])); w[i] = a
            for j in range(i): w[j] *= (1 - a)
        return [(st[0], wi) for st, wi in zip(s.states, w)]

def gas(cv, cam, path, t, n, speed, col=None, size=2.0, seed=1, t0=None, t1=None, a=1.0, lat=0.8, tails=2, dt=0.016, colf=None,
        swirl=0.0, af=None, glow=0.2, core=0.6, zbias=0.004, span=None):
    """curent de gaze: puncte luminoase cu coada scurta, de-a lungul unui traseu"""
    for j in range(tails + 1):
        P, al, sf, r = flow(path, t - j * dt, n, speed, seed, lat, t0, t1, swirl=swirl, span=span)
        c = colf(sf, r) if colf is not None else col
        if af is not None: al = al * af(sf, r)
        x, y, z = cam.proj(P); rp = cam.px(size * (0.75 + 0.5 * r[:, 4]), z) * (1 - 0.2 * j)
        al = al * a * (1 - 0.32 * j)
        if j == 0 and glow > 0: cv.dots(x, y, z, rp * 2.0, c, al * glow, 'add', 'g', zbias=zbias)
        cv.dots(x, y, z, rp * core, lighten(c, 0.38 if j == 0 else 0.15), al * (0.96 if j == 0 else 0.55), 'over', 'd', zbias=zbias)

# ------------------------------------------------------------------ planuri
def exh_col(sf, r):
    return ramp(sf, [0, G.F_DPF0, G.F_DPF1, 1], [C_EXH, C_EXH, C_EXH2, C_EXH2])

def fx_route(u, cam, cv, k):
    t0 = 0.9
    for i, p in enumerate(G.RUN):
        gas(cv, cam, p, u + 0.13 * i, 50, 300, C_EXH, 1.6, seed=20 + i, t0=t0 - 0.35)
    gas(cv, cam, G.EXH, u, 2000, 330, size=1.7, seed=1, t0=t0, colf=exh_col)

def fx_egr(u, cam, cv, k):
    for i, p in enumerate(G.RUN):
        gas(cv, cam, p, u + 0.13 * i, 50, 300, C_EXH, 1.6, seed=20 + i, a=0.6)
    gas(cv, cam, G.EXH, u, 2000, 330, size=1.7, seed=1, colf=exh_col, a=0.5)
    te = 0.5
    ec = lambda sf, r: ramp(sf, [0, G.G_COOL0, G.G_COOL1, 1], [C_EXH2, C_EXH2, C_EGR, C_EGR])
    gas(cv, cam, G.EGR, u, 1300, 300, size=1.8, seed=3, t0=te, colf=ec)
    gas(cv, cam, G.AIR, u, 420, 330, C_AIR, 1.8, seed=4)
    t_mix = te + G.EGR.len / 300.0
    sh = 0.34 * float(seg(u, t_mix, t_mix + 0.9))
    cc = lambda sf, r: np.where((r[:, 5] < sh)[:, None], C_EGR[None, :], C_AIR[None, :])
    gas(cv, cam, G.CHG, u, 1000, 360, size=1.8, seed=5, colf=cc, swirl=0.02)

# ---- filtrul de particule in sectiune: canale de intrare (pare) si de iesire (impare) pe cele doua fete taiate
P6 = L.DPF_P; Z0 = L.DPF_Z0; Z1 = L.DPF_Z1
def _dpf_tab(n, seed):
    r = X.rnd(seed, n, 10)
    face = (r[:, 0] < 0.5).astype(np.int64)                 # 0: fata y = 0 (canale dupa x), 1: fata x = 0 (canale dupa y)
    ch = 2 * (1 + (r[:, 1] * 5).astype(np.int64))           # canal de intrare: 2, 4, 6, 8, 10
    side = np.where(r[:, 2] < 0.5, -1, 1); side = np.where(ch >= 10, -1, side)
    zc = Z0 + 14 + r[:, 3] * (Z1 - Z0 - 34)                 # adancimea la care trece prin perete
    return r, face, ch, side, zc

def _dpf_pos(face, a, b, z):
    """a = coordonata de-a lungul fetei (x pe fata y=0, y pe fata x=0), b = adancimea in canal (negativa), z = pe curgere"""
    xl = np.where(face == 0, a, b); yl = np.where(face == 0, b, a)
    return L.M0[None, :] + L.MX[None, :] * xl[:, None] + L.MY[None, :] * yl[:, None] + L.MD[None, :] * z[:, None]

def dpf_gas(cv, cam, u, n=620, speed=62.0, seed=11, a=1.0, soot_k=0.0, clean=None, t0=None, size=0.8):
    """gaze care coboara prin canalele de intrare, trec prin peretele poros si ies prin canalele vecine"""
    r, face, ch, side, zc = _dpf_tab(n, seed)
    zin = Z0 - 26.0; zout = Z1 + 14.0; cross = 9.0
    D = (zout - zin) + cross
    for j in range(3):
        d = (r[:, 4] * D + (u - j * 0.02) * speed * (0.85 + 0.3 * r[:, 5])) % D
        d1 = zc - zin
        k = np.clip((d - d1) / cross, 0, 1)                   # 0 in canalul de intrare, 1 in cel de iesire
        z = zin + np.minimum(d, d1) + np.maximum(d - d1 - cross, 0) + k * 2.5
        lim = 1.25 - 0.75 * soot_k
        off = (r[:, 6] - 0.5) * 2 * lim
        a_pos = ch * P6 + off * (1 - k) + side * P6 * ease(k) + (r[:, 7] - 0.5) * 2.2 * k
        b_pos = np.where((k > 0.02) & (k < 0.98), 0.35, -0.35 - r[:, 8] * (1.6 - 0.9 * soot_k))
        P = _dpf_pos(face, a_pos, b_pos, z)
        al = np.clip((d) / 8.0, 0, 1) * np.clip((D - d) / 10.0, 0, 1) * a
        if t0 is not None: al = al * np.clip(((u - t0) * speed * 1.6 - (z - zin)) / 12.0, 0, 1)
        mid = (k > 0.02) & (k < 0.98)
        col = ramp(k, [0, 0.5, 1], [C_EXH, hexc(0xff8a26), clean if clean is not None else hexc(0xff9632)])
        x, y, zz = cam.proj(P); rp = cam.px(size * (0.8 + 0.4 * r[:, 9]), zz) * (1 - 0.2 * j) * np.where(mid, 0.7, 1.0)
        al = al * (1 - 0.34 * j) * np.where(mid, 0.75, 1.0)
        if j == 0: cv.dots(x, y, zz, rp * 2.0, col, al * 0.16, 'add', 'g', zbias=0.0012)
        cv.dots(x, y, zz, rp * 0.62, lighten(col, 0.3 if j == 0 else 0.1), al * (0.96 if j == 0 else 0.5), 'over', 'd', zbias=0.0012)

def dpf_soot(cv, cam, u, n=420, speed=62.0, seed=12, a=1.0, col=None, size=0.72, hold=60.0, t0=None, stick=True):
    """funinginea vine cu gazele si ramane lipita de perete, la locul in care gazele trec prin el"""
    r, face, ch, side, zc = _dpf_tab(n, seed)
    zin = Z0 - 26.0
    D = (zc - zin) + hold
    d = (r[:, 4] * D + u * speed * (0.85 + 0.3 * r[:, 5])) % D
    d1 = zc - zin
    st = np.clip((d - d1) / 4.0, 0, 1)
    z = zin + np.minimum(d, d1)
    off = (r[:, 6] - 0.5) * 2 * 1.2
    a_pos = ch * P6 + off * (1 - st) + side * 2.25 * st
    b_pos = -0.35 - r[:, 8] * 1.5
    P = _dpf_pos(face, a_pos, b_pos, z)
    al = np.clip(d / 8.0, 0, 1) * (1 - np.clip((d - d1 - 6.0) / (hold - 6.0), 0, 1) ** 0.7) * a
    if t0 is not None: al = al * np.clip(((u - t0) * speed * 1.6 - (z - zin)) / 12.0, 0, 1)
    x, y, zz = cam.proj(P); rp = cam.px(size * (0.7 + 0.6 * r[:, 9]), zz)
    cv.dots(x, y, zz, rp, C_SOOT if col is None else col, al * 0.95, 'over', 'd', zbias=0.0012)

def fx_dpf(u, cam, cv, k):
    kk = float(seg(u, 1.2, 5.6))
    dpf_gas(cv, cam, u, soot_k=kk, t0=0.15)
    dpf_soot(cv, cam, u, t0=0.3)


def puffs(cv, cam, p0, dirv, t, n, life, speed, spread, col, s0, s1, a=1.0, seed=31, t0=None, t1=None, grav=(0, 0, 0), mode='over',
          shape='g', zbias=0.004, ztest=True, drag=0.0, col1=None, src=None):
    """emisie continua dintr-un punct (sau dintr-o lista de puncte src): particule care se nasc, se departeaza, cresc si se sting"""
    r = X.rnd(seed, n, 10)
    age = ((t / life + r[:, 0]) % 1.0) * life
    born = t - age
    al = np.clip(age / (0.12 * life), 0, 1) * np.clip(1 - age / life, 0, 1) ** 1.1 * a
    if t0 is not None: al = al * (born >= t0)
    if t1 is not None: al = al * (born <= t1)
    d = np.asarray(dirv, np.float64)[None, :] + (r[:, 1:4] - 0.5) * 2 * spread
    d /= np.linalg.norm(d, axis=1)[:, None]
    tt = age if drag <= 0 else (1 - np.exp(-drag * age)) / drag
    base = np.asarray(p0, np.float64)[None, :] if src is None else np.asarray(src, np.float64)[(r[:, 6] * len(src)).astype(np.int64)]
    P = base + d * (speed * (0.55 + 0.9 * r[:, 4]) * tt)[:, None] + 0.5 * np.asarray(grav, np.float64)[None, :] * (age ** 2)[:, None]
    f = age / life
    c = np.asarray(col, np.float64) if col1 is None else np.asarray(col)[None, :] * (1 - f)[:, None] + np.asarray(col1)[None, :] * f[:, None]
    x, y, z = cam.proj(P); rp = cam.px(s0 + (s1 - s0) * f, z) * (0.8 + 0.4 * r[:, 5])
    cv.dots(x, y, z, rp, c, al, mode, shape, zbias=zbias, ztest=ztest)
    return P, al

def signal(cv, cam, path, t, n, speed, col, size=1.25, seed=41, a=1.0, cut=None):
    """semnalul de presiune care urca prin teava / furtun pana la senzor (desenat peste piese, ca o radiografie)"""
    for j in range(3):
        P, al, sf, r = flow(path, t - j * 0.03, n, speed, seed, lat=0.25, jit=0.03, fade=10.0)
        if cut is not None: al = al * np.clip((cut[0] - sf) / 0.03, cut[1], 1)
        x, y, z = cam.proj(P); rp = cam.px(size, z) * (1 - 0.2 * j)
        if j == 0: cv.dots(x, y, z, rp * 2.4, col, al * a * 0.5, 'add', 'g', ztest=False)
        cv.dots(x, y, z, rp * 0.8, lighten(col, 0.45), al * a * (1 - 0.3 * j), 'over', 'd', ztest=False)

C_P1 = hexc(0xff8a2a); C_P2 = hexc(0x6cc4ff)
def fx_dps(u, cam, cv, k):
    gas(cv, cam, G.EXH, u, 2000, 330, size=1.7, seed=1, colf=exh_col, a=0.55)
    signal(cv, cam, G.DPS1, u, 30, 85, C_P1, seed=41, a=float(seg(u, 0.9, 1.5)), size=1.7)
    signal(cv, cam, G.DPS2, u, 52, 85, C_P2, seed=42, a=float(seg(u, 1.7, 2.3)), size=1.7)

HCP = np.array(S.META['misc']['hose_crack_pos']); HCD = np.array(S.META['misc']['hose_crack_dir'])
F_CRACK = None
def fx_leak(u, cam, cv, k):
    global F_CRACK
    if F_CRACK is None: F_CRACK = G._frac(G.DPS1, HCP - HCD * 6.0)
    lk = float(seg(u, 1.2, 1.9))
    signal(cv, cam, G.DPS1, u, 26, 85, C_P1, seed=41, cut=(F_CRACK, 1 - 0.85 * lk))
    signal(cv, cam, G.DPS2, u, 46, 85, C_P2, seed=42)
    if lk > 0:
        puffs(cv, cam, HCP, HCD, u, 46, 0.9, 70, 0.45, hexc(0xffa860), 1.6, 9.0, a=0.34 * lk, seed=43, t0=1.2, mode='over', shape='g', drag=1.6, col1=hexc(0xb8b2ac))
        puffs(cv, cam, HCP, HCD, u, 30, 0.5, 120, 0.3, C_P1, 0.7, 0.3, a=0.9 * lk, seed=44, t0=1.2, mode='add', shape='g', drag=1.0)

# ---- racitorul EGR: gaze prin tevi, antigel prin fisura
CC = L.COOL_C
TUBX = [-19.5, -6.5, 6.5, 19.5]
CRK = np.array(S.META['egr']['crack_pos'])
def _integ(fn, u, n=48):
    xs = np.linspace(0.0, max(u, 1e-6), n); ys = np.array([fn(x) for x in xs])
    return float(((ys[1:] + ys[:-1]) * 0.5 * np.diff(xs)).sum())

TUBR = L.COOL_TUBE_R - 0.7                    # raza interioara a tevilor
def clog_thick(ti, zz, side, g):
    """grosimea crustei de pe peretele lateral (side = -1 / +1) al tevii ti, la inaltimea zz: profil neregulat, creste cu g"""
    prof = 0.72 + 0.16 * np.sin(zz * 0.21 + ti * 1.7 + side * 0.9) + 0.12 * np.sin(zz * 0.57 + ti * 2.9 + side * 2.1)
    return np.minimum(3.3 * g * prof, TUBR - 0.55)

def cool_gas(u, cam, cv, flow=1.0, dist=None, g=0.0):
    """gazele care urca prin tevile racitorului; flow = cat din debit mai trece (1 = normal); g = cat de infundate sunt tevile"""
    n = 300; r = X.rnd(51, n, 10)
    ti = (r[:, 0] * 4).astype(np.int64); zs = 150.0
    d0 = u * 95.0 if dist is None else dist
    keep = (r[:, 7] < flow) * 1.0
    for j in range(3):
        zz = ((r[:, 1] * zs + (d0 - j * 1.9 * max(flow, 0.35)) * (0.85 + 0.3 * r[:, 2])) % zs) - zs / 2
        xl = -np.minimum(2.6, TUBR - clog_thick(ti, zz, -1.0, g) - 0.45); xr = np.minimum(2.6, TUBR - clog_thick(ti, zz, 1.0, g) - 0.45)
        P = np.stack([CC[0] + np.array(TUBX)[ti] + xl + (xr - xl) * r[:, 3], CC[1] - 19.5 + 0.5 + r[:, 4] * 2.4 * (0.4 + 0.6 * flow), CC[2] + zz], 1)
        col = ramp((zz + zs / 2) / zs, [0, 0.25, 0.8, 1], [C_EXH, C_EXH, C_EGR, C_EGR])
        x, y, z = cam.proj(P); rp = cam.px(0.95 * (0.8 + 0.4 * r[:, 5]), z) * (1 - 0.2 * j)
        if j == 0: cv.dots(x, y, z, rp * 2.0, col, keep * 0.2, 'add', 'g', zbias=0.0015)
        cv.dots(x, y, z, rp * 0.62, lighten(col, 0.3 if j == 0 else 0.1), keep * 0.95 * (1 - 0.34 * j), 'over', 'd', zbias=0.0015)

C_DEP0 = hexc(0x0b0a09); C_DEP1 = hexc(0x2b2019); C_DEP2 = hexc(0x15110e); C_DEP3 = hexc(0x4a3626)
def cool_clog(cam, cv, g, hole=None):
    """depuneri (funingine si reziduuri) in tevile racitorului: peretele se innegreste, apoi crusta creste dinspre pereti
    spre mijloc si lasa doar o trecere ingusta. hole = (punct, raza): zona lasata curata (ca sa se vada fisura)"""
    if g <= 0: return
    R = TUBR; yc = CC[1] - 19.5; TX = np.array(TUBX)
    def hmask(P):
        if hole is None: return 1.0
        d = np.linalg.norm(P - np.asarray(hole[0])[None, :], axis=1); return np.clip((d - hole[1]) / 4.0, 0, 1)
    # 1) pelicula neagra pe tot peretele interior (pete moi, fara contur)
    n = 5200; r = X.rnd(56, n, 8); ti = (r[:, 0] * 4).astype(np.int64); phi = (0.08 + 0.84 * r[:, 2]) * np.pi
    P = np.stack([CC[0] + TX[ti] + (R - 0.15) * np.cos(phi), yc + 0.1 + (R - 0.15) * np.sin(phi), CC[2] + r[:, 1] * 150.0 - 75.0], 1)
    al = np.clip((g * 1.7 - r[:, 3] * 0.7) / 0.35, 0, 1) * 0.55 * hmask(P)
    x, y, z = cam.proj(P)
    cv.dots(x, y, z, cam.px(1.5, z), C_DEP0, al, 'over', 'g', zbias=0.0009)
    # 2) crusta de pe pereti, vazuta in sectiune: masa compacta, cu grosime neregulata, care creste spre mijloc
    n = 15000; r = X.rnd(55, n, 10); ti = (r[:, 0] * 4).astype(np.int64); side = np.where(r[:, 2] < 0.5, -1.0, 1.0)
    zz = r[:, 1] * 150.0 - 75.0
    thick = clog_thick(ti, zz, side, g)
    q = r[:, 4] ** 0.8
    xx = side * np.minimum(R - q * thick, R - 0.34)
    yy = yc + 0.15 + r[:, 5] * np.sqrt(np.maximum(R * R - xx * xx, 0.0)) * 0.8
    P = np.stack([CC[0] + TX[ti] + xx, yy, CC[2] + zz], 1)
    edge = np.clip((q - 0.7) / 0.3, 0, 1)
    col = C_DEP2[None, :] * (1 - edge[:, None]) + C_DEP1[None, :] * edge[:, None]
    al = np.clip((thick - 0.1) / 0.35, 0, 1) * hmask(P)
    x, y, z = cam.proj(P)
    cv.dots(x, y, z, cam.px(0.3 + 0.22 * r[:, 6], z), col, al, 'over', 'd', zbias=0.002)
    # 3) cocoloase pe suprafata crustei (relief)
    n = 1500; r = X.rnd(57, n, 10); ti = (r[:, 0] * 4).astype(np.int64); side = np.where(r[:, 2] < 0.5, -1.0, 1.0)
    zz = r[:, 1] * 150.0 - 75.0
    thick = clog_thick(ti, zz, side, g)
    xx = side * (R - thick * (0.82 + 0.26 * r[:, 4]))
    P = np.stack([CC[0] + TX[ti] + xx, yc + 0.2 + r[:, 5] * 1.2, CC[2] + zz], 1)
    col = np.where((r[:, 7] < 0.3)[:, None], C_DEP3[None, :], C_DEP1[None, :])
    al = np.clip((thick - 0.5) / 0.5, 0, 1) * hmask(P)
    x, y, z = cam.proj(P)
    cv.dots(x, y, z, cam.px(0.32 + 0.4 * r[:, 6], z), col, al * 2.2, 'over', 'd', zbias=0.002, shade=0.7)

def cool_leak(u, cam, cv, t0):
    """antigelul intra prin fisura in teava, e luat de gaze si se face abur"""
    lk = float(seg(u, t0, t0 + 0.6))
    if lk <= 0: return
    m = 54; q = X.rnd(52, m, 10); life = 1.7
    age = ((u / life + q[:, 0]) % 1.0) * life; born = u - age
    z0 = CC[2] - 3 + q[:, 1] * 27
    x0 = CC[0] - 6.5 + 1.6 + (q[:, 2] - 0.5) * 1.2
    rise = np.maximum(age - 0.4, 0)
    zc = z0 + 0.5 * 170 * rise ** 2 + 20 * rise
    P = np.stack([x0 + np.sin(age * 5 + q[:, 3] * 6) * 0.9 * np.clip(rise * 3, 0, 1), np.full(m, CC[1] - 19.5 + 1.4) - rise * 1.0, zc], 1)
    f = np.clip((age - 0.75) / 0.6, 0, 1)                    # 0 = picatura de antigel, 1 = abur
    al = np.clip(age / 0.25, 0, 1) * (born >= t0) * lk
    x, y, z = cam.proj(P)
    rd = cam.px(0.55 + 0.5 * np.clip(age / 0.4, 0, 1), z)
    cv.dots(x, y, z, rd, C_COOL, al * (1 - f), 'over', 'd', zbias=0.0015, shade=0.9)
    cv.dots(x, y, z, cam.px(1.3 + 3.0 * f, z), C_STEAM, al * f * 0.3 * np.clip(1 - (age - 1.3) / 0.4, 0, 1), 'add', 'g', zbias=0.0015)

CLOG = lambda u: float(seg(u, 0.7, 4.8))
def fx_clog(u, cam, cv, k):
    g = CLOG(u)
    cool_gas(u, cam, cv, flow=1.0 - 0.8 * g, dist=95.0 * _integ(lambda x: 1.0 - 0.62 * CLOG(x), u), g=g)
    cool_clog(cam, cv, g)

def fx_coolcrack(u, cam, cv, k):
    cool_gas(u, cam, cv, flow=0.45, dist=52.0 * u + 400.0, g=0.5)
    cool_clog(cam, cv, 0.5, hole=(CRK, 7.0))
    cool_leak(u, cam, cv, 0.5)

def steam(cv, cam, path, t, n, speed, lo, hi, a=1.0, seed=61, size=5.0):
    P, al, sf, r = flow(path, t, n, speed, seed, lat=0.7)
    al = al * np.clip((sf - lo) / 0.04, 0, 1) * np.clip((hi - sf) / 0.04, 0, 1) * a
    x, y, z = cam.proj(P)
    cv.dots(x, y, z, cam.px(size * (0.7 + 0.6 * r[:, 4]), z), C_STEAM, al * 0.5, 'over', 'g')
    cv.dots(x, y, z, cam.px(1.15, z), C_COOL, al * (r[:, 5] < 0.34) * 0.95, 'over', 'd', shade=0.8)

def fx_thin(u, cam, cv, k):
    """racitorul infundat: prin EGR mai trece doar un firicel, in admisie intra aproape numai aer proaspat"""
    for i, p in enumerate(G.RUN):
        gas(cv, cam, p, u + 0.13 * i, 50, 300, C_EXH, 1.6, seed=20 + i, a=0.6)
    gas(cv, cam, G.EXH, u, 2000, 330, size=1.7, seed=1, colf=exh_col, a=0.5)
    ec = lambda sf, r: ramp(sf, [0, G.G_COOL0, G.G_COOL1, 1], [C_EXH2, C_EXH2, C_EGR, C_EGR])
    gas(cv, cam, G.EGR, u, 1300, 120, size=1.7, seed=3, colf=ec, af=lambda sf, r: (r[:, 6] < 0.16) * 1.0)
    gas(cv, cam, G.AIR, u, 520, 330, C_AIR, 1.8, seed=4)
    cc = lambda sf, r: np.where((r[:, 5] < 0.05)[:, None], C_EGR[None, :], C_AIR[None, :])
    gas(cv, cam, G.CHG, u, 1000, 360, size=1.8, seed=5, colf=cc, swirl=0.02)

def fx_steam(u, cam, cv, k):
    for i, p in enumerate(G.RUN):
        gas(cv, cam, p, u + 0.13 * i, 50, 300, C_EXH, 1.6, seed=20 + i, a=0.5)
    gas(cv, cam, G.EXH, u, 2000, 330, size=1.7, seed=1, colf=exh_col, a=0.45)
    ec = lambda sf, r: ramp(sf, [0, G.G_COOL0, G.G_COOL1, 1], [C_EXH2, C_EXH2, C_EGR, C_EGR])
    gas(cv, cam, G.EGR, u, 900, 300, size=1.7, seed=3, colf=ec, a=0.55)
    gas(cv, cam, G.AIR, u, 420, 330, C_AIR, 1.8, seed=4, a=0.7)
    cc = lambda sf, r: np.where((r[:, 5] < 0.34)[:, None], C_EGR[None, :], C_AIR[None, :])
    gas(cv, cam, G.CHG, u, 800, 360, size=1.8, seed=5, colf=cc, swirl=0.02, a=0.6)
    steam(cv, cam, G.EGR, u, 520, 300, (G.G_COOL0 + G.G_COOL1) / 2, 1.0, seed=61)
    steam(cv, cam, G.CHG, u, 420, 360, 0.0, 1.0, seed=62, a=float(seg(u, 0.2, 1.2)))

def fx_glaze(u, cam, cv, k):
    dpf_gas(cv, cam, u, soot_k=0.5, n=520)
    dpf_soot(cv, cam, u, n=160)
    # aburul si reziduurile de antigel ajung pe fata de intrare
    n = 110; r = X.rnd(71, n, 10)
    life = 1.5; age = ((u / life + r[:, 0]) % 1.0) * life
    a_pos = 6 + r[:, 1] * 58; face = (r[:, 2] < 0.5).astype(np.int64)
    z = Z0 - 30 + np.minimum(age * 26, 29.5)
    P = _dpf_pos(face, a_pos, -0.4 - r[:, 3] * 1.6, z)
    al = np.clip(age / 0.2, 0, 1) * np.clip((life - age) / 0.5, 0, 1)
    x, y, zz = cam.proj(P)
    cv.dots(x, y, zz, cam.px(2.6 + 2.0 * r[:, 4], zz), C_STEAM, al * 0.3, 'over', 'g', zbias=0.0015)
    cv.dots(x, y, zz, cam.px(0.6, zz), hexc(0xcfe6d4), al * 0.9 * (r[:, 5] < 0.6), 'over', 'd', zbias=0.0015)

# ---- supapa EGR
VC = np.array(S.META['egr']['VC']); _vz = L.nrm([17.0, 20.0, 52.0]); _vt = np.array([0.55, -0.82, 0.1])
_vy = L.nrm(_vt - _vz * (_vt @ _vz)); _vx = np.cross(_vy, _vz)
def valve_dep(cam, cv, a, ang=8.0):
    """depuneri care tin clapeta intepenita: crusta pe marginea discului si pe peretele tevii, in dreptul lui"""
    if a <= 0: return
    ca, sa = np.cos(np.radians(ang)), np.sin(np.radians(ang))
    def world(lx, ly, lz): return VC[None, :] + lx[:, None] * _vx[None, :] + ly[:, None] * _vy[None, :] + lz[:, None] * _vz[None, :]
    # pelicula inchisa pe peretele tevii, de o parte si de alta a clapetei
    n = 700; r = X.rnd(72, n, 6); phi = r[:, 0] * 2 * np.pi
    lz = (r[:, 1] - 0.5) * 30.0
    P = world(15.6 * np.cos(phi), 15.6 * np.sin(phi), lz)
    x, y, z = cam.proj(P)
    cv.dots(x, y, z, cam.px(2.4, z), C_DEP0, a * 0.42 * np.clip(1 - np.abs(lz) / 16.0, 0, 1), 'over', 'g', zbias=0.0025)
    # crusta de pe marginea discului (unde calca pe teava)
    n = 3200; r = X.rnd(71, n, 8); phi = r[:, 0] * 2 * np.pi
    rho = 15.4 - 3.4 * r[:, 2] ** 1.6
    off = (r[:, 3] - 0.5) * (2.2 + 5.0 * np.clip((rho - 12.0) / 3.4, 0, 1) ** 2)
    ly0 = rho * np.sin(phi)
    P = world(rho * np.cos(phi), ly0 * ca, ly0 * sa + off)
    col = np.where((r[:, 5] < 0.25)[:, None], C_DEP1[None, :], C_DEP2[None, :])
    x, y, z = cam.proj(P)
    cv.dots(x, y, z, cam.px(0.35 + 0.4 * r[:, 6], z), col, a, 'over', 'd', zbias=0.004)
    n = 260; r = X.rnd(73, n, 8); phi = r[:, 0] * 2 * np.pi; rho = 14.6 - 2.0 * r[:, 2]
    ly0 = rho * np.sin(phi)
    P = world(rho * np.cos(phi), ly0 * ca, ly0 * sa + (r[:, 3] - 0.5) * 5.0)
    x, y, z = cam.proj(P)
    cv.dots(x, y, z, cam.px(0.4 + 0.35 * r[:, 6], z), np.where((r[:, 5] < 0.15)[:, None], C_DEP3[None, :], C_DEP1[None, :]), a * 1.6, 'over', 'd', zbias=0.004, shade=0.5)

def fx_valve(u, cam, cv, k):
    op = 1.0 - float(seg(u, 2.9, 3.4))                   # supapa ramane intepenita aproape inchisa
    thr = 0.12 + 0.88 * op
    ec = lambda sf, r: ramp(sf, [0, G.G_COOL0, G.G_COOL1, 1], [C_EXH2, C_EXH2, C_EGR, C_EGR])
    af = lambda sf, r: np.where(sf > G.G_VALVE, (r[:, 6] < thr) * 1.0, 1.0)
    gas(cv, cam, G.EGR, u, 1500, 260, size=1.5, seed=3, colf=ec, af=af)
    gas(cv, cam, G.AIR, u, 520, 330, C_AIR, 1.5, seed=4, af=lambda sf, r: (r[:, 6] > 0.42 * op) * 1.0)
    sh = 0.06 + 0.5 * op
    cc = lambda sf, r: np.where((r[:, 5] < sh)[:, None], C_EGR[None, :], C_AIR[None, :])
    gas(cv, cam, G.CHG, u, 900, 360, size=1.5, seed=5, colf=cc, swirl=0.02)
    valve_dep(cam, cv, float(seg(u, 3.0, 3.6)))

# ---- cilindrul 1 in sectiune: injectie, ardere, evacuare, admisie
SX = L.SEC_X
EXP = X.Path([(SX - 7, -8, 229), (SX - 6, -25, 240), (SX - 6, -25.5, 252), (SX - 6, -35, 277), (SX - 6, -62, 296), (SX - 6, -94, 301), (SX - 6, -128, 302)], 7.5, smooth=6, step=1.5)
INP = X.Path([(SX - 6, 128, 302), (SX - 6, 94, 301), (SX - 6, 62, 296), (SX - 6, 35, 277), (SX - 6, 25.5, 252), (SX - 6, 25, 240), (SX - 7, 8, 229)], 7.5, smooth=6, step=1.5)
def th_of(u, rate=30.0, off=45, n=60):
    return ((u * rate + off) % n) * (720.0 / n)
def inwin(th, a, b, soft=6.0):
    best = 0.0
    for sh in (-720.0, 0.0, 720.0):
        x = th + sh
        best = max(best, min(min(max((x - a) / soft, 0.0), 1.0), min(max((b - x) / soft, 0.0), 1.0)))
    return best
TIP = np.array([SX - 1.2, 0.0, L.DECK - 3.4])

def chamber_pts(r, crown, n):
    """puncte in camera de ardere (jumatatea din spatele planului de sectiune)"""
    rad = 3 + r[:, 1] * 33; an = r[:, 2] * np.pi
    zlo = crown - np.where(rad < 27, 11.0, 0.5); zhi = np.full(n, L.DECK - 0.8)
    zhi = np.maximum(zhi, zlo + 1.0)
    return np.stack([SX - 1.5 - rad * np.sin(an) * 0.85, rad * np.cos(an), zlo + r[:, 3] * (zhi - zlo)], 1)

def fx_inj(u, cam, cv, k, mode='inj'):
    th = th_of(u); pz = L.piston_z(math.radians(th)); crown = pz + 45.0
    bad = float(seg(u, 4.3, 4.8)) if mode == 'inj' else 0.0
    w_inj = inwin(th, -12, 14 + 22 * bad)
    if w_inj > 0 and mode == 'inj':
        n = 150; r = X.rnd(81, n, 10)
        jet = (r[:, 0] * 5).astype(np.int64); a = np.radians(jet * 45.0); el = math.radians(14)
        d = np.stack([-np.sin(a) * math.cos(el), np.cos(a) * math.cos(el), np.full(n, -math.sin(el))], 1)
        reach = 27.0
        for j in range(2):
            dist = ((r[:, 1] + (u - j * 0.012) * 6.5) % 1.0) * reach
            P = TIP[None, :] + d * dist[:, None] + (r[:, 2:5] - 0.5) * 2 * (0.11 * dist)[:, None]
            col = ramp(dist / reach, [0, 0.55, 1], [C_FUEL, hexc(0xfff2b0), hexc(0xffa030)])
            x, y, z = cam.proj(P); rp = cam.px(0.55 + 0.5 * dist / reach, z)
            al = w_inj * np.clip(1.15 - dist / reach, 0, 1) * (1 - 0.4 * j)
            if j == 0: cv.dots(x, y, z, rp * 2.2, col, al * 0.3, 'add', 'g', zbias=0.002)
            cv.dots(x, y, z, rp * 0.7, lighten(col, 0.3), al, 'over', 'd', zbias=0.002)
    w_f = inwin(th, -3, 62 + 26 * bad, soft=12)
    if w_f > 0:
        n = 80; r = X.rnd(82, n, 10); life = 0.22
        age = ((u / life + r[:, 0]) % 1.0); P = chamber_pts(r, crown, n); P[:, 2] += age * 3
        hot = np.clip(1 - max(th if th < 360 else th - 720, 0) / (70.0 + 30 * bad), 0, 1)
        col = ramp(age, [0, 0.4, 1], [hexc(0xfff3c4), C_FIRE, hexc(0xc43a10)])
        x, y, z = cam.proj(P); rp = cam.px(3.0 + 5.5 * age, z)
        cv.dots(x, y, z, rp, col, w_f * (1 - age) * (0.35 + 0.4 * hot), 'add', 'g', zbias=0.002)
        cv.dots(x, y, z, rp * 0.45, lighten(col, 0.2), w_f * (1 - age) * 0.5 * hot, 'over', 'g', zbias=0.002)
    # funingine in camera (mai multa cand injectorul picura)
    w_s = inwin(th, 24, 350, soft=20) * (0.25 + 0.75 * bad)
    if w_s > 0:
        n = 110; r = X.rnd(83, n, 10); P = chamber_pts(r, crown, n)
        P[:, 1] += np.sin(u * 3 + r[:, 4] * 6) * 1.5; P[:, 2] += np.cos(u * 2.3 + r[:, 5] * 6) * 1.0
        x, y, z = cam.proj(P)
        cv.dots(x, y, z, cam.px(0.5 + 0.5 * r[:, 6], z), C_SOOT, w_s * (r[:, 7] < (0.3 + 0.7 * bad)) * 0.9, 'over', 'd', zbias=0.002)
        cv.dots(x, y, z, cam.px(4.5, z), hexc(0x2a2624), w_s * 0.16 * bad, 'over', 'g', zbias=0.002)
    # picaturi care cad din duza dupa injectie (injector care picura)
    if bad > 0:
        w_d = inwin(th, 20, 170, soft=8) * bad
        if w_d > 0:
            n = 5; r = X.rnd(84, n, 10); life = 0.42
            age = ((u / life + r[:, 0]) % 1.0) * life
            fall = np.minimum(0.5 * 700 * np.maximum(age - 0.12, 0) ** 2, max(TIP[2] - (crown - 6.4), 0.0))
            P = np.stack([TIP[0] - 0.8 - r[:, 1] * 1.5, (r[:, 2] - 0.5) * 2.0, TIP[2] - 0.6 - fall], 1)
            x, y, z = cam.proj(P)
            cv.dots(x, y, z, cam.px(0.6 + 0.6 * np.clip(age / 0.12, 0, 1), z), C_FUEL, w_d, 'over', 'd', zbias=0.002, shade=0.9)
    # evacuare: gazele ies pe langa supapa de evacuare
    w_e = inwin(th, 150, 364, soft=14)
    if w_e > 0:
        sootsh = 0.1 + 0.55 * bad
        colf = lambda sf, r: np.where((r[:, 5] < sootsh)[:, None], C_SOOT[None, :], C_EXH[None, :])
        gas(cv, cam, EXP, u, 150, 230, size=1.25, seed=85, a=w_e, colf=colf, glow=0.16, zbias=0.002, lat=0.85)
    # admisie: aer (si gaze recirculate) pe langa supapa de admisie
    w_i = inwin(th, 366, 560, soft=14)
    if w_i > 0:
        colf = lambda sf, r: np.where((r[:, 5] < 0.25)[:, None], C_EGR[None, :], C_AIR[None, :])
        gas(cv, cam, INP, u, 150, 230, size=1.25, seed=86, a=w_i, colf=colf, glow=0.16, zbias=0.002, lat=0.85)
        n = 60; r = X.rnd(87, n, 10); P = chamber_pts(r, crown, n)
        x, y, z = cam.proj(P)
        cv.dots(x, y, z, cam.px(0.8, z), C_AIR, w_i * 0.55 * inwin(th, 400, 560, 30), 'over', 'd', zbias=0.002)
    return th, crown

C_SMOKE = hexc(0xa9bde6)
def fx_oil(u, cam, cv, k):
    th, crown = fx_inj(u, cam, cv, k, mode='oil')
    pz = crown - 45.0
    on = float(seg(u, 0.2, 0.9))
    # 1) ulei care urca pe langa segmenti, pe ambele parti ale pistonului (merge odata cu pistonul)
    n = 170; r = X.rnd(91, n, 10)
    side = np.where(r[:, 0] < 0.5, -1.0, 1.0); h = (r[:, 1] + u * 0.22) % 1.0
    P = np.stack([SX - 0.3 - r[:, 2] * 1.5, side * (40.2 + 1.2 * r[:, 3]), pz + 12.0 + h * 35.0], 1)
    al = np.clip(h / 0.1, 0, 1) * np.clip((1 - h) / 0.08, 0, 1) * on
    x, y, z = cam.proj(P); rp = cam.px(0.8 + 0.8 * r[:, 4], z)
    cv.dots(x, y, z, rp * 2.6, C_OIL, al * 0.05, 'add', 'g', zbias=0.003)
    cv.dots(x, y, z, rp, C_OIL, al, 'over', 'd', zbias=0.003, shade=0.9)
    # 2) pelicula de ulei ramasa pe peretele cilindrului, deasupra pistonului
    m = 300; q = X.rnd(96, m, 10)
    side = np.where(q[:, 0] < 0.5, -1.0, 1.0); zz = (L.DECK - 97.0) + q[:, 1] * 96.0
    above = zz - crown
    al = np.clip((above - 0.3) / 1.5, 0, 1) * (0.25 + 0.75 * np.exp(-np.maximum(above, 0) / 26.0)) * on
    P = np.stack([SX - 0.3 - q[:, 3] * 1.2, side * (40.45 + 0.45 * q[:, 4]), zz], 1)
    x, y, z = cam.proj(P)
    cv.dots(x, y, z, cam.px(0.5 + 0.5 * q[:, 5], z), C_OIL, al * 0.95, 'over', 'd', zbias=0.003, shade=0.7)
    # 3) uleiul ajuns deasupra pistonului arde: fum albastrui in cilindru, care iese apoi pe evacuare
    on2 = float(seg(u, 0.6, 1.4))
    w = inwin(th, 8, 366, soft=16) * on2
    if w > 0:
        m = 100; q = X.rnd(92, m, 10); P = chamber_pts(q, crown, m)
        P[:, 1] = np.sign(P[:, 1]) * (12 + q[:, 4] * 27)
        P[:, 2] += np.sin(u * 2.1 + q[:, 7] * 6.28) * 1.5
        x, y, z = cam.proj(P)
        cv.dots(x, y, z, cam.px(4.5 + 3.5 * q[:, 5], z), C_SMOKE, w * 0.42, 'over', 'g', zbias=0.002)
        cv.dots(x, y, z, cam.px(0.55, z), C_ASH, w * 0.8 * (q[:, 6] < 0.5), 'over', 'd', zbias=0.002)
    w_e = inwin(th, 150, 364, soft=14) * on2
    if w_e > 0:
        P, al, sf, rr = flow(EXP, u, 120, 230, 93, lat=0.85)
        x, y, z = cam.proj(P)
        cv.dots(x, y, z, cam.px(4.0 + 2.5 * rr[:, 5], z), C_SMOKE, al * w_e * 0.5, 'over', 'g', zbias=0.002)
        cv.dots(x, y, z, cam.px(0.6, z), C_ASH, al * w_e * 0.9 * (rr[:, 6] < 0.6), 'over', 'd', zbias=0.002)

# ---- turbina care pierde ulei pe la etansarea axului
def fx_turbo(u, cam, cv, k):
    gas(cv, cam, G.EXH, u, 2000, 330, size=1.6, seed=1, colf=exh_col, a=0.75, af=lambda sf, r: (sf < 0.5) * 1.0)
    for i, p in enumerate(G.RUN):
        gas(cv, cam, p, u + 0.13 * i, 50, 300, C_EXH, 1.5, seed=20 + i, a=0.7)
    gas(cv, cam, G.AIR, u, 420, 330, C_AIR, 1.6, seed=4, a=0.8)
    gas(cv, cam, G.CHG, u, 1000, 360, C_AIR, 1.6, seed=5, a=0.8, swirl=0.02)
    n = 80; r = X.rnd(95, n, 10)
    h = (r[:, 0] + u * 0.42) % 1.0
    TY, TZ = L.TURBO_Y, L.TURBO_Z
    ang = r[:, 1] * 2 * np.pi + u * 5.2
    k1 = np.clip(h / 0.3, 0, 1); k2 = np.clip((h - 0.3) / 0.22, 0, 1); k3 = np.clip((h - 0.52) / 0.48, 0, 1)
    xs = 46 - 20 * k1 - 8 * k2; rad = 5.6 + 20 * ease(k2)
    P1 = np.stack([xs, TY + rad * np.cos(ang), TZ + rad * np.sin(ang)], 1)
    f0 = G.F_TURB - 0.03
    C, T, N, B, R = G.EXH.at((f0 + k3 * (0.5 - f0)) * G.EXH.len)
    P3 = C + (R * 0.6 * np.sqrt(r[:, 2]))[:, None] * (np.cos(r[:, 3] * 6.28)[:, None] * N + np.sin(r[:, 3] * 6.28)[:, None] * B)
    P = np.where((k3 > 0)[:, None], P3, P1)
    al = np.clip(h / 0.06, 0, 1) * np.clip((1 - h) / 0.1, 0, 1) * float(seg(u, 0.15, 0.7))
    x, y, z = cam.proj(P)
    burn = np.clip(k3 * 2.2, 0, 1)
    cv.dots(x, y, z, cam.px(1.25 + 0.5 * r[:, 4], z), C_OIL, al * (1 - burn), 'over', 'd', shade=0.9)
    cv.dots(x, y, z, cam.px(3.0 + 5.0 * k3, z), hexc(0x9aa6bd), al * burn * 0.3, 'over', 'g')
    cv.dots(x, y, z, cam.px(0.8, z), C_ASH, al * burn * 0.9, 'over', 'd')

def fx_ash(u, cam, cv, k):
    kk = float(seg(u, 0.4, 2.8))
    dpf_gas(cv, cam, u, soot_k=0.5, n=520)
    r, face, ch, side, zc = _dpf_tab(260, 14)
    zin = Z0 - 26.0; zb = Z1 - L.DPF_PLUG - 62.0 * kk - 1.0 + r[:, 3] * 3.0
    hold = 50.0; D = (zb - zin) + hold
    d = (r[:, 4] * D + u * 66 * (0.85 + 0.3 * r[:, 5])) % D
    z = zin + np.minimum(d, zb - zin)
    P = _dpf_pos(face, ch * P6 + (r[:, 6] - 0.5) * 2.2, -0.35 - r[:, 8] * 1.2, z)
    al = np.clip(d / 8.0, 0, 1) * (1 - np.clip((d - (zb - zin) - 4.0) / (hold - 4.0), 0, 1))
    x, y, zz = cam.proj(P)
    cv.dots(x, y, zz, cam.px(0.7 * (0.7 + 0.6 * r[:, 9]), zz), C_ASH, al * 0.95, 'over', 'd', zbias=0.0012)

LEAKD = L.nrm([0.62, 0.42, 0.62]); LEAKP = np.array([99.8, -148.8, 354.0]) + 22.5 * L.nrm([0.76, 0.65, 0.0])
F_LEAK = None
def fx_maf(u, cam, cv, k):
    """aerul trece prin debitmetru si e numarat; dupa compresor, o parte se pierde printr-o fisura a tevii de admisie"""
    global F_LEAK
    if F_LEAK is None: F_LEAK = G._frac(G.CHG, (99.8, -148.8, 354.0))
    lk = float(seg(u, 1.6, 2.3))
    gas(cv, cam, G.AIR, u, 620, 300, C_AIR, 1.7, seed=4, t0=0.2)
    gas(cv, cam, G.CHG, u, 900, 360, C_AIR, 1.6, seed=5, swirl=0.02, t0=0.6,
        af=lambda sf, r: np.where(sf > F_LEAK, (r[:, 6] > 0.5 * lk) * 1.0, 1.0))
    if lk > 0:
        puffs(cv, cam, LEAKP, LEAKD, u, 90, 1.0, 110, 0.4, C_AIR, 2.5, 12.0, a=0.26 * lk, seed=73, t0=1.6, mode='add', shape='g', drag=0.7, ztest=False)
        puffs(cv, cam, LEAKP, LEAKD, u, 140, 0.6, 200, 0.16, hexc(0xcdeaff), 1.5, 0.9, a=1.0 * lk, seed=74, t0=1.6, mode='add', shape='g', drag=0.3, ztest=False)

def fx_regen(u, cam, cv, k):
    kk = float(seg(u, 0.3, 1.2))
    dpf_gas(cv, cam, u, soot_k=0.85, n=520, clean=hexc(0xffc070))
    # scantei din funinginea care arde
    r, face, ch, side, zc = _dpf_tab(170, 15)
    life = 0.8; age = ((u / life + r[:, 4]) % 1.0)
    P = _dpf_pos(face, ch * P6 + side * 2.0 * (1 - age * 0.6), -0.3 - r[:, 8] * 1.0, zc - age * 9)
    x, y, zz = cam.proj(P)
    cv.dots(x, y, zz, cam.px(1.1 * (1 - age * 0.5), zz), hexc(0xffc45a), kk * (1 - age) * 0.8, 'add', 'g', zbias=0.0012)
    # ceramica crapa de la caldura: fisura de-a curmezisul canalelor (inelara), aceeasi pe ambele fete taiate
    kc = float(seg(u, 2.2, 2.75))
    if kc > 0:
        m = 1500; q = X.rnd(16, m, 6)
        for fc in (0, 1):
            a = 0.3 + q[:, 0] * 64.7
            s_ = a if fc == 0 else -a                          # coordonata continua peste muchia dintre fete
            zj = Z0 + 61.0 + 1.5 * np.sin(s_ * 0.19 + 0.6) + 0.8 * np.sin(s_ * 0.83 + 1.0) + 0.45 * np.sign(np.sin(s_ * 2.9)) + (q[:, 1] - 0.5) * 0.5
            P = _dpf_pos(np.full(m, fc), a, np.full(m, -0.05), zj)
            x, y, zz = cam.proj(P)
            p = 0.5 + 0.5 * q[:, 0] * (1 if fc == 0 else -1)   # fisura inainteaza de la un capat la celalalt
            grow = np.clip((kc * 1.15 - p) / 0.08, 0, 1)
            cv.dots(x, y, zz, cam.px(0.3 + 0.22 * q[:, 3], zz), hexc(0x050505), grow, 'over', 'd', ztest=False)
            cv.dots(x, y, zz, cam.px(1.25, zz), hexc(0xff6a1c), grow * 0.07 * (1 - 0.7 * float(seg(u, 3.0, 4.0))), 'add', 'g', ztest=False)
        # prin fisura, funinginea trece direct in canalele de iesire si pleaca nefiltrata
        ks = float(seg(u, 2.7, 3.3))
        r, face, ch, side, zc = _dpf_tab(300, 17)
        zcr = Z0 + 61.0; Dz = (Z1 + 14.0) - zcr
        d = ((r[:, 4] + u * 0.85 * (0.8 + 0.4 * r[:, 5])) % 1.0) * Dz
        P = _dpf_pos(face, (ch + side) * P6 + (r[:, 6] - 0.5) * 2.6, -0.35 - r[:, 8] * 1.4, zcr + d)
        x, y, zz = cam.proj(P)
        cv.dots(x, y, zz, cam.px(0.8 * (0.7 + 0.6 * r[:, 9]), zz), C_SOOT, ks * np.clip(d / 6.0, 0, 1) * 0.95, 'over', 'd', zbias=0.0012)

DIM = lambda a, b, lvl=0.8: (lambda u: lvl * float(seg(u, a, b)))

#       hook rutaA rutaB filtru senzor logica furtun racit firicel fisura supapa aer inject regen ulei turbo cenusa final
DUR = [5.0,  5.5,  5.5,  6.5,   6.5,   12.5,  5.5,   6.5,  3.5,     3.5,   7.0,   5.0, 6.0,   5.0,  4.0, 3.0,  3.5,   8.5]
T = [0.0]
for d in DUR: T.append(round(T[-1] + d, 3))
SHOTS = [
    Shot('s00', T[0], T[1], 'heroB', [('solid', None)], kind='orbit', xf=False),
    Shot('s01', T[1], T[2], 'route', [('solid', None), ('ghostNR', (0.25, 1.15))], loop=('rotor', 12, 30, 0), fx=fx_route, zoom=(1.0, 1.05), pan=((0, 0), (10, -14))),
    Shot('s02', T[2], T[3], 'routeC', [('ghostNR', None)], loop=('rotor', 12, 30, 0), fx=fx_egr, zoom=(1.0, 1.045)),
    Shot('s03', T[3], T[4], 'dpf', [('soot0', None), ('soot1', (1.2, 5.6))], fx=fx_dpf, zoom=(1.0, 1.06), pan=((0, 0), (0, -20))),
    Shot('s04', T[4], T[5], 'dps', [('gexh', None)], fx=fx_dps, zoom=(1.0, 1.05), pan=((0, 0), (16, 0))),
    Shot('s05', T[5], T[6], 'heroB', [('solid', None)], dim=DIM(0.0, 0.7, 0.86), zoom=(1.04, 1.0)),
    # --- calculatorul e pacalit (filtrul e bun)
    Shot('s06', T[6], T[7], 'dpsC', [('solid', None), ('crack', (0.9, 1.5))], fx=fx_leak, zoom=(1.0, 1.06)),
    Shot('s07', T[7], T[8], 'cool', [('solid', None)], fx=fx_clog, zoom=(1.0, 1.07), pan=((0, 0), (0, -16))),
    Shot('s08', T[8], T[9], 'routeC', [('ghostNR', None)], loop=('rotor', 12, 30, 0), fx=fx_thin, zoom=(1.045, 1.075)),
    Shot('s09', T[9], T[10], 'cool', [('solid', None), ('ecrack', (0.3, 0.8))], fx=fx_coolcrack, zoom=(1.07, 1.11), pan=((0, -16), (0, -24))),
    Shot('s10', T[10], T[11], 'egrvB', [('vopen', None), ('vclosed', (2.9, 3.4))], fx=fx_valve, zoom=(1.0, 1.05)),
    Shot('s16', T[11], T[12], 'mafG', [('gint', None)], fx=fx_maf, zoom=(1.0, 1.05)),
    # --- filtrul e victima (cauza e in motor)
    Shot('s11', T[12], T[13], 'inj', [('noeng', None)], loop=('engine', 60, 30, 45), fx=fx_inj, zoom=(1.0, 1.05), pan=((0, -110), (0, -110)), grade=(0.80, 1.22)),
    Shot('s12', T[13], T[14], 'dpf', [('soot1', None), ('regen2', (0.3, 1.2))], fx=fx_regen, zoom=(1.03, 1.08)),
    Shot('s13', T[14], T[15], 'sec', [('noeng', None)], loop=('engine', 60, 30, 45), fx=fx_oil, zoom=(1.0, 1.05), grade=(0.80, 1.22)),
    Shot('s14', T[15], T[16], 'turboG', [('gturbo', None)], loop=('rotor', 12, 30, 0), fx=fx_turbo, zoom=(1.0, 1.04)),
    Shot('s15', T[16], T[17], 'dpf', [('sootM', None), ('ash', (0.4, 2.8))], fx=fx_ash, zoom=(1.1, 1.16), pan=((0, -150), (0, -170))),
    Shot('s17', T[17], T[18], 'heroB', [('solid', None)], dim=DIM(0.0, 0.8, 0.84), zoom=(1.0, 1.04)),
]
TOTAL = SHOTS[-1].t1

# ============================================================== texte pe ecran (HUD)
def cam_J(name):
    """matricea camerei calculata direct din definitie (la fel ca in Blender: priveste de-a lungul -Z, Y in sus)"""
    c = S.CAMS[name]; p = np.asarray(c['pos'], np.float64) * 0.001; t = np.asarray(c['tgt'], np.float64) * 0.001
    f = (t - p) / np.linalg.norm(t - p); r = np.cross(f, [0, 0, 1.0]); r /= np.linalg.norm(r); up = np.cross(r, f)
    M = np.eye(4); M[:3, 0] = r; M[:3, 1] = up; M[:3, 2] = -f; M[:3, 3] = p
    return {'M': M.tolist(), 'lens': c['lens'], 'sensor': 24.0}

def dp(face, a, b, z):
    return _dpf_pos(np.array([face]), np.array([float(a)]), np.array([float(b)]), np.array([float(z)]))[0]

ORANGE = '#ff9238'; RED = '#ff5a4d'; BLUE = '#58b6ff'; PINK = '#ff6fb5'; GREEN = '#3fd68a'; AMBER = '#f0b23e'; GREY = '#c9d0d8'
MISC = S.META['misc']
# etichete: (text, punct 3D mm, pozitia textului pe ecran x, y, aliniere, t_on, t_off, culoare)
END = 99.0        # „pana la sfarsitul planului”
OKF = 'FILTRUL E BUN'; VIC = 'FILTRUL E VICTIMA'
HUD = {
 's00': dict(title=('Eroare de eficiență pe DPF?', 'Nu întotdeauna e vina filtrului.'), tag='PROBLEMA', chip='EROARE DE EFICIENȚĂ DPF',
             caps=[(0.5, END, 'La motoarele 2.0 TDI EA288, eroarea vine des din altă parte.')], step=0),
 's01': dict(title=('Traseul gazelor', 'de la motor până la filtru'), tag='TRASEUL GAZELOR', chip='EVACUARE',
             caps=[(0.3, END, 'Gazele arse trec prin turbină, catalizator și filtrul de particule.')], step=1,
             labels=[('Turbină', (4, -258, 290), 700, 500, 'l', 1.4, END, ORANGE),
                     ('Catalizator de oxidare', tuple(L.mw(34, 34, 47)), 120, 760, 'l', 2.2, END, ORANGE),
                     ('Filtru de particule (DPF)', tuple(L.mw(36, 36, 215)), 80, 1330, 'l', 3.0, END, ORANGE)]),
 's02': dict(title=('Traseul gazelor', 'EGR de joasă presiune'), tag='TRASEUL GAZELOR', chip='EGR DE JOASĂ PRESIUNE',
             caps=[(0.3, END, 'După filtru, o parte din gaze se întoarce în motor.')], step=1,
             labels=[('Răcitor EGR', (-52, -296, 30), 60, 1344, 'l', 0.9, END, AMBER),
                     ('Supapă EGR', (176, -262, 206), 690, 1180, 'l', 2.2, END, AMBER),
                     ('Aer proaspăt', (144, -212, 266), 800, 338, 'l', 0.6, END, BLUE),
                     ('Compresor', (104, -262, 262), 540, 560, 'l', 3.0, END, BLUE)]),
 's03': dict(title=('Ce se întâmplă în filtru', 'gazele trec, funinginea rămâne'), tag='ÎN FILTRU', chip='FILTRU ÎN SECȚIUNE',
             caps=[(0.3, END, 'În filtru, gazele trec prin pereții poroși. Funinginea rămâne în canale.')], step=2,
             labels=[('Canal de intrare', tuple(dp(0, 12, -1, Z0 + 40)), 330, 596, 'l', 0.8, END, ORANGE),
                     ('Dop', tuple(dp(0, 18, -1, Z0 + 5)), 770, 396, 'l', 1.6, END, GREY),
                     ('Perete poros', tuple(dp(0, 39, 0, Z0 + 95)), 700, 1250, 'l', 2.6, END, GREY),
                     ('Funingine', tuple(dp(1, 10.2, -1, Z0 + 110)), 60, 1300, 'l', 3.6, END, GREY)]),
 's04': dict(title=('Cum judecă calculatorul', 'filtrul de particule'), tag='CE MĂSOARĂ', chip='SENZOR DE PRESIUNE DIFERENȚIALĂ',
             caps=[(0.3, END, 'Calculatorul nu vede în filtru. Măsoară presiunea înainte și după el.')], step=3,
             labels=[('Senzor de presiune', (-266, -212, 318), 50, 376, 'l', 0.6, END, GREY),
                     ('Înainte de filtru', tuple(MISC['dps_b1']), 50, 880, 'l', 1.5, END, ORANGE, [(0, 'PRESIUNE MAI MARE', ORANGE)]),
                     ('După filtru', tuple(MISC['dps_b2']), 50, 1262, 'l', 2.6, END, BLUE, [(0, 'PRESIUNE MAI MICĂ', BLUE)])]),
 's05': dict(title=('Cum judecă calculatorul', 'filtrul de particule'), tag='CE CALCULEAZĂ', chip='DOUĂ VALORI COMPARATE',
             caps=[(0.3, 5.0, 'Separat, calculează câtă funingine ar trebui să fie în filtru.'),
                   (5.2, 9.3, 'Dacă măsoară mult mai puțin decât a calculat, crede că filtrul nu mai reține.'),
                   (9.5, END, 'Așa apare eroarea, chiar și cu un filtru bun.')], step=3, info=True),
 # ---------------- calculatorul e pacalit, filtrul e bun
 's06': dict(title=('Cauza 1', 'Senzorul și furtunașele'), tag='CAUZA 1', chip=OKF, chipc=GREEN, bad=True,
             caps=[(0.3, END, 'Furtunaș crăpat sau înfundat: senzorul citește o presiune prea mică.')], step=4,
             ecu=dict(calc=(0.5, 0.5), meas=(0.5, 0.2), t=(1.4, 2.4)),
             labels=[('Furtunaș fisurat', tuple(HCP), 560, 1130, 'l', 1.6, END, RED)]),
 's07': dict(title=('Cauza 2', 'Răcitorul EGR'), tag='CAUZA 2', chip=OKF, chipc=GREEN, bad=True,
             caps=[(0.3, 3.3, 'Răcitorul EGR se înfundă cu funingine și depuneri.'),
                   (3.5, END, 'Trec mai puține gaze decât a socotit calculatorul.')], step=5,
             ecu=dict(calc=(0.5, 0.5), meas=(0.5, 0.42), t=(3.6, 6.2)),
             labels=[('Depuneri', (CC[0] + TUBX[0] + 2.2, CC[1] - 19.5 + 1.2, CC[2] + 4), 150, 800, 'l', 1.9, END, RED),
                     ('Antigel', (CC[0] + 13.0, CC[1] - 19.5, CC[2] - 24), 720, 1240, 'l', 0.7, END, PINK),
                     ('Gaze spre admisie', (CC[0] + 19.5, CC[1] - 18.5, CC[2] + 30), 660, 560, 'l', 1.2, END, AMBER)]),
 's08': dict(title=('Cauza 2', 'Răcitorul EGR'), tag='CAUZA 2', chip=OKF, chipc=GREEN, bad=True,
             caps=[(0.2, END, 'Pe filtru, presiunea iese mai mică decât cea așteptată.')], step=5,
             ecu=dict(calc=(0.5, 0.5), meas=(0.42, 0.26), t=(0.3, 2.0)),
             labels=[('Debit EGR mic', (95, -280, 151), 600, 960, 'l', 0.4, END, AMBER)]),
 's09': dict(title=('Cauza 2', 'Răcitorul EGR'), tag='CAUZA 2', chip=OKF, chipc=GREEN, bad=True,
             caps=[(0.2, END, 'Uneori e și fisurat: pierde antigel, fără pată sub mașină.')], step=5,
             ecu=dict(calc=(0.5, 0.5), meas=(0.26, 0.26), t=(0.0, 1.0)),
             labels=[('Fisură', tuple(CRK), 150, 800, 'l', 0.9, END, RED)]),
 's10': dict(title=('Cauza 3', 'Supapa EGR'), tag='CAUZA 3', chip=OKF, chipc=GREEN, bad=True,
             caps=[(0.3, END, 'Supapa EGR înțepenită nu se deschide cât i se cere. Efectul e același.')], step=6,
             ecu=dict(calc=(0.5, 0.5), meas=(0.5, 0.28), t=(3.4, 6.0)),
             labels=[('Supapă EGR', (176 + 14, -240 - 22, 206 + 6), 560, 1296, 'l', 0.6, END, AMBER,
                      [(0, 'COMANDĂ: DESCHISĂ · POZIȚIE: DESCHISĂ', '#8fe0b6'), (3.0, 'COMANDĂ: DESCHISĂ · POZIȚIE: ÎNCHISĂ', '#ff8377')]),
                     ('Gaze recirculate', (185, -230, 233), 770, 878, 'l', 1.3, END, AMBER)]),
 's16': dict(title=('Cauza 4', 'Aerul și senzorii'), tag='CAUZA 4', chip=OKF, chipc=GREEN, bad=True,
             caps=[(0.3, END, 'Debitmetru care minte sau aer pierdut pe admisie: calculul pornește de la date greșite.')], step=7,
             ecu=dict(calc=(0.5, 0.5), meas=(0.5, 0.25), t=(2.2, 4.2)),
             labels=[('Debitmetru', tuple(S.META['turbo']['maf_pos']), 700, 610, 'l', 0.6, END, BLUE),
                     ('Aer pierdut', tuple(LEAKP), 330, 660, 'l', 2.0, END, RED)]),
 # ---------------- filtrul e victima: cauza e in motor
 's11': dict(title=('Cauza 5', 'Injecția'), tag='CAUZA 5', chip=VIC, chipc=AMBER, bad=True,
             caps=[(0.3, END, 'Injector care picură sau dă prea multă motorină: mai multă funingine decât în calcul.')], step=8,
             ecu=dict(calc=(0.5, 0.5), meas=(0.5, 0.82), t=(4.4, 5.8)),
             labels=[('Injector', (SX, 5.5, 262), 650, 760, 'l', 0.5, END, GREY),
                     ('Evacuare', (SX - 6, -34, 274), 50, 520, 'l', 1.6, END, ORANGE),
                     ('Admisie', (SX - 6, 34, 274), 870, 520, 'l', 2.2, END, BLUE),
                     ('Motorină în plus', (SX, 2, L.DECK - 10), 650, 1300, 'l', 4.5, END, RED)]),
 's12': dict(title=('Cauza 5', 'Injecția'), tag='CAUZA 5', chip=VIC, chipc=AMBER, bad=True,
             caps=[(0.15, 2.3, 'Regenerări dese și foarte fierbinți.'),
                   (2.5, END, 'Așa crapă filtrul. Unul nou pățește la fel.')], step=8,
             ecu=dict(calc=[(0.0, 0.5)], meas=[(0.5, 0.82), (2.1, 0.66), (2.9, 0.66), (3.7, 0.12)]),
             labels=[('Funinginea arde', tuple(dp(0, 24, -1, Z0 + 70)), 600, 520, 'l', 0.6, 2.3, ORANGE),
                     ('Fisură', tuple(dp(0, 30, -0.05, Z0 + 61.0)), 600, 520, 'l', 3.0, END, RED)]),
 's13': dict(title=('Cauza 6', 'Motorul și turbina'), tag='CAUZA 6', chip=VIC, chipc=AMBER, bad=True,
             caps=[(0.3, END, 'Uleiul trecut de segmenți arde în cilindru.')], step=9,
             ecu=dict(calc=(0.5, 0.5), meas=(0.5, 0.6), t=(1.0, 4.0)),
             labels=[('Segmenți uzați', (SX, -40.5, 176), 60, 1300, 'l', 0.7, END, AMBER),
                     ('Fum albăstrui', (SX - 6, -52, 291), 50, 560, 'l', 1.9, END, GREY)]),
 's14': dict(title=('Cauza 6', 'Motorul și turbina'), tag='CAUZA 6', chip=VIC, chipc=AMBER, bad=True,
             caps=[(0.2, END, 'La fel și uleiul scăpat pe axul turbinei.')], step=9,
             ecu=dict(calc=(0.5, 0.5), meas=(0.6, 0.68), t=(0.0, 3.0)),
             labels=[('Etanșarea axului', (34, -218, 266), 600, 1280, 'l', 0.5, END, AMBER)]),
 's15': dict(title=('Cauza 6', 'Motorul și turbina'), tag='CAUZA 6', chip=VIC, chipc=AMBER, bad=True,
             caps=[(0.2, END, 'Rămâne cenușă. Nu arde la regenerare și umple filtrul.')], step=9,
             ecu=dict(calc=(0.5, 0.5), meas=(0.68, 0.86), t=(0.4, 2.8)),
             labels=[('Cenușă', tuple(dp(0, 24, -1, Z1 - 30)), 640, 1250, 'l', 1.0, END, GREY)]),
 's17': dict(title=('Înainte de a schimba filtrul', 'se caută cauza'), tag='DIAGNOZĂ', chip='ÎNAINTE DE FILTRU NOU',
             caps=[], step=10, final=True),
}
STEPS = [['s00'], ['s01', 's02'], ['s03'], ['s04', 's05'], ['s06'], ['s07', 's08', 's09'], ['s10'], ['s16'], ['s11', 's12'], ['s13', 's14', 's15'], ['s17']]

def shot_2d(s, u, k=1.0):
    """zoom-ul si deplasarea 2D ale planului la momentul local u (la fel ca in comp.compose)"""
    dur = s.t1 - s.t0; e = float(X.ease(u / dur)) if s.ease else u / dur
    e = min(max(e, 0.0), 1.0 + 0.4 / dur)
    zoom = s.zoom[0] + (s.zoom[1] - s.zoom[0]) * e
    return zoom, (s.pan[0][0] + (s.pan[1][0] - s.pan[0][0]) * e) * k, (s.pan[0][1] + (s.pan[1][1] - s.pan[0][1]) * e) * k

def export_hud(path):
    import json
    W, H = S.W, S.H; out = {'fps': S.FPS, 'total': TOTAL, 'W': W, 'H': H, 'shots': [], 'steps': []}
    for grp in STEPS:
        ss = [s for s in SHOTS if s.id in grp]; out['steps'].append([ss[0].t0, ss[-1].t1])
    for s in SHOTS:
        h = dict(HUD.get(s.id, {})); d = {'id': s.id, 't0': s.t0, 't1': s.t1}
        dur = s.t1 - s.t0
        for k in ('title', 'tag', 'chip', 'chipc', 'step', 'info', 'final', 'bad', 'hook'):
            if k in h: d[k] = h[k]
        if 'ecu' in h:                         # valorile widgetului, ca chei (t, v) pe fiecare pista
            e = h['ecu']
            if 't' in e: d['ecu'] = {k: [[e['t'][0], e[k][0]], [e['t'][1], e[k][1]]] for k in ('calc', 'meas')}
            else: d['ecu'] = {k: [list(p) for p in e[k]] for k in ('calc', 'meas')}
        d['caps'] = [(c[0], min(c[1], dur), c[2]) for c in h.get('caps', [])]
        labs = []
        f0 = int(round(s.t0 * S.FPS)); f1 = int(round(s.t1 * S.FPS)) + 12
        d['f0'] = f0
        if 'labels' in h:
            cam = X.Cam(cam_J(s.cam), W, H)
            for lab in h['labels']:
                (txt, p3, tx, ty, al, a, b, col) = lab[:8]; sub = lab[8] if len(lab) > 8 else None
                ax = []; ay = []
                for f in range(f0, f1):
                    cam.set2d(*shot_2d(s, f / S.FPS - s.t0))
                    x, y, z = cam.proj(np.array(p3, np.float64)); ax.append(round(float(x[0]), 1)); ay.append(round(float(y[0]), 1))
                labs.append({'text': txt, 'ax': ax, 'ay': ay, 'tx': tx, 'ty': ty, 'al': al, 'on': a, 'off': min(b, dur), 'col': col, 'sub': sub})
        d['labels'] = labs
        out['shots'].append(d)
    open(path, 'w').write('window.TL = ' + json.dumps(out, ensure_ascii=False) + ';\n')
    return out

if __name__ == '__main__':
    import os, json
    o = export_hud(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hud_data.js'))
    for s in o['shots']:
        for l in s['labels']: print(s['id'], l['text'], round(l['ax'][0]), round(l['ay'][0]), '->', l['tx'], l['ty'])
    # verificare: matricea calculata = matricea salvata de Blender
    for n in ('route', 'dpf'):
        p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pl', '%s__%s.json' % (n, 'ghostNR' if n == 'route' else 'soot1'))
        if os.path.exists(p):
            J = json.load(open(p)); print(n, 'dif', float(np.abs(np.array(J['M']) - np.array(cam_J(n)['M'])).max()))
