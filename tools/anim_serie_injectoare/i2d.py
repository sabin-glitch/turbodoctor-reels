# Grafica 2D comuna pentru episoadele 5–13: text (PIL), puncte si fluxuri pe trasee 2D, arce, diagrame circulare,
# schema sistemului de alimentare (SVG, cu evidentieri pe componente) si pictogramele noi.
import os, math
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
import icomp as IC
from fxlib import seg

FONTS = os.path.join(IC.HERE, 'hud', 'fonts')
FF = {'anton': 'Anton_400Regular.ttf', 'mont': 'Montserrat_800ExtraBold.ttf', 'mont9': 'Montserrat_900Black.ttf', 'mont7': 'Montserrat_700Bold.ttf'}
_FC = {}; _TC = {}

def _font(name, size):
    k = (name, size)
    if k not in _FC: _FC[k] = ImageFont.truetype(os.path.join(FONTS, FF[name]), size)
    return _FC[k]

def _blit_u8(C, buf, X0, Y0, a=1.0):
    al = buf[..., 3:4].astype(np.float32) / 255.0
    IC.blit(C.ov, np.concatenate([buf[..., :3].astype(np.float32) / 255.0 * al, al], -1) * a, X0, Y0, 1.0); C.used = True

def text(C, s, x, y, size, col=(255, 255, 255), a=1.0, font='anton', anchor='mm', shadow=True, spacing=0):
    """text in coordonate 1080x1920; anchor ca la PIL (lt, mm, rb...)"""
    if a <= 0.003 or not s: return
    k = C.k; sz = max(6, int(round(size * k)))
    key = (s, sz, font, tuple(col), shadow)
    if key not in _TC:
        f = _font(font, sz); bb = f.getbbox(s); w, h = bb[2] - bb[0] + 4, bb[3] - bb[1] + 4
        pad = int(sz * 0.25)
        im = Image.new('RGBA', (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        if shadow:
            sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
            ds.text((pad - bb[0] + 2, pad - bb[1] + max(2, sz // 22)), s, font=f, fill=(0, 0, 0, 200))
            from PIL import ImageFilter
            sh = sh.filter(ImageFilter.GaussianBlur(max(1, sz // 16))); im = Image.alpha_composite(im, sh); d = ImageDraw.Draw(im)
        d.text((pad - bb[0], pad - bb[1]), s, font=f, fill=tuple(col) + (255,))
        _TC[key] = (np.asarray(im), pad, w, h)
    arr, pad, w, h = _TC[key]
    X = x * k; Y = y * k
    X -= {'l': 0, 'm': w / 2, 'r': w}[anchor[0]]; Y -= {'t': 0, 'm': h / 2, 'b': h}[anchor[1]]
    _blit_u8(C, arr, int(X - pad), int(Y - pad), a)

def canvas(C, x, y, w, h, draw, a=1.0):
    """deseneaza cu cv2 intr-un tampon local; draw(buf, P, k) cu P(px, py) -> coordonate cu shift=4"""
    if a <= 0.003: return
    k = C.k; X0, Y0 = int(x * k), int(y * k); Wd, Hd = int(w * k) + 4, int(h * k) + 4
    if Wd <= 4 or Hd <= 4: return
    buf = np.zeros((Hd, Wd, 4), np.uint8)
    def P(px, py): return (int(round((px * k - X0) * 16)), int(round((py * k - Y0) * 16)))
    draw(buf, P, k)
    _blit_u8(C, buf, X0, Y0, a)

def dots2(C, P, r, col, a=1.0, glow=0.0, ring=False):
    """puncte 2D (N,2) in coordonate 1080x1920, raza r (px la 1080), culoare 0–255"""
    P = np.asarray(P, float).reshape(-1, 2)
    if len(P) == 0 or a <= 0.003: return
    rr = np.broadcast_to(np.asarray(r, float), (len(P),))
    m = rr.max() * (3.2 if glow else 1.4) + 4
    x0, y0 = P[:, 0].min() - m, P[:, 1].min() - m; x1, y1 = P[:, 0].max() + m, P[:, 1].max() + m
    def draw(buf, Q, k):
        for (px, py), ri in zip(P, rr):
            c = Q(px, py)
            if glow:
                for gk, ga in ((3.0, 40), (2.0, 70)):
                    cv2.circle(buf, c, int(ri * gk * k * 16), (*col, ga), -1, cv2.LINE_AA, shift=4)
            if ring: cv2.circle(buf, c, int(ri * k * 16), (*col, 255), max(1, int(2.2 * k)), cv2.LINE_AA, shift=4)
            else: cv2.circle(buf, c, int(ri * k * 16), (*col, 255), -1, cv2.LINE_AA, shift=4)
    canvas(C, x0, y0, x1 - x0, y1 - y0, draw, a)

class Poly:
    """traseu 2D (polilinie) cu parametrizare dupa lungime"""
    def __init__(s, pts):
        s.p = np.asarray(pts, float); d = np.linalg.norm(np.diff(s.p, axis=0), axis=1)
        s.cum = np.concatenate([[0], np.cumsum(d)]); s.len = float(s.cum[-1])
    def at(s, u):
        u = np.clip(np.asarray(u, float), 0, s.len)
        i = np.clip(np.searchsorted(s.cum, u, side='right') - 1, 0, len(s.p) - 2)
        t = ((u - s.cum[i]) / np.maximum(s.cum[i + 1] - s.cum[i], 1e-9))[:, None]
        return s.p[i] * (1 - t) + s.p[i + 1] * t

def flow2(C, polys, n, speed, col, r, t0=None, t1=None, a=1.0, seed=1, glow=0.0, jit=0.25, lat=0.0, ring=False):
    """particule pe trasee 2D: fiecare particula pe unul din trasee; t0 = frontul porneste, t1 = sursa se opreste"""
    t = C.t
    if t0 is not None and t < t0: return
    rng = np.random.RandomState(seed); u0 = rng.rand(n); which = rng.randint(0, len(polys), n); sv = 1 + (rng.rand(n) - 0.5) * 2 * jit
    off = (rng.rand(n) - 0.5) * 2 * lat
    pts = []
    for i in range(n):
        p = polys[which[i]]; s = (u0[i] * p.len + (t - (t0 or 0)) * speed * sv[i]) % p.len
        if t0 is not None and s > (t - t0) * speed * sv[i]: continue          # frontul inca n-a ajuns aici
        if t1 is not None and t > t1:
            if (t - t1) * speed * sv[i] > s: continue                            # coada a trecut deja
        q = p.at([s])[0]
        if lat:
            j = min(int(np.searchsorted(p.cum, s)), len(p.p) - 1); j0 = max(j - 1, 0)
            dv = p.p[j] - p.p[j0]; nv = np.array([-dv[1], dv[0]]) / (np.linalg.norm(dv) + 1e-9); q = q + nv * off[i]
        pts.append(q)
    if pts: dots2(C, np.array(pts), r, col, a, glow, ring)

def arc(C, cx, cy, R, a0, a1, col, th=10, a=1.0):
    """arc de cerc (grade, 0 = dreapta, sens orar pe ecran)"""
    if a <= 0.003 or abs(a1 - a0) < 0.2: return
    def draw(buf, P, k):
        c = P(cx, cy); cv2.ellipse(buf, c, (int(R * k * 16), int(R * k * 16)), 0, a0, a1, (*col, 255), max(1, int(th * k)), cv2.LINE_AA, shift=4)
    canvas(C, cx - R - th, cy - R - th, 2 * (R + th), 2 * (R + th), draw, a)

def pie(C, cx, cy, R, fracs, cols, prog=1.0, a=1.0, hole=0.55, gap=2.0):
    """diagrama inel: fracs insumate 1, desenata progresiv (prog 0..1) incepand de sus"""
    if a <= 0.003: return
    def draw(buf, P, k):
        c = P(cx, cy); ang = -90.0; tot = 360.0 * prog
        for f, col in zip(fracs, cols):
            sweep = min(360.0 * f, max(0.0, tot - (ang + 90.0)))
            if sweep > 0.2:
                cv2.ellipse(buf, c, (int(R * k * 16), int(R * k * 16)), 0, ang + gap / 2, ang + sweep - gap / 2, (*col, 255), -1, cv2.LINE_AA, shift=4)
            ang += 360.0 * f
        cv2.circle(buf, c, int(R * hole * k * 16), (0, 0, 0, 0), -1, cv2.LINE_AA, shift=4)
    canvas(C, cx - R - 4, cy - R - 4, 2 * R + 8, 2 * R + 8, draw, a)

def rbox(C, x, y, w, h, col, a=1.0, th=5, fill=None, r=14):
    """chenar cu colturi rotunjite (evidentiere), optional umplut"""
    if a <= 0.003: return
    def draw(buf, P, k):
        rr = r * k * 16
        x0, y0 = P(x, y); x1, y1 = P(x + w, y + h); t = max(1, int(th * k))
        if fill is not None:
            f = (*fill[:3], fill[3] if len(fill) > 3 else 255)
            cv2.rectangle(buf, (x0 + int(rr), y0), (x1 - int(rr), y1), f, -1, cv2.LINE_AA, shift=4)
            cv2.rectangle(buf, (x0, y0 + int(rr)), (x1, y1 - int(rr)), f, -1, cv2.LINE_AA, shift=4)
            for cx_, cy_ in ((x0 + rr, y0 + rr), (x1 - rr, y0 + rr), (x0 + rr, y1 - rr), (x1 - rr, y1 - rr)):
                cv2.circle(buf, (int(cx_), int(cy_)), int(rr), f, -1, cv2.LINE_AA, shift=4)
        c = (*col, 255)
        cv2.line(buf, (int(x0 + rr), y0), (int(x1 - rr), y0), c, t, cv2.LINE_AA, shift=4)
        cv2.line(buf, (int(x0 + rr), y1), (int(x1 - rr), y1), c, t, cv2.LINE_AA, shift=4)
        cv2.line(buf, (x0, int(y0 + rr)), (x0, int(y1 - rr)), c, t, cv2.LINE_AA, shift=4)
        cv2.line(buf, (x1, int(y0 + rr)), (x1, int(y1 - rr)), c, t, cv2.LINE_AA, shift=4)
        R = (int(rr), int(rr))
        cv2.ellipse(buf, (int(x0 + rr), int(y0 + rr)), R, 0, 180, 270, c, t, cv2.LINE_AA, shift=4)
        cv2.ellipse(buf, (int(x1 - rr), int(y0 + rr)), R, 0, 270, 360, c, t, cv2.LINE_AA, shift=4)
        cv2.ellipse(buf, (int(x0 + rr), int(y1 - rr)), R, 0, 90, 180, c, t, cv2.LINE_AA, shift=4)
        cv2.ellipse(buf, (int(x1 - rr), int(y1 - rr)), R, 0, 0, 90, c, t, cv2.LINE_AA, shift=4)
    canvas(C, x - th - 2, y - th - 2, w + 2 * th + 4, h + 2 * th + 4, draw, a)

def line2(C, pts, col, th=4, a=1.0, prog=1.0):
    """polilinie 2D desenata progresiv"""
    if a <= 0.003 or prog <= 0: return
    p = Poly(pts); L = p.len * min(1.0, prog)
    u = np.concatenate([p.cum[p.cum < L], [L]]); q = p.at(u)
    x0, y0 = q.min(0) - th - 4; x1, y1 = q.max(0) + th + 4
    def draw(buf, P, k):
        cv2.polylines(buf, [np.array([P(*v) for v in q], np.int32)], False, (*col, 255), max(1, int(th * k)), cv2.LINE_AA, shift=4)
    canvas(C, x0, y0, x1 - x0, y1 - y0, draw, a)

def fmt_km(v):
    return '{:,}'.format(int(round(v))).replace(',', '.')

# ------------------------------------------------------------------ schema sistemului de alimentare (sprite 1000x720 la SYS_X, SYS_Y)
SYS_X, SYS_Y = 40, 540
INJ_X = (450, 590, 730, 870)
_ST = '<linearGradient id="st" x1="0" x2="1"><stop offset="0" stop-color="#8d98a4"/><stop offset=".45" stop-color="#d9e0e7"/><stop offset="1" stop-color="#6f7a86"/></linearGradient>'
_TXT = 'font-family:Mont;font-weight:800;font-size:28px;letter-spacing:1px;fill:#e8edf3'
def _parts(stroke='#9aa7b5', fill='rgba(20,26,33,.94)', only=None, glow=None, sw=4):
    """componentele schemei; only = lista de componente desenate (pentru evidentieri)"""
    g = []
    def want(n): return only is None or n in only
    if want('tank'):
        g.append(f'<rect x="40" y="560" width="520" height="130" rx="26" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
        if only is None: g.append('<rect x="48" y="612" width="504" height="70" rx="18" fill="#ffc02a" opacity=".5"/>')
    if want('filter'):
        g.append(f'<rect x="70" y="380" width="90" height="140" rx="16" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
        if only is None: g += ['<path d="M88 400v100M100 400v100M112 400v100M124 400v100M136 400v100M148 400v100" stroke="#e8edf3" stroke-width="3" opacity=".55"/>']
    if want('pump'):
        g.append(f'<rect x="170" y="150" width="170" height="170" rx="24" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
        if only is None: g += ['<circle cx="255" cy="250" r="42" fill="none" stroke="#e8edf3" stroke-width="5" opacity=".75"/>',
                               '<circle cx="255" cy="250" r="9" fill="#e8edf3" opacity=".75"/>', '<rect x="240" y="166" width="30" height="40" rx="5" fill="#cfd6de" opacity=".85"/>']
    if want('rail'):
        g.append(f'<rect x="380" y="60" width="560" height="46" rx="23" fill="{"url(#st)" if only is None else fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    if want('inj'):
        for x in INJ_X:
            g.append(f'<rect x="{x - 20}" y="130" width="40" height="150" rx="8" fill="{"url(#st)" if only is None else fill}" stroke="{stroke}" stroke-width="{sw}"/>')
            g.append(f'<path d="M{x - 11} 280h22l-6 52h-10z" fill="{"#c3cbd4" if only is None else fill}" stroke="{stroke}" stroke-width="{max(2, sw - 1)}"/>')
            if only is None: g.append(f'<rect x="{x + 20}" y="150" width="16" height="26" rx="4" fill="#3a434d" stroke="#9aa7b5" stroke-width="2"/>')
    if want('hp'):
        c = '#ff5a26' if only is None else stroke
        g.append(f'<path d="M255 150V83H380" fill="none" stroke="{c}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>')
        for x in INJ_X: g.append(f'<path d="M{x} 106V130" stroke="{c}" stroke-width="8" stroke-linecap="round"/>')
    if want('lp'):
        c = '#ffc02a' if only is None else stroke
        g.append(f'<path d="M115 560V520M115 380V250H170" fill="none" stroke="{c}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>')
        g.append(f'<path d="M940 83H975V625H560" fill="none" stroke="{c}" stroke-width="5" stroke-dasharray="12 9" stroke-linecap="round" opacity="{1 if only else .75}"/>')
    return ''.join(g)

def sys_svg(labels=True):
    lab = ''
    if labels:
        lab = (f'<text x="300" y="598" text-anchor="middle" style="{_TXT}">REZERVOR</text>'
               f'<text x="174" y="470" style="{_TXT}">FILTRU</text>'
               f'<text x="255" y="352" text-anchor="middle" style="{_TXT}">POMPA</text>'
               f'<text x="660" y="44" text-anchor="middle" style="{_TXT}">RAMPA</text>'
               f'<text x="660" y="370" text-anchor="middle" style="{_TXT}">INJECTOARE</text>'
               f'<text x="990" y="360" text-anchor="middle" transform="rotate(90 990 360)" style="{_TXT};font-size:18px;fill:#b6c2cf">RETUR</text>')
    return f'<svg width="1000" height="720" viewBox="0 0 1000 720"><defs>{_ST}</defs>{_parts()}{lab}</svg>'

def sys_hl(names, col='#ff4b4b', fill='rgba(255,75,75,.22)'):
    """evidentiere aliniata cu schema (acelasi cadru 1000x720)"""
    flt = '<filter id="gl" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
    return f'<svg width="1000" height="720" viewBox="0 0 1000 720"><defs>{flt}</defs><g filter="url(#gl)">{_parts(col, fill, names, sw=6)}</g></svg>'

def sys_paths():
    """traseele de curgere in coordonate de cadru"""
    ox, oy = SYS_X, SYS_Y
    def T(pts): return Poly([(x + ox, y + oy) for x, y in pts])
    lp = T([(115, 650), (115, 520), (115, 380), (115, 250), (170, 250), (255, 250)])
    hp = [(255, 250), (255, 83), (380, 83)]
    inj = [T(hp + [(x, 83), (x, 334)]) for x in INJ_X]
    rail_inj = [T([(380, 83), (x, 83), (x, 334)]) for x in INJ_X]
    ret = T([(940, 83), (975, 83), (975, 625), (560, 625)])
    tank = T([(60, 650), (540, 650)])
    return dict(lp=lp, inj=inj, rail_inj=rail_inj, ret=ret, tank=tank)

SYS_BOX = {'tank': (40, 560, 520, 130), 'filter': (70, 380, 90, 140), 'pump': (170, 150, 170, 170), 'rail': (380, 60, 560, 46)}
def sys_pt(name):
    x, y, w, h = SYS_BOX[name]; return (SYS_X + x + w / 2, SYS_Y + y + h / 2)

# ------------------------------------------------------------------ pictograme noi
ICON2 = {
 'key': '<svg width="80" height="80" viewBox="0 0 64 64"><circle cx="20" cy="32" r="11" fill="none" stroke="#FFB224" stroke-width="5"/><path d="M31 32h26M49 32v9M56 32v7" stroke="#FFB224" stroke-width="5" stroke-linecap="round"/></svg>',
 'tow': '<svg width="80" height="80" viewBox="0 0 64 64"><path d="M6 42V30h14l6-8h10v20z" fill="none" stroke="#FFB224" stroke-width="4" stroke-linejoin="round"/><path d="M36 42h22M36 30l18-14M54 16v10" stroke="#FFB224" stroke-width="4" stroke-linecap="round"/><circle cx="16" cy="46" r="5" fill="#fff"/><circle cx="46" cy="46" r="5" fill="#fff"/></svg>',
 'drain': '<svg width="80" height="80" viewBox="0 0 64 64"><rect x="6" y="12" width="52" height="26" rx="7" fill="none" stroke="#FFB224" stroke-width="4.5"/><path d="M32 38v8" stroke="#FFB224" stroke-width="4.5"/><path d="M32 50c-4 5-4 8 0 8s4-3 0-8z" fill="#ffc02a"/></svg>',
 'wrench': '<svg width="80" height="80" viewBox="0 0 64 64"><path d="M10 52l24-24" stroke="#FFB224" stroke-width="7" stroke-linecap="round"/><path d="M34 28a12 12 0 1 0 6-16l-6 6 2 6 6 2 6-6a12 12 0 0 1-14 8z" fill="#FFB224"/><path d="M14 22a18 18 0 0 1 10-10" fill="none" stroke="#fff" stroke-width="3.5" stroke-linecap="round"/><path d="M22 10l3 3-4 2" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"/></svg>',
 'cap': '<svg width="80" height="80" viewBox="0 0 64 64"><rect x="18" y="14" width="28" height="22" rx="5" fill="#ff4b4b"/><rect x="22" y="36" width="20" height="14" fill="#cfd6de"/><path d="M22 41h20M22 46h20" stroke="#7d8894" stroke-width="2"/></svg>',
 'clean': '<svg width="80" height="80" viewBox="0 0 64 64"><path d="M32 8l4 10 10 4-10 4-4 10-4-10-10-4 10-4z" fill="#3ddc84"/><path d="M48 36l2.5 6 6 2.5-6 2.5L48 53l-2.5-6-6-2.5 6-2.5z" fill="#fff"/><path d="M16 40l2 5 5 2-5 2-2 5-2-5-5-2 5-2z" fill="#fff"/></svg>',
 'pipe': '<svg width="80" height="80" viewBox="0 0 64 64"><path d="M6 40h30l10-8h12" fill="none" stroke="#ff5a26" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/><path d="M40 22l6 10-6 10" fill="none" stroke="#fff" stroke-width="4" stroke-linejoin="round"/></svg>',
 'air': '<svg width="80" height="80" viewBox="0 0 64 64"><circle cx="22" cy="38" r="10" fill="none" stroke="#e8edf3" stroke-width="4"/><circle cx="42" cy="24" r="7" fill="none" stroke="#e8edf3" stroke-width="4"/><circle cx="44" cy="46" r="5" fill="none" stroke="#e8edf3" stroke-width="3.5"/></svg>',
 'ret': '<svg width="80" height="80" viewBox="0 0 64 64"><path d="M50 14v18a10 10 0 0 1-10 10H14" fill="none" stroke="#ffc02a" stroke-width="5" stroke-linecap="round"/><path d="M22 34l-8 8 8 8" fill="none" stroke="#ffc02a" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>',
 'ecu': '<svg width="80" height="80" viewBox="0 0 64 64"><rect x="10" y="14" width="44" height="36" rx="5" fill="none" stroke="#FFB224" stroke-width="4.5"/><path d="M18 22h12M18 30h20M18 38h8" stroke="#fff" stroke-width="3.5" stroke-linecap="round"/><path d="M16 8v6M26 8v6M36 8v6M46 8v6M16 50v6M26 50v6M36 50v6M46 50v6" stroke="#FFB224" stroke-width="3"/></svg>',
 'bench': '<svg width="80" height="80" viewBox="0 0 64 64"><rect x="8" y="40" width="48" height="16" rx="3" fill="none" stroke="#FFB224" stroke-width="4"/><path d="M20 40V14h24v26" fill="none" stroke="#FFB224" stroke-width="4"/><path d="M32 18v14" stroke="#fff" stroke-width="5"/><path d="M28 32h8l-2 6h-4z" fill="#fff"/><circle cx="48" cy="48" r="3" fill="#3ddc84"/></svg>',
 'part': '<svg width="80" height="80" viewBox="0 0 64 64"><circle cx="32" cy="32" r="12" fill="none" stroke="#FFB224" stroke-width="5"/><path d="M32 8v8M32 48v8M8 32h8M48 32h8M15 15l6 6M43 43l6 6M15 49l6-6M43 21l6-6" stroke="#FFB224" stroke-width="5" stroke-linecap="round"/></svg>',
 'plug': '<svg width="80" height="80" viewBox="0 0 64 64"><rect x="16" y="22" width="32" height="24" rx="5" fill="none" stroke="#FFB224" stroke-width="4.5"/><path d="M24 10v12M40 10v12M32 46v12" stroke="#FFB224" stroke-width="4.5" stroke-linecap="round"/><circle cx="24" cy="34" r="3" fill="#3ddc84"/><circle cx="40" cy="34" r="3" fill="#3ddc84"/></svg>',
 'bolt': '<svg width="80" height="80" viewBox="0 0 64 64"><path d="M36 6L14 36h14l-4 22 22-30H32z" fill="#FFB224"/></svg>',
 'cut': '<svg width="80" height="80" viewBox="0 0 64 64"><path d="M6 32h18M40 32h18" stroke="#FFB224" stroke-width="6" stroke-linecap="round"/><path d="M26 22l4 8-4 4 6 8" fill="none" stroke="#ff4b4b" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/></svg>',
 'layers': '<svg width="80" height="80" viewBox="0 0 64 64"><g fill="#cfd6de"><rect x="14" y="10" width="36" height="4"/><rect x="14" y="17" width="36" height="4"/><rect x="14" y="24" width="36" height="4"/><rect x="14" y="31" width="36" height="4"/><rect x="14" y="38" width="36" height="4"/><rect x="14" y="45" width="36" height="4"/></g><g fill="#FFB224"><rect x="14" y="14" width="36" height="3"/><rect x="14" y="28" width="36" height="3"/><rect x="14" y="42" width="36" height="3"/></g></svg>',
 'odo': '<svg width="80" height="80" viewBox="0 0 64 64"><path d="M8 44a24 24 0 0 1 48 0" fill="none" stroke="#FFB224" stroke-width="5" stroke-linecap="round"/><path d="M32 44l12-14" stroke="#fff" stroke-width="5" stroke-linecap="round"/><circle cx="32" cy="44" r="5" fill="#fff"/></svg>',
 'flame': '<svg width="80" height="80" viewBox="0 0 64 64"><path d="M32 6c4 10 14 14 14 28a14 14 0 0 1-28 0c0-8 5-12 7-18 2 5 5 7 7 7 0-6-2-11 0-17z" fill="#ff5a26"/><path d="M32 30c3 5 7 7 7 13a7 7 0 0 1-14 0c0-4 3-7 7-13z" fill="#FFD21F"/></svg>',
 'drop': '<svg width="80" height="80" viewBox="0 0 64 64"><path d="M32 6C24 20 14 30 14 40a18 18 0 0 0 36 0C50 30 40 20 32 6z" fill="#ffc02a"/></svg>',
 'oil': '<svg width="80" height="80" viewBox="0 0 64 64"><path d="M10 26h28l8-8h8v8l-8 4v20H10z" fill="none" stroke="#FFB224" stroke-width="4.5" stroke-linejoin="round"/><path d="M56 34c-3 5-3 8 0 8s3-3 0-8z" fill="#FFB224"/></svg>',
 'barrel': '<svg width="80" height="80" viewBox="0 0 64 64"><rect x="16" y="8" width="32" height="48" rx="6" fill="none" stroke="#ff8a3a" stroke-width="4.5"/><path d="M16 22h32M16 42h32" stroke="#ff8a3a" stroke-width="4"/></svg>',
 'crystal': '<svg width="80" height="80" viewBox="0 0 64 64"><path d="M32 6l10 14-10 38-10-38z" fill="#eef6ff"/><path d="M14 22l8 6-4 22-8-18z" fill="#cfe3f5"/><path d="M50 22l-8 6 4 22 8-18z" fill="#cfe3f5"/></svg>',
}
