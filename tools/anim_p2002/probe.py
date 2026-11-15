# unde cad pe ecran punctele unui plan: etichetele (la aparitie si la sfarsitul planului) si puncte de pe trasee
#   probe.py <plan> [TRASEU:f0,f1,...] [x,y,z] ...
import sys
sys.path.insert(0, '/home/claude/dpf/work')
import numpy as np
import reel_story as R, fxlib as X, shots as S, gas as G, story as ST
sid = sys.argv[1]; s = R.BY[sid]; cam = X.Cam(ST.cam_J(s.cam), S.W, S.H)
def pr(p, u):
    cam.set2d(*s.kb(u)); x, y, z = cam.proj(np.array(p, np.float64)); return round(float(x[0])), round(float(y[0]))
print(sid, s.cam, 'durata %.2f' % (s.t1 - s.t0), 'kb start', [round(v, 3) for v in s.kb(0)], 'kb end', [round(v, 3) for v in s.kb(s.t1 - s.t0)])
for lab in R.LABELS.get(sid, []):
    a = lab[5]; print('  %-26s on %6.2f (u=%.2f)  punct %s -> %s   text (%d,%d)' % (lab[0], a, a - s.t0, pr(lab[1], a - s.t0), pr(lab[1], s.t1 - s.t0), lab[2], lab[3]))
um = (s.t1 - s.t0) * 0.6
for a in sys.argv[2:]:
    if ':' in a:
        n, fr = a.split(':'); path = getattr(G, n)
        for f in fr.split(','):
            f = float(f); p = path.P[int(round(f * (path.n - 1)))]; print('  %s %.2f %s -> %s' % (n, f, np.round(p).tolist(), pr(p, um)))
    else:
        p = [float(v) for v in a.split(',')]; print('  pt', p, '->', pr(p, um))
