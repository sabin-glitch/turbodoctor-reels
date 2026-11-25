"""Engine of the DPF training film: the Blender layers (../out), mask effects, gas flows and simulated states, all driven by a state object.

World space = pixels of the T1 plate (2160 x 2160) of the main camera.  FMT=V (1080 x 1920) or FMT=H (1920 x 1080).
"""
import os, json, math
import numpy as np, skia, cv2
from fk import *

HERE = os.path.dirname(os.path.abspath(__file__))
OUTD = os.path.join(HERE, '..', 'out')
INFO = json.load(open(os.path.join(OUTD, 'info.json')))
CROPS = INFO['crops']; S1 = INFO['base']; D = INFO['dims']; LAT = INFO['lattice']
FMT = os.environ.get('FMT', 'V')
W, H = (1080, 1920) if FMT == 'V' else (1920, 1080)
FPS = 30
Y, WHT, BG = '#ffc21a', '#ffffff', '#0a1220'
C_GAS, C_CLN, C_SOOT, C_ASH, C_HOT, C_FUEL = '#ff7a30', '#6ec6ff', '#0c0c0c', '#c2bcab', '#ff5a14', '#ffd23a'
SAMP = skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear)
XM = D['XM']
DPF_Z0, DPF_Z1, DOC_Z0, DOC_Z1, R_B = D['DPF_Z0'], D['DPF_Z1'], D['DOC_Z0'], D['DOC_Z1'], D['R_B']
PLUG = D['DPF_PLUG']

# ------------------------------------------------------------------ camera projection (main)
_M = np.array(INFO['M']); _LENS = INFO['lens']; _SEN = INFO['sensor']
_MI = np.linalg.inv(_M)


def proj(p):
    q = _M @ np.array([p[0], p[1], p[2], 1.0])
    k = _LENS / _SEN
    return (0.5 + k * q[0] / -q[2]) * S1, (0.5 - k * q[1] / -q[2]) * S1


def projs(pts): return [proj(p) for p in pts]


def unproject_plane_y0(X, Yp):
    k = _LENS / _SEN
    xn = X / S1 - 0.5; yn = 0.5 - Yp / S1
    d = np.stack([xn / k, yn / k, -np.ones_like(xn)], -1)
    R = _MI[:3, :3]; o = _MI[:3, 3]
    dw = d @ R.T
    t = -o[1] / dw[..., 1]
    P_ = o + dw * t[..., None]
    return P_[..., 0], P_[..., 2]


PXMM = math.hypot(*(np.array(proj((10.0, 0, -60.0))) - np.array(proj((0.0, 0, -60.0))))) / 10.0      # world px per mm on the section plane

# ------------------------------------------------------------------ images
TIERS = {'T1': (1, (0, 0)), 'T2': (2, CROPS['T2'][:2]), 'T8': (8, CROPS['T8'][:2]), 'TA': (24, CROPS['TA'][:2]), 'TB': (24, CROPS['TB'][:2]),
         'TC': (8, CROPS['TC'][:2])}
FEATH = {'T1': 0, 'T2': 0, 'T8': 70, 'TA': 60, 'TB': 60, 'TC': 70}


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
_GHK = {'ghPipe': ('D', 0), 'ghHose': ('D', 1)}


def fx(tn, kind):
    """effect layers built once from the mask plates of a tier -> (image, ox, oy) in tier px, or None."""
    k = (tn, kind)
    if k in _FX: return _FX[k]
    out = None
    tier, (x0, y0) = TIERS[tn]
    if kind in ('soot', 'tin', 'tout', 'glow', 'glow_doc', 'ash'):
        A = mask(tn, 'A'); B = mask(tn, 'B') if tn != 'TC' else None
        src = None
        if kind == 'glow' and A is not None: src = A[..., 0]
        elif kind == 'glow_doc' and A is not None: src = A[..., 1]
        elif kind in ('tin', 'ash') and B is not None: src = B[..., 0]
        elif kind == 'tout' and B is not None: src = B[..., 1]
        elif kind == 'soot' and A is not None and B is not None: src = A[..., 0]
        bb = _bbox(src) if src is not None else None
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
                col = {'tin': C_GAS, 'tout': C_CLN, 'glow': '#ff6a1e', 'glow_doc': '#ff8a2a', 'ash': C_ASH}[kind]
                out = (_sk(_rgba(col, src[sl] / 255.0)), bx0, by0)
    elif kind.startswith('gh'):
        key, ch = _GHK[kind]; m = mask(tn, key)
        if m is not None:
            bb = _bbox(m[..., ch], pad=2)
            if bb is not None:
                bx0, by0, bx1, by1 = bb
                out = (_sk(_rgba('#14233c', m[by0:by1, bx0:bx1, ch].astype(np.float32) / 255.0)), bx0, by0)
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


