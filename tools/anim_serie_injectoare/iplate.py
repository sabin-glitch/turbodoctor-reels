# Randeaza placile seriei injectoarelor: imagine (PNG RGBA) + adancime (.z.npy) + camera (.json). Sare peste ce exista.
#   venv_bpy/bin/python iplate.py cam:state [cam:state ...] [--preview] [--out DIR] [--spp N] [--force]
import sys, os, json, math, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, '/home/claude/w/inj')
import bpy, numpy as np
import kit as K, irig, imats
import ishots as S
import OpenEXR

a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
PREV = '--preview' in a; FORCE = '--force' in a
OUT = a[a.index('--out') + 1] if '--out' in a else os.path.join(HERE, 'pl_prev' if PREV else 'pl')
SPP = int(a[a.index('--spp') + 1]) if '--spp' in a else (8 if PREV else 32)
JOBS = [x for x in a if ':' in x and not x.startswith('-')]
os.makedirs(OUT, exist_ok=True)
W, H = (270, 480) if PREV else (S.W, S.H)

CUR = {'blend': None}; INIT = {}
def load(blend):
    if CUR['blend'] == blend: return
    path = blend if blend.endswith('.blend') else (S.INJ + blend + '.blend' if os.path.exists(S.INJ + blend + '.blend') else S.MIC + blend + '.blend')
    bpy.ops.wm.open_mainfile(filepath=path); K.init(empty=False)
    irig.setup_world(0.3); irig.setup_camera(); irig.setup_render(W, H, SPP, 0.0)
    INIT.clear()
    for o in bpy.data.objects: INIT[o.name] = (o.hide_render, tuple(o.location))
    INIT['__liq'] = {}
    for m in bpy.data.materials:
        if m.node_tree and 'COL' in m.node_tree.nodes and 'FADE' in m.node_tree.nodes:
            INIT['__liq'][m.name] = (tuple(m.node_tree.nodes['COL'].outputs[0].default_value), m.node_tree.nodes['FADE'].inputs['Fac'].default_value,
                                     m.node_tree.nodes['Principled BSDF'].inputs['Emission Strength'].default_value)
    INIT['__cov'] = {}
    for m in bpy.data.materials:
        if m.node_tree and 'COVER' in m.node_tree.nodes:
            c = m.node_tree.nodes['COVER']; INIT['__cov'][m.name] = (c.inputs['From Min'].default_value, c.inputs['From Max'].default_value)
    CUR['blend'] = blend

def hide(name, v=True):
    o = bpy.data.objects.get(name)
    if o is None: print('  (lipseste %s)' % name); return
    o.hide_render = v
    for c in o.children_recursive: c.hide_render = v

def reset():
    for o in bpy.data.objects:
        if o.type in ('CAMERA', 'LIGHT'): continue
        if o.name.startswith('x_'): o.hide_render = True; continue          # piese adaugate de o stare ('fn'): ascunse la fiecare reset
        if o.name in INIT: o.hide_render, o.location = INIT[o.name][0], INIT[o.name][1]
    for mn, (col, op, em) in INIT['__liq'].items():
        N = bpy.data.materials[mn].node_tree.nodes
        N['COL'].outputs[0].default_value = col; N['FADE'].inputs['Fac'].default_value = op; N['Principled BSDF'].inputs['Emission Strength'].default_value = em
    for mn, (a0, a1) in INIT['__cov'].items():
        c = bpy.data.materials[mn].node_tree.nodes['COVER']; c.inputs['From Min'].default_value = a0; c.inputs['From Max'].default_value = a1
    for k in [k for k in INIT if k.startswith('__co_')]:
        o = bpy.data.objects.get(k[5:])
        if o is not None:
            for v, c0 in zip(o.data.vertices, INIT[k]): v.co = c0
            o.data.update()

