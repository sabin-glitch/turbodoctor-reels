"""Montage source for the Bosch Budapesta reel: selected moments of each clip, in filming order, cuts on the music beat.
Each segment keeps its own image and its own sound. Romanian speech (hook, CP4/CP5, testimony) goes to the main audio track
(transcribed + subtitled); the other segments' real sound (instructor in Hungarian/English, workshop) goes to a separate bed
that skips the voice chain. The last segment is photo #2 (TURBO DOCTOR on the back) with a slow push-in, for the closing message.
Kinds: 'voice' = Romanian speech on the main track (transcribed + subtitled), 'bed' = real sound to audio/amb_bed.wav (out/v2.json beds),
'mute' = image only (music only underneath). Approved version (24.11.2026): Sabin asked to remove the background words (instructor in
Hungarian/English, small talk) and the colleague's closing line, so every segment except the hook and "Un CP4 si un CP5" is 'mute'
and out/v2.json has "beds": [].
Outputs: all.mp4 (1080x1920/30, voice-only audio), amb_bed.wav (48 kHz stereo, silent when nothing is 'bed'), segs.json."""
import json, subprocess, sys
import cv2, numpy as np, soundfile as sf

SDR = "/home/claude/work/sdr"; OUT = "/home/claude/work/montage"; FPS = 30; SR = 48000
BEAT = 60 / 104  # audio.py default bpm 104 -> cuts land on the beat grid of the music bed
PHOTO = "/mnt/user-data/uploads/e94171ba-image.jpg"
# name, clip, src start (s), end: ('beat', k) | ('frames', n) | ('src', t1), kind
SPEC = [
    ("hook_bosch",   "IMG_7422",      0.00, ("frames", 191), "voice"),
    ("inj_fixture",  "2c60881a-5b7",  4.45, ("beat", 18),    "mute"),
    ("inj_close",    "2c60881a-5b7", 14.55, ("beat", 23),    "mute"),
    ("pump_bench",   "IMG_7427",      0.40, ("beat", 28),    "mute"),
    ("pump_cp4cp5",  "IMG_7432",      0.55, ("beat", 39),    "voice"),
    ("prec_beard",   "IMG_7433",      0.20, ("beat", 44),    "mute"),
    ("prec_measure", "IMG_7434",     10.05, ("beat", 47),    "mute"),
    ("prec_hands",   "IMG_7435",      6.80, ("beat", 51),    "mute"),
    ("clean_bench",  "IMG_7436",      6.40, ("beat", 61),    "mute"),
    ("smile",        "IMG_7436",     28.30, ("beat", 65),    "mute"),
    ("testimony",    "IMG_7437",      0.20, ("src", 7.05),   "mute"),
    # photo #2 not used: the last testimony frame (logo centred) carries the closing message as a near-freeze (v2.json tip)
]
BED_TARGET = float(sys.argv[1]) if len(sys.argv) > 1 else -24.0  # dBFS RMS of the active (loudest 40 %) part of each bed segment
BED_MAXGAIN = 8.0

import os; os.makedirs(OUT, exist_ok=True)
segs = []; f_out = 0
for name, clip, t0, end, kind in SPEC:
    if end[0] == "frames": n = end[1]
    elif end[0] == "beat": n = int(round(end[1] * BEAT * FPS)) - f_out
    else: n = int(round((end[1] - t0) * FPS))
    f0 = int(round(t0 * FPS))
    segs.append(dict(name=name, clip=clip, f0=f0, n=n, kind=kind, out_f0=f_out, out_t0=round(f_out / FPS, 4), out_t1=round((f_out + n) / FPS, 4),
                     src_t0=round(f0 / FPS, 4), src_t1=round((f0 + n) / FPS, 4)))
    f_out += n
N = f_out
for s in segs: print(f"{s['name']:13s} {s['clip'] or 'PHOTO':14s} src {s['src_t0']:6.2f}-{s['src_t1']:6.2f}  out {s['out_t0']:6.2f}-{s['out_t1']:6.2f}  ({s['n']} fr) {s['kind']}")
print("total", N / FPS)

# ---------------- video ----------------
enc = subprocess.Popen(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "1080x1920", "-r", str(FPS), "-i", "-",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "10", "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
                        f"{OUT}/video_only.mp4"], stdin=subprocess.PIPE)