def view_at(p3, px_per_mm, sx, sy):
    z = px_per_mm / PXMM; wx, wy = proj(p3)
    return z, wx - (sx - W / 2) / z, wy - (sy - H / 2) / z


def zoomed(V, k): return (V[0] * k, V[1], V[2])


def interp_view(a, b, f):
    if abs(b[0] - a[0]) < 1e-9: return (a[0], lerp(a[1], b[1], f), lerp(a[2], b[2], f))
    z = math.exp(lerp(math.log(a[0]), math.log(b[0]), f))
    g = (1 / a[0] - 1 / z) / (1 / a[0] - 1 / b[0])          # pan in step with the zoom, so the target stays put on screen
    return z, lerp(a[1], b[1], g), lerp(a[2], b[2], g)


def to_screen(V, p):
    z, cx, cy = V
    return (p[0] - cx) * z + W / 2, (p[1] - cy) * z + H / 2


def anchor(V, key=None, p3=None):
    if key == 'pipe2x': p3 = (D['PX2'], D['Y_P'], 28.0)
    w = proj(p3) if p3 is not None else INFO['anch'][key][:2]
    return to_screen(V, w)


_BB = os.path.join(OUTD, 'bbox.json')
if os.path.exists(_BB): BBX = json.load(open(_BB))
else:
    def _ab(names, thr=8):
        box = None
        for nm in names:
            a = _read(nm)
            ys, xs = np.nonzero(a[..., 3] > thr); b = [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]
            box = b if box is None else [min(box[0], b[0]), min(box[1], b[1]), max(box[2], b[2]), max(box[3], b[3])]
        return box
    BBX = {'sec': _ab(['T1_sec']), 'ext': _ab(['T1_sec', 'T1_front'])}
    json.dump(BBX, open(_BB, 'w'))


# ------------------------------------------------------------------ drawing: plates + effects
def draw_im(c, im, k, x0, y0, alpha=1.0, blend=None):
    if im is None or alpha <= 0.003: return
    p = skia.Paint(); p.setAlphaf(min(1.0, alpha))
    if blend is not None: p.setBlendMode(blend)
    c.save(); c.translate(x0 / k, y0 / k); c.scale(1.0 / k, 1.0 / k); c.drawImage(im, 0, 0, SAMP, p); c.restore()


def draw_fx(c, tn, kind, alpha=1.0, blend=None):
    e = fx(tn, kind)
    if e is None or alpha <= 0.003: return
    k, (x0, y0) = TIERS[tn]
    draw_im(c, e[0], k, x0 + e[1], y0 + e[2], alpha, blend)


def wy_of_z(zmm): return proj((0.0, 0.0, zmm))[1]


def band_layer(c, draw, y_a, y_b, mode='below', blend=None, alpha=1.0):
    """draws `draw()` in a layer and keeps only: 'below' the line y_a..y_b (soft edge between them), 'above' it, or a 'band' fading towards both."""
    paint = skia.Paint(); paint.setAlphaf(alpha)
    if blend is not None: paint.setBlendMode(blend)
    c.saveLayer(None, paint)
    draw()
    mp = skia.Paint(); mp.setBlendMode(skia.BlendMode.kDstIn)
    T0, T1 = skia.Color4f(0, 0, 0, 0).toColor(), skia.Color4f(0, 0, 0, 1).toColor()
    if mode == 'below': cols, pos = [T0, T1], None
    elif mode == 'above': cols, pos = [T1, T0], None
    else: cols, pos = [T0, T1, T0], [0.0, 0.45, 1.0]
    mp.setShader(skia.GradientShader.MakeLinear([skia.Point(0, y_a), skia.Point(0, y_b)], cols, pos))
    c.drawRect(skia.Rect.MakeLTRB(-5000, -5000, 8000, 8000), mp)
    c.restore()


