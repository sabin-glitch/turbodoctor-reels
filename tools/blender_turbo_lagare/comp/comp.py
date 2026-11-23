"""Compositor: Turbo Doctor turbo bearing animations (skia + numpy), from the Blender layers in ../out.

  FMT=V|H VAR=A|B python3 comp.py --png 5,12,20        -> proof/<VAR><FMT>_<t>.png
  FMT=V|H VAR=A|B python3 comp.py --out x.mp4 [--frames a b] [--clean]
World space of the main scene = pixels of the T1 plate (2160 x 2160) of the main camera.
"""
import sys, os, json, math, subprocess, functools
import numpy as np, skia, cv2
from fk import *

HERE = os.path.dirname(os.path.abspath(__file__))
OUTD = os.path.join(HERE, '..', 'out')
INFO = json.load(open(os.path.join(OUTD, 'info.json')))
CROPS = INFO['crops']; S1 = INFO['base']
FMT = os.environ.get('FMT', 'V'); VAR = os.environ.get('VAR', 'A')
CLEAN = os.environ.get('CLEAN', '0') == '1'
W, H = (1080, 1920) if FMT == 'V' else (1920, 1080)
FPS = 30
DUR = 51.0
Y, WHT, BG = '#ffc21a', '#ffffff', '#0a1220'
C_OIL, C_OIL_HI, C_OIL_DK = '#f0b43a', '#ffe08a', '#c98a12'
C_AIR, C_GAS = '#6ec6ff', '#ff7a30'
SAMP = skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear)

# ------------------------------------------------------------------ camera projection (main)
_M = np.array(INFO['M']); _LENS = INFO['lens']; _SEN = INFO['sensor']
_MI = np.linalg.inv(_M)


def proj(p):
    """3D (mm) -> world px (T1 plate)."""
    q = _M @ np.array([p[0], p[1], p[2], 1.0])
    k = _LENS / _SEN
    return (0.5 + k * q[0] / -q[2]) * S1, (0.5 - k * q[1] / -q[2]) * S1


def projs(pts): return [proj(p) for p in pts]


def unproject_plane_y0(X, Yp):
    """world px arrays -> (x, z) on the plane y = 0."""
    k = _LENS / _SEN
    xn = X / S1 - 0.5; yn = 0.5 - Yp / S1
    d = np.stack([xn / k, yn / k, -np.ones_like(xn)], -1)          # camera space
    R = _MI[:3, :3]; o = _MI[:3, 3]
    dw = d @ R.T
    t = -o[1] / dw[..., 1]
    P = o + dw * t[..., None]
    return P[..., 0], P[..., 2]


# ------------------------------------------------------------------ images
def _read(name):
    p = os.path.join(OUTD, name + '.png')
    if not os.path.exists(p): return None
    a = cv2.imread(p, cv2.IMREAD_UNCHANGED)
    if a is None: return None
    if a.dtype == np.uint16: a = ((a.astype(np.float32) + 128.0) / 257.0).astype(np.uint8)
    if a.shape[2] == 3: a = np.dstack([a, np.full(a.shape[:2], 255, np.uint8)])
    return cv2.cvtColor(a, cv2.COLOR_BGRA2RGBA)


def _sk(a):
    return skia.Image.fromarray(np.ascontiguousarray(a), colorType=skia.kRGBA_8888_ColorType, alphaType=skia.kUnpremul_AlphaType).withDefaultMipmaps()


def feather(a, F=36, excl=None):
    h, w = a.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    f = np.clip(np.minimum.reduce([xx, yy, w - 1 - xx, h - 1 - yy]) / F, 0, 1)
    f = f * f * (3 - 2 * f)
    if excl is not None: f = f * (1 - excl)
    b = a.copy(); b[..., 3] = (b[..., 3].astype(np.float32) * f).astype(np.uint8)
    return b


_IM = {}


def img(name, fe=None, excl=None):
    k = (name, fe, excl is not None)
    if k not in _IM:
        a = _read(name)
        if a is None: _IM[k] = None
        else:
            if fe: a = feather(a, fe, excl(a.shape, name) if excl else None)
            _IM[k] = _sk(a)
    return _IM[k]


def bearing_excl(shape, name):
    """mask (in a T2-density loop image) of the CHRA bore region, where variant-specific parts live."""
    h, w = shape[:2]; x0, y0 = CROPS['LC' if name.startswith('LC') else 'LT'][:2]
    pts = []
    for x in (-23.5, 23.5):
        for yy in (-9.5, 9.5):
            for z in (-9.5, 9.5): pts.append(proj((x, yy, z)))
    pts = np.array(pts) * 2 - np.array([x0, y0])
    hull = cv2.convexHull(pts.astype(np.float32)).astype(np.int32)
    m = np.zeros((h, w), np.uint8); cv2.fillConvexPoly(m, hull, 255)
    m = cv2.GaussianBlur(m, (0, 0), 6).astype(np.float32) / 255
    return m


# ------------------------------------------------------------------ oil masks with reveal maps
TIERS = {'T1': (1, [0, 0]), 'T2': (2, CROPS['T2'][:2]), 'T3': (4, CROPS['T3'][:2])}
GZ = 12.5; FX = 16.0
# oil feed route on the section plane (x, z): feed pipe from the engine -> banjo eye -> cross hole -> hollow banjo bolt -> CHRA bore
PIPE_X, PIPE_TOP, BJ_Z = -22.0, 74.0, 36.9
FEED_ROUTE = [(PIPE_X, PIPE_TOP), (PIPE_X, BJ_Z + 6.0)] + \
             [(-16.0 - 6.0 * math.cos(math.radians(a)), BJ_Z + 6.0 - 6.0 * math.sin(math.radians(a))) for a in range(9, 91, 9)] + \
             [(-5.0, BJ_Z), (0.0, BJ_Z), (0.0, 19.3), (0.0, GZ)]


def _route_s(route):
    s = [0.0]
    for (x0, z0), (x1, z1) in zip(route, route[1:]): s.append(s[-1] + math.hypot(x1 - x0, z1 - z0))
    return s


_RS = _route_s(FEED_ROUTE)
S_GAL = _RS[-1]                                   # path length to the gallery
S_C = _RS[FEED_ROUTE.index((0.0, BJ_Z))]          # ... to the middle of the banjo bolt


def route_arrival(x, z, route, s0, k=0.6):
    best = np.full(x.shape, 1e9, np.float32); s = _route_s(route)
    for (x0, z0), (x1, z1), sa in zip(route, route[1:], s):
        dx, dz = x1 - x0, z1 - z0; L2 = dx * dx + dz * dz
        t = np.clip(((x - x0) * dx + (z - z0) * dz) / max(L2, 1e-9), 0, 1)
        d = np.hypot(x - (x0 + t * dx), z - (z0 + t * dz))
        best = np.minimum(best, s0 + sa + t * math.sqrt(L2) + k * d)
    return best


def arrival(x, z, zone):
    """path length (mm) the oil travels from the feed pipe to the point (x, z) on the section plane."""
    a = np.full(x.shape, 1e9, np.float32)
    if zone in ('feed', 'thrust', 'holes'):
        up = z > GZ + 2.6
        r = np.minimum(route_arrival(x, z, FEED_ROUTE, 0.0), route_arrival(x, z, [(0.0, BJ_Z), (5.0, BJ_Z), (7.4, BJ_Z)], S_C))
        a = np.where(up, r, a)
        gal = (np.abs(z - GZ) <= 2.6)
        a = np.where(gal, S_GAL + np.abs(x), a)
        rest = ~(up | gal)
        drop = np.where(x < -22, 27.4, FX)
        a = np.where(rest, S_GAL + drop + np.maximum(0, GZ - z), a)
        if zone == 'holes': a = a + 2.0
    elif zone == 'outer':
        a = S_GAL + FX + (GZ - 6.5) + np.abs(np.abs(x) - FX) * 1.4 + np.where(z < 0, 14.0, 0.0)
    elif zone == 'inner':
        a = S_GAL + FX + (GZ - 6.5) + 8.0 + np.abs(np.abs(x) - FX) * 1.4 + np.where(z < 0, 10.0, 0.0)
    return a


