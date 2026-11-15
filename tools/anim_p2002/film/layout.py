# Asezarea ansamblului (mm). X = axa arborelui cotit (+X spre distributie), -Y = spatele motorului (evacuare), Z = sus.
import numpy as np, math

def nrm(v):
    v = np.asarray(v, np.float64); return v / np.linalg.norm(v)

def rot_about(v, axis, ang):
    v = np.asarray(v, np.float64); k = nrm(axis)
    return v * math.cos(ang) + np.cross(k, v) * math.sin(ang) + k * (k @ v) * (1 - math.cos(ang))

# ---------------- motor
CYL_X = [132.0, 44.0, -44.0, -132.0]     # cilindrii 1..4
BORE = 81.0; STROKE = 95.5; ROD = 144.0; DECK = 237.0; COMP_H = 45.0
SEC_X = 132.0                              # planul sectiunii (prin axa cilindrului 1)
HEAD_TOP = 372.0; COVER_TOP = 428.0
BLOCK_Y = 108.0                            # semilatimea blocului in zona cilindrilor
HEAD_Y = 116.0
PORT_Z = 302.0                             # inaltimea portilor de evacuare / admisie pe chiulasa

# ---------------- turbosuflanta (axa paralela cu arborele cotit)
TURBO_Y = -212.0; TURBO_Z = 266.0
TURB_X = 4.0          # centrul rotorului de turbina
COMP_X = 104.0        # centrul rotorului de compresor
TURB_OUT_X = -46.0    # flansa de iesire din turbina (spre -X)
COMP_IN_X = 146.0     # gura compresorului (spre +X)

# ---------------- modulul catalizator + filtru de particule
M0 = np.array([-158.0, -226.0, 214.0])               # centrul fetei de intrare in carcasa (sus)
MD = nrm([-0.10, -0.045, -1.0])                      # directia de curgere (in jos, usor inclinata)
_CH = np.array([0.50, -0.87, 0.0]); _CH = nrm(_CH - MD * (_CH @ MD))   # spre camera: bisectoarea ferestrei taiate
MX = nrm(rot_about(_CH, MD, -math.pi / 4)); MY = np.cross(MD, MX)
def mw(x, y, z):
    """reper local al modulului (x, y in sectiune, z de-a lungul curgerii) -> reperul ansamblului"""
    return M0 + MX * x + MY * y + MD * z
def mpol(r, phi_deg, z):
    a = math.radians(phi_deg); return mw(r * math.cos(a), r * math.sin(a), z)
def mdir(phi_deg):
    a = math.radians(phi_deg); return MX * math.cos(a) + MY * math.sin(a)

CAT_R = 67.0; CAT_Z0 = 8.0; CAT_Z1 = 86.0; CAT_P = 3.6; CAT_W = 0.45
DPF_R = 73.0; DPF_Z0 = 118.0; DPF_Z1 = 284.0; DPF_P = 6.0; DPF_W = 1.1; DPF_PLUG = 9.0
SHELL_R1 = 72.0; SHELL_R2 = 79.5; SHELL_T = 1.6
MOD_END = 298.0

# ---------------- racitorul EGR (joasa presiune) - cutie verticala langa filtru
COOL_C = np.array([-52.0, -252.0, 14.0]); COOL_S = np.array([58.0, 84.0, 150.0])
COOL_TUBE_R = 4.6; COOL_PITCH = 13.0

# ---------------- senzorul de presiune diferentiala
DPS = np.array([-262.0, -208.0, 318.0])

def piston_z(theta):
    """inaltimea boltului pistonului fata de axa arborelui (theta = unghi maneton fata de PMS)"""
    r = STROKE / 2
    return r * math.cos(theta) + math.sqrt(ROD * ROD - (r * math.sin(theta)) ** 2)