def tier_fx(c, tn, S):
    """mask-based effects of one tier: channel tints, soot, ash, regeneration glow."""
    hg = S['heat']
    if tn == 'TC':
        if hg > 0.01:
            draw_fx(c, tn, 'glow_doc', 0.20 * hg); draw_fx(c, tn, 'glow_doc', 0.17 * hg, skia.BlendMode.kPlus)
        return
    a_t = 0.26 * S['tint']
    if a_t > 0.01:
        draw_fx(c, tn, 'tin', a_t); draw_fx(c, tn, 'tout', a_t)
    if tn == 'TB': return
    s = S['soot'] * (0.62 if tn == 'TA' else 1.0); fr = S['front']
    if s > 0.01:
        if fr is None: draw_fx(c, tn, 'soot', s)
        elif fr > DPF_Z0 - 24.0:
            band_layer(c, lambda: draw_fx(c, tn, 'soot', s), wy_of_z(fr + 9.0), wy_of_z(fr - 9.0), 'below')
    aw = S['ashw']
    if aw > 0.5 and tn in ('T1', 'T2'):
        zt = DPF_Z0 + PLUG + aw
        band_layer(c, lambda: draw_fx(c, tn, 'ash', 0.92), wy_of_z(zt + 2.5), wy_of_z(zt - 2.5), 'below')
    if hg > 0.01:
        draw_fx(c, tn, 'glow_doc', 0.20 * hg * S['docglow']); draw_fx(c, tn, 'glow_doc', 0.17 * hg * S['docglow'], skia.BlendMode.kPlus)
        draw_fx(c, tn, 'glow', 0.16 * hg * S['dpfglow'], skia.BlendMode.kPlus)
    if fr is not None and DPF_Z0 - 24.0 < fr < DPF_Z1 + 20.0:
        band_layer(c, lambda: draw_fx(c, tn, 'glow'), wy_of_z(fr + 26.0), wy_of_z(fr - 30.0), 'band', blend=skia.BlendMode.kPlus, alpha=0.95)
        band_layer(c, lambda: draw_fx(c, tn, 'glow'), wy_of_z(fr + 9.0), wy_of_z(fr - 12.0), 'band', blend=skia.BlendMode.kPlus, alpha=0.7)


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
BOX_T = {'T1': wbox(CAB['t1']), 'T2': wbox(CAB['t2']), 'T3': wbox(CAB['t3'])}
BOX_P2 = wbox(INFO['paths3d']['p2'] + INFO['paths3d']['hose2'], pad=18)
BOX_P1 = wbox(INFO['paths3d']['p1'] + INFO['paths3d']['hose1'], pad=18)
BOX_H1 = wbox(INFO['paths3d']['hose1'], pad=16)


def highlights(c, tn, S):
    h = S['hl']
    if not h: return
    hl(c, tn, 'hlL', h.get('L', 0.0))
    for k in ('T1', 'T2', 'T3'): hl(c, tn, 'hlT', h.get(k, 0.0), BOX_T[k])
    hl(c, tn, 'hlPipe', h.get('Pipe', 0.0)); hl(c, tn, 'hlHose', h.get('Hose', 0.0)); hl(c, tn, 'hlDps', h.get('Dps', 0.0))
    hl(c, tn, 'hlHose', h.get('Hose1', 0.0), BOX_H1)
    hl(c, tn, 'hlPipe', h.get('Pipe1', 0.0), BOX_P1); hl(c, tn, 'hlHose', h.get('Pipe1', 0.0), BOX_P1)
    g = S['onep']
    if g > 0.01:                                    # variant with a single pipe: the pipe after the filter is ghosted
        c.save(); c.clipRect(skia.Rect.MakeLTRB(*BOX_P2))
        draw_fx(c, tn, 'ghPipe', 0.90 * g); draw_fx(c, tn, 'ghHose', 0.90 * g)
        c.restore()


