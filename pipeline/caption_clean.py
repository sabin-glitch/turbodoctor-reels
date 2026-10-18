"""Clean a clip taken from TikTok BEFORE new_reel.sh, without touching the framing or the order of the footage
(approved on the DPF #001 pilot, 18.10.2026): no crop, no zoom, PiP and original edit stay as they are.
  - removes a STATIC burned-in caption / sticker (old title text) by inpainting only its letters,
  - blurs licence plates inside given boxes for given time ranges.

usage: python3 caption_clean.py <src.mp4> <out.mp4> [--band 1500-1700[@t0-t1] ...] [--blur t0-t1:x0:y0:x1:y1 ...]
  --band y0-y1   vertical band (source px, 1080x1920) holding the static text; mask = pixels near-white in >=90%
                 of 40 samples + their consistently dark outline, dilated. Omit when the clip has no static text.
                 Optional @t0-t1: the text is on screen only in that time range (mask sampled and applied only there).
                 Repeat --band for several texts.
  --dynbox B,G,R,tol@y0-y1[@t0-t1]   word-by-word burned captions on a solid coloured box (TikTok auto-captions):
                 the box is found in every frame (pixels within tol of the BGR colour, inside the band), and its rectangle
                 (box + white text) is inpainted (Navier-Stokes). Clean on clothing/walls; hands passing behind smear a bit.
  --txtbox y0-y1[@t0-t1]   burned caption boxes on a FIXED line (y0-y1 = the box rows) whose colour also occurs in the
                 footage (e.g. teal box over teal scrubs): the white letters inside the line give the box's x-extent each
                 frame; that rectangle is inpainted (Navier-Stokes), or with @fill=B,G,R painted as a solid rounded box
                 (our dark caption box: our captions are then placed on it with reel.js capTop).
  --dyntext y0-y1[@t0-t1][@thr]   word-by-word burned captions WITHOUT a box (plain white text): per frame, near-white
                 pixels (min channel > thr, default 222) in the band are taken as letters, dilated (anti-aliasing + shadow) and
                 inpainted (Telea). Works best when our own captions sit on the same line afterwards (reel.js capTop).
  --rect x0:y0:x1:y1[@t0-t1]   fixed rectangle inpainted every frame (e.g. a TikTok reply bubble over a plain car ceiling or wall);
                 only for low-texture backgrounds - check the result on a contact sheet.
  --blur ...     soft blur box (feathered) on [t0, t1) seconds; repeat for each plate / time range.
Output: 30 fps CFR, libx264 crf 12, original audio (AAC 256k), same timing as the source. Check with a contact sheet."""
import argparse, subprocess
import cv2, numpy as np

ap = argparse.ArgumentParser(); ap.add_argument("src"); ap.add_argument("out")
ap.add_argument("--band", action="append", default=[]); ap.add_argument("--blur", action="append", default=[]); ap.add_argument("--dynbox", action="append", default=[]); ap.add_argument("--dyntext", action="append", default=[]); ap.add_argument("--txtbox", action="append", default=[]); ap.add_argument("--rect", action="append", default=[])
a = ap.parse_args()
W, H, FPS = 1080, 1920, 30