class OilLayer:
    """one zone at one tier: base white mask (alpha) + arrival map (mm)."""
    def __init__(self, tier, zone):
        self.ok = False
        var = VAR; job = 'rgb' if zone in ('feed', 'outer', 'inner') else 'th'
        a = _read(f'oil{var}_{tier}_{job}')
        if a is None: return
        ch = {'feed': 0, 'outer': 1, 'inner': 2, 'thrust': 0, 'holes': 1}[zone]
        m = (a[..., 3].astype(np.float32) / 255) * (a[..., ch].astype(np.float32) / 255)
        if m.max() < 0.05: return
        k, (x0, y0) = TIERS[tier]
        ys, xs = np.nonzero(m > 0.01)
        self.ys, self.xs = ys, xs
        self.m = m[ys, xs]
        wx = (xs + x0) / k; wy = (ys + y0) / k
        X, Z = unproject_plane_y0(wx, wy)
        self.arr = arrival(X, Z, zone).astype(np.float32)
        self.shape = m.shape; self.k = k; self.off = (x0, y0); self.ok = True
        self.full = self._mk(np.ones_like(self.m))

    def _mk(self, f):
        a = np.zeros(self.shape + (4,), np.uint8); a[..., :3] = 255
        a[self.ys, self.xs, 3] = np.clip(self.m * f * 255, 0, 255).astype(np.uint8)
        return _sk(a)

    @functools.lru_cache(maxsize=48)
    def at(self, front_q):
        if front_q >= 9999: return self.full
        f = np.clip((front_q - self.arr) / 3.0, 0, 1)
        return self._mk(f)


_OIL = {}


def oil(tier, zone):
    k = (tier, zone)
    if k not in _OIL:
        o = OilLayer(tier, zone); _OIL[k] = o if o.ok else None
    return _OIL[k]


# ------------------------------------------------------------------ timeline
TL = {
    'A': dict(open0=3.2, open1=5.0, wide1=11.6, chra0=13.4, chra1=21.0, brg0=22.8, brg1=30.8, tr0=32.2, tr1=41.0, back1=42.6, end0=47.6),
    'B': dict(open0=3.2, open1=5.0, wide1=11.6, chra0=13.4, chra1=21.0, brg0=22.8, brg1=30.8, tr0=32.2, trp0=36.6, trp1=37.4, tr1=41.0, back1=42.6, end0=47.6),
}[VAR]
OIL_T0 = TL['chra0'] + 0.3          # oil starts to arrive
OIL_SPEED = 48.0                    # mm of path per second while filling


def oil_front(t):
    if t < OIL_T0: return -10.0
    d = (t - OIL_T0) * OIL_SPEED
    return 9999.0 if d > 175 else d


def omega(t):
    """rotor speed, deg/s (visual)"""
    return 180.0 * ramp(t, TL['open1'] - 0.3, 1.6)


_TT = np.arange(0, DUR + 2, 1 / FPS)
_ANG = np.concatenate([[0], np.cumsum([omega(x) / FPS for x in _TT[:-1]])])


def rotor_angle(t):
    i = min(len(_TT) - 1, max(0, int(round(t * FPS)))); return float(_ANG[i])


# ---------------- views
def fit_view(pts3, rect):
    q = np.array(projs(pts3)); x0, y0 = q.min(0); x1, y1 = q.max(0)
    sx0, sy0, sx1, sy1 = rect
    z = min((sx1 - sx0) / (x1 - x0), (sy1 - sy0) / (y1 - y0))
    cx = (x0 + x1) / 2 - ((sx0 + sx1) / 2 - W / 2) / z
    cy = (y0 + y1) / 2 - ((sy0 + sy1) / 2 - H / 2) / z
    return z, cx, cy


def box3(x0, x1, z0, z1, y0=0.0, y1=0.0):
    return [(x, y, z) for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)]


def alpha_bbox(names, thr=8):
    box = None
    for nm in names:
        a = _read(nm)
        if a is None: continue
        ys, xs = np.nonzero(a[..., 3] > thr)
        b = [xs.min(), ys.min(), xs.max(), ys.max()]
        box = b if box is None else [min(box[0], b[0]), min(box[1], b[1]), max(box[2], b[2]), max(box[3], b[3])]
    return box


def fit_px(b, rect):
    x0, y0, x1, y1 = b; sx0, sy0, sx1, sy1 = rect
    z = min((sx1 - sx0) / (x1 - x0), (sy1 - sy0) / (y1 - y0))
    return z, (x0 + x1) / 2 - ((sx0 + sx1) / 2 - W / 2) / z, (y0 + y1) / 2 - ((sy0 + sy1) / 2 - H / 2) / z


_BB = os.path.join(OUTD, 'bbox.json')
if os.path.exists(_BB): BBX = json.load(open(_BB))
else:
    BBX = {'sec': [int(v) for v in alpha_bbox(['T1_A'])], 'ext': [int(v) for v in alpha_bbox(['T1_A', 'T1_front'])]}
    json.dump(BBX, open(_BB, 'w'))
if FMT == 'V':
    V_WIDE = fit_px(BBX['sec'], (40, 500, 1040, 1420))
    V_EXT = fit_px(BBX['ext'], (60, 470, 1020, 1430))
    V_CHRA = fit_view(box3(-42, 40, -44, 46, 0, 12), (40, 330, 1040, 1470))
    V_BRG = fit_view(box3(-3.5, 25.5, -10, 12) if VAR == 'A' else box3(-3.5, 24.5, -12, 11), (20, 420, 1060, 1440))
else:
    V_WIDE = fit_px(BBX['sec'], (120, 220, 1150, 990))
    V_EXT = fit_px(BBX['ext'], (150, 200, 1210, 1010))
    V_CHRA = fit_view(box3(-42, 40, -44, 46, 0, 12), (60, 80, 1270, 1010))
    V_BRG = fit_view(box3(-31.5, 25.5, -11, 12), (50, 150, 1280, 960))


def interp_view(a, b, f):
    z = math.exp(lerp(math.log(a[0]), math.log(b[0]), f))
    g = (math.log(z) - math.log(a[0])) / (math.log(b[0]) - math.log(a[0])) if abs(b[0] - a[0]) > 1e-6 else f
    return z, lerp(a[1], b[1], g), lerp(a[2], b[2], g)


def main_view(t):
    T = TL
    K = [(0.0, V_EXT), (T['open0'], (V_EXT[0] * 1.03, V_EXT[1], V_EXT[2])), (T['open1'], V_WIDE), (T['wide1'], V_WIDE),
         (T['chra0'], V_CHRA), (T['chra1'], V_CHRA), (T['brg0'], V_BRG), (T['brg1'], V_BRG),
         (T['tr0'], (V_BRG[0] * 1.25, V_BRG[1], V_BRG[2])), (T['tr1'], (V_BRG[0] * 1.25, V_BRG[1], V_BRG[2])), (T['back1'], V_WIDE), (DUR, V_WIDE)]
    if t <= K[0][0]: return K[0][1]
    for (t0, a), (t1, b) in zip(K, K[1:]):
        if t <= t1:
            return interp_view(a, b, eio((t - t0) / max(1e-6, t1 - t0)))
    return K[-1][1]


