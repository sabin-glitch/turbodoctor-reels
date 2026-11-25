# -*- coding: utf-8 -*-
"""Planurile seriei: SHOTS[episod] = câte un dicționar pe rând rostit (rândul 1 = cartonul de titlu, ultimele două = formula de final, se pun singure)."""
from eng import XM, D, DPF_Z0, DPF_Z1, DOC_Z0, DOC_Z1, PLUG, CELLS, J_IN, X_IN, X_OUT, X_WALL
ZF = DPF_Z1 + 22.0; ZB = DPF_Z0 - 30.0
LB_DD = [('Catalizator de oxidare', 'doc', 'L', 0.10, 'catalizatorul'), ('Filtru de particule', (-42.0, 0.0, -150.0), 'L', 0.93, 'filtrul')]
SENS = [('Pipe', .2, .95), ('Hose', .2, .95), ('Dps', .2, .95)]
TS3 = [('T1', .2, .95), ('T2', .3, .95), ('T3', .4, .95)]
T = None
SHOTS = {}

SHOTS[1] = [
    dict(v='ext', rev=(0.0, 1.0, 0.5, 1.0), flow=0.0),
    T,
    dict(v='wide', lb=LB_DD, leg=True),
    dict(v='maca', tint=1.0, arrows=1.0, soot=(0.0, 0.85, 0.45, 1.0), specks=1.0,
         lb=[('Canal de intrare', (X_IN, 0.0, -10.5), 'L', 0.70, 0.1), ('Dop', (X_OUT, 0.0, -3.0), 'R', 0.31, 0.15), ('Perete poros', (X_WALL, 0.0, -8.5), 'L', 0.555, 'pereti'),
             ('Funinginea rămâne', (CELLS[J_IN][0] + 0.12, 0.0, -14.0), 'R', 0.86, 'funinginea')]),
    dict(v='can', soot=(1.0, 0.0, 0.8, 1.0), heat=(0.0, 1.0, 0.0, 0.35), fuel=1.0, front=(ZF, ZB, 0.25, 0.95), flb=True, temps=(450, (300, 630, 0.0, 0.4), (250, 560, 0.3, 0.8)), note='ilu'),
    dict(v='right', soot=0.3, pul=1.0, hl=[('Pipe', 'presiunea', .98), ('Hose', 'presiunea', .98), ('Dps', 'presiunea', .98), ('T1', 'cateva', .98), ('T2', 'cateva', .98), ('T3', 'cateva', .98)],
         lb=[('Senzor de presiune\ndiferențială', 'dps', 'R', 0.05, 'presiunea'), ('Priză înainte de filtru', 'p1', 'R', 0.50, 'dinainte'), ('Priză după filtru', 'p2', 'R', 0.90, 'dupa'),
             ('Senzori de temperatură', 't2', 'L', 0.34, 'cateva')]),
    dict(v='can', soot=(0.3, 1.0), dp=(0.3, 1.0), note='ilu', pan=('soot2', dict(m=(6.0, 43.0, 0.05, 0.75), c=(6.0, 40.5, 0.05, 0.75), thr=40.0, bad='peste limită: martorul se aprinde', badt=4.4))),
    dict(v='can', soot=1.0, dp=1.0, pan=('four', dict(title='PATRU FELURI DE AVARIE', items=[('ÎNCĂRCARE', 'prea multă funingine sau cenușă'), ('REGENERARE', 'nu pornește, nu se termină'), ('SENZOR', 'semnal lipsă sau fals'), ('EFICIENȚĂ', 'filtrul nu mai reține')],
                                                  at=['incarcare', 'regenerare', 'senzor', 'eficienta']))),
    dict(v='can', soot=1.0, dp=1.0, pan=('card', dict(title='UN SINGUR COD, MAI MULTE CAUZE POSIBILE', items=[('dot', 'Filtrul de particule'), ('dot', 'Senzorul de presiune și țevile lui'), ('dot', 'O scăpare pe evacuare'), ('dot', 'Debitmetrul de aer')],
                                                      at=[0.1, 0.3, 0.55, 0.75]))),
    dict(v='wide', soot=1.0, smoke=1.0, pan=('chain', dict(title='DE CELE MAI MULTE ORI: CEVA DIN AMONTE', nodes=['Aer\nși EGR', 'Injecție', 'Motor', 'Turbină', 'FILTRU'], bad=[0, 1, 2, 3], at=[0.05, 0.1, 0.15, 0.2, 0.25],
                                                           badt=[0.55, 0.62, 0.69, 0.76], rows=1))),
    dict(v='wide', soot=1.0, pan=('grid', dict(w2='doar', l1='de cauze', l2='țin de ceramica filtrului'))),
    dict(v='ext', rev=0.0, flow=0.0, soot=0.0),
]


def chk(*items, title='CE VERIFICĂM', at=None): return ('card', dict(title=title, items=[('ok', s) for s in items], at=at))
def dots(title, *items, at=None, kind='dot'): return ('card', dict(title=title, items=[(kind, s) for s in items], at=at))
def rpm(val, sub, col='#57d08a'): return ('gauge', dict(title='TURAȚIA MOTORULUI', unit='rot/min', lo=800, hi=3500, val=val, thr=1800, bad='below', ticks=[1000, 2000, 3000], sub=sub, col=col))
def cool(val, **k): return ('gauge', dict(dict(title='TEMPERATURA MOTORULUI', unit='°C', lo=20, hi=110, val=val, thr=75, thr_lab='prag pentru regenerare', bad='below', ticks=[40, 60, 80, 100]), **k))
REGEN = dict(v='can', heat=1.0, fuel=1.0, flb=True, note='ilu')

