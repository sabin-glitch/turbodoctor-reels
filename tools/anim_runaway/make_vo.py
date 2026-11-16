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
script = json.load(open(f"{HERE}/vo_script.json")); os.makedirs(f"{HERE}/vo", exist_ok=True)
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


def load(f):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()


def rms_db(x, win=.02, hop=.005):
    w, h = int(win * SR), int(hop * SR); c = np.cumsum(np.concatenate([[0.0], x.astype(np.float64) ** 2]))
    idx = np.arange(0, len(x) - w, h); return 10 * np.log10((c[idx + w] - c[idx]) / w + 1e-12), hop


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
elif mode == "take":
    # one or more takes of the WHOLE text (e.g. two ElevenLabs takes of the user's own voice). Every line is located in each take by
    # ASR + character alignment, cut out at the quietest point of the pause on either side, and the clearer take is used line by line
    # (the main take is kept unless the other one is clearly better, so the voice stays even). Lines are then paced with the script gaps.
    G = [parse(L["text"]) for L in script]
    all_words = [w for g in G for _, s in g for w in s]; nline = [sum(len(s) for _, s in g) for g in G]
    first = np.concatenate([[0], np.cumsum(nline)])           # index of each line's first say-word
    takes = []
    for f in sys.argv[2:]:
        x = load(f); x /= max(1e-6, np.abs(x).max()) / .9; x16 = resample_poly(x, 1, 3).astype(np.float32)
        db, hop = rms_db(x); thr = db.max() - 38
        # ASR in chunks cut at pauses (the recognizer is most reliable on < 25 s)
        quiet = db < thr; cuts = [0]; t = 0.0; D = len(x) / SR
        while D - t > 24:
            lo, hi = int((t + 12) / hop), int((t + 23) / hop); q = np.where(quiet[lo:hi])[0]
            if len(q):   # middle of the longest quiet run in the window
                runs = np.split(q, np.where(np.diff(q) > 1)[0] + 1); r = max(runs, key=len); k = lo + int(r[len(r) // 2])
            else: k = lo + int(np.argmin(db[lo:hi]))
            t = k * hop; cuts.append(t)
        cuts.append(D); toks, ts = [], []
        for a_, b_ in zip(cuts[:-1], cuts[1:]):
            tk, tt, _ = heard(x16[int(a_ * 16000):int(b_ * 16000)]); toks += tk; ts += [a_ + v for v in tt]
        st = word_starts(all_words, toks, ts, D)
        # cut points: the quietest 60 ms between the last word of a line and the first word of the next
        cp = [0.0]
        for i in range(1, len(script)):
            # the window reaches a little into the next line's first word: recognizer times can be ~0.1 s early, and the true pause is far quieter than any speech
            a_ = st[first[i] - 1] + .12; b_ = st[first[i]] + .16; lo, hi = int(a_ / hop), max(int(a_ / hop) + 2, int(b_ / hop))
            sm = np.convolve(db[lo:hi], np.ones(12) / 12, mode="same"); cp.append((lo + int(np.argmin(sm))) * hop)
        cp.append(D); segs = []
        for i in range(len(script)):
            a_, b_ = int(cp[i] / hop), int(cp[i + 1] / hop); loud = np.where(db[a_:b_] > thr)[0]
            s0 = max(cp[i], (a_ + loud[0]) * hop - .05); s1 = min(cp[i + 1], (a_ + loud[-1]) * hop + .02 + .10)
            y = x[int(s0 * SR):int(s1 * SR)].copy(); fi, fo = int(.008 * SR), int(.03 * SR); y[:fi] *= np.linspace(0, 1, fi); y[-fo:] *= np.linspace(1, 0, fo)
            say = re.sub(r"\s+([,.;:!?])", r"\1", " ".join(" ".join(s_) for _, s_ in G[i]))
            tk, tt, txt = heard(resample_poly(y, 1, 3).astype(np.float32))
            segs.append(dict(audio=y, toks=tk, ts=tt, txt=txt, sim=difflib.SequenceMatcher(None, norm(say), norm(txt)).ratio(), src=(round(s0, 2), round(s1, 2))))
        takes.append(dict(f=os.path.basename(f), segs=segs, dur=D, mean=float(np.mean([q["sim"] for q in segs]))))
        print(f"take {os.path.basename(f)}: {D:.1f} s, mean match {takes[-1]['mean']:.3f}")
    main = int(np.argmax([t_["mean"] for t_ in takes])); FORCE = json.loads(os.environ.get("VO_PICK", "{}"))   # {"7": 1} forces a take for a line
    for i, L in enumerate(script):
        pick = main
        for k, t_ in enumerate(takes):
            if t_["segs"][i]["sim"] > takes[pick]["segs"][i]["sim"] + .05: pick = k
        if str(i) in FORCE: pick = int(FORCE[str(i)])
        q = takes[pick]["segs"][i]
        clips.append(dict(i=i, g=G[i], audio=q["audio"], dur=len(q["audio"]) / SR, toks=q["toks"], ts=q["ts"], line=L))
        print(f"[{i:2d}] take {pick + 1} {len(q['audio']) / SR:5.2f}s " + " ".join(f"{t_['segs'][i]['sim']:.2f}" for t_ in takes) + f" | {q['txt']}")
    GAPK = float(os.environ.get("VO_GAPK", "1")); t = 0.0
    for c in clips:
        c["start"] = t + c["line"].get("gap", 0.3) * (GAPK if c["i"] else 1); t = c["start"] + c["dur"]
elif mode == "lines":
    # Every line generated on its own. ElevenLabs v4 holds a calm register only at the start of a generation (the tone tags wear off in
    # ~10 s), so each line is its own generation that starts with the tags: <dir>/*L<NN><x>.* = take x of line NN. Each take is trimmed,
    # checked by ASR and measured (vo_qc.metrics). The pick per line: the clearest text first (ASR match), then no long pause and the tone
    # closest to the speaker's natural one (VO_F0, Hz). The picked lines are level-matched (gated RMS), so separately generated lines sit at one
    # volume, and paced with the script gaps. VO_PICK='{"7": "b"}' forces a take. vo/picks.json keeps what was picked and why.
    from vo_qc import metrics
    F0T = float(os.environ.get("VO_F0", "168")); LVL = -20.0; FORCE = json.loads(os.environ.get("VO_PICK", "{}"))
    G = [parse(L["text"]) for L in script]; files = sorted(glob.glob(sys.argv[2].rstrip("/") + "/*")); picks = []
    def gated(y):
        f = int(.02 * SR); k = len(y) // f; p = (y[:k * f].astype(np.float64).reshape(k, f) ** 2).mean(1); return 10 * np.log10(p[p > p.max() * 1e-3].mean() + 1e-12)
    def calm_pauses(y, ref, thr=-32.0, knee=8.0, rng=14.0):
        # v4 leaves a faint room tone in the pauses inside a line (40-45 dB under the speech). A gentle downward expander takes it another
        # 14 dB down, only where nothing louder than ref+thr comes within 40 ms, so consonants, word tails and breaths are left alone.
        from scipy.ndimage import maximum_filter1d
        db, hop = rms_db(y); Lh = maximum_filter1d(db - ref, size=17, mode="nearest"); g = -rng * np.clip((thr - Lh) / knee, 0, 1)
        out = np.empty_like(g); cur = 0.0
        for k, v in enumerate(g):
            cur += (.6 if v > cur else .2) * (v - cur); out[k] = cur      # opens in ~10 ms, closes in ~25 ms
        gs = np.interp(np.arange(len(y)), np.arange(len(out)) * int(hop * SR) + int(.01 * SR), out)
        return (y * 10 ** (gs / 20)).astype(np.float32)
    def tilt(y):   # timbre check: 2-5 kHz against 150-800 Hz, dB (a take that sounds muffled or thin stands out here)
        f = np.fft.rfftfreq(4096, 1 / SR); k = (len(y) - 4096) // 2048; w = np.hanning(4096)
        P = np.mean([np.abs(np.fft.rfft(y[j * 2048:j * 2048 + 4096] * w)) ** 2 for j in range(max(1, k))], 0)
        return float(10 * np.log10(P[(f > 2000) & (f < 5000)].sum() / P[(f > 150) & (f < 800)].sum()))
    for i, L in enumerate(script):
        say = re.sub(r"\s+([,.;:!?])", r"\1", " ".join(" ".join(s_) for _, s_ in G[i])); cands = []
        for f in files:
            m = re.search(r"L(\d\d)([a-z])\.[^.]+$", os.path.basename(f))
            if not m or int(m.group(1)) != i: continue
            x = load(f); x /= max(1e-6, np.abs(x).max()) / .9; db, hop = rms_db(x); thr = db.max() - 38; loud = np.where(db > thr)[0]
            s0 = max(0.0, loud[0] * hop - .05); s1 = min(len(x) / SR, loud[-1] * hop + .02 + .10)
            y = x[int(s0 * SR):int(s1 * SR)].copy(); fi, fo = int(.008 * SR), int(.03 * SR); y[:fi] *= np.linspace(0, 1, fi); y[-fo:] *= np.linspace(1, 0, fo)
            tk, tt, txt = heard(resample_poly(y, 1, 3).astype(np.float32)); q = metrics(y, len(norm(say)))
            sim = difflib.SequenceMatcher(None, norm(say), norm(txt)).ratio()
            cost = abs(12 * np.log2(max(60.0, q["f0"]) / F0T)) + .5 * max(0.0, q["rng"] - 13.5) + 6 * max(0.0, q["p_max"] - .35)
            cands.append(dict(take=m.group(2), audio=y, toks=tk, ts=tt, txt=txt, sim=sim, q=q, cost=float(cost), tilt=tilt(y), lead=s0, tail=len(x) / SR - s1))
        if not cands: raise SystemExit(f"no take for line {i}")
        pick = min(cands, key=lambda c: (-round(c["sim"], 2), c["cost"]))   # the clearest text first; equally clear -> the closest tone
        if str(i) in FORCE: pick = next(c for c in cands if c["take"] == FORCE[str(i)])
        pick["audio"] = calm_pauses((pick["audio"] * 10 ** ((LVL - gated(pick["audio"])) / 20)).astype(np.float32), LVL)
        clips.append(dict(i=i, g=G[i], audio=pick["audio"], dur=len(pick["audio"]) / SR, toks=pick["toks"], ts=pick["ts"], line=L))
        for c in cands:
            q = c["q"]; print(f"[{i:2d}{c['take']}]{'*' if c is pick else ' '} {q['dur']:5.2f}s sim {c['sim']:.2f} | F0 {q['f0']:3.0f} p90 {q['f90']:3.0f} p98 {q['f98']:3.0f} int {q['rng']:4.1f} st | "
                               f"{q['rate']:4.1f} lit/s | pauze {q['n_p']} max {q['p_max']:.2f} | timbru {c['tilt']:5.1f} dB | cost {c['cost']:.1f} | {c['txt'][:60]}")
        picks.append(dict(i=i, take=pick["take"], sim=round(pick["sim"], 3), cands=[dict(take=c["take"], sim=round(c["sim"], 3), cost=round(c["cost"], 2), tilt=round(c["tilt"], 1),
                          **{k: round(float(v), 2) for k, v in c["q"].items()}) for c in cands]))
    json.dump(picks, open(f"{HERE}/vo/picks.json", "w"), ensure_ascii=False, indent=1)
    GAPK = float(os.environ.get("VO_GAPK", "1")); t = 0.0
    for c in clips:
        c["start"] = t + c["line"].get("gap", 0.3) * (GAPK if c["i"] else 1); t = c["start"] + c["dur"]
else:
    raise SystemExit("usage: make_vo.py piper | take <take1> [take2 ...] | lines <dir>")

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
