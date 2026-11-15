# Marcajul "TURBO DOCTOR" din fundal (cerut de Sabin pe 15.11.2026 pentru toate animatiile): acelasi desen si aceeasi miscare ca in seria turbinelor.
# Sta direct pe fundal, in spatele scenei: cadru = original + (transparenta scenei + k) * delta, unde delta = alfa_marcaj * (culoare_marcaj - fundal)
# si k = cat de mult e cadrul stins spre culoarea fundalului (fadeBlack din pagina), ca marcajul sa ramana si in treceri.
import json, math, os
import numpy as np, cv2
HERE = os.path.dirname(os.path.abspath(__file__))
# taria: alb si galben, ca in seria turbinelor. Prima proba de acolo (.085 / .115) i s-a parut lui Sabin prea vizibila ("Sa fie mai discret", 15.11.2026),
# asa ca valorile implicite sunt cele coborate la jumatate.
WM_W, WM_Y = float(os.environ.get('WM_W', '.04')), float(os.environ.get('WM_Y', '.052'))
SPEED = 9.0                                   # px/s de-a lungul randurilor
BG = np.array([23, 20, 17], np.float32)       # #111417 in BGR
_P = json.load(open(os.path.join(HERE, 'wm/pattern.json'))); UNIT = _P['unit']
_im = cv2.imread(os.path.join(HERE, 'wm/pattern.png'), cv2.IMREAD_UNCHANGED).astype(np.float32)
_a = _im[..., 3] / 255.0
_yel = np.clip((243.0 - _im[..., 0]) / 212.0, 0, 1)            # 0 = alb (TURBO), 1 = galben (DOCTOR); canalul albastru le deosebeste
_ae = _a * (WM_W + (WM_Y - WM_W) * _yel)
D0 = (_ae[..., None] * (_im[..., :3] - BG)).astype(np.float32)   # delta in coordonatele modelului
del _im, _a, _yel, _ae
_c, _s = math.cos(math.radians(20)), math.sin(math.radians(20))
def delta(f):
    """delta pentru cadrul f al reelului (30 fps): HxWx3 float32, BGR"""
    s = (f / 30.0 * SPEED) % UNIT
    ox = -UNIT + s - 1240.0; oy = -1460.0
    M = np.float32([[_c, _s, _c * ox + _s * oy + 540.0], [-_s, _c, -_s * ox + _c * oy + 960.0]])
    return cv2.warpAffine(D0, M, (1080, 1920), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
def ease(x): x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)
_y = np.arange(1920, dtype=np.float32)
# transparenta degrade-urilor HUD din modul cu voce (sus 0-240, jos 1150-1330): marcajul se stinge spre zona subtitrarilor.
# In cadrele obisnuite degrade-urile sunt deja in masca / in trecerea 'ovl'; profilul e pentru momentele in care pagina stinge cadrul spre fundal.
GRAD = ((1 - 0.85 * np.clip(1 - _y / 240.0, 0, 1)) * (1 - 0.9 * np.clip((_y - 1150.0) / 180.0, 0, 1)))[:, None]      # (1920, 1)
def kfade(U):
    """cat de mult stinge pagina cadrul spre fundal la timpul U al animatiei (fadeBlack din 80_hud.js)"""
    k = max(1 - ease(abs(U - 60.2) / 0.35), 1 - ease(abs(U - 78.7) / 0.35))
    return max(k, (1 - ease(abs(U - 54.5) / 0.3)) * 0.85)
if __name__ == '__main__':
    import sys
    d = delta(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
    cv2.imwrite(os.path.join(HERE, 'wm/test_delta.jpg'), np.clip(BG + d, 0, 255).astype(np.uint8)); print('max delta', d.max(), 'min', d.min())
