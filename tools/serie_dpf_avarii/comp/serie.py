"""Seria „De ce intră filtrul de particule în avarie” · montajul unui episod (9:16), pe straturile Blender ale filtrului (eng.py).

  EP=3 python3 serie.py --info                 cronologia episodului
  EP=3 python3 serie.py --cues                 scrie ../vo/epNN/cues.json (unde începe fiecare rând; pentru pista de voce)
  EP=3 python3 serie.py --mid [--only 0,5]     cadre de probă (mijlocul fiecărui rând) în proof/epNN_RR.png
  EP=3 python3 serie.py --png 12.5,40          cadre la secundele date
  EP=3 python3 serie.py --out x.mp4 [--frames a b]
Un rând rostit = un plan (shots.py). Lungimea planului = lungimea rândului rostit (../vo/meas.json).
"""
import sys, os, json, math, subprocess, re, unicodedata
import numpy as np, skia
from fk import *
import eng as E
from eng import (W, H, FPS, Y, WHT, BG, C_GAS, C_CLN, C_SOOT, C_ASH, C_FUEL, SAMP, XM, D, DPF_Z0, DPF_Z1, DOC_Z0, DOC_Z1, PLUG, CELLS, J_IN, X_IN, X_OUT, X_WALL,
                 proj, to_screen, anchor, fit_px, fit_view, box3, view_at, zoomed, interp_view, BBX)

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
sys.path.insert(0, ROOT)
from episoade import EP as EPS, SERIA, N as NEP
from statx import rows_full
import shots as SHM

EPN = int(os.environ.get('EP', '1'))
EPD = [e for e in EPS if e['n'] == EPN][0]
ROWS = rows_full(EPD); N = len(ROWS); FINAL = bool(EPD.get('final'))
GRN, RED = '#57d08a', '#ff5a4a'

# ------------------------------------------------------------------ layout (9:16, cu loc liber jos pentru interfața rețelelor)
R_FULL = (40, 200, 1040, 1370); R_HI = (40, 200, 1040, 925); R_PAN = (40, 945, 1040, 1378)
CAPX, CAPY, CAPW = 60, 1452, 960


def mk_views(R):
    p = 22; Rp = (R[0] + p, R[1] + p, R[2] - p, R[3] - p)
    cxm, cym = (R[0] + R[2]) / 2, (R[1] + R[3]) / 2; wr, hr = R[2] - R[0], R[3] - R[1]
    V = {}
    V['ext'] = fit_px(BBX['ext'], Rp)
    V['wide'] = fit_px(BBX['sec'], Rp)
    V['can'] = fit_view(box3(-150, 150, -256, 176, 0, 30), Rp)
    V['right'] = fit_view(box3(-70, 196, -236, 252, 0, 30), Rp)
    V['dps'] = fit_view(box3(46, 192, -10, 252, 0, 30), Rp)
    V['top'] = fit_view(box3(-196, 110, 56, 334, 0, 30), Rp)
    V['mid'] = fit_view(box3(-200, 120, -96, 112, 0, 30), Rp)
    V['bot'] = fit_view(box3(-196, 150, -336, -150, 0, 30), Rp)
    V['doc'] = view_at((XM, 0.0, 61.0), min(wr / 70.0, hr / 88.0), cxm, cym)
    V['face'] = view_at((XM, 0.0, -6.0), min(wr / 62.0, hr / 64.0), cxm, cym)
    V['maca'] = view_at((XM, 0.0, -6.1), 72.0, cxm, cym + 10)
    V['macb'] = view_at((XM, 0.0, -171.2), 72.0, cxm, cym + 10)
    return V


VIEWS = {0: mk_views(R_FULL), 1: mk_views(R_HI)}

# ------------------------------------------------------------------ planurile episodului
_user = SHM.SHOTS[EPN]
SH = []
for _i in range(N):
    if _i == N - 2: s = dict(v='ext', rev=0.0, flow=0.0, kind='c1')
    elif _i == N - 1: s = dict(v='ext', rev=0.0, flow=0.0, kind='c2')
    else:
        s = dict(_user[_i] if _i < len(_user) and _user[_i] else {})
        if _i == 1: s.setdefault('v', 'wide'); s['kind'] = 'title'
        elif _i == 0: s['kind'] = 'hook'
    s.setdefault('v', 'wide'); s.setdefault('kind', 'row')
    s['big'] = s.get('big', ROWS[_i][2]); s['say'] = ROWS[_i][0]
    SH.append(s)
if FINAL: SH[1]['say'] = ROWS[1][0]
else: SH[1]['say'] = f"Seria „{SERIA}”. Episodul {EPN} din {NEP}: {EPD['nume']}."

# ------------------------------------------------------------------ vocea: durate și cuvinte
_L = json.load(open(os.path.join(ROOT, 'vo', 'lines.json')))
_MP = os.path.join(ROOT, 'vo', 'meas.json'); MEAS = json.load(open(_MP)) if os.path.exists(_MP) else {}
_AP = os.path.join(ROOT, 'vo', 'asr.json'); ASR = json.load(open(_AP)) if os.path.exists(_AP) else {}
IDS = _L['eps'][str(EPN)]; JOIN = 0.22


def _sp1(k): return MEAS[str(k)]['sp'] if str(k) in MEAS else len(_L['lines'][k]['v']) / 15.6 + 0.2


def sp(i): return sum(_sp1(k) for k in IDS[i]) + JOIN * (len(IDS[i]) - 1)


def _nrm(s):
    s = unicodedata.normalize('NFD', s.lower()); return ''.join(c for c in s if unicodedata.category(c) != 'Mn' and c.isalnum())


WORDS = []
for _i in range(N):
    ws = []; off = 0.0
    for k in IDS[_i]:
        ws += [(_nrm(w), t + off) for w, t in ASR.get(str(k), {}).get('words', [])]; off += _sp1(k) + JOIN
    WORDS.append(ws)

T0, LEAD = 0.25, 0.22
GAPS = [0.36] * N; GAPS[1] = 0.42; GAPS[2] = 0.45; GAPS[N - 2] = 0.55; GAPS[N - 1] = 0.45
CUE = []; _t = T0
for _i in range(N):
    if _i > 0: _t += GAPS[_i]
    CUE.append(_t); _t += sp(_i)
T_END = _t; DUR = T_END + 2.4
SS = [0.0] + [CUE[i] - LEAD for i in range(1, N)]; SE = SS[1:] + [DUR]
NF = int(round(DUR * FPS))


def wt(i, key, default=None):
    """secunde de la începutul rândului i până la primul cuvânt care începe cu `key` (număr = fracțiune din rând)."""
    if isinstance(key, (int, float)): return key * sp(i)
    for w, t in WORDS[i]:
        if w.startswith(_nrm(key)): return max(0.0, t)
    return default if default is not None else 0.3 * sp(i)


def shot_at(t):
    lo, hi = 0, N - 1
    while lo < hi:
        m = (lo + hi + 1) // 2
        if SS[m] <= t: lo = m
        else: hi = m - 1
    return lo


DEF = dict(E.SDEF); DEF['hi'] = 0.0
TRK = dict(rev=1.2, hi=0.6, soot=1.0, tint=0.8)
RES = {}
for _k in DEF:
    prev = DEF[_k]; RES[_k] = []
    for _i, s in enumerate(SH):
        x = s.get(_k, DEF[_k])
        if _k == 'hi': x = 1.0 if 'pan' in s else 0.0
        if isinstance(x, tuple):
            a, b = x[0], x[1]; f0 = x[2] if len(x) > 2 else 0.0; f1 = x[3] if len(x) > 3 else 1.0
            if isinstance(f0, str):                       # pornește la un cuvânt rostit, ține f1 secunde
                w0 = wt(_i, f0) + LEAD; d = SE[_i] - SS[_i]; f0, f1 = w0 / d, min(1.0, (w0 + x[3]) / d)
            RES[_k].append(('anim', a, b, f0, f1, prev)); prev = b
        else:
            RES[_k].append(('to', prev, float(x), 0.0, 1.0, prev)); prev = float(x)


def sval(k, t, i=None):
    if i is None: i = shot_at(t)
    kind, a, b, f0, f1, pe = RES[k][i]; tl = t - SS[i]
    if kind == 'to': return lerp(a, b, sm(tl / TRK.get(k, 0.8)))
    f = tl / (SE[i] - SS[i]); v = lerp(a, b, sm((f - f0) / max(1e-6, f1 - f0)))
    return lerp(pe, v, sm(tl / 0.5)) if abs(pe - a) > 1e-6 else v


def pv(x, f):
    if isinstance(x, tuple):
        f0 = x[2] if len(x) > 2 else 0.0; f1 = x[3] if len(x) > 3 else 1.0
        return lerp(x[0], x[1], sm((f - f0) / max(1e-6, f1 - f0)))
    return x


def hl_times(i, spec):
    kind, a, b = spec; d = SE[i] - SS[i]
    t0 = SS[i] + (a * d if isinstance(a, (int, float)) else LEAD + wt(i, a) - 0.15)
    t1 = SS[i] + (b * d if isinstance(b, (int, float)) else LEAD + wt(i, b, 0.9 * sp(i)) - 0.1)
    return kind, t0, max(t1, t0 + 0.8)


HLT = [[hl_times(i, s_) for s_ in s.get('hl', [])] for i, s in enumerate(SH)]


def state(t):
    i = shot_at(t); s = SH[i]; f = (t - SS[i]) / (SE[i] - SS[i])
    S = {k: sval(k, t, i) for k in DEF}
    S['t'] = t; S['ft'] = flow_time(t); S['ct'] = chan_time(t); S['i'] = i; S['f'] = f
    S['chem'] = s.get('chem')
    if S['chem'] is None and i > 0 and t - SS[i] < 0.5: S['chem'] = SH[i - 1].get('chem')
    S['dropcol'] = s.get('dropcol', '#5a3410')
    fr = s.get('front'); S['front'] = None if fr is None else pv(fr, f)
    h = {}
    for j in (i - 1, i):
        if j < 0: continue
        for kind, t0, t1 in HLT[j]:
            a = ramp(t, t0, 0.25) * (1 - ramp(t, t1, 0.6)) * (0.82 + 0.18 * math.sin(t * 5.0))
            if a > 0.01: h[kind] = max(h.get(kind, 0.0), a)
    S['hl'] = h
    return S


# ------------------------------------------------------------------ camera
def _vkey(i): return (SH[i]['v'], 1 if 'pan' in SH[i] else 0)


GRP = []
for _i in range(N):
    if _i == 0 or _vkey(_i) != _vkey(_i - 1): GRP.append([_i, _i])
    else: GRP[-1][1] = _i
PRE = 0.3


def gview(g, t):
    a, b = GRP[g]; name, hi = _vkey(a); u = cl((t - SS[a]) / (SE[b] - SS[a]))
    k = 0.03 if name.startswith('mac') else (0.09 if a == 0 else 0.05)
    return zoomed(VIEWS[hi][name], 1.0 + k * u)


