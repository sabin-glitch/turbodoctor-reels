"""Cold open FĂRĂ repetare, făcut direct în sursă (reel-ul „O nouă viață la doar 30–40% din costul unei turbine noi”, 17.11.2026).
Sabin a cerut ca hook fraza pe care o spune la sfârșitul ultimului clip. Fraza se mută la început cu imaginea și vocea ei,
restul rulează în ordinea filmată, fără tăieturi, iar fraza nu se mai aude a doua oară la final:
    [c2 de la cadrul K] + [c1 întreg] + [c2 până la cadrul K]        (nimic nu se repetă, nimic nu se pierde)
c1, c2 = clipurile trecute prin pipeline/sdr.sh (1080x1920, 30 fps, SDR). K = cadrul din c2 de la care începe fraza (cu ~0,12 s înainte de primul cuvânt).
Sunetul se ia din filmările originale (.mov), ca să nu mai treacă printr-o recodare; la îmbinări are fade de 12 ms.
Tot aici: pe hârtia de lângă geometria veche (fișa clientului) semnătura și scrisul de mână se estompează cu cadre-cheie interpolate
pe fiecare cadru (KEYS, în numerotarea filmării lipite c1+c2). Verificarea se face cu tools/cold_open/sigcheck.py (contrast local, cadru cu cadru).
    python3 build_src_noua_viata.py <c1.mp4> <c2.mp4> <IMG_2563.mov> <IMG_2564.mov> <out.mp4> [keys.json]
Apoi: new_reel.sh <slug> <out.mp4>, transcribe.py, transcribe2.py, out/curated.json, build_timeline.py, fix_words.py, retime.py, extract_frames.py.
În out/v2.json: "tip": {"dur": 4.2, "src": 0.0, "speed": 0.7} — Rețeta rulează pe continuarea firească a ultimului cadru al poveștii (începutul hook-ului, încetinit)."""
import subprocess, sys, json
import numpy as np, cv2, soundfile as sf
c1, c2, mov1, mov2, out = sys.argv[1:6]
W, H, FPS, SR = 1080, 1920, 30, 48000
N1, N2 = 586, 567          # cadre în c1 / c2 (30 fps)
K = 938 - N1               # cadrul din c2 de la care începe hook-ul (orig 31,267 s; vocea începe la 31,385 s)
# cadre-cheie (număr de cadru în filmarea lipită, 30 fps): [cadru, x0, y0, x1, y1]
KEYS = [
  [[775,150,730,290,880],[777,170,700,290,840],[780,190,650,320,790],[783,205,620,330,770],[786,200,575,330,730],[789,205,530,330,680],[792,200,490,340,645],[795,140,385,310,575],[798,55,235,240,450],[801,0,10,130,190],[803,0,0,80,80]],   # semnătura, prima apariție
  [[777,40,560,190,650],[780,60,520,200,600],[783,65,485,205,565],[786,0,430,195,540],[789,0,400,225,520],[792,0,325,200,445],[795,0,215,145,340],[798,0,50,100,200]],                                                              # scrisul de mână
  [[877,60,230,260,380],[879,110,420,300,590],[881,170,520,330,680],[883,190,590,320,750],[885,160,690,320,830],[887,160,750,310,910],[889,120,850,250,1000],[891,60,950,200,1090],[893,0,1040,150,1200]],                          # semnătura, a doua apariție
]
if len(sys.argv) > 6: KEYS = json.load(open(sys.argv[6]))
def boxes(n):
    r = []
    for ks in KEYS:
        if not (ks[0][0] <= n <= ks[-1][0]): continue
        for a, b in zip(ks, ks[1:]):
            if a[0] <= n <= b[0]:
                k = (n - a[0]) / ((b[0] - a[0]) or 1); r.append([a[i] + (b[i] - a[i]) * k for i in range(1, 5)]); break
    return r
def soften(fr, n):
    bs = boxes(n)
    if not bs: return fr
    m = np.zeros((H, W), np.float32)
    for x0, y0, x1, y1 in bs: cv2.rectangle(m, (int(max(0, x0)), int(max(0, y0))), (int(min(W - 1, x1)), int(min(H - 1, y1))), 1.0, -1)
    ys, xs = np.where(m > 0); X0, X1, Y0, Y1 = max(0, xs.min() - 70), min(W, xs.max() + 71), max(0, ys.min() - 70), min(H, ys.max() + 71)
    a = cv2.GaussianBlur(m[Y0:Y1, X0:X1], (0, 0), 9)[..., None]; reg = fr[Y0:Y1, X0:X1].astype(np.float32)
    fr[Y0:Y1, X0:X1] = (cv2.GaussianBlur(reg, (0, 0), 20) * a + reg * (1 - a)).astype(np.uint8); return fr
def frames(path):
    p = subprocess.Popen(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", path, "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE); FB = W * H * 3; i = 0
    while True:
        b = p.stdout.read(FB)
        if len(b) < FB: break
        yield i, np.frombuffer(b, np.uint8).reshape(H, W, 3).copy(); i += 1
    p.wait()
enc = subprocess.Popen(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
    "-c:v", "libx264", "-preset", "veryfast", "-crf", "8", "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", out + ".v.mp4"], stdin=subprocess.PIPE)
n = 0
for i, fr in frames(c2):
    if i >= K: enc.stdin.write(fr.tobytes()); n += 1                       # hook: finalul lui IMG_2564
for i, fr in frames(c1): enc.stdin.write(fr.tobytes()); n += 1            # IMG_2563 întreg
for i, fr in frames(c2):
    if i < K: enc.stdin.write(soften(fr, N1 + i).tobytes()); n += 1        # IMG_2564 până la fraza mutată
enc.stdin.close(); enc.wait(); assert n == N1 + N2, n
# sunetul: din filmările originale, fără recodare intermediară
def wav(mov, nfr):
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", mov, "-map", "0:a:0", "-ac", "1", "-ar", str(SR), "-c:a", "pcm_f32le", "/tmp/_a.wav"], check=True)
    x, _ = sf.read("/tmp/_a.wav", dtype="float32"); L = round(nfr / FPS * SR); return x[:L] if len(x) >= L else np.concatenate([x, np.zeros(L - len(x), np.float32)])
a1, a2 = wav(mov1, N1), wav(mov2, N2); k = round(K / FPS * SR)
def fade(x, ms=12):
    x = x.copy(); f = int(ms / 1000 * SR); r = np.linspace(0, 1, f, dtype=np.float32); x[:f] *= r; x[-f:] *= r[::-1]; return x
a = np.concatenate([fade(a2[k:]), fade(a1), fade(a2[:k])]); sf.write(out + ".a.wav", a, SR, subtype="PCM_24")
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", out + ".v.mp4", "-i", out + ".a.wav", "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", out], check=True)
print(f"SRC_OK frames {n}  hook {(N2 - K) / FPS:.3f}s  story {(N1 + K) / FPS:.3f}s  audio {len(a) / SR:.3f}s")
