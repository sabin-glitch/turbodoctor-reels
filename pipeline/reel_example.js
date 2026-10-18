// Reel r0214 – Turbo Doctor Piatra Neamț, Ford Transit 2.2: pierdere de ulei + turbină -> joc axial/radial, miez rupt
window.REEL_CFG = ({ aw, ew, cw, cwe, S0, SEND }) => {
  const A = {
    ford: aw(0, 'Ford'), piatra: aw(0, 'Piatra'), cu1: aw(1, 'cu'), pierderea: aw(1, 'pierderea'), turbina1: aw(1, 'turbină'),
    in2: aw(2, 'În'), demontarii: aw(2, 'demontării'), ident: aw(2, 'identificat'), joc: aw(3, 'joc'), axial: aw(3, 'axial'), radial: aw(3, 'radial'), marit: aw(3, 'mărit'),
    se3: aw(3, 'Se'), miezul: aw(3, 'miezul'), rupt: aw(3, 'rupt'), ruptE: ew(3, 'rupt'),
    bine4: aw(4, 'Bineînțeles'), trimisa: aw(4, 'trimisă'), verif4: aw(4, 'verificări'), recond: aw(4, 'recondiționare'), garantie: aw(4, 'garanție'), n24: aw(4, '24'),
    sist: aw(5, 'Sistemul'), verificat5: aw(5, 'verificat'), curatat: aw(5, 'curățat'), iar: aw(5, 'iar'), remontare: aw(5, 'remontare'), adapt: aw(5, 'adaptările'), probe: aw(5, 'probe'), gata: aw(5, 'gata'),
  };
  const F = t => Math.round(t * 30);
  return {
    hook: { pill: ['round_pushpin', 'TURBO DOCTOR PIATRA NEAMȚ'], l1: 'FORD TRANSIT <span class="y">2.2</span>', l2: 'MIEZ TURBINĂ RUPT!', l2At: cw('miezul'),
      chips: [['cross_mark', 'JOC AXIAL'], ['cross_mark', 'JOC RADIAL']], chipsAt: cw('rupt') + .05, stk1: 'police_light', stk2: 'warning' },
    chaps: [[A.ford - .2, A.in2 - .2, 'CONSULTAȚIE', 'stethoscope'], [A.in2 - .2, A.bine4 - .2, 'DIAGNOSTIC', 'microscope'],
            [A.bine4 - .2, A.iar - .2, 'TRATAMENT', 'hammer_and_wrench'], [A.iar - .2, SEND, 'EXTERNARE', 'check_mark_button']],
    items: [
      { k: 'file', t0: A.ford - .1, t1: A.in2 - .3, y: 450, no: '0214', rows: [[A.ford, 'PACIENT', 'FORD TRANSIT 2.2', 'c', 'automobile'], [A.piatra, 'UNITATE', 'PIATRA NEAMȚ', 'y', 'round_pushpin'],
        [A.pierderea, 'INTERNAT CU', 'PIERDERE DE ULEI', 'r', 'droplet'], [A.turbina1, '', 'PROBLEME LA TURBINĂ', 'r']] },
      { k: 'chip', t0: A.in2 - .1, t1: A.joc - .3, y: 310, ph: [[A.in2 - .1, 'microscope', 'TURBINA DEMONTATĂ', 'blue']] },
      { k: 'file', t0: A.joc - .15, t1: A.bine4 - .3, y: 450, no: '0214', title: 'REZULTAT INVESTIGAȚIE', ico: 'microscope', rows: [[A.axial, 'DIAGNOSTIC', 'JOC AXIAL + RADIAL MĂRIT', 'r'], [A.miezul, '', 'MIEZUL TURBINEI RUPT', 'r']], stamp: [A.rupt + .12, 'GRAV', 'red'] },
      { k: 'art', t0: A.bine4 - .1, t1: A.garantie - .45, y: 460, art: 'turbo', ico: 'test_tube', title: 'TURBINA', status: [[A.trimisa, '<img src="assets/emoji/test_tube.png">VERIFICARE ÎN LABORATOR', '#0369A1'], [A.recond, '<img src="assets/emoji/sparkles.png">RECONDIȚIONARE', '#15803D']] },
      { k: 'stat', t0: A.garantie - .2, t1: A.sist - .3, y: 450, ico: 'shield', title: 'GARANȚIE TURBO DOCTOR', from: 0, to: 24, at: A.n24 - .1, dur: .6, unit: 'LUNI', sub: 'PENTRU TURBINA RECONDIȚIONATĂ', subIco: 'check_mark_button' },
      { k: 'art', t0: A.sist - .1, t1: A.iar - .3, y: 460, art: 'intake', ico: 'broom', title: 'SISTEMUL DE ADMISIE', status: [[A.verificat5, '<img src="assets/emoji/magnifying_glass_tilted_left.png">VERIFICAT', '#0369A1'], [A.curatat, '<img src="assets/emoji/sparkles.png">CURĂȚAT', '#15803D']] },
      { k: 'list', t0: A.iar - .1, t1: A.gata - .25, y: 450, ico: 'test_tube', title: 'ÎNAINTE DE EXTERNARE', rows: [[A.remontare, 'REMONTARE COMPLETĂ'], [A.adapt, 'ADAPTĂRI NECESARE'], [A.probe, 'PROBE DE DRUM']] },
      { k: 'stamp', t: A.gata - .05, t1: SEND - .15, y: 470, txt: 'GATA DE PREDARE', col: 'green', s: .85 },
    ],
    rings: [{ f0: F(A.joc - .1), f1: F(A.marit + .6), track: 'track_inlet', r: 130, label: 'JOC AXIAL + RADIAL', ico: 'magnifying_glass_tilted_left', col: '#FF4B4B', cls: 'red', lx: 760, ly: 1150 }],
    fx: [
      { k: 'red', t0: A.pierderea - .05, t1: A.turbina1 + .6 },
      { k: 'xray', t0: A.demontarii - .05, t1: A.demontarii + .95 },
      { k: 'red', t0: A.miezul - .05, t1: A.ruptE + .3, silent: true }, { k: 'punch', t: A.rupt, a: .07, sh: 10 }, { k: 'punch', t: A.axial, a: .04 },
      { k: 'green', t0: A.recond - .05, t1: A.recond + .8 }, { k: 'green', t0: A.gata - .1, t1: SEND - .2, silent: true },
    ],
    sfx: [[A.gata, 'shimmer', .55]],
    bursts: [[A.recond, 540, 460, 6, 300, .8], [A.n24 + .5, 540, 450, 6, 320, .8], [A.gata, 540, 470, 6, 330, .8]],
  };
};
