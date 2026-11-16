# Pune marcajul "TURBO DOCTOR" din fundal pe cadrele reelului care nu sunt refacute cu Blender (cele din regie il primesc in compose.py).
#   python3 wmapply.py <director.json> <frames_in> <masks> <frames_out> [k n]
# cadru = original + clip(transparenta + k_fade * degrade) * delta; transparenta = 1 - masca (540x960, marita la 1080x1920).
# Masca (anim/amask.cjs) = ce acopera fundalul: obiectele opace ale scenei si HUD-ul. Caroseria "raze X" si stralucirile sunt aditive,
# deci fundalul se vede intreg prin ele si marcajul ramane sub ele. Mastile sunt randate rar (mask2_list.json: din 4 in 4 cadre, mai des
# la miscari rapide, pe ambele parti ale taieturilor); la un cadru fara masca se interpoleaza liniar intre vecinii randati.
import json, os, sys
import numpy as np, cv2
import wm
dj, FIN, MASK, OUT = sys.argv[1:5]; K, N = (int(sys.argv[5]), int(sys.argv[6])) if len(sys.argv) > 6 else (0, 1)
skip = set(r['f'] for r in json.load(open(dj))['frames'])
U = json.load(open(os.environ.get('UF', '/home/claude/reels/amorsare_filtru/vo/uframes.json')))
ONLY = set(int(x) for x in os.environ['ONLY'].split(',')) if os.environ.get('ONLY') else None      # proba: doar aceste cadre
have = set(int(x[:5]) for x in os.listdir(MASK) if x.endswith('.png'))
os.makedirs(OUT, exist_ok=True); n = 0
_c = {}
def mask(f):
    if f not in _c:
        if len(_c) > 8: _c.pop(min(_c))
        _c[f] = cv2.imread(os.path.join(MASK, '%05d.png' % f), cv2.IMREAD_GRAYSCALE).astype(np.float32)
    return _c[f]
for f in range(len(U)):
    if f % N != K or f in skip or (ONLY is not None and f not in ONLY): continue
    op = os.path.join(OUT, '%05d.jpg' % f)
    if os.path.exists(op): continue          # facut deja (o rulare anterioara)
    if f in have: m = mask(f)
    else:              # masca interpolata liniar intre cei mai apropiati vecini randati
        lo = next((g for g in range(f - 1, f - 6, -1) if g in have), None); hi = next((g for g in range(f + 1, f + 6) if g in have), None)
        if lo is None or hi is None: raise FileNotFoundError('masca %05d' % f)
        w = (f - lo) / (hi - lo); m = (1 - w) * mask(lo) + w * mask(hi)
    m = cv2.resize(m, (1080, 1920), interpolation=cv2.INTER_LINEAR) / 255.0
    T = np.clip(1.0 - m + wm.kfade(U[f]) * wm.GRAD, 0, 1)[..., None]
    im = cv2.imread(os.path.join(FIN, '%05d.jpg' % f), cv2.IMREAD_COLOR).astype(np.float32)
    tp = os.path.join(OUT, '.tmp%d_%d.jpg' % (K, N))
    cv2.imwrite(tp, np.clip(im + T * wm.delta(f) + 0.5, 0, 255).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 95]); os.replace(tp, op); n += 1
    if n % 300 == 0: print('marcaj', f, flush=True)
print('gata', K, 'cadre cu marcaj:', n)