BANDS = []   # (t0, t1, X0, Y0, X1, Y1, mroi, feather)
for bi, bspec in enumerate(a.band):
    yr, _, tr = bspec.partition("@"); B0, B1 = map(int, yr.split("-"))
    cap = cv2.VideoCapture(a.src); n_src = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); fps_src = cap.get(cv2.CAP_PROP_FPS) or 30
    dur = n_src / fps_src; T0, T1 = (map(float, tr.split("-")) if tr else (0.0, 1e9)); T1 = min(T1, dur)
    lo, hi = (T0 + 0.1, T1 - 0.1) if tr else (0.5, max(0.6, dur - 0.5))
    white, dark = [], []
    for t in np.linspace(lo, max(lo + 0.05, hi), 40):
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(t * fps_src)); ok, fr = cap.read()
        if not ok: continue
        if fr.shape[1] != W or fr.shape[0] != H: fr = cv2.resize(fr, (W, H))
        roi = fr[B0:B1]; white.append(roi.min(axis=2) > 200); dark.append(roi.max(axis=2) < 60)
    core = (np.mean(white, 0) > 0.9).astype(np.uint8)
    outl = ((np.mean(dark, 0) > 0.85).astype(np.uint8) & cv2.dilate(core, np.ones((15, 15), np.uint8)))
    band = cv2.dilate(((core | outl) > 0).astype(np.uint8) * 255, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13)))
    mask = np.zeros((H, W), np.uint8); mask[B0:B1] = band
    if mask.sum() == 0: raise SystemExit(f"no static text found in band {bspec}")
    ys, xs = np.where(mask > 0); X0, X1, Y0, Y1 = max(0, xs.min() - 14), min(W, xs.max() + 15), max(0, ys.min() - 14), min(H, ys.max() + 15)
    mroi = mask[Y0:Y1, X0:X1]
    feather = cv2.GaussianBlur(cv2.dilate(mroi, np.ones((5, 5), np.uint8)).astype(np.float32) / 255, (0, 0), 2.0)[..., None]
    cv2.imwrite(a.out.rsplit(".", 1)[0] + f"_mask{bi}.png", mask)
    BANDS.append((T0, T1, X0, Y0, X1, Y1, mroi, feather))
    print(f"caption mask {bi}: bbox x {xs.min()}-{xs.max()} y {ys.min()}-{ys.max()} t {T0:.2f}-{min(T1, dur):.2f}", flush=True)

DYN = []   # (bgr, tol, y0, y1, t0, t1)
for d in a.dynbox:
    parts = d.split("@"); col = list(map(int, parts[0].split(",")))
    y0, y1 = map(int, parts[1].split("-")); t0, t1 = (map(float, parts[2].split("-")) if len(parts) > 2 else (0.0, 1e9))
    DYN.append((np.array(col[:3], np.int16), col[3] if len(col) > 3 else 45, y0, y1, t0, t1))

DTX = []   # (y0, y1, t0, t1, thr)
for d in a.dyntext:
    parts = d.split("@"); y0, y1 = map(int, parts[0].split("-")); t0, t1, thr = 0.0, 1e9, 222
    for q in parts[1:]:
        if "-" in q: t0, t1 = map(float, q.split("-"))
        else: thr = int(q)
    DTX.append((y0, y1, t0, t1, thr))
TXB = []   # (y0, y1, t0, t1)
for d in a.txtbox:
    parts = d.split("@"); y0, y1 = map(int, parts[0].split("-")); t0, t1, fill = 0.0, 1e9, None
    for q in parts[1:]:
        if q.startswith("fill="): fill = tuple(map(int, q[5:].split(",")))
        else: t0, t1 = map(float, q.split("-"))
    TXB.append((y0, y1, t0, t1, fill))
def _txb_extent(strip):
    m = (strip.min(axis=2) > 200).astype(np.uint8); hh = strip.shape[0]
    nc, lab, st, _ = cv2.connectedComponentsWithStats(m)
    ok = [k for k in range(1, nc) if st[k, 4] >= 15 and st[k, 3] < hh - 2 and st[k, 1] > 0 and st[k, 1] + st[k, 3] < hh and st[k, 2] < 120]
    if len(ok) < 2: return None
    return (min(st[k, 0] for k in ok), max(st[k, 0] + st[k, 2] for k in ok))
