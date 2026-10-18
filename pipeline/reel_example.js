// v2 – Reel r0214 – Ford Transit 2.2: joc axial + radial -> miezul turbinei rupt (abordare inginerească)
window.REEL_CFG = ({ aw, ew, cw, cwe, S0, SEND, TEND }) => {
  const A = {
    ford: aw(0, 'Ford'), piatra: aw(0, 'Piatra'), pierderea: aw(1, 'pierderea'), probleme2: aw(1, 'probleme', 1), turbina1: aw(1, 'turbină'),
    in2: aw(2, 'În'), ident: aw(2, 'identificat'), joc: aw(3, 'joc'), axial: aw(3, 'axial'), radial: aw(3, 'radial'), marit: aw(3, 'mărit'), miezul: aw(3, 'miezul'), rupt: aw(3, 'rupt'), ruptE: ew(3, 'rupt'),
    bine4: aw(4, 'Bineînțeles'), trimisa: aw(4, 'trimisă'), verif: aw(4, 'verificări'), recond: aw(4, 'recondiționare'), garantie: aw(4, 'garanție'), n24: aw(4, '24'), luniE: ew(4, 'luni'),
    sist: aw(5, 'Sistemul'), verificat5: aw(5, 'verificat'), curatat: aw(5, 'curățat'), iar: aw(5, 'iar'), remontare: aw(5, 'remontare'), adapt: aw(5, 'adaptările'), probe: aw(5, 'probe'), gata: aw(5, 'gata'),
  };
  return {
    hook: { tag: 'ANALIZĂ TEHNICĂ · CAZ #0214', l1: 'MIEZUL TURBINEI', l1At: .05, l2: 'RUPT!', l2At: cw('rupt') - .04, l2Col: '#FF3B30', car: 'FORD TRANSIT 2.2', carAt: .9 },
    stages: [[S0, 'SIMPTOME'], [A.in2 - .1, 'INVESTIGAȚIE'], [A.joc - .1, 'CAUZA'], [A.bine4 - .1, 'SOLUȚIA']],
    items: [
      { k: 'scan', t0: .12, t1: S0 - .15, box: [210, 860, 540, 540], lab: 'SCANARE TURBINĂ...', lab2: 'MIEZ RUPT', at2: cw('rupt') - .04 },
      { k: 'file', t0: A.ford - .1, t1: A.in2 - .3, no: '0214', ecg: 'crit', rows: [[A.ford, 'PACIENT', 'FORD TRANSIT 2.2', 'c', 'automobile'], [A.piatra, 'UNITATE', 'PIATRA NEAMȚ', 'y', 'round_pushpin'],
        [A.pierderea, 'SIMPTOME', 'PIERDERE DE ULEI', 'r', 'droplet'], [A.probleme2, '', 'PROBLEME LA TURBINĂ', 'r', 'warning']] },
      { k: 'scan', t0: A.in2, t1: A.joc - .2, box: [250, 880, 520, 560], lab: 'VERIFICARE AX TURBINĂ...', lab2: 'JOC MĂRIT DETECTAT', at2: A.ident },
      { k: 'schem', t0: A.joc - .15, t1: A.bine4 - .25, type: 'turboPlay', title: 'SCHEMĂ · AXUL TURBINEI', sub: 'SECȚIUNE', stepNames: ['NORMAL', 'DEFECT 1', 'DEFECT 2', 'REZULTAT'],
        steps: [[A.joc - .15, 'Axul se rotește pe lagăre, în pelicula de ulei', ''], [A.axial - .05, 'JOC AXIAL: axul se mișcă pe lungimea lui', 'r'], [A.radial - .05, 'JOC RADIAL: axul se mișcă lateral, roțile ating carcasa', 'r'], [A.miezul - .05, 'Miezul turbinei s-a rupt', 'r']] },
      { k: 'ring', t0: A.joc, t1: A.marit + .5, p: [430, 1195], r: 130, col: '#FF4B4B' },
      { k: 'pipe', t0: A.bine4 - .1, t1: A.sist - .3, ico: 'test_tube', title: 'TRATAMENT ÎN LABORATORUL TURBO DOCTOR', steps: [[A.trimisa, 'test_tube', 'TRIMISĂ<br>ÎN LABORATOR'], [A.verif, 'microscope', 'VERIFICĂRI'], [A.recond, 'hammer_and_wrench', 'RECONDIȚIONARE'], [A.garantie, 'shield', 'GARANȚIE<br>24 LUNI']] },
      { k: 'kin', t: A.n24 - .02, dur: 1.0, txt: '24 LUNI GARANȚIE', col: '#FFD21F', y: 1060, size: 120, rot: -3 },
      { k: 'chip', t0: A.sist - .1, t1: A.iar - .3, y: 330, ph: [[A.sist - .1, 'magnifying_glass_tilted_left', 'ADMISIA: VERIFICATĂ', 'blue'], [A.curatat - .05, 'sparkles', 'ADMISIA: CURĂȚATĂ', 'green']] },
      { k: 'list', t0: A.iar - .1, t1: A.gata - .25, ico: 'test_tube', title: 'ÎNAINTE DE EXTERNARE', rows: [[A.remontare, 'REMONTARE COMPLETĂ'], [A.adapt, 'ADAPTĂRI NECESARE'], [A.probe, 'PROBE DE DRUM']] },
      { k: 'stamp', t: A.gata - .05, t1: SEND - .1, y: 520, txt: 'GATA DE PREDARE', col: 'green', s: .85 },
      { k: 'tip', t0: SEND + .1, t1: TEND - .15, top: 520, title: 'REȚETA TURBO DOCTOR', sub: 'SFAT DE INGINER · TURBO', ico: 'stethoscope',
        rows: [[SEND + .35, 'oil_drum', 'Ulei bun, schimbat la timp: turbina trăiește din ulei'], [SEND + 1.15, 'hourglass', 'După drum solicitant: 30–60 s la relanti, apoi oprești'], [SEND + 1.95, 'warning', 'Fum sau pierderi de ulei? Fă diagnoza din timp']] },
    ],
    fx: [
      { k: 'red', t0: A.pierderea - .05, t1: A.turbina1 + .4, max: 1.6 },
      { k: 'punch', t: A.axial, a: .04 }, { k: 'punch', t: A.radial, a: .04 }, { k: 'punch', t: A.rupt, a: .07, sh: 10 }, { k: 'red', t0: A.miezul - .05, t1: A.ruptE + .3, silent: true, max: 1.2 },
      { k: 'green', t0: A.recond - .05, t1: A.recond + .7 }, { k: 'green', t0: A.gata - .1, t1: SEND - .15, silent: true },
      { k: 'glitch', t: A.joc - .2, d: .14 },
    ],
    sfx: [[A.gata, 'shimmer', .55]],
    bursts: [[A.recond, 540, 520, 6, 320, .8], [A.n24 + .1, 540, 1060, 6, 360, .9], [A.gata, 540, 520, 6, 330, .8]],
  };
};
