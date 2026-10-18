"""Audio v2: voice per EDL at 1x -> atempo(speed) + clean-up, procedural 'tech' music bed ducked under the voice,
synthesized SFX from out/sfx.json, final loudnorm -14 LUFS.  Output: audio/mix_final.wav"""
import os, json, subprocess
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt, sawtooth

ROOT = os.environ.get("REEL_ROOT") or os.path.dirname(os.path.abspath(__file__)); SR = 48000
tl = json.load(open(f"{ROOT}/out/timeline.json")); SP = tl.get("speed", 1.0)
cfg = json.load(open(f"{ROOT}/out/v2.json")) if os.path.exists(f"{ROOT}/out/v2.json") else {}
src, sr = sf.read(f"{ROOT}/audio/src48.wav", dtype="float32"); assert sr == SR
if src.ndim == 1: src = np.stack([src, src], 1)
TOTAL = tl["total"]; n_total = int(round(round(TOTAL * 30) / 30 * SR))
S0, SEND, TEND = tl["story_out0"], tl["story_end"], tl.get("tip_end", tl["story_end"])
rng = np.random.default_rng(7)

# ---------------- voice: place segments in the 1x domain, then time-compress ----------------
n1 = int((SEND * SP + 1.0) * SR); v1 = np.zeros((n1, 2), np.float32); FADE = int(0.006 * SR)
for s in tl["segments"]:
    if s["kind"] not in ("cold_audio", "story"): continue
    x = src[int(round(s["src_a"] * SR)):int(round(s["src_b"] * SR))].copy()
    if len(x) < 2 * FADE: continue
    f = np.linspace(0, 1, FADE, dtype=np.float32)[:, None]; x[:FADE] *= f; x[-FADE:] *= f[::-1]
    o = int(round(s["out_a"] * SP * SR)); n = min(len(x), n1 - o)
    if n > 0: v1[o:o + n] += x[:n]
sf.write(f"{ROOT}/audio/voice1x.wav", v1, SR, subtype="FLOAT")
chain = (f"atempo={SP}," if abs(SP - 1) > 1e-3 else "") + ("highpass=f=75,lowpass=f=14500,afftdn=nr=10:nf=-30,equalizer=f=3200:t=q:w=1.2:g=2.5,equalizer=f=250:t=q:w=1:g=-1.5,"
         "acompressor=threshold=-21dB:ratio=3:attack=8:release=160:makeup=5dB,loudnorm=I=-15:TP=-2:LRA=9")
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", f"{ROOT}/audio/voice1x.wav", "-af", chain, "-ar", str(SR), "-c:a", "pcm_f32le", f"{ROOT}/audio/voice_proc.wav"], check=True)
vp, _ = sf.read(f"{ROOT}/audio/voice_proc.wav", dtype="float32")
if vp.ndim == 1: vp = np.stack([vp, vp], 1)
vp = vp[:n_total] if len(vp) >= n_total else np.vstack([vp, np.zeros((n_total - len(vp), 2), np.float32)])
vp[int((SEND + .35) * SR):] = 0

def bp(x, lo, hi, order=2): return sosfilt(butter(order, [lo, hi], btype="band", fs=SR, output="sos"), x, axis=0)
def lp(x, fc, order=2): return sosfilt(butter(order, fc, btype="low", fs=SR, output="sos"), x, axis=0)
def hp(x, fc, order=2): return sosfilt(butter(order, fc, btype="high", fs=SR, output="sos"), x, axis=0)
def env(n, a, d): t = np.arange(n) / SR; e = np.exp(-t * d); na = max(1, int(a * SR)); e[:na] *= np.linspace(0, 1, na); return e
T = lambda d: np.arange(int(d * SR)) / SR
mf = lambda m: 440.0 * 2 ** ((m - 69) / 12)

