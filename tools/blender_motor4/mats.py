"""Material library (realistic surfaces + Sabin's section/fluid conventions)."""
import math
from lib import mat_metal, mat_plastic, mat_section, mat_glow_fluid, mat_gas, srgb, new_mat, _n, obj_attr
import bpy

M = {}

LP_BLUE = srgb(0x2f8cff)     # low-pressure fuel
HP_ORANGE = srgb(0xff6a3d)   # high-pressure fuel
OIL_A = srgb(0xffb52e)       # oil (amber)
OIL_B = srgb(0xff8a1c)       # oil under pressure (deeper)


def mat_bore(name):
    """honed cylinder bore: polished iron with cross-hatch."""
    m, new = new_mat(name)
    if not new: return m
    nt = m.node_tree; b = nt.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (0.42, 0.43, 0.45, 1); b.inputs['Metallic'].default_value = 1.0
    b.inputs['Roughness'].default_value = 0.2
    tc = _n(nt, 'ShaderNodeTexCoord'); sx = _n(nt, 'ShaderNodeSeparateXYZ'); nt.links.new(tc.outputs['Object'], sx.inputs[0])
    # cylindrical coords: angle*R and z -> two diagonal line sets
    at = _n(nt, 'ShaderNodeMath', operation='ARCTAN2'); nt.links.new(sx.outputs['Y'], at.inputs[0]); nt.links.new(sx.outputs['X'], at.inputs[1])
    s = _n(nt, 'ShaderNodeMath', operation='MULTIPLY'); s.inputs[1].default_value = 40.5; nt.links.new(at.outputs[0], s.inputs[0])
    hs = []
    for sg in (1, -1):
        a1 = _n(nt, 'ShaderNodeMath', operation='MULTIPLY_ADD'); a1.inputs[1].default_value = 0.42 * sg
        nt.links.new(s.outputs[0], a1.inputs[0]); nt.links.new(sx.outputs['Z'], a1.inputs[2])
        w = _n(nt, 'ShaderNodeTexWave'); w.wave_type = 'BANDS'; w.inputs['Scale'].default_value = 1.0
        w.inputs['Distortion'].default_value = 1.5; w.inputs['Detail'].default_value = 1.0
        cm = _n(nt, 'ShaderNodeCombineXYZ'); mm = _n(nt, 'ShaderNodeMath', operation='MULTIPLY'); mm.inputs[1].default_value = 1.9
        nt.links.new(a1.outputs[0], mm.inputs[0]); nt.links.new(mm.outputs[0], cm.inputs['X'])
        nt.links.new(cm.outputs[0], w.inputs['Vector']); hs.append(w.outputs['Fac'])
    mx = _n(nt, 'ShaderNodeMath', operation='MAXIMUM'); nt.links.new(hs[0], mx.inputs[0]); nt.links.new(hs[1], mx.inputs[1])
    bp = _n(nt, 'ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.08; bp.inputs['Distance'].default_value = 0.05
    nt.links.new(mx.outputs[0], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    return m


def mat_belt(name):
    m, new = new_mat(name)
    if not new: return m
    nt = m.node_tree; b = nt.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (0.022, 0.022, 0.025, 1); b.inputs['Roughness'].default_value = 0.62
    b.inputs['Sheen Weight'].default_value = 0.3
    tc = _n(nt, 'ShaderNodeTexCoord')
    w = _n(nt, 'ShaderNodeTexWave'); w.wave_type = 'BANDS'; w.inputs['Scale'].default_value = 0.9; w.inputs['Distortion'].default_value = 0.4
    nt.links.new(tc.outputs['Object'], w.inputs['Vector'])
    nz = _n(nt, 'ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 2.0
    nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    ad = _n(nt, 'ShaderNodeMath', operation='ADD'); nt.links.new(w.outputs['Fac'], ad.inputs[0]); nt.links.new(nz.outputs['Fac'], ad.inputs[1])
    bp = _n(nt, 'ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.12; bp.inputs['Distance'].default_value = 0.1
    nt.links.new(ad.outputs[0], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    return m


def mat_piston(name):
    """aluminium piston with graphite-coated skirt on the thrust faces (|y| large, below the ring belt)."""
    m, new = new_mat(name)
    if not new: return m
    nt = m.node_tree; b = nt.nodes['Principled BSDF']
    tc = _n(nt, 'ShaderNodeTexCoord'); sx = _n(nt, 'ShaderNodeSeparateXYZ'); nt.links.new(tc.outputs['Object'], sx.inputs[0])
    ay = _n(nt, 'ShaderNodeMath', operation='ABSOLUTE'); nt.links.new(sx.outputs['Y'], ay.inputs[0])
    m1 = _n(nt, 'ShaderNodeMapRange'); m1.inputs['From Min'].default_value = 22.0; m1.inputs['From Max'].default_value = 24.0
    nt.links.new(ay.outputs[0], m1.inputs['Value'])
    m2 = _n(nt, 'ShaderNodeMapRange'); m2.inputs['From Min'].default_value = 21.0; m2.inputs['From Max'].default_value = 19.0
    nt.links.new(sx.outputs['Z'], m2.inputs['Value'])
    m3 = _n(nt, 'ShaderNodeMapRange'); m3.inputs['From Min'].default_value = -25.5; m3.inputs['From Max'].default_value = -23.5
    nt.links.new(sx.outputs['Z'], m3.inputs['Value'])
    k = _n(nt, 'ShaderNodeMath', operation='MULTIPLY'); nt.links.new(m1.outputs['Result'], k.inputs[0]); nt.links.new(m2.outputs['Result'], k.inputs[1])
    k2 = _n(nt, 'ShaderNodeMath', operation='MULTIPLY'); nt.links.new(k.outputs[0], k2.inputs[0]); nt.links.new(m3.outputs['Result'], k2.inputs[1])
    mx = _n(nt, 'ShaderNodeMix', data_type='RGBA'); mx.inputs[6].default_value = (0.62, 0.62, 0.63, 1); mx.inputs[7].default_value = (0.05, 0.05, 0.055, 1)
    nt.links.new(k2.outputs[0], mx.inputs[0]); nt.links.new(mx.outputs[2], b.inputs['Base Color'])
    mr = _n(nt, 'ShaderNodeMapRange'); mr.inputs['To Min'].default_value = 0.28; mr.inputs['To Max'].default_value = 0.6
    nt.links.new(k2.outputs[0], mr.inputs['Value']); nt.links.new(mr.outputs['Result'], b.inputs['Roughness'])
    mm = _n(nt, 'ShaderNodeMapRange'); mm.inputs['To Min'].default_value = 1.0; mm.inputs['To Max'].default_value = 0.2
    nt.links.new(k2.outputs[0], mm.inputs['Value']); nt.links.new(mm.outputs['Result'], b.inputs['Metallic'])
    nz = _n(nt, 'ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 1.5; nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    bp = _n(nt, 'ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.08; nt.links.new(nz.outputs['Fac'], bp.inputs['Height'])
    nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    return m


def mat_glow_tip(name):
    """glow plug sheath: steel that glows orange by object property 'g' (0..1), hottest at the tip."""
    m, new = new_mat(name)
    if not new: return m
    nt = m.node_tree; b = nt.nodes['Principled BSDF']; L = nt.links
    b.inputs['Base Color'].default_value = (0.32, 0.30, 0.28, 1); b.inputs['Metallic'].default_value = 1.0; b.inputs['Roughness'].default_value = 0.35
    g = obj_attr(nt, 'g')
    tc = _n(nt, 'ShaderNodeTexCoord'); sx = _n(nt, 'ShaderNodeSeparateXYZ'); L.new(tc.outputs['Object'], sx.inputs[0])
    # object z = distance from the tip along the plug axis (mesh built along +Z from the tip)
    fall = _n(nt, 'ShaderNodeMapRange'); fall.inputs['From Min'].default_value = 3.0; fall.inputs['From Max'].default_value = 22.0
    fall.inputs['To Min'].default_value = 1.0; fall.inputs['To Max'].default_value = 0.0
    L.new(sx.outputs['Z'], fall.inputs['Value'])
    k = _n(nt, 'ShaderNodeMath', operation='MULTIPLY'); L.new(g.outputs['Fac'], k.inputs[0]); L.new(fall.outputs['Result'], k.inputs[1])
    bb = _n(nt, 'ShaderNodeBlackbody'); tmp = _n(nt, 'ShaderNodeMapRange'); tmp.inputs['To Min'].default_value = 900; tmp.inputs['To Max'].default_value = 1350
    L.new(k.outputs[0], tmp.inputs['Value']); L.new(tmp.outputs['Result'], bb.inputs['Temperature'])
    L.new(bb.outputs['Color'], b.inputs['Emission Color'])
    st = _n(nt, 'ShaderNodeMath', operation='POWER'); st.inputs[1].default_value = 2.0; L.new(k.outputs[0], st.inputs[0])
    st2 = _n(nt, 'ShaderNodeMath', operation='MULTIPLY'); st2.inputs[1].default_value = 9.0; L.new(st.outputs[0], st2.inputs[0])
    L.new(st2.outputs[0], b.inputs['Emission Strength'])
    return m


def mat_spray(name):
    """injection jets: orange (high-pressure fuel) glowing mist, denser near the axis of each jet (object z = along jet)."""
    m, new = new_mat(name)
    if not new: return m
    nt = m.node_tree; N = nt.nodes; L = nt.links
    for n in list(N):
        if n.type != 'OUTPUT_MATERIAL': N.remove(n)
    out = N['Material Output']
    lw = _n(nt, 'ShaderNodeLayerWeight'); lw.inputs['Blend'].default_value = 0.5
    inv = _n(nt, 'ShaderNodeMath', operation='SUBTRACT'); inv.inputs[0].default_value = 1.0; L.new(lw.outputs['Facing'], inv.inputs[1])
    pw = _n(nt, 'ShaderNodeMath', operation='POWER'); pw.inputs[1].default_value = 1.4; L.new(inv.outputs[0], pw.inputs[0])
    tc = _n(nt, 'ShaderNodeTexCoord'); nz = _n(nt, 'ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 0.35; nz.inputs['Detail'].default_value = 6
    L.new(tc.outputs['Object'], nz.inputs['Vector'])
    mr = _n(nt, 'ShaderNodeMapRange'); mr.inputs['From Min'].default_value = 0.35; mr.inputs['From Max'].default_value = 0.7; mr.inputs['To Min'].default_value = 0.4
    L.new(nz.outputs['Fac'], mr.inputs['Value'])
    k = _n(nt, 'ShaderNodeMath', operation='MULTIPLY'); L.new(pw.outputs[0], k.inputs[0]); L.new(mr.outputs['Result'], k.inputs[1])
    a = obj_attr(nt, 'a')
    ka = _n(nt, 'ShaderNodeMath', operation='MULTIPLY'); L.new(k.outputs[0], ka.inputs[0]); L.new(a.outputs['Fac'], ka.inputs[1])
    em = _n(nt, 'ShaderNodeEmission'); em.inputs['Color'].default_value = (*HP_ORANGE, 1); em.inputs['Strength'].default_value = 4.0
    tr = _n(nt, 'ShaderNodeBsdfTransparent'); ms = _n(nt, 'ShaderNodeMixShader')
    L.new(ka.outputs[0], ms.inputs[0]); L.new(tr.outputs[0], ms.inputs[1]); L.new(em.outputs[0], ms.inputs[2])
    L.new(ms.outputs[0], out.inputs['Surface'])
    return m


def mat_emit_dot(name, col, strength=4.0):
    m, new = new_mat(name)
    if not new: return m
    nt = m.node_tree; N = nt.nodes; L = nt.links
    for n in list(N):
        if n.type != 'OUTPUT_MATERIAL': N.remove(n)
    em = _n(nt, 'ShaderNodeEmission'); em.inputs['Color'].default_value = (*col, 1); em.inputs['Strength'].default_value = strength
    L.new(em.outputs[0], N['Material Output'].inputs['Surface'])
    return m


def build():
    if M: return M
    sec = lambda n, c, l, a, p, ax='Y': mat_section(n, c, l, a, p, axis=ax)
    M.update(
        iron=mat_metal('cast_iron', (0.13, 0.135, 0.14), 0.6, metal=0.8, bump=(0.9, 0.35, 0.2)),
        iron_sec=sec('sec_iron', (0.20, 0.205, 0.215), (0.085, 0.09, 0.10), 45, 3.0),
        iron_secX=sec('sec_ironX', (0.20, 0.205, 0.215), (0.085, 0.09, 0.10), 45, 3.0, 'X'),
        alu=mat_metal('cast_alu', (0.50, 0.51, 0.53), 0.42, metal=1.0, bump=(1.6, 0.18, 0.12)),
        alu_sec=sec('sec_alu', (0.33, 0.34, 0.36), (0.15, 0.155, 0.17), -45, 2.4),
        alu_secX=sec('sec_aluX', (0.33, 0.34, 0.36), (0.15, 0.155, 0.17), -45, 2.4, 'X'),
        bore=mat_bore('bore_honed'),
        steel=mat_metal('steel_machined', (0.60, 0.61, 0.63), 0.2, aniso=0.35),
        steel_sec=sec('sec_steel', (0.36, 0.37, 0.40), (0.15, 0.16, 0.18), 30, 1.6),
        steel_secX=sec('sec_steelX', (0.36, 0.37, 0.40), (0.15, 0.16, 0.18), 30, 1.6, 'X'),
        mov_sec=sec('sec_moving', (0.62, 0.63, 0.66), (0.40, 0.41, 0.44), 60, 2.2),
        mov_secX=sec('sec_movingX', (0.62, 0.63, 0.66), (0.40, 0.41, 0.44), 60, 2.2, 'X'),
        forged=mat_metal('steel_forged', (0.30, 0.31, 0.33), 0.42, bump=(1.2, 0.2, 0.15)),
        piston=mat_piston('piston_alu'),
        piston_sec=sec('sec_piston', (0.40, 0.40, 0.42), (0.18, 0.18, 0.2), -30, 1.8),
        piston_secX=sec('sec_pistonX', (0.40, 0.40, 0.42), (0.18, 0.18, 0.2), -30, 1.8, 'X'),
        ring=mat_metal('ring_steel', (0.18, 0.18, 0.19), 0.3),
        shell=mat_metal('bearing_shell', (0.78, 0.50, 0.30), 0.3),
        valve=mat_metal('valve_steel', (0.55, 0.555, 0.57), 0.24),
        valve_hot=mat_metal('valve_exh', (0.33, 0.27, 0.21), 0.4),
        spring=mat_metal('spring_black', (0.035, 0.035, 0.04), 0.32, metal=0.9),
        follower=mat_metal('follower_steel', (0.52, 0.53, 0.55), 0.3),
        belt=mat_belt('belt_rubber'),
        pulley=mat_metal('pulley_steel', (0.30, 0.31, 0.33), 0.32),
        pulley_black=mat_metal('pulley_black', (0.06, 0.06, 0.065), 0.38),
        plastic=mat_plastic('plastic_black', (0.028, 0.03, 0.033), 0.48, bump=(2.5, 0.05)),
        plastic_sec=sec('sec_plastic', (0.08, 0.08, 0.09), (0.03, 0.03, 0.035), 45, 1.6),
        plastic_secX=sec('sec_plasticX', (0.08, 0.08, 0.09), (0.03, 0.03, 0.035), 45, 1.6, 'X'),
        gasket=mat_metal('gasket_mls', (0.45, 0.45, 0.47), 0.32),
        pan=mat_metal('pan_black', (0.05, 0.05, 0.055), 0.42, metal=0.6, bump=(0.5, 0.1)),
        pan_sec=sec('sec_pan', (0.16, 0.16, 0.17), (0.07, 0.07, 0.08), 45, 1.5),
        pan_secX=sec('sec_panX', (0.16, 0.16, 0.17), (0.07, 0.07, 0.08), 45, 1.5, 'X'),
        rail=mat_metal('rail_forged', (0.34, 0.35, 0.37), 0.4, bump=(1.0, 0.15)),
        rail_sec=sec('sec_rail', (0.30, 0.31, 0.33), (0.13, 0.14, 0.16), 45, 1.4),
        line=mat_metal('hp_line', (0.62, 0.63, 0.66), 0.22),
        zinc=mat_metal('zinc_bolt', (0.66, 0.65, 0.58), 0.34),
        bolt=mat_metal('bolt_black', (0.08, 0.08, 0.085), 0.4),
        inj_body=mat_metal('inj_steel', (0.70, 0.72, 0.75), 0.30),
        inj_nut=mat_metal('inj_nut', (0.64, 0.66, 0.70), 0.26),
        copper=mat_metal('copper', (0.90, 0.48, 0.30), 0.30),
        glow=mat_glow_tip('glow_sheath'),
        gp_body=mat_metal('gp_body', (0.62, 0.62, 0.60), 0.3),
        fuel_lp=mat_glow_fluid('fuel_lp', LP_BLUE, HP_ORANGE, emit=0.75, alpha=0.95),
        fuel_hp=mat_glow_fluid('fuel_hp', HP_ORANGE, HP_ORANGE, emit=0.75, alpha=0.95),
        fuel_var=mat_glow_fluid('fuel_var', LP_BLUE, HP_ORANGE, emit=0.75, alpha=0.95),
        oil=mat_glow_fluid('oil', OIL_A, OIL_B, emit=0.6, alpha=0.93),
        gas=mat_gas('gas', 1.0),
        spray=mat_spray('spray'),
        dot_oil=mat_emit_dot('dot_oil', srgb(0xffe08a), 3.0),
        dot_lp=mat_emit_dot('dot_lp', srgb(0x9fd0ff), 3.0),
        dot_hp=mat_emit_dot('dot_hp', srgb(0xffc0a0), 3.0),
        sensor=mat_plastic('sensor_grey', (0.12, 0.12, 0.13), 0.4),
    )
    return M
