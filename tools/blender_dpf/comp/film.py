"""Turbo Doctor - training film "Filtrul de particule (DPF)": shots, timeline, texts, panels, render.

  [FMT=V|H] python3 film.py --info                    -> timeline
  [FMT=V|H] python3 film.py --png 5,12,20 | --mid     -> proof/<FMT>_<t>.png  (--mid: the middle of every line)
  [FMT=V|H] python3 film.py --out x.mp4 [--jobs 2] [--force 3,4]     one file per chapter in x.mp4.seg/, joined without re-encoding
  [FMT=V|H] python3 film.py --out x.mp4 --frames a b
  python3 film.py --cues vo/cues.json                 -> where every narration line starts (for the voice track)
One shot per narration line (script.py); the length of a shot is the length of its spoken line (vo/meas.json).
"""
import sys, os, json, math, subprocess, time
import numpy as np, skia, cv2
from fk import *
import eng as E
from eng import (W, H, FMT, FPS, Y, WHT, BG, C_GAS, C_CLN, C_SOOT, C_ASH, C_HOT, C_FUEL, SAMP, XM, D, DPF_Z0, DPF_Z1, DOC_Z0, DOC_Z1, PLUG, CELLS, J_IN, X_IN, X_OUT,
                 X_WALL, proj, to_screen, anchor, fit_px, fit_view, box3, view_at, zoomed, interp_view, BBX, chemtxt, chemw)
import script as SC

HERE = os.path.dirname(os.path.abspath(__file__))
N = SC.N
GRN, RED = '#57d08a', '#ff5a4a'

# ------------------------------------------------------------------ layout
if FMT == 'V':
    R_FULL = (40, 236, 1040, 1540); R_HI = (40, 236, 1040, 1124); R_PAN = (40, 1150, 1040, 1572); R_BIG = (40, 1150, 1040, 1856)
    E.TAG_FADE = (218, 1500)
    CAPX, CAPY, CAPW, CAPT, CAPB, CAPLH = 60, 1652, 960, 50, 33, 44
else:
    R_FULL = R_HI = (30, 96, 1010, 1046); R_PAN = (1076, 474, 1880, 1040); R_BIG = (1076, 214, 1880, 1040)
    CAPX, CAPY, CAPW, CAPT, CAPB, CAPLH = 1076, 262, 800, 44, 30, 41


def mk_views(R):
    p = 22; Rp = (R[0] + p, R[1] + p, R[2] - p, R[3] - p)
    cxm, cym = (R[0] + R[2]) / 2, (R[1] + R[3]) / 2; wr, hr = R[2] - R[0], R[3] - R[1]
    V = {}
    V['ext'] = fit_px(BBX['ext'], Rp)
    V['wide'] = fit_px(BBX['sec'], Rp)
    V['can'] = fit_view(box3(-150, 150, -256, 176, 0, 30), Rp)
    V['right'] = fit_view(box3(-70, 196, -236, 252, 0, 30), Rp)
    V['dps'] = fit_view(box3(46, 192, -10, 252, 0, 30), Rp)
    V['top'] = fit_view(box3(-196, 110, 56, 334, 0, 30), Rp)
    V['mid'] = fit_view(box3(-200, 120, -96, 112, 0, 30), Rp)
    V['bot'] = fit_view(box3(-196, 150, -336, -150, 0, 30), Rp)
    V['doc'] = view_at((XM, 0.0, 61.0), min(wr / 70.0, hr / 88.0), cxm, cym)
    V['face'] = view_at((XM, 0.0, -6.0), min(wr / 62.0, hr / 64.0), cxm, cym)
    V['maca'] = view_at((XM, 0.0, -6.1), 72.0, cxm, cym + 10)
    V['macb'] = view_at((XM, 0.0, -171.2), 72.0, cxm, cym + 10)
    return V


VIEWS = {0: mk_views(R_FULL), 1: mk_views(R_HI)}

# ------------------------------------------------------------------ the shots: one per narration line
R_SO = D['R_SO']
LB_DD = [('Catalizator de oxidare (DOC)', 'doc', 'L', 0.10, 0.25), ('Filtru de particule (DPF)', (-42.0, 0.0, -150.0), 'L', 0.93, 0.55)]
STEPS = ['Toate erorile, nu doar cea a filtrului', 'Valorile măsurate: funingine măsurată și calculată, cenușă, presiune diferențială, temperaturi, distanța de la ultima regenerare',
         'Furtunașe, țevi, senzor, etanșeitatea evacuării', 'Cauza din amonte: injecție, EGR, turbină și admisie, consum de ulei, termostat, bujii',
         'La urmă, filtrul: regenerare, curățare sau înlocuire, cu adaptările făcute corect']
ZF = DPF_Z1 + 22.0

