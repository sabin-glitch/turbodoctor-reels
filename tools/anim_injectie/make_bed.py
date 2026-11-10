"""Sound design bed for the injection reel, driven by the animation itself (vo/probe.json, sampled by probe.js):
spray hiss while the needle is lifted, injector clicks, combustion thump + rumble, the hard metallic knock when the pilot
injection is missing, and a soft roar while the catalyst and the soot burn.  Output: 48 kHz stereo WAV for audio.py "beds".
usage: python3 make_bed.py <out.wav> <mute windows 'a-b,c-d' where the camera is not on the cylinder>"""
import json, sys
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt

SR = 48000
out = sys.argv[1]
MUTE = [tuple(map(float, w.split('-'))) for w in sys.argv[2].split(',')] if len(sys.argv) > 2 and sys.argv[2] else []
p = json.load(open('vo/probe.json')); d = np.array(p['data']); hz = p['hz']
n = int(len(d) / hz * SR); tt = np.arange(n) / SR; ts = np.arange(len(d)) / hz
col = lambda k: np.interp(tt, ts, d[:, k])
needle, burn, knock, doc, dpf = col(0), col(1), col(2), col(3), col(4)
rng = np.random.default_rng(11)
bp = lambda x, lo, hi, o=2: sosfilt(butter(o, [lo, hi], btype='band', fs=SR, output='sos'), x)
lp = lambda x, fc, o=2: sosfilt(butter(o, fc, btype='low', fs=SR, output='sos'), x)
def smooth(x, ms):
    w = max(1, int(ms / 1000 * SR)); c = np.cumsum(np.concatenate([[0.0], x])); y = (c[w:] - c[:-w]) / w
    return np.concatenate([np.full(w // 2, y[0]), y, np.full(len(x) - len(y) - w // 2, y[-1])])
cyl = np.ones(n)                                     # cylinder sounds fade down while the camera is on the exhaust line
for a, b in MUTE: cyl *= 1 - 0.85 * np.clip(np.minimum((tt - a) / .25, (b - tt) / .25), 0, 1)
L = np.zeros(n); R = np.zeros(n)
def add(t0, x, g=1.0, pan=0.0):
    i = int(round(t0 * SR));
    if i >= n or i < 0: return
    m = min(len(x), n - i); k = g * cyl[i]
    L[i:i + m] += x[:m] * k * (1 - .35 * max(0, pan)); R[i:i + m] += x[:m] * k * (1 + .35 * min(0, pan))

# 1 · spray: high hiss + a little body, following the needle lift
env = smooth(np.clip(needle, 0, 1), 10) ** 1.25
env *= .45 + .55 * np.clip((tt - 1.1) / .8, 0, 1)      # the very first words of the hook stay clear of the hiss
for ch, seed in ((L, 1), (R, 2)):
    nz = np.random.default_rng(seed).standard_normal(n)
    ch += (bp(nz, 3200, 11000) * .085 + bp(nz, 900, 2600) * .03) * env * cyl

# 2 · injector clicks (solenoid / needle seat) at every opening and closing
def click(g):
    m = int(.03 * SR); t = np.arange(m) / SR
    return (bp(rng.standard_normal(m), 2200, 6500) * np.exp(-t * 380) + .5 * np.sin(2 * np.pi * 1750 * t) * np.exp(-t * 260)) * g
x = np.clip(d[:, 0], 0, 1)
ups = np.where((x[1:] > .05) & (x[:-1] <= .05))[0] / hz; dns = np.where((x[1:] <= .05) & (x[:-1] > .05))[0] / hz
for t0 in ups: add(t0, click(.30), pan=.4)
for t0 in dns: add(t0, click(.17), pan=-.4)

# 3 · combustion: thump at ignition + low rumble while it burns; the missing pilot gives the hard knock
def thump(g, f0=62, df=70, dec=7.0, dur=.8):
    m = int(dur * SR); t = np.arange(m) / SR; f = f0 + df * np.exp(-t * 20)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * dec) * np.minimum(1, t / .004) * g
def clack(g):
    m = int(.5 * SR); t = np.arange(m) / SR
    ring = sum(a * np.sin(2 * np.pi * f * t + ph) * np.exp(-t * dk) for f, a, dk, ph in
               [(940, 1.0, 34, 0), (1720, .8, 46, 1.1), (2630, .55, 60, .4), (3850, .35, 85, 2.0), (5300, .2, 120, .7)])
    snap = bp(rng.standard_normal(m), 900, 5200) * np.exp(-t * 110) * 1.5
    return (ring * .5 + snap) * np.minimum(1, t / .0015) * g
b = d[:, 1]; on = np.where((b[1:] > .12) & (b[:-1] <= .12))[0]
for i in on:
    t0 = i / hz; kn = d[min(len(d) - 1, i + 3), 2] > .5; peak = b[i:i + int(1.5 * hz)].max()
    if kn:
        add(t0, thump(1.0, 55, 120, 5.0, 1.0)); add(t0, clack(.95))
        add(t0 + .135, clack(.42), pan=.5); add(t0 + .27, clack(.22), pan=-.5)
    else:
        add(t0, thump(.2 + .34 * min(1, peak)))
rum = lp(rng.standard_normal(n), 170) * smooth(np.clip(burn, 0, 1.7), 40) * .5 * cyl
L += rum; R += np.roll(rum, 211)

# 4 · catalyst and soot burning: soft roar with crackle
fl = .55 + .45 * np.clip(lp(rng.standard_normal(n), 9) * 6, -1, 1)
lvl = smooth(.55 * doc + .8 * dpf, 120)
for ch, seed in ((L, 5), (R, 6)):
    nz = np.random.default_rng(seed).standard_normal(n)
    ch += bp(nz, 260, 1900) * fl * lvl * .16
pops = (rng.random(n) < 14 / SR) * dpf
for i in np.where(pops > 0)[0]:
    m = int(.012 * SR); t = np.arange(m) / SR; x = bp(rng.standard_normal(m), 1500, 7000) * np.exp(-t * 500) * (.10 + .14 * rng.random())
    k = min(m, n - i); pan = rng.random(); L[i:i + k] += x[:k] * pan; R[i:i + k] += x[:k] * (1 - pan)

y = np.stack([L, R], 1)
fade = int(.02 * SR); y[:fade] *= np.linspace(0, 1, fade)[:, None]; y[-fade:] *= np.linspace(1, 0, fade)[:, None]
pk = np.abs(y).max();
if pk > .89: y *= .89 / pk
sf.write(out, y.astype(np.float32), SR, subtype='FLOAT')
rms = lambda a, b_: 20 * np.log10(np.sqrt(np.mean(y[int(a * SR):int(b_ * SR)] ** 2)) + 1e-9)
print('bed', out, 'dur %.2f s' % (n / SR), 'peak %.2f' % np.abs(y).max(), 'knocks', [round(i / hz, 2) for i in on if d[min(len(d) - 1, i + 3), 2] > .5])
print('rms dB: hook main spray %.1f | chapter-2 spray %.1f | knock %.1f | regen %.1f | quiet %.1f' % (rms(2.5, 4.2), rms(36, 39), rms(29.0, 29.5), rms(64, 66), rms(8, 9)))
