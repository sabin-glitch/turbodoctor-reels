# Raftul unei dezmembrari: zece pompe folosite, toate curate pe dinafara (episodul 17).
# Pompa intreaga din pump.blend se uneste intr-un singur mesh si se pune de zece ori pe trei polite (aceleasi date, obiecte diferite).
#   venv_bpy/bin/python pshelf.py   ->  blend/shelf.blend + blend/shelf.json
# Reper (mm): Z in sus, raftul cu fata spre -Y, centrat pe x = 0; fata de sus a politelor la z = 0, 215 si 430.
import bpy, math, json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, '/home/claude/w/inj')
import kit as K, imats, irig

ZB = 66.5                    # de la talpa pompei pana la axa arborelui
ROWS = [(430.0, [-200.0, 0.0, 200.0]), (215.0, [-262.5, -87.5, 87.5, 262.5]), (0.0, [-200.0, 0.0, 200.0])]
YAW = {(0, 0): 14, (0, 1): -9, (0, 2): 22, (1, 0): -17, (1, 1): 8, (1, 2): 156, (1, 3): -12, (2, 0): 19, (2, 1): -24, (2, 2): 6}       # (rand, loc) -> grade; una e intoarsa cu spatele (racordurile)
META = {'pts': {}, 'pumps': []}

def build():
    bpy.ops.wm.open_mainfile(filepath=os.path.join(HERE, 'blend', 'pump.blend')); scn, ROOT = K.init(empty=False)
    D = bpy.data.objects; Ri = ROOT.matrix_world.inverted()
    src = []
    for g in ('FULL', 'cp4.zme', 'cp4.ports', 'shaft'):
        o = D[g]; src += [c for c in ([o] + list(o.children_recursive)) if c.type == 'MESH' and not c.name.startswith(('d_', 'x_'))]
    parts = []
    for o in src:
        me = o.data.copy(); me.transform(Ri @ o.matrix_world)
        ob = bpy.data.objects.new('w.' + o.name, me); scn.collection.objects.link(ob); ob.parent = ROOT; parts.append(ob)
    bpy.context.view_layer.update()
    pump = K.join(parts, 'pumpW')
    for o in list(bpy.data.objects):
        if o is not pump and o is not ROOT and o.type not in ('CAMERA', 'LIGHT'): bpy.data.objects.remove(o, do_unlink=True)
    M = {m.name: m for m in bpy.data.materials}
    board = imats.metal('shBoard', 0x5d4c38, 0.78, metal=0.0, bump=(1.2, 0.3, 0.2))
    edge = imats.metal('shEdge', 0x3a3f47, 0.5, metal=0.0)
    post = imats.metal('shPost', 0x1b2c47, 0.45, metal=0.35, coat=0.3, bevel=0.6)
    tagm = imats.metal('shTag', 0xa9a18d, 0.9, metal=0.0)
    G = K.empty('SHELF', ROOT)
    # politele si montantii
    for i, (z, xs) in enumerate(ROWS):
        K.box('board%d' % i, (780.0, 220.0, 20.0), c=(0, 0, z - 10.0), mat=board, bev=1.5, parent=G)
        K.box('lipF%d' % i, (780.0, 6.0, 34.0), c=(0, -113.0, z - 13.0), mat=post, bev=1.2, parent=G)
        K.box('lipB%d' % i, (780.0, 6.0, 34.0), c=(0, 113.0, z - 13.0), mat=post, bev=1.2, parent=G)
    for sx in (-1, 1):
        for sy in (-1, 1):
            K.box('post%d%d' % (sx, sy), (34.0, 34.0, 800.0), c=(sx * 407.0, sy * 99.0, 250.0), mat=post, bev=2.0, parent=G)
        K.box('side%d' % sx, (6.0, 170.0, 34.0), c=(sx * 407.0, 0, 632.0), mat=post, bev=1.2, parent=G)
    # pompele: aceleasi date, zece obiecte
    k = 0
    for i, (z, xs) in enumerate(ROWS):
        for j, x in enumerate(xs):
            yaw = math.radians(YAW[(i, j)]); y = 6.0 * math.sin(k * 2.1)
            if k == 0: ob = pump; ob.parent = G
            else:
                ob = bpy.data.objects.new('pump%d' % k, pump.data); scn.collection.objects.link(ob); ob.parent = G
            ob.name = 'pump%d' % k; ob.location = (x, y, z + ZB); ob.rotation_euler = (0, 0, yaw)
            META['pumps'].append({'k': k, 'row': i, 'col': j, 'pos': [x, y, z + ZB], 'yaw': YAW[(i, j)]})
            # eticheta de carton de pe marginea politei
            K.box('tag%d' % k, (58.0, 1.2, 30.0), c=(x + 8.0, -116.8, z - 14.0), mat=tagm, bev=0.0, parent=G)
            k += 1
    P = META['pts']
    P['mid'] = [0, 0, 250.0]; P['open'] = [-87.5, 0.0, 215.0 + ZB + 18.0]; P['back'] = [87.5, 0.0, 215.0 + ZB + 18.0]
    print('pompa: %d fete, %d obiecte' % (len(pump.data.polygons), len(bpy.data.objects)), flush=True)

if __name__ == '__main__':
    out = os.path.join(HERE, 'blend', 'shelf.blend')
    build()
    json.dump(META, open(out.replace('.blend', '.json'), 'w'), indent=1)
    irig.setup_world(0.3); irig.setup_camera(); irig.setup_render(1080, 1920, 32, 0.0)
    bpy.ops.wm.save_as_mainfile(filepath=out, compress=True)
    print('SAVED', out, len(bpy.data.objects), 'obiecte', flush=True)
