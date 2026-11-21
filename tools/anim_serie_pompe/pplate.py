# Randeaza placile seriei pompelor: imagine (PNG RGBA) + adancime (.z.npy) + camera (.json). Sare peste ce exista.
#   venv_bpy/bin/python pplate.py cam:state [cam:state ...] [--preview] [--out DIR] [--spp N] [--force] [--loop] [--phi x]
#   --loop: pe langa placa, randeaza bucla pieselor in miscare (doar regiunea lor) in <cam>__<state>.loop/kNNN.png + box.json
import sys, os, json, math, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, '/home/claude/w/inj')
import bpy, numpy as np
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector
import kit as K, irig, imats
import pshots as S, pkin
import OpenEXR

a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
PREV = '--preview' in a; FORCE = '--force' in a; LOOP = '--loop' in a
OUT = a[a.index('--out') + 1] if '--out' in a else os.path.join(HERE, 'pl_prev' if PREV else 'pl')
SPP = int(a[a.index('--spp') + 1]) if '--spp' in a else (8 if PREV else 32)
PHI = float(a[a.index('--phi') + 1]) if '--phi' in a else None
LSPP = int(a[a.index('--lspp') + 1]) if '--lspp' in a else None      # esantioane pentru cadrele buclelor (piese in miscare)
JOBS = [x for x in a if ':' in x and not x.startswith('-')]
os.makedirs(OUT, exist_ok=True)
W, H = (270, 480) if PREV else (S.W, S.H)
if '--size' in a: W, H = int(a[a.index('--size') + 1]), int(a[a.index('--size') + 2])

CUR = {'blend': None}; INIT = {}
def load(blend):
    if CUR['blend'] == blend: return
    cands = [blend] if blend.endswith('.blend') else [S.BL + blend + '.blend', S.INJ + blend + '.blend', S.MIC + blend + '.blend']
    path = [p for p in cands if os.path.exists(p)][0]
    bpy.ops.wm.open_mainfile(filepath=path); K.init(empty=False)
    irig.setup_world(0.3); irig.setup_camera(); irig.setup_render(W, H, SPP, 0.0)
    INIT.clear()
    for o in bpy.data.objects: INIT[o.name] = (o.hide_render, tuple(o.location), tuple(o.rotation_euler), tuple(o.scale))
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
    o.hide_render = v; own = name.startswith(('d_', 'x_'))                 # o piele aratata pe nume isi arata si mesh-urile
    for c in o.children_recursive:
        if v or own or not c.name.startswith(('d_', 'x_')): c.hide_render = v      # pieile (d_) raman ascunse pana le arata o stare

def reset():
    for o in bpy.data.objects:
        if o.type in ('CAMERA', 'LIGHT'): continue
        if o.name in INIT: o.hide_render, o.location, o.rotation_euler, o.scale = INIT[o.name]
    for mn, (col, op, em) in INIT['__liq'].items():
        N = bpy.data.materials[mn].node_tree.nodes
        N['COL'].outputs[0].default_value = col; N['FADE'].inputs['Fac'].default_value = op; N['Principled BSDF'].inputs['Emission Strength'].default_value = em
    for mn, (a0, a1) in INIT['__cov'].items():
        c = bpy.data.materials[mn].node_tree.nodes['COVER']; c.inputs['From Min'].default_value = a0; c.inputs['From Max'].default_value = a1
    if 'rollerPol' in bpy.data.materials: bpy.data.materials['rollerPol'].node_tree.nodes['Principled BSDF'].inputs['Emission Strength'].default_value = 0.0

def lerp3(c0, c1, k): return [c0[i] + (c1[i] - c0[i]) * k for i in range(3)] + [1.0]

def pose(phi, rot=0.0, spin=0.0, st=None):
    """pune piesele pompei la unghiul phi al arborelui"""
    D = bpy.data.objects
    if 'shaft' not in D: return
    s = pkin.state(phi, rot); h = s['h']; up = s['up']
    for n in ('shaft', 'shaftDam'): D[n].rotation_euler = (0, 0, -phi)
    D['tap'].location = (0, h, 0); D['tap'].rotation_euler = (0, 0, 0)
    # tachetul rotit: corpul e de revolutie, deci in sectiune se vede doar rola intoarsa in jurul axei tachetului (intai se invarte in jurul axei ei, apoi se intoarce)
    D['roller'].rotation_mode = 'ZYX'; D['roller'].rotation_euler = (0, rot * math.pi / 2, spin)
    D['plunger'].location = (0, h, 0)
    D['spring'].data.shape_keys.key_blocks['B'].value = (h - pkin.HA) / (pkin.HB - pkin.HA)
    il = pkin.clamp(-up) * 1.1
    D['inValve'].location = (0, 84.2 - il, 0); D['inSpring'].scale = (1, (4.4 - il) / 4.4, 1)
    ol = pkin.clamp(up) * 0.9; D['outBall'].location = (15.66 + ol, 81.6, 0)
    D['outSpring'].location = (D['outBall'].location.x + 1.5, 81.6, 0); D['outSpring'].scale = ((28 - D['outSpring'].location.x) / 10.8, 1, 1)
    top = h + 50.4; D['fCol'].location = (0, top, 0); D['fCol'].scale = (1, max(0.05, 79 - top), 1)
    liq = (st or {}).get('liq', {})
    cl = liq.get('fuelCh', liq.get('fuelLP', imats.C_LP)); cl = cl[0] if isinstance(cl, (tuple, list)) else cl
    ch = liq.get('fuelHP', imats.C_HP); ch = ch[0] if isinstance(ch, (tuple, list)) else ch
    bpy.data.materials['fuelCh'].node_tree.nodes['COL'].outputs[0].default_value = lerp3(K.srgb(cl), K.srgb(ch), s['press'])

