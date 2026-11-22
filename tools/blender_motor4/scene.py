"""World, lights, cameras, section cuts, render settings."""
import bpy, math
from mathutils import Vector, Matrix
from lib import _n, box, apply_bool, remove


def section_cut(ob, axis, value, keep, sec_mat, eps=0.0):
    """cut `ob` (mesh in world == local space, i.e. identity transform assumed unless local_offset given)
    keep: +1 keeps coordinates >= value, -1 keeps <= value. Faces on the plane get `sec_mat`."""
    big = 5000.0
    lo, hi = [-big] * 3, [big] * 3
    i = 'xyz'.index(axis)
    if keep > 0: hi[i] = value - eps
    else: lo[i] = value + eps
    c = box('cutter', lo[0], hi[0], lo[1], hi[1], lo[2], hi[2])
    apply_bool(ob, c); remove(c)
    mark_section(ob, sec_mat, axis, value - eps * keep if keep > 0 else value + eps, -keep)
    return ob


def mark_section(ob, sec_mat, axis, value, sign, tol=0.03):
    me = ob.data
    if sec_mat is None: return
    if sec_mat.name not in [m.name for m in me.materials if m]:
        me.materials.append(sec_mat)
    mi = [m.name if m else '' for m in me.materials].index(sec_mat.name)
    i = 'xyz'.index(axis)
    n = 0
    for p in me.polygons:
        if abs(p.center[i] - value) < tol and p.normal[i] * sign > 0.97:
            p.material_index = mi; n += 1
    return n


def world_studio(cam_yaw_deg, strength=1.0):
    """dark studio + soft boxes by azimuth around the camera (from the CRI2 model)."""
    sc = bpy.context.scene
    w = bpy.data.worlds.get('studio') or bpy.data.worlds.new('studio')
    sc.world = w
    try: w.use_nodes = True
    except Exception: pass
    nt = w.node_tree
    for n in list(nt.nodes):
        if n.type not in ('OUTPUT_WORLD',): nt.nodes.remove(n)
    out = [n for n in nt.nodes if n.type == 'OUTPUT_WORLD'][0]
    bg = _n(nt, 'ShaderNodeBackground'); nt.links.new(bg.outputs[0], out.inputs['Surface'])
    tc = _n(nt, 'ShaderNodeTexCoord'); sx = _n(nt, 'ShaderNodeSeparateXYZ'); nt.links.new(tc.outputs['Generated'], sx.inputs[0])
    az = _n(nt, 'ShaderNodeMath', operation='ARCTAN2'); nt.links.new(sx.outputs['Y'], az.inputs[0]); nt.links.new(sx.outputs['X'], az.inputs[1])
    el = sx.outputs['Z']

    def mr(src, a0, a1, b0=0.0, b1=1.0):
        m = _n(nt, 'ShaderNodeMapRange'); m.clamp = True
        m.inputs[1].default_value = a0; m.inputs[2].default_value = a1; m.inputs[3].default_value = b0; m.inputs[4].default_value = b1
        nt.links.new(src, m.inputs[0]); return m.outputs[0]

    def mul(a_, b_):
        m = _n(nt, 'ShaderNodeMath', operation='MULTIPLY'); nt.links.new(a_, m.inputs[0])
        if isinstance(b_, float): m.inputs[1].default_value = b_
        else: nt.links.new(b_, m.inputs[1])
        return m.outputs[0]

    def add(a_, b_):
        m = _n(nt, 'ShaderNodeMath', operation='ADD'); nt.links.new(a_, m.inputs[0]); nt.links.new(b_, m.inputs[1]); return m.outputs[0]

    yaw = math.radians(cam_yaw_deg)
    cam_back = math.atan2(-math.cos(yaw), -math.sin(yaw))

    def box_light(center, half, e0, e1, gain):
        d = _n(nt, 'ShaderNodeMath', operation='SUBTRACT'); nt.links.new(az.outputs[0], d.inputs[0]); d.inputs[1].default_value = center
        wr = _n(nt, 'ShaderNodeMath', operation='WRAP'); nt.links.new(d.outputs[0], wr.inputs[0]); wr.inputs[1].default_value = math.pi; wr.inputs[2].default_value = -math.pi
        ab = _n(nt, 'ShaderNodeMath', operation='ABSOLUTE'); nt.links.new(wr.outputs[0], ab.inputs[0])
        h = mr(ab.outputs[0], half, half * 0.55, 0.0, 1.0)
        v = mul(mr(el, e0, e0 + 0.08), mr(el, e1, e1 - 0.08))
        return mul(mul(h, v), gain)

    L = box_light(cam_back, math.radians(13), -0.35, 0.70, 2.6)
    L = add(L, box_light(cam_back + math.radians(68), math.radians(9), -0.25, 0.75, 2.0))
    L = add(L, box_light(cam_back - math.radians(72), math.radians(8), -0.25, 0.75, 1.6))
    L = add(L, box_light(cam_back + math.radians(180), math.radians(25), -0.10, 0.60, 0.8))
    L = add(L, mul(mr(el, 0.80, 0.95), 1.4))
    base = mr(el, -0.6, 0.9, 0.02, 0.16)
    tot = add(L, base)
    nt.links.new(tot, bg.inputs['Color']); bg.inputs['Strength'].default_value = strength
    # visible to camera? keep transparent film anyway
    return w


