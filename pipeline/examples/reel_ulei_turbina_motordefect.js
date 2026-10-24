// v2 – Reel r_ulei – „Motor defect = consum de ulei la turbină, deși turbina e bună” (5 clipuri în ordinea filmării, fără tăieturi)
// clipuri: 0 selfie (IMG_1722) · 6.55 motor secționat (1723) · 21.25 selfie (1724) · 30.38 turbină secționată (1726) · 122.63 selfie (1727)
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND }) => {
  const A = {
    consum0: aw(0, 'consum'), desi0: aw(0, 'deși'), zilele: aw(0, 'Zilele'), comentariu: aw(0, 'comentariu'),
    din1: aw(1, 'Din'), realitate: aw(1, 'realitate'),
    treaba: aw(2, 'Treaba'), izolata: aw(2, 'izolată'), segment2: aw(2, 'segment'),
    doar: aw(3, 'Doar'), si4: aw(4, 'Și'), si5: aw(5, 'Și'),
    adica7: aw(7, 'Adică'), iar8: aw(8, 'iar'), daca8: aw(8, 'Dacă'),
    presiune10: aw(10, 'presiune'), pierde10: aw(10, 'pierde'), ghiciti: aw(10, 'Ghiciți'),
    turbina11: aw(11, 'Turbina'), bunaE11: ew(11, 'bună'),
    asa12: aw(12, 'Așa'), motor12: aw(12, 'motor'), desi12: aw(12, 'deși'),
    genul: aw(13, 'Genul'), diferenta: aw(13, 'diferența'), trebuie14: aw(14, 'Trebuie'), zi14: aw(14, 'zi'),
    la15: aw(15, 'La'), motor15: aw(15, 'motor'), turbine15: aw(15, 'turbine'), injectie15: aw(15, 'injecție'), evacuare15: aw(15, 'evacuare'),
    cam16: aw(16, 'cam'), nu16: aw(16, 'Nu'), la17: aw(17, 'la'), pusa17: aw(17, 'pusă'),
  };
  const CLIP = [0, 6.55, 21.25, 30.38, 122.63];
  return {
    hook: { tag: 'ANALIZĂ TEHNICĂ · CONSUM DE ULEI', l1: 'MOTOR DEFECT =', l1At: .3, l2: 'ULEI PE TURBINĂ!', l2At: A.consum0 - .04, l2Col: '#FF3B30',
      car: 'TURBINA NU E DE VINĂ', carAt: A.desi0, stk1: 'thinking_face', end: A.zilele - .15 },
    hideCap: [[0, A.zilele - .1]],
    stages: [[CLIP[1] + .05, 'SIMPTOMUL'], [A.treaba - .1, 'MECANISMUL'], [A.presiune10 - .1, 'CAUZA'], [CLIP[4] + .2, 'DIAGNOZA']],
    items: [
      // comentariul primit (peste motorul secționat)
      { k: 'comment', t0: A.comentariu - .1, t1: CLIP[2] - .2, head: 'Un comentariu primit de noi', y: 300,
        text: '„Ia uite, mă, ce mangleală are Turbo Doctor!” Motorul pierde compresie și turbina consumă ulei? Ce vrăjeală ieftină!' },
      { k: 'chip', t0: CLIP[2] + .15, t1: CLIP[3] - .2, y: 330, ph: [[CLIP[2] + .15, 'thinking_face', 'VRĂJEALĂ IEFTINĂ?', 'red'], [A.realitate - .05, 'check_mark_button', 'NU: REALITATE TEHNICĂ', 'green']] },
      // diagrame sus, cât explică pe turbina secționată
      { k: 'schem', t0: A.treaba - .1, t1: A.si5 - .3, top: 268, h: 410, type: 'turboBlowby', title: 'SCHEMĂ · ETANȘAREA TURBINEI', sub: 'SECȚIUNE',
        stepNames: ['TURBINA', 'SEGMENT', 'ULEI', 'LIMITĂ'],
        steps: [[A.treaba - .1, 'Admisia și evacuarea, separate de ansamblul central', '', 0], [A.izolata - .05, 'Pe fiecare parte etanșează un simplu segment', 'g', 0],
          [A.doar - .05, 'Segmentul ține circuitul de ulei în ansamblul central', 'g', 0], [A.si4 - .05, 'Un segment nu poate etanșa complet', 'y', 1]] },
      { k: 'call', t0: A.segment2 - .1, t1: 47.3, track: 'track_seg', p: [770, 905], lab: [600, 1165], h: 'SEGMENT', v: 'ETANȘAREA TURBINEI', cps: 36 },
      { k: 'schem', t0: A.si5 - .05, t1: A.asa12 - .3, top: 268, h: 410, type: 'turboBlowby', title: 'SCHEMĂ · DE CE DĂ ULEI O TURBINĂ BUNĂ', sub: 'PRESIUNI',
        stepNames: ['PRINCIPIU', 'ADMISIE', 'EVACUARE', 'PRESIUNE ↑', 'CAUZA', 'EFECT'],
        steps: [[A.si5 - .05, 'Turbina se bazează pe o diferență de presiune', '', 2], [A.adica7 - .05, 'Admisie: presiune pozitivă', 'g', 3], [A.iar8 - .05, 'Evacuare: presiune pozitivă', 'g', 4],
          [A.daca8 - .05, 'Presiune suplimentară în ansamblul central', 'r', 5], [A.presiune10 - .05, 'Motorul pierde compresie: gazele ajung pe retur', 'r', 6],
          [A.turbina11 - .05, 'Turbina, deși e bună, dă ulei pe evacuare sau admisie', 'r', 7]] },
      { k: 'chip', t0: A.asa12 - .05, t1: CLIP[4] - .15, y: 330, ph: [[A.asa12 - .05, 'warning', 'CONSUM DE ULEI LA TURBINĂ', 'red'], [A.desi12 - .05, 'check_mark_button', 'TURBINA E BUNĂ · CAUZA E MOTORUL', 'green']] },
      { k: 'stamp', t: A.motor12 - .04, t1: A.desi12 - .2, y: 760, txt: 'MOTOR DEFECT', col: 'red', s: 1.0, rot: -7 },
      // concluzia (selfie): chip-uri compacte deasupra capului
      { k: 'chip', t0: A.genul - .05, t1: A.trebuie14 - .3, y: 330, ph: [[A.genul - .05, 'magnifying_glass_tilted_left', 'DETALII CRUCIALE ÎN DIAGNOZĂ', 'blue'], [A.diferenta - .05, 'warning', 'DIFERENȚA DINTRE SUCCES ȘI EȘEC', 'red']] },
      { k: 'chip', t0: A.trebuie14 - .05, t1: A.la15 - .3, y: 330, ph: [[A.trebuie14 - .05, 'brain', 'ÎNVĂȚAT DIN CAZURI REALE', 'blue'], [A.zi14 - .05, 'calendar', 'ZI DE ZI, ÎN TURBO DOCTOR', 'blue']] },
      { k: 'chip', t0: A.la15 - .05, t1: A.cam16 - .3, y: 330, ph: [[A.la15 - .05, 'stethoscope', 'SPECIALIȘTI ÎN DIAGNOZĂ', 'blue'], [A.motor15 - .03, 'gear', 'MOTOR', 'blue'], [A.turbine15 - .03, 'gear', 'MOTOR · TURBINE', 'blue'],
        [A.injectie15 - .03, 'gear', 'MOTOR · TURBINE · INJECȚIE', 'blue'], [A.evacuare15 - .03, 'gear', 'MOTOR · TURBINE · INJECȚIE · EVACUARE', 'blue']] },
      { k: 'chip', t0: A.cam16 - .05, t1: A.la17 - .3, y: 330, ph: [[A.cam16 - .05, 'handshake', 'TOATE LUCREAZĂ ÎMPREUNĂ', 'green'], [A.nu16 - .05, 'warning', 'NU SUNT LA ÎNDEMÂNA ORICUI', 'red']] },
      { k: 'chip', t0: A.la17 - .05, t1: SEND - .2, y: 330, ph: [[A.la17 - .05, 'check_mark_button', 'ȘTIM CE AVEM DE FĂCUT', 'green'], [A.pusa17 - .05, 'automobile', 'ÎNAPOI PE DRUM', 'green']] },
    ],
    fx: [
      { k: 'glitch', t: A.ghiciti, d: .12 }, { k: 'punch', t: A.turbina11, a: .04 },
      ],
    sfx: [],
    bursts: [],
  };
};
