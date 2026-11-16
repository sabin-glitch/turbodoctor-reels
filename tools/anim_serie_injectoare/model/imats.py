# Materialele seriei „De ce se strica injectoarele” (Cycles). Coordonatele de textura sunt in mm (spatiul obiectului = reperul injectorului).
# Conventia de culori a seriei: motorina de inalta presiune = portocaliu-rosu, motorina de joasa presiune / retur = galben-chihlimbar, apa = albastru.
import bpy, math, os
from kit import srgb

EV = lambda k, d: float(os.environ.get(k, d))
SEC_K, SEC_M, SEC_R, HATCH, SEC_TONE = EV('SEC_K', 0.46), EV('SEC_M', 0.5), EV('SEC_R', 0.6), EV('HATCH', 1.25), EV('SEC_TONE', 0.28)
LIQ_EMIT = EV('LIQ_EMIT', 0.75)
C_HP, C_LP, C_WATER = 0xff5a26, 0xffc02a, 0x2f9bff
MAT = {}

def dim(h, k):
    return sum(int(round(min(255, ((h >> sh) & 255) * k))) << sh for sh in (16, 8, 0))

def _new(name):
    m = bpy.data.materials.new(name); m.use_nodes = True
    return m, m.node_tree.nodes, m.node_tree.links, m.node_tree.nodes['Principled BSDF']

def metal(name, col, rough=0.3, metal=1.0, bump=None, aniso=0.0, coat=0.0, bevel=0.0, mix=None, streak=None):
    """metal / plastic. bump=(scara, tarie[, variatie asperitate]); bevel = raza (mm) a muchiilor rotunjite la randare;
    mix=(culoare2, scara, contrast) pete; streak=(scara, tarie) urme fine de strunjire in jurul axei Z."""
    m, N, L, b = _new(name)
    b.inputs['Base Color'].default_value = srgb(col)
    b.inputs['Metallic'].default_value = metal; b.inputs['Roughness'].default_value = rough
    if aniso: b.inputs['Anisotropic'].default_value = aniso
    if coat: b.inputs['Coat Weight'].default_value = coat
    tc = N.new('ShaderNodeTexCoord')
    nrm = None
    if mix:
        nz = N.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = mix[1]; nz.inputs['Detail'].default_value = 5
        L.new(tc.outputs['Object'], nz.inputs['Vector'])
        cr = N.new('ShaderNodeValToRGB'); c = mix[2] if len(mix) > 2 else 0.25
        cr.color_ramp.elements[0].position = 0.5 - c; cr.color_ramp.elements[0].color = srgb(col)
        cr.color_ramp.elements[1].position = 0.5 + c; cr.color_ramp.elements[1].color = srgb(mix[0])
        L.new(nz.outputs['Fac'], cr.inputs['Fac']); L.new(cr.outputs['Color'], b.inputs['Base Color'])
    hgt = None
    if bump:
        nz = N.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = bump[0]; nz.inputs['Detail'].default_value = 6
        L.new(tc.outputs['Object'], nz.inputs['Vector']); hgt = nz.outputs['Fac']
        if len(bump) > 2:
            mr = N.new('ShaderNodeMapRange'); mr.inputs['To Min'].default_value = max(0.03, rough - bump[2] / 2); mr.inputs['To Max'].default_value = min(1.0, rough + bump[2] / 2)
            L.new(nz.outputs['Fac'], mr.inputs['Value']); L.new(mr.outputs['Result'], b.inputs['Roughness'])
    if streak:
        # urme de strunjire: zgomot intins pe circumferinta (variaza doar cu z)
        sx = N.new('ShaderNodeSeparateXYZ'); L.new(tc.outputs['Object'], sx.inputs[0])
        cz = N.new('ShaderNodeCombineXYZ'); L.new(sx.outputs['Z'], cz.inputs['Z'])
        nz2 = N.new('ShaderNodeTexNoise'); nz2.inputs['Scale'].default_value = streak[0]; nz2.inputs['Detail'].default_value = 3
        L.new(cz.outputs[0], nz2.inputs['Vector'])
        if hgt is not None:
            ad = N.new('ShaderNodeMath'); ad.operation = 'MULTIPLY_ADD'; ad.inputs[1].default_value = streak[1]
            L.new(nz2.outputs['Fac'], ad.inputs[0]); L.new(hgt, ad.inputs[2]); hgt = ad.outputs[0]
        else: hgt = nz2.outputs['Fac']
    if hgt is not None:
        bp = N.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = (bump[1] if bump else streak[1]); bp.inputs['Distance'].default_value = 0.05
        L.new(hgt, bp.inputs['Height']); nrm = bp
    if bevel:
        bv = N.new('ShaderNodeBevel'); bv.samples = 4; bv.inputs['Radius'].default_value = bevel * 0.001
        if nrm is not None: L.new(nrm.outputs['Normal'], bv.inputs['Normal'])
        L.new(bv.outputs['Normal'], b.inputs['Normal'])
    elif nrm is not None:
        L.new(nrm.outputs['Normal'], b.inputs['Normal'])
    return m