def scene_alpha(t):
    """(main alpha, transverse alpha)"""
    a_tr = ramp(t, TL['brg1'] + 0.1, TL['tr0'] - TL['brg1'] - 0.1) * (1 - ramp(t, TL['tr1'], TL['back1'] - TL['tr1'] - 0.4))
    return 1.0 - a_tr, a_tr


# ------------------------------------------------------------------ drawing: main scene
def draw_img(c, name, s, x, y, alpha=1.0, fe=None, excl=None, cf=None, blend=None):
    im = img(name, fe, excl)
    if im is None or alpha <= 0.003: return
    p = skia.Paint(); p.setAlphaf(min(1.0, alpha))
    if cf is not None: p.setColorFilter(cf)
    if blend is not None: p.setBlendMode(blend)
    c.save(); c.translate(x, y); c.scale(s, s); c.drawImage(im, 0, 0, SAMP, p); c.restore()


def tint(col, gain=1.0):
    r, g, b = hexc(col) if isinstance(col, str) else col
    return skia.ColorFilters.Matrix([r * gain, 0, 0, 0, 0, 0, g * gain, 0, 0, 0, 0, 0, b * gain, 0, 0, 0, 0, 0, 1, 0])


ROT_STEP = 6.0


def loop_frame(prefix, n, period_deg, ang):
    k = int(math.floor((ang % period_deg) / ROT_STEP + 1e-6)) % n
    return f'{prefix}_{k:02d}'


def draw_main(c, t, V, alpha):
    if alpha <= 0.003: return
    z, cx, cy = V
    c.saveLayerAlpha(None, int(alpha * 255))
    c.save(); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-cx, -cy)
    # plates
    draw_img(c, 'T1_A', 1.0, 0, 0)
    x0, y0 = CROPS['T2'][:2]; draw_img(c, f'T2_{VAR}', 0.5, x0 / 2, y0 / 2, fe=40)
    ang = rotor_angle(t)
    if omega(t) > 0.5 or ang > 0.5:
        for key, n, per in (('LC', 10, 60.0), ('LT', 6, 36.0)):
            nm = loop_frame(key, n, per, ang)
            x0, y0 = CROPS[key][:2]
            draw_img(c, nm, 0.5, x0 / 2, y0 / 2, fe=22, excl=bearing_excl)
    if z > 1.1:
        x0, y0 = CROPS['T3'][:2]; draw_img(c, f'T3_{VAR}', 0.25, x0 / 4, y0 / 4, alpha=ramp(z, 1.1, 0.6), fe=60)
    # oil
    draw_oil(c, t, z)
    # front halves (cutaway reveal)
    rv = ramp(t, TL['open0'], TL['open1'] - TL['open0'])
    if rv < 0.999:
        k = eio(rv); ax, ay = proj((-6.0, -40.0, 10.0))
        c.save(); c.translate(ax - 420 * k, ay - 260 * k); c.scale(1 + 0.6 * k, 1 + 0.6 * k); c.translate(-ax, -ay)
        draw_img(c, 'T1_front', 1.0, 0, 0, alpha=1 - sm(rv * 1.1))
        c.restore()
    # particles in world space
    flows(c, t, z)
    c.restore()
    c.restore()


def draw_oil(c, t, z):
    fr = oil_front(t)
    if fr < 0: return
    fq = 9999.0 if fr >= 9999 else round(fr * 2) / 2
    # pick the tier for the current zoom (crossfade)
    w2 = ramp(z, 0.55, 0.25); w3 = ramp(z, 1.25, 0.45)
    zones = [('feed', '#f6b23c', 0.84), ('thrust', '#f0a830', 0.9), ('outer', '#f0b43a', 0.95), ('inner', '#ffd060', 0.95)] + ([('holes', '#f0b43a', 0.95)] if VAR == 'B' else [])
    for tier, a_t in (('T1', 1 - w2), ('T2', w2 * (1 - w3)), ('T3', w3)):
        if a_t <= 0.01: continue
        k, (x0, y0) = TIERS[tier]
        for zone, col, op in zones:
            L = oil(tier, zone)
            if L is None: continue
            im = L.at(fq)
            p = skia.Paint(); p.setAlphaf(op * a_t); p.setColorFilter(tint(col, 1.0))
            c.save(); c.translate(x0 / k, y0 / k); c.scale(1 / k, 1 / k); c.drawImage(im, 0, 0, SAMP, p); c.restore()


# ---------------- flows (3D polylines projected to world px)
def c_mid(s, t):
    hx, hr = (-66.0 + 25.5 * math.sin(t * PI / 2), 25.0 - 19.0 * math.cos(t * PI / 2))
    sx, sr = (-66.0 + 21.5 * math.sin(t * PI / 2), 25.0 - 7.0 * math.cos(t * PI / 2))
    return hx + (sx - hx) * s, hr + (sr - hr) * s


def t_mid(s, t):
    hx, hr = (66.0 - 27.4 * math.cos(t * PI / 2), 21.5 - 15.0 * math.sin(t * PI / 2))
    sx, sr = (66.0 - 20.5 * math.cos(t * PI / 2), 21.5 - 3.0 * math.sin(t * PI / 2))
    return hx + (sx - hx) * s, hr + (sr - hr) * s


PI = math.pi


def comp_volute_pt(phi):          # same as turbo.py cvol(), turned by C_ROT = +90 deg (scroll end at the top)
    r = 4.0 + 9.5 * (min(max(phi, 0), 360.0) / 360.0) ** 0.9; a = math.radians(phi + 90.0)
    Rc = 40.0 + 0.8 * r; xv = -40.0 - r
    return (xv, Rc * math.cos(a), Rc * math.sin(a))


def turb_volute_pt(phi):          # same as turbo.py tvol(), turned by T_ROT = -90 deg (inlet at the bottom)
    r = 13.0 - 10.0 * (max(phi, 0) / 340.0) ** 0.85; a = math.radians(phi - 90.0)
    Rc = 36.0 + 0.9 * r; xv = 43.0 + 0.6 * r
    return (xv, Rc * math.cos(a), Rc * math.sin(a))


