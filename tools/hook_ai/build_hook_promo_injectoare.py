"""Promo injectoare (28.10.2026): build the hook source = AI clip „pornește greu” (cranking loop until the engine
catches right after „greu”) + AI clip „motor care trepidează” (with a vibration synced to its sound), then Sabin's
clips from „Ei bine”. Writes:
  /home/claude/work/hook_src.mp4   video 1080x1920/30 fps (hook + clips), audio = Sabin's voice delayed by PRE
  /home/claude/work/hook_bed.wav   48 kHz stereo engine sound for the hook only (mixed by audio.py as a 'bed')
  /home/claude/work/hook_meta.json frame/time markers for reel.js
Run: python3 -I build_hook.py"""
import json, subprocess, os
import numpy as np, soundfile as sf, cv2
from scipy.signal import butter, sosfilt

W = "/home/claude/work"; AI = f"{W}/ai"; FPS = 30; SR = 48000
CRANK_V = f"{AI}/ai_promoinj_pornire_grea_v1.mp4"; SHAKE_V = f"{AI}/ai_promoinj_motor_trepideaza_v1.mp4"
CRANK_A = f"{AI}/ai_promoinj_pornire_grea_v1.wav"; SHAKE_A = f"{AI}/ai_promoinj_motor_trepideaza_v1.wav"
ALL = f"{W}/all.mp4"

PRE_F = 18                 # Sabin's voice starts 0.6 s after the first cranking pulse
CUT1_F = 148               # crank -> shaking engine (f 4.933, just before „Sau”)
CUT2_F = 235               # shaking engine -> Sabin (f 7.833, clip 7.233, just before „Ei bine”)
PRE = PRE_F / FPS; CUT1 = CUT1_F / FPS; CUT2 = CUT2_F / FPS

# ---------------- audio: cranking loop (cuts on the troughs between compression pulses) ----------------
ca, sr = sf.read(CRANK_A, dtype="float64"); assert sr == SR
sa, sr = sf.read(SHAKE_A, dtype="float64"); assert sr == SR
A0, A1 = 2.98, 5.2875            # first pass: starter engagement + steady cranking
M0, M1 = 3.5725, 4.0275          # 4 more pulses
B0 = 3.5725                      # last pass: steady cranking -> the engine catches at AI 5.475
CATCH_AI = 5.475
segs = [(A0, A1), (M0, M1), (B0, B0 + (CUT1 + .06) - ((A1 - A0) + (M1 - M0)))]
XF = int(.025 * SR)
def cut(x, a, b): return x[int(round(a * SR)):int(round(b * SR))].copy()
crank = cut(ca, *segs[0])
for a, b in segs[1:]:
    nx = cut(ca, a, b); r = np.linspace(0, 1, XF)[:, None]
    crank[-XF:] = crank[-XF:] * (1 - r) + nx[:XF] * r; crank = np.vstack([crank, nx[XF:]])
f_catch = (A1 - A0) + (M1 - M0) - 2 * XF / SR + (CATCH_AI - B0)
# pulse times in hook time (for the vibration of the image)
PULSES_AI = [3.010, 3.220, 3.380, 3.515, 3.630, 3.740, 3.855, 3.970, 4.085, 4.200, 4.310, 4.425, 4.540, 4.655, 4.775, 4.885, 5.000, 5.115, 5.230, 5.345]
pulses = [p - A0 for p in PULSES_AI if A0 <= p < A1]
o1 = (A1 - A0) - XF / SR; pulses += [o1 + p - M0 for p in PULSES_AI if M0 <= p < M1]
o2 = o1 + (M1 - M0) - XF / SR; pulses += [o2 + p - B0 for p in PULSES_AI if B0 <= p < CATCH_AI]
f_catch = o2 + (CATCH_AI - B0)

def hpf(x, fc): return sosfilt(butter(2, fc, btype="high", fs=SR, output="sos"), x, axis=0)
def rms_db(x): return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)
crank = hpf(crank, 28)
g = 10 ** ((-21 - rms_db(crank[int(.1 * SR):int((f_catch - .05) * SR)])) / 20); crank *= g   # cranking at -21 dBFS RMS
S0_AI = 6.0233 - (CUT2 - CUT1)   # shaking clip: its last 2.9 s (closest framing on the injector lines)
shake = hpf(cut(sa, S0_AI, S0_AI + (CUT2 - CUT1)), 28)
shake *= 10 ** ((-21 - rms_db(shake)) / 20)
n = int(round(CUT2 * SR)) + int(.02 * SR); bed = np.zeros((n, 2))
i1 = int(round(CUT1 * SR)); crank = crank[:i1 + XF]
bed[:len(crank)] += crank * np.r_[np.ones(len(crank) - XF), np.linspace(1, 0, XF)][:, None]
r = np.linspace(0, 1, XF)[:, None]; sh = shake.copy(); sh[:XF] *= r
m = min(len(sh), n - i1); bed[i1:i1 + m] += sh[:m]
fo = int(.06 * SR); bed[int(round(CUT2 * SR)) - fo:int(round(CUT2 * SR))] *= np.linspace(1, 0, fo)[:, None]; bed[int(round(CUT2 * SR)):] = 0
bed[:int(.004 * SR)] *= np.linspace(0, 1, int(.004 * SR))[:, None]
pk = np.abs(bed).max(); bed *= min(1.0, .89 / pk)
sf.write(f"{W}/hook_bed.wav", bed.astype(np.float32), SR, subtype="FLOAT")

