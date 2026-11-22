"""Illustrative effects: cylinder gases (fresh air / flame / exhaust), injection jets, port gases.
Colours follow the project convention: high-pressure fuel orange, fresh air pale blue, burnt gas grey-brown."""
import math, bpy
from mathutils import Vector, Matrix
from lib import *
from dims import *
import mats
from parts_core import BOWL
import parts_head as ph


def build_gas(i):
    """unit-height column (z 0..1) at the cylinder axis: located at the piston crown, scaled to the head deck."""
    g = cyl(f'gas{i}', (0, 0, 0), (0, 0, 1.0), RB - 0.35, segs=96)
    g.location = (CX[i], 0, 0)
    set_mats(g, mats.M['gas'])
    for k, v in (('e', 0.0), ('a', 0.0)): g[k] = v
    g['col'] = [0.6, 0.8, 1.0]
    # bowl volume (moves with the piston; local origin = piston pin centre)
    prof = [(0.0, BOWL[0][1] + 0.3)] + [(max(0.0, r - 0.3), z + 0.3) for r, z in BOWL[1:-1]] + [(BOWL[-1][0] - 0.3, CH + 0.05), (0.0, CH + 0.05)]
    b = revolve(f'gasbowl{i}', prof, segs=64)
    b.location = (CX[i], 0, 0)
    set_mats(b, mats.M['gas'])
    for k, v in (('e', 0.0), ('a', 0.0)): b[k] = v
    b['col'] = [0.6, 0.8, 1.0]
    return g, b


def build_spray(i):
    """8 jets with apex at the nozzle tip (object origin), unit length along each hole direction; scaled = jet length."""
    jets = []
    for k in range(8):
        a = TAU * k / 8
        d = Vector((math.sin(math.radians(75)) * math.cos(a), math.sin(math.radians(75)) * math.sin(a), -math.cos(math.radians(75))))
        c = cyl('jet', d * 0.02, d * 1.0, 0.012, r1=0.115, segs=20)
        jets.append(c)
    sp = union(jets, f'spray{i}')
    set_mats(sp, mats.M['spray'])
    sp['a'] = 0.0
    sp.location = (CX[i], 0, Z_TIP + 0.6)
    sp.scale = (0.001, 0.001, 0.001)
    return sp


def build_port_gas():
    out = []
    for (i, kind, x, y) in ph.valves():
        sy = -1 if kind == 'I' else 1
        pp = ph.port_path(x, sy)
        rr = [r - 0.4 for r in ph.port_radii(len(pp) - 1)]
        keep = [k for k, p in enumerate(pp) if abs(p.y) < Y_H - 1.5]
        g = tube(f'pgas_{kind}{i}_{x:.0f}', [pp[k] for k in keep[1:]], [rr[k] for k in keep[1:]], segs=40)
        set_mats(g, mats.M['gas'])
        g['e'] = 0.0; g['a'] = 0.0; g['col'] = [0.6, 0.8, 1.0]
        g['cyl'] = i; g['kind'] = kind
        out.append(g)
    return out


# ------------------------------------------------------------------ gas state as a function of the cycle phase
AIR = (0.55, 0.78, 1.0)
HOT_AIR = (0.95, 0.85, 0.80)
FLAME = (1.0, 0.76, 0.30)
FLAME2 = (1.0, 0.40, 0.09)
EXH = (0.42, 0.36, 0.32)


def smooth(x):
    x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)


def lerp3(a, b, t):
    return tuple(a[k] + (b[k] - a[k]) * t for k in range(3))


def gas_state(c):
    """returns (rgb, emission, alpha) for cylinder phase c (deg)"""
    # unwrap so that compression -> ignition -> power is continuous: use d = c in (-180, 540]
    d = c if c < 540 else c - 720          # -180..540; 0 = firing TDC
    if -180 <= d < 2:                      # compression: air heats slightly (pilot flame flicker near -12)
        t = smooth((d + 180) / 182)
        pil = 0.9 * max(0.0, 1 - abs(d + 11) / 6.0)
        return lerp3(lerp3(AIR, HOT_AIR, t * 0.6), FLAME, pil * 0.6), 0.22 + 0.12 * t + pil, 0.16 + 0.08 * t
    if 2 <= d < 25:                        # ignition after the delay -> flame fills the bowl and the chamber
        t = smooth((d - 2) / 14)
        col = lerp3(HOT_AIR, FLAME, t)
        e = 0.34 + 5.5 * t
        a = 0.24 + 0.46 * t
        return col, e, a
    if 25 <= d < 140:                      # expansion: flame fades to dull red
        t = smooth((d - 25) / 115)
        return lerp3(FLAME, FLAME2, t), 5.84 * (1 - t) ** 1.6 + 0.25, 0.70 - 0.28 * t
    if 140 <= d < 365:                     # exhaust: burnt gas pushed out
        t = smooth((d - 140) / 225)
        return lerp3(FLAME2, EXH, smooth((d - 140) / 50)), 0.25 * (1 - smooth((d - 140) / 70)) + 0.05, 0.42 - 0.30 * t
    # intake (365..540): fresh air fills
    t = smooth((d - 355) / 120)
    return lerp3(EXH, AIR, smooth((d - 360) / 60)), 0.05 + 0.17 * t, 0.12 + 0.04 * t


def spray_state(c):
    """(length mm, alpha) of the jets: pilot injection + main injection"""
    d = c if c < 540 else c - 720
    L, a = 0.0, 0.0
    if -22 <= d < -14:                     # pilot
        t = (d + 22) / 8
        L = 7.0 * smooth(t * 2.2); a = 0.9 * (1 - smooth((t - 0.6) / 0.4))
    if -6 <= d < 18:                       # main
        t = (d + 6) / 24
        L = 24.0 * smooth(t * 2.6); a = 1.0 * (1 - smooth((t - 0.72) / 0.28))
    return L, a


def port_state(kind, c):
    """intake port: air flows when the intake valve is open; exhaust port: hot gas when the exhaust valve is open."""
    if kind == 'I':
        lift = valve_lift(c, 'I') / LIFT_I
        return AIR, 0.18 + 0.25 * lift, 0.22 + 0.25 * lift
    lift = valve_lift(c, 'E') / LIFT_E
    d = c
    hot = smooth(1 - (d - 140) / 160) if 140 <= d < 300 else 0.0
    col = lerp3(EXH, FLAME2, hot * 0.8)
    return col, 0.06 + 1.6 * hot * lift, 0.10 + 0.40 * lift
