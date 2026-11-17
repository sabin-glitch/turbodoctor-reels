"""Hook-ul „turometru care accelerează puternic” (Audi A7 biturbo, 17.11.2026): sunetul turometrului și curba lui de turație, din ACEEAȘI sursă.
Sursa: o turare reală de turbodiesel până la limitator (Freesound 865222, CC0, „3008gtrevving.wav”, Peugeot 3008 1.5 BlueHDi), redată cu viteză
variabilă (fără time-stretch): urcarea reală 822 -> 3.927 rpm e adusă la ~0,8 s (prima turare) și ~0,63 s (a doua), cu înălțimea crescând continuu.
Acul turometrului NU e animat separat: turația afișată e o funcție afină de frecvența de aprindere a sunetului (ralanti 850 -> limitator 5.300),
deci acul urcă și coboară exact odată cu motorul care se aude.
  python3 build_tach_bed.py <folder reel> <T_top1> <T_top2> <T_end>   -> audio/hook_bed.wav (48 kHz stereo) + out/track_tach.json
T_top1 = momentul în care acul ajunge sus prima dată (titlul „BITURBO”), T_top2 = a doua oară (pe cuvântul lui), T_end = sfârșitul hook-ului."""
import sys, json, os, numpy as np, soundfile as sf
from scipy.signal import resample_poly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from revtrack import track, smooth
R, T_TOP1, T_TOP2, T_END = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
SRC = os.environ.get("TACH_SRC", "/home/claude/snd/fsr_865222.wav"); SR = 48000
x, sr = sf.read(SRC, dtype="float32"); assert sr == SR
mono = x.mean(1).astype(np.float64); src2 = resample_poly(mono, 2, 1)       # 96 kHz for clean fractional reads
F_IDLE, F_TOP = 27.4, 130.6                    # firing frequency of the source: 822 rpm idle, 3.918 rpm on the limiter (4 cylinders: rpm = 30 x Hz)
TA, TJ, TH, TF, TE = 52.20, 53.30, 53.92, 54.30, 56.03   # source: rev starts / jump point in the rise / on the limiter / lift-off / back at idle
IDLE_A = 60.30                                   # a long, clean idle stretch of the same recording
tt, ff, _ = track(mono, SR, 52.2, 56.2); fs = smooth(ff)
def f_src(tau):
    tau = np.asarray(tau, float); f = np.interp(tau, tt, fs)
    u = np.clip((tau - TA) / (52.48 - TA), 0, 1); lo = F_IDLE + (np.interp(52.48, tt, fs) - F_IDLE) * (u * u * (3 - 2 * u))   # the tracker is unreliable below ~45 Hz
    f = np.where(tau < 52.48, lo, f)
    u2 = np.clip((tau - 55.86) / (TE - 55.86), 0, 1); hi = np.interp(55.86, tt, fs) + (F_IDLE - np.interp(55.86, tt, fs)) * (u2 * u2 * (3 - 2 * u2))
    f = np.where(tau > 55.86, hi, f)
    return np.where((tau < TA) | (tau > TE), F_IDLE, f)
R_IDLE, R_TOP = 1.30, 1.35
R_J = R_TOP * F_TOP / float(f_src(TJ))            # rate at the jump point: same pitch before and after the jump onto the limiter
def rate_rise(tau, fast):
    u = np.clip((tau - TA) / (TJ - TA), 0, 1)
    base = R_IDLE + (R_J - R_IDLE) * u            # gentle: 1.30 -> ~1.52
    return base + (0.50 * np.sin(np.pi * u ** 0.75) if fast else 0.0)      # fast: a bump up to ~1.95 in the middle of the rise
def rate_fall(tau):
    u = np.clip((tau - TF) / (TE - TF), 0, 1); return R_TOP + (1.80 - R_TOP) * u
DT = 1 / 4000.0
def integrate(tau0, tau1, rfun):
    taus = [tau0]
    while taus[-1] < tau1: taus.append(taus[-1] + float(rfun(taus[-1])) * DT)
    return np.array(taus)
