"""Assemble the voice track per the EDL, process it, synthesize SFX from out/sfx.json, mix, normalize."""
import os
import json, subprocess
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt

ROOT = os.environ.get("REEL_ROOT") or os.path.dirname(os.path.abspath(__file__)); SR = 48000
tl = json.load(open(f"{ROOT}/out/timeline.json"))
src, sr = sf.read(f"{ROOT}/audio/src48.wav", dtype="float32"); assert sr == SR
if src.ndim == 1: src = np.stack([src, src], 1)
n_total = int(round(round(tl["total"] * 30) / 30 * SR))
voice = np.zeros((n_total, 2), np.float32)
FADE = int(0.006 * SR)


def place(a, b, out_a):
    x = src[int(round(a * SR)):int(round(b * SR))].copy()
    f = np.linspace(0, 1, FADE, dtype=np.float32)[:, None]
    x[:FADE] *= f; x[-FADE:] *= f[::-1]
    o = int(round(out_a * SR)); n = min(len(x), n_total - o)
    voice[o:o + n] += x[:n]


for s in tl["segments"]:
    if s["kind"] in ("cold_audio", "story"):
        place(s["src_a"], s["src_b"], s["out_a"])
sf.write(f"{ROOT}/audio/voice_edit.wav", voice, SR, subtype="FLOAT")
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", f"{ROOT}/audio/voice_edit.wav", "-af",
                "highpass=f=75,lowpass=f=14500,afftdn=nr=10:nf=-30,equalizer=f=3200:t=q:w=1.2:g=2.5,equalizer=f=250:t=q:w=1:g=-1.5,"
                "acompressor=threshold=-21dB:ratio=3:attack=8:release=160:makeup=5dB,loudnorm=I=-15:TP=-2:LRA=9",
                "-ar", str(SR), "-c:a", "pcm_f32le", f"{ROOT}/audio/voice_proc.wav"], check=True)
vp, _ = sf.read(f"{ROOT}/audio/voice_proc.wav", dtype="float32")
if vp.ndim == 1: vp = np.stack([vp, vp], 1)
vp = vp[:n_total] if len(vp) >= n_total else np.vstack([vp, np.zeros((n_total - len(vp), 2), np.float32)])

# ---------------- SFX synthesis ----------------
rng = np.random.default_rng(3)
T = lambda d: np.arange(int(d * SR)) / SR


def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], btype="band", fs=SR, output="sos"), x)


def lp(x, f, order=2):
    return sosfilt(butter(order, f, btype="low", fs=SR, output="sos"), x)


def hp(x, f, order=2):
    return sosfilt(butter(order, f, btype="high", fs=SR, output="sos"), x)


def env(n, a, d):  # attack (s), exp decay rate
    t = np.arange(n) / SR; e = np.exp(-t * d); na = max(1, int(a * SR)); e[:na] *= np.linspace(0, 1, na); return e


def impact():
    t = T(0.9); f = 38 + 85 * np.exp(-t * 9); ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * env(len(t), .004, 4.2)
    nz = lp(rng.standard_normal(len(t)), 900) * env(len(t), .001, 30) * .6
    return np.stack([body + nz] * 2, 1) * .9


def crack():
    t = T(0.45); nz = hp(rng.standard_normal(len(t)), 1200) * env(len(t), .0005, 26)
    snap = bp(rng.standard_normal(len(t)), 1800, 5200) * env(len(t), .0003, 60) * 1.4
    x = nz * .7 + snap
    for k in range(5):
        o = int((.01 + .03 * k + rng.random() * .02) * SR); w = int(.004 * SR)
        x[o:o + w] += rng.standard_normal(w) * .8 * np.exp(-k * .5)
    return np.stack([x, np.roll(x, 90)], 1) * .55


def whoosh(d=0.5):
    n = int(d * SR); t = np.arange(n) / SR; nz = rng.standard_normal(n)
    out = np.zeros(n); seg = 1024
    for i in range(0, n, seg):
        c = 350 + 3200 * (i / n) ** 1.4
        out[i:i + seg] = bp(nz[max(0, i - 2048):i + seg], c * .6, min(c * 1.6, 20000))[-len(out[i:i + seg]):]
    e = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 2.2
    x = out * e
    pan = np.clip(t / d, 0, 1)
    return np.stack([x * (1 - .6 * pan), x * (.4 + .6 * pan)], 1) * .55


