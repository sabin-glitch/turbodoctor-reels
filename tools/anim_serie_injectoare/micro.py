# Scena micro (1 unitate = 1 micron): acul si ghidajul in sectiune, cu jocul de 3 microni plin cu motorina, si un fir de par de 60 de microni.
# Straturi pentru stari: zgarieturi pe marginile jocului (ep1), rugina pe pereti si rugina care umple jocul (ep2), apa in loc de motorina (ep2).
#   venv_bpy/bin/python micro.py   -> blend/micro.blend + blend/micro.json
import sys, os, json, math
sys.path.insert(0, '/home/claude/w/inj')
import bpy, bmesh, numpy as np
import kit as K, imats as IM

OUT = '/home/claude/w/serinj/blend/'; os.makedirs(OUT, exist_ok=True)
K.init(empty=True); M = IM.make_all()
G = 1.5                  # jumatate din joc (jocul = 3 microni)
ZH = 120.0               # jumatate din inaltimea blocurilor

def sec_lin(name, col, period=9.0, sign=1.0, strength=0.25):
    """hasura in linii drepte (piesa plana): fract((x + sign*z) / perioada)"""
    m, N, L, b = IM._new(name)
    base = IM.srgb(IM.dim(col, IM.SEC_K)); b.inputs['Base Color'].default_value = base
    b.inputs['Metallic'].default_value = IM.SEC_M; b.inputs['Roughness'].default_value = IM.SEC_R
    tc = N.new('ShaderNodeTexCoord'); sx = N.new('ShaderNodeSeparateXYZ'); L.new(tc.outputs['Object'], sx.inputs[0])
    a2 = N.new('ShaderNodeMath'); a2.operation = 'MULTIPLY_ADD'; a2.inputs[1].default_value = sign; L.new(sx.outputs['Z'], a2.inputs[0]); L.new(sx.outputs['X'], a2.inputs[2])
    a3 = N.new('ShaderNodeMath'); a3.operation = 'DIVIDE'; a3.inputs[1].default_value = period; L.new(a2.outputs[0], a3.inputs[0])
    a4 = N.new('ShaderNodeMath'); a4.operation = 'FRACT'; L.new(a3.outputs[0], a4.inputs[0])
    a5 = N.new('ShaderNodeMath'); a5.operation = 'SUBTRACT'; a5.inputs[1].default_value = 0.5; L.new(a4.outputs[0], a5.inputs[0])
    a6 = N.new('ShaderNodeMath'); a6.operation = 'ABSOLUTE'; L.new(a5.outputs[0], a6.inputs[0])
    mr = N.new('ShaderNodeMapRange'); mr.interpolation_type = 'SMOOTHSTEP'
    mr.inputs['From Min'].default_value = 0.21; mr.inputs['From Max'].default_value = 0.29
    mr.inputs['To Min'].default_value = 1.0 - strength * IM.HATCH; mr.inputs['To Max'].default_value = 1.0
    L.new(a6.outputs[0], mr.inputs['Value'])
    vs = N.new('ShaderNodeVectorMath'); vs.operation = 'SCALE'; vs.inputs[0].default_value = base[:3]
    L.new(mr.outputs['Result'], vs.inputs['Scale']); L.new(vs.outputs['Vector'], b.inputs['Base Color'])
    return m

def hair_mat():
    m, N, L, b = IM._new('hair')
    b.inputs['Base Color'].default_value = IM.srgb(0x3a271a); b.inputs['Roughness'].default_value = 0.38
    b.inputs['Coat Weight'].default_value = 0.35; b.inputs['Coat Roughness'].default_value = 0.25
    tc = N.new('ShaderNodeTexCoord')
    wv = N.new('ShaderNodeTexWave'); wv.wave_type = 'BANDS'; wv.bands_direction = 'X'; wv.wave_profile = 'SAW'
    wv.inputs['Scale'].default_value = 0.11; wv.inputs['Distortion'].default_value = 3.0; wv.inputs['Detail'].default_value = 2.0
    wv.inputs['Detail Scale'].default_value = 0.6
    L.new(tc.outputs['Object'], wv.inputs['Vector'])
    bp = N.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.55; bp.inputs['Distance'].default_value = 0.8
    L.new(wv.outputs['Fac'], bp.inputs['Height']); L.new(bp.outputs['Normal'], b.inputs['Normal'])
    nz = N.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 0.05; L.new(tc.outputs['Object'], nz.inputs['Vector'])
    cr = N.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].color = IM.srgb(0x2a1b12); cr.color_ramp.elements[1].color = IM.srgb(0x5a3b26)
    L.new(nz.outputs['Fac'], cr.inputs['Fac']); L.new(cr.outputs['Color'], b.inputs['Base Color'])
    return m

