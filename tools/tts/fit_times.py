"""Fit external narrator lines (audio/ext/NN.wav from split_lines.py) on the footage, before vo_external.py.
Usage: fit_times.py <reel_dir> <plan.json>
plan.json: {"t": {"0": 0.2, "3": 21.9, ...}, "tempo": {"0": 1.05, ...}, "gap": 0.3, "hard": [3, 5, 8]}
- tempo: optional speed-up per line (ffmpeg atempo; originals kept in audio/ext/orig/, so re-running is idempotent; <= ~1.07 is not audible)
- t: desired start of a line on the footage (where its step/moment begins); lines without one follow the previous line
- each line's t in vo_script.json becomes max(desired, previous line end + gap); "tip" lines are left as they are
Durations are measured as vo_external.py trims them (-45 dB, 0.05 s lead, 0.08 s tail). Prints the drift of every line vs its
desired start and flags hard lines pushed more than 0.6 s (07.11.2026, asamblare turbină)."""
import sys, os, json, shutil, subprocess
import numpy as np, soundfile as sf

R, plan = sys.argv[1], json.load(open(sys.argv[2]))
EXT = f"{R}/audio/ext"; ORIG = f"{EXT}/orig"; os.makedirs(ORIG, exist_ok=True)
script = json.load(open(f"{R}/vo_script.json"))
want = {int(k): v for k, v in plan.get("t", {}).items()}; tempo = {int(k): float(v) for k, v in plan.get("tempo", {}).items()}
gap = float(plan.get("gap", 0.3)); hard = set(plan.get("hard", []))

def trimmed_dur(path):
    x, sr = sf.read(path, dtype="float32"); x = x if x.ndim == 1 else x.mean(1)
    idx = np.where(np.abs(x) > 10 ** (-45 / 20))[0]
    return (min(len(x), idx[-1] + int(.08 * sr)) - max(0, idx[0] - int(.05 * sr))) / sr

durs = []
for i in range(len(script)):
    f, o = f"{EXT}/{i:02d}.wav", f"{ORIG}/{i:02d}.wav"
    if not os.path.exists(o): shutil.copy(f, o)
    k = tempo.get(i, 1.0)
    if abs(k - 1.0) > 1e-3:
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", o, "-af", f"atempo={k}", "-ar", "48000", "-ac", "1", "-c:a", "pcm_f32le", f], check=True)
    else: shutil.copy(o, f)
    durs.append(trimmed_dur(f))

end, warn = 0.0, 0
for i, L in enumerate(script):
    if "tip" in L:
        print(f"[{i:02d}] tip +{L['tip']:.2f}  dur {durs[i]:5.2f}  -> needs tip section >= {L['tip'] + durs[i] + .3:.2f}s"); continue
    w = want.get(i); start = max(w if w is not None else 0.0, end + gap if i else (w or 0.0))
    drift = start - w if w is not None else None
    flag = "  <-- PUSHED" if (w is not None and drift > .6 and (i in hard or not hard)) else ""
    warn += bool(flag)
    L["t"] = round(start, 2); end = start + durs[i]
    print(f"[{i:02d}] t {start:7.2f} -> {end:7.2f}  dur {durs[i]:5.2f}" + (f"  tempo {tempo[i]}" if i in tempo else "") + (f"  want {w:7.2f}  drift {drift:+.2f}" if w is not None else "") + flag)
json.dump(script, open(f"{R}/vo_script.json", "w"), ensure_ascii=False, indent=1)
print(f"story narration ends at {end:.2f}s;", f"{warn} hard line(s) pushed" if warn else "all hard lines on time")