SHOTS[2] = [
    dict(v='wide', soot=(0.3, 1.0), dp=(0.3, 1.0), pan=('dash', dict(lights=[('dpf', 'blink')], msg='FILTRU DE PARTICULE PLIN', mt=0.05))),
    T,
    dict(v='can', soot=0.6, smoke=0.7, note='ilu', pan=('soot2', dict(m=None, c=(4.0, 21.0, 0.2, 0.9), sub='calculată: din regimul motorului (motorină, aer, EGR)'))),
    dict(v='right', soot=0.6, pul=1.0, dp=(0.2, 0.7), hl=SENS, note='ilu', pan=('soot2', dict(m=(4.0, 23.0, 0.2, 0.9), c=21.0, sub='măsurată: din presiunea diferențială și din debitul de gaze'))),
    dict(v='right', soot=(0.6, 1.0), pul=1.0, dp=(0.7, 1.0), note='ilu', pan=('soot2', dict(m=(23.0, 41.5, 0.0, 0.75), c=(21.0, 33.0, 0.0, 0.75), thr=40.0, bad='prima la prag: cea măsurată', badt=2.4))),
    dict(v='can', soot=0.45, dp=0.45, note='ex', pan=('thr', dict(val=(8.0, 19.4, 0.1, 0.8)))),
    dict(v='can', soot=(0.45, 0.9), dp=(0.45, 0.9), note='ex', pan=('thr', dict(val=(19.4, 41.0, 0.1, 0.8)))),
    dict(v='can', soot=(0.9, 1.0), dp=1.0, note='ex', pan=('thr', dict(val=(41.0, 46.5, 0.05, 0.6)))),
    dict(v='can', soot=1.0, dp=1.0, heat=(0.0, 1.0, 0.25, 0.6), melt=(0.0, 0.62, 0.4, 0.95), crack=(0.0, 1.0, 0.55, 0.95), note='sim', big='SE POATE FISURA SAU TOPI'),
    dict(v='wide', soot=1.0, dp=1.0, pan=('big', dict(text='„FILTRU PLIN”\nE UN REZULTAT', fs=84, sub='Întrebarea: de ce nu s-a curățat la timp?', subt=0.55))),
    dict(v='wide', soot=1.0, dp=1.0, pan=('four', dict(cols=3, items=[('REGENERAREA', 'n-a avut condiții'), ('MOTORUL', 'face prea multă funingine'), ('SENZORUL', 'minte')], at=['regenerarea', 'motorul', 'senzorul'], fs=32))),
    dict(v='can', soot=(1.0, 0.0, 0.7, 0.9), heat=(0.0, 1.0, 0.0, 0.25), fuel=1.0, front=(ZF, ZB, 0.1, 0.8), flb=True, dp=(1.0, 0.2)),
]

SHOTS[3] = [
    dict(v='wide', soot=0.35, pan=('tester', dict(title='PE TESTER', rows=[('Filtru de particule', 'eficiență sub prag', 'bad'), ('Cod generic', 'P2002', 'hi')], at=[0.05, 0.2]))),
    T,
    dict(v='can', soot=0.35, slip=(0.0, 1.0, 0.3, 0.8), big='FUNINGINEA TRECE?'),
    dict(v='macb', tint=1.0, arrows=1.0, soot=0.8, leg=True, lb=[('Gaze filtrate, spre ieșire', (X_OUT, 0.0, DPF_Z0 + 2.0), 'R', 0.86, 0.3), ('Funinginea rămâne\nîn canalele de intrare', (X_IN, 0.0, DPF_Z0 + PLUG + 9.0), 'L', 0.2, 0.1)]),
    dict(v='bot', soot=0.35, note='sch', pan=('pm', {})),
    dict(v='right', soot=0.2, pul=1.0, note='ilu', pan=('dpx', dict(mea=(0.60, 0.15, 0.15, 0.6), fault=True))),
    dict(v='can', soot=0.4, crack=(0.0, 1.0, 0.1, 0.55), melt=(0.0, 1.0, 0.5, 0.9), note='sim', big='FISURATĂ SAU TOPITĂ', lb=[('Fisură: funinginea trece', (-17.0, 0.0, -104.0), 'L', 0.72, 0.35, 'bad')]),
    dict(v='bot', soot=0.4, crack=1.0, melt=1.0, pan=('rag', {})),
    dict(v='can', soot=0.2, gone=(0.0, 1.0, 0.62, 0.9), pan=('four', dict(cols=2, items=[('FĂRĂ METALE PREȚIOASE', 'filtru de schimb'), ('GOLIT', 'miezul a fost scos')], at=['schimb', 'unul'], fs=30))),
    dict(v='dps', soot=0.2, pul=1.0, hl=[('Dps', .15, .98)], lb=[('Senzorul de presiune\ndiferențială', 'dps', 'R', 0.06, 0.1)]),
    dict(v='wide', soot=0.2, note='sch', pan=('chain', dict(title='EGR DE JOASĂ PRESIUNE · schemă', nodes=['Filtru de\nparticule', 'Răcitor\nEGR', 'Supapă\nEGR', 'Compresor', 'Motor'], bad=[1, 2], badt=[0.6, 0.5], notes={1: 'înfundat'}, rows=1))),
    dict(v='wide', soot=0.2, pan=('vs', dict(title='CINE ARE DREPTATE?', a=('FILTRUL', ''), b=('MĂSURĂTOAREA', '')))),
]

