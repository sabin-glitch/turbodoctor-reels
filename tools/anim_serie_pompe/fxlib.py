# Montaj: proiectia camerei, trasee, curgeri de particule (functii de timp, fara stare), pictare cu test de adancime.
import math
import numpy as np

class Cam:
    def __init__(s, J, W, H):
        M = np.array(J['M'], np.float64); s.V = np.linalg.inv(M); s.W, s.H = W, H
        s.f = J['lens'] / J['sensor'] * H
        s.pos = M[:3, 3] * 1000.0
        s.s = 1.0; s.dx = 0.0; s.dy = 0.0
    def set2d(s, zoom=1.0, dx=0.0, dy=0.0):
        s.s, s.dx, s.dy = zoom, dx, dy
    def proj(s, P):
        P = np.asarray(P, np.float64).reshape(-1, 3) * 0.001
        pc = P @ s.V[:3, :3].T + s.V[:3, 3]
        z = -pc[:, 2]; zz = np.where(z > 1e-4, z, 1e-4)
        x = s.W / 2 + s.f * pc[:, 0] / zz; y = s.H / 2 - s.f * pc[:, 1] / zz
        x = (x - s.W / 2) * s.s + s.W / 2 + s.dx; y = (y - s.H / 2) * s.s + s.H / 2 + s.dy
        return x, y, z
    def px(s, size_mm, z):
        return size_mm * 0.001 * s.f * s.s / np.maximum(z, 1e-4)
    def affine(s):
        return np.array([[s.s, 0, (1 - s.s) * s.W / 2 + s.dx], [0, s.s, (1 - s.s) * s.H / 2 + s.dy]], np.float32)

class Canvas:
    RMAX = 420         # jumatatea maxima a nucleului unui strop. A fost 56: stropii mari (fumul scaparii de la furtunas, r pana la ~200 px) ieseau taiati in patrate vizibile
    def __init__(s, W, H, zbuf):
        s.W, s.H = W, H; s.zf = zbuf.ravel(); s.items = {'add': [], 'over': []}
    def dots(s, x, y, z, r, col, a=1.0, mode='add', shape='g', zbias=0.004, ztest=True, shade=0.0):
        """x, y (px), z (m), r (px); col (3,) sau (N,3); a (N,). shape: 'g' gaussian (stralucire), 'd' disc cu margine neteda."""
        x = np.asarray(x, np.float32); n = len(x)
        if n == 0: return
        y = np.asarray(y, np.float32); z = np.broadcast_to(np.asarray(z, np.float32), (n,))
        r = np.broadcast_to(np.asarray(r, np.float32), (n,)); a = np.broadcast_to(np.asarray(a, np.float32), (n,))
        col = np.broadcast_to(np.asarray(col, np.float32), (n, 3))
        W, H = s.W, s.H
        ext = 1.7 if shape == 'g' else 1.0
        ok = np.isfinite(x) & np.isfinite(y) & (z > 0.02) & (a > 0.004) & (r > 0.05)
        ok &= (x > -r * ext) & (x < W + r * ext) & (y > -r * ext) & (y < H + r * ext)
        if not ok.any(): return
        x, y, z, r, a, col = x[ok], y[ok], z[ok], r[ok], a[ok], col[ok]
        Rk = np.minimum(np.ceil(r * ext + 0.5).astype(np.int32), s.RMAX)
        for k in np.unique(Rk):
            m = Rk == k; o = np.arange(-k, k + 1, dtype=np.float32)
            ox, oy = np.meshgrid(o, o); ox = ox.ravel()[None, :]; oy = oy.ravel()[None, :]
            xm, ym, rm = x[m][:, None], y[m][:, None], r[m][:, None]
            xi = np.floor(xm); yi = np.floor(ym)
            dx = xi + 0.5 + ox - xm; dy = yi + 0.5 + oy - ym
            d2 = dx * dx + dy * dy
            if shape == 'g': w = np.exp(-d2 / (2 * (0.5 * rm) ** 2))
            elif shape == 'r': w = np.clip(1.0 - np.abs(np.sqrt(d2) - rm * 0.78) / (rm * 0.2 + 0.6), 0, 1)
            else: w = np.clip(rm - np.sqrt(d2) + 0.5, 0, 1)
            px = (xi + ox).astype(np.int32); py = (yi + oy).astype(np.int32)
            inb = (px >= 0) & (px < W) & (py >= 0) & (py < H)
            idx = np.where(inb, py * W + px, 0)
            w = w * inb * a[m][:, None]
            if ztest: w = w * (s.zf[idx] > (z[m][:, None] - zbias))
            keep = w > 0.003
            if not keep.any(): continue
            c = np.broadcast_to(col[m][:, None, :], (w.shape[0], w.shape[1], 3))[keep]
            if shade:
                h = np.clip(0.5 - (dx + dy) / (2.4 * rm), 0, 1)[keep]
                c = c * (1 - shade * 0.5 + shade * h[:, None]) + (shade * 0.55 * np.clip(h - 0.72, 0, 1) / 0.28)[:, None]
            s.items[mode].append((idx[keep], w[keep].astype(np.float32), c.astype(np.float32)))
    def flush(s):
        out = {}; n = s.W * s.H
        for mode in ('add', 'over'):
            it = s.items[mode]
            if not it: out[mode] = None; continue
            idx = np.concatenate([i[0] for i in it]); w = np.concatenate([i[1] for i in it]); c = np.concatenate([i[2] for i in it])
            rgb = np.stack([np.bincount(idx, w * c[:, k], n) for k in range(3)], -1).reshape(s.H, s.W, 3).astype(np.float32)
            if mode == 'add': out[mode] = rgb
            else:
                sw = np.bincount(idx, w, n).reshape(s.H, s.W).astype(np.float32)
                A = 1.0 - np.exp(-sw)
                out[mode] = (rgb * (A / np.maximum(sw, 1e-6))[..., None], A)
        return out