def build_paths():
    P = {}
    for i, s in enumerate((0.2, 0.5, 0.8)):
        for sg in (1, -1):
            pts = [(-118.0, 0.0, sg * (6 + 12 * s * 0.9)), (-80.0, 0.0, sg * (6 + 12 * s * 0.9))]
            for k in range(13):
                tt = k / 12; x, r = c_mid(s, tt); pts.append((x, 0.0, sg * r))
            pts += [(-42.0 - 1.4 * s, 0.0, sg * 31.0), (-42.5 - 2 * s, 0.0, sg * 38.0)]
            if sg < 0:
                pts += [comp_volute_pt(phi) for phi in range(180, 271, 6)]
            else:
                pts += [(-48.0 - 2.0 * s, 0.0, 45.5), (-53.0, -3.0, 50.5), (-53.5, -9.0, 52.0)]
            P[f'air{i}{"t" if sg > 0 else "b"}'] = pts
    for i, s in enumerate((0.25, 0.55, 0.85)):
        for sg in (1, -1):
            if sg > 0: pts = [turb_volute_pt(phi) for phi in range(90, 181, 6)]
            else: pts = [(51.5, -34.0, -64.0), (51.0, -16.0, -52.0), turb_volute_pt(0)]
            pts += [(42.5 + 3 * s, 0.0, sg * 31.0), (41.5 + 4 * s, 0.0, sg * 23.0)]
            for k in range(13):
                tt = k / 12; x, r = t_mid(s, tt); pts.append((x, 0.0, sg * r))
            pts += [(80.0, 0.0, sg * (6.5 + 11 * s)), (100.0, 0.0, sg * (6.5 + 12.5 * s)), (112.0, 0.0, sg * (6.5 + 13 * s))]
            P[f'gas{i}{"t" if sg > 0 else "b"}'] = pts
    # oil
    P['o_pipe'] = [(x, 0.0, z) for (x, z) in FEED_ROUTE]
    P['o_gal_t'] = [(0.0, 0.0, GZ), (FX, 0.0, GZ), (FX, 0.0, 6.9 if VAR == 'A' else 6.4)]
    P['o_gal_c'] = [(0.0, 0.0, GZ), (-FX, 0.0, GZ), (-FX, 0.0, 6.9 if VAR == 'A' else 6.4)]
    P['o_gal_th'] = [(-FX, 0.0, GZ), (-27.4, 0.0, GZ), (-27.4, 0.0, 5.0)]
    ro = 6.65 if VAR == 'A' else 6.5
    for sx, nm in ((1, 't'), (-1, 'c')):
        for zs in (1, -1):
            P[f'o_out_{nm}{zs}a'] = [(sx * FX, 0.0, zs * ro), (sx * 21.0, 0.0, zs * ro)]
            P[f'o_out_{nm}{zs}b'] = [(sx * FX, 0.0, zs * ro), (sx * 11.0, 0.0, zs * ro)]
            P[f'o_in_{nm}{zs}a'] = [(sx * FX, 0.0, zs * 4.2), (sx * 21.2, 0.0, zs * 4.2)]
            P[f'o_in_{nm}{zs}b'] = [(sx * FX, 0.0, zs * 4.2), (sx * 10.8, 0.0, zs * 4.2)]
    # drips to the drain
    if VAR == 'A':
        P['o_drain0'] = [(0.0, 0.0, -9.0), (0.0, 0.0, -66.0)]
    else:
        P['o_drain0'] = [(7.0, 0.0, -7.0), (7.0, 0.0, -27.0), (3.0, 0.0, -34.0), (1.0, 0.0, -66.0)]
        P['o_drain3'] = [(-7.0, 0.0, -7.0), (-7.0, 0.0, -27.0), (-3.0, 0.0, -34.0), (-1.0, 0.0, -66.0)]
    P['o_drain1'] = [(22.5, 0.0, -9.0), (21.0, 0.0, -26.0), (11.0, 0.0, -28.5), (5.0, 0.0, -34.0), (2.0, 0.0, -66.0)]
    P['o_drain2'] = [(-24.0, 0.0, -9.0), (-22.0, 0.0, -26.0), (-11.0, 0.0, -28.5), (-5.0, 0.0, -34.0), (-2.0, 0.0, -66.0)]
    return {k: Poly(projs(v)) for k, v in P.items()}


PATHS = build_paths()


