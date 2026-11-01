"""Promo flote (01.11.2026): hook = AI drone shot over a huge fleet of identical white vans ("ca la UMB"), under Sabin's
first phrase „Deții o flotă auto?”, then his 10 clips glued in shooting order (2028 trimmed before the first word).
Writes /home/claude/work/flote/build/{all.mp4, hook_src.mp4, hook_bed.wav, hook_meta.json}.  Run: python3 -I build_hook_flote.py"""
import json, subprocess, os
import numpy as np, soundfile as sf, cv2
from scipy.signal import butter, sosfilt
W = "/home/claude/work/flote"; B = f"{W}/build"; FPS = 30; SR = 48000
DRONE_V = f"{W}/ai/ai_flote_drona_v1.mp4"; DRONE_A = f"{W}/ai/ai_flote_drona_v1.wav"
CLIPS = ["2028", "2030", "2034b", "2035", "2036", "2037", "2038", "2039", "2052", "2053"]  # shooting order (2034b = plates blurred)
VOICE_ON = 2.55            # „Deții” starts at 2.55 s in IMG_2028 (energy onset)
PRE = 1.30                 # drone shot alone before his voice
TRIM = round(VOICE_ON - PRE, 3)            # 1.25 s of IMG_2028 dropped (he stands silently; the AI shot covers it anyway)
LA_ON = 3.80               # „La Turbo Doctor” in IMG_2028
CUT_F = int((LA_ON - TRIM - .03) * FPS)    # drone -> Sabin, just before „La”
CUT = CUT_F / FPS
AI0, AI1 = 0.8, 6.0        # drone source span, eased (fast at the start, ~1.2x at the end)
def ai_t(h):
    u = min(1.0, h / CUT); return AI0 + (AI1 - AI0) * (.45 * u + .55 * (1 - (1 - u) ** 2))
# ---------- 1. his clips glued in shooting order ----------
ins, fl = [], []
for k, c in enumerate(CLIPS):
    if c == "2028": ins += ["-ss", f"{TRIM:.3f}"]
    ins += ["-i", f"{W}/sdr/{c}.mp4"]; fl.append(f"[{k}:v]setsar=1,setpts=PTS-STARTPTS[v{k}];[{k}:a]aresample=48000,asetpts=PTS-STARTPTS[a{k}]")
fc = ";".join(fl) + ";" + "".join(f"[v{k}][a{k}]" for k in range(len(CLIPS))) + f"concat=n={len(CLIPS)}:v=1:a=1[v][a]"
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *ins, "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "10", "-pix_fmt", "yuv420p", "-r", "30",
                "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "1",
                f"{B}/all.mp4"], check=True)
starts = []; t = 0.0
for c in CLIPS:
    d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{W}/sdr/{c}.mp4"]).decode())
    if c == "2028": d -= TRIM
    starts.append(round(t, 3)); t += d
# ---------- 2. hook frames from the drone shot ----------
cap = cv2.VideoCapture(DRONE_V); dfps = cap.get(cv2.CAP_PROP_FPS); fr = []
while True:
    ok, im = cap.read()
    if not ok: break
    fr.append(im)
os.makedirs(f"{B}/hookfr", exist_ok=True)
for f in range(CUT_F):
    src = fr[max(0, min(len(fr) - 1, int(round(ai_t(f / FPS) * dfps))))]
    im = cv2.resize(src, (1080, 1920), interpolation=cv2.INTER_LANCZOS4)
    bl = cv2.GaussianBlur(im, (0, 0), 1.4); im = cv2.addWeighted(im, 1.32, bl, -.32, 0)
    cv2.imwrite(f"{B}/hookfr/{f:04d}.png", im)
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-framerate", str(FPS), "-i", f"{B}/hookfr/%04d.png", "-c:v", "libx264", "-preset", "veryfast",
                "-crf", "10", "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", f"{B}/hook_video.mp4"], check=True)
# ---------- 3. source = hook frames + his clips from CUT, audio = his voice (from TRIM) ----------
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", f"{B}/hook_video.mp4", "-ss", f"{CUT:.4f}", "-i", f"{B}/all.mp4", "-i", f"{B}/all.mp4",
                "-filter_complex", "[0:v]setsar=1[h];[1:v]setsar=1,setpts=PTS-STARTPTS[c];[h][c]concat=n=2:v=1:a=0[v]",
                "-map", "[v]", "-map", "2:a", "-c:v", "libx264", "-preset", "veryfast", "-crf", "10", "-pix_fmt", "yuv420p", "-r", "30",
                "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", f"{B}/hook_src.mp4"], check=True)
# ---------- 4. hook bed = the drone shot's own sound (wind, rotors, distant idling), under the voice ----------
a, sr = sf.read(DRONE_A, dtype="float64"); assert sr == SR
seg = a[int(AI0 * SR):int(AI0 * SR) + int(CUT * SR) + int(.06 * SR)].copy()
seg = sosfilt(butter(2, 28, btype="high", fs=SR, output="sos"), seg, axis=0)
rms = 20 * np.log10(np.sqrt(np.mean(seg ** 2)) + 1e-12); seg *= 10 ** ((-21 - rms) / 20)
fo = int(.06 * SR); seg[-fo:] *= np.linspace(1, 0, fo)[:, None]; fi = int(.01 * SR); seg[:fi] *= np.linspace(0, 1, fi)[:, None]
seg *= min(1.0, .89 / np.abs(seg).max())
sf.write(f"{B}/hook_bed.wav", seg.astype(np.float32), SR, subtype="FLOAT")
meta = dict(TRIM=TRIM, PRE=PRE, CUT=CUT, CUT_F=CUT_F, AI=[AI0, AI1], clips=CLIPS, starts=starts, total=round(t, 3))
json.dump(meta, open(f"{B}/hook_meta.json", "w"), indent=1); print(json.dumps(meta))
