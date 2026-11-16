"""Hook v7 (16.11, cerut de Sabin): în timp ce motorul se turează, vocea spune „Turbina o ia pe ulei! Află de ce.” (rândul 0, la T_A);
rândul „Știi de ce se întâmplă asta? Hai să-ți explic inginerește.” rămâne la locul lui (5,4 s) și devine rândul 1.
Pornește mereu de la vocea și cronologia v6 (copiile din /tmp/v6_reel), deci poate fi rulat de mai multe ori.
  python3 splice_hook_vo2.py <T_A> [pauza_suplimentară_între_propoziții=0]"""
import json, sys, numpy as np, soundfile as sf
# rândul asamblat: „Turbina o ia pe ulei!” (varianta b) + „Află de ce!” generat separat, ferm (varianta e) – /tmp/hookvo3
R = "/home/claude/reels/runaway_diesel"; H = "/tmp/hookvo3/vo"; B = "/tmp/v6_reel"; SR = 48000
T_A = float(sys.argv[1]); XGAP = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0
vo, sr = sf.read(f"{B}/vo_track.wav", dtype="float32"); assert sr == SR
hk, sr2 = sf.read(f"{H}/vo_track.wav", dtype="float32"); assert sr2 == SR
if vo.ndim > 1: vo = vo.mean(1)
if hk.ndim > 1: hk = hk.mean(1)
cues = json.load(open(f"{H}/cues.json")); hend = cues["lines"][0]["end"]; words = [dict(w) for w in cues["words"]]
hk = hk[:int(round((hend + 0.06) * SR))]
def act_db(x):                                     # nivelul pe porțiunile vorbite
    f = int(.02 * SR); k = len(x) // f; r = np.sqrt((x[:k * f].reshape(k, f) ** 2).mean(1) + 1e-12); a = r[r > r.max() * .1]; return 20 * np.log10(np.sqrt((a ** 2).mean()))
