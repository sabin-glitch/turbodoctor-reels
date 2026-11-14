"""Screen frames for the `phone` piece (14.11.2026, „Recondiționări perfecte la prețuri corecte”).
A phone screen recording is re-timed onto the reel's timeline (parts played at 1x, typing/scrolling faster, dead time skipped)
and written as one JPEG per output frame: <reel>/assets/phone/00000.jpg ...

  python3 build_phone_frames.py <reel folder> <spec.json>

spec.json: {"src": "<screen recording>", "f0": <reel time of frame 0>, "w": 1100,
            "segs": [[out_a, out_b, rec_a, rec_b], ...]}   # reel seconds -> recording seconds, linear inside each segment;
                                                            # segments are contiguous in out time; a jump in rec time is a cut
Prints the reel time of each recording moment listed in "marks" (rec seconds), to place taps and labels.
"""
import json, os, sys, shutil
import cv2

reel, spec = sys.argv[1], json.load(open(sys.argv[2]))
segs = spec["segs"]; f0 = spec["f0"]; W = spec.get("w", 1100); FPS = 30
for (a, b, _, _), (a2, _, _, _) in zip(segs[:-1], segs[1:]):
    assert abs(b - a2) < 1e-6, f"segments not contiguous at {b} / {a2}"
end = segs[-1][1]; n = int(round((end - f0) * FPS))

def rec_time(t):
    for a, b, ra, rb in segs:
        if t < b: return ra + (rb - ra) * max(0.0, t - a) / max(1e-9, b - a)
    return segs[-1][3]

def out_time(r):
    for a, b, ra, rb in segs:
        if min(ra, rb) - 1e-6 <= r <= max(ra, rb) + 1e-6: return a + (b - a) * (r - ra) / max(1e-9, rb - ra)
    return None

cap = cv2.VideoCapture(spec["src"]); rfps = cap.get(cv2.CAP_PROP_FPS); last = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
need = {}
for i in range(n):
    need.setdefault(max(0, min(last, int(round(rec_time(f0 + i / FPS) * rfps)))), []).append(i)
out = f"{reel}/assets/phone"; shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
H = None; k = min(need); cap.set(cv2.CAP_PROP_POS_FRAMES, k); stop = max(need); written = 0
while k <= stop:
    ok, fr = cap.read()
    if not ok: break
    if k in need:
        if H is None: H = int(round(fr.shape[0] * W / fr.shape[1] / 2) * 2)
        im = cv2.resize(fr, (W, H), interpolation=cv2.INTER_AREA)
        for i in need[k]:
            cv2.imwrite(f"{out}/{i:05d}.jpg", im, [cv2.IMWRITE_JPEG_QUALITY, spec.get("q", 88)]); written += 1
    k += 1
json.dump({"n": n, "f0": f0, "w": W, "h": H, "sw": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), "sh": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}, open(f"{out}/phone.json", "w"))
print(f"phone frames: {written}/{n}  {W}x{H}  reel {f0:.2f}-{end:.2f}s  -> {out}")
for name, r in spec.get("marks", {}).items():
    t = out_time(r); print(f"  {name:22s} rec {r:6.2f} -> reel {t:.3f}" if t is not None else f"  {name:22s} rec {r:6.2f} -> (not shown)")
