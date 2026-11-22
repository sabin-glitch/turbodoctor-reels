"""fast keyframing on Blender 5 slotted actions"""
import bpy
from bpy_extras import anim_utils

INTERP = {'CONSTANT': 0, 'LINEAR': 1, 'BEZIER': 2}


def fcurve(idb, path, index=0):
    ad = idb.animation_data
    if ad is None or ad.action is None:
        idb.keyframe_insert(path, index=index, frame=0) if index >= 0 else idb.keyframe_insert(path, frame=0)
        ad = idb.animation_data
    cb = anim_utils.action_ensure_channelbag_for_slot(ad.action, ad.action_slot)
    f = cb.fcurves.find(path, index=max(index, 0))
    if f is None:
        f = cb.fcurves.new(path, index=max(index, 0))
    return f


def keys(idb, path, index, frames, values, interp='LINEAR'):
    f = fcurve(idb, path, index)
    kp = f.keyframe_points
    kp.clear()
    kp.add(len(frames))
    co = []
    for fr, v in zip(frames, values): co += [float(fr), float(v)]
    kp.foreach_set('co', co)
    kp.foreach_set('interpolation', [INTERP[interp]] * len(frames))
    try:
        kp.foreach_set('handle_left', co); kp.foreach_set('handle_right', co)
    except Exception:
        pass
    f.update()
    return f
