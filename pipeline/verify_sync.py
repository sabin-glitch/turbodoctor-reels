import os
import json, numpy as np, soundfile as sf, sherpa_onnx
from scipy.signal import resample_poly
M = os.environ.get("TD_MODELS", "/home/claude/models") + "/sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8"
rec = sherpa_onnx.OfflineRecognizer.from_transducer(encoder=f"{M}/encoder.int8.onnx", decoder=f"{M}/decoder.int8.onnx",
    joiner=f"{M}/joiner.int8.onnx", tokens=f"{M}/tokens.txt", num_threads=1, model_type="nemo_transducer")
x, sr = sf.read("audio/mix_final.wav", dtype="float32"); x = x.mean(1)
x16 = resample_poly(x, 1, 3).astype(np.float32)
tl = json.load(open("out/timeline.json"))
import sys
# usage: python3 verify_sync.py 0-4.5,55-60.5   (output-time windows; default = 4 windows spread over the story)
if len(sys.argv) > 1: WINS = [tuple(map(float, w.split("-"))) for w in sys.argv[1].split(",")]
else:
    se = tl["story_end"]; WINS = [(0, 5)] + [(round(se * f, 1), round(se * f + 5.5, 1)) for f in (.3, .6, .9)]
for a, b in WINS:
    s = rec.create_stream(); s.accept_waveform(16000, x16[int(a*16000):int(b*16000)]); rec.decode_stream(s)
    words = [(t, round(a + ts, 2)) for t, ts in zip(s.result.tokens, s.result.timestamps) if t.startswith(' ')]
    print(f"[{a}-{b}] {s.result.text}\n   heard word starts: {words}")
    print("   timeline:", [(w['text'], w['os']) for w in tl['words'] if a <= w['os'] < b])