# ---------------- procedural music bed ----------------
def music():
    if not cfg.get("music", True): return np.zeros((n_total, 2), np.float32)
    bpm = cfg.get("bpm", 104); beat = 60 / bpm; bar = 4 * beat
    prog = cfg.get("prog", [[57, 60, 64], [53, 57, 60], [55, 60, 64], [55, 59, 62]])  # Am F C G
    roots = cfg.get("roots", [45, 41, 48, 43])
    N = n_total; pad = np.zeros((N, 2)); bass = np.zeros(N); kick = np.zeros(N); hat = np.zeros(N)
    nb = int(np.ceil(TOTAL / bar)) + 1
    for b in range(nb):
        t0 = b * bar; i0 = int(t0 * SR); L = int((bar + .35) * SR)
        if i0 >= N: break
        L = min(L, N - i0); t = np.arange(L) / SR
        e = np.minimum(1, t / .25) * np.minimum(1, np.maximum(0, (bar + .35 - t) / .35))
        for k, m in enumerate(prog[b % 4]):
            fq = mf(m); ph = rng.random() * 6
            l = sawtooth(2 * np.pi * fq * 1.003 * t + ph) * .5 + np.sin(2 * np.pi * fq * t) * .5
            r = sawtooth(2 * np.pi * fq * .997 * t + ph + 1) * .5 + np.sin(2 * np.pi * fq * t + .3) * .5
            pad[i0:i0 + L, 0] += l * e * .06; pad[i0:i0 + L, 1] += r * e * .06
        for q in range(8):  # 8th-note bass pluck
            tq = t0 + q * beat / 2; j = int(tq * SR); Lb = int(.3 * SR)
            if j >= N: break
            Lb = min(Lb, N - j); tb = np.arange(Lb) / SR; fq = mf(roots[b % 4])
            w = (np.sin(2 * np.pi * fq * tb) * .75 + sawtooth(2 * np.pi * fq * tb) * .25) * env(Lb, .004, 9) * (1.0 if q % 2 == 0 else .7)
            bass[j:j + Lb] += w * .28
        for q in range(4):
            tq = t0 + q * beat; j = int(tq * SR)
            if j >= N: break
            if q % 2 == 0:
                Lk = min(int(.42 * SR), N - j); tk = np.arange(Lk) / SR; fk = 44 + 85 * np.exp(-tk * 32)
                kick[j:j + Lk] += np.sin(2 * np.pi * np.cumsum(fk) / SR) * env(Lk, .002, 8) * .55
            jh = int((tq + beat / 2) * SR); Lh = min(int(.06 * SR), N - jh)
            if Lh > 0: hat[jh:jh + Lh] += rng.standard_normal(Lh) * env(Lh, .001, 85) * .05
    pad = lp(pad, 1100); bass = lp(bass, 420); hat = hp(hat, 7000)
    # sidechain pump on pad + bass
    tt = np.arange(N) / SR; ph = (tt % beat); pump = 1 - .32 * np.exp(-ph / .11)
    m = pad * pump[:, None] + np.stack([bass * pump, bass * pump], 1) + np.stack([kick, kick], 1) + np.stack([hat * .9, hat * 1.1], 1)
    # normalise bed to ~ -19 dBFS RMS
    rms = np.sqrt(np.mean(m ** 2) + 1e-12); m *= 10 ** (-19 / 20) / rms
    # section levels
    g = np.ones(N)
    def ramp(a, b, va, vb):
        ia, ib = int(a * SR), int(b * SR); ia = max(0, min(N, ia)); ib = max(0, min(N, ib))
        if ib > ia: g[ia:ib] = np.linspace(va, vb, ib - ia)
    g[:] = .78
    ramp(0, .25, 0, .95); ramp(.25, max(.3, S0), .95, .95); ramp(max(.3, S0), max(.6, S0 + .4), .95, .78)
    ramp(SEND, SEND + .4, .78, 1.0); g[int((SEND + .4) * SR):] = 1.0
    ramp(TEND, TEND + .3, 1.0, 1.1); g[int((TEND + .3) * SR):] = 1.1
    ramp(TOTAL - 1.4, TOTAL, 1.1, 0)
    # ducking under the voice
    mono = np.abs(vp[:, 0]); win = int(.03 * SR)
    rmsv = np.sqrt(np.convolve(mono ** 2, np.ones(win) / win, mode="same") + 1e-12)
    act = np.clip((20 * np.log10(rmsv + 1e-9) + 42) / 14, 0, 1)
    # attack 60 ms / release 450 ms smoothing
    out = np.zeros_like(act); a_att = np.exp(-1 / (.06 * SR)); a_rel = np.exp(-1 / (.45 * SR)); y = 0.0
    step = 48; idx = np.arange(0, N, step); ys = np.zeros(len(idx))
    for k, i in enumerate(idx):
        x = act[i]; c = a_att ** step if x > y else a_rel ** step; y = c * y + (1 - c) * x; ys[k] = y
    duck = np.interp(np.arange(N), idx, ys)
    g = g * (1 - .72 * duck)
    return (m * g[:, None]).astype(np.float32)