def apply(cam, st, phi, k=0, n=1):
    reset()
    D = bpy.data.objects
    for nm in cam.get('hide', []): hide(nm, True)
    for nm in st.get('show', []): hide(nm, False)
    for nm in st.get('hide', []): hide(nm, True)
    if 'shaftDam' in D and 'shaftDam' not in st.get('show', []): hide('shaftDam', True)
    for mn, v in st.get('liq', {}).items():
        if isinstance(v, int): imats.set_liquid(mn, col=v)
        else: imats.set_liquid(mn, col=v[0], op=v[1] if len(v) > 1 else None, emit=v[2] if len(v) > 2 else None)
    for mn, thr in st.get('cover', {}).items(): imats.set_cover(mn, thr)
    spin = 0.0 if st.get('stuck') else -2 * 2 * math.pi * k / max(n, 1)
    pose(phi, st.get('rot', 0.0) if not callable(st.get('rot')) else st['rot'](k / max(n, 1)), spin, st)
    if st.get('hot') and 'rollerPol' in bpy.data.materials:
        bpy.data.materials['rollerPol'].node_tree.nodes['Principled BSDF'].inputs['Emission Strength'].default_value = st['hot']
    for on, loc in st.get('loc', {}).items(): D[on].location = loc
    fn = st.get('fn')
    if fn: exec(fn, {'bpy': bpy, 'D': D, 'np': np, 'math': math, 'imats': imats, 'K': K, 'k': k, 'n': n})
    bpy.context.view_layer.update()

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

MOVERS = ['shaft', 'shaftDam', 'tap', 'plunger', 'spring', 'inValve', 'inSpring', 'outBall', 'outSpring', 'fCol', 'fCh']
def bbox2d(camO, names=None):
    """dreptunghiul de pe ecran (0..1, y de jos) al pieselor in miscare, vizibile"""
    scn = bpy.context.scene; xs = []; ys = []
    for nm in (names or MOVERS):
        o = bpy.data.objects.get(nm)
        if o is None: continue
        for c in [o] + list(o.children_recursive):
            if c.type != 'MESH' or c.hide_render: continue
            for v in c.bound_box:
                p = world_to_camera_view(scn, camO, c.matrix_world @ Vector(v)); xs.append(p.x); ys.append(p.y)
    if not xs: return None
    return min(xs), min(ys), max(xs), max(ys)