SH = [
    # ---------------- 0 ce e în carcasă
    dict(v='ext', rev=0.0, flow=0.0, cap=('FILTRUL DE PARTICULE (DPF)', 'Ce e în el, cum se încarcă, cum se regenerează și de ce dă erori.')),
    dict(v='ext', rev=0.0, flow=0.0, hl=[('L', .42, .95), ('T1', .50, .95), ('T2', .56, .95), ('T3', .62, .95), ('Dps', .68, .95), ('Pipe', .68, .95), ('Hose', .68, .95)],
         lb=[('Intrare: gaze de la turbină', 'inlet', 'L', 0.05, 0.25), ('Ieșire spre eșapament', 'outlet', 'R', 0.95, 0.38), ('Senzorii, pe carcasă', 't2', 'L', 0.60, 0.62)],
         cap=('CARCASA', 'Stă imediat după turbină, cu senzorii prinși pe ea.')),
    dict(v='wide', rev=(0.0, 1.0, 0.0, 0.26), lb=LB_DD, cap=('DOUĂ PIESE CERAMICE', 'Sus catalizatorul de oxidare (DOC), sub el filtrul de particule (DPF).')),
    dict(v='wide', lb=[(a, b, c_, d, 0) for a, b, c_, d, e in LB_DD] + [('Saltea de fixare', 'mat_dpf', 'L', 0.70, 0.2), ('Carcasă de inox', (R_SO, 0.0, -150.0), 'R', 0.84, 0.45)],
         cap=('SALTELE DE FIXARE', 'Țin ceramica pe loc și preiau dilatarea.')),
    # ---------------- 1 rolul DOC-ului
    dict(v='doc', lb=[('Canale drepte, deschise\nla ambele capete', (XM - 14.0, 0.0, 70.0), 'L', 0.15, 0.25), ('Strat cu platină și paladiu', (XM + 10.2, 0.0, 44.0), 'R', 0.82, 0.6)],
         cap=('DOC · CATALIZATORUL DE OXIDARE', 'Un fagure cu canale drepte, acoperite cu platină și paladiu.')),
    dict(v='doc', chem='ox', chem_a=1.0, cap=('ROLUL 1 · ARDE CO ȘI HC', 'Monoxidul de carbon și motorina nearsă (HC) ies ca CO₂ și apă.')),
    dict(v='doc', chem='no2', chem_a=1.0, cap=('ROLUL 2 · FACE NO₂', 'Cu dioxidul de azot, funinginea din filtru poate arde încet, la temperaturi obișnuite de drum.')),
    dict(v='doc', chem='fuel', fuel=1.0, heat=(0.0, 1.0, 0.25, 0.8),
         lb=[('Motorină din post-injecție', (XM - 12.7, 0.0, 106.0), 'L', 0.06, 0.4), ('După DOC: gaze la peste 600 °C', (XM + 12.7, 0.0, 26.0), 'R', 0.93, 0.7)],
         cap=('ROLUL 3 · ÎNCĂLZEȘTE GAZELE', 'La regenerare arde motorina trimisă pe evacuare și încălzește gazele înainte de filtru.')),
    dict(v='doc', chem='cold', fuel=1.0, cold=1.0, heat=0.0,
         lb=[('DOC rece: sub ≈ 200 °C', (XM - 6.0, 0.0, 60.0), 'L', 0.48, 0.2), ('Motorina iese nearsă', (XM + 12.7, 0.0, 26.0), 'R', 0.93, 0.5)],
         cap=('LUCREAZĂ DOAR CALD', 'Sub circa 200 °C, motorina trece prin el nearsă.')),
    # ---------------- 2 cum filtrează
    dict(v='face', tint=1.0, lb=[('Catalizatorul (DOC)', (XM - 14.0, 0.0, 26.0), 'L', 0.07, 0.2), ('Dopuri ceramice', (XM + 9.9, 0.0, -3.0), 'R', 0.74, 0.45),
                                 ('Canale închise alternativ', (XM - 9.0, 0.0, -22.0), 'L', 0.92, 0.6)],
         cap=('FILTRUL · CARBURĂ DE SILICIU', 'Canale închise alternativ: unul are dop la ieșire, vecinul lui are dop la intrare.')),
    dict(v='maca', tint=1.0, arrows=1.0, lb=[('Canal de intrare', (X_IN, 0.0, -10.5), 'L', 0.70, 0.15), ('Dop', (X_OUT, 0.0, -3.0), 'R', 0.31, 0.3),
                                             ('Perete poros', (X_WALL, 0.0, -8.5), 'L', 0.555, 0.5), ('Canal de ieșire', (X_OUT, 0.0, -13.5), 'R', 0.877, 0.7)],
         cap=('GAZELE TREC PRIN PERETE', 'Canalul de intrare e închis la capăt. Singura cale e prin peretele poros.')),
    dict(v='maca', tint=1.0, arrows=1.0, soot=(0.0, 1.0, 0.1, 0.85), specks=1.0, lb=[('Strat de funingine', (CELLS[J_IN][0] + 0.12, 0.0, -12.0), 'L', 0.80, 0.5)],
         cap=('FUNINGINEA RĂMÂNE ÎN FILTRU', 'Nu trece prin perete. Se așază strat peste strat în canalul de intrare.')),
    dict(v='macb', tint=1.0, arrows=1.0, soot=1.0, lb=[('Dop', (X_IN, 0.0, DPF_Z0 + 3.0), 'L', 0.785, 0.3), ('Gaze filtrate, spre ieșire', (X_OUT, 0.0, DPF_Z0 + 2.0), 'R', 0.86, 0.45),
                                                       ('Peste 95 % din particule\nrămân în canalele de intrare', (X_IN, 0.0, DPF_Z0 + PLUG + 9.0), 'L', 0.20, 0.12)],
         cap=('PESTE 95 % DIN PARTICULE', 'La un filtru bun, țeava de evacuare e curată pe dinăuntru.')),
    # ---------------- 3 cum se încarcă
    dict(v='can', soot=(0.1, 1.0), dp=(0.12, 1.0), pan=('dp', {}), note='ilu', cap=('FILTRUL SE ÎNCARCĂ', 'Gazele trec mai greu, iar presiunea dinaintea filtrului crește.')),
    dict(v='right', soot=1.0, dp=1.0, pul=1.0, hl=[('Dps', .3, .9)], note='ilu', pan=('soot2', dict(m=(3.0, 21.0, 0.25, 0.8), c=None, sub='din presiunea diferențială și din debitul de gaze')),
         cap=('FUNINGINEA MĂSURATĂ', 'Calculatorul o scoate din presiunea diferențială și din debitul de gaze.')),
    dict(v='right', soot=1.0, dp=1.0, pul=1.0, note='ilu', pan=('soot2', dict(m=21.0, c=(2.0, 19.6, 0.2, 0.8), sub='model: cât a produs motorul (injecție, aer, EGR) minus cât s-a ars')),
         cap=('FUNINGINEA CALCULATĂ', 'Un model adună cât a produs motorul și scade cât s-a ars pe drum.')),
    dict(v='right', soot=1.0, dp=1.0, pul=1.0, note='ilu', pan=('soot2', dict(m=21.0, c=19.6, ok='apropiate: sistem sănătos')),
         cap=('PE TESTER: AMÂNDOUĂ, ÎN GRAME', 'La un sistem sănătos, merg aproape una de alta.')),
    # ---------------- 4 senzorii
    dict(v='top', soot=0.25, dp=0.3, hl=[('L', 'sonda', .95)], lb=[('Sondă lambda', 'lam', 'R', 0.10, 0.2)],
         cap=('SONDA LAMBDA', 'Măsoară oxigenul din gaze. După ea, calculatorul corectează injecția și EGR-ul.')),
    dict(v='top', soot=0.25, hl=[('T1', .1, .95)], lb=[('Senzor de temperatură 1\nînainte de DOC', 't1', 'L', 0.60, 0.15)],
         cap=('TEMPERATURA ÎNAINTE DE DOC', 'Arată dacă DOC-ul e destul de cald ca să primească motorină.')),
    dict(v='mid', soot=0.25, hl=[('T2', .1, .95)], lb=[('Senzor de temperatură 2\nîntre DOC și filtru', 't2', 'L', 0.26, 0.15)],
         cap=('TEMPERATURA ÎNAINTE DE FILTRU', 'După ea se reglează regenerarea.')),
    dict(v='bot', soot=0.25, hl=[('T3', .1, .95)], lb=[('Senzor de temperatură 3\ndupă filtru', 't3', 'L', 0.30, 0.15)],
         cap=('TEMPERATURA DUPĂ FILTRU', 'Arată cum arde funinginea și păzește filtrul de supraîncălzire.')),
    dict(v='right', soot=0.25, pul=1.0, hl=[('Pipe', 'doua', 'masoara'), ('Hose', 'una', .95), ('Dps', 'masoara', .98)],
         lb=[('Priză de presiune\nînainte de filtru', 'p1', 'R', 0.50, 'una'), ('Priză de presiune\ndupă filtru', 'p2', 'R', 0.90, 'dupa'), ('Senzor de presiune\ndiferențială', 'dps', 'R', 0.05, 0.08)],
         cap=('SENZORUL DE PRESIUNE DIFERENȚIALĂ', 'Două țevi: una înainte de filtru, una după. Măsoară diferența dintre ele.')),
    dict(v='dps', soot=0.25, pul=1.0, onep=1.0, lb=[('O singură țeavă:\ncea dinainte de filtru', 'pipe1', 'L', 0.66, 0.25), ('Cealaltă parte:\npresiunea de afară', 'dps', 'R', 0.06, 0.55),
             ('Țeava de după filtru\nlipsește', 'pipe2x', 'R', 0.80, 0.4)],
         cap=('VARIANTA CU O SINGURĂ ȚEAVĂ', 'La unele modele, senzorul compară presiunea dinaintea filtrului cu presiunea de afară.')),
    dict(v='right', pul=1.0, soot=(0.1, 1.0, 0.3, 0.9), dp=(0.12, 1.0, 0.3, 0.9), note='ilu', pan=('dp', dict(volt=True)),
         cap=('CURAT: DIFERENȚĂ MICĂ · PLIN: DIFERENȚĂ MARE', 'Diferență mai mare înseamnă tensiune mai mare spre calculator.')),
    # ---------------- 5 regenerarea
    dict(v='can', soot=(0.85, 0.5), dp=(0.85, 0.5), heat=0.2, docglow=0.3, temps=(390, 420, 400), note='ilu',
         cap=('REGENERAREA PASIVĂ', 'Pe drum lung, la 350–500 °C, funinginea arde încet, fără nicio comandă.')),
    dict(v='can', soot=(0.5, 1.0, 0.0, 0.7), dp=(0.5, 1.0, 0.0, 0.7), heat=0.0, temps=(250, 230, 210), note='ilu', pan=('thr', dict(val=(9.0, 19.0, 0.0, 0.7), act=True)),
         cap=('REGENERAREA ACTIVĂ', 'Pornește când încărcarea trece de prag. Exemplu 2.0 TDI: în jur de 18 g.')),
    dict(v='can', soot=1.0, dp=1.0, heat=(0.0, 0.35), docglow=0.5, dpfglow=0.3, temps=((250, 440), (230, 410), (210, 340)), note='ilu', pan=('inj', dict(s1=(0.0, 1.0, 0.05, 0.75), s2=0.0)),
         cap=('CE FACE MOTORUL', 'Închide EGR-ul, strânge clapeta de admisie și întârzie injecția principală.')),
    dict(v='doc', soot=1.0, dp=1.0, chem='fuel', fuel=1.0, heat=(0.35, 1.0), pan=('inj', dict(s1=1.0, s2=(0.0, 1.0, 0.1, 0.5))),
         cap=('POST-INJECȚII TÂRZII', 'Motorina nu mai arde în cilindru. Pleacă pe evacuare și arde în DOC.')),
    dict(v='can', soot=1.0, heat=1.0, fuel=1.0, front=(ZF, -64.0), dp=(1.0, 0.62), temps=(450, (540, 635), (400, 560)), note='ilu', flb=True,
         cap=('600–650 °C ÎNAINTE DE FILTRU', 'Funinginea se aprinde și arde în 10–15 minute.')),
    dict(v='can', soot=(1.0, 0.0, 0.86, 1.0), heat=(1.0, 0.0, 0.72, 1.0), fuel=(1.0, 0.0, 0.5, 0.8), front=(-64.0, DPF_Z0 - 30.0, 0.0, 0.78), dp=(0.62, 0.12, 0.0, 0.78),
         temps=((450, 330, .6, 1), (635, 360, .6, 1), (560, 380, .7, 1)), note='ilu', flb=True, pan=('dp', {}),
         cap=('DIFERENȚA DE PRESIUNE SCADE', 'Calculatorul oprește post-injecția.')),
    dict(v='wide', pan=('card', dict(title='CONDIȚII PENTRU REGENERARE', items=[('ok', 'Motor cald'), ('ok', 'Drum destul de lung'), ('ok', 'Nicio eroare care blochează regenerarea')],
                                     at=['motor', 'drum', 'nicio'])), cap=('ÎI TREBUIE CONDIȚII', '')),
    dict(v='wide', soot=(0.3, 1.0), dp=(0.3, 1.0), pan=('card', dict(title='REGENERARE ÎNTRERUPTĂ MEREU', items=[('bad', 'Motorina din post-injecție ajunge în ulei'), ('bad', 'Nivelul uleiului crește'),
                                                                                                             ('bad', 'Filtrul rămâne plin')], at=['motorina', 'nivelul', 'iar'])),
         cap=('REGENERĂRI ÎNTRERUPTE', '')),
    # ---------------- 6 cenușa
    dict(v='macb', tint=1.0, arrows=1.0, soot=0.0, dp=0.3, ash=(0.0, 7.0, 0.1, 0.9), ashfall=1.0, note='ilu',
         lb=[('Cenușă', (X_IN, 0.0, DPF_Z0 + PLUG + 2.6), 'L', 0.31, 0.5), ('Dop', (X_IN, 0.0, DPF_Z0 + 3.0), 'L', 0.785, 0.2)],
         cap=('CENUȘA NU ARDE', 'Vine din aditivii uleiului ars în motor și se strânge la capătul canalelor de intrare.')),
    dict(v='can', ash=7.0, ashw=(6.0, 60.0), soot=0.45, note='ilu', pan=('cycles', {}), lb=[('Cenușă', (44.0, 0.0, DPF_Z0 + 16.0), 'R', 0.80, 0.3)],
         cap=('TOT MAI PUȚIN LOC', 'Regenerările se îndesesc. La sfârșit, filtrul trebuie curățat profesional sau înlocuit.')),
    dict(v='can', ash=7.0, ashw=60.0, soot=0.45, pan=('card', dict(title='CONSUM DE ULEI = CENUȘĂ MULTĂ', items=[('dot', 'Turbina'), ('dot', 'Semeringurile de supape'), ('dot', 'Epuratorul')],
                                                                 at=['turbina', 'semeringurile', 'epurator'])),
         lb=[('Cenușă', (44.0, 0.0, DPF_Z0 + 16.0), 'R', 0.80, 0)], cap=('MOTORUL CARE CONSUMĂ ULEI', 'Umple filtrul de cenușă mult mai repede.')),
    # ---------------- 7 erorile de încărcare
    dict(v='can', ash=0.0, ashw=0.0, soot=1.0, dp=1.0, pan=('codes', dict(title='ERORI DE ÎNCĂRCARE · coduri generice', rows=[('P2463', 'încărcare cu funingine'), ('P242F', 'încărcare cu cenușă'),
                                                                                                                         ('P2458 · P2459', 'durata / frecvența regenerării'),
                                                                                                                         ('P244B', 'presiune diferențială prea mare')])),
         cap=('ERORILE DE ÎNCĂRCARE', '„În filtru e mai multă funingine decât am voie.” Întrebarea corectă e: de ce?')),
    dict(v='wide', soot=1.0, dp=1.0, hl=[('T1', 'senzor', 'sau'), ('T2', 'senzor', 'sau'), ('T3', 'senzor', 'sau')],
         pan=('card', dict(title='1 · REGENERAREA N-A PUTUT MERGE', items=[('dot', 'Drumuri scurte'), ('dot', 'Termostat blocat deschis'), ('dot', 'Bujii arse'), ('dot', 'Senzor de temperatură defect'),
                                                                         ('dot', 'DOC obosit: nu mai încălzește')], at=['drumuri', 'termostat', 'bujii', 'senzor', 'doc'])),
         cap=('PRIMA VARIANTĂ', '')),
    dict(v='wide', soot=1.0, dp=1.0, smoke=1.0, note='sim',
         pan=('card', dict(title='2 · MOTORUL SCOATE PREA MULTĂ FUNINGINE', items=[('dot', 'Injectoare care picură'), ('dot', 'EGR blocat deschis'), ('dot', 'Pierderi de aer pe admisie'),
                                                                                 ('dot', 'Turbină care nu mai dă presiune')], at=['injectoare', 'egr', 'pierderi', 'turbina'])),
         cap=('A DOUA', '')),
    dict(v='right', soot=1.0, dp=1.0, pul=1.0, hl=[('Hose', 'furtunas', 'apa'), ('Pipe', 'apa', 'senzor'), ('Dps', 'senzor', .98)],
         pan=('card', dict(title='3 · MĂSURĂTOAREA MINTE', items=[('dot', 'Furtunaș înfundat sau fisurat'), ('dot', 'Apă în țevi'), ('dot', 'Senzor decalibrat')], at=['furtunas', 'apa', 'senzor'])),
         cap=('A TREIA', '')),
    dict(v='macb', tint=1.0, arrows=0.5, soot=1.0, dp=1.0, ash=7.0, note='ilu',
         pan=('card', dict(title='4 · FILTRUL E PLIN DE CENUȘĂ', items=[('dot', 'Presiunea e mare'), ('dot', 'Nu mai are ce să ardă'), ('dot', 'Regenerează des și degeaba')],
                           at=['presiunea', 'dar', 'regenera'])),
         cap=('A PATRA', '')),
    dict(v='dps', soot=1.0, dp=1.0, hl=[('Dps', 'senzorul', .98)], pan=('zero', {}), cap=('PRIMA VERIFICARE', 'Contact pus, motor oprit: senzorul de presiune trebuie să arate zero.')),
    dict(v='can', soot=1.0, dp=1.0, note='ilu', pan=('soot2', dict(m=38.0, c=17.0, bad='măsurată mult peste calculată', sub='→ măsurătoarea · cenușa · un motor care scoate mai multă funingine decât crede calculatorul')),
         cap=('APOI COMPARAȚI VALORILE', 'Măsurată mult peste calculată: măsurătoarea, cenușa sau motorul.')),
    dict(v='can', soot=1.0, dp=1.0, note='ilu', pan=('soot2', dict(m=37.0, c=38.6, bad='amândouă mari și apropiate', sub='→ filtrul chiar e plin: trebuie aflat ce a oprit regenerările')),
         cap=('AMÂNDOUĂ MARI ȘI APROPIATE', 'Filtrul chiar e plin. Regenerările n-au mers.')),
    dict(v='can', soot=1.0, dp=1.0, crack=(0.0, 1.0, 0.76, 0.95), heat=(0.0, 0.9, 0.66, 0.85), docglow=0.0, note='sim', pan=('thr', dict(val=(30.0, 47.5, 0.05, 0.6), lim=True)),
         cap=('ATENȚIE LA LIMITE · EXEMPLU 2.0 TDI', 'Peste ≈ 40 g: regenerare doar în service. Peste ≈ 45 g: filtrul se înlocuiește.')),
    # ---------------- 8 erorile de eficiență
    dict(v='can', soot=0.25, dp=0.3, crack=0.0, heat=0.0, pan=('codes', dict(title='ERORI DE EFICIENȚĂ · coduri generice', rows=[('P2002', 'eficiența filtrului sub prag'), ('P244A', 'presiune diferențială prea mică')])),
         cap=('ERORILE DE EFICIENȚĂ', 'P2002 înseamnă: filtrul nu mai reține cât trebuie.')),
    dict(v='right', soot=0.25, pul=1.0, note='ilu', pan=('dpx', dict(mea=0.60)), cap=('CALCULATORUL JUDECĂ DUPĂ PRESIUNE', 'La un anumit debit de gaze, un filtru întreg trebuie să opună o anumită rezistență.')),
    dict(v='right', soot=0.25, pul=1.0, note='ilu', pan=('dpx', dict(mea=(0.60, 0.15, 0.1, 0.55), fault=True)),
         cap=('MĂSURATĂ MULT SUB CEA AȘTEPTATĂ', 'Mai multe drumuri la rând: concluzia lui e că gazele trec prea ușor.')),
    dict(v='can', soot=0.25, crack=(0.0, 1.0, 0.1, 0.5), note='sim', lb=[('Fisură: funinginea trece mai departe', (-17.0, 0.0, -104.0), 'L', 0.66, 0.5)],
         cap=('CAUZA POATE FI CHIAR FILTRUL', 'Crăpat sau topit după o regenerare scăpată de sub control, ori golit.')),
    dict(v='wide', soot=0.25, crack=0.0, leakf=(0.0, 1.0, 'scapare', 0.3), leakh=(0.0, 1.0, 'furtunasul', 0.3), hl=[('Hose1', 'furtunasul', 'sau'), ('Dps', 'senzor', .98)], note='sim',
         pan=('card', dict(title='PRESIUNEA E FALSĂ', items=[('dot', 'Scăpare pe evacuare înainte de filtru'), ('dot', 'Furtunașul dinainte de filtru fisurat'), ('dot', 'Senzor care arată prea puțin')],
                           at=['scapare', 'furtunasul', 'senzor'])),
         cap=('LA FEL DE DES: PRESIUNEA E FALSĂ', '')),
    dict(v='wide', soot=0.25, note='sch', pan=('lpegr', dict(st=0.0)), cap=('SAU DEBITUL E SOCOTIT GREȘIT', '2.0 Euro 6 (VAG): cel mai des, răcitorul EGR de joasă presiune înfundat.')),
    dict(v='wide', soot=0.25, note='sch', pan=('lpegr', dict(st=(0.0, 1.0, 0.05, 0.4))), cap=('MAI PUȚIN GAZ DECÂT CREDE CALCULATORUL', 'Presiunea iese prea mică, deși filtrul e bun.')),
    dict(v='bot', soot=0.25, note='sch', pan=('pm', {}), cap=('SENZORUL DE PARTICULE', 'Funinginea scăpată se așază între doi electrozi. Dacă se adună prea repede, filtrul nu mai reține.')),
    dict(v='bot', soot=0.25, note='sch', pan=('pipe2', {}), cap=('PROBA CEA MAI SIMPLĂ', 'Uitați-vă în țeava de evacuare.')),
    # ---------------- 9 ordinea de lucru
    dict(v='wide', soot=0.25, pan=('steps', dict(cur=0)), cap=('ORDINEA DE LUCRU', '')),
    dict(v='wide', soot=0.25, pan=('steps', dict(cur=1)), cap=('ORDINEA DE LUCRU', '')),
    dict(v='wide', soot=0.25, pul=1.0, hl=[('Hose', .12, .95), ('Pipe', .12, .95), ('Dps', .12, .95)], pan=('steps', dict(cur=2)), cap=('ORDINEA DE LUCRU', '')),
    dict(v='wide', soot=0.25, pan=('steps', dict(cur=3)), cap=('ORDINEA DE LUCRU', '')),
    dict(v='wide', soot=0.25, pan=('steps', dict(cur=4)), cap=('ORDINEA DE LUCRU', '')),
    dict(v='wide', soot=0.0, pan=('final', {}), cap=('', '')),
]
assert len(SH) == N, (len(SH), N)

