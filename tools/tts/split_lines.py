"""Split one narration file (ElevenLabs take of the whole vo_script.json, lines separated by paragraph pauses) into one WAV per line.
Usage: split_lines.py <narration.mp3> <vo_script.json> <out_dir>   -> <out_dir>/NN.wav (48 kHz mono) + <out_dir>/split.json
Alignment: Silero VAD + Parakeet (word timestamps) on the whole file, then the normalised character stream of the ASR output is matched
against the concatenated script (difflib); each line's first/last matched characters give its start/end; cuts fall in the gap between lines."""
import sys, json, os, re, unicodedata, difflib, subprocess
import numpy as np, soundfile as sf, sherpa_onnx
from scipy.signal import resample_poly

src, script_p, out = sys.argv[1], sys.argv[2], sys.argv[3]; os.makedirs(out, exist_ok=True)
M = os.environ.get("TD_MODELS", "/home/claude/models"); PK = M + "/sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8"
SR = 48000
tmp = out + "/_full48.wav"
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", src, "-ac", "1", "-ar", str(SR), "-c:a", "pcm_f32le", tmp], check=True)
x48, _ = sf.read(tmp, dtype="float32"); x16 = resample_poly(x48, 16000, SR).astype(np.float32)
lines = [L["text"] for L in json.load(open(script_p))]

def norm(s):
    s = unicodedata.normalize("NFD", s.lower()); s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return "".join(c for c in s if c.isalnum())

# ---- VAD segments
vad = sherpa_onnx.VoiceActivityDetector(sherpa_onnx.VadModelConfig(silero_vad=sherpa_onnx.SileroVadModelConfig(model=M + "/silero_vad.onnx", threshold=0.5, min_silence_duration=0.25, min_speech_duration=0.1, max_speech_duration=20)), buffer_size_in_seconds=400)
segs = []; W = 512
for i in range(0, len(x16), W):
    vad.accept_waveform(x16[i:i + W])
    while not vad.empty(): s = vad.front; segs.append((s.start / 16000, s.start / 16000 + len(s.samples) / 16000)); vad.pop()
vad.flush()
while not vad.empty(): s = vad.front; segs.append((s.start / 16000, s.start / 16000 + len(s.samples) / 16000)); vad.pop()
print("vad segments", len(segs))

# ---- ASR per segment -> char stream with times
asr = sherpa_onnx.OfflineRecognizer.from_transducer(encoder=f"{PK}/encoder.int8.onnx", decoder=f"{PK}/decoder.int8.onnx", joiner=f"{PK}/joiner.int8.onnx", tokens=f"{PK}/tokens.txt", num_threads=2, model_type="nemo_transducer")
chars, times, heard = [], [], []
for a, b in segs:
    seg = x16[int(a * 16000):int(b * 16000)]
    st = asr.create_stream(); st.accept_waveform(16000, np.concatenate([np.zeros(1600, np.float32), seg, np.zeros(3200, np.float32)])); asr.decode_stream(st)
    toks = list(st.result.tokens); ts = [float(t) - 0.1 + a for t in st.result.timestamps]; heard.append(st.result.text)
    for k, tok in enumerate(toks):
        t0 = ts[k]; t1 = ts[k + 1] if k + 1 < len(ts) else t0 + .24; n = norm(tok)
        for j, ch in enumerate(n): chars.append(ch); times.append(t0 + (t1 - t0) * j / max(1, len(n)))
pstr = "".join(chars)
# ---- align script chars to ASR chars
cstr, first, last = "", [], []
for L in lines: n = norm(L); first.append(len(cstr)); cstr += n; last.append(len(cstr) - 1)
cmap = {}
for a, b, n in difflib.SequenceMatcher(None, cstr, pstr, autojunk=False).get_matching_blocks():
    for q in range(n): cmap[a + q] = b + q
ratio = len(cmap) / max(1, len(cstr)); print(f"alignment: {ratio:.2f} of script chars matched")
bounds = []
for i, L in enumerate(lines):
    ks = [k for k in range(first[i], last[i] + 1) if k in cmap]
    if len(ks) < 0.3 * (last[i] - first[i] + 1): print(f"!! line {i} poorly matched ({len(ks)} chars)")
    s = times[cmap[ks[0]]] if ks else None; e = times[cmap[ks[-1]]] + .25 if ks else None
    bounds.append([s, e])
for i in range(len(bounds)):  # fill holes from neighbours
    if bounds[i][0] is None: bounds[i][0] = bounds[i - 1][1] if i else 0.0
    if bounds[i][1] is None: bounds[i][1] = bounds[i + 1][0] if i + 1 < len(bounds) and bounds[i + 1][0] else len(x48) / SR
# ---- cut points: in the VAD silence between consecutive lines (closest gap to the next line's first word); fallback just before it
gaps = [(segs[k][1], segs[k + 1][0]) for k in range(len(segs) - 1)]
cuts = [0.0]
for i in range(1, len(lines)):
    pe, ns = bounds[i - 1][1], bounds[i][0]
    cand = [g for g in gaps if g[0] >= pe - 0.6 and g[1] <= ns + 0.15]
    if cand:
        g = min(cand, key=lambda g: abs(g[1] - ns)); c = max(g[0] + 0.06, g[1] - 0.12) if g[1] - g[0] > 0.18 else (g[0] + g[1]) / 2
        print(f"   cut {i:02d}: vad gap {g[0]:.2f}-{g[1]:.2f} ({g[1] - g[0]:.2f}s) -> {c:.2f}")
    else:  # short pause: cut at the quietest 20 ms between the end of the previous line and the start of the next
        lo, hi = max(0, int((pe - 0.45) * SR)), min(len(x48), int((ns + 0.06) * SR)); w = int(0.02 * SR)
        r = [(float(np.sqrt(np.mean(x48[j:j + w] ** 2))), j) for j in range(lo, hi - w, w // 2)]
        rm, j = min(r); c = (j + w / 2) / SR; print(f"   cut {i:02d}: no vad gap near {ns:.2f}, quietest point {c:.2f} (rms {20 * np.log10(rm + 1e-9):.0f} dB)")
    cuts.append(c)
cuts.append(len(x48) / SR)
info = []
for i, L in enumerate(lines):
    a, b = cuts[i], cuts[i + 1]
    y = x48[int(a * SR):int(b * SR)].copy(); f = int(.012 * SR); y[:f] *= np.linspace(0, 1, f); y[-f:] *= np.linspace(1, 0, f)
    sf.write(f"{out}/{i:02d}.wav", y, SR, subtype="FLOAT")
    info.append(dict(i=i, a=round(a, 3), b=round(b, 3), dur=round(b - a, 2), speech=[round(bounds[i][0], 2), round(bounds[i][1], 2)], text=L))
    print(f"[{i:02d}] {a:7.2f}-{b:7.2f}  dur {b - a:5.2f}  speech {bounds[i][0]:.2f}-{bounds[i][1]:.2f}  {L[:60]}")
json.dump(dict(lines=info, heard=heard, ratio=ratio), open(f"{out}/split.json", "w"), ensure_ascii=False, indent=1)
os.remove(tmp)
