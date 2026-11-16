# Materialele filmului (Cycles / EEVEE). Coordonatele de textura sunt in mm (spatiul obiectului).
import bpy
from kit import pbr, srgb

MAT = {}

def heat_inox(name, ghost=None):
    """inox de evacuare cu irizatii de caldura (pai / albastrui) - materialul catalizatorului si al filtrului"""
    m = pbr(name, 0xa9aaab, 1.0, 0.36, bump=(2.2, 0.06, 0.16), ghost=ghost)
    nt = m.node_tree; N = nt.nodes; L = nt.links; b = N['Principled BSDF']
    tc = N.new('ShaderNodeTexCoord')
    nz = N.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 0.018; nz.inputs['Detail'].default_value = 3; nz.inputs['Roughness'].default_value = 0.55
    L.new(tc.outputs['Object'], nz.inputs['Vector'])
    cr = N.new('ShaderNodeValToRGB'); e = cr.color_ramp.elements
    e[0].position = 0.42; e[0].color = srgb(0xa9aaab)
    e[1].position = 0.60; e[1].color = srgb(0xa08a62)
    e2 = cr.color_ramp.elements.new(0.68); e2.color = srgb(0x80604f)
    e3 = cr.color_ramp.elements.new(0.75); e3.color = srgb(0x535f85)
    e4 = cr.color_ramp.elements.new(0.84); e4.color = srgb(0x9a9da2)
    L.new(nz.outputs['Fac'], cr.inputs['Fac']); L.new(cr.outputs['Color'], b.inputs['Base Color'])
    return m

def brushed(name, col, rough=0.3, ghost=None):
    m = pbr(name, col, 1.0, rough, ghost=ghost)
    return m

def emissive(name, col, strength=1.0, alpha_attr=False):
    m = bpy.data.materials.new(name); m.use_nodes = True
    N = m.node_tree.nodes; L = m.node_tree.links
    b = N['Principled BSDF']
    b.inputs['Base Color'].default_value = srgb(col)
    b.inputs['Emission Color'].default_value = srgb(col); b.inputs['Emission Strength'].default_value = strength
    b.inputs['Roughness'].default_value = 0.6
    try: m.cycles.emission_sampling = 'NONE'
    except Exception: pass
    return m

