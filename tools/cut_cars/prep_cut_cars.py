"""Sticker assets for the `cut` piece of the compositor ("Am tăiat prețurile", 11.11.2026): a car cut-out that is sliced in two.
python3 -I prep_cut_cars.py <reel folder> name=cutout.png [name=cutout.png ...]
For every car it writes assets/cars/<name>_w.png (whole), <name>_a.png (front piece), <name>_b.png (rear piece) on the same
canvas (same registration, so the two pieces laid over each other rebuild the whole car) and assets/cars/cars.json with the sizes.
Each image is a sticker: white outline + soft shadow. The cut is a straight line through the middle of the car, leaning ANG degrees."""
import json, os, sys
import cv2, numpy as np

CARW = 1360          # car width in the asset (2x of the 680 px it has on screen)
PAD = 76             # room for the outline and the shadow
BORDER, SHADOW, OFF = 15, 22, 12
ANG = 17.0           # lean of the cut from the vertical, degrees (top to the right)


def ground_clean(rgba, frac=0.075):
    """Floor shadow next to the tyres: in the lowest rows keep only what is as dark as rubber."""
    h = rgba.shape[0]; y0 = int(h * (1 - frac))
    lum = rgba[y0:, :, :3].astype(np.float32).mean(axis=2)
    keep = np.clip((84.0 - lum) / 18.0, 0, 1)
    rgba[y0:, :, 3] = (rgba[y0:, :, 3].astype(np.float32) * keep).astype(np.uint8)
    return rgba


def sticker(rgb, a):
    """rgb float 0..1, a float 0..1 on the final canvas -> RGBA uint8 with white outline and shadow."""
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * BORDER + 1, 2 * BORDER + 1))
    dil = cv2.dilate((a > 0.04).astype(np.uint8) * 255, k).astype(np.float32) / 255
    dil = cv2.GaussianBlur(dil, (0, 0), 1.2)
    sh = cv2.GaussianBlur(dil, (0, 0), SHADOW / 2)
    sh = cv2.warpAffine(sh, np.float32([[1, 0, 0], [0, 1, OFF]]), (sh.shape[1], sh.shape[0])) * 0.5
    C = np.zeros_like(rgb); A = sh.copy()
    C = 1.0 * dil[..., None] + C * (1 - dil[..., None]); A = dil + A * (1 - dil)
    C = rgb * a[..., None] + C * (1 - a[..., None]); A = a + A * (1 - a)
    out = np.where(A[..., None] > 1e-4, C / np.maximum(A[..., None], 1e-4), 0)
    return np.dstack([np.clip(out[..., ::-1] * 255, 0, 255), np.clip(A * 255, 0, 255)]).astype(np.uint8)  # BGR + A for cv2


def main():
    reel = sys.argv[1]; out_dir = f"{reel}/assets/cars"; os.makedirs(out_dir, exist_ok=True)
    meta_p = f"{out_dir}/cars.json"; meta = json.load(open(meta_p)) if os.path.exists(meta_p) else {}
    for arg in sys.argv[2:]:
        name, src = arg.split("=", 1)
        im = cv2.imread(src, cv2.IMREAD_UNCHANGED); assert im is not None and im.shape[2] == 4, src
        im = ground_clean(im)
        ys, xs = np.where(im[..., 3] > 8); im = im[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
        s = CARW / im.shape[1]; im = cv2.resize(im, (CARW, int(round(im.shape[0] * s))), interpolation=cv2.INTER_AREA)
        ch, cw = im.shape[0] + 2 * PAD, CARW + 2 * PAD
        rgb = np.zeros((ch, cw, 3), np.float32); a = np.zeros((ch, cw), np.float32)
        rgb[PAD:PAD + im.shape[0], PAD:PAD + CARW] = im[..., 2::-1].astype(np.float32) / 255   # RGB
        a[PAD:PAD + im.shape[0], PAD:PAD + CARW] = im[..., 3].astype(np.float32) / 255
        # cut line through the canvas centre; signed distance > 0 = rear piece (right of the line)
        yy, xx = np.mgrid[0:ch, 0:cw].astype(np.float32)
        th = np.deg2rad(ANG); nx, ny = np.cos(th), np.sin(th)            # normal of a line leaning ANG deg from the vertical
        dist = (xx - cw / 2) * nx + (yy - ch / 2) * ny
        mb = np.clip(dist + 0.5, 0, 1); ma = 1 - mb
        cv2.imwrite(f"{out_dir}/{name}_w.png", sticker(rgb, a))
        info = {"cw": cw, "ch": ch, "carw": CARW, "ang": ANG}
        for key, m in (("a", ma), ("b", mb)):
            pa = a * m; cv2.imwrite(f"{out_dir}/{name}_{key}.png", sticker(rgb, pa))
            w = pa.sum(); info[key + "x"] = round(float((pa * xx).sum() / w / cw * 100), 2); info[key + "y"] = round(float((pa * yy).sum() / w / ch * 100), 2)
        meta[name] = info
        print(name, info)
    json.dump(meta, open(meta_p, "w"), indent=1)


if __name__ == "__main__":
    main()
