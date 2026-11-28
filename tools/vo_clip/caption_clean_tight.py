"""Scoate un titlu vechi ars în imagine (text static, fără contur), cu o mască strânsă pe litere, la rezoluția sursei.
Completează pipeline/caption_clean.py: acela lucrează la 1080x1920 și își lărgește mult masca (bun pentru text alb cu contur negru);
pe un text subțire, fără contur, masca lată lasă pete pe muchiile pieselor. Aici masca e textul + câțiva pixeli, iar cadrul nu e redimensionat.

  python3 caption_clean_tight.py <src> <out.mp4> --box x0,y0,x1,y1 [--color white|red] [--ref t] [--grow 2] [--radius 4]
    --box     dreptunghiul (în pixelii sursei) în care stă textul
    --color   white: literele = pixelii aproape albi în >= 90 % din 60 de cadre (textul stă pe loc, imaginea se mișcă)
              red:   la fel, pentru text roșu
    --ref t   în plus, un moment în care în spatele textului e negru complet (ex. primul cadru al unui montaj cu fundal negru):
              tot ce nu e negru în `box` la acel moment e text, inclusiv marginea lui netezită
    --grow    cu câți pixeli se lărgește masca (implicit 2)
    --radius  raza de inpainting (Telea, implicit 4)
Ieșire: aceeași rezoluție, 30 fps, libx264 crf 10, sunetul sursei. Scrie și <out>_mask.png. Fără crop, fără zoom, cadrele rămân în ordine."""
import argparse, subprocess
import cv2, numpy as np

ap = argparse.ArgumentParser(); ap.add_argument("src"); ap.add_argument("out"); ap.add_argument("--box", required=True)
ap.add_argument("--color", default="white"); ap.add_argument("--ref", type=float, default=None)
ap.add_argument("--grow", type=int, default=2); ap.add_argument("--radius", type=int, default=4)
a = ap.parse_args()
X0, Y0, X1, Y1 = map(int, a.box.split(","))
cap = cv2.VideoCapture(a.src); W, H = int(cap.get(3)), int(cap.get(4)); n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); fps = cap.get(cv2.CAP_PROP_FPS) or 30


def textlike(roi):
    b, g, r = [roi[..., i].astype(np.int16) for i in range(3)]
    if a.color == "red": return (r > 150) & (g < 125) & (b < 135) & (r - np.maximum(g, b) > 70)
    return roi.min(axis=2) > 205


acc = []
for t in np.linspace(0.3, max(0.4, n / fps - 0.3), 60):
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(t * fps)); ok, fr = cap.read()
    if ok: acc.append(textlike(fr[Y0:Y1, X0:X1]))
core = (np.mean(acc, 0) > 0.9).astype(np.uint8)
if a.ref is not None:
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(a.ref * fps)); ok, fr = cap.read()
    core |= (fr[Y0:Y1, X0:X1].max(axis=2) > 40).astype(np.uint8)
if core.sum() == 0: raise SystemExit("nu am găsit text în box")
k = 2 * a.grow + 1
m = cv2.dilate(core * 255, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)))
ys, xs = np.where(m > 0); pad = a.radius + 6
rx0, rx1, ry0, ry1 = max(0, X0 + xs.min() - pad), min(W, X0 + xs.max() + pad + 1), max(0, Y0 + ys.min() - pad), min(H, Y0 + ys.max() + pad + 1)
mask = np.zeros((H, W), np.uint8); mask[Y0:Y1, X0:X1] = m; mroi = mask[ry0:ry1, rx0:rx1]
feather = cv2.GaussianBlur(cv2.dilate(mroi, np.ones((3, 3), np.uint8)).astype(np.float32) / 255, (0, 0), 1.0)[..., None]
cv2.imwrite(a.out.rsplit(".", 1)[0] + "_mask.png", mask)
print(f"text mask: {int((mask > 0).sum())} px, bbox x {X0 + xs.min()}-{X0 + xs.max()} y {Y0 + ys.min()}-{Y0 + ys.max()} (sursă {W}x{H})", flush=True)

dec = subprocess.Popen(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", a.src, "-vf", "fps=30", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
enc = subprocess.Popen(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                        "-i", a.src, "-map", "0:v", "-map", "1:a?", "-c:v", "libx264", "-preset", "veryfast", "-crf", "10", "-pix_fmt", "yuv420p",
                        "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", a.out], stdin=subprocess.PIPE)
i = 0; FB = W * H * 3
while True:
    buf = dec.stdout.read(FB)
    if len(buf) < FB: break
    fr = np.frombuffer(buf, np.uint8).reshape(H, W, 3).copy(); roi = fr[ry0:ry1, rx0:rx1]
    fixed = cv2.inpaint(roi, mroi, a.radius, cv2.INPAINT_TELEA).astype(np.float32)
    fr[ry0:ry1, rx0:rx1] = (fixed * feather + roi.astype(np.float32) * (1 - feather)).astype(np.uint8)
    enc.stdin.write(fr.tobytes()); i += 1
enc.stdin.close(); enc.wait(); dec.wait()
print("CAPTION_CLEAN_TIGHT_OK frames", i)
