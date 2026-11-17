"""Snap phrase-initial words to the acoustic speech onsets (voice envelope), in one pass: python3 snap_words.py <reel_dir> [index=time ...]
Run after build_timeline.py and before retime.py. Parakeet's token times come up to ~0.3 s early after a pause; cards and captions are
anchored on words, so the first word of every speech run is moved to the run's real onset. "index=time" = manual override for word #index
of out/timeline.json. Only valid for cuts:false / speed 1.0, no cold open (os == s). Writes out/speech_runs.json.
The automatic alternative to check_words.py + out/word_fix.json + pipeline/fix_words.py (which also works with a cold open)."""
import json, sys, os, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
ARGS = sys.argv[1:]; ROOT = ARGS.pop(0) if ARGS and "=" not in ARGS[0] else (os.environ.get("REEL_ROOT") or os.getcwd())
tl = json.load(open(f"{ROOT}/out/timeline.json")); assert not tl.get("speed"), "run before retime.py"
assert len([s for s in tl["segments"] if s["kind"] == "story"]) == 1 and not tl["cold_words"], "cuts:false only"
x, sr = sf.read(f"{ROOT}/audio/src48.wav", dtype="float32")
if x.ndim > 1: x = x.mean(1)
xb = sosfilt(butter(4, [180, 3800], btype="band", fs=sr, output="sos"), x)
hop = int(sr * 0.01); n = len(xb) // hop
db = 20 * np.log10(np.sqrt((xb[:n * hop].reshape(n, hop) ** 2).mean(1) + 1e-12)); db = np.convolve(db, np.ones(3) / 3, mode="same")
floor, peak = np.percentile(db, 10), np.percentile(db, 97); act = db > floor + 0.38 * (peak - floor)
runs = []; i = 0
while i < n:
    if act[i]:
        j = i
        while j < n and act[j]: j += 1
        runs.append([i * 0.01, j * 0.01]); i = j
    else: i += 1
m = []
for a, b in runs:
    if m and a - m[-1][1] < 0.12: m[-1][1] = b
    else: m.append([a, b])
runs = [(a, b) for a, b in m if b - a >= 0.05]
def run_of(t, pad=0.03):
    for k, (a, b) in enumerate(runs):
        if a - pad <= t < b: return k
    return None
W = tl["words"]; manual = dict(a.split("=") for a in ARGS)   # "idx=time" overrides (word index in the timeline)
moved = []
for i, w in enumerate(W):
    s0 = w["s"]; k = run_of(s0)
    if str(i) in manual: w["s"] = float(manual[str(i)])
    elif k is None:                       # the word "starts" in silence -> the next speech onset
        nx = [a for a, b in runs if a > s0]
        if nx and nx[0] - s0 <= 0.5: w["s"] = round(nx[0], 3)
    elif runs[k][1] - s0 <= 0.08 and k + 1 < len(runs) and runs[k + 1][0] - runs[k][1] <= 0.3:   # at the very end of a run -> it belongs to the next one
        w["s"] = round(runs[k + 1][0], 3)
    if abs(w["s"] - s0) > 1e-6: moved.append((i, w["text"], s0, w["s"]))
for i in range(1, len(W)):
    if W[i]["s"] <= W[i - 1]["s"] + 0.06: W[i]["s"] = round(W[i - 1]["s"] + 0.08, 3)
DUR = len(x) / sr
for i, w in enumerate(W):
    k = run_of(w["s"]); nxt = W[i + 1]["s"] if i + 1 < len(W) else DUR
    e = nxt
    if k is not None and (i + 1 == len(W) or run_of(nxt) != k): e = min(nxt, runs[k][1] + 0.05)
    w["e"] = round(min(max(e, w["s"] + 0.08), w["s"] + 1.1), 3); w["os"] = w["s"]; w["oe"] = w["e"]
json.dump(tl, open(f"{ROOT}/out/timeline.json", "w"), ensure_ascii=False, indent=1)
json.dump(runs, open(f"{ROOT}/out/speech_runs.json", "w"))
for i, t, a, b in moved: print(f"  #{i} {t}: {a:.2f} -> {b:.2f}")
print("words moved:", len(moved), " runs:", len(runs))
