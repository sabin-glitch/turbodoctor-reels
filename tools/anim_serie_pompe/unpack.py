"""Splits the voice packs fetched on branch `sources` (sppk<asset>.mp4: the takes of one sandbox call, each followed by 0.6 s of digital
silence) into ep<N>/vo_in/p<N>_L<NN><x>.flac. The CDN serves a re-muxed/re-encoded preview, so the split is done on the decoded audio:
the takes are found one after another, each ending at the silent gap nearest to its expected end (durations come from the manifest).
Run with python3 -I (the packs are downloaded data)."""
import json, os, subprocess, sys
import numpy as np
W = '/home/claude/w/serpmp'; R = '/home/claude/turbodoctor-reels'; SR = 44100
packs = json.load(open(f'{W}/packs.json')); got = json.load(open(f'{W}/packs_got.json')) if os.path.exists(f'{W}/packs_got.json') else []
names = json.load(open(f'{W}/take_names.json')); done = json.load(open(f'{W}/fetched.json')) if os.path.exists(f'{W}/fetched.json') else {}
ls = subprocess.run(['git', '-C', R, 'ls-tree', '--name-only', 'FETCH_HEAD'], capture_output=True, text=True).stdout.split()
os.makedirs(f'{W}/packs_in', exist_ok=True)
for p in packs:
    a = p['asset']; f = f'sppk{a}.mp4'
    if a in got: continue
    if f not in ls: print('not on the branch yet:', f); continue
    raw = subprocess.run(['git', '-C', R, 'show', f'FETCH_HEAD:{f}'], capture_output=True).stdout
    src = f'{W}/packs_in/{a}.mp3'; open(src, 'wb').write(raw)
    x = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', src, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout, np.float32)
    B = 220; nb = len(x) // B; e = np.abs(x[:nb * B]).reshape(nb, B).max(1); q = e < 2e-4          # 5 ms blocks, quiet = below -74 dBFS
    runs = []; i = 0
    while i < nb:
        if q[i]:
            j = i
            while j < nb and q[j]: j += 1
            if (j - i) * B / SR >= .40: runs.append((i * B, j * B))
            i = j
        else: i += 1
    pos = 0; out = []; ok = True
    for n, _, d in p['man']:
        g = pos + d * SR
        c = [r for r in runs if r[1] > pos + .3 * SR and abs(r[0] - g) < .6 * SR]
        if not c: print('  NO GAP for', n, 'in', a); ok = False; break
        r = min(c, key=lambda r: abs(r[0] - g))
        out.append((n, pos, min(r[0] + int(.03 * SR), r[1]), (r[0] - pos) / SR - d)); pos = max(r[1] - int(.03 * SR), r[0])
    if not ok or len(out) != len(p['man']): print('SPLIT FAILED', a, 'gaps found', len(runs), 'takes', len(p['man'])); continue
    worst = max(abs(o[3]) for o in out)
    for n, s0, s1, _ in out:
        ep = n[2:n.index('L')]; d = f'{W}/ep{ep}/vo_in'; os.makedirs(d, exist_ok=True)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', '-c:a', 'flac', f"{d}/p{ep}_{n[n.index('L'):]}.flac"],
                       input=x[s0:s1].tobytes(), check=True)
        done[n] = names.get(n, '?')
    got.append(a); print('pack', a, 'ok:', len(out), 'takes,', len(runs), 'gaps, largest duration difference', round(worst, 3), 's, total', round(len(x) / SR, 1), 's')
json.dump(got, open(f'{W}/packs_got.json', 'w')); json.dump(done, open(f'{W}/fetched.json', 'w'))
print('takes fetched in total', len(done))
