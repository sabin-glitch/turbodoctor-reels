# Pompa CP4 in sectiune pentru reelul "Un banal schimb de filtru de motorina...": randare Blender care inlocuieste pompa three.js.
# Camerele sunt fixe si identice cu camera paginii three.js (FOV vertical 30 de grade, decalaj pe verticala), deci etichetele,
# panoul si particulele paginii se suprapun exact. Mecanismul merge in bucle de NL cadre pe o jumatate de tura (cama e dubla),
# randate doar pe regiunea pieselor in miscare; restul cadrului vine dintr-o placa fixa.
#
#   venv/bin/python reel_scene.py proj  <cam>                         -> proiectia unor puncte de control (verificarea camerei)
#   venv/bin/python reel_scene.py boxes <cam>                         -> regiunile pieselor in miscare (out_reel/boxes_<cam>.json)
#   venv/bin/python reel_scene.py plate <cam> <stare> [spp]           -> placa fixa, cadru intreg (out_reel/<cam>_<stare>_plate.png)
#   venv/bin/python reel_scene.py loop  <cam> <stare> <reg> a b [spp] [pas] -> cadrele a..b ale buclei/secventei, doar regiunea <reg> (R1 | R2)
#   venv/bin/python reel_scene.py frames <lista.json> [spp]           -> cadre intregi cu camera data explicit (miscarile de camera)
#   venv/bin/python reel_scene.py still <cam> <stare> <k> <out.png> [spp] [latime]
# Stari: FUEL (motorina, rece) | AIR (aer, rece) | HOT (aer, rola incinsa) | ROT0 / ROT1 (tachetul se roteste 0-90 de grade in LR cadre, cama intreaga / taiata) | CROSS (rola de-a curmezisul, cama taiata)
import os, sys, math, json
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
_src = open(os.path.join(HERE, 'scene.py')).read()
exec(compile(_src[:_src.index('# cronologia probei')], os.path.join(HERE, 'scene.py'), 'exec'))   # materiale, geometrie, arc, cinematica
from bpy_extras.object_utils import world_to_camera_view
# conectorul regulatorului de debit e plastic negru, ca in pagina (in proba iesea gri deschis sub lumina cheie)
MAT['plasticGrey'].node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = srgb(0x1b1c1f)

NL = 38            # cadre pe o jumatate de tura a camei (o cursa a pistonului); planul larg reda din doi in doi (~5 rad/s, ca in pagina)
LR = 90            # cadre pentru rotirea tachetului
OUT = os.path.join(HERE, 'out_reel'); os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- lumina de la contact, camera, lumini, fundal
glow = bpy.data.lights.new('glow', 'POINT'); glow.color = (1.0, 0.42, 0.1); glow.shadow_soft_size = 0.002
glowO = bpy.data.objects.new('glow', glow); scn.collection.objects.link(glowO)

cam = bpy.data.cameras.new('cam'); camO = bpy.data.objects.new('cam', cam); scn.collection.objects.link(camO); scn.camera = camO
cam.sensor_fit = 'VERTICAL'; cam.sensor_height = 24.0; cam.lens = 12.0 / math.tan(math.radians(15.0))   # FOV vertical 30 de grade, ca in pagina
cam.clip_start = 0.01; cam.clip_end = 50.0; cam.dof.use_dof = False
# camere fixe (reperul pompei, mm): tinta, azimut, elevatie, distanta, decalaj pe verticala in pixeli (oy din pagina, cu -10 din modul vo)
SHOTS = {
    'W': dict(c=(0, 34, 0), az=44.0, el=13.5, d=620.0, oy=160.0),
    'C': dict(c=(0, 24, 0), az=47.0, el=14.5, d=410.0, oy=140.0),
}
def place(name):
    s = SHOTS[name]; c = s['c']; A, E = math.radians(s['az']), math.radians(s['el']); d = s['d']
    cp = (c[0] + d * math.sin(A) * math.cos(E), c[1] + d * math.sin(E), c[2] + d * math.cos(A) * math.cos(E))
    camO.location = W(cp); camO.rotation_euler = (W(c) - W(cp)).to_track_quat('-Z', 'Y').to_euler()
    cam.shift_y = -s['oy'] / 1920.0    # setViewOffset(W,H,0,oy,W,H): imaginea urca cu oy pixeli

def area(name, loc, target, size, energy, col=(1, 1, 1), shape='RECTANGLE', sy=None):
    l = bpy.data.lights.new(name, 'AREA'); l.energy = energy; l.color = col; l.shape = shape; l.size = size; l.size_y = sy or size
    o = bpy.data.objects.new(name, l); scn.collection.objects.link(o); o.location = loc
    d = (Vector(target) - Vector(loc)); o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler(); return o
