import sys, glob, cv2, numpy as np
ep = sys.argv[1]; fs = sorted(glob.glob(f'/home/claude/work/serie_dpf/comp/proof/{ep}_*.png')); sel = sys.argv[2].split(',') if len(sys.argv) > 2 else None
if sel: fs = [f for f in fs if f.split('_')[-1][:-4] in sel]
ims = [cv2.resize(cv2.imread(f), (432, 768), interpolation=cv2.INTER_AREA) for f in fs]
per = 5 if len(ims) > 4 else len(ims)
rows = [np.hstack(ims[i:i + per] + [np.zeros_like(ims[0])] * (per - len(ims[i:i + per]))) for i in range(0, len(ims), per)]
cv2.imwrite(f'/home/claude/work/serie_dpf/comp/proof/sheet_{ep}_{sys.argv[2] if sel else "all"}.jpg'.replace(',', '-'), np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 82])
