# Cadrele reelului „Eroarea P2002”: planurile din reel_story.py (imagine Blender + particule + texte) -> <out>/NNNNN.jpg (1080x1920).
#   python comp_reel.py --out <reel>/frames_base [--part i n] [--range f0 f1]     cadrele lipsa (se poate relua, sare peste cele existente)
#   python comp_reel.py --t 3 12.5 60 --out proba.jpg --sheet 4 [--guides] [--nohud]   cadre de proba
import os, sys, json, math, argparse, time
import numpy as np, cv2
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import fxlib as X, shots as S, comp as CP
import reel_story as R
from fxlib import seg

T_ORB = S.ORBIT_N / S.FPS
def hero_rgba(u, W, H):
    """hook: rotirea in jurul motorului (5 s), apoi cadrul fix din acelasi unghi"""
    p, z, J = CP.plate('heroB', 'solid', W, H)
    if u >= T_ORB + 0.30: return p, J
    i = int(np.clip(round(u * S.FPS), 0, S.ORBIT_N - 1)); key = ('o', i, W, H)
    o = CP._cache.get(key)
    if o is None: o = CP._keep(key, CP._rgba(os.path.join(CP.PL, 'orbit', '%04d.png' % i), W, H), cap=6)
    a = float(seg(u, T_ORB - 0.03, T_ORB + 0.30))
    return (o if a <= 0 else o * (1 - a) + p * a), J

def edge_mask(W, H, k, m=80.0):
    key = ('em', W, H); e = CP._cache.get(key)
    if e is None:
        x = np.arange(W, dtype=np.float32); y = np.arange(H, dtype=np.float32)
        mx = np.clip(np.minimum(x, W - 1 - x) / (m * k), 0, 1); my = np.clip(np.minimum(y, H - 1 - y) / (m * k), 0, 1)
        mx = mx * mx * (3 - 2 * mx); my = my * my * (3 - 2 * my)
        e = CP._keep(key, (my[:, None] * mx[None, :]).astype(np.float32), cap=64)
    return e

