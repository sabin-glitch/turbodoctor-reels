"""Render shots from out/motor4.blend.
  vbpy/bin/python render.py <shot> <k0> <k1> [pct] [spp] [outdir]     -> frames k0..k1-1 of the loop (skips existing)
  vbpy/bin/python render.py still <shot> <k> [pct] [spp] [out.png]
"""
import sys, os, json, math, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import bpy
import scene

BLEND = os.path.join(HERE, 'out', 'motor4.blend')


def setup_shot(name, spp=None, pct=100):
    sc = bpy.context.scene
    S = json.loads(sc['shots'])[name]
    for vl in sc.view_layers:
        vl.use = (vl.name == name)
    sc.camera = bpy.data.objects['CAM_' + name]
    yaw = sc.camera['yaw']
    scene.world_studio(yaw)
    scene.sun_lights(yaw)
    for i in range(4):
        gp = bpy.data.objects.get(f'glowplug{i + 1}')
        if gp is not None:
            gp['g'] = float(S.get('glow', 0.0)) if i == 1 else 0.0
    sc.render.resolution_percentage = pct
    if spp: sc.cycles.samples = spp
    sc.render.threads_mode = 'AUTO'
    return S


def frame_of(S, k):
    th = S['thetas'][k % len(S['thetas'])] % 720.0
    return th


def goto(sc, th):
    f = int(math.floor(th)); sub = th - f
    sc.frame_set(f, subframe=sub)


if __name__ == '__main__':
    a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    bpy.ops.wm.open_mainfile(filepath=BLEND)
    sc = bpy.context.scene
    if a[0] == 'still':
        name, k = a[1], int(a[2]); pct = int(a[3]) if len(a) > 3 else 100; spp = int(a[4]) if len(a) > 4 else None
        out = a[5] if len(a) > 5 else os.path.join(HERE, 'out', f'still_{name}_{k}.png')
        S = setup_shot(name, spp, pct)
        goto(sc, frame_of(S, k)); sc.render.filepath = out
        t = time.time(); bpy.ops.render.render(write_still=True); print(f'STILL {name} {k} {time.time() - t:.1f}s', flush=True)
    else:
        name, k0, k1 = a[0], int(a[1]), int(a[2])
        pct = int(a[3]) if len(a) > 3 else 100; spp = int(a[4]) if len(a) > 4 else None
        outdir = a[5] if len(a) > 5 else os.path.join(HERE, 'out', 'frames', name)
        os.makedirs(outdir, exist_ok=True)
        S = setup_shot(name, spp, pct)
        k1 = min(k1, len(S['thetas']))
        for k in range(k0, k1):
            path = os.path.join(outdir, f'f{k:04d}.png')
            if os.path.exists(path): continue
            goto(sc, frame_of(S, k)); sc.render.filepath = path
            t = time.time(); bpy.ops.render.render(write_still=True)
            print(f'DONE {name} {k} {time.time() - t:.1f}s', flush=True)
