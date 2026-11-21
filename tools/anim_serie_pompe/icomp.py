# Montajul seriei „De ce se strică pompele de înaltă presiune”: plăci Blender (imagine + adâncime + cameră, cu bucle de mișcare pe regiuni)
# + particule + etichete -> cadre 1080x1920. Pornit de la montajul seriei injectoarelor (/home/claude/w/serinj/icomp.py).
#   python3 icomp.py epN --out <dir> [--part i n] [--range f0 f1]         cadrele lipsă (se poate relua)
#   python3 icomp.py epN --t 3 12.5 60 --out proba.jpg --sheet 4 [--scale .5] [--guides]
import os, sys, json, math, argparse, time, importlib, unicodedata, re
import numpy as np, cv2
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import fxlib as X
from fxlib import seg, win, ease, hexc

W, H, FPS = 1080, 1920, 30
PLD = [os.path.join(HERE, 'pl'), os.path.join(HERE, 'pl_x'), '/home/claude/w/serinj/pl', '/home/claude/w/serinj/pl_x']
HUD = os.path.join(HERE, 'hud')

# ------------------------------------------------------------------ cache
_cache = {}; _order = []
def keep(key, val, cap=14):
    _cache[key] = val; _order.append(key)
    while len(_order) > cap:
        k = _order.pop(0)
        if k not in _order: _cache.pop(k, None)
    return val

def read_rgba(path, w=None, h=None):
    im = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if im is None: raise FileNotFoundError(path)
    if im.ndim == 2: im = cv2.cvtColor(im, cv2.COLOR_GRAY2BGRA)
    if im.shape[2] == 3: im = cv2.cvtColor(im, cv2.COLOR_BGR2BGRA)
    im = cv2.cvtColor(im, cv2.COLOR_BGRA2RGBA).astype(np.float32) / 255.0
    im[..., :3] *= im[..., 3:4]
    if w and (im.shape[1] != w or im.shape[0] != h):
        im = cv2.resize(im, (w, h), interpolation=cv2.INTER_AREA if im.shape[1] > w else cv2.INTER_CUBIC)
    return im

def find_plate(name):
    for d in PLD:
        b = os.path.join(d, name)
        if os.path.exists(b + '.png'): return b
    raise FileNotFoundError(name)

def plate(cam, st):
    key = ('p', cam, st, W, H)
    if key in _cache: return _cache[key]
    b = find_plate('%s__%s' % (cam, st))
    rgba = read_rgba(b + '.png', W, H)
    if os.path.exists(b + '.z.npy'):
        z = np.load(b + '.z.npy')
        if z.shape != (H, W): z = cv2.resize(z, (W, H), interpolation=cv2.INTER_NEAREST)
    else:
        z = np.full((H, W), 1e6, np.float32)
    return keep(key, (rgba, z.astype(np.float32), json.load(open(b + '.json'))))

# ------------------------------------------------------------------ bucle de miscare (regiuni randate cadru cu cadru peste placa fixa)
_loops = {}
def loop_of(cam, st):
    """bucla placii cam:st (pl/<cam>__<st>.loop: box.json + kNNN.png, optional kkNNN.png pentru pana arborelui) sau None"""
    key = (cam, st)
    if key in _loops: return _loops[key]
    L = None
    try: b = find_plate('%s__%s' % (cam, st))
    except FileNotFoundError: b = None
    if b and os.path.exists(b + '.loop/box.json'):
        J = json.load(open(b + '.loop/box.json'))
        if all(os.path.exists(b + '.loop/k%03d.png' % k) for k in range(J['n'])):
            K = J.get('key')
            if K and not all(os.path.exists(b + '.loop/kk%03d.png' % k) for k in range(K['n'])): J['key'] = None
            L = dict(J=J, dir=b + '.loop', fr={})
    _loops[key] = L; return L

