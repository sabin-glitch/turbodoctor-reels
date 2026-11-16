# hasura in linii drepte pentru piese plane (din micro.py)
import imats as IM

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