SHOTS[4] = [
    dict(v='can', soot=(0.3, 1.0), dp=(0.3, 1.0), pan=('dash', dict(lights=[('dpf', 'blink')], lt=[0.5], spd=0.12, rpm=0.2, sub='oraș · drumuri scurte'))),
    T,
    dict(REGEN, soot=1.0, front=(ZF, ZB, 0.1, 1.0), dp=(1.0, 0.3), pan=('timer', dict(title='REGENERAREA', val=(0.0, 18.0), full=20.0, lines=[('10–20 de minute', 'y'), ('de mers susținut', '')]))),
    dict(v='can', soot=1.0, fuel=(1.0, 0.0, 0.5, 0.6), heat=(1.0, 0.0, 0.5, 0.9), front=(ZF, -70.0, 0.0, 0.5), dp=0.8, note='ilu', pan=('timer', dict(title='ÎN ORAȘ', val=(0.0, 7.0, 0.0, 0.5), full=20.0, stop=7.0, lines=[('Motor oprit', 'r'), ('Regenerarea rămâne la jumătate', '')]))),
    dict(v='can', soot=1.0, dp=0.9, dim=1.0, gspeed=0.55, note='ex', pan=rpm((2300.0, 1300.0, 0.1, 0.6), 'Treaptă lungă, turație mică: gaze prea reci pentru regenerare.')),
    dict(v='can', soot=1.0, dp=0.9, pan=('dash', dict(lights=[('fuel', 'on'), ('dpf', 'on')], lt=[0.1, 0.5], msg='REGENERAREA NU PORNEȘTE', mt=0.55, sub='la unele mașini'))),
    dict(v='can', soot=1.0, dp=0.9, fuel=1.0, pan=('inj', dict(title='POST-INJECȚIA DE LA REGENERARE', s1=1.0, s2=(0.0, 1.0, 0.1, 0.6), late='o parte ajunge în ulei'))),
    dict(v='can', soot=1.0, dp=0.9, pan=('dip', dict(lv=(0.0, 1.0, 0.1, 0.7)))),
    dict(v='can', soot=1.0, dp=1.0, pan=('dash', dict(lights=[('dpf', 'on'), ('glow', 'blink'), ('eng', 'on')], lt=[0.35, 0.7, 0.7], msg='AVARIE', mt=0.72))),
    dict(REGEN, soot=1.0, front=(ZF, ZB, 0.2, 1.0), dp=(1.0, 0.3), note='ex', pan=rpm((1300.0, 2200.0, 0.1, 0.5), 'Drum întins, turație medie, până se stinge martorul.')),
    dict(v='can', soot=1.0, dp=1.0, pan=('dash', dict(lights=[('dpf', 'blink'), ('glow', 'blink')], lt=[0.05, 0.05], msg='LA DIAGNOZĂ', mt=0.6))),
    dict(v='wide', soot=1.0, dp=1.0, pan=chk('Încărcarea filtrului', 'Starea și nivelul uleiului', 'Dacă regenerarea mai poate porni', at=['incarcarea', 'starea', 'daca'])),
]

SHOTS[5] = [
    dict(v='can', soot=(0.2, 1.0), dp=(0.2, 1.0), icon='temp', note='ilu', pan=cool((30.0, 66.0, 0.0, 0.5), flag='TERMOSTAT')),
    T,
    dict(v='can', soot=0.6, note='ilu', pan=cool((40.0, 90.0, 0.1, 0.7))),
    dict(v='can', soot=0.6, note='ex', pan=cool((90.0, 70.0, 0.3, 0.7), flag='FĂRĂ REGENERARE', thr_lab='75 °C')),
    dict(v='can', soot=0.7, note='sch', pan=('chain', dict(title='TERMOSTAT BLOCAT DESCHIS · schemă', nodes=['Motor', 'Termostat', 'Radiator', 'Pompă\nde apă'], bad=[1], badt=[0.2], notes={1: 'deschis tot timpul'}, rows=1,
                                                         sub='Lichidul trece prin radiator și la rece: motorul nu se mai încălzește.'))),
    dict(v='can', soot=0.8, note='ex', pan=cool((40.0, 68.0, 0.0, 0.55), flag='FĂRĂ REGENERARE', sub='Caz descris de un atelier.')),
    dict(v='can', soot=(0.8, 1.0), dp=(0.6, 1.0)),
    dict(v='wide', soot=1.0, pan=('big', dict(text='BUJIILE\nINCANDESCENTE', fs=80, sub='Nu sunt doar pentru pornirea la rece.', subt=0.5))),
    dict(v='can', soot=1.0, heat=(0.0, 0.7), fuel=1.0, pan=('four', dict(cols=2, all=True, items=[('LA PORNIRE', 'încălzesc camera de ardere'), ('LA REGENERARE', 'ridică temperatura gazelor')], at=[0.0, 0.3]))),
    dict(v='can', soot=1.0, dp=1.0, pan=('dash', dict(lights=[('glow', 'blink'), ('dpf', 'on')], lt=[0.3, 0.6], msg='FĂRĂ REGENERARE', mt=0.62))),
    dict(v='wide', soot=1.0, pan=chk('Temperatura reală a motorului', 'Termostatul', 'Bujiile și modulul lor', at=['temperatura', 'temperatura', 'bujiile'])),
    dict(v='can', soot=(0.0, 1.0, 0.1, 0.9), dp=(0.1, 1.0)),
]

SHOTS[6] = [
    dict(v='wide', soot=(0.2, 0.8), icon='eng', pan=('dash', dict(lights=[('eng', 'on')], msg='EROARE EGR', mt=0.1))),
    T,
    dict(REGEN, soot=1.0, front=(ZF, -70.0), temps=(450, (540, 640), (400, 560))),
    dict(v='can', soot=1.0, pan=chk('Motor cald', 'Senzori fără erori', 'EGR, clapetă, injecție: fără erori', title='CONDIȚII PENTRU REGENERARE', at=[0.2, 0.5, 0.75])),
    dict(v='can', soot=1.0, note='ex', pan=dots('GM · NICIO EROARE ACTIVĂ LA', 'EGR', 'Clapeta de admisie', 'Injectorul de pe evacuare', at=[0.42, 0.58, 0.78])),
    dict(v='right', soot=1.0, note='ex', hl=[('T1', 0.3, .95), ('T2', 0.3, .95), ('T3', 0.3, .95), ('Dps', 0.65, .98), ('Pipe', 0.65, .98)],
         pan=dots('VW · REGENERAREA SE OPREȘTE LA EROARE PE', 'Un senzor de temperatură', 'Debitmetru', 'Presiunea diferențială', at=['senzor', 'debitmetru', 'presiunea'], kind='bad')),
    dict(v='can', soot=1.0, note='sch', pan=('chain', dict(nodes=['Senzor presiune\nsupraalimentare', 'Comanda\nturbinei', 'REGENERARE'], bad=[0, 1], badt=[0.25, 0.6], cut=[2], rows=1, flow=False))),
    dict(v='can', soot=(0.5, 1.0), dp=(0.5, 1.0)),
    dict(v='can', soot=1.0, dp=1.0, pan=('tester', dict(title='ERORILE, ÎN ORDINEA APARIȚIEI', rows=[('Supapa EGR', 'prima', 'hi'), ('Filtrul de particule', 'a doua', 'bad')], at=[0.05, 0.3]))),
    dict(v='can', soot=1.0, pan=('big', dict(text='ÎNTÂI SOFTUL', top='Uneori', sub='La unele modele, constructorul a cerut actualizarea înainte de orice diagnoză.', subt=0.4))),
    dict(v='can', soot=1.0, pan=('tester', dict(title='TOATE ERORILE', rows=[('Supapa EGR', 'eroare', 'hi'), ('Senzor temperatură gaze', 'eroare', 'hi'), ('Filtrul de particule', 'încărcare', 'bad')], at=[0.1, 0.25, 0.6]))),
    dict(v='wide', soot=(1.0, 0.0, 0.5, 1.0), pan=('card', dict(items=[('1', 'Reparăm prima cauză'), ('2', 'Curățăm filtrul')], at=[0.0, 0.5]))),
]

