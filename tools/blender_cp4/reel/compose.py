# Compune cadrele de baza ale reelului din randarile Blender (placa fixa + regiunea pieselor in miscare + pana arborelui),
# peste fundalul reelului, apoi adauga trecerile paginii three.js: 'add' (scantei, stralucire) si 'ovl' (bule, pilitura, etichete, panou).
#   python3 compose.py <director.json> <out_dir> [f0 f1] [--allow-missing]
# Variabile: BL = dosarul out_reel al randarilor Blender, OV = dosarul trecerilor paginii (ov/ovl, ov/add), WM=0 scoate marcajul din fundal.
import json, os, sys
import numpy as np, cv2
HERE = os.path.dirname(os.path.abspath(__file__))
BL = os.environ.get('BL', os.path.join(HERE, '../bl/out_reel'))
OV = os.environ.get('OV', os.path.join(HERE, 'ov'))
args = [a for a in sys.argv[1:] if not a.startswith('--')]; ALLOW = '--allow-missing' in sys.argv
DJ = json.load(open(args[0])); OUT = args[1]; os.makedirs(OUT, exist_ok=True)
F0, F1 = (int(args[2]), int(args[3])) if len(args) > 3 else (0, 10 ** 9)
BG = np.array([23, 20, 17], np.float32)          # fundalul paginii, #111417, in ordinea BGR
FE = 24                                          # latimea zonei de trecere de la marginea regiunii R1 (px)
H, W = 1920, 1080
USE_WM = os.environ.get('WM', '1') != '0'      # marcajul "TURBO DOCTOR" din fundal, in spatele pompei (wm.py)
if USE_WM: import wm

def rgba(path):
    """PNG cu alfa -> BGRA float32 premultiplicat (0..255)"""
    im = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if im is None: raise FileNotFoundError(path)
    im = im.astype(np.float32)
    if im.shape[2] == 3: im = np.dstack([im, np.full(im.shape[:2], 255, np.float32)])
    im[..., :3] *= im[..., 3:4] / 255.0
    return im

def feather(h, w, fe):
    y = np.minimum(np.arange(h), np.arange(h)[::-1]).astype(np.float32); x = np.minimum(np.arange(w), np.arange(w)[::-1]).astype(np.float32)
    s = lambda v: np.clip(v / fe, 0, 1) ** 2 * (3 - 2 * np.clip(v / fe, 0, 1))
    return (s(y)[:, None] * s(x)[None, :])[..., None]

BOX = {c: json.load(open(os.path.join(BL, 'boxes_%s.json' % c))) for c in ('W', 'C')}
_plate, _m1, _m2 = {}, {}, {}
def plate(cam, s):
    if (cam, s) not in _plate: _plate[(cam, s)] = rgba(os.path.join(BL, '%s_%s_plate.png' % (cam, s)))
    return _plate[(cam, s)]
def m1(cam):
    if cam not in _m1: b = BOX[cam]['R1']; _m1[cam] = feather(b[3] - b[1], b[2] - b[0], FE)
    return _m1[cam]
def m2(cam):
    """masca penei: pixelii care se schimba de-a lungul unei ture, largiti si inmuiati"""
    if cam not in _m2:
        d = os.path.join(BL, '%s_HOT_R2' % cam); fs = sorted(os.listdir(d)) if os.path.isdir(d) else []
        if len(fs) < 76:
            if not ALLOW: raise FileNotFoundError('bucla penei incompleta: ' + d)
            _m2[cam] = None; return None
        st = np.stack([cv2.imread(os.path.join(d, f), cv2.IMREAD_UNCHANGED).astype(np.int16) for f in fs])
        var = (st.max(0) - st.min(0)).max(-1).astype(np.float32)
        m = (var > 10).astype(np.uint8); m = cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13)))
        m = cv2.GaussianBlur(m.astype(np.float32), (0, 0), 2.5)[..., None] * feather(m.shape[0], m.shape[1], 8)
        _m2[cam] = m; cv2.imwrite(os.path.join(OUT, '_mask_r2_%s.png' % cam), (m[..., 0] * 255).astype(np.uint8))
    return _m2[cam]

def blender(r):
    b = r['bl']
    if 'full' in b: return rgba(os.path.join(BL, b['full']))
    cam = b['cam']
    P = sum(plate(cam, s) * w for s, w in b['plates']) if len(b['plates']) > 1 else plate(cam, b['plates'][0][0]).copy()
    x0, y0, x1, y1 = BOX[cam]['R1']
    crop = None
    for s, k, w in b['r1']:
        c = rgba(os.path.join(BL, '%s_%s_R1' % (cam, s), 'k%03d.png' % k)); crop = c * w if crop is None else crop + c * w
    M = m1(cam); P[y0:y1, x0:x1] = P[y0:y1, x0:x1] * (1 - M) + crop * M
    M2 = m2(cam)
    if M2 is not None:
        x0, y0, x1, y1 = BOX[cam]['R2']; c = rgba(os.path.join(BL, '%s_HOT_R2' % cam, 'k%03d.png' % b['r2']))
        P[y0:y1, x0:x1] = P[y0:y1, x0:x1] * (1 - M2) + c * M2
    return P

n = 0
for r in DJ['frames']:
    f = r['f']
    if not (F0 <= f <= F1): continue
    try: P = blender(r)
    except FileNotFoundError as e:
        if ALLOW: print('lipsa', f, e); continue
        raise
    T = 1 - P[..., 3:4] / 255.0
    img = P[..., :3] + BG * T
    if USE_WM: D = wm.delta(f); img += D * T
    if r['add']:
        a = cv2.imread(os.path.join(OV, 'add', '%05d.png' % f), cv2.IMREAD_COLOR)
        if a is None: raise FileNotFoundError('add %05d' % f)
        img += a.astype(np.float32)
    o = cv2.imread(os.path.join(OV, 'ovl', '%05d.png' % f), cv2.IMREAD_UNCHANGED)
    if o is None: raise FileNotFoundError('ovl %05d' % f)
    o = o.astype(np.float32); al = o[..., 3:4] / 255.0
    img = np.clip(img, 0, 255) * (1 - al) + o[..., :3] * al
    if USE_WM:
        k = wm.kfade(r['U'])          # cand pagina stinge cadrul spre fundal, marcajul ramane
        if k > 0: img += D * (k * wm.GRAD[..., None])
    cv2.imwrite(os.path.join(OUT, '%05d.jpg' % f), np.clip(img + 0.5, 0, 255).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 95])
    n += 1
    if n % 100 == 0: print('compus', f, flush=True)
print('gata:', n, 'cadre in', OUT)