# ------------------------------------------------------------------ timeline (from the measured narration)
_MP = os.path.join(HERE, 'vo', 'meas.json'); MEAS = json.load(open(_MP)) if os.path.exists(_MP) else {}
_WP = os.path.join(HERE, 'vo', 'words.json'); WORDS = json.load(open(_WP)) if os.path.exists(_WP) else {}


def sp(i): return MEAS[str(i)]['sp'] if str(i) in MEAS else len(SC.SAY[i]) / 16.1


CHS = [i for i, _ in SC.CH]
T0, GAP, CHGAP, LEAD = 1.3, 0.42, 1.05, 0.28
CUE = []; _t = T0
for _i in range(N):
    if _i > 0: _t += CHGAP if _i in CHS else GAP
    CUE.append(_t); _t += sp(_i)
T_END = _t; OUT0 = T_END + 1.0; DUR = OUT0 + 4.2
SS = [0.0] + [CUE[i] - LEAD for i in range(1, N)]; SE = SS[1:] + [OUT0]
NF = int(round(DUR * FPS))


def wt(i, key, default=None):
    """seconds from the start of line i to the first word that starts with `key` (number = fraction of the line)."""
    if isinstance(key, (int, float)): return key * sp(i)
    for w, t in WORDS.get(str(i), []):
        if w.startswith(key): return max(0.0, t)
    return default


def shot_at(t):
    lo, hi = 0, N - 1
    while lo < hi:
        m = (lo + hi + 1) // 2
        if SS[m] <= t: lo = m
        else: hi = m - 1
    return lo


DEF = dict(rev=1.0, flow=1.0, soot=0.0, tint=0.0, heat=0.0, ash=0.0, ashw=0.0, ashfall=0.0, dp=0.12, pul=0.0, onep=0.0, smoke=0.0, crack=0.0, fuel=0.0, cold=0.0,
           chem_a=0.0, arrows=0.0, specks=0.0, leakf=0.0, leakh=0.0, docglow=1.0, dpfglow=1.0, hi=0.0)
TRK = dict(rev=1.4, hi=0.6, soot=1.0, tint=0.8)
RES = {}
for _k in DEF:
    prev = DEF[_k]; RES[_k] = []
    for _i, s in enumerate(SH):
        x = s.get(_k, DEF[_k])
        if _k == 'hi': x = 1.0 if ('pan' in s and FMT == 'V') else 0.0
        if isinstance(x, tuple):
            a, b = x[0], x[1]; f0 = x[2] if len(x) > 2 else 0.0; f1 = x[3] if len(x) > 3 else 1.0
            if isinstance(f0, str):                       # starts at a spoken word, lasts f1 seconds
                w0 = wt(_i, f0, 0.3 * sp(_i)) + LEAD; d = SE[_i] - SS[_i]; f0, f1 = w0 / d, min(1.0, (w0 + x[3]) / d)
            RES[_k].append(('anim', a, b, f0, f1, prev)); prev = b
        else:
            RES[_k].append(('to', prev, float(x), 0.0, 1.0, prev)); prev = float(x)


def sval(k, t, i=None):
    if i is None: i = shot_at(t)
    kind, a, b, f0, f1, pe = RES[k][i]; tl = t - SS[i]
    if kind == 'to': return lerp(a, b, sm(tl / TRK.get(k, 0.9)))
    f = tl / (SE[i] - SS[i]); v = lerp(a, b, sm((f - f0) / max(1e-6, f1 - f0)))
    return lerp(pe, v, sm(tl / 0.5)) if abs(pe - a) > 1e-6 else v


def pv(x, f):
    """panel / temperature parameter: number, or (a, b[, f0, f1]) animated over the shot."""
    if isinstance(x, tuple):
        f0 = x[2] if len(x) > 2 else 0.0; f1 = x[3] if len(x) > 3 else 1.0
        return lerp(x[0], x[1], sm((f - f0) / max(1e-6, f1 - f0)))
    return x


def hl_times(i, spec):
    kind, a, b = spec; d = SE[i] - SS[i]
    t0 = SS[i] + (a * d if isinstance(a, (int, float)) else LEAD + wt(i, a, 0.2 * sp(i)) - 0.15)
    t1 = SS[i] + (b * d if isinstance(b, (int, float)) else LEAD + wt(i, b, 0.9 * sp(i)) - 0.1)
    return kind, t0, max(t1, t0 + 0.8)


HLT = [[hl_times(i, s_) for s_ in s.get('hl', [])] for i, s in enumerate(SH)]


def state(t):
    i = shot_at(t); s = SH[i]; f = (t - SS[i]) / (SE[i] - SS[i])
    S = {k: sval(k, t, i) for k in DEF}
    S['t'] = t; S['ft'] = t; S['ct'] = chan_time(t); S['i'] = i; S['f'] = f
    S['chem'] = s.get('chem')
    if S['chem'] is None and i > 0 and t - SS[i] < 0.5: S['chem'] = SH[i - 1].get('chem')
    if S['chem'] in ('ox', 'no2'):                      # the molecule tags fade between two different reactions
        if i > 0 and SH[i - 1].get('chem') in ('ox', 'no2') and SH[i - 1].get('chem') != S['chem']: S['chem_a'] *= ramp(t, SS[i] + 0.05, 0.4)
        if i + 1 < N and SH[i + 1].get('chem') != S['chem']: S['chem_a'] *= 1 - ramp(t, SE[i] - 0.4, 0.35)
    fr = s.get('front'); S['front'] = None if fr is None else pv(fr, f)
    h = {}
    for j in (i - 1, i):
        if j < 0: continue
        for kind, t0, t1 in HLT[j]:
            a = ramp(t, t0, 0.25) * (1 - ramp(t, t1, 0.6)) * (0.82 + 0.18 * math.sin(t * 5.0))
            if a > 0.01: h[kind] = max(h.get(kind, 0.0), a)
    S['hl'] = h
    return S


# ------------------------------------------------------------------ camera
def _vkey(i): return (SH[i]['v'], 1 if ('pan' in SH[i] and FMT == 'V') else 0)


GRP = []
for _i in range(N):
    if _i == 0 or _vkey(_i) != _vkey(_i - 1): GRP.append([_i, _i])
    else: GRP[-1][1] = _i
PRE = 0.35


def gview(g, t):
    a, b = GRP[g]; name, hi = _vkey(a); u = cl((t - SS[a]) / (SE[b] - SS[a]))
    return zoomed(VIEWS[hi][name], 1.0 + (0.03 if name.startswith('mac') else 0.045) * u)


def cam(t):
    """-> (view, view2, mix): view2 is set while one view dissolves into the next."""
    g = 0
    for k in range(len(GRP)):
        if SS[GRP[k][0]] - PRE <= t: g = k
    Vc = gview(g, t)
    if g == 0: return Vc, None, 0.0
    gs = SS[GRP[g][0]]; Vp = gview(g - 1, gs)
    r = abs(math.log(Vc[0] / Vp[0]))
    dist = math.hypot(Vc[1] - Vp[1], Vc[2] - Vp[2]) * min(Vc[0], Vp[0]) / W
    if r > math.log(5.0):
        m = sm((t - (gs - 0.30)) / 0.6)
        return (Vc, None, 0.0) if m >= 0.999 else (Vp, Vc, m)
    mv = 1.0 + 0.6 * r + 0.35 * min(1.5, dist)
    return interp_view(Vp, Vc, sm((t - (gs - PRE)) / mv)), None, 0.0


