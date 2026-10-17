"""Synthesize the Romanian voiceover sentence by sentence, place it on the timeline, get word timings
(ASR on the clean TTS audio + char alignment), and write out/timeline.json + audio/vo_track.wav."""
import os
import json, re, glob, difflib, unicodedata
import numpy as np, soundfile as sf, sherpa_onnx
from scipy.signal import resample_poly

ROOT = os.environ.get("REEL_ROOT") or os.path.dirname(os.path.abspath(__file__)); SR = 48000; SPEED = 1.1
SRC_DUR = 45.9; END_CARD = 7.5; TAIL_AFTER_LAST = 1.2
script = json.load(open(f"{ROOT}/vo_script.json"))

D = os.environ.get("TD_MODELS", "/home/claude/models") + "/tts/vits-piper-ro_RO-mihai-medium"
tts = sherpa_onnx.OfflineTts(sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(
    vits=sherpa_onnx.OfflineTtsVitsModelConfig(model=glob.glob(D + "/*.onnx")[0], lexicon="", data_dir=D + "/espeak-ng-data",
                                               tokens=D + "/tokens.txt", noise_scale=0.6, noise_scale_w=0.75, length_scale=1.0),
    provider="cpu", num_threads=2), max_num_sentences=1))
PK = os.environ.get("TD_MODELS", "/home/claude/models") + "/sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8"
asr = sherpa_onnx.OfflineRecognizer.from_transducer(encoder=f"{PK}/encoder.int8.onnx", decoder=f"{PK}/decoder.int8.onnx",
    joiner=f"{PK}/joiner.int8.onnx", tokens=f"{PK}/tokens.txt", num_threads=2, model_type="nemo_transducer")


def norm(s):
    s = unicodedata.normalize("NFD", s.lower()); s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return "".join(c for c in s if c.isalnum())


def parse(text):
    """returns list of (show_word, [say_words])"""
    groups = []
    for part in re.split(r"(\{[^}]*\})", text):
        if not part: continue
        if part.startswith("{"):
            show, say = part[1:-1].split("|")
            # attach trailing punctuation handled by following text part
            groups.append([show, say.split()])
        else:
            for w in part.split():
                if groups and re.fullmatch(r"[,.;:!?]+", w):
                    groups[-1][0] += w; continue
                groups.append([w, [w]])
    # punctuation directly after a {} group comes as ", ..." part -> merge leading punctuation
    out = []
    for show, say in groups:
        if out and re.fullmatch(r"[,.;:!?]+", show):
            out[-1][0] += show; continue
        out.append([show, say])
    return out


def say_text(groups):
    s = " ".join(" ".join(say) for _, say in groups)
    return re.sub(r"\s+([,.;:!?])", r"\1", s)


clips = []
for i, line in enumerate(script):
    g = parse(line["text"]); st = say_text(g)
    a = tts.generate(st, sid=0, speed=SPEED)
    x = np.array(a.samples, dtype=np.float32)
    # trim leading/trailing silence
    thr = 10 ** (-42 / 20); idx = np.where(np.abs(x) > thr)[0]
    x = x[max(0, idx[0] - int(.05 * a.sample_rate)):idx[-1] + int(.08 * a.sample_rate)]
    x48 = resample_poly(x, SR, a.sample_rate).astype(np.float32)
    x16 = resample_poly(x, 16000, a.sample_rate).astype(np.float32)
    s = asr.create_stream(); s.accept_waveform(16000, np.concatenate([np.zeros(1600, np.float32), x16, np.zeros(3200, np.float32)])); asr.decode_stream(s)
    toks, ts = list(s.result.tokens), [float(t) - 0.1 for t in s.result.timestamps]
    clips.append(dict(i=i, groups=g, say=st, audio=x48, dur=len(x48) / SR, toks=toks, ts=ts, heard=s.result.text, line=line))
    print(f"[{i}] {len(x48) / SR:5.2f}s  say: {st}\n      heard: {s.result.text}")

# ---- placement
t = 0.0; story_end = None
for c in clips:
    L = c["line"]
    if L.get("endcard") is not None:
        continue
    start = L["t"] if L["t"] > 0 else t + L.get("gap", 0.3)
    start = max(start, t + 0.12)
    c["start"] = start; t = start + c["dur"]
