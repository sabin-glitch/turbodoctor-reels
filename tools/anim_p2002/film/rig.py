# Camera, lumini, fundal, setari de randare (Cycles pe CPU; merge la fel pe GPU / EEVEE).
import bpy, math, os
import numpy as np
from mathutils import Vector
import kit as K

SRC = os.environ.get('DPF_SRC', '/home/claude/dpf/src')

def setup_world(strength=0.35, rot=0.0):
    scn = bpy.context.scene
    world = bpy.data.worlds.get('W') or bpy.data.worlds.new('W')
    scn.world = world; world.use_nodes = True
    WN = world.node_tree.nodes; WL = world.node_tree.links
    for n in list(WN):
        if n.type not in ('OUTPUT_WORLD',): WN.remove(n)
    out = [n for n in WN if n.type == 'OUTPUT_WORLD'][0]
    bg = WN.new('ShaderNodeBackground'); bg.name = 'BG'
    env = WN.new('ShaderNodeTexEnvironment')
    env.image = bpy.data.images.load(os.path.join(SRC, 'studio.exr'), check_existing=True)
    tc = WN.new('ShaderNodeTexCoord'); mp = WN.new('ShaderNodeMapping'); mp.inputs['Rotation'].default_value = (0, 0, rot)
    WL.new(tc.outputs['Generated'], mp.inputs['Vector']); WL.new(mp.outputs['Vector'], env.inputs['Vector'])
    WL.new(env.outputs['Color'], bg.inputs['Color']); bg.inputs['Strength'].default_value = strength
    WL.new(bg.outputs[0], out.inputs['Surface'])
    return world

def area(name, loc_mm, target_mm, size_mm, energy, col=(1, 1, 1), sy=None, spread=None):
    scn = bpy.context.scene
    l = bpy.data.lights.new(name, 'AREA'); l.energy = energy; l.color = col; l.shape = 'RECTANGLE'
    l.size = size_mm * 0.001; l.size_y = (sy or size_mm) * 0.001
    if spread is not None: l.spread = spread
    o = bpy.data.objects.new(name, l); scn.collection.objects.link(o)
    o.location = K.W(loc_mm)
    o.rotation_euler = (K.W(target_mm) - K.W(loc_mm)).to_track_quat('-Z', 'Y').to_euler()
    return o

def setup_lights():
    c = (-40, -150, 150)
    L = {}
    L['key'] = area('key', (700, -1100, 900), c, 700, 150, (1.0, 0.965, 0.92), sy=500)
    L['fill'] = area('fill', (-900, -800, 250), c, 900, 30, (0.82, 0.89, 1.0))
    L['rim'] = area('rim', (-500, 500, 900), c, 300, 120, (0.78, 0.87, 1.0), sy=900)
    L['side'] = area('side', (1300, -150, 420), (132, 0, 200), 600, 70, (1.0, 0.97, 0.94))
    L['low'] = area('low', (150, -900, -500), c, 800, 16, (0.9, 0.93, 1.0))
    return L

def setup_camera():
    scn = bpy.context.scene
    cam = bpy.data.cameras.new('cam'); camO = bpy.data.objects.new('cam', cam)
    scn.collection.objects.link(camO); scn.camera = camO
    cam.sensor_fit = 'VERTICAL'; cam.sensor_height = 24.0
    cam.clip_start = 0.01; cam.clip_end = 50
    cam.dof.use_dof = False; cam.dof.aperture_blades = 7
    return camO

def aim(camO, pos_mm, tgt_mm, lens=50, fstop=None, focus_mm=None, roll=0.0):
    p = K.W(pos_mm); t = K.W(tgt_mm)
    camO.location = p
    q = (t - p).to_track_quat('-Z', 'Y')
    camO.rotation_mode = 'QUATERNION'; camO.rotation_quaternion = q
    cam = camO.data; cam.lens = lens
    if fstop:
        cam.dof.use_dof = True; cam.dof.aperture_fstop = fstop
        f = K.W(focus_mm) if focus_mm is not None else t
        cam.dof.focus_distance = (f - p).length
    else:
        cam.dof.use_dof = False

def setup_render(w=720, h=1280, spp=16, engine='CYCLES'):
    scn = bpy.context.scene; R = scn.render
    R.engine = engine
    R.resolution_x, R.resolution_y = w, h; R.resolution_percentage = 100
    R.film_transparent = True
    R.image_settings.file_format = 'PNG'; R.image_settings.color_mode = 'RGBA'; R.image_settings.compression = 20
    R.use_persistent_data = True
    scn.view_settings.view_transform = 'AgX'
    try: scn.view_settings.look = 'AgX - Medium High Contrast'
    except Exception: pass
    scn.view_settings.exposure = 0.0
    if engine == 'CYCLES':
        cy = scn.cycles
        dev = os.environ.get('DPF_DEVICE', 'CPU')
        cy.device = dev
        cy.samples = spp; cy.use_adaptive_sampling = False
        cy.use_denoising = True; cy.denoiser = 'OPENIMAGEDENOISE'
        try:
            cy.denoising_input_passes = 'RGB_ALBEDO_NORMAL'; cy.denoising_prefilter = 'FAST'; cy.denoising_quality = 'FAST'
        except Exception: pass
        cy.max_bounces = 6; cy.diffuse_bounces = 2; cy.glossy_bounces = 3; cy.transmission_bounces = 4
        cy.transparent_max_bounces = 24; cy.volume_bounces = 0
        cy.caustics_reflective = False; cy.caustics_refractive = False; cy.blur_glossy = 1.0
        cy.sample_clamp_indirect = 6.0; cy.sample_clamp_direct = 0.0
        cy.seed = 7
        try: cy.use_light_tree = True
        except Exception: pass
    else:
        e = scn.eevee; e.taa_render_samples = spp; e.use_raytracing = False
    R.threads_mode = 'AUTO'
    return R

def still(path, w=None, h=None, spp=None):
    scn = bpy.context.scene; R = scn.render
    if w: R.resolution_x, R.resolution_y = w, h
    if spp and R.engine == 'CYCLES': scn.cycles.samples = spp
    R.filepath = path
    bpy.ops.render.render(write_still=True)
