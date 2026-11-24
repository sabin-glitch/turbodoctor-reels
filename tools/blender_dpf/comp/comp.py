"""Compositor: Turbo Doctor DPF + DOC animation (skia + numpy + OpenCV) from the Blender layers in ../out.

  python3 comp.py --png 5,12,20          -> proof/V_<t>.png
  [CLEAN=1] python3 comp.py --out x.mp4 [--jobs 2] [--force 8,9]
        one encoded file per chapter in x.mp4.seg/ (kept: only missing or forced chapters are rendered again), joined without re-encoding
  [CLEAN=1] python3 comp.py --out x.mp4 --frames a b      -> just these frames, one file
  [CLEAN=1] python3 comp.py --stills     -> stills/*.jpg
  python3 comp.py --cover x.jpg         -> cover frame with the texts
World space = pixels of the T1 plate (2160 x 2160) of the main camera. Format: 9:16 (1080 x 1920).
"""
import sys, os, json, math, subprocess, time
import numpy as np, skia, cv2
from fk import *

HERE = os.path.dirname(os.path.abspath(__file__))
OUTD = os.path.join(HERE, '..', 'out')
INFO = json.load(open(os.path.join(OUTD, 'info.json')))
CROPS = INFO['crops']; S1 = INFO['base']; D = INFO['dims']; LAT = INFO['lattice']
FMT = 'V'
CLEAN = os.environ.get('CLEAN', '0') == '1'
W, H = 1080, 1920
FPS = 30
Y, WHT, BG = '#ffc21a', '#ffffff', '#0a1220'
C_GAS, C_CLN, C_SOOT, C_ASH, C_HOT = '#ff7a30', '#6ec6ff', '#0c0c0c', '#c2bcab', '#ff5a14'
SAMP = skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear)
XM = D['XM']                                # macro centre (mm): middle of a filter segment
DPF_Z0, DPF_Z1, DOC_Z0, DOC_Z1, R_B = D['DPF_Z0'], D['DPF_Z1'], D['DOC_Z0'], D['DOC_Z1'], D['R_B']
PLUG = D['DPF_PLUG']

# ------------------------------------------------------------------ timeline (s)
TL = dict(open0=3.4, open1=5.2, wide1=12.0, face0=13.6, face1=19.6, mac0=21.2, soot0=25.6, mac1=29.8, sens0=32.2, sens1=38.6,
          dp0=40.0, dpz0=43.2, dpz1=44.6, dp1=50.4, reg0=52.0, burn0=53.0, burn1=57.6, reg1=58.6, ash0=60.6, ash1=65.8, back1=68.0,
          sum0=68.3, sum1=72.7, end0=72.9)
DUR = 69.8 if CLEAN else 76.3

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
    d = np.stack([xn / k, yn / k, -np.ones_like(xn)], -1)
    R = _MI[:3, :3]; o = _MI[:3, 3]
    dw = d @ R.T
    t = -o[1] / dw[..., 1]
    P = o + dw * t[..., None]
    return P[..., 0], P[..., 2]


PXMM = math.hypot(*(np.array(proj((10.0, 0, -60.0))) - np.array(proj((0.0, 0, -60.0))))) / 10.0      # world px per mm on the section plane

# ------------------------------------------------------------------ images
TIERS = {'T1': (1, (0, 0)), 'T2': (2, CROPS['T2'][:2]), 'T8': (8, CROPS['T8'][:2]), 'TA': (24, CROPS['TA'][:2]), 'TB': (24, CROPS['TB'][:2])}
FEATH = {'T1': 0, 'T2': 0, 'T8': 70, 'TA': 60, 'TB': 60}


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


def _fmask(h, w, F):
    yy, xx = np.mgrid[0:h, 0:w]
    f = np.clip(np.minimum.reduce([xx, yy, w - 1 - xx, h - 1 - yy]) / F, 0, 1)
    return f * f * (3 - 2 * f)


_IM = {}


def img(name):
    if name not in _IM:
        a = _read(name)
        if a is not None:
            F = FEATH.get(name.split('_')[0], 0)
            if F:
                a = a.copy(); a[..., 3] = (a[..., 3].astype(np.float32) * _fmask(a.shape[0], a.shape[1], F)).astype(np.uint8)
            a = _sk(a)
        _IM[name] = a
    return _IM[name]


_MASK = {}


def mask(tn, key):
    """key 'A' / 'B' / 'C' / 'D' -> uint8 (h, w, 3): group channels x coverage, feathered like the plate."""
    k = (tn, key)
    if k not in _MASK:
        a = _read(f'{tn}_id{key}')
        if a is None: _MASK[k] = None
        else:
            m = a[..., :3].astype(np.float32) * (a[..., 3:4].astype(np.float32) / 255.0)
            F = FEATH.get(tn, 0)
            if F: m *= _fmask(m.shape[0], m.shape[1], F)[..., None]
            _MASK[k] = m.astype(np.uint8)
    return _MASK[k]


def _bbox(a, thr=3, pad=0):
    ys = np.nonzero(a.max(1) > thr)[0]; xs = np.nonzero(a.max(0) > thr)[0]
    if len(xs) == 0: return None
    h, w = a.shape[:2]
    return max(0, xs[0] - pad), max(0, ys[0] - pad), min(w, xs[-1] + 1 + pad), min(h, ys[-1] + 1 + pad)


def _rgba(col, alpha):
    r, g, b = hexc(col) if isinstance(col, str) else col
    out = np.empty(alpha.shape + (4,), np.uint8)
    out[..., 0] = int(r * 255); out[..., 1] = int(g * 255); out[..., 2] = int(b * 255)
    out[..., 3] = np.clip(alpha * 255.0, 0, 255).astype(np.uint8)
    return out


_FX = {}
_HLK = {'hlT': ('C', 0), 'hlL': ('C', 1), 'hlP': ('C', 2), 'hlPipe': ('D', 0), 'hlHose': ('D', 1), 'hlDps': ('D', 2)}


def fx(tn, kind):
    """effect layers built once from the mask plates of a tier -> (image, ox, oy) in tier px, or None."""
    k = (tn, kind)
    if k in _FX: return _FX[k]
    out = None
    tier, (x0, y0) = TIERS[tn]
    if kind in ('soot', 'tin', 'tout', 'glow', 'glow_doc'):
        A, B = mask(tn, 'A'), mask(tn, 'B')
        if A is not None and B is not None:
            src = {'soot': A[..., 0], 'tin': B[..., 0], 'tout': B[..., 1], 'glow': A[..., 0], 'glow_doc': A[..., 1]}[kind]
            bb = _bbox(src)
            if bb is not None:
                bx0, by0, bx1, by1 = bb; sl = (slice(by0, by1), slice(bx0, bx1))
                if kind == 'soot':
                    h, w = by1 - by0, bx1 - bx0
                    yy, xx = np.mgrid[by0:by1, bx0:bx1].astype(np.float32)
                    _, zz = unproject_plane_y0((xx + x0) / tier, (yy + y0) / tier)
                    top = (zz > DPF_Z1 + 0.25).astype(np.float32)                   # the inlet face of the filter (above the cut edge)
                    rng = np.random.default_rng(7); nz = cv2.GaussianBlur(rng.random((h, w)).astype(np.float32), (0, 0), max(1.5, 0.6 * tier))
                    nz = np.clip((nz - 0.5) * 6.0 + 0.5, 0, 1)
                    al = np.clip(B[sl][..., 0] / 255.0 * (0.80 + 0.12 * nz) + A[sl][..., 0] / 255.0 * top * 0.62, 0, 0.93)
                    out = (_sk(_rgba(C_SOOT, al)), bx0, by0)
                else:
                    col = {'tin': C_GAS, 'tout': C_CLN, 'glow': '#ff6a1e', 'glow_doc': '#ff8a2a'}[kind]
                    out = (_sk(_rgba(col, src[sl] / 255.0)), bx0, by0)
    elif kind.startswith('hl'):
        glow = kind.endswith('g'); key, ch = _HLK[kind[:-1] if glow else kind]
        m = mask(tn, key)
        if m is not None:
            bb = _bbox(m[..., ch], pad=int(26 * tier) if glow else 2)
            if bb is not None:
                bx0, by0, bx1, by1 = bb; a = m[by0:by1, bx0:bx1, ch].astype(np.float32) / 255.0
                if glow: a = np.clip(cv2.GaussianBlur(a, (0, 0), 7.0 * tier) * 1.6, 0, 1)
                out = (_sk(_rgba(Y, a)), bx0, by0)
    _FX[k] = out
    return out


