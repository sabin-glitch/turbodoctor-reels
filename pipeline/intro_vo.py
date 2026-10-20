"""Synthetic intro hook (graphics + generated voice) before the clip.
Reads out/intro_script.json {"speed": 1.15, "tail": 0.5, "bg_src": 0.0, "phrases": [{"text": "...", "gap": 0.16}, ...]},
synthesizes each phrase with the Romanian TTS voice, matches its loudness to the presenter (audio/src48.wav),
keeps the clearest of several takes per phrase (the TTS varies from take to take; ASR on the whole sequence, clean and under
a noise bed, scores them; a phrase can instead reuse a verified clip: {"text": ..., "wav": "cta.wav"}, or be spoken
differently from its caption: {"text": "1.500 €", "say": "o mie cinci sute de euro"}),
gets word timings with ASR on the clean TTS audio and writes audio/intro_vo.wav + out/intro.json.
build_timeline.py then starts the story after the intro (story_out0 = intro dur)."""
import os, json, glob, difflib, unicodedata
import numpy as np, soundfile as sf, sherpa_onnx
from scipy.signal import resample_poly, butter, sosfilt

ROOT = os.environ.get("REEL_ROOT") or os.path.dirname(os.path.abspath(__file__)); SR = 48000
M = os.environ.get("TD_MODELS", "/home/claude/models")
cfg = json.load(open(f"{ROOT}/out/intro_script.json"))
D = M + "/tts/vits-piper-ro_RO-mihai-medium"
tts = sherpa_onnx.OfflineTts(sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(
    vits=sherpa_onnx.OfflineTtsVitsModelConfig(model=glob.glob(D + "/*.onnx")[0], lexicon="", data_dir=D + "/espeak-ng-data",
                                               tokens=D + "/tokens.txt", noise_scale=0.6, noise_scale_w=0.75, length_scale=1.0),
    provider="cpu", num_threads=2), max_num_sentences=1))
PK = M + "/sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8"
asr = sherpa_onnx.OfflineRecognizer.from_transducer(encoder=f"{PK}/encoder.int8.onnx", decoder=f"{PK}/decoder.int8.onnx",
    joiner=f"{PK}/joiner.int8.onnx", tokens=f"{PK}/tokens.txt", num_threads=2, model_type="nemo_transducer")


def norm(s):
    s = unicodedata.normalize("NFD", s.lower()); s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return "".join(c for c in s if c.isalnum())


def synth(text, speed):
    a = tts.generate(text, sid=0, speed=speed); x = resample_poly(np.array(a.samples, np.float32), SR, a.sample_rate).astype(np.float32)
    e = np.abs(x); idx = np.where(e > .02 * e.max())[0]; i0 = np.where(e > .004 * e.max())[0][0]  # low threshold at the start keeps soft onsets (T, V)
    return x[max(0, min(i0, idx[0]) - int(.04 * SR)):min(len(x), idx[-1] + int(.06 * SR))]


def speech_rms(x):  # RMS over 20 ms frames that carry speech
    f = int(.02 * SR); n = len(x) // f; r = np.sqrt((x[:n * f].reshape(n, f) ** 2).mean(1) + 1e-12)
    return float(np.sqrt(np.mean(r[r > r.max() * .1] ** 2)))


def word_times(text, x, off):
    s = asr.create_stream(); s.accept_waveform(16000, resample_poly(x, 1, 3).astype(np.float32)); asr.decode_stream(s)
    toks, ts = s.result.tokens, s.result.timestamps
    pch, pt = "", []
    for k, tok in enumerate(toks):
        t0 = ts[k]; t1 = ts[k + 1] if k + 1 < len(ts) else t0 + .2; n = norm(tok)
        for j, c in enumerate(n): pch += c; pt.append(t0 + (t1 - t0) * j / max(1, len(n)))
    ws = text.split(); cst, first = "", []
    for w in ws: first.append(len(cst)); cst += norm(w)
    cmap = {}
    for a, b, size in difflib.SequenceMatcher(None, cst, pch, autojunk=False).get_matching_blocks():
        for q in range(size): cmap[a + q] = b + q
    st = []
    for k, w in enumerate(ws):
        hit = [first[k] + j for j in range(len(norm(w))) if first[k] + j in cmap]
        st.append(pt[cmap[hit[0]]] if hit else None)
    dur = len(x) / SR
    for k in range(len(st)):  # fill gaps by interpolation
        if st[k] is None:
            prv = next((st[j] for j in range(k - 1, -1, -1) if st[j] is not None), 0.0)
            nxt = next((st[j] for j in range(k + 1, len(st)) if st[j] is not None), dur)
            st[k] = (prv + nxt) / 2
    for k in range(1, len(st)): st[k] = max(st[k], st[k - 1] + .06)
    out = []
    for k, w in enumerate(ws):
        e = st[k + 1] - .02 if k + 1 < len(ws) else dur
        out.append(dict(text=w, s=round(off + st[k], 3), e=round(off + max(st[k] + .1, e), 3)))
    return out


