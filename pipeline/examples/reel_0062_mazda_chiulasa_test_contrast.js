// v2 – Reel r0062 – „Mazda 2.2 diesel: consum mare de ulei și antigel → test pe chiulasă pozitiv → motorul jos” (IMG_0062, un singur clip, fără tăieturi)
// clip: motorul scos de pe mașină, pe podeaua atelierului (Piatra Neamț): 0–34 fața cu distribuția și axele cu came · 36–46 partea blocului de unde s-a demontat biturbo-ul · 48–86 motorul din mai multe unghiuri · fără fețe
// Hook: titlu boom „CONSUM FOARTE MARE DE / ULEI / ȘI ANTIGEL?” peste prima frază (fidel cu simptomele spuse la 10–13 s), ca la Opel #0030. Fără CTA pe imagine (25.10).
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND }) => {
  const A = {
    motorizare: aw(0, 'motorizare'), masina0: aw(0, 'mașină'), piatra: aw(0, 'Piatra'), unde0: aw(0, 'unde'),
    lipsa1: aw(1, 'lipsă'), consum1: aw(1, 'consum'), consum1b: aw(1, 'consum', 1), in1: aw(1, 'În'),
    testare: aw(2, 'testare'), substanta: aw(2, 'substanță'),
    bine3: aw(3, 'Bineînțeles'), rezultatul: aw(3, 'rezultatul'), pozitiv: aw(3, 'pozitiv'), motorul3: aw(3, 'Motorul'),
    pentru4: aw(4, 'pentru'), chiulasa4: aw(4, 'chiulasă'), ansamblul: aw(4, 'Ansamblul'), demontat4: aw(4, 'demontat'),
    trimis5: aw(5, 'trimis'), verificari5: aw(5, 'verificări'), garantie5: aw(5, 'garanție'), n24: aw(5, '24'), fara5: aw(5, 'fără'),
    sistemul6: aw(6, 'Sistemul'), demontat6: aw(6, 'demontat'), trimis6: aw(6, 'trimis'), verificari6: aw(6, 'verificări'),
    urmand7: aw(7, 'urmând'), dezechipat: aw(7, 'dezechipat'), constatare7: aw(7, 'constatare'),
    iar8: aw(8, 'Iar'), remontare8: aw(8, 'remontare'), reconditionare: aw(8, 'recondiționare'), chiulasei8: aw(8, 'chiulasei'), blocului: aw(8, 'blocului'),
    sistemul9: aw(9, 'Sistemul'), admisie9: aw(9, 'admisie'), curatat9: aw(9, 'curățat'),
    iar10: aw(10, 'Iar'), probe10: aw(10, 'probe'), adaptarile10: aw(10, 'adaptările'), gata10: aw(10, 'gata'),
  };
  // HOOK: „CONSUM FOARTE MARE DE” → „ULEI” (impactul mare) → „ȘI ANTIGEL?”
  const B0 = .22, B1 = .85, B2 = 1.6, HB = A.masina0 - .1;
  return {
    hook: { tag: 'ANALIZĂ TEHNICĂ · CAZ #0062', end: HB },
    hideCap: [[0, HB - .05]],
    stages: [[A.unde0 - .1, 'SIMPTOME'], [A.in1 - .1, 'TESTARE'], [A.bine3 - .1, 'REZULTAT'], [A.motorul3 - .1, 'REPARAȚIA'], [A.iar10 - .1, 'EXTERNARE']],
    tags: {
      1: { lipsa: 'r', putere: 'r', consum: 'r', ulei: 'c', antigel: 'c' }, 2: { testare: 'y', chiulasei: 'c', substanta: 'y', contrast: 'y' }, 3: { pozitiv: 'r', demontat: 'y' },
      4: { chiulasa: 'c', bloc: 'c', motor: 'c', biturbo: 'c', demontat: 'y' }, 5: { laboratorul: 'g', verificari: 'g', garantie: 'g' }, 6: { injectie: 'c', laboratorul: 'g', verificari: 'g' },
      7: { dezechipat: 'y', complet: 'y' }, 8: { remontare: 'g', reconditionare: 'g', chiulasei: 'c', blocului: 'c', motor: 'c' }, 9: { admisie: 'c', curatat: 'g', profesional: 'g' }, 10: { gata: 'g', predare: 'g' },
    },
    items: [
      // ---- hook: boom
      { k: 'boom', t: B0, dur: HB - B0, txt: 'CONSUM FOARTE MARE DE', y: 590, size: 86, col: '#FFFFFF', from: 2.2, sh: 10, ca: 12, riser: false, bg: .45, glow: 'rgba(98,216,255,.5)' },
      { k: 'boom', t: B1, dur: HB - B1, txt: 'ULEI', y: 870, size: 300, col: '#FFB020', from: 3.8, sh: 24, ca: 30, bg: 1, glow: 'rgba(255,176,32,.6)' },
      { k: 'boom', t: B2, dur: HB - B2, txt: 'ȘI ANTIGEL?', y: 1110, size: 150, col: '#62D8FF', from: 2.6, sh: 14, ca: 18, riser: false, bg: .7, glow: 'rgba(98,216,255,.6)' },
      // ---- fișa pacientului
      { k: 'file', t0: HB + .02, t1: A.in1 - .3, no: '0062', ecg: 'crit', rows: [[A.masina0, 'PACIENT', 'MAZDA', 'c', 'automobile'], [A.masina0 + .15, 'MOTOR', '2.2 DIESEL', 'y', 'gear'],
        [A.piatra, 'UNITATE', 'PIATRA NEAMȚ', 'y', 'round_pushpin'], [A.lipsa1, 'SIMPTOME', 'LIPSĂ DE PUTERE', 'r', 'warning'], [A.consum1, 'CONSUM ULEI', 'FOARTE MARE', 'r', 'oil_drum'],
        [A.consum1b, 'CONSUM ANTIGEL', 'FOARTE MARE', 'r', 'droplet']] },
      // ---- testarea chiulasei cu substanță de contrast → pozitiv
      { k: 'schem', t0: A.in1 - .05, t1: A.motorul3 - .2, top: 268, h: 430, type: 'combustionTest', title: 'SCHEMĂ · TESTAREA CHIULASEI', sub: 'SUBSTANȚĂ DE CONTRAST',
        stepNames: ['TESTARE', 'PRINCIPIU', 'REZULTAT'],
        steps: [[A.in1 - .05, 'În urma constatării: testarea chiulasei', '', 0], [A.substanta - .05, 'Substanța de contrast reacționează la gazele de ardere', 'y', 0],
          [A.rezultatul - .05, 'Rezultatul a ieșit pozitiv', 'r', 1]] },
      { k: 'stamp', t: A.pozitiv - .03, t1: A.motorul3 - .25, y: 960, txt: 'POZITIV', col: 'red', s: .85 },
      // ---- reparația: motorul jos, biturbo + injecție în laborator
      { k: 'chip', t0: A.motorul3 - .05, t1: A.ansamblul - .3, y: 330, ph: [[A.motorul3 - .05, 'wrench', 'MOTORUL: DEMONTAT DE PE MAȘINĂ', 'yellow'],
        [A.pentru4 - .05, 'magnifying_glass_tilted_left', 'CONSTATARE AMĂNUNȚITĂ', 'blue'], [A.chiulasa4 - .05, 'magnifying_glass_tilted_left', 'CHIULASĂ + BLOC MOTOR', 'blue']] },
      { k: 'pipe', t0: A.ansamblul - .1, t1: A.sistemul6 - .3, ico: 'test_tube', title: 'BITURBO · ÎN LABORATORUL TURBO DOCTOR',
        steps: [[A.demontat4, 'wrench', 'DEMONTAT'], [A.trimis5, 'test_tube', 'TRIMIS ÎN<br>LABORATOR'], [A.verificari5, 'microscope', 'VERIFICĂRI'], [A.garantie5, 'shield', 'GARANȚIE<br>24 LUNI']] },
      { k: 'kin', t: A.n24 - .02, dur: 1.0, txt: '24 LUNI GARANȚIE', col: '#FFD21F', y: 1060, size: 120, rot: -3 },
      { k: 'kin', t: A.fara5 - .02, dur: 1.3, txt: 'FĂRĂ LIMITĂ DE KM', col: '#4ADE80', y: 1060, size: 110, rot: -3 },
      { k: 'pipe', t0: A.sistemul6 - .1, t1: A.urmand7 - .3, ico: 'test_tube', title: 'SISTEMUL DE INJECȚIE · LABORATOR',
        steps: [[A.demontat6, 'wrench', 'DEMONTAT'], [A.trimis6, 'test_tube', 'TRIMIS ÎN<br>LABORATOR'], [A.verificari6, 'microscope', 'VERIFICĂRI']] },
      { k: 'chip', t0: A.urmand7 - .05, t1: A.iar8 - .3, y: 330, ph: [[A.urmand7 - .05, 'wrench', 'URMEAZĂ: DEZECHIPAREA', 'yellow'], [A.dezechipat - .05, 'wrench', 'MOTORUL: DEZECHIPAT COMPLET', 'yellow'],
        [A.constatare7 - .05, 'magnifying_glass_tilted_left', 'CONSTATARE MAI AMĂNUNȚITĂ', 'blue']] },
      // ---- protocolul: recondiționare chiulasă + bloc, admisia curățată
      { k: 'schem', t0: A.iar8 - .05, t1: A.iar10 - .3, top: 268, h: 300, type: 'systemMap', title: 'PROTOCOL TURBO DOCTOR · MAZDA 2.2', sub: 'REPARAȚIA COMPLETĂ',
        P: {
          nodes: [[150, 70, 'CHIULASĂ', 'gear'], [457, 70, 'BLOC MOTOR', 'nutbolt'], [764, 70, 'BITURBO', 'dashing_away'], [300, 210, 'INJECȚIE', 'fuel_pump'], [614, 210, 'ADMISIE', 'broom']],
          links: [[0, 1], [1, 2], [3, 4], [0, 3, true], [2, 4, true]],
          events: [[A.iar8, 2, 'lab'], [A.iar8, 3, 'lab'], [A.reconditionare + .1, 0, 'lab'], [A.blocului, 1, 'lab'], [A.admisie9, 4, 'lab'], [A.curatat9, 4, 'ok']],
        },
        stepNames: ['PROTOCOL', 'MOTOR', 'ADMISIE'],
        steps: [[A.iar8 - .05, 'Remontare completă, cu recondiționare', ''], [A.reconditionare - .05, 'Recondiționare: chiulasa și blocul motor', 'y'],
          [A.sistemul9 - .05, 'Sistemul de admisie: demontat și curățat profesional', 'g']] },
      // ---- externarea
      { k: 'list', t0: A.iar10 - .1, t1: A.gata10 - .25, ico: 'test_tube', title: 'ÎNAINTE DE EXTERNARE', rows: [[A.probe10, 'PROBE DE DRUM'], [A.adaptarile10, 'ADAPTĂRI NECESARE']] },
      { k: 'stamp', t: A.gata10 - .05, t1: SEND - .1, y: 520, txt: 'GATA DE PREDARE', col: 'green', s: .85 },
      { k: 'tip', t0: SEND + .1, t1: TEND - .15, top: 520, title: 'REȚETA TURBO DOCTOR', sub: 'SFAT DE INGINER · MOTOR', ico: 'stethoscope',
        rows: [[SEND + .35, 'oil_drum', 'Consumă ulei și antigel? Testează chiulasa din timp'], [SEND + 1.15, 'test_tube', 'Substanța de contrast arată gazele de ardere din antigel'],
          [SEND + 1.95, 'warning', 'Nu doar completa ulei și antigel: află cauza']] },
    ],
    fx: [
      { k: 'punch', t: B0, a: .05, sh: 10 },
      { k: 'flash', t: B1 - .11, a: .75 }, { k: 'punch', t: B1, a: .16, sh: 34 }, { k: 'glitch', t: B1, d: .2 }, { k: 'shock', t: B1 + .01, x: 540, y: 870, r: 760, n: 2, col: '#FFB020' },
      { k: 'flash', t: B2 - .11, a: .45 }, { k: 'punch', t: B2, a: .08, sh: 16 }, { k: 'shock', t: B2 + .01, x: 540, y: 1110, r: 520, n: 1 },
      { k: 'glitch', t: HB - .05, d: .14 },
      { k: 'glitch', t: A.in1 - .12, d: .12 }, { k: 'punch', t: A.pozitiv, a: .07, sh: 10 }, { k: 'glitch', t: A.motorul3 - .12, d: .12 }, { k: 'glitch', t: A.ansamblul - .12, d: .12 },
      { k: 'punch', t: A.n24, a: .04 }, { k: 'glitch', t: A.sistemul6 - .12, d: .12 }, { k: 'glitch', t: A.iar8 - .12, d: .12 }, { k: 'glitch', t: A.iar10 - .12, d: .12 },
    ],
    sfx: [[HB - .1, 'whoosh', .6], [A.gata10, 'shimmer', .55]],
    bursts: [[B1 + .04, 540, 870, 8, 560, 1.7], [B2 + .04, 540, 1110, 4, 420, 1.2], [A.n24 + .1, 540, 1060, 6, 360, .9], [A.gata10, 540, 520, 6, 330, .8]],
  };
};
