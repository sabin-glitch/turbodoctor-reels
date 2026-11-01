"""Track licence plates with OpenCV CSRT (promo flote, 01.11.2026) instead of placing keyframes by hand:
   python3 -I track_plates.py <video> <out.json> name:t_init:x0,y0,x1,y1:f|b:t_stop ...
Init box = the plate read on a 20 px grid at full resolution (fullcrop.py); f/b = track forward/backward until t_stop or until the
tracker is lost. Stop each track where the plate goes behind someone (check with verify_track.py) and cover the frames where it is
half hidden with a short hand-made box list. Then turn the tracks into plates.py keyframes (+10 px margin) and check with fullcrop.py."""
import cv2, json, sys, numpy as np
vid, out = sys.argv[1], sys.argv[2]
cap = cv2.VideoCapture(vid); fps = cap.get(cv2.CAP_PROP_FPS); N = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frames = []
while True:
    ok, im = cap.read()
    if not ok: break
    frames.append(im)
def refine(im, box):
    x0, y0, x1, y1 = box; pad = 25
    X0, Y0, X1, Y1 = max(0, x0 - pad), max(0, y0 - pad), min(1080, x1 + pad), min(1920, y1 + pad)
    roi = im[Y0:Y1, X0:X1]; hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    m = ((hsv[..., 2] > 150) & (hsv[..., 1] < 70)).astype(np.uint8) * 255
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not cs: return box
    c = max(cs, key=cv2.contourArea); x, y, w, h = cv2.boundingRect(c)
    return [X0 + x, Y0 + y, X0 + x + w, Y0 + y + h]
res = {}
for spec in sys.argv[3:]:
    name, ti, b, d, ts = spec.split(":"); ti = float(ti); ts = float(ts); b = [int(v) for v in b.split(",")]
    f0 = int(round(ti * fps)); fs = int(round(ts * fps))
    print(name, "init", f0, b, flush=True)
    tr = cv2.TrackerCSRT.create(); tr.init(frames[f0], (b[0], b[1], b[2] - b[0], b[3] - b[1]))
    step = 1 if d == "f" else -1; boxes = {f0: b}
    for f in range(f0 + step, fs + step, step):
        if f < 0 or f >= len(frames): break
        ok, (x, y, w, h) = tr.update(frames[f])
        if not ok: print(name, "lost at", f, round(f / fps, 2), flush=True); break
        boxes[f] = [int(x), int(y), int(x + w), int(y + h)]
    res[name] = {str(k): v for k, v in sorted(boxes.items())}
    ks = sorted(boxes); print(name, "frames", ks[0], ks[-1], "first", boxes[ks[0]], "last", boxes[ks[-1]], flush=True)
json.dump(res, open(out, "w"))
