"""draw all labels of one shot on a given rendered frame (layout check)"""
import sys; sys.path.insert(0, '/home/claude/m4/comp')
import comp, skia
from fk import *
shot, k, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
surf = skia.Surface(W, H); c = surf.getCanvas()
comp.background(c, 0.2); comp.draw_frame(c, shot, k); comp.vignette(c); comp.header(c)
for (text, key, (lx, ly), side, tin) in comp.LABELS[shot]:
    ax, ay = comp.project(shot, comp.WA[key]); comp.label(c, text, ax, ay, lx, ly, 1.0, side, size=27)
t, b = comp.CAPS[shot]; comp.caption(c, t, b, 1.0); comp.legend(c, comp.LEG[shot], 1.0)
img = surf.makeImageSnapshot()
img.save(out, skia.kPNG)
