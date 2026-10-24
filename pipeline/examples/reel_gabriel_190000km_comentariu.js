// v2 – Reel r_gabriel – răspuns la comentariul lui gabriel antal: de ce își vând occidentalii mașinile la 190.000 km (3 clipuri în ordinea filmării, fără tăieturi)
// clipuri: 0 selfie (IMG_1738) · 57.85 motor secționat (1739) · 75.92 selfie (1740)
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND }) => {
  const A = {
    k190: aw(0, '190.000'), realitatea: aw(1, 'Realitatea'), preturile: aw(1, 'prețurile'),
    inainte2: aw(2, 'Înainte'), acum3: aw(3, 'Acum'), masina3: aw(3, 'Mașina'), actualizata: aw(3, 'actualizată'),
    adica4: aw(4, 'Adică'), anumite: aw(5, 'anumite'),
    daca6: aw(6, 'Dacă'), acum6: aw(6, 'acum'), pe7: aw(7, 'Pe'),
    avem8: aw(8, 'Avem'), carpeala8: aw(8, 'cârpeala'), ca9: aw(9, 'Că'), acum10: aw(10, 'Acum'), e10: aw(10, 'E'),
    asa11: aw(11, 'Așa'), tii11: aw(11, 'ții'), sau11: aw(11, 'Sau'), probabil12: aw(12, 'probabil'), est12: aw(12, 'est'), africa: aw(13, 'Africa'),
  };
  const CLIP = [0, 57.85, 75.92];
  return {
    hook: { tag: 'RĂSPUNS LA COMENTARIU', l1: '', l2: '', car: '', end: A.realitatea - .1 },
    stages: [[A.realitatea - .1, 'REALITATEA'], [A.daca6 - .1, 'CAUZELE'], [A.avem8 - .1, 'CÂRPEALA'], [A.asa11 - .1, 'SFATUL']],
    items: [
      { k: 'comment', t0: .1, t1: A.realitatea - .25, name: 'gabriel antal', initial: 'G', col: '#B45309', y: 290, s: 1.0,
        text: 'Oare dece occidentalii isi vand masinile la 190000 km?' },
      { k: 'kin', t: A.k190 - .02, dur: 1.4, txt: '190.000 KM', col: '#FFD21F', y: 1185, size: 130, rot: -4 },
      { k: 'chip', t0: A.realitatea - .05, t1: A.inainte2 - .3, y: 330, ph: [[A.realitatea - .05, 'money_with_wings', 'REPARAȚIILE AU DEVENIT FOARTE SCUMPE', 'red'], [A.preturile - .05, 'euro_banknote', 'PREȚURI ȘI SALARII ÎN CREȘTERE', 'yellow']] },
      { k: 'chip', t0: A.inainte2 - .05, t1: A.acum3 - .3, y: 330, ph: [[A.inainte2 - .05, 'automobile', 'ÎNAINTE: LA 200.000 KM REPARAI IEFTIN', 'blue']] },
      { k: 'chip', t0: A.acum3 - .05, t1: A.adica4 - .3, y: 330, ph: [[A.acum3 - .05, 'cross_mark', 'ACUM NU MAI E AȘA', 'red'], [A.masina3 - .05, 'chart_down', 'MAȘINA SE DEVALORIZEAZĂ', 'blue'], [A.actualizata - .05, 'wrench', 'MANOPERA: LA PREȚUL DE AZI', 'red']] },
      { k: 'chip', t0: A.adica4 - .05, t1: CLIP[1] - .2, y: 330, ph: [[A.adica4 - .05, 'money_bag', 'PLĂTEȘTI MANOPERA DE AZI', 'red'], [A.anumite - .05, 'warning', 'UNELE MAȘINI NU MAI MERITĂ', 'red']] },
      // diagramă sus, pe motorul secționat
      { k: 'schem', t0: A.daca6 - .1, t1: CLIP[2] - .2, top: 268, h: 410, type: 'valueVsLabor', title: 'SCHEMĂ · DE CE NU MAI MERITĂ REPARATĂ', sub: 'COSTURI',
        stepNames: ['ÎNAINTE', 'ACUM', 'EXPLOATARE'],
        steps: [[A.daca6 - .1, 'Reparațiile complicate erau ieftine', '', 0], [A.acum6 - .05, 'Acum nu prea mai sunt: mașina pierde valoare, manopera crește', 'r', 1],
          [A.pe7 - .05, 'Mașinile sunt exploatate mult mai intens decât acum 5-10 ani', 'y', 2]] },
      { k: 'chip', t0: A.avem8 - .05, t1: A.ca9 - .3, y: 330, ph: [[A.avem8 - .05, 'racing_car', 'MAI MULTE AUTOSTRĂZI, MAI MULȚI KM', 'blue'], [A.carpeala8 - .05, 'cross_mark', 'CÂRPEALA NU MAI ȚINE', 'red']] },
      { k: 'chip', t0: A.ca9 - .05, t1: A.acum10 - .3, y: 330, ph: [[A.ca9 - .05, 'calendar', 'ÎNAINTE: CÂRPEALA ȚINEA UN AN, 15.000 KM', 'blue']] },
      { k: 'chip', t0: A.acum10 - .05, t1: A.asa11 - .3, y: 330, ph: [[A.acum10 - .05, 'rocket', 'ACUM: ZECI DE MII DE KM PE AN', 'red'], [A.e10 - .05, 'eyes', 'S-A SCHIMBAT PERCEPȚIA, NU REALITATEA', 'yellow']] },
      { k: 'chip', t0: A.asa11 - .05, t1: A.probabil12 - .3, y: 330, ph: [[A.asa11 - .05, 'check_mark_button', 'MÂNA A DOUA: PÂNĂ ÎN 100.000 KM', 'green'],
        [A.tii11 - .05, 'check_mark_button', 'ȚINE-O PÂNĂ LA 150-200.000 KM', 'green'], [A.sau11 - .05, 'sparkles', 'SAU NOUĂ, PÂNĂ LA 150-200.000 KM', 'green']] },
      { k: 'chip', t0: A.probabil12 - .05, t1: SEND - .2, y: 330, ph: [[A.probabil12 - .05, 'globe', 'APOI O VINZI MAI DEPARTE', 'blue'], [A.est12 - .05, 'round_pushpin', 'SPRE EST, UNDE REPARAȚIILE SUNT MAI IEFTINE', 'blue'], [A.africa - .05, 'globe2', 'SAU ÎN AFRICA, CINE ȘTIE', 'blue']] },
    ],
    fx: [ { k: 'punch', t: A.k190, a: .05 }, { k: 'glitch', t: A.acum3, d: .12 }, { k: 'punch', t: A.acum6, a: .04 } ],
    sfx: [],
    bursts: [],
  };
};
