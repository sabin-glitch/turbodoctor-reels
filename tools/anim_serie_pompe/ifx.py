# Efectele seriei pompelor (pornite de la seria injectoarelor): curgeri de particule pe fetele de sectiune, scantei, fum, bule, si etichetele
# (sprite + linie de legatura cu punct), lupa, grafice. Toate functiile primesc contextul C din icomp.compose.
import os, json, math
import numpy as np, cv2
import fxlib as X
from fxlib import seg, win, ease, hexc
import icomp as IC

HP = hexc(0xff5a26); LP = hexc(0xffc02a); WATER = hexc(0x2f9bff); WHITE = np.ones(3); YEL = hexc(0xFFD21F)
GRIT = hexc(0x15110d); RED = hexc(0xff4b4b); GREEN = hexc(0x3ddc84); RUST = hexc(0xa8471c)
METAL = np.array([0.86, 0.88, 0.92]); AIR = np.array([0.90, 0.95, 1.0]); PETROL = hexc(0xa8e85a); ADBLUE = hexc(0xbfe6ff); LAC = hexc(0x4a2a12)
EZ = np.array([0, 0, 1.0])
# Pompa CP4 in reperul scenei (mm): arborele pe axa Y (capatul filetat la y = -69), cama in origine, pistonul pe +Z.
# Sectiunea scoate sfertul x > 0, y < 0: fata 'R' = planul y = 0 (se vede din fata, x > 0), fata 'L' = planul x = 0 (y < 0).
NR = np.array([0.0, -1.0, 0.0]); NL = np.array([1.0, 0.0, 0.0])
def PR(x, z): return np.array([x, -0.06, z])
def PLf(y, z): return np.array([0.06, y, z])

# ------------------------------------------------------------------ trasee
class IPath(X.Path):
    """traseu pe o fata de sectiune: imprastierea laterala ramane in planul fetei"""
    def __init__(s, pts, plane=None, r=0.5, smooth=10, step=0.05):
        X.Path.__init__(s, pts, r=r, smooth=smooth, step=step)
        s.plane = plane
        if plane is not None:
            n = NR if plane == 'R' else NL
            L = np.cross(n[None, :], s.T); ln = np.linalg.norm(L, axis=1)[:, None]
            s.L = np.where(ln > 1e-6, L / np.maximum(ln, 1e-9), s.N)
        else:
            s.L = s.N
    def atL(s, sm):
        f = np.clip(np.asarray(sm, np.float64) / s.len, 0, 1) * (s.n - 1)
        i = np.minimum(f.astype(np.int64), s.n - 2); t = (f - i)[:, None]
        return s.L[i] * (1 - t) + s.L[i + 1] * t

def ring(r, a0, a1, n=24, plane='R'):
    """arc in jurul camei pe fata de sectiune (unghiuri in grade, 0 = dreapta, 90 = sus)"""
    a = np.radians(np.linspace(a0, a1, n))
    if plane == 'R': return [PR(r * math.cos(t), r * math.sin(t)) for t in a]
    return [PLf(-r * math.cos(t), r * math.sin(t)) for t in a]

