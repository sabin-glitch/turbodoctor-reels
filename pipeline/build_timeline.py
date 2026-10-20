"""Align curated transcript to Parakeet token timestamps, build the edit decision list (EDL)
with tightened pauses + cold open (+ optional synthetic intro, out/intro.json), map word times to output time, write out/timeline.json."""
import os
import json, unicodedata, difflib, re

ROOT = os.environ.get("REEL_ROOT") or os.path.dirname(os.path.abspath(__file__))
ctx = json.load(open(f"{ROOT}/out/transcript_ctx.json"))
p1 = json.load(open(f"{ROOT}/out/transcript.json"))
VAD = [(s["start"], s["end"]) for s in p1]
import soundfile as sf
SRC_DUR = sf.info(f"{ROOT}/audio/voice16k.wav").duration
# One curated string per context window (out/transcript_ctx.json). Write out/curated.json after reading the ASR text;
# falls back to the raw Whisper text so the pipeline can run end-to-end before curation.
CP = f"{ROOT}/out/curated.json"
CURATED = json.load(open(CP)) if os.path.exists(CP) else [w["whisper"] for w in ctx]
assert len(CURATED) == len(ctx), f"curated.json has {len(CURATED)} lines, transcript_ctx.json has {len(ctx)} windows"


def norm_chars(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return "".join(c for c in s if c.isalnum())


def vad_index(t):
    for i, (a, b) in enumerate(VAD):
        if a - 0.05 <= t <= b + 0.05:
            return i
    return None


def snap_to_speech(t):
    """If t falls in a silence gap, move it to the start of the next speech segment."""
    if vad_index(t) is not None:
        return t
    for a, b in VAD:
        if a > t:
            return a
    return t


def char_timeline(toks, ts):
    pchars, ptimes = [], []
    for k, tok in enumerate(toks):
        t0 = ts[k]; t1 = ts[k + 1] if k + 1 < len(ts) else t0 + 0.24
        n = norm_chars(tok)
        for j, c in enumerate(n):
            pchars.append(c); ptimes.append(t0 + (t1 - t0) * j / max(1, len(n)))
    return "".join(pchars), ptimes


def align(cw, toks, ts):
    """Return start time per curated word (None if unmatched)."""
    pstr, ptimes = char_timeline(toks, ts)
    cstr, owner, first = "", [], []
    for k, w in enumerate(cw):
        n = norm_chars(w)
        first.append(len(cstr)); cstr += n; owner += [k] * len(n)
    sm = difflib.SequenceMatcher(None, cstr, pstr, autojunk=False)
    cmap = {}
    for a, b, size in sm.get_matching_blocks():
        for q in range(size):
            cmap[a + q] = b + q
    starts = [None] * len(cw)
    for k in range(len(cw)):
        n = len(norm_chars(cw[k]))
        # need >= 60% of the word's chars matched, and use its first matched char (<=1 offset)
        idx = [first[k] + j for j in range(n) if first[k] + j in cmap]
        if n and len(idx) >= max(1, round(0.6 * n)) and idx[0] - first[k] <= 1:
            starts[k] = ptimes[cmap[idx[0]]] - (0.04 if idx[0] > first[k] else 0)
    return starts


words = []  # dicts: text, src_start, src_end, window
for wi, (win, text) in enumerate(zip(ctx, CURATED)):
    cw = text.split()
    starts = align(cw, win["tokens"], win["token_ts"])
    # fallback: first-pass (per-VAD-segment) tokens inside this window
    t1, s1 = [], []
    for s in p1:
        if s["start"] >= win["start"] - 0.3 and s["end"] <= win["end"] + 0.3:
            t1 += s["tokens"]; s1 += s["token_ts"]
    fb = align(cw, t1, s1) if t1 else [None] * len(cw)
    for k in range(len(cw)):
        if starts[k] is None and fb[k] is not None:
            starts[k] = fb[k]
    # interpolate the rest, weighted by character length
    lens = [max(1, len(norm_chars(w))) for w in cw]
    known = [(k, t) for k, t in enumerate(starts) if t is not None]
    for k in range(len(cw)):
        if starts[k] is None:
            prev = [(kk, tt) for kk, tt in known if kk < k]
            nxt = [(kk, tt) for kk, tt in known if kk > k]
            if prev and nxt:
                (k0, t0), (k1_, t1_) = prev[-1], nxt[0]
                tot = sum(lens[k0:k1_]); part = sum(lens[k0:k])
                starts[k] = t0 + (t1_ - t0) * part / tot
            elif nxt:
                starts[k] = max(win["start"], nxt[0][1] - 0.075 * sum(lens[k:nxt[0][0]]))
            else:
                starts[k] = prev[-1][1] + 0.075 * sum(lens[prev[-1][0]:k])
    for k, w in enumerate(cw):
        words.append(dict(text=w, s=snap_to_speech(starts[k]), win=wi))

# monotonic fix
for i in range(1, len(words)):
    if words[i]["s"] <= words[i - 1]["s"] + 0.06:
        words[i]["s"] = words[i - 1]["s"] + 0.06
# ends
for i, w in enumerate(words):
    vi = vad_index(w["s"])
    seg_end = VAD[vi][1] if vi is not None else w["s"] + 0.4
    nxt = words[i + 1]["s"] if i + 1 < len(words) else SRC_DUR
    e = min(nxt, seg_end + 0.05) if (i + 1 < len(words) and vad_index(nxt) != vi) else nxt
    w["e"] = round(min(e, w["s"] + 1.1), 3)
    w["s"] = round(w["s"], 3)

# ---------------- EDL ----------------
# story: tighten pauses between VAD segments AND inside them (energy-based silences, never across a word start)
import numpy as np
from scipy.signal import butter, sosfilt
x16, _sr = sf.read(f"{ROOT}/audio/voice16k.wav", dtype="float32")
if x16.ndim > 1: x16 = x16.mean(1)
xb = sosfilt(butter(4, [150, 3800], btype="band", fs=16000, output="sos"), x16)
HOP = 160; WIN = 320
nfr = max(1, (len(xb) - WIN) // HOP)
rms = np.array([np.sqrt(np.mean(xb[i * HOP:i * HOP + WIN] ** 2) + 1e-12) for i in range(nfr)])
db = 20 * np.log10(rms)
from scipy.ndimage import median_filter
db = median_filter(db, 5)
floor, peak = np.percentile(db, 12), np.percentile(db, 95)
thr = floor + 0.33 * (peak - floor)
sil = db < thr
starts_w = sorted(w["s"] for w in words)
gaps = []
i = 0
while i < nfr:
    if sil[i]:
        j = i
        while j < nfr and sil[j]: j += 1
        a, b = i * HOP / 16000, j * HOP / 16000
        inside = [ws for ws in starts_w if a + 0.06 < ws < b - 0.04]
        if inside: b = inside[0] - 0.08
        if b - a >= 0.32: gaps.append((a, b))
        i = j
    else: i += 1
# merge with VAD gaps
for (a0, b0), (a1, b1) in zip(VAD[:-1], VAD[1:]):
    if a1 - b0 > 0.45: gaps.append((b0, a1))
gaps.sort(); mg = []
for a, b in gaps:
    if mg and a <= mg[-1][1]: mg[-1] = (mg[-1][0], max(mg[-1][1], b))
    else: mg.append((a, b))
st0 = max(0.0, VAD[0][0] - 0.2); en0 = min(SRC_DUR, VAD[-1][1] + 0.45)
keep = []; cur_a = st0; removed_before = []
for a, b in mg:
    if b <= st0 or a >= en0: continue
    L = b - a
    tail, head = (0.9, 0.7) if L > 2.5 else ((0.16, 0.10) if L > 0.6 else (0.11, 0.07))
    ca, cb = a + tail, b - head
    if cb - ca < 0.14: continue
    keep.append((cur_a, ca)); removed_before.append(cb - ca); cur_a = cb
keep.append((cur_a, en0))
keep = [(a, b) for a, b in keep if b - a > 0.05]
# out/v2.json "cuts": default false = no cuts, footage exactly as filmed (pauses kept); {"cuts": true} = tighten pauses
_V2 = json.load(open(f"{ROOT}/out/v2.json")) if os.path.exists(f"{ROOT}/out/v2.json") else {}
if _V2.get("cuts", False) is False:  # default (Sabin, 18.10.2026): natural pace, pauses kept
    keep = [(0.0, SRC_DUR)]; removed_before = []
ZG = [0]
for k in range(1, len(keep)):
    ZG.append(ZG[-1] + (1 if removed_before[k - 1] >= 0.55 else 0))

import os
COLD = json.load(open(f"{ROOT}/out/cold.json")) if os.path.exists(f"{ROOT}/out/cold.json") else {"audio": [], "video_src": 0.0, "extra": 0.0}
COLD_AUDIO = [tuple(x) for x in COLD["audio"]]
# optional synthetic intro hook (graphics + generated voice, out/intro.json from intro_vo.py): the story starts after it
INTRO = json.load(open(f"{ROOT}/out/intro.json")) if os.path.exists(f"{ROOT}/out/intro.json") else None
segments = []
t = 0.0
if INTRO:
    segments.append(dict(kind="intro", src_a=INTRO["bg_src"], src_b=INTRO["bg_src"], out_a=0.0, dur=INTRO["dur"])); t = INTRO["dur"]
for a, b in COLD_AUDIO:
    segments.append(dict(kind="cold_audio", src_a=a, src_b=b, out_a=round(t, 3))); t += b - a
cold_len = t
if COLD_AUDIO:
    segments.append(dict(kind="video_override", src_a=COLD["video_src"], src_b=COLD["video_src"] + cold_len + COLD["extra"], out_a=0.0))
    t += COLD["extra"]
story_out0 = t
for k, (a, b) in enumerate(keep):
    segments.append(dict(kind="story", src_a=round(a, 3), src_b=round(b, 3), out_a=round(t, 3), zg=ZG[k] if k < len(ZG) else 0)); t += b - a
story_end = t
END_CARD = 7.5
total = t + END_CARD


def src_to_out(ts):
    for sg in segments:
        if sg["kind"] == "story" and sg["src_a"] - 1e-6 <= ts <= sg["src_b"] + 1e-6:
            return sg["out_a"] + (ts - sg["src_a"])
    # in a removed gap -> map to the start of the next kept segment
    for sg in segments:
        if sg["kind"] == "story" and sg["src_a"] > ts:
            return sg["out_a"]
    return story_end


for w in words:
    w["os"] = round(src_to_out(w["s"]), 3)
    w["oe"] = round(max(w["os"] + 0.08, src_to_out(w["e"])), 3)

cold_words = []
for w in words:
    for sg in segments:
        if sg["kind"] == "cold_audio" and sg["src_a"] - 0.02 <= w["s"] <= sg["src_b"]:
            os_ = sg["out_a"] + (w["s"] - sg["src_a"]); oe_ = sg["out_a"] + (min(w["e"], sg["src_b"]) - sg["src_a"])
            cold_words.append(dict(text=w["text"], os=round(max(0, os_), 3), oe=round(oe_, 3)))

intro_words = [dict(text=w["text"], s=w["s"], e=w["e"], os=w["s"], oe=w["e"], win=-1, ph=w["ph"]) for w in INTRO["words"]] if INTRO else []
tl = dict(fps=30, width=1080, height=1920, total=round(total, 3), story_out0=round(story_out0, 3),
          story_end=round(story_end, 3), end_card=END_CARD, segments=segments, words=intro_words + words,
          cold_words=cold_words)
if INTRO: tl["intro"] = dict(dur=INTRO["dur"], vo_dur=INTRO["vo_dur"], bg_src=INTRO["bg_src"], phrases=INTRO["phrases"])
json.dump(tl, open(f"{ROOT}/out/timeline.json", "w"), ensure_ascii=False, indent=1)
print(f"total {total:.2f}s  story starts {story_out0:.2f}  story ends {story_end:.2f}  cuts {len(keep)}  src story {sum(b-a for a,b in keep):.1f}s of {SRC_DUR:.1f}s")
import sys
for w in (words if "-v" in sys.argv else []):
    print(f"{w['os']:7.2f}-{w['oe']:6.2f}  src {w['s']:6.2f}  {w['text']}")