def catmull(pts, n_per=10):
    P = np.asarray(pts, np.float64)
    if len(P) < 3 or n_per <= 1: return P
    Q = np.vstack([2 * P[0] - P[1], P, 2 * P[-1] - P[-2]]); out = []
    for i in range(1, len(Q) - 2):
        p0, p1, p2, p3 = Q[i - 1], Q[i], Q[i + 1], Q[i + 2]
        for k in range(n_per):
            t = k / n_per; t2 = t * t; t3 = t2 * t
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    out.append(P[-1]); return np.array(out)

def fillet_path(pts, r, n=8):
    """polilinie cu colturi rotunjite (aceeasi constructie ca la tevile modelate)"""
    P = [np.asarray(p, np.float64) for p in pts]
    out = [P[0]]
    for i in range(1, len(P) - 1):
        a, p, b = P[i - 1], P[i], P[i + 1]
        d1 = a - p; d2 = b - p; l1 = np.linalg.norm(d1); l2 = np.linalg.norm(d2); d1 /= l1; d2 /= l2
        th = math.acos(max(-1.0, min(1.0, float(d1 @ d2))))
        if th > math.pi - 1e-3:
            out.append(p); continue
        rr = r
        t = rr / math.tan(th / 2); tm = min(l1, l2) * 0.49
        if t > tm: t = tm; rr = t * math.tan(th / 2)
        p1 = p + d1 * t; p2 = p + d2 * t
        bis = (d1 + d2); bis /= np.linalg.norm(bis)
        c = p + bis * (rr / math.sin(th / 2))
        v1 = p1 - c; v2 = p2 - c
        ax = np.cross(v1, v2); ax /= np.linalg.norm(ax)
        tot = math.acos(max(-1.0, min(1.0, float(v1 @ v2) / (rr * rr))))
        for k in range(n + 1):
            a_ = tot * k / n
            v = v1 * math.cos(a_) + np.cross(ax, v1) * math.sin(a_) + ax * (ax @ v1) * (1 - math.cos(a_))
            out.append(c + v)
    out.append(P[-1])
    return np.array(out)