last_end = t
story_end = min(SRC_DUR, last_end + TAIL_AFTER_LAST)
for c in clips:
    if c["line"].get("endcard") is not None:
        c["start"] = story_end + c["line"]["endcard"]
total = story_end + END_CARD


# ---- word timings: align ASR tokens to say-words, map to show-words
def char_tl(toks, ts):
    chars, times = [], []
    for k, tok in enumerate(toks):
        t0 = ts[k]; t1 = ts[k + 1] if k + 1 < len(ts) else t0 + .24; n = norm(tok)
        for j, ch in enumerate(n): chars.append(ch); times.append(t0 + (t1 - t0) * j / max(1, len(n)))
    return "".join(chars), times


words = []
for c in clips:
    say_words = [w for _, say in c["groups"] for w in say]
    owner = [gi for gi, (_, say) in enumerate(c["groups"]) for _ in say]
    pstr, ptimes = char_tl(c["toks"], c["ts"])
    cstr, first = "", []
    for w in say_words: first.append(len(cstr)); cstr += norm(w)
    sm = difflib.SequenceMatcher(None, cstr, pstr, autojunk=False); cmap = {}
    for a, b, n in sm.get_matching_blocks():
        for q in range(n): cmap[a + q] = b + q
    st = [None] * len(say_words)
    for k, w in enumerate(say_words):
        n = len(norm(w)); idx = [first[k] + j for j in range(n) if first[k] + j in cmap]
        if n and len(idx) >= max(1, round(.5 * n)) and idx[0] - first[k] <= 1: st[k] = max(0.0, ptimes[cmap[idx[0]]])
    known = [(k, v) for k, v in enumerate(st) if v is not None]
    lens = [max(1, len(norm(w))) for w in say_words]
    for k in range(len(st)):
        if st[k] is None:
            prev = [(kk, v) for kk, v in known if kk < k]; nxt = [(kk, v) for kk, v in known if kk > k]
            if prev and nxt:
                (k0, v0), (k1, v1) = prev[-1], nxt[0]; st[k] = v0 + (v1 - v0) * sum(lens[k0:k]) / sum(lens[k0:k1])
            elif nxt: st[k] = max(0.0, nxt[0][1] - 0.07 * sum(lens[k:nxt[0][0]]))
            elif prev: st[k] = prev[-1][1] + 0.07 * sum(lens[prev[-1][0]:k])
            else: st[k] = c["dur"] * k / len(st)
    for k in range(1, len(st)): st[k] = max(st[k], st[k - 1] + 0.05)
    gstart = {}
    for k, gi in enumerate(owner): gstart.setdefault(gi, st[k])
    for gi, (show, _) in enumerate(c["groups"]):
        os_ = c["start"] + min(gstart[gi], c["dur"] - 0.1)
        nxt = c["start"] + gstart[gi + 1] if gi + 1 in gstart else c["start"] + c["dur"]
        words.append(dict(text=show, os=round(os_, 3), oe=round(max(os_ + .1, nxt), 3), win=c["i"]))

# ---- VO track
n = int(round(round(total * 30) / 30 * SR)); vo = np.zeros(n, np.float32)
for c in clips:
    o = int(round(c["start"] * SR)); m = min(len(c["audio"]), n - o); vo[o:o + m] += c["audio"][:m]
sf.write(f"{ROOT}/audio/vo_track.wav", vo, SR, subtype="FLOAT")
segments = [dict(kind="story", src_a=0.0, src_b=round(story_end, 3), out_a=0.0)]
tl = dict(fps=30, width=1080, height=1920, total=round(total, 3), story_out0=0.0, story_end=round(story_end, 3), end_card=END_CARD,
          segments=segments, words=words, cold_words=[],
          sentences=[dict(i=c["i"], start=round(c["start"], 3), end=round(c["start"] + c["dur"], 3), text=" ".join(g[0] for g in c["groups"])) for c in clips])
json.dump(tl, open(f"{ROOT}/out/timeline.json", "w"), ensure_ascii=False, indent=1)
for s_ in tl["sentences"]: print(f"{s_['start']:6.2f}-{s_['end']:6.2f}  {s_['text']}")
print("story_end", round(story_end, 2), "total", round(total, 2))