def cam(t):
    g = 0
    for k in range(len(GRP)):
        if SS[GRP[k][0]] - PRE <= t: g = k
    Vc = gview(g, t)
    if g == 0: return Vc, None, 0.0
    gs = SS[GRP[g][0]]; Vp = gview(g - 1, gs)
    r = abs(math.log(Vc[0] / Vp[0]))
    dist = math.hypot(Vc[1] - Vp[1], Vc[2] - Vp[2]) * min(Vc[0], Vp[0]) / W
    if r > math.log(5.0):
        m = sm((t - (gs - 0.25)) / 0.5)
        return (Vc, None, 0.0) if m >= 0.999 else (Vp, Vc, m)
    mv = 0.8 + 0.5 * r + 0.3 * min(1.5, dist)
    return interp_view(Vp, Vc, sm((t - (gs - PRE)) / mv)), None, 0.0


def chan_speed(z): return max(4.4, min(11.0, 330.0 / (z * E.PXMM)))


_CS = None; _FT = None


def chan_time(t):
    global _CS
    if _CS is None:
        v = []
        for k in range(NF + 2):
            a, b, m = cam(k / FPS); v.append(chan_speed((b if (b is not None and m > 0.5) else a)[0]) / 5.0 / FPS)
        _CS = np.concatenate([[0], np.cumsum(v)])
    return float(_CS[min(len(_CS) - 1, max(0, int(round(t * FPS))))])


def flow_time(t):
    """timpul gazelor, integrat cu viteza lor (gspeed), ca să nu sară când se schimbă viteza."""
    global _FT
    if _FT is None: _FT = np.concatenate([[0], np.cumsum([sval('gspeed', k / FPS) / FPS for k in range(NF + 2)])])
    return float(_FT[min(len(_FT) - 1, max(0, int(round(t * FPS))))])


# ------------------------------------------------------------------ UI
def wrap_lines(text, size, name, maxw):
    out = []
    for para in text.split('\n'):
        cur = ''
        for wd in para.split():
            cand = (cur + ' ' + wd).strip()
            if tw(cand, size, name) > maxw and cur: out.append(cur); cur = wd
            else: cur = cand
        out.append(cur)
    return out


def tick(c, x, y, s, col, a, w=None):
    c.drawPath(path_of([(x - s * 0.5, y), (x - s * 0.12, y + s * 0.38), (x + s * 0.55, y - s * 0.42)]), P(col, a, stroke=w or s * 0.24, join='miter'))


def cross(c, x, y, s, col, a, w=None):
    c.drawLine(x - s * 0.42, y - s * 0.42, x + s * 0.42, y + s * 0.42, P(col, a, stroke=w or s * 0.24)); c.drawLine(x - s * 0.42, y + s * 0.42, x + s * 0.42, y - s * 0.42, P(col, a, stroke=w or s * 0.24))


def _wm(c, t, pw, pk=None, cols=None):
    c.save(); c.rotate(-20, W / 2, H / 2)
    f = font('anton', 58); s = 'TURBO DOCTOR'; w = f.measureText(s) + 120; off = (t * 9) % w
    for row in range(-16, 26):
        yy = row * 110; sh = (row % 2) * w / 2
        for k in range(-4, 9):
            x = -600 + k * w + sh + off
            if pk is not None: c.drawString(s, x + 2, yy + 2, f, pk); c.drawString(s, x, yy, f, pw)
            else:
                col = (1, 1, 1, .04) if (row + k) % 3 else (1, .76, .1, .052)
                c.drawString(s, x, yy, f, P(col[:3], col[3]))
    c.restore()


def background(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), P(shader=lin(0, 0, 0, H, ['#0e1a2c', '#060b14'])))
    cx, cy = W / 2, H * 0.42; R = H * 0.62
    c.drawCircle(cx, cy, R, P(shader=rad(cx, cy, R, [skia.Color4f(.13, .21, .34, .55).toColor(), skia.Color4f(0, 0, 0, 0).toColor()])))
    _wm(c, t, None)


def watermark_over(c, t, a):
    if a > 0.01: _wm(c, t, P('#ffffff', 0.034 * a), P('#000000', 0.040 * a))


_K = lambda a: skia.Color4f(0.02, 0.04, 0.07, a).toColor()


def bands(c, hi):
    c.drawRect(skia.Rect.MakeLTRB(0, 0, W, 215), P(shader=lin(0, 0, 0, 215, [_K(0.95), _K(0.86), _K(0.0)], [0.0, 0.66, 1.0])))
    yb = lerp(R_FULL[3], R_HI[3], hi)
    c.drawRect(skia.Rect.MakeLTRB(0, yb - 70, W, H), P(shader=lin(0, yb - 70, 0, yb + 40, [_K(0.0), _K(0.94)])))


def header(c, t):
    x0, x1 = 60, 1020
    w = txt(c, 'TURBO', x0, 104, 34, 'anton', WHT, 1.0); txt(c, 'DOCTOR', x0 + w + 7, 104, 34, 'anton', Y, 1.0)
    s_ = 'EPISODUL FINAL' if FINAL else f'EPISODUL {EPN} DIN {NEP}'
    wd = tw(s_, 22, 'm9') + 28
    rrect(c, x1 - wd, 76, x1, 112, 10, P(Y, 1.0)); txt(c, s_, x1 - wd / 2, 102, 22, 'm9', BG, 1.0, 'c')
    txt(c, 'DE CE INTRĂ FILTRUL DE PARTICULE ÎN AVARIE', x0, 140, 19, 'm8', WHT, 0.62)
    txt(c, 'MODEL 3D RECONSTRUIT', x1, 140, 15, 'm8', WHT, 0.36, 'r')
    rrect(c, x0, 156, x1, 162, 3, P('#ffffff', 0.16)); rrect(c, x0, 156, x0 + (x1 - x0) * cl(t / T_END), 162, 3, P(Y, 0.95))


def label(c, text, ax, ay, side, ly, a, R, col=WHT, size=27, dot=Y):
    if a <= 0.01: return
    lines = text.split('\n'); tw_ = max(tw(s_, size, 'm8') for s_ in lines); lh = size * 1.22
    bh = size * 1.34 + lh * (len(lines) - 1)
    x0 = R[0] + 18 if side == 'L' else R[2] - 18 - tw_ - 28
    y0 = max(R[1] + 6, min(R[3] - bh - 6, ly - bh / 2))
    c.drawCircle(ax, ay, 6, P(dot, a)); c.drawCircle(ax, ay, 12, P(dot, a * 0.35, stroke=2))
    ex = x0 if ax < x0 else (x0 + tw_ + 28 if ax > x0 + tw_ + 28 else ax)
    ey = y0 + bh / 2 if (ax < x0 or ax > x0 + tw_ + 28) else (y0 if ay < y0 else y0 + bh)
    c.drawPath(path_of([(ax, ay), (ex, ey)]), P(dot, a * 0.85, stroke=2.4))
    rrect(c, x0, y0, x0 + tw_ + 28, y0 + bh, 12, P('#0b1424', a * 0.9))
    rrect(c, x0, y0, x0 + tw_ + 28, y0 + bh, 12, P(dot, a * 0.55, stroke=2))
    for k, s_ in enumerate(lines): txt(c, s_, x0 + 14, y0 + size * 1.0 + k * lh, size, 'm8', col, a)


def _lbkey(l): return (l[0], str(l[1]))


def labels(c, t, V):
    for i in (shot_at(t) - 1, shot_at(t)):
        if i < 0 or t > SE[i] + 0.1: continue
        s = SH[i]; R = R_HI if 'pan' in s else R_FULL
        nxt = {_lbkey(l) for l in SH[i + 1].get('lb', [])} if i + 1 < N else set()
        prv = {_lbkey(l) for l in SH[i - 1].get('lb', [])} if i > 0 else set()
        for l in s.get('lb', []):
            text, key, side, yf, at = l[0], l[1], l[2], l[3], (l[4] if len(l) > 4 else 0.15)
            t0 = SS[i] + LEAD + (wt(i, at) if isinstance(at, str) else at * sp(i)) - 0.1
            a = 1.0 if _lbkey(l) in prv else ramp(t, t0, 0.3)
            if _lbkey(l) not in nxt: a *= 1 - ramp(t, SE[i] - 0.45, 0.3)
            elif t > SE[i]: continue
            if a <= 0.01: continue
            ax, ay = anchor(V, p3=key) if isinstance(key, tuple) else anchor(V, key)
            label(c, text, ax, ay, side, R[1] + yf * (R[3] - R[1]), a, R, dot=(RED if (len(l) > 5 and l[5] == 'bad') else Y))
        if s.get('flb'):
            fr = pv(s['front'], (t - SS[i]) / (SE[i] - SS[i]))
            if DPF_Z0 + 4.0 < fr < DPF_Z1 - 4.0:
                ax, ay = anchor(V, p3=(-56.0, 0.0, fr))
                label(c, 'Funinginea arde', ax, ay, 'L', ay + 4, cl((DPF_Z1 - 4.0 - fr) / 8.0) * cl((fr - DPF_Z0 - 44.0) / 14.0), R)


def tcol(v): return mix(mix('#8fd0ff', '#ffffff', cl((v - 200) / 150.0)), '#ff6a2a', cl((v - 380) / 240.0))


def temps(c, t, V):
    i = shot_at(t); s = SH[i]
    if 'temps' not in s: return
    f = (t - SS[i]) / (SE[i] - SS[i]); R = R_HI if 'pan' in s else R_FULL
    a = (1.0 if (i > 0 and 'temps' in SH[i - 1]) else ramp(t, SS[i] + 0.3, 0.4)) * (1.0 if (i + 1 < N and 'temps' in SH[i + 1]) else 1 - ramp(t, SE[i] - 0.45, 0.3))
    if a <= 0.01: return
    for k, (key, nm) in enumerate((('t1', 'T1'), ('t2', 'T2'), ('t3', 'T3'))):
        if s['temps'][k] is None: continue
        v = pv(s['temps'][k], f); ax, ay = anchor(V, key)
        s_ = f'{int(round(v / 5.0) * 5)} °C'.replace('-', '−'); wd = tw(nm, 20, 'm8') + tw(s_, 30, 'anton') + 44
        x0 = R[0] + 18; y0 = ay - 86 if k < 2 else ay - 96
        col = tcol(v) if v > -30 else RED
        c.drawPath(path_of([(ax, ay), (x0 + wd * 0.6, y0 + 50)]), P(col, a * 0.8, stroke=2.2)); c.drawCircle(ax, ay, 5, P(col, a))
        rrect(c, x0, y0, x0 + wd, y0 + 52, 12, P('#0b1424', a * 0.93)); rrect(c, x0, y0, x0 + wd, y0 + 52, 12, P(col, a * 0.8, stroke=2))
        txt(c, nm, x0 + 14, y0 + 34, 20, 'm8', WHT, a * 0.8); txt(c, s_, x0 + 26 + tw(nm, 20, 'm8'), y0 + 39, 30, 'anton', col, a)