# ---------------- video ----------------
def frames(path):
    cap = cv2.VideoCapture(path); out = []
    while True:
        ok, fr = cap.read()
        if not ok: break
        out.append(fr)
    return out, cap.get(cv2.CAP_PROP_FPS) or 24
cf, cfps = frames(CRANK_V); sfr, sfps = frames(SHAKE_V)
# crank video path (ping-pong on the steady part, so the frame of the catch lands on the catch in the sound)
X, Y = 5.2, None
# forward A0->X, back X->Y, forward Y->CATCH_AI so that CATCH_AI is shown at f_catch
Y = X - (f_catch - (CATCH_AI - A0)) / 2   # path: (X-A0) + (X-Y) + (CATCH_AI-Y) = f_catch
def crank_t(f):
    if f < X - A0: return A0 + f
    f2 = f - (X - A0)
    if f2 < X - Y: return X - f2
    return Y + (f2 - (X - Y))
rng = np.random.default_rng(28)
def vib_crank(f):  # small jolt on every compression pulse, a strong rock when the engine catches
    dx = dy = 0.0
    for k, p in enumerate(pulses):
        d = f - p
        if 0 <= d < .09: a = 2.6 * np.exp(-d / .03); dx += a * np.sin(k * 2.1); dy += a * (.6 + .4 * np.cos(k * 1.3))
    d = f - f_catch
    if 0 <= d < .7: a = 11 * np.exp(-d / .16); dx += a * np.sin(d * 2 * np.pi * 7.5); dy += a * .8 * np.cos(d * 2 * np.pi * 6.1)
    return dx, dy
# shaking engine: irregular vibration whose strength follows the engine's low rumble (20-150 Hz)
lo = sosfilt(butter(4, [20, 150], btype="band", fs=SR, output="sos"), sa.mean(1))
hop = int(SR / FPS); env = np.sqrt(np.convolve(lo ** 2, np.ones(hop) / hop, mode="same"))
def env_at(t): i = int(t * SR); return float(env[max(0, min(len(env) - 1, i))])
E = np.array([env_at(S0_AI + k / FPS) for k in range(CUT2_F - CUT1_F + 2)]); En = (E - E.min()) / (E.max() - E.min() + 1e-9)
ph = rng.random(6) * 6.28
def vib_shake(k):
    t = k / FPS; a = 2.2 + 6.5 * En[min(k, len(En) - 1)] ** 1.5
    dx = a * (np.sin(2 * np.pi * 9.7 * t + ph[0]) * .6 + np.sin(2 * np.pi * 13.3 * t + ph[1]) * .4)
    dy = a * (np.sin(2 * np.pi * 11.1 * t + ph[2]) * .6 + np.sin(2 * np.pi * 7.3 * t + ph[3]) * .4)
    return dx, dy
def up(fr, dx, dy, z=1.045):
    fr = cv2.resize(fr, (1080, 1920), interpolation=cv2.INTER_LANCZOS4)
    bl = cv2.GaussianBlur(fr, (0, 0), 1.4); fr = cv2.addWeighted(fr, 1.32, bl, -.32, 0)
    M = np.float32([[z, 0, (1 - z) * 540 + dx], [0, z, (1 - z) * 960 + dy]])
    return cv2.warpAffine(fr, M, (1080, 1920), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
os.makedirs(f"{W}/hookfr", exist_ok=True)
for f_ in range(CUT2_F):
    f = f_ / FPS
    if f_ < CUT1_F:
        t = crank_t(f); fr = cf[max(0, min(len(cf) - 1, int(round(t * cfps))))]; dx, dy = vib_crank(f)
    else:
        k = f_ - CUT1_F; t = S0_AI + k / FPS; fr = sfr[max(0, min(len(sfr) - 1, int(round(t * sfps))))]; dx, dy = vib_shake(k)
    cv2.imwrite(f"{W}/hookfr/{f_:04d}.png", up(fr, dx, dy))
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-framerate", str(FPS), "-i", f"{W}/hookfr/%04d.png",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "10", "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
                f"{W}/hook_video.mp4"], check=True)
# clips from CUT2 (clip time CUT2 - PRE) + voice delayed by PRE
clip0 = (CUT2_F - PRE_F) / FPS
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", f"{W}/hook_video.mp4", "-ss", f"{clip0:.4f}", "-i", ALL, "-i", ALL,
                "-filter_complex", f"[0:v]setsar=1[h];[1:v]setsar=1,setpts=PTS-STARTPTS[c];[h][c]concat=n=2:v=1:a=0[v];[2:a]adelay={int(PRE * 1000)}|{int(PRE * 1000)},apad[a]",
                "-map", "[v]", "-map", "[a]", "-shortest", "-c:v", "libx264", "-preset", "veryfast", "-crf", "10", "-pix_fmt", "yuv420p",
                "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", f"{W}/hook_src.mp4"], check=True)
meta = dict(PRE=PRE, CUT1=CUT1, CUT2=CUT2, catch=round(f_catch, 3), pulses=[round(p, 3) for p in pulses], clip0=clip0, Y=round(Y, 3),
            shake_ai=[S0_AI, S0_AI + (CUT2 - CUT1)])
json.dump(meta, open(f"{W}/hook_meta.json", "w"), indent=1); print(json.dumps(meta))
