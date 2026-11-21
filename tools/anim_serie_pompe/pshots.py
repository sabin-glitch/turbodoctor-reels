# Camerele si starile placilor pentru seria pompelor de inalta presiune (comun pentru Blender si pentru montaj). Unitati: mm, grade.
# Reperul scenei: Z in sus; pompa are arborele pe -Y (spre privitor), capul hidraulic sus. Punct din reperul pompei (x, y, z) -> (x, -z, y).
W, H = 1080, 1920
BL = '/home/claude/w/serpmp/blend/'
INJ = '/home/claude/w/inj/out/'; MIC = '/home/claude/w/serinj/blend/'
PUMP_IN = ['shaft', 'shaftDam', 'tap', 'plunger', 'spring', 'inValve', 'inSpring', 'outBall', 'outSpring']
LIQ = ['fLP', 'fCol', 'fCh', 'fOut', 'fIn']

# cam: blend, tinta, azimut, elevatie, distanta, obiectiv; ls = scara luminilor; hide = obiecte / grupuri ascunse
CAMS = {
    'pw':  dict(blend='pump', tgt=(4, -4, -2), az=52, el=17, dist=505, lens=42, ls=0.9, hide=['FULL']),            # pompa in sectiune, plan larg
    'pc':  dict(blend='pump', tgt=(4, -6, 4), az=38, el=17, dist=320, lens=52, ls=0.6, hide=['FULL']),           # cama, rola, tachetul
    'ph':  dict(blend='pump', tgt=(13, -4, 46), az=40, el=12, dist=330, lens=60, ls=0.6, hide=['FULL']),          # capul hidraulic: piston, supape
    'pm':  dict(blend='pump', tgt=(1, -3, 14), az=24, el=6, dist=170, lens=60, ls=0.35, hide=['FULL']),           # contactul rola - cama, de aproape
    'px':  dict(blend='pump', tgt=(4, -4, -2), az=52, el=17, dist=505, lens=42, ls=0.9, hide=[]),                 # pompa intreaga (aceeasi camera ca pw)
}
# stari: phi = unghiul arborelui (rad); rot = tachetul rotit (0..1); hide/show; liq = {material: culoare | (culoare, opacitate)}; hot = rola incinsa
STATES = {
    'fuel':  dict(),
    'dry':   dict(hide=LIQ),
    'dam':   dict(hide=LIQ + ['shaft'], show=['shaftDam']),            # cama zgariata, fara motorina
    'damf':  dict(hide=['shaft'], show=['shaftDam']),                  # cama zgariata, cu motorina
    'full':  dict(show=['FULL'], hide=['CUT'] + [n for n in PUMP_IN if n != 'shaft'] + LIQ),
    # piei de defect peste piesele lustruite (pmodel.py): rugina, lac (motorina imbatranita), uzura mata; varianta cu 'd' la sfarsit = fara motorina
    'rust':  dict(show=['d_rust_shaft', 'd_rust_roller', 'd_rust_plunger']), 'rustd': dict(hide=LIQ, show=['d_rust_shaft', 'd_rust_roller', 'd_rust_plunger']),
    'lac':   dict(show=['d_lac_shaft', 'd_lac_roller', 'd_lac_plunger']), 'lacd': dict(hide=LIQ, show=['d_lac_shaft', 'd_lac_roller', 'd_lac_plunger']),
    'wear':  dict(show=['d_wear_shaft', 'd_wear_roller', 'd_wear_plunger']), 'weard': dict(hide=LIQ, show=['d_wear_shaft', 'd_wear_roller', 'd_wear_plunger']),
}

