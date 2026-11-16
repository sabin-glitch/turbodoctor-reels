# Probe de aspect: python look.py <blend> <iesire.png> tx,ty,tz az el dist lens [w h spp] [scara lumini] 
import sys, os, json, math, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import bpy, numpy as np
import kit as K, irig
a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
blend, out = a[0], a[1]
tgt = [float(x) for x in a[2].split(',')]; az, el, dist, lens = [float(x) for x in a[3:7]]
w, h, spp = (int(a[7]), int(a[8]), int(a[9])) if len(a) > 9 else (540, 960, 24)
ls = float(a[10]) if len(a) > 10 else 1.0
bpy.ops.wm.open_mainfile(filepath=blend); K.init(empty=False)
irig.setup_world(float(os.environ.get('WORLD', '0.3'))); irig.setup_lights(tgt, ls, float(os.environ.get('KEYK', '1.0')))
cam = irig.setup_camera(); irig.setup_render(w, h, spp, float(os.environ.get('EXPO', '0')))
irig.aim(cam, irig.orbit_pos(tgt, az, el, dist), tgt, lens)
D = bpy.data.objects
if os.environ.get('LIFT'):
    ln, lv = [float(x) for x in os.environ['LIFT'].split(',')]
    D['NEEDLE'].location.z = ln; D['ARM'].location.z = lv; D['BALL'].location.z = lv
if os.environ.get('HIDE'):
    for n in os.environ['HIDE'].split(','):
        o = D[n]; o.hide_render = True
        for c in o.children_recursive: c.hide_render = True
bpy.context.scene.render.filepath = out
t = time.time(); bpy.ops.render.render(write_still=True); print('RENDER %.1fs' % (time.time() - t), flush=True)