def render(job):
    cn, sn = job.split(':'); cam = dict(S.CAMS[cn]); st = S.STATES.get(sn, {})
    base = os.path.join(OUT, '%s__%s' % (cn, sn))
    load(st.get('blend', cam['blend']))
    scn = bpy.context.scene; R = scn.render; R.resolution_x, R.resolution_y = W, H
    scn.cycles.samples = st.get('spp', cam.get('spp', SPP)) if not PREV else SPP
    irig.setup_world(cam.get('world', 0.3), cam.get('wrot', 0.0))
    tgt = cam['tgt']; irig.setup_lights(tgt, cam.get('ls', 1.0), cam.get('keyk', 1.0))
    camO = bpy.data.objects['cam']
    irig.aim(camO, irig.orbit_pos(tgt, cam['az'], cam['el'], cam['dist']), tgt, cam['lens'], cam.get('roll', 0.0))
    scn.view_settings.exposure = cam.get('expo', 0.0)
    phi0 = PHI if PHI is not None else st.get('phi', S.PHI0)
    R.use_border = False; R.use_crop_to_border = False
    if FORCE or not (os.path.exists(base + '.png') and (PREV or os.path.exists(base + '.z.npy'))):
        apply(cam, st, phi0)
        R.filepath = base + '.png'
        t = time.time(); bpy.ops.render.render(write_still=True); t1 = time.time() - t
        J = irig.cam_info(camO); J['tgt'] = list(tgt); J['phi'] = phi0; json.dump(J, open(base + '.json', 'w'))
        if not PREV: zpass(base)
        print('PLATE %s %.1fs (total %.1fs)' % (job, t1, time.time() - t), flush=True)
    if LOOP or st.get('loop'):
        n = st.get('nloop', S.NLOOP); d = base + '.loop'; os.makedirs(d, exist_ok=True)
        bx = [1, 1, 0, 0]
        for k in range(n):
            apply(cam, st, phi0 + math.pi * k / n * st.get('turns', 1.0), k, n); b = bbox2d(camO, st.get('movers'))
            if b is None: continue
            bx = [min(bx[0], b[0]), min(bx[1], b[1]), max(bx[2], b[2]), max(bx[3], b[3])]
        mg = 0.012
        x0 = max(0, int(math.floor((bx[0] - mg) * W))); x1 = min(W, int(math.ceil((bx[2] + mg) * W)))
        yb0 = max(0, int(math.floor((bx[1] - mg * W / H) * H))); yb1 = min(H, int(math.ceil((bx[3] + mg * W / H) * H)))
        json.dump(dict(x=x0, y=H - yb1, w=x1 - x0, h=yb1 - yb0, n=n, W=W, H=H, phi0=phi0), open(os.path.join(d, 'box.json'), 'w'))
        R.use_border = True; R.use_crop_to_border = True
        R.border_min_x, R.border_max_x, R.border_min_y, R.border_max_y = x0 / W, x1 / W, yb0 / H, yb1 / H
        t = time.time(); done = 0
        if LSPP:
            scn.cycles.samples = LSPP
            try: scn.cycles.denoising_prefilter = 'FAST'; scn.cycles.denoising_quality = 'BALANCED'
            except Exception: pass
        for k in range(n):
            fp = os.path.join(d, 'k%03d.png' % k)
            if os.path.exists(fp) and not FORCE: continue
            apply(cam, st, phi0 + math.pi * k / n * st.get('turns', 1.0), k, n)
            R.filepath = fp; bpy.ops.render.render(write_still=True); done += 1
        R.use_border = False; R.use_crop_to_border = False
        print('LOOP %s %d cadre %dx%d  %.1fs/cadru' % (job, done, x1 - x0, yb1 - yb0, (time.time() - t) / max(done, 1)), flush=True)
        # pana arborelui are perioada de o tura intreaga (bucla e de o jumatate de tura): regiune mica, 2n cadre (kkNNN.png)
        KEYS = [nm for nm in ('shaft.steelDark', 'shaftDam.steelDark') if nm in bpy.data.objects]
        if st.get('turns', 1.0) == 1.0 and KEYS and not st.get('nokey'):
            kb = None
            for k in range(2 * n):
                apply(cam, st, phi0 + math.pi * k / n, k, n); b = bbox2d(camO, KEYS)
                if b is None: continue
                kb = list(b) if kb is None else [min(kb[0], b[0]), min(kb[1], b[1]), max(kb[2], b[2]), max(kb[3], b[3])]
            J = json.load(open(os.path.join(d, 'box.json')))
            if kb is not None and kb[2] > 0 and kb[0] < 1 and kb[3] > 0 and kb[1] < 1:
                mg = 0.008
                kx0 = max(0, int(math.floor((kb[0] - mg) * W))); kx1 = min(W, int(math.ceil((kb[2] + mg) * W)))
                ky0 = max(0, int(math.floor((kb[1] - mg * W / H) * H))); ky1 = min(H, int(math.ceil((kb[3] + mg * W / H) * H)))
                R.use_border = True; R.use_crop_to_border = True
                R.border_min_x, R.border_max_x, R.border_min_y, R.border_max_y = kx0 / W, kx1 / W, ky0 / H, ky1 / H
                t = time.time(); done = 0
                for k in range(2 * n):
                    fp = os.path.join(d, 'kk%03d.png' % k)
                    if os.path.exists(fp) and not FORCE: continue
                    apply(cam, st, phi0 + math.pi * k / n, k, n)
                    R.filepath = fp; bpy.ops.render.render(write_still=True); done += 1
                R.use_border = False; R.use_crop_to_border = False
                J['key'] = dict(x=kx0, y=H - ky1, w=kx1 - kx0, h=ky1 - ky0, n=2 * n)
                print('KEY %s %d cadre %dx%d  %.1fs/cadru' % (job, done, kx1 - kx0, ky1 - ky0, (time.time() - t) / max(done, 1)), flush=True)
            else:
                J['key'] = None
            json.dump(J, open(os.path.join(d, 'box.json'), 'w'))

order = sorted(JOBS, key=lambda j: S.STATES.get(j.split(':')[1], {}).get('blend', S.CAMS[j.split(':')[0]]['blend']))
for j in order: render(j)
print('DONE', len(order), flush=True)