class Path:
    """traseu 3D (mm) reesantionat uniform, cu raza si reper transportat (pentru imprastierea in sectiune)"""
    def __init__(s, pts, r=10.0, smooth=10, step=2.0):
        P0 = np.asarray(pts, np.float64); m = len(P0)
        P = catmull(P0, smooth) if smooth and m >= 3 else P0
        ci = np.arange(m) * (smooth if (smooth and m >= 3) else 1)
        d = np.linalg.norm(np.diff(P, axis=0), axis=1); cl = np.r_[0, np.cumsum(d)]
        s.len = float(cl[-1]); n = max(2, int(s.len / step) + 1); u = np.linspace(0, s.len, n)
        s.P = np.stack([np.interp(u, cl, P[:, k]) for k in range(3)], 1)
        rr = np.full(m, r, np.float64) if np.isscalar(r) else np.asarray(r, np.float64)
        s.R = np.interp(u, cl[np.minimum(ci, len(cl) - 1)], rr)
        T = np.gradient(s.P, axis=0); T /= np.linalg.norm(T, axis=1)[:, None]
        N = np.zeros_like(T); a = np.array([0, 0, 1.0]) if abs(T[0, 2]) < 0.9 else np.array([1.0, 0, 0])
        v = a - T[0] * (a @ T[0]); N[0] = v / np.linalg.norm(v)
        for i in range(1, n):
            v = N[i - 1] - T[i] * (N[i - 1] @ T[i]); N[i] = v / np.linalg.norm(v)
        s.T, s.N, s.B, s.n = T, N, np.cross(T, N), n
    def at(s, sm):
        f = np.clip(np.asarray(sm, np.float64) / s.len, 0, 1) * (s.n - 1)
        i = np.minimum(f.astype(np.int64), s.n - 2); t = (f - i)[:, None]
        L = lambda A: A[i] * (1 - t) + A[i + 1] * t
        return L(s.P), L(s.T), L(s.N), L(s.B), s.R[i] * (1 - t[:, 0]) + s.R[i + 1] * t[:, 0]

_RT = {}
def rnd(seed, n, k=8):
    key = (seed, n, k)
    if key not in _RT: _RT[key] = np.random.default_rng(seed).random((n, k))
    return _RT[key]

def flow(path, t, n, speed, seed=1, lat=0.8, t0=None, t1=None, jit=0.15, swirl=0.0, fade=18.0, ends=(True, True), span=None):
    """n particule care merg pe traseu cu viteza speed (mm/s). t0 / t1 = momentul in care porneste / se opreste sursa
    (frontul inainteaza pe traseu). Intoarce pozitii (mm), alfa, fractiunea de traseu, tabela de numere aleatoare."""
    r = rnd(seed, n); sv = 1 + (r[:, 1] - 0.5) * 2 * jit
    Lp = path.len if span is None else span
    sm = (r[:, 0] * Lp + t * speed * sv) % Lp
    a = np.ones(n)
    if t0 is not None: a *= np.clip(((t - t0) * speed * sv - sm) / fade, 0, 1)
    if t1 is not None: a *= np.clip((sm - (t - t1) * speed * sv) / fade, 0, 1)
    if ends[0]: a *= np.clip(sm / fade, 0, 1)
    if ends[1]: a *= np.clip((path.len - sm) / fade, 0, 1)
    a *= (sm <= path.len)
    C, T, N, B, R = path.at(sm)
    rr = np.sqrt(r[:, 2]) * lat; th = r[:, 3] * 2 * np.pi + swirl * sm
    P = C + (R * rr)[:, None] * (np.cos(th)[:, None] * N + np.sin(th)[:, None] * B)
    return P, a, sm / path.len, r

def ramp(x, xs, cs):
    """interpolare de culoare: x (N,) in [0,1], xs noduri, cs culori (K,3)"""
    cs = np.asarray(cs, np.float64)
    return np.stack([np.interp(x, xs, cs[:, k]) for k in range(3)], -1)

def hexc(h):
    return np.array([((h >> 16) & 255) / 255.0, ((h >> 8) & 255) / 255.0, (h & 255) / 255.0])

def ease(u):
    u = np.clip(u, 0, 1); return u * u * (3 - 2 * u)
def seg(t, a, b):
    """0 inainte de a, 1 dupa b, neted intre ele"""
    return ease((t - a) / max(b - a, 1e-6))
def win(t, a, b, f=0.3):
    """fereastra: urca in f secunde de la a, coboara in f secunde pana la b"""
    return float(np.clip((t - a) / f, 0, 1) * np.clip((b - t) / f, 0, 1))