for s in segs:
    if s["kind"] == "photo":
        im = cv2.imread(PHOTO); H, W = im.shape[:2]  # 1200x1600 portrait
        cw = H * 9 / 16; cx = W / 2; x0 = cx - cw / 2   # 9:16 crop of the full height, centred (the logo is in the middle)
        for k in range(s["n"]):
            p = k / max(1, s["n"] - 1); e = p * p * (3 - 2 * p)
            z = 1.0 + 0.07 * (0.35 * p + 0.65 * e)      # slow push-in towards the logo
            fx, fy = 0.51, 0.38                         # zoom centre (fraction of the crop): the TURBO DOCTOR logo
            w = cw / z; h = H / z; ax = x0 + fx * cw - fx * w; ay = fy * H - fy * h
            M = np.array([[1080 / w, 0, -ax * 1080 / w], [0, 1920 / h, -ay * 1920 / h]], np.float32)
            fr = cv2.warpAffine(im, M, (1080, 1920), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT)
            enc.stdin.write(fr.tobytes())
        continue
    cap = cv2.VideoCapture(f"{SDR}/{s['clip']}.mp4")
    for _ in range(s["f0"]): cap.grab()   # frame-exact: sequential skip instead of a keyframe seek
    got = 0; last = None
    while got < s["n"]:
        ok, fr = cap.read()
        if not ok: fr = last; assert fr is not None
        if fr.shape[:2] != (1920, 1080): fr = cv2.resize(fr, (1080, 1920), interpolation=cv2.INTER_LANCZOS4)
        enc.stdin.write(fr.tobytes()); last = fr; got += 1
    # verify the seek landed on the right frame (sequential read from 0 as reference)
    cap.release()
enc.stdin.close(); enc.wait()

# ---------------- audio ----------------
def load(clip):
    p = f"{OUT}/{clip}.wav"
    if not os.path.exists(p):
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", f"{SDR}/{clip}.mp4", "-vn", "-ac", "1", "-ar", str(SR), p], check=True)
    x, _ = sf.read(p, dtype="float32"); return x
voice = np.zeros(N * SR // FPS, np.float32); bed = np.zeros(N * SR // FPS, np.float32)
FV = int(.010 * SR); FB = int(.045 * SR)
for s in segs:
    if s["kind"] in ("photo", "mute"): continue
    x = load(s["clip"]); a = s["f0"] * SR // FPS; L = s["n"] * SR // FPS
    seg = x[a:a + L].copy()
    if len(seg) < L: seg = np.concatenate([seg, np.zeros(L - len(seg), np.float32)])
    o = s["out_f0"] * SR // FPS
    if s["kind"] == "voice":
        r = np.linspace(0, 1, FV, dtype=np.float32); seg[:FV] *= r; seg[-FV:] *= r[::-1]
        voice[o:o + L] += seg
    else:
        w = int(.05 * SR); k = len(seg) // w
        rms = np.sqrt((seg[:k * w].reshape(k, w) ** 2).mean(1) + 1e-12)
        act = np.sort(rms)[int(k * .6):]; lvl = 20 * np.log10(np.sqrt(np.mean(act ** 2)) + 1e-9)
        g = min(BED_MAXGAIN, BED_TARGET - lvl); s["bed_level_db"] = round(float(lvl), 1); s["bed_gain_db"] = round(float(g), 1)
        seg *= 10 ** (g / 20)
        r = np.linspace(0, 1, FB, dtype=np.float32); seg[:FB] *= r; seg[-FB:] *= r[::-1]
        bed[o:o + L] += seg
        print(f"bed {s['name']:13s} active {lvl:6.1f} dBFS -> gain {g:+.1f} dB")
peak = np.abs(bed).max(); print("bed peak", 20 * np.log10(peak + 1e-9))
if peak > .95: bed *= .95 / peak
sf.write(f"{OUT}/voice48.wav", voice, SR, subtype="PCM_16")
sf.write(f"{OUT}/amb_bed.wav", np.stack([bed, bed], 1), SR, subtype="FLOAT")
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", f"{OUT}/video_only.mp4", "-i", f"{OUT}/voice48.wav", "-map", "0:v", "-map", "1:a",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-ar", str(SR), "-shortest", f"{OUT}/all.mp4"], check=True)
json.dump(dict(fps=FPS, beat=BEAT, total=N / FPS, segs=segs), open(f"{OUT}/segs.json", "w"), indent=1)
print("MONTAGE_OK", N, "frames", N / FPS, "s")
