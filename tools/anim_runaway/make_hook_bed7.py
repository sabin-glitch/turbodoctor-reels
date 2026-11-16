"""Sunetul hook-ului v6 (16.11) – „turbina o ia pe ulei”, construit după filmări reale (Jetta 1.9 TDI, hatchback „mad run away diesel”):
motorul pleacă de la ralanti și turația urcă ÎNCONTINUU, fără salturi și fără limitator, până peste turația maximă, iar peste motor
se aude șuieratul turbinei care crește în înălțime și în volum odată cu turația. Fumul din imagine pornește la T_ON și crește până la tăietură,
deci curba de turație pornește tot la T_ON (citit din audio/hook_smoke.json) și urcă până înainte de voce.

Straturi:
 1. motorul: urcarea reală de turație a unui turbodiesel (Freesound 865222, CC0), redată cu viteză variabilă crescătoare (eng/revsweep.py):
    870 rpm → ~6.200 rpm, urcare constantă în octave/secundă;
 2. șuieratul turbinei: ton îngust, cu armonica a doua, a cărui frecvență și volum urcă odată cu turația (sinteză);
 3. jetul de gaze: zgomot filtrat 1,5–7 kHz care crește cu turația (sinteză);
 4. opțional, sunetul clipului Higgsfield cu șoferul (ușa, pașii), încet, de la T_MAN.
Sub vocea lui Sabin (de la T_voce) motorul rămâne doar în fundal, încet, la turația maximă, până la tăietura spre animație
(ca la celelalte hook-uri AI: sunetul scenei stă sub voce).
  python3 make_hook_bed7.py <T_voce> <AICUT> [T_MAN clip_om.mp4]  -> audio/hook_bed.wav (48 kHz stereo) + audio/hook_rpm.json"""
import sys, os, json, subprocess, numpy as np, soundfile as sf
from scipy.signal import resample_poly, butter, sosfilt
sys.path.insert(0, "/home/claude/runaway/eng")
from revsweep import SR, SRC, T_A, T_B, load, track_src, smooth

TV = float(sys.argv[1]); CUT = float(sys.argv[2])
T_MAN = float(sys.argv[3]) if len(sys.argv) > 3 else None
MAN_CLIP = sys.argv[4] if len(sys.argv) > 4 else None
R = "/home/claude/reels/runaway_diesel"
import os
def smoke_onset(default=0.30):         # momentul în care apare fumul în imagine (măsurat de build_hook_v6b.py): turația pornește odată cu el
    try:
        sm = json.load(open(f"{R}/audio/hook_smoke.json")); i = next(k for k, v in enumerate(sm["smoke_pct"]) if v >= 0.1); return max(0.0, i / sm["fps"] - 0.05)
    except Exception: return default
T_ON = float(os.environ["HOOK_T_ON"]) if os.environ.get("HOOK_T_ON") else round(smoke_onset(), 2)
T_TOP = TV - 0.35                  # turația maximă chiar înainte de voce
F_IDLE, F_TOP = 29.0, 196.0        # frecvența de aprindere: 870 rpm → 5.880 rpm (4 cilindri: rpm = 30 × Hz)
RMIN, RMAX, TAU0 = 0.70, 1.60, 11.22
L_IDLE, L_TOP = -26.0, -14.0       # nivelul motorului (dBFS RMS): ralanti → urlet
DUCK = float(os.environ.get("HOOK_DUCK", "-15"))   # sub vocea lui Sabin motorul rămâne în fundal, la turația maximă, cu atât mai încet (dB)
rng = np.random.default_rng(7)

# ---------- 1. motorul: viteza de redare care dă curba de turație
ts, f = track_src(); fs = smooth(f); ipk = int(fs.argmax()); TAU_END = float(ts[ipk]) + 0.50   # după vârf înregistrarea mai ține ~0,5 s la turație mare
f_src = lambda tau: np.interp(tau, ts, fs)
n = int(round(CUT * SR)); t = np.arange(n) / SR
dt = 1 / 2000; tg = np.arange(0, CUT, dt); rg = np.zeros_like(tg); taug = np.zeros_like(tg)
cur = TAU0
for i, ti in enumerate(tg):
    ft = F_IDLE if ti < T_ON else F_IDLE * (F_TOP / F_IDLE) ** min(1.0, (ti - T_ON) / (T_TOP - T_ON))
    ri = min(max(ft / f_src(cur), RMIN), RMAX)              # viteza care ține exact curba-țintă: urcare constantă în octave pe secundă
    rg[i] = ri; taug[i] = cur; cur = min(cur + ri * dt, TAU_END)
