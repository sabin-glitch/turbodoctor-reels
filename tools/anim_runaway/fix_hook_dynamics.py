"""Hook-ul v6: sunetul motorului trebuie să urce CONSTANT până la voce. Normalizarea finală din audio.py (loudnorm dinamic) ridică
începutul mai încet și coboară amplificarea pe măsură ce motorul urcă, deci aplatizează urcarea (măsurat: 14 dB devin ~7 dB, cu paliere).
Aici partea de hook (până după primele cuvinte) e refăcută din mixul de dinainte de normalizare, cu amplificarea constantă pe care
normalizarea o aplică imediat după hook; restul rămâne exact cum îl scoate audio.py. Rulează după audio.py.
  python3 fix_hook_dynamics.py [t_x0=5.55] [t_x1=5.85]"""
import sys, numpy as np, soundfile as sf
from scipy.signal import resample_poly
X0 = float(sys.argv[1]) if len(sys.argv) > 1 else 5.55; X1 = float(sys.argv[2]) if len(sys.argv) > 2 else 5.85
pre, sr = sf.read("audio/mix_pre.wav", dtype="float32"); fin, sr2 = sf.read("audio/mix_final.wav", dtype="float32"); assert sr == sr2
n = min(len(pre), len(fin))
def db(x): return 20 * np.log10(np.sqrt((x.astype(np.float64) ** 2).mean()) + 1e-12)
gs = [db(fin[int(a * sr):int((a + .25) * sr)]) - db(pre[int(a * sr):int((a + .25) * sr)]) for a in np.arange(X0, X0 + 3.0, .25)]
g = float(np.median(gs)); print("loudnorm gain after the hook: %.2f dB (min %.2f, max %.2f)" % (g, min(gs), max(gs)))
hook = pre[:int(X1 * sr) + 1] * 10 ** (g / 20)
# vârfuri: limitare lină doar dacă trece de -1,5 dBTP (măsurat cu supraeșantionare 4x)
tp = float(np.abs(resample_poly(hook, 4, 1, axis=0)).max()); lim = 10 ** (-1.5 / 20)
if tp > lim:
    k = 10 ** (-4.0 / 20); a = np.abs(hook); over = a > k
    hook = np.where(over, np.sign(hook) * (k + (lim * 0.985 - k) * np.tanh((a - k) / (lim * 0.985 - k))), hook)
    print("soft limit applied: true peak %.2f dBFS -> %.2f" % (20 * np.log10(tp), 20 * np.log10(np.abs(resample_poly(hook, 4, 1, axis=0)).max())))
t = np.arange(len(hook)) / sr; w = np.clip((t - X0) / (X1 - X0), 0, 1)[:, None]
out = fin.copy(); out[:len(hook)] = hook * (1 - w) + fin[:len(hook)] * w
sf.write("audio/mix_final.wav", out, sr, subtype="PCM_16")
print("hook levels (0.25 s windows):", " ".join(f"{a:.2f}:{db(out[int(a * sr):int((a + .25) * sr)]):.1f}" for a in np.arange(0, X1 + 1.3, .25)))
