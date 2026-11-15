# Traseele gazelor prin ansamblu (mm), construite din aceleasi puncte ca piesele.
import math
import numpy as np
import layout as L, shots as S
from fxlib import Path, catmull

TY, TZ = L.TURBO_Y, L.TURBO_Z
M = S.META
def spiral(cx, a0, a1, r0, r1, x0, x1, n=36):
    a = np.radians(np.linspace(a0, a1, n)); r = np.linspace(r0, r1, n); x = np.linspace(x0, x1, n)
    return np.stack([x, TY + r * np.cos(a), TZ + r * np.sin(a)], 1)

def cat(*parts):
    P, R = [], []
    for pts, r in parts:
        pts = np.asarray(pts, np.float64).reshape(-1, 3)
        rr = np.full(len(pts), r, np.float64) if np.isscalar(r) else np.linspace(r[0], r[1], len(pts))
        P.append(pts); R.append(rr)
    return np.vstack(P), np.concatenate(R)

mw = L.mw
# ---- evacuare: colector -> turbina -> palnie -> catalizator -> filtru -> palnie -> teava
_leg = [(10, -163, 300), (7, -180, 311), (5, -202, 319), (4, -222, 314)]
_vol = spiral(L.TURB_X, 103, 103 + 330, 45, 20, 4, 12)
_out = [(4, TY, TZ + 6), (-22, TY, TZ), (L.TURB_OUT_X, TY, TZ)]
_fin = [(-92, -216, 266), (-126, -220, 263), tuple(mw(6, 4, -44)), tuple(mw(0, 0, -14))]
_mod = [tuple(mw(0, 0, z)) for z in (0, 60, 120, 180, 240, 298)]
_fo = [tuple(mw(0, 0, 326)), (-192.5, -241.5, -128), (-194, -247, -152), (-193, -263, -173), (-190.5, -292, -187), (-188, -332, -193)]
_exh = M['egr']['paths']['exh'][1:]
P, R = cat((_leg, (12, 14)), (_vol, (12, 8)), (_out, (8, 20)), (_fin, (20, 24)), (_mod, 56), (_fo, (38, 22)), (_exh, 22))
EXH = Path(P, R, smooth=4, step=2.0)
EXH_MOD0 = None  # fractiunile de traseu la care incepe / se termina modulul (calculate mai jos)
def _frac(path, p):
    d = np.linalg.norm(path.P - np.asarray(p, np.float64)[None, :], axis=1); return float(np.argmin(d)) / (path.n - 1)
F_TURB = _frac(EXH, (L.TURB_OUT_X, TY, TZ)); F_CAT0 = _frac(EXH, mw(0, 0, L.CAT_Z0)); F_CAT1 = _frac(EXH, mw(0, 0, L.CAT_Z1))
F_DPF0 = _frac(EXH, mw(0, 0, L.DPF_Z0)); F_DPF1 = _frac(EXH, mw(0, 0, L.DPF_Z1)); F_FO = _frac(EXH, (-188, -332, -193))
# canalele de evacuare ale celor 4 cilindri (pana in colector)
RUN = []
for xi in L.CYL_X:
    pts = [(xi, -L.HEAD_Y - 2, L.PORT_Z), (xi * 0.9, -142, 301), (xi * 0.8, -160, 300)]
    if abs(xi * 0.8) > 40: pts.append((xi * 0.42, -163, 300))
    pts.append((10, -163, 300))
    RUN.append(Path(pts, 11.0, smooth=6))
# ---- EGR de joasa presiune: priza de dupa filtru -> racitor -> teava -> supapa -> amestecator -> compresor
E = M['egr']['paths']
_take = [tuple(mw(0, 0, 300)), tuple(mw(8, -10, 322))] + [tuple(p) for p in E['take'][::4]]
_cool = [tuple(E['cool_in']), (-52, -252, 14), tuple(E['cool_out'])]
_up = [tuple(p) for p in E['up'][::4]] + [tuple(E['up'][-1])]
_pipe = [tuple(p) for p in E['pipe'][1:]]
_valve = [tuple(E['v1']), tuple(M['egr']['VC']), tuple(E['v2']), tuple(E['vend'])]
_mix = [(186, -218, 256), (176, TY - 2, TZ - 2), (160, TY, TZ), (L.COMP_IN_X, TY, TZ), (118, TY, TZ)]
P, R = cat((_take, (30, 15)), (_cool, 22), (_up, (20, 14)), (_pipe, 13), (_valve, 12), (_mix, (13, 20)))
EGR = Path(P, R, smooth=4, step=2.0)
G_COOL0 = _frac(EGR, E['cool_in']); G_COOL1 = _frac(EGR, E['cool_out']); G_VALVE = _frac(EGR, M['egr']['VC']); G_MIX = _frac(EGR, (176, TY - 2, TZ - 2))
# ---- aer proaspat: tubulatura (debitmetru) -> compresor
_duct = [tuple(p) for p in M['turbo']['paths']['duct'][::-4]] + [(198, TY, TZ), (160, TY, TZ), (L.COMP_IN_X, TY, TZ), (118, TY, TZ)]
AIR = Path(_duct, 24.0, smooth=3, step=2.0)
A_MAF = _frac(AIR, M['turbo']['maf_pos'])
# ---- aer comprimat: rotor -> voluta -> teava de presiune spre racitorul de aer / admisie
cx = L.COMP_X
_cvol = spiral(cx, 120, 360, 14, 50, 100, 104, n=30)
_cout = [(cx, TY + 50, TZ + 4), (cx - 2, TY + 57, TZ + 42), (cx - 4, TY + 62, TZ + 79)]
_ch = [tuple(p) for p in M['turbo']['paths']['charge'][::5]] + [tuple(M['turbo']['paths']['charge'][-1])]
P, R = cat((_cvol, (8, 15)), (_cout, 15), (_ch, 16))
CHG = Path(P, R, smooth=3, step=2.0)
# ---- prizele senzorului de presiune diferentiala (de la carcasa pana la senzor)
from fxlib import fillet_path
def _dps(lst, k):
    A = np.array(lst); t = A[:k][::-1]; h = A[k:]
    return Path(np.vstack([fillet_path(t, 16), h]), 1.5, smooth=0, step=1.0)
DPS1 = _dps(M['misc']['dps_tube1'], 5); DPS2 = _dps(M['misc']['dps_tube2'], 6)
if __name__ == '__main__':
    for n in ('EXH', 'EGR', 'AIR', 'CHG', 'DPS1', 'DPS2'):
        p = globals()[n]; print(n, 'len', round(p.len), 'n', p.n, 'start', np.round(p.P[0]), 'end', np.round(p.P[-1]))
    print('fracs', F_TURB, F_CAT0, F_CAT1, F_DPF0, F_DPF1, F_FO, '| egr', G_COOL0, G_COOL1, G_VALVE, G_MIX, '| maf', A_MAF)
    print('dps1', M['misc']['dps_tube1'][0], M['misc']['dps_tube1'][-1], 'b1', M['misc']['dps_b1'], 'b2', M['misc']['dps_b2'])
