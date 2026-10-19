"""Licence plates: find them in a clip and write tracks for caption_clean.py --plates (blur only the plate, frame by frame).
Rule (approved on the DPF batch): no readable licence plate may stay in a reel - ours, clients', cars in the background.

usage: python3 plates.py <video.mp4> <out.json> [--fps 10] [--conf 0.25] [--windows 12-16,140-170] [--prior coarse.json@25,32,...]
                         [--model yolo-v9-t-384-license-plate-end2end] [--sheet sheet.jpg]
  - detector: YOLOv9 licence-plate model from open-image-models (ONNX, CPU; ~65 ms per 1080x1920 frame with the 384 model),
    run on 3 overlapping 1080x1080 squares per frame so small plates in the background are found too;
  - frames are numbered on the 30 fps CFR grid (t = n/30), the same grid caption_clean.py works on; --fps samples every
    30/fps-th frame, --windows limits the scan to time ranges (seconds);
  - detections are linked into tracks (same plate across samples, gaps up to 0.6 s), written as
    {"fps", "src", "tracks": [{"id", "t0", "t1", "n", "conf", "boxes": [[t, x0, y0, x1, y1, conf], ...]}]} in 1080x1920 coords;
  - the sheet: one crop per track (best sample) with id / time / size; check that every kept track is a real plate.
    A false positive (sign, sticker, van lettering, lift branding) gets "skip": true, or caption_clean.py --plates out.json@skip=3,7.
  - two passes for handheld footage (the detector misses a plate in some frames, so a coarse pass alone leaves gaps):
      1. plates.py clip.mp4 coarse.json --fps 10 --sheet coarse.jpg          -> look at the sheet, note the real plates' ids
      2. plates.py clip.mp4 dense.json --fps 30 --prior coarse.json@25,32,41 --sheet dense.jpg
         every frame, only around the real plates (+-1.5 s); dense tracks touching a real coarse track are kept, the rest
         get "skip": true (they are on the sheet with an x: check that none of them is a plate the coarse pass missed);
      3. caption_clean.py ... --plates dense.json; then plates.py on the cleaned clip (same windows) must find no readable plate.
Setup: pip install --break-system-packages open-image-models onnxruntime (the model downloads itself from GitHub on first use)."""
import argparse, json, subprocess, warnings
import cv2, numpy as np

warnings.filterwarnings("ignore")
ap = argparse.ArgumentParser(); ap.add_argument("src"); ap.add_argument("out")
ap.add_argument("--fps", type=float, default=10); ap.add_argument("--conf", type=float, default=0.25)
ap.add_argument("--windows", default=""); ap.add_argument("--prior", default="")
ap.add_argument("--model", default="yolo-v9-t-384-license-plate-end2end"); ap.add_argument("--sheet", default=None)
a = ap.parse_args()
from open_image_models import create_detector   # noqa: E402  (slow import, after argument parsing)

W, H, FPS = 1080, 1920, 30
STEP = max(1, int(round(FPS / a.fps)))
TILES = (0, 420, 840)   # 1080x1080 squares; overlap 660 px, so every plate is whole in at least one
det = create_detector(a.model, conf_thresh=a.conf)


def iou(p, q):
    ix = max(0, min(p[2], q[2]) - max(p[0], q[0])); iy = max(0, min(p[3], q[3]) - max(p[1], q[1])); i = ix * iy
    return i / max(1, (p[2] - p[0]) * (p[3] - p[1]) + (q[2] - q[0]) * (q[3] - q[1]) - i)


PRIOR = []   # real plates from the coarse pass: (times, boxes)
if a.prior:
    path, _, ids = a.prior.partition("@"); keep = {int(v) for v in ids.split(",") if v}
    for tr in json.load(open(path))["tracks"]:
        if tr["id"] in keep:
            bx = np.array([r[:5] for r in tr["boxes"]], np.float32); PRIOR.append((bx[:, 0], bx[:, 1:5]))
WIN = [tuple(map(float, w.split("-"))) for w in a.windows.split(",") if w]
if not WIN and PRIOR:
    for ts, _ in sorted(PRIOR, key=lambda p: p[0][0]):
        s, e = float(ts[0]) - 1.5, float(ts[-1]) + 1.5
        if WIN and s <= WIN[-1][1]: WIN[-1] = (WIN[-1][0], max(WIN[-1][1], e))
        else: WIN.append((max(0.0, s), e))
in_win = (lambda t: any(s <= t <= e for s, e in WIN)) if WIN else (lambda t: True)


def detect(fr):
    found = []
    for ty in TILES:
        for d in det.predict(np.ascontiguousarray(fr[ty:ty + 1080])):
            b = d.bounding_box; found.append([b.x1, b.y1 + ty, b.x2, b.y2 + ty, float(d.confidence)])
    found.sort(key=lambda r: -r[4]); keep = []
    for r in found:   # same plate seen in two squares -> keep the most confident box
        if all(iou(r, k) < 0.3 for k in keep): keep.append(r)
    return keep


