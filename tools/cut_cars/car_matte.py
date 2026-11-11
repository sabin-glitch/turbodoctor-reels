"""Cut a generated studio car photo (white background) out of its background -> RGBA PNG trimmed to the car.
python3 -I car_matte.py <in.png> <out.png>
ISNet (isnet-general-use.onnx) finds the car; the edge alpha comes from the real pixels (how white they are), so edges stay sharp."""
import sys
import cv2, numpy as np, onnxruntime as ort

src, dst = sys.argv[1], sys.argv[2]
im = cv2.imread(src, cv2.IMREAD_COLOR)
H, W = im.shape[:2]
sess = ort.InferenceSession("/home/claude/models/matting/isnet-general-use.onnx", providers=["CPUExecutionProvider"])
x = cv2.resize(cv2.cvtColor(im, cv2.COLOR_BGR2RGB), (1024, 1024), interpolation=cv2.INTER_AREA).astype(np.float32) / 255.0
x = ((x - 0.5) / 1.0).transpose(2, 0, 1)[None]
m = sess.run(None, {sess.get_inputs()[0].name: x})[0][0, 0]
m = (m - m.min()) / (m.max() - m.min() + 1e-8)
m = cv2.resize(m, (W, H), interpolation=cv2.INTER_CUBIC)
fg = (m > 0.5).astype(np.uint8)
# keep the largest component (the car), fill holes smaller than a window
n, lab, st, _ = cv2.connectedComponentsWithStats(fg, 8)
if n > 1: fg = (lab == 1 + np.argmax(st[1:, cv2.CC_STAT_AREA])).astype(np.uint8)
# whiteness of each pixel: 1 = pure background white
mn = im.min(axis=2).astype(np.float32); mx = im.max(axis=2).astype(np.float32)
white = np.clip((mn - 226.0) / 24.0, 0, 1) * np.clip(1 - (mx - mn) / 14.0, 0, 1)
# background = near-white pixels connected to the image border, never deeper than BAND px inside the ISNet car mask
BAND = 9
k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * BAND + 1, 2 * BAND + 1))
core = cv2.erode(fg, k)                       # surely car
cand = ((white > 0.25) & (core == 0)).astype(np.uint8)
ff = cand.copy(); mask = np.zeros((H + 2, W + 2), np.uint8)
border = np.zeros_like(cand); border[0, :] = border[-1, :] = border[:, 0] = border[:, -1] = 1
n, lab = cv2.connectedComponents(cand, connectivity=4)
ids = np.unique(lab[(border == 1) & (cand == 1)])
bg = np.isin(lab, ids[ids > 0])
outer = cv2.dilate(fg, k)                     # anything outside this is background whatever its colour (floor shadow)
alpha = np.ones((H, W), np.float32)
alpha[bg] = 1 - white[bg]
alpha[outer == 0] = 0
# floor shadow inside the band: grey, colourless, below the car's lowest dark pixels -> fade it out with the ISNet mask
soft = np.clip((m - 0.35) / 0.3, 0, 1)
grey = (mx - mn < 18) & (mn > 95) & (core == 0)
alpha[grey] = np.minimum(alpha[grey], soft[grey])
alpha = cv2.GaussianBlur(alpha, (0, 0), 0.6)
# un-mix the white background from edge pixels
a3 = np.maximum(alpha, 1e-3)[..., None]
col = np.clip((im.astype(np.float32) - (1 - alpha[..., None]) * 255.0) / a3, 0, 255)
ys, xs = np.where(alpha > 0.02)
y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
out = np.dstack([col, alpha * 255]).astype(np.uint8)[y0:y1, x0:x1]
cv2.imwrite(dst, out)
print(dst, out.shape, "aspect", round(out.shape[1] / out.shape[0], 3))
