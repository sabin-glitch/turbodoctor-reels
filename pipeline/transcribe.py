"""Transcribe voice16k.wav with Parakeet-TDT v3 (word timestamps) and Whisper turbo (text cross-check).
Output: out/transcript.json with VAD segments, parakeet words+times, whisper text per segment."""
import os
import json, sys, time
import numpy as np
import soundfile as sf
import sherpa_onnx

ROOT = os.environ.get("REEL_ROOT") or os.path.dirname(os.path.abspath(__file__))
M = os.environ.get("TD_MODELS", "/home/claude/models")
samples, sr = sf.read(f"{ROOT}/audio/voice16k.wav", dtype="float32")
assert sr == 16000
if samples.ndim > 1:
    samples = samples.mean(axis=1)

# ---- VAD segmentation
cfg = sherpa_onnx.VadModelConfig()
cfg.silero_vad.model = f"{M}/silero_vad.onnx"
cfg.silero_vad.min_silence_duration = 0.30
cfg.silero_vad.min_speech_duration = 0.20
cfg.silero_vad.max_speech_duration = 20
cfg.silero_vad.threshold = 0.45
cfg.sample_rate = sr
vad = sherpa_onnx.VoiceActivityDetector(cfg, buffer_size_in_seconds=200)
win = cfg.silero_vad.window_size
segs = []
i = 0
while i < len(samples):
    vad.accept_waveform(samples[i:i + win]); i += win
    while not vad.empty():
        segs.append((vad.front.start / sr, np.array(vad.front.samples, dtype=np.float32))); vad.pop()
vad.flush()
while not vad.empty():
    segs.append((vad.front.start / sr, np.array(vad.front.samples, dtype=np.float32))); vad.pop()
print(f"{len(segs)} VAD segments", file=sys.stderr)

PK = f"{M}/sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8"
parakeet = sherpa_onnx.OfflineRecognizer.from_transducer(
    encoder=f"{PK}/encoder.int8.onnx", decoder=f"{PK}/decoder.int8.onnx",
    joiner=f"{PK}/joiner.int8.onnx", tokens=f"{PK}/tokens.txt",
    num_threads=2, model_type="nemo_transducer", decoding_method="greedy_search")

WH = f"{M}/sherpa-onnx-whisper-turbo"
whisper = sherpa_onnx.OfflineRecognizer.from_whisper(
    encoder=f"{WH}/turbo-encoder.int8.onnx", decoder=f"{WH}/turbo-decoder.int8.onnx",
    tokens=f"{WH}/turbo-tokens.txt", language="ro", task="transcribe", num_threads=2)

out = []
PAD = 0.15  # context padding around each VAD segment (s)
for k, (st, seg) in enumerate(segs):
    a = max(0, int((st - PAD) * sr)); b = min(len(samples), int((st + len(seg) / sr + PAD) * sr))
    chunk = samples[a:b]; off = a / sr
    t0 = time.time()
    s1 = parakeet.create_stream(); s1.accept_waveform(sr, chunk); parakeet.decode_stream(s1)
    r1 = s1.result
    toks = list(r1.tokens); ts = [off + float(x) for x in r1.timestamps]
    durs = [float(x) for x in getattr(r1, "durations", [])] if hasattr(r1, "durations") else []
    s2 = whisper.create_stream(); s2.accept_waveform(sr, chunk); whisper.decode_stream(s2)
    out.append(dict(i=k, start=round(st, 3), end=round(st + len(seg) / sr, 3), parakeet=r1.text,
                    tokens=toks, token_ts=ts, token_durs=durs, whisper=s2.result.text.strip()))
    print(f"[{st:6.2f}-{st+len(seg)/sr:6.2f}] ({time.time()-t0:.1f}s)\n  P: {r1.text}\n  W: {s2.result.text.strip()}", file=sys.stderr)

json.dump(out, open(f"{ROOT}/out/transcript.json", "w"), ensure_ascii=False, indent=1)
print("done", file=sys.stderr)