# ------------------------------------------------------------------ flows
def flow_poly(pts3): return Poly(projs(pts3))


def streak(c, p, q, w, col, a, glow=True, head=True):
    if a < 0.02: return
    if glow: c.drawLine(q[0], q[1], p[0], p[1], P(col, a * 0.20, stroke=w * 3.2))
    c.drawLine(q[0], q[1], p[0], p[1], P(col, a, stroke=w * 1.5))
    if head: c.drawLine((q[0] + p[0]) / 2, (q[1] + p[1]) / 2, p[0], p[1], P('#ffffff', a * 0.75, stroke=w * 0.6))


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
        i_doc0 = len(pts) - 1
        pts += [(xb, 1.0, DOC_Z0), (xb, 1.0, DPF_Z1)]
        i_doc1 = len(pts) - 2; i_dpf0 = len(pts) - 1
        pts.append((xb, 1.0, DPF_Z0)); i_dpf1 = len(pts) - 1
        for i in range(1, 11):
            f = i / 10; g = sm(f)
            pts.append((lerp(xb, o2, g), 1.0, lerp(DPF_Z0 - 4.0, OUT_Z, f)))
        for i in range(1, 13):
            th = (math.pi / 2) * i / 12
            pts.append((OUT_R - (OUT_R - o2) * math.cos(th), 1.0, OUT_Z - (OUT_R - o2) * math.sin(th)))
        pts.append((D['OUT_X1'] + 46.0, 1.0, OUT_PZ + o2))
        poly = flow_poly(pts)
        S.append(dict(poly=poly, s0=float(poly.cum[i_dpf0]), s1=float(poly.cum[i_dpf1]), d0=float(poly.cum[i_doc0]), d1=float(poly.cum[i_doc1]), k=k))
    return S


STREAMS = build_streams()


def wide_flow(c, S, z, a):
    """streams through the whole canister: orange = with soot, blue = filtered; 'smoke' = sooty engine, 'crack' = soot gets past the filter,
    'fuel' = post-injected fuel that lights up in the catalyst (or passes unburnt when 'cold')."""
    if a <= 0.02: return
    ft = S['ft']; speed = 330.0; sp = 62.0; w = 2.5 / z
    gc, cc = hexc(C_GAS), hexc(C_CLN)
    smoke, crack, fuel, cold = S['smoke'], S['crack'], S['fuel'], S['cold']
    if smoke > 0.01: gc = mix(gc, '#6b3a1c', 0.55 * smoke)
    fc, hc = hexc(C_FUEL), hexc('#ffb060')
    for st in STREAMS:
        poly = st['poly']; L = poly.L
        d = ft * speed + st['k'] * 23.0
        i1 = int(math.floor(d / sp)); i0 = int(math.ceil((d - L) / sp))
        thru = crack * (1.0 if st['k'] in (2, 3, 4) else 0.0)
        for i in range(i0, i1 + 1):
            s = d - i * sp
            if s < 0 or s > L: continue
            pt, _ = poly.at(np.array([s, max(0.0, s - sp * 0.5)]))
            ssw = st['s0'] + (0.10 + 0.82 * h01(i * 7.31 + st['k'] * 3.7)) * (st['s1'] - st['s0'])
            col = mix(gc, cc, sm((s - ssw) / 36.0 + 0.5) * (1.0 - thru))
            fa = min(1.0, s / (1.4 * sp), (L - s) / (1.4 * sp)); ww = w
            if fuel > 0.01 and (i + st['k']) % 2 == 0:
                if s < st['d0'] or cold > 0.5:
                    if s < st['s0'] + 30.0: col = mix(col, fc, fuel); ww = w * (1 + 0.5 * fuel)
                elif s < st['s0']:
                    col = mix(col, hc, fuel); ww = w * (1 + 0.9 * fuel)
            streak(c, pt[0], pt[1], ww, col, a * fa)
            if smoke > 0.01 and s < ssw and (i + st['k']) % 2:
                c.drawCircle(pt[1][0], pt[1][1], 1.5 * w, P('#120a06', a * fa * 0.85 * smoke))


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

    def draw(self, c, z, a, a_soot, ft, V):
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

