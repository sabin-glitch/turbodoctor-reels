"""Verificări numerice pe sunetul hook-ului (nu îl pot asculta): turația urmărită independent, nivel, benzi, șuierat, pocnituri."""
import sys, json, numpy as np, soundfile as sf
sys.path.insert(0, "/home/claude/runaway/eng")
from revsweep import comb_scores
from scipy.signal import resample_poly, butter, sosfiltfilt
R = "/home/claude/reels/runaway_diesel"
bed, sr = sf.read(f"{R}/audio/hook_bed.wav", dtype="float32"); eng, _ = sf.read("/tmp/hook_engine_only.wav", dtype="float32")
meta = json.load(open(f"{R}/audio/hook_rpm.json")); T_ON, T_TOP = meta["T_ON"], meta["T_TOP"]
def db(x): return 20 * np.log10(np.sqrt((np.asarray(x, np.float64) ** 2).mean()) + 1e-12)
# 1. turația urmărită independent pe stratul de motor (comb pe armonici), cu continuitate
x = resample_poly(eng.mean(1), 1, 3); s16 = sr // 3
prev = 29.0; out = []
for t in np.arange(0.2, T_TOP + 0.31, 0.1):
    a = int((t - 0.13) * s16); seg = x[max(0, a):a + int(0.26 * s16)]
    c = np.arange(prev * 0.93, prev * 1.22, 0.1); prev = float(c[comb_scores(seg, s16, c).argmax()]); out.append((t, prev))
tt = np.array([o[0] for o in out]); ff = np.array([o[1] for o in out])
m = (tt >= T_ON + 0.2) & (tt <= T_TOP)
A = np.vstack([tt[m], np.ones(m.sum())]).T; sl, ic = np.linalg.lstsq(A, np.log2(ff[m]), rcond=None)[0]
res = np.log2(ff[m]) - (sl * tt[m] + ic)
print(f"f0 urmărit: {ff[0]:.1f} Hz ({30*ff[0]:.0f} rpm) la {tt[0]:.1f}s -> {ff[m][-1]:.1f} Hz ({30*ff[m][-1]:.0f} rpm) la {tt[m][-1]:.1f}s")
print(f"  panta {sl:.3f} octave/s, abatere max de la dreaptă {np.abs(res).max()*1200:.0f} cenți, pași descrescători: {int((np.diff(ff[m]) < -0.3).sum())}")
print("  rpm la fiecare 0,5 s:", [int(round(30 * ff[np.argmin(np.abs(tt - a))])) for a in np.arange(0.5, T_TOP + 0.01, 0.5)])
# 2. nivelul patului (fereastră 0,25 s) și benzi
def band(x, lo, hi):
    sos = butter(4, [lo / (sr / 2), min(hi, sr / 2 - 100) / (sr / 2)], btype="band", output="sos"); return sosfiltfilt(sos, x, axis=0)
B = {"60-250": (60, 250), "250-1k": (250, 1000), "1-2.5k": (1000, 2500), "2.5-5k": (2500, 5000), "5-10k": (5000, 10000)}
bb = {k: band(bed.mean(1), *v) for k, v in B.items()}
print("  t     total   " + "  ".join(f"{k:>7s}" for k in B))
lv = []
for a in np.arange(0, T_TOP + 0.3, 0.25):
    i, j = int(a * sr), int((a + 0.25) * sr); lv.append(db(bed[i:j])); print(f" {a:4.2f}  {lv[-1]:6.1f}   " + "  ".join(f"{db(bb[k][i:j]):7.1f}" for k in B))
lv = np.array(lv); ta = np.arange(0, T_TOP + 0.3, 0.25); mm = (ta >= T_ON) & (ta + 0.25 <= T_TOP)
print(f"  nivel: pași descrescători între ferestre (în urcare): {int((np.diff(lv[mm]) < -0.3).sum())}, creștere totală {lv[mm][-1]-lv[mm][0]:.1f} dB, pas mediu {np.diff(lv[mm]).mean():.2f} dB / 0,25 s, min {np.diff(lv[mm]).min():.2f}, max {np.diff(lv[mm]).max():.2f}")
# 3. șuieratul turbinei față de motor în banda lui (±6 %)
wh = meta["whine_hz"]
print("  șuieratul turbinei: t, frecvență, nivel în banda lui (pat) vs. motorul singur în aceeași bandă")
for a in np.arange(1.0, T_TOP + 0.01, 0.5):
    f0 = wh[int(a * 30)]; i, j = int((a - .12) * sr), int((a + .12) * sr)
    sos = butter(4, [f0 * 0.94 / (sr / 2), f0 * 1.06 / (sr / 2)], btype="band", output="sos")
    print(f"   {a:3.1f}s  {f0:5.0f} Hz   pat {db(sosfiltfilt(sos, bed.mean(1)[i:j])):6.1f} dB   motor {db(sosfiltfilt(sos, eng.mean(1)[i:j] * (10 ** 0))):6.1f} dB")
# 4. pocnituri: salt între eșantioane raportat la RMS-ul local
d = np.abs(np.diff(bed.mean(1))); w = 2400; r = np.sqrt(np.convolve(bed.mean(1) ** 2, np.ones(w) / w, mode="same") + 1e-12)[1:]
k = int(np.argmax(d / (r + 1e-4))); print(f"  salt maxim/RMS local: {float((d / (r + 1e-4)).max()):.2f} la {k / sr:.3f}s (peste ~3 ar fi pocnitură)")
print(f"  vârf {20*np.log10(np.abs(bed).max()):.1f} dBFS, durată {len(bed)/sr:.2f}s, nivel după voce (TV+0.4…): {db(bed[int((T_TOP+0.35+0.4)*sr):]):.1f} dB")