PATHS = {}
def path(name):
    if name in PATHS: return PATHS[name]
    if name == 'cam_R': p = IPath(ring(24.0, -80, 80), 'R', 2.6, smooth=0, step=0.25)              # in baia camei, in dreapta arborelui
    elif name == 'cam_Rup': p = IPath(ring(24.0, -80, 60) + [PR(11.0, 22.0), PR(6.0, 22.5)], 'R', 2.4, smooth=0, step=0.25)
    elif name == 'cam_Ldn': p = IPath([PLf(-10.0, -19.0), PLf(-6.0, -24.0), PLf(-1.0, -24.5)], 'L', 2.0, smooth=4, step=0.25)
    elif name == 'cam_Lup': p = IPath([PLf(-10.0, 17.0), PLf(-6.0, 22.0), PLf(-1.0, 23.5)], 'L', 2.0, smooth=4, step=0.25)
    elif name == 'bore': p = IPath([PR(0.0, 72.0), PR(0.0, 79.0)], 'R', 2.4, smooth=0, step=0.2)                      # camera de deasupra pistonului
    elif name == 'hp_out': p = IPath([PR(0.5, 81.6), PR(14.0, 81.6), PR(28.0, 81.6), PR(52.5, 81.6)], 'R', 1.3, smooth=0, step=0.25)   # spre rampa
    elif name == 'lp_in': p = IPath([PLf(-17.5, 88.3), PLf(-6.0, 88.3), PLf(-1.0, 87.0)], 'L', 1.6, smooth=4, step=0.25)        # galeria de admisie
    elif name == 'lp_inR': p = IPath([PR(7.5, 88.3), PR(2.0, 88.3), PR(0.6, 85.6)], 'R', 1.3, smooth=4, step=0.2)
    else: raise KeyError(name)
    PATHS[name] = p; return p

# ------------------------------------------------------------------ particule
def zb_for(C, z):
    return float(max(3e-5, 0.0007 * float(np.median(z)) if len(z) else 1e-4))

def flow(C, p, n, speed, col, size, lat=0.85, seed=1, t0=None, t1=None, a=1.0, mode='over', shape='d', shade=0.35, jit=0.2,
         fade=None, ends=(True, True), sz_var=0.5, glow=0.0, tail=0, tail_dt=0.012, ztest=True, minpx=0.6):
    """n particule pe traseul p (mm/s); t0/t1 = cand porneste / se opreste sursa (frontul inainteaza pe traseu)"""
    if isinstance(p, str): p = path(p)
    t = C.t; fade = fade if fade is not None else max(p.len * 0.04, 0.2)
    r = X.rnd(seed, n); sv = 1 + (r[:, 1] - 0.5) * 2 * jit
    for k in range(tail + 1):
        tt = t - k * tail_dt
        sm = (r[:, 0] * p.len + tt * speed * sv) % p.len
        al = np.ones(n) * (1.0 if k == 0 else 0.55 * (1 - k / (tail + 1)))
        if t0 is not None: al *= np.clip(((tt - t0) * speed * sv - sm) / fade, 0, 1)
        if t1 is not None: al *= np.clip((sm - (tt - t1) * speed * sv) / fade, 0, 1)
        if ends[0]: al *= np.clip(sm / fade, 0, 1)
        if ends[1]: al *= np.clip((p.len - sm) / fade, 0, 1)
        Cc, T, N, B, R = p.at(sm); L = p.atL(sm)
        off = (r[:, 2] * 2 - 1) * lat
        P = Cc + (R * off)[:, None] * L
        x, y, z = C.cam.proj(P)
        rp = C.cam.px(size * (1 + (r[:, 4] - 0.5) * 2 * sz_var), z) * (1.0 if k == 0 else 0.8)
        cc = np.broadcast_to(np.asarray(col, np.float32), (n, 3)) if np.ndim(col) == 1 else col
        C.cv.dots(x, y, z, np.maximum(rp, minpx * C.k), cc, al * a, mode=mode, shape=shape, zbias=zb_for(C, z), shade=shade, ztest=ztest)
        if glow > 0 and k == 0:
            C.cv.dots(x, y, z, np.maximum(rp, minpx * C.k) * 3.0, cc, al * a * glow, mode='add', shape='g', zbias=zb_for(C, z), ztest=ztest)

def grit(C, p, n, speed, size=0.06, seed=7, a=1.0, sz_var=0.6, **kw):
    """particule dure, inchise la culoare, cu un mic luciu (vizibile pe motorina portocalie)"""
    r = X.rnd(seed + 99, n)
    col = np.stack([0.10 + 0.10 * r[:, 0], 0.085 + 0.07 * r[:, 0], 0.07 + 0.05 * r[:, 0]], -1)
    flow(C, p, n, speed, col, size, seed=seed, a=a, shade=0.8, sz_var=sz_var, **kw)

