"""Voice-over (vocea „Sabin” din ElevenLabs) peste un clip real, filmat fără voce sau doar cu o frază la început.
  python3 build_vo_clip.py <folder reel> <folder variante> <prefix>
Citește <folder reel>/vo_script.json:
  {"f0": 168, "end_card": 7.5,
   "orig": {"until": 7.6, "fade": 0.3, "words": [["Clientul", 1.14, 1.70], ...]},   # opțional: sunetul clipului rămâne doar până la `until`
   "lines": [{"n": 1, "t": 7.95, "text": "Am desfăcut {pompa|pompa} ..."}, ...]}     # n = numărul rândului din numele fișierelor, t = momentul din reel
Variantele fiecărui rând: <folder variante>/<prefix>L<NN><x>.* (ElevenLabs eleven_v4, fiecare rând generat separat, cu
[calm] [matter of fact] în față). Alegerea pe rând e ca în tools/anim_amorsare/make_vo.py: întâi textul cel mai clar (ASR), apoi tonul
cel mai apropiat de vocea lui (f0) și fără pauze lungi. Rândurile alese sunt aduse la același nivel și puse la `t`.
Scrie audio/vo_track.wav (48 kHz), audio/src48.wav (sunetul clipului doar până la orig.until; originalul rămâne în audio/src48_orig.wav),
out/timeline.json (format narator: povestea = clipul întreg, fără tăieturi) și out/vo_picks.json. Apoi: retime.py, extract_frames.py.
Cuvintele din `orig.words` (fraza spusă în clip) intră în fereastra 0, rândurile de voice-over în ferestrele 1, 2, ..."""
import os, sys, json, re, glob, difflib, shutil
import numpy as np, soundfile as sf, sherpa_onnx
from scipy.signal import resample_poly
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "anim_amorsare"))
from vo_qc import metrics, parse, norm, heard, word_starts, load, rms_db, SR

R, TAKES, PRE = sys.argv[1].rstrip("/"), sys.argv[2].rstrip("/"), sys.argv[3]
S = json.load(open(f"{R}/vo_script.json")); F0T = float(S.get("f0", 168)); END_CARD = float(S.get("end_card", 7.5)); LVL = -20.0
FORCE = json.loads(os.environ.get("VO_PICK", "{}"))
M = os.environ.get("TD_MODELS", "/home/claude/models"); WH = f"{M}/sherpa-onnx-whisper-turbo"
wh = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=f"{WH}/turbo-encoder.int8.onnx", decoder=f"{WH}/turbo-decoder.int8.onnx",
    tokens=f"{WH}/turbo-tokens.txt", language="ro", task="transcribe", num_threads=2)
def whisper(x16):
    s = wh.create_stream(); s.accept_waveform(16000, x16); wh.decode_stream(s); return s.result.text.strip()
def gated(y):
    f = int(.02 * SR); k = len(y) // f; p = (y[:k * f].astype(np.float64).reshape(k, f) ** 2).mean(1); return 10 * np.log10(p[p > p.max() * 1e-3].mean() + 1e-12)
def calm_pauses(y, ref, thr=-32.0, knee=8.0, rng=14.0):   # fondul slab din pauzele dintr-un rând coboară încă 14 dB (ca în make_vo.py)
    from scipy.ndimage import maximum_filter1d
    db, hop = rms_db(y); Lh = maximum_filter1d(db - ref, size=17, mode="nearest"); g = -rng * np.clip((thr - Lh) / knee, 0, 1)
    out = np.empty_like(g); cur = 0.0
    for k, v in enumerate(g):
        cur += (.6 if v > cur else .2) * (v - cur); out[k] = cur
    gs = np.interp(np.arange(len(y)), np.arange(len(out)) * int(hop * SR) + int(.01 * SR), out)
    return (y * 10 ** (gs / 20)).astype(np.float32)