def flow_dots(c, key, t, speed, spacing, col, a, r, z, glow=True, jit=0.0, fade_end=True, accel=False, streak=1.0):
    """particles as short motion streaks; r = half width in screen px, streak = length in multiples of the spacing"""
    if a <= 0.01: return
    poly = PATHS[key]; L = poly.L
    if L < 1: return
    n = int(L // spacing) + 2
    off = (t * speed) % spacing
    s = off + np.arange(n) * spacing
    s = s[s < L]
    if accel: s = L * (s / L) ** 1.7
    xy, d = poly.at(s)
    xy2, _ = poly.at(np.maximum(0, s - spacing * 0.55 * streak))
    fa = np.clip(np.minimum(s / (1.5 * spacing), (L - s) / (1.5 * spacing)), 0, 1) if fade_end else np.ones(len(s))
    w = r / z
    pg = P(col, 1.0, stroke=w * 3.2); pc = P(col, 1.0, stroke=w * 1.5); pw = P('#ffffff', 1.0, stroke=w * 0.6)
    for (px, py), (qx, qy), f in zip(xy, xy2, fa):
        aa = a * f
        if aa < 0.02: continue
        if glow: pg.setAlphaf(aa * 0.20); c.drawLine(float(qx), float(qy), float(px), float(py), pg)
        pc.setAlphaf(aa); c.drawLine(float(qx), float(qy), float(px), float(py), pc)
        pw.setAlphaf(aa * 0.75); c.drawLine(float((qx + px) / 2), float((qy + py) / 2), float(px), float(py), pw)


def flows(c, t, z):
    T = TL
    a_gas = win(t, T['open1'] - 0.4, T['chra0'] - 0.6, 0.8, 0.8) + win(t, T['back1'] - 0.6, DUR, 0.8, 0.5)
    a_gas = min(1.0, a_gas)
    sp = 0.9 + 0.1 * (omega(t) / 180.0)
    if a_gas > 0.01:
        for k in PATHS:
            if k.startswith('air'):
                flow_dots(c, k, t + h01(sum(map(ord, k)) % 97) * 3, 300 * sp, 40, C_AIR, a_gas * 0.9, 2.6, z)
            elif k.startswith('gas'):
                flow_dots(c, k, t + h01(sum(map(ord, k)) % 89) * 3, 340 * sp, 42, C_GAS, a_gas * 0.9, 2.6, z)
    fr = oil_front(t)
    if fr >= 9999 or fr > 120:
        a_oil = ramp(t, OIL_T0 + 2.6, 0.8) * (1 - 0.45 * ramp(t, T['back1'] - 0.5, 0.5))
        rr = 1.7 if z > 1.5 else 2.0
        for k in ('o_pipe', 'o_gal_t', 'o_gal_c', 'o_gal_th'):
            flow_dots(c, k, t, 90, 30, '#fff0b0', a_oil, rr, z, glow=True)
        for k in PATHS:
            if k.startswith('o_out') or k.startswith('o_in'):
                flow_dots(c, k, t + (0.13 if 'in' in k else 0), 26 if 'out' in k else 34, 9, '#fff0b0', a_oil * 0.95, rr * 0.8, z, glow=False, streak=0.8)
        for i, k in enumerate([k for k in PATHS if k.startswith('o_drain')]):
            flow_dots(c, k, t + i * 0.37, 70, 34, C_OIL, a_oil * 0.9, rr * 1.6, z, accel=True, streak=0.6)


# ------------------------------------------------------------------ transverse scene
TR = {'A': [('trA', 0.0, 99.0)], 'B': [('trB', 0.0, TL.get('trp0', 99) + 0.4), ('trP', TL.get('trp0', 99), 99.0)]}[VAR]


def tr_info(nm):
    return INFO['trA' if nm in ('trA', 'trB') else 'trP']


def draw_tr(c, t, alpha):
    if alpha <= 0.003: return
    CX, CY, R = TR_GEOM[FMT]
    for nm, ta, tb in TR:
        a_sub = alpha
        if VAR == 'B':
            if nm == 'trB': a_sub *= 1 - ramp(t, TL['trp0'], TL['trp1'] - TL['trp0'])
            else: a_sub *= ramp(t, TL['trp0'], TL['trp1'] - TL['trp0'])
        if a_sub <= 0.003: continue
        inf = tr_info(nm); ppm = inf['px_per_mm'] / 10.0; ccx, ccy = inf['center'][:2]
        zoom = R / (12.0 * abs(ppm))
        c.saveLayerAlpha(None, int(a_sub * 255))
        # disc background + clip
        c.drawCircle(CX, CY, R + 14, P('#05080e', 0.92))
        pa = skia.Path(); pa.addCircle(CX, CY, R)
        c.save(); c.clipPath(pa, doAntiAlias=True)
        c.translate(CX, CY); c.scale(zoom, zoom); c.translate(-ccx, -ccy)
        draw_img(c, f'{nm}_static', 1.0, 0, 0)
        ws = math.radians(1.0)
        ang_s = tr_angle(t)                      # shaft angle (deg, clockwise on screen)
        ang_b = ang_s * 0.5 if nm == 'trA' else 0.0
        for zone, col in (('feed', C_OIL_HI), ('outer', C_OIL), ('inner', '#ffcf55')):
            draw_img(c, f'{nm}_oil_{zone}', 1.0, 0, 0, alpha=0.93, cf=tint(col))
        pp = abs(ppm)
        if nm == 'trA':
            c.save(); c.translate(ccx, ccy); c.rotate(ang_b); c.translate(-ccx, -ccy)
            ring_ = skia.Path(); ring_.addCircle(ccx, ccy, 6.27 * pp); ring_.addCircle(ccx, ccy, 4.38 * pp)
            ring_.setFillType(skia.PathFillType.kEvenOdd)
            c.save(); c.clipPath(ring_, doAntiAlias=True)
            draw_img(c, 'trA_bush', 1.0, 0, 0)
            draw_img(c, 'trA_oil_holes', 1.0, 0, 0, alpha=0.95, cf=tint(C_OIL))
            c.restore()
            c.restore()
        elif nm == 'trB':
            draw_img(c, 'trB_oil_holes', 1.0, 0, 0, alpha=0.95, cf=tint(C_OIL))
        c.save(); c.translate(ccx, ccy); c.rotate(ang_s); c.translate(-ccx, -ccy)
        disc = skia.Path(); disc.addCircle(ccx, ccy, 3.99 * pp)
        c.clipPath(disc, doAntiAlias=True)
        draw_img(c, f'{nm}_shaft', 1.0, 0, 0)
        c.restore()
        # film particles (in plate px)
        film_particles(c, t, nm, ccx, ccy, abs(ppm), zoom, ang_s, ang_b)
        c.restore()
        # rim
        c.drawCircle(CX, CY, R, P('#ffffff', 0.55, stroke=3.0))
        c.drawCircle(CX, CY, R + 7, P(Y, 0.35, stroke=2.0))
        c.restore()
        tr_overlays(c, t, nm, CX, CY, R, a_sub, inf, zoom)


def tr_angle(t):
    return (t - TL['brg1']) * 110.0        # deg, shaft


def film_particles(c, t, nm, ccx, ccy, ppm, zoom, ang_s, ang_b):
    if nm == 'trP':
        rings = [(4.7, 0.5, 26), (6.38, 0.02, 30)]
    elif nm == 'trA':
        rings = [(4.2, 0.75, 22), (6.65, 0.25, 30)]
    else:
        rings = [(4.2, 0.5, 22), (6.5, 0.0, 30)]
    for i, (rmm, kspeed, n) in enumerate(rings):
        rp = rmm * ppm
        for j in range(n):
            base = 360.0 * j / n + h01(j * 7 + i * 31) * 6
            a = math.radians(base + ang_s * kspeed)
            if nm == 'trP' and rmm > 6.0 and abs(((base + ang_s * kspeed) % 360.0) - 90.0) < 16.0: continue   # not over the pin
            wob = 0.0
            if kspeed == 0.0:      # squeeze film: breathes instead of turning
                wob = 0.25 * ppm * math.sin(t * 7.0 + j * 0.9)
            x = ccx + (rp + wob) * math.cos(a); y = ccy + (rp + wob) * math.sin(a)
            r0 = 2.4 / zoom
            c.drawCircle(x, y, r0 * 2.2, P(C_OIL_HI, 0.18))
            c.drawCircle(x, y, r0, P('#fff3c4', 0.95))


def arc_arrow(c, cx, cy, r, a0, a1, col, a, w=7.0):
    if a <= 0.01: return
    rect = skia.Rect.MakeLTRB(cx - r, cy - r, cx + r, cy + r)
    c.drawArc(rect, a0, a1 - a0, False, P(col, a, stroke=w, cap='butt'))
    ang = math.radians(a1); tx, ty = -math.sin(ang), math.cos(ang)
    if a1 < a0: tx, ty = -tx, -ty
    px, py = cx + r * math.cos(ang), cy + r * math.sin(ang)
    hd = w * 3.2
    q = path_of([(px + tx * hd, py + ty * hd), (px - ty * hd * 0.6 - tx * 0.0, py + tx * hd * 0.6), (px + ty * hd * 0.6, py - tx * hd * 0.6)], True)
    c.drawPath(q, P(col, a))


def axis_ring(c, V, x_mm, r_mm, t, speed, col, a, n=10, still=False):
    """ring around the shaft axis at x (drawn as the projected circle), dots moving with the rotation (+theta)."""
    if a <= 0.01 or CLEAN: return
    pts = []
    for k in range(73):
        th = 2 * PI * k / 72
        pts.append(anchor(V, p3=(x_mm, r_mm * math.cos(th), r_mm * math.sin(th))))
    # back half (y > 0) faint, front half (y < 0) solid
    back = [p for k, p in enumerate(pts) if math.cos(2 * PI * k / 72) >= 0]
    front = [pts[k] for k in range(18, 55)]
    c.drawPath(path_of(front), P(col, a * 0.9, stroke=4.0))
    for k in range(0, 18, 2):
        c.drawLine(*pts[k], *pts[k + 1], P(col, a * 0.35, stroke=3.0))
    for k in range(54, 72, 2):
        c.drawLine(*pts[k], *pts[k + 1], P(col, a * 0.35, stroke=3.0))
    if still: return
    for j in range(n):
        th = (2 * PI * j / n + math.radians(speed * t)) % (2 * PI)
        if not (PI / 2 - 0.1 < th < 3 * PI / 2 + 0.1): continue
        x, y = anchor(V, p3=(x_mm, r_mm * math.cos(th), r_mm * math.sin(th)))
        c.drawCircle(x, y, 9.0, P(col, a * 0.25)); c.drawCircle(x, y, 5.0, P(col, a))
    # arrow head on the front half, pointing the way it moves (down)
    k0 = 42; p0 = pts[k0]; p1 = pts[k0 + 3]
    ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0]); hd = 20
    q = path_of([(p1[0] + math.cos(ang) * hd * 0.6, p1[1] + math.sin(ang) * hd * 0.6),
                 (p1[0] + math.cos(ang + 2.5) * hd * 0.6, p1[1] + math.sin(ang + 2.5) * hd * 0.6),
                 (p1[0] + math.cos(ang - 2.5) * hd * 0.6, p1[1] + math.sin(ang - 2.5) * hd * 0.6)], True)
    c.drawPath(q, P(col, a))


def tr_overlays(c, t, nm, CX, CY, R, a, inf, zoom):
    if CLEAN: return
    ppm = abs(inf['px_per_mm']) / 10.0
    def S(mm): return mm * ppm * zoom
    tt = tr_angle(t)
    # rotation arrows: shaft (inner) and bushing (outer)
    spin = (t * 2.0) % 1.0
    a1 = a * ramp(t, TL['tr0'] + 0.5, 0.6)
    if a1 > 0.01 and not CLEAN:
        rs = S(2.6); base = tt * 1.0
        arc_arrow(c, CX, CY, rs, base - 70, base + 70, '#ffffff', a1 * 0.9, w=max(3.0, S(0.28)))
        if nm == 'trA':
            rb = S(5.4); bb = tt * 0.5
            arc_arrow(c, CX, CY, rb, bb + 110, bb + 200, Y, a1 * 0.95, w=max(3.0, S(0.26)))


