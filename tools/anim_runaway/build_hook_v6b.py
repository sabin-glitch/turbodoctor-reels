"""Hook v6 (16.11): un singur cadru continuu, fără tăietură – „turbina o ia pe ulei”, ca în filmările reale.
  - Golf 5 la ralanti → fum continuu pe țeavă care crește (Higgsfield Kling 3.0, clipul hf4_k0, cadrele 0..K0_N-1);
  - continuarea generată din cadrul K0_N al aceluiași clip (image-to-video, clipul CONT): fumul crește mai departe fără întrerupere,
    ușa șoferului se deschide, clientul sare de la volan, vine spre cameră și se ia cu mâinile de cap, în același decor.
Redarea: 1,25× (un cadru sursă de 24 fps pe fiecare cadru de 30 fps, deci fără cadre dublate și cu jetul de fum mai rapid),
cu 1,5× pe porțiunea în care se vede doar fumul, ca ușa să se deschidă înainte de vocea lui Sabin.
Continuarea Kling pornește mai moale decât clipul-sursă: îi potrivesc claritatea și luminozitatea la îmbinare, ca să nu se vadă trecerea.
Tot continuarea desenează un rând de litere fără sens pe buza hayonului (artefact AI): îl scoate tailgate_fix.py.
Scrie cadrele 0..N-1 (30 fps) în frames_base, harta cadrelor (audio/hook_map.json) și cantitatea de fum pe cadru (audio/hook_smoke.json).
  python3 build_hook_v6b.py <cont.mp4> [K0_N=54] [AICUT=7.1] [--dry]"""
import sys, json, os, subprocess, shutil, numpy as np, cv2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
args = [a for a in sys.argv[1:] if not a.startswith("--")]; DRY = "--dry" in sys.argv
CONT = args[0]; K0_N = int(args[1]) if len(args) > 1 else 54; AICUT = float(args[2]) if len(args) > 2 else 7.1
R = "/home/claude/reels/runaway_diesel"; TMP = "/tmp/hook6"; K0 = "/tmp/hf4/hf4_k0.mp4"
FPS_SRC, FPS = 24.0, 30
T_J = K0_N / FPS_SRC / 1.25                        # momentul îmbinării în reel (1,25× pe primul clip)
# viteza de redare în timp (s din reel → viteză); între chei, interpolare liniară
SPEED = [(0, 1.25), (T_J, 1.25), (T_J + .3, 1.5), (3.35, 1.5), (3.65, 1.25), (AICUT + 1, 1.25)]
REG = (800, 0, 1080, 420)                           # blocul din dreapta-sus: zonă statică, fără fum, pentru claritate și luminozitate
SH_N_CONT, GAIN_N = 84, 48

def read_all(path, a=0, b=10 ** 6):
    cap = cv2.VideoCapture(path); cap.set(1, a); out = []
    for _ in range(a, b):
        ok, im = cap.read()
        if not ok: break
        out.append(im)
    return out
def lapvar(im, reg=REG):
    x0, y0, x1, y1 = reg; g = cv2.cvtColor(im[y0:y1, x0:x1], cv2.COLOR_BGR2GRAY).astype(np.float32); return float(cv2.Laplacian(g, cv2.CV_32F).var())
def mean_reg(im, reg=REG):
    x0, y0, x1, y1 = reg; return float(im[y0:y1, x0:x1].mean())
def unsharp(im, a, sigma=1.2):
    if abs(a) < 1e-4: return im
    f = im.astype(np.float32); bl = cv2.GaussianBlur(f, (0, 0), sigma); return np.clip(np.rint(f + a * (f - bl)), 0, 255).astype(np.uint8)
def solve(fn, im, target, lo, hi):
    for _ in range(18):
        mid = (lo + hi) / 2
        if lapvar(fn(im, mid)) < target: lo = mid
        else: hi = mid
    return (lo + hi) / 2

k0 = read_all(K0, 0, K0_N + 1); k0_next = k0[K0_N]; k0 = k0[:K0_N]
import tailgate_fix                                 # scoate rândul de litere fără sens pe care Kling îl desenează pe buza hayonului
cont_raw = read_all(CONT); cont_fixed, _ = tailgate_fix.fix_frames(cont_raw)
cont = cont_fixed[1:]                               # primul cadru al continuării e dublat (= cadrul de start)
print("k0 frames", len(k0), " cont frames", len(cont), " join at", round(T_J, 3), "s")
# ---- potrivirea la îmbinare: luminozitatea și claritatea continuării față de cadrul din care a pornit
g1 = mean_reg(k0_next) / mean_reg(cont[0])
lv_k0 = lapvar(k0[-1]); lv_end = float(np.mean([lapvar(cont[i]) for i in range(SH_N_CONT, SH_N_CONT + 12)]))
def cont_frame(i):
    im = cont[i]
    wg = max(0.0, 1 - i / GAIN_N)
    if wg > 0: im = np.clip(np.rint(im.astype(np.float32) * (1 + (g1 - 1) * wg)), 0, 255).astype(np.uint8)
    if i < SH_N_CONT:
        target = lv_k0 + (lv_end - lv_k0) * i / SH_N_CONT
        if lapvar(im) < target: im = unsharp(im, solve(unsharp, im, target, 0.0, 2.5))
    return im
