# Lista cadrelor pentru care se randeaza masca de acoperire (anim/amask.cjs) -> mask2_list.json
# Din 4 in 4 cadre unde imaginea se schimba incet, din 2 in 2 sau la fiecare cadru la miscari rapide de camera,
# pe ambele parti ale taieturilor si la capetele sirurilor de cadre fara Blender. wmapply.py interpoleaza intre ele.
#   python3 mask_list.py [frames_src]
import json, os, sys
import numpy as np, cv2
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/reels/amorsare_filtru/frames_src'
D = set(r['f'] for r in json.load(open(os.path.join(HERE, 'director.json')))['frames'])
N = len(json.load(open(os.environ.get('UF', '/home/claude/reels/amorsare_filtru/vo/uframes.json'))))
sp = os.path.join(HERE, 'motion_score.json')
if os.path.exists(sp): sc = json.load(open(sp))
else:                      # cat se schimba imaginea de la un cadru la altul (medie pe imaginea micsorata de 8 ori)
    sc = [0.0]; prev = None
    for f in range(N):
        g = cv2.imread(os.path.join(SRC, '%05d.jpg' % f), cv2.IMREAD_REDUCED_GRAYSCALE_8).astype(np.float32)
        if prev is not None: sc.append(float(np.abs(g - prev).mean()))
        prev = g
    json.dump(sc, open(sp, 'w'))
rest = [f for f in range(N) if f not in D]
need = set()
for f in rest:
    loc = max(sc[max(0, f - 2):f + 3]); step = 1 if loc > 10 else (2 if loc > 5 else 4)
    if f % step == 0: need.add(f)
cuts = []
for f in range(1, N):      # taietura = varf izolat fata de vecini
    nb = sc[max(1, f - 4):f] + sc[f + 1:f + 5]
    if sc[f] > 8 and sc[f] > 3 * (np.median(nb) + 0.5): cuts.append(f)
for f in cuts: need.update((f - 1, f))
for i, f in enumerate(rest):
    if i == 0 or rest[i - 1] != f - 1 or i == len(rest) - 1 or rest[i + 1] != f + 1: need.add(f)
need = sorted(f for f in need if f not in D)
json.dump(need, open(os.path.join(HERE, 'mask2_list.json'), 'w'))
s = set(need); bad = [f for f in rest if f not in s and not (any(g in s for g in range(f - 5, f)) and any(g in s for g in range(f + 1, f + 6)))]
print('cadre fara Blender', len(rest), '| masti de randat', len(need), '| taieturi', cuts, '| fara acoperire', len(bad))
