# Pista de voce a unui episod: rândurile (vo/takes) puse la timpii din vo/epNN/cues.json, egalizate ca tărie.  python3 vo_ep.py N
import json, sys, os, subprocess, numpy as np, soundfile as sf
ep = int(sys.argv[1]); d = f'vo/ep{ep:02d}'; C = json.load(open(d + '/cues.json')); SR = 44100
PICK = json.load(open('vo/pick.json')) if os.path.exists('vo/pick.json') else {}
out = np.zeros(int((C['dur'] + 0.2) * SR), np.float32)
def act_rms(y):
    fr = int(0.05 * SR); e = np.array([np.sqrt((y[q:q + fr] ** 2).mean()) for q in range(0, len(y) - fr, fr)]); e = e[e > 0.25 * e.max()]
    return float(np.sqrt((e ** 2).mean()))
for ev in C['events']:
    k = ev['line']; y, _ = sf.read(f"vo/takes/L{k:03d}{PICK.get(str(k), '')}.wav", dtype='float32')
    y = y * (0.085 / act_rms(y)); a = int(ev['t'] * SR); out[a:a + len(y)] += y[:len(out) - a]
sf.write(d + '/raw.wav', out, SR, subtype='PCM_16')
subprocess.run(['ffmpeg', '-y', '-nostdin', '-loglevel', 'error', '-i', d + '/raw.wav', '-af', 'highpass=f=70,loudnorm=I=-16:TP=-1.5:LRA=11:linear=true,alimiter=limit=0.84:level=false', '-ar', '48000', '-ac', '2', d + '/vo_track.wav'], check=True)
r = subprocess.run(['ffmpeg', '-nostdin', '-i', d + '/vo_track.wav', '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
print(ep, [l.strip() for l in r.splitlines() if l.strip().startswith(('I:', 'Peak:'))][-2:])