def piece(taus):                                  # (tau, rate) on the DT grid
    r = np.gradient(taus) / DT; return taus, r
P = {}
PRE0 = 52.06                                     # the rev is read from a little before it starts: one continuous read, no join at the moment it starts
P["rise1"] = piece(integrate(PRE0, TJ, lambda t: R_IDLE if t < TA else rate_rise(t, False)))
P["rise2"] = piece(integrate(PRE0, TJ, lambda t: R_IDLE if t < TA else rate_rise(t, True)))
PRE_S = (TA - PRE0) / R_IDLE                     # seconds of idle before the needle leaves idle
P["hold"] = piece(integrate(TH, TF, lambda t: R_TOP))
P["fall"] = piece(integrate(TF, TE, rate_fall))
dur = {k: len(v[0]) * DT for k, v in P.items()}
print("durations (s):", {k: round(v, 3) for k, v in dur.items()}, " R_J", round(R_J, 3))
XF = 0.05                                         # equal-power crossfade at every join (steady state or same pitch)
n_out = int(round((T_END + 0.2) * SR)); out = np.zeros(n_out); fo = np.full(int(round((T_END + 0.2) / DT)) + 1, np.nan)
def render(taus, rates):
    """variable-rate read of the source along tau(t) given on the DT grid -> samples at SR"""
    n = int(round(len(taus) * DT * SR)); tq = np.arange(n) / SR; tau = np.interp(tq, np.arange(len(taus)) * DT, taus)
    pos = tau * SR * 2; i0 = np.floor(pos).astype(int); fr = pos - i0
    return src2[i0] * (1 - fr) + src2[i0 + 1] * fr
def place(t0, taus, rates, fade_in=XF, fade_out=XF):
    y = render(taus, rates); n = len(y); a = int(round(t0 * SR)); nf_i, nf_o = int(fade_in * SR), int(fade_out * SR)
    w = np.ones(n)
    if nf_i: w[:nf_i] *= np.sin(0.5 * np.pi * np.arange(nf_i) / nf_i)
    if nf_o: w[-nf_o:] *= np.cos(0.5 * np.pi * np.arange(nf_o) / nf_o)
    b = min(n_out, a + n); a0 = max(0, a)
    if b > a0: out[a0:b] += (y * w)[a0 - a:b - a]
    k0 = int(round(t0 / DT)); f = rates * f_src(taus)
    for j in range(len(taus)):
        k = k0 + j
        if 0 <= k < len(fo) and (np.isnan(fo[k]) or (j * DT > fade_in * 0.5)): fo[k] = f[j]
    return t0 + n / SR
def idle(t0, t1, r0, r1, off=0.0):                # idle of the same recording; the rate relaxes r0 -> r1 (the engine settles)
    n = int(round((t1 - t0 + XF) / DT)); u = np.clip(np.arange(n) * DT / max(0.35, 0.6 * (t1 - t0)), 0, 1); r = r0 + (r1 - r0) * u
    taus = IDLE_A + off + np.concatenate([[0], np.cumsum(r[:-1]) * DT]); place(t0, taus, r)
def rev(t_top, fast, hold_s, tag):
    rise = P["rise2" if fast else "rise1"]; t_pre = t_top - dur["rise2" if fast else "rise1"]; t_r = t_pre + PRE_S
    place(t_pre, *rise)
    t = t_top - XF                                                               # jump onto the limiter, same pitch on both sides
    left = hold_s; k = 0; rng = np.random.default_rng(11)
    while left > 1e-3:                                                            # the limiter: one pass, or several overlapped passes for a longer hold
        d = min(dur["hold"] - (XF if left > dur["hold"] else 0), left + XF); off = 0.0 if k == 0 else float(rng.uniform(0.0, 0.05))
        m = int(round(d / DT)); taus = P["hold"][0][:m] + off; taus = taus[taus < TF + 0.02]
        t_new = place(t, taus, P["hold"][1][:len(taus)]); left -= (t_new - t - XF); t = t_new - XF; k += 1
    t_fall = t + XF - XF                                                          # the last limiter pass ends where the real lift-off starts
    t_end = place(t_fall, *P["fall"])
    print(f"{tag}: pre {t_pre:.3f}  rise {t_r:.3f}  top {t_top:.3f}  lift-off {t_fall + XF:.3f}  idle again {t_end:.3f}")
    return t_pre, t_end
