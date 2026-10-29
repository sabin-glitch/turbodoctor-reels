"""Promo reparații motoare (29.10.2026): build the compilation source from engine sequences already published.
Each segment keeps its own picture with its own voice (no voice over other footage, no re-ordering inside a segment).
Old reels (already edited: burned-in captions + graphics) -> voice separated from their music/SFX (UVR MDX-Net),
the older TikTok clip (no music) keeps its original sound. Every segment is loudness-matched, with 12 ms fades.
Output: /home/claude/promo/all.mp4 (preview audio) + all_voice48.wav / all_voice16.wav (lossless, mono) + segs.json"""
import json, os, subprocess, sys
import numpy as np, soundfile as sf
from scipy.signal import resample_poly

FPS = 30
SRC = "/home/claude/src_dl"
SEP = "/home/claude/turbodoctor-reels/pipeline/sep_voice.py"
W = "/home/claude/promo/work"; os.makedirs(W, exist_ok=True)
SEGS = [  # name, file, t0, t1, audio ('orig' = original sound, 'sep' = voice separated from the old reel's music/SFX), what is said
    ("hook",  "/home/claude/promo/seg/pre_clean.mp4", 0.00, 11.25, "orig", "Ai probleme cu motorul mașinii tale? ... rezolvarea completă și corectă a problemei tale."),
    ("merc",  f"{SRC}/orig_mercedes_0193.mp4",       2.62, 7.30, "sep",  "Nu trebuie să deții doar motor diesel ca să poți veni la Turbo Doctor."),
    ("suz",   f"{SRC}/orig_suzuki_0172.mp4",        21.85, 34.56, "sep", "În urma constatării cu camera endoscopică ... foarte multă motorină."),
    ("opel",  f"{SRC}/orig_opel_0213.mp4",           5.05, 15.50, "sep",  "La Turbo Doctor primim și motoare din afara țării ... din Piatra Neamț."),
    ("trust", "/home/claude/promo/seg/pre_clean.mp4", 108.35, 129.65, "orig", "Țineți minte: ... diagnoza este complet gratuită."),
    ("cta",   "/home/claude/promo/seg/pre_clean.mp4", 141.25, 147.80, "orig", "Țineți minte că vă puteți programa ... turbodoctor.ro"),
]
TARGET_LUFS = -20.0
ONLY = [x for x in os.environ.get("ONLY", "").split(",") if x]
AUDIO_SRC = {"/home/claude/promo/seg/pre_clean.mp4": f"{SRC}/named/pre_reparatie_corecta_motoare.mp4"}


def run(cmd): subprocess.run(cmd, check=True)


def lufs(path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True)
    I = [l for l in r.stderr.splitlines() if l.strip().startswith("I:")]
    return float(I[-1].split()[1])


segs, vids, voice = [], [], []
t_out = 0.0
for k, (name, f, t0, t1, mode, txt) in enumerate(SEGS):
    n0, n1 = round(t0 * FPS), round(t1 * FPS); t0, t1 = n0 / FPS, n1 / FPS; nfr = n1 - n0; dur = nfr / FPS
    v = f"{W}/{k}_{name}.mp4"
    if ONLY and name not in ONLY: continue
    if not os.path.exists(v): run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{t0:.4f}", "-i", f, "-frames:v", str(nfr), "-an",
         "-vf", "fps=30,scale=1080:1920:flags=lanczos,format=yuv420p", "-c:v", "libx264", "-preset", "medium", "-crf", "10", v])
    # audio: a little context around the cut for the separation model, then trimmed to the exact frame range
    pad = 0.5; a0 = max(0.0, t0 - pad)
    raw = f"{W}/{k}_{name}_raw.wav"
    af = AUDIO_SRC.get(f, f)  # the cleaned clip re-encodes the sound: take it from the original file (same timing)
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{a0:.4f}", "-t", f"{dur + 2 * pad:.4f}", "-i", af, "-vn", "-ac", "2", "-ar", "44100", raw])
    src = raw
    if mode == "sep":
        voc = f"{W}/{k}_{name}_voc.wav"
        if not os.path.exists(voc): run([sys.executable, SEP, raw, voc, "-"])
        src = voc
    x, sr = sf.read(src, dtype="float32", always_2d=True); x = x.mean(1)
    x = resample_poly(x, 48000, sr).astype(np.float32) if sr != 48000 else x
    i0 = int(round((t0 - a0) * 48000)); n = int(round(dur * 48000))
    y = x[i0:i0 + n]; y = np.pad(y, (0, n - len(y)))
    tmp = f"{W}/{k}_{name}_v48.wav"; sf.write(tmp, y, 48000)
    L = lufs(tmp); g = 10 ** ((TARGET_LUFS - L) / 20); y = y * g
    fl = int(.012 * 48000); y[:fl] *= np.linspace(0, 1, fl); y[-fl:] *= np.linspace(1, 0, fl)
    pk = float(np.abs(y).max())
    if pk > .97: y *= .97 / pk
    voice.append(y); vids.append(v)
    segs.append(dict(i=k, name=name, file=os.path.basename(f), src_t0=round(t0, 4), src_t1=round(t1, 4), out_t0=round(t_out, 4), out_t1=round(t_out + dur, 4),
                     frames=nfr, audio=mode, lufs_in=round(L, 1), gain_db=round(20 * np.log10(g), 1), text=txt))
    print(f"{k} {name:6s} src {t0:7.3f}-{t1:7.3f}  out {t_out:6.3f}-{t_out + dur:6.3f}  {mode}  LUFS {L:.1f} -> {TARGET_LUFS}", flush=True)
    t_out += dur

if ONLY: sys.exit(0)
voice = np.concatenate(voice)
sf.write("/home/claude/promo/all_voice48.wav", voice, 48000)
sf.write("/home/claude/promo/all_voice16.wav", resample_poly(voice, 1, 3).astype(np.float32), 16000)
open(f"{W}/list.txt", "w").write("".join(f"file '{v}'\n" for v in vids))
run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{W}/list.txt", "-i", "/home/claude/promo/all_voice48.wav",
     "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", "/home/claude/promo/all.mp4"])
json.dump(segs, open("/home/claude/promo/segs.json", "w"), ensure_ascii=False, indent=1)
print(f"total {t_out:.3f}s  frames {sum(s['frames'] for s in segs)}")