def _rho_z(N, L, tc):
    """(raza fata de axa Z, z) in spatiul obiectului"""
    sx = N.new('ShaderNodeSeparateXYZ'); L.new(tc.outputs['Object'], sx.inputs[0])
    xx = N.new('ShaderNodeMath'); xx.operation = 'MULTIPLY'; L.new(sx.outputs['X'], xx.inputs[0]); L.new(sx.outputs['X'], xx.inputs[1])
    yy = N.new('ShaderNodeMath'); yy.operation = 'MULTIPLY_ADD'; L.new(sx.outputs['Y'], yy.inputs[0]); L.new(sx.outputs['Y'], yy.inputs[1]); L.new(xx.outputs[0], yy.inputs[2])
    rr = N.new('ShaderNodeMath'); rr.operation = 'SQRT'; L.new(yy.outputs[0], rr.inputs[0])
    return rr.outputs[0], sx.outputs['Z']

def sec(name, col, period=2.0, sign=1.0, strength=0.25, k=None, metal=None, rough=None, plain=False):
    """fata de sectiune cu hasura: fract((rho + sign*z) / perioada); cele doua plane de taiere au tonuri diferite (dupa normala)."""
    m, N, L, b = _new(name)
    base = srgb(dim(col, SEC_K if k is None else k))
    b.inputs['Base Color'].default_value = base
    b.inputs['Metallic'].default_value = SEC_M if metal is None else metal
    b.inputs['Roughness'].default_value = SEC_R if rough is None else rough
    tc = N.new('ShaderNodeTexCoord')
    rho, z = _rho_z(N, L, tc)
    fac = None
    if not plain:
        a2 = N.new('ShaderNodeMath'); a2.operation = 'MULTIPLY_ADD'; a2.inputs[1].default_value = sign
        L.new(z, a2.inputs[0]); L.new(rho, a2.inputs[2])
        a3 = N.new('ShaderNodeMath'); a3.operation = 'DIVIDE'; a3.inputs[1].default_value = period; L.new(a2.outputs[0], a3.inputs[0])
        a4 = N.new('ShaderNodeMath'); a4.operation = 'FRACT'; L.new(a3.outputs[0], a4.inputs[0])
        a5 = N.new('ShaderNodeMath'); a5.operation = 'SUBTRACT'; a5.inputs[1].default_value = 0.5; L.new(a4.outputs[0], a5.inputs[0])
        a6 = N.new('ShaderNodeMath'); a6.operation = 'ABSOLUTE'; L.new(a5.outputs[0], a6.inputs[0])
        mrh = N.new('ShaderNodeMapRange'); mrh.interpolation_type = 'SMOOTHSTEP'
        mrh.inputs['From Min'].default_value = 0.21; mrh.inputs['From Max'].default_value = 0.29
        mrh.inputs['To Min'].default_value = 1.0 - strength * HATCH; mrh.inputs['To Max'].default_value = 1.0
        L.new(a6.outputs[0], mrh.inputs['Value']); fac = mrh.outputs['Result']
    # ton dupa planul de taiere: normala cu x > 0 (fata din stanga imaginii) e mai inchisa
    sn = N.new('ShaderNodeSeparateXYZ'); L.new(tc.outputs['Normal'], sn.inputs[0])
    tn = N.new('ShaderNodeMapRange'); tn.inputs['From Min'].default_value = -0.6; tn.inputs['From Max'].default_value = 0.6
    tn.inputs['To Min'].default_value = 1.0; tn.inputs['To Max'].default_value = 1.0 - SEC_TONE
    L.new(sn.outputs['X'], tn.inputs['Value'])
    if fac is not None:
        mt = N.new('ShaderNodeMath'); mt.operation = 'MULTIPLY'; L.new(fac, mt.inputs[0]); L.new(tn.outputs['Result'], mt.inputs[1]); fac = mt.outputs[0]
    else: fac = tn.outputs['Result']
    vs = N.new('ShaderNodeVectorMath'); vs.operation = 'SCALE'; vs.inputs[0].default_value = base[:3]
    L.new(fac, vs.inputs['Scale']); L.new(vs.outputs['Vector'], b.inputs['Base Color'])
    return m

