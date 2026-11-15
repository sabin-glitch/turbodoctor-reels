# Montajul: cadre Blender + particule + texte -> film. Rulat cu venv2 (numpy, OpenCV).
import os, sys, json, math, subprocess, argparse, time
import numpy as np, cv2
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import fxlib as X, shots as S

PL = os.environ.get('DPF_PL', os.path.join(HERE, 'pl')); PLT = os.path.join(HERE, 'pl_test')
_cache = {}; _order = []
def _keep(key, val, cap=10):
    _cache[key] = val; _order.append(key)
    while len(_order) > cap: _cache.pop(_order.pop(0), None)
    return val

def _rgba(path, W, H):
    im = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if im is None: raise FileNotFoundError(path)
    im = cv2.cvtColor(im, cv2.COLOR_BGRA2RGBA).astype(np.float32) / 255.0
    im[..., :3] *= im[..., 3:4]
    if im.shape[0] != H or im.shape[1] != W:
        im = cv2.resize(im, (W, H), interpolation=cv2.INTER_AREA if im.shape[0] > H else cv2.INTER_CUBIC)
    return np.clip(im, 0, 1)

def _z(path, W, H):
    z = np.load(path)
    if os.path.basename(path).startswith('cool__'):       # lichidul de racire e translucid: adancimea lui iese cu puncte „gaurite”
        z = cv2.erode(z, np.ones((5, 5), np.uint8))
    if z.shape != (H, W): z = cv2.resize(z, (W, H), interpolation=cv2.INTER_NEAREST)
    return z

def find(name):
    for d in (PL, PLT):
        b = os.path.join(d, name)
        if os.path.exists(b + '.png') and os.path.exists(b + '.z.npy'): return b
    raise FileNotFoundError(name)

def plate(cam, state, W, H):
    key = ('p', cam, state, W, H)
    if key in _cache: return _cache[key]
    b = find('%s__%s' % (cam, state))
    return _keep(key, (_rgba(b + '.png', W, H), _z(b + '.z.npy', W, H), json.load(open(b + '.json'))))

def loop_frame(cam, kind, k, W, H):
    key = ('l', cam, kind, k, W, H)
    if key in _cache: return _cache[key]
    b = find('loop_%s_%s_%03d' % (cam, kind, k))
    return _keep(key, (_rgba(b + '.png', W, H), _z(b + '.z.npy', W, H)), cap=10)

_bg = {}
def background(W, H):
    if (W, H) in _bg: return _bg[(W, H)]
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((x - W * 0.5) / (W * 1.05)) ** 2 + ((y - H * 0.45) / (H * 0.62)) ** 2)
    g = np.clip(1 - d, 0, 1) ** 1.7
    c0 = X.hexc(0x0d0f12); c1 = X.hexc(0x242930)
    bg = (c0 + (c1 - c0) * g[..., None]).astype(np.float32)
    rng = np.random.default_rng(3); bg += (rng.random((H, W, 1)).astype(np.float32) - 0.5) * (1.6 / 255)
    _bg[(W, H)] = bg; return bg

def over(dst, src):
    """src premultiplicat peste dst premultiplicat (RGBA)"""
    return src + dst * (1 - src[..., 3:4])

def disjoint_over(dst, src):
    """strat randat cu restul scenei ca masca (holdout) peste cadrul fix: acoperirile nu se suprapun in pixel,
    deci la margini se aduna; unde stratul e opac, acopera ce era in spate"""
    a_s = src[..., 3:4]; a_d = dst[..., 3:4]
    k = np.where(a_s + a_d <= 1.0, 1.0, (1.0 - a_s) / np.maximum(a_d, 1e-4))
    return src + dst * k