a1, e1 = rev(T_TOP1, False, 0.24, "rev 1")
a2, e2 = rev(T_TOP2, True, float(os.environ.get("TACH_HOLD2", "0.72")), "rev 2")
idle(-0.05, a1 + XF, R_IDLE, R_IDLE)
if a2 - e1 > 0.02: idle(e1 - XF, a2 + XF, 1.80, R_IDLE, off=0.9)
else: print("WARN: rev 2 starts before rev 1 is back at idle", e1, a2)
# ---- fill the frequency curve, then the displayed rpm (affine in the firing frequency that is actually heard)
k = np.arange(len(fo)); ok = ~np.isnan(fo); fo = np.interp(k, k[ok], fo[ok])
F0, F1 = R_IDLE * F_IDLE, R_TOP * F_TOP; D0, D1 = 850.0, 5300.0
rpm = D0 + (fo - F0) * (D1 - D0) / (F1 - F0)
# ---- level: natural dynamics of the recording (idle ~16 dB under the limiter); master gain puts the limiter at -13 dBFS RMS
i0, i1 = int((T_TOP1 + 0.03) * SR), int((T_TOP1 + 0.22) * SR); top_rms = np.sqrt(np.mean(out[i0:i1] ** 2)); g = 10 ** (-13 / 20) / top_rms
out *= g
# in-file ducking under his words (v2.json "duck": 0): „Audi 3.0” and „Biturbo”; full level only in the pauses
DUCK = json.loads(os.environ.get("TACH_DUCK", "[]"))      # [[t0, t1, dB], ...] with 0.07 s ramps
t = np.arange(n_out) / SR; gdb = np.zeros(n_out)
for a, b, d in DUCK:
    w = np.clip((t - (a - 0.07)) / 0.07, 0, 1) * np.clip(((b + 0.07) - t) / 0.07, 0, 1); gdb = np.minimum(gdb, d * w)
out *= 10 ** (gdb / 20)
out *= np.clip(t / 0.04, 0, 1) * np.clip((T_END - t) / 0.22, 0, 1)             # in: 40 ms; out: the last 0.22 s of the hook
pk = np.abs(out).max()
if pk > 0.89: out *= 0.89 / pk; print("peak limited", pk)
st = np.stack([out, out], 1).astype(np.float32)
os.makedirs(f"{R}/audio", exist_ok=True); sf.write(f"{R}/audio/hook_bed.wav", st, SR, subtype="PCM_24")
fps = 120; idx = np.clip((np.arange(int(T_END * fps) + 2) / fps / DT).round().astype(int), 0, len(rpm) - 1)
json.dump({"fps": fps, "rpm": [round(float(v), 1) for v in rpm[idx]], "idle": D0, "top": D1, "t_top1": T_TOP1, "t_top2": T_TOP2, "t_end": T_END,
           "src": "Freesound 865222 (CC0) 3008gtrevving.wav"}, open(f"{R}/out/track_tach.json", "w"))
for q in np.arange(0, T_END + 0.01, 0.1): print(f"  t {q:4.1f}  f {fo[int(q / DT)]:6.1f} Hz  rpm {rpm[int(q / DT)]:6.0f}  lvl {20 * np.log10(np.sqrt(np.mean(out[int(q * SR):int(q * SR) + 2400] ** 2)) + 1e-9):6.1f} dB")
print("bed written", n_out / SR, "s  peak", round(float(np.abs(out).max()), 3))
