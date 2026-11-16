# Caută stropii de particule tăiați de limita de nucleu (Canvas.RMAX): un gaussian tăiat lasă un pătrat cu margine vizibilă.
#   python clipscan.py [pas_s]   -> pe plan: câți stropi sunt tăiați, raza maximă și înălțimea treptei de la margine (a * valoarea gaussianului la tăietură)
import os, sys, json, math
import numpy as np
sys.path.insert(0, '/home/claude/dpf/work')
import fxlib as X, shots as S, comp as CP
import reel_story as R
W, H = S.W, S.H; k = 1.0; step = float(sys.argv[1]) if len(sys.argv) > 1 else 0.5
class Rec:
    RMAX = X.Canvas.RMAX
    def __init__(s): s.rows = []
    def dots(s, x, y, z, r, col, a=1.0, mode='add', shape='g', zbias=0.004, ztest=True, shade=0.0):
        x = np.asarray(x, np.float32); n = len(x)
        if n == 0: return
        y = np.asarray(y, np.float32); z = np.broadcast_to(np.asarray(z, np.float32), (n,))
        r = np.broadcast_to(np.asarray(r, np.float32), (n,)); a = np.broadcast_to(np.asarray(a, np.float32), (n,))
        ext = 1.7 if shape == 'g' else 1.0
        ok = np.isfinite(x) & np.isfinite(y) & (z > 0.02) & (a > 0.004) & (r > 0.05)
        ok &= (x > -r * ext) & (x < W + r * ext) & (y > -r * ext) & (y < H + r * ext)
        if not ok.any(): return
        r, a = r[ok], a[ok]
        need = np.ceil(r * ext + 0.5)
        cl = need > s.RMAX
        if not cl.any(): return
        if shape == 'g': edge = a[cl] * np.exp(-(s.RMAX ** 2) / (2 * (0.5 * r[cl]) ** 2))
        else: edge = a[cl] * 1.0
        s.rows.append((mode, shape, int(cl.sum()), float(r[cl].max()), float(edge.max()), float(edge.sum())))
for sh in R.SHOTS:
    if sh.fx is None: print('%-8s fără particule' % sh.id if hasattr(sh, 'id') else sh.cam); continue
    worst = None; ncl = 0
    u = 0.0
    while u < sh.t1 - sh.t0:
        if sh.kind == 'hero': J = json.load(open(CP.find('heroB__solid') + '.json'))
        else:
            lay = [(st, w) for (st, w) in sh.layers(u) if w > 0.001]; st = max(lay, key=lambda q: q[1])[0]
            J = json.load(open(CP.find('%s__%s' % (sh.cam, st)) + '.json'))
        cam = X.Cam(J, W, H); zoom, dx, dy = sh.kb(u); cam.set2d(zoom, dx * k, dy * k)
        cv = Rec(); sh.fx(u, cam, cv, k)
        for row in cv.rows:
            ncl += row[2]
            if worst is None or row[4] > worst[1][4]: worst = (u, row)
        u += step
    name = getattr(sh, 'id', None) or getattr(sh, 'name', None) or sh.cam
    if worst is None: print('%-10s t0=%6.2f  fără stropi tăiați' % (name, sh.t0))
    else: print('%-10s t0=%6.2f  stropi tăiați (însumat pe probe): %5d   cel mai rău la u=%.1f (t=%.1f): mod %s formă %s, n=%d, r max %.0f px, treaptă max %.3f, sumă %.2f' % ((name, sh.t0, ncl, worst[0], sh.t0 + worst[0]) + worst[1]))
