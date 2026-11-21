import sys, bpy
bpy.ops.wm.open_mainfile(filepath=sys.argv[-1])
def show(o, d=0):
    if d > 2: return
    kids = [c for c in o.children]
    print('  ' * d + o.name, o.type, 'hid' if o.hide_render else '', len(o.children_recursive), [m.name for m in o.data.materials][:3] if o.type == 'MESH' else '')
    for c in kids: show(c, d + 1)
for o in bpy.data.objects:
    if o.parent is None: show(o)
