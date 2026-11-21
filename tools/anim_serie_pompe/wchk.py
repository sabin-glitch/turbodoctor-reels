"""Whisper second opinion on the picked take of every generated line of one episode; where it differs from the script, the other takes too.
  ./run_iso.sh wchk.py <epdir>     (needs <epdir>/vo/picks.json and <epdir>/vo_in)"""
import os, sys, re, glob, json, subprocess, unicodedata, difflib
import numpy as np, sherpa_onnx
M = os.environ.get("TD_MODELS", "/home/claude/models"); WH = M + "/sherpa-onnx-whisper-turbo"
D = sys.argv[1].rstrip("/"); S = json.load(open(D + "/vo_script.json")); P = {p["i"]: p for p in json.load(open(D + "/vo/picks.json"))}
wh = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=f"{WH}/turbo-encoder.int8.onnx", decoder=f"{WH}/turbo-decoder.int8.onnx", tokens=f"{WH}/turbo-tokens.txt",
                                                language="ro", task="transcribe", num_threads=4)
def load(f):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()
def rec(x):
    s = wh.create_stream(); s.accept_waveform(16000, np.concatenate([np.zeros(3200, np.float32), x, np.zeros(4800, np.float32)])); wh.decode_stream(s); return s.result.text.strip()
def spoken(t): return re.sub(r"\{[^|}]*\|([^}]*)\}", r"\1", t)
def norm(t):
    t = unicodedata.normalize("NFD", t.lower()); t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9 ]+", " ", t.replace("-", " ")).split()
def diff(a, b):
    out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op != "equal": out.append(f"{' '.join(a[i1:i2]) or '∅'}→{' '.join(b[j1:j2]) or '∅'}")
    return out
res = []; n = len(S); ep = os.path.basename(D)
for i in range(n):
    if i == 1 or i >= n - 3: continue
    ref = norm(spoken(S[i]["text"])); fs = sorted(glob.glob(f"{D}/vo_in/*L{i:02d}[a-z].*")); tk = {re.search(r"L\d\d([a-z])\.", f).group(1): f for f in fs}
    pk = P[i]["take"]; d = diff(ref, norm(rec(load(tk[pk])))); row = dict(i=i, pick=pk, d={pk: d})
    if d:
        for k, f in tk.items():
            if k != pk: row["d"][k] = diff(ref, norm(rec(load(f))))
        print(f"{ep} L{i:02d} pick {pk}: " + " || ".join(f"{k}: {'; '.join(v) if v else 'OK'}" for k, v in row["d"].items()), flush=True)
    res.append(row)
json.dump(res, open(D + "/vo/wchk.json", "w"), ensure_ascii=False, indent=1); print(ep, "checked", len(res), "lines,", sum(1 for r in res if r["d"][r["pick"]]), "differ", flush=True)