def sec_coil(name, pitch=0.62):
    """sectiunea bobinei: spire de cupru (puncte) in rasina inchisa"""
    m, N, L, b = _new(name)
    tc = N.new('ShaderNodeTexCoord'); rho, z = _rho_z(N, L, tc)
    def cell(v, off=0.0):
        d = N.new('ShaderNodeMath'); d.operation = 'DIVIDE'; d.inputs[1].default_value = pitch; L.new(v, d.inputs[0])
        a = N.new('ShaderNodeMath'); a.operation = 'ADD'; a.inputs[1].default_value = off; L.new(d.outputs[0], a.inputs[0])
        f = N.new('ShaderNodeMath'); f.operation = 'FRACT'; L.new(a.outputs[0], f.inputs[0])
        s = N.new('ShaderNodeMath'); s.operation = 'SUBTRACT'; s.inputs[1].default_value = 0.5; L.new(f.outputs[0], s.inputs[0])
        return s.outputs[0]
    cx = cell(rho); cz = cell(z, 0.25)
    p1 = N.new('ShaderNodeMath'); p1.operation = 'MULTIPLY'; L.new(cx, p1.inputs[0]); L.new(cx, p1.inputs[1])
    p2 = N.new('ShaderNodeMath'); p2.operation = 'MULTIPLY_ADD'; L.new(cz, p2.inputs[0]); L.new(cz, p2.inputs[1]); L.new(p1.outputs[0], p2.inputs[2])
    d = N.new('ShaderNodeMath'); d.operation = 'SQRT'; L.new(p2.outputs[0], d.inputs[0])
    mr = N.new('ShaderNodeMapRange'); mr.interpolation_type = 'SMOOTHSTEP'
    mr.inputs['From Min'].default_value = 0.34; mr.inputs['From Max'].default_value = 0.42; mr.inputs['To Min'].default_value = 0.0; mr.inputs['To Max'].default_value = 1.0
    L.new(d.outputs[0], mr.inputs['Value'])
    cr = N.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].position = 0.0; cr.color_ramp.elements[0].color = srgb(0xc9773f)
    cr.color_ramp.elements[1].position = 1.0; cr.color_ramp.elements[1].color = srgb(0x1b1512)
    L.new(mr.outputs['Result'], cr.inputs['Fac']); L.new(cr.outputs['Color'], b.inputs['Base Color'])
    b.inputs['Metallic'].default_value = 0.6; b.inputs['Roughness'].default_value = 0.45
    return m

