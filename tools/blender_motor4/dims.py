"""Dimensions (mm) and timing of the 4-cylinder common-rail diesel (architecture of the VW 2.0 TDI CR, EA189/EA288 family).
Sources: VW SSP 403 (2.0 TDI CR: CP4.1 single-piston pump driven by the toothed belt at engine speed, two cams offset 180 deg,
up to 1800 bar; injector vertical and central over the piston bowl; roller cam followers with hydraulic lash adjusters;
camshafts linked by spur gears, belt drives the exhaust camshaft), VW SSP 820433 / 514 (EA288: bore 81, stroke 95.5,
vane oil pump with eccentric ring, steel glow plugs > 1000 C in 2 s). Proportions not published by VW are reconstructed.
"""
import math

BORE = 81.0; RB = BORE / 2
STROKE = 95.5; RC = STROKE / 2          # crank radius 47.75
ROD = 144.0                             # con-rod centre distance
CH = 47.9                               # piston compression height (pin centre -> crown)
PITCH = 88.0
CX = [-132.0, -44.0, 44.0, 132.0]       # cylinder axes (cyl 1 at the belt end, -X)
MAINS = [-176.0, -88.0, 0.0, 88.0, 176.0]
Z_BD = 239.0                            # block deck
GASKET = 1.6
Z_HD = Z_BD + GASKET                    # head deck (fire face) 240.6
SKIRT = 27.0                            # piston skirt below the pin centre

# crank throws: +1 = rod journal at local +Z when theta = 0 (cyl 1 & 4), -1 = cyl 2 & 3
THROW = [1, -1, -1, 1]
FIRE = {0: 0.0, 2: 180.0, 3: 360.0, 1: 540.0}   # firing order 1-3-4-2 (0-based index -> crank angle of firing TDC)

# block / head extents
X_BF, X_BR = -222.0, 205.0              # block front / rear faces
X_HF, X_HR = -215.0, 200.0              # head
Y_BU = 70.0                             # block upper half-width
Y_BL = 104.0                            # crankcase half-width
Z_PAN = -55.0                           # pan rail
Z_PANB = -150.0                         # pan bottom
Y_H = 76.0                              # head half-width

# valves (vertical), per cylinder: intake at y=-18, exhaust at y=+18, x = cx +- 16.5
VX = 16.5
VY = 18.0
R_VI, R_VE = 14.0, 13.0                 # valve head radii
R_STEM = 3.0
V_LEN = 92.0                            # face -> tip
V_REC = 0.7                             # valve face recess into the head
Z_VFACE = Z_HD + V_REC                  # 241.3
Z_VTIP = Z_VFACE + V_LEN                # 333.3
Z_SSEAT = Z_HD + 45.0                   # spring seat (floor of the valve chamber) 285.6
SPR_LEN = 34.0                          # installed spring length
Z_RET = Z_SSEAT + SPR_LEN               # retainer underside 319.6
LIFT_I, LIFT_E = 9.0, 8.6

# roller finger followers: pivot ball on the HLA at |y| = 64, roller at |y| = 38 (under the cam), valve pad at |y| = 18
Y_HLA = 64.0
Y_CAM = 38.0
Z_PIV = Z_VTIP + 2.7                    # pivot (ball centre) 336.0
R_ROLL = 8.0
Z_ROLL = Z_VTIP + 8.2                   # roller centre at zero lift 341.5
R_BASE = 17.0                           # cam base circle
Z_CAM = Z_ROLL + R_ROLL + R_BASE        # 366.5
R_JOUR = 14.0                           # cam journal

# timing (cycle phase c in degrees: 0 = firing TDC)
IVO, IVC = 355.0, 575.0
EVO, EVC = 140.0, 365.0

# injector (Bosch CRI2 profile, tip 2.5 mm below the fire face, HP inlet pointing -X)
Z_TIP = Z_HD - 2.5                      # 238.1
Z_INLET = Z_TIP + 96.0                  # 334.1
X_RISER = -30.0                         # HP riser offset from the cylinder axis (along X)

# glow plug: tip near the nozzle on the intake side, 25 deg from vertical in the y-z plane
GP_TIP = (0.0, -10.5, Z_HD - 3.6)
GP_ANG = math.radians(25.0)
GP_DIR = (0.0, -math.sin(GP_ANG), math.cos(GP_ANG))

# timing belt (plane x = X_BELT), pitch 9.525 mm
X_BELT = -240.0
BELT_P = 9.525
BELT_W = 25.0
N_CRANK, N_CAM, N_HPP, N_WP = 22, 44, 22, 19
Y_HPP, Z_HPP = -112.0, 210.0            # HP pump shaft (y, z)
Y_WP, Z_WP = 96.0, 122.0                # coolant pump
X_DAMP = -272.0                         # crankshaft damper pulley

# cam gears (couple exhaust -> intake), module 2, 38 teeth
X_GEAR = -200.0
N_GEAR = 38

# oil pump (vane pump), chain driven 1:1 from the crankshaft
X_CHAIN = -205.0
CHAIN_P = 8.0
N_CHS = 18                              # sprocket teeth (both)
Z_OP = -92.0                            # oil pump shaft (y=0)
X_OPR = -183.0                          # rotor mid-plane

# HP pump (CP4.1) cam plane
X_HPC = -183.0

# rail
Z_RAIL = 430.0
R_RAIL = 12.0


def cyc(theta, i):
    """cycle phase (deg, 0..720) of cylinder i at crank angle theta"""
    return (theta - FIRE[i]) % 720.0


def piston_z(theta, i):
    a = math.radians(theta + (0.0 if THROW[i] > 0 else 180.0))
    s = RC * math.sin(a)
    return RC * math.cos(a) + math.sqrt(ROD * ROD - s * s)


def crankpin(theta, i):
    a = math.radians(theta + (0.0 if THROW[i] > 0 else 180.0))
    return (-RC * math.sin(a), RC * math.cos(a))   # (y, z)


def bump(u):
    if u <= 0.0 or u >= 1.0: return 0.0
    return math.sin(math.pi * u) ** 2


def valve_lift(c, kind):
    if kind == 'I':
        c2 = c if c >= IVO - 1 else c + 720
        return LIFT_I * bump((c2 - IVO) / (IVC - IVO))
    c2 = c
    return LIFT_E * bump((c2 - EVO) / (EVC - EVO))

X_FRONT = -183.0                        # front section plane (HP pump cam + oil pump rotor)
X_T = CX[1] - VX                        # transverse section through the front valves of cylinder 2
