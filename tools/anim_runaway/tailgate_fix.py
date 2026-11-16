"""Continuarea Kling (hf7_e0) desenează, de pe la secunda 1, un rând de litere fără sens pe buza hayonului (artefact AI).
Îl scot: urmăresc hayonul (caroseria se leagănă când coboară șoferul), aduc peste bandă aceeași zonă din primul cadru (curată),
potrivită la lumina cadrului curent, și las neatinse fumul și omul când trec prin față.
  fix_frames(frames) -> lista de cadre corectate (BGR uint8), frames[1] = cadrul de referință curat
  python3 tailgate_fix.py <clip.mp4> <out_dir>   (scrie planșe de control)"""
import sys, numpy as np, cv2

BOX = (350, 890, 850, 1050)                         # zona de lucru (x0, y0, x1, y1)
POLY = np.array([(401, 954), (600, 953), (793, 950), (795, 997), (401, 997)], np.int32)   # banda cu litere + reflexia ei pe bară (coordonate în referință)
TRK = {"logo": (560, 845, 645, 915), "stopL": (385, 850, 480, 935), "stopR": (730, 850, 805, 925), "placa": (545, 1005, 770, 1055),
       "golf": (410, 930, 490, 952), "tdi": (735, 925, 790, 945)}
SRCH = 14
SMOKE_G = 212.0; SMOKE_BGR = np.array([222, 214, 203], np.float32)   # luminozitatea / culoarea tipică a fumului dens din clip

def _track(ref_g, g, box):
    x0, y0, x1, y1 = box; tpl = ref_g[y0:y1, x0:x1]; srch = g[y0 - SRCH:y1 + SRCH, x0 - SRCH:x1 + SRCH]
    r = cv2.matchTemplate(srch, tpl, cv2.TM_CCOEFF_NORMED); _, mx, _, (px, py) = cv2.minMaxLoc(r)
    def sub(a, b, c):
        d = a - 2 * b + c; return 0.0 if abs(d) < 1e-9 else float(np.clip(0.5 * (a - c) / d, -.5, .5))
    edge = px in (0, r.shape[1] - 1) or py in (0, r.shape[0] - 1)
    sx = 0 if edge else sub(r[py, px - 1], r[py, px], r[py, px + 1]); sy = 0 if edge else sub(r[py - 1, px], r[py, px], r[py + 1, px])
    return px - SRCH + sx, py - SRCH + sy, (0.0 if edge else float(mx))

def fit_motion(ref_g, g, prev):
    """translație + rotație mică a caroseriei față de referință; prev = (tx, ty, th) din cadrul anterior (pentru cadre cu puține repere)"""
    cx, cy = 600.0, 975.0; rows, rhs, ws = [], [], []; used = []
    for k, b in TRK.items():
        dx, dy, sc = _track(ref_g, g, b); w = max(0.0, (sc - 0.62) / 0.38) ** 2
        if w <= 0: continue
        px, py = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
        rows += [[1, 0, -(py - cy)], [0, 1, (px - cx)]]; rhs += [dx, dy]; ws += [w, w]; used.append((k, dx, dy, sc))
    lam = 4000.0                                            # leagă rotația de cadrul anterior (în px² pe radian²)
    rows.append([0, 0, 1]); rhs.append(prev[2]); ws.append(lam)
    if len(used) < 2: return prev, used, 9.9
    A = np.array(rows, float); b_ = np.array(rhs, float); W = np.sqrt(np.array(ws, float))[:, None]
    sol, *_ = np.linalg.lstsq(A * W, b_ * W[:, 0], rcond=None)
    res = A[:-1] @ sol - b_[:-1]; rms = float(np.sqrt((np.array(ws[:-1]) * res ** 2).sum() / (np.sum(ws[:-1]) + 1e-9)))
    return (float(sol[0]), float(sol[1]), float(sol[2])), used, rms

def _affine(tx, ty, th, cx=600.0, cy=975.0):
    c, s = np.cos(th), np.sin(th)                           # p' = R(p - c) + c + t
    return np.array([[c, -s, cx - c * cx + s * cy + tx], [s, c, cy - s * cx - c * cy + ty]], np.float32)