def pop():
    t = T(0.14); f = 900 * np.exp(-t * 22) + 260; ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) * env(len(t), .002, 34)
    return np.stack([x] * 2, 1) * .5


def beep():
    t = T(0.13); x = np.sin(2 * np.pi * 1020 * t) * np.minimum(1, np.minimum(t / .005, (.13 - t) / .02))
    return np.stack([x] * 2, 1) * .28


def alarm():
    out = np.zeros(int(.42 * SR))
    for k, f in enumerate([880, 660, 880]):
        t = T(.1); x = np.sign(np.sin(2 * np.pi * f * t)) * .5 + np.sin(2 * np.pi * f * t) * .5
        x = lp(x, 3500) * np.minimum(1, np.minimum(t / .004, (.1 - t) / .01))
        o = int(k * .14 * SR); out[o:o + len(x)] += x
    return np.stack([out] * 2, 1) * .22


def shimmer():
    t = T(0.9); x = np.zeros(len(t))
    for k in range(9):
        f = 2400 + rng.random() * 4200; st = int(rng.random() * .25 * SR)
        x[st:] += np.sin(2 * np.pi * f * t[:len(t) - st] + rng.random() * 6) * env(len(t) - st, .003, 7 + rng.random() * 5)
    x += hp(rng.standard_normal(len(t)), 6000) * env(len(t), .01, 6) * .25
    return np.stack([x, np.roll(x, 240)], 1) * .11


def stamp():
    t = T(0.3); body = np.sin(2 * np.pi * 95 * t) * env(len(t), .001, 18)
    click = lp(rng.standard_normal(len(t)), 2400) * env(len(t), .0004, 55)
    return np.stack([body + click * .8] * 2, 1) * .7


def tick():
    t = T(0.03); x = bp(rng.standard_normal(len(t)), 2800, 7000) * env(len(t), .0002, 260)
    return np.stack([x] * 2, 1) * .5


def tick2():
    t = T(0.08); x = np.sin(2 * np.pi * 1850 * t) * env(len(t), .001, 60) + bp(rng.standard_normal(len(t)), 3000, 8000) * env(len(t), .0002, 200) * .5
    return np.stack([x] * 2, 1) * .35


def ding():
    def note(f0, d=1.3):
        t = T(d); x = np.zeros(len(t))
        for r, a, dec in [(1, 1, 3.2), (2.0, .45, 4.5), (2.76, .25, 6), (4.07, .12, 8)]:
            x += a * np.sin(2 * np.pi * f0 * r * t) * env(len(t), .002, dec)
        return x
    a = note(1046.5); b = note(1568.0); o = int(.09 * SR)
    x = np.zeros(len(a) + o); x[:len(a)] += a; x[o:o + len(b)] += b * .9
    return np.stack([x, np.roll(x, 120)], 1) * .16


def confetti():
    x = np.zeros((int(1.0 * SR), 2)); p = pop(); x[:len(p)] += p * 1.2
    nz = bp(rng.standard_normal(int(.25 * SR)), 1500, 9000) * env(int(.25 * SR), .001, 22)
    x[:len(nz)] += np.stack([nz] * 2, 1) * .35
    s = shimmer(); x[int(.05 * SR):int(.05 * SR) + len(s)] += s[:len(x) - int(.05 * SR)] * 1.2
    return x


GEN = dict(impact=impact, crack=crack, whoosh=whoosh, pop=pop, beep=beep, alarm=alarm, shimmer=shimmer, stamp=stamp,
           tick=tick, tick2=tick2, ding=ding, confetti=confetti)
fx = np.zeros((n_total, 2), np.float32)
for c in json.load(open(f"{ROOT}/out/sfx.json")):
    s = GEN[c["kind"]]().astype(np.float32) * c["gain"]
    o = int(round(c["t"] * SR))
    if o < 0: s = s[-o:]; o = 0
    n = min(len(s), n_total - o)
    if n > 0: fx[o:o + n] += s[:n]
fx *= 0.5  # SFX bus level under the voice
mix = vp + fx
sf.write(f"{ROOT}/audio/mix_pre.wav", mix, SR, subtype="FLOAT")
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", f"{ROOT}/audio/mix_pre.wav", "-af",
                "loudnorm=I=-14:TP=-1.5:LRA=10", "-ar", str(SR), "-c:a", "pcm_s16le", f"{ROOT}/audio/mix_final.wav"], check=True)
print("audio done", n_total / SR, "s")