def chan_speed(z): return max(4.4, min(11.0, 330.0 / (z * E.PXMM)))


_CS = None


def chan_time(t):
    global _CS
    if _CS is None:
        v = []
        for k in range(NF + 2):
            a, b, m = cam(k / FPS); v.append(chan_speed((b if (b is not None and m > 0.5) else a)[0]) / 5.0 / FPS)
        _CS = np.concatenate([[0], np.cumsum(v)])
    return float(_CS[min(len(_CS) - 1, max(0, int(round(t * FPS))))])


# ------------------------------------------------------------------ UI pieces
def wrap_lines(text, size, name, maxw):
    out = []
    for para in text.split('\n'):
        cur = ''
        for wd in para.split():
            cand = (cur + ' ' + wd).strip()
            if tw(cand, size, name) > maxw and cur: out.append(cur); cur = wd
            else: cur = cand
        out.append(cur)
    return out


def tick(c, x, y, s, col, a, w=None):
    c.drawPath(path_of([(x - s * 0.5, y), (x - s * 0.12, y + s * 0.38), (x + s * 0.55, y - s * 0.42)]), P(col, a, stroke=w or s * 0.24, join='miter'))


def cross(c, x, y, s, col, a, w=None):
    c.drawLine(x - s * 0.42, y - s * 0.42, x + s * 0.42, y + s * 0.42, P(col, a, stroke=w or s * 0.24)); c.drawLine(x - s * 0.42, y + s * 0.42, x + s * 0.42, y - s * 0.42, P(col, a, stroke=w or s * 0.24))


def background(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), P(shader=lin(0, 0, 0, H, ['#0e1a2c', '#060b14'])))
    cx, cy = (R_FULL[0] + R_FULL[2]) / 2, H * 0.45
    R = max(W, H) * 0.62
    c.drawCircle(cx, cy, R, P(shader=rad(cx, cy, R, [skia.Color4f(.13, .21, .34, .55).toColor(), skia.Color4f(0, 0, 0, 0).toColor()])))
    c.save(); c.rotate(-20, W / 2, H / 2)
    f = font('anton', 58); s = 'TURBO DOCTOR'; w = f.measureText(s) + 120; off = (t * 9) % w
    for row in range(-16, 26):
        yy = row * 110; sh = (row % 2) * w / 2
        for k in range(-4, 9):
            x = -600 + k * w + sh + off
            col = (1, 1, 1, .04) if (row + k) % 3 else (1, .76, .1, .052)
            c.drawString(s, x, yy, f, P(col[:3], col[3]))
    c.restore()


def watermark_over(c, t, a):
    """in the close-ups the plates cover the whole frame, so the mark goes over them, very faint."""
    if a <= 0.01: return
    c.save()
    if FMT == 'H': c.clipRect(skia.Rect.MakeLTRB(0, 0, R_FULL[2] + 20, H))
    c.rotate(-20, W / 2, H / 2)
    f = font('anton', 58); s = 'TURBO DOCTOR'; w = f.measureText(s) + 120; off = (t * 9) % w
    pw, pk = P('#ffffff', 0.034 * a), P('#000000', 0.040 * a)
    for row in range(-16, 26):
        yy = row * 110; sh = (row % 2) * w / 2
        for k in range(-4, 9):
            x = -600 + k * w + sh + off
            c.drawString(s, x + 2, yy + 2, f, pk); c.drawString(s, x, yy, f, pw)
    c.restore()


_K = lambda a: skia.Color4f(0.02, 0.04, 0.07, a).toColor()


def bands(c, hi):
    if FMT == 'V':
        c.drawRect(skia.Rect.MakeLTRB(0, 0, W, 250), P(shader=lin(0, 0, 0, 250, [_K(0.95), _K(0.86), _K(0.0)], [0.0, 0.66, 1.0])))
        yb = lerp(R_FULL[3], R_HI[3], hi)
        c.drawRect(skia.Rect.MakeLTRB(0, yb - 70, W, H), P(shader=lin(0, yb - 70, 0, yb + 40, [_K(0.0), _K(0.94)])))
    else:
        x0 = R_FULL[2] - 16
        c.drawRect(skia.Rect.MakeLTRB(x0, 0, W, H), P(shader=lin(x0, 0, x0 + 70, 0, [_K(0.0), _K(0.97)])))


CH_T = [SS[i] for i in CHS] + [OUT0]


def header(c, t):
    k = 0
    for j in range(len(CHS)):
        if t >= CH_T[j] - 0.2: k = j
    a_in = ramp(t, CH_T[k] - 0.2, 0.4) if k > 0 else 1.0
    a_out = 1 - ramp(t, CH_T[k + 1] - 0.5, 0.3) if k + 1 < len(CHS) else 1.0
    a = a_in * a_out
    if FMT == 'V': x0, x1, yb, yc, cs, ybar = 60, 1020, 62, 138, 52, 172
    else: x0, x1, yb, yc, cs, ybar = 1076, 1880, 66, 136, 46, 166
    w = txt(c, 'TURBO', x0, yb, 30, 'anton', WHT, 1.0); w += txt(c, 'DOCTOR', x0 + w + 6, yb, 30, 'anton', Y, 1.0)
    txt(c, 'TRAINING INTERN', x0 + w + 26, yb - 2, 19, 'm8', WHT, 0.72)
    if FMT == 'V': txt(c, 'MODEL 3D RECONSTRUIT', x1, yb - 2, 17, 'm8', WHT, 0.42, 'r')
    else: txt(c, 'MODEL 3D RECONSTRUIT', 40, H - 28, 17, 'm8', WHT, 0.42)
    s_ = f'{k + 1} · {SC.CH[k][1]}'
    txt(c, s_, x0 + 14 * (1 - a_in), yc, cs, 'anton', WHT, a, shadow=8)
    # progress: one segment per chapter
    tot = OUT0; gap = 5; xw = x1 - x0
    for j in range(len(CHS)):
        xa = x0 + xw * CH_T[j] / tot + (gap / 2 if j else 0); xb = x0 + xw * CH_T[j + 1] / tot - gap / 2
        rrect(c, xa, ybar, xb, ybar + 7, 3.5, P('#ffffff', 0.16))
        fr = cl((t - CH_T[j]) / (CH_T[j + 1] - CH_T[j]))
        if fr > 0: rrect(c, xa, ybar, xa + (xb - xa) * fr, ybar + 7, 3.5, P(Y, 0.95 if j == k else 0.55))


def label(c, text, ax, ay, side, ly, a, R, col=WHT, size=None, dot=Y):
    if a <= 0.01: return
    size = size or (27 if FMT == 'V' else 24)
    lines = text.split('\n'); tw_ = max(tw(s_, size, 'm8') for s_ in lines); lh = size * 1.22
    bh = size * 1.34 + lh * (len(lines) - 1)
    x0 = R[0] + 18 if side == 'L' else R[2] - 18 - tw_ - 28
    y0 = max(R[1] + 6, min(R[3] - bh - 6, ly - bh / 2))
    c.drawCircle(ax, ay, 6, P(dot, a)); c.drawCircle(ax, ay, 12, P(dot, a * 0.35, stroke=2))
    ex = x0 if ax < x0 else (x0 + tw_ + 28 if ax > x0 + tw_ + 28 else ax)
    ey = y0 + bh / 2 if (ax < x0 or ax > x0 + tw_ + 28) else (y0 if ay < y0 else y0 + bh)
    c.drawPath(path_of([(ax, ay), (ex, ey)]), P(dot, a * 0.85, stroke=2.4))
    rrect(c, x0, y0, x0 + tw_ + 28, y0 + bh, 12, P('#0b1424', a * 0.9))
    rrect(c, x0, y0, x0 + tw_ + 28, y0 + bh, 12, P(dot, a * 0.55, stroke=2))
    for k, s_ in enumerate(lines): txt(c, s_, x0 + 14, y0 + size * 1.0 + k * lh, size, 'm8', col, a)


def _lbkey(l): return (l[0], str(l[1]))


def labels(c, t, V):
    for i in (shot_at(t) - 1, shot_at(t)):
        if i < 0 or t > SE[i] + 0.1: continue
        s = SH[i]; R = R_HI if ('pan' in s and FMT == 'V') else R_FULL
        nxt = {_lbkey(l) for l in SH[i + 1].get('lb', [])} if i + 1 < N else set()
        prv = {_lbkey(l) for l in SH[i - 1].get('lb', [])} if i > 0 else set()
        for l in s.get('lb', []):
            text, key, side, yf, at = l[0], l[1], l[2], l[3], (l[4] if len(l) > 4 else 0.2)
            t0 = SS[i] + LEAD + (wt(i, at, 0.3 * sp(i)) if isinstance(at, str) else at * sp(i)) - 0.1
            a = 1.0 if _lbkey(l) in prv else ramp(t, t0, 0.3)
            if _lbkey(l) not in nxt: a *= 1 - ramp(t, SE[i] - 0.5, 0.3)
            elif t > SE[i]: continue
            if a <= 0.01: continue
            ax, ay = anchor(V, p3=key) if isinstance(key, tuple) else anchor(V, key)
            label(c, text, ax, ay, side, R[1] + yf * (R[3] - R[1]), a, R)
        if s.get('flb'):                                   # the label that follows the burning front
            fr = pv(s['front'], (t - SS[i]) / (SE[i] - SS[i]))
            if DPF_Z0 + 4.0 < fr < DPF_Z1 - 4.0:
                ax, ay = anchor(V, p3=(-56.0, 0.0, fr))
                label(c, 'Funinginea arde', ax, ay, 'L', ay + 4, cl((DPF_Z1 - 4.0 - fr) / 8.0) * cl((fr - DPF_Z0 - 44.0) / 14.0), R)


def tcol(v): return mix(mix('#8fd0ff', '#ffffff', cl((v - 200) / 150.0)), '#ff6a2a', cl((v - 380) / 240.0))


def temps(c, t, V):
    """temperature read-outs next to the three sensors (illustrative values)."""
    i = shot_at(t); s = SH[i]
    if 'temps' not in s: return
    f = (t - SS[i]) / (SE[i] - SS[i]); R = R_HI if ('pan' in s and FMT == 'V') else R_FULL
    a = (1.0 if (i > 0 and 'temps' in SH[i - 1]) else ramp(t, SS[i] + 0.3, 0.4)) * (1.0 if (i + 1 < N and 'temps' in SH[i + 1]) else 1 - ramp(t, SE[i] - 0.45, 0.3))
    if a <= 0.01: return
    sz = 30 if FMT == 'V' else 27
    for k, (key, nm) in enumerate((('t1', 'T1'), ('t2', 'T2'), ('t3', 'T3'))):
        v = pv(s['temps'][k], f); ax, ay = anchor(V, key)
        s_ = f'{int(round(v / 5.0) * 5)} °C'; wd = tw(nm, 20, 'm8') + tw(s_, sz, 'anton') + 44
        x0 = R[0] + 18; y0 = ay - 86 if k < 2 else ay - 96
        col = tcol(v)
        c.drawPath(path_of([(ax, ay), (x0 + wd * 0.6, y0 + 50)]), P(col, a * 0.8, stroke=2.2)); c.drawCircle(ax, ay, 5, P(col, a))
        rrect(c, x0, y0, x0 + wd, y0 + 52, 12, P('#0b1424', a * 0.93)); rrect(c, x0, y0, x0 + wd, y0 + 52, 12, P(col, a * 0.8, stroke=2))
        txt(c, nm, x0 + 14, y0 + 34, 20, 'm8', WHT, a * 0.8); txt(c, s_, x0 + 26 + tw(nm, 20, 'm8'), y0 + 39, sz, 'anton', col, a)


