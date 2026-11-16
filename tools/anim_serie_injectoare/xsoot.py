# Calamina din putul injectorului (ep5), ca piesa sectionata: inel de revolutie fara pana din fata (WEDGE 120).
# Se ruleaza din iplate (cheia 'fn' a starii): LEVEL = 1 (strat subtire) sau 2 (putul plin, injectorul prins).
import math
WEDGE = 120.0; A0 = -90.0 + WEDGE / 2
if bpy.data.materials.get('secCarbon') is None: imats.sec('secCarbon', 0x4a4139, 1.6, 1.0, 0.4)
if bpy.data.materials.get('carbonX') is None: imats.metal('carbonX', 0x312a23, 0.9, metal=0.0, bump=(9, 1.2))
PROF = {1: [(4.75, 25.22), (9.38, 25.22), (9.38, 35.5), (8.97, 34.6), (8.97, 26.3), (4.75, 26.3)],
        2: [(4.75, 25.22), (9.38, 25.22), (9.38, 54.0), (8.62, 52.4), (8.62, 29.2), (6.42, 27.02), (4.75, 27.02)]}
nm = 'x_soot%d' % LEVEL
o = bpy.data.objects.get(nm)
if o is None:
    o = K.lathe(nm, PROF[LEVEL], seg=96, mat=[bpy.data.materials['carbonX'], bpy.data.materials['secCarbon']], sharp=40,
                closed=True, deg=360.0 - WEDGE, a0=A0)
    me = o.data; aR = math.radians(A0); aL = math.radians(A0 + 360.0 - WEDGE)
    nR = np.array([-math.sin(aR), math.cos(aR), 0.0]); nL = np.array([-math.sin(aL), math.cos(aL), 0.0])
    for p in me.polygons:
        n = np.array(p.normal[:])
        if abs(n @ nR) > 0.98 or abs(n @ nL) > 0.98: p.material_index = 1
    me.update()
o.hide_render = False
