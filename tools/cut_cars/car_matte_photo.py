"""Cut a car out of a real photo (street, parking lot...) -> RGBA PNG trimmed to the car, for prep_cut_cars.py.
python3 -I car_matte_photo.py <in.jpg> <out.png> [--crop x0,y0,x1,y1] [--flip] [--shrink px] [--ground frac] [--hold x0,y0,x1,y1 ...]
ISNet (isnet-general-use.onnx) finds the car, GrabCut snaps the mask to the real edges (trimap from the ISNet map),
the edge is pulled in by --shrink px so no background fringe is left under the white sticker outline.
--crop: part of the photo that holds the car (fractions 0..1), so the model does not pick another object.
--flip: mirror the car (all stickers face left: the name plate sits over the bonnet).
--ground: in the lowest `frac` of the car's height keep only pixels as dark as rubber (the floor shadow between and beside the tyres).
--hold: rectangles (fractions of the crop) that are surely car, when GrabCut eats a window or a pale panel."""
import argparse
import cv2, numpy as np, onnxruntime as ort

ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("dst")
ap.add_argument("--crop", default=""); ap.add_argument("--flip", action="store_true")
ap.add_argument("--shrink", type=float, default=1.5); ap.add_argument("--ground", type=float, default=0.0)
ap.add_argument("--hold", nargs="*", default=[]); ap.add_argument("--work", type=int, default=2200)
ap.add_argument("--no-grabcut", action="store_true")
a = ap.parse_args()

im = cv2.imread(a.src, cv2.IMREAD_COLOR); assert im is not None, a.src
if a.crop:
    x0, y0, x1, y1 = [float(v) for v in a.crop.split(",")]; H, W = im.shape[:2]
    im = im[int(y0 * H):int(y1 * H), int(x0 * W):int(x1 * W)]
H, W = im.shape[:2]
s = min(1.0, a.work / max(H, W))
if s < 1: im = cv2.resize(im, (int(round(W * s)), int(round(H * s))), interpolation=cv2.INTER_AREA); H, W = im.shape[:2]

sess = ort.InferenceSession("/home/claude/models/matting/isnet-general-use.onnx", providers=["CPUExecutionProvider"])
x = cv2.resize(cv2.cvtColor(im, cv2.COLOR_BGR2RGB), (1024, 1024), interpolation=cv2.INTER_AREA).astype(np.float32) / 255.0
x = (x - 0.5).transpose(2, 0, 1)[None]
m = sess.run(None, {sess.get_inputs()[0].name: x})[0][0, 0]
m = (m - m.min()) / (m.max() - m.min() + 1e-8)
m = cv2.resize(m, (W, H), interpolation=cv2.INTER_CUBIC)


def largest(b):
    n, lab, st, _ = cv2.connectedComponentsWithStats(b.astype(np.uint8), 8)
    return (lab == 1 + np.argmax(st[1:, cv2.CC_STAT_AREA])) if n > 1 else b.astype(bool)


fg = largest(m > 0.5)
hold = np.zeros((H, W), bool)
for r in a.hold:
    hx0, hy0, hx1, hy1 = [float(v) for v in r.split(",")]; hold[int(hy0 * H):int(hy1 * H), int(hx0 * W):int(hx1 * W)] = True
if a.no_grabcut:
    res = fg | hold
else:
    k = lambda r: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
    band = max(6, int(round(W / 170)))
    sure_fg = cv2.erode(((m > 0.85) & fg).astype(np.uint8), k(band)).astype(bool) | hold
    sure_bg = ~cv2.dilate(((m > 0.15) | fg).astype(np.uint8), k(band)).astype(bool)
    gc = np.where(fg, cv2.GC_PR_FGD, cv2.GC_PR_BGD).astype(np.uint8)
    gc[sure_fg] = cv2.GC_FGD; gc[sure_bg] = cv2.GC_BGD
    bgd = np.zeros((1, 65), np.float64); fgd = np.zeros((1, 65), np.float64)
    cv2.grabCut(im, gc, None, bgd, fgd, 4, cv2.GC_INIT_WITH_MASK)
    res = largest((gc == cv2.GC_FGD) | (gc == cv2.GC_PR_FGD))
    # holes inside the car (windows seen through, wheel gaps) stay car
    inv = (~res).astype(np.uint8); n, lab = cv2.connectedComponents(inv, connectivity=4)
    border = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
    res = res | ((inv == 1) & ~np.isin(lab, border) & (m > 0.3))
alpha = res.astype(np.float32)
if a.shrink > 0:
    r = int(np.ceil(a.shrink)); alpha = cv2.erode(alpha, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1)))
alpha = cv2.GaussianBlur(alpha, (0, 0), 1.0)
ys, xs = np.where(alpha > 0.03); y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
out = np.dstack([im, (alpha * 255).astype(np.uint8)])[y0:y1, x0:x1]
if a.ground > 0:
    h = out.shape[0]; g0 = int(h * (1 - a.ground)); lum = out[g0:, :, :3].astype(np.float32).mean(axis=2)
    out[g0:, :, 3] = (out[g0:, :, 3].astype(np.float32) * np.clip((84.0 - lum) / 18.0, 0, 1)).astype(np.uint8)
if a.flip: out = np.ascontiguousarray(out[:, ::-1])
cv2.imwrite(a.dst, out)
print(a.dst, out.shape, "aspect", round(out.shape[1] / out.shape[0], 3))
