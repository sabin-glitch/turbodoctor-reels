"""Both recognizers on given audio files (takes).  ./run_iso.sh asrf.py <file> [<file> ...]"""
import sys, subprocess
import numpy as np, sherpa_onnx
M = "/home/claude/models"; PK = M + "/sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8"; WH = M + "/sherpa-onnx-whisper-turbo"
pk = sherpa_onnx.OfflineRecognizer.from_transducer(encoder=f"{PK}/encoder.int8.onnx", decoder=f"{PK}/decoder.int8.onnx", joiner=f"{PK}/joiner.int8.onnx", tokens=f"{PK}/tokens.txt", num_threads=2, model_type="nemo_transducer")
wh = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=f"{WH}/turbo-encoder.int8.onnx", decoder=f"{WH}/turbo-decoder.int8.onnx", tokens=f"{WH}/turbo-tokens.txt", language="ro", task="transcribe", num_threads=4)
def rec(r, x):
    s = r.create_stream(); s.accept_waveform(16000, np.concatenate([np.zeros(3200, np.float32), x, np.zeros(4800, np.float32)])); r.decode_stream(s); return s.result.text.strip()
for f in sys.argv[1:]:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.float32).copy()
    print(f"{f.split('/')[-1]}  {len(x)/16000:.2f}s\n  P: {rec(pk, x)}\n  W: {rec(wh, x)}", flush=True)