# ------------------------------------------------------------------ views (zoom, world centre x, y)
def fit_px(b, rect):
    x0, y0, x1, y1 = b; sx0, sy0, sx1, sy1 = rect
    z = min((sx1 - sx0) / (x1 - x0), (sy1 - sy0) / (y1 - y0))
    return z, (x0 + x1) / 2 - ((sx0 + sx1) / 2 - W / 2) / z, (y0 + y1) / 2 - ((sy0 + sy1) / 2 - H / 2) / z


def fit_view(pts3, rect):
    q = np.array(projs(pts3)); x0, y0 = q.min(0); x1, y1 = q.max(0)
    return fit_px((x0, y0, x1, y1), rect)


def box3(x0, x1, z0, z1, y0=0.0, y1=0.0):
    return [(x, y, z) for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)]


def view_at(p3, px_per_mm, sx=W / 2, sy=H / 2):
    z = px_per_mm / PXMM; wx, wy = proj(p3)
    return z, wx - (sx - W / 2) / z, wy - (sy - H / 2) / z


def zoomed(V, k): return (V[0] * k, V[1], V[2])


def alpha_bbox(names, thr=8):
    box = None
    for nm in names:
        a = _read(nm)
        if a is None: continue
        ys, xs = np.nonzero(a[..., 3] > thr)
        b = [xs.min(), ys.min(), xs.max(), ys.max()]
        box = b if box is None else [min(box[0], b[0]), min(box[1], b[1]), max(box[2], b[2]), max(box[3], b[3])]
    return box


_BB = os.path.join(OUTD, 'bbox.json')
if os.path.exists(_BB): BBX = json.load(open(_BB))
else:
    BBX = {'sec': [int(v) for v in alpha_bbox(['T1_sec'])], 'ext': [int(v) for v in alpha_bbox(['T1_sec', 'T1_front'])]}
    json.dump(BBX, open(_BB, 'w'))
V_EXT = fit_px(BBX['ext'], (60, 300, 1020, 1500))
V_WIDE = fit_px(BBX['sec'], (60, 290, 1020, 1480))
V_RIGHT = (V_WIDE[0] * 1.06, V_WIDE[1] + 70, V_WIDE[2])
V_FACE = view_at((XM, 0.0, -6.0), W / 62.0, W / 2, 900)
V_MACA = view_at((XM, 0.0, -6.1), 72.0, W / 2, 910)
V_MACB = view_at((XM, 0.0, -171.2), 72.0, W / 2, 910)
V_CAN = fit_view(box3(-92, 92, -252, 172), (60, 285, 1020, 1490))
V_DPS = fit_view(box3(50, 188, -6, 250, 0, 30), (40, 290, 1040, 1470))

KEYS = [(0.0, zoomed(V_EXT, 0.965), 'h'), (TL['open0'], V_EXT, 'm'), (TL['open1'], V_WIDE, 'h'), (TL['wide1'], zoomed(V_WIDE, 1.035), 'm'),
        (TL['face0'], V_FACE, 'h'), (TL['face1'], zoomed(V_FACE, 1.06), 'm'), (TL['mac0'], zoomed(V_MACA, 0.93), 'h'), (TL['mac1'], V_MACA, 'm'),
        (TL['sens0'], V_WIDE, 'h'), (TL['sens1'], zoomed(V_WIDE, 1.03), 'm'), (TL['dp0'], V_RIGHT, 'h'), (TL['dpz0'], zoomed(V_RIGHT, 1.03), 'm'),
        (TL['dpz1'], V_DPS, 'h'), (TL['dp1'], zoomed(V_DPS, 1.05), 'm'), (TL['reg0'], V_CAN, 'h'), (TL['reg1'], zoomed(V_CAN, 1.04), 'm'),
        (TL['ash0'], zoomed(V_MACB, 0.94), 'h'), (TL['ash1'], V_MACB, 'm'), (TL['back1'], V_WIDE, 'h'), (80.0, zoomed(V_WIDE, 1.04), 'h')]


def interp_view(a, b, f):
    if abs(b[0] - a[0]) < 1e-9: return (a[0], lerp(a[1], b[1], f), lerp(a[2], b[2], f))
    z = math.exp(lerp(math.log(a[0]), math.log(b[0]), f))
    # pan in step with the zoom so that the target stays put on screen
    g = (1 / a[0] - 1 / z) / (1 / a[0] - 1 / b[0])
    return z, lerp(a[1], b[1], g), lerp(a[2], b[2], g)


def main_view(t):
    if t <= KEYS[0][0]: return KEYS[0][1]
    for (t0, a, _), (t1, b, kind) in zip(KEYS, KEYS[1:]):
        if t <= t1:
            f = (t - t0) / max(1e-6, t1 - t0)
            return interp_view(a, b, f if kind == 'h' else sm(f))        # smoothstep: the big zooms never jump more than ~9 % per frame
    return KEYS[-1][1]


def to_screen(V, p):
    z, cx, cy = V
    return (p[0] - cx) * z + W / 2, (p[1] - cy) * z + H / 2


def anchor(V, key=None, p3=None):
    if key == 'pipe2x': p3 = (D['PX2'], D['Y_P'], 28.0)
    w = proj(p3) if p3 is not None else INFO['anch'][key][:2]
    return to_screen(V, w)


# ------------------------------------------------------------------ state of the filter along the film
def soot_load(t):
    """0..1 how much soot sits in the inlet channels."""
    return ramp(t, TL['soot0'] + 0.6, TL['mac1'] - TL['soot0'] - 1.0)


def burn_front(t):
    """z (mm) of the regeneration front: above it the soot is gone. None before / after."""
    if t < TL['burn0']: return None
    f = cl((t - TL['burn0']) / (TL['burn1'] - TL['burn0']))
    return lerp(DPF_Z1 + 22.0, DPF_Z0 - 26.0, f)


def heat(t):
    """0..1 exhaust temperature raised for the regeneration."""
    return ramp(t, TL['reg0'] + 0.3, 1.0) * (1 - ramp(t, TL['burn1'] - 0.2, 1.1))


def ash_h(t):
    """mm of ash above the plugs at the end of the inlet channels (macro B)."""
    return 7.0 * sm((t - TL['ash0'] - 0.5) / (TL['ash1'] - TL['ash0'] - 1.4))


def dp_level(t):
    """0..1 differential pressure shown by the gauge."""
    if t < TL['reg0'] - 1.0: return 0.12 + 0.88 * sm((t - TL['dpz1'] - 1.6) / 3.4)
    fr = burn_front(t)
    if fr is None: return 1.0
    return 0.12 + 0.88 * cl((fr - (DPF_Z0 - 10.0)) / (DPF_Z1 - DPF_Z0 + 20.0))


# ------------------------------------------------------------------ drawing: plates + effects
def draw_im(c, im, k, x0, y0, alpha=1.0, blend=None, cf=None):
    if im is None or alpha <= 0.003: return
    p = skia.Paint(); p.setAlphaf(min(1.0, alpha))
    if blend is not None: p.setBlendMode(blend)
    if cf is not None: p.setColorFilter(cf)
    c.save(); c.translate(x0 / k, y0 / k); c.scale(1.0 / k, 1.0 / k); c.drawImage(im, 0, 0, SAMP, p); c.restore()


def draw_fx(c, tn, kind, alpha=1.0, blend=None):
    e = fx(tn, kind)
    if e is None or alpha <= 0.003: return
    k, (x0, y0) = TIERS[tn]
    draw_im(c, e[0], k, x0 + e[1], y0 + e[2], alpha, blend)


def wy_of_z(zmm):
    """world px y of a height on the section plane at the filter axis."""
    return proj((0.0, 0.0, zmm))[1]


def band_layer(c, draw, y_a, y_b, mode='below', blend=None, alpha=1.0):
    """draws `draw()` in a layer and keeps only: 'below' the line y_a..y_b (soft edge between them) or a 'band' fading out towards both."""
    paint = skia.Paint(); paint.setAlphaf(alpha)
    if blend is not None: paint.setBlendMode(blend)
    c.saveLayer(None, paint)
    draw()
    mp = skia.Paint(); mp.setBlendMode(skia.BlendMode.kDstIn)
    if mode == 'below':
        cols = [skia.Color4f(0, 0, 0, 0).toColor(), skia.Color4f(0, 0, 0, 1).toColor()]; pos = None
    else:
        cols = [skia.Color4f(0, 0, 0, 0).toColor(), skia.Color4f(0, 0, 0, 1).toColor(), skia.Color4f(0, 0, 0, 0).toColor()]; pos = [0.0, 0.45, 1.0]
    mp.setShader(skia.GradientShader.MakeLinear([skia.Point(0, y_a), skia.Point(0, y_b)], cols, pos))
    c.drawRect(skia.Rect.MakeLTRB(-5000, -5000, 8000, 8000), mp)
    c.restore()