C0 = W((0, 20, 0))
area('key', C0 + Vector((0.55, -0.35, 0.55)), C0, 0.35, 55 * EV('KEYK', 1.0), (1.0, 0.97, 0.93), sy=0.2)
area('fill', C0 + Vector((0.2, -0.7, 0.05)), C0, 0.5, 5, (0.85, 0.9, 1.0))
area('rim', C0 + Vector((-0.45, 0.45, 0.35)), C0, 0.08, 45, (0.8, 0.88, 1.0), sy=0.6)
area('top', C0 + Vector((0.05, 0.0, 0.8)), C0, 0.3, 12)

world = bpy.data.worlds.new('W'); scn.world = world; world.use_nodes = True
WN = world.node_tree.nodes; WL = world.node_tree.links
bg = WN['Background']
env = WN.new('ShaderNodeTexEnvironment'); env.image = bpy.data.images.load(os.path.join(SRC, 'studio.exr'))
WL.new(env.outputs['Color'], bg.inputs['Color']); bg.inputs['Strength'].default_value = 0.22
# peretele intunecat din proba ramane pentru lumina, dar nu se vede: fundalul cadrului e transparent si vine din reel
bpy.ops.mesh.primitive_plane_add(size=3, location=W((0, 0, 0)) + Vector((-0.6, 0.6, 0)), rotation=(math.pi / 2, 0, math.radians(45)))
wall = bpy.context.active_object; wall.name = 'wall'
wall.data.materials.append(pbr('wall', 0x101215, 0, 0.8, bump=(0.4, 0.2))); wall.visible_camera = False

# ---------------------------------------------------------------- starea pompei (aceleasi formule ca in CP.set din pagina)
RP = MAT['rollerPol'].node_tree.nodes['Principled BSDF']
def apply(phi, rot=0.0, dam=0, fuel=1.0, heat=0.0, spin=0.0):
    h = lerp(look(hPar, phi), look(hCross, phi), ease(rot))
    shaft.rotation_euler = (0, 0, phi); shaftDam.rotation_euler = (0, 0, phi)
    shaft.scale = (1, 1, 1) if dam < 0.5 else (0, 0, 0); shaftDam.scale = (0, 0, 0) if dam < 0.5 else (1, 1, 1)
    tap.location = (0, h, 0); tap.rotation_euler = (0, rot * math.pi / 2, 0); roller.rotation_euler = (0, 0, spin)
    plunger.location = (0, h, 0)
    spring.data.shape_keys.key_blocks['B'].value = (h - HA) / (HB - HA)
    v = look(hPar, phi + 0.02) - look(hPar, phi - 0.02); up = clamp(v * 4, -1, 1)
    il = clamp(-up) * 1.1 * fuel + clamp(-up) * 0.4 * (1 - fuel)
    inValve.location = (0, 84.2 - il, 0); inSpring.scale = (1, (4.4 - il) / 4.4, 1)
    ol = clamp(up) * 0.9 * fuel; outBall.location = (15.66 + ol, 81.6, 0)
    outSpring.location = (outBall.location.x + 1.5, 81.6, 0); outSpring.scale = ((28 - outSpring.location.x) / 10.8, 1, 1)
    top = h + 50.4; fCol.location = (0, top, 0); fCol.scale = (1, max(0.05, 79 - top), 1)
    press = clamp(up * 1.5)
    l3 = lambda a, b, k: [a[i] + (b[i] - a[i]) * k for i in range(3)] + [1]
    cCh = l3(l3(C_BLUE, C_HPC, press), C_AIRC, 1 - fuel); oCh = lerp(0.1, lerp(0.5, 0.65, press), fuel)
    cLP = l3(C_BLUE, C_AIRC, (1 - fuel) * 0.8); oLP = lerp(0.04, 0.5, fuel); oHP = lerp(0.08, 0.6, fuel)
    for nm, c_, o_ in (('fuel', cLP, oLP), ('fuelCh', cCh, oCh), ('fuelHP', C_HPC, oHP)):
        nd = MAT[nm].node_tree.nodes
        nd['COL'].outputs[0].default_value = c_; nd['FADE'].inputs['Fac'].default_value = min(1.0, o_ * LIQ_OP)
    RP.inputs['Emission Strength'].default_value = 6.0 * heat ** 1.5
    glow.energy = 0.35 * heat; glowO.location = W((4, h - 5.5, 4))
    bpy.context.view_layer.update()
    return h