SRC_DUR = sf.info(f"{R}/audio/voice16k.wav").duration
files = sorted(glob.glob(f"{TAKES}/{PRE}L*")); clips = []; picks = []
for L in S["lines"]:
    g = parse(L["text"]); say = re.sub(r"\s+([,.;:!?])", r"\1", " ".join(" ".join(s_) for _, s_ in g)); cands = []
    for f in files:
        m = re.search(r"L(\d\d)([a-z])\.[^.]+$", os.path.basename(f))
        if not m or int(m.group(1)) != L["n"]: continue
        x = load(f); x /= max(1e-6, np.abs(x).max()) / .9; db, hop = rms_db(x); thr = db.max() - 38; loud = np.where(db > thr)[0]
        s0 = max(0.0, loud[0] * hop - .05); s1 = min(len(x) / SR, loud[-1] * hop + .02 + .10)
        y = x[int(s0 * SR):int(s1 * SR)].copy(); fi, fo = int(.008 * SR), int(.03 * SR); y[:fi] *= np.linspace(0, 1, fi); y[-fo:] *= np.linspace(1, 0, fo)
        y16 = resample_poly(y, 1, 3).astype(np.float32); tk, tt, txt = heard(y16); q = metrics(y, len(norm(say))); wtxt = whisper(y16)
        sim = difflib.SequenceMatcher(None, norm(say), norm(txt)).ratio(); simw = difflib.SequenceMatcher(None, norm(say), norm(wtxt)).ratio()
        cost = abs(12 * np.log2(max(60.0, q["f0"]) / F0T)) + .5 * max(0.0, q["rng"] - 13.5) + 6 * max(0.0, q["p_max"] - .35)
        cands.append(dict(take=m.group(2), audio=y, toks=tk, ts=tt, txt=txt, wtxt=wtxt, sim=sim, simw=simw, q=q, cost=float(cost), floor=float(np.percentile(db, 2))))
    if not cands: raise SystemExit(f"nicio variantă pentru rândul {L['n']}")
    pick = min(cands, key=lambda c: (-round(min(c["sim"], c["simw"]), 2), c["cost"]))   # ambele recunoașteri trebuie să audă textul
    if str(L["n"]) in FORCE: pick = next(c for c in cands if c["take"] == FORCE[str(L["n"])])
    pick["audio"] = calm_pauses((pick["audio"] * 10 ** ((LVL - gated(pick["audio"])) / 20)).astype(np.float32), LVL)
    clips.append(dict(n=L["n"], g=g, say=say, audio=pick["audio"], dur=len(pick["audio"]) / SR, toks=pick["toks"], ts=pick["ts"], start=float(L["t"]), line=L))
    for c in cands:
        q = c["q"]; print(f"[{L['n']:2d}{c['take']}]{'*' if c is pick else ' '} {q['dur']:5.2f}s P {c['sim']:.2f} W {c['simw']:.2f} | F0 {q['f0']:3.0f} p90 {q['f90']:3.0f} int {q['rng']:4.1f} st | "
                           f"{q['rate']:4.1f} lit/s | pauze {q['n_p']} max {q['p_max']:.2f} | fond {c['floor']:5.1f} dB | cost {c['cost']:.1f}\n        P: {c['txt']}\n        W: {c['wtxt']}")
    picks.append(dict(n=L["n"], take=pick["take"], t=L["t"], dur=round(len(pick["audio"]) / SR, 3), sim=round(pick["sim"], 3), simw=round(pick["simw"], 3),
                      cands=[dict(take=c["take"], sim=round(c["sim"], 3), simw=round(c["simw"], 3), cost=round(c["cost"], 2), txt=c["txt"], wtxt=c["wtxt"],
                                  **{k: round(float(v), 2) for k, v in c["q"].items()}) for c in cands]))
json.dump(picks, open(f"{R}/out/vo_picks.json", "w"), ensure_ascii=False, indent=1)

ORIG = S.get("orig"); prev_end = ORIG["until"] if ORIG else 0.0
for c in sorted(clips, key=lambda c: c["start"]):
    if c["start"] < prev_end + .1: print(f"!! rândul {c['n']} începe la {c['start']:.2f}, dar ce e înaintea lui se termină la {prev_end:.2f}")
    prev_end = c["start"] + c["dur"]
    if prev_end > SRC_DUR + float(S.get("tip", 0)): print(f"!! rândul {c['n']} trece de sfârșitul clipului cu {prev_end - SRC_DUR:.2f}s")

def runs_of(y):   # rostirile din rând (anvelopa vocii curate): [(început, sfârșit)] în secunde de la începutul rândului
    db, hop = rms_db(y); act = db > np.percentile(db, 97) - 30; runs = []; i = 0; n = len(act)
    while i < n:
        if act[i]:
            j = i
            while j < n and act[j]: j += 1
            runs.append([i * hop, j * hop]); i = j
        else: i += 1
    m = []
    for a, b in runs:
        if m and a - m[-1][1] < .12: m[-1][1] = b
        else: m.append([a, b])
    return [(a, b) for a, b in m if b - a >= .05]

words = []
if ORIG:
    for w, a, b in ORIG["words"]: words.append(dict(text=w, s=a, e=b, os=a, oe=b, win=0))
