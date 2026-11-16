# Camerele si starile placilor pentru seria injectoarelor (comun pentru Blender si pentru montaj). Unitati: mm, grade.
W, H = 1080, 1920
INJ = '/home/claude/w/inj/out/'
MIC = '/home/claude/w/serinj/blend/'

# cam: blend, tinta, azimut, elevatie, distanta, obiectiv; ls = scara luminilor (1 = injectorul intreg); hide = obiecte / grupuri ascunse
CAMS = {
    'hero':    dict(blend='inj_cut', tgt=(0, 0, 95), az=18, el=5, dist=700, lens=70, ls=1.0, hide=['ENGINE', 'PISTON']),
    'upper':   dict(blend='inj_cut', tgt=(0, 0, 138), az=12, el=8, dist=260, lens=70, ls=0.45, hide=['ENGINE', 'PISTON']),
    'valve':   dict(blend='inj_cut', tgt=(0, 0, 139.5), az=6, el=9, dist=78, lens=70, ls=0.2, hide=['ENGINE', 'PISTON']),
    'seat':    dict(blend='inj_dmg', tgt=(0, 0, 136.9), az=4, el=7, dist=15, lens=70, ls=0.06, hide=['ENGINE', 'PISTON']),
    'needle':  dict(blend='inj_cut', tgt=(0, 0, 20), az=8, el=6, dist=150, lens=70, ls=0.3, hide=['ENGINE', 'PISTON']),
    'tip':     dict(blend='inj_cut', tgt=(0, 0, 3.0), az=5, el=4, dist=38, lens=70, ls=0.08, hide=['ENGINE', 'PISTON']),
    'tipw':    dict(blend='inj_cut', tgt=(0, 0, 10.0), az=5, el=5, dist=150, lens=70, ls=0.15, hide=['ENGINE', 'PISTON']),
    'seattop': dict(blend='inj_dmg', tgt=(0, 0, 136.72), az=0, el=58, dist=8.5, lens=70, ls=0.05,
                    hide=['ENGINE', 'PISTON', 'ARM', 'BALL', 'FUEL_LP', 'f_cc', 'screw', 'core', 'coil', 'bobbin', 'magnut', 'cap', 'connbox', 'vspring', 'NEEDLE']),
    'chamber': dict(blend='inj_cut', tgt=(0, 0, 4), az=10, el=12, dist=380, lens=55, ls=0.5, hide=[]),
    'chamberz': dict(blend='inj_cut', tgt=(0, 0, -3.5), az=10, el=16, dist=120, lens=55, ls=0.25, hide=[]),
    'micro':   dict(blend='micro', tgt=(0, 0, 8), az=0, el=5, dist=600, lens=70, ls=0.6, hide=[]),
    'microz':  dict(blend='micro', tgt=(0, 0, 0), az=0, el=4, dist=300, lens=70, ls=0.4, hide=[]),
    'microf':  dict(blend='micro', tgt=(0, 0, 0), az=0, el=4, dist=110, lens=70, ls=0.4, hide=['m_hair']),
    'well':    dict(blend='inj_cut', tgt=(0, 0, 33), az=10, el=8, dist=240, lens=70, ls=0.45, hide=['PISTON']),
    'tank':    dict(blend='tank', tgt=(0, 60, 128), az=0, el=14, dist=3350, lens=70, ls=3.4, hide=[]),
    'filter':  dict(blend='filter', tgt=(0, 0, 80), az=0, el=9, dist=560, lens=70, ls=1.0, hide=[]),
}
# stari: lift = (ac, bila/armatura) mm; cover = {material: acoperire 0..1} (pielea respectiva devine vizibila); show/hide = obiecte
STATES = {
    'shut':   dict(lift=(0.0, 0.0)),
    'open':   dict(lift=(0.3, 0.32), liq={'fuelCC': 0xffc02a}),
    'vopen':  dict(lift=(0.0, 0.32), liq={'fuelCC': 0xffc02a}),
    'full':   dict(blend='inj_full'),
    'clean':  dict(blend='inj_dmg'),
    'pits':   dict(blend='inj_dmg', hide=['valve'], show=['valve_pits']),
    'chan':   dict(blend='inj_dmg', hide=['valve'], show=['valve_chan']),
    'tclean': dict(blend='inj_dmg', show=['f_cc_low']),
    'tpits':  dict(blend='inj_dmg', hide=['valve'], show=['valve_pits', 'f_cc_low']),
    'tchan':  dict(blend='inj_dmg', hide=['valve'], show=['valve_chan', 'f_cc_low']),
    'worn':   dict(lift=(0.3, 0.32), cover={'eroded': 0.6}),
    'fdirty': dict(show=['f_dirt'], cover={'dirt': 0.92}),
    'mhair':   dict(),
    'mclean':  dict(hide=['m_hair']),
    'mscored': dict(hide=['m_hair'], show=['dm_scL', 'dm_scR']),
    'mrust1':  dict(hide=['m_hair'], show=['m_rustL1', 'm_rustR1']),
    'mrust2':  dict(hide=['m_hair', 'm_fuel'], show=['m_rustL2', 'm_rustR2']),
    'mwater':  dict(hide=['m_hair', 'm_fuel'], show=['m_water']),
    'nrust':   dict(cover={'rust': 0.5}),
    'fwlo':    dict(wlevel=17.0),
    'fwhi':    dict(wlevel=62.0),
    'dry':     dict(hide=['T_WATER', 'T_DROPS']),
    'cond':    dict(),
    'mlac1':   dict(hide=['m_hair'], show=['m_lacL1', 'm_lacR1']),
    'mlac2':   dict(hide=['m_hair'], show=['m_lacL2', 'm_lacR2']),
    'nowasher': dict(hide=['washer']),
    'mdry0':   dict(hide=['m_hair', 'm_fuel']),
    'mdry':    dict(hide=['m_hair', 'm_fuel'], fn="D['m_needle'].location.x += 1.42\nD['m_guide'].location.x -= 1.42"),
    'empty':   dict(hide=['T_FUEL', 'T_WATER', 'T_DROPS']),
    'adb':     dict(hide=['T_DROPS'], liq={'water': 0xbfefff}),
    'soot1':   dict(hide=['washer'], fn="LEVEL = 1\nexec(open('/home/claude/w/serinj/xsoot.py').read())"),
    'soot2':   dict(hide=['washer'], fn="LEVEL = 2\nexec(open('/home/claude/w/serinj/xsoot.py').read())"),
}
PLATES = [
    ('hero', 'shut'), ('hero', 'full'),
]
