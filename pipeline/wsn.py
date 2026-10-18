"""Whisper + Parakeet on narrow windows: python3 wsn.py a-b [a-b ...] (run in reel folder)"""
import sys, soundfile as sf, sherpa_onnx
M = "/home/claude/models"
x, sr = sf.read("audio/voice16k.wav", dtype="float32")
wh = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=f"{M}/sherpa-onnx-whisper-turbo/turbo-encoder.int8.onnx", decoder=f"{M}/sherpa-onnx-whisper-turbo/turbo-decoder.int8.onnx",
    tokens=f"{M}/sherpa-onnx-whisper-turbo/turbo-tokens.txt", language="ro", task="transcribe", num_threads=2)
for w in sys.argv[1:]:
    a, b = map(float, w.split("-")); s = wh.create_stream(); s.accept_waveform(sr, x[int(a * sr):int(b * sr)]); wh.decode_stream(s)
    print(f"[{a}-{b}] {s.result.text}")