def k0_frame(i): return k0[i]
print(f"join: gain {g1:.4f}  lapvar k0 {lv_k0:.0f}, cont first {lapvar(cont[0]):.0f} -> {lapvar(cont_frame(0)):.0f}, cont native at {SH_N_CONT}: {lv_end:.0f}")
# ---- harta de timp: poziția în sursă (cadre de 24 fps) pentru fiecare cadru de ieșire
n_out = int(round(AICUT * FPS)); ks = np.array(SPEED, float)
tt = np.arange(0, AICUT + 1e-9, 1 / 3000.0); v = np.interp(tt, ks[:, 0], ks[:, 1]); S = np.concatenate([[0], np.cumsum(v[:-1]) / 3000.0]) * FPS_SRC
pos = np.interp(np.arange(n_out) / FPS, tt, S); idx = np.round(pos).astype(int)
assert idx.max() < len(k0) + len(cont), (idx.max(), len(k0) + len(cont))
dup = int((np.diff(idx) == 0).sum()); print("out frames", n_out, " last src idx", int(idx.max()), "= cont t", round((idx.max() - K0_N + 1) / FPS_SRC, 2), "s  dup", dup, " skipped", int((np.diff(idx) > 1).sum()))
cont_t = lambda j: (j - K0_N + 1) / FPS_SRC          # timpul din clipul de continuare (cu tot cu primul cadru dublat)
def t_of_cont(tc):                                   # momentul din reel la care se vede secunda tc a continuării
    j = tc * FPS_SRC + K0_N - 1; return float(np.interp(j, pos, np.arange(n_out) / FPS))
print("events (reel s): " + "  ".join(f"cont {tc:.2f}s -> {t_of_cont(tc):.2f}" for tc in (2.75, 3.0, 3.5, 4.0, 4.5, 5.5, 6.0, 6.5, 7.0)))
if DRY: sys.exit(0)
shutil.rmtree(TMP, ignore_errors=True); os.makedirs(f"{TMP}/src"); os.makedirs(f"{TMP}/out")
cache = {}
for i, j in enumerate(idx):
    j = int(j)
    if j not in cache: cache = {j: (k0_frame(j) if j < K0_N else cont_frame(j - K0_N))}
    cv2.imwrite(f"{TMP}/src/{i:05d}.png", cache[j])
subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", f"{TMP}/src/%05d.png", "-vf", "scale=1080:1920:flags=lanczos,format=yuvj420p",
                "-frames:v", str(n_out), "-q:v", "2", "-start_number", "0", f"{TMP}/out/%05d.jpg"], check=True)
got = sorted(os.listdir(f"{TMP}/out")); assert len(got) == n_out, (len(got), n_out)
for f in got: shutil.copy(f"{TMP}/out/{f}", f"{R}/frames_base/{f}")
# ---- cantitatea de fum pe cadru: pixeli care au devenit mai luminoși și mai puțin saturați decât în primele cadre (fără cer)
sm = []; ref = None
for f in got:
    im = cv2.resize(cv2.imread(f"{TMP}/out/{f}"), (270, 480), interpolation=cv2.INTER_AREA)
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV).astype(np.float32)
    if ref is None: ref = hsv.copy()
    m = ((hsv[..., 2] - ref[..., 2]) > 28) & (hsv[..., 1] < 70) & (hsv[..., 2] > 150); m[:130] = False
    sm.append(round(float(m.mean()) * 100, 2))
json.dump({"fps": FPS, "smoke_pct": sm, "k0_frames": K0_N, "cont": os.path.basename(CONT)}, open(f"{R}/audio/hook_smoke.json", "w"))
json.dump({"fps": FPS, "k0_frames": K0_N, "cont": os.path.basename(CONT), "join_t": T_J, "speed": SPEED, "src_idx": [int(x) for x in idx],
           "events": {f"cont_{tc}": round(t_of_cont(tc), 3) for tc in (2.75, 3.0, 3.5, 4.0, 4.5, 5.5, 6.0, 6.5, 7.0)}}, open(f"{R}/audio/hook_map.json", "w"))
lv = [round(lapvar(cv2.imread(f"{TMP}/out/{got[i]}")), 0) for i in range(0, n_out, 6)]
print("lapvar every 0.2 s:", lv)
print("frames written:", n_out, " smoke % each 0.5 s:", [sm[min(i * 15, n_out - 1)] for i in range(15)])