# --- piesele din jurul pompei (blend/aux.blend): filtrul masinii, modulul din rezervor, injectorul, rampa, racordurile ---
AUXG = ['FLT', 'TM', 'INJ', 'RAIL', 'QUICK', 'UNUT']
CAMS.update({
    'fl':  dict(blend='aux', tgt=(0, 0, 64), az=45, el=14, dist=500, lens=42, ls=0.7, hide=[]),                    # filtrul de motorina in sectiune
    'flz': dict(blend='aux', tgt=(0, 0, 75), az=45, el=10, dist=380, lens=50, ls=0.6, hide=[]),                    # hartia filtrului, de aproape
    'tm':  dict(blend='aux', tgt=(-40, 0, -130), az=45, el=12, dist=790, lens=42, ls=1.0, hide=['FLT']),            # modulul pompei electrice din rezervor
    'tmz': dict(blend='aux', tgt=(0, 0, -200), az=45, el=8, dist=420, lens=50, ls=0.7, hide=['FLT']),              # sorbul si motorasul, de aproape
    'ij':  dict(blend='aux', tgt=(10, 0, 78), az=40, el=10, dist=430, lens=42, ls=0.6, hide=['FLT']),               # injectorul intreg
    'rl':  dict(blend='aux', tgt=(0, 0, -30), az=78, el=16, dist=1150, lens=42, ls=1.4, hide=['FLT']),             # rampa
    'qk':  dict(blend='aux', tgt=(0, -12, -6), az=60, el=14, dist=110, lens=42, ls=0.25, hide=['FLT']),            # racordul rapid
    'un':  dict(blend='aux', tgt=(0, -8, -6), az=60, el=14, dist=110, lens=42, ls=0.25, hide=['FLT']),             # piulita olandeza
})
STATES.update({
    'fempty': dict(hide=['fltOut', 'fltCore']),          # filtrul gol (aer)
    'ffull':  dict(),                                     # filtrul plin
    'tmfuel': dict(show=['TM']), 'tmdry': dict(show=['TM'], hide=['tmFuel']),
    'inj':    dict(show=['INJ']), 'rail': dict(show=['RAIL']), 'quick': dict(show=['QUICK']), 'unut': dict(show=['UNUT']),
})

# --- atelierul (blend/wk_*.blend): desene schematice ---
CAMS.update({
    'wm':  dict(blend='wk_mic', tgt=(-4, 10, 90), az=24, el=24, dist=1700, lens=42, ls=1.5, hide=[]),          # pompa desfacuta, sub microscop
    'wu':  dict(blend='wk_usb', tgt=(0, 0, 40), az=26, el=38, dist=1600, lens=42, ls=1.5, hide=[]),            # baia cu ultrasunete
    'wb':  dict(blend='wk_bench', tgt=(0, 110, 185), az=-32, el=18, dist=1700, lens=42, ls=1.8, hide=[]),      # bancul de proba
    'wi':  dict(blend='wk_inj', tgt=(0, 40, 235), az=28, el=14, dist=1500, lens=42, ls=1.8, hide=[]),          # standul de injectoare
})
STATES.update({'wk': dict(), 'wkdam': dict(hide=['shaft'], show=['shaftDam']), 'wkup': dict(loc={'usb.basket': (0, 0, 78)})})
# --- regulatorul de debit in sectiune (blend/reg.blend, preg.py): s = cat e ridicat pistonasul, 0 = inchis ... 4.4 = deschis de tot ---
def reg_fn(expr):
    return ("s = %s\n"
            "D['R_MOVE'].location = (0, 0, s)\n"
            "kz = (16.9 + s) / 16.9; D['r_spring'].scale = (1, 1, kz); D['r_spring'].location = (0, 0, 2.1 * (1 - kz))\n"
            "D['r_fBore'].scale = (1, 1, (18.9 + s) / 18.9)\n"
            "ku = (3.96 + s) / 3.96; D['r_fUnder'].scale = (1, 1, ku); D['r_fUnder'].location = (0, 0, 2.02 * (1 - ku))\n") % expr
