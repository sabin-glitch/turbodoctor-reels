"""Intelligibility check of the narrator on the FINAL video (voice + music + original sound): ASR (Parakeet) on each narrator line,
cut from the delivered MP4 at the line's place in out/timeline.json, compared with the script text.
Usage: check_mix.py <reel_dir> <final.mp4>   -> one row per line with the match ratio; lines under 0.85 are flagged (07.11.2026)."""
import sys, json, re, difflib, unicodedata, subprocess, os
import numpy as np, soundfile as sf, sherpa_onnx

R, mp4 = sys.argv[1], sys.argv[2]; M = os.environ.get("TD_MODELS", "/home/claude/models"); PK = M + "/sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8"
tmp = "/tmp/_mix16.wav"; subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", mp4, "-vn", "-ac", "1", "-ar", "16000", tmp], check=True)
x, _ = sf.read(tmp, dtype="float32")
tl = json.load(open(f"{R}/out/timeline.json")); script = json.load(open(f"{R}/vo_script.json"))
asr = sherpa_onnx.OfflineRecognizer.from_transducer(encoder=f"{PK}/encoder.int8.onnx", decoder=f"{PK}/decoder.int8.onnx", joiner=f"{PK}/joiner.int8.onnx",
                                                    tokens=f"{PK}/tokens.txt", num_threads=2, model_type="nemo_transducer")
def norm(s):
    s = unicodedata.normalize("NFD", s.lower()); s = "".join(c for c in s if unicodedata.category(c) != "Mn"); return re.sub(r"[^a-z0-9 ]", "", s)
low = 0
for i, L in enumerate(script):
    ws = [w for w in tl["words"] if w["win"] == i]
    if not ws: continue
    a, b = ws[0]["os"] - .15, ws[-1]["oe"] + .25
    st = asr.create_stream(); st.accept_waveform(16000, x[int(a * 16000):int(b * 16000)]); asr.decode_stream(st); heard = st.result.text
    r = difflib.SequenceMatcher(None, norm(L["text"]), norm(heard)).ratio(); low += r < .85
    print(f"[{i:02d}] {a:7.2f}  match {r:.2f}{'  <--' if r < .85 else ''}  {heard[:90]}")
print("lines under 0.85:", low)