src, sr = sf.read(f"{ROOT}/audio/src48.wav", dtype="float32"); src = src.mean(1) if src.ndim > 1 else src
target = speech_rms(src); P = cfg["phrases"]


def clip(p):  # a verified clip (path relative to out/), or a fresh TTS take
    if p.get("wav"):
        y, r = sf.read(os.path.join(f"{ROOT}/out", p["wav"]), dtype="float32"); y = y.mean(1) if y.ndim > 1 else y
        y = resample_poly(y, SR, r).astype(np.float32) if r != SR else y
    else: y = synth(p.get("say", p["text"]), p.get("speed", cfg.get("speed", 1.15)))  # "say": spoken form when it differs from the caption
    return y * target / speech_rms(y) * float(cfg.get("gain", 1.0))


def heard(x, spans):  # ASR on the sequence -> text heard inside each phrase span
    s = asr.create_stream(); s.accept_waveform(16000, resample_poly(x, 1, 3).astype(np.float32)); asr.decode_stream(s)
    return ["".join(tok for tok, ts in zip(s.result.tokens, s.result.timestamps) if a <= ts < b) for a, b in spans]


bed = sosfilt(butter(1, 1200, fs=SR, output="sos"), np.random.default_rng(5).standard_normal(SR * 30)).astype(np.float32)  # music-like noise
best = [(-1.0, None, "")] * len(P)
for k in range(int(cfg.get("takes", 6))):  # per phrase, keep the take the ASR understands best in context, clean and 15 dB under a noise bed
    ys = [best[i][1] if p.get("wav") and k else clip(p) for i, p in enumerate(P)]
    seq, spans, t = [], [], 0.0
    for i, y in enumerate(ys):  # each phrase owns the audio up to the middle of the gaps around it (ASR stamps a word's start early)
        g0 = float(P[i - 1].get("gap", .14)) / 2 if i else 0.0; g1 = float(P[i].get("gap", .14)) / 2
        spans.append((t - g0, t + len(y) / SR + g1)); seq += [y, np.zeros(int(2 * g1 * SR), np.float32)]; t += len(y) / SR + 2 * g1
    x = np.concatenate(seq + [np.zeros(int(.4 * SR), np.float32)]); nz = bed[:len(x)] * (speech_rms(x) / speech_rms(bed[:len(x)]) * 10 ** (-15 / 20))
    for i, (hc, hn) in enumerate(zip(heard(x, spans), heard(x + nz, spans))):
        sc = min(difflib.SequenceMatcher(None, norm(P[i].get("say", P[i]["text"])), norm(h), autojunk=False).ratio() for h in (hc, hn))
        if sc > best[i][0]: best[i] = (sc, ys[i], f"{hc.strip()} / {hn.strip()}")
    if min(b[0] for b in best) > .98: break
for i, b in enumerate(best): print(f"take p{i} {b[0]:.2f} | {P[i]['text']} | heard: {b[2]}")
x = np.concatenate([np.concatenate([b[1], np.zeros(int(float(P[i].get("gap", .14)) * SR), np.float32)]) for i, b in enumerate(best)] + [np.zeros(int(.4 * SR), np.float32)])
s = asr.create_stream(); s.accept_waveform(16000, resample_poly(x, 1, 3).astype(np.float32)); asr.decode_stream(s); print("whole intro heard:", s.result.text)
parts, phrases, words, t = [], [], [], 0.0
for i, p in enumerate(P):
    y = best[i][1]
    phrases.append(dict(t0=round(t, 3), t1=round(t + len(y) / SR, 3), text=p["text"]))
    words += [dict(w, ph=i) for w in word_times(p["text"], y, t)]
    parts.append(y); t += len(y) / SR
    if i < len(P) - 1: g = float(p.get("gap", .14)); parts.append(np.zeros(int(g * SR), np.float32)); t += g
vo = np.concatenate(parts); peak = np.abs(vo).max()
if peak > .98: vo *= .98 / peak
sf.write(f"{ROOT}/audio/intro_vo.wav", vo, SR, subtype="FLOAT")
dur = round(round((t + float(cfg.get("tail", .5))) * 30) / 30, 4)  # whole frames
json.dump(dict(dur=dur, vo_dur=round(t, 3), bg_src=float(cfg.get("bg_src", 0.0)), phrases=phrases, words=words),
          open(f"{ROOT}/out/intro.json", "w"), ensure_ascii=False, indent=1)
print(f"intro {dur}s (voice {t:.2f}s)")
for w in words: print(f"  {w['s']:6.2f}-{w['e']:5.2f} p{w['ph']} {w['text']}")
