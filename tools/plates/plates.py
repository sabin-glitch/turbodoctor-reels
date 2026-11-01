"""Blur licence plates that MOVE through the frame (reparații în lucru Iași, 01.11.2026), before new_reel.sh:
   python3 plates.py <src.mp4> <out.mp4> <plates.json>
plates.json: {"boxes": [[[t, x0, y0, x1, y1], ...], ...],                   # one list of keyframes per plate (1080x1920 coords)
              "segments": [{"th": 62, "n": 5, "keys": [[t, xa, ya, xb, yb], ...]}]}  # plate seen edge-on along a diagonal
Keyframes are interpolated linearly on every frame (30 fps) and passed to pipeline/caption_clean.py as one --blur per frame;
a segment is covered by n small boxes along the line (thickness th), so the blur stays on the plate, not on half the frame.
Find the keyframes with fullcrop.py (full-res crops with a 60 px grid) and check the result the same way: nothing readable."""
import json, os, subprocess, sys
FPS = 30
src, out, cfg = sys.argv[1], sys.argv[2], json.load(open(sys.argv[3]))
def interp(keys, t):
    t = min(max(t, keys[0][0]), keys[-1][0])
    for a, b in zip(keys, keys[1:]):
        if a[0] <= t <= b[0]:
            k = (t - a[0]) / ((b[0] - a[0]) or 1); return [a[i] + (b[i] - a[i]) * k for i in range(1, 5)]
    return keys[-1][1:5]
def frames(keys):
    for n in range(round(keys[0][0] * FPS), round(keys[-1][0] * FPS) + 1): yield n, interp(keys, n / FPS)
rng = lambda n: f"{max(0.0, (n - .5) / FPS):.4f}-{(n + .5) / FPS:.4f}"  # frame 0 -> 0.0000 (a negative start broke the --blur parser)
args = []
for keys in cfg.get("boxes", []):
    for n, (x0, y0, x1, y1) in frames(keys): args += ["--blur", f"{rng(n)}:{int(x0)}:{int(y0)}:{int(x1)}:{min(int(y1), 1919)}"]
for seg in cfg.get("segments", []):
    th, K = seg.get("th", 62), seg.get("n", 5)
    for n, (xa, ya, xb, yb) in frames(seg["keys"]):
        for j in range(K):
            p0, p1 = j / K, (j + 1) / K
            x0, x1 = sorted((xa + (xb - xa) * p0, xa + (xb - xa) * p1)); y0, y1 = sorted((ya + (yb - ya) * p0, ya + (yb - ya) * p1))
            args += ["--blur", f"{rng(n)}:{max(0, int(x0 - th))}:{max(0, int(y0 - th / 2))}:{min(1079, int(x1 + th))}:{min(1919, int(y1 + th / 2))}"]
print(len(args) // 2, "blur boxes", flush=True)
cc = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline", "caption_clean.py")
subprocess.run(["python3", cc, src, out] + args, check=True)