def liquid(name, col, op=0.9, emit=None, rough=0.35, spec=0.06, tone=0.16):
    """lichid „grafic”: culoare plina, nelegata de lumina (emisie), putin translucid. Nod 'COL' = culoarea, 'FADE' = opacitatea.
    Cele doua plane de taiere au tonuri putin diferite (dupa normala), ca muchia sectiunii sa se citeasca."""
    m, N, L, b = _new(name)
    rgb = N.new('ShaderNodeRGB'); rgb.name = 'COL'; rgb.outputs[0].default_value = srgb(col)
    b.inputs['Base Color'].default_value = [0, 0, 0, 1]
    tc = N.new('ShaderNodeTexCoord'); sn = N.new('ShaderNodeSeparateXYZ'); L.new(tc.outputs['Normal'], sn.inputs[0])
    tn = N.new('ShaderNodeMapRange'); tn.inputs['From Min'].default_value = -0.6; tn.inputs['From Max'].default_value = 0.6
    tn.inputs['To Min'].default_value = 1.0; tn.inputs['To Max'].default_value = 1.0 - tone
    L.new(sn.outputs['X'], tn.inputs['Value'])
    vs = N.new('ShaderNodeVectorMath'); vs.operation = 'SCALE'; L.new(rgb.outputs[0], vs.inputs[0]); L.new(tn.outputs['Result'], vs.inputs['Scale'])
    L.new(vs.outputs['Vector'], b.inputs['Emission Color'])
    b.inputs['Emission Strength'].default_value = LIQ_EMIT if emit is None else emit
    b.inputs['Roughness'].default_value = rough; b.inputs['IOR'].default_value = 1.46
    b.inputs['Specular IOR Level'].default_value = spec
    tr = N.new('ShaderNodeBsdfTransparent'); mx = N.new('ShaderNodeMixShader'); mx.name = 'FADE'
    mx.inputs['Fac'].default_value = op
    L.new(tr.outputs[0], mx.inputs[1]); L.new(b.outputs[0], mx.inputs[2]); L.new(mx.outputs[0], N['Material Output'].inputs['Surface'])
    try: m.cycles.emission_sampling = 'NONE'
    except Exception: pass
    return m

def set_liquid(name, col=None, op=None, emit=None):
    m = bpy.data.materials[name]; N = m.node_tree.nodes
    if col is not None: N['COL'].outputs[0].default_value = srgb(col)
    if op is not None: N['FADE'].inputs['Fac'].default_value = op
    if emit is not None: N['Principled BSDF'].inputs['Emission Strength'].default_value = emit

def damage(name, col, col2, rough=0.7, scale=9.0, stretch=(1, 1, 0.08), thr=0.5, soft=0.12, bump=0.8, metal=0.9, emis=None):
    """strat de uzura / rugina peste o suprafata: culoare + relief procedural, cu alfa in pete (thr = cat de mult acopera, 0..1).
    Nodul 'COVER' (Map Range) controleaza acoperirea: From Min = prag."""
    m, N, L, b = _new(name)
    tc = N.new('ShaderNodeTexCoord'); mp = N.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = stretch
    L.new(tc.outputs['Object'], mp.inputs['Vector'])
    nz = N.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = scale; nz.inputs['Detail'].default_value = 7; nz.inputs['Roughness'].default_value = 0.62
    L.new(mp.outputs['Vector'], nz.inputs['Vector'])
    cr = N.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].position = 0.35; cr.color_ramp.elements[0].color = srgb(col)
    cr.color_ramp.elements[1].position = 0.7; cr.color_ramp.elements[1].color = srgb(col2)
    L.new(nz.outputs['Fac'], cr.inputs['Fac']); L.new(cr.outputs['Color'], b.inputs['Base Color'])
    b.inputs['Metallic'].default_value = metal; b.inputs['Roughness'].default_value = rough
    bp = N.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = bump; bp.inputs['Distance'].default_value = 0.04
    L.new(nz.outputs['Fac'], bp.inputs['Height']); L.new(bp.outputs['Normal'], b.inputs['Normal'])
    # masca de acoperire: zgomot mai larg
    nz2 = N.new('ShaderNodeTexNoise'); nz2.inputs['Scale'].default_value = scale * 0.35; nz2.inputs['Detail'].default_value = 4
    L.new(mp.outputs['Vector'], nz2.inputs['Vector'])
    cv = N.new('ShaderNodeMapRange'); cv.name = 'COVER'; cv.interpolation_type = 'SMOOTHSTEP'
    cv.inputs['From Min'].default_value = 1.0 - thr; cv.inputs['From Max'].default_value = 1.0 - thr + soft
    L.new(nz2.outputs['Fac'], cv.inputs['Value']); L.new(cv.outputs['Result'], b.inputs['Alpha'])
    if emis is not None:
        b.inputs['Emission Color'].default_value = srgb(emis[0]); b.inputs['Emission Strength'].default_value = emis[1]
    return m