def frames():   # (n, t, frame) on the 30 fps grid, only the sampled ones inside the windows
    p = subprocess.Popen(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", a.src, "-vf", f"fps={FPS},scale={W}:{H}",
                          "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
    FB = W * H * 3; n = 0; last = max((e for _, e in WIN), default=1e9)
    while True:
        b = p.stdout.read(FB)
        if len(b) < FB: break
        t = round(n / FPS, 3)
        if t > last + 0.1: break
        if n % STEP == 0 and in_win(t): yield n, t, np.frombuffer(b, np.uint8).reshape(H, W, 3)
        n += 1
    p.kill()


tracks = []; GAP = 0.6; nf = 0
for n, t, fr in frames():
    nf += 1
    for x0, y0, x1, y1, c in detect(fr):
        w = x1 - x0; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; best, bd = None, 1e9
        for tr in tracks:
            lt, lx0, ly0, lx1, ly1, _ = tr["boxes"][-1]
            if lt >= t or t - lt > GAP: continue
            lw = lx1 - lx0; dist = np.hypot(cx - (lx0 + lx1) / 2, cy - (ly0 + ly1) / 2)
            if dist < max(120, 2.5 * max(w, lw)) * (1 + (t - lt) * 2) and 0.4 < w / max(1, lw) < 2.5 and dist < bd: best, bd = tr, dist
        if best is None: best = {"id": len(tracks) + 1, "boxes": []}; tracks.append(best)
        best["boxes"].append([t, int(x0), int(y0), int(x1), int(y1), round(c, 3)])
for tr in tracks:
    tr["t0"], tr["t1"] = tr["boxes"][0][0], tr["boxes"][-1][0]; tr["conf"] = max(r[5] for r in tr["boxes"]); tr["n"] = len(tr["boxes"])
    if PRIOR:   # kept only if it touches a real plate of the coarse pass (same place, same moment)
        hit = False
        for t, x0, y0, x1, y1, _ in tr["boxes"]:
            for ts, bs in PRIOR:
                if ts[0] - 0.35 <= t <= ts[-1] + 0.35:
                    pb = [float(np.interp(t, ts, bs[:, j])) for j in range(4)]; pw = pb[2] - pb[0]; ph = pb[3] - pb[1]
                    grown = [pb[0] - pw, pb[1] - ph, pb[2] + pw, pb[3] + ph]   # the plate moves between coarse samples
                    if iou([x0, y0, x1, y1], grown) > 0: hit = True; break
            if hit: break
        if not hit: tr["skip"] = True
json.dump({"fps": a.fps, "src": a.src, "model": a.model, "windows": WIN, "tracks": tracks}, open(a.out, "w"), indent=1)
for tr in tracks:
    md = np.median([[r[3] - r[1], r[4] - r[2]] for r in tr["boxes"]], axis=0)
    print(f"#{tr['id']:<3d} t {tr['t0']:7.2f}-{tr['t1']:7.2f}  n {tr['n']:3d}  conf {tr['conf']:.2f}  ~{md[0]:.0f}x{md[1]:.0f}{'  skip' if tr.get('skip') else ''}")
print(f"PLATES_OK tracks {len(tracks)} kept {sum(not tr.get('skip') for tr in tracks)} frames {nf} windows {len(WIN)}")

if a.sheet and tracks:   # one crop per track (best sample): id, time, samples, conf, size; skipped tracks marked with an x
    CW, CH, COLS = 240, 150, 8; want = {}
    for tr in tracks:
        r = max(tr["boxes"], key=lambda r: r[5]); want.setdefault(int(round(r[0] * FPS)), []).append((tr, r))
    crops = {}
    for n, t, fr in frames():
        for tr, (_, x0, y0, x1, y1, c) in want.get(n, []):
            cx, cy = (x0 + x1) // 2, (y0 + y1) // 2; X0 = max(0, min(W - CW, cx - CW // 2)); Y0 = max(0, min(H - CH, cy - CH // 2))
            cr = fr[Y0:Y0 + CH, X0:X0 + CW].copy(); cv2.rectangle(cr, (x0 - X0 - 2, y0 - Y0 - 2), (x1 - X0 + 2, y1 - Y0 + 2), (0, 255, 0), 1)
            cv2.rectangle(cr, (0, 0), (CW, 16), (0, 0, 0), -1)
            cv2.putText(cr, f"#{tr['id']} {t:.1f} n{tr['n']} {c:.2f} {x1 - x0}x{y1 - y0}", (2, 12), 0, .4, (0, 255, 255), 1)
            if tr.get("skip"): cv2.line(cr, (CW - 22, 2), (CW - 8, 14), (0, 0, 255), 2); cv2.line(cr, (CW - 8, 2), (CW - 22, 14), (0, 0, 255), 2)
            crops[tr["id"]] = cr
    ids = [tr["id"] for tr in tracks]; per = COLS * 8
    for s in range(0, len(ids), per):
        g = [crops.get(i, np.zeros((CH, CW, 3), np.uint8)) for i in ids[s:s + per]]
        while len(g) % COLS: g.append(np.zeros((CH, CW, 3), np.uint8))
        name = a.sheet if len(ids) <= per else a.sheet.replace(".jpg", f"_{s // per}.jpg")
        cv2.imwrite(name, np.vstack([np.hstack(g[i:i + COLS]) for i in range(0, len(g), COLS)]), [cv2.IMWRITE_JPEG_QUALITY, 90])
