"""Remove a TikTok watermark (logo + "TikTok" + @username) from src/cfr.mp4 -> src/clean.mp4 (30 fps, audio copied).

TikTok downloads carry the watermark in two places: phase 1 (left-middle, first ~3.5 s) and phase 2 (bottom-right,
rest of the video). Usage:
  python3 wm_remove.py --probe            # prints the frame where the bottom-right logo appears (= SWITCH)
  python3 wm_remove.py [SWITCH]           # builds the masks and writes src/clean.mp4
Defaults below match a 540x960 TikTok export; for other sizes adjust CROP1/CROP2 after looking at a contact sheet.

Mask = 10th percentile of a white top-hat over each phase: static bright glyphs survive, moving background does not.
The long phase gives a clean reference; its row bands (logo / "TikTok" / username) are template-matched into the
short phase, whose own top-hat is noisy. Logo gets a filled hull + wider dilation (its cyan/red fringes are not white).
"""
import os, sys, subprocess
import cv2, numpy as np

ROOT = os.environ.get("REEL_ROOT") or os.path.dirname(os.path.abspath(__file__))
SRC, DST = f"{ROOT}/src/cfr.mp4", f"{ROOT}/src/clean.mp4"
CROP1 = (400, 560, 0, 240)      # y0, y1, x0, x1 of the phase-1 search area (left-middle)
CROP2 = (690, 840, 330, 540)    # phase-2 search area (bottom-right)
LOGO2 = (728, 762, 484, 512)    # bottom-right logo box used by --probe
TH = 45                         # top-hat threshold for the reference mask

cap = cv2.VideoCapture(SRC); W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)); H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
N = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

if len(sys.argv) > 1 and sys.argv[1] == "--probe":
    y0, y1, x0, x1 = LOGO2; prev = None
    for i in range(min(N, 600)):
        ok, f = cap.read()
        if not ok: break
        v = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)[y0:y1, x0:x1].mean()
        if prev is not None and v - prev > 25: print("SWITCH", i, f"({i / 30:.2f}s)"); break
        prev = v
    else: print("no jump found in first 20 s (watermark may be bottom-right only: use SWITCH=0)")
    sys.exit()

SWITCH = int(sys.argv[1]) if len(sys.argv) > 1 else 105
k45 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (45, 45))
P1, P2 = [], []; i = 0
while True:
    ok, f = cap.read()
    if not ok: break
    g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
    if i < SWITCH - 1: P1.append(cv2.morphologyEx(g[CROP1[0]:CROP1[1], CROP1[2]:CROP1[3]], cv2.MORPH_TOPHAT, k45))
    elif i > SWITCH + 1 and i % 4 == 0: P2.append(cv2.morphologyEx(g[CROP2[0]:CROP2[1], CROP2[2]:CROP2[3]], cv2.MORPH_TOPHAT, k45))
    i += 1
m2 = np.percentile(np.stack(P2), 10, axis=0)
b2 = (m2 > TH).astype(np.uint8)
rows = np.where(b2.any(1))[0]
bands, start = [], rows[0]
for a, b in zip(rows[:-1], rows[1:]):
    if b - a > 3: bands.append((start, a + 1)); start = b
bands.append((start, rows[-1] + 1))
print("bands (rows in CROP2):", bands)
full2 = np.zeros((H, W), np.uint8); full2[CROP2[0]:CROP2[1], CROP2[2]:CROP2[3]] = b2
full1 = np.zeros((H, W), np.uint8)
if P1:
    m1 = np.percentile(np.stack(P1), 10, axis=0).astype(np.float32)
    for a, b in bands:
        blk = b2[a:b]; xs = np.where(blk.any(0))[0]; tpl = blk[:, xs.min():xs.max() + 1].astype(np.float32) * 255
        r = cv2.matchTemplate(m1, tpl, cv2.TM_CCORR_NORMED); _, sc, _, loc = cv2.minMaxLoc(r)
        print(f"band {a}-{b}: match {sc:.2f} at {loc}")
        full1[CROP1[0] + loc[1]:CROP1[0] + loc[1] + (b - a), CROP1[2] + loc[0]:CROP1[2] + loc[0] + tpl.shape[1]] |= (tpl > 0).astype(np.uint8)
k7 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)); k13 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13))


def build(full):
    if not full.any(): return full
    ys = np.where(full.any(1))[0]; l0, l1 = ys.min(), ys.min() + (bands[0][1] - bands[0][0]) + 2
    text = full.copy(); text[l0:l1] = 0; logo = np.zeros_like(full); logo[l0:l1] = full[l0:l1]
    hull = cv2.convexHull(np.vstack(cv2.findContours(logo, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]))
    lf = np.zeros_like(full); cv2.fillConvexPoly(lf, hull, 1)
    return np.maximum(cv2.dilate(text, k7), cv2.dilate(lf, k13)) * 255


M1, M2 = build(full1), build(full2)
cv2.imwrite(f"{ROOT}/frames/wm_mask1.png", M1); cv2.imwrite(f"{ROOT}/frames/wm_mask2.png", M2)
cap = cv2.VideoCapture(SRC)
ff = subprocess.Popen(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                       "-i", SRC, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "11", "-pix_fmt", "yuv420p",
                       "-c:a", "copy", DST], stdin=subprocess.PIPE)
i = 0
while True:
    ok, f = cap.read()
    if not ok: break
    m = M1 if i < SWITCH else M2
    if SWITCH - 2 <= i <= SWITCH + 1: m = cv2.bitwise_or(M1, M2)
    if m.any():
        ys, xs = np.where(m); y0, y1, x0, x1 = max(0, ys.min() - 12), min(H, ys.max() + 13), max(0, xs.min() - 12), min(W, xs.max() + 13)
        roi, mr = f[y0:y1, x0:x1], m[y0:y1, x0:x1]
        fixed = cv2.inpaint(roi, mr, 6, cv2.INPAINT_TELEA)
        soft = cv2.GaussianBlur(fixed, (5, 5), 0); a = (cv2.GaussianBlur(mr, (7, 7), 0) / 255.0)[..., None]
        f[y0:y1, x0:x1] = (fixed * (1 - a * .6) + soft * (a * .6)).astype(np.uint8)
    ff.stdin.write(f.tobytes()); i += 1
ff.stdin.close(); ff.wait(); print("frames", i, "->", DST)