def _loop_frame(L, kind, k):
    ck = (kind, k, W)
    if ck not in L['fr']:
        im = read_rgba(os.path.join(L['dir'], '%s%03d.png' % (kind, k)))
        if W != L['J']['W']:
            s = W / float(L['J']['W'])
            im = cv2.resize(im, (max(1, int(round(im.shape[1] * s))), max(1, int(round(im.shape[0] * s)))), interpolation=cv2.INTER_AREA)
        L['fr'][ck] = (np.clip(im, 0, 1) * 255.0 + 0.5).astype(np.uint8)
    return L['fr'][ck].astype(np.float32) * (1.0 / 255.0)

def _feather(h, w, m):
    key = ('fe', h, w, m); f = _cache.get(key)
    if f is None:
        y = np.minimum(np.arange(h), np.arange(h)[::-1]).astype(np.float32); x = np.minimum(np.arange(w), np.arange(w)[::-1]).astype(np.float32)
        f = keep(key, (np.clip((y + 0.5) / m, 0, 1)[:, None] * np.clip((x + 0.5) / m, 0, 1)[None, :])[..., None].astype(np.float32), cap=64)
    return f

def _paste(q, fr, x, y, m):
    h, w = fr.shape[:2]; h = min(h, H - y); w = min(w, W - x)
    if h <= 0 or w <= 0 or x < 0 or y < 0: return
    f = _feather(h, w, m); d = q[y:y + h, x:x + w]
    d[...] = d * (1 - f) + fr[:h, :w] * f

def with_loop(cam, st, p, phase):
    """placa cu regiunea pieselor in miscare la faza data (in curse: 1.0 = o cursa a pistonului = jumatate de tura a arborelui)"""
    L = loop_of(cam, st)
    if L is None or phase is None: return p
    J = L['J']; n = J['n']; s = W / float(J['W'])
    k2 = int(math.floor(phase * n + 1e-6)) % (2 * n); k = k2 % n
    q = p.copy(); m = max(2, int(round(6 * s)))
    _paste(q, _loop_frame(L, 'k', k), int(round(J['x'] * s)), int(round(J['y'] * s)), m)
    K = J.get('key')
    if K and k2 >= n: _paste(q, _loop_frame(L, 'kk', k2), int(round(K['x'] * s)), int(round(K['y'] * s)), max(2, int(round(3 * s))))
    return q

