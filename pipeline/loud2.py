"""Two-pass loudness for a short reel: python3 loud2.py [target LUFS, default -14]   (run after audio.py, in the reel folder)
audio.py normalises audio/mix_pre.wav in one pass; on a clip of ~20 s that opens with a hook boom and ends with a quiet end
card, the one-pass loudnorm lands 2-3 LU under the target. This measures first, then applies the measured values, and
writes audio/mix_final.wav again (the one-pass result stays in audio/mix_final_1pass.wav)."""
import os, sys, json, re, subprocess, shutil
ROOT = os.environ.get("REEL_ROOT") or os.path.dirname(os.path.abspath(__file__)); I = float(sys.argv[1]) if len(sys.argv) > 1 else -14.0
src = f"{ROOT}/audio/mix_pre.wav"; out = f"{ROOT}/audio/mix_final.wav"
if not os.path.exists(f"{ROOT}/audio/mix_final_1pass.wav"): shutil.copyfile(out, f"{ROOT}/audio/mix_final_1pass.wav")
flt = f"loudnorm=I={I}:TP=-1.5:LRA=11"
r = subprocess.run(["ffmpeg", "-hide_banner", "-i", src, "-af", flt + ":print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
m = json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r, re.S).group(0))
f2 = flt + f":measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true"
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", src, "-af", f2, "-ar", "48000", "-c:a", "pcm_s16le", out], check=True)
r = subprocess.run(["ffmpeg", "-hide_banner", "-i", out, "-af", "loudnorm=print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
o = json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r, re.S).group(0))
print(f"mix_pre {m['input_i']} LUFS, TP {m['input_tp']}  ->  mix_final {o['input_i']} LUFS, TP {o['input_tp']} dBTP, LRA {o['input_lra']}")