# ---- the catalyst close-up: straight through its open channels
DCELLS = LAT['doc']['cells']
Z_DT, Z_DB = 124.0, 4.0


class DocFlow:
    def __init__(self, x0, x1, seed=8, n_per=4):
        rng = np.random.default_rng(seed); self.P = []
        for j, (xa, xb, _) in enumerate(DCELLS):
            xc = (xa + xb) / 2
            if xc < x0 or xc > x1 or j % 2: continue
            for n in range(n_per):
                self.P.append((xc + rng.uniform(-0.12, 0.12), (n / n_per + rng.uniform(0, 0.2) + 0.37 * j) % 1.0, int(rng.integers(0, 1000))))
        self.L = Z_DT - Z_DB

    def draw(self, c, z, a, ft, V, mode, heat):
        if a <= 0.02: return
        w = 2.4 / z; lenmm = 40.0 / (z * PXMM)
        gc = hexc(C_GAS); fc = hexc(C_FUEL); hot = hexc('#ffe6a0')
        for (x, ph, sd) in self.P:
            s = ((ft * 9.0 / self.L + ph) % 1.0) * self.L; zz = Z_DT - s
            A = proj((x, 0.3, zz)); B = proj((x, 0.3, min(Z_DT, zz + lenmm)))
            sy = to_screen(V, A)[1]
            if sy < -60 or sy > H + 60: continue
            fa = min(1.0, s / 6.0, (self.L - s) / 6.0); col = gc; ww = w; drop = False
            if mode in ('fuel', 'cold') and sd % 3 == 0:
                if mode == 'cold' or zz > DOC_Z1 - 4.0: col = fc; drop = True
                else:
                    k = cl((DOC_Z1 - 4.0 - zz) / 22.0); col = mix(fc, hot, k); ww = w * (1.0 + 1.2 * math.sin(math.pi * min(1.0, k * 1.2)))
            elif mode == 'fuel' and zz < DOC_Z1 - 20.0:
                col = mix(gc, '#ffb060', 0.7 * heat); ww = w * (1 + 0.4 * heat)
            if drop:
                c.drawCircle(A[0], A[1], 5.2 / z, P(col, a * fa)); c.drawCircle(A[0] - 1.2 / z, A[1] - 1.4 / z, 1.8 / z, P('#fff6c8', a * fa * 0.9))
            else: streak(c, A, B, ww, col, a * fa, glow=True)


DF = DocFlow(XM - 36.0, XM + 36.0)
_TAGX = [XM - 25.4, XM - 12.7, XM + 0.0, XM + 12.7, XM + 25.4]


def chemtxt(c, s, x, y, size, col, a, name='m9'):
    """text with the digits set as subscripts (CO2, H2O, NO2); returns the width. x = left."""
    w = 0.0
    for ch in s:
        if ch.isdigit(): w += txt(c, ch, x + w, y + size * 0.22, size * 0.64, name, col, a)
        else: w += txt(c, ch, x + w, y, size, name, col, a)
    return w


def chemw(s, size, name='m9'): return sum(tw(ch, size * 0.64 if ch.isdigit() else size, name) for ch in s)


TAG_FADE = None          # (top, bottom) in screen px: the tags fade out before they reach the header and the caption (set by film.py)


