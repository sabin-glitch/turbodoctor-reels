"""Both ASR models on the picked take of every generated line; word diff against the spoken text.
python3 -I asr_picked.py <epdir> [all]"""
import os, sys, re, glob, json, subprocess, difflib, unicodedata
import numpy as np, sherpa_onnx
M = "/home/claude/models"; PK = M + "/sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8"; WH = M + "/sherpa-onnx-whisper-turbo"
E = sys.argv[1].rstrip('/'); S = json.load(open(E + "/vo_script.json")); P = json.load(open(E + "/vo/picks.json"))
ALL = len(sys.argv) > 2 and sys.argv[2] == 'all'
pk = sherpa_onnx.OfflineRecognizer.from_transducer(encoder=f"{PK}/encoder.int8.onnx", decoder=f"{PK}/decoder.int8.onnx", joiner=f"{PK}/joiner.int8.onnx",
                                                   tokens=f"{PK}/tokens.txt", num_threads=2, model_type="nemo_transducer")
wh = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=f"{WH}/turbo-encoder.int8.onnx", decoder=f"{WH}/turbo-decoder.int8.onnx", tokens=f"{WH}/turbo-tokens.txt",
                                                language="ro", task="transcribe", num_threads=4)
def load(f):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()
def rec(r, x):
    s = r.create_stream(); s.accept_waveform(16000, np.concatenate([np.zeros(3200, np.float32), x, np.zeros(4800, np.float32)])); r.decode_stream(s); return s.result.text.strip()
def say(t): return re.sub(r"\{([^|}]*)\|([^}]*)\}", r"\2", t)
def norm(t):
    t = t.lower().replace('ş', 'ș').replace('ţ', 'ț')
    t = re.sub(r"[^\w\s-]", " ", t); return t.split()
n = re.search(r"ep(\d+)$", E).group(1)
for p in P:
    i = p['i']; cands = p.get('cands', [])
    if len(cands) < 2 and not ALL: continue
    takes = [c['take'] for c in cands] if ALL else [p['take']]
    for tk in takes:
        f = glob.glob(f"{E}/vo_in/i{n}_L{i:02d}{tk}.*")[0]
        x = load(f); a = rec(pk, x); b = rec(wh, x)
        ref = norm(say(S[i]['text']))
        flags = []
        for name, hyp in (('P', a), ('W', b)):
            sm = difflib.SequenceMatcher(None, ref, norm(hyp))
            d = [f"{' '.join(ref[i1:i2])}→{' '.join(norm(hyp)[j1:j2])}" for op, i1, i2, j1, j2 in sm.get_opcodes() if op != 'equal']
            flags.append((name, d))
        star = '*' if tk == p['take'] else ' '
        print(f"[ep{n} {i:2d}{tk}{star}] T: {say(S[i]['text'])}\n      P: {a}\n      W: {b}")
        for name, d in flags:
            if d: print(f"      {name}-diff: {' | '.join(d)}")
        sys.stdout.flush()