SHOTS[7] = [
    dict(v='can', soot=1.0, fuel=1.0, cold=1.0, temps=(250, (250, 275), (225, 235)), note='ilu'),
    T,
    dict(v='wide', soot=0.8, hlD=1.0, lb=[('Catalizator de oxidare', 'doc', 'L', 0.10, 0.2), ('Filtru de particule', (-42.0, 0.0, -150.0), 'L', 0.93, 0.6)]),
    dict(v='mid', chem='fuel', fuel=1.0, heat=(0.0, 1.0, 0.2, 0.8), lb=[('Motorină din post-injecție', (XM - 12.7, 0.0, 106.0), 'L', 0.06, 0.1), ('Gaze încinse, spre filtru', (XM + 12.7, 0.0, 26.0), 'R', 0.93, 0.6)]),
    dict(v='mid', chem='cold', fuel=1.0, cold=1.0, docplug=(0.0, 1.0, 0.05, 0.5), note='sim', big='FAȚA ASTUPATĂ', lb=[('Funingine pe fața de intrare', (XM - 8.0, 0.0, DOC_Z1 - 2.0), 'L', 0.05, 0.3, 'bad'), ('Motorina iese nearsă', (XM + 12.7, 0.0, 26.0), 'R', 0.93, 0.6)]),
    dict(v='mid', chem='cold', fuel=1.0, cold=1.0, white=(0.0, 1.0, 0.1, 0.6), note='sim', lb=[('Strat activ acoperit:\nulei sau lichid de răcire', (XM + 6.0, 0.0, DOC_Z1 - 12.0), 'R', 0.2, 0.3, 'bad')]),
    dict(v='can', soot=1.0, fuel=1.0, cold=1.0, note='ilu', pan=('gauge', dict(title='TEMPERATURA ÎNAINTE DE FILTRU', unit='°C', lo=100, hi=700, val=(250.0, 335.0, 0.1, 0.7), thr=550, thr_lab='necesar pentru ardere', bad='below', ticks=[200, 400, 600], flag='REGENERARE RECE'))),
    dict(v='can', soot=1.0, note='sch', pan=('chain', dict(grp='vap', title='VAPORIZATORUL · schemă', nodes=['Pompă de\nmotorină', 'Vaporizator\n(cu bujie)', 'Catalizator', 'Filtru'], rows=1, sub='La aceste mașini, motorina pentru regenerare intră direct pe evacuare.'))),
    dict(v='can', soot=1.0, note='sch', pan=('chain', dict(grp='vap', title='VAPORIZATORUL · schemă', nodes=['Pompă de\nmotorină', 'Vaporizator\n(cu bujie)', 'Catalizator', 'Filtru'], rows=1, bad=[1], badt=[0.1], cut=[2], notes={1: 'înfundat'}, at=[0, 0, 0, 0],
                                                         sub='Regenerarea rămâne fără motorină.', subt=0.5))),
    dict(v='can', soot=1.0, note='sch', pan=('chain', dict(title='SISTEM CU ADITIV · schemă', nodes=['Rezervor\nde aditiv', 'Motorină', 'Motor', 'Filtru'], rows=1, bad=[0], badt=[0.35], notes={0: 'gol / contor neresetat'}))),
    dict(v='wide', soot=1.0, fuel=1.0, heat=(0.0, 1.0, 0.3, 0.9), hl=[('T1', 'dinainte', .98), ('T2', 'dupa', .98)], temps=(310, (320, 615, 0.3, 0.9), None), note='ilu'),
    dict(v='wide', soot=1.0, hlD=1.0, pan=('big', dict(text='ÎN FAȚA FILTRULUI,\nNU ÎN FILTRU', fs=78))),
]

AIR = ['Filtru\nde aer', 'Debitmetru', 'Turbină', 'Intercooler', 'Supapă\nEGR', 'Motor']
def air(bad, note, **k): return ('chain', dict(dict(grp='air', title='TRASEUL AERULUI · schemă', nodes=AIR, rows=2, bad=[bad], badt=[0.25], notes={bad: note}, at=[0] * 6), **k))
SAW = dict(fill=None, top=0.0, rise=15.0)