def caption(c, t):
    for i in (shot_at(t) - 1, shot_at(t)):
        if i < 0: continue
        ti, body = SH[i].get('cap', ('', '')) if SH[i].get('pan', ('',))[0] not in BIGP else ('', '')
        _hp = lambda k: FMT == 'H' and ('pan' in SH[k]) != ('pan' in SH[i])
        same_n = bool(ti) and i + 1 < N and SH[i + 1].get('cap', ('', ''))[0] == ti and not _hp(i + 1)
        same_p = bool(ti) and i > 0 and SH[i - 1].get('cap', ('', ''))[0] == ti and not _hp(i - 1)
        a_t = (1.0 if same_p else ramp(t, SS[i] + 0.12, 0.3)) * ((1.0 if t < SE[i] else 0.0) if same_n else 1 - ramp(t, SE[i] - 0.32, 0.3))
        a_b = ramp(t, SS[i] + 0.2, 0.3) * (1 - ramp(t, SE[i] - 0.32, 0.3))
        big = FMT == 'H' and 'pan' not in SH[i]              # 16:9 without a panel: the text has the whole right column
        cy_, ct_, cb_, clh = (CAPY + 150, 60, 37, 52) if big else (CAPY, CAPT, CAPB, CAPLH)
        if ti and a_t > 0.01:
            ts = ct_
            while tw(ti, ts, 'anton') > CAPW and ts > 30: ts -= 2
            txt(c, ti, CAPX, cy_ + (0 if same_p else 14 * (1 - a_t)), ts, 'anton', Y, a_t, shadow=10)
        if body and a_b > 0.01:
            yy = cy_ + ct_ * 1.12 + (8 if big else 0)
            for ln in wrap_lines(body, cb_, 'm7', CAPW):
                txt(c, ln, CAPX, yy, cb_, 'm7', WHT, a_b, shadow=8); yy += clh


LEG = (2, 3, 9, 10, 11, 12)                       # shots that show what the two gas colours mean


def legend(c, t):
    for i in (shot_at(t) - 1, shot_at(t)):
        if i not in LEG: continue
        a = (1.0 if (i - 1) in LEG else ramp(t, SS[i] + 1.0, 0.5)) * ((1.0 if t < SE[i] else 0.0) if (i + 1) in LEG else 1 - ramp(t, SE[i] - 0.4, 0.3))
        if a <= 0.01: continue
        fs = 23 if FMT == 'V' else 21
        x, y = (60, 1568) if FMT == 'V' else (R_PAN[0], R_PAN[3] - 22)
        for col, s_ in ((C_GAS, 'gaze cu funingine'), (C_CLN, 'gaze filtrate')):
            c.drawRoundRect(skia.Rect.MakeXYWH(x, y - 20, 24, 24), 6, 6, P(col, a)); c.drawRoundRect(skia.Rect.MakeXYWH(x, y - 20, 24, 24), 6, 6, P('#ffffff', a * 0.35, stroke=1.5))
            x += 34 + txt(c, s_, x + 34, y, fs, 'm7', WHT, a * 0.9, shadow=6) + 30
        return


NOTES = {'ilu': 'VALORI ILUSTRATIVE', 'sim': 'STARE SIMULATĂ', 'sch': 'DESEN SCHEMATIC'}


def note_tag(c, t):
    i = shot_at(t); n = SH[i].get('note')
    if not n: return
    a = (1.0 if (i > 0 and SH[i - 1].get('note') == n) else ramp(t, SS[i] + 0.3, 0.3)) * (1.0 if (i + 1 < N and SH[i + 1].get('note') == n) else 1 - ramp(t, SE[i] - 0.4, 0.3))
    s_ = NOTES[n]
    if FMT == 'V': x, y = 1020, 222
    else: x, y = R_FULL[2] - 30, R_FULL[1] + 4
    wd = tw(s_, 17, 'm8') + 24
    rrect(c, x - wd, y - 22, x, y + 8, 8, P('#0b1424', a * 0.8)); rrect(c, x - wd, y - 22, x, y + 8, 8, P('#ffffff', a * 0.3, stroke=1.3))
    txt(c, s_, x - 12, y, 17, 'm8', WHT, a * 0.78, 'r')


# ------------------------------------------------------------------ panels
def pbox(c, R, a, title=None, ts=31):
    x0, y0, x1, y1 = R
    rrect(c, x0, y0, x1, y1, 22, P('#0a1322', a * 0.95)); rrect(c, x0, y0, x1, y1, 22, P('#ffffff', a * 0.15, stroke=1.6))
    if title:
        while tw(title, ts, 'anton') > x1 - x0 - 56 and ts > 22: ts -= 1
        txt(c, title, x0 + 28, y0 + 50, ts, 'anton', Y, a)


def ro(v, d=1): return f'{v:.{d}f}'.replace('.', ',')


def pan_card(c, R, a, i, f, tl, p):
    x0, y0, x1, y1 = R; pbox(c, R, a, p['title'], 38 if FMT == 'V' else 34)
    items = p['items']; n = len(items); ats = p.get('at') or [0.2 + 0.6 * k / n for k in range(n)]
    fs = (42 if n <= 3 else (40 if n == 4 else 37)) if FMT == 'V' else (36 if n <= 3 else (34 if n == 4 else 32))
    while True:
        rows = [wrap_lines(s_, fs, 'm7', x1 - x0 - 120) for (kind, s_) in items]
        nl = sum(len(r) for r in rows); lh = fs * 1.3
        if nl * lh + (n - 1) * 8 <= y1 - y0 - 104 or fs <= 22: break
        fs -= 1
    gp = min(46.0, (y1 - y0 - 104 - nl * lh) / max(1, n))
    yy = y0 + 78 + (y1 - y0 - 98 - nl * lh - (n - 1) * gp) / 2 + fs; last = -1
    tts = [LEAD + wt(i, at_, (0.2 + 0.6 * k / n) * sp(i)) - 0.12 for k, at_ in enumerate(ats)]
    for k in range(n):
        if tl >= tts[k]: last = k
    for k, ((kind, s_), ls) in enumerate(zip(items, rows)):
        ai = a * ramp(tl, tts[k], 0.3); cur = k == last
        if ai > 0.01:
            bx, by = x0 + 50, yy - fs * 0.34; dx = 10 * (1 - ramp(tl, tts[k], 0.3))
            if kind == 'ok': c.drawCircle(bx, by, 21, P(GRN, ai * 0.2)); tick(c, bx, by, 27, GRN, ai)
            elif kind == 'bad': c.drawCircle(bx, by, 21, P(RED, ai * 0.2)); cross(c, bx, by, 24, RED, ai)
            else: c.drawCircle(bx, by, 10, P(Y, ai)); c.drawCircle(bx, by, 18, P(Y, ai * (0.35 if cur else 0.0), stroke=2))
            for j, ln in enumerate(ls): txt(c, ln, x0 + 92 + dx, yy + j * lh, fs, 'm7', WHT, ai * (1.0 if cur else 0.82))
        yy += len(ls) * lh + gp


def pan_steps(c, R, a, i, f, tl, p):
    x0, y0, x1, y1 = R; pbox(c, R, a, 'ORDINEA DE LUCRU', 40 if FMT == 'V' else 34)
    cur = p['cur']; fs = 33 if FMT == 'V' else 28; lh = fs * 1.28
    rows = [wrap_lines(s_, fs, 'm7', x1 - x0 - 130) for s_ in STEPS]
    nl = sum(len(r) for r in rows); gp = min(40.0, max(6.0, (y1 - y0 - 110 - nl * lh) / 5.0)); yy = y0 + 118
    for k, ls in enumerate(rows):
        ak = a * (1.0 if k < cur else (ramp(tl, LEAD + 0.5, 0.35) if k == cur else 0.0))
        if ak > 0.01:
            on = k == cur; bx, by = x0 + 54, yy - fs * 0.34
            c.drawCircle(bx, by, 23, P(Y if on else '#22314a', ak)); txt(c, str(k + 1), bx, by + 10, 28, 'm9', BG if on else WHT, ak, 'c')
            for j, ln in enumerate(ls): txt(c, ln, x0 + 98, yy + j * lh, fs, 'm7', WHT, ak * (1.0 if on else 0.6))
        yy += len(ls) * lh + gp


def pan_codes(c, R, a, i, f, tl, p):
    x0, y0, x1, y1 = R; pbox(c, R, a, p['title'])
    rows = p['rows']; n = len(rows); fs = 28 if FMT == 'V' else 25
    rh = min(74.0, (y1 - y0 - 96) / n); yy = y0 + 92 + rh * 0.5
    cw = max(tw(code, fs + 4, 'm9') for code, _ in rows) + 34
    for k, (code, s_) in enumerate(rows):
        ak = a * ramp(tl, 0.5 + 0.45 * k, 0.3)
        rrect(c, x0 + 30, yy - 25, x0 + 30 + cw, yy + 23, 10, P('#1a2740', ak)); rrect(c, x0 + 30, yy - 25, x0 + 30 + cw, yy + 23, 10, P(Y, ak * 0.7, stroke=1.8))
        txt(c, code, x0 + 30 + cw / 2, yy + 10, fs + 4, 'm9', Y, ak, 'c')
        ls = wrap_lines(s_, fs, 'm7', x1 - x0 - cw - 90)
        for j, ln in enumerate(ls): txt(c, ln, x0 + 30 + cw + 24, yy + 10 - (len(ls) - 1) * fs * 0.6 + j * fs * 1.2, fs, 'm7', WHT, ak)
        yy += rh


def pan_dp(c, R, a, i, f, tl, p, S):
    """two bars: pressure before / after the filter; the gap between them is the differential pressure."""
    x0, y0, x1, y1 = R; pbox(c, R, a, 'PRESIUNEA ÎNAINTE ȘI DUPĂ FILTRU'); lv = S['dp']
    volt = p.get('volt'); hh = y1 - y0; ya = y0 + (118 if volt or FMT == 'V' else 150); st = 70 if FMT == 'V' else 86
    lw = 250; bx = x0 + 30 + lw; full = x1 - 40 - bx
    b_after = 0.22 * full; b_before = b_after + (0.05 + 0.62 * lv) * full
    txt(c, 'înainte de filtru', x0 + 30, ya + 10, 26, 'm7', WHT, a * 0.92); txt(c, 'după filtru', x0 + 30, ya + st + 10, 26, 'm7', WHT, a * 0.92)
    rrect(c, bx, ya - 16, bx + b_before, ya + 18, 8, P(C_GAS, a)); rrect(c, bx, ya + st - 16, bx + b_after, ya + st + 18, 8, P(C_CLN, a))
    xa, xb = bx + b_after, bx + b_before; yb = ya + st + 52
    c.drawLine(xa, ya + st + 22, xa, yb + 8, P(Y, a * 0.9, stroke=2.5)); c.drawLine(xb, ya + 22, xb, yb + 8, P(Y, a * 0.9, stroke=2.5))
    c.drawLine(xa, yb, xb, yb, P(Y, a, stroke=3.5))
    for xx, sg in ((xa, 1), (xb, -1)):
        if xb - xa > 26: c.drawPath(path_of([(xx, yb), (xx + sg * 11, yb - 7), (xx + sg * 11, yb + 7)], True), P(Y, a))
    txt(c, 'Δp', (xa + xb) / 2, yb - 12, 30, 'm9', Y, a, 'c', stroke=6, scol='#0a1322')
    if not volt:
        txt(c, 'Diferența dintre ele = presiunea diferențială (Δp).', x0 + 30, y1 - 40, 23 if FMT == 'V' else 20, 'm7', WHT, a * 0.7)
    if volt:
        yv = yb + (74 if FMT == 'V' else 110); u = 0.7 + 3.3 * lv
        txt(c, 'semnal spre calculator', x0 + 30, yv + 10, 26, 'm7', WHT, a * 0.92)
        bx2 = x0 + 30 + 330; fw = x1 - 190 - bx2
        rrect(c, bx2, yv - 14, bx2 + fw, yv + 16, 8, P('#22314a', a)); rrect(c, bx2, yv - 14, bx2 + fw * (u / 5.0), yv + 16, 8, P(Y, a))
        txt(c, ro(u) + ' V', x1 - 36, yv + 14, 40, 'anton', Y, a, 'r')


