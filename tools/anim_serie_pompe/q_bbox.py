import bpy, sys, numpy as np, json
from mathutils import Vector
bpy.ops.wm.open_mainfile(filepath='/home/claude/w/serpmp/blend/pump.blend')
out = {}
def bb(o):
    pts = []
    def rec(x):
        if x.type == 'MESH':
            M = x.matrix_world
            for c in x.bound_box: pts.append(M @ Vector(c))
        for ch in x.children: rec(ch)
    rec(o)
    if not pts: return None
    a = np.array([[p.x, p.y, p.z] for p in pts]) * 1000.0
    return [round(float(v), 1) for v in a.min(0)] + [round(float(v), 1) for v in a.max(0)]
for o in bpy.data.objects:
    if o.type == 'EMPTY' and o.name not in ('ROOT',):
        b = bb(o)
        print('%-16s parent=%-8s children=%s' % (o.name, o.parent.name if o.parent else '-', [c.name for c in o.children][:8]))
        if b: print('     bbox mm', b)