SHOTS[8] = [
    dict(v='can', soot=(0.2, 1.0), smoke=1.0, dp=(0.2, 1.0), note='sch', pan=('chain', dict(nodes=['Turbină', 'Intercooler', 'Motor'], rows=1, bad=[1], badt=[0.05], cut=[2], notes={1: 'furtun crăpat'}, at=[0, 0, 0]))),
    T,
    dict(v='can', soot=0.2, pan=('big', dict(text='MULT AER', top='Dieselul arde motorina până la capăt doar cu', fs=110))),
    dict(v='can', soot=(0.2, 0.9), smoke=(0.0, 1.0, 0.1, 0.5), dp=(0.2, 0.8)),
    dict(v='can', soot=(0.4, 1.0), smoke=1.0, pan=('cycles', dict(SAW, title='CU O SCĂPARE DE AER: FILTRUL SE UMPLE REPEDE'))),
    dict(v='can', soot=1.0, smoke=1.0, note='sch', pan=air(3, 'fisurat', at=[0.0, 0.05, 0.1, 0.15, 0.2, 0.25])),
    dict(v='can', soot=1.0, smoke=1.0, note='sch', pan=air(0, 'înfundat')),
    dict(v='can', soot=1.0, smoke=1.0, note='sch', pan=air(1, 'murdar: cifră falsă')),
    dict(v='can', soot=1.0, smoke=1.0, note='sch', pan=air(2, 'geometrie blocată')),
    dict(v='can', soot=1.0, smoke=1.0, note='sch', pan=air(4, 'rămasă deschisă')),
    dict(v='can', soot=1.0, smoke=1.0, pan=('cycles', dict(SAW, title='SEMNUL COMUN: REGENERĂRI TOT MAI DESE'))),
    dict(v='wide', soot=1.0, pan=chk('Tot traseul de aer, cu fum sub presiune', 'Valorile debitmetrului', at=['traseul', 'valorile'])),
]

SHOTS[9] = [
    dict(v='can', soot=0.6, fuel=1.0, heat=(0.0, 1.0, 0.2, 0.6), melt=(0.0, 0.7, 0.35, 0.95), note='sim', big='UN SINGUR INJECTOR'),
    T,
    dict(v='maca', tint=1.0, arrows=1.0, soot=(0.2, 1.0, 0.1, 0.9), specks=1.0),
    dict(v='can', soot=0.6, smoke=1.0, pan=('four', dict(title='INJECTOR UZAT', cols=2, all=True, items=[('PREA MULTĂ', 'motorină'), ('PULVERIZARE', 'proastă')], at=['prea', 'pulverizeaza']))),
    dict(v='can', soot=(0.4, 1.0), smoke=1.0, dp=(0.3, 1.0), note='ilu', pan=('dp', {})),
    dict(v='can', soot=0.8, fuel=1.0, cold=1.0, drops=1.0, dropcol='#ffd23a', lb=[('Motorină nearsă', 'cone_in', 'R', 0.1, 0.3, 'bad')]),
    dict(v='can', soot=0.8, fuel=1.0, heat=1.0, melt=(0.0, 1.0, 0.1, 0.8), crack=(0.0, 1.0, 0.5, 0.95), note='sim'),
    dict(v='can', soot=0.8, smoke=1.0, pan=dots('MOTOR OBOSIT', 'Compresie mică', 'Supape nereglate', at=['compresie', 'supape'])),
    dict(v='can', soot=0.8, smoke=1.0, pan=('big', dict(text='MOTORINĂ CU APĂ\nSAU MURDARĂ', fs=70))),
    dict(v='can', soot=0.8, smoke=1.0, pan=('big', dict(text='MODIFICĂRI', sub='Constructorul le trece printre cauzele de funingine multă.', subt=0.35))),
    dict(v='wide', soot=1.0, pan=chk('Injectoarele, pe stand', at=['injectoarele'])),
    dict(v='wide', soot=1.0, pan=chk('Injectoarele, pe stand', 'Proba de compresie a motorului', at=[-1.0, 'proba'])),
]

SHOTS[10] = [
    dict(v='dps', pul=1.0, hl=[('Hose1', 'vinovat', .98)], pan=('dash', dict(lights=[('dpf', 'blink')], msg='FILTRU PLIN', mt=0.3))),
    T,
    dict(v='right', pul=1.0, soot=0.3, hl=[('Pipe', .2, .98), ('Hose', .2, .98), ('Dps', .05, .98)],
         lb=[('Senzor de presiune\ndiferențială', 'dps', 'R', 0.05, 0.05), ('Înainte de filtru', 'p1', 'R', 0.50, 'dinainte'), ('După filtru', 'p2', 'R', 0.90, 'dupa')]),
    dict(v='right', pul=1.0, soot=(0.1, 1.0, 0.2, 0.9), dp=(0.1, 1.0, 0.2, 0.9), note='ilu', pan=('dp', dict(volt=True))),
    dict(v='dps', pul=1.0, soot=0.3, hl=[('Pipe', 'tevi', 'furtunase'), ('Hose', 'furtunase', .98)], lb=[('Țevi subțiri de metal', 'pipe1', 'L', 0.66, 'tevi'), ('Furtunașe de cauciuc', 'hose1', 'L', 0.3, 'furtunase')]),
    dict(v='right', pul=1.0, soot=0.3, pplug=(0.0, 1.0, 0.1, 0.4), note='sim', big='ȚEAVĂ ÎNFUNDATĂ', lb=[('Dop de funingine\nsau de gheață', 'pipe1', 'R', 0.45, 0.3, 'bad')]),
    dict(v='dps', pul=1.0, soot=0.3, leakh=(0.0, 1.0, 0.1, 0.4), hl=[('Hose1', .1, .98)], note='sim', big='FURTUNAȘ CRĂPAT', lb=[('Presiunea scapă', 'hose1', 'L', 0.3, 0.35, 'bad')]),
    dict(v='right', soot=0.3, pan=('four', dict(title='MĂSURĂTOARE FALSĂ', cols=2, all=True, items=[('PARE PLIN', 'dar e curat'), ('PARE CURAT', 'dar e plin', 'bad')], at=['plin', 'sau']))),
    dict(v='can', soot=(0.3, 1.0), pplug=1.0, note='ilu', pan=('soot2', dict(m=(6.0, 7.0), c=(6.0, 9.0), sub='Senzorul arată puțin. Regenerarea nu mai pornește, iar filtrul se umple.'))),
    dict(v='wide', soot=0.5, leakf=(0.0, 1.0, 0.2, 0.4), note='sim', hl=[('Dps', 'fir', .98)], lb=[('Scăpare la îmbinare', 'vband', 'L', 0.06, 'scapare', 'bad'), ('Cablul senzorului', 'dps_sock', 'R', 0.05, 'fir')]),
    dict(v='dps', soot=0.3, pul=1.0, hl=[('Dps', .1, .98)], lb=[('Senzorul de presiune\ndiferențială', 'dps', 'R', 0.06, 0.1)]),
    dict(v='right', soot=0.3, pan=chk('Senzorul', 'Țevile, suflate cu aer', 'Scăpările de pe evacuare', at=['senzorul', 'suflam', 'cautam'])),
]