# ------------------------------------------------------------------ UI
def label(c, text, ax, ay, lx, ly, a, side='r', col=WHT, size=30, dot=Y):
    if a <= 0.01 or CLEAN: return
    tw_ = tw(text, size, 'm8')
    c.drawCircle(ax, ay, 6, P(dot, a)); c.drawCircle(ax, ay, 12, P(dot, a * 0.35, stroke=2))
    ex = lx - 14 if side == 'r' else lx + 14
    c.drawPath(path_of([(ax, ay), (ex, ly)]), P(dot, a * 0.85, stroke=2.4))
    x0 = lx if side == 'r' else lx - tw_ - 28
    rrect(c, x0, ly - size * 0.86, x0 + tw_ + 28, ly + size * 0.48, 12, P('#0b1424', a * 0.88))
    rrect(c, x0, ly - size * 0.86, x0 + tw_ + 28, ly + size * 0.48, 12, P(dot, a * 0.55, stroke=2))
    txt(c, text, x0 + 14, ly, size, 'm8', col, a)


def wrap_lines(text, size, name, maxw):
    out, cur = [], ''
    for wd in text.split():
        cand = (cur + ' ' + wd).strip()
        if tw(cand, size, name) > maxw and cur: out.append(cur); cur = wd
        else: cur = cand
    return out + [cur]


def caption(c, title, body, a):
    if a <= 0.01 or CLEAN: return
    dy = 18 * (1 - a)
    if FMT == 'V':
        x, y0, ts, bs, mw, lh = 64, 1530, 56, 36, 950, 49
    else:
        x, y0, ts, bs, mw, lh = 1340, 700, 48, 31, 540, 43
    txt(c, title, x, y0 + dy, ts, 'anton', Y, a, shadow=10)
    yy = y0 + ts * 1.18 + dy
    for ln in wrap_lines(body, bs, 'm7', mw):
        txt(c, ln, x, yy, bs, 'm7', WHT, a, shadow=8); yy += lh


def to_screen(V, p):
    z, cx, cy = V
    return (p[0] - cx) * z + W / 2, (p[1] - cy) * z + H / 2


def anchor(V, key=None, p3=None):
    w = proj(p3) if p3 is not None else INFO['anch'][key][:2]
    return to_screen(V, w)


def background(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), P(shader=lin(0, 0, 0, H, ['#0e1a2c', '#060b14'])))
    cx, cy = W / 2, H * 0.45
    R = max(W, H) * 0.62
    c.drawCircle(cx, cy, R, P(shader=rad(cx, cy, R, [skia.Color4f(.13, .21, .34, .55).toColor(), skia.Color4f(0, 0, 0, 0).toColor()])))
    c.save(); c.rotate(-20, W / 2, H / 2)
    f = font('anton', 58); s = 'TURBO DOCTOR'; w = f.measureText(s) + 120; off = (t * 9) % w
    for row in range(-16, 26):
        yy = row * 110; sh = (row % 2) * w / 2
        for k in range(-4, 9):
            x = -600 + k * w + sh + off
            col = (1, 1, 1, .04) if (row + k) % 3 else (1, .76, .1, .052)
            c.drawString(s, x, yy, f, P(col[:3], col[3]))
    c.restore()


TITLE = {'A': ('TURBINA CU LAGĂRE FLOTANTE', 'lagăr hidrodinamic · două bucșe care se rotesc'),
         'B': ('TURBINA CU LAGĂR FIX', 'lagăr semi-flotant · o singură bucată, nu se rotește')}[VAR]


def header(c, t):
    if CLEAN:
        txt(c, 'MODEL 3D RECONSTRUIT · JOCURI MĂRITE', W - 60, 64 if FMT == 'V' else 58, 20 if FMT == 'V' else 19, 'm8', WHT, 0.45, 'r')
        return
    if FMT == 'V':
        c.drawRect(skia.Rect.MakeLTRB(0, 0, W, 250), P(shader=lin(0, 0, 0, 250, [skia.Color4f(0.02, 0.04, 0.07, 0.8).toColor(), skia.Color4f(0.02, 0.04, 0.07, 0.0).toColor()])))
        txt(c, TITLE[0], 60, 118, 54, 'anton', WHT, 1.0, shadow=8)
        txt(c, TITLE[1], 62, 164, 28, 'm7', WHT, 0.82)
        txt(c, 'MODEL 3D RECONSTRUIT · JOCURI MĂRITE', 1020, 64, 20, 'm8', WHT, 0.45, 'r')
    else:
        c.drawRect(skia.Rect.MakeLTRB(0, 0, W, 190), P(shader=lin(0, 0, 0, 190, [skia.Color4f(0.02, 0.04, 0.07, 0.75).toColor(), skia.Color4f(0.02, 0.04, 0.07, 0.0).toColor()])))
        txt(c, TITLE[0], 64, 92, 50, 'anton', WHT, 1.0, shadow=8)
        txt(c, TITLE[1], 66, 134, 26, 'm7', WHT, 0.82)
        txt(c, 'MODEL 3D RECONSTRUIT · JOCURI MĂRITE', 1870, 58, 19, 'm8', WHT, 0.45, 'r')


def bottom_band(c):
    if CLEAN: return
    if FMT == 'V':
        c.drawRect(skia.Rect.MakeLTRB(0, 1380, W, H), P(shader=lin(0, 1380, 0, 1600, [skia.Color4f(0.02, 0.04, 0.07, 0.0).toColor(), skia.Color4f(0.02, 0.04, 0.07, 0.86).toColor()])))
    else:
        c.drawRect(skia.Rect.MakeLTRB(1200, 0, W, H), P(shader=lin(1200, 0, 1420, 0, [skia.Color4f(0.02, 0.04, 0.07, 0.0).toColor(), skia.Color4f(0.02, 0.04, 0.07, 0.82).toColor()])))


def legend(c, a, items):
    if a <= 0.01 or CLEAN: return
    if FMT == 'V': x, y = 64, 1860
    else: x, y = 64, 1040
    for col, s in items:
        c.drawRoundRect(skia.Rect.MakeXYWH(x, y - 22, 26, 26), 6, 6, P(col, a))
        txt(c, s, x + 38, y, 26, 'm7', WHT, a * 0.9); x += 38 + tw(s, 26, 'm7') + 34


def endcard(c, t, a):
    if a <= 0.01 or CLEAN: return
    c.drawRect(skia.Rect.MakeWH(W, H), P('#060b14', a * 0.95))
    cx = W / 2; cy = H / 2 - (40 if FMT == 'V' else 10)
    big = 170 if FMT == 'V' else 150
    txt(c, 'TURBO', cx, cy - 200, big, 'anton', WHT, a, 'c')
    txt(c, 'DOCTOR', cx, cy - 200 + big * 1.03, big, 'anton', Y, a, 'c')
    y2 = cy - 200 + big * 1.03 + 95
    txt(c, 'Experți în turbine', cx, y2, 36, 'm7', WHT, a * 0.9, 'c')
    rrect(c, cx - 310, y2 + 50, cx + 310, y2 + 140, 26, P(Y, a)); txt(c, 'DIAGNOZĂ GRATUITĂ', cx, y2 + 110, 40, 'm9', BG, a, 'c')
    txt(c, '0739 065 065', cx, y2 + 250, 96, 'anton', WHT, a, 'c')
    txt(c, 'GALAȚI · BUCUREȘTI · IAȘI · PIATRA NEAMȚ', cx, y2 + 330, 30, 'm8', WHT, a * 0.85, 'c')