def apply(cam, st):
    reset()
    for n in cam.get('hide', []) + st.get('hide', []): hide(n, True)
    for n in st.get('show', []): hide(n, False)
    D = bpy.data.objects
    if 'lift' in st:
        ln, lv = st['lift']
        if 'NEEDLE' in D: D['NEEDLE'].location.z = INIT['NEEDLE'][1][2] + ln
        for n in ('ARM', 'BALL'):
            if n in D: D[n].location.z = INIT[n][1][2] + lv
    for mn, v in st.get('liq', {}).items():
        if isinstance(v, int): imats.set_liquid(mn, col=v)
        else: imats.set_liquid(mn, col=v[0], op=v[1] if len(v) > 1 else None, emit=v[2] if len(v) > 2 else None)
    for mn, thr in st.get('cover', {}).items():
        imats.set_cover(mn, thr)
        for o in D:
            if o.type == 'MESH' and any(s.material is not None and s.material.name == mn for s in o.material_slots) and o.name.startswith(('d_', 'dm_')):
                o.hide_render = False
    if 'wlevel' in st:      # nivelul apei din filtru (ep2): apa pana la nivel, motorina de la nivel in sus
        Lv = st['wlevel']
        for on, mode in (('f_water', 'min'), ('f_fuel', 'max')):
            o = D.get(on)
            if o is None: continue
            key = '__co_' + on
            if key not in INIT: INIT[key] = [tuple(v.co) for v in o.data.vertices]
            rmax = 30.4 if Lv < 23.6 else (26.4 if Lv < 31.0 else 38.8)
            for v, c0 in zip(o.data.vertices, INIT[key]):
                v.co = c0; z0 = c0[2]
                if mode == 'min':
                    v.co.z = min(z0, Lv)
                    if z0 > Lv:
                        r = math.hypot(v.co.x, v.co.y)
                        if r > rmax: v.co.x *= rmax / r; v.co.y *= rmax / r
                else: v.co.z = max(z0, Lv)
            o.data.update()
        hide('f_water', False)
    for on, loc in st.get('loc', {}).items():
        D[on].location = loc
    fn = st.get('fn')
    if fn: exec(fn, {'bpy': bpy, 'D': D, 'np': np, 'math': math, 'imats': imats, 'K': K})

def read_z(path):
    f = OpenEXR.File(path)
    for p in f.parts:
        for k, v in p.channels.items():
            if 'Depth' in k: return np.asarray(v.pixels, np.float32)

def zpass(base):
    scn = bpy.context.scene; cy = scn.cycles
    old = (cy.samples, cy.use_denoising, cy.max_bounces)
    cy.samples = 1; cy.use_denoising = False; cy.max_bounces = 0
    bpy.ops.render.render(write_still=False)
    s = scn.render.image_settings
    s.media_type = 'MULTI_LAYER_IMAGE'; s.file_format = 'OPEN_EXR_MULTILAYER'; s.color_depth = '32'; s.exr_codec = 'ZIP'
    tmp = base + '.tmp.exr'; bpy.data.images['Render Result'].save_render(tmp, scene=scn)
    s.media_type = 'IMAGE'; s.file_format = 'PNG'; s.color_mode = 'RGBA'; s.color_depth = '8'
    z = read_z(tmp); os.remove(tmp)
    np.save(base + '.z.npy', np.where(z > 1e6, 1e6, z).astype(np.float32))
    cy.samples, cy.use_denoising, cy.max_bounces = old

def render(job):
    cn, sn = job.split(':'); cam = dict(S.CAMS[cn]); st = S.STATES.get(sn, {})
    base = os.path.join(OUT, '%s__%s' % (cn, sn))
    if not FORCE and os.path.exists(base + '.png') and (PREV or os.path.exists(base + '.z.npy')): return
    load(st.get('blend', cam['blend']))
    scn = bpy.context.scene; scn.render.resolution_x, scn.render.resolution_y = W, H
    scn.cycles.samples = st.get('spp', cam.get('spp', SPP)) if not PREV else SPP
    irig.setup_world(cam.get('world', 0.3), cam.get('wrot', 0.0))
    tgt = cam['tgt']; irig.setup_lights(tgt, cam.get('ls', 1.0), cam.get('keyk', 1.0))
    camO = bpy.data.objects['cam']
    irig.aim(camO, irig.orbit_pos(tgt, cam['az'], cam['el'], cam['dist']), tgt, cam['lens'], cam.get('roll', 0.0))
    scn.view_settings.exposure = cam.get('expo', 0.0)
    apply(cam, st)
    scn.render.filepath = base + '.png'
    t = time.time(); bpy.ops.render.render(write_still=True); t1 = time.time() - t
    J = irig.cam_info(camO); J['tgt'] = list(tgt); json.dump(J, open(base + '.json', 'w'))
    if not PREV: zpass(base)
    print('PLATE %s %.1fs (total %.1fs)' % (job, t1, time.time() - t), flush=True)

order = sorted(JOBS, key=lambda j: S.STATES.get(j.split(':')[1], {}).get('blend', S.CAMS[j.split(':')[0]]['blend']))
for j in order: render(j)
print('DONE', len(order), flush=True)