def block(name, x0, x1, mat_side, mat_sec, y0=0.0, y1=70.0):
    """bloc cu fata din fata (y = y0) hasurata = fata de sectiune"""
    o = K.box(name, (x1 - x0, y1 - y0, 2 * ZH), c=((x0 + x1) / 2, (y0 + y1) / 2, 0), mat=[mat_side, mat_sec])
    me = o.data
    for p in me.polygons:
        if p.normal.y < -0.9: p.material_index = 1
    me.update(); return o

secN = sec_lin('secMicN', 0xcfd3d8, 10.0, -1.0, 0.24); secG = sec_lin('secMicG', 0xaab0b8, 12.0, 1.0, 0.24)
needle = block('m_needle', -90.0, -G, M['steelPol'], secN)
guide = block('m_guide', G, 90.0, M['body'], secG)
fuel = K.box('m_fuel', (2 * G, 70.0, 2 * ZH), c=(0, 35.06, 0), mat=M['fuelHP']); fuel.visible_shadow = False
water = K.box('m_water', (2 * G, 70.0, 2 * ZH), c=(0, 35.06, 0), mat=M['water']); water.visible_shadow = False; water.hide_render = True
# firul de par, in fata sectiunii, de-a curmezisul
hm = hair_mat()
hair = K.cyl('m_hair', 30.0, 400.0, c=(0, -46.0, 46.0), axis='X', mat=hm, seg=96)
# zgarieturi pe marginile jocului (stratul de uzura, vazut in sectiune)
def edge_strip(name, x0, x1, mat, y=-0.02, z0=-ZH, z1=ZH):
    o = K.box(name, (x1 - x0, 0.04, z1 - z0), c=((x0 + x1) / 2, y, (z0 + z1) / 2), mat=mat); o.visible_shadow = False; o.hide_render = True; return o
IM.set_cover('scored', 0.62)
sc = [edge_strip('dm_scL', -G - 1.6, -G, M['scored']), edge_strip('dm_scR', G, G + 1.6, M['scored'])]
# rugina: crusta pe pereti (strat subtire) si crusta care umple jocul
rustC = IM.damage('rustC', 0x4a220f, 0xc0602a, rough=0.92, scale=0.35, stretch=(1, 1, 0.5), thr=1.0, soft=0.05, bump=1.0, metal=0.1)
def crust(name, x0, x1):
    o = K.box(name, (x1 - x0, 70.0, 2 * ZH), c=((x0 + x1) / 2, 35.0 - 0.03, 0), mat=rustC); o.hide_render = True; return o
r1 = [crust('m_rustL1', -G, -G + 0.75), crust('m_rustR1', G - 0.75, G)]
r2 = [crust('m_rustL2', -G, 0.02), crust('m_rustR2', -0.02, G)]
# pelicula de lac (ep3): strat subtire, chihlimbar lucios, pe ambii pereti
lacq = IM.metal('lacq', 0x3d2208, 0.22, metal=0.0, coat=0.5)      # lac maro-inchis, sa se deosebeasca de motorina portocalie
def film(name, x0, x1):
    o = K.box(name, (x1 - x0, 70.0, 2 * ZH), c=((x0 + x1) / 2, 35.0 - 0.03, 0), mat=lacq); o.hide_render = True; return o
l1 = [film('m_lacL1', -G, -G + 0.5), film('m_lacR1', G - 0.5, G)]      # schematic: 0,5 si 1 micron pe fiecare perete
l2 = [film('m_lacL2', -G, -G + 1.0), film('m_lacR2', G - 1.0, G)]
json.dump({'G': G, 'hair': {'c': [0, -46.0, 46.0], 'r': 30.0}}, open(OUT + 'micro.json', 'w'))
bpy.ops.wm.save_as_mainfile(filepath=OUT + 'micro.blend')
print('SAVED micro', flush=True)
