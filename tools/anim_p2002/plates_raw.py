# planurile reelului fara asezarea 2D (zoom 1, fara deplasare), cu grila: ca sa aleg asezarea fiecarui plan
import sys, os
sys.path.insert(0, '/home/claude/dpf/work')
import numpy as np, cv2
import comp_reel as CR, comp as CP, reel_story as R, shots as S
out = sys.argv[1]; ids = sys.argv[2].split(','); per = int(sys.argv[3]) if len(sys.argv) > 3 else 5
ims = []
for sid in ids:
    frac = 0.8
    if ':' in sid: sid, frac = sid.split(':'); frac = float(frac)
    s = R.BY[sid]; s.kb = (lambda u: (1.0, 0.0, 0.0)); u = (s.t1 - s.t0) * frac
    im = CP.to8(CR.compose(s, u, S.W, S.H)); im = CR.guides(im)
    cv2.putText(im, '%s %s u=%.1f' % (sid, s.cam, u), (300, 1880), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
    ims.append(im); print(sid, flush=True)
rows = [np.concatenate(ims[i:i + per] + [np.zeros_like(ims[0])] * (per - len(ims[i:i + per])), 1) for i in range(0, len(ims), per)]
sh = np.concatenate(rows, 0); sc = 2160.0 / sh.shape[1]
sh = cv2.resize(sh, (2160, int(sh.shape[0] * sc)), interpolation=cv2.INTER_AREA)
cv2.imwrite(out, sh, [cv2.IMWRITE_JPEG_QUALITY, 88])
