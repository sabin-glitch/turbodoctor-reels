"""Drawing kit (from the Euro norms film / CRI2 injector): fonts, colours, paints, text, flows, easing (skia-python)."""
import math, unicodedata
import numpy as np, skia

FD = '/home/claude/turbodoctor-reels/assets/fonts/'
_TF = {k: skia.Typeface.MakeFromFile(FD + f) for k, f in dict(
    anton='Anton_400Regular.ttf', m6='Montserrat_600SemiBold.ttf', m7='Montserrat_700Bold.ttf',
    m8='Montserrat_800ExtraBold.ttf', m9='Montserrat_900Black.ttf').items()}
_FC = {}


def font(name, size):
    k = (name, round(size * 4))
    if k not in _FC:
        f = skia.Font(_TF[name], size); f.setSubpixel(True); f.setEdging(skia.Font.Edging.kAntiAlias); _FC[k] = f
    return _FC[k]


def hexc(h):
    h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def C(h, a=1.0):
    r, g, b = hexc(h) if isinstance(h, str) else h
    return skia.Color4f(r, g, b, max(0.0, min(1.0, a)))


def mix(h1, h2, f):
    a, b = (hexc(h1) if isinstance(h1, str) else h1), (hexc(h2) if isinstance(h2, str) else h2)
    f = max(0, min(1, f)); return tuple(a[i] + (b[i] - a[i]) * f for i in range(3))


def P(col='#ffffff', a=1.0, stroke=None, cap='round', join='round', blur=None, shader=None, pe=None):
    p = skia.Paint(AntiAlias=True)
    p.setColor4f(C(col, a))
    if stroke is not None:
        p.setStyle(skia.Paint.kStroke_Style); p.setStrokeWidth(stroke)
        p.setStrokeCap({'round': skia.Paint.kRound_Cap, 'butt': skia.Paint.kButt_Cap, 'square': skia.Paint.kSquare_Cap}[cap])
        p.setStrokeJoin({'round': skia.Paint.kRound_Join, 'miter': skia.Paint.kMiter_Join, 'bevel': skia.Paint.kBevel_Join}[join])
    if blur: p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    if shader is not None: p.setShader(shader); p.setAlphaf(max(0.0, min(1.0, a)))
    if pe is not None: p.setPathEffect(pe)
    return p


def _cols(cols):
    return [skia.Color4f(*hexc(c), 1).toColor() if isinstance(c, str) else c for c in cols]


def lin(x0, y0, x1, y1, cols, pos=None):
    return skia.GradientShader.MakeLinear([skia.Point(x0, y0), skia.Point(x1, y1)], _cols(cols), pos)


def rad(x, y, r, cols, pos=None):
    return skia.GradientShader.MakeRadial(skia.Point(x, y), r, _cols(cols), pos)


# ---------------------------------------------------------------- easing
def cl(x, a=0.0, b=1.0): return a if x < a else b if x > b else x
def sm(x): x = cl(x); return x * x * (3 - 2 * x)
def eio(x): x = cl(x); return 4 * x * x * x if x < .5 else 1 - (-2 * x + 2) ** 3 / 2
def eout(x): x = cl(x); return 1 - (1 - x) ** 3
def ramp(t, t0, d=.5): return sm((t - t0) / d) if d > 0 else (1.0 if t >= t0 else 0.0)
def win(t, t0, t1, fi=.4, fo=.4): return ramp(t, t0, fi) * (1 - ramp(t, t1 - fo, fo))
def lerp(a, b, f): return a + (b - a) * f


def h01(k, salt=0.0):
    v = math.sin(k * 12.9898 + salt * 78.233) * 43758.5453; return v - math.floor(v)


# ---------------------------------------------------------------- text
def tw(s, size, name='m8'): return font(name, size).measureText(s)


def txt(c, s, x, y, size, name='m8', col='#ffffff', a=1.0, align='l', stroke=None, scol='#050a12', sa=None, shadow=0):
    if a <= 0.003 or not s: return 0
    f = font(name, size); w = f.measureText(s)
    if align == 'c': x -= w / 2
    elif align == 'r': x -= w
    if shadow:
        c.drawString(s, x, y + shadow * .4, f, P('#000000', a * .55, blur=shadow))
    if stroke:
        c.drawString(s, x, y, f, P(scol, a if sa is None else sa, stroke=stroke))
    c.drawString(s, x, y, f, P(col, a))
    return w


def path_of(pts, close=False):
    p = skia.Path(); p.moveTo(*pts[0])
    for q in pts[1:]: p.lineTo(*q)
    if close: p.close()
    return p


class Poly:
    def __init__(self, pts):
        self.pts = pts; self.p = np.array(pts, float); d = np.diff(self.p, axis=0)
        self.seg = np.maximum(1e-9, np.hypot(d[:, 0], d[:, 1])); self.cum = np.concatenate([[0], np.cumsum(self.seg)]); self.L = float(self.cum[-1])
        self.dir = d / self.seg[:, None]

    def at(self, s):
        s = np.clip(np.asarray(s, float), 0, self.L); i = np.clip(np.searchsorted(self.cum, s, side='right') - 1, 0, len(self.seg) - 1)
        f = (s - self.cum[i]); pt = self.p[i] + self.dir[i] * f[..., None]; return pt, self.dir[i]


def rrect(c, x0, y0, x1, y1, r, paint):
    c.drawRoundRect(skia.Rect.MakeLTRB(x0, y0, x1, y1), r, r, paint)


def norm(s):
    s = unicodedata.normalize('NFD', s.lower()); s = ''.join(ch for ch in s if unicodedata.category(ch) != 'Mn')
    return ''.join(ch for ch in s if ch.isalnum())