def compose(shot, u, W, H):
    k = W / S.W
    zb = None
    if shot.kind == 'hero':
        rgba, J = hero_rgba(u, W, H)
    else:
        lay = shot.layers(u); rgba = None; J = None; wmax = -1
        for (st, w) in lay:
            if w <= 0.001: continue
            p, z, Jp = CP.plate(shot.cam, st, W, H)
            rgba = p * w if rgba is None else rgba + p * w
            if w > wmax: wmax = w; zb = z; J = Jp
        if shot.loop:
            kind, n, rate, off = shot.loop
            ph = int(round(shot.lu(u) * rate + off)) % n
            try:
                lp, lz = CP.loop_frame(shot.cam, kind, ph, W, H)
                rgba = CP.disjoint_over(rgba, lp); zb = np.minimum(zb, lz)
            except FileNotFoundError:
                pass
        if shot.grade is not None:
            gn, gm = shot.grade; al = np.maximum(rgba[..., 3:4], 1e-4)
            rgba = np.concatenate([np.clip(rgba[..., :3] / al, 0, 1) ** gm * gn * rgba[..., 3:4], rgba[..., 3:4]], -1)
    cam = X.Cam(J, W, H)
    zoom, dx, dy = shot.kb(u); dx *= k; dy *= k
    if zoom < 0.999:            # imaginea micsorata (hook): marginile ei se topesc in fundal
        rgba = rgba * (1 - min((1 - zoom) / 0.04, 1.0) * (1 - edge_mask(W, H, k)))[..., None]
    if abs(zoom - 1) > 1e-5 or abs(dx) > 1e-3 or abs(dy) > 1e-3:
        cam.set2d(zoom, dx, dy); A = cam.affine()
        rgba = cv2.warpAffine(rgba, A, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
        if zb is not None: zb = cv2.warpAffine(zb, A, (W, H), flags=cv2.INTER_NEAREST, borderMode=cv2.BORDER_CONSTANT, borderValue=1e6)
    shot._cam = cam
    add = None
    if shot.fx is not None:
        cv = X.Canvas(W, H, zb); shot.fx(u, cam, cv, k)
        out = cv.flush()
        if out['over'] is not None:
            c, a = out['over']
            rgba = np.concatenate([c + rgba[..., :3] * (1 - a[..., None]), (a + rgba[..., 3] * (1 - a))[..., None]], -1)
        add = out['add']
    bg = CP.background(W, H)
    rgb = bg * (1 - rgba[..., 3:4]) + rgba[..., :3]
    if shot.dim is not None:
        d = shot.dim(u)
        if d > 0.001:
            bl = cv2.GaussianBlur(rgb, (0, 0), 9 * k)
            rgb = rgb * (1 - d) + (bl * 0.34 + bg * 0.10) * d
    if add is not None:
        sm = cv2.resize(add, (W // 4, H // 4), interpolation=cv2.INTER_AREA)
        bloom = cv2.resize(cv2.GaussianBlur(sm, (0, 0), 5.0 * k), (W, H), interpolation=cv2.INTER_LINEAR)
        g = add + bloom * 0.45
        rgb = 1 - (1 - np.clip(rgb, 0, 1)) * (1 - np.clip(g, 0, 1))
    # planul urcat in cadru: marginea de jos a imaginii se topeste in fundal (nu ramane o linie sub subtitrari)
    yb = zoom * (H - H * 0.5) + H * 0.5 + dy
    if yb < H - 1:
        y = np.arange(H, dtype=np.float32); m = np.clip((yb - 6 * k - y) / (190.0 * k), 0, 1); m = (m * m * (3 - 2 * m))[:, None, None]
        rgb = bg + (rgb - bg) * m
    return np.clip(rgb, 0, 1)

def frame(t, W, H, SH, xf=0.28):
    act = [s for s in SH if s.t0 <= t < s.t1]
    s = act[0] if act else SH[-1]
    img = compose(s, t - s.t0, W, H)
    i = SH.index(s)
    if i > 0 and (t - s.t0) < xf and s.xf:
        p = SH[i - 1]; a = (t - s.t0) / xf; a = a * a * (3 - 2 * a)
        prev = compose(p, min(t - p.t0, p.t1 - p.t0 + xf), W, H)
        img = prev * (1 - a) + img * a
    return img

def guides(im):
    for y, c in ((196, (0, 255, 0)), (440, (0, 255, 0)), (1250, (0, 255, 255)), (1290, (0, 200, 255)), (1530, (0, 200, 255))):
        cv2.line(im, (0, y), (im.shape[1], y), c, 2)
    for x in range(120, 1080, 120):
        cv2.line(im, (x, 0), (x, 1920), (90, 90, 90), 1); cv2.putText(im, str(x), (x + 4, 1900), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 200), 2)
    for y in range(120, 1920, 120):
        cv2.line(im, (0, y), (1080, y), (90, 90, 90), 1); cv2.putText(im, str(y), (4, y - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 200), 2)
    return im

JPG = [cv2.IMWRITE_JPEG_QUALITY, 93]
if hasattr(cv2, 'IMWRITE_JPEG_SAMPLING_FACTOR'): JPG += [cv2.IMWRITE_JPEG_SAMPLING_FACTOR, cv2.IMWRITE_JPEG_SAMPLING_FACTOR_444]

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--t', type=float, nargs='*'); ap.add_argument('--range', type=int, nargs=2)
    ap.add_argument('--out', default='reel_frames'); ap.add_argument('--hud', default=os.path.join(HERE, 'hudr'))
    ap.add_argument('--nohud', action='store_true'); ap.add_argument('--sheet', type=int, default=0)
    ap.add_argument('--guides', action='store_true'); ap.add_argument('--part', type=int, nargs=2, default=None)
    ap.add_argument('--scale', type=float, default=1.0); ap.add_argument('--crop', type=int, nargs=2, default=None)
    ap.add_argument('--frames', type=int, nargs='*', default=None)
    a = ap.parse_args()
    W = int(S.W * a.scale); H = int(S.H * a.scale); SH = R.SHOTS
    if a.t is not None:
        ims = []
        for t in a.t:
            t0 = time.time(); f = int(round(t * S.FPS)); im = frame(f / S.FPS, W, H, SH)
            if not a.nohud: im = CP.with_hud(im, f, W, H, a.hud)
            im = CP.to8(im)
            if a.guides: im = guides(im)
            if a.crop: im = np.ascontiguousarray(im[a.crop[0]:a.crop[1]])
            if a.sheet: cv2.putText(im, '%.2f' % t, (int(880 * a.scale), im.shape[0] - 40), cv2.FONT_HERSHEY_SIMPLEX, 1.6 * a.scale, (255, 255, 255), 3)
            ims.append(im); print('t=%.2f %.2fs' % (t, time.time() - t0), flush=True)
        if a.sheet:
            rows = [np.concatenate(ims[i:i + a.sheet] + [np.zeros_like(ims[0])] * (a.sheet - len(ims[i:i + a.sheet])), 1) for i in range(0, len(ims), a.sheet)]
            sh = np.concatenate(rows, 0); sc = min(1.0, 2160.0 / sh.shape[1])
            if sc < 1: sh = cv2.resize(sh, (int(sh.shape[1] * sc), int(sh.shape[0] * sc)), interpolation=cv2.INTER_AREA)
            cv2.imwrite(a.out, sh, [cv2.IMWRITE_JPEG_QUALITY, 90])
        else:
            for t, im in zip(a.t, ims): cv2.imwrite(a.out if len(ims) == 1 else a.out.replace('.', '_%06.2f.' % t, 1), im, [cv2.IMWRITE_JPEG_QUALITY, 93])
        sys.exit()
    NF = int(R.TOTAL * S.FPS) + 1
    f0, f1 = a.range if a.range else (0, NF)
    fr = list(range(f0, f1))
    if a.frames: fr = a.frames
    if a.part: fr = [f for f in fr if f % a.part[1] == a.part[0]]
    os.makedirs(a.out, exist_ok=True); ts = time.time(); done = 0
    for f in fr:
        p = os.path.join(a.out, '%05d.jpg' % f)
        if os.path.exists(p): continue
        hp = os.path.join(a.hud, '%05d.png' % f)
        if not a.nohud and not os.path.exists(hp): print('lipseste HUD', f, flush=True); continue
        im = frame(f / S.FPS, W, H, SH)
        if not a.nohud: im = CP.with_hud(im, f, W, H, a.hud)
        cv2.imwrite(p + '.tmp.jpg', CP.to8(im), JPG); os.replace(p + '.tmp.jpg', p); done += 1
        if done % 50 == 0: print('cadru %d  (%d facute)  %.2f s/cadru' % (f, done, (time.time() - ts) / done), flush=True)
    print('gata', done, flush=True)