REG_MOVE = ['R_MOVE', 'r_spring', 'r_fBore', 'r_fUnder']
CAMS.update({
    'rg':  dict(blend='reg', tgt=(3, 0, 32), az=0, el=8, dist=350, lens=70, ls=0.62, hide=['R_FULL']),                  # regulatorul intreg, in sectiune
    'rgz': dict(blend='reg', tgt=(0, 0, 12.5), az=0, el=6, dist=150, lens=70, ls=0.32, hide=['R_FULL']),                # pistonasul, ferestrele si sita, de aproape
    'rgf': dict(blend='reg', tgt=(3, 0, 31), az=28, el=14, dist=350, lens=70, ls=0.62, hide=['R_FULL']),          # regulatorul intreg, vazut din afara
    'rgs': dict(blend='reg', tgt=(0, 0, 11.5), az=28, el=10, dist=130, lens=70, ls=0.3, hide=['R_FULL']),            # sita de la intrare, de aproape
})
STATES.update({
    'reg':     dict(fn=reg_fn('2.4')),                                               # pe la jumatate
    'regopen': dict(fn=reg_fn('4.4')), 'regshut': dict(fn=reg_fn('0.0')),
    'regmove': dict(fn=reg_fn('2.4 + 2.0 * math.sin(2 * math.pi * k / max(n, 1))'), movers=REG_MOVE, nokey=True),      # bucla: pistonasul dozeaza
    'regdry':  dict(fn=reg_fn('2.4'), hide=['R_FUEL']),
    'regshutd': dict(fn=reg_fn('0.0'), hide=['R_FUEL']),
    'regfull': dict(show=['R_FULL'], hide=['R_BODY', 'R_MOVE', 'R_FUEL']),                  # regulatorul intreg, nesectionat
})
# --- cupla rapida (blend/qc.blend) si capatul conductei de inalta presiune (blend/hpe.blend), in sectiune (pconn.py) ---
CAMS.update({
    'qs':  dict(blend='qc', tgt=(0, 0, 6), az=0, el=6, dist=300, lens=70, ls=0.55, hide=['Q_FULL']),               # cupla pe conducta, plan larg
    'qsz': dict(blend='qc', tgt=(0, 0, 10), az=0, el=6, dist=150, lens=70, ls=0.32, hide=['Q_FULL']),              # garniturile, de aproape
    'qsf': dict(blend='qc', tgt=(0, 0, 6), az=24, el=10, dist=300, lens=70, ls=0.55, hide=['Q_FULL']),             # cupla intreaga, din afara
    'hc':  dict(blend='hpe', tgt=(0, 0, 8), az=0, el=6, dist=230, lens=70, ls=0.45, hide=[]),                      # racordul de inalta presiune, plan larg
    'hcz': dict(blend='hpe', tgt=(0, 0, -1), az=0, el=5, dist=112, lens=70, ls=0.26, hide=[]),                     # conul si scaunul, de aproape
})
STATES.update({
    'qok':  dict(), 'qbad': dict(show=['Q_BAD'], hide=['Q_OK']), 'qbadd': dict(show=['Q_BAD'], hide=['Q_OK', 'Q_FUEL']),
    'qfull': dict(show=['Q_FULL'], hide=['Q_BODY', 'Q_OK', 'Q_BAD', 'Q_FUEL']),
    'hok':  dict(hide=['H_BAD']), 'hbad': dict(show=['H_BAD'], hide=['H_OK']), 'hokd': dict(hide=['H_BAD', 'H_FUEL']), 'hbadd': dict(show=['H_BAD'], hide=['H_OK', 'H_FUEL']),
})
# --- tachetul rotit cu 90 de grade (cauza 13) si pistonul intepenit sus, lipit de lac (cauza 8) ---
import math as _m
STUCK_FN = ("h = 26.5\n"
            "D['tap'].location = (0, h, 0); D['plunger'].location = (0, h, 0); D['spring'].data.shape_keys.key_blocks['B'].value = (h - 18.0) / 22.0\n"
            "top = h + 50.4; D['fCol'].location = (0, top, 0); D['fCol'].scale = (1, max(0.05, 79 - top), 1)\n"
            "D['inValve'].location = (0, 84.2, 0); D['inSpring'].scale = (1, 1, 1); D['outBall'].location = (15.66, 81.6, 0)\n"
            "D['outSpring'].location = (17.16, 81.6, 0); D['outSpring'].scale = ((28 - 17.16) / 10.8, 1, 1)\n"
            "bpy.data.materials['fuelCh'].node_tree.nodes['COL'].outputs[0].default_value = list(K.srgb(imats.C_LP))[:3] + [1.0]\n")
LAC = ['d_lac_shaft', 'd_lac_roller', 'd_lac_plunger']
STATES.update({
    'rot':     dict(rot=1.0, stuck=True),                                              # tachetul rotit: rola sta de-a curmezisul si aluneca
    'rotdam':  dict(rot=1.0, stuck=True, hide=['shaft'], show=['shaftDam']),           # la fel, cu cama zgariata
    'rotturn': dict(rot=lambda u: 0.5 - 0.5 * _m.cos(_m.pi * min(1.0, u / 0.9)), nloop=30, turns=1.0, nokey=True),      # bucla jucata o data: tachetul se roteste
    'stuckp':  dict(show=LAC, fn=STUCK_FN),                                            # pistonul ramane sus; cama se invarte in gol
})
PHI0 = 0.55          # unghiul arborelui in placile fixe (pistonul la jumatatea cursei, in urcare)
NLOOP = 30           # cadre pe bucla (o jumatate de tura a arborelui = o cursa completa a pistonului)

# --- raftul dezmembrarii, cu zece pompe folosite (blend/shelf.blend, pshelf.py) ---
CAMS.update({
    'sh':  dict(blend='shelf', tgt=(8, 0, 250), az=13, el=7, dist=4150, lens=60, ls=4.0),                # raftul intreg
    'shz': dict(blend='shelf', tgt=(133, 0, 270), az=9, el=9, dist=1330, lens=60, ls=1.7),               # pompa intoarsa cu racordurile spre noi, de aproape
    'sh2': dict(blend='shelf', tgt=(-100, 0, 512), az=8, el=6, dist=1740, lens=60, ls=2.2),               # doua pompe la fel, una langa alta (polita de sus)
})
STATES.update({'shelf': dict()})
