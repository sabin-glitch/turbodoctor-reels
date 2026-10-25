// v2 – Reel r_1746 – „BMW N47: reparația corectă” (2 clipuri în ordinea filmării, fără tăieturi)
// clipuri: 0 compartiment motor (IMG_1746) · 63.70 compartiment motor (IMG_1747) · fără fețe în cadru
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND }) => {
  const A = {
    bmw: aw(0, 'BMW'), reparatie0: aw(0, 'reparație'), motorizarile0: aw(0, 'motorizările'), n47a: aw(0, 'N47.'),
    stim: aw(1, 'Știm'), destul: aw(1, 'destul'), multe1: aw(1, 'multe'), la1: aw(1, 'La'), admisiei: aw(1, 'admisiei,'), injectiei: aw(1, 'injecției'),
    evacuarii: aw(1, 'evacuării'), demontarea: aw(1, 'demontarea'), turbinei: aw(1, 'turbinei,'), dpf: aw(1, 'DPF-ului,'),
    tot: aw(2, 'tot'), galeria: aw(2, 'galeria'), injectoarele: aw(2, 'injectoarele'), verificate: aw(2, 'verificate,'), schimbat: aw(2, 'schimbat'),
    capacul: aw(2, 'capacul'), culbutori: aw(2, 'culbutori,'), probleme2: aw(2, 'probleme.'),
    inclusiv: aw(3, 'Inclusiv,'), pierderi: aw(3, 'pierderi'), sistemul3: aw(3, 'sistemul'),
    la4: aw(4, 'La'), aducem: aw(4, 'aducem'), viata: aw(4, 'viață'), si4: aw(4, 'Și'), distributie: aw(4, 'distribuție.'),
    curatarea: aw(5, 'Curățarea'), admisie5: aw(5, 'admisie,'), injectie5: aw(5, 'injecție'), evacuare5: aw(5, 'evacuare'), exploatarea: aw(5, 'exploatarea'),
    probleme6: aw(6, 'probleme'), desigur6: aw(6, 'Desigur,'), schimbului: aw(6, 'schimbului'), mult6: aw(6, 'mult'), surprize: aw(6, 'surprize'),
  };
  const CLIP = [0, 63.70];
  return {
    hook: { tag: 'ANALIZĂ TEHNICĂ · CAZ #1746', l1: 'BMW N47:', l1At: .1, l2: 'REPARAȚIA CORECTĂ', l2At: A.reparatie0 - .04, l2Col: '#4ADE80',
      car: 'BMW · MOTORIZAREA N47', carAt: A.motorizarile0, stk1: 'hammer_and_wrench', end: A.stim - .15 },
    hideCap: [[0, A.stim - .1]],
    stages: [[A.stim - .1, 'PROBLEMELE'], [A.la1 - .1, 'REPARAȚIA'], [A.la4 - .1, 'REZULTATUL'], [A.desigur6 - .1, 'SFATUL']],
    items: [
      { k: 'scan', t0: .12, t1: A.stim - .3, box: [150, 760, 780, 760], lab: 'SCANARE BMW...', lab2: 'MOTOR N47', at2: A.n47a - .04 },
      // fișa pacientului: N47, probleme cunoscute
      { k: 'file', t0: A.stim - .05, t1: A.la1 - .3, no: '1746', ecg: 'crit', rows: [[A.stim, 'PACIENT', 'BMW', 'c', 'automobile'], [A.destul, 'MOTOR', 'N47', 'y', 'gear'],
        [A.multe1, 'ISTORIC', 'MULTE PROBLEME CUNOSCUTE', 'r', 'warning']] },
      // schema reparației complete: admisie, injecție, evacuare (sus, peste motor)
      { k: 'schem', t0: A.la1 - .05, t1: A.inclusiv - .3, top: 268, h: 410, type: 'systemMap', title: 'SCHEMĂ · REPARAȚIA COMPLETĂ N47', sub: 'PROTOCOL TURBO DOCTOR',
        P: {
          nodes: [[150, 70, 'ADMISIE', 'dashing_away'], [457, 70, 'INJECȚIE', 'fuel_pump'], [764, 70, 'EVACUARE', 'fire'],
            [150, 210, 'GALERIE', 'nutbolt'], [457, 210, 'INJECTOARE', 'droplet'], [764, 210, 'TURBINĂ', 'gear'],
            [457, 350, 'CULBUTORI', 'oil_drum'], [764, 350, 'DPF', 'leaf']],
          links: [[0, 1], [1, 2], [0, 3, true], [1, 4, true], [4, 6, true], [2, 5, true], [5, 7, true]],
          events: [[A.admisiei, 0, 'lab'], [A.injectiei, 1, 'lab'], [A.evacuarii, 2, 'lab'], [A.turbinei, 5, 'lab'], [A.dpf, 7, 'lab'],
            [A.galeria, 3, 'lab'], [A.injectoarele, 4, 'lab'], [A.verificate, 4, 'ok'], [A.culbutori, 6, 'bad']],
        },
        stepNames: ['PROTOCOL', 'EVACUARE', 'ADMISIE', 'INJECȚIE', 'CULBUTORI'],
        steps: [[A.la1 - .05, 'Reparație completă: admisie, injecție, evacuare', ''], [A.demontarea - .05, 'Se demontează turbina și DPF-ul', 'y'],
          [A.tot - .05, 'Tot circuitul de admisie, cu galeria de admisie', 'y'], [A.injectoarele - .05, 'Injectoarele: date jos și verificate', 'g'],
          [A.schimbat - .05, 'Capacul de culbutori: schimbat, are mai multe probleme', 'r']] },
      // capacul de culbutori
      { k: 'def', t0: A.inclusiv - .05, t1: A.pierderi - .3, term: 'CAPACUL DE CULBUTORI', text: 'Capacul de deasupra chiulasei. Pe N47 are integrat și sistemul care curăță de ulei gazele din carter.' },
      { k: 'list', t0: A.pierderi - .1, t1: A.la4 - .3, ico: 'warning', title: 'CAPACUL DE CULBUTORI · PROBLEME', rows: [[A.pierderi, 'PIERDERI DE ULEI', 'bad'], [A.sistemul3, 'SISTEMUL DE EPURARE A GAZELOR', 'bad']] },
      { k: 'call', t0: 35.7, t1: 37.6, track: 'track_cap', p: [470, 880], lab: [640, 1130], h: 'CAPAC CULBUTORI', v: 'SCHIMBAT LA TURBO DOCTOR', cps: 36 },
      // rezultatul: motorul adus la viață
      { k: 'ecg', t0: A.la4 - .05, t1: A.si4 - .3, label: 'PULS MOTOR N47', ico: 'stethoscope', states: [[A.la4 - .05, 'crit', 'PROBLEME'], [A.aducem, 'ok', 'ADUS LA VIAȚĂ']] },
      { k: 'chip', t0: A.si4 - .05, t1: A.curatarea - .3, y: 330, ph: [[A.si4 - .05, 'gear', 'ȘI DISTRIBUȚIA, CÂND E NECESAR', 'blue']] },
      { k: 'pipe', t0: A.curatarea - .1, t1: A.exploatarea - .3, ico: 'test_tube', title: 'TRATAMENT ÎN LABORATORUL TURBO DOCTOR',
        steps: [[A.curatarea, 'broom', 'CURĂȚARE<br>+ SERVISARE'], [A.admisie5, 'dashing_away', 'ADMISIE'], [A.injectie5, 'fuel_pump', 'INJECȚIE'], [A.evacuare5, 'fire', 'EVACUARE']] },
      { k: 'list', t0: A.exploatarea - .1, t1: A.desigur6 - .3, ico: 'shield', title: 'REZULTATUL', rows: [[A.exploatarea, 'EXPLOATARE ÎNDELUNGATĂ'], [A.probleme6, 'FĂRĂ PROBLEME SERIOASE']] },
      // sfatul: schimbul de ulei
      { k: 'chip', t0: A.desigur6 - .05, t1: A.schimbului - .3, y: 330, ph: [[A.desigur6 - .05, 'oil_drum', 'ȘI TOTUȘI: SCHIMBUL DE ULEI', 'yellow']] },
      { k: 'cmp', t0: A.schimbului - .1, t1: SEND - .2, ico: 'oil_drum', title: 'SCHIMBUL DE ULEI', dimA: true,
        a: [A.schimbului, 'calendar', 'PRODUCĂTORUL', 'INTERVALUL RECOMANDAT'], b: [A.mult6, 'oil_drum', 'TURBO DOCTOR', 'MULT MAI DES'] },
      { k: 'kin', t: A.surprize - .02, dur: 1.2, txt: 'FĂRĂ SURPRIZE!', col: '#FFD21F', y: 1080, size: 120, rot: -3 },
      { k: 'tip', t0: SEND + .1, t1: TEND - .15, top: 520, title: 'REȚETA TURBO DOCTOR', sub: 'SFAT DE INGINER · BMW N47', ico: 'stethoscope',
        rows: [[SEND + .35, 'oil_drum', 'Schimbă uleiul mult mai des decât recomandă producătorul'], [SEND + 1.3, 'magnifying_glass_tilted_left', 'Admisie, injecție, evacuare: curățate și verificate complet'],
          [SEND + 2.25, 'warning', 'Pierderi de ulei la capacul de culbutori? Fă diagnoza din timp']] },
    ],
    fx: [
      { k: 'punch', t: A.n47a, a: .05 }, { k: 'glitch', t: A.la1 - .1, d: .12 }, { k: 'punch', t: A.culbutori, a: .04 },
      { k: 'glitch', t: A.la4 - .1, d: .12 }, { k: 'punch', t: A.viata, a: .05 }, { k: 'punch', t: A.mult6, a: .04 },
    ],
    sfx: [],
    bursts: [[A.viata + .05, 540, 420, 6, 320, .8]],
  };
};
