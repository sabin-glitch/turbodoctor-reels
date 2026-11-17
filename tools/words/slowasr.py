"""Slowed-down ASR check on narrow windows: python3 slowasr.py <reel_dir> <tempo> a-b [a-b ...]
Runs Whisper turbo + Parakeet on the window, time-stretched (ffmpeg atempo) and loudness-normalised."""
import sys, subprocess, tempfile, os, soundfile as sf, sherpa_onnx
R = sys.argv[1]; tempo = float(sys.argv[2]); M = "/home/claude/models"
WH = f"{M}/sherpa-onnx-whisper-turbo"; PK = f"{M}/sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8"
wh = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=f"{WH}/turbo-encoder.int8.onnx", decoder=f"{WH}/turbo-decoder.int8.onnx",
    tokens=f"{WH}/turbo-tokens.txt", language="ro", task="transcribe", num_threads=2)
pk = sherpa_onnx.OfflineRecognizer.from_transducer(encoder=f"{PK}/encoder.int8.onnx", decoder=f"{PK}/decoder.int8.onnx",
    joiner=f"{PK}/joiner.int8.onnx", tokens=f"{PK}/tokens.txt", num_threads=2, model_type="nemo_transducer", decoding_method="greedy_search")
src = sys.argv[3] if sys.argv[3].endswith(".wav") else f"{R}/audio/src48.wav"
wins = [a for a in sys.argv[3:] if not a.endswith(".wav")]
for w in wins:
    a, b = map(float, w.split("-"))
    tmp = tempfile.mktemp(suffix=".wav")
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", str(a), "-t", str(b - a), "-i", src,
                    "-af", f"highpass=f=90,atempo={tempo},dynaudnorm=f=150:g=7", "-ac", "1", "-ar", "16000", tmp], check=True)
    x, sr = sf.read(tmp, dtype="float32"); os.remove(tmp)
    s = wh.create_stream(); s.accept_waveform(sr, x); wh.decode_stream(s)
    p = pk.create_stream(); p.accept_waveform(sr, x); pk.decode_stream(p)
    print(f"[{a}-{b}] x{tempo}\n   W: {s.result.text.strip()}\n   P: {p.result.text.strip()}")
