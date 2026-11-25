# Taie pachetele (vo/raw/sdbNN.mp3, aduse prin fetch-sources) în rânduri: vo/takes/L###.wav (44,1 kHz mono), tăiate de liniște, + vo/meas.json.
# Verifică fiecare rând cu Parakeet (recunoaștere de vorbire): vo/asr.json.   python3 vo_split.py [NN ...]
import json, subprocess, os, sys, re, unicodedata, difflib, numpy as np, soundfile as sf
SR = 44100; os.makedirs('vo/takes', exist_ok=True)
P = json.load(open('vo/packs.json')); L = json.load(open('vo/lines.json'))['lines']
MP = 'vo/meas.json'; M = json.load(open(MP)) if os.path.exists(MP) else {}
AP = 'vo/asr.json'; A = json.load(open(AP)) if os.path.exists(AP) else {}
import sherpa_onnx
PK = '/home/claude/work/models/sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8'
asr = sherpa_onnx.OfflineRecognizer.from_transducer(encoder=f'{PK}/encoder.int8.onnx', decoder=f'{PK}/decoder.int8.onnx', joiner=f'{PK}/joiner.int8.onnx', tokens=f'{PK}/tokens.txt', num_threads=2, model_type='nemo_transducer')
def norm(s):
    s = unicodedata.normalize('NFD', s.lower()); s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9 ]', ' ', s).split()
def rec(x):
    y = np.interp(np.arange(0, len(x), SR / 16000.0), np.arange(len(x)), x).astype(np.float32)
    st = asr.create_stream(); st.accept_waveform(16000, y); asr.decode_stream(st)
    r = st.result; return r.text, list(zip(r.tokens, r.timestamps))
for b in (sys.argv[1:] or sorted(P['lens'])):
    f = f'vo/raw/sdb{b}.mp3'
    if not os.path.exists(f): print('lipsă', f); continue
    x = np.frombuffer(subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', f, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout, np.float32)
    lens = P['lens'][b]; exp = sum(lens) + len(lens) * (SR // 2); off = 0
    # the preview is an MP3 copy: find the small constant delay from the first gap
    t = lens[0]; best = None
    for o in range(-2500, 4000, 50):
        g = np.abs(x[max(0, t + o + 2000):t + o + SR // 2 - 2000]).max()
        if best is None or g < best[0]: best = (g, o)
    off = best[1]; t = 0
    for j, n in enumerate(lens):
        i = int(b) * 20 + j; alt = ''
        if i >= len(L): i = P['retakes'][i - len(L)]; alt = 'r'
        seg = x[max(0, t + off - 1500):t + off + n + 1500]; t += n + SR // 2
        e = np.abs(seg); thr = max(0.012, 0.03 * e.max()); nz = np.nonzero(e > thr)[0]
        a0 = max(0, nz[0] - int(0.05 * SR)); a1 = min(len(seg), nz[-1] + int(0.12 * SR)); y = seg[a0:a1].copy()
        k = int(0.012 * SR); y[:k] *= np.linspace(0, 1, k); y[-k:] *= np.linspace(1, 0, k)
        sf.write(f'vo/takes/L{i:03d}{alt}.wav', y, SR, subtype='PCM_16')
        # pauses inside the line
        fr = int(0.02 * SR); en = np.array([np.abs(y[q:q + fr]).max() for q in range(0, len(y) - fr, fr)]); q = en < thr; run = mx = 0
        for v in q:
            run = run + 1 if v else 0; mx = max(mx, run)
        text, toks = rec(y); want = norm(L[i]['v']); got = norm(text)
        r = max(difflib.SequenceMatcher(None, ' '.join(w_), ' '.join(got)).ratio() for w_ in (want, norm(L[i]['show'])))
        # word start times (first token of each word)
        ws = []; cur = ''; t0 = 0
        for tk, ts in toks:
            if tk.startswith(' ') or not cur:
                if cur.strip(): ws.append([cur.strip(), round(t0, 2)])
                cur = tk; t0 = ts
            else: cur += tk
        if cur.strip(): ws.append([cur.strip(), round(t0, 2)])
        M[str(i) + alt] = dict(sp=round(len(y) / SR, 3), pause=round(mx * 0.02, 2), peak=round(float(e.max()), 3), rms=round(float(np.sqrt((y ** 2).mean())), 4))
        A[str(i) + alt] = dict(r=round(r, 3), text=text, words=ws)
        flag = '' if r > 0.93 else '   <<<<'
        if flag or alt or M[str(i) + alt]['pause'] > 0.75: print(i, alt, M[str(i) + alt]['sp'], 'pauză', M[str(i) + alt]['pause'], round(r, 2), '|', text, '|', L[i]['v'] if flag else '', flag)
    print('pachet', b, 'decalaj', off, 'lungime', len(x), 'așteptat', exp)
json.dump(M, open(MP, 'w')); json.dump(A, open(AP, 'w'), ensure_ascii=False)
