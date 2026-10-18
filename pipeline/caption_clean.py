"""Clean a clip taken from TikTok BEFORE new_reel.sh, without touching the framing or the order of the footage
(approved on the DPF #001 pilot, 18.10.2026): no crop, no zoom, PiP and original edit stay as they are.
  - removes a STATIC burned-in caption / sticker (old title text) by inpainting only its letters,
  - blurs licence plates inside given boxes for given time ranges.

usage: python3 caption_clean.py <src.mp4> <out.mp4> [--band 1500-1700] [--blur t0-t1:x0:y0:x1:y1 ...]
  --band y0-y1   vertical band (source px, 1080x1920) holding the static text; mask = pixels near-white in >=90%
                 of 40 samples + their consistently dark outline, dilated. Omit when the clip has no static text.
  --blur ...     soft blur box (feathered) on [t0, t1) seconds; repeat for each plate / time range.
Output: 30 fps CFR, libx264 crf 12, original audio (AAC 256k), same timing as the source. Check with a contact sheet."""
import argparse, subprocess
import cv2, numpy as np

ap = argparse.ArgumentParser(); ap.add_argument("src"); ap.add_argument("out")
ap.add_argument("--band", default=""); ap.add_argument("--blur", action="append", default=[])
a = ap.parse_args()
W, H, FPS = 1080, 1920, 30

mroi = None
if a.band:
    B0, B1 = map(int, a.band.split("-"))
    cap = cv2.VideoCapture(a.src); n_src = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); fps_src = cap.get(cv2.CAP_PROP_FPS) or 30
    white, dark = [], []
    for t in np.linspace(0.5, max(0.6, n_src / fps_src - 0.5), 40):
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
    print(f"caption mask bbox x {xs.min()}-{xs.max()} y {ys.min()}-{ys.max()}", flush=True)

BL = []
for b in a.blur:
    rng, x0, y0, x1, y1 = b.split(":"); t0, t1 = map(float, rng.split("-")); x0, y0, x1, y1 = map(int, (x0, y0, x1, y1))
    al = np.zeros((H, W), np.float32); cv2.rectangle(al, (x0, y0), (x1, y1), 1.0, -1); al = cv2.GaussianBlur(al, (0, 0), 9)[..., None]
    BL.append((t0, t1, al, (max(0, x0 - 40), max(0, y0 - 40), min(W, x1 + 40), min(H, y1 + 40))))

dec = subprocess.Popen(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", a.src, "-vf", f"fps={FPS},scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
enc = subprocess.Popen(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                        "-i", a.src, "-map", "0:v", "-map", "1:a?", "-c:v", "libx264", "-preset", "veryfast", "-crf", "12", "-pix_fmt", "yuv420p",
                        "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", a.out], stdin=subprocess.PIPE)
n = 0; FB = W * H * 3
while True:
    buf = dec.stdout.read(FB)
    if len(buf) < FB: break
    out = np.frombuffer(buf, np.uint8).reshape(H, W, 3).copy(); t = n / FPS
    if mroi is not None:
        roi = out[Y0:Y1, X0:X1]
        fixed = cv2.inpaint(roi, mroi, 7, cv2.INPAINT_TELEA).astype(np.float32)
        out[Y0:Y1, X0:X1] = (fixed * feather + roi.astype(np.float32) * (1 - feather)).astype(np.uint8)
    for t0, t1, al, (px0, py0, px1, py1) in BL:
        if t0 <= t < t1:
            reg = out[py0:py1, px0:px1].astype(np.float32); bl = cv2.GaussianBlur(reg, (0, 0), 14)
            aa = al[py0:py1, px0:px1]; out[py0:py1, px0:px1] = (bl * aa + reg * (1 - aa)).astype(np.uint8)
    enc.stdin.write(out.tobytes()); n += 1
enc.stdin.close(); enc.wait(); dec.wait()
print("CAPTION_CLEAN_OK frames", n)