def dots3(C, P, size, col, a=1.0, mode='over', shape='d', shade=0.4, ztest=True):
    P = np.asarray(P, np.float64).reshape(-1, 3)
    x, y, z = C.cam.proj(P); rp = C.cam.px(np.asarray(size, np.float64), z)
    C.cv.dots(x, y, z, np.maximum(rp, 0.6), col, a, mode=mode, shape=shape, zbias=zb_for(C, z), shade=shade, ztest=ztest)

def sparks(C, p0, tb, n=40, life=0.35, speed=3.0, size=0.03, seed=3, col=None, spread=1.0, up=None, a=1.0):
    """scantei la momentul tb in punctul p0 (mm); speed in mm/s"""
    u = C.t - tb
    if u < 0 or u > life * 1.6: return
    r = X.rnd(seed, n, 8)
    d = np.stack([r[:, 0] - 0.5, r[:, 1] - 0.5, r[:, 2] - 0.5], -1); d /= np.maximum(np.linalg.norm(d, axis=1)[:, None], 1e-6)
    if up is not None: d = d * spread + np.asarray(up)[None, :]; d /= np.linalg.norm(d, axis=1)[:, None]
    lf = life * (0.5 + r[:, 3]); v = speed * (0.4 + r[:, 4])
    for k in range(4):
        uu = u - k * 0.012
        al = np.clip(1 - uu / lf, 0, 1) * (uu > 0) * (1 - k * 0.22)
        P = np.asarray(p0)[None, :] + d * (v * uu)[:, None]
        x, y, z = C.cam.proj(P); rp = C.cam.px(size, z)
        cc = np.array([1.0, 0.86, 0.45]) if col is None else col
        C.cv.dots(x, y, z, np.maximum(rp, 0.8), cc, al * a, mode='add', shape='g', zbias=zb_for(C, z))

def glow(C, p0, r_px, col, a):
    if a <= 0.003: return
    x, y = C.P(p0)
    C.cv.dots([x], [y], [0.05], [r_px], np.asarray(col)[None, :], [a], mode='add', shape='g', ztest=False)

def smoke(C, p0, t0, rate=1.0, n=60, rise=(0, 0, 8.0), spread=6.0, size=3.0, col=(0.12, 0.12, 0.13), a=0.35, life=2.2, seed=31, t1=None):
    t = C.t
    if t < t0: return
    r = X.rnd(seed, n, 8)
    age = (t - t0 - r[:, 0] * life) % life; birth = t - age
    ok = (birth >= t0) & ((birth <= t1) if t1 is not None else True)
    if not ok.any(): return
    u = age / life
    P = np.asarray(p0)[None, :] + np.asarray(rise)[None, :] * (age[:, None]) + np.stack([(r[:, 1] - .5), (r[:, 2] - .5), (r[:, 3] - .5) * .4], -1) * spread * (0.3 + u[:, None])
    x, y, z = C.cam.proj(P); rp = C.cam.px(size * (0.5 + 1.5 * u) * (0.6 + r[:, 4]), z)
    al = ok * np.sin(np.clip(u, 0, 1) * math.pi) * a
    C.cv.dots(x, y, z, rp, np.asarray(col)[None, :] * (0.8 + 0.4 * r[:, 5:6]), al, mode='over', shape='g', zbias=zb_for(C, z))

def bubbles(C, p, n, speed, size, seed=41, a=0.9, col=(0.85, 0.93, 1.0), implode=None, **kw):
    """bule (aer sau cavitatie) pe un traseu; implode=(punct, raza): langa punct se strang si dispar cu o sclipire"""
    flow(C, p, n, speed, np.asarray(col), size, seed=seed, a=a, shape='r', shade=0.0, mode='over', **kw)