# ---------------- SFX ----------------
def impact():
    t = T(0.9); f = 38 + 85 * np.exp(-t * 9); body = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(t), .004, 4.2)
    nz = lp(rng.standard_normal(len(t)), 900) * env(len(t), .001, 30) * .6; return np.stack([body + nz] * 2, 1) * .9
def hit():
    t = T(1.3); f = 32 + 70 * np.exp(-t * 6); body = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(t), .003, 2.6)
    nz = lp(rng.standard_normal(len(t)), 1500) * env(len(t), .001, 18) * .5; x = body + nz; return np.stack([x, x], 1) * .95
def crack():
    t = T(0.45); nz = hp(rng.standard_normal(len(t)), 1200) * env(len(t), .0005, 26); snap = bp(rng.standard_normal(len(t)), 1800, 5200) * env(len(t), .0003, 60) * 1.4
    return np.stack([nz * .7 + snap, np.roll(nz * .7 + snap, 90)], 1) * .55
def whoosh(d=0.5):
    n = int(d * SR); t = np.arange(n) / SR; nz = rng.standard_normal(n); out = np.zeros(n); seg = 1024
    for i in range(0, n, seg):
        c = 350 + 3200 * (i / n) ** 1.4; out[i:i + seg] = bp(nz[max(0, i - 2048):i + seg], c * .6, min(c * 1.6, 20000))[-len(out[i:i + seg]):]
    e = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 2.2; x = out * e; pan = np.clip(t / d, 0, 1)
    return np.stack([x * (1 - .6 * pan), x * (.4 + .6 * pan)], 1) * .55
def riser(d=0.9):
    n = int(d * SR); t = np.arange(n) / SR; nz = rng.standard_normal(n); out = np.zeros(n); seg = 1024
    for i in range(0, n, seg):
        c = 300 + 6000 * (i / n) ** 2; out[i:i + seg] = bp(nz[max(0, i - 2048):i + seg], c * .7, min(c * 1.4, 20000))[-len(out[i:i + seg]):]
    e = (t / d) ** 2; return np.stack([out * e, out * e], 1) * .5
def pop():
    t = T(0.14); f = 900 * np.exp(-t * 22) + 260; x = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(t), .002, 34); return np.stack([x] * 2, 1) * .5
def beep():
    t = T(0.13); x = np.sin(2 * np.pi * 1020 * t) * np.minimum(1, np.minimum(t / .005, (.13 - t) / .02)); return np.stack([x] * 2, 1) * .28
def alarm():
    out = np.zeros(int(.42 * SR))
    for k, f in enumerate([880, 660, 880]):
        t = T(.1); x = np.sign(np.sin(2 * np.pi * f * t)) * .5 + np.sin(2 * np.pi * f * t) * .5; x = lp(x, 3500) * np.minimum(1, np.minimum(t / .004, (.1 - t) / .01))
        o = int(k * .14 * SR); out[o:o + len(x)] += x
    return np.stack([out] * 2, 1) * .2
def shimmer():
    t = T(0.9); x = np.zeros(len(t))
    for k in range(9):
        f = 2400 + rng.random() * 4200; st = int(rng.random() * .25 * SR)
        x[st:] += np.sin(2 * np.pi * f * t[:len(t) - st] + rng.random() * 6) * env(len(t) - st, .003, 7 + rng.random() * 5)
    x += hp(rng.standard_normal(len(t)), 6000) * env(len(t), .01, 6) * .25; return np.stack([x, np.roll(x, 240)], 1) * .11
def stamp():
    t = T(0.3); body = np.sin(2 * np.pi * 95 * t) * env(len(t), .001, 18); click = lp(rng.standard_normal(len(t)), 2400) * env(len(t), .0004, 55)
    return np.stack([body + click * .8] * 2, 1) * .7
def tick():
    t = T(0.03); x = bp(rng.standard_normal(len(t)), 2800, 7000) * env(len(t), .0002, 260); return np.stack([x] * 2, 1) * .5
def tick2():
    t = T(0.08); x = np.sin(2 * np.pi * 1850 * t) * env(len(t), .001, 60) + bp(rng.standard_normal(len(t)), 3000, 8000) * env(len(t), .0002, 200) * .5
    return np.stack([x] * 2, 1) * .35