def pan_dpx(c, R, a, i, f, tl, p):
    """expected (from the gas flow) against measured differential pressure."""
    x0, y0, x1, y1 = R; pbox(c, R, a, 'PRESIUNEA DIFERENȚIALĂ: AȘTEPTATĂ ȘI MĂSURATĂ')
    mea = pv(p['mea'], f); ex = 0.62; st = 84 if FMT == 'V' else 110; ya = y0 + 124
    lw = 290; bx = x0 + 30 + lw; full = x1 - 40 - bx
    bad = p.get('fault') and mea < 0.33
    for k, (nm, sub, v, col) in enumerate((('așteptată', 'din debitul de gaze', ex, '#9fb4cc'), ('măsurată', 'de senzor', mea, RED if bad else C_GAS))):
        yy = ya + k * st
        txt(c, nm, x0 + 30, yy + 4, 28, 'm8', WHT, a); txt(c, sub, x0 + 30, yy + 32, 20, 'm7', WHT, a * 0.6)
        rrect(c, bx, yy - 14, bx + full, yy + 22, 8, P('#1a2740', a)); rrect(c, bx, yy - 14, bx + full * v, yy + 22, 8, P(col, a))
    xm = bx + full * ex * 0.55
    c.drawLine(xm, ya - 26, xm, ya + st + 34, P(WHT, a * 0.55, stroke=2, pe=skia.DashPathEffect.Make([7, 6], 0)))
    txt(c, 'minimul pentru un filtru întreg', xm + 10, ya + st + 62, 20, 'm7', WHT, a * 0.6)
    yv = y1 - 44
    if p.get('fault'):
        ab = a * (1 - ramp(mea, 0.22, 0.12))
        if ab > 0.01:
            s_ = 'P2002 · eficiență sub prag'; wd = tw(s_, 30, 'm9') + 44
            rrect(c, x1 - 30 - wd, yv - 34, x1 - 30, yv + 16, 12, P(RED, ab)); txt(c, s_, x1 - 30 - wd / 2, yv + 2, 30, 'm9', '#ffffff', ab, 'c')
    else:
        tick(c, x1 - 60, yv - 10, 30, GRN, a); txt(c, 'în limite', x1 - 92, yv, 28, 'm8', GRN, a, 'r')


def pan_soot2(c, R, a, i, f, tl, p):
    x0, y0, x1, y1 = R; pbox(c, R, a, 'FUNINGINEA DIN FILTRU, PE TESTER')
    st = 78 if FMT == 'V' else 100; ya = y0 + 122; lw = 190; bx = x0 + 30 + lw; full = x1 - 190 - bx
    for k, (nm, key, col) in enumerate((('măsurată', 'm', C_GAS), ('calculată', 'c', C_CLN))):
        yy = ya + k * st; v = p.get(key)
        on = v is not None; v = pv(v, f) if on else 0.0
        txt(c, nm, x0 + 30, yy + 10, 28, 'm8', WHT, a * (1.0 if on else 0.35))
        rrect(c, bx, yy - 16, bx + full, yy + 20, 8, P('#1a2740', a))
        if on:
            rrect(c, bx, yy - 16, bx + full * min(1.0, v / 50.0), yy + 20, 8, P(col, a))
            txt(c, ro(v) + ' g', x1 - 34, yy + 16, 42, 'anton', col, a, 'r')
    yy = ya + 2 * st - 6
    if p.get('ok'):
        ao = a * ramp(tl, 1.2, 0.4); tick(c, x0 + 46, yy + 16, 30, GRN, ao); txt(c, p['ok'], x0 + 80, yy + 26, 28, 'm8', GRN, ao)
    if p.get('bad'):
        ao = a * ramp(tl, 0.8, 0.4); wd = tw(p['bad'], 26, 'm9') + 36
        rrect(c, x0 + 30, yy - 8, x0 + 30 + wd, yy + 36, 10, P(RED, ao * 0.9)); txt(c, p['bad'], x0 + 30 + wd / 2, yy + 23, 26, 'm9', '#ffffff', ao, 'c'); yy += 54
    if p.get('sub'):
        ao = a * ramp(tl, 1.4 if p.get('bad') else 0.8, 0.4); fs = 24 if FMT == 'V' else 23
        for j, ln in enumerate(wrap_lines(p['sub'], fs, 'm7', x1 - x0 - 60)): txt(c, ln, x0 + 30, yy + 26 + j * fs * 1.3, fs, 'm7', WHT, ao * 0.9)