def chem_tags(c, S, V):
    """molecule tags riding through the catalyst: what goes in above, what comes out below. Drawn in screen space."""
    mode, a = S['chem'], S['chem_a']
    if a <= 0.02 or mode not in ('ox', 'no2'): return
    pairs = {'ox': [('CO', 'CO2'), ('HC', 'CO2 + H2O')], 'no2': [('NO', 'NO2'), ('NO', 'NO2'), ('NO', 'NO')]}[mode]
    L = Z_DT - Z_DB
    for k, x in enumerate(_TAGX):
        for n in range(2):
            ph = (S['ft'] * 9.0 * 0.62 / L + 0.5 * n + 0.21 * k) % 1.0; zz = Z_DT - ph * L
            before, after = pairs[(k + n) % len(pairs)]
            mid = (DOC_Z0 + DOC_Z1) / 2 + 6.0 * math.sin(k * 2.1 + n)
            done = zz < mid; s = after if done else before
            sx, sy = to_screen(V, proj((x, 0.3, zz)))
            fa = a * min(1.0, ph * 9, (1 - ph) * 9)
            if TAG_FADE: fa *= max(0.0, min(1.0, (sy - TAG_FADE[0]) / 50.0, (TAG_FADE[1] - sy) / 60.0))
            if fa <= 0.01: continue
            sz = 30 if FMT == 'V' else 27; wd = chemw(s, sz) + 26
            col = ('#8ff0a0' if mode == 'ox' else '#ffb347') if done and before != after else '#e8edf4'
            pop = 1.0 + 0.25 * max(0.0, 1.0 - abs(zz - mid) / 5.0) if before != after else 1.0
            c.save(); c.translate(sx, sy); c.scale(pop, pop)
            rrect(c, -wd / 2, -sz * 0.72, wd / 2, sz * 0.62, 12, P('#0b1424', fa * 0.92)); rrect(c, -wd / 2, -sz * 0.72, wd / 2, sz * 0.62, 12, P(col, fa * 0.9, stroke=2.2))
            chemtxt(c, s, -wd / 2 + 13, sz * 0.32, sz, col, fa)
            c.restore()


# ---- soot layer / ash in the macro views (drawn from the lattice, in mm)
_RN = np.random.default_rng(11).random(4096)


def _noise(i, salt=0): return float(_RN[(i * 7919 + salt * 104729) % 4096])


def quad_mm(c, x0, x1, z0, z1, paint, y=0.0):
    c.drawPath(path_of([proj((x0, y, z0)), proj((x1, y, z0)), proj((x1, y, z1)), proj((x0, y, z1))], True), paint)


def macro_soot(c, s, zr, x0, x1, fr=None):
    """soot cake on the inlet channel walls between heights zr = (lo, hi)."""
    if s <= 0.01: return
    lo, hi = zr
    if fr is not None: hi = min(hi, fr)
    if hi <= lo: return
    dmax = 0.30 * s
    for j, (xa, xb, is_in) in enumerate(CELLS):
        if not is_in or xb < x0 or xa > x1: continue
        zb = max(lo, DPF_Z0 + PLUG); zt = min(hi, DPF_Z1)
        if zt <= zb: continue
        quad_mm(c, xa, xb, zb, zt, P(C_SOOT, 0.50 * s), y=0.0)
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


def macro_ash(c, hgt, x0, x1):
    """ash plug growing above the plugs at the closed end of the inlet channels."""
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


def ash_fall(c, a, hgt, z, x0, x1, ft):
    """light ash grains drifting down the inlet channels towards the plugs."""
    if a <= 0.02: return
    for j, (xa, xb, is_in) in enumerate(CELLS):
        if not is_in or xb < x0 or xa > x1: continue
        zb = DPF_Z0 + PLUG + hgt * 0.9
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