def set_cover(name, thr, soft=0.12):
    cv = bpy.data.materials[name].node_tree.nodes['COVER']
    cv.inputs['From Min'].default_value = 1.0 - thr; cv.inputs['From Max'].default_value = 1.0 - thr + soft

def make_all():
    M = MAT
    BV = 0.12
    # exterior
    M['body'] = metal('body', 0xb9bec6, 0.34, bump=(2.2, 0.05, 0.14), bevel=BV, streak=(26, 0.05))
    M['bodyDark'] = metal('bodyDark', 0x5a5f67, 0.42, bump=(3, 0.05, 0.12), bevel=BV)
    M['nut'] = metal('nut', 0x2d3035, 0.36, bump=(5, 0.04, 0.1), bevel=BV)
    M['nozzle'] = metal('nozzle', 0xd9dce1, 0.16, bevel=0.08, streak=(40, 0.03))
    M['zinc'] = metal('zinc', 0xcfd3d9, 0.3, bump=(3, 0.05, 0.12), bevel=BV)
    M['zincY'] = metal('zincY', 0xc9bf9a, 0.33, bump=(3, 0.05, 0.12), bevel=BV)
    M['steel'] = metal('steel', 0xb7bcc2, 0.3, bevel=0.06)
    M['steelPol'] = metal('steelPol', 0xe3e6ea, 0.11, bevel=0.05)
    M['steelGnd'] = metal('steelGnd', 0xd0d4d9, 0.2, bevel=0.05, streak=(60, 0.025))
    M['steelDark'] = metal('steelDark', 0x474b52, 0.38, bevel=0.06)
    M['ball'] = metal('ball', 0xeceef1, 0.14)
    M['copper'] = metal('copper', 0xc8794a, 0.3, bevel=0.1)
    M['brass'] = metal('brass', 0xc8a24e, 0.3)
    M['plastic'] = metal('plastic', 0x16171a, 0.42, metal=0.0, bump=(8, 0.05), coat=0.2, bevel=0.25)
    M['plasticG'] = metal('plasticG', 0x3a3d43, 0.5, metal=0.0, bevel=0.2)
    M['seal'] = metal('seal', 0xd9d2c2, 0.5, metal=0.0)
    M['castAlu'] = metal('castAlu', 0xb4b7bb, 0.52, bump=(1.2, 0.3, 0.2), bevel=0.3)
    M['machAlu'] = metal('machAlu', 0xd3d6da, 0.26, bump=(40, 0.03), bevel=0.15)
    M['iron'] = metal('iron', 0x6b6f75, 0.5, bump=(1.5, 0.25, 0.2), bevel=0.3)
    M['pistonAlu'] = metal('pistonAlu', 0xc3c6ca, 0.34, bump=(30, 0.03), bevel=0.2, streak=(18, 0.05))
    M['carbon'] = metal('carbon', 0x141312, 0.9, metal=0.0, bump=(6, 0.9))
    # sectiuni (perioada hasurii in mm, sensul)
    M['secBody'] = sec('secBody', 0xaab0b8, 2.0, 1.0, 0.24)
    M['secNozzle'] = sec('secNozzle', 0xcfd3d8, 1.3, -1.0, 0.22)
    M['secNut'] = sec('secNut', 0x666b73, 2.6, -1.0, 0.26)
    M['secValve'] = sec('secValve', 0xd6d0c0, 1.1, -1.0, 0.22)
    M['secScrew'] = sec('secScrew', 0x8d939b, 1.6, 1.0, 0.24)
    M['secCore'] = sec('secCore', 0x7b8088, 1.8, -1.0, 0.24)
    M['secMagNut'] = sec('secMagNut', 0xbfc4cb, 2.4, 1.0, 0.22)
    M['secArm'] = sec('secArm', 0xb3ada0, 0.9, 1.0, 0.24)
    M['secConn'] = sec('secConn', 0xc6cad0, 1.7, -1.0, 0.22)
    M['secPlastic'] = sec('secPlastic', 0x30333a, 1.0, 1.0, 0.0, k=0.9, metal=0.0, rough=0.7, plain=True)
    M['secCopper'] = sec('secCopper', 0xd08a55, 0.8, 1.0, 0.18, k=0.62)
    M['secSeal'] = sec('secSeal', 0xe6dfcf, 1.0, 1.0, 0.0, k=0.8, metal=0.0, rough=0.7, plain=True)
    M['secCoil'] = sec_coil('secCoil')
    M['secAlu'] = sec('secAlu', 0xd9dbde, 3.4, 1.0, 0.2)
    M['secIron'] = sec('secIron', 0x8a8f96, 3.0, -1.0, 0.24)
    M['secPiston'] = sec('secPiston', 0xc9cdd2, 2.6, -1.0, 0.2)
    # lichide
    M['fuelHP'] = liquid('fuelHP', C_HP, 0.93)
    M['fuelCC'] = liquid('fuelCC', C_HP, 0.93)          # camera de comanda (isi schimba presiunea)
    M['fuelSac'] = liquid('fuelSac', C_HP, 0.93)
    M['fuelLP'] = liquid('fuelLP', C_LP, 0.88)
    M['water'] = liquid('water', C_WATER, 0.9, emit=0.6)
    # filtrul de motorina
    M['paper'] = metal('paper', 0xe6dcc2, 0.92, metal=0.0, bump=(3.5, 0.5))
    M['secPaper'] = sec('secPaper', 0xefe5cb, 1.5, 0.0, 0.2, k=0.8, metal=0.0, rough=0.9)
    M['canPaint'] = metal('canPaint', 0x1d2733, 0.3, metal=0.35, coat=0.6, bevel=0.3)
    M['secCan'] = sec('secCan', 0x8d939b, 1.2, 1.0, 0.22)
    M['rubber'] = metal('rubber', 0x101011, 0.8, metal=0.0, bump=(5, 0.08))
    M['secRubber'] = sec('secRubber', 0x2a2b2e, 1.0, 1.0, 0.0, k=0.9, metal=0.0, rough=0.8, plain=True)
    M['bowl'] = metal('bowl', 0xdfe9f2, 0.08, metal=0.0, coat=0.4)
    M['bowl'].node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value = 0.22
    M['secBowl'] = sec('secBowl', 0xcfe0ee, 1.0, 1.0, 0.0, k=0.9, metal=0.0, rough=0.4, plain=True)
    M['secBowl'].node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value = 0.55
    M['dirt'] = damage('dirt', 0x2a2118, 0x6b5a40, rough=0.95, scale=3.0, stretch=(1, 1, 0.5), thr=0.75, soft=0.25, bump=0.6, metal=0.0)
    # uzura / rugina
    M['scored'] = damage('scored', 0x3a2f28, 0x8a6f58, rough=0.75, scale=7.0, stretch=(1, 1, 0.06), thr=0.62, bump=1.0)
    M['eroded'] = damage('eroded', 0x1e1a18, 0x6b5b4c, rough=0.85, scale=16.0, stretch=(1, 1, 1), thr=0.7, bump=1.0, metal=0.6)
    M['rust'] = damage('rust', 0x5a2a12, 0xc9652a, rough=0.9, scale=5.0, stretch=(1, 1, 0.6), thr=0.6, soft=0.2, bump=0.9, metal=0.15)
    for m in M.values(): m.use_fake_user = True
    return M
