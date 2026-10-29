"""Voice/music separation with UVR MDX-Net (sherpa-onnx). Usage: sep_voice.py <in.wav 44.1k> <vocals.wav> [<rest.wav>] [model]"""
import sys, time
import numpy as np, soundfile as sf, sherpa_onnx
inp, outv = sys.argv[1], sys.argv[2]
outr = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] != '-' else None
model = sys.argv[4] if len(sys.argv) > 4 else "/home/claude/models/sep/UVR-MDX-NET-Voc_FT.onnx"
cfg = sherpa_onnx.OfflineSourceSeparationConfig(model=sherpa_onnx.OfflineSourceSeparationModelConfig(
    uvr=sherpa_onnx.OfflineSourceSeparationUvrModelConfig(model=model), num_threads=2, debug=False, provider="cpu"))
assert cfg.validate()
sp = sherpa_onnx.OfflineSourceSeparation(cfg)
x, sr = sf.read(inp, dtype="float32", always_2d=True)
t = time.time(); out = sp.process(sample_rate=sr, samples=np.ascontiguousarray(x.T))
print(f"stems={len(out.stems)} sr={out.sample_rate} took {time.time()-t:.1f}s for {len(x)/sr:.1f}s", file=sys.stderr)
v = np.asarray(out.stems[0].data); sf.write(outv, v.T, out.sample_rate)
if outr: sf.write(outr, np.asarray(out.stems[1].data).T, out.sample_rate)
