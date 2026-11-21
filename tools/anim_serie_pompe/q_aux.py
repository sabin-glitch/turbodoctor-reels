# cutiile de incadrare ale grupurilor din blend/aux.blend, in reperul scenei (mm)
import sys, bpy, numpy as np
from mathutils import Vector
bpy.ops.wm.open_mainfile(filepath='/home/claude/w/serpmp/blend/aux.blend')
for g in ['FLT', 'TM', 'INJ', 'RAIL', 'QUICK', 'UNUT']:
    e = bpy.data.objects[g]; P = []
    for o in e.children_recursive:
        if o.type != 'MESH': continue
        M = o.matrix_world
        P += [M @ Vector(c) for c in o.bound_box]
    P = np.array(P); print(g, 'min', np.round(P.min(0)*1000), "max", np.round(P.max(0)*1000))
    for c in e.children:
        Q = []
        for o in [c] + list(c.children_recursive):
            if o.type == 'MESH': Q += [o.matrix_world @ Vector(b) for b in o.bound_box]
        if Q:
            Q = np.array(Q); print("   ", c.name, np.round(Q.min(0)*1000), np.round(Q.max(0)*1000), [m.data.materials[0].name for m in c.children if m.type == 'MESH'])