# ------------------------------------------------------------------ etichete
def _line(C, p0, p1, a=1.0, col=(255, 255, 255), th=2.6, frac=1.0, dot=True, dot_r=6.0):
    """linie de legatura alba cu umbra; frac = cat din linie e desenat (de la p0 spre p1)"""
    if a <= 0.003 or frac <= 0.001: return
    k = C.k; x0, y0 = p0; x1, y1 = p1
    x1 = x0 + (x1 - x0) * frac; y1 = y0 + (y1 - y0) * frac
    pad = int(14 * k)
    xa, xb = int(min(x0, x1)) - pad, int(max(x0, x1)) + pad; ya, yb = int(min(y0, y1)) - pad, int(max(y0, y1)) + pad
    xa, ya = max(0, xa), max(0, ya); xb, yb = min(IC.W, xb), min(IC.H, yb)
    if xb <= xa or yb <= ya: return
    buf = np.zeros((yb - ya, xb - xa, 4), np.uint8); S = 4
    q0 = (int(round((x0 - xa) * S)), int(round((y0 - ya) * S))); q1 = (int(round((x1 - xa) * S)), int(round((y1 - ya) * S)))
    cv2.line(buf, q0, q1, (0, 0, 0, 120), max(1, int(round((th + 3.0) * k))), cv2.LINE_AA, shift=2)
    if dot: cv2.circle(buf, q0, int(round((dot_r + 2.5) * k * S)), (0, 0, 0, 120), -1, cv2.LINE_AA, shift=2)
    m = buf[..., 3:4].astype(np.float32) / 255.0
    sh = np.zeros_like(buf); cv2.line(sh, q0, q1, (*col, 255), max(1, int(round(th * k))), cv2.LINE_AA, shift=2)
    if dot: cv2.circle(sh, q0, int(round(dot_r * k * S)), (*col, 255), -1, cv2.LINE_AA, shift=2)
    ms = sh[..., 3:4].astype(np.float32) / 255.0
    rgb = sh[..., :3].astype(np.float32) / 255.0 * ms
    A = np.clip(ms + m * (1 - ms), 0, 1) * a; RGB = rgb * a
    d = C.ov[ya:yb, xa:xb]
    d[..., :3] = RGB + d[..., :3] * (1 - A); d[..., 3:4] = A + d[..., 3:4] * (1 - A)
    C.used = True

def pop(t, t_in, t_out=None, din=0.22, dout=0.25):
    a = float(seg(t, t_in, t_in + din))
    if t_out is not None: a *= 1 - float(seg(t, t_out - dout, t_out))
    return a

def spr(C, sid, x, y, t_in, t_out=None, anchor='tl', scale=1.0, slide=(0, 10), popk=0.9):
    """sprite (eticheta, card, panou) la (x, y) in coordonate 1080x1920"""
    a = pop(C.t, t_in, t_out)
    if a <= 0.003: return None
    s = IC.sprite(C.ep, sid); k = C.k; h, w = s.shape[:2]
    if k != 1.0: s = cv2.resize(s, (max(1, int(w * k)), max(1, int(h * k))), interpolation=cv2.INTER_AREA); h, w = s.shape[:2]
    xx, yy = x * k, y * k
    if anchor[1] == 'c': xx -= w / 2
    elif anchor[1] == 'r': xx -= w
    if anchor[0] == 'c': yy -= h / 2
    elif anchor[0] == 'b': yy -= h
    e = float(ease(a)); sc = scale * (popk + (1 - popk) * e)
    xx += slide[0] * (1 - e) * k; yy += slide[1] * (1 - e) * k
    IC.blit(C.ov, s, xx, yy, a, sc); C.used = True
    return (xx, yy, w, h)