# ---------------- label sets: (text, anchor key or 3D point, label position on screen, side)
def LBL():
    V = FMT == 'V'
    if V:
        over = [('Roata compresorului', 'comp_wheel', (70, 520), 'r'), ('Roata turbinei', 'turb_wheel', (1010, 520), 'l'),
                ('Palete geometrie variabilă', 'vanes', (1010, 440), 'l'), ('Axul', (6.0, 0.0, -3.8), (700, 1350), 'r'),
                ('Carcasa lagărelor', (-14.0, 0.0, -21.0), (70, 1420), 'r')]
    else:
        over = [('Roata compresorului', 'comp_wheel', (90, 196), 'r'), ('Axul', (-14.0, 0.0, 3.6), (560, 196), 'r'),
                ('Roata turbinei', 'turb_wheel', (1250, 250), 'r'), ('Palete geometrie variabilă', 'vanes_bot', (1250, 560), 'r'),
                ('Carcasa lagărelor', 'chra', (800, 1036), 'r')]
    if VAR == 'A':
        if V:
            chra = [('Ulei de la pompa motorului', (-13.0, 0.0, BJ_Z), (640, 250), 'r'),
                    ('Lagăr flotant (bucșă)', 'bush_c', (70, 640), 'r'), ('Lagăr flotant (bucșă)', 'bush_t', (1010, 640), 'l'),
                    ('Lagăr axial', 'thrust_low', (70, 1250), 'r'), ('Retur ulei, liber, spre baie', 'drain', (1010, 1400), 'l')]
            brg = [('Bucșa (se rotește)', (FX, 0.0, 5.3), (70, 430), 'r'), ('Film exterior: carcasă – bucșă', (FX + 2.5, 0.0, 6.65), (1010, 480), 'l'),
                   ('Film interior: bucșă – ax', (FX + 2.5, 0.0, -4.2), (1010, 1430), 'l'), ('Axul', (FX - 6.0, 0.0, -2.0), (70, 1430), 'r')]
        else:
            chra = [('Ulei de la pompa motorului', (-13.0, 0.0, BJ_Z), (770, 170), 'r'),
                    ('Lagăr flotant (bucșă)', 'bush_c', (330, 292), 'r'), ('Lagăr flotant (bucșă)', 'bush_t', (1250, 330), 'r'),
                    ('Lagăr axial', 'thrust_low', (330, 900), 'l'), ('Retur ulei, liber, spre baie', 'drain', (790, 1010), 'r')]
            brg = [('Bucșa (se rotește)', (FX, 0.0, 5.3), (1250, 250), 'r'), ('Film exterior: carcasă – bucșă', (FX + 2.5, 0.0, 6.65), (1250, 330), 'r'),
                   ('Film interior: bucșă – ax', (FX + 2.5, 0.0, -4.2), (1250, 560), 'r'), ('Axul', (-2.0, 0.0, -3.0), (330, 962), 'r')]
    else:
        if V:
            chra = [('Ulei de la pompa motorului', (-13.0, 0.0, BJ_Z), (640, 250), 'r'),
                    ('Lagăr dintr-o bucată (semi-flotant)', 'bush_t', (1010, 640), 'l'), ('Știft: nu-l lasă să se rotească', 'pin', (1010, 1300), 'l'),
                    ('Lagăr axial', 'thrust_low', (70, 1250), 'r'), ('Retur ulei, liber, spre baie', 'drain', (1010, 1400), 'l')]
            brg = [('Lagărul nu se rotește', (FX, 0.0, 5.3), (70, 430), 'r'), ('Film exterior: amortizează', (FX + 2.5, 0.0, 6.5), (1010, 480), 'l'),
                   ('Film interior: poartă axul', (FX + 2.5, 0.0, -4.2), (1010, 1430), 'l'), ('Știftul', (0.0, 0.0, -10.0), (70, 1430), 'r')]
        else:
            chra = [('Ulei de la pompa motorului', (-13.0, 0.0, BJ_Z), (770, 170), 'r'),
                    ('Lagăr dintr-o bucată (semi-flotant)', 'bush_t', (1250, 330), 'r'), ('Știft: nu-l lasă să se rotească', 'pin', (1250, 600), 'r'),
                    ('Lagăr axial', 'thrust_low', (330, 900), 'l'), ('Retur ulei, liber, spre baie', 'drain', (790, 1010), 'r')]
            brg = [('Lagărul nu se rotește', (FX, 0.0, 5.3), (1250, 250), 'r'), ('Film exterior: amortizează', (FX + 2.5, 0.0, 6.5), (1250, 330), 'r'),
                   ('Film interior: poartă axul', (FX + 2.5, 0.0, -4.2), (1250, 560), 'r'), ('Știftul', (0.0, 0.0, -10.0), (330, 962), 'r')]
    return over, chra, brg


LB_OVER, LB_CHRA, LB_BRG = LBL()


def draw_labels(c, t, V, items, t0, t1, step=0.32):
    a0 = win(t, t0, t1, 0.3, 0.5)
    if a0 <= 0.01: return
    for i, (s_, key, off, side) in enumerate(items):
        a = a0 * ramp(t, t0 + 0.15 + i * step, 0.3)
        if isinstance(key, tuple): ax, ay = anchor(V, p3=key)
        else: ax, ay = anchor(V, key)
        label(c, s_, ax, ay, off[0], off[1], a, side, size=28 if FMT == 'V' else 26)


CAPS = {
    'A': [(0.3, 3.1, 'Cum arată pe dinăuntru', 'o turbină cu lagăre flotante (hidrodinamice)'),
          (5.3, 11.4, 'GAZE ȘI AER', 'Gazele de evacuare rotesc roata turbinei. Pe același ax, roata compresorului împinge aer spre motor.'),
          (13.7, 20.8, 'ULEIUL', 'Vine sub presiune de la pompa motorului și ajunge la cele două lagăre și la lagărul axial. Apoi se scurge liber înapoi, spre baie.'),
          (23.1, 30.7, 'DOUĂ FILME DE ULEI', 'Bucșa plutește între două filme de ulei: unul spre carcasă, unul spre ax. Uleiul ține piesele despărțite, metalul nu atinge metalul.'),
          (32.5, 40.8, 'BUCȘA SE ROTEȘTE', 'La lagărele flotante bucșa se învârte și ea, cam la jumătate din turația axului. Ambele filme de ulei sunt hidrodinamice.'),
          (42.8, 47.5, 'PE SCURT', 'Axul și bucșele plutesc pe ulei. Fără presiune sau cu ulei murdar, filmul se rupe și lagărele se uzează.')],
    'B': [(0.3, 3.1, 'Cum arată pe dinăuntru', 'o turbină cu lagăr fix (semi-flotant)'),
          (5.3, 11.4, 'GAZE ȘI AER', 'Gazele de evacuare rotesc roata turbinei. Pe același ax, roata compresorului împinge aer spre motor.'),
          (13.7, 20.8, 'ULEIUL', 'Vine sub presiune de la pompa motorului și intră în lagărul dintr-o bucată, prin găurile lui, și în lagărul axial. Apoi se scurge liber înapoi, spre baie.'),
          (23.1, 30.7, 'UN SINGUR FILM CARE POARTĂ', 'Lagărul stă pe loc. Doar filmul dintre ax și lagăr ține axul; filmul exterior lucrează mai ales ca amortizor pentru mișcările axului.'),
          (32.5, 36.5, 'LAGĂRUL STĂ PE LOC', 'Axul se rotește în filmul interior. Lagărul nu se rotește, deci filmul exterior nu e hidrodinamic: el amortizează mișcările axului.'),
          (36.8, 40.8, 'DE CE «FIX»', 'Un știft din carcasă intră în lagăr și nu-l lasă să se rotească. Așa sunt majoritatea turbinelor mici, de turație mare, de la autoturisme.'),
          (42.8, 47.5, 'PE SCURT', 'Lagărul fix nu se rotește, axul plutește pe filmul interior. Fără presiune sau cu ulei murdar, filmul se rupe și lagărul se uzează.')],
}[VAR]