LB_ASH = [('Cenușă', (44.0, 0.0, DPF_Z0 + 16.0), 'R', 0.80, 0.3)]
LB_ASHM = [('Cenușă', (X_IN, 0.0, DPF_Z0 + PLUG + 2.6), 'L', 0.31, 0.3), ('Dop', (X_IN, 0.0, DPF_Z0 + 3.0), 'L', 0.785, 0.1)]
RECON = [('Monolit nou,\ndin carbură de siliciu', (-30.0, 0.0, -110.0), 'L', 0.62, 'monolit'), ('Carcasa originală', 'shell', 'R', 0.42, 'carcasa')]

SHOTS[11] = [
    dict(v='wide', soot=0.3, hl=[('T2', .05, .98)], temps=(95, -40, 90), icon='eng', pan=('tester', dict(title='TEMPERATURA GAZELOR, PE TESTER', rows=[('Senzor 1', '95 °C'), ('Senzor 2', '−40 °C', 'bad'), ('Senzor 3', '90 °C')], at=[0.0, 0.05, 0.1]))),
    T,
    dict(v='wide', soot=0.3, hl=[('T1', .15, .5), ('T2', .35, .7), ('T3', .55, .95)],
         lb=[('Înainte de catalizator', 't1', 'L', 0.12, 0.15), ('Înainte de filtru', 't2', 'L', 0.45, 0.35), ('După filtru', 't3', 'L', 0.80, 0.55), ('Al patrulea, la unele mașini:\nînainte de turbină', 'inlet', 'R', 0.30, 0.7)]),
    dict(REGEN, soot=1.0, front=(ZF, -90.0), temps=((300, 450), (320, 630, 0.1, 0.6), (250, 520, 0.4, 1.0))),
    dict(v='can', soot=0.8, pan=('four', dict(title='UN SENZOR CARE CITEȘTE GREȘIT', cols=2, all=True, items=[('PREA SCURT', 'funinginea rămâne'), ('PREA LUNG', 'consum mai mare')], at=['scurte', 'lungi']))),
    dict(v='can', soot=0.8, note='ilu', pan=('soot2', dict(m=12.0, c=(12.0, 34.0, 0.1, 0.8), bad='socoteală greșită', badt=2.6))),
    dict(v='can', soot=(0.6, 1.0), dp=(0.5, 1.0), hl=[('T2', .1, .98)], note='ex', pan=('dash', dict(lights=[('eng', 'on'), ('dpf', 'on')], lt=[0.1, 0.7], msg='FĂRĂ REGENERARE', mt=0.5))),
    dict(v='mid', soot=1.0, hl=[('T2', .1, .98)], note='sim', lb=[('Fir rupt în interior', 't2', 'L', 0.26, 0.2, 'bad')]),
    dict(v='bot', soot=0.3, note='sch', pan=('pm', dict(k=0.25))),
    dict(v='bot', soot=0.3, pan=dots('SENZOR DE PARTICULE DEFECT SAU UD', 'Erori de emisii', 'Regenerări inutile', at=['erori', 'cere'], kind='bad')),
    dict(v='wide', soot=0.3, hl=TS3, note='ilu', pan=('tester', dict(title='MOTOR RECE · SENZORII DE TEMPERATURĂ', rows=[('Senzor 1', '21 °C', 'ok'), ('Senzor 2', '22 °C', 'ok'), ('Senzor 3', '21 °C', 'ok'), ('Senzor 4', '−40 °C', 'bad')], at=[0.1, 0.2, 0.3, 0.6]))),
    dict(v='ext', rev=0.0, flow=0.0),
]

SHOTS[12] = [
    dict(v='can', soot=(1.0, 0.0, 0.55, 0.8), heat=(1.0, 0.3, 0.7, 1.0), fuel=1.0, front=(ZF, ZB, 0.0, 0.7), ash=7.0, ashw=45.0, lb=[('Cenușă', (44.0, 0.0, DPF_Z0 + 16.0), 'R', 0.80, 'ceva')]),
    T,
    dict(v='can', soot=(0.9, 0.0, 0.5, 0.75), heat=1.0, fuel=1.0, front=(ZF, ZB, 0.0, 0.65), flb=True, ash=7.0, ashw=45.0, lb=[('Cenușa rămâne', (44.0, 0.0, DPF_Z0 + 16.0), 'R', 0.80, 'cenusa')]),
    dict(v='macb', tint=1.0, arrows=1.0, ash=(0.0, 5.0, 0.1, 0.95), ashfall=1.0, lb=LB_ASHM),
    dict(v='macb', tint=1.0, arrows=1.0, ash=(5.0, 8.6), ashfall=1.0, lb=LB_ASHM + [('Canalul rămâne mai scurt', (X_IN, 0.0, DPF_Z0 + PLUG + 12.0), 'R', 0.12, 0.4)]),
    dict(v='can', soot=0.4, ash=7.0, ashw=(8.0, 40.0), lb=LB_ASH, pan=('cycles', {})),
    dict(v='can', soot=0.4, ash=7.0, ashw=(40.0, 75.0), lb=LB_ASH, pan=('cycles', dict(title='CU ULEI NEPOTRIVIT: MULT MAI REPEDE', pw=0.55, top=0.8))),
    dict(v='can', soot=0.4, ash=7.0, ashw=75.0, lb=LB_ASH, pan=('big', dict(text='ULEI CU\nCENUȘĂ PUȚINĂ', top='Motoarele cu filtru de particule cer', fs=84, sub='Celălalt îl poate înfunda definitiv.', subt=0.55))),
    dict(v='can', soot=(1.0, 0.0, 0.45, 0.7), heat=(1.0, 0.0, 0.7, 1.0), fuel=1.0, front=(ZF, ZB, 0.0, 0.6), ash=7.0, ashw=75.0, note='ilu', pan=('dp', dict(lv=(1.0, 0.62, 0.1, 0.7), sub='După regenerare, presiunea nu mai scade cât trebuie.', bad=True, subt=2.5))),
    dict(v='macb', tint=1.0, ash=8.6, heat=1.0, lb=LB_ASHM),
    dict(v='macb', tint=0.3, flow=0.0, ash=(8.6, 0.0, 0.35, 0.95), big='DOAR CU FILTRUL DEMONTAT'),
    dict(v='wide', pan=chk('Ce ulei e în motor', 'Cât ulei consumă motorul', at=['ce', 'cat'])),
]

