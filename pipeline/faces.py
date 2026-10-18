"""Where are the faces? (so graphics never cover the presenter or a PiP face)
usage (in a reel folder): python3 faces.py [step_s=0.25]
-> out/faces.json: [[t, [[x0, y0, x1, y1, score], ...]], ...] in 1080x1920 output coordinates (source time),
   and a 1-second summary printed: union of face boxes, padded up for hair (+30% of face height) and down for chin/neck.
Model: OpenCV YuNet (face_detection_yunet_2023mar.onnx in /home/claude/models/face/yunet.onnx; setup.sh downloads it)."""
import json, os, sys
import cv2, numpy as np

ROOT = os.environ.get("REEL_ROOT") or os.getcwd(); step = float(sys.argv[1]) if len(sys.argv) > 1 else 0.25
MODEL = os.environ.get("YUNET", "/home/claude/models/face/yunet.onnx")
import subprocess
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{ROOT}/src/cfr.mp4"], capture_output=True, text=True).stdout)
W, H = 360, 640; S = 1080 / W; THR = float(os.environ.get("FACE_THR", "0.85"))
det = cv2.FaceDetectorYN.create(MODEL, "", (W, H), THR, 0.3, 50)
p = subprocess.Popen(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", f"{ROOT}/src/cfr.mp4", "-vf", f"fps={1 / step},scale={W}:{H}",
                      "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
res = []; k = 0; FB = W * H * 3
while True:
    buf = p.stdout.read(FB)
    if len(buf) < FB: break
    f = np.frombuffer(buf, np.uint8).reshape(H, W, 3); _, faces = det.detect(f); fl = []
    for r in (faces if faces is not None else []):
        x, y, w, h = r[:4]; fl.append([int(x * S), int(y * S), int((x + w) * S), int((y + h) * S), round(float(r[-1]), 2)])
    res.append([round(k * step, 2), fl]); k += 1
p.wait(); n, fps = dur * 30, 30
json.dump(res, open(f"{ROOT}/out/faces.json", "w"))
# 1-second summary of no-go zones (face + hair + chin)
for s in range(int(np.ceil(n / fps))):
    bx = [b for tt, fl in res if s <= tt < s + 1 for b in fl]
    if not bx: print(f"{s:4d}s  -"); continue
    zs = []
    for b in bx:
        hh = b[3] - b[1]; zs.append([max(0, b[0] - 20), max(0, int(b[1] - .3 * hh)), min(1080, b[2] + 20), min(1920, int(b[3] + .12 * hh))])
    # cluster: big faces (main presenter) vs small (PiP)
    big = [z for z in zs if z[2] - z[0] > 260]; small = [z for z in zs if z[2] - z[0] <= 260]
    def uni(L): return [min(z[0] for z in L), min(z[1] for z in L), max(z[2] for z in L), max(z[3] for z in L)] if L else None
    print(f"{s:4d}s  face {uni(big)}  small {uni(small)}")