def pan_thr(c, R, a, i, f, tl, p):
    x0, y0, x1, y1 = R; pbox(c, R, a, 'ÎNCĂRCAREA CU FUNINGINE · exemplu 2.0 TDI')
    val = pv(p['val'], f); xa, xb = x0 + 40, x1 - 40; yb = y0 + (176 if FMT == 'V' else 200); bh = 44
    X = lambda g: xa + (xb - xa) * g / 50.0
    zones = [(0, 18, '#3ba86a'), (18, 40, '#e0a020'), (40, 45, '#e86a1a'), (45, 50, '#d8322a')]
    for g0, g1, col in zones:
        on = g0 <= val
        c.drawRect(skia.Rect.MakeLTRB(X(g0) + 1.5, yb, X(g1) - 1.5, yb + bh), P(col, a * (0.95 if on else 0.38)))
    for g in (0, 18, 40, 45):
        s_ = f'{g} g' if g else '0'
        txt(c, s_, X(g) + (0 if g else 2), yb + bh + 30, 22, 'm8', WHT, a * 0.85, 'c' if g else 'l')
    px = X(min(50.0, val))
    c.drawPath(path_of([(px, yb - 6), (px - 13, yb - 28), (px + 13, yb - 28)], True), P(WHT, a))
    txt(c, ro(val) + ' g', px, yb - 40, 34, 'anton', WHT, a, 'c')
    leg = [('#3ba86a', 'se arde singură pe drum (pasiv)'), ('#e0a020', 'regenerare activă, în mers'), ('#e86a1a', 'peste ≈ 40 g: doar în service'), ('#d8322a', 'peste ≈ 45 g: filtrul se înlocuiește')]
    fs = 22 if FMT == 'V' else 22; yy = yb + bh + 78; colw = (x1 - x0 - 60) / 2
    for k, (col, s_) in enumerate(leg):
        if FMT == 'V': lx, ly = x0 + 40 + (k % 2) * colw, yy + (k // 2) * 42
        else: lx, ly = x0 + 40, yy + k * 46
        hot = (k == 1 and p.get('act') and val >= 18) or (p.get('lim') and ((k == 2 and 40 <= val < 45) or (k == 3 and val >= 45)))
        c.drawRoundRect(skia.Rect.MakeXYWH(lx, ly - 19, 22, 22), 5, 5, P(col, a))
        txt(c, s_, lx + 34, ly, fs, 'm8' if hot else 'm7', WHT, a * (1.0 if hot else 0.72))


def pan_inj(c, R, a, i, f, tl, p):
    x0, y0, x1, y1 = R; pbox(c, R, a, 'CE SCHIMBĂ CALCULATORUL LA REGENERAREA ACTIVĂ')
    s1 = pv(p['s1'], f); s2 = pv(p['s2'], f); wv = x1 - x0
    chips = [('EGR închis', s1 > 0.12), ('Clapeta de admisie strânsă', s1 > 0.42), ('Injecția principală întârziată', s1 > 0.72), ('Post-injecții târzii', s2 > 0.25)]
    fs = 22; xx = x0 + 28; yy = y0 + 96
    for k, (s_, on) in enumerate(chips):
        wd = tw(s_, fs, 'm8') + 30
        if xx + wd > x1 - 24: xx = x0 + 28; yy += 46
        rrect(c, xx, yy - 26, xx + wd, yy + 10, 10, P(Y if on else '#1a2740', a)); txt(c, s_, xx + 15, yy, fs, 'm8', BG if on else WHT, a * (1.0 if on else 0.55)); xx += wd + 12
    # injection diagram along the crank angle
    ya = y1 - 76; xl, xr = x0 + 40, x1 - 40; xp = xl + (xr - xl) * 0.30
    c.drawLine(xl, ya, xr, ya, P(WHT, a * 0.7, stroke=2.5)); c.drawLine(xp, ya - 8, xp, ya + 10, P(WHT, a * 0.8, stroke=2.5))
    txt(c, 'PMS', xp, ya + 34, 20, 'm8', WHT, a * 0.8, 'c'); txt(c, 'unghiul arborelui cotit →', xr, ya + 34, 19, 'm7', WHT, a * 0.5, 'r')
    sc = (xr - xl) / 920.0; hmax = min(120.0, ya - yy - 62)
    def bar(xc, wd, hh, col, lab, al=1.0):
        if al <= 0.01: return
        rrect(c, xc - wd / 2, ya - hh, xc + wd / 2, ya - 2, 5, P(col, a * al)); txt(c, lab, xc, ya - hh - 12, 19, 'm8', WHT, a * al * 0.9, 'c')
    bar(xp - 64 * sc, 14, hmax * 0.26, C_FUEL, 'pilot')
    xm = xp + (14 + 74 * s1) * sc
    if s1 > 0.02: c.drawRoundRect(skia.Rect.MakeLTRB(xp + 14 * sc - 17, ya - hmax * 0.9, xp + 14 * sc + 17, ya - 2), 5, 5, P(C_FUEL, a * 0.22))
    bar(xm, 34, hmax * 0.9, C_FUEL, 'principală')
    bar(xp + 300 * sc, 22, hmax * 0.5, '#ff9a3a', 'post-injecție', ramp(s2, 0.05, 0.3))
    for k in (0, 1): bar(xp + (470 + 90 * k) * sc, 16, hmax * 0.3, '#ff6a2a', 'târzie' if k == 0 else '', ramp(s2, 0.3 + 0.2 * k, 0.3))
    ap = a * ramp(s2, 0.75, 0.25)
    if ap > 0.01: txt(c, 'ard în DOC', xp + 515 * sc, ya - hmax * 0.3 - 40, 20, 'm9', Y, ap, 'c')


def pan_cycles(c, R, a, i, f, tl, p):
    x0, y0, x1, y1 = R; pbox(c, R, a, 'CU CENUȘĂ, REGENERĂRILE SE ÎNDESESC')
    xl, xr, yt, yb = x0 + 60, x1 - 40, y0 + 96, y1 - 58
    c.drawLine(xl, yb, xr, yb, P(WHT, a * 0.6, stroke=2)); c.drawLine(xl, yb, xl, yt, P(WHT, a * 0.6, stroke=2))
    txt(c, 'kilometri →', xr, yb + 34, 20, 'm7', WHT, a * 0.55, 'r')
    Yv = lambda v: yb - (yb - yt) * v
    lim = 0.90
    c.drawLine(xl, Yv(lim), xr, Yv(lim), P(RED, a * 0.8, stroke=2, pe=skia.DashPathEffect.Make([9, 7], 0))); txt(c, 'pragul de regenerare', xl + 10, Yv(lim) - 10, 19, 'm8', RED, a * 0.9)
    base = lambda u: 0.06 + 0.66 * u ** 1.25
    pts = []; u = 0.0; rise = 5.2
    while u < 1.0:
        b0 = base(u); du = (lim - b0) / rise
        pts.append((u, b0)); pts.append((min(1.0, u + du), b0 + rise * (min(1.0, u + du) - u))); u += du
        if u < 1.0: pts.append((u, base(u)))
    rev = cl((f - 0.08) / 0.8)
    c.save(); c.clipRect(skia.Rect.MakeLTRB(xl, yt - 10, xl + (xr - xl) * rev, yb + 2))
    ash = [(xl + (xr - xl) * k / 40, Yv(base(k / 40))) for k in range(41)]
    c.drawPath(path_of(ash + [(xr, yb), (xl, yb)], True), P(C_ASH, a * 0.55)); c.drawPath(path_of(ash), P(C_ASH, a, stroke=3))
    c.drawPath(path_of([(xl + (xr - xl) * u_, Yv(v)) for u_, v in pts]), P(C_GAS, a, stroke=3.5, join='miter'))
    c.restore()
    txt(c, 'funingine', xl + 24, Yv(0.50), 20, 'm8', C_GAS, a * ramp(rev, 0.1, 0.1)); txt(c, 'cenușă', xr - 24, Yv(0.30), 21, 'm8', '#1b1b18', a * ramp(rev, 0.8, 0.15), 'r')


def pan_zero(c, R, a, i, f, tl, p):
    x0, y0, x1, y1 = R; pbox(c, R, a, 'CONTACT PUS · MOTOR OPRIT'); cy = (y0 + y1) / 2 + 26
    txt(c, 'presiunea diferențială', x0 + 40, cy - 62, 26, 'm7', WHT, a * 0.8)
    w = txt(c, 'Δp = ', x0 + 40, cy + 36, 84, 'm9', WHT, a); w += txt(c, '0', x0 + 40 + w, cy + 36, 104, 'anton', GRN, a); txt(c, ' hPa', x0 + 40 + w, cy + 36, 60, 'm8', WHT, a * 0.9)
    ak = a * ramp(tl, 1.6, 0.4); bx = x1 - 110
    c.drawCircle(bx, cy - 4, 52, P(GRN, ak * 0.2)); tick(c, bx, cy - 4, 62, GRN, ak)
    txt(c, 'Dacă arată altceva cu motorul oprit, senzorul sau semnalul lui nu sunt bune.', x0 + 40, y1 - 34, 21 if FMT == 'V' else 18, 'm7', WHT, a * 0.62)


def pan_pm(c, R, a, i, f, tl, p):
    x0, y0, x1, y1 = R; pbox(c, R, a, 'SENZORUL DE PARTICULE · după filtru (unele Euro 6)')
    # comb electrodes
    ex0, ey0 = x0 + 40, y0 + 92; ew = (x1 - x0) * 0.42; eh = y1 - 40 - ey0
    rrect(c, ex0, ey0, ex0 + ew, ey0 + eh, 12, P('#e9e4d6', a)); n = 9; fw = ew / (2 * n + 1)
    c.drawRect(skia.Rect.MakeLTRB(ex0 + fw * 0.6, ey0 + 14, ex0 + ew - fw * 0.6, ey0 + 26), P('#8a8f98', a)); c.drawRect(skia.Rect.MakeLTRB(ex0 + fw * 0.6, ey0 + eh - 26, ex0 + ew - fw * 0.6, ey0 + eh - 14), P('#8a8f98', a))
    for k in range(n * 2 - 1):
        xk = ex0 + fw * (1.5 + k)
        if k % 2 == 0: c.drawRect(skia.Rect.MakeLTRB(xk, ey0 + 20, xk + fw * 0.42, ey0 + eh - 44), P('#8a8f98', a))
        else: c.drawRect(skia.Rect.MakeLTRB(xk, ey0 + 44, xk + fw * 0.42, ey0 + eh - 20), P('#8a8f98', a))
    rng = np.random.default_rng(5); m = int(260 * cl((f - 0.25) / 0.6))
    px = rng.uniform(ex0 + fw * 1.2, ex0 + ew - fw * 1.2, 260); py = rng.uniform(ey0 + 50, ey0 + eh - 50, 260); pr = rng.uniform(3.0, 6.5, 260)
    for k in range(m): c.drawCircle(px[k], py[k], pr[k], P('#0a0a0a', a * 0.92))
    txt(c, 'doi electrozi', ex0 + ew / 2, ey0 + eh + 26, 19, 'm8', WHT, a * 0.7, 'c')
    # current against time
    gx0, gx1, gy0, gy1 = ex0 + ew + 70, x1 - 36, y0 + 110, y1 - 66
    c.drawLine(gx0, gy1, gx1, gy1, P(WHT, a * 0.6, stroke=2)); c.drawLine(gx0, gy1, gx0, gy0, P(WHT, a * 0.6, stroke=2))
    txt(c, 'timp →', gx1, gy1 - 10, 19, 'm7', WHT, a * 0.55, 'r'); txt(c, 'curent', gx0 + 8, gy0 + 2, 19, 'm7', WHT, a * 0.55)
    yth = lerp(gy1, gy0, 0.72)
    c.drawLine(gx0, yth, gx1, yth, P(WHT, a * 0.6, stroke=2, pe=skia.DashPathEffect.Make([8, 6], 0))); txt(c, 'prag', gx1, yth - 8, 18, 'm8', WHT, a * 0.7, 'r')
    rev = cl((f - 0.25) / 0.6)
    for (k_, col, lab) in ((3.2, RED, 'filtru care nu mai reține'), (0.75, GRN, 'filtru bun')):
        pts = [(gx0 + (gx1 - gx0) * u, lerp(gy1, gy0, min(0.95, k_ * max(0.0, u - 0.12) ** 1.6))) for u in np.linspace(0, rev, 40)]
        c.drawPath(path_of(pts), P(col, a, stroke=4))
    ya = gy1 + 58 if FMT == 'H' else gy1 + 30
    if FMT == 'H':
        c.drawLine(gx0, ya - 7, gx0 + 34, ya - 7, P(RED, a, stroke=4)); w_ = txt(c, 'nu mai reține', gx0 + 44, ya, 19, 'm8', WHT, a * 0.85)
        c.drawLine(gx0 + 70 + w_, ya - 7, gx0 + 104 + w_, ya - 7, P(GRN, a, stroke=4)); txt(c, 'filtru bun', gx0 + 114 + w_, ya, 19, 'm8', WHT, a * 0.85)
    else:
        txt(c, 'filtru care nu mai reține', gx0, gy1 + 30, 18, 'm8', RED, a * 0.95); txt(c, 'filtru bun', gx0 + tw('filtru care nu mai reține', 18, 'm8') + 24, gy1 + 30, 18, 'm8', GRN, a * 0.95)


def pan_pipe2(c, R, a, i, f, tl, p):
    x0, y0, x1, y1 = R; pbox(c, R, a, 'ȚEAVA DE EVACUARE, PE DINĂUNTRU'); r = min((y1 - y0 - 150) / 2.0, (x1 - x0) / 5.4); cy = y0 + 86 + r
    for k, (inner, ring, lab, good) in enumerate((('#8b8e92', '#c9ccd0', 'curată: filtrul reține', True), ('#050505', '#3a3a3a', 'neagră de funingine: nu mai reține', False))):
        cx = x0 + (x1 - x0) * (0.27 + 0.46 * k); ak = a * ramp(tl, LEAD + (wt(i, 'curata', 0.5 * sp(i)) if k == 0 else wt(i, 'neagra', 0.72 * sp(i))) - 0.2, 0.35)
        c.drawCircle(cx, cy, r, P(shader=rad(cx - r * 0.3, cy - r * 0.3, r * 1.6, ['#e6e8ea', '#70747a']), a=ak)); c.drawCircle(cx, cy, r * 0.84, P(inner, ak))
        c.drawCircle(cx, cy, r * 0.84, P(shader=rad(cx, cy, r * 0.84, [skia.Color4f(0, 0, 0, 0.55).toColor(), skia.Color4f(0, 0, 0, 0.0).toColor()]), a=ak))
        if not good:
            rng = np.random.default_rng(3)
            for _ in range(70):
                an = rng.uniform(0, 6.28); rr = r * rng.uniform(0.62, 0.84); c.drawCircle(cx + rr * math.cos(an), cy + rr * math.sin(an), rng.uniform(2, 6), P('#000000', ak * 0.8))
        bx, by = cx + r * 0.78, cy - r * 0.78
        c.drawCircle(bx, by, 26, P('#0a1322', ak)); c.drawCircle(bx, by, 26, P(GRN if good else RED, ak, stroke=3))
        (tick if good else cross)(c, bx, by, 28, GRN if good else RED, ak)
        fs = 23 if FMT == 'V' else 20
        for j, ln in enumerate(wrap_lines(lab, fs, 'm8', (x1 - x0) * 0.44)): txt(c, ln, cx, cy + r + 36 + j * fs * 1.25, fs, 'm8', WHT, ak, 'c')


def pan_lpegr(c, R, a, i, f, tl, p, t):
    """the low pressure EGR loop: gas taken after the filter, through the cooler, back in front of the compressor."""
    x0, y0, x1, y1 = R; pbox(c, R, a, 'EGR DE JOASĂ PRESIUNE · schemă')
    st = pv(p['st'], f); wv = x1 - x0; hv = y1 - y0
    yt = y0 + (118 if FMT == 'V' else 150); yb = yt + (112 if FMT == 'V' else 150); bh = 54
    xs = [x0 + wv * q for q in (0.09, 0.33, 0.56, 0.80)]; nm = ['COMPRESOR', 'MOTOR', 'TURBINĂ', 'DOC + DPF']; bw = wv * 0.185
    def box(xc, yc, s_, col='#1a2740', bc='#ffffff', w_=bw):
        rrect(c, xc - w_ / 2, yc - bh / 2, xc + w_ / 2, yc + bh / 2, 10, P(col, a)); rrect(c, xc - w_ / 2, yc - bh / 2, xc + w_ / 2, yc + bh / 2, 10, P(bc, a * 0.5, stroke=1.6))
        txt(c, s_, xc, yc + 8, 20 if FMT == 'V' else 18, 'm8', WHT, a, 'c')
    for k in range(3): c.drawLine(xs[k] + bw / 2, yt, xs[k + 1] - bw / 2, yt, P(C_GAS if k else C_CLN, a * 0.9, stroke=5))
    xo = x1 - 22; c.drawLine(xs[3] + bw / 2, yt, xo, yt, P(C_CLN, a * 0.9, stroke=5))
    xt = xs[3] + bw / 2 + (xo - xs[3] - bw / 2) * 0.45; xc_ = (xs[0] + xs[3]) / 2 + wv * 0.02; cw = wv * 0.26
    col_e = mix(C_CLN, '#5a6676', 0.8)
    c.drawPath(path_of([(xt, yt), (xt, yb), (xc_ + cw / 2, yb)]), P(col_e, a * 0.9, stroke=5, join='miter')); c.drawPath(path_of([(xc_ - cw / 2, yb), (xs[0], yb), (xs[0], yt + bh / 2)]), P(col_e, a * 0.9, stroke=5, join='miter'))
    for k in range(4): box(xs[k], yt, nm[k])
    box(xc_, yb, 'RĂCITOR EGR', col='#3a1512', bc=RED, w_=cw)
    cross(c, xc_ + cw / 2 + 26, yb, 24, RED, a); txt(c, 'înfundat', xc_, yb + bh / 2 + 24, 19, 'm9', RED, a, 'c')
    # moving dots: full flow on the main line, a trickle through the cooler
    for k in range(10):
        ph = (t * 0.35 + k / 10) % 1.0; xx = lerp(xs[0] + bw / 2, xo, ph)
        if any(abs(xx - q) < bw / 2 for q in xs): continue
        c.drawCircle(xx, yt, 5, P(WHT, a * 0.9))
    for k in range(2):
        ph = (t * 0.12 + k / 2) % 1.0; L1 = (yb - yt); L2 = xt - xs[0]; L = L1 + L2 + L1; s_ = ph * L
        q = (xt, yt + s_) if s_ < L1 else ((xt - (s_ - L1), yb) if s_ < L1 + L2 else (xs[0], yb - (s_ - L1 - L2)))
        if abs(q[0] - xc_) < cw / 2 and q[1] == yb: continue
        c.drawCircle(q[0], q[1], 4, P(WHT, a * 0.55))
    # computed against real flow through the filter
    yy = yb + bh / 2 + (58 if FMT == 'V' else 96); lw = 300; bx = x0 + 30 + lw; full = x1 - 40 - bx; a2 = a * ramp(st, 0.05, 0.4)
    for k, (s_, v, col) in enumerate((('debit prin filtru, calculat', 0.80, '#9fb4cc'), ('debit prin filtru, real', lerp(0.80, 0.52, sm(st)), C_GAS))):
        y_ = yy + k * (40 if FMT == 'V' else 54)
        txt(c, s_, x0 + 30, y_ + 8, 21, 'm7', WHT, a2); rrect(c, bx, y_ - 10, bx + full, y_ + 12, 6, P('#1a2740', a2)); rrect(c, bx, y_ - 10, bx + full * v, y_ + 12, 6, P(col, a2))


def pan_final(c, R, a, i, f, tl, p):
    x0, y0, x1, y1 = R; pbox(c, R, a); cx = (x0 + x1) / 2; cy = (y0 + y1) / 2
    a1 = a * ramp(tl, LEAD + 0.3, 0.4); a2 = a * ramp(tl, LEAD + wt(i, 0.68, 0) , 0.4)
    s1 = 'Filtrul de particule e victima,'; s2 = 'nu vinovatul.'; fs = 52 if FMT == 'V' else 44
    txt(c, s1, cx, cy - 110, fs, 'm8', WHT, a1, 'c'); txt(c, s2, cx, cy - 110 + fs * 1.2, fs, 'm8', WHT, a1, 'c')
    ts = 92 if FMT == 'V' else 72
    txt(c, 'ÎNTÂI CAUZA, APOI FILTRUL', cx, cy + 130, ts, 'anton', Y, a2, 'c', shadow=10)


PANS = dict(card=pan_card, steps=pan_steps, codes=pan_codes, dpx=pan_dpx, soot2=pan_soot2, thr=pan_thr, inj=pan_inj, cycles=pan_cycles, zero=pan_zero, pm=pan_pm, pipe2=pan_pipe2,
            final=pan_final)


BIGP = ('card', 'steps', 'final')


def panel(c, t, S):
    for i in (shot_at(t) - 1, shot_at(t)):
        if i < 0 or 'pan' not in SH[i]: continue
        kind, p = SH[i]['pan']
        same_n = i + 1 < N and 'pan' in SH[i + 1] and SH[i + 1]['pan'][0] == kind and kind in ('steps', 'soot2', 'lpegr', 'inj', 'dpx')
        same_p = i > 0 and 'pan' in SH[i - 1] and SH[i - 1]['pan'][0] == kind and kind in ('steps', 'soot2', 'lpegr', 'inj', 'dpx')
        if t >= SE[i] and same_n: continue
        a = (1.0 if same_p else ramp(t, SS[i] + 0.15, 0.35)) * (1.0 if same_n else 1 - ramp(t, SE[i] - 0.34, 0.3))
        if a <= 0.01: continue
        f = cl((t - SS[i]) / (SE[i] - SS[i])); tl = t - SS[i]
        c.save()
        if not same_p: c.translate(0, 16 * (1 - ramp(t, SS[i] + 0.15, 0.35)))
        R = R_BIG if kind in BIGP else R_PAN
        if kind == 'dp': pan_dp(c, R, a, i, f, tl, p, S)
        elif kind == 'lpegr': pan_lpegr(c, R, a, i, f, tl, p, t)
        else: PANS[kind](c, R, a, i, f, tl, p)
        c.restore()


def endcard(c, t):
    a = ramp(t, OUT0 + 0.1, 0.7)
    if a <= 0.01: return
    c.drawRect(skia.Rect.MakeWH(W, H), P('#060b14', a * 0.96))
    cx = W / 2; cy = H / 2 - 30; big = 170 if FMT == 'V' else 150
    txt(c, 'TURBO', cx, cy - 60, big, 'anton', WHT, a, 'c'); txt(c, 'DOCTOR', cx, cy - 60 + big * 1.03, big, 'anton', Y, a, 'c')
    y2 = cy - 60 + big * 1.03 + 70
    wd = tw('TRAINING INTERN', 36, 'm9') + 70
    rrect(c, cx - wd / 2, y2, cx + wd / 2, y2 + 76, 22, P(Y, a)); txt(c, 'TRAINING INTERN', cx, y2 + 51, 36, 'm9', BG, a, 'c')
    txt(c, 'Filtrul de particule (DPF)', cx, y2 + 150, 40, 'm8', WHT, a * 0.9, 'c')


# ------------------------------------------------------------------ the frame
def scene_image(t, S, V):
    surf = skia.Surface(W, H); c = surf.getCanvas()
    background(c, t); E.scene(c, S, V); watermark_over(c, t, ramp(V[0], 2.0, 2.5))
    return surf.makeImageSnapshot()


def frame(t):
    S = state(t); Va, Vb, m = cam(t)
    surf = skia.Surface(W, H); c = surf.getCanvas()
    background(c, t); E.scene(c, S, Va); watermark_over(c, t, ramp(Va[0], 2.0, 2.5))
    V = Va
    if Vb is not None and m > 0.003:
        p = skia.Paint(); p.setAlphaf(m); c.drawImage(scene_image(t, S, Vb), 0, 0, SAMP, p)
        if m > 0.5: V = Vb
    bands(c, S['hi'])
    header(c, t)
    labels(c, t, V); temps(c, t, V)
    caption(c, t); legend(c, t); note_tag(c, t); panel(c, t, S)
    endcard(c, t)
    return surf.makeImageSnapshot()


# ------------------------------------------------------------------ render
def render(out, f0=0, f1=None):
    f1 = NF if f1 is None else min(f1, NF)
    crf = os.environ.get('CRF', '25')
    p = subprocess.Popen(['ffmpeg', '-y', '-nostdin', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-vf', 'scale=out_color_matrix=bt709:out_range=tv', '-c:v', 'libx264', '-preset', 'medium', '-crf', crf, '-g', '60', '-pix_fmt', 'yuv420p',
                          '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    for fi in range(f0, f1):
        p.stdin.write(frame(fi / FPS).toarray(colorType=skia.kRGBA_8888_ColorType).tobytes())
    p.stdin.close()
    if p.wait() != 0: raise SystemExit('ffmpeg failed')


CLOSE = ('doc', 'face', 'maca', 'macb')
PLATES = ['T8_sec', 'TA_sec', 'TB_sec', 'TC_sec', 'T8_idA', 'T8_idB', 'TA_idA', 'TA_idB', 'TB_idA', 'TB_idB', 'TC_idA']


def seg_frames():
    """-> [(first frame, end frame, needs the close-up plates)]: cut 0.4 s before a line starts (before any camera move or dissolve), at the chapters and
    wherever the film goes into or comes out of a close-up, so the parts that only need the wide plates can be rendered on their own."""
    st = set(CHS)
    for i in range(1, N):
        a, b = SH[i - 1]['v'] in CLOSE, SH[i]['v'] in CLOSE
        if a != b: st.add(i)
        if a and not b and i + 1 < N: st.add(i + 1)
    st = sorted(st); fr = lambda i: 0 if i == 0 else (NF if i >= N else int(round((SS[i] - 0.4) * FPS)))
    out = []
    for a, b in zip(st, st[1:] + [N]):
        dep = any(SH[k]['v'] in CLOSE for k in range(a, b)) or (a > 0 and SH[a - 1]['v'] in CLOSE)
        cuts = [a]
        while fr(b) - fr(cuts[-1]) > 1000:                # long parts are cut again at line starts
            nx = [k for k in range(cuts[-1] + 1, b) if fr(k) - fr(cuts[-1]) >= 600]
            if not nx or fr(b) - fr(nx[0]) < 250: break
            cuts.append(nx[0])
        for x, y in zip(cuts, cuts[1:] + [b]): out.append((fr(x), fr(y), dep))
    return out


def plates_ready(): return all(os.path.exists(os.path.join(E.OUTD, n + '.png')) for n in PLATES)


def render_segments(out, jobs=2, force=(), only=None):
    d = out + '.seg'; os.makedirs(d, exist_ok=True)
    segs = seg_frames(); todo = []; ready = plates_ready()
    for i, (f0, f1, dep) in enumerate(segs):
        p = os.path.join(d, f'{i:02d}.mp4')
        if only is not None and i not in only: continue
        if dep and not ready: continue
        if not os.path.exists(p) or i in force: todo.append((i, f0, f1, p))
    running = []
    while todo or running:
        while todo and len(running) < jobs:
            i, f0, f1, p = todo.pop(0); tmp = p[:-4] + '.tmp.mp4'
            pr = subprocess.Popen([sys.executable, os.path.abspath(__file__), '--out', tmp, '--frames', str(f0), str(f1)], stderr=open(p + '.log', 'w'))
            running.append((pr, tmp, p, i))
        for r in list(running):
            if r[0].poll() is None: continue
            running.remove(r)
            if r[0].returncode != 0 or not os.path.exists(r[1]): raise SystemExit(f'segment {r[3]} failed, see {r[2]}.log')
            os.replace(r[1], r[2]); print('segment', r[3], 'done', time.strftime('%H:%M:%S'), flush=True)
        time.sleep(0.5)
    miss = [i for i in range(len(segs)) if not os.path.exists(os.path.join(d, f'{i:02d}.mp4'))]
    if miss: print('still missing segments', miss, flush=True); return
    lst = os.path.join(d, 'list.txt')
    with open(lst, 'w') as f:
        for i in range(len(segs)): f.write(f"file '{i:02d}.mp4'\n")
    subprocess.run(['ffmpeg', '-y', '-nostdin', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', '-movflags', '+faststart', out], check=True)
    print('joined', out, flush=True)


if __name__ == '__main__':
    a = sys.argv[1:]
    if '--info' in a:
        print(f'{N} lines, speech {sum(sp(i) for i in range(N)):.1f} s, film {DUR:.1f} s = {NF} frames; segments', seg_frames())
        for i in range(N): print(f'{i:02d} {SS[i]:7.2f} cue {CUE[i]:7.2f} +{sp(i):5.2f}  {SH[i]["v"]:5s} {SH[i].get("pan", ("",))[0]:6s} {SC.TXT[i][:60]}')
    elif '--cues' in a:
        json.dump(dict(cues=[round(x, 3) for x in CUE], dur=round(DUR, 3), fps=FPS), open(a[a.index('--cues') + 1], 'w'))
    elif '--png' in a or '--mid' in a:
        os.makedirs(os.path.join(HERE, 'proof'), exist_ok=True)
        ts = [float(x) for x in a[a.index('--png') + 1].split(',')] if '--png' in a else [SS[i] + (SE[i] - SS[i]) * 0.62 for i in range(N)]
        if '--only' in a: ts = [ts[int(k)] for k in a[a.index('--only') + 1].split(',')]
        for t_ in ts:
            frame(t_).save(os.path.join(HERE, 'proof', f'{FMT}_{t_:06.1f}.png'), skia.kPNG)
    elif '--out' in a:
        o = a[a.index('--out') + 1]
        if '--frames' in a:
            k = a.index('--frames'); render(o, int(a[k + 1]), int(a[k + 2]))
        else:
            render_segments(o, int(a[a.index('--jobs') + 1]) if '--jobs' in a else 2, [int(v) for v in a[a.index('--force') + 1].split(',')] if '--force' in a else (),
                            [int(v) for v in a[a.index('--only') + 1].split(',')] if '--only' in a else None)
