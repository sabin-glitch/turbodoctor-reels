# Construieste toate piesele si salveaza assets.blend + meta.json (trasee, puncte de ancorare).
import sys, time, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import bpy, numpy as np
import kit as K
K.init()
import mats; mats.make_all()
import layout as L, rig
import m_module, m_engine, m_turbo, m_egr, m_misc
SRC = os.environ.get('DPF_SRC', os.path.join(HERE, '..', 'src'))
OUT = os.environ.get('DPF_OUT', os.path.join(HERE, 'out')); os.makedirs(OUT, exist_ok=True)
meta = {}
def keep(tag, O):
    d = {}
    for k, v in O.items():
        if isinstance(v, bpy.types.Object): d[k] = v.name
        else: d[k] = v
    meta[tag] = d
only = os.environ.get('ONLY', 'module,engine,turbo,egr,misc').split(',')
for tag, fn in (('module', m_module.build), ('engine', lambda: m_engine.build(SRC)), ('turbo', m_turbo.build), ('egr', m_egr.build), ('misc', m_misc.build)):
    if tag not in only: continue
    t = time.time(); keep(tag, fn()); print('built', tag, round(time.time() - t, 1), flush=True)
print('tris', sum(len(o.data.polygons) for o in bpy.data.objects if o.type == 'MESH'), 'objects', len(bpy.data.objects))
json.dump(meta, open(os.path.join(OUT, 'meta.json'), 'w'))
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, 'assets.blend'))
