"""Controlul vocii generate, înainte de a o monta (nu o pot asculta, deci o măsor):
  python3 vo_qc.py <script.json> <take1> [take2 ...]   -> pe fiecare variantă și pe fiecare rând: zgomotul de fond din pauze, pauzele
  (număr, cele lungi), tonul (F0 median / p90 / interval p10-p90 în semitonuri), ritmul (litere/s) și cât de clar aude ASR-ul rândul.
Rândurile se găsesc în variantă ca în make_vo.py (ASR Parakeet + aliniere pe caractere, tăiere în punctul cel mai liniștit al pauzei).
Repere (14.11.2026, vocea „Sabin”): zgomot de fond sub -60 dBFS (o variantă multilingual_v2 a avut -53 dBFS = fâșâit care se aude),
pauze în interiorul rândului sub ~0,45 s (v2 avea 20+ s de pauze, multe peste 0,5 s), F0 median ~150-180 Hz (vocea lui reală din reel-uri ~170 Hz;
v4 fără tag-uri ~200 Hz, „cinematic”; v4 rând cu rând, cu [calm] [matter of fact] în față: ~160 Hz)."""
import os, sys, json, re, difflib, unicodedata, subprocess
import numpy as np, sherpa_onnx, parselmouth
from scipy.signal import resample_poly
SR = 48000
M = os.environ.get("TD_MODELS", "/home/claude/models"); PK = M + "/sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8"
_asr = None
def asr():
    global _asr
    if _asr is None:
        _asr = sherpa_onnx.OfflineRecognizer.from_transducer(encoder=f"{PK}/encoder.int8.onnx", decoder=f"{PK}/decoder.int8.onnx",
            joiner=f"{PK}/joiner.int8.onnx", tokens=f"{PK}/tokens.txt", num_threads=2, model_type="nemo_transducer")
    return _asr
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
    s = asr().create_stream(); s.accept_waveform(16000, np.concatenate([np.zeros(1600, np.float32), x16, np.zeros(3200, np.float32)])); asr().decode_stream(s)
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
    idx = np.arange(0, max(1, len(x) - w), h); return 10 * np.log10((c[idx + w] - c[idx]) / w + 1e-14), hop
def runs_below(db, hop, thr, mind=.12):
    q = db < thr; out = []; i = 0
    while i < len(q):
        if q[i]:
            j = i
            while j < len(q) and q[j]: j += 1
            if (j - i) * hop >= mind: out.append((i * hop, j * hop))
            i = j
        else: i += 1
    return out
