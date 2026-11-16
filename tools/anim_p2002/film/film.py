# Partea de Blender a filmului: incarca ansamblul, stari (transparente, chei de forma, pozitii), randare de cadre cu adancime.
import sys, os, json, math, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import bpy, numpy as np
from mathutils import Vector, Matrix
import kit as K, layout as L, rig

D = None; scn = None; cam = None; META = None
GH_A0 = 0.045; GH_A1 = 0.62

def _ghost_nodes(m):
    """alfa de tip raze X: aproape transparent privit din fata, mai opac pe contur (se vede forma piesei)"""
    nt = m.node_tree; N = nt.nodes; Lk = nt.links; b = N['Principled BSDF']
    for l in list(Lk):
        if l.to_node == b and l.to_socket.name == 'Alpha': Lk.remove(l)
    if N.get('GH_OUT'): return
    lw = N.new('ShaderNodeLayerWeight'); lw.inputs['Blend'].default_value = 0.32
    pw = N.new('ShaderNodeMath'); pw.operation = 'POWER'; pw.inputs[1].default_value = 2.2
    Lk.new(lw.outputs['Facing'], pw.inputs[0])
    mr = N.new('ShaderNodeMapRange'); mr.name = 'GH_OUT'
    mr.inputs['To Min'].default_value = GH_A0; mr.inputs['To Max'].default_value = GH_A1
    Lk.new(pw.outputs[0], mr.inputs['Value'])

def ghost(group, g):
    """g = 0 piesa plina (alfa deconectat, randare rapida); g = 1 piesa transparenta"""
    for m in bpy.data.materials:
        if m.get('ghost') == group and m.node_tree:
            nt = m.node_tree; b = nt.nodes['Principled BSDF']; o = nt.nodes['GH_OUT']
            links = [l for l in nt.links if l.to_node == b and l.to_socket.name == 'Alpha']
            if g <= 0.001:
                for l in links: nt.links.remove(l)
                b.inputs['Alpha'].default_value = 1.0
            else:
                o.inputs['To Min'].default_value = 1.0 + (GH_A0 - 1.0) * g; o.inputs['To Max'].default_value = 1.0 + (GH_A1 - 1.0) * g
                if not links: nt.links.new(o.outputs['Result'], b.inputs['Alpha'])

def load(w=1080, h=1920, spp=32, world=0.28, expo=-0.6):
    global D, scn, cam, META
    bpy.ops.wm.open_mainfile(filepath=os.path.join(HERE, 'out', 'assets.blend'))
    K.init(empty=False)
    D = bpy.data.objects; scn = bpy.context.scene
    META = json.load(open(os.path.join(HERE, 'out', 'meta.json')))
    for m in bpy.data.materials:
        if m.get('ghost') and m.node_tree: _ghost_nodes(m)
    for g in ('exh', 'int', 'egr'): ghost(g, 0)
    rig.setup_world(world); rig.setup_lights(); cam = rig.setup_camera(); rig.setup_render(w, h, spp)
    scn.view_settings.exposure = expo
    if os.environ.get('DPF_GPU'):                     # randare pe placa video (OptiX / CUDA), de ex. pe un laptop cu RTX
        pr = bpy.context.preferences.addons['cycles'].preferences
        for kind in ('OPTIX', 'CUDA'):
            try:
                pr.compute_device_type = kind; pr.get_devices()
                if any(d.type == kind for d in pr.devices):
                    for d in pr.devices: d.use = (d.type == kind)
                    scn.cycles.device = 'GPU'; print('Cycles pe', kind, flush=True); break
            except Exception as e: print('fara', kind, e, flush=True)
    vl = bpy.context.view_layer; vl.use_pass_z = True; vl.pass_alpha_threshold = 0.9
    return scn

def key(name, v):
    D[name].data.shape_keys.key_blocks['K'].value = v

def show(name, on=True):
    o = D[name]; o.hide_render = not on
    for c in o.children_recursive: c.hide_render = not on

EX_MAX = math.radians(250); IN_MAX = math.radians(470)
def valve_lift(th, th_max, dur=math.radians(236), lift=7.0):
    d = (th - th_max + 2 * math.pi) % (4 * math.pi) - 2 * math.pi
    if abs(d) >= dur / 2: return 0.0
    return lift * (0.5 + 0.5 * math.cos(2 * math.pi * d / dur))

def pose(th):
    """th = unghiul arborelui cotit (rad), 0 = PMS la inceputul destinderii; ciclul are 4*pi"""
    r = L.STROKE / 2; pz = L.piston_z(th)
    D['CRANK'].rotation_euler = (th, 0, 0)
    D['PISTON'].location = (L.SEC_X, 0, pz)
    D['ROD'].location = (L.SEC_X, -r * math.sin(th), r * math.cos(th)); D['ROD'].rotation_euler = (-math.asin(r * math.sin(th) / L.ROD), 0, 0)
    for nm, y, tm in (('VEX', -25.0, EX_MAX), ('VIN', 25.0, IN_MAX)):
        lf = valve_lift(th, tm)
        D[nm].location = (L.SEC_X, y, L.DECK + 0.6 - lf)
        D[nm + '.SPR'].scale = (1, 1, (22.0 - lf) / 22.0)
        D[nm + '.CAM'].rotation_euler = ((th - tm) / 2, 0, 0)
    return pz

def flap(name, ang):
    D[name].rotation_euler = (ang, 0, 0)

def rotor(a):
    D['ROTOR'].rotation_euler = (a, 0, 0)

def cam_info():
    c = cam.data; R = scn.render
    return {'M': [list(r) for r in cam.matrix_world], 'lens': c.lens, 'sensor': c.sensor_height, 'w': R.resolution_x, 'h': R.resolution_y,
            'fstop': c.dof.aperture_fstop if c.dof.use_dof else 0, 'focus': c.dof.focus_distance}

def render(base, exr=True):
    """scrie base.png (RGBA, cu transformarea de culoare) si, optional, base.exr (multistrat, cu adancimea) + base.json (camera)"""
    R = scn.render; s = R.image_settings
    if hasattr(s, 'media_type'): s.media_type = 'IMAGE'
    s.file_format = 'PNG'; s.color_mode = 'RGBA'; s.color_depth = '8'; s.compression = 20
    R.filepath = base + '.png'
    bpy.context.view_layer.update()
    t = time.time(); bpy.ops.render.render(write_still=True); dt = time.time() - t
    if exr:
        if hasattr(s, 'media_type'): s.media_type = 'MULTI_LAYER_IMAGE'
        s.file_format = 'OPEN_EXR_MULTILAYER'; s.color_depth = '32'; s.exr_codec = 'ZIP'
        bpy.data.images['Render Result'].save_render(base + '.exr', scene=scn)
        if hasattr(s, 'media_type'): s.media_type = 'IMAGE'
        s.file_format = 'PNG'; s.color_mode = 'RGBA'; s.color_depth = '8'
    json.dump(cam_info(), open(base + '.json', 'w'))
    return dt
