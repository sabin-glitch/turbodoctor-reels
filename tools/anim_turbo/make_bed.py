"""Sound design bed for the turbo lubrication reel, driven by the animation (vo/probe.json from probe.js):
turbo whine that follows the compressor speed (it winds down after the shaft breaks), a low engine bed, metal grinding while the
dry bearings seize (wobble + sparks), and a hard crack + clang + rattle when the shaft breaks.  Output: 48 kHz stereo WAV for audio.py "beds".
The continuous sounds (whine, air, engine) play only in the hook: they fade out before <hook end> (Sabin, 11.11.2026: „scoate zgomotul de turbină de pe tot parcursul, lasă-l doar în hook”).
usage: python3 make_bed.py <out.wav> [hook end s]"""
import json, sys
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt

SR = 48000
out = sys.argv[1]
p = json.load(open('vo/probe.json')); d = np.array(p['data']); hz = p['hz']
n = int(len(d) / hz * SR); tt = np.arange(n) / SR; ts = np.arange(len(d)) / hz
col = lambda k: np.interp(tt, ts, d[:, k])
wob, spk, sa, heat, spin = col(0), col(1), col(2), col(3), col(4)
rng = np.random.default_rng(7)
bp = lambda x, lo, hi, o=2: sosfilt(butter(o, [lo, hi], btype='band', fs=SR, output='sos'), x)
lp = lambda x, fc, o=2: sosfilt(butter(o, fc, btype='low', fs=SR, output='sos'), x)
def smooth(x, ms):
    w = max(1, int(ms / 1000 * SR)); c = np.cumsum(np.concatenate([[0.0], x])); y = (c[w:] - c[:-w]) / w
    return np.concatenate([np.full(w // 2, y[0]), y, np.full(len(x) - len(y) - w // 2, y[-1])])
L = np.zeros(n); R = np.zeros(n)
HK = float(sys.argv[2]) if len(sys.argv) > 2 else 1e9
hook = np.clip((HK - tt) / .6, 0, 1)                 # 1 in the hook, fades to 0 over the last 0.6 s before the cut
def add(t0, x, g=1.0, pan=0.0):
    i = int(round(t0 * SR))
    if i >= n or i < 0: return
    m = min(len(x), n - i); L[i:i + m] += x[:m] * g * (1 - .35 * max(0, pan)); R[i:i + m] += x[:m] * g * (1 + .35 * min(0, pan))

# 1 · turbo whine: a thin tone + harmonics with slight wobble, pitch and level follow the spin factor
sp = smooth(spin, 30); f = 2900 * (.25 + .75 * sp) * (1 + .004 * np.sin(2 * np.pi * 5.3 * tt))
ph = 2 * np.pi * np.cumsum(f) / SR
whine = (np.sin(ph) * .5 + np.sin(2 * ph + .3) * .18 + np.sin(3.02 * ph) * .07) * (sp ** 1.5) * .035
air = bp(rng.standard_normal(n), 1500, 6000) * sp * .018
L += (whine + air) * hook; R += (whine + np.roll(air, 97)) * hook
# low engine bed
eng = lp(rng.standard_normal(n), 120) * .22 * (1 + .3 * np.sin(2 * np.pi * 23 * tt))
L += eng * hook; R += np.roll(eng, 300) * hook

# 2 · grinding of the dry bearings: rough metallic band noise, amplitude-modulated at the shaft whirl
g = smooth(np.clip(np.maximum(wob, .8 * spk), 0, 1), 40)
am = .55 + .45 * np.sin(2 * np.pi * 44 / (2 * np.pi) * 2 * np.pi * tt) ** 2
for ch, seed in ((L, 3), (R, 4)):
    nz = np.random.default_rng(seed).standard_normal(n)
    ch += (bp(nz, 1800, 5200) * .09 + bp(nz, 350, 900) * .05) * g * am
# squeal: a metal-on-metal tone rising with heat while grinding
sq = np.sin(2 * np.pi * np.cumsum(1900 + 600 * smooth(heat, 200)) / SR) * g * smooth(heat, 200) * .02
L += sq; R += sq
# spark ticks
ticks = (rng.random(n) < 60 / SR) * smooth(spk, 30)
for i in np.where(ticks > 0)[0]:
    m = int(.006 * SR); t = np.arange(m) / SR; x = bp(rng.standard_normal(m), 3000, 9000) * np.exp(-t * 900) * .12
    k = min(m, n - i); pn = rng.random(); L[i:i + k] += x[:k] * pn; R[i:i + k] += x[:k] * (1 - pn)

# 3 · the break: crack + low hit + ringing clang, then rattle of the loose rotor
def crack():
    m = int(1.6 * SR); t = np.arange(m) / SR
    snap = bp(rng.standard_normal(m), 900, 8000) * np.exp(-t * 60) * 1.4
    hit = np.sin(2 * np.pi * np.cumsum(55 + 140 * np.exp(-t * 25)) / SR) * np.exp(-t * 6) * 1.1
    ring = sum(a * np.sin(2 * np.pi * fr * t + p_) * np.exp(-t * dk) for fr, a, dk, p_ in
               [(820, 1.0, 5.5, 0), (1460, .7, 7, 1.1), (2310, .5, 9, .4), (3470, .3, 13, 2.0)])
    return (snap + hit + ring * .35) * np.minimum(1, t / .001)
raw = d[:, 2]; starts = np.where((raw[1:] >= 0) & (raw[:-1] < 0))[0] / hz
for t0 in starts:
    add(t0, crack(), .55)
    for k in range(10):   # rattle
        add(t0 + .18 + k * .09 + rng.random() * .04, bp(rng.standard_normal(int(.04 * SR)), 1200, 5000) * np.exp(-np.arange(int(.04 * SR)) / SR * 140) * .14 * np.exp(-k * .3), pan=rng.random() - .5)

y = np.stack([L, R], 1)
fade = int(.02 * SR); y[:fade] *= np.linspace(0, 1, fade)[:, None]; y[-fade:] *= np.linspace(1, 0, fade)[:, None]
pk = np.abs(y).max()
if pk > .89: y *= .89 / pk
sf.write(out, y.astype(np.float32), SR, subtype='FLOAT')
rms = lambda a, b_: 20 * np.log10(np.sqrt(np.mean(y[int(a * SR):int(b_ * SR)] ** 2)) + 1e-9)
print('bed', out, 'dur %.2f s' % (n / SR), 'peak %.2f' % np.abs(y).max(), 'breaks', [round(x, 2) for x in starts])
print('rms dB: hook grind %.1f | break %.1f | normal %.1f | spin-down %.1f' % (rms(.5, 2.5), rms(2.97, 3.5), rms(12, 14), rms(4, 5.5)))