def say_of(g): return re.sub(r"\s+([,.;:!?])", r"\1", " ".join(" ".join(s) for _, s in g))
def locate(x, script):
    """-> per line: dict(s0, s1, sim, txt, toks, ts) in the take x (48 kHz, not normalised), same method as make_vo.py take mode."""
    G = [parse(L["text"]) for L in script]; all_words = [w for g in G for _, s in g for w in s]
    nline = [sum(len(s) for _, s in g) for g in G]; first = np.concatenate([[0], np.cumsum(nline)])
    xn = x / (max(1e-6, np.abs(x).max()) / .9); x16 = resample_poly(xn, 1, 3).astype(np.float32)
    db, hop = rms_db(xn); thr = db.max() - 38; quiet = db < thr; cuts = [0]; t = 0.0; D = len(x) / SR
    while D - t > 24:
        lo, hi = int((t + 12) / hop), int((t + 23) / hop); q = np.where(quiet[lo:hi])[0]
        if len(q):
            rr = np.split(q, np.where(np.diff(q) > 1)[0] + 1); r = max(rr, key=len); k = lo + int(r[len(r) // 2])
        else: k = lo + int(np.argmin(db[lo:hi]))
        t = k * hop; cuts.append(t)
    cuts.append(D); toks, ts = [], []
    for a_, b_ in zip(cuts[:-1], cuts[1:]):
        tk, tt, _ = heard(x16[int(a_ * 16000):int(b_ * 16000)]); toks += tk; ts += [a_ + v for v in tt]
    st = word_starts(all_words, toks, ts, D); cp = [0.0]
    for i in range(1, len(script)):
        a_ = st[first[i] - 1] + .12; b_ = st[first[i]] + .16; lo, hi = int(a_ / hop), max(int(a_ / hop) + 2, int(b_ / hop))
        sm = np.convolve(db[lo:hi], np.ones(12) / 12, mode="same"); cp.append((lo + int(np.argmin(sm))) * hop)
    cp.append(D); segs = []
    for i in range(len(script)):
        a_, b_ = int(cp[i] / hop), int(cp[i + 1] / hop); loud = np.where(db[a_:b_] > thr)[0]
        s0 = max(cp[i], (a_ + loud[0]) * hop - .05); s1 = min(cp[i + 1], (a_ + loud[-1]) * hop + .02 + .10)
        y = xn[int(s0 * SR):int(s1 * SR)]; tk, tt, txt = heard(resample_poly(y, 1, 3).astype(np.float32))
        segs.append(dict(s0=s0, s1=s1, txt=txt, toks=tk, ts=tt, sim=difflib.SequenceMatcher(None, norm(say_of(G[i])), norm(txt)).ratio(),
                         letters=len(norm(say_of(G[i]))), st=[v - s0 for v in st[first[i]:first[i + 1]]]))
    return segs, xn
def f0_of(y):
    s = parselmouth.Sound(resample_poly(y, 1, 3).astype(np.float64), sampling_frequency=16000)
    p = s.to_pitch_ac(time_step=0.01, pitch_floor=60, pitch_ceiling=400, very_accurate=True, octave_cost=0.02, octave_jump_cost=0.9).selected_array["frequency"]
    return p[p > 0]
def metrics(y, letters):
    db, hop = rms_db(y); sp = np.percentile(db, 95); pz = runs_below(db, hop, sp - 30); pd = np.array([b - a for a, b in pz]) if pz else np.zeros(0)
    v = f0_of(y); d = dict(dur=len(y) / SR, sp=sp, floor=float(np.percentile(db, 2)), n_p=len(pd), p_tot=float(pd.sum()), p_max=float(pd.max()) if len(pd) else 0.0,
                           rate=letters / max(.5, len(y) / SR - float(pd.sum())), dyn=float(np.percentile(db[db > sp - 30], 95) - np.percentile(db[db > sp - 30], 30)))
    if len(v) > 20:
        d.update(f0=float(np.median(v)), f90=float(np.percentile(v, 90)), f98=float(np.percentile(v, 98)), rng=float(12 * np.log2(np.percentile(v, 90) / np.percentile(v, 10))))
    else: d.update(f0=0, f90=0, f98=0, rng=0)
    return d
if __name__ == "__main__":
    script = json.load(open(sys.argv[1])); res = {}
    for f in sys.argv[2:]:
        x = load(f); segs, xn = locate(x, script); name = os.path.basename(f); rows = []
        dbw, hop = rms_db(xn); print(f"\n== {name}: {len(x) / SR:.1f} s, zgomot de fond (p2 al nivelului) {np.percentile(dbw, 2) - 20 * np.log10(.9 / max(1e-6, np.abs(x).max())):.1f} dBFS în fișier")
        for i, q in enumerate(segs):
            m = metrics(xn[int(q["s0"] * SR):int(q["s1"] * SR)], q["letters"]); m.update(sim=q["sim"], s0=q["s0"], s1=q["s1"]); rows.append(m)
            print(f"[{i:2d}] {m['dur']:5.2f}s sim {m['sim']:.2f} | F0 med {m['f0']:3.0f} p90 {m['f90']:3.0f} p98 {m['f98']:3.0f} int {m['rng']:4.1f} st | {m['rate']:4.1f} lit/s | pauze {m['n_p']} tot {m['p_tot']:.2f} max {m['p_max']:.2f} | {q['txt'][:70]}")
        A = lambda k: float(np.mean([r[k] for r in rows])); W = lambda k: float(np.sum([r[k] * r['dur'] for r in rows]) / np.sum([r['dur'] for r in rows]))
        print(f"   MEDIE: sim {A('sim'):.3f} | F0 med {W('f0'):.0f} p90 {W('f90'):.0f} p98 {W('f98'):.0f} interval {W('rng'):.1f} st | {W('rate'):.1f} lit/s | pauze: {sum(r['n_p'] for r in rows)} tot {sum(r['p_tot'] for r in rows):.1f}s, max {max(r['p_max'] for r in rows):.2f}s | vorbire {sum(r['dur'] for r in rows):.1f}s")
        res[name] = rows
    json.dump(res, open(os.environ.get("QC_OUT", "/tmp/vo_qc.json"), "w"))
