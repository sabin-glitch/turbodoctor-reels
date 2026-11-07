"""Narrator over the full clip from EXTERNAL per-line audio (ElevenLabs via .github/workflows/tts-elevenlabs.yml, or an MP3 Sabin generated himself),
instead of the Piper voice of vo_narrator.py. Same vo_script.json; line i is read from audio/ext/<i:02d>.mp3|.wav (set "voice": {"ext_dir": ...} in out/v2.json).
Word timings come from Parakeet ASR on each line, as in vo_narrator.py; no deepening by default ("voice": {"formant": 1.0, "pitch": 0}).
Writes audio/vo_track.wav and out/timeline.json, then run retime.py and extract_frames.py as usual (07.11.2026)."""
import os, sys, json, re, glob, difflib, unicodedata, subprocess
import numpy as np, soundfile as sf, sherpa_onnx, parselmouth
from parselmouth.praat import call
from scipy.signal import resample_poly

ROOT = os.environ.get("REEL_ROOT") or os.path.dirname(os.path.abspath(__file__)); SR = 48000
M = os.environ.get("TD_MODELS", "/home/claude/models"); D = M + "/tts/vits-piper-ro_RO-mihai-medium"
cfg = json.load(open(f"{ROOT}/out/v2.json")) if os.path.exists(f"{ROOT}/out/v2.json") else {}
VC = cfg.get("voice", {}); FORMANT = VC.get("formant", 1.0); PITCH = VC.get("pitch", 0); EXT = f"{ROOT}/" + VC.get("ext_dir", "audio/ext")
TIP_DUR = float(cfg.get("tip", {}).get("dur", 0)); END_CARD = 7.5
SRC_DUR = sf.info(f"{ROOT}/audio/voice16k.wav").duration
script = json.load(open(f"{ROOT}/vo_script.json"))

PK = M + "/sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8"
asr = sherpa_onnx.OfflineRecognizer.from_transducer(encoder=f"{PK}/encoder.int8.onnx", decoder=f"{PK}/decoder.int8.onnx",
    joiner=f"{PK}/joiner.int8.onnx", tokens=f"{PK}/tokens.txt", num_threads=2, model_type="nemo_transducer")


def norm(s):
    s = unicodedata.normalize("NFD", s.lower()); s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return "".join(c for c in s if c.isalnum())


def parse(text):
    """-> [[show_word, [say_words]], ...]"""
    out = []
    for part in re.split(r"(\{[^}]*\})", text):
        if not part: continue
        if part.startswith("{"):
            show, say = part[1:-1].split("|"); out.append([show, say.split()]); continue
        for w in part.split():
            if out and re.fullmatch(r"[,.;:!?]+", w): out[-1][0] += w; continue
            out.append([w, [w]])
    return out


def deepen(x, sr):
    if FORMANT == 1.0 and not PITCH: return x
    snd = parselmouth.Sound(x.astype(np.float64), sampling_frequency=sr)
    return call(snd, "Change gender", 60, 400, FORMANT, PITCH or 0, 1.0, 1.0).values[0].astype(np.float32)


def heard(x16):
    s = asr.create_stream(); s.accept_waveform(16000, np.concatenate([np.zeros(1600, np.float32), x16, np.zeros(3200, np.float32)])); asr.decode_stream(s)
    return list(s.result.tokens), [float(t) - 0.1 for t in s.result.timestamps], s.result.text


clips = []
for i, L in enumerate(script):
    g = parse(L["text"]); say = re.sub(r"\s+([,.;:!?])", r"\1", " ".join(" ".join(s) for _, s in g))
    f = next((f"{EXT}/{i:02d}{e}" for e in (".mp3", ".wav", ".m4a") if os.path.exists(f"{EXT}/{i:02d}{e}")), None)
    assert f, f"lipsește audio/ext/{i:02d}.mp3 pentru replica {i}"
    tmp = f"{ROOT}/audio/ext_{i:02d}.wav"
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", f, "-ac", "1", "-ar", "48000", "-c:a", "pcm_f32le", tmp], check=True)
    x, srx = sf.read(tmp, dtype="float32"); os.remove(tmp)
    idx = np.where(np.abs(x) > 10 ** (-45 / 20))[0]; x = x[max(0, idx[0] - int(.05 * srx)):idx[-1] + int(.08 * srx)]
    x = deepen(x, srx) if (FORMANT != 1.0 or PITCH) else x
    x16 = resample_poly(x, 16000, srx).astype(np.float32); toks, ts, txt = heard(x16)
    sim = difflib.SequenceMatcher(None, norm(say), norm(txt)).ratio()
    best = (sim, x, toks, ts, txt)
    class _A: sample_rate = srx
    a = _A()
    sim, x, toks, ts, txt = best
    x48 = resample_poly(x, SR, a.sample_rate).astype(np.float32)
    clips.append(dict(i=i, g=g, say=say, audio=x48, dur=len(x48) / SR, toks=toks, ts=ts, line=L))
    print(f"[{i}] {len(x48) / SR:5.2f}s  match {sim:.2f}\n     say:   {say}\n     heard: {txt}")

