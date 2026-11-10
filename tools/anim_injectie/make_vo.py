"""Voice track for the injection explainer reel.
  python3 make_vo.py piper            -> stand-in narrator (Piper ro_RO-mihai, deepened like vo_narrator.py), lines placed one after another
  python3 make_vo.py take <file.mp3>  -> a real recording / ElevenLabs take of the same text: lines are found in it by ASR + char alignment
Writes vo/vo_track.wav (48 kHz), vo/timeline.json (pipeline narrator format, story_end = END), vo/cues.json for the animation director."""
import os, sys, json, re, glob, difflib, unicodedata, subprocess
import numpy as np, soundfile as sf, sherpa_onnx
from scipy.signal import resample_poly

HERE = os.path.dirname(os.path.abspath(__file__)); SR = 48000
M = os.environ.get("TD_MODELS", "/home/claude/models"); D = M + "/tts/vits-piper-ro_RO-mihai-medium"
script = json.load(open(f"{HERE}/vo_script.json")); os.makedirs(f"{HERE}/vo", exist_ok=True)
TAIL = 1.0; END_CARD = 7.5
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


def word_starts(say_words, toks, ts, dur):
    pstr, ptimes = char_tl(toks, ts); cstr, first = "", []
    for w in say_words: first.append(len(cstr)); cstr += norm(w)
    cmap = {}
    for a, b, n in difflib.SequenceMatcher(None, cstr, pstr, autojunk=False).get_matching_blocks():
        for q in range(n): cmap[a + q] = b + q
    st = [None] * len(say_words)
    for k, w in enumerate(say_words):
        n = len(norm(w)); idx = [first[k] + j for j in range(n) if first[k] + j in cmap]
        if n and len(idx) >= max(1, round(.5 * n)) and idx[0] - first[k] <= 1: st[k] = max(0.0, ptimes[cmap[idx[0]]])
    known = [(k, v) for k, v in enumerate(st) if v is not None]; lens = [max(1, len(norm(w))) for w in say_words]
    for k in range(len(st)):
        if st[k] is None:
            pv = [(kk, v) for kk, v in known if kk < k]; nx = [(kk, v) for kk, v in known if kk > k]
            if pv and nx: (k0, v0), (k1, v1) = pv[-1], nx[0]; st[k] = v0 + (v1 - v0) * sum(lens[k0:k]) / sum(lens[k0:k1])
            elif nx: st[k] = max(0.0, nx[0][1] - .07 * sum(lens[k:nx[0][0]]))
            elif pv: st[k] = pv[-1][1] + .07 * sum(lens[pv[-1][0]:k])
            else: st[k] = dur * k / len(st)
    for k in range(1, len(st)): st[k] = max(st[k], st[k - 1] + .05)
    return st


mode = sys.argv[1]
clips = []
if mode == "piper":
    import parselmouth
    from parselmouth.praat import call
    tts = sherpa_onnx.OfflineTts(sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(
        vits=sherpa_onnx.OfflineTtsVitsModelConfig(model=glob.glob(D + "/*.onnx")[0], lexicon="", data_dir=D + "/espeak-ng-data",
                                                   tokens=D + "/tokens.txt", noise_scale=0.55, noise_scale_w=0.7, length_scale=1.0),
        provider="cpu", num_threads=2), max_num_sentences=1))
    def deepen(x, sr):
        snd = parselmouth.Sound(x.astype(np.float64), sampling_frequency=sr)
        return call(snd, "Change gender", 60, 400, 0.94, 95, 1.0, 1.0).values[0].astype(np.float32)
    for i, L in enumerate(script):
        g = parse(L["text"]); say = re.sub(r"\s+([,.;:!?])", r"\1", " ".join(" ".join(s) for _, s in g)); best = None
        for take in range(8):
            a = tts.generate(say, sid=0, speed=L.get("speed", 1.0)); x = np.array(a.samples, dtype=np.float32)
            idx = np.where(np.abs(x) > 10 ** (-42 / 20))[0]; x = x[max(0, idx[0] - int(.05 * a.sample_rate)):idx[-1] + int(.08 * a.sample_rate)]
            x = deepen(x, a.sample_rate)
            x16 = resample_poly(x, 16000, a.sample_rate).astype(np.float32); toks, ts, txt = heard(x16)
            sim = difflib.SequenceMatcher(None, norm(say), norm(txt)).ratio()
            if best is None or sim > best[0]: best = (sim, x, toks, ts, txt)
        sim, x, toks, ts, txt = best
        x48 = resample_poly(x, SR, a.sample_rate).astype(np.float32)
        clips.append(dict(i=i, g=g, audio=x48, dur=len(x48) / SR, toks=toks, ts=ts, line=L))
        print(f"[{i:2d}] {len(x48) / SR:5.2f}s match {sim:.2f} | {txt}")
    t = 0.0
    for c in clips:
        c["start"] = t + c["line"].get("gap", 0.3); t = c["start"] + c["dur"]
else:
    raise SystemExit("take mode is added when the real voice arrives")

story_end = round((clips[-1]["start"] + clips[-1]["dur"] + TAIL) * 30) / 30
words = []
for c in clips:
    say_words = [w for _, s in c["g"] for w in s]; owner = [gi for gi, (_, s) in enumerate(c["g"]) for _ in s]
    st = word_starts(say_words, c["toks"], c["ts"], c["dur"]); gs = {}
    for k, gi in enumerate(owner): gs.setdefault(gi, st[k])
    for gi, (show, _) in enumerate(c["g"]):
        a = c["start"] + min(gs[gi], c["dur"] - .1); b = c["start"] + gs[gi + 1] if gi + 1 in gs else c["start"] + c["dur"]
        words.append(dict(text=show, s=round(a, 3), e=round(max(a + .1, b), 3), os=round(a, 3), oe=round(max(a + .1, b), 3), win=c["i"]))
total = story_end + END_CARD
n = int(round(round(total * 30) / 30 * SR)); vo = np.zeros(n, np.float32)
for c in clips:
    o = int(round(c["start"] * SR)); m = min(len(c["audio"]), n - o); vo[o:o + m] += c["audio"][:m]
sf.write(f"{HERE}/vo/vo_track.wav", vo, SR, subtype="FLOAT")
sents = [dict(i=c["i"], start=round(c["start"], 3), end=round(c["start"] + c["dur"], 3), text=" ".join(g[0] for g in c["g"])) for c in clips]
tl = dict(fps=30, width=1080, height=1920, total=round(total, 3), story_out0=0.0, story_end=round(story_end, 3), end_card=END_CARD,
          segments=[dict(kind="story", src_a=0.0, src_b=round(story_end, 3), out_a=0.0, zg=0)], words=words, cold_words=[], narrator=True, sentences=sents)
json.dump(tl, open(f"{HERE}/vo/timeline.json", "w"), ensure_ascii=False, indent=1)
json.dump(dict(end=story_end, lines=sents, words=words), open(f"{HERE}/vo/cues.json", "w"), ensure_ascii=False, indent=1)
for s in sents: print(f"{s['start']:6.2f}-{s['end']:6.2f}  {s['text']}")
print("story_end", story_end, "total", round(total, 2))
