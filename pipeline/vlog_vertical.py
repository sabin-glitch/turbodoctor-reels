# 16:9 vlog segment -> 1080x1920 vertical: the whole frame at full width from y=Y (868 on the senzor/regulator vlog), background = the same frame blurred and darkened.
# usage: vlog_vertical.py <vlog.mp4> <out.mp4> T0 T1 Y [masks...]
# Masks: "t0-t1:x0,y0,x1,y1" (source px) inpainted inside a padded ROI;
# "t0-t1:x0,y0,x1,y1@tref" fills the box from a clean frame of the same shot (tref), aligned by phase correlation, feathered;
# "...@tref#cx0,cy0,cx1,cy1" sets the correlation region (default: strip below the box; use one above it for bottom labels)
import cv2, numpy as np, subprocess, sys
src, out, T0, T1, Y = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5])
MS = []
for m in sys.argv[6:]:
    tr, bx = m.split(':'); a, b = map(float, tr.split('-')); ref = None; cb = None
    if '@' in bx: bx, ref = bx.split('@')
    if ref and '#' in ref: ref, cb = ref.split('#'); cb = tuple(map(int, cb.split(',')))
    if ref is not None: ref = float(ref)
    MS.append((a, b, tuple(map(int, bx.split(','))), ref, cb))
REFS = {}
_c = cv2.VideoCapture(src)
for m in MS:
    if m[3] is not None and m[3] not in REFS: _c.set(cv2.CAP_PROP_POS_MSEC, m[3] * 1000); REFS[m[3]] = _c.read()[1]
cap = cv2.VideoCapture(src); fps = cap.get(cv2.CAP_PROP_FPS); cap.set(cv2.CAP_PROP_POS_MSEC, T0 * 1000)
W, H = 1080, 1920; vh = round(720 * W / 1280)
p = subprocess.Popen(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(fps), '-i', '-',
                      '-ss', str(T0), '-t', str(T1 - T0), '-i', src, '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-crf', '12', '-preset', 'veryfast',
                      '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k', '-shortest', out], stdin=subprocess.PIPE)
P = 24
n = 0; N = int(round((T1 - T0) * fps))
while n < N:
    ok, fr = cap.read()
    if not ok: break
    t = T0 + n / fps
    for a, b, (x0, y0, x1, y1), ref, cb in MS:
        if a <= t < b and ref is not None:
            R = REFS[ref]; X0, Y0, X1, Y1 = cb or (max(0, x0 - 140), max(0, y1 + 8), min(1280, x1 + 60), min(720, y1 + 200))
            g = lambda im: cv2.cvtColor(im[Y0:Y1, X0:X1], cv2.COLOR_BGR2GRAY).astype(np.float32)
            (dx, dy), resp = cv2.phaseCorrelate(g(R), g(fr), cv2.createHanningWindow((X1 - X0, Y1 - Y0), cv2.CV_32F))
            if resp < .5: ref = None
        if a <= t < b and ref is not None:
            W2 = cv2.warpAffine(R, np.float32([[1, 0, dx], [0, 1, dy]]), (1280, 720), borderMode=cv2.BORDER_REPLICATE)
            al = np.zeros((720, 1280), np.float32); al[max(0, y0 - 6):y1 + 6, max(0, x0 - 6):x1 + 6] = 1; al = cv2.GaussianBlur(al, (0, 0), 6)[..., None]
            fr = (fr * (1 - al) + W2 * al).astype(np.uint8); continue
        if a <= t < b:
            X0, Y0, X1, Y1 = max(0, x0 - P), max(0, y0 - P), min(1280, x1 + P), min(720, y1 + P)
            roi = fr[Y0:Y1, X0:X1]; mk = np.zeros(roi.shape[:2], np.uint8); mk[y0 - Y0:y1 - Y0, x0 - X0:x1 - X0] = 255
            fr[Y0:Y1, X0:X1] = cv2.inpaint(roi, mk, 9, cv2.INPAINT_TELEA)
    bg = cv2.resize(fr, (int(1920 * 1280 / 720), H)); x0 = (bg.shape[1] - W) // 2; bg = bg[:, x0:x0 + W]
    bg = cv2.GaussianBlur(cv2.resize(bg, (W // 8, H // 8)), (0, 0), 3); bg = (cv2.resize(bg, (W, H)) * 0.35).astype(np.uint8)
    bg[Y:Y + vh] = cv2.resize(fr, (W, vh), interpolation=cv2.INTER_LANCZOS4)
    p.stdin.write(bg.tobytes()); n += 1
p.stdin.close(); p.wait(); print('frames', n)