k = np.hanning(81); k /= k.sum(); rg = np.convolve(np.pad(rg, 40, mode="edge"), k, mode="valid")      # fără trepte în viteză (40 ms)
taug = TAU0 + np.concatenate([[0], np.cumsum(rg[:-1]) * dt])
tau_fade = float(np.interp(TV + 0.10, tg, taug)); assert tau_fade <= TAU_END + 0.02, ("înregistrarea se termină înainte de voce", tau_fade, TAU_END)
taug = np.minimum(taug, T_B - 0.10)                          # după ce motorul a dispărut sub voce, poziția rămâne pe loc (nu se mai aude)
rate = np.interp(t, tg, rg); tau = np.interp(t, tg, taug)
f_out = rate * f_src(tau)                                   # frecvența de aprindere la ieșire (Hz)
rpm = 30 * f_out
src = load(SRC, T_A, T_B - T_A)                             # stereo 48 kHz
src2 = resample_poly(src, 2, 1, axis=0)                     # 96 kHz pentru interpolare curată
pos = (tau - T_A) * SR * 2
i0 = np.floor(pos).astype(int); fr = (pos - i0)[:, None]
eng = src2[i0] * (1 - fr) + src2[i0 + 1] * fr
u = np.clip(np.log(f_out / F_IDLE) / np.log(F_TOP / F_IDLE), 0, 1)       # 0 la ralanti … 1 la turația maximă
def rms_db(y): return 20 * np.log10(np.sqrt((np.asarray(y, np.float64) ** 2).mean()) + 1e-12)
# volumul urcă și el constant: aduc nivelul motorului (mediat pe ~0,4 s) pe o dreaptă în dB, de la ralanti la urlet
hop = 480; w = int(0.40 * SR); e2 = (eng.astype(np.float64) ** 2).mean(1); cs = np.concatenate([[0], np.cumsum(e2)])
cen = np.arange(0, n, hop); lo = np.clip(cen - w // 2, 0, n); hi = np.clip(cen + w // 2, 0, n)
lvl = 10 * np.log10((cs[hi] - cs[lo]) / np.maximum(hi - lo, 1) + 1e-14)
tgt = L_IDLE + (L_TOP - L_IDLE) * np.clip((cen / SR - T_ON) / (T_TOP - T_ON), 0, 1)
gdb = np.interp(t, cen / SR, tgt - lvl)
eng *= (10 ** (gdb / 20))[:, None]
top = (t > T_TOP - 0.55) & (t < T_TOP + 0.05)
# ---------- 1b. după vârf motorul rămâne la turația maximă (când o ia pe ulei nu mai coboară singur): susținere din porțiunea de turație mare
# a înregistrării, redată la aceeași frecvență de aprindere (granule de 0,28 s suprapuse pe jumătate, din poziții aleatoare, putere constantă)
T_H = T_TOP + 0.04
if CUT > T_H + 0.2:
    g_n = int(0.28 * SR); g_hop = g_n // 2; win = np.sin(np.pi * (np.arange(g_n) + 0.5) / g_n).astype(np.float32)[:, None]
    i_h = int((T_H - 0.14) * SR); sus = np.zeros((n + g_n, 2), np.float32); kk = i_h; blk = 48
    while kk < n:
        cur = rng.uniform(16.72, 17.20); pp = np.empty(g_n)
        for b0 in range(0, g_n, blk):
            r_ = F_TOP / f_src(cur); m_ = min(blk, g_n - b0); pp[b0:b0 + m_] = cur + r_ * np.arange(m_) / SR; cur += r_ * m_ / SR
        q = (pp - T_A) * SR * 2; j0 = np.floor(q).astype(int); fq = (q - j0)[:, None]
        sus[kk:kk + g_n] += (src2[j0] * (1 - fq) + src2[j0 + 1] * fq) * win; kk += g_hop
    sus = sus[:n]; ref_seg = slice(int((T_H + 0.15) * SR), n - 1)
    sus *= 10 ** ((L_TOP - rms_db(sus[ref_seg])) / 20)
    xf = np.clip((t - (T_H - 0.10)) / 0.12, 0, 1)[:, None]                      # trecerea de la urcare la susținere (120 ms, putere constantă)
    eng = eng * np.cos(xf * np.pi / 2) + sus * np.sin(xf * np.pi / 2)
    f_out = np.where(t >= T_TOP, F_TOP, f_out); rpm = 30 * f_out; u = np.clip(np.log(f_out / F_IDLE) / np.log(F_TOP / F_IDLE), 0, 1)

# ---------- 2. șuieratul turbinei (crește în înălțime și în volum odată cu turația)
WH_REL = float(os.environ.get("HOOK_WHINE_REL", "-13"))      # nivelul șuieratului la vârf față de motor (dB)
WH_F0, WH_EXP = float(os.environ.get("HOOK_WHINE_F0", "850")), float(os.environ.get("HOOK_WHINE_EXP", "0.62"))
BREATH = float(os.environ.get("HOOK_WHINE_BREATH", "-7"))    # suflul de aer din jurul tonului, față de ton (dB)
f_w = WH_F0 * (f_out / F_IDLE) ** WH_EXP                     # ~850 Hz la ralanti (neauzit) → ~2,8 kHz la turația maximă
def lp_noise(fc, size):                                      # zgomot trece-jos, normalizat
    sos = butter(2, fc / (SR / 2), output="sos"); y = sosfilt(sos, rng.standard_normal(size)); return y / (y.std() + 1e-12)
jit = 1 + 0.004 * lp_noise(6, n)                             # mică instabilitate a tonului (nu e un sinus curat)
ph = 2 * np.pi * np.cumsum(f_w * jit) / SR + 0.6 * lp_noise(40, n)
am = 1 + 0.22 * lp_noise(18, n)
tone = (np.sin(ph) + 0.20 * np.sin(2 * ph + 1.1) + 0.07 * np.sin(3 * ph + 0.3)) * am
breath = lp_noise(260, n) * np.sin(ph + 0.9) * np.sqrt(2)    # bandă îngustă de zgomot în jurul tonului (aerul prin compresor)
tone_r = np.sqrt((tone ** 2).mean())
whine = tone + breath * tone_r * 10 ** (BREATH / 20)
a_w = u ** 1.7
whine = whine * a_w
whine *= 10 ** ((L_TOP + WH_REL - rms_db(whine[top])) / 20)
# ---------- 3. jetul de gaze
sos = butter(2, [1500 / (SR / 2), 7000 / (SR / 2)], btype="band", output="sos")
hiss = sosfilt(sos, rng.standard_normal((n, 2)), axis=0) * (u ** 2.2)[:, None]
hiss *= 10 ** ((L_TOP - 14.0 - rms_db(hiss[top])) / 20)
mix = eng + whine[:, None] + hiss

# ---------- 4. ușa și pașii din clipul cu șoferul (dacă e dat), încet
if MAN_CLIP and T_MAN is not None:
    a = load(MAN_CLIP, 0, max(0.1, TV - T_MAN + 0.2)); o = int(T_MAN * SR); L = min(len(a), n - o)
    amb = np.zeros((n, 2), np.float32); amb[o:o + L] = a[:L]
    seg = amb[o:o + L]
    if rms_db(seg) > -70:
        amb *= 10 ** ((-27.0 - rms_db(seg)) / 20); mix = mix + amb

# ---------- motorul coboară sub vocea din timpul turării (hook v7: „Turbina o ia pe ulei! Află de ce.”) și revine după ea
# activitatea vocii se citește din audio/vo_track.wav; sub cuvinte, motorul e ținut pe o dreaptă care urcă încet (U0 → +U_SLOPE dB/s),
# în pauza dintre propoziții revine pe jumătate, iar după ultimul cuvânt urcă înapoi la curba lui
U0, U_SLOPE = float(os.environ.get("HOOK_UNDER_DB", "-31")), float(os.environ.get("HOOK_UNDER_SLOPE", "1.6"))
vduck = np.zeros(n); voice_iv = []
try:
    vx, vsr = sf.read(f"{R}/audio/vo_track.wav", dtype="float32", frames=int(TV * 48000)); vx = vx.mean(1) if vx.ndim > 1 else vx
    hv = int(.01 * vsr); ev = np.sqrt((vx[:len(vx) // hv * hv].reshape(-1, hv) ** 2).mean(1)); on = 20 * np.log10(ev + 1e-9) > -45
    on[int((TV - 0.25) * 100):] = False                      # rândul de la TV are coborârea lui (DUCK)
    ed = np.flatnonzero(np.diff(np.concatenate([[0], on.astype(int), [0]]))); iv = [(a * .01, b * .01) for a, b in zip(ed[::2], ed[1::2])]
    for a, b in iv:                                          # lipesc golurile scurte (consoane), păstrez pauzele adevărate
        if voice_iv and a - voice_iv[-1][1] < 0.22: voice_iv[-1] = (voice_iv[-1][0], b)
        elif b - a > 0.04: voice_iv.append((a, b))
except Exception as ex:
    print("no voice track for ducking:", ex)
if voice_iv:
    act = np.zeros(n)
    for a, b in voice_iv:
        act = np.maximum(act, np.clip((t - (a - 0.16)) / 0.12, 0, 1) * np.clip(1 - (t - (b + 0.05)) / 0.55, 0, 1))
    l_nat = L_IDLE + (L_TOP - L_IDLE) * np.clip((t - T_ON) / (T_TOP - T_ON), 0, 1)
    under = U0 + U_SLOPE * (t - voice_iv[0][0])
    vduck = -act * np.maximum(0.0, l_nat - under)
    mix *= (10 ** (vduck / 20))[:, None]
    print("voice during the rev-up:", [(round(a, 2), round(b, 2)) for a, b in voice_iv], " max duck %.1f dB" % vduck.min())

# ---------- anvelopa: intrare scurtă; când începe vocea, motorul coboară repede în fundal și rămâne acolo (urlă mai departe, ca în cadru) până la tăietură
ks = np.array([(0, -60), (.05, 0), (TV - .30, 0), (TV + .05, DUCK), (CUT - .25, DUCK - 1), (CUT - .03, -60), (CUT, -90)], float)
mix *= (10 ** (np.interp(t, ks[:, 0], ks[:, 1]) / 20))[:, None]
pk = np.abs(mix).max(); mix *= min(1.0, 0.85 / pk)
sf.write(f"{R}/audio/hook_bed.wav", mix.astype(np.float32), SR, subtype="FLOAT")
sf.write("/tmp/hook_engine_only.wav", eng.astype(np.float32), SR, subtype="FLOAT")
step = int(SR / 30)
json.dump({"fps": 30, "T_ON": T_ON, "T_TOP": T_TOP, "voice": voice_iv, "rpm": [round(float(x)) for x in rpm[::step]], "whine_hz": [round(float(x)) for x in f_w[::step]],
           "rate": [round(float(x), 3) for x in rate[::step]]}, open(f"{R}/audio/hook_rpm.json", "w"))
print("bed", round(n / SR, 2), "s  peak", round(20 * np.log10(np.abs(mix).max()), 1), "dBFS")
for a in np.arange(0, CUT - .4, .5):
    b = min(a + .5, CUT); i, j = int(a * SR), int(b * SR)
    print(f"  {a:4.1f}s  rpm {rpm[i]:5.0f}  viteza {rate[i]:.2f}  turbina {f_w[i]:5.0f} Hz  nivel {rms_db(mix[i:j]):6.1f} dB  (motor {rms_db(eng[i:j]):6.1f}, turbina {rms_db(whine[i:j]):6.1f})")
