// v2 – Reel r_jecmaneala – „Cum scapi de jecmăneala din domeniul auto” (4 clipuri selfie în ordinea filmării, fără tăieturi)
// clipuri: 0 IMG_1748 · 11.47 IMG_1750 · 85.70 IMG_1751 · 132.81 IMG_1752 · toate selfie: grafică compactă deasupra capului
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND }) => {
  const A = {
    jecm0: aw(0, 'jecmăneala'), mecanicii: aw(0, 'Mecanicii'), care0: aw(0, 'care'), pielea: aw(0, 'pielea'),
    haideti1: aw(1, 'Haideți'), si1: aw(1, 'Și'), extra: aw(1, 'extraordinar'),
    cand2: aw(2, 'Când'), va2b: aw(2, 'Vă', 2), si3: aw(3, 'și'), care3: aw(3, 'care'), k100a: aw(3, '100.000'),
    lucrurile: aw(4, 'Lucrurile'), k200a: aw(4, '200'), daca4: aw(4, 'Dacă'), nu4: aw(4, 'Nu'),
    iar5: aw(5, 'Iar'), jecm5: aw(5, 'jecmăneală,'), este5: aw(5, 'este'),
    trebuie: aw(6, 'Trebuie'), nu7: aw(7, 'nu'), jumatate: aw(7, 'jumătate'), deoarece: aw(7, 'deoarece'), si7: aw(7, 'și'),
    daca8: aw(8, 'Dacă'), cumparati: aw(8, 'Cumpărați'), nu8: aw(8, 'nu', 1), care8b: aw(8, 'care', 1),
    si9: aw(9, 'și'), o9: aw(9, 'O'), k150: aw(9, '150-200.000'), si9b: aw(9, 'și', 1),
    in10: aw(10, 'În'), doar11: aw(11, 'doar'), cand11b: aw(11, 'când', 1), lucru11: aw(11, 'Lucru'),
    ps: aw(12, 'P.S.:'), land: aw(12, 'Land'), ca12: aw(12, 'că'),
  };
  const CLIP = [0, 11.47, 85.70, 132.81];
  return {
    hook: { tag: 'ADEVĂRUL DIN SERVICE', y: -70, l1: 'SĂ VORBIM DESPRE', l1At: .35, l2: 'JECMĂNEALA DIN AUTO!', l2At: A.jecm0 - .04, l2Col: '#FF3B30',
      stk1: 'money_with_wings', end: A.mecanicii - .1 },
    hideCap: [[0, A.mecanicii - .12]],
    stages: [[A.mecanicii - .05, 'JECMĂNEALA?'], [A.cand2 - .1, 'ALEGEREA'], [A.lucrurile - .1, 'REALITATEA'], [A.daca8 - .1, 'SOLUȚIA']],
    items: [
      // intro (IMG_1748): ce spun oamenii
      { k: 'chip', t0: A.mecanicii - .05, t1: A.haideti1 - .3, y: 330, ph: [[A.mecanicii - .05, 'speech_balloon', '„MECANICII ĂȘTIA NENOROCIȚI...”', 'red'], [A.care0 - .05, 'money_with_wings', '„...CARE IAU PIELEA DE PE OM”', 'red']] },
      { k: 'chip', t0: A.haideti1 - .05, t1: A.cand2 - .3, y: 330, ph: [[A.haideti1 - .05, 'hammer_and_wrench', 'CUM SCAPI DE JECMĂNEALĂ', 'blue'], [A.si1 - .05, 'check_mark_button', 'EXTRAORDINAR DE SIMPLU', 'green']] },
      // alegerea mașinii
      { k: 'chip', t0: A.cand2 - .05, t1: A.lucrurile - .3, y: 330, ph: [[A.cand2 - .05, 'thinking_face', 'MAȘINA PE CARE V-AȚI DORI-O', 'blue'], [A.va2b - .05, 'automobile', 'CE MAȘINĂ SH AȚI CUMPĂRA', 'blue'],
        [A.si3 - .05, 'pointing_right', 'APOI: VARIANTA DE BUGET', 'green'], [A.care3 - .05, 'check_mark_button', 'SUB 100.000 KM', 'green']] },
      { k: 'kin', t: A.k100a - .02, dur: 1.3, txt: 'SUB 100.000 KM', col: '#FFD21F', y: 1185, size: 110, rot: -4 },
      // realitatea: premium cu rulaj mare
      { k: 'chip', t0: A.lucrurile - .05, t1: A.iar5 - .3, y: 330, ph: [[A.lucrurile - .05, 'warning', 'PROBLEMELE GRAVE: CAM DUPĂ 200.000 KM', 'red'],
        [A.daca4 - .05, 'money_bag', 'PREMIUM PESTE 200.000 KM = MULȚI BANI', 'red'], [A.nu4 - .05, 'cross_mark', 'NU AI CUM SĂ EVIȚI ASTA', 'red']] },
      { k: 'kin', t: A.k200a - .02, dur: 1.2, txt: '200.000 KM', col: '#FFD21F', y: 1185, size: 120, rot: -4 },
      { k: 'def', t0: A.iar5 - .05, t1: A.trebuie - .3, top: 262, term: 'JECMĂNEALĂ?', text: 'De fapt: problema care vine la pachet cu orice mașină premium cu rulaj foarte mare.' },
      { k: 'chip', t0: A.trebuie - .05, t1: A.daca8 - .3, y: 330, ph: [[A.trebuie - .05, 'racing_car', 'S-CLASS · SERIA 7: NOI, 100+ MII €', 'yellow'], [A.nu7 - .05, 'chart_down', 'ÎN 5 ANI: SUB JUMĂTATE DIN PREȚ', 'red'],
        [A.deoarece - .05, 'warning', 'UN CALVAR DE ÎNTREȚINUT', 'red'], [A.si7 - .05, 'money_with_wings', 'FOARTE SCUMPĂ LA REPARAT', 'red']] },
      { k: 'kin', t: A.jumatate - .02, dur: 1.3, txt: '-50% ÎN 5 ANI', col: '#FF3B30', y: 1185, size: 110, rot: -4 },
      // soluția
      { k: 'chip', t0: A.daca8 - .05, t1: A.si9 - .3, y: 330, ph: [[A.daca8 - .05, 'shield', 'NU MAI VREI SĂ FII JECMĂNIT?', 'blue'], [A.cumparati - .05, 'automobile', 'CUMPĂRĂ O MAȘINĂ MAI IEFTINĂ', 'green'],
        [A.nu8 - .05, 'money_bag', 'NU LA PREȚ: IEFTINĂ ȘI DE NOUĂ', 'green'], [A.care8b - .05, 'check_mark_button', 'ÎN BUGET, RELAXAT', 'green']] },
      { k: 'chip', t0: A.si9 - .05, t1: A.in10 - .3, y: 330, ph: [[A.si9 - .05, 'counter', 'PÂNĂ ÎN 100.000 KM', 'green'], [A.o9 - .05, 'racing_car', 'FĂRĂ PROBLEME PÂNĂ LA 150-200.000 KM', 'green'],
        [A.si9b - .05, 'wrench', 'PUȚINE PROBLEME, CU ÎNTREȚINERE CORECTĂ', 'green']] },
      { k: 'kin', t: A.k150 - .02, dur: 1.4, txt: '150-200.000 KM', col: '#4ADE80', y: 1185, size: 100, rot: -4 },
      { k: 'chip', t0: A.in10 - .05, t1: A.ps - .3, y: 330, ph: [[A.in10 - .05, 'check_mark_button', 'AȘA SCAPI DE JECMĂNEALĂ', 'green'], [A.doar11 - .05, 'warning', '„JECMĂNEALA”: DOAR LA RULAJE FOARTE MARI', 'yellow'],
        [A.cand11b - .05, 'money_with_wings', 'ȘI LA PROBLEME FOARTE COSTISITOARE', 'red'], [A.lucru11 - .05, 'counter', 'DE CELE MAI MULTE ORI: DUPĂ 200.000 KM', 'yellow']] },
      // P.S.
      { k: 'chip', t0: A.ps - .05, t1: SEND - .2, y: 330, ph: [[A.ps - .05, 'speech_balloon', 'P.S.: EXCEPTÂND LAND ROVER ȘI FORD', 'yellow'], [A.ca12 - .05, 'face_screaming_in_fear', 'ACOLO NU SE ȘTIE!', 'red']] },
      { k: 'stk', t0: A.ca12, t1: SEND - .1, ico: 'face_screaming_in_fear', x: 930, y: 560, size: 130 },
    ],
    fx: [
      { k: 'glitch', t: A.cand2 - .1, d: .12 }, { k: 'punch', t: A.k100a, a: .05 }, { k: 'glitch', t: A.lucrurile - .1, d: .12 }, { k: 'punch', t: A.k200a, a: .05 },
      { k: 'punch', t: A.jumatate, a: .05 }, { k: 'glitch', t: A.daca8 - .1, d: .12 }, { k: 'punch', t: A.k150, a: .04 }, { k: 'glitch', t: A.ps, d: .12 },
    ],
    sfx: [],
    bursts: [],
  };
};
