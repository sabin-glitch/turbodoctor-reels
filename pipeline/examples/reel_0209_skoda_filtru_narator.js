// v2 – Reel r0209 – Skoda Octavia: filtrul de ulei „beton” (narator, clipul întreg în ordinea filmată)
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND }) => {
  const A = {
    beton0: aw(0, 'beton'), avem: aw(1, 'Avem'), skoda: aw(1, 'Skoda'), schimbul: aw(1, 'schimbul'), uleiE: ew(1, 'ulei'),
    am: aw(2, 'Am'), filtrul: aw(2, 'filtrul'), acoperit: aw(2, 'acoperit'), depuneriE: ew(2, 'depuneri'),
    iar3: aw(3, 'Iar'), intarit: aw(3, 'întărit'), beton3: aw(3, 'beton'), prin: aw(3, 'Prin'), nimicE: ew(3, 'nimic'),
    atunci: aw(4, 'Atunci'), supapa: aw(4, 'supapa'), bypassE: ew(4, 'bypass'),
    iar5: aw(5, 'iar'), nefiltrat: aw(5, 'nefiltrat'), turbina: aw(5, 'turbină'), cuzineti: aw(5, 'cuzineți'), cameE: ew(5, 'came'),
  };
  const KNOCK = [13.52, 14.15];  // loviturile reale în filtru, din sunetul clipului
  return {
    hook: { tag: 'ANALIZĂ TEHNICĂ · CAZ #0209', l1: 'FILTRUL DE ULEI...', l1At: .05, l2: 'BETON!', l2At: A.beton0 + .3, l2Col: '#FF3B30', car: 'SKODA OCTAVIA', carAt: .9, stk1: 'face_screaming_in_fear', end: A.avem - .15 },
    hideCap: [[0, A.avem - .05]],
    stages: [[A.avem + .05, 'CONSULTAȚIE'], [A.am - .1, 'ANALIZĂ'], [A.iar3 - .1, 'DIAGNOSTIC'], [A.atunci - .1, 'RISCURI']],
    items: [
      { k: 'scan', t0: .12, t1: A.avem - .25, box: [40, 640, 1000, 540], lab: 'SCANARE PACIENT...', lab2: 'FILTRU DE ULEI SUSPECT', at2: A.beton0 + .3 },
      { k: 'file', t0: A.avem - .05, t1: A.am - .25, no: '0209', ecg: 'crit', rows: [[A.skoda, 'PACIENT', 'SKODA OCTAVIA', 'c', 'automobile'], [A.schimbul, 'MOTIV VIZITĂ', 'SCHIMB DE ULEI', 'c', 'oil_drum'],
        [A.uleiE - .1, 'PROCEDURĂ', 'FILTRUL VECHI, LA CONTROL', 'y', 'magnifying_glass_tilted_left']] },
      { k: 'chip', t0: A.am - .05, t1: A.iar3 - .3, y: 330, ph: [[A.am - .05, 'microscope', 'ANALIZĂ: FILTRUL DE ULEI', 'blue'], [A.acoperit - .05, 'warning', 'ACOPERIT COMPLET DE DEPUNERI', 'red']] },
      { k: 'scan', t0: A.filtrul, t1: A.iar3 - .35, box: [60, 640, 960, 900], lab: 'ANALIZĂ FILTRU...', lab2: 'NĂMOL ÎNTĂRIT', at2: A.acoperit },
      { k: 'chip', t0: A.iar3 - .05, t1: A.atunci - .3, y: 330, ph: [[A.iar3 - .05, 'magnifying_glass_tilted_left', 'DEPUNERI ÎNTĂRITE', 'red'], [A.prin - .05, 'cross_mark', 'FLUX DE ULEI: BLOCAT', 'red']] },
      { k: 'stamp', t: A.beton3 - .04, t1: A.prin + .55, y: 760, txt: 'BETON!', col: 'red', s: 1.35, rot: -8 },
      { k: 'schem', t0: A.atunci - .15, t1: A.iar5 - .15, type: 'oilFilter', title: 'SCHEMĂ · CE FACE UN FILTRU BLOCAT', sub: 'MECANISM', stepNames: ['NORMAL', 'COLMATARE', 'BYPASS'],
        steps: [[A.atunci - .15, 'Filtru curat: uleiul trece prin hârtia filtrantă', 'g'], [A.atunci + .6, 'Depunerile astupă filtrul: uleiul abia mai trece', 'y'], [A.supapa - .05, 'Supapa de bypass se deschide: ulei NEFILTRAT spre motor', 'r']] },
      { k: 'list', t0: A.iar5 - .05, t1: SEND - .2, ico: 'warning', title: 'CE RISCĂ MOTORUL', rows: [[A.nefiltrat, 'ULEI NEFILTRAT PRIN MOTOR', 'bad'], [A.turbina, 'TURBINA: LAGĂRE UZATE', 'bad'], [A.cuzineti, 'CUZINEȚI ȘI AXE CU CAME', 'bad']] },
      { k: 'tip', t0: SEND + .1, t1: TEND - .15, top: 520, title: 'REȚETA TURBO DOCTOR', sub: 'SFAT DE INGINER · ULEI ȘI FILTRU', ico: 'stethoscope',
        rows: [[SEND + .35, 'oil_drum', 'Schimbă uleiul ȘI filtrul la intervalul recomandat'], [SEND + 1.3, 'calendar', 'Mult oraș și drumuri scurte? Schimbă mai des'], [SEND + 2.25, 'test_tube', 'Ulei cu specificația cerută de producător']] },
    ],
    fx: [
      { k: 'red', t0: A.beton0 + .25, t1: A.beton0 + .95, silent: true, max: 1.2 },
      { k: 'punch', t: A.beton3, a: .06, sh: 8 }, { k: 'red', t0: A.beton3 - .05, t1: A.beton3 + .9, silent: true, max: 1.4 },
      { k: 'punch', t: KNOCK[0], a: .04 }, { k: 'punch', t: KNOCK[1], a: .035 },
      { k: 'glitch', t: A.supapa - .1, d: .12 },
    ],
    sfx: [[A.acoperit, 'scan', .4]],
    bursts: [],
  };
};