story_end = SRC_DUR
for c in clips:
    L = c["line"]
    c["start"] = story_end + L["tip"] if "tip" in L else L["t"]
    c["tip"] = "tip" in L
prev = None
for c in sorted(clips, key=lambda c: c["start"]):
    if prev and c["start"] < prev["start"] + prev["dur"] + .12: print(f"!! line {c['i']} overlaps line {prev['i']} by {prev['start'] + prev['dur'] + .12 - c['start']:.2f}s")
    if not c["tip"] and c["start"] + c["dur"] > story_end: print(f"!! line {c['i']} runs past the clip end by {c['start'] + c['dur'] - story_end:.2f}s")
    if c["tip"] and c["start"] + c["dur"] > story_end + TIP_DUR: print(f"!! tip line {c['i']} runs past the tip by {c['start'] + c['dur'] - story_end - TIP_DUR:.2f}s")
    prev = c
total = story_end + TIP_DUR + END_CARD


def char_tl(toks, ts):
    chars, times = [], []
    for k, tok in enumerate(toks):
        t0 = ts[k]; t1 = ts[k + 1] if k + 1 < len(ts) else t0 + .24; n = norm(tok)
        for j, ch in enumerate(n): chars.append(ch); times.append(t0 + (t1 - t0) * j / max(1, len(n)))
    return "".join(chars), times


words = []
for c in clips:
    say_words = [w for _, s in c["g"] for w in s]; owner = [gi for gi, (_, s) in enumerate(c["g"]) for _ in s]
    pstr, ptimes = char_tl(c["toks"], c["ts"]); cstr, first = "", []
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
            else: st[k] = c["dur"] * k / len(st)
    for k in range(1, len(st)): st[k] = max(st[k], st[k - 1] + .05)
    gs = {}
    for k, gi in enumerate(owner): gs.setdefault(gi, st[k])
    for gi, (show, _) in enumerate(c["g"]):
        a = c["start"] + min(gs[gi], c["dur"] - .1); b = c["start"] + gs[gi + 1] if gi + 1 in gs else c["start"] + c["dur"]
        words.append(dict(text=show, s=round(a, 3), e=round(max(a + .1, b), 3), os=round(a, 3), oe=round(max(a + .1, b), 3), win=c["i"]))

n = int(round(round(total * 30) / 30 * SR)); vo = np.zeros(n, np.float32)
for c in clips:
    o = int(round(c["start"] * SR)); m = min(len(c["audio"]), n - o); vo[o:o + m] += c["audio"][:m]
sf.write(f"{ROOT}/audio/vo_track.wav", vo, SR, subtype="FLOAT")
tl = dict(fps=30, width=1080, height=1920, total=round(story_end + END_CARD, 3), story_out0=0.0, story_end=round(story_end, 3), end_card=END_CARD,
          segments=[dict(kind="story", src_a=0.0, src_b=round(story_end, 3), out_a=0.0, zg=0)], words=words, cold_words=[], narrator=True,
          sentences=[dict(i=c["i"], start=round(c["start"], 3), end=round(c["start"] + c["dur"], 3), text=" ".join(g[0] for g in c["g"])) for c in clips])
json.dump(tl, open(f"{ROOT}/out/timeline.json", "w"), ensure_ascii=False, indent=1)
if os.path.exists(f"{ROOT}/out/timeline_1x.json"): os.remove(f"{ROOT}/out/timeline_1x.json")
for s in tl["sentences"]: print(f"{s['start']:6.2f}-{s['end']:6.2f}  {s['text']}")
print(f"story_end {story_end:.2f}  total {total:.2f}  (run retime.py next)")
