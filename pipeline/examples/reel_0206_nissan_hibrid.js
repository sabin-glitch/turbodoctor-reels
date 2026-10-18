// v2 – Reel r0206 – Turbo Doctor Piatra Neamț, Nissan Qashqai 2023 1.5 hibrid (e-POWER, 3 pistoane): pierderi de antigel -> EGR + radiator invertor
window.REEL_CFG = ({ aw, ew, cw, cwe, S0, SEND, TEND }) => {
  const A = {
    nissan: aw(0, 'Nissan'), motoriz: aw(0, 'motorizarea'), hibrid: aw(0, 'hibrid'), pist: aw(0, 'pistoane'), piatra: aw(0, 'Piatra'), pierderi0: aw(0, 'pierderi'), antigel0E: ew(0, 'antigel'),
    sa1: aw(1, 'S-a'), test: aw(1, 'test'), substanta: aw(1, 'substanță'), contrast: aw(1, 'contrast'), negativ: aw(1, 'negativ'), testul: aw(1, 'Testul'), presiune: aw(1, 'presiune'),
    ident1: aw(1, 'identificat'), problema1: aw(1, 'problemă'), partea: aw(1, 'partea'), egr: aw(1, 'EGR'), foarte: aw(1, 'foarte'), micaE: ew(1, 'mică'), ident2: aw(1, 'identificat', 1),
    bine2: aw(2, 'Bineînțeles'), radiator: aw(2, 'radiatorul'), inverterE: ew(2, 'inverterului'),
    masina3: aw(3, 'Mașina'), demontare: aw(3, 'demontare'), constatare: aw(3, 'constatare'),
    ulterior4: aw(4, 'Ulterior'), inlocui: aw(4, 'înlocui'), adapt: aw(4, 'adaptări'), probe: aw(4, 'probe'),
    testare: aw(5, 'testare'), vasul: aw(5, 'vasul'), ambele: aw(5, 'ambele'), ulterior5: aw(5, 'Ulterior'), gata: aw(5, 'gata'),
  };
  return {
    hook: { tag: 'ANALIZĂ TEHNICĂ · CAZ #0206', l1: 'HIBRIDUL PIERDE', l1At: .05, l2: 'ANTIGEL!', l2At: cw('antigel') - .04, l2Col: '#62D8FF', car: 'NISSAN QASHQAI 1.5 HIBRID', carAt: .75, stk1: 'droplet' },
    stages: [[S0, 'SIMPTOME'], [A.sa1 - .1, 'ANALIZE'], [A.partea - .1, 'DIAGNOSTIC'], [A.masina3 - .1, 'TRATAMENT']],
    items: [
      { k: 'scan', t0: .12, t1: S0 - .15, box: [20, 980, 1040, 760], labBelow: false, lab: 'SCANARE CIRCUITE DE RĂCIRE...', lab2: 'PIERDERI DE ANTIGEL', at2: cw('antigel') + .15 },
      { k: 'file', t0: A.nissan - .1, t1: A.sa1 - .3, no: '0206', ecg: 'crit', rows: [[A.nissan, 'PACIENT', 'NISSAN QASHQAI 2023', 'c', 'automobile'], [A.motoriz, 'MOTORIZARE', '1.5 HIBRID e-POWER', 'y', 'battery'],
        [A.pist - .1, 'CONFIGURAȚIE', '3 PISTOANE', 'y', 'gear'], [A.piatra, 'UNITATE', 'PIATRA NEAMȚ', 'y', 'round_pushpin'], [A.pierderi0, 'INTERNAT CU', 'PIERDERI DE ANTIGEL', 'r', 'droplet']] },
      { k: 'file', t0: A.sa1 - .1, t1: A.presiune - .1, no: '0206', title: 'BULETIN DE ANALIZE', ico: 'test_tube', rows: [[A.test, 'TEST', 'GARNITURĂ DE CHIULASĂ', 'c', 'test_tube'], [A.substanta, 'METODĂ', 'SUBSTANȚĂ DE CONTRAST', 'c', 'droplet'],
        [A.negativ - .05, 'REZULTAT', 'NEGATIV', 'g', 'check_mark_button']], stamp: [A.negativ + .1, 'GARNITURĂ OK', 'green'] },
      { k: 'gauge', t0: A.presiune, t1: A.partea - .3, ico: 'counter', title: 'TEST DE PRESIUNE', sub: 'SISTEM DE RĂCIRE', ends: ['0', 'MAX'], mid: 'BAR', zones: [[0, .5, '#FF4B4B'], [.5, .65, '#FFD21F'], [.65, 1, '#4ADE80']],
        needle: [[A.presiune, .04], [A.presiune + .9, .8], [A.ident1 - .2, .8], [A.problema1 + .4, .42]], read: [[A.presiune + .1, 'SISTEM PUS SUB PRESIUNE...', '#62D8FF'], [A.ident1 - .05, '▼ PRESIUNEA SCADE = PIERDERE', '#FF4B4B']] },
      { k: 'schem', t0: A.partea - .1, t1: A.masina3 - .3, type: 'coolingHybrid', P: { egrLab: 'ZONA EGR' }, title: 'SCHEMĂ · RĂCIREA UNUI HIBRID', sub: 'DIAGNOSTIC', stepNames: ['CIRCUIT 1', 'HIBRID', 'CIRCUIT 2'],
        steps: [[A.partea - .1, 'Circuitul motorului: pierdere foarte mică în zona EGR', 'r', 1], [A.bine2 - .05, 'Hibridul are 2 circuite: al doilea răcește invertorul', '', 1], [A.radiator - .05, 'Circuitul invertorului: radiatorul pierde antigel', 'r', 2]] },
      { k: 'kin', t: A.ident2 - .02, dur: .95, txt: 'IDENTIFICATĂ!', col: '#FFD21F', y: 1080, size: 118, rot: -3 },
      { k: 'chip', t0: A.masina3 - .1, t1: A.ulterior4 - .3, y: 330, ph: [[A.masina3 - .1, 'hammer_and_wrench', 'MAȘINA INTRĂ ÎN DEMONTARE', ''], [A.constatare - .05, 'microscope', 'CONSTATARE AMĂNUNȚITĂ', 'blue']] },
      { k: 'scan', t0: A.constatare, t1: A.ulterior4 - .3, box: [100, 560, 880, 900], lab: 'MOTOR + PIERDERI DE ANTIGEL...' },
      { k: 'pipe', t0: A.ulterior4 - .1, t1: A.ulterior5 - .3, ico: 'hammer_and_wrench', title: 'TRATAMENT', steps: [[A.inlocui - .05, 'nutbolt', 'PIESE<br>ÎNLOCUITE'], [A.adapt - .05, 'gear', 'ADAPTĂRI'], [A.probe - .05, 'automobile', 'PROBE<br>DE DRUM'], [A.testare - .05, 'droplet', 'TEST DE<br>PRESIUNE']] },
      { k: 'call', t0: A.testare + .25, t1: A.ulterior5 - .35, track: 'track_tank1', p: [440, 707], lab: [720, 640], h: 'TEST DE PRESIUNE', v: 'VASUL 1', cps: 40 },
      { k: 'call', t0: A.vasul - .05, t1: A.ulterior5 - .35, track: 'track_tank2', p: [70, 1110], lab: [420, 1180], h: 'TEST DE PRESIUNE', v: 'VASUL 2', cps: 40 },
      { k: 'stamp', t: A.gata - .05, t1: SEND - .1, y: 560, txt: 'GATA DE PREDARE', col: 'green', s: .85 },
      { k: 'tip', t0: SEND + .1, t1: TEND - .15, top: 520, title: 'REȚETA TURBO DOCTOR', sub: 'SFAT DE INGINER · HIBRID', ico: 'stethoscope',
        rows: [[SEND + .35, 'droplet', 'Verifică lunar AMBELE vase de expansiune, cu motorul rece'], [SEND + 1.15, 'magnifying_glass_tilted_left', 'Nivelul scade, dar nu vezi pete pe jos? Cere un test de presiune'], [SEND + 1.95, 'battery', 'Invertorul are circuitul lui de răcire: verifică-l și pe el']] },
    ],
    fx: [
      { k: 'red', t0: A.pierderi0 - .05, t1: A.antigel0E + .1, max: 1.2 },
      { k: 'xray', t0: A.contrast - .05, t1: A.contrast + .85 },
      { k: 'green', t0: A.negativ + .05, t1: A.negativ + .75, silent: true }, { k: 'punch', t: A.negativ, a: .04 },
      { k: 'red', t0: A.egr - .05, t1: A.micaE + .1, max: 1.6 }, { k: 'punch', t: A.egr, a: .05, sh: 6 }, { k: 'punch', t: A.radiator, a: .05, sh: 6 },
      { k: 'xray', t0: A.constatare - .05, t1: A.constatare + .8 },
      { k: 'green', t0: A.gata - .1, t1: SEND - .15 },
      { k: 'glitch', t: A.presiune - .2, d: .12 }, { k: 'glitch', t: A.partea - .3, d: .12 },
    ],
    bursts: [[A.gata, 540, 560, 6, 330, .8]],
  };
};
