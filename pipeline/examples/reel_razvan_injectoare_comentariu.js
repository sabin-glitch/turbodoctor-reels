// v2 – Reel r_razvan – răspuns la comentariul lui razvan: de ce cerem toate injectoarele (6 clipuri în ordinea filmării, fără tăieturi)
// clipuri: 0 selfie (IMG_1729) · 9.13 selfie (1731) · 34.50 motor/injectoare (1733) · 59.76 motor (1734) · 115.20 selfie (1735) · 136.81 selfie (1736)
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND }) => {
  const A = {
    p80: aw(0, '80%'), intorc: aw(0, 'întorc'), sechestram: aw(1, 'sechestrăm'), calorifer: aw(1, 'calorifer'),
    a2: aw(2, 'A'), garantez: aw(2, 'garantez'),
    realitatea: aw(3, 'Realitatea'), aceeasi1: aw(4, 'aceeași'), aceeasi2: aw(4, 'aceeași', 1), acelasi: aw(4, 'același'), incep: aw(4, 'încep'), ca5: aw(5, 'Ca'),
    daca7: aw(7, 'Dacă'), factori: aw(7, 'factori'), cand9: aw(9, 'când'), daca10: aw(10, 'Dacă'), dar10: aw(10, 'Dar'),
    am11: aw(11, 'Am'), calicindu: aw(11, 'calicindu-se'), verificarea: aw(12, 'Verificarea'), stiti: aw(12, 'știți'), curatare: aw(12, 'curățare'),
    daca13: aw(13, 'Dacă'), reparatii13: aw(13, 'reparații'), tineti: aw(14, 'Țineți'), nu14: aw(14, 'Nu'),
  };
  const CLIP = [0, 9.13, 34.5, 59.76, 115.2, 136.81];
  return {
    hook: { tag: 'RĂSPUNS LA COMENTARIU · INJECTOARE', l1: '', l2: '', car: '', end: CLIP[1] + .05 },
    stages: [[A.a2 - .1, 'PROBLEMA'], [A.realitatea - .1, 'REALITATEA TEHNICĂ'], [A.cand9 - .1, 'CE URMEAZĂ'], [CLIP[4] + .15, 'SOLUȚIA']],
    items: [
      // hook: comentariul lui razvan, mare; apoi sticker mic în colț cât răspunde ironic
      { k: 'comment', t0: .1, t1: A.a2 - .3, name: 'razvan', y: 250, s: .92, mini: CLIP[1] + .1, miniX: 24, miniY: 300, miniS: .44,
        text: 'mergi la ei cu un injector stricat si te obliga sa le dai jos pe toate 4 sa mai faca niste banii 😢😢😢😢 la telefon zice ca e ok sa iti faca doar unu apoi nu mai' },
      { k: 'kin', t: A.p80 - .02, dur: 1.3, txt: 'PESTE 80%', col: '#FFD21F', y: 1185, size: 140, rot: -4 },
      { k: 'kin', t: A.intorc - .02, dur: 1.7, txt: 'SE ÎNTORC ȘI CU CELELALTE!', col: '#FF3B30', y: 1200, size: 74, rot: -3 },
      { k: 'stk', ico: 'police_light', t0: A.sechestram - .05, t1: A.sechestram + 1.3, x: 950, y: 640, size: 130 },
      { k: 'stk', ico: 'face_screaming_in_fear', t0: A.calorifer - .05, t1: A.calorifer + 1.3, x: 950, y: 640, size: 130 },
      { k: 'chip', t0: A.a2 - .05, t1: CLIP[2] - .2, y: 330, ph: [[A.a2 - .05, 'person_raising_hand', 'VREȚI MOTORUL SĂ MEARGĂ BINE', 'blue'], [A.garantez - .05, 'warning', '1 INJECTOR VERIFICAT ≠ MOTOR GARANTAT', 'red']] },
      // diagrame sus, pe motor
      { k: 'schem', t0: A.realitatea - .1, t1: A.daca7 - .3, top: 268, h: 410, type: 'injectorSet', title: 'SCHEMĂ · DE CE SE UZEAZĂ ÎMPREUNĂ', sub: 'INJECȚIE',
        stepNames: ['INJECTOARE', 'MOTORINĂ', 'TEMPERATURĂ', 'IMPULSURI', 'UZURĂ', 'ECHILIBRU'],
        steps: [[A.realitatea - .1, 'Injectoarele: 4, 6, 8, câte or fi', '', 0], [A.aceeasi1 - .05, 'Aceeași motorină', '', 1], [A.aceeasi2 - .05, 'Aceeași temperatură', '', 2],
          [A.acelasi - .05, 'Același număr de impulsuri electrice', '', 3], [A.incep - .05, 'Când încep să se strice, au aceleași probleme', 'y', 4],
          [A.ca5 - .05, 'Motorul are nevoie de 4 injectoare bune, echilibrate', 'g', 5]] },
      { k: 'schem', t0: A.daca7 - .1, t1: A.am11 - .3, top: 268, h: 410, type: 'injectorSet', title: 'SCHEMĂ · CE SE ÎNTÂMPLĂ CU UN SINGUR INJECTOR', sub: 'INJECȚIE',
        stepNames: ['O REPARAȚIE', 'CORECȚII', 'PRIMUL DEFECT', 'CAZUL 1', 'CAZUL 2'],
        steps: [[A.daca7 - .1, 'Repari un singur injector', '', 6], [A.factori - .05, 'Celelalte primesc factori de corecție mari', 'r', 7],
          [A.cand9 - .05, 'Injectorul 3 a cedat primul', 'r', 8], [A.daca10 - .05, 'La 20.000 km: defect de fabricație', 'y', 9],
          [A.dar10 - .05, 'La 300.000 km: vor pica toate, unul câte unul', 'r', 10]] },
      // soluția (selfie): chip-uri compacte deasupra capului
      { k: 'chip', t0: CLIP[4] + .15, t1: A.verificarea - .3, y: 330, ph: [[CLIP[4] + .15, 'hourglass', 'PIERD TIMP ȘI BANI', 'red'], [A.calicindu - .05, 'cross_mark', 'DOAR UN SINGUR INJECTOR?', 'red']] },
      { k: 'chip', t0: A.verificarea - .05, t1: A.daca13 - .3, y: 330, ph: [[A.verificarea - .05, 'magnifying_glass_tilted_left', 'VERIFICARE: 75 LEI / INJECTOR', 'blue'],
        [A.stiti - .05, 'check_mark_button', 'ȘTII EXACT STAREA LOR', 'green'], [A.curatare - .05, 'sparkles', 'CURĂȚARE + RECALIBRARE, NU REPARAȚIE', 'green']] },
      { k: 'chip', t0: A.daca13 - .05, t1: A.tineti - .3, y: 330, ph: [[A.daca13 - .05, 'warning', 'ALTFEL: MAȘINA PRIN SERVICE-URI', 'red'], [A.reparatii13 - .05, 'hammer_and_wrench', 'REPARAȚII FĂCUTE CU CAP, DEODATĂ', 'green']] },
      { k: 'chip', t0: A.tineti - .05, t1: SEND - .2, y: 330, ph: [[A.tineti - .05, 'shield', 'SERVICII PROFESIONALE', 'green'], [A.nu14 - .05, 'cross_mark', 'NU IEFTINE · NU CÂRPEALĂ', 'red']] },
    ],
    fx: [
      { k: 'punch', t: A.p80, a: .05 }, { k: 'glitch', t: A.cand9, d: .12 }, { k: 'punch', t: A.dar10, a: .04 },
    ],
    sfx: [],
    bursts: [],
  };
};