SHOTS[13] = [
    dict(v='can', soot=0.5, smoke=0.6, drops=1.0, icon='oil'),
    T,
    dict(v='can', soot=0.5, drops=1.0, pan=('four', dict(title='PE UNDE AJUNGE ULEIUL ÎN ARDERE', cols=3, all=True, items=[('SEMERINGURI', 'de supape'), ('SEGMENȚI', 'uzați'), ('AERISIREA', 'carterului')], at=['semeringurile', 'segmenti', 'aerisirea'], fs=30))),
    dict(v='macb', tint=1.0, arrows=1.0, ash=(0.0, 6.5, 0.1, 0.95), ashfall=1.0, lb=LB_ASHM),
    dict(v='can', soot=0.5, drops=(0.0, 1.0, 0.3, 0.6), note='sch', pan=('chain', dict(nodes=['Turbină', 'Catalizator', 'Filtru'], rows=1, bad=[0], badt=[0.35], notes={0: 'etanșarea a cedat: scapă ulei'}, at=[0, 0, 0]))),
    dict(v='can', soot=0.6, drops=1.0, oil=(0.0, 1.0, 0.1, 0.8), docplug=(0.0, 0.7), note='sim', big='ÎMBIBAT CU ULEI'),
    dict(v='can', soot=1.0, oil=1.0, docplug=0.7, drops=1.0, pan=('chain', dict(title='ȘI INVERS: UN CERC', nodes=['Filtru\nînfundat', 'Gaze împinse\nîn turbină', 'Turbina\nscapă ulei', 'Ulei\nîn filtru'], rows=1, at=[0.15, 0.35, 0.6, 0.8], flow=True,
                                                                                 sub='…iar filtrul se înfundă și mai tare.', subt=0.85))),
    dict(v='can', soot=0.5, drops=1.0, dropcol='#dfeaf0', pan=('four', dict(title='LICHID DE RĂCIRE PE EVACUARE', cols=2, all=True, items=[('RĂCITOR EGR', 'fisurat'), ('GARNITURĂ', 'de chiulasă')], at=['racitor', 'garnitura']))),
    dict(v='mid', soot=0.3, drops=1.0, dropcol='#dfeaf0', white=(0.0, 1.0, 0.1, 0.7), note='sim', lb=[('Depuneri care nu ard', (-40.0, 0.0, DPF_Z1 - 4.0), 'L', 0.72, 0.5, 'bad')]),
    dict(v='can', soot=0.5, white=1.0, heat=(0.0, 1.0, 0.2, 0.6), melt=(0.0, 0.7, 0.45, 0.95), note='sim'),
    dict(v='can', soot=0.5, pan=('four', dict(title='DOUĂ ÎNTREBĂRI', cols=2, all=True, items=[('CONSUMĂ ULEI?', ''), ('SCADE LICHIDUL?', 'de răcire')], at=['consuma', 'scade']))),
    dict(v='wide', soot=0.0, pan=chk('Turbina', 'Epuratorul', 'Răcitorul EGR', at=['turbina', 'epuratorul', 'racitorul'])),
]

SHOTS[14] = [
    dict(v='can', soot=1.0, heat=1.0, fuel=0.0, melt=(0.0, 0.62, 0.3, 0.9), temps=(600, (700, 1250, 0.0, 0.5), (600, 1100, 0.2, 0.7)), note='sim'),
    T,
    dict(REGEN, soot=1.0, front=(ZF, -90.0), temps=(450, (540, 610), (400, 540))),
    dict(v='can', soot=1.0, dp=1.0, heat=(0.0, 1.0, 0.5, 0.95), note='ex', pan=('thr', dict(val=(40.0, 47.5, 0.05, 0.5)))),
    dict(v='can', soot=(1.0, 0.4), heat=1.0, temps=(650, (700, 1050), (650, 1000)), note='sim'),
    dict(v='can', soot=0.4, heat=1.0, gspeed=0.3, note='ex', pan=rpm((2300.0, 800.0, 0.2, 0.6), 'La ralanti, gazele care răceau filtrul aproape dispar.')),
    dict(v='can', soot=0.3, heat=(1.0, 0.2), crack=(0.0, 1.0, 0.05, 0.4), melt=(0.6, 1.0, 0.1, 0.5), note='sim',
         pan=('four', dict(cols=2, all=True, items=[('CORDIERITĂ', 'cedează mai devreme'), ('CARBURĂ DE SILICIU', 'rezistă mai mult')], at=['cordierita', 'carbura'], fs=30))),
    dict(v='can', soot=0.3, crack=1.0, melt=1.0, note='sim', pan=('tester', dict(title='PE TESTER', rows=[('Filtru de particule', 'eficiență sub prag', 'bad')], at=[0.45]))),
    dict(v='can', soot=0.6, oil=(0.0, 1.0, 0.0, 0.4), heat=(0.0, 1.0, 0.5, 0.9), melt=(0.0, 0.62, 0.6, 1.0), note='sim', big='ULEI SAU MOTORINĂ'),
    dict(v='can', soot=0.3, crack=1.0, melt=1.0, note='sim', pan=('big', dict(text='CURĂȚAREA\nNU-L MAI SALVEAZĂ', fs=74, col='#ff5a4a'))),
    dict(v='can', crack=(1.0, 0.0, 0.2, 0.45), melt=(1.0, 0.0, 0.2, 0.45), hlF=(0.0, 1.0, 0.4, 0.7), lb=RECON),
    dict(v='wide', pan=('big', dict(text='DE CE S-A\nSUPRAÎNCĂRCAT?', fs=84))),
]

