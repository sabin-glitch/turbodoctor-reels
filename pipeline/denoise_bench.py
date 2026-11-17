"""Turn down a steady machine noise (test bench, compressor) under the presenter's voice, before audio.py.
Usage (in the reel folder): python3 denoise_bench.py a-b [a-b ...]   -> the ranges are stretches with noise only (no speech).
audio/src48.wav is replaced by the cleaned track; the untouched sound stays in audio/src48_orig.wav.

Why: the bench runs during the whole clip at about -20 dBFS, with the voice only ~8 dB above it. The voice chain in
audio.py (compressor + loudnorm) then lifts the noise to ~4 dB under the voice. A stationary spectral gate with the noise
profile taken from the clip itself (noisereduce, 4096-point FFT, 85 % reduction) brings it to ~13 dB under the voice and
leaves the bench audible as a low hum. Needs: pip install noisereduce."""
import os, sys, shutil
import numpy as np, soundfile as sf, noisereduce as nr

ROOT = os.environ.get("REEL_ROOT") or os.path.dirname(os.path.abspath(__file__)); SR = 48000
P = f"{ROOT}/audio/src48.wav"; O = f"{ROOT}/audio/src48_orig.wav"
if not os.path.exists(O): shutil.copyfile(P, O)
x, sr = sf.read(O, dtype="float32"); assert sr == SR
mono = x if x.ndim == 1 else x.mean(1)
rng = [tuple(map(float, a.split("-"))) for a in sys.argv[1:]]; assert rng, "give at least one noise-only range a-b (seconds)"
noise = np.concatenate([mono[int(a * SR):int(b * SR)] for a, b in rng])
y = nr.reduce_noise(y=mono, sr=SR, y_noise=noise, stationary=True, prop_decrease=.85, n_fft=4096, n_std_thresh_stationary=2.0).astype(np.float32)
sf.write(P, y, SR, subtype="PCM_24")
db = lambda s: 20 * np.log10(np.sqrt(np.mean(s ** 2)) + 1e-9)
a, b = rng[np.argmax([q - p for p, q in rng])]
print(f"denoised: noise {db(mono[int(a * SR):int(b * SR)]):.1f} dB -> {db(y[int(a * SR):int(b * SR)]):.1f} dB (range {a}-{b}), profile {len(noise) / SR:.1f} s")
