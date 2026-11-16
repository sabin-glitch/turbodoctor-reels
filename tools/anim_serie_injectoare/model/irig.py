# Lumini, camera, fundal si setari de randare pentru seria injectoarelor (Cycles pe CPU).
import bpy, math, os
import numpy as np
from mathutils import Vector
import kit as K

import sys, glob
STUDIO = ([p for p in glob.glob(os.path.join(sys.prefix, 'lib', 'python*', 'site-packages', 'bpy', '*', 'datafiles', 'studiolights', 'world', 'studio.exr'))] + [os.environ.get('STUDIO_EXR', '')])[0]

def setup_world(strength=0.3, rot=0.0):
    scn = bpy.context.scene
    world = bpy.data.worlds.get('W') or bpy.data.worlds.new('W')
    scn.world = world; world.use_nodes = True
    WN = world.node_tree.nodes; WL = world.node_tree.links
    for n in list(WN):
        if n.type not in ('OUTPUT_WORLD',): WN.remove(n)
    out = [n for n in WN if n.type == 'OUTPUT_WORLD'][0]
    bg = WN.new('ShaderNodeBackground'); bg.name = 'BG'
    env = WN.new('ShaderNodeTexEnvironment'); env.image = bpy.data.images.load(STUDIO, check_existing=True)
    tc = WN.new('ShaderNodeTexCoord'); mp = WN.new('ShaderNodeMapping'); mp.name = 'ROT'; mp.inputs['Rotation'].default_value = (0, 0, rot)
    WL.new(tc.outputs['Generated'], mp.inputs['Vector']); WL.new(mp.outputs['Vector'], env.inputs['Vector'])
    WL.new(env.outputs['Color'], bg.inputs['Color']); bg.inputs['Strength'].default_value = strength
    WL.new(bg.outputs[0], out.inputs['Surface'])
    return world

def area(name, loc_mm, target_mm, size_mm, energy, col=(1, 1, 1), sy=None, spread=None):
    scn = bpy.context.scene
    old = bpy.data.objects.get(name)
    if old is not None: bpy.data.objects.remove(old)
    l = bpy.data.lights.new(name, 'AREA'); l.energy = energy; l.color = col; l.shape = 'RECTANGLE'
    l.size = size_mm * 0.001; l.size_y = (sy or size_mm) * 0.001
    if spread is not None: l.spread = spread
    o = bpy.data.objects.new(name, l); scn.collection.objects.link(o)
    o.location = K.W(loc_mm)
    o.rotation_euler = (K.W(target_mm) - K.W(loc_mm)).to_track_quat('-Z', 'Y').to_euler()
    return o

def setup_lights(c=(0, 0, 90), s=1.0, k=1.0):
    """lumini in jurul tintei c (mm); s = scara scenei (1 = injectorul intreg, ~180 mm); k = tarie.
    Energia creste cu s^2 ca iluminarea pe piesa sa ramana aceeasi cand apropii luminile."""
    c = np.asarray(c, float); e = k * s * s
    L = {}
    L['key'] = area('key', c + np.array([330, -420, 330]) * s, c, 300 * s, 20 * e, (1.0, 0.965, 0.92), sy=220 * s)
    L['fill'] = area('fill', c + np.array([-420, -380, 20]) * s, c, 420 * s, 4.5 * e, (0.82, 0.89, 1.0))
    L['rim'] = area('rim', c + np.array([-260, 300, 260]) * s, c, 90 * s, 16 * e, (0.78, 0.87, 1.0), sy=420 * s)
    L['top'] = area('top', c + np.array([40, -60, 520]) * s, c, 260 * s, 5 * e)
    L['low'] = area('low', c + np.array([120, -380, -330]) * s, c, 360 * s, 2.2 * e, (0.9, 0.93, 1.0))
    return L

def setup_camera():
    scn = bpy.context.scene
    old = bpy.data.objects.get('cam')
    if old is not None: bpy.data.objects.remove(old)
    cam = bpy.data.cameras.new('cam'); camO = bpy.data.objects.new('cam', cam)
    scn.collection.objects.link(camO); scn.camera = camO
    cam.sensor_fit = 'VERTICAL'; cam.sensor_height = 24.0
    cam.clip_start = 0.001; cam.clip_end = 50
    cam.dof.use_dof = False
    return camO

def aim(camO, pos_mm, tgt_mm, lens=50, roll=0.0):
    p = K.W(pos_mm); t = K.W(tgt_mm)
    camO.location = p
    q = (t - p).to_track_quat('-Z', 'Y')
    if roll:
        from mathutils import Quaternion
        q = q @ Quaternion((0, 0, 1), math.radians(roll))
    camO.rotation_mode = 'QUATERNION'; camO.rotation_quaternion = q
    camO.data.lens = lens; camO.data.dof.use_dof = False

def orbit_pos(tgt, az, el, dist):
    """pozitia camerei: azimut (grade, 0 = din fata, dinspre -Y; pozitiv = spre +X), elevatie, distanta (mm)"""
    a = math.radians(az); e = math.radians(el)
    return np.asarray(tgt, float) + dist * np.array([math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), math.sin(e)])

def setup_render(w=1080, h=1920, spp=32, expo=0.0):
    scn = bpy.context.scene; R = scn.render
    R.engine = 'CYCLES'
    R.resolution_x, R.resolution_y = w, h; R.resolution_percentage = 100
    R.film_transparent = True
    R.image_settings.file_format = 'PNG'; R.image_settings.color_mode = 'RGBA'; R.image_settings.compression = 20
    R.use_persistent_data = True
    scn.view_settings.view_transform = 'AgX'
    try: scn.view_settings.look = 'AgX - Medium High Contrast'
    except Exception: pass
    scn.view_settings.exposure = expo
    cy = scn.cycles
    cy.device = 'CPU'
    cy.samples = spp; cy.use_adaptive_sampling = False
    cy.use_denoising = True; cy.denoiser = 'OPENIMAGEDENOISE'
    try:
        cy.denoising_input_passes = 'RGB_ALBEDO_NORMAL'; cy.denoising_prefilter = 'ACCURATE'; cy.denoising_quality = 'HIGH'
    except Exception: pass
    cy.max_bounces = 8; cy.diffuse_bounces = 2; cy.glossy_bounces = 4; cy.transmission_bounces = 4
    cy.transparent_max_bounces = 32; cy.volume_bounces = 0
    cy.caustics_reflective = False; cy.caustics_refractive = False; cy.blur_glossy = 0.6
    cy.sample_clamp_indirect = 6.0; cy.sample_clamp_direct = 0.0
    cy.seed = 7
    try: cy.use_light_tree = True
    except Exception: pass
    R.threads_mode = 'AUTO'
    vl = bpy.context.view_layer; vl.use_pass_z = True
    try: vl.pass_alpha_threshold = 0.5
    except Exception: pass
    return R

def cam_info(camO):
    scn = bpy.context.scene; c = camO.data; R = scn.render
    bpy.context.view_layer.update()
    return {'M': [list(r) for r in camO.matrix_world], 'lens': c.lens, 'sensor': c.sensor_height, 'w': R.resolution_x, 'h': R.resolution_y}