def particle_mat(name, rough=0.5, metal=0.0, emis=0.0, soft=False, spec=0.5):
    """material pentru norii de particule: culoarea si alfa vin din atributul de culoare 'pc' (pe varf).
    emis -> tarie de emisie (culoarea proprie); soft -> margini moi (aburi, fum)."""
    m = bpy.data.materials.new(name); m.use_nodes = True
    N = m.node_tree.nodes; L = m.node_tree.links
    b = N['Principled BSDF']
    at = N.new('ShaderNodeAttribute'); at.attribute_name = 'pc'; at.attribute_type = 'GEOMETRY'
    L.new(at.outputs['Color'], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = rough; b.inputs['Metallic'].default_value = metal
    b.inputs['Specular IOR Level'].default_value = spec
    if emis:
        L.new(at.outputs['Color'], b.inputs['Emission Color']); b.inputs['Emission Strength'].default_value = emis
    if soft:
        lw = N.new('ShaderNodeLayerWeight'); lw.inputs['Blend'].default_value = 0.35
        inv = N.new('ShaderNodeMath'); inv.operation = 'SUBTRACT'; inv.inputs[0].default_value = 1.0
        L.new(lw.outputs['Facing'], inv.inputs[1])
        pw = N.new('ShaderNodeMath'); pw.operation = 'POWER'; pw.inputs[1].default_value = 1.6
        L.new(inv.outputs[0], pw.inputs[0])
        mu = N.new('ShaderNodeMath'); mu.operation = 'MULTIPLY'
        L.new(pw.outputs[0], mu.inputs[0]); L.new(at.outputs['Alpha'], mu.inputs[1])
        L.new(mu.outputs[0], b.inputs['Alpha'])
    else:
        L.new(at.outputs['Alpha'], b.inputs['Alpha'])
    try: m.cycles.emission_sampling = 'NONE'
    except Exception: pass
    return m

def make_all():
    M = MAT
    # fonta / aluminiu turnat
    M['castIron'] = pbr('castIron', 0x4d4640, 0.9, 0.7, bump=(0.9, 0.5, 0.22), mix=(0x6a4c3a, 0.03, 0.22), ghost='exh')
    M['blockIron'] = pbr('blockIron', 0x3e4145, 0.75, 0.58, bump=(0.8, 0.35, 0.2))
    M['castAlu'] = pbr('castAlu', 0xb2b5b9, 1.0, 0.5, bump=(1.4, 0.32, 0.22))
    M['castAluG'] = pbr('castAluG', 0xb2b5b9, 1.0, 0.5, bump=(1.4, 0.32, 0.22), ghost='int')
    M['headAlu'] = pbr('headAlu', 0xa9acb0, 1.0, 0.52, bump=(1.2, 0.3, 0.2))
    M['machAlu'] = pbr('machAlu', 0xd3d6da, 1.0, 0.24, bump=(40, 0.03))
    M['machIron'] = pbr('machIron', 0x9da1a6, 1.0, 0.3, bump=(30, 0.04))
    M['secIron'] = pbr('secIron', 0x8f9399, 1.0, 0.36, bump=(25, 0.05, 0.1))
    M['secAlu'] = pbr('secAlu', 0xc9cdd2, 1.0, 0.3, bump=(25, 0.05, 0.1))
    M['secDark'] = pbr('secDark', 0x2b2d30, 0.3, 0.5)
    # tabla si tevi de evacuare
    M['inoxHeat'] = heat_inox('inoxHeat', ghost='exh')
    M['inoxHeatS'] = heat_inox('inoxHeatS')            # varianta care nu devine transparenta
    M['inox'] = pbr('inox', 0xc2c4c7, 1.0, 0.3, bump=(3, 0.03, 0.1), ghost='exh')
    M['inoxS'] = pbr('inoxS', 0xc2c4c7, 1.0, 0.3, bump=(3, 0.03, 0.1))
    M['inoxEgr'] = pbr('inoxEgr', 0xbfc1c4, 1.0, 0.33, bump=(3, 0.03, 0.1), ghost='egr')
    M['flex'] = pbr('flex', 0x9a9c9f, 1.0, 0.42, bump=(6, 0.5, 0.1), ghost='exh')
    M['steel'] = pbr('steel', 0xb4b9bf, 1.0, 0.3)
    M['steelPol'] = pbr('steelPol', 0xdde0e4, 1.0, 0.14)
    M['steelDark'] = pbr('steelDark', 0x44484e, 1.0, 0.42)
    M['zinc'] = pbr('zinc', 0xbfb891, 1.0, 0.34, bump=(3, 0.05, 0.12))
    M['zincW'] = pbr('zincW', 0xc6cbd2, 1.0, 0.32, bump=(3, 0.05, 0.12))
    M['clamp'] = pbr('clamp', 0xc9ccd0, 1.0, 0.26)
    M['copper'] = pbr('copper', 0xc27a4e, 1.0, 0.3)
    M['brass'] = pbr('brass', 0xc8a24e, 1.0, 0.3)
    # plastic, cauciuc
    M['plasticBlack'] = pbr('plasticBlack', 0x17181a, 0.0, 0.42, bump=(8, 0.05), coat=0.15)
    M['plasticBlackG'] = pbr('plasticBlackG', 0x17181a, 0.0, 0.42, coat=0.15, ghost='int')
    M['plasticGrey'] = pbr('plasticGrey', 0x3b3e43, 0.0, 0.5)
    M['rubber'] = pbr('rubber', 0x0e0e0f, 0.0, 0.78, bump=(5, 0.08))
    M['rubberHose'] = pbr('rubberHose', 0x141414, 0.0, 0.7, bump=(2.5, 0.1))
    M['wire'] = pbr('wire', 0x1a1a1c, 0.0, 0.55)
    M['connGrey'] = pbr('connGrey', 0x55595f, 0.0, 0.5)
    M['gasket'] = pbr('gasket', 0x2a2d31, 0.4, 0.5)
    # ceramica, depuneri
    M['ceramic'] = pbr('ceramic', 0xd8cdb6, 0.0, 0.92, bump=(9, 0.25))
    M['ceramicCat'] = pbr('ceramicCat', 0x9d9589, 0.0, 0.9, bump=(9, 0.2))
    M['mat'] = pbr('mat', 0xe2dfd6, 0.0, 1.0, bump=(6, 0.5))
    M['soot'] = pbr('soot', 0x0b0b0c, 0.0, 0.95, bump=(12, 0.6), emis=0xff5a14, emis_str=0.0)
    M['ash'] = pbr('ash', 0xcfc9bd, 0.0, 1.0, bump=(10, 0.7))
    M['glaze'] = pbr('glaze', 0x9fb7a6, 0.0, 0.25, bump=(6, 0.4), coat=0.6)
    M['carbon'] = pbr('carbon', 0x121110, 0.0, 0.85, bump=(4, 0.9))
    # lichide
    M['coolant'] = pbr('coolant', 0xe0408a, 0.0, 0.12, alpha=0.78, emis=0xe0408a, emis_str=0.25)
    M['oilLiq'] = pbr('oilLiq', 0xa86a12, 0.0, 0.08, alpha=0.85)
    M['fuelLiq'] = pbr('fuelLiq', 0xd9c04a, 0.0, 0.1, alpha=0.8)
    M['crack'] = pbr('crack', 0x050505, 0.0, 0.9)
    # nori de particule
    M['p_gas'] = particle_mat('p_gas', rough=0.6, emis=2.2, soft=True)
    M['p_soot'] = particle_mat('p_soot', rough=0.95, spec=0.1)
    M['p_liq'] = particle_mat('p_liq', rough=0.08, emis=0.35)
    M['p_steam'] = particle_mat('p_steam', rough=0.9, emis=0.5, soft=True)
    M['p_fire'] = particle_mat('p_fire', rough=0.6, emis=14.0, soft=True)
    M['p_smoke'] = particle_mat('p_smoke', rough=1.0, emis=0.0, soft=True, spec=0.0)
    for m in M.values(): m.use_fake_user = True
    return M