# ------------------------------------------------------------------ fundal + marcaj
def stage_bg():
    key = ('stage', W, H)
    if key in _cache: return _cache[key]
    p = os.path.join(HUD, 'common', 'stage.png')
    im = cv2.cvtColor(cv2.imread(p), cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
    if im.shape[0] != H: im = cv2.resize(im, (W, H), interpolation=cv2.INTER_AREA)
    rng = np.random.default_rng(3); im += (rng.random((H, W, 1)).astype(np.float32) - 0.5) * (1.4 / 255)
    return keep(key, im, cap=64)

def wm_sheet():
    key = ('wm',)
    if key in _cache: return _cache[key]
    p = os.path.join(HUD, 'common', 'wm.png'); idx = json.load(open(os.path.join(HUD, 'common', 'index.json')))['wm']
    im = cv2.imread(p, cv2.IMREAD_UNCHANGED)             # BGRA uint8, alfa drept
    a = im[..., 3:4].astype(np.float32) / 255.0
    pm = np.concatenate([(im[..., :3].astype(np.float32) * a)[..., ::-1], a * 255.0], -1)   # RGB premultiplicat, 0..255
    return keep(key, (np.clip(pm, 0, 255).astype(np.uint8), idx['unit']), cap=64)

def watermark(t):
    """randurile TURBO DOCTOR din spatele scenei (ca la seria turbinelor: -20 de grade, 9 px/s)"""
    sheet, unit = wm_sheet(); c, s = math.cos(math.radians(20)), math.sin(math.radians(20))
    o = (t * 9.0) % unit; k = W / 1080.0
    tx0 = -unit + o - 1240.0; ty0 = -1460.0
    M = np.array([[c * k, s * k, (c * tx0 + s * ty0 + 540.0) * k], [-s * k, c * k, (-s * tx0 + c * ty0 + 960.0) * k]], np.float32)
    out = cv2.warpAffine(sheet, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    return out.astype(np.float32) / 255.0

def background(t):
    bg = stage_bg(); wm = watermark(t)
    return bg * (1 - wm[..., 3:4]) + wm[..., :3]

# ------------------------------------------------------------------ cuvinte
def norm(w):
    w = unicodedata.normalize('NFD', w.lower()); w = ''.join(ch for ch in w if unicodedata.category(ch) != 'Mn')
    return re.sub(r'[^a-z0-9µ]', '', w)

class Cues:
    def __init__(s, path):
        c = json.load(open(path)); s.lines = c['lines']; s.words = c['words']; s.end = c['end']
    def L(s, i): return s.lines[i]['start']
    def LE(s, i): return s.lines[i]['end']
    def W(s, i, word, n=1, end=False):
        k = 0; nw = norm(word)
        for w in s.words:
            if w['win'] != i: continue
            if norm(w['text']).startswith(nw):
                k += 1
                if k == n: return w['e'] if end else w['s']
        raise KeyError('cuvantul %r (%d) nu e in randul %d' % (word, n, i))

# ------------------------------------------------------------------ sprite-uri
def sprite(ep, sid):
    key = ('s', ep, sid)
    if key in _cache: return _cache[key]
    for d in (os.path.join(HUD, ep), os.path.join(HUD, 'common')):
        p = os.path.join(d, sid + '.png')
        if os.path.exists(p): return keep(key, read_rgba(p), cap=400)
    raise FileNotFoundError('sprite %s/%s' % (ep, sid))

def blit(dst, spr, x, y, a=1.0, scale=1.0):
    """spr premultiplicat peste dst (RGB premultiplicat cu alfa separat sau RGB simplu), colt stanga-sus la (x, y)"""
    if a <= 0.003: return
    if abs(scale - 1.0) > 1e-3:
        h0, w0 = spr.shape[:2]; nw, nh = max(1, int(round(w0 * scale))), max(1, int(round(h0 * scale)))
        x += (w0 - nw) / 2.0; y += (h0 - nh) / 2.0
        spr = cv2.resize(spr, (nw, nh), interpolation=cv2.INTER_AREA if scale < 1 else cv2.INTER_LINEAR)
    xi, yi = int(round(x)), int(round(y)); h, w = spr.shape[:2]
    x0, y0, x1, y1 = max(0, xi), max(0, yi), min(dst.shape[1], xi + w), min(dst.shape[0], yi + h)
    if x1 <= x0 or y1 <= y0: return
    s = spr[y0 - yi:y1 - yi, x0 - xi:x1 - xi] * a
    d = dst[y0:y1, x0:x1]
    d[..., :3] = s[..., :3] + d[..., :3] * (1 - s[..., 3:4])
    if dst.shape[2] == 4: d[..., 3:4] = s[..., 3:4] + d[..., 3:4] * (1 - s[..., 3:4])

# ------------------------------------------------------------------ planuri
class Shot:
    """un plan: camera + stari (cu treceri), Ken Burns, particule, etichete. Timpi absoluti (secunde in reel)."""
    def __init__(s, cam, t0, t1, st='shut', seq=(), kb=None, fx=None, ov=None, tr=('xf', 0.3), wipe=None, spot=None, dim=None, grade=None, name='', shake=None, phase=None, pf=None):
        s.cam, s.t0, s.t1, s.st0, s.seq = cam, t0, t1, st, list(seq); s.shake = shake
        s.phase = phase          # None = pompa merge (o cursa pe secunda); False = sta; functie t -> faza in curse
        s.pf = pf                # functie (rgba premultiplicat, t) -> rgba: recolorarea lichidului din placa etc.
        s.kb = kb or [(t0, 1.0, 0.0, 0.0)]; s.fx, s.ov, s.tr, s.wipe, s.spot, s.dim, s.grade = fx, ov, tr, wipe, spot, dim, grade
        s.name = name or '%s:%s@%.1f' % (cam, st, t0)
    def layers(s, t):
        w = {s.st0: 1.0}
        for (st, ta, tb) in s.seq:
            e = float(seg(t, ta, tb))
            if e <= 0: break
            w = {k: v * (1 - e) for k, v in w.items()}; w[st] = w.get(st, 0.0) + e
        return w
    def ph(s, t):
        if s.phase is None: return t
        if s.phase is False: return None
        return s.phase(t) if callable(s.phase) else float(s.phase)
    def kbat(s, t):
        K = s.kb
        if len(K) == 1 or t <= K[0][0]: return K[0][1:]
        for a, b in zip(K[:-1], K[1:]):
            if t <= b[0]:
                e = float(ease((t - a[0]) / max(b[0] - a[0], 1e-6)))
                # zoom interpolat logaritmic
                z = math.exp(math.log(a[1]) + (math.log(b[1]) - math.log(a[1])) * e)
                return z, a[2] + (b[2] - a[2]) * e, a[3] + (b[3] - a[3]) * e
        return K[-1][1:]

class Ctx:
    """ce primesc functiile de particule si de etichete"""
    def __init__(s, ep, t, cam, shot, k):
        s.ep, s.t, s.cam, s.shot, s.k = ep, t, cam, shot, k
        s.ov = np.zeros((H, W, 4), np.float32); s.used = False
    def P(s, p):
        """punct 3D (mm) sau ('px', x, y) -> coordonate pe ecran"""
        if isinstance(p, tuple) and len(p) == 3 and p[0] == 'px': return float(p[1]) * s.k, float(p[2]) * s.k
        x, y, z = s.cam.proj(np.asarray(p, np.float64)[None, :]); return float(x[0]), float(y[0])

def edge_mask(m=80.0):
    key = ('em', W, H, m); e = _cache.get(key)
    if e is None:
        x = np.arange(W, dtype=np.float32); y = np.arange(H, dtype=np.float32); k = W / 1080.0
        mx = np.clip(np.minimum(x, W - 1 - x) / (m * k), 0, 1); my = np.clip(np.minimum(y, H - 1 - y) / (m * k), 0, 1)
        mx = mx * mx * (3 - 2 * mx); my = my * my * (3 - 2 * my)
        e = keep(key, (my[:, None] * mx[None, :]).astype(np.float32), cap=64)
    return e

def compose(ep, shot, t):
    """cadrul unui plan la momentul absolut t, RGB float"""
    k = W / 1080.0
    lay = shot.layers(t); rgba = None; zb = None; J = None; wmax = -1
    for st, w in lay.items():
        if w <= 0.002: continue
        p, z, Jp = plate(shot.cam, st)
        p = with_loop(shot.cam, st, p, shot.ph(t))
        rgba = p * w if rgba is None else rgba + p * w
        if w > wmax: wmax = w; zb = z; J = Jp
    wy = None
    if shot.wipe is not None:
        stB, ta, tb, soft = shot.wipe[:4]; wmode = shot.wipe[4] if len(shot.wipe) > 4 else 'down'
        rng = shot.wipe[5] if len(shot.wipe) > 5 else None
        e = float(seg(t, ta, tb))
        if wmode == 'down' and rng is None:         # stergere completa de sus in jos, cu linie luminoasa
            if 0 < e < 1:
                pB, zB, _ = plate(shot.cam, stB); pB = with_loop(shot.cam, stB, pB, shot.ph(t))
                y = np.arange(H, dtype=np.float32)[:, None, None]
                yb = -0.05 * H + e * 1.10 * H
                m = np.clip((yb - y) / (soft * k) + 0.5, 0, 1); wy = yb
                rgba = rgba * (1 - m) + pB * m; zb = np.where(m[..., 0] > 0.5, zB, zb)
            elif e >= 1:
                rgba, zb, J = plate(shot.cam, stB); rgba = with_loop(shot.cam, stB, rgba, shot.ph(t))
        elif e > 0 or rng is not None:
            # 'up': placa B urca de jos in sus (umplere); 'drop': placa B coboara de sus (nivelul scade). Linia merge de la y0 la y1 (px la 1080)
            # si ramane acolo; al saptelea element = functie t -> panta liniei (px pe px), pentru lichidul care fuge intr-o parte
            ya, yz = rng if rng is not None else ((1960, -40) if wmode == 'up' else (-40, 1960))
            sl = shot.wipe[6](t) if len(shot.wipe) > 6 and shot.wipe[6] is not None else 0.0
            pB, zB, _ = plate(shot.cam, stB); pB = with_loop(shot.cam, stB, pB, shot.ph(t))
            y = np.arange(H, dtype=np.float32)[:, None, None]
            yb = (ya + (yz - ya) * e) * k
            if sl: yb = yb + sl * (np.arange(W, dtype=np.float32)[None, :, None] - W / 2.0)
            m = np.clip((y - yb) / (soft * k) + 0.5, 0, 1) if wmode == 'up' else np.clip((yb - y) / (soft * k) + 0.5, 0, 1)
            rgba = rgba * (1 - m) + pB * m; zb = np.where(m[..., 0] > 0.5, zB, zb)
    if shot.grade is not None:
        g = shot.grade(t) if callable(shot.grade) else shot.grade
        if g is not None:
            gn, gm = g; al = np.maximum(rgba[..., 3:4], 1e-4)
            rgba = np.concatenate([np.clip(rgba[..., :3] / al, 0, 1) ** gm * gn * rgba[..., 3:4], rgba[..., 3:4]], -1)
    if shot.pf is not None: rgba = shot.pf(rgba, t)
    cam = X.Cam(J, W, H)
    zoom, dx, dy = shot.kbat(t)
    if shot.shake is not None:
        sx, sy = shot.shake(t); dx += sx; dy += sy
    dx *= k; dy *= k
    if zoom < 0.999:
        rgba = rgba * (1 - min((1 - zoom) / 0.04, 1.0) * (1 - edge_mask()))[..., None]
    if abs(zoom - 1) > 1e-5 or abs(dx) > 1e-3 or abs(dy) > 1e-3:
        cam.set2d(zoom, dx, dy); A = cam.affine()
        rgba = cv2.warpAffine(rgba, A, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
        zb = cv2.warpAffine(zb, A, (W, H), flags=cv2.INTER_NEAREST, borderMode=cv2.BORDER_CONSTANT, borderValue=1e6)
        if wy is not None: wy = zoom * (wy - H / 2) + H / 2 + dy
    C = Ctx(ep, t, cam, shot, k); C.zb = zb
    add = None
    if shot.fx is not None:
        cv = X.Canvas(W, H, zb); C.cv = cv
        for f in (shot.fx if isinstance(shot.fx, (list, tuple)) else [shot.fx]): f(C)
        out = cv.flush()
        if out['over'] is not None:
            c, a = out['over']
            rgba = np.concatenate([c + rgba[..., :3] * (1 - a[..., None]), (a + rgba[..., 3] * (1 - a))[..., None]], -1)
        add = out['add']
    bg = background(t)
    rgb = bg * (1 - rgba[..., 3:4]) + rgba[..., :3]
    if shot.spot is not None:
        sp = shot.spot(t, C)
        if sp is not None:
            sx, sy, sr, sa = sp
            if sa > 0.003:
                yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
                d = np.sqrt((xx - sx) ** 2 + (yy - sy) ** 2) / max(sr, 1.0)
                m = np.clip((d - 1.0) / 0.6, 0, 1); m = m * m * (3 - 2 * m)
                rgb = rgb * (1 - sa * 0.62 * m[..., None])
    if shot.dim is not None:
        d = shot.dim(t)
        if d > 0.003:
            bl = cv2.GaussianBlur(rgb, (0, 0), 9 * k)
            rgb = rgb * (1 - d) + (bl * 0.36 + bg * 0.12) * d
    if wy is not None:
        y = np.arange(H, dtype=np.float32); g = np.exp(-((y - wy) / (7.0 * k)) ** 2)[:, None, None] * 0.9 + np.exp(-((y - wy) / (40.0 * k)) ** 2)[:, None, None] * 0.25
        col = np.array([1.0, 0.82, 0.25], np.float32)
        add = g * col if add is None else add + g * col
    if add is not None:
        sm = cv2.resize(add, (W // 4, H // 4), interpolation=cv2.INTER_AREA)
        bloom = cv2.resize(cv2.GaussianBlur(sm, (0, 0), 5.0 * k), (W, H), interpolation=cv2.INTER_LINEAR)
        g = add + bloom * 0.5
        rgb = 1 - (1 - np.clip(rgb, 0, 1)) * (1 - np.clip(g, 0, 1))
    if shot.ov is not None:
        for f in (shot.ov if isinstance(shot.ov, (list, tuple)) else [shot.ov]): f(C)
        if C.used:
            a = C.ov[..., 3:4]; rgb = rgb * (1 - a) + C.ov[..., :3]
    shot._cam = cam
    return np.clip(rgb, 0, 1)

def compose_tr(ep, shot, t, zm=1.0, c=(540, 960)):
    """plan cu zoom suplimentar in jurul unui punct de pe ecran (pentru trecerea prin zoom)"""
    if abs(zm - 1) < 1e-4: return compose(ep, shot, t)
    z0, dx0, dy0 = shot.kbat(t)
    cx, cy = c
    # pozitia noua: x' = c + (x_kb - c) * zm ; x_kb = (x - W/2) * z0 + W/2 + dx0
    nz = z0 * zm; ndx = cx + (W / 2 / (W / 1080.0) + dx0 - cx) * zm - W / 2 / (W / 1080.0); ndy = cy + (H / 2 / (W / 1080.0) + dy0 - cy) * zm - H / 2 / (W / 1080.0)
    old = shot.kb; shot.kb = [(t, nz, ndx, ndy)]
    try: return compose(ep, shot, t)
    finally: shot.kb = old

def frame(ep, SH, t, glob=None):
    act = [s for s in SH if s.t0 <= t < s.t1]
    s = act[0] if act else (SH[-1] if t >= SH[-1].t0 else SH[0])
    i = SH.index(s); tr = s.tr or ('cut',)
    img = None
    if i > 0 and tr[0] != 'cut':
        d = tr[1]; u = t - s.t0
        if u < d:
            p = SH[i - 1]; e = float(ease(u / d))
            if tr[0] == 'xf':
                img = compose(ep, p, t) * (1 - e) + compose(ep, s, t) * e
            elif tr[0] == 'dive':
                cx, cy = tr[2]; zmax = tr[3] if len(tr) > 3 else 3.2
                A = compose_tr(ep, p, t, 1 + (zmax - 1) * e ** 1.6, (cx, cy))
                z2 = 1.0 if (len(tr) > 4 and tr[4] == 'full') else 0.42 + 0.58 * e          # 'full': planul nou sta pe tot cadrul (placi care ating marginile)
                B = compose_tr(ep, s, t, z2, (cx + (540 - cx) * e, cy + (960 - cy) * e))
                a = float(np.clip((e - 0.12) / 0.6, 0, 1)); a = a * a * (3 - 2 * a)
                img = A * (1 - a) + B * a
            elif tr[0] == 'flash':
                img = compose(ep, s, t); fl = math.exp(-u * 9.0) * 0.8
                img = img + (1 - img) * fl
    if img is None: img = compose(ep, s, t)
    if glob is not None: img = glob(t, img)
    return img

# ------------------------------------------------------------------ iesire
def to8(img): return cv2.cvtColor((np.clip(img, 0, 1) * 255 + 0.5).astype(np.uint8), cv2.COLOR_RGB2BGR)

def guides(im):
    s = im.shape[1] / 1080.0
    for y, c in ((196, (0, 255, 0)), (350, (0, 255, 0)), (940, (0, 255, 0)), (1280, (0, 255, 255)), (1290, (0, 200, 255)), (1530, (0, 200, 255))):
        cv2.line(im, (0, int(y * s)), (im.shape[1], int(y * s)), c, 2)
    for x in range(120, 1080, 120):
        cv2.line(im, (int(x * s), 0), (int(x * s), im.shape[0]), (90, 90, 90), 1)
    for y in range(120, 1920, 120):
        cv2.line(im, (0, int(y * s)), (im.shape[1], int(y * s)), (90, 90, 90), 1); cv2.putText(im, str(y), (4, int(y * s) - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
    return im

JPG = [cv2.IMWRITE_JPEG_QUALITY, 93]
if hasattr(cv2, 'IMWRITE_JPEG_SAMPLING_FACTOR'): JPG += [cv2.IMWRITE_JPEG_SAMPLING_FACTOR, cv2.IMWRITE_JPEG_SAMPLING_FACTOR_444]

def main():
    global W, H
    ap = argparse.ArgumentParser()
    ap.add_argument('ep'); ap.add_argument('--t', type=float, nargs='*'); ap.add_argument('--range', type=int, nargs=2)
    ap.add_argument('--out', default=None); ap.add_argument('--sheet', type=int, default=0)
    ap.add_argument('--guides', action='store_true'); ap.add_argument('--part', type=int, nargs=2, default=None)
    ap.add_argument('--scale', type=float, default=1.0); ap.add_argument('--frames', type=int, nargs='*', default=None)
    a = ap.parse_args()
    W = int(1080 * a.scale); H = int(1920 * a.scale)
    st = importlib.import_module('st_' + a.ep)
    SH, glob = st.SHOTS, getattr(st, 'GLOB', None)
    if a.t is not None:
        ims = []
        for t in a.t:
            t0 = time.time(); f = int(round(t * FPS)); im = to8(frame(a.ep, SH, f / FPS, glob))
            if a.guides: im = guides(im)
            if a.sheet: cv2.putText(im, '%.2f' % t, (int(860 * a.scale), im.shape[0] - int(40 * a.scale)), cv2.FONT_HERSHEY_SIMPLEX, 1.6 * a.scale, (255, 255, 255), max(1, int(3 * a.scale)))
            ims.append(im); print('t=%.2f %.2fs' % (t, time.time() - t0), flush=True)
        out = a.out or os.path.join(HERE, 'proba_%s.jpg' % a.ep)
        if a.sheet:
            rows = [np.concatenate(ims[i:i + a.sheet] + [np.zeros_like(ims[0])] * (a.sheet - len(ims[i:i + a.sheet])), 1) for i in range(0, len(ims), a.sheet)]
            sh = np.concatenate(rows, 0); sc = min(1.0, 2400.0 / sh.shape[1])
            if sc < 1: sh = cv2.resize(sh, (int(sh.shape[1] * sc), int(sh.shape[0] * sc)), interpolation=cv2.INTER_AREA)
            cv2.imwrite(out, sh, [cv2.IMWRITE_JPEG_QUALITY, 90])
        else:
            for t, im in zip(a.t, ims): cv2.imwrite(out if len(ims) == 1 else out.replace('.jpg', '_%06.2f.jpg' % t), im, JPG)
        sys.exit()
    NF = int(round(st.TOTAL * FPS))
    f0, f1 = a.range if a.range else (0, NF)
    fr = a.frames if a.frames else list(range(f0, f1))
    if a.part: fr = [f for f in fr if f % a.part[1] == a.part[0]]
    out = a.out; os.makedirs(out, exist_ok=True); ts = time.time(); done = 0
    for f in fr:
        p = os.path.join(out, '%05d.jpg' % f)
        if os.path.exists(p): continue
        im = frame(a.ep, SH, f / FPS, glob)
        cv2.imwrite(p + '.tmp.jpg', to8(im), JPG); os.replace(p + '.tmp.jpg', p); done += 1
        if done % 50 == 0: print('cadru %d  (%d facute)  %.2f s/cadru' % (f, done, (time.time() - ts) / done), flush=True)
    print('gata', done, flush=True)

if __name__ == '__main__':
    import icomp as _M
    _M.main()