def fix_frames(frames, verbose=False):
    ref = frames[1]; H, W = ref.shape[:2]; ref_g = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY).astype(np.float32)
    x0, y0, x1, y1 = BOX; bw, bh = x1 - x0, y1 - y0
    M = np.zeros((H, W), np.float32); cv2.fillPoly(M, [POLY], 1.0)
    k9 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)); k7 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    k5 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)); k41 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (41, 41)); D0 = np.zeros(4, np.float32); Sg = SMOKE_G
    out = [frames[0], frames[1]]; prev = (0.0, 0.0, 0.0); log = []
    for i in range(2, len(frames)):
        cur = frames[i]; g = cv2.cvtColor(cur, cv2.COLOR_BGR2GRAY).astype(np.float32)
        prev, used, rms = fit_motion(ref_g, g, prev); A = _affine(*prev)
        Ab = A.copy(); Ab[:, 2] += A[:, :2] @ np.array([x0, y0], np.float32) - np.array([x0, y0], np.float32)   # aceeași transformare, în coordonatele decupajului
        clean = cv2.warpAffine(ref[y0:y1, x0:x1], Ab, (bw, bh), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE).astype(np.float32)
        m = cv2.warpAffine(M[y0:y1, x0:x1], Ab, (bw, bh), flags=cv2.INTER_LINEAR)
        c = cur[y0:y1, x0:x1].astype(np.float32)
        gc_ = cv2.cvtColor(clean.astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32); gg = g[y0:y1, x0:x1]
        V = c.max(2); C9 = cv2.dilate(V, k9) - cv2.erode(V, k9)
        man = ((cv2.dilate(V, k9) < 60) & (C9 < 26)).astype(np.uint8)       # întunecat și neted pe o zonă mare = geaca omului
        ring = (cv2.dilate(m, k7) < 0.01) & (cv2.dilate(m, k41) > 0.5) & (man == 0)
        # 1. lumina cadrului curent față de referință (mediană robustă pe tabla din jurul benzii, fără fum)
        dg = gg - gc_; ok = ring & (np.abs(dg - D0[3]) < 35)
        if ok.sum() > 400: D0 = np.array([np.median((c[..., ch] - clean[..., ch])[ok]) for ch in range(3)] + [np.median(dg[ok])], np.float32)
        # 2. cât fum e în fața tablei: deschiderea morfologică scoate literele subțiri și păstrează forma fumului
        og = cv2.morphologyEx(gg, cv2.MORPH_OPEN, k9); ogc = cv2.morphologyEx(gc_, cv2.MORPH_OPEN, k9) + D0[3]
        sm_px = (C9 < 12) & (gg > gc_ + 60)                                  # fum dens: luminos și neted
        if sm_px.sum() > 300: Sg = 0.5 * Sg + 0.5 * float(np.percentile(gg[sm_px], 70))
        a = np.clip((og - ogc) / np.maximum(Sg - ogc, 50.0), 0, 1); a = np.clip((cv2.GaussianBlur(a, (0, 0), 2.0) - 0.08) / 0.84, 0, 1)
        # culoarea fumului din apropiere (media pe fumul dens), altfel o valoare tipică
        ws = ((a > 0.8) & (C9 < 20)).astype(np.float32)
        Sn = cv2.GaussianBlur(c * ws[..., None], (0, 0), 12.0); Sd = cv2.GaussianBlur(ws, (0, 0), 12.0)[..., None]
        S = (Sn + 0.02 * SMOKE_BGR) / (Sd + 0.02)
        # 3. lumina locală (membrană din jurul benzii, doar pe tablă fără fum), cu mediana ca rezervă
        wv = (ring & (a < 0.1) & (np.abs(dg - D0[3]) < 30)).astype(np.float32)
        num = cv2.GaussianBlur((c - clean) * wv[..., None], (0, 0), 9.0); den = cv2.GaussianBlur(wv, (0, 0), 9.0)[..., None]
        D = (num + 0.05 * D0[:3]) / (den + 0.05)
        patch = np.clip(clean + D, 0, 255) * (1 - a[..., None]) + S * a[..., None]
        # 4. unde fumul e dens (literele nu se mai văd) sau trece omul, rămâne cadrul original
        opaque = ((a > 0.85) & (C9 < 14)).astype(np.uint8)
        occ = cv2.dilate(np.maximum(opaque, man), k5).astype(np.float32); alpha = np.clip(cv2.GaussianBlur(occ, (0, 0), 1.5), 0, 1)
        w = (cv2.GaussianBlur(m, (0, 0), 2.2) * (1 - alpha))[..., None]
        res = c * (1 - w) + patch * w
        o = cur.copy(); o[y0:y1, x0:x1] = np.clip(np.rint(res), 0, 255).astype(np.uint8); out.append(o)
        log.append((i, prev, len(used), rms, float(alpha[m > .5].mean()) if (m > .5).any() else 0))
        if verbose and i % 8 == 0: print(f"f{i:3d} tx {prev[0]:5.2f} ty {prev[1]:5.2f} rot {np.degrees(prev[2]):5.2f}°  repere {len(used)}  rms {rms:4.2f}  acoperit {log[-1][4]:.2f}")
    return out, log

if __name__ == "__main__":
    clip, outd = sys.argv[1], sys.argv[2]
    cap = cv2.VideoCapture(clip); F = []
    while True:
        ok, im = cap.read()
        if not ok: break
        F.append(im)
    G, log = fix_frames(F, verbose=True)
    X0, Y0, X1, Y1 = 370, 915, 830, 1045
    for name, idx in (("a", (12, 24, 40, 64, 84, 90)), ("b", (94, 98, 102, 106, 112, 118)), ("c", (124, 132, 140, 148, 156, 162)), ("d", (166, 170, 174, 180, 186, 192))):
        rows = []
        for i in idx:
            a = cv2.resize(F[i][Y0:Y1, X0:X1], None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC); b = cv2.resize(G[i][Y0:Y1, X0:X1], None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
            cv2.putText(a, f"f{i}", (6, 26), cv2.FONT_HERSHEY_SIMPLEX, .8, (0, 255, 255), 2); rows.append(np.hstack([a, b]))
        cv2.imwrite(f"{outd}/fix_{name}.jpg", np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 90])
    np.save(f"{outd}/e0_fixed.npy", np.array(G))
