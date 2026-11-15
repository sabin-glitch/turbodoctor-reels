"""Verificarea mixului final (nu îl pot asculta, deci îl recunosc): fiecare rând din vo/cues.json este tăiat din mix și trecut prin Parakeet și Whisper.
  ./run_iso.sh mix_qc.py <reel>/audio/mix_final.wav   -> pe rând: potrivirea cu textul (0..1) la fiecare recunoaștere; la final hook-ul întreg (rândurile 0-1, cu sunetul dintre ele)"""
import os, sys, json, re, difflib, unicodedata, subprocess
import numpy as np, sherpa_onnx
M = os.environ.get("TD_MODELS", "/home/claude/models"); PK = M + "/sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8"; WH = M + "/sherpa-onnx-whisper-turbo"
H = os.path.dirname(os.path.abspath(__file__)); S = json.load(open(H + "/vo_script.json")); C = json.load(open(H + "/vo/cues.json"))
pk = sherpa_onnx.OfflineRecognizer.from_transducer(encoder=f"{PK}/encoder.int8.onnx", decoder=f"{PK}/decoder.int8.onnx", joiner=f"{PK}/joiner.int8.onnx",
                                                   tokens=f"{PK}/tokens.txt", num_threads=2, model_type="nemo_transducer")
wh = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=f"{WH}/turbo-encoder.int8.onnx", decoder=f"{WH}/turbo-decoder.int8.onnx", tokens=f"{WH}/turbo-tokens.txt",
                                                language="ro", task="transcribe", num_threads=2)
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", sys.argv[1], "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True, check=True).stdout
X = np.frombuffer(raw, np.float32).copy()
def norm(s):
    s = unicodedata.normalize("NFD", s.lower()); s = "".join(c for c in s if unicodedata.category(c) != "Mn"); return re.sub(r"[^a-z0-9 ]", "", s.replace("-", " "))
def said(t): return re.sub(r"\{[^|}]*\|([^}]*)\}", r"\1", t)
def rec(r, x):
    s = r.create_stream(); s.accept_waveform(16000, np.concatenate([np.zeros(3200, np.float32), x, np.zeros(4800, np.float32)])); r.decode_stream(s); return s.result.text.strip()
def sim(a, b): return difflib.SequenceMatcher(None, norm(a).split(), norm(b).split()).ratio()
worst = 1
for i, l in enumerate(C["lines"]):
    x = X[int(max(0, l["start"] - .15) * 16000):int((l["end"] + .2) * 16000)]; t = said(S[i]["text"]); p, w = rec(pk, x), rec(wh, x); sp, sw = sim(t, p), sim(t, w); worst = min(worst, max(sp, sw))
    print(f"[{i:2d}] P {sp:.2f}  W {sw:.2f}" + ("" if min(sp, sw) > .999 else f"\n      T: {t}\n      P: {p}\n      W: {w}"))
x = X[:int((C["lines"][1]["end"] + .3) * 16000)]; print("hook întreg (cu sunetul):\n      P:", rec(pk, x), "\n      W:", rec(wh, x))
print("cea mai slabă potrivire (cea mai bună dintre cele două recunoașteri):", round(worst, 2))
