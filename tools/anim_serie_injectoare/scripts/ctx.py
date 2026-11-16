"""ASR in context: the assembled track around the start of a line.  python3 -I ctx.py <epdir> <line> [pre=1.6] [post=2.6]"""
import sys, json, subprocess
import numpy as np, sherpa_onnx
M = "/home/claude/models"; PK = M + "/sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8"; WH = M + "/sherpa-onnx-whisper-turbo"
E = sys.argv[1].rstrip('/'); i = int(sys.argv[2]); pre = float(sys.argv[3]) if len(sys.argv) > 3 else 1.6; post = float(sys.argv[4]) if len(sys.argv) > 4 else 2.6
C = json.load(open(E + "/vo/cues.json")); L = C['lines'][i]
t0 = max(0, L['start'] - pre); t1 = L['start'] + post
raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t0), "-t", str(t1 - t0), "-i", E + "/vo/vo_track.wav", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True, check=True).stdout
x = np.frombuffer(raw, np.float32).copy()
pk = sherpa_onnx.OfflineRecognizer.from_transducer(encoder=f"{PK}/encoder.int8.onnx", decoder=f"{PK}/decoder.int8.onnx", joiner=f"{PK}/joiner.int8.onnx", tokens=f"{PK}/tokens.txt", num_threads=2, model_type="nemo_transducer")
wh = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=f"{WH}/turbo-encoder.int8.onnx", decoder=f"{WH}/turbo-decoder.int8.onnx", tokens=f"{WH}/turbo-tokens.txt", language="ro", task="transcribe", num_threads=4)
def rec(r):
    s = r.create_stream(); s.accept_waveform(16000, np.concatenate([np.zeros(3200, np.float32), x, np.zeros(4800, np.float32)])); r.decode_stream(s); return s.result.text.strip()
print(f"{E} line {i} @ {L['start']:.2f}s  [{t0:.2f}-{t1:.2f}]\n  P: {rec(pk)}\n  W: {rec(wh)}")