def label(C, sid, at, box, t_in, t_out=None, side=None, anchor='tl'):
    """eticheta cu linie de legatura: at = punct 3D (mm) sau ('px', x, y); box = (x, y) al etichetei (1080x1920)"""
    t = C.t
    if t < t_in or (t_out is not None and t > t_out): return
    s = IC.sprite(C.ep, sid); k = C.k; h, w = s.shape[0] * k, s.shape[1] * k
    bx, by = box[0] * k, box[1] * k
    if anchor[1] == 'c': bx -= w / 2
    elif anchor[1] == 'r': bx -= w
    if anchor[0] == 'c': by -= h / 2
    elif anchor[0] == 'b': by -= h
    ax, ay = C.P(at)
    if side is None: side = 'l' if ax < bx + w / 2 else 'r'
    ex = bx if side == 'l' else bx + w; ey = by + h / 2
    al = 1.0 - (float(seg(t, t_out - 0.25, t_out)) if t_out is not None else 0.0)
    fr = float(ease((t - t_in) / 0.22))
    _line(C, (ax, ay), (ex, ey), al, frac=fr)
    if t >= t_in + 0.12:
        spr(C, sid, box[0], box[1], t_in + 0.12, t_out, anchor=anchor, slide=(10 if side == 'l' else -10, 0))

def tag(C, sid, at, t_in, t_out=None, dx=60, dy=-80, side=None):
    """eticheta asezata relativ la punctul ei pe ecran"""
    if C.t < t_in or (t_out is not None and C.t > t_out): return
    ax, ay = C.P(at); k = C.k
    s = IC.sprite(C.ep, sid); w, h = s.shape[1], s.shape[0]
    bx = ax / k + dx; by = ay / k + dy
    if dx < 0: bx -= w
    bx = min(max(bx, 24), 1080 - 24 - w); by = min(max(by, 200), 1260 - h)
    label(C, sid, at, (bx, by), t_in, t_out, side=side)

