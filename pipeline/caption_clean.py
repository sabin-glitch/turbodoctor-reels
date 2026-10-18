"""Clean a clip downloaded from TikTok before editing (run before new_reel.sh):
  - removes a STATIC burned-in caption / sticker (old title text) by inpainting only its letters,
  - optionally replaces time ranges with a crop window (e.g. to drop an old picture-in-picture), scaled to 1080x1920.

usage: python3 caption_clean.py <src.mp4> <out.mp4> --band 1500-1700 [--from 13.33] [--crop 0-13.33:0:350:680:1209 ...]
  --band y0-y1   vertical band (source px) that contains the static text; mask = pixels near-white in >=90% of samples
                 plus their consistently dark outline, dilated. Check the result with a contact sheet.
  --from t       inpaint only from t seconds on (default 0)
  --crop a-b:x:y:w:h   for t in [a, b): use this source window (keep 9:16), resized to 1080x1920 (no inpaint there)
Output: 30 fps CFR, libx264 crf 12, original audio (AAC 256k). Frame-accurate with the original timing."""
import argparse, subprocess
import cv2, numpy as np

ap = argparse.ArgumentParser(); ap.add_argument("src"); ap.add_argument("out")
ap.add_argument("--band", required=True); ap.add_argument("--from", dest="t_from", type=float, default=0.0)
ap.add_argument("--crop", action="append", default=[]); ap.add_argument("--fps", type=int, default=30)
a = ap.parse_args()
W, H, FPS = 1080, 1920, a.fps
B0, B1 = map(int, a.band.split("-"))
CROPS = []
for c in a.crop:
    rng, x, y, w, h = c.split(":"); t0, t1 = map(float, rng.split("-")); CROPS.append((t0, t1, int(x), int(y), int(w), int(h)))

# 1) static-text mask from ~40 samples
cap = cv2.VideoCapture(a.src); n_src = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); fps_src = cap.get(cv2.CAP_PROP_FPS) or 30
white, dark = [], []
for t in np.linspace(a.t_from + 0.5, n_src / fps_src - 0.5, 40):
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(t * fps_src)); ok, fr = cap.read()
    if not ok: continue
    if fr.shape[1] != W or fr.shape[0] != H: fr = cv2.resize(fr, (W, H))
    roi = fr[B0:B1]; white.append(roi.min(axis=2) > 200); dark.append(roi.max(axis=2) < 60)
core = (np.mean(white, 0) > 0.9).astype(np.uint8)
outl = ((np.mean(dark, 0) > 0.85).astype(np.uint8) & cv2.dilate(core, np.ones((15, 15), np.uint8)))
band = cv2.dilate(((core | outl) > 0).astype(np.uint8) * 255, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13)))
mask = np.zeros((H, W), np.uint8); mask[B0:B1] = band
if mask.sum() == 0: raise SystemExit("no static text found in the band")
ys, xs = np.where(mask > 0); X0, X1, Y0, Y1 = max(0, xs.min() - 14), min(W, xs.max() + 15), max(0, ys.min() - 14), min(H, ys.max() + 15)
mroi = mask[Y0:Y1, X0:X1]
feather = cv2.GaussianBlur(cv2.dilate(mroi, np.ones((5, 5), np.uint8)).astype(np.float32) / 255, (0, 0), 2.0)[..., None]
cv2.imwrite(a.out.rsplit(".", 1)[0] + "_mask.png", mask)
print(f"mask bbox x {xs.min()}-{xs.max()} y {ys.min()}-{ys.max()}", flush=True)

# 2) decode at FPS, clean, encode
dec = subprocess.Popen(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", a.src, "-vf", f"fps={FPS},scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
enc = subprocess.Popen(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                        "-i", a.src, "-map", "0:v", "-map", "1:a?", "-c:v", "libx264", "-preset", "veryfast", "-crf", "12", "-pix_fmt", "yuv420p",
                        "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", a.out], stdin=subprocess.PIPE)
n = 0; FB = W * H * 3
while True:
    buf = dec.stdout.read(FB)
    if len(buf) < FB: break
    fr = np.frombuffer(buf, np.uint8).reshape(H, W, 3); t = n / FPS
    crop = next((c for c in CROPS if c[0] <= t < c[1]), None)
    if crop:
        _, _, x, y, w, h = crop; out = cv2.resize(fr[y:y + h, x:x + w], (W, H), interpolation=cv2.INTER_LANCZOS4)
    elif t >= a.t_from:
        out = fr.copy(); roi = out[Y0:Y1, X0:X1]
        fixed = cv2.inpaint(roi, mroi, 7, cv2.INPAINT_TELEA).astype(np.float32)
        out[Y0:Y1, X0:X1] = (fixed * feather + roi.astype(np.float32) * (1 - feather)).astype(np.uint8)
    else:
        out = fr
    enc.stdin.write(out.tobytes()); n += 1
enc.stdin.close(); enc.wait(); dec.wait()
print("CAPTION_CLEAN_OK frames", n)