def sun_lights(cam_yaw_deg, key=3.0, rim=2.2, fill=0.42):
    sc = bpy.context.scene
    for n in ('key', 'rim', 'fill'):
        o = bpy.data.objects.get(n)
        if o: bpy.data.objects.remove(o, do_unlink=True)
    yaw = cam_yaw_deg
    for name, (pit, az), en, ang in (('key', (50, yaw - 35), key, 10), ('rim', (62, yaw + 150), rim, 6), ('fill', (75, yaw + 40), fill, 30)):
        ld = bpy.data.lights.get(name) or bpy.data.lights.new(name, 'SUN')
        ld.energy = en; ld.angle = math.radians(ang)
        lo = bpy.data.objects.new(name, ld)
        lo.rotation_euler = (math.radians(pit), 0, math.radians(az))
        sc.collection.objects.link(lo)


def camera(name, target, yaw, pitch, dist, lens, shift=(0.0, 0.0)):
    """yaw: azimuth of the viewing direction (deg, 0 = looking +Y), pitch: down angle (deg)."""
    sc = bpy.context.scene
    cd = bpy.data.cameras.get(name) or bpy.data.cameras.new(name)
    cd.sensor_fit = 'VERTICAL'; cd.sensor_height = 24.0; cd.sensor_width = 24.0 * 1080 / 1920
    cd.lens = lens; cd.clip_start = 5.0; cd.clip_end = 20000.0
    cd.shift_x, cd.shift_y = shift
    co = bpy.data.objects.get(name) or bpy.data.objects.new(name, cd)
    if co.name not in sc.collection.objects: sc.collection.objects.link(co)
    y, p = math.radians(yaw), math.radians(pitch)
    d = Vector((math.sin(y) * math.cos(p), math.cos(y) * math.cos(p), -math.sin(p)))
    co.location = Vector(target) - d * dist
    co.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    co['yaw'] = yaw
    return co


def render_settings(samples=24, pct=100, w=1080, h=1920):
    sc = bpy.context.scene
    r = sc.render; r.engine = 'CYCLES'; r.resolution_x = w; r.resolution_y = h; r.resolution_percentage = pct
    r.film_transparent = True
    r.use_persistent_data = True
    cy = sc.cycles; cy.device = 'CPU'; cy.samples = samples; cy.use_adaptive_sampling = True; cy.adaptive_threshold = 0.05
    cy.use_denoising = True; cy.denoiser = 'OPENIMAGEDENOISE'
    try:
        cy.denoising_input_passes = 'RGB_ALBEDO_NORMAL'; cy.denoising_prefilter = 'FAST'
    except Exception: pass
    cy.max_bounces = 6; cy.glossy_bounces = 2; cy.diffuse_bounces = 1; cy.transmission_bounces = 1
    cy.transparent_max_bounces = 12; cy.volume_bounces = 0
    cy.caustics_reflective = False; cy.caustics_refractive = False
    cy.blur_glossy = 1.0
    try: cy.use_light_tree = True
    except Exception: pass
    sc.view_settings.view_transform = 'AgX'
    for lk in ('AgX - Medium High Contrast', 'Medium High Contrast'):
        try:
            sc.view_settings.look = lk; break
        except Exception:
            pass
    r.image_settings.file_format = 'PNG'; r.image_settings.color_mode = 'RGBA'; r.image_settings.color_depth = '8'
    r.threads_mode = 'AUTO'