ref = act_db(vo[int(10.4 * SR):int(40 * SR)]); cur = act_db(hk); hk = hk * 10 ** ((ref - cur) / 20)
# vocea generată lasă „Află de ce.” mult mai încet decât prima propoziție (măsurat: ~7 dB, iar „ce” încă 8 dB mai jos), deci peste motor s-ar pierde.
# 1) fiecare propoziție e adusă la nivelul narațiunii (a doua cu PUNCH dB în plus: e poanta hook-ului); 2) în interiorul propoziției,
# silabele slabe sunt ridicate lin cu cel mult LEV_MAX dB. Pauzele sunt goale (voce generată), deci nu se ridică niciun zgomot.
PUNCH, LEV_MAX = float(sys.argv[3]) if len(sys.argv) > 3 else 1.5, 5.0
hop = int(.01 * SR)
def intervals(x, thr=-45.0):
    e = 20 * np.log10(np.sqrt((x[:len(x) // hop * hop].reshape(-1, hop) ** 2).mean(1)) + 1e-9); on = e > thr
    ed = np.flatnonzero(np.diff(np.concatenate([[0], on.astype(int), [0]]))); out = []
    for a_, b_ in zip(ed[::2], ed[1::2]):
        a_, b_ = a_ * .01, b_ * .01
        if out and a_ - out[-1][1] < 0.22: out[-1] = (out[-1][0], b_)
        elif b_ - a_ > 0.04: out.append((a_, b_))
    return out
iv0 = intervals(hk); tt = np.arange(len(hk)) / SR
pts_t, pts_g = [], []
for k_, (a_, b_) in enumerate(iv0):
    g_ = ref - act_db(hk[int(a_ * SR):int(b_ * SR)]) + (PUNCH if k_ == len(iv0) - 1 and len(iv0) > 1 else 0.0)
    pts_t += [a_ - 0.03, b_ + 0.03]; pts_g += [g_, g_]
hk = hk * 10 ** (np.interp(tt, pts_t, pts_g) / 20)
w = int(.08 * SR); cs = np.concatenate([[0], np.cumsum(hk.astype(np.float64) ** 2)]); cen = np.arange(0, len(hk), hop)
lv = 10 * np.log10((cs[np.clip(cen + w // 2, 0, len(hk))] - cs[np.clip(cen - w // 2, 0, len(hk))]) / w + 1e-12)
gain = np.where(lv > -40, np.clip((ref - 1.0) - lv, 0.0, LEV_MAX), np.nan)
idx = np.flatnonzero(~np.isnan(gain)); gain = np.interp(np.arange(len(gain)), idx, gain[idx])
k = np.hanning(15); k /= k.sum(); gain = np.convolve(np.pad(gain, 7, mode="edge"), k, mode="valid")
hk = hk * 10 ** (np.interp(np.arange(len(hk)), cen, gain) / 20)
pk = np.abs(hk).max()
if pk > 0.7: hk = np.tanh(hk / 0.7 * 0.9) * 0.7 / np.tanh(0.9)
print(f"voice level: narration {ref:.1f} dB; sentence gains {[round(float(g), 1) for g in pts_g[::2]]} dB, syllable lift up to +{gain.max():.1f} dB; "
      f"sentences now {[round(float(act_db(hk[int(a_ * SR):int(b_ * SR)])), 1) for a_, b_ in iv0]} dB, peak {20*np.log10(np.abs(hk).max()):.1f} dBFS")
if XGAP > 0:                                       # pauză mai lungă între „…pe ulei!” și „Află de ce.” (tăietura în mijlocul pauzei)
    i_af = next(k for k, w in enumerate(words) if w["text"].lower().startswith("afl")); t_cut = words[i_af]["s"] - 0.12
    c = int(t_cut * SR); hk = np.concatenate([hk[:c], np.zeros(int(XGAP * SR), np.float32), hk[c:]])
    for w in words[i_af:]:
        for k in ("s", "e", "os", "oe"): w[k] = round(w[k] + XGAP, 3)
    words[i_af - 1]["e"] = round(words[i_af - 1]["e"], 3); hend += XGAP
old0 = json.load(open(f"{B}/timeline.json"))["sentences"][0]
assert T_A + hend < old0["start"] - 0.5, "the new line runs into the next one"
assert np.abs(vo[:int((old0["start"] - 0.3) * SR)]).max() < 1e-4
o = int(round(T_A * SR)); vo[o:o + len(hk)] += hk
sf.write(f"{R}/audio/vo_track.wav", vo, SR, subtype="FLOAT")
# începuturile de propoziție se iau din anvelopa vocii (ASR-ul le pune cu până la ~0,15 s mai devreme, în pauză)
iv = intervals(hk)
print("speech intervals in the take:", [(round(a, 2), round(b, 2)) for a, b in iv])
for k_, w_ in enumerate(words):
    first = k_ == 0 or (k_ > 0 and any(abs(a - w_["s"]) < 0.25 and a - iv[j - 1][1] > 0.25 for j, (a, b) in enumerate(iv) if j > 0))
    if first:
        a = min((a for a, b in iv), key=lambda a: abs(a - w_["s"]))
        if k_ > 0: words[k_ - 1]["e"] = words[k_ - 1]["oe"] = round(max(b for a2, b in iv if b <= a + 1e-6), 3)
        w_["s"] = w_["os"] = round(a, 3)
new_words = [dict(text=w["text"], s=round(w["s"] + T_A, 3), e=round(w["e"] + T_A, 3), os=round(w["os"] + T_A, 3), oe=round(w["oe"] + T_A, 3), win=0) for w in words]
text = cues["lines"][0]["text"]
for name in ("timeline.json", "timeline_1x.json"):
    try: tl = json.load(open(f"{B}/{name}"))
    except FileNotFoundError: continue
    olds = [dict(w, win=1) for w in tl["words"] if w["win"] == 0]
    tl["words"] = new_words + olds + [w for w in tl["words"] if w["win"] not in (0, 1)]
    s0 = tl["sentences"][0]
    tl["sentences"][1] = dict(i=1, start=s0["start"], end=s0["end"], text=s0["text"])
    tl["sentences"][0] = dict(i=0, start=round(T_A, 3), end=round(T_A + hend, 3), text=text)
    json.dump(tl, open(f"{R}/out/{name}", "w"), ensure_ascii=False, indent=1)
    print(name, "words", len(tl["words"]), "| s0", tl["sentences"][0], "| s1", tl["sentences"][1])
json.dump({"T_A": T_A, "end": round(T_A + hend, 3), "words": [(w["text"], w["s"], w["e"]) for w in new_words]}, open(f"{R}/audio/hook_line0.json", "w"), ensure_ascii=False)
print("line 0:", [(w["text"], w["s"]) for w in new_words], "end", round(T_A + hend, 3))
