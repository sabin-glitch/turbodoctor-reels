"""Second opinion on every generated take: Parakeet and Whisper side by side (a difference flagged by both is real).
  ./run_iso.sh asr2.py <dir> [line numbers...]"""
import os, sys, re, glob, json, subprocess
import numpy as np, sherpa_onnx
M = os.environ.get("TD_MODELS", "/home/claude/models"); PK = M + "/sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8"; WH = M + "/sherpa-onnx-whisper-turbo"
H = os.path.dirname(os.path.abspath(__file__)); S = json.load(open(H + "/vo_script.json"))
pk = sherpa_onnx.OfflineRecognizer.from_transducer(encoder=f"{PK}/encoder.int8.onnx", decoder=f"{PK}/decoder.int8.onnx", joiner=f"{PK}/joiner.int8.onnx",
                                                   tokens=f"{PK}/tokens.txt", num_threads=2, model_type="nemo_transducer")
wh = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=f"{WH}/turbo-encoder.int8.onnx", decoder=f"{WH}/turbo-decoder.int8.onnx", tokens=f"{WH}/turbo-tokens.txt",
                                                language="ro", task="transcribe", num_threads=4)
def load(f):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()
def rec(r, x):
    s = r.create_stream(); s.accept_waveform(16000, np.concatenate([np.zeros(3200, np.float32), x, np.zeros(4800, np.float32)])); r.decode_stream(s); return s.result.text.strip()
only = set(map(int, sys.argv[2:]))
for f in sorted(glob.glob(sys.argv[1].rstrip("/") + "/*")):
    m = re.search(r"L(\d\d)([a-z])\.[^.]+$", os.path.basename(f))
    if not m or (only and int(m.group(1)) not in only): continue
    x = load(f); i = int(m.group(1))
    print(f"[{i:2d}{m.group(2)}] T: {S[i]['text']}\n      P: {rec(pk, x)}\n      W: {rec(wh, x)}")
