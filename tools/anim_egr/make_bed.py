"""Sound bed for the EGR reel: a metallic clank on every chunk hitting the variable-geometry vanes, and a heavy crunch when the big
chunk is crushed between piston and head. Times come from vo/uframes.json (animation time U on every 30 fps frame).
  python3 make_bed.py <out.wav>"""
import json, sys, os, numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__)); SR = 48000
U = np.array(json.load(open(f"{HERE}/vo/uframes.json"))); N = len(U); dur = json.load(open(f"{HERE}/vo/timeline.json"))["total"]
HIT_T = [46.0, 46.55, 47.0, 47.35, 47.8, 48.15, 48.5, 48.9, 49.25]; U_IMP = 32.2125
def crossings(u):   # frame times where the animation passes u (forward)
    return [(i + (u - U[i]) / (U[i + 1] - U[i])) / 30 for i in range(N - 1) if U[i] < u <= U[i + 1]]
rng = np.random.default_rng(7); out = np.zeros(int(dur * SR), np.float32)
def put(t, y):
    o = int(t * SR); m = min(len(y), len(out) - o)
    if m > 0: out[o:o + m] += y[:m]
def clank(g):
    n = int(.45 * SR); t = np.arange(n) / SR; y = np.zeros(n)
    for f, d, a in [(1870, 9, .5), (2630, 12, .35), (3410, 15, .25), (5200, 22, .15), (930, 7, .3)]:
        f *= rng.uniform(.93, 1.07); y += a * np.sin(2 * np.pi * f * t + rng.uniform(0, 6)) * np.exp(-d * t)
    y += .9 * rng.standard_normal(n) * np.exp(-90 * t); return (g * y / np.abs(y).max()).astype(np.float32)
def crunch():
    n = int(1.1 * SR); t = np.arange(n) / SR
    y = 1.2 * np.sin(2 * np.pi * (70 - 30 * t) * t) * np.exp(-5 * t) + .7 * rng.standard_normal(n) * np.exp(-14 * t)
    y += .4 * np.sin(2 * np.pi * 1450 * t) * np.exp(-11 * t); return (.55 * y / np.abs(y).max()).astype(np.float32)
for h in HIT_T:
    for t in crossings(h): put(t, clank(.32))
for t in crossings(U_IMP): put(t, crunch())
sf.write(sys.argv[1], out, SR); print("bed", len(out) / SR, "s")