TXB_EXT = {}   # per txtbox spec index -> list of (x0, x1) or None per output frame (30 fps)
for ti, (y0, y1, t0, t1, fill) in enumerate(TXB):
    pp = subprocess.Popen(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", a.src, "-vf", f"fps={FPS},scale={W}:{H},crop={W}:{y1 - y0 - 16}:0:{y0 + 8}",
                           "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
    ext = []; FBs = W * (y1 - y0 - 16) * 3
    while True:
        b = pp.stdout.read(FBs)
        if len(b) < FBs: break
        ext.append(_txb_extent(np.frombuffer(b, np.uint8).reshape(y1 - y0 - 16, W, 3)))
    pp.wait()
    sm = list(ext); R = 7   # fades: borrow the extent of the nearest detected frame (both sides -> union)
    for i, e in enumerate(ext):
        if e is not None: continue
        bk = next((ext[j] for j in range(i - 1, max(-1, i - R - 1), -1) if ext[j] is not None), None)
        fw = next((ext[j] for j in range(i + 1, min(len(ext), i + R + 1)) if ext[j] is not None), None)
        if bk and fw: sm[i] = (min(bk[0], fw[0]), max(bk[1], fw[1]))
        else: sm[i] = bk or fw
    TXB_EXT[ti] = sm
    print(f"txtbox {ti}: detected {sum(e is not None for e in ext)}/{len(ext)} frames, painted {sum(e is not None for e in sm)}", flush=True)
RECT = []   # (x0, y0, x1, y1, t0, t1, mask, feather)
for d in a.rect:
    parts = d.split("@"); x0, y0, x1, y1 = map(int, parts[0].split(":")); t0, t1 = (map(float, parts[1].split("-")) if len(parts) > 1 else (0.0, 1e9))
    P = 30; cx0, cy0, cx1, cy1 = max(0, x0 - P), max(0, y0 - P), min(W, x1 + P), min(H, y1 + P)
    mk = np.zeros((cy1 - cy0, cx1 - cx0), np.uint8); mk[y0 - cy0:y1 - cy0, x0 - cx0:x1 - cx0] = 255
    fe = cv2.GaussianBlur(cv2.dilate(mk, np.ones((9, 9), np.uint8)).astype(np.float32) / 255, (0, 0), 3)[..., None]
    RECT.append((cx0, cy0, cx1, cy1, t0, t1, mk, fe))
K5 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (23, 23))   # letters + their soft shadow

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
    for T0, T1, X0, Y0, X1, Y1, mroi, feather in BANDS:
        if not (T0 <= t < T1): continue
        roi = out[Y0:Y1, X0:X1]
        fixed = cv2.inpaint(roi, mroi, 7, cv2.INPAINT_TELEA).astype(np.float32)
        out[Y0:Y1, X0:X1] = (fixed * feather + roi.astype(np.float32) * (1 - feather)).astype(np.uint8)
    for col, tol, y0, y1, t0, t1 in DYN:
        if not (t0 <= t < t1): continue
        band = out[y0:y1].astype(np.int16); m = (np.abs(band - col).max(axis=2) < tol).astype(np.uint8)
        nc, lab, st, _ = cv2.connectedComponentsWithStats(m)
        if nc < 2: continue
        k = 1 + int(np.argmax(st[1:, 4]))
        if st[k, 4] < 600: continue
        bx, by, bw, bh = st[k, :4]; bx0, by0, bx1, by1 = max(0, bx - 7), max(0, y0 + by - 7), min(W, bx + bw + 7), min(H, y0 + by + bh + 7)
        cx0, cy0, cx1, cy1 = max(0, bx0 - 24), max(0, by0 - 24), min(W, bx1 + 24), min(H, by1 + 24)
        crop = out[cy0:cy1, cx0:cx1]; mk = np.zeros(crop.shape[:2], np.uint8); mk[by0 - cy0:by1 - cy0, bx0 - cx0:bx1 - cx0] = 255
        out[cy0:cy1, cx0:cx1] = cv2.inpaint(crop, mk, 9, cv2.INPAINT_NS)
    for cx0, cy0, cx1, cy1, t0, t1, mk, fe in RECT:
        if not (t0 <= t < t1): continue
        crop = out[cy0:cy1, cx0:cx1]; sm = cv2.resize(crop, None, fx=.5, fy=.5, interpolation=cv2.INTER_AREA)
        fx = cv2.resize(cv2.inpaint(sm, cv2.resize(mk, (sm.shape[1], sm.shape[0]), interpolation=cv2.INTER_NEAREST), 6, cv2.INPAINT_TELEA), (crop.shape[1], crop.shape[0]), interpolation=cv2.INTER_CUBIC)
        out[cy0:cy1, cx0:cx1] = (fx.astype(np.float32) * fe + crop.astype(np.float32) * (1 - fe)).astype(np.uint8)
    for ti, (y0, y1, t0, t1, fill) in enumerate(TXB):
        if not (t0 <= t < t1): continue
        e = TXB_EXT[ti][n] if n < len(TXB_EXT[ti]) else None
        if e is None: continue   # no caption on this frame
        xs0, xs1 = e
        bx0, bx1 = max(0, xs0 - 30), min(W, xs1 + 30); by0, by1 = max(0, y0 - 4), min(H, y1 + 4)
        cx0, cy0, cx1, cy1 = max(0, bx0 - 24), max(0, by0 - 24), min(W, bx1 + 24), min(H, by1 + 24)
        if fill is not None:   # solid rounded box (radius 16) in our colour, slightly larger than the old one
            r = 16; x0f, y0f, x1f, y1f = bx0 - 6, by0 - 4, bx1 + 6, by1 + 4
            cv2.rectangle(out, (x0f + r, y0f), (x1f - r, y1f), fill, -1); cv2.rectangle(out, (x0f, y0f + r), (x1f, y1f - r), fill, -1)
            for cx, cy in ((x0f + r, y0f + r), (x1f - r, y0f + r), (x0f + r, y1f - r), (x1f - r, y1f - r)): cv2.circle(out, (cx, cy), r, fill, -1, cv2.LINE_AA)
            continue
        crop = out[cy0:cy1, cx0:cx1]; mk = np.zeros(crop.shape[:2], np.uint8); mk[by0 - cy0:by1 - cy0, bx0 - cx0:bx1 - cx0] = 255
        out[cy0:cy1, cx0:cx1] = cv2.inpaint(crop, mk, 9, cv2.INPAINT_NS)
    for y0, y1, t0, t1, thr in DTX:
        if not (t0 <= t < t1): continue
        band = out[y0:y1]; m = (band.min(axis=2) > thr).astype(np.uint8)
        nc, lab, st, _ = cv2.connectedComponentsWithStats(m)
        keep = np.zeros(nc, np.uint8); keep[1:] = (st[1:, 4] >= 12) & (st[1:, 3] <= 90)   # letters: not specks, not tall bright objects
        m = keep[lab] * 255
        if m.sum() == 0: continue
        m = cv2.dilate(m.astype(np.uint8), K5); ys, xs = np.where(m > 0)
        cx0, cy0, cx1, cy1 = max(0, xs.min() - 20), max(0, ys.min() - 20), min(W, xs.max() + 21), min(y1 - y0, ys.max() + 21)
        crop = out[y0 + cy0:y0 + cy1, cx0:cx1]
        out[y0 + cy0:y0 + cy1, cx0:cx1] = cv2.inpaint(crop, m[cy0:cy1, cx0:cx1], 7, cv2.INPAINT_TELEA)
    for t0, t1, al, (px0, py0, px1, py1) in BL:
        if t0 <= t < t1:
            reg = out[py0:py1, px0:px1].astype(np.float32); bl = cv2.GaussianBlur(reg, (0, 0), 14)
            aa = al[py0:py1, px0:px1]; out[py0:py1, px0:px1] = (bl * aa + reg * (1 - aa)).astype(np.uint8)
    enc.stdin.write(out.tobytes()); n += 1
enc.stdin.close(); enc.wait(); dec.wait()
print("CAPTION_CLEAN_OK frames", n)