def ding():
    def note(f0, d=1.3):
        t = T(d); x = np.zeros(len(t))
        for r, a, dec in [(1, 1, 3.2), (2.0, .45, 4.5), (2.76, .25, 6), (4.07, .12, 8)]: x += a * np.sin(2 * np.pi * f0 * r * t) * env(len(t), .002, dec)
        return x
    a = note(1046.5); b = note(1568.0); o = int(.09 * SR); x = np.zeros(len(a) + o); x[:len(a)] += a; x[o:o + len(b)] += b * .9
    return np.stack([x, np.roll(x, 120)], 1) * .16
def typing():
    out = np.zeros(int(.34 * SR))
    for k in range(7):
        o = int((k * .045 + rng.random() * .015) * SR); n = int(.012 * SR); x = bp(rng.standard_normal(n), 1800, 6500) * env(n, .0003, 320) * (.6 + .4 * rng.random())
        out[o:o + n] += x
    return np.stack([out, np.roll(out, 60)], 1) * .42
def scan():
    t = T(0.6); f = 500 + 2200 * (t / .6) ** 1.3; x = np.sin(2 * np.pi * np.cumsum(f) / SR) * (.5 + .5 * np.sin(2 * np.pi * 28 * t)) * np.sin(np.pi * t / .6) ** 1.5
    x += bp(rng.standard_normal(len(t)), 2500, 8000) * .15 * np.sin(np.pi * t / .6); return np.stack([x, np.roll(x, 200)], 1) * .16
def lock():
    out = np.zeros(int(.2 * SR))
    for k, f in enumerate([1400, 2100]):
        t = T(.06); x = np.sin(2 * np.pi * f * t) * np.minimum(1, np.minimum(t / .003, (.06 - t) / .01)); o = int(k * .08 * SR); out[o:o + len(x)] += x
    return np.stack([out] * 2, 1) * .2
def glitch():
    n = int(.16 * SR); x = rng.standard_normal(n); x = np.round(x * 3) / 3; hold = 24; x = np.repeat(x[::hold], hold)[:n]
    sq = np.sign(np.sin(2 * np.pi * 180 * np.arange(n) / SR)) * .4; x = (x * .5 + sq) * env(n, .002, 14)
    x = bp(x, 300, 6000); return np.stack([x, -x], 1) * .3
def data():
    out = np.zeros(int(.3 * SR))
    for k in range(8):
        f = 900 + rng.random() * 2200; t = T(.022); x = np.sin(2 * np.pi * f * t) * np.minimum(1, np.minimum(t / .002, (.022 - t) / .004)); o = int(k * .034 * SR); out[o:o + len(x)] += x
    return np.stack([out] * 2, 1) * .14
def confetti():
    x = np.zeros((int(1.0 * SR), 2)); p = pop(); x[:len(p)] += p * 1.2; s = shimmer(); x[int(.05 * SR):int(.05 * SR) + len(s)] += s[:len(x) - int(.05 * SR)] * 1.2; return x
GEN = dict(impact=impact, hit=hit, crack=crack, whoosh=whoosh, riser=riser, pop=pop, beep=beep, alarm=alarm, shimmer=shimmer, stamp=stamp,
           tick=tick, tick2=tick2, ding=ding, confetti=confetti, type=typing, scan=scan, lock=lock, glitch=glitch, data=data)
fx = np.zeros((n_total, 2), np.float32)
for c in json.load(open(f"{ROOT}/out/sfx.json")):
    if c["kind"] not in GEN: continue
    s = GEN[c["kind"]]().astype(np.float32) * c["gain"]; o = int(round(c["t"] * SR))
    if o < 0: s = s[-o:]; o = 0
    n = min(len(s), n_total - o)
    if n > 0: fx[o:o + n] += s[:n]
fx *= 0.5
mus = music()
mix = vp + fx + mus * float(cfg.get("music_gain", 1.0))
sf.write(f"{ROOT}/audio/mix_pre.wav", mix, SR, subtype="FLOAT")
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", f"{ROOT}/audio/mix_pre.wav", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
                "-ar", str(SR), "-c:a", "pcm_s16le", f"{ROOT}/audio/mix_final.wav"], check=True)
print("audio v2 done", n_total / SR, "s  speed", SP)
