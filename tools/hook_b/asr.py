import sys, numpy as np, soundfile as sf, sherpa_onnx
from scipy.signal import resample_poly
import os
PK = os.environ.get("TD_MODELS", "/home/claude/models") + "/sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8"
asr = sherpa_onnx.OfflineRecognizer.from_transducer(encoder=f"{PK}/encoder.int8.onnx", decoder=f"{PK}/decoder.int8.onnx",
    joiner=f"{PK}/joiner.int8.onnx", tokens=f"{PK}/tokens.txt", num_threads=2, model_type="nemo_transducer")
for p in sys.argv[1:]:
    x, sr = sf.read(p, dtype="float32"); x = x if x.ndim == 1 else x.mean(1); x = resample_poly(x, 16000, sr).astype(np.float32)
    s = asr.create_stream(); s.accept_waveform(16000, x); asr.decode_stream(s); r = s.result
    print(p, "|", r.text)
    print("  ", [(t, round(ts, 2)) for t, ts in zip(r.tokens, r.timestamps)][:80])
