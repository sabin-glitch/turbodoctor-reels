import sys, os, json, math, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import film as F, rig, layout as L
import numpy as np
F.load(360, 640, int(os.environ.get('SPP', '12')))
D = F.D
for n in ('mod.glazeTop', 'egr.crack', 'dps.crack'): D[n].hide_render = True
F.key('mod.soot', 0.5); F.pose(math.radians(60))
gh = os.environ.get('GH', '')
for g in gh.split(','):
    if g: F.ghost(g, 1)
mc = lambda x, y, z: tuple(L.mw(x, y, z))
ch = np.array([0.50, -0.87, 0.0])
V = {
 'hero':  ((640, -1850, 520), (-45, -150, 105), 35),
 'heroL': ((-560, -1850, 420), (-45, -150, 105), 35),
 'route': ((330, -1700, 330), (20, -240, 70), 40),
 'dpf':   (tuple(L.mw(0, 0, 200) + ch * 620 + np.array([0, 0, 90])), mc(8, 8, 196), 50),
 'dps':   ((-640, -820, 330), (-240, -230, 190), 60),
 'cool':  ((70, -720, 90), (-45, -252, 14), 60),
 'egrv':  ((560, -800, 360), (175, -235, 235), 60),
 'exf':   ((240, -1000, -20), (-170, -430, -160), 60),
 'sec':   ((1080, -90, 330), (132, 0, 245), 50),
 'inj':   ((640, -40, 300), (132, 0, 262), 70),
 'turbo': ((-150, -700, 380), (30, -212, 262), 60),
 'maf':   ((760, -700, 520), (290, -250, 320), 60),
}
names = os.environ.get('VIEWS', ','.join(V)).split(',')
tag = os.environ.get('TAG', 's')
for n in names:
    p, t, lens = V[n]
    rig.aim(F.cam, p, t, lens=lens)
    dt = F.render(os.path.join(HERE, 'sc', '%s_%s' % (tag, n)), exr=False); print('render', n, round(dt, 1), flush=True)
