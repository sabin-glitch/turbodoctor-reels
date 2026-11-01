// v2 – Reel „Reparații în lucru la Turbo Doctor Iași” (3 clipuri în ordinea filmării, fără tăieturi, 24.10.2026)
// clipuri: 0 IMG_0149 (Renault Master) · 29.14 IMG_0153 (Ford Transit → Range Rover Sport → Opel Vivaro → Mercedes Sprinter) · 127.76 IMG_0154 (VW Crafter)
// fără fețe în cadru (doar mașini și compartimente motor) · plăcile Transit / Vivaro / Crafter estompate local (caption_clean --blur)
// Temă: „vizita de gardă” prin atelier: fiecare mașină = un pacient (capitol + fișă), bara „ÎN LUCRU · IAȘI” sus, raportul de gardă la final.
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND }) => {
  const A = {
    renault: aw(0, 'Renault'), sistemul0: aw(0, 'sistemul'), injectie0: aw(0, 'injecție,'), motorizarea: aw(1, 'Motorizarea'), renumita: aw(1, 'renumită'),
    injectoarele1: aw(1, 'injectoarele'), blocate: aw(2, 'blocate'), chiulasa: aw(2, 'chiulasă.'), in2: aw(2, 'În', 1), doua2: aw(2, 'două'),
    dar3: aw(3, 'dar'), nicio: aw(3, 'nicio'),
    ford: aw(4, 'Ford'), denso: aw(4, 'Denso.'), recond5: aw(5, 'recondiționate,'), montate: aw(5, 'montate'), urmeaza5: aw(5, 'Urmează'), teste: aw(5, 'teste'),
    verificarile: aw(6, 'verificările'), aici6: aw(6, 'Aici'), range: aw(6, 'Range'),
    an2021: aw(7, '2021,'), multiple: aw(7, 'multiple'), retansari: aw(8, 'retanșări'), inlocuirea: aw(8, 'înlocuirea'),
    recond9: aw(9, 'recondiționarea'), filtru9: aw(9, 'filtru'), original: aw(9, 'original.'),
    bineinteles10: aw(10, 'Bineînțeles'), saptamana: aw(10, 'săptămâna'), dubelor: aw(10, 'dubelor:'), opel: aw(10, 'Opel'), eficienta: aw(10, 'eficiența'),
    demontat11: aw(11, 'demontat,'), urmeaza12: aw(12, 'Urmează'), supra12: aw(12, 'supraalimentare'), motivul: aw(12, 'motivul'),
    mercedes: aw(13, 'Mercedes'), injectie13: aw(13, 'injecție.'), trimise: aw(14, 'trimise'), clientul14: aw(14, 'Clientul'), trepidatii: aw(14, 'trepidații'),
    pierderi15: aw(15, 'pierderi'), urmeaza15: aw(15, 'Urmează'), cauza: aw(15, 'cauza'),
    data16: aw(16, 'data'), filtru16: aw(16, 'filtru'), acesta: aw(17, 'Acesta'), demontat17: aw(17, 'demontat.'), constatare17: aw(17, 'constatare'),
    turbo17: aw(17, 'turbosuflantă'), supra17: aw(17, 'supraalimentare.'), ulterior: aw(18, 'Ulterior,'), remedia: aw(18, 'remedia'),
  };
  const CLIP = [0, 29.14, 127.76];
  const HEND = A.motorizarea - .15;
  // capitolele: [t, nr, titlu, sub, mașina pe bară]
  const CH = [[A.ford - .05, 'PACIENTUL 2 / 6', 'FORD TRANSIT 2.4', 'INJECȚIE DENSO', 'FORD TRANSIT 2.4'],
              [A.range - .1, 'PACIENTUL 3 / 6', 'RANGE ROVER SPORT', 'MODEL 2021', 'RANGE ROVER SPORT 2021'],
              [A.opel - .1, 'PACIENTUL 4 / 6', 'OPEL VIVARO', 'EFICIENȚĂ DPF', 'OPEL VIVARO'],
              [A.mercedes - .1, 'PACIENTUL 5 / 6', 'MERCEDES SPRINTER 3.0', 'INJECȚIE', 'MERCEDES SPRINTER 3.0'],
              [A.data16 - .05, 'PACIENTUL 6 / 6', 'VOLKSWAGEN CRAFTER', 'FILTRU DE PARTICULE', 'VW CRAFTER']];
  const CHD = 1.65;  // cât stă cardul de capitol
  const items = [], fx = [];
  CH.forEach(([t, k, title, sub]) => {
    fx.push({ k: 'veil', t0: t, t1: t + CHD - .05, out: .16 }, { k: 'flash', t, a: .45 }, { k: 'glitch', t, d: .12 });
    items.push({ k: 'chap', t0: t, t1: t + CHD, kicker: k, title, sub, y: 880 });
  });
  items.push({ k: 'band', t0: HEND, t1: SEND, y: 222, w: 980, h: 76, kicker: 'ÎN LUCRU · IAȘI',
    ph: [[HEND, 'RENAULT MASTER 2.0', 'PACIENT 1/6'], ...CH.map(([t, k, , , car]) => [t, car, 'PACIENT ' + k.replace('PACIENTUL ', '').replace(/ /g, '')])] });

  // ---- HOOK (0 – prima frază): titlul cerut de Sabin + scanare pe motor
  items.push({ k: 'scan', t0: 2.7, t1: HEND - .2, box: [150, 860, 780, 700], lab: 'SCANARE MOTOR...', lab2: 'SISTEM DE INJECȚIE', at2: A.sistemul0 - .04 });

  // ---- 1 · RENAULT MASTER 2.0: injectoare blocate în chiulasă
  items.push({ k: 'file', t0: HEND + .05, t1: A.blocate - .1, no: '', ecg: 'crit', rows: [[HEND + .1, 'PACIENT', 'RENAULT MASTER 2.0', 'c', 'automobile'],
    [A.renumita, 'RENUMIT PENTRU', 'INJECTOARE BLOCATE', 'r', 'warning'], [A.injectoarele1, 'SISTEM', 'INJECȚIE', 'y', 'fuel_pump']] });
  items.push({ k: 'def', t0: A.blocate - .05, t1: A.in2 - .1, term: 'INJECTOR BLOCAT ÎN CHIULASĂ',
    text: 'Calamina și coroziunea îl „lipesc” de chiulasă: nu mai iese pe cale normală.' });
  items.push({ k: 'list', t0: A.in2 - .05, t1: CLIP[1] + .3, ico: 'fuel_pump', title: 'INJECTOARELE · RENAULT MASTER',
    rows: [[A.doua2, '2 INJECTOARE: EXTRASE'], [A.dar3, '2 INJECTOARE: BLOCATE ÎN CHIULASĂ', 'bad']] });
  items.push({ k: 'stamp', t: A.nicio - .04, t1: A.nicio + 1.5, txt: 'NU IES!', y: 760, col: 'red', s: .9, rot: -8 });

  // ---- 2 · FORD TRANSIT 2.4: injectoare recondiționate, urmează testele
  items.push({ k: 'file', t0: CH[0][0] + CHD + .05, t1: A.urmeaza5 - .1, no: '', ecg: 'ok', rows: [[CH[0][0] + CHD + .1, 'PACIENT', 'FORD TRANSIT 2.4', 'c', 'automobile'],
    [A.denso, 'INJECȚIE', 'DENSO', 'y', 'fuel_pump'], [A.recond5, 'INJECTOARE', 'RECONDIȚIONATE', 'g', 'test_tube'], [A.montate, 'MONTAJ', 'MONTATE PE MAȘINĂ', 'g', 'wrench']] });
  items.push({ k: 'chip', t0: A.urmeaza5 - .05, t1: A.aici6 - .5, y: 330, ph: [[A.urmeaza5 - .05, 'stopwatch', 'URMEAZĂ: TESTELE', 'blue'],
    [A.verificarile - .05, 'check_mark_button', 'ȘI VERIFICĂRILE FINALE', 'green']] });

  // ---- 3 · RANGE ROVER SPORT 2021: lucrări multiple pe motor
  items.push({ k: 'file', t0: CH[1][0] + CHD + .05, t1: A.retansari - .1, no: '', ecg: 'ok', rows: [[CH[1][0] + CHD + .1, 'PACIENT', 'RANGE ROVER SPORT', 'c', 'automobile'],
    [A.an2021, 'AN', '2021', 'y', 'calendar'], [A.multiple, 'INTERVENȚII', 'MULTIPLE, PE MOTOR', 'c', 'hammer_and_wrench']] });
  items.push({ k: 'list', t0: A.retansari - .05, t1: CH[2][0] - 1.6, ico: 'hammer_and_wrench', title: 'LUCRĂRI EFECTUATE · MOTOR',
    rows: [[A.retansari, 'RETANȘĂRI COMPLETE: PIERDERI DE ULEI'], [A.inlocuirea, 'CUZINEȚI ÎNLOCUIȚI'], [A.recond9, 'TURBOSUFLANTE RECONDIȚIONATE'],
      [A.filtru9, 'FILTRU DE PARTICULE NOU, ORIGINAL']] });

  // ---- 4 · OPEL VIVARO: eroare de eficiență DPF, constatare completă
  items.push({ k: 'kin', t: A.saptamana - .02, dur: 1.45, txt: 'SĂPTĂMÂNA DUBELOR!', col: '#FFD21F', y: 420, size: 104, rot: -4 });
  items.push({ k: 'file', t0: CH[2][0] + CHD + .05, t1: A.urmeaza12 - .1, no: '', ecg: 'crit', rows: [[CH[2][0] + CHD + .1, 'PACIENT', 'OPEL VIVARO', 'c', 'automobile'],
    [CH[2][0] + CHD + .35, 'SIMPTOM', 'EROARE EFICIENȚĂ DPF', 'r', 'warning'], [A.demontat11, 'DPF', 'DEMONTAT · INSPECTAT', 'y', 'leaf']] });
  items.push({ k: 'schem', t0: A.urmeaza12 - .05, t1: CH[3][0] - .3, top: 268, h: 330, type: 'causeEffect', title: 'SCHEMĂ · CAUZĂ › EFECT', sub: 'CONSTATARE COMPLETĂ',
    P: { sym: ['warning', 'EROARE EFICIENȚĂ DPF'], causes: [['gear', 'TURBO'], ['dashing_away', 'ADMISIE'], ['leaf', 'DPF']], sweep: 2.6 },
    stepNames: ['SIMPTOM', 'CONSTATARE', 'CAUZA?'],
    steps: [[A.urmeaza12 - .05, 'Urmează o constatare completă', 'y', 0], [A.supra12 - .05, 'Supraalimentarea și admisia, verificate', '', 1],
      [A.motivul - .05, 'Ca să aflăm exact de ce apare eroarea DPF', 'y', 1]] });

  // ---- 5 · MERCEDES SPRINTER 3.0: injecție, trepidații la ralanti, pierderi de ulei
  items.push({ k: 'file', t0: CH[3][0] + CHD + .05, t1: A.clientul14 - .1, no: '', ecg: 'crit', rows: [[CH[3][0] + CHD + .1, 'PACIENT', 'MERCEDES SPRINTER', 'c', 'automobile'], [CH[3][0] + CHD + .3, 'MOTOR', '3.0', 'y', 'gear'],
    [A.injectie13, 'PROBLEME PE', 'INJECȚIE', 'r', 'fuel_pump'], [A.trimise, 'INJECTOARE', 'TRIMISE LA LABORATOR', 'y', 'microscope']] });
  items.push({ k: 'ecg', t0: A.clientul14 - .05, t1: A.pierderi15 - .15, label: 'TURAȚIE LA RALANTI', ico: 'stethoscope', mode: 'rpm',
    states: [[A.clientul14 - .05, 'crit', 'INSTABIL'], [A.trepidatii, 'crit', 'TREPIDAȚII']] });
  items.push({ k: 'stamp', t: A.pierderi15 - .04, t1: A.urmeaza15 - .2, txt: 'PIERDERI MASIVE DE ULEI', y: 520, col: 'red', s: .72, rot: -6 });
  items.push({ k: 'chip', t0: A.urmeaza15 - .05, t1: CH[4][0] - .3, y: 330, ph: [[A.urmeaza15 - .05, 'magnifying_glass_tilted_left', 'URMEAZĂ: VERIFICĂRI SUPLIMENTARE', 'blue'],
    [A.cauza - .05, 'oil_drum', 'CAUZA PIERDERILOR DE ULEI', 'yellow']] });

  // ---- 6 · VW CRAFTER: DPF demontat, constatare pe turbo și supraalimentare
  items.push({ k: 'file', t0: CH[4][0] + CHD + .05, t1: A.constatare17 - .1, no: '', ecg: 'crit', rows: [[CH[4][0] + CHD + .1, 'PACIENT', 'VW CRAFTER', 'c', 'automobile'],
    [A.filtru16, 'PROBLEME PE', 'FILTRUL DPF', 'r', 'leaf'], [A.demontat17, 'DPF', 'DEMONTAT', 'y', 'wrench']] });
  items.push({ k: 'list', t0: A.constatare17 - .05, t1: A.ulterior - .1, ico: 'magnifying_glass_tilted_left', title: 'CONSTATARE TOTALĂ',
    rows: [[A.turbo17, 'TURBOSUFLANTA'], [A.supra17, 'SISTEMUL DE SUPRAALIMENTARE']] });
  items.push({ k: 'chip', t0: A.ulterior - .05, t1: SEND - .2, y: 330, ph: [[A.ulterior - .05, 'speech_balloon', 'URMEAZĂ: DISCUȚIA CU CLIENTUL', 'blue'],
    [A.remedia - .05, 'wrench', 'APOI REMEDIEREA PROBLEMELOR', 'green']] });

  // ---- raportul de gardă (pe ultimul cadru, încetinit)
  items.push({ k: 'tip', t0: SEND + .1, t1: TEND - .15, top: 300, title: 'RAPORTUL DE GARDĂ', sub: 'ÎN LUCRU LA TURBO DOCTOR IAȘI', ico: 'stethoscope',
    rows: [[SEND + .35, 'fuel_pump', 'Renault Master 2.0: injectoare blocate în chiulasă'], [SEND + 1.05, 'stopwatch', 'Ford Transit 2.4: injectoare recondiționate, intră în teste'],
      [SEND + 1.75, 'hammer_and_wrench', 'Range Rover Sport: lucrări complete pe motor'], [SEND + 2.45, 'leaf', 'Opel Vivaro: constatare pentru eroarea DPF'],
      [SEND + 3.15, 'microscope', 'Mercedes 3.0: injectoarele la laborator'], [SEND + 3.85, 'magnifying_glass_tilted_left', 'VW Crafter: constatare turbo și supraalimentare']] });

  fx.push({ k: 'punch', t: A.blocate, a: .05 }, { k: 'punch', t: A.nicio, a: .06, sh: 10 }, { k: 'punch', t: A.original, a: .04 },
    { k: 'punch', t: A.dubelor, a: .05 }, { k: 'punch', t: A.pierderi15, a: .05, sh: 10 });

  return {
    hook: { tag: 'VIZITA DE GARDĂ · 6 PACIENȚI', l1: 'REPARAȚII ÎN LUCRU', l1At: .1, l2: 'LA TURBO DOCTOR <span class="w">IAȘI</span>', l2At: .75, l2Col: '#FFD21F',
      car: 'RENAULT MASTER 2.0', carAt: A.renault, stk1: 'stethoscope', end: HEND },
    hideCap: [[0, HEND]],
    stages: null,
    tags: {
      0: { renault: 'c', master: 'c', 20: 'y', probleme: 'r', injectie: 'c' },
      1: { renumita: 'y', injectoarele: 'c' },
      2: { blocate: 'r', chiulasa: 'c', doua: 'y' },
      3: { reusit: 'g', doua: 'y', nicio: 'r', forma: 'r' },
      4: { ford: 'c', transit: 'c', 24: 'y', injectie: 'c', denso: 'c' },
      5: { injectoarele: 'c', reconditionate: 'g', montate: 'g', teste: 'y' },
      6: { verificarile: 'g', finale: 'g', range: 'c', rover: 'c', sport: 'c' },
      7: { 2021: 'y', multiple: 'y', motorizare: 'c' },
      8: { retansari: 'g', pierderile: 'r', ulei: 'r', inlocuirea: 'g', cuzinetilor: 'c' },
      9: { reconditionarea: 'g', turbosuflantelor: 'c', filtru: 'c', particule: 'c', nou: 'g', original: 'g' },
      10: { saptamana: 'y', dubelor: 'y', opel: 'c', vivaro: 'c', probleme: 'r', eficienta: 'r' },
      11: { filtrului: 'r', particule: 'c', demontat: 'y', inspectat: 'y' },
      12: { constatare: 'g', completa: 'g', supraalimentare: 'c', admisie: 'c', exactitate: 'y', eroare: 'r' },
      13: { mercedes: 'c', 30: 'y', probleme: 'r', injectie: 'r' },
      14: { injectoarele: 'c', laborator: 'g', trepidatii: 'r', ralanti: 'r' },
      15: { pierderi: 'r', masive: 'r', ulei: 'r', verificari: 'g', suplimentare: 'g', cauza: 'y' },
      16: { volkswagen: 'c', crafter: 'c', probleme: 'r', filtru: 'r', particule: 'r' },
      17: { demontat: 'y', constatare: 'g', totala: 'g', turbosuflanta: 'c', supraalimentare: 'c' },
      18: { clientul: 'y', remedia: 'g', problemele: 'r' },
    },
    items, fx, sfx: [], bursts: [],
  };
};