def compose(shot, u, W, H):
    """un cadru al unui plan, la momentul local u (secunde). Intoarce RGB float32."""
    dur = shot.t1 - shot.t0; e = float(X.ease(u / dur)) if shot.ease else u / dur
    k = W / S.W
    if shot.kind == 'orbit':
        n = S.ORBIT_N; i = int(np.clip(round(u * S.FPS), 0, n - 1))
        key = ('o', i, W, H)
        rgba = _cache.get(key)
        if rgba is None: rgba = _keep(key, _rgba(os.path.join(PL, 'orbit', '%04d.png' % i), W, H), cap=6)
        bg = background(W, H)
        return bg * (1 - rgba[..., 3:4]) + rgba[..., :3]
    lay = shot.layers(u)
    rgba = None; zb = None; J = None; wmax = -1
    for (st, w) in lay:
        if w <= 0.001: continue
        p, z, Jp = plate(shot.cam, st, W, H)
        rgba = p * w if rgba is None else rgba + p * w
        if w > wmax: wmax = w; zb = z; J = Jp
    if shot.loop:
        kind, n, rate, off = shot.loop
        ph = int(round(u * rate + off)) % n
        try:
            lp, lz = loop_frame(shot.cam, kind, ph, W, H)
            rgba = disjoint_over(rgba, lp); zb = np.minimum(zb, lz)
        except FileNotFoundError:
            pass
    if shot.grade is not None:
        gn, gm = shot.grade; al = np.maximum(rgba[..., 3:4], 1e-4)
        rgba = np.concatenate([np.clip(rgba[..., :3] / al, 0, 1) ** gm * gn * rgba[..., 3:4], rgba[..., 3:4]], -1)
    cam = X.Cam(J, W, H)
    zoom = shot.zoom[0] + (shot.zoom[1] - shot.zoom[0]) * e
    dx = (shot.pan[0][0] + (shot.pan[1][0] - shot.pan[0][0]) * e) * k; dy = (shot.pan[0][1] + (shot.pan[1][1] - shot.pan[0][1]) * e) * k
    if abs(zoom - 1) > 1e-5 or abs(dx) > 1e-3 or abs(dy) > 1e-3:
        cam.set2d(zoom, dx, dy); A = cam.affine()
        rgba = cv2.warpAffine(rgba, A, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
        zb = cv2.warpAffine(zb, A, (W, H), flags=cv2.INTER_NEAREST, borderMode=cv2.BORDER_CONSTANT, borderValue=1e6)
    shot._cam = cam
    add = None
    if shot.fx is not None:
        cv = X.Canvas(W, H, zb); shot.fx(u, cam, cv, k)
        out = cv.flush()
        if out['over'] is not None:
            c, a = out['over']
            rgba = np.concatenate([c + rgba[..., :3] * (1 - a[..., None]), (a + rgba[..., 3] * (1 - a))[..., None]], -1)
        add = out['add']
    bg = background(W, H)
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
    return np.clip(rgb, 0, 1)

def frame(t, W, H, SH, xf=0.28):
    """cadrul filmului la momentul t (cu trecere scurta intre planuri)"""
    act = [s for s in SH if s.t0 <= t < s.t1]
    if not act: act = [SH[-1]]
    s = act[0]
    img = compose(s, t - s.t0, W, H)
    i = SH.index(s)
    if i > 0 and (t - s.t0) < xf and s.xf:
        p = SH[i - 1]; a = (t - s.t0) / xf; a = a * a * (3 - 2 * a)
        prev = compose(p, min(t - p.t0, p.t1 - p.t0 + xf), W, H)
        img = prev * (1 - a) + img * a
    return img

def with_hud(img, f, W, H, hud_dir):
    p = os.path.join(hud_dir, '%05d.png' % f)
    if not os.path.exists(p): return img
    h = cv2.imread(p, cv2.IMREAD_UNCHANGED)
    h = cv2.cvtColor(h, cv2.COLOR_BGRA2RGBA).astype(np.float32) / 255.0
    if h.shape[0] != H: h = cv2.resize(h, (W, H), interpolation=cv2.INTER_AREA)
    a = h[..., 3:4]
    return img * (1 - a) + h[..., :3] * a

def to8(img):
    return cv2.cvtColor((np.clip(img, 0, 1) * 255 + 0.5).astype(np.uint8), cv2.COLOR_RGB2BGR)

if __name__ == '__main__':
    import story
    ap = argparse.ArgumentParser()
    ap.add_argument('--scale', type=float, default=1.0); ap.add_argument('--t', type=float, nargs='*')
    ap.add_argument('--range', type=float, nargs=2); ap.add_argument('--every', type=int, default=1)
    ap.add_argument('--out', default='out.mp4'); ap.add_argument('--hud', default=os.path.join(HERE, 'hud'))
    ap.add_argument('--nohud', action='store_true'); ap.add_argument('--sheet', type=int, default=0)
    ap.add_argument('--part', type=int, nargs=2, default=None)
    a = ap.parse_args()
    W = int(S.W * a.scale); H = int(S.H * a.scale); SH = story.SHOTS
    if a.t is not None:
        ims = []
        for t in a.t:
            t0 = time.time(); f = int(round(t * S.FPS)); im = frame(f / S.FPS, W, H, SH)
            if not a.nohud: im = with_hud(im, f, W, H, a.hud)
            ims.append(to8(im)); print('t=%.2f %.2fs' % (t, time.time() - t0), flush=True)
        if a.sheet:
            rows = [np.concatenate(ims[i:i + a.sheet] + [np.zeros_like(ims[0])] * (a.sheet - len(ims[i:i + a.sheet])), 1) for i in range(0, len(ims), a.sheet)]
            cv2.imwrite(a.out, np.concatenate(rows, 0), [cv2.IMWRITE_JPEG_QUALITY, 90])
        else:
            for t, im in zip(a.t, ims): cv2.imwrite(a.out if len(ims) == 1 else a.out.replace('.', '_%06.2f.' % t, 1), im)
        sys.exit()
    t0, t1 = a.range if a.range else (0.0, story.TOTAL)
    f0, f1 = int(round(t0 * S.FPS)), int(round(t1 * S.FPS))
    fr = list(range(f0, f1, a.every))
    if a.part: fr = [f for f in fr if f % a.part[1] == a.part[0]]
    if a.out.endswith('.mp4'):
        cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', '%dx%d' % (W, H), '-r', str(S.FPS / a.every), '-i', '-',
               '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p', '-c:v', 'libx264', '-crf', '18', '-preset', 'slow',
               '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', '-color_range', 'tv', '-movflags', '+faststart', a.out]
        pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        ts = time.time()
        for n, f in enumerate(fr):
            im = frame(f / S.FPS, W, H, SH)
            if not a.nohud: im = with_hud(im, f, W, H, a.hud)
            pr.stdin.write(to8(im).tobytes())
            if n % 60 == 0: print('cadru %d / %d  %.1fs' % (n, len(fr), time.time() - ts), flush=True)
        pr.stdin.close(); pr.wait()
    else:
        os.makedirs(a.out, exist_ok=True); ts = time.time()
        for n, f in enumerate(fr):
            p = os.path.join(a.out, '%05d.png' % f)
            if os.path.exists(p): continue
            im = frame(f / S.FPS, W, H, SH)
            cv2.imwrite(p, to8(im), [cv2.IMWRITE_PNG_COMPRESSION, 1])
            if n % 60 == 0: print('cadru %d / %d  %.1fs' % (n, len(fr), time.time() - ts), flush=True)
    print('gata', flush=True)