def pulses(c, t, z, a, a2=1.0):
    if a <= 0.02: return
    for poly, col, ph, am in ((PIPE1, C_GAS, 0.0, 1.0), (PIPE2, C_CLN, 0.5, a2)):
        aa = a * am
        if aa <= 0.02: continue
        L = poly.L; sp = 46.0; sp_px = 150.0
        d = t * sp_px + ph * sp
        n = int(L // sp) + 2
        for i in range(n):
            s = (d % sp) + i * sp
            if s > L: continue
            pt, _ = poly.at(np.array([s, max(0.0, s - 16.0)]))
            fa = min(1.0, s / 30.0, (L - s) / 30.0)
            c.drawLine(pt[1][0], pt[1][1], pt[0][0], pt[0][1], P(col, aa * fa * 0.28, stroke=9.0 / z))
            c.drawLine(pt[1][0], pt[1][1], pt[0][0], pt[0][1], P(col, aa * fa, stroke=4.4 / z))
            c.drawCircle(pt[0][0], pt[0][1], 1.6 / z, P('#ffffff', aa * fa * 0.9))


# ---- simulated faults, drawn on the section plane
_CRK = [[(-58.0, -52.0), (-44.0, -58.0), (-31.0, -54.0), (-17.0, -62.0), (-4.0, -57.0), (9.0, -64.0), (22.0, -60.0), (34.0, -67.0)],
        [(-17.0, -62.0), (-20.0, -84.0), (-14.0, -103.0), (-19.0, -126.0), (-13.0, -150.0), (-16.0, -172.0)],
        [(9.0, -64.0), (13.0, -40.0), (8.0, -18.0), (12.0, -2.0)]]


def cracks(c, a, z):
    if a <= 0.02: return
    for k, ln in enumerate(_CRK):
        n = max(2, int(round(len(ln) * cl(a * 1.6 - 0.25 * k))))
        if n < 2: continue
        pts = projs([(x, 0.0, zz) for x, zz in ln[:n]])
        sw = max(2.2, 4.4 / z)
        c.drawPath(path_of(pts), P('#ff8a3a', 0.42 * a, stroke=sw * 3.2, blur=sw * 1.2))
        c.drawPath(path_of(pts), P('#020202', 0.96 * a, stroke=sw, join='miter'))
        c.drawPath(path_of([(x + sw * 0.35, y + sw * 0.35) for x, y in pts]), P('#d8d2c4', 0.4 * a, stroke=sw * 0.25))


def puffs(c, t, a, p3, d3, col, n=9, reach=46.0, z=1.0):
    """a leak: short streaks leaving a point in a fan around the direction d3 (both in mm)."""
    if a <= 0.02: return
    for k in range(n):
        ph = (t * 0.9 + k / n + 0.37 * h01(k, 3)) % 1.0
        ang = (h01(k, 5) - 0.5) * 1.5
        dx = d3[0] * math.cos(ang) - d3[2] * math.sin(ang); dz = d3[0] * math.sin(ang) + d3[2] * math.cos(ang)
        r0 = reach * ph; r1 = reach * max(0.0, ph - 0.16)
        A = proj((p3[0] + dx * r0, p3[1], p3[2] + dz * r0)); B = proj((p3[0] + dx * r1, p3[1], p3[2] + dz * r1))
        fa = a * (1 - ph) ** 1.2
        c.drawLine(B[0], B[1], A[0], A[1], P(col, fa * 0.25, stroke=9.0 / z)); c.drawLine(B[0], B[1], A[0], A[1], P(col, fa, stroke=3.6 / z))
    q = proj(p3)
    c.drawCircle(q[0], q[1], 9.0 / z, P('#ff3b30', a * 0.95, stroke=3.0 / z)); c.drawCircle(q[0], q[1], 16.0 / z, P('#ff3b30', a * 0.4, stroke=2.0 / z))


LEAK_F = ((D['IN_X0'] + 4.0, 0.0, D['IN_PZ'] + 33.0), (-0.25, 0.0, 1.0))           # V-band joint towards the turbocharger
_h1 = INFO['paths3d']['hose1']; LEAK_H = (tuple(_h1[9]), (-1.0, 0.0, 0.25))        # a cracked hose (the one before the filter)


# ------------------------------------------------------------------ the scene
def scene(c, S, V):
    z, cx, cy = V; t = S['t']
    c.save(); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-cx, -cy)
    fb = ramp(cy, wy_of_z(-95.0), wy_of_z(-135.0) - wy_of_z(-95.0))        # 0: inlet end of the filter in view ... 1: outlet end
    indoc = 1 - ramp(cy, wy_of_z(30.0), wy_of_z(8.0) - wy_of_z(30.0))        # 1: the catalyst in view ... 0: the filter
    w2 = ramp(z, 0.72, 0.26)
    kx = 1 - ramp(abs(cx - proj((XM, 0.0, 0.0))[0]), 60.0, 50.0)          # the close-up plates belong to the views centred on the bricks
    w8 = ramp(z, 2.0, 1.6) * (1 - ramp(cy, wy_of_z(-40.0), wy_of_z(-95.0) - wy_of_z(-40.0))) * kx
    wa = ramp(z, 8.0, 7.0) * (1 - fb) * (1 - indoc); wb = ramp(z, 2.8, 6.0) * fb; wm = max(wa, wb)
    ft = S['ft']; ct = S['ct']
    under = wm < 0.999 or z < 21.5                 # the macro plates cover the whole frame only at the final macro zoom
    layers = [('T1', 1.0 if w2 < 0.999 else 0.0), ('T2', w2 if under else 0.0), ('T8', w8 if under else 0.0), ('TC', ramp(z, 2.0, 1.6) * kx if under else 0.0),
              ('TA', wa), ('TB', wb)]
    for tn, wgt in layers:
        if wgt <= 0.003 or img(tn + '_sec') is None: continue
        k, (x0, y0) = TIERS[tn]
        c.saveLayerAlpha(None, int(min(1.0, wgt) * 255))
        draw_im(c, img(tn + '_sec'), k, x0, y0)
        tier_fx(c, tn, S)
        if tn in ('T1', 'T2'): highlights(c, tn, S)
        if tn == 'TA': macro_soot(c, S['soot'], (-26.0, DPF_Z1), XM - 15.0, XM + 15.0)
        if tn == 'TB':
            macro_ash(c, S['ash'], XM - 15.0, XM + 15.0); ash_fall(c, S['ashfall'], S['ash'], z, XM - 15.0, XM + 15.0, ft)
        c.restore()
    cracks(c, S['crack'], z)
    # front half (cutaway reveal)
    rv = S['rev']
    if rv < 0.999:
        k_ = eio(rv); ax, ay = proj((0.0, -40.0, -30.0))
        c.save(); c.translate(ax - 430 * k_, ay - 120 * k_); c.scale(1 + 0.5 * k_, 1 + 0.5 * k_); c.translate(-ax, -ay)
        draw_im(c, img('T1_front'), 1, 0, 0, alpha=1 - sm(rv * 1.12))
        c.restore()
    # gases
    a_w = S['flow'] * sm(rv * 1.3 - 0.3) * (1 - ramp(z, 3.2, 2.4))
    wide_flow(c, S, z, a_w * 0.92)
    a_c = ramp(z, 3.4, 2.4) * S['flow']
    if a_c * indoc > 0.02:
        DF.draw(c, z, a_c * indoc * 0.95, ct, V, S['chem'], S['heat'])
    if a_c * fb > 0.02:
        CF_B.draw(c, z, a_c * fb * ramp(z, 9.0, 5.0) * 0.95, 0.0, ct, V)
        wall_arrows(c, t, z, fb * ramp(z, 9.0, 5.0) * S['arrows'], (DPF_Z0 + PLUG + 10.5, -152.0), XM - 15.0, XM + 15.0)
    if a_c * (1 - fb) * (1 - indoc) > 0.02:
        wmac = ramp(z, 9.0, 5.0); kk = (1 - fb) * (1 - indoc)
        CF_F.draw(c, z, a_c * kk * (1 - wmac) * 0.95, 0.0, ct, V)
        CF_A.draw(c, z, a_c * kk * wmac * 0.95, S['specks'], ct, V)
        wall_arrows(c, t, z, kk * wmac * S['arrows'], (-27.0, DPF_Z1 - 5.0), XM - 15.0, XM + 15.0)
    pulses(c, t, z, S['pul'], 1.0 - S['onep'])
    puffs(c, t, S['leakf'], LEAK_F[0], LEAK_F[1], C_GAS, z=z)
    puffs(c, t, S['leakh'], LEAK_H[0], LEAK_H[1], C_GAS, n=7, reach=30.0, z=z)
    c.restore()
    chem_tags(c, S, V)