for k, c in enumerate(sorted(clips, key=lambda c: c["start"])):
    say_words = [w for _, s in c["g"] for w in s]; owner = [gi for gi, (_, s) in enumerate(c["g"]) for _ in s]
    st = word_starts(say_words, c["toks"], c["ts"], c["dur"]); gs = {}
    for j, gi in enumerate(owner): gs.setdefault(gi, st[j])
    ws = [min(gs[gi], c["dur"] - .1) for gi in range(len(c["g"]))]; runs = runs_of(c["audio"]); moved = []
    def run_at(t, pad=.03):
        for q, (a, b) in enumerate(runs):
            if a - pad <= t < b: return q
        return None
    # timpii ASR vin cu până la ~0,3 s prea devreme după o pauză: primul cuvânt al fiecărei rostiri se mută pe începutul ei real
    for gi in range(len(ws)):
        s0 = ws[gi]; q = run_at(s0)
        if gi == 0 and runs: ws[gi] = runs[0][0]
        elif q is None:
            nx = [a for a, b in runs if a > s0]
            if nx and nx[0] - s0 <= .5: ws[gi] = nx[0]
        elif runs[q][1] - s0 <= .08 and q + 1 < len(runs) and runs[q + 1][0] - runs[q][1] <= .3: ws[gi] = runs[q + 1][0]
        if abs(ws[gi] - s0) > .03: moved.append(f"{c['g'][gi][0]} {c['start'] + s0:.2f}->{c['start'] + ws[gi]:.2f}")
    occ = {}
    for gi, (show, _) in enumerate(c["g"]):   # "fix": {"cuvânt#k": timp absolut} = corecție de mână (începutul cuvântului citit din anvelopă)
        key = norm(show); occ[key] = occ.get(key, -1) + 1
        for fk, ft in (c["line"].get("fix") or {}).items():
            fw, _, fn = fk.partition("#")
            if norm(fw) == key and int(fn or 0) == occ[key]: moved.append(f"{show} {c['start'] + ws[gi]:.2f}=>{ft:.2f}"); ws[gi] = float(ft) - c["start"]
    for gi in range(1, len(ws)): ws[gi] = max(ws[gi], ws[gi - 1] + .06)
    if moved: print(f"   rândul {c['n']}: " + ", ".join(moved))
    for gi, (show, _) in enumerate(c["g"]):
        a = ws[gi]; b = ws[gi + 1] if gi + 1 < len(ws) else c["dur"]; q = run_at(a)
        if q is not None and (gi + 1 == len(ws) or run_at(ws[gi + 1]) != q): b = min(b, runs[q][1] + .05)
        a += c["start"]; b += c["start"]
        words.append(dict(text=show, s=round(a, 3), e=round(max(a + .1, b), 3), os=round(a, 3), oe=round(max(a + .1, b), 3), win=k + 1))
story_end = round(SRC_DUR * 30) / 30; total = story_end + END_CARD + float(S.get("tip", 0))
n = int(round(round(total * 30) / 30 * SR)); vo = np.zeros(n, np.float32)
for c in clips:
    o = int(round(c["start"] * SR)); m = min(len(c["audio"]), n - o); vo[o:o + m] += c["audio"][:m]
sf.write(f"{R}/audio/vo_track.wav", vo, SR, subtype="FLOAT")
# sunetul clipului: doar fraza de la început (orig) sau deloc
if not os.path.exists(f"{R}/audio/src48_orig.wav"): shutil.copyfile(f"{R}/audio/src48.wav", f"{R}/audio/src48_orig.wav")
src, sr = sf.read(f"{R}/audio/src48_keep.wav" if os.path.exists(f"{R}/audio/src48_keep.wav") else f"{R}/audio/src48_orig.wav", dtype="float32"); assert sr == SR
if ORIG:
    u, fd = float(ORIG["until"]), float(ORIG.get("fade", .3)); a, b = int((u - fd) * SR), int(u * SR)
    env = np.ones(len(src), np.float32); env[a:b] = np.linspace(1, 0, b - a); env[b:] = 0
    src = src * (env if src.ndim == 1 else env[:, None])
else: src = src * 0
sf.write(f"{R}/audio/src48.wav", src, SR, subtype="PCM_16")
sents = ([dict(i=0, start=ORIG["words"][0][1], end=ORIG["words"][-1][2], text=" ".join(w[0] for w in ORIG["words"]))] if ORIG else []) + \
        [dict(i=k + 1, start=round(c["start"], 3), end=round(c["start"] + c["dur"], 3), text=" ".join(g[0] for g in c["g"])) for k, c in enumerate(sorted(clips, key=lambda c: c["start"]))]
tl = dict(fps=30, width=1080, height=1920, total=round(story_end + END_CARD, 3), story_out0=0.0, story_end=round(story_end, 3), end_card=END_CARD,
          segments=[dict(kind="story", src_a=0.0, src_b=round(story_end, 3), out_a=0.0, zg=0)], words=words, cold_words=[], narrator=True, sentences=sents)
json.dump(tl, open(f"{R}/out/timeline.json", "w"), ensure_ascii=False, indent=1)
if os.path.exists(f"{R}/out/timeline_1x.json"): os.remove(f"{R}/out/timeline_1x.json")
for s in sents: print(f"{s['start']:6.2f}-{s['end']:6.2f}  {s['text']}")
print(f"story_end {story_end:.2f}  (urmează retime.py și extract_frames.py)")
