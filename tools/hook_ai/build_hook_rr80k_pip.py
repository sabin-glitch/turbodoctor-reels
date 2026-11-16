"""Range Rover Velar 80.000 km, v2 of the hook (14.11.2026, Sabin: „vreau omul care plânge să fie pus doar într-o parte,
să se vadă și ecranul meu de început”): Sabin's clip runs whole from 0 (his opening shot stays visible) and the AI clip of the
crying man sits in a picture-in-picture window, top right, until just before „Venit la revizie” (5.2 s), then shrinks away.
Writes <W>/hook_src_pip.mp4 (1080x1920/30, the clip's own audio, unchanged). The sobbing bed is still <W>/hook_bed.wav
(build_hook_rr80k_om_plange.py). Run: python3 -I build_hook_rr80k_pip.py <W>"""
import json, subprocess, sys
import numpy as np, cv2

W = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/work"
AI_V = f"{W}/ai/ai_rr80k_om_plange_v1.mp4"; ALL = f"{W}/all.mp4"
FPS = 30
CUT = 156 / FPS                      # „Venit” at 5.29: the window is gone by then
OUT0, OUT1 = CUT - .18, CUT + .02     # exit: shrinks towards its top-right corner and fades
BX, BY, BW, BH = 548, 236, 492, 620   # window (content area) in the 1080x1920 frame
RAD, BORDER = 28, 7
CROP0, CROP1, CC = 940, 880, (545, 740)   # AI crop width (slow push-in) and centre, in the 1080x1920 AI frame
F_END = int(np.ceil(OUT1 * FPS)) + 1

# AI frames, pre-cropped to the widest window and downscaled once (memory)
cap = cv2.VideoCapture(AI_V); afps = cap.get(cv2.CAP_PROP_FPS) or 24
ar = BW / BH; cw0 = CROP0; ch0 = cw0 / ar
X0, Y0 = int(CC[0] - cw0 / 2), int(CC[1] - ch0 / 2); X1, Y1 = int(CC[0] + cw0 / 2), int(CC[1] + ch0 / 2)
SC = .62; ai = []
while True:
    ok, im = cap.read()
    if not ok: break
    if im.shape[:2] != (1920, 1080): im = cv2.resize(im, (1080, 1920), interpolation=cv2.INTER_LANCZOS4)
    ai.append(cv2.resize(im[max(0, Y0):Y1, max(0, X0):X1], None, fx=SC, fy=SC, interpolation=cv2.INTER_AREA))
ox, oy = max(0, X0), max(0, Y0)

def rounded_mask(w, h, r):
    m = np.zeros((h, w), np.uint8); cv2.rectangle(m, (r, 0), (w - r, h), 255, -1); cv2.rectangle(m, (0, r), (w, h - r), 255, -1)
    for cx, cy in ((r, r), (w - r - 1, r), (r, h - r - 1), (w - r - 1, h - r - 1)): cv2.circle(m, (cx, cy), r, 255, -1, cv2.LINE_AA)
    return m

PAD = 48                                    # room for border + shadow in the layer
LW, LH = BW + 2 * PAD, BH + 2 * PAD
m_in = rounded_mask(BW, BH, RAD).astype(np.float32) / 255
m_out = rounded_mask(BW + 2 * BORDER, BH + 2 * BORDER, RAD + BORDER).astype(np.float32) / 255
sh = np.zeros((LH, LW), np.float32); sh[PAD - BORDER + 14:PAD + BH + BORDER + 14, PAD - BORDER:PAD + BW + BORDER] = m_out
sh = cv2.GaussianBlur(sh, (0, 0), 16) * .6

def layer(f):
    t = f / FPS; im = ai[max(0, min(len(ai) - 1, int(round(t * afps))))]
    p = min(1.0, t / CUT); p = p * p * (3 - 2 * p); cw = CROP0 + (CROP1 - CROP0) * p; ch = cw / ar
    x = (CC[0] - cw / 2 - ox) * SC; y = (CC[1] - ch / 2 - oy) * SC
    M = np.float32([[BW / (cw * SC), 0, -x * BW / (cw * SC)], [0, BH / (ch * SC), -y * BH / (ch * SC)]])
    content = cv2.warpAffine(im, M, (BW, BH), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE).astype(np.float32)
    rgb = np.zeros((LH, LW, 3), np.float32); a = sh.copy()
    ob = np.zeros((LH, LW), np.float32); ob[PAD - BORDER:PAD + BH + BORDER, PAD - BORDER:PAD + BW + BORDER] = m_out
    rgb += 255 * ob[..., None]; a = np.maximum(a, ob)                      # white border
    ib = np.zeros((LH, LW), np.float32); ib[PAD:PAD + BH, PAD:PAD + BW] = m_in
    rgb[PAD:PAD + BH, PAD:PAD + BW] = rgb[PAD:PAD + BH, PAD:PAD + BW] * (1 - m_in[..., None]) + content * m_in[..., None]
    return rgb, a

cap = cv2.VideoCapture(ALL); frames = []
enc = subprocess.Popen(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "1080x1920",
                        "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "10", "-pix_fmt", "yuv420p",
                        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", f"{W}/hook_pip_part.mp4"], stdin=subprocess.PIPE)
for f in range(F_END):
    ok, base = cap.read(); assert ok
    t = f / FPS; e = min(1.0, max(0.0, (t - OUT0) / (OUT1 - OUT0))); e = e * e
    s = 1 - .5 * e; alpha = 1 - e
    if alpha > .003:
        rgb, a = layer(f)
        if s != 1:
            rgb = cv2.resize(rgb, None, fx=s, fy=s, interpolation=cv2.INTER_AREA); a = cv2.resize(a, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
        # anchor: the window's top-right corner stays put while it shrinks
        ax = BX + BW - (BW + PAD) * s; ay = BY - PAD * s
        x0, y0 = int(round(ax)), int(round(ay)); h, w = a.shape
        xa, ya, xb, yb = max(0, x0), max(0, y0), min(1080, x0 + w), min(1920, y0 + h)
        A = (a[ya - y0:yb - y0, xa - x0:xb - x0] * alpha)[..., None]
        reg = base[ya:yb, xa:xb].astype(np.float32)
        base[ya:yb, xa:xb] = np.clip(reg * (1 - A) + rgb[ya - y0:yb - y0, xa - x0:xb - x0] * A, 0, 255).astype(np.uint8)
    enc.stdin.write(base.tobytes())
enc.stdin.close(); assert enc.wait() == 0

subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", f"{W}/hook_pip_part.mp4", "-i", ALL,
                "-filter_complex", f"[0:v]setsar=1[h];[1:v]trim=start_frame={F_END},setpts=PTS-STARTPTS,setsar=1[c];[h][c]concat=n=2:v=1:a=0[v]",
                "-map", "[v]", "-map", "1:a", "-c:v", "libx264", "-preset", "veryfast", "-crf", "10", "-pix_fmt", "yuv420p",
                "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
                f"{W}/hook_src_pip.mp4"], check=True)
print(json.dumps(dict(CUT=CUT, F_END=F_END, box=[BX, BY, BW, BH], crop=[CROP0, CROP1, CC], ai_frames=len(ai), ai_fps=afps)))