def fit_txt(s, size, name, maxw, lo=30):
    while tw(s, size, name) > maxw and size > lo: size -= 2
    return size


def caption(c, t):
    for i in (shot_at(t) - 1, shot_at(t)):
        if i < 0: continue
        s = SH[i]; kind = s['kind']
        if kind in ('title', 'c2'): continue
        ti = s['big']; body = s['say']
        a_t = ramp(t, SS[i] + 0.06, 0.22) * (1 - ramp(t, SE[i] - 0.3, 0.28))
        a_b = ramp(t, SS[i] + 0.12, 0.25) * (1 - ramp(t, SE[i] - 0.3, 0.28))
        if kind == 'hook':
            ts = fit_txt(ti, 96, 'anton', CAPW, 44); pop = 1.0 + 0.16 * (1 - ramp(t, 0.0, 0.42)); a_t = 1 - ramp(t, SE[i] - 0.3, 0.28)
            c.save(); c.translate(W / 2, CAPY + 22); c.scale(pop, pop)
            wd = tw(ti, ts, 'anton')
            rrect(c, -wd / 2 - 26, -ts * 0.98, wd / 2 + 26, ts * 0.30, 14, P(Y, a_t))
            txt(c, ti, 0, 0, ts, 'anton', BG, a_t, 'c')
            c.restore(); yy = CAPY + 104
        else:
            ts = fit_txt(ti, 60, 'anton', CAPW, 34)
            if a_t > 0.01: txt(c, ti, CAPX, CAPY + 12 * (1 - a_t), ts, 'anton', Y, a_t, shadow=10)
            yy = CAPY + 62
        if a_b > 0.01:
            fs = 35; ls = wrap_lines(body, fs, 'm7', CAPW)
            if len(ls) > 3: fs = 32; ls = wrap_lines(body, fs, 'm7', CAPW)
            for ln in ls:
                txt(c, ln, CAPX, yy, fs, 'm7', WHT, a_b, shadow=8); yy += fs * 1.27


NOTES = {'ilu': 'VALORI ILUSTRATIVE', 'sim': 'STARE SIMULATĂ', 'sch': 'DESEN SCHEMATIC', 'ex': 'EXEMPLU · DIFERĂ DE LA MOTOR LA MOTOR'}


def note_tag(c, t):
    i = shot_at(t); n = SH[i].get('note')
    if not n: return
    a = (1.0 if (i > 0 and SH[i - 1].get('note') == n) else ramp(t, SS[i] + 0.3, 0.3)) * (1.0 if (i + 1 < N and SH[i + 1].get('note') == n) else 1 - ramp(t, SE[i] - 0.4, 0.3))
    s_ = NOTES[n]; x, y = 1020, 206; wd = tw(s_, 17, 'm8') + 24
    rrect(c, x - wd, y - 22, x, y + 8, 8, P('#0b1424', a * 0.8)); rrect(c, x - wd, y - 22, x, y + 8, 8, P('#ffffff', a * 0.3, stroke=1.3))
    txt(c, s_, x - 12, y, 17, 'm8', WHT, a * 0.78, 'r')


def legend(c, t):
    i = shot_at(t)
    if not SH[i].get('leg'): return
    a = ramp(t, SS[i] + 0.6, 0.4) * (1 - ramp(t, SE[i] - 0.4, 0.3)); R = R_HI if 'pan' in SH[i] else R_FULL
    x, y = 60, R[3] - 16
    for col, s_ in ((C_GAS, 'gaze cu funingine'), (C_CLN, 'gaze filtrate')):
        c.drawRoundRect(skia.Rect.MakeXYWH(x, y - 20, 24, 24), 6, 6, P(col, a)); x += 34 + txt(c, s_, x + 34, y, 23, 'm7', WHT, a * 0.9, shadow=6) + 30


# ------------------------------------------------------------------ panouri
def pbox(c, R, a, title=None, ts=31):
    x0, y0, x1, y1 = R
    rrect(c, x0, y0, x1, y1, 22, P('#0a1322', a * 0.95)); rrect(c, x0, y0, x1, y1, 22, P('#ffffff', a * 0.15, stroke=1.6))
    if title:
        ts = fit_txt(title, ts, 'anton', x1 - x0 - 56, 20); txt(c, title, x0 + 28, y0 + 50, ts, 'anton', Y, a)


def ro(v, d=1): return f'{v:.{d}f}'.replace('.', ',')


def item_times(i, p, n):
    ats = p.get('at') or [0.12 + 0.72 * k / n for k in range(n)]
    return [LEAD + (wt(i, a_) if isinstance(a_, str) else a_ * sp(i)) - 0.12 for a_ in ats]


def pan_card(c, R, a, i, f, tl, p):
    x0, y0, x1, y1 = R; pbox(c, R, a, p.get('title'), 36)
    items = p['items']; n = len(items); top = 78 if p.get('title') else 26
    fs = 40 if n <= 3 else (37 if n == 4 else 33)
    while True:
        rows = [wrap_lines(s_, fs, 'm7', x1 - x0 - 120) for (kind, s_) in items]
        nl = sum(len(r) for r in rows); lh = fs * 1.26
        if nl * lh + (n - 1) * 6 <= y1 - y0 - top - 22 or fs <= 22: break
        fs -= 1
    gp = min(34.0, (y1 - y0 - top - 22 - nl * lh) / max(1, n))
    yy = y0 + top + (y1 - y0 - top - 16 - nl * lh - (n - 1) * gp) / 2 + fs * 0.8; last = -1
    tts = item_times(i, p, n)
    for k in range(n):
        if tl >= tts[k]: last = k
    for k, ((kind, s_), ls) in enumerate(zip(items, rows)):
        ai = a * ramp(tl, tts[k], 0.3); cur = k == last
        if ai > 0.01:
            bx, by = x0 + 50, yy - fs * 0.34; dx = 10 * (1 - ramp(tl, tts[k], 0.3))
            if kind == 'ok': c.drawCircle(bx, by, 20, P(GRN, ai * 0.2)); tick(c, bx, by, 25, GRN, ai)
            elif kind == 'bad': c.drawCircle(bx, by, 20, P(RED, ai * 0.2)); cross(c, bx, by, 22, RED, ai)
            elif kind.isdigit(): c.drawCircle(bx, by, 21, P(Y if cur else '#22314a', ai)); txt(c, kind, bx, by + 9, 26, 'm9', BG if cur else WHT, ai, 'c')
            else: c.drawCircle(bx, by, 9, P(Y, ai)); c.drawCircle(bx, by, 17, P(Y, ai * (0.35 if cur else 0.0), stroke=2))
            for j, ln in enumerate(ls): txt(c, ln, x0 + 92 + dx, yy + j * lh, fs, 'm7', WHT, ai * (1.0 if cur else 0.8))
        yy += len(ls) * lh + gp


def pan_codes(c, R, a, i, f, tl, p):
    x0, y0, x1, y1 = R; pbox(c, R, a, p['title'])
    rows = p['rows']; n = len(rows); fs = 28
    rh = min(74.0, (y1 - y0 - 96) / n); yy = y0 + 92 + rh * 0.5
    cw = max(tw(code, fs + 4, 'm9') for code, _ in rows) + 34
    for k, (code, s_) in enumerate(rows):
        ak = a * ramp(tl, 0.4 + 0.4 * k, 0.3)
        rrect(c, x0 + 30, yy - 25, x0 + 30 + cw, yy + 23, 10, P('#1a2740', ak)); rrect(c, x0 + 30, yy - 25, x0 + 30 + cw, yy + 23, 10, P(Y, ak * 0.7, stroke=1.8))
        txt(c, code, x0 + 30 + cw / 2, yy + 10, fs + 4, 'm9', Y, ak, 'c')
        ls = wrap_lines(s_, fs, 'm7', x1 - x0 - cw - 90)
        for j, ln in enumerate(ls): txt(c, ln, x0 + 30 + cw + 24, yy + 10 - (len(ls) - 1) * fs * 0.6 + j * fs * 1.2, fs, 'm7', WHT, ak)
        yy += rh


def pan_dp(c, R, a, i, f, tl, p, S):
    """două bare: presiunea înainte / după filtru."""
    x0, y0, x1, y1 = R; pbox(c, R, a, p.get('title', 'PRESIUNEA ÎNAINTE ȘI DUPĂ FILTRU')); lv = pv(p['lv'], f) if 'lv' in p else S['dp']
    volt = p.get('volt'); ya = y0 + 118; st = 70
    lw = 250; bx = x0 + 30 + lw; full = x1 - 40 - bx
    b_after = 0.22 * full; b_before = b_after + (0.03 + 0.64 * lv) * full
    txt(c, 'înainte de filtru', x0 + 30, ya + 10, 26, 'm7', WHT, a * 0.92); txt(c, 'după filtru', x0 + 30, ya + st + 10, 26, 'm7', WHT, a * 0.92)
    rrect(c, bx, ya - 16, bx + b_before, ya + 18, 8, P(C_GAS, a)); rrect(c, bx, ya + st - 16, bx + b_after, ya + st + 18, 8, P(C_CLN, a))
    xa, xb = bx + b_after, bx + b_before; yb = ya + st + 52
    c.drawLine(xa, ya + st + 22, xa, yb + 8, P(Y, a * 0.9, stroke=2.5)); c.drawLine(xb, ya + 22, xb, yb + 8, P(Y, a * 0.9, stroke=2.5))
    c.drawLine(xa, yb, xb, yb, P(Y, a, stroke=3.5))
    txt(c, 'Δp', (xa + xb) / 2, yb - 12, 30, 'm9', Y, a, 'c', stroke=6, scol='#0a1322')
    sub = p.get('sub')
    if volt:
        yv = yb + 74; u = 0.7 + 3.3 * lv
        txt(c, 'semnal spre calculator', x0 + 30, yv + 10, 26, 'm7', WHT, a * 0.92)
        bx2 = x0 + 30 + 330; fw = x1 - 190 - bx2
        rrect(c, bx2, yv - 14, bx2 + fw, yv + 16, 8, P('#22314a', a)); rrect(c, bx2, yv - 14, bx2 + fw * (u / 5.0), yv + 16, 8, P(Y, a))
        txt(c, ro(u) + ' V', x1 - 36, yv + 14, 40, 'anton', Y, a, 'r')
    elif sub:
        col = RED if p.get('bad') else WHT
        for j, ln in enumerate(wrap_lines(sub, 27, 'm8', x1 - x0 - 60)): txt(c, ln, x0 + 30, yb + 66 + j * 34, 27, 'm8', col, a * ramp(tl, p.get('subt', 0.8), 0.4))
    else: txt(c, 'Diferența dintre ele = presiunea diferențială (Δp).', x0 + 30, y1 - 36, 23, 'm7', WHT, a * 0.7)


