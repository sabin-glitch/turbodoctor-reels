"""Hook v7: sunetul final. Sabin a aprobat sunetul reel-ului v6 („videoclipul acum este bun”) și a cerut doar vocea pe hook.
  - tot ce urmează după hook (de la ~9,8 s) rămâne IDENTIC cu mixul final v6 (aceleași eșantioane);
  - partea de hook (0 … 9,5 s) vine din mixul nou de dinainte de normalizare, cu o amplificare constantă (fără loudnorm dinamic, care
    aplatizează urcarea motorului și schimbă nivelul vocii în funcție de ce e înaintea ei), aleasă ca vocea din hook să fie la nivelul narațiunii;
  - trecerea se face la 9,2–9,8 s, unde e doar muzică (aceeași în ambele), deci nu se aude.
  python3 finish_hook_audio.py [tinta_voce_dB=-15.0]   (rulează după audio.py)"""
import sys, json, numpy as np, soundfile as sf
from scipy.signal import resample_poly
V6 = "/tmp/v6_reel/mix_final.wav"; X0, X1 = 9.2, 9.8
TARGET = float(sys.argv[1]) if len(sys.argv) > 1 else -15.0
pre, sr = sf.read("audio/mix_pre.wav", dtype="float32"); v6, sr2 = sf.read(V6, dtype="float32"); vo, sr3 = sf.read("audio/vo_proc.wav", dtype="float32")
assert sr == sr2 == sr3 and abs(len(pre) - len(v6)) < sr, (len(pre), len(v6))
if v6.ndim == 1: v6 = np.stack([v6, v6], 1)
if pre.ndim == 1: pre = np.stack([pre, pre], 1)
def db(x): return 20 * np.log10(np.sqrt((np.asarray(x, np.float64) ** 2).mean()) + 1e-12)
def act_db(x):
    f = int(.02 * sr); k = len(x) // f; r = np.sqrt((x[:k * f].reshape(k, f) ** 2).mean(1) + 1e-12); a = r[r > r.max() * .1]; return 20 * np.log10(np.sqrt((a ** 2).mean()))
tl = json.load(open("out/timeline.json")); s0, s1 = tl["sentences"][0], tl["sentences"][1]
l0 = act_db(vo[int(s0["start"] * sr):int((s0["end"] + .1) * sr)]); l1 = act_db(vo[int(s1["start"] * sr):int((s1["end"] + .1) * sr)])
g = TARGET - l0
print(f"voice in the pre-mix: line 0 {l0:.1f} dB, line 1 {l1:.1f} dB -> hook gain {g:+.2f} dB (line 0 at {TARGET:.1f}, line 1 at {l1 + g:.1f})")
n1 = int(X1 * sr) + 1; hook = pre[:n1] * 10 ** (g / 20)
tp = float(np.abs(resample_poly(hook, 4, 1, axis=0)).max()); lim = 10 ** (-1.5 / 20)
if tp > lim:
    k = 10 ** (-4.5 / 20); a = np.abs(hook); top = lim * 0.98
    hook = np.where(a > k, np.sign(hook) * (k + (top - k) * np.tanh((a - k) / (top - k))), hook)
    print("soft limit: true peak %.2f dBFS -> %.2f" % (20 * np.log10(tp), 20 * np.log10(np.abs(resample_poly(hook, 4, 1, axis=0)).max())))
t = np.arange(n1) / sr; w = np.clip((t - X0) / (X1 - X0), 0, 1)[:, None]
out = v6.copy(); out[:n1] = hook * (1 - w) + v6[:n1] * w
m = slice(int(X0 * sr), int(X1 * sr)); print(f"crossfade {X0}-{X1} s: new part {db(hook[m]):.1f} dB vs v6 {db(v6[m]):.1f} dB (music only)")
sf.write("audio/mix_final.wav", out, sr, subtype="PCM_16")
assert np.array_equal(sf.read("audio/mix_final.wav", dtype="int16", start=int(10 * sr), frames=sr * 5)[0], sf.read(V6, dtype="int16", start=int(10 * sr), frames=sr * 5)[0]), "tail differs from v6"
print("0.25 s windows:", " ".join(f"{a:.2f}:{db(out[int(a * sr):int((a + .25) * sr)]):.1f}" for a in np.arange(0, 10.01, .25)))
