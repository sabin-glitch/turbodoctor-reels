"""Second pass: re-transcribe with longer context windows (merged VAD segments) so both models
see full sentences. Keeps Parakeet token timestamps (absolute)."""
import os
import json, sys
import numpy as np, soundfile as sf, sherpa_onnx

ROOT = os.environ.get("REEL_ROOT") or os.path.dirname(os.path.abspath(__file__)); M = os.environ.get("TD_MODELS", "/home/claude/models")
samples, sr = sf.read(f"{ROOT}/audio/voice16k.wav", dtype="float32")
segs = json.load(open(f"{ROOT}/out/transcript.json"))

# windows chosen by sentence boundaries (pauses) seen in pass 1
WP = f"{ROOT}/out/wins.json"
if os.path.exists(WP):
    wins = [tuple(w) for w in json.load(open(WP))]
else:  # merge pass-1 VAD segments into sentence-sized windows (<= 16 s, split at pauses >= 0.35 s once >= 5 s long)
    wins = []; a = b = None
    for sg in segs:
        if a is None: a, b = sg["start"], sg["end"]; continue
        gap = sg["start"] - b
        if sg["end"] - a > 16 or (gap >= 0.35 and b - a >= 5): wins.append((round(max(0, a - 0.25), 2), round(b + 0.25, 2))); a, b = sg["start"], sg["end"]
        else: b = sg["end"]
    if a is not None: wins.append((round(max(0, a - 0.25), 2), round(b + 0.25, 2)))
    json.dump(wins, open(WP, "w"))
PK = f"{M}/sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8"
parakeet = sherpa_onnx.OfflineRecognizer.from_transducer(
    encoder=f"{PK}/encoder.int8.onnx", decoder=f"{PK}/decoder.int8.onnx",
    joiner=f"{PK}/joiner.int8.onnx", tokens=f"{PK}/tokens.txt",
    num_threads=2, model_type="nemo_transducer", decoding_method="greedy_search")
WH = f"{M}/sherpa-onnx-whisper-turbo"
whisper = sherpa_onnx.OfflineRecognizer.from_whisper(
    encoder=f"{WH}/turbo-encoder.int8.onnx", decoder=f"{WH}/turbo-decoder.int8.onnx",
    tokens=f"{WH}/turbo-tokens.txt", language="ro", task="transcribe", num_threads=2)
res = []
for a, b in wins:
    chunk = samples[int(a * sr):int(b * sr)]
    s1 = parakeet.create_stream(); s1.accept_waveform(sr, chunk); parakeet.decode_stream(s1)
    s2 = whisper.create_stream(); s2.accept_waveform(sr, chunk); whisper.decode_stream(s2)
    r = s1.result
    res.append(dict(start=a, end=b, parakeet=r.text, whisper=s2.result.text.strip(),
                    tokens=list(r.tokens), token_ts=[a + float(t) for t in r.timestamps]))
    print(f"[{a:5.1f}-{b:5.1f}]\n  P: {r.text}\n  W: {s2.result.text.strip()}")
json.dump(res, open(f"{ROOT}/out/transcript_ctx.json", "w"), ensure_ascii=False, indent=1)
