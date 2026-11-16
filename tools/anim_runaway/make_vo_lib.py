"""Voice track for the injection explainer reel.
  python3 make_vo.py piper            -> stand-in narrator (Piper ro_RO-mihai, deepened like vo_narrator.py), lines placed one after another
  python3 make_vo.py take <file.mp3>  -> a real recording / ElevenLabs take of the same text: lines are found in it by ASR + char alignment
  python3 make_vo.py lines <dir>      -> every line generated on its own (<dir>/*L<NN><x>.* = take x of line NN); the pick per line is measured
Writes vo/vo_track.wav (48 kHz), vo/timeline.json (pipeline narrator format, story_end = END), vo/cues.json for the animation director."""
import os, sys, json, re, glob, difflib, unicodedata, subprocess
import numpy as np, soundfile as sf, sherpa_onnx
from scipy.signal import resample_poly

HERE = os.path.dirname(os.path.abspath(__file__)); SR = 48000
M = os.environ.get("TD_MODELS", "/home/claude/models"); D = M + "/tts/vits-piper-ro_RO-mihai-medium"

TAIL = float(os.environ.get("VO_TAIL", "1.0")); END_CARD = float(os.environ.get("VO_END", "7.5"))
PK = M + "/sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8"
asr = sherpa_onnx.OfflineRecognizer.from_transducer(encoder=f"{PK}/encoder.int8.onnx", decoder=f"{PK}/decoder.int8.onnx",
    joiner=f"{PK}/joiner.int8.onnx", tokens=f"{PK}/tokens.txt", num_threads=2, model_type="nemo_transducer")


def norm(s):
    s = unicodedata.normalize("NFD", s.lower()); s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return "".join(c for c in s if c.isalnum())


def parse(text):
    out = []
    for part in re.split(r"(\{[^}]*\})", text):
        if not part: continue
        if part.startswith("{"):
            show, say = part[1:-1].split("|"); out.append([show, say.split()]); continue
        for w in part.split():
            if out and re.fullmatch(r"[,.;:!?]+", w): out[-1][0] += w; continue
            out.append([w, [w]])
    return out


def heard(x16):
    s = asr.create_stream(); s.accept_waveform(16000, np.concatenate([np.zeros(1600, np.float32), x16, np.zeros(3200, np.float32)])); asr.decode_stream(s)
    return list(s.result.tokens), [float(t) - 0.1 for t in s.result.timestamps], s.result.text


def char_tl(toks, ts):
    chars, times = [], []
    for k, tok in enumerate(toks):
        t0 = ts[k]; t1 = ts[k + 1] if k + 1 < len(ts) else t0 + .24; n = norm(tok)
        for j, ch in enumerate(n): chars.append(ch); times.append(t0 + (t1 - t0) * j / max(1, len(n)))
    return "".join(chars), times


