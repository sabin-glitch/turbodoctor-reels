import sys, time, os, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import bpy, numpy as np
bpy.ops.wm.open_mainfile(filepath=os.path.join(HERE, 'out', 'assets.blend'))
import kit as K
K.init(empty=False)
import layout as L, rig
D = bpy.data.objects
def pose(th):
    r = L.STROKE/2; pz = L.piston_z(th)
    D['CRANK'].rotation_euler = (th, 0, 0)
    D['PISTON'].location = (L.SEC_X, 0, pz)
    D['ROD'].location = (L.SEC_X, -r*math.sin(th), r*math.cos(th)); D['ROD'].rotation_euler = (-math.asin(r*math.sin(th)/L.ROD), 0, 0)
pose(math.radians(50))
for n in ('mod.glazeTop','egr.crack','dps.crack'): D[n].hide_render = True
D['mod.soot'].data.shape_keys.key_blocks['K'].value = 0.6
D['mod.ash'].data.shape_keys.key_blocks['K'].value = 0.15
gh = float(os.environ.get('GHOST', '1'))
for g in ('exh','int','egr'): K.set_ghost(g, gh)
rig.setup_world(float(os.environ.get('WORLD','0.28'))); rig.setup_lights(); cam = rig.setup_camera(); rig.setup_render(540, 960, int(os.environ.get('SPP','16')))
bpy.context.scene.view_settings.exposure = float(os.environ.get('EXPO','-0.6'))
VIEWS = {
 'hero':  ((640, -1250, 520), (-45, -150, 120), 50),
 'heroL': ((-760, -1150, 420), (-45, -150, 120), 50),
 'mod':   ((250, -820, 260), (-150, -235, 70), 60),
 'sec':   ((980, -330, 330), (132, -10, 170), 55),
 'egr':   ((330, -760, 230), (30, -250, 90), 60),
 'top':   ((150, -900, 900), (-20, -150, 200), 50),
 'dps':   ((-120, -640, 520), (-250, -215, 280), 70),
 'cool':  ((60, -560, 80), (-52, -270, 14), 70),
}
names = os.environ.get('VIEWS', 'hero,heroL,mod,sec').split(',')
out = []
for n in names:
    p, t, lens = VIEWS[n]
    rig.aim(cam, p, t, lens=lens)
    t0 = time.time(); fp = os.path.join(HERE, 'v_%s.png' % n); rig.still(fp); print('render', n, round(time.time()-t0, 1), flush=True)
    out.append(fp)
from PIL import Image
