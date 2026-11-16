# Definitiile filmului folosite si de Blender (cadre) si de montaj: camere, stari ale pieselor, lista de cadre.
import os, json, math
import numpy as np
import layout as L

HERE = os.path.dirname(os.path.abspath(__file__))
META = json.load(open(os.path.join(HERE, 'out', 'meta.json')))
FPS = 30; W, H = 1080, 1920
C0 = np.array([-45.0, -150.0, 105.0])
def orb(a_deg, R=1560.0, h=420.0):
    a = math.radians(a_deg); return C0 + np.array([R * math.sin(a), -R * math.cos(a), h])
CH = np.array([0.50, -0.87, 0.0])
HC = np.array(META['misc']['hose_crack_pos']); HD = np.array(META['misc']['hose_crack_dir'])
ORB_A0, ORB_A1 = -20.0, 24.0

CAMS = {
    'heroB':  dict(pos=orb(24), tgt=C0, lens=35, fstop=8, focus=(-60, -240, 120)),
    'route':  dict(pos=(300, -1560, 330), tgt=(10, -240, 60), lens=40, fstop=8, focus=(-60, -240, 100)),
    'routeC': dict(pos=(470, -1320, 400), tgt=(35, -245, 105), lens=50, fstop=8, focus=(40, -250, 120)),
    'dpf':    dict(pos=L.mw(0, 0, 200) + CH * 700 + np.array([0, 0, 110.0]), tgt=L.mw(8, 8, 200), lens=50, fstop=16),
    'dps':    dict(pos=(-622, -1368, 178), tgt=(-215, -250, 93), lens=33, fstop=11, focus=(-250, -250, 150)),
    'dpsC':   dict(pos=HC + HD * 300 + np.array([60.0, 0, 40.0]), tgt=HC + np.array([0, 0, 15.0]), lens=70, fstop=16),
    'cool':   dict(pos=(80, -800, 100), tgt=(-45, -252, 14), lens=60, fstop=16, focus=(-52, -285, 14)),
    'egrvB':  dict(pos=(380, -760, 330), tgt=(175, -238, 228), lens=70, fstop=11),
    'exfG':   dict(pos=(200, -1050, 20), tgt=(-170, -440, -170), lens=60, fstop=11, focus=(-183, -500, -205)),
    'sec':    dict(pos=(1080, -90, 330), tgt=(132, 0, 245), lens=50, fstop=16),
    'inj':    dict(pos=(640, -40, 300), tgt=(132, 0, 262), lens=70, fstop=16),
    'turboG': dict(pos=(-40, -760, 400), tgt=(45, -212, 255), lens=60, fstop=11),
    'mafG':   dict(pos=(700, -760, 420), tgt=(255, -240, 315), lens=60, fstop=11),
}
G3 = ('exh', 'egr', 'int')
STATES = {
    'solid':   dict(),
    'ghost':   dict(ghost=G3),
    'ghostNR': dict(ghost=G3, no_rotor=True),
    'soot0':   dict(soot=0.0),
    'sootM':   dict(soot=0.5),
    'soot1':   dict(soot=0.85),
    'glaze':   dict(soot=0.5, glaze=1.0, glazeTop=True),
    'ash':     dict(soot=0.5, ash=1.0),
    'regen':   dict(soot=0.85, glow=2.6),
    'regen2':  dict(soot=0.85, glow=2.2, glow_col=(1.0, 0.06, 0.002)),
    'crack':   dict(dps_crack=True),
    'ecrack':  dict(egr_crack=True),
    'vclosed': dict(ghost=('egr', 'int'), egrv=8),
    'vopen':   dict(ghost=('egr', 'int'), egrv=62),
    'exfG':    dict(ghost=('exh',), exf=28),
    'noeng':   dict(no_eng=True),
    'gint':    dict(ghost=('int',)),
    'gexh':    dict(ghost=('exh',)),
    'gturbo':  dict(ghost=('exh', 'int'), no_rotor=True),
}
# (camera, stare) in ordinea in care se randeaza
PLATES = [
    ('route', 'ghostNR'), ('route', 'solid'), ('dpf', 'soot1'), ('routeC', 'ghostNR'), ('heroB', 'solid'),
    ('dps', 'gexh'), ('dpf', 'soot0'), ('dpsC', 'solid'), ('dpsC', 'crack'), ('cool', 'solid'), ('cool', 'ecrack'),
    ('egrvB', 'vclosed'), ('egrvB', 'vopen'), ('inj', 'noeng'), ('dpf', 'sootM'), ('dpf', 'glaze'), ('dpf', 'ash'), ('dpf', 'regen2'),
    ('sec', 'noeng'), ('turboG', 'gturbo'), ('mafG', 'gint'),
]
# straturi in bucla: piesele in miscare randate separat (restul = masca)
LOOPS = [
    dict(cam='route', state='ghostNR', kind='rotor', n=12),
    dict(cam='inj', state='noeng', kind='engine', n=60),
    dict(cam='routeC', state='ghostNR', kind='rotor', n=12),
    dict(cam='sec', state='noeng', kind='engine', n=60),
    dict(cam='turboG', state='gturbo', kind='rotor', n=12),
]
ORBIT_N = 150