def pan_dpx(c, R, a, i, f, tl, p):
    x0, y0, x1, y1 = R; pbox(c, R, a, 'PRESIUNEA DIFERENȚIALĂ: AȘTEPTATĂ ȘI MĂSURATĂ')
    mea = pv(p['mea'], f); ex = 0.62; st = 84; ya = y0 + 124
    lw = 290; bx = x0 + 30 + lw; full = x1 - 40 - bx
    bad = p.get('fault') and mea < 0.33
    for k, (nm, sub, v, col) in enumerate((('așteptată', 'din debitul de gaze', ex, '#9fb4cc'), ('măsurată', 'de senzor', mea, RED if bad else C_GAS))):
        yy = ya + k * st
        txt(c, nm, x0 + 30, yy + 4, 28, 'm8', WHT, a); txt(c, sub, x0 + 30, yy + 32, 20, 'm7', WHT, a * 0.6)
        rrect(c, bx, yy - 14, bx + full, yy + 22, 8, P('#1a2740', a)); rrect(c, bx, yy - 14, bx + full * v, yy + 22, 8, P(col, a))
    xm = bx + full * ex * 0.55
    c.drawLine(xm, ya - 26, xm, ya + st + 34, P(WHT, a * 0.55, stroke=2, pe=skia.DashPathEffect.Make([7, 6], 0)))
    txt(c, 'minimul pentru un filtru întreg', xm + 10, ya + st + 62, 20, 'm7', WHT, a * 0.6)
    yv = y1 - 40
    if p.get('fault'):
        ab = a * (1 - ramp(mea, 0.22, 0.12))
        if ab > 0.01:
            s_ = p.get('msg', 'eficiență sub prag'); wd = tw(s_, 30, 'm9') + 44
            rrect(c, x1 - 30 - wd, yv - 34, x1 - 30, yv + 16, 12, P(RED, ab)); txt(c, s_, x1 - 30 - wd / 2, yv + 2, 30, 'm9', '#ffffff', ab, 'c')
    else:
        tick(c, x1 - 60, yv - 10, 30, GRN, a); txt(c, 'în limite', x1 - 92, yv, 28, 'm8', GRN, a, 'r')


def pan_soot2(c, R, a, i, f, tl, p):
    x0, y0, x1, y1 = R; pbox(c, R, a, p.get('title', 'FUNINGINEA DIN FILTRU, PE TESTER'))
    st = 78; ya = y0 + 122; lw = 190; bx = x0 + 30 + lw; full = x1 - 190 - bx; thr = p.get('thr')
    for k, (nm, key, col) in enumerate((('măsurată', 'm', C_GAS), ('calculată', 'c', C_CLN))):
        yy = ya + k * st; v = p.get(key)
        on = v is not None; v = pv(v, f) if on else 0.0
        txt(c, nm, x0 + 30, yy + 10, 28, 'm8', WHT, a * (1.0 if on else 0.35))
        rrect(c, bx, yy - 16, bx + full, yy + 20, 8, P('#1a2740', a))
        if on:
            rrect(c, bx, yy - 16, bx + full * min(1.0, v / 50.0), yy + 20, 8, P(col, a))
            txt(c, ro(v) + ' g', x1 - 34, yy + 16, 42, 'anton', col, a, 'r')
    if thr:
        xt = bx + full * thr / 50.0
        c.drawLine(xt, ya - 30, xt, ya + st + 30, P(RED, a * 0.9, stroke=3, pe=skia.DashPathEffect.Make([8, 6], 0))); txt(c, 'prag', xt + 8, ya - 28, 20, 'm8', RED, a)
    yy = ya + 2 * st - 6
    if p.get('ok'):
        ao = a * ramp(tl, 1.0, 0.4); tick(c, x0 + 46, yy + 16, 30, GRN, ao); txt(c, p['ok'], x0 + 80, yy + 26, 28, 'm8', GRN, ao)
    if p.get('bad'):
        ao = a * ramp(tl, p.get('badt', 0.8), 0.4); wd = tw(p['bad'], 26, 'm9') + 36
        rrect(c, x0 + 30, yy - 8, x0 + 30 + wd, yy + 36, 10, P(RED, ao * 0.9)); txt(c, p['bad'], x0 + 30 + wd / 2, yy + 23, 26, 'm9', '#ffffff', ao, 'c'); yy += 54
    if p.get('sub'):
        ao = a * ramp(tl, 1.2 if p.get('bad') else 0.6, 0.4)
        for j, ln in enumerate(wrap_lines(p['sub'], 27, 'm7', x1 - x0 - 60)): txt(c, ln, x0 + 30, yy + 28 + j * 35, 27, 'm7', WHT, ao * 0.9)