def state(name, k):
    """starea pompei la cadrul k al buclei/secventei `name`; faza camei continua din k (o jumatate de tura la NL cadre)"""
    phi = -math.pi * k / NL
    roll = 4 * math.pi * k / NL          # cat timp e unsa, rola se rostogoleste pe cama: doua ture pe bucla, deci bucla se inchide
    if name == 'FUEL': return dict(phi=phi, rot=0.0, dam=0, fuel=1.0, heat=0.0, spin=roll)
    if name == 'AIR': return dict(phi=phi, rot=0.0, dam=0, fuel=0.0, heat=0.0, spin=roll)
    if name == 'HOT': return dict(phi=phi, rot=0.0, dam=0, fuel=0.0, heat=1.0)
    if name == 'ROT0': return dict(phi=phi, rot=ease(k / LR), dam=0, fuel=0.0, heat=1.0)     # rotirea tachetului, cama inca intreaga
    if name == 'ROT1': return dict(phi=phi, rot=ease(k / LR), dam=1, fuel=0.0, heat=1.0)     # rotirea tachetului, cama taiata
    if name == 'CROSS': return dict(phi=phi, rot=1.0, dam=1, fuel=0.0, heat=1.0)
    raise SystemExit('stare necunoscuta: ' + name)

# ---------------------------------------------------------------- randare
R = scn.render
R.engine = 'CYCLES'
cy_ = scn.cycles
cy_.device = 'CPU'; cy_.samples = 32; cy_.use_adaptive_sampling = True; cy_.adaptive_threshold = EV('ADAPT', 0.03)
R.use_persistent_data = True
cy_.use_denoising = True; cy_.denoiser = 'OPENIMAGEDENOISE'
cy_.max_bounces = 6; cy_.glossy_bounces = 3; cy_.transmission_bounces = 6; cy_.volume_bounces = 1; cy_.diffuse_bounces = 2
cy_.caustics_reflective = False; cy_.caustics_refractive = False; cy_.blur_glossy = 1.0
R.resolution_x, R.resolution_y = 1080, 1920; R.resolution_percentage = 100
R.use_motion_blur = False
scn.view_settings.view_transform = os.environ.get('VT', 'AgX')
try: scn.view_settings.look = os.environ.get('LOOK', 'AgX - Medium High Contrast')
except Exception as e: print('look', e)
scn.view_settings.exposure = EV('EXPO', 0.0)
R.image_settings.file_format = 'PNG'; R.image_settings.color_mode = 'RGBA'; R.image_settings.compression = 15
R.film_transparent = True

def px(p):   # punct din reperul pompei (mm) -> pixel (x, y de sus)
    v = world_to_camera_view(scn, camO, W(p)); return (v.x * R.resolution_x, (1 - v.y) * R.resolution_y)