SHOTS[15] = [
    dict(v='ext', rev=0.0, flow=0.0, pan=('dash', dict(lights=[('dpf', 'blink')], lt=[0.45], msg='FILTRU DE PARTICULE', mt=0.5, sub='filtru nou · câteva sute de kilometri'))),
    T,
    dict(v='can', soot=(0.0, 1.0, 0.1, 0.9), smoke=1.0, dp=(0.1, 1.0), pan=('gauge', dict(title='FILTRU NOU, CAUZA NEREPARATĂ', unit='km', lo=0, hi=300, val=(0.0, 95.0, 0.3, 0.95), ticks=[0, 100, 200, 300], col='#ff5a4a',
                                                                                         sub='Un producător de filtre: se poate înfunda în mai puțin de 100 km.'))),
    dict(v='mid', lb=[('Stratul cu metale prețioase', (XM + 10.2, 0.0, 44.0), 'R', 0.82, 'metale'), ('Catalizator', (XM - 14.0, 0.0, 70.0), 'L', 0.15, 0.1)]),
    dict(v='can', soot=(0.3, 1.0), dp=(0.3, 1.0), pan=('four', dict(cols=2, all=True, items=[('ORIGINAL', 'funinginea arde din mers'), ('IEFTIN', 'funinginea se strânge', 'bad')], at=[0.05, 0.3]))),
    dict(v='can', gone=(0.0, 1.0, 0.1, 0.45), note='ilu', pan=('dp', dict(lv=(0.5, 0.0, 0.15, 0.5), sub='Presiunea pe filtru a dispărut.', bad=True, subt=2.6))),
    dict(v='can', gone=1.0, pan=('big', dict(text='FĂRĂ VIZĂ ITP', top='Scoaterea filtrului: lucrare neautorizată', col='#ff5a4a', t1=0.55))),
    dict(v='right', soot=0.2, hl=[('Dps', 'senzor', .98)], pan=('tester', dict(title='DUPĂ UN FILTRU SAU UN SENZOR NOU', rows=[('Adaptarea filtrului', 'de făcut', 'hi'), ('Adaptarea senzorului', 'de făcut', 'hi')], at=['filtru', 'senzor']))),
    dict(v='can', soot=1.0, heat=(0.0, 1.0, 0.2, 0.6), fuel=1.0, crack=(0.0, 1.0, 0.6, 0.95), note='sim'),
    dict(v='can', soot=0.6, heat=(0.0, 0.8), pan=('big', dict(text='ADITIVI ÎN EXCES', sub='Cei ieftini, cu fier, pot supraîncălzi miezul.', subt=0.4))),
    dict(v='wide', soot=0.4, pan=('card', dict(title='S-A LUCRAT', items=[('ok', 'pe filtru'), ('bad', 'nu pe cauză')], at=['filtru', 'nu']))),
    dict(v='wide', pan=('card', dict(title='ORDINEA CORECTĂ', items=[('1', 'Cauza'), ('2', 'Filtrul'), ('3', 'Adaptările și proba de drum')], at=['cauza', 'filtrul', 'apoi']))),
]

SHOTS[16] = [
    dict(v='wide', soot=0.6, pan=('grid', dict(w2='doar', t1=0.0, l1='de cauze', l2='sunt în filtru'))),
    T,
    dict(v='wide', soot=0.6, pan=('chain', dict(title='NE UITĂM LA TOATĂ MAȘINA', nodes=['Aer', 'EGR', 'Injecție', 'Turbină', 'FILTRU'], rows=1, at=[0.45, 0.52, 0.6, 0.68, 0.1]))),
    dict(v='wide', soot=0.8, note='ilu', pan=('tester', dict(title='DIAGNOZA', rows=[('Erori memorate', 'toate', 'hi'), ('Funingine calculată', '31 g'), ('Funingine măsurată', '38 g'), ('Cenușă · regenerări', 'valori', '')], at=['erorile', 'calculata', 'masurata', 'cenusa']))),
    dict(v='face', soot=0.5, crack=(0.0, 0.5, 0.5, 0.9), note='sim', lb=[('Căutăm fisuri\nși urme de topire', (XM - 9.0, 0.0, -22.0), 'L', 0.9, 'fisuri')]),
    dict(v='macb', tint=0.3, flow=0.0, ash=(8.6, 0.0, 0.3, 0.9), lb=[('Canalele rămân libere', (X_IN, 0.0, DPF_Z0 + PLUG + 9.0), 'R', 0.15, 'canalele')]),
    dict(v='can', crack=(1.0, 0.0, 0.3, 0.55), melt=(1.0, 0.0, 0.3, 0.55), hlF=(0.0, 1.0, 0.5, 0.8), lb=RECON, note='sim'),
    dict(v='can', hlF=0.6, pan=('tester', dict(title='PREȚUL', rows=[('Filtru original nou', '100 %'), ('Recondiționare', '30–40 %', 'ok')], at=[0.05, 0.1]))),
    dict(v='wide', pan=('big', dict(text='CĂUTĂM CAUZA', top='Cât filtrul e la curățat', sub='pe mașină', fs=100))),
    dict(v='wide', pan=('four', dict(cols=4, all=True, items=['AERUL', 'EGR-UL', 'INJECTOARELE', 'TURBINA', 'ULEIUL', 'SENZORII', 'TERMOSTATUL', 'BUJIILE'], at=[0.0, 0.1, 0.24, 0.42, 0.54, 0.66, 0.78, 0.9], fs=28))),
    dict(v='wide', pan=chk('Ce am găsit', 'Ce trebuie reparat', title='CONSTATAREA', at=['ce', 'si'])),
    dict(v='ext', rev=0.0, flow=0.0),
]
