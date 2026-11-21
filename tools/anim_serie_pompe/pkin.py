# Cinematica pompei CP4 (aceeasi ca in animatia three.js / proba Blender): cama dubla, tachet cu rola, piston, supape.
# Reperul pieselor e cel al animatiei three.js (mm, Y in sus, arborele pe Z); in Blender stau sub empty-ul CP4 (rotit 90 de grade pe X).
import math
import numpy as np

Rb, LIFT, RRr = 14.5, 6.5, 5.5
NT = 360
_aa = np.linspace(0, 2 * np.pi, 1440, endpoint=False)
_camR = Rb + LIFT * (0.5 + 0.5 * np.cos(2 * _aa))
hPar = np.zeros(NT + 1); hCross = np.zeros(NT + 1)
for _i in range(NT + 1):
    _ph = _i / NT * math.pi; _px = _camR * np.cos(_aa + _ph); _py = _camR * np.sin(_aa + _ph)
    _m = np.abs(_px) < RRr; hPar[_i] = np.max(_py[_m] + np.sqrt(RRr * RRr - _px[_m] ** 2)); hCross[_i] = _py.max() + RRr
HA, HB = 18.0, 40.0

def look(tb, ph):
    u = (ph / math.pi) % 1.0; x = u * NT; i = int(math.floor(x)); f = x - i
    return float(tb[i] * (1 - f) + tb[min(NT, i + 1)] * f)

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))

def state(phi, rot=0.0):
    """phi = unghiul arborelui (rad, perioada pi); rot = 0..1 tachetul rotit pana la 90 de grade.
    Intoarce h (inaltimea tachetului, mm), up (-1..1: coboara / urca), press (0..1)."""
    h = look(hPar, phi) * (1 - rot) + look(hCross, phi) * rot
    v = look(hPar, phi + 0.02) - look(hPar, phi - 0.02); up = clamp(v * 4, -1, 1)
    return dict(h=h, up=up, press=clamp(up * 1.5))

def W3(p):
    """punct din reperul pompei (three.js) -> reperul scenei Blender in mm (Z in sus)"""
    return (p[0], -p[2], p[1])