def lens(C, cam, st, cx, cy, R, t_in, t_out=None, kb=(1.0, 0, 0), src=None, ring=(255, 210, 31), pf=None, tag='', grow=True, din=0.3):
    """lupa: placa cam:st (fara particule) intr-un cerc cu rama, legata de punctul src (3D sau ('px', x, y))"""
    a = pop(C.t, t_in, t_out, din, 0.3)
    if a <= 0.003: return
    k = C.k; e = float(ease(a)); Rr = R * (0.6 + 0.4 * e) if grow else R          # grow=False: doar se topeste peste ce e dedesubt (schimbarea starii din lupa)
    key = ('lens', cam, st, kb, IC.W, IC.H, tag)
    img = IC._cache.get(key)
    if img is None:
        p, z, Jp = IC.plate(cam, st); camo = X.Cam(Jp, IC.W, IC.H); camo.set2d(kb[0], kb[1] * k, kb[2] * k)
        if pf is not None: p = pf(p, 1e9)                                           # lichidul recolorat (tag deosebeste variantele in memorie)
        rg = cv2.warpAffine(p, camo.affine(), (IC.W, IC.H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
        bg = IC.stage_bg(); img = IC.keep(key, bg * (1 - rg[..., 3:4]) + rg[..., :3], cap=40)
    if src is not None:
        sx, sy = C.P(src); dx, dy = cx * k - sx, cy * k - sy; dl = math.hypot(dx, dy) + 1e-6
        _line(C, (sx, sy), (cx * k - dx / dl * Rr * k, cy * k - dy / dl * Rr * k), a, col=ring, th=2.6, frac=e)
    # cercul: imaginea centrata pe centrul placii, decupata
    rr = int(Rr * k); x0, y0 = int(cx * k - rr), int(cy * k - rr)
    hh, ww = IC.H, IC.W; sx0 = int(ww / 2 - rr); sy0 = int(hh / 2 - rr)
    yy, xx = np.mgrid[-rr:rr, -rr:rr].astype(np.float32)
    m = np.clip(rr - np.sqrt(xx ** 2 + yy ** 2), 0, 1)[..., None]
    crop = img[max(0, sy0):sy0 + 2 * rr, max(0, sx0):sx0 + 2 * rr]
    if crop.shape[0] != 2 * rr or crop.shape[1] != 2 * rr: return
    tile = np.concatenate([crop * m, m], -1) * a
    IC.blit(C.ov, tile, x0, y0, 1.0)
    buf = np.zeros((2 * rr + 20, 2 * rr + 20, 4), np.uint8)
    cv2.circle(buf, (rr + 10, rr + 10), rr, (0, 0, 0, 140), max(2, int(9 * k)), cv2.LINE_AA)
    cv2.circle(buf, (rr + 10, rr + 10), rr, (*ring, 255), max(2, int(5 * k)), cv2.LINE_AA)
    al = buf[..., 3:4].astype(np.float32) / 255.0
    rgb = buf[..., :3].astype(np.float32) / 255.0 * al
    IC.blit(C.ov, np.concatenate([rgb, al], -1) * a, x0 - 10, y0 - 10, 1.0); C.used = True

def graph(C, x, y, w, h, curves, prog, a=1.0, axis_col=(150, 160, 172), grid=True, tl=None):
    """grafic simplu in coordonate 1080x1920: curves = [(xs 0..1, ys 0..1, (r,g,b), grosime)], prog = cat din curbe e desenat (0..1)"""
    if a <= 0.003: return
    k = C.k; X0, Y0, Wd, Hd = int(x * k), int(y * k), int(w * k), int(h * k)
    buf = np.zeros((Hd + 8, Wd + 8, 4), np.uint8); S = 4
    def pt(u, v): return (int(round((4 + u * Wd) * S)), int(round((4 + (1 - v) * Hd) * S)))
    cv2.line(buf, pt(0, 0), pt(1, 0), (*axis_col, 230), max(1, int(3 * k)), cv2.LINE_AA, shift=2)
    cv2.line(buf, pt(0, 0), pt(0, 1), (*axis_col, 230), max(1, int(3 * k)), cv2.LINE_AA, shift=2)
    if grid:
        for g in (0.25, 0.5, 0.75): cv2.line(buf, pt(0, g), pt(1, g), (*axis_col, 50), max(1, int(1.5 * k)), cv2.LINE_AA, shift=2)
    for xs, ys, col, th in curves:
        xs = np.asarray(xs); ys = np.asarray(ys); m = xs <= prog
        if m.sum() < 2: continue
        pts = np.array([pt(u, v) for u, v in zip(xs[m], ys[m])], np.int32)
        cv2.polylines(buf, [pts], False, (*col, 255), max(1, int(th * k)), cv2.LINE_AA, shift=2)
    al = buf[..., 3:4].astype(np.float32) / 255.0
    IC.blit(C.ov, np.concatenate([buf[..., :3].astype(np.float32) / 255.0 * al, al], -1) * a, X0 - 4, Y0 - 4, 1.0); C.used = True

def bracket(C, p0, p1, a, col=(255, 210, 31), th=3.0, tick=14):
    """cota intre doua puncte de pe ecran (px 1080x1920), cu capete"""
    if a <= 0.003: return
    k = C.k; x0, y0 = p0[0] * k, p0[1] * k; x1, y1 = p1[0] * k, p1[1] * k
    dx, dy = x1 - x0, y1 - y0; L = math.hypot(dx, dy) + 1e-6; nx, ny = -dy / L * tick * k, dx / L * tick * k
    _line(C, (x0, y0), (x1, y1), a, col=col, th=th, dot=False)
    _line(C, (x0 - nx, y0 - ny), (x0 + nx, y0 + ny), a, col=col, th=th, dot=False)
    _line(C, (x1 - nx, y1 - ny), (x1 + nx, y1 + ny), a, col=col, th=th, dot=False)

def rect(C, x, y, w, h, col, a):
    if a <= 0.003: return
    k = C.k; X0, Y0, X1, Y1 = int(x * k), int(y * k), int((x + w) * k), int((y + h) * k)
    X0, Y0, X1, Y1 = max(0, X0), max(0, Y0), min(IC.W, X1), min(IC.H, Y1)
    if X1 <= X0 or Y1 <= Y0: return
    d = C.ov[Y0:Y1, X0:X1]; c = np.asarray(col, np.float32)
    d[..., :3] = c * a + d[..., :3] * (1 - a); d[..., 3:4] = a + d[..., 3:4] * (1 - a); C.used = True