def moving_boxes(cname):
    """regiunile care se schimba de la un cadru la altul: R1 = cama, tachet, rola, piston, arc, supape, coloana de motorina; R2 = pana de pe conul arborelui"""
    place(cname); bpy.context.view_layer.update()
    b1 = [1e9, 1e9, -1e9, -1e9]; b2 = [1e9, 1e9, -1e9, -1e9]
    def add(b, q): b[0] = min(b[0], q[0]); b[1] = min(b[1], q[1]); b[2] = max(b[2], q[0]); b[3] = max(b[3], q[1])
    dg = None
    for k in list(range(0, NL, 3)) + [-1, -2]:
        st = state('FUEL', k) if k >= 0 else (dict(phi=0.0, rot=1.0, dam=1, fuel=0, heat=1) if k == -1 else dict(phi=-math.pi / 2, rot=0.5, dam=1, fuel=0, heat=1))
        apply(**st)
        for grp, flt in ((shaftDam if st['dam'] else shaft, 'cam'), (tap, None), (plunger, None), (inValve, None), (inSpring, None), (outBall, None), (outSpring, None), (fCol, None), (fCh, None)):
            for ob in [o for o in grp.children_recursive if o.type == 'MESH']:
                me = ob.data; n = len(me.vertices); co = np.zeros(n * 3); me.vertices.foreach_get('co', co); co = co.reshape(-1, 3)
                if flt == 'cam':
                    if 'steelDark' in ob.name:
                        for p in co[:: max(1, n // 60)]: add(b2, world_to_camera_view(scn, camO, ob.matrix_world @ Vector(p)))
                        continue
                    co = co[np.abs(co[:, 2]) <= 13.5]
                for p in co[:: max(1, len(co) // 400)]: add(b1, world_to_camera_view(scn, camO, ob.matrix_world @ Vector(p)))
        me = spring.data; co = np.zeros(len(me.vertices) * 3); me.vertices.foreach_get('co', co)
        for p in co.reshape(-1, 3)[::40]: add(b1, world_to_camera_view(scn, camO, spring.matrix_world @ Vector(p)))
    # pana: toata tura
    for a in range(0, 360, 20):
        apply(phi=math.radians(a))
        for ob in [o for o in shaft.children_recursive if o.type == 'MESH' and 'steelDark' in o.name]:
            me = ob.data; n = len(me.vertices); co = np.zeros(n * 3); me.vertices.foreach_get('co', co)
            for p in co.reshape(-1, 3)[:: max(1, n // 60)]: add(b2, world_to_camera_view(scn, camO, ob.matrix_world @ Vector(p)))
    def box(b, m):
        x0 = int(math.floor(b[0] * 1080)) - m; x1 = int(math.ceil(b[2] * 1080)) + m
        y0 = int(math.floor((1 - b[3]) * 1920)) - m; y1 = int(math.ceil((1 - b[1]) * 1920)) + m
        return [max(0, x0), max(0, y0), min(1080, x1), min(1920, y1)]
    return {'R1': box(b1, int(EV('M1', 44))), 'R2': box(b2, int(EV('M2', 22)))}

def set_border(bx):
    if bx is None: R.use_border = False; R.use_crop_to_border = False; return
    R.use_border = True; R.use_crop_to_border = True
    R.border_min_x = bx[0] / 1080; R.border_max_x = bx[2] / 1080; R.border_min_y = 1 - bx[3] / 1920; R.border_max_y = 1 - bx[1] / 1920

if __name__ == '__main__':
    a = sys.argv[1:]; mode = a[0]
    if mode == 'proj':
        place(a[1]); bpy.context.view_layer.update()
        print('PROJ', json.dumps([px(p) for p in [(0, 0, 0), (0, 34, 0), (0, 80, 0), (30, 0, 0), (0, 0, 30), (13, -11, 0), (0, 90, 0)]]))
    elif mode == 'boxes':
        B = moving_boxes(a[1]); json.dump(B, open(os.path.join(OUT, 'boxes_%s.json' % a[1]), 'w')); print('BOXES', a[1], B)
    elif mode == 'still':
        place(a[1]); apply(**state(a[2], int(a[3])))
        if len(a) > 5: cy_.samples = int(a[5])
        if len(a) > 6: R.resolution_x = int(a[6]); R.resolution_y = R.resolution_x * 16 // 9
        if os.environ.get('BOX'): set_border([int(x) for x in os.environ['BOX'].split(',')])
        R.filepath = os.path.join(OUT, a[4]); bpy.ops.render.render(write_still=True)
    elif mode == 'plate':
        place(a[1]); apply(**state(a[2], 0)); cy_.samples = int(a[3]) if len(a) > 3 else 128
        R.filepath = os.path.join(OUT, '%s_%s_plate.png' % (a[1], a[2])); bpy.ops.render.render(write_still=True)
    elif mode == 'loop':
        cname, sname, reg, k0, k1 = a[1], a[2], a[3], int(a[4]), int(a[5])
        if len(a) > 6: cy_.samples = int(a[6])
        step = int(a[7]) if len(a) > 7 else 1
        B = json.load(open(os.path.join(OUT, 'boxes_%s.json' % cname)))[reg]
        place(cname); set_border(B)
        d = os.path.join(OUT, '%s_%s_%s' % (cname, sname, reg)); os.makedirs(d, exist_ok=True)
        for k in range(k0, k1 + 1, step):
            fp = os.path.join(d, 'k%03d.png' % k)
            if os.path.exists(fp): continue
            apply(**state(sname, k)); R.filepath = fp; bpy.ops.render.render(write_still=True)
    elif mode == 'frames':
        # cadre intregi cu camera data explicit (miscarile de camera): lista JSON [{out, shot:{c,az,el,d,oy}, sname, k}]
        L = json.load(open(a[1]))
        if len(a) > 2: cy_.samples = int(a[2])
        for it in L:
            fp = os.path.join(OUT, it['out'])
            if os.path.exists(fp): continue
            os.makedirs(os.path.dirname(fp), exist_ok=True)
            SHOTS['_'] = it['shot']; place('_'); apply(**state(it['sname'], it['k'])); R.filepath = fp; bpy.ops.render.render(write_still=True)