def tier_fx(c, tn, t):
    """mask-based effects of one tier: channel tints, soot, regeneration glow."""
    a_t = tint_alpha(t)
    if a_t > 0.01:
        draw_fx(c, tn, 'tin', a_t); draw_fx(c, tn, 'tout', a_t)
    if tn == 'TB': return
    s = soot_load(t) * (0.62 if tn == 'TA' else 1.0); fr = burn_front(t)
    if s > 0.01:
        if fr is None: draw_fx(c, tn, 'soot', s)
        elif fr > DPF_Z0 - 24.0:
            band_layer(c, lambda: draw_fx(c, tn, 'soot', s), wy_of_z(fr + 9.0), wy_of_z(fr - 9.0), 'below')
    hg = heat(t)
    if hg > 0.01:
        draw_fx(c, tn, 'glow_doc', 0.34 * hg, skia.BlendMode.kPlus)
        draw_fx(c, tn, 'glow', 0.16 * hg, skia.BlendMode.kPlus)
    if fr is not None and DPF_Z0 - 24.0 < fr < DPF_Z1 + 20.0:
        band_layer(c, lambda: draw_fx(c, tn, 'glow'), wy_of_z(fr + 26.0), wy_of_z(fr - 30.0), 'band', blend=skia.BlendMode.kPlus, alpha=0.95)
        band_layer(c, lambda: draw_fx(c, tn, 'glow'), wy_of_z(fr + 9.0), wy_of_z(fr - 12.0), 'band', blend=skia.BlendMode.kPlus, alpha=0.7)


def tint_alpha(t):
    """inlet channels orange / outlet channels blue, from the close-up on the filter face until the sensors chapter."""
    return 0.26 * ramp(t, TL['face0'] + 2.6, 0.8) * (1 - ramp(t, TL['mac1'] + 0.2, 1.0)) + 0.22 * ramp(t, TL['ash0'] - 0.2, 0.8) * (1 - ramp(t, TL['ash1'], 1.0))


def hl(c, tn, kind, a, clip=None):
    """yellow highlight of a sensor group (mask + soft glow); clip = world rect."""
    if a <= 0.01: return
    if clip is not None:
        c.save(); c.clipRect(skia.Rect.MakeLTRB(*clip))
    draw_fx(c, tn, kind + 'g', 0.46 * a, skia.BlendMode.kPlus)
    draw_fx(c, tn, kind, 0.22 * a, skia.BlendMode.kPlus)
    if clip is not None: c.restore()


def wbox(pts3, pad=26):
    q = np.array(projs(pts3)); return (q[:, 0].min() - pad, q[:, 1].min() - pad, q[:, 0].max() + pad, q[:, 1].max() + pad)


CAB = INFO['cab']
HL_T = [(TL['sens0'] + 1.6, wbox(CAB['t1'])), (TL['sens0'] + 2.9, wbox(CAB['t2'])), (TL['sens0'] + 4.2, wbox(CAB['t3']))]
HL_L = TL['sens0'] + 0.3


def pulse(t, t0, hold=1.25):
    """highlight envelope: quick rise, hold, fade out (the part gets its own colour back)."""
    return ramp(t, t0, 0.25) * (1 - ramp(t, t0 + hold, 0.7))


def highlights(c, tn, t):
    if t < TL['sens0'] - 0.2 or t > TL['dp1'] + 0.5: return
    e = (1 - ramp(t, TL['sens1'] - 0.3, 0.5))
    if e > 0.01:
        hl(c, tn, 'hlL', pulse(t, HL_L) * e)
        for (t0, bx) in HL_T: hl(c, tn, 'hlT', pulse(t, t0) * e, bx)
    e2 = ramp(t, TL['dp0'], 0.3) * (1 - ramp(t, TL['dp1'] - 0.4, 0.5))
    if e2 > 0.01:
        hl(c, tn, 'hlPipe', pulse(t, TL['dp0'] + 0.2, 2.6) * e2)
        hl(c, tn, 'hlHose', pulse(t, TL['dp0'] + 1.5, 1.8) * e2)
        hl(c, tn, 'hlDps', pulse(t, TL['dp0'] + 2.4, 2.0) * e2)


# ------------------------------------------------------------------ flows
def flow_poly(pts3): return Poly(projs(pts3))


def streak(c, p, q, w, col, a, glow=True, head=True):
    if a < 0.02: return
    if glow: c.drawLine(q[0], q[1], p[0], p[1], P(col, a * 0.20, stroke=w * 3.2))
    c.drawLine(q[0], q[1], p[0], p[1], P(col, a, stroke=w * 1.5))
    if head: c.drawLine((q[0] + p[0]) / 2, (q[1] + p[1]) / 2, p[0], p[1], P('#ffffff', a * 0.75, stroke=w * 0.6))


# ---- wide streams: inlet pipe -> elbow -> cone -> catalyst -> filter -> cone -> elbow -> outlet
def build_streams():
    S = []
    IN_Z, IN_R, IN_PZ, OUT_Z, OUT_R, OUT_PZ = D['IN_Z'], D['IN_R'], D['IN_PZ'], D['OUT_Z'], D['OUT_R'], D['OUT_PZ']
    us = [-0.84, -0.63, -0.42, -0.21, 0.0, 0.21, 0.42, 0.63, 0.84]
    for k, u in enumerate(us):
        o = u * (D['R_IN'] - 5.0); xb = u * (R_B - 7.0); o2 = u * (D['R_OUT'] - 5.0)
        pts = [(D['IN_X0'] - 46.0, 1.0, IN_PZ + o), (-IN_R, 1.0, IN_PZ + o)]
        for i in range(1, 13):
            th = (math.pi / 2) * (1 - i / 12)
            pts.append((-IN_R + (IN_R + o) * math.cos(th), 1.0, IN_Z + (IN_R + o) * math.sin(th)))
        for i in range(1, 11):
            f = i / 10; g = sm(f)
            pts.append((lerp(o, xb, g), 1.0, lerp(IN_Z, DOC_Z1 + 3.0, f)))
        s_doc = len(pts)
        pts += [(xb, 1.0, DOC_Z0), (xb, 1.0, DPF_Z1)]
        i_dpf0 = len(pts) - 1
        pts.append((xb, 1.0, DPF_Z0)); i_dpf1 = len(pts) - 1
        for i in range(1, 11):
            f = i / 10; g = sm(f)
            pts.append((lerp(xb, o2, g), 1.0, lerp(DPF_Z0 - 4.0, OUT_Z, f)))
        for i in range(1, 13):
            th = (math.pi / 2) * i / 12
            pts.append((OUT_R - (OUT_R - o2) * math.cos(th), 1.0, OUT_Z - (OUT_R - o2) * math.sin(th)))
        pts.append((D['OUT_X1'] + 46.0, 1.0, OUT_PZ + o2))
        poly = flow_poly(pts)
        S.append(dict(poly=poly, s0=float(poly.cum[i_dpf0]), s1=float(poly.cum[i_dpf1]), k=k))
    return S


STREAMS = build_streams()


def gas_speed(t):
    return ramp(t, TL['open1'] + 0.2, 1.2)


_TT = np.arange(0, 82.0, 1 / FPS)
_PH = np.concatenate([[0], np.cumsum([gas_speed(x) / FPS for x in _TT[:-1]])])            # integrated "flow time"


def flow_time(t):
    i = min(len(_TT) - 1, max(0, int(round(t * FPS)))); return float(_PH[i])


def wide_flow(c, t, z, a):
    if a <= 0.02: return
    ft = flow_time(t); speed = 330.0; sp = 62.0; w = 2.5 / z
    gc, cc = hexc(C_GAS), hexc(C_CLN)
    for S in STREAMS:
        poly = S['poly']; L = poly.L
        d = ft * speed + S['k'] * 23.0
        i1 = int(math.floor(d / sp)); i0 = int(math.ceil((d - L) / sp))
        for i in range(i0, i1 + 1):
            s = d - i * sp
            if s < 0 or s > L: continue
            pt, _ = poly.at(np.array([s, max(0.0, s - sp * 0.5)]))
            ssw = S['s0'] + (0.10 + 0.82 * h01(i * 7.31 + S['k'] * 3.7)) * (S['s1'] - S['s0'])
            col = mix(gc, cc, sm((s - ssw) / 36.0 + 0.5))
            fa = min(1.0, s / (1.4 * sp), (L - s) / (1.4 * sp))
            streak(c, pt[0], pt[1], w, col, a * fa)