def pan_thr(c, R, a, i, f, tl, p):
    x0, y0, x1, y1 = R; pbox(c, R, a, 'ÎNCĂRCAREA CU FUNINGINE · exemplu 2.0 TDI')
    val = pv(p['val'], f); xa, xb = x0 + 40, x1 - 40; yb = y0 + 176; bh = 44
    X = lambda g: xa + (xb - xa) * g / 50.0
    zones = [(0, 18.9, '#3ba86a'), (18.9, 40, '#e0a020'), (40, 45, '#e86a1a'), (45, 50, '#d8322a')]
    for g0, g1, col in zones:
        c.drawRect(skia.Rect.MakeLTRB(X(g0) + 1.5, yb, X(g1) - 1.5, yb + bh), P(col, a * (0.95 if g0 <= val else 0.38)))
    for g, s_ in ((0, '0'), (18.9, '18,9 g'), (40, '40 g'), (45, '45 g')):
        txt(c, s_, X(g) + (0 if g else 2), yb + bh + 30, 22, 'm8', WHT, a * 0.85, 'c' if g else 'l')
    px = X(min(50.0, val))
    c.drawPath(path_of([(px, yb - 6), (px - 13, yb - 28), (px + 13, yb - 28)], True), P(WHT, a))
    txt(c, ro(val) + ' g', px, yb - 40, 34, 'anton', WHT, a, 'c')
    leg = [('#3ba86a', 'sub prag'), ('#e0a020', 'regenerare în mers'), ('#e86a1a', 'peste 40 g: doar în service'), ('#d8322a', 'peste 45 g: filtrul se înlocuiește')]
    yy = yb + bh + 78; colw = (x1 - x0 - 60) / 2
    for k, (col, s_) in enumerate(leg):
        lx, ly = x0 + 40 + (k % 2) * colw, yy + (k // 2) * 42
        hot = (k == 0 and val < 18.9) or (k == 1 and 18.9 <= val < 40) or (k == 2 and 40 <= val < 45) or (k == 3 and val >= 45)
        c.drawRoundRect(skia.Rect.MakeXYWH(lx, ly - 19, 22, 22), 5, 5, P(col, a))
        txt(c, s_, lx + 34, ly, 22, 'm8' if hot else 'm7', WHT, a * (1.0 if hot else 0.65))


def pan_inj(c, R, a, i, f, tl, p):
    x0, y0, x1, y1 = R; pbox(c, R, a, p.get('title', 'CE FACE CALCULATORUL LA REGENERARE'))
    s1 = pv(p['s1'], f); s2 = pv(p['s2'], f)
    chips = [('EGR închis', s1 > 0.12), ('Clapeta de admisie strânsă', s1 > 0.42), ('Injecția principală întârziată', s1 > 0.72), ('Post-injecții târzii', s2 > 0.25)]
    fs = 22; xx = x0 + 28; yy = y0 + 96
    for k, (s_, on) in enumerate(chips):
        wd = tw(s_, fs, 'm8') + 30
        if xx + wd > x1 - 24: xx = x0 + 28; yy += 46
        rrect(c, xx, yy - 26, xx + wd, yy + 10, 10, P(Y if on else '#1a2740', a)); txt(c, s_, xx + 15, yy, fs, 'm8', BG if on else WHT, a * (1.0 if on else 0.55)); xx += wd + 12
    ya = y1 - 76; xl, xr = x0 + 40, x1 - 40; xp = xl + (xr - xl) * 0.30
    c.drawLine(xl, ya, xr, ya, P(WHT, a * 0.7, stroke=2.5)); c.drawLine(xp, ya - 8, xp, ya + 10, P(WHT, a * 0.8, stroke=2.5))
    txt(c, 'PMS', xp, ya + 34, 20, 'm8', WHT, a * 0.8, 'c'); txt(c, 'unghiul arborelui cotit →', xr, ya + 34, 19, 'm7', WHT, a * 0.5, 'r')
    sc = (xr - xl) / 920.0; hmax = min(120.0, ya - yy - 62)
    def bar(xc, wd, hh, col, lab, al=1.0):
        if al <= 0.01: return
        rrect(c, xc - wd / 2, ya - hh, xc + wd / 2, ya - 2, 5, P(col, a * al)); txt(c, lab, xc, ya - hh - 12, 19, 'm8', WHT, a * al * 0.9, 'c')
    bar(xp - 64 * sc, 14, hmax * 0.26, C_FUEL, 'pilot')
    bar(xp + (14 + 74 * s1) * sc, 34, hmax * 0.9, C_FUEL, 'principală')
    bar(xp + 300 * sc, 22, hmax * 0.5, '#ff9a3a', 'post-injecție', ramp(s2, 0.05, 0.3))
    for k in (0, 1): bar(xp + (470 + 90 * k) * sc, 16, hmax * 0.3, '#ff6a2a', 'târzie' if k == 0 else '', ramp(s2, 0.3 + 0.2 * k, 0.3))
    ap = a * ramp(s2, 0.75, 0.25)
    if ap > 0.01: txt(c, p.get('late', 'ard în catalizator'), xp + 515 * sc, ya - hmax * 0.3 - 40, 20, 'm9', Y, ap, 'c')


def pan_cycles(c, R, a, i, f, tl, p):
    x0, y0, x1, y1 = R; pbox(c, R, a, p.get('title', 'CU CENUȘĂ, REGENERĂRILE SE ÎNDESESC'))
    xl, xr, yt, yb = x0 + 60, x1 - 40, y0 + 96, y1 - 58
    c.drawLine(xl, yb, xr, yb, P(WHT, a * 0.6, stroke=2)); c.drawLine(xl, yb, xl, yt, P(WHT, a * 0.6, stroke=2))
    txt(c, 'kilometri →', xr, yb + 34, 20, 'm7', WHT, a * 0.55, 'r')
    Yv = lambda v: yb - (yb - yt) * v
    lim = 0.90; pw = p.get('pw', 1.25); top = p.get('top', 0.66); fill = p.get('fill', 'cenușă')
    c.drawLine(xl, Yv(lim), xr, Yv(lim), P(RED, a * 0.8, stroke=2, pe=skia.DashPathEffect.Make([9, 7], 0))); txt(c, 'pragul de regenerare', xl + 10, Yv(lim) - 10, 19, 'm8', RED, a * 0.9)
    base = lambda u: 0.06 + top * u ** pw
    pts = []; u = 0.0; rise = p.get('rise', 5.2)
    while u < 1.0:
        b0 = base(u); du = max(0.012, (lim - b0) / rise)
        pts.append((u, b0)); pts.append((min(1.0, u + du), b0 + rise * (min(1.0, u + du) - u))); u += du
        if u < 1.0: pts.append((u, base(u)))
    rev = cl((f - 0.08) / 0.8)
    c.save(); c.clipRect(skia.Rect.MakeLTRB(xl, yt - 10, xl + (xr - xl) * rev, yb + 2))
    if fill:
        ash = [(xl + (xr - xl) * k / 40, Yv(base(k / 40))) for k in range(41)]
        c.drawPath(path_of(ash + [(xr, yb), (xl, yb)], True), P(C_ASH, a * 0.55)); c.drawPath(path_of(ash), P(C_ASH, a, stroke=3))
    c.drawPath(path_of([(xl + (xr - xl) * u_, Yv(v)) for u_, v in pts]), P(C_GAS, a, stroke=3.5, join='miter'))
    c.restore()
    txt(c, 'funingine', xl + 24, Yv(0.50), 20, 'm8', C_GAS, a * ramp(rev, 0.1, 0.1))
    if fill: txt(c, fill, xr - 24, Yv(0.30), 21, 'm8', '#1b1b18', a * ramp(rev, 0.8, 0.15), 'r')


def pan_pm(c, R, a, i, f, tl, p):
    x0, y0, x1, y1 = R; pbox(c, R, a, 'SENZORUL DE PARTICULE · după filtru')
    ex0, ey0 = x0 + 40, y0 + 92; ew = (x1 - x0) * 0.42; eh = y1 - 40 - ey0
    rrect(c, ex0, ey0, ex0 + ew, ey0 + eh, 12, P('#e9e4d6', a)); n = 9; fw = ew / (2 * n + 1)
    c.drawRect(skia.Rect.MakeLTRB(ex0 + fw * 0.6, ey0 + 14, ex0 + ew - fw * 0.6, ey0 + 26), P('#8a8f98', a)); c.drawRect(skia.Rect.MakeLTRB(ex0 + fw * 0.6, ey0 + eh - 26, ex0 + ew - fw * 0.6, ey0 + eh - 14), P('#8a8f98', a))
    for k in range(n * 2 - 1):
        xk = ex0 + fw * (1.5 + k)
        if k % 2 == 0: c.drawRect(skia.Rect.MakeLTRB(xk, ey0 + 20, xk + fw * 0.42, ey0 + eh - 44), P('#8a8f98', a))
        else: c.drawRect(skia.Rect.MakeLTRB(xk, ey0 + 44, xk + fw * 0.42, ey0 + eh - 20), P('#8a8f98', a))
    rng = np.random.default_rng(5); m = int(260 * cl((f - 0.25) / 0.6) * p.get('k', 1.0))
    px = rng.uniform(ex0 + fw * 1.2, ex0 + ew - fw * 1.2, 260); py = rng.uniform(ey0 + 50, ey0 + eh - 50, 260); pr = rng.uniform(3.0, 6.5, 260)
    for k in range(m): c.drawCircle(px[k], py[k], pr[k], P('#0a0a0a', a * 0.92))
    gx0, gx1, gy0, gy1 = ex0 + ew + 70, x1 - 36, y0 + 110, y1 - 66
    c.drawLine(gx0, gy1, gx1, gy1, P(WHT, a * 0.6, stroke=2)); c.drawLine(gx0, gy1, gx0, gy0, P(WHT, a * 0.6, stroke=2))
    txt(c, 'timp →', gx1, gy1 - 10, 19, 'm7', WHT, a * 0.55, 'r'); txt(c, 'curent între electrozi', gx0 + 8, gy0 + 2, 19, 'm7', WHT, a * 0.55)
    yth = lerp(gy1, gy0, 0.72)
    c.drawLine(gx0, yth, gx1, yth, P(WHT, a * 0.6, stroke=2, pe=skia.DashPathEffect.Make([8, 6], 0))); txt(c, 'prag', gx1, yth - 8, 18, 'm8', WHT, a * 0.7, 'r')
    rev = cl((f - 0.25) / 0.6)
    for (k_, col) in ((3.2, RED), (0.75, GRN)):
        pts = [(gx0 + (gx1 - gx0) * u, lerp(gy1, gy0, min(0.95, k_ * max(0.0, u - 0.12) ** 1.6))) for u in np.linspace(0, rev, 40)]
        c.drawPath(path_of(pts), P(col, a, stroke=4))
    txt(c, 'filtru care nu mai reține', gx0, gy1 + 30, 18, 'm8', RED, a * 0.95); txt(c, 'filtru bun', gx0 + tw('filtru care nu mai reține', 18, 'm8') + 24, gy1 + 30, 18, 'm8', GRN, a * 0.95)


def pan_rag(c, R, a, i, f, tl, p):
    """proba cu cârpa: două petice, unul curat, unul negru."""
    x0, y0, x1, y1 = R; pbox(c, R, a, p.get('title', 'PROBA CU CÂRPA, ÎN ȚEAVA DE DUPĂ FILTRU')); r = min((y1 - y0 - 170) / 2.0, 105.0); cy = y0 + 92 + r
    for k, (lab, good) in enumerate((('curată: filtrul reține', True), ('neagră: funinginea trece', False))):
        cx = x0 + (x1 - x0) * (0.27 + 0.46 * k); ak = a * ramp(tl, LEAD + (0.25 if k == 0 else 0.55) * sp(i), 0.35)
        rrect(c, cx - r * 1.25, cy - r, cx + r * 1.25, cy + r, 18, P(shader=lin(cx - r, cy - r, cx + r, cy + r, ['#f4f1e8', '#cfcabb']), a=ak))
        if not good:
            rng = np.random.default_rng(3)
            c.drawCircle(cx, cy, r * 0.62, P('#050505', ak * 0.9, blur=r * 0.16))
            for _ in range(40):
                an = rng.uniform(0, 6.28); rr = r * rng.uniform(0.2, 0.8); c.drawCircle(cx + rr * math.cos(an), cy + rr * math.sin(an) * 0.8, rng.uniform(3, 9), P('#000000', ak * 0.75))
        bx, by = cx + r * 1.1, cy - r * 0.86
        c.drawCircle(bx, by, 26, P('#0a1322', ak)); c.drawCircle(bx, by, 26, P(GRN if good else RED, ak, stroke=3))
        (tick if good else cross)(c, bx, by, 28, GRN if good else RED, ak)
        txt(c, lab, cx, cy + r + 40, 25, 'm8', WHT, ak, 'c')


def _icon(c, kind, x, y, s, col, a):
    """martori de bord, desenați simplu."""
    if a <= 0.01: return
    st = dict(stroke=s * 0.085)
    if kind == 'dpf':
        rrect(c, x - s * 0.55, y - s * 0.3, x + s * 0.55, y + s * 0.3, s * 0.1, P(col, a, **st))
        c.drawLine(x - s * 0.85, y, x - s * 0.55, y, P(col, a, **st)); c.drawLine(x + s * 0.55, y, x + s * 0.85, y, P(col, a, **st))
        for kx in (-0.3, 0.0, 0.3):
            for ky in (-0.12, 0.12): c.drawCircle(x + kx * s, y + ky * s, s * 0.055, P(col, a))
    elif kind == 'glow':
        pts = [(x - s * 0.7 + s * 1.4 * k / 60, y - s * 0.28 * math.sin(k / 60 * math.pi * 6) * (1 if 6 < k < 54 else 0)) for k in range(61)]
        c.drawPath(path_of(pts), P(col, a, **st))
    elif kind == 'eng':
        pts = [(-0.7, -0.05), (-0.5, -0.05), (-0.5, -0.3), (-0.15, -0.3), (-0.15, -0.45), (0.25, -0.45), (0.25, -0.3), (0.5, -0.3), (0.5, -0.05), (0.75, -0.05), (0.75, 0.3), (0.5, 0.3), (0.5, 0.45), (-0.3, 0.45), (-0.5, 0.25), (-0.7, 0.25)]
        c.drawPath(path_of([(x + px * s, y + py * s) for px, py in pts], True), P(col, a, **st))
    elif kind == 'fuel':
        rrect(c, x - s * 0.4, y - s * 0.45, x + s * 0.15, y + s * 0.45, s * 0.06, P(col, a, **st)); rrect(c, x - s * 0.28, y - s * 0.33, x + s * 0.03, y - s * 0.08, s * 0.03, P(col, a))
        c.drawPath(path_of([(x + s * 0.15, y - s * 0.1), (x + s * 0.4, y - s * 0.1), (x + s * 0.4, y + s * 0.3), (x + s * 0.55, y + s * 0.3), (x + s * 0.55, y - s * 0.3), (x + s * 0.38, y - s * 0.45)]), P(col, a, **st))
    elif kind == 'temp':
        c.drawLine(x, y - s * 0.5, x, y + s * 0.15, P(col, a, stroke=s * 0.12)); c.drawCircle(x, y + s * 0.28, s * 0.17, P(col, a))
        for k in range(3): c.drawLine(x + s * 0.08, y - s * 0.42 + k * s * 0.17, x + s * 0.3, y - s * 0.42 + k * s * 0.17, P(col, a, stroke=s * 0.07))
        for k in (-1, 1): c.drawPath(path_of([(x + k * s * 0.3 + (j - 3) * s * 0.07, y + s * 0.5 + s * 0.05 * math.sin(j * 1.6)) for j in range(7)]), P(col, a, stroke=s * 0.06))
    elif kind == 'oil':
        c.drawPath(path_of([(x - s * 0.6, y - s * 0.05), (x - s * 0.35, y - s * 0.05), (x - s * 0.2, y - s * 0.25), (x + s * 0.25, y - s * 0.25), (x + s * 0.7, y - s * 0.4), (x + s * 0.3, y + s * 0.3), (x - s * 0.45, y + s * 0.3), (x - s * 0.45, y + s * 0.1), (x - s * 0.6, y + s * 0.1)], True), P(col, a, **st))
        c.drawCircle(x + s * 0.72, y + s * 0.05, s * 0.07, P(col, a))


AMB = '#ffb21a'


def pan_dash(c, R, a, i, f, tl, p, t):
    """bordul: martori și mesaj."""
    x0, y0, x1, y1 = R; pbox(c, R, a)
    cy = (y0 + y1) / 2 - 20; r = 128
    for k, cx in enumerate((x0 + 170, x1 - 170)):
        c.drawCircle(cx, cy, r, P('#0d1828', a)); c.drawCircle(cx, cy, r, P('#3a4a66', a, stroke=4))
        for j in range(9):
            an = math.radians(140 + j * 32.5); c.drawLine(cx + (r - 20) * math.cos(an), cy + (r - 20) * math.sin(an), cx + (r - 6) * math.cos(an), cy + (r - 6) * math.sin(an), P(WHT, a * 0.7, stroke=3))
        v = pv(p.get('rpm', 0.25), f) if k == 0 else pv(p.get('spd', 0.3), f)
        an = math.radians(140 + 260 * cl(v) + 2.0 * math.sin(t * 7 + k)); c.drawLine(cx, cy, cx + (r - 30) * math.cos(an), cy + (r - 30) * math.sin(an), P(RED, a, stroke=5)); c.drawCircle(cx, cy, 11, P('#c9d1dc', a))
        txt(c, 'rot/min ×1000' if k == 0 else 'km/h', cx, cy + r * 0.62, 17, 'm7', WHT, a * 0.55, 'c')
    lights = p.get('lights', [('dpf', 'on')]); n = len(lights); mx = (x0 + x1) / 2; sp_ = 112
    for k, (kind, st) in enumerate(lights):
        t0 = LEAD + (p.get('lt', [0.1] * n)[k]) * sp(i)
        on = 0.0 if tl < t0 else (1.0 if st == 'on' else (0.5 + 0.5 * math.copysign(1, math.sin((tl - t0) * 9.0))))
        lx = mx + (k - (n - 1) / 2) * sp_; ly = cy - 46
        c.drawCircle(lx, ly, 46, P(AMB, a * 0.16 * on)); _icon(c, kind, lx, ly, 46, AMB, a * (0.16 + 0.84 * on))
    msg = p.get('msg')
    if msg:
        am = a * ramp(tl, LEAD + p.get('mt', 0.2) * sp(i), 0.3); fs = fit_txt(msg, 30, 'm9', 330, 18); wd = tw(msg, fs, 'm9') + 36
        rrect(c, mx - wd / 2, cy + 36, mx + wd / 2, cy + 92, 10, P('#1a2740', am)); rrect(c, mx - wd / 2, cy + 36, mx + wd / 2, cy + 92, 10, P(AMB, am * 0.8, stroke=2)); txt(c, msg, mx, cy + 74, fs, 'm9', AMB, am, 'c')
    sub = p.get('sub')
    if sub: txt(c, sub, mx, y1 - 28, 23, 'm7', WHT, a * 0.75, 'c')


def pan_gauge(c, R, a, i, f, tl, p):
    """o scală orizontală cu prag: valoarea urcă sau coboară."""
    x0, y0, x1, y1 = R; pbox(c, R, a, p['title'])
    lo, hi = p['lo'], p['hi']; val = pv(p['val'], f); thr = p.get('thr'); xa, xb = x0 + 50, x1 - 50; yb = y0 + 210; bh = 46
    X = lambda v: xa + (xb - xa) * cl((v - lo) / (hi - lo))
    bad = p.get('bad', 'below'); isbad = thr is not None and ((val < thr) if bad == 'below' else (val > thr))
    rrect(c, xa, yb, xb, yb + bh, 10, P('#1a2740', a))
    if thr is not None:
        if bad == 'below': rrect(c, xa, yb, X(thr), yb + bh, 10, P(RED, a * 0.28)); rrect(c, X(thr), yb, xb, yb + bh, 10, P(GRN, a * 0.22))
        else: rrect(c, X(thr), yb, xb, yb + bh, 10, P(RED, a * 0.28)); rrect(c, xa, yb, X(thr), yb + bh, 10, P(GRN, a * 0.22))
    rrect(c, xa, yb + 8, X(val), yb + bh - 8, 7, P(RED if isbad else p.get('col', GRN), a))
    for v in p.get('ticks', []): txt(c, f'{v:g}'.replace('.', ','), X(v), yb + bh + 30, 21, 'm8', WHT, a * 0.7, 'c')
    if thr is not None:
        c.drawLine(X(thr), yb - 16, X(thr), yb + bh + 8, P(WHT, a, stroke=3)); txt(c, p.get('thr_lab', ''), X(thr), yb - 26, 23, 'm8', WHT, a, 'c')
    s_ = (ro(val, p.get('dec', 0)) + ' ' + p['unit']).replace('-', '−')
    txt(c, s_, x0 + 50, y0 + 150, 76, 'anton', RED if isbad else WHT, a)
    if p.get('sub'):
        for j, ln in enumerate(wrap_lines(p['sub'], 26, 'm7', x1 - x0 - 100)): txt(c, ln, x0 + 50, y1 - 72 + j * 33, 26, 'm7', WHT, a * 0.85 * ramp(tl, p.get('subt', 0.6), 0.4))
    if p.get('flag'):
        af = a * (1.0 if isbad else 0.0) * ramp(tl, 0.5, 0.3); wd = tw(p['flag'], 28, 'm9') + 40
        rrect(c, x1 - 40 - wd, y0 + 100, x1 - 40, y0 + 154, 12, P(RED, af)); txt(c, p['flag'], x1 - 40 - wd / 2, y0 + 138, 28, 'm9', '#ffffff', af, 'c')


def pan_grid(c, R, a, i, f, tl, p):
    """39 de pătrate; cinci rămân aprinse."""
    x0, y0, x1, y1 = R; pbox(c, R, a); n, hot = p.get('n', 39), p.get('hot', 5)
    cols = 13; sz = 58; gp = 12; gw = cols * sz + (cols - 1) * gp; gx = (x0 + x1 - gw) / 2; gy = y0 + 46
    t1 = LEAD + p.get('t1', 0.1) * sp(i); t2 = LEAD + (wt(i, p['w2']) if 'w2' in p else p.get('t2', 0.6) * sp(i))
    for k in range(n):
        r_, q = divmod(k, cols); xx = gx + q * (sz + gp); yy = gy + r_ * (sz + gp)
        ak = a * ramp(tl, t1 + 0.022 * k, 0.15); ishot = k >= n - hot
        dim = ramp(tl, t2, 0.4) if not ishot else 0.0
        col = mix(Y, '#22314a', dim) if not ishot else mix(Y, RED, ramp(tl, t2, 0.4))
        rrect(c, xx, yy, xx + sz, yy + sz, 9, P(col, ak)); txt(c, str(k + 1), xx + sz / 2, yy + sz * 0.66, 24, 'm9', BG if dim < 0.5 else WHT, ak * (1.0 if dim < 0.5 else 0.5), 'c')
    yy = gy + 3 * (sz + gp) + 56
    w = txt(c, f'{n}', x0 + 60, yy + 24, 86, 'anton', Y, a * ramp(tl, t1, 0.3)); txt(c, p.get('l1', 'de cauze'), x0 + 60 + w + 16, yy + 20, 34, 'm8', WHT, a * ramp(tl, t1, 0.3))
    a2 = a * ramp(tl, t2, 0.4); w2 = tw(p.get('l2', 'în filtru'), 34, 'm8')
    txt(c, p.get('l2', 'în filtru'), x1 - 60, yy + 20, 34, 'm8', WHT, a2, 'r'); txt(c, f'{hot}', x1 - 60 - w2 - 16, yy + 24, 86, 'anton', RED, a2, 'r')


def pan_four(c, R, a, i, f, tl, p):
    """casete care se aprind pe rând (2 × 2 sau 1 × n)."""
    x0, y0, x1, y1 = R; pbox(c, R, a, p.get('title'), 34)
    items = p['items']; n = len(items); cols = p.get('cols', 2 if n == 4 else n); rows_ = (n + cols - 1) // cols
    top = y0 + (76 if p.get('title') else 26); gp = 18; bw = (x1 - x0 - 56 - gp * (cols - 1)) / cols; bh = (y1 - 24 - top - gp * (rows_ - 1)) / rows_
    tts = item_times(i, p, n); last = max([k for k in range(n) if tl >= tts[k]] or [-1])
    for k, it in enumerate(items):
        nm, sub = (it if isinstance(it, tuple) else (it, ''))[:2]; kind = it[2] if isinstance(it, tuple) and len(it) > 2 else ''
        r_, q = divmod(k, cols); bx = x0 + 28 + q * (bw + gp); by = top + r_ * (bh + gp)
        on = ramp(tl, tts[k], 0.3); cur = k == last and not p.get('all'); bad = kind == 'bad'
        colb = RED if bad else Y
        rrect(c, bx, by, bx + bw, by + bh, 14, P(mix('#131f33', colb, 0.9 * on * (1.0 if cur or p.get('all') else 0.0) if not bad else 0.0), a))
        if bad and on > 0.01: rrect(c, bx, by, bx + bw, by + bh, 14, P('#3a1512', a * on))
        rrect(c, bx, by, bx + bw, by + bh, 14, P(colb, a * (0.25 + 0.75 * on), stroke=2.5))
        dark = (cur or p.get('all')) and not bad
        fs = fit_txt(nm, p.get('fs', 34), 'anton', bw - 30, 20); nl = wrap_lines(sub, 22, 'm7', bw - 30) if sub else []
        ty = by + bh / 2 + fs * 0.36 - (len(nl) * 14)
        txt(c, nm, bx + bw / 2, ty, fs, 'anton', mix(WHT, BG, on) if dark else (RED if bad and on > 0.5 else WHT), a * (0.45 + 0.55 * on), 'c')
        for j, ln in enumerate(nl): txt(c, ln, bx + bw / 2, ty + 34 + j * 28, 22, 'm7', BG if dark and on > 0.5 else WHT, a * on * 0.9, 'c')
        if bad and on > 0.01: cross(c, bx + bw - 26, by + 26, 20, RED, a * on)


def pan_chain(c, R, a, i, f, tl, p, t):
    """un lanț de casete legate cu săgeți; unele pot fi marcate (defect), cu o notă dedesubt."""
    x0, y0, x1, y1 = R; pbox(c, R, a, p.get('title'), 33)
    nodes = p['nodes']; n = len(nodes); top = y0 + (84 if p.get('title') else 40)
    rows_ = p.get('rows', 1 if n <= 4 else 2); per = (n + rows_ - 1) // rows_; gp = 34; bw = (x1 - x0 - 60 - gp * (per - 1)) / per; bh = min(150.0 if rows_ == 1 else 104.0, (y1 - top - 30 - (rows_ - 1) * 60 - (64 if p.get('sub') else 0)) / rows_ - (40 if p.get('notes') else 0))
    if rows_ == 1 and not p.get('sub'): top += (y1 - top - 30 - bh - (40 if p.get('notes') else 0)) / 2
    tts = item_times(i, p, n); bads = p.get('bad', []); notes = p.get('notes', {}); flow = p.get('flow', True); pos = []
    for k in range(n):
        r_, q = divmod(k, per)
        if r_ % 2 == 1: q = per - 1 - q                     # șerpuit
        bx = x0 + 30 + q * (bw + gp); by = top + r_ * (bh + 60 + (40 if notes else 0)); pos.append((bx, by))
    for k in range(n - 1):
        (ax, ay), (bx, by) = pos[k], pos[k + 1]; ak = a * ramp(tl, tts[k + 1], 0.3)
        if abs(ay - by) < 1: pa, pb = ((ax + bw, ay + bh / 2), (bx, by + bh / 2)) if bx > ax else ((ax, ay + bh / 2), (bx + bw, by + bh / 2))
        else: pa, pb = (ax + bw / 2, ay + bh), (bx + bw / 2, by)
        cut = k + 1 in p.get('cut', [])
        c.drawLine(pa[0], pa[1], pb[0], pb[1], P(RED if cut else C_CLN, ak * 0.9, stroke=5, pe=(skia.DashPathEffect.Make([6, 7], 0) if cut else None)))
        if flow and not cut:
            ph = (t * 0.9 + 0.3 * k) % 1.0; c.drawCircle(lerp(pa[0], pb[0], ph), lerp(pa[1], pb[1], ph), 6, P(WHT, ak * 0.9))
    for k, nm in enumerate(nodes):
        bx, by = pos[k]; on = ramp(tl, tts[k], 0.3); bad = k in bads
        tb = LEAD + (p['badt'][bads.index(k)] * sp(i) if bad and 'badt' in p else 0.0) if bad else 0.0
        bon = ramp(tl, max(tts[k], tb), 0.3) if bad else 0.0
        rrect(c, bx, by, bx + bw, by + bh, 12, P(mix('#1a2740', '#3a1512', bon), a * (0.5 + 0.5 * on))); rrect(c, bx, by, bx + bw, by + bh, 12, P(mix(WHT, RED, bon), a * (0.3 + 0.5 * on), stroke=2.2))
        ls = nm.split('\n'); fs = min(fit_txt(max(ls, key=len), 25, 'm8', bw - 16, 15), 25)
        for j, ln in enumerate(ls): txt(c, ln, bx + bw / 2, by + bh / 2 + fs * 0.35 - (len(ls) - 1) * fs * 0.6 + j * fs * 1.2, fs, 'm8', WHT, a * (0.5 + 0.5 * on), 'c')
        if bad and bon > 0.01: c.drawCircle(bx + bw - 8, by + 8, 18, P('#0a1322', a * bon)); cross(c, bx + bw - 8, by + 8, 20, RED, a * bon)
        if k in notes: txt(c, notes[k], bx + bw / 2, by + bh + 30, 20, 'm9', RED if bad else Y, a * (bon if bad else on), 'c')
    if p.get('sub'):
        for j, ln in enumerate(wrap_lines(p['sub'], 25, 'm7', x1 - x0 - 80)): txt(c, ln, x0 + 40, y1 - 58 + j * 32 + (30 if len(wrap_lines(p['sub'], 25, 'm7', x1 - x0 - 80)) == 1 else 0), 25, 'm7', WHT, a * 0.85 * ramp(tl, LEAD + p.get('subt', 0.55) * sp(i), 0.4))


def pan_big(c, R, a, i, f, tl, p):
    """o afirmație mare, cu un rând mic dedesubt."""
    x0, y0, x1, y1 = R; pbox(c, R, a); cx = (x0 + x1) / 2
    top = p.get('top'); t1 = LEAD + p.get('t1', 0.1) * sp(i)
    lines = p['text'].split('\n'); fs = min(fit_txt(max(lines, key=len), p.get('fs', 92), 'anton', x1 - x0 - 80, 36), p.get('fs', 92))
    hh = len(lines) * fs * 1.08 + (40 if top else 0) + (50 if p.get('sub') else 0); yy = (y0 + y1) / 2 - hh / 2 + fs * 0.9 + (40 if top else 0)
    if top: txt(c, top, cx, yy - fs * 0.9 - 6, 28, 'm8', WHT, a * 0.8 * ramp(tl, 0.2, 0.3), 'c')
    for j, ln in enumerate(lines):
        aj = a * ramp(tl, t1 + 0.35 * j, 0.3); pop = 1.0 + 0.12 * (1 - ramp(tl, t1 + 0.35 * j, 0.3))
        c.save(); c.translate(cx, yy + j * fs * 1.08); c.scale(pop, pop); txt(c, ln, 0, 0, fs, 'anton', p.get('col', Y) if j == len(lines) - 1 or p.get('allcol') else WHT, aj, 'c', shadow=10); c.restore()
    if p.get('sub'):
        ls = wrap_lines(p['sub'], 27, 'm7', x1 - x0 - 100)
        for j, ln in enumerate(ls): txt(c, ln, cx, yy + (len(lines) - 1) * fs * 1.08 + 52 + j * 34, 27, 'm7', WHT, a * 0.85 * ramp(tl, LEAD + p.get('subt', 0.5) * sp(i), 0.4), 'c')


def pan_dip(c, R, a, i, f, tl, p):
    """joja de ulei: nivelul urcă peste maxim."""
    x0, y0, x1, y1 = R; pbox(c, R, a, p.get('title', 'NIVELUL ULEIULUI, PE JOJĂ')); lv = pv(p['lv'], f)
    xa, xb = x0 + 70, x1 - 250; cy = y0 + 200
    rrect(c, xa, cy - 16, xb, cy + 16, 10, P('#c9ced6', a)); c.drawCircle(xa - 26, cy, 30, P('#ffb21a', a, stroke=10))
    xm0, xm1 = lerp(xa, xb, 0.52), lerp(xa, xb, 0.80)
    for xx, s_ in ((xm0, 'MIN'), (xm1, 'MAX')):
        c.drawLine(xx, cy - 30, xx, cy + 30, P(WHT, a, stroke=3)); txt(c, s_, xx, cy - 40, 22, 'm9', WHT, a, 'c')
    xo = lerp(xb, xa, 0.0); xl = lerp(xb, lerp(xa, xb, 0.30), cl(lv) ) if False else lerp(lerp(xa, xb, 0.60), lerp(xa, xb, 0.98), cl(lv))
    over = xl > xm1 + 4
    rrect(c, lerp(xa, xb, 0.40), cy - 11, xl, cy + 11, 7, P(mix('#b07a1c', '#6b5a2a', cl(lv)), a * 0.95))
    txt(c, 'peste maxim' if over else 'în limite', x1 - 50, cy - 12, 30, 'm9', RED if over else GRN, a, 'r')
    txt(c, 'ulei + motorină' if over else 'ulei', x1 - 50, cy + 26, 24, 'm7', WHT, a * 0.8, 'r')
    for j, ln in enumerate(wrap_lines(p.get('sub', 'Motorina din post-injecție se strânge în baie: uleiul se subțiază, iar nivelul urcă.'), 26, 'm7', x1 - x0 - 100)):
        txt(c, ln, x0 + 50, y1 - 86 + j * 34, 26, 'm7', WHT, a * 0.85)


def pan_tester(c, R, a, i, f, tl, p):
    """ecranul testerului: rânduri cu valori; unele sunt marcate."""
    x0, y0, x1, y1 = R; pbox(c, R, a, p.get('title', 'PE TESTER'))
    rows = p['rows']; n = len(rows); rh = min(74.0, (y1 - y0 - 100) / n); yy = y0 + 92 + rh * 0.5; fs = 28 if n <= 4 else 25
    tts = item_times(i, p, n)
    for k, r_ in enumerate(rows):
        nm, val = r_[0], r_[1]; st = r_[2] if len(r_) > 2 else ''
        ak = a * ramp(tl, tts[k], 0.3); col = RED if st == 'bad' else (GRN if st == 'ok' else (Y if st == 'hi' else WHT))
        rrect(c, x0 + 26, yy - rh * 0.42, x1 - 26, yy + rh * 0.42, 10, P('#3a1512' if st == 'bad' else '#131f33', ak))
        if st in ('bad', 'hi'): rrect(c, x0 + 26, yy - rh * 0.42, x1 - 26, yy + rh * 0.42, 10, P(col, ak * 0.8, stroke=2))
        txt(c, nm, x0 + 48, yy + fs * 0.36, fs, 'm7', WHT, ak)
        v = val if isinstance(val, str) else (ro(pv(val[0], f), val[2] if len(val) > 2 else 0) + ' ' + val[1]).replace('-', '−')
        txt(c, v, x1 - 48, yy + fs * 0.4, fs + 6, 'm9', col, ak, 'r')
        yy += rh


def pan_vs(c, R, a, i, f, tl, p, t):
    """două casete față în față, cu un semn între ele."""
    x0, y0, x1, y1 = R; pbox(c, R, a, p.get('title'), 34); cx = (x0 + x1) / 2; cy = (y0 + y1) / 2 + (24 if p.get('title') else 0)
    bw, bh = 370, 150
    for k, (nm, sub) in enumerate((p['a'], p['b'])):
        bx = x0 + 40 if k == 0 else x1 - 40 - bw; on = ramp(tl, LEAD + (0.2 + 0.3 * k) * sp(i), 0.3)
        win = p.get('win'); hot = win == k and tl > LEAD + p.get('wt', 0.75) * sp(i)
        rrect(c, bx, cy - bh / 2, bx + bw, cy + bh / 2, 16, P(Y if hot else '#131f33', a * on)); rrect(c, bx, cy - bh / 2, bx + bw, cy + bh / 2, 16, P(Y, a * on * 0.8, stroke=2.5))
        fs = fit_txt(nm, 40, 'anton', bw - 30, 22); txt(c, nm, bx + bw / 2, cy + (fs * 0.36 if not sub else -6), fs, 'anton', BG if hot else WHT, a * on, 'c')
        if sub: txt(c, sub, bx + bw / 2, cy + 38, 22, 'm7', BG if hot else WHT, a * on * 0.85, 'c')
    s_ = p.get('mid', '?'); pop = 1.0 + 0.1 * math.sin(t * 4.0)
    c.save(); c.translate(cx, cy + 30); c.scale(pop, pop); txt(c, s_, 0, 0, 96, 'anton', Y, a, 'c', shadow=8); c.restore()


def pan_timer(c, R, a, i, f, tl, p):
    """un cronometru care merge; se poate opri (regenerare întreruptă)."""
    x0, y0, x1, y1 = R; pbox(c, R, a, p.get('title')); cx = x0 + 220; cy = (y0 + y1) / 2 + 26; r = 120
    v = pv(p['val'], f); full = p.get('full', 20.0); stop = p.get('stop')
    c.drawCircle(cx, cy, r, P('#0d1828', a)); c.drawCircle(cx, cy, r, P('#3a4a66', a, stroke=6))
    arc = skia.Path(); arc.addArc(skia.Rect.MakeLTRB(cx - r, cy - r, cx + r, cy + r), -90, 360 * cl(v / full))
    bad = stop is not None and v >= stop - 1e-3
    c.drawPath(arc, P(RED if bad else GRN, a, stroke=12, cap='butt'))
    txt(c, ro(v, 0), cx, cy + 22, 84, 'anton', RED if bad else WHT, a, 'c'); txt(c, 'min', cx, cy + 62, 24, 'm8', WHT, a * 0.7, 'c')
    lx = x0 + 400; yy = y0 + 150
    for j, (s_, col) in enumerate(p.get('lines', [])):
        for ln in wrap_lines(s_, 30, 'm8' if col else 'm7', x1 - lx - 40):
            txt(c, ln, lx, yy, 30, 'm8' if col else 'm7', {'r': RED, 'g': GRN, 'y': Y}.get(col, WHT), a * ramp(tl, 0.3 + 0.6 * j, 0.3)); yy += 40
        yy += 14


PANS = dict(card=pan_card, codes=pan_codes, dpx=pan_dpx, soot2=pan_soot2, thr=pan_thr, inj=pan_inj, cycles=pan_cycles, pm=pan_pm, rag=pan_rag, gauge=pan_gauge, grid=pan_grid,
            four=pan_four, big=pan_big, dip=pan_dip, tester=pan_tester, timer=pan_timer)
KEEP = ('soot2', 'inj', 'dpx', 'thr', 'dash')


def panel(c, t, S):
    for i in (shot_at(t) - 1, shot_at(t)):
        if i < 0 or 'pan' not in SH[i]: continue
        kind, p = SH[i]['pan']
        _same = lambda j: 0 <= j < N and 'pan' in SH[j] and SH[j]['pan'][0] == kind and (kind in KEEP or (p.get('grp') and SH[j]['pan'][1].get('grp') == p.get('grp')))
        same_n = _same(i + 1); same_p = _same(i - 1)
        if t >= SE[i] and same_n: continue
        a = (1.0 if same_p else ramp(t, SS[i] + 0.12, 0.3)) * (1.0 if same_n else 1 - ramp(t, SE[i] - 0.3, 0.28))
        if a <= 0.01: continue
        f = cl((t - SS[i]) / (SE[i] - SS[i])); tl = t - SS[i]
        c.save()
        if not same_p: c.translate(0, 16 * (1 - ramp(t, SS[i] + 0.12, 0.3)))
        if kind == 'dp': pan_dp(c, R_PAN, a, i, f, tl, p, S)
        elif kind in ('dash', 'chain', 'vs'): dict(dash=pan_dash, chain=pan_chain, vs=pan_vs)[kind](c, R_PAN, a, i, f, tl, p, t)
        else: PANS[kind](c, R_PAN, a, i, f, tl, p)
        c.restore()


# ------------------------------------------------------------------ cârlig, titlu, final
def hook_fx(c, t):
    if shot_at(t) != 0: return
    a = 1 - ramp(t, SE[0] - 0.3, 0.28)
    fl = 1 - ramp(t, 0.0, 0.5)
    if fl > 0.01: c.drawRect(skia.Rect.MakeWH(W, H), P(Y, 0.28 * fl))
    ic = SH[0].get('icon', 'dpf')
    if ic:
        on = 0.5 + 0.5 * math.copysign(1, math.sin(t * 9.0)); x, y = 930, 300
        c.drawCircle(x, y, 74, P('#0a1322', a * 0.92)); c.drawCircle(x, y, 74, P(AMB, a * (0.3 + 0.7 * on), stroke=4)); c.drawCircle(x, y, 74, P(AMB, a * 0.14 * on))
        _icon(c, ic, x, y, 62, AMB, a * (0.25 + 0.75 * on))


def title_card(c, t):
    i = 1
    if not (SS[i] - 0.1 <= t <= SE[i] + 0.3): return
    a = ramp(t, SS[i], 0.3) * (1 - ramp(t, SE[i] - 0.3, 0.3))
    if a <= 0.01: return
    c.drawRect(skia.Rect.MakeWH(W, H), P('#060b14', a * 0.80)); cx = W / 2; y = 640
    txt(c, 'SERIA', cx, y, 30, 'm9', WHT, a * 0.75, 'c')
    for j, ln in enumerate(('DE CE INTRĂ', 'FILTRUL DE PARTICULE', 'ÎN AVARIE')):
        txt(c, ln, cx, y + 100 + j * 108, 92 if j != 1 else 84, 'anton', Y if j == 2 else WHT, a, 'c', shadow=10)
    a2 = a * ramp(t, SS[i] + LEAD + (_sp1(IDS[1][0]) + JOIN if len(IDS[1]) > 1 else wt(1, 'episodul', 0.5 * sp(1))) - 0.1, 0.3)
    s_ = 'EPISODUL FINAL' if FINAL else f'EPISODUL {EPN} DIN {NEP}'; wd = tw(s_, 40, 'm9') + 60; y2 = y + 100 + 2 * 108 + 70
    rrect(c, cx - wd / 2, y2, cx + wd / 2, y2 + 76, 20, P(Y, a2)); txt(c, s_, cx, y2 + 53, 40, 'm9', BG, a2, 'c')
    ls = wrap_lines(EPD['titlu'], 54, 'm8', 940)
    for j, ln in enumerate(ls): txt(c, ln, cx, y2 + 160 + j * 66, 54, 'm8', WHT, a2, 'c', shadow=8)


def endcard(c, t):
    i = N - 1; a = ramp(t, SS[i] + 0.05, 0.5)
    if a <= 0.01: return
    c.drawRect(skia.Rect.MakeWH(W, H), P('#060b14', a * 0.965)); cx = W / 2; cy = 560
    txt(c, 'TURBO', cx, cy, 190, 'anton', WHT, a, 'c'); txt(c, 'DOCTOR', cx, cy + 190, 190, 'anton', Y, a, 'c')
    a1 = a * ramp(t, SS[i] + LEAD + wt(i, 'curatam', 0.15 * sp(i)), 0.3)
    for j, (s_, w_) in enumerate((('Curățăm sau recondiționăm filtrul', 'curatam'), ('și căutăm cauza care l-a înfundat.', 'cautam'))):
        txt(c, s_, cx, cy + 300 + j * 58, 44, 'm8', WHT, a * ramp(t, SS[i] + LEAD + wt(i, w_, (0.15 + 0.25 * j) * sp(i)) - 0.1, 0.3), 'c')
    a2 = a * ramp(t, SS[i] + LEAD + wt(i, 'doar', 0.7 * sp(i)) - 0.1, 0.3)
    y2 = cy + 470; wd = tw('DIAGNOZĂ GRATUITĂ', 54, 'anton') + 90
    rrect(c, cx - wd / 2, y2, cx + wd / 2, y2 + 104, 26, P(Y, a2)); txt(c, 'DIAGNOZĂ GRATUITĂ', cx, y2 + 74, 54, 'anton', BG, a2, 'c')
    txt(c, '0739 065 065', cx, y2 + 220, 96, 'anton', WHT, a2, 'c')
    txt(c, 'Galați · București · Iași · Piatra Neamț', cx, y2 + 290, 34, 'm8', WHT, a2 * 0.85, 'c')
    if not FINAL: txt(c, f'Seria „{SERIA}” · episodul {EPN} din {NEP}', cx, y2 + 370, 24, 'm7', WHT, a * 0.5, 'c')


def c1_card(c, t):
    i = N - 2
    if not (SS[i] <= t <= SE[i] + 0.2): return
    a = ramp(t, SS[i] + 0.1, 0.35) * (1 - ramp(t, SE[i] - 0.25, 0.25)); R = R_FULL
    y = R[3] - 250
    rrect(c, 60, y, 1020, y + 200, 22, P('#0a1322', a * 0.93)); rrect(c, 60, y, 1020, y + 200, 22, P(Y, a * 0.7, stroke=2.5))
    txt(c, 'FILTRUL E O PIESĂ STATICĂ.', 540, y + 84, 62, 'anton', WHT, a, 'c')
    txt(c, 'ALTCEVA ÎL FACE SĂ INTRE ÎN AVARIE.', 540, y + 156, 50, 'anton', Y, a * ramp(t, SS[i] + LEAD + wt(i, 'altceva', 0.5 * sp(i)) - 0.1, 0.3), 'c')


# ------------------------------------------------------------------ cadrul
def scene_image(t, S, V):
    surf = skia.Surface(W, H); c = surf.getCanvas()
    background(c, t); E.scene(c, S, V); watermark_over(c, t, ramp(V[0], 2.0, 2.5))
    return surf.makeImageSnapshot()


def frame(t):
    S = state(t); Va, Vb, m = cam(t)
    surf = skia.Surface(W, H); c = surf.getCanvas()
    background(c, t); E.scene(c, S, Va); watermark_over(c, t, ramp(Va[0], 2.0, 2.5))
    V = Va
    if Vb is not None and m > 0.003:
        p = skia.Paint(); p.setAlphaf(m); c.drawImage(scene_image(t, S, Vb), 0, 0, SAMP, p)
        if m > 0.5: V = Vb
    bands(c, S['hi'])
    labels(c, t, V); temps(c, t, V); legend(c, t); note_tag(c, t)
    panel(c, t, S); c1_card(c, t); caption(c, t); hook_fx(c, t)
    title_card(c, t); header(c, t); endcard(c, t)
    return surf.makeImageSnapshot()


def render(out, f0=0, f1=None):
    f1 = NF if f1 is None else min(f1, NF); crf = os.environ.get('CRF', '21')
    p = subprocess.Popen(['ffmpeg', '-y', '-nostdin', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-vf', 'scale=out_color_matrix=bt709:out_range=tv', '-c:v', 'libx264', '-preset', 'medium', '-crf', crf, '-g', '60', '-pix_fmt', 'yuv420p',
                          '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    for fi in range(f0, f1):
        p.stdin.write(frame(fi / FPS).toarray(colorType=skia.kRGBA_8888_ColorType).tobytes())
    p.stdin.close()
    if p.wait() != 0: raise SystemExit('ffmpeg failed')


if __name__ == '__main__':
    a = sys.argv[1:]; tag = f'ep{EPN:02d}'
    if '--info' in a:
        print(f'{tag}: {N} rânduri, vorbire {sum(sp(i) for i in range(N)):.1f} s, film {DUR:.1f} s = {NF} cadre')
        for i in range(N): print(f'{i:02d} {SS[i]:6.2f} cue {CUE[i]:6.2f} +{sp(i):5.2f} {SH[i]["v"]:5s} {SH[i].get("pan", ("",))[0]:6s} {SH[i]["big"][:30]:30s} | {SH[i]["say"][:50]}')
    elif '--cues' in a:
        d = os.path.join(ROOT, 'vo', tag); os.makedirs(d, exist_ok=True)
        ev = []
        for i in range(N):
            off = 0.0
            for k in IDS[i]: ev.append(dict(line=k, t=round(CUE[i] + off, 3))); off += _sp1(k) + JOIN
        json.dump(dict(events=ev, dur=round(DUR, 3), nf=NF, fps=FPS, rows=[dict(t=round(CUE[i], 3), sp=round(sp(i), 3), text=SH[i]['say']) for i in range(N)]), open(os.path.join(d, 'cues.json'), 'w'), ensure_ascii=False, indent=1)
        print(tag, DUR, NF)
    elif '--png' in a or '--mid' in a:
        os.makedirs(os.path.join(HERE, 'proof'), exist_ok=True)
        if '--png' in a: ts = [(f'{float(x):05.1f}', float(x)) for x in a[a.index('--png') + 1].split(',')]
        else:
            fr = float(a[a.index('--at') + 1]) if '--at' in a else 0.62
            ts = [(f'{i:02d}', SS[i] + (SE[i] - SS[i]) * fr) for i in range(N)]
            if '--only' in a: ts = [ts[int(k)] for k in a[a.index('--only') + 1].split(',')]
        for nm, t_ in ts: frame(t_).save(os.path.join(HERE, 'proof', f'{tag}_{nm}.png'), skia.kPNG)
    elif '--out' in a:
        o = a[a.index('--out') + 1]
        if '--frames' in a:
            k = a.index('--frames'); render(o, int(a[k + 1]), int(a[k + 2]))
        else: render(o)