TR_GEOM = {'V': (540.0, 930.0, 420.0), 'H': (720.0, 572.0, 418.0)}


def tr_labels(c, t, CX, CY, R):
    if CLEAN: return
    inf = tr_info('trA'); ppm = abs(inf['px_per_mm']) / 10.0; zoom = R / (12.0 * ppm)
    def P2(ymm, zmm):       # transverse view: world y -> screen x (+y to the left), z up
        return CX - ymm * ppm * zoom, CY - zmm * ppm * zoom
    V = FMT == 'V'
    if V: slots = {1: (70, 300, 'r'), 2: (1010, 300, 'l'), 3: (70, 390, 'r'), 4: (70, 1440, 'r'), 5: (1010, 1440, 'l')}
    else: slots = {1: (1200, 230, 'r'), 2: (1200, 310, 'r'), 3: (1200, 390, 'r'), 4: (1200, 470, 'r'), 5: (1200, 550, 'r')}
    if VAR == 'A':
        items = [('Bucșa: cam ½ din turația axului', P2(3.9, 3.9), 1), ('Film exterior', P2(-4.75, 4.75), 2), ('Ulei din galerie', P2(0.0, 11.0), 3),
                 ('Axul (turația turbinei)', P2(0.0, -2.0), 4), ('Film interior', P2(-2.97, -2.97), 5)]
        win_ = (TL['tr0'] + 0.6, TL['tr1'] - 0.2)
    else:
        items = [('Lagărul: fix', P2(3.9, 3.9), 1), ('Film exterior: amortizare', P2(-4.6, 4.6), 2), ('Ulei din galerie', P2(0.0, 11.0), 3),
                 ('Axul se rotește', P2(0.0, -2.0), 4), ('Film interior: hidrodinamic', P2(-2.97, -2.97), 5)]
        win_ = (TL['tr0'] + 0.6, TL['trp0'] + 0.1)
    if not V: items.sort(key=lambda it: it[1][1])
    a0 = win(t, win_[0], win_[1], 0.3, 0.4)
    for i, (s_, (ax, ay), slot) in enumerate(items):
        a = a0 * ramp(t, win_[0] + 0.2 + i * 0.35, 0.3)
        lx, ly, side = slots[slot if V else i + 1]
        label(c, s_, ax, ay, lx, ly, a, side, size=27 if V else 26)
    if VAR == 'B':
        a1 = win(t, TL['trp1'] - 0.2, TL['tr1'] - 0.2, 0.3, 0.4)
        if a1 > 0.01:     # highlight the anti-rotation pin
            x0, y0 = P2(1.22, -5.15); x1, y1 = P2(-1.22, -min(12.0, 11.6))
            pulse = 0.65 + 0.35 * math.sin(t * 5.0)
            rr = skia.Rect.MakeLTRB(min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1))
            c.drawRect(rr, P(Y, a1 * 0.35 * pulse, stroke=12.0, blur=6.0))
            c.drawRect(rr, P(Y, a1 * 0.95, stroke=3.0))
        ax, ay = P2(0.0, -9.5)
        lx, ly, side = slots[4] if V else slots[3]
        label(c, 'Știftul ține lagărul pe loc', ax, ay, lx, ly, a1, side, size=28 if V else 27)


def frame(t):
    surf = skia.Surface(W, H); c = surf.getCanvas()
    background(c, t)
    V = main_view(t)
    a_main, a_tr = scene_alpha(t)
    draw_main(c, t, V, a_main)
    draw_tr(c, t, a_tr)
    bottom_band(c)
    header(c, t)
    # labels on the main scene
    if a_main > 0.5:
        draw_labels(c, t, V, LB_OVER, TL['open1'] + 0.6, TL['wide1'] - 0.1)
        draw_labels(c, t, V, LB_CHRA, TL['chra0'] + 1.2, TL['chra1'] - 0.1, 0.45)
        draw_labels(c, t, V, LB_BRG, TL['brg0'] + 0.3, TL['brg1'] - 0.1, 0.45)
        # bushing rotation hint (A) / no rotation (B) in the bearing close-up
        a_r = win(t, TL['brg0'] + 0.9, TL['brg1'] - 0.2, 0.4, 0.4)
        if a_r > 0.01:
            axis_ring(c, V, 23.0, 5.2, t, 220.0, '#ffffff', a_r)           # shaft
            if VAR == 'A':
                axis_ring(c, V, FX, 7.8, t, 110.0, Y, a_r)               # bushing: about half the speed
    if a_tr > 0.5: tr_labels(c, t, *TR_GEOM[FMT])
    for (t0, t1, ti, body) in CAPS:
        caption(c, ti, body, win(t, t0, t1, 0.4, 0.4))
    leg = [(C_AIR, 'aer'), (C_GAS, 'gaze de evacuare'), (C_OIL, 'ulei')]
    legend(c, ramp(t, TL['open1'], 0.5) * (1 - ramp(t, TL['end0'], 0.4)), leg)
    endcard(c, t, ramp(t, TL['end0'], 0.7))
    return surf.makeImageSnapshot()


def render(out, f0=0, f1=None):
    n = int(round(DUR * FPS)); f1 = n if f1 is None else min(f1, n)
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-vf', 'scale=out_color_matrix=bt709:out_range=tv', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p',
                          '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    for fi in range(f0, f1):
        p.stdin.write(frame(fi / FPS).toarray(colorType=skia.kRGBA_8888_ColorType).tobytes())
    p.stdin.close(); p.wait()


if __name__ == '__main__':
    a = sys.argv[1:]
    if '--stills' in a:
        os.makedirs(os.path.join(HERE, 'stills'), exist_ok=True)
        name = {'A': 'Lagare_Flotante', 'B': 'Lagar_Fix'}[VAR]
        shots = [('01_exterior', 1.6), ('02_sectiune', 9.5), ('03_ulei', 19.5), ('04_lagar', 27.0)]
        shots += [('05_sectiune_transversala', 36.0)] if VAR == 'A' else [('05_sectiune_transversala', 34.5), ('06_stift', 39.5)]
        for nm, ts in shots:
            im = frame(ts); arr = im.toarray(colorType=skia.kRGBA_8888_ColorType)
            cv2.imwrite(os.path.join(HERE, 'stills', f'TurboDoctor_Turbina_{name}_{FMT}_{nm}.jpg'), cv2.cvtColor(arr, cv2.COLOR_RGBA2BGR), [cv2.IMWRITE_JPEG_QUALITY, 93])
    elif '--png' in a:
        os.makedirs(os.path.join(HERE, 'proof'), exist_ok=True)
        for ts in a[a.index('--png') + 1].split(','):
            frame(float(ts)).save(os.path.join(HERE, 'proof', f'{VAR}{FMT}_{float(ts):05.1f}.png'), skia.kPNG)
    elif '--out' in a:
        o = a[a.index('--out') + 1]
        if '--frames' in a:
            i = a.index('--frames'); render(o, int(a[i + 1]), int(a[i + 2]))
        else: render(o)