# ---- channel flow (close-ups): down an inlet channel, through the porous wall, down the neighbouring outlet channel
CELLS = LAT['dpf']['cells']                         # [xa, xb, is_inlet] of the cut row
HW = (LAT['dpf']['pitch'] - LAT['dpf']['wall']) / 2
_JC = int(np.argmin([abs((xa + xb) / 2 - XM) for xa, xb, _ in CELLS]))
J_IN = _JC if CELLS[_JC][2] else _JC + 1
X_IN = (CELLS[J_IN][0] + CELLS[J_IN][1]) / 2; X_OUT = (CELLS[J_IN + 1][0] + CELLS[J_IN + 1][1]) / 2
X_WALL = (CELLS[J_IN - 1][1] + CELLS[J_IN][0]) / 2                    # wall on the left of that inlet channel


def _bez(P0, P1, P2, P3, n=10):
    out = []
    for k in range(1, n + 1):
        f = k / n; u = 1 - f
        out.append((u ** 3 * P0[0] + 3 * u * u * f * P1[0] + 3 * u * f * f * P2[0] + f ** 3 * P3[0],
                    u ** 3 * P0[1] + 3 * u * u * f * P1[1] + 3 * u * f * f * P2[1] + f ** 3 * P3[1]))
    return out


class ChanFlow:
    """particles in the mm plane (x, z) of the section, projected at y = 0.36 mm (inside the half channels)."""
    def __init__(self, x0, x1, z_top, z_bot, zc_lo, zc_hi, seed, n_per=22, top_spread=0.0, z_face=None, blue_from_top=False, speed=5.0):
        rng = np.random.default_rng(seed); self.P = []; self.speed = speed
        idx = [j for j, (xa, xb, ii) in enumerate(CELLS) if xb > x0 and xa < x1 and 0 < j < len(CELLS) - 1]
        for j in idx:
            xa, xb, is_in = CELLS[j]; xc = (xa + xb) / 2
            if is_in:
                for n in range(n_per):
                    lane = (n % 3 - 1) * 0.40 + rng.uniform(-0.07, 0.07); xi = xc + lane
                    sd = 1 if rng.random() < 0.5 else -1
                    if not (0 <= j + sd < len(CELLS)) or CELLS[j + sd][2] != 0: sd = -sd
                    if not (0 <= j + sd < len(CELLS)) or CELLS[j + sd][2] != 0: continue
                    oa, ob, _ = CELLS[j + sd]; xo = (oa + ob) / 2 - sd * rng.uniform(0.05, 0.50)
                    zc = rng.uniform(zc_lo, zc_hi)
                    pts = []
                    if z_face is not None:                              # comes down through the gap and funnels into the open channel
                        xs = xi + rng.uniform(-top_spread, top_spread)
                        pts.append((xs, z_top)); zs = z_top
                        if z_top > DOC_Z0 + 1.0:
                            zs = DOC_Z0 + 1.0; pts.append((xs, zs))
                        g = zs - z_face
                        pts += _bez((xs, zs), (xs, zs - g * 0.35), (xi, z_face + g * 0.40), (xi, z_face + 0.6), 10)
                    else: pts += [(xi, z_top)]
                    cross = zc > z_bot + 2.0
                    if cross:
                        pts.append((xi, zc + 1.5)); i_w = len(pts)
                        pts += _bez((xi, zc + 1.5), (xi, zc + 0.15), (xo, zc - 0.15), (xo, zc - 1.5), 12)
                        pts.append((xo, z_bot))
                    else:
                        pts.append((xi, z_bot)); i_w = None
                    pw = Poly(pts)
                    xw = xb if sd > 0 else xa                                   # inlet-side surface of the wall that is crossed
                    s_w = None
                    if cross:
                        seg = np.array(pts[i_w - 1:i_w + 12]); dd = np.abs(seg[:, 0] - xw); kk = int(np.argmin(dd))
                        s_w = float(pw.cum[i_w - 1 + kk])
                    self.P.append(dict(mm=pw, s_w=s_w, xw=xw, sd=sd, ph=((n * 0.618034) % 1.0 + rng.uniform(-0.02, 0.02)) % 1.0, dirty=True, zc=zc))
            elif blue_from_top:
                for n in range(n_per // 2):
                    xo = xc + (n % 3 - 1) * 0.40 + rng.uniform(-0.07, 0.07)
                    self.P.append(dict(mm=Poly([(xo, z_top), (xo, z_bot)]), s_w=-1.0, xw=None, sd=0, ph=rng.random(), dirty=False, zc=None))
        self.L = max(p['mm'].L for p in self.P)

    def draw(self, c, t, z, a, a_soot, ft, V):
        if a <= 0.02: return
        w = (2.7 if z > 12 else 2.3) / z; gc, cc = hexc(C_GAS), hexc(C_CLN)
        lenmm = (46.0 if z > 12 else 38.0) / (z * PXMM)                 # streak length on screen (px)
        for p in self.P:
            L = p['mm'].L
            s = ((ft * self.speed / self.L + p['ph']) % 1.0) * self.L
            if s > L: continue
            pt, _ = p['mm'].at(np.array([s, max(0.0, s - lenmm)]))
            A = proj((pt[0][0], 0.36, pt[0][1])); B = proj((pt[1][0], 0.36, pt[1][1]))
            sx, sy = to_screen(V, A)
            if sx < -80 or sx > W + 80 or sy < -160 or sy > H + 160: continue
            if p['s_w'] is None: col = gc
            elif p['s_w'] < 0: col = cc
            else: col = mix(gc, cc, sm((s - p['s_w']) / 0.5 + 0.2))
            fa = min(1.0, s / 1.5, (L - s) / 1.5)
            streak(c, A, B, w, col, a * fa, glow=z < 12)
            if a_soot > 0.02 and p['dirty']:
                # soot specks ride with the gas and stay on the inlet side of the wall
                for kk, back in enumerate((0.45, 1.05, 1.7)):
                    ss = s - back * lenmm * 1.3
                    if ss < 0: continue
                    stuck = p['s_w'] is not None and ss > p['s_w']
                    sq = p['s_w'] if stuck else ss
                    (qx, qz) = p['mm'].at(np.array([sq]))[0][0]
                    fade = 1.0 if not stuck else 1.0 - cl((ss - p['s_w']) / 4.0)
                    if fade <= 0.02: continue
                    Q = proj(((p['xw'] - 0.07 * p['sd']) if stuck else qx, 0.2, qz + (kk - 1) * 0.12))
                    rr = (3.4 + 0.7 * kk) / z
                    c.drawCircle(Q[0], Q[1], rr, P('#050505', a_soot * fade * fa))
                    c.drawCircle(Q[0], Q[1], rr, P('#d8cfc0', a_soot * fade * fa * 0.42, stroke=0.9 / z))


CF_F = ChanFlow(XM - 37.0, XM + 37.0, 36.0, -54.0, -72.0, -2.5, seed=3, n_per=14, top_spread=0.55, z_face=DPF_Z1)     # close-up on the filter face
CF_A = ChanFlow(XM - 15.0, XM + 15.0, 8.0, -28.0, -40.0, -2.5, seed=4, n_per=30, top_spread=0.45, z_face=DPF_Z1)      # macro, inlet end
CF_B = ChanFlow(XM - 15.0, XM + 15.0, -150.0, DPF_Z0 - 9.0, DPF_Z0 + PLUG + 1.2, -154.0, seed=5, n_per=26, blue_from_top=True)   # macro, outlet end


def chan_speed(z):
    """mm/s so that the particles move ~330 px/s on screen, within limits."""
    return max(4.4, min(11.0, 330.0 / (z * PXMM)))


_CS = np.concatenate([[0], np.cumsum([chan_speed(main_view(x)[0]) / 5.0 / FPS for x in _TT[:-1]])])       # integrated, in units of the base speed


def chan_time(t):
    i = min(len(_TT) - 1, max(0, int(round(t * FPS)))); return float(_CS[i])


# ---- soot layer / ash in the macro views (drawn from the lattice, in mm)
_RN = np.random.default_rng(11).random(4096)


def _noise(i, salt=0): return float(_RN[(i * 7919 + salt * 104729) % 4096])


def quad_mm(c, x0, x1, z0, z1, paint, y=0.0):
    c.drawPath(path_of([proj((x0, y, z0)), proj((x1, y, z0)), proj((x1, y, z1)), proj((x0, y, z1))], True), paint)


def macro_soot(c, t, zr, x0, x1, fr=None):
    """soot cake on the inlet channel walls between heights zr = (lo, hi)."""
    s = soot_load(t)
    if s <= 0.01: return
    lo, hi = zr
    if fr is not None: hi = min(hi, fr)
    if hi <= lo: return
    dmax = 0.30 * s
    for j, (xa, xb, is_in) in enumerate(CELLS):
        if not is_in or xb < x0 or xa > x1: continue
        zb = max(lo, DPF_Z0 + PLUG); zt = min(hi, DPF_Z1)
        if zt <= zb: continue
        quad_mm(c, xa, xb, zb, zt, P(C_SOOT, 0.50 * s), y=0.0)                      # back of the channel gets dark
        for side in (0, 1):
            n = max(6, int((zt - zb) / 0.55)); pts_o = []
            xw = xa if side == 0 else xb; sg = 1 if side == 0 else -1
            for k in range(n + 1):
                zz = zb + (zt - zb) * k / n
                dd = dmax * (0.62 + 0.38 * _noise(int(zz * 3.1) + j * 57, side)) * (0.85 + 0.15 * cl((DPF_Z1 - zz) / 30.0))
                pts_o.append(proj((xw + sg * dd, 0.0, zz)))
            poly = [proj((xw, 0.0, zb))] + pts_o + [proj((xw, 0.0, zt))]
            c.drawPath(path_of(poly, True), P('#070707', 0.96 * min(1.0, s * 2.2)))
            c.drawPath(path_of(pts_o), P('#3a3632', 0.55 * s, stroke=0.016 * PXMM))


_ASHG = {}


def _ash_grains(j, xa, xb):
    if j not in _ASHG:
        rng = np.random.default_rng(100 + j); n = 240
        _ASHG[j] = (rng.uniform(xa + 0.05, xb - 0.05, n), rng.uniform(0.04, 8.6, n), rng.uniform(0.02, 0.05, n), rng.uniform(0.0, 1.0, n))
    return _ASHG[j]


def macro_ash(c, t, x0, x1):
    """ash plug growing above the plugs at the closed end of the inlet channels."""
    hgt = ash_h(t)
    if hgt <= 0.05: return
    for j, (xa, xb, is_in) in enumerate(CELLS):
        if not is_in or xb < x0 or xa > x1: continue
        zb = DPF_Z0 + PLUG; hh = hgt * (0.82 + 0.3 * _noise(j, 3)); zt = zb + hh
        n = 9; top = []
        for k in range(n + 1):
            xx = xa + (xb - xa) * k / n
            top.append(proj((xx, 0.0, zt + 0.22 * (_noise(j * 13 + k, 5) - 0.5) - 0.25 * abs(k / n - 0.5))))
        poly = [proj((xa, 0.0, zb))] + top + [proj((xb, 0.0, zb))]
        c.drawPath(path_of(poly, True), P(C_ASH, 0.97))
        gx, gz, gr, gg = _ash_grains(j, xa, xb)
        for i in np.nonzero(gz < hh - 0.25)[0]:
            q = proj((gx[i], 0.0, zb + gz[i]))
            c.drawCircle(q[0], q[1], gr[i] * PXMM, P(mix('#8f897a', '#e9e4d6', gg[i]), 0.9))
        c.drawPath(path_of(top), P('#f1ecdf', 0.8, stroke=0.035 * PXMM))


def ash_fall(c, t, z, x0, x1, ft):
    """light ash grains drifting down the inlet channels towards the plugs."""
    a = win(t, TL['ash0'] + 0.2, TL['ash1'] - 0.4, 0.6, 0.6)
    if a <= 0.02: return
    for j, (xa, xb, is_in) in enumerate(CELLS):
        if not is_in or xb < x0 or xa > x1: continue
        zb = DPF_Z0 + PLUG + ash_h(t) * 0.9
        for n in range(7):
            ph = (_noise(j * 31 + n, 9) + ft * 0.11 * (0.8 + 0.4 * _noise(n, j))) % 1.0
            zz = lerp(DPF_Z0 + 26.0, zb, ph); xx = xa + (xb - xa) * (0.15 + 0.7 * _noise(j * 17 + n, 2)) + 0.12 * math.sin(ph * 9 + n)
            q = proj((xx, 0.3, zz))
            c.drawCircle(q[0], q[1], 2.6 / z, P('#ece7d8', a * min(1.0, ph * 6, (1 - ph) * 6 + 0.2)))


def wall_arrows(c, t, z, a, zr, x0, x1):
    """small chevrons sliding through the porous walls, from each inlet channel into its outlet neighbours."""
    if a <= 0.02: return
    gc, cc = hexc(C_GAS), hexc(C_CLN); lo, hi = zr
    for j, (xa, xb, is_in) in enumerate(CELLS):
        if not is_in or xb < x0 or xa > x1: continue
        for sd in (-1, 1):
            if not (0 <= j + sd < len(CELLS)) or CELLS[j + sd][2] != 0: continue
            xin = xb if sd > 0 else xa; xout = CELLS[j + sd][0] if sd > 0 else CELLS[j + sd][1]
            n = int((hi - lo) / 3.3)
            for k in range(n):
                zz = hi - 2.0 - k * 3.3 - (1.1 if sd > 0 else 0.0)
                if zz < lo: continue
                ph = (t * 0.55 + 0.37 * k + (0.5 if sd > 0 else 0.0) + 0.13 * j) % 1.0
                xx = lerp(xin - sd * 0.30, xout + sd * 0.34, ph); al = a * math.sin(math.pi * ph) ** 1.2
                col = mix(gc, cc, sm((ph - 0.3) / 0.4))
                tip = proj((xx, 0.0, zz)); u1 = proj((xx - sd * 0.30, 0.0, zz + 0.29)); u2 = proj((xx - sd * 0.30, 0.0, zz - 0.29))
                for wgt, cl_, aa in ((6.5, '#0b1424', al * 0.6), (3.4, col, al)):
                    c.drawPath(path_of([u1, tip, u2]), P(cl_, aa, stroke=wgt / z, join='miter'))


# ---- pressure pulses in the two pipes
PIPE1 = flow_poly(INFO['paths3d']['p1'] + INFO['paths3d']['hose1'] + [(D['PORT_X1'], D['Y_P'], D['PORT_Z'] + 22.0)])
PIPE2 = flow_poly(INFO['paths3d']['p2'] + INFO['paths3d']['hose2'] + [(D['PORT_X2'], D['Y_P'], D['PORT_Z'] + 22.0)])


def pulses(c, t, z):
    a = ramp(t, TL['dp0'] + 0.3, 0.5) * (1 - ramp(t, TL['dp1'] - 0.3, 0.5))
    if a <= 0.02: return
    for poly, col, t0, ph in ((PIPE1, C_GAS, TL['dp0'] + 0.3, 0.0), (PIPE2, C_CLN, TL['dp0'] + 1.3, 0.5)):
        aa = a * ramp(t, t0, 0.4)
        if aa <= 0.02: continue
        L = poly.L; sp = 46.0; sp_px = 150.0
        front = (t - t0) * 330.0
        d = t * sp_px + ph * sp
        n = int(L // sp) + 2
        for i in range(n):
            s = (d % sp) + i * sp
            if s > L or s > front: continue
            pt, _ = poly.at(np.array([s, max(0.0, s - 16.0)]))
            fa = min(1.0, s / 30.0, (L - s) / 30.0)
            c.drawLine(pt[1][0], pt[1][1], pt[0][0], pt[0][1], P(col, aa * fa * 0.28, stroke=9.0 / z))
            c.drawLine(pt[1][0], pt[1][1], pt[0][0], pt[0][1], P(col, aa * fa, stroke=4.4 / z))
            c.drawCircle(pt[0][0], pt[0][1], 1.6 / z, P('#ffffff', aa * fa * 0.9))


# ------------------------------------------------------------------ the scene
def scene(c, t, V):
    z, cx, cy = V
    c.save(); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-cx, -cy)
    fb = ramp(cy, wy_of_z(-95.0), wy_of_z(-135.0) - wy_of_z(-95.0))        # 0: inlet end of the filter in view ... 1: outlet end
    w2 = ramp(z, 0.72, 0.26)
    w8 = ramp(z, 2.0, 1.6) * (1 - ramp(cy, wy_of_z(-40.0), wy_of_z(-95.0) - wy_of_z(-40.0)))
    wa = ramp(z, 8.0, 7.0) * (1 - fb); wb = ramp(z, 2.8, 6.0) * fb; wm = max(wa, wb)
    ft = flow_time(t); ct = chan_time(t)
    under = wm < 0.999 or z < 21.5                 # the macro plates cover the whole frame only at the final macro zoom
    layers = [('T1', 1.0 if w2 < 0.999 else 0.0), ('T2', w2 if under else 0.0), ('T8', w8 if under else 0.0), ('TA', wa), ('TB', wb)]
    for tn, wgt in layers:
        if wgt <= 0.003 or img(tn + '_sec') is None: continue
        k, (x0, y0) = TIERS[tn]
        c.saveLayerAlpha(None, int(min(1.0, wgt) * 255))
        draw_im(c, img(tn + '_sec'), k, x0, y0)
        tier_fx(c, tn, t)
        if tn in ('T1', 'T2'): highlights(c, tn, t)
        if tn == 'TA': macro_soot(c, t, (-26.0, DPF_Z1), XM - 15.0, XM + 15.0)
        if tn == 'TB':
            macro_ash(c, t, XM - 15.0, XM + 15.0); ash_fall(c, t, z, XM - 15.0, XM + 15.0, ft)
        c.restore()
    # front half (cutaway reveal)
    rv = ramp(t, TL['open0'], TL['open1'] - TL['open0'])
    if rv < 0.999:
        k_ = eio(rv); ax, ay = proj((0.0, -40.0, -30.0))
        c.save(); c.translate(ax - 430 * k_, ay - 120 * k_); c.scale(1 + 0.5 * k_, 1 + 0.5 * k_); c.translate(-ax, -ay)
        draw_im(c, img('T1_front'), 1, 0, 0, alpha=1 - sm(rv * 1.12))
        c.restore()
    # gases
    a_w = ramp(t, TL['open1'] + 0.2, 0.8) * (1 - ramp(z, 3.2, 2.4))
    a_w *= 1 - 0.62 * win(t, TL['sens0'] - 0.3, TL['dp1'] + 0.4, 0.6, 0.6)
    wide_flow(c, t, z, a_w * 0.92)
    a_c = ramp(z, 3.4, 2.4)
    if a_c * fb > 0.02:
        CF_B.draw(c, t, z, a_c * fb * ramp(z, 9.0, 5.0) * 0.95, 0.0, ct, V)
        wall_arrows(c, t, z, fb * ramp(z, 9.0, 5.0), (DPF_Z0 + PLUG + 10.5, -152.0), XM - 15.0, XM + 15.0)
    if a_c * (1 - fb) > 0.02:
        wmac = ramp(z, 9.0, 5.0)
        CF_F.draw(c, t, z, a_c * (1 - fb) * (1 - wmac) * 0.95, 0.0, ct, V)
        CF_A.draw(c, t, z, a_c * (1 - fb) * wmac * 0.95, win(t, TL['soot0'], TL['mac1'] + 0.6, 0.7, 0.5), ct, V)
        wall_arrows(c, t, z, (1 - fb) * wmac * win(t, TL['mac0'] + 1.0, TL['mac1'] + 0.4, 0.6, 0.5), (-27.0, DPF_Z1 - 5.0), XM - 15.0, XM + 15.0)
    pulses(c, t, z)
    c.restore()


# ------------------------------------------------------------------ UI
def label(c, text, ax, ay, lx, ly, a, side='r', col=WHT, size=28, dot=Y):
    if a <= 0.01 or CLEAN: return
    lines = text.split('\n'); tw_ = max(tw(s_, size, 'm8') for s_ in lines); lh = size * 1.22
    bh = size * 1.34 + lh * (len(lines) - 1)
    x0 = lx if side == 'r' else lx - tw_ - 28
    x0 = max(14, min(W - tw_ - 42, x0)); y0 = ly - size * 0.86
    c.drawCircle(ax, ay, 6, P(dot, a)); c.drawCircle(ax, ay, 12, P(dot, a * 0.35, stroke=2))
    ex = x0 if ax < x0 else (x0 + tw_ + 28 if ax > x0 + tw_ + 28 else ax)
    ey = y0 + bh / 2 if (ax < x0 or ax > x0 + tw_ + 28) else (y0 if ay < y0 else y0 + bh)
    c.drawPath(path_of([(ax, ay), (ex, ey)]), P(dot, a * 0.85, stroke=2.4))
    rrect(c, x0, y0, x0 + tw_ + 28, y0 + bh, 12, P('#0b1424', a * 0.9))
    rrect(c, x0, y0, x0 + tw_ + 28, y0 + bh, 12, P(dot, a * 0.55, stroke=2))
    for i, s_ in enumerate(lines): txt(c, s_, x0 + 14, ly + i * lh, size, 'm8', col, a)


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
    x, y0, ts, bs, mw, lh = 60, 1562, 54, 35, 960, 47
    txt(c, title, x, y0 + dy, ts, 'anton', Y, a, shadow=10)
    yy = y0 + ts * 1.16 + dy
    for ln in wrap_lines(body, bs, 'm7', mw):
        txt(c, ln, x, yy, bs, 'm7', WHT, a, shadow=8); yy += lh


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


def watermark_over(c, t, a):
    """in the close-ups the plates cover the whole frame, so the mark goes over them, very faint (light + dark, readable on any ceramic)."""
    if a <= 0.01: return
    c.save(); c.rotate(-20, W / 2, H / 2)
    f = font('anton', 58); s = 'TURBO DOCTOR'; w = f.measureText(s) + 120; off = (t * 9) % w
    pw, pk = P('#ffffff', 0.034 * a), P('#000000', 0.040 * a)
    for row in range(-16, 26):
        yy = row * 110; sh = (row % 2) * w / 2
        for k in range(-4, 9):
            x = -600 + k * w + sh + off
            c.drawString(s, x + 2, yy + 2, f, pk); c.drawString(s, x, yy, f, pw)
    c.restore()


TITLE = ('FILTRUL DE PARTICULE (DPF)', 'cu catalizator de oxidare (DOC), în aceeași carcasă')
NOTE = 'MODEL 3D RECONSTRUIT'


def header(c, t):
    if CLEAN:
        txt(c, NOTE, W - 60, 64, 20, 'm8', WHT, 0.45, 'r'); return
    c.drawRect(skia.Rect.MakeLTRB(0, 0, W, 300), P(shader=lin(0, 0, 0, 300, [skia.Color4f(0.02, 0.04, 0.07, 0.94).toColor(), skia.Color4f(0.02, 0.04, 0.07, 0.84).toColor(),
                                                                             skia.Color4f(0.02, 0.04, 0.07, 0.0).toColor()], [0.0, 0.62, 1.0])))
    txt(c, TITLE[0], 60, 122, 56, 'anton', WHT, 1.0, shadow=8)
    txt(c, TITLE[1], 62, 168, 27, 'm7', WHT, 0.84)
    txt(c, NOTE, 1020, 64, 20, 'm8', WHT, 0.45, 'r')


def bottom_band(c):
    if CLEAN: return
    c.drawRect(skia.Rect.MakeLTRB(0, 1400, W, H), P(shader=lin(0, 1400, 0, 1610, [skia.Color4f(0.02, 0.04, 0.07, 0.0).toColor(), skia.Color4f(0.02, 0.04, 0.07, 0.90).toColor()])))


def legend(c, a, items):
    if a <= 0.01 or CLEAN: return
    x, y = 60, 1872
    for col, s in items:
        c.drawRoundRect(skia.Rect.MakeXYWH(x, y - 22, 26, 26), 6, 6, P(col, a))
        c.drawRoundRect(skia.Rect.MakeXYWH(x, y - 22, 26, 26), 6, 6, P('#ffffff', a * 0.35, stroke=1.5))
        txt(c, s, x + 38, y, 25, 'm7', WHT, a * 0.9); x += 38 + tw(s, 25, 'm7') + 30


def gauge(c, a, lv):
    """two bars: pressure before / after the filter; the gap between them is the differential pressure."""
    if a <= 0.01 or CLEAN: return
    x0, y0 = 60, 1770; lw = 268; bx = x0 + lw; full = 620.0
    b_after = 0.22 * full; b_before = b_after + (0.05 + 0.60 * lv) * full
    rrect(c, x0 - 18, y0 - 44, W - 42, y0 + 104, 18, P('#0b1424', a * 0.92)); rrect(c, x0 - 18, y0 - 44, W - 42, y0 + 104, 18, P('#ffffff', a * 0.16, stroke=1.5))
    txt(c, 'înainte de filtru', x0, y0, 25, 'm7', WHT, a * 0.92)
    txt(c, 'după filtru', x0, y0 + 58, 25, 'm7', WHT, a * 0.92)
    rrect(c, bx, y0 - 22, bx + b_before, y0 + 8, 8, P(C_GAS, a))
    rrect(c, bx, y0 + 36, bx + b_after, y0 + 66, 8, P(C_CLN, a))
    # the difference
    xa, xb = bx + b_after, bx + b_before
    c.drawLine(xa, y0 + 20, xa, y0 + 86, P(Y, a * 0.9, stroke=2.5)); c.drawLine(xb, y0 + 12, xb, y0 + 86, P(Y, a * 0.9, stroke=2.5))
    c.drawLine(xa, y0 + 80, xb, y0 + 80, P(Y, a, stroke=3.5))
    for xx, sg in ((xa, 1), (xb, -1)):
        if xb - xa > 26: c.drawPath(path_of([(xx, y0 + 80), (xx + sg * 11, y0 + 73), (xx + sg * 11, y0 + 87)], True), P(Y, a))
    txt(c, 'Δp', (xa + xb) / 2, y0 + 70, 30, 'm9', Y, a, 'c', stroke=6, scol='#0b1424')
    txt(c, 'valori ilustrative', W - 62, y0 - 20, 18, 'm7', WHT, a * 0.5, 'r')


def temp_tag(c, V, t):
    a = win(t, TL['reg0'] + 0.9, TL['reg1'] - 0.2, 0.4, 0.5)
    if a <= 0.01 or CLEAN: return
    ax, ay = anchor(V, 't2_tip')
    x0, y0 = 646, 590
    c.drawPath(path_of([(ax, ay), (x0 + 20, y0 + 74)]), P(C_HOT, a * 0.9, stroke=2.4)); c.drawCircle(ax, ay, 6, P(C_HOT, a))
    rrect(c, x0, y0, x0 + 392, y0 + 74, 16, P('#1a0d06', a * 0.94)); rrect(c, x0, y0, x0 + 392, y0 + 74, 16, P(C_HOT, a * 0.9, stroke=2.5))
    txt(c, '600–650 °C', x0 + 20, y0 + 53, 46, 'anton', '#ffd9a8', a)
    txt(c, 'înainte', x0 + 262, y0 + 32, 20, 'm8', WHT, a * 0.85); txt(c, 'de filtru', x0 + 262, y0 + 56, 20, 'm8', WHT, a * 0.85)


def summary(c, t):
    a = win(t, TL['sum0'], TL['sum1'], 0.5, 0.4)
    if a <= 0.01 or CLEAN: return
    c.drawRect(skia.Rect.MakeWH(W, H), P('#060b14', a * 0.72))
    txt(c, 'PE SCURT', 60, 520, 84, 'anton', Y, a, shadow=10)
    yy = 640
    for i, s_ in enumerate(('Catalizatorul de oxidare și filtrul de particule stau în aceeași carcasă.',
                            'Filtrul are canalele închise alternativ: gazele trec prin pereți, funinginea rămâne.',
                            'Senzorii de temperatură și senzorul de presiune diferențială îi arată calculatorului cât de încărcat e filtrul și când să-l regenereze.',
                            'Funinginea arde la regenerare. Cenușa rămâne în filtru.')):
        ai = a * ramp(t, TL['sum0'] + 0.3 + i * 0.45, 0.4)
        c.drawCircle(76, yy - 13, 9, P(Y, ai))
        for ln in wrap_lines(s_, 37, 'm7', 880):
            txt(c, ln, 106, yy, 37, 'm7', WHT, ai, shadow=6); yy += 50
        yy += 30


def endcard(c, t, a):
    if a <= 0.01 or CLEAN: return
    c.drawRect(skia.Rect.MakeWH(W, H), P('#060b14', a * 0.95))
    cx = W / 2; cy = H / 2 - 40; big = 170
    txt(c, 'TURBO', cx, cy - 200, big, 'anton', WHT, a, 'c')
    txt(c, 'DOCTOR', cx, cy - 200 + big * 1.03, big, 'anton', Y, a, 'c')
    y2 = cy - 200 + big * 1.03 + 60
    rrect(c, cx - 310, y2 + 50, cx + 310, y2 + 140, 26, P(Y, a)); txt(c, 'DIAGNOZĂ GRATUITĂ', cx, y2 + 110, 40, 'm9', BG, a, 'c')
    txt(c, '0739 065 065', cx, y2 + 250, 96, 'anton', WHT, a, 'c')
    txt(c, 'GALAȚI · BUCUREȘTI · IAȘI · PIATRA NEAMȚ', cx, y2 + 330, 30, 'm8', WHT, a * 0.85, 'c')


# ---------------- labels: (text, anchor key or 3D point, label position on screen, side)
LB_EXT = [('Intrare: gaze de la turbină', 'inlet', (60, 290), 'r'), ('Ieșire spre eșapament', 'outlet', (1020, 1440), 'l')]
LB_WIDE = [('Catalizator de oxidare (DOC)', 'doc', (60, 350), 'r'), ('Filtru de particule (DPF)', (-42.0, 0.0, -150.0), (60, 1400), 'r'),
           ('Saltea de fixare', 'mat_dpf', (60, 1180), 'r'), ('Carcasă de inox', (D['R_SO'], 0.0, -150.0), (1020, 1330), 'l')]
LB_FACE = [('Catalizator: canale deschise\nla ambele capete', (XM - 14.0, 0.0, 26.0), (60, 330), 'r'),
           ('Dopuri ceramice', (XM + 9.9, 0.0, -3.0), (1020, 1240), 'l'),
           ('Filtru: canale închise alternativ', (XM - 9.0, 0.0, -22.0), (60, 1390), 'r')]
LB_MAC = [('Canal de intrare', (X_IN, 0.0, -10.5), (60, 1150), 'r'), ('Dop', (X_OUT, 0.0, -3.0), (1020, 640), 'l'),
          ('Perete poros', (X_WALL, 0.0, -8.5), (60, 960), 'r'), ('Canal de ieșire', (X_OUT, 0.0, -13.5), (1020, 1380), 'l')]
LB_SOOT = [('Strat de funingine', (CELLS[J_IN][0] + 0.12, 0.0, -12.0), (60, 1280), 'r')]
LB_SENS = [('Sondă lambda', 'lam', (1020, 300), 'l', HL_L), ('Senzor de temperatură\nînainte de catalizator', 't1', (40, 520), 'r', HL_T[0][0]),
           ('Senzor de temperatură\nînainte de filtru', 't2', (40, 760), 'r', HL_T[1][0]), ('Senzor de temperatură\ndupă filtru', 't3', (40, 1420), 'r', HL_T[2][0])]
LB_DPW = [('Priză de presiune\nînainte de filtru', 'p1', (1040, 920), 'l', TL['dp0'] + 0.3), ('Priză de presiune\ndupă filtru', 'p2', (1040, 1440), 'l', TL['dp0'] + 1.3),
          ('Senzor de presiune\ndiferențială', 'dps', (1040, 300), 'l', TL['dp0'] + 2.4)]
LB_DPS = [('Senzor de presiune diferențială', 'dps_sock', (1040, 300), 'l'), ('Furtunașe flexibile', 'hose2', (1040, 900), 'l'),
          ('Țevi metalice, de la cele\ndouă prize de pe carcasă', 'pipe2x', (1040, 1230), 'l')]
LB_REG = [('Catalizatorul încălzește gazele', 'doc', (60, 350), 'r')]
LB_ASH = [('Dop', (X_IN, 0.0, DPF_Z0 + 3.0), (60, 1260), 'r'), ('Gaze filtrate, spre ieșire', (X_OUT, 0.0, DPF_Z0 + 2.0), (1020, 1330), 'l'),
          ('Cenușă', (X_IN, 0.0, DPF_Z0 + PLUG + 2.6), (60, 640), 'r')]


def draw_labels(c, t, V, items, t0, t1, step=0.36):
    a0 = win(t, t0, t1, 0.3, 0.45)
    if a0 <= 0.01: return
    for i, it in enumerate(items):
        s_, key, off, side = it[:4]
        ts = it[4] if len(it) > 4 else t0 + 0.15 + i * step
        a = a0 * ramp(t, ts, 0.3)
        ax, ay = anchor(V, p3=key) if isinstance(key, tuple) else anchor(V, key)
        label(c, s_, ax, ay, off[0], off[1], a, side)


CAPS = [
    (0.5, TL['open0'] + 0.2, 'FILTRUL, VĂZUT DIN AFARĂ', 'O carcasă de inox, montată de obicei imediat după turbină, cu senzorii pe ea.'),
    (TL['open1'] + 0.9, TL['wide1'] - 0.1, 'DOUĂ PIESE, O SINGURĂ CARCASĂ', 'Gazele trec întâi prin catalizatorul de oxidare, apoi prin filtrul de particule.'),
    (TL['face0'] + 0.2, TL['face1'] - 0.1, 'CANALE ÎNCHISE ALTERNATIV', 'La filtru, fiecare canal e astupat la un capăt: unul la ieșire, vecinul lui la intrare.'),
    (TL['mac0'] + 0.2, TL['soot0'] - 0.1, 'GAZELE TREC PRIN PEREȚI', 'Canalul de intrare e închis la capăt. Gazele scapă doar prin pereții poroși, în canalele vecine.'),
    (TL['soot0'] + 0.2, TL['mac1'] - 0.1, 'FUNINGINEA RĂMÂNE ÎN FILTRU', 'Particulele nu trec prin perete. Se așază strat cu strat în canalele de intrare.'),
    (TL['sens0'] + 0.2, TL['sens1'] - 0.1, 'SENZORII DE PE CARCASĂ', 'Sonda lambda măsoară oxigenul din gaze. Senzorii de temperatură urmăresc gazele înainte de catalizator, înainte de filtru și după filtru.'),
    (TL['dp0'] + 0.2, TL['dpz0'] + 0.3, 'DOUĂ PRIZE DE PRESIUNE', 'Una înainte de filtru, una după. Țevile duc cele două presiuni la senzor.'),
    (TL['dpz1'] + 0.1, TL['dp1'] - 0.1, 'PRESIUNEA DIFERENȚIALĂ', 'Cu cât filtrul e mai încărcat, cu atât diferența dintre cele două presiuni e mai mare.'),
    (TL['reg0'] + 0.2, TL['reg1'] - 0.1, 'REGENERAREA', 'Calculatorul ridică temperatura gazelor și funinginea adunată arde.'),
    (TL['ash0'] + 0.2, TL['ash1'] - 0.1, 'CENUȘA RĂMÂNE', 'Cenușa din ulei nu arde. Se strânge la capătul canalelor de intrare și, cu timpul, înfundă filtrul.'),
]


def frame(t):
    surf = skia.Surface(W, H); c = surf.getCanvas()
    background(c, t)
    V = main_view(t)
    scene(c, t, V)
    watermark_over(c, t, ramp(V[0], 2.0, 2.5))
    bottom_band(c)
    header(c, t)
    draw_labels(c, t, V, LB_EXT, 0.9, TL['open0'] + 0.1)
    draw_labels(c, t, V, LB_WIDE, TL['open1'] + 0.5, TL['wide1'] - 0.1)
    draw_labels(c, t, V, LB_FACE, TL['face0'] + 0.3, TL['face1'] - 0.1, 0.9)
    draw_labels(c, t, V, LB_MAC, TL['mac0'] + 0.5, TL['soot0'] - 0.1, 0.7)
    draw_labels(c, t, V, LB_SOOT, TL['soot0'] + 2.2, TL['mac1'] - 0.1)
    draw_labels(c, t, V, LB_SENS, TL['sens0'] + 0.1, TL['sens1'] - 0.1)
    draw_labels(c, t, V, LB_DPW, TL['dp0'] + 0.1, TL['dpz0'] + 0.2)
    draw_labels(c, t, V, LB_DPS, TL['dpz1'] + 0.2, TL['dp1'] - 0.1, 0.6)
    draw_labels(c, t, V, LB_REG, TL['reg0'] + 0.6, TL['reg1'] - 0.1, 1.6)
    fr = burn_front(t)
    if fr is not None and DPF_Z0 + 4.0 < fr < DPF_Z1 - 4.0:                 # the label follows the burning front
        ax, ay = anchor(V, p3=(-56.0, 0.0, fr))
        label(c, 'Funinginea arde', ax, ay, 34, ay + 9, win(t, TL['burn0'] + 0.5, TL['burn1'] - 0.2, 0.3, 0.3), 'r')
    draw_labels(c, t, V, LB_ASH, TL['ash0'] + 0.5, TL['ash1'] - 0.1, 0.8)
    temp_tag(c, V, t)
    for (t0, t1, ti, body) in CAPS:
        caption(c, ti, body, win(t, t0, t1, 0.4, 0.4))
    a_g = win(t, TL['dpz1'] + 1.0, TL['dp1'] - 0.1, 0.5, 0.4) + win(t, TL['reg0'] + 0.8, TL['reg1'] - 0.1, 0.5, 0.4)
    gauge(c, a_g, dp_level(t))
    leg = [(C_GAS, 'gaze cu funingine'), (C_CLN, 'gaze filtrate')]
    legend(c, ramp(t, TL['open1'] + 0.4, 0.5) * (1 - ramp(t, TL['sum0'] - 0.3, 0.4)) * (1 - a_g), leg)
    summary(c, t)
    endcard(c, t, ramp(t, TL['end0'], 0.7))
    return surf.makeImageSnapshot()


def render(out, f0=0, f1=None):
    n = int(round(DUR * FPS)); f1 = n if f1 is None else min(f1, n)
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-vf', 'scale=out_color_matrix=bt709:out_range=tv', '-c:v', 'libx264', '-preset', 'medium', '-crf', '22', '-pix_fmt', 'yuv420p',
                          '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    for fi in range(f0, f1):
        p.stdin.write(frame(fi / FPS).toarray(colorType=skia.kRGBA_8888_ColorType).tobytes())
    p.stdin.close()
    if p.wait() != 0: raise SystemExit('ffmpeg failed')


SEGS = [0.0, 5.2, 12.8, 20.4, 30.9, 39.3, 51.2, 59.6, 67.0, 72.8]          # chapter cuts (s): one encoded file per chapter


def seg_frames():
    n = int(round(DUR * FPS)); b = [int(round(s_ * FPS)) for s_ in SEGS if s_ * FPS < n - 15] + [n]
    return list(zip(b, b[1:]))


def render_segments(out, jobs=2, force=()):
    """one file per chapter (a changed chapter is rendered again without touching the others), joined without re-encoding."""
    d = out + '.seg'; os.makedirs(d, exist_ok=True)
    segs = seg_frames(); todo = []
    for i, (f0, f1) in enumerate(segs):
        p = os.path.join(d, f'{i:02d}.mp4')
        if not os.path.exists(p) or i in force: todo.append((i, f0, f1, p))
    running = []
    while todo or running:
        while todo and len(running) < jobs:
            i, f0, f1, p = todo.pop(0); tmp = p[:-4] + '.tmp.mp4'
            pr = subprocess.Popen([sys.executable, os.path.abspath(__file__), '--out', tmp, '--frames', str(f0), str(f1)], stderr=open(p + '.log', 'w'))
            running.append((pr, tmp, p, i))
        for r in list(running):
            if r[0].poll() is None: continue
            running.remove(r)
            if r[0].returncode != 0 or not os.path.exists(r[1]): raise SystemExit(f'chapter {r[3]} failed, see {r[2]}.log')
            os.replace(r[1], r[2]); print('chapter', r[3], 'done', flush=True)
        time.sleep(0.5)
    lst = os.path.join(d, 'list.txt')
    with open(lst, 'w') as f:
        for i in range(len(segs)): f.write(f"file '{i:02d}.mp4'\n")
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', '-movflags', '+faststart', out], check=True)


STILLS = [('01_exterior', 2.2), ('02_sectiune', 10.5), ('03_fata_filtrului', 18.5), ('04_canale_gaze', 24.8), ('05_canale_funingine', 29.6),
          ('06_senzori', 37.6), ('07_presiune_diferentiala', 48.5), ('08_regenerare', 55.4), ('09_cenusa', 65.2)]

if __name__ == '__main__':
    a = sys.argv[1:]
    if '--stills' in a:
        os.makedirs(os.path.join(HERE, 'stills'), exist_ok=True)
        for nm, ts in STILLS:
            arr = frame(ts).toarray(colorType=skia.kRGBA_8888_ColorType)
            cv2.imwrite(os.path.join(HERE, 'stills', f'TurboDoctor_DPF_{nm}.jpg'), cv2.cvtColor(arr, cv2.COLOR_RGBA2BGR), [cv2.IMWRITE_JPEG_QUALITY, 93])
    elif '--cover' in a:
        arr = frame(9.8).toarray(colorType=skia.kRGBA_8888_ColorType)
        cv2.imwrite(a[a.index('--cover') + 1], cv2.cvtColor(arr, cv2.COLOR_RGBA2BGR), [cv2.IMWRITE_JPEG_QUALITY, 93])
    elif '--png' in a:
        os.makedirs(os.path.join(HERE, 'proof'), exist_ok=True)
        for ts in a[a.index('--png') + 1].split(','):
            frame(float(ts)).save(os.path.join(HERE, 'proof', f'{"C" if CLEAN else "V"}_{float(ts):05.1f}.png'), skia.kPNG)
    elif '--out' in a:
        o = a[a.index('--out') + 1]
        if '--frames' in a:
            i = a.index('--frames'); render(o, int(a[i + 1]), int(a[i + 2]))
        else:
            render_segments(o, int(a[a.index('--jobs') + 1]) if '--jobs' in a else 2,
                            [int(v) for v in a[a.index('--force') + 1].split(',')] if '--force' in a else ())
