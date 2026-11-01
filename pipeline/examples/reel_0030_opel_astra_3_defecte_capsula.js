// v2 – Reel r0030 – „Opel Astra J 1.7: nu trage și trebuie repornită → 3 defecte găsite” (IMG_0030, un singur clip, fără tăieturi)
// clip: 0 compartiment motor (Piatra Neamț) · 30–51 supapa răcitorului de gaze (arătată cu degetul) · 52–79 turbina + capsula vacuumatică · 80–92 compartiment motor · fără fețe
// Hook: titlu boom „NU TRAGE?” + „3 DEFECTE GĂSITE” peste prima frază (fidel: DPF cu cenușă, răcitor de gaze blocat, capsula turbinei spartă). Fără CTA pe imagine (25.10).
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND }) => {
  const A = {
    opel: aw(0, 'Opel'), motorizare: aw(0, 'motorizare'), masina0: aw(0, 'mașină'), piatra: aw(0, 'Piatra'),
    unde: aw(1, 'unde'), nu1: aw(1, 'nu'), trage: aw(1, 'trage'), repornirea: aw(1, 'repornirea'),
    in2: aw(2, 'În'), filtru2: aw(2, 'filtru'), incarcare: aw(2, 'încărcare'),
    cenusa: aw(3, 'cenușă'), bine3: aw(3, 'Bineînțeles'), demontat3: aw(3, 'demontat'), curatat3: aw(3, 'curățat'), remontat3: aw(3, 'remontat'),
    in4: aw(4, 'În'), am4: aw(4, 'am'),
    racitor: aw(5, 'răcitor'), blocat: aw(5, 'blocat'), clientul5: aw(5, 'Clientul'), decizia: aw(5, 'decizia'),
    deblocam: aw(6, 'deblocăm'), efectuat6: aw(6, 'efectuat'), supapa: aw(6, 'supapa'), lucreaza: aw(6, 'lucrează'), functionala: aw(6, 'funcțională'),
    totodata: aw(7, 'Totodată'), capsula: aw(7, 'capsula'), sparta: aw(7, 'spartă'),
    testarea: aw(8, 'Testarea'), pistol: aw(8, 'pistol'), bine8: aw(8, 'Bineînțeles'), demontata8: aw(8, 'demontată'), trimisa: aw(8, 'trimisă'), verificari: aw(8, 'verificări'), recond: aw(8, 'recondiționare'),
    garantie: aw(9, 'garanție'), n24: aw(9, '24'), fara: aw(9, 'fără'),
    turbina10: aw(10, 'Turbina'), remontata10: aw(10, 'remontată'), sistemul: aw(10, 'Sistemul'), curatat10: aw(10, 'curățat'),
    urmand: aw(11, 'Urmând'), remontare: aw(11, 'remontare'), adaptarile: aw(11, 'adaptările'), probe: aw(11, 'probe'), gata: aw(11, 'gata'),
  };
  // HOOK: „NU TRAGE?” (impactul mare) + „3 DEFECTE GĂSITE” (al doilea impact), peste prima frază
  const B1 = .18, B2 = 1.0, HB = A.masina0 - .1;
  return {
    hook: { tag: 'ANALIZĂ TEHNICĂ · CAZ #0030', car: 'OPEL ASTRA J · 1.7 DIESEL', carAt: A.motorizare - .02, end: HB },
    hideCap: [[0, HB - .05]],
    stages: [[A.unde - .1, 'SIMPTOME'], [A.in2 - .1, 'DPF'], [A.in4 - .1, 'RĂCITOR'], [A.totodata - .1, 'TURBINĂ'], [A.turbina10 - .1, 'EXTERNARE']],
    tags: {
      1: { nu: 'r', trage: 'r', repornirea: 'r' }, 2: { filtru: 'c', particule: 'c', incarcare: 'r' }, 3: { cenusa: 'r', curatat: 'g', laboratorul: 'g' },
      5: { racitor: 'c', gaze: 'c', blocat: 'r' }, 6: { deblocam: 'g', supapa: 'c', lucreaza: 'g', functionala: 'g' },
      7: { capsula: 'c', vacuumatica: 'c', turbinei: 'c', sparta: 'r' }, 8: { pistol: 'c', vacuum: 'c', reconditionare: 'g' },
      9: { completa: 'g', garantie: 'g' }, 10: { remontata: 'g', curatat: 'g', complet: 'g' }, 11: { gata: 'g', predare: 'g' },
    },
    items: [
      // ---- hook: boom
      { k: 'boom', t: B1, dur: HB - B1, txt: 'NU TRAGE?', y: 920, size: 230, col: '#FF4B4B', from: 3.8, sh: 24, ca: 30, bg: 1, glow: 'rgba(255,75,75,.6)' },
      { k: 'boom', t: B2, dur: HB - B2, txt: '3 DEFECTE GĂSITE', y: 1130, size: 118, col: '#FFD21F', from: 2.6, sh: 14, ca: 18, riser: false, bg: .7 },
      // ---- fișa pacientului: mașina + simptomele
      { k: 'file', t0: HB + .02, t1: A.in2 - .3, no: '0030', ecg: 'crit', rows: [[A.masina0, 'PACIENT', 'OPEL ASTRA J', 'c', 'automobile'], [A.masina0 + .15, 'MOTOR', '1.7 DIESEL', 'y', 'gear'],
        [A.piatra, 'UNITATE', 'PIATRA NEAMȚ', 'y', 'round_pushpin'], [A.nu1, 'SIMPTOME', 'NU TRAGE', 'r', 'warning'], [A.repornirea, '', 'TREBUIE REPORNITĂ', 'r', 'key']] },
      // ---- defectul 1: filtrul de particule încărcat cu cenușă
      { k: 'schem', t0: A.in2 - .05, t1: A.bine3 - .3, top: 268, type: 'dpfFlow', title: 'SCHEMĂ · FILTRUL DE PARTICULE', sub: 'DEFECTUL #1',
        P: { modes: ['flow', 'clog'], labels: { clog: ['ÎNCĂRCARE FOARTE MARE CU CENUȘĂ', '#FF4B4B'] } }, stepNames: ['CONSTATARE', 'DEFECT'],
        steps: [[A.in2 - .05, 'Constatare: filtrul de particule (DPF)', ''], [A.incarcare - .05, 'Încărcare foarte mare cu cenușă', 'r']] },
      { k: 'pipe', t0: A.bine3 - .1, t1: A.in4 - .3, ico: 'test_tube', title: 'DPF · TRATAMENT ÎN LABORATORUL TURBO DOCTOR',
        steps: [[A.demontat3, 'wrench', 'DEMONTAT'], [A.curatat3, 'test_tube', 'CURĂȚAT<br>ÎN LABORATOR'], [A.remontat3, 'hammer_and_wrench', 'REMONTAT<br>PE MAȘINĂ']] },
      // ---- defectul 2: răcitorul de gaze blocat (supapa arătată cu degetul)
      { k: 'chip', t0: A.in4 - .05, t1: A.racitor - .3, y: 330, ph: [[A.in4 - .05, 'magnifying_glass_tilted_left', 'CONSTATARE MAI DETALIATĂ', 'blue'], [A.am4 - .05, 'warning', 'ÎNCĂ O PROBLEMĂ', 'yellow']] },
      { k: 'def', t0: A.racitor - .05, t1: A.clientul5 - .3, term: 'RĂCITORUL DE GAZE (EGR)', text: 'Răcește gazele de evacuare recirculate, înainte să intre înapoi în admisie.' },
      { k: 'stamp', t: A.blocat - .03, t1: A.clientul5 - .25, y: 720, txt: 'BLOCAT', col: 'red', s: .8 },
      { k: 'list', t0: A.clientul5 - .1, t1: A.totodata - .3, ico: 'hammer_and_wrench', title: 'RĂCITORUL DE GAZE · REZOLVARE',
        rows: [[A.decizia, 'CLIENTUL A DECIS: DEBLOCARE'], [A.deblocam, 'DEBLOCAT'], [A.supapa, 'SUPAPA LUCREAZĂ'], [A.functionala, 'FUNCȚIONALĂ PE MAȘINĂ']] },
      { k: 'kin', t: A.deblocam - .02, dur: 1.2, txt: 'DEBLOCAT!', col: '#4ADE80', y: 880, size: 130, rot: -4 },
      { k: 'call', t0: A.supapa - .1, t1: A.totodata - .35, track: 'track_valve', p: [600, 1230], lab: [700, 1050], h: 'SUPAPA', v: 'LUCREAZĂ', col: 'green', cps: 30 },
      // ---- defectul 3: capsula vacuumatică a turbinei, spartă (test cu pistolul de vacuum)
      { k: 'schem', t0: A.totodata - .05, t1: A.bine8 - .3, top: 268, h: 400, type: 'vacuumCapsule', title: 'SCHEMĂ · CAPSULA VACUUMATICĂ', sub: 'DEFECTUL #3',
        stepNames: ['FUNCȚIONARE', 'DEFECT', 'TESTARE'],
        steps: [[A.totodata - .05, 'Capsula comandă turbina cu vacuum', '', 0], [A.sparta - .05, 'Capsula e spartă: nu ține vacuumul', 'r', 1], [A.testarea - .05, 'Testarea: cu pistolul de vacuum', 'y', 2]] },
      { k: 'ring', t0: A.capsula - .05, t1: A.testarea - .3, track: 'track_caps', p: [460, 1160], r: 175, col: '#FF4B4B' },
      { k: 'stamp', t: A.sparta - .03, t1: A.testarea - .25, y: 900, txt: 'SPARTĂ', col: 'red', s: .8 },
      { k: 'pipe', t0: A.bine8 - .1, t1: A.turbina10 - .3, ico: 'test_tube', title: 'TURBINA · TRATAMENT ÎN LABORATOR',
        steps: [[A.demontata8, 'wrench', 'DEMONTATĂ'], [A.trimisa, 'microscope', 'LABORATOR<br>+ VERIFICĂRI'], [A.recond, 'hammer_and_wrench', 'RECONDIȚIONARE<br>COMPLETĂ'], [A.garantie, 'shield', 'GARANȚIE<br>24 LUNI']] },
      { k: 'kin', t: A.n24 - .02, dur: 1.0, txt: '24 LUNI GARANȚIE', col: '#FFD21F', y: 1060, size: 120, rot: -3 },
      { k: 'kin', t: A.fara - .02, dur: 1.3, txt: 'FĂRĂ LIMITĂ DE KM', col: '#4ADE80', y: 1060, size: 110, rot: -3 },
      // ---- externarea
      { k: 'chip', t0: A.turbina10 - .05, t1: A.urmand - .3, y: 330, ph: [[A.turbina10 - .05, 'check_mark_button', 'TURBINA: REMONTATĂ', 'green'], [A.sistemul - .05, 'sparkles', 'ADMISIA: CURĂȚATĂ COMPLET', 'green']] },
      { k: 'list', t0: A.urmand - .1, t1: A.gata - .25, ico: 'test_tube', title: 'ÎNAINTE DE EXTERNARE', rows: [[A.remontare, 'REMONTARE COMPLETĂ'], [A.adaptarile, 'ADAPTĂRI NECESARE'], [A.probe, 'PROBE DE DRUM']] },
      { k: 'stamp', t: A.gata - .05, t1: SEND - .1, y: 520, txt: 'GATA DE PREDARE', col: 'green', s: .85 },
      { k: 'tip', t0: SEND + .1, t1: TEND - .15, top: 520, title: 'REȚETA TURBO DOCTOR', sub: 'SFAT DE INGINER · DIESEL', ico: 'stethoscope',
        rows: [[SEND + .35, 'warning', 'Nu trage și revine după repornire? Fă diagnoza din timp'], [SEND + 1.15, 'magnifying_glass_tilted_left', 'Un simptom poate avea mai multe cauze: verifică tot sistemul'],
          [SEND + 1.95, 'leaf', 'Cenușa nu arde la regenerare: DPF-ul se curăță în laborator']] },
    ],
    fx: [
      { k: 'flash', t: B1 - .11, a: .75 }, { k: 'punch', t: B1, a: .16, sh: 34 }, { k: 'glitch', t: B1, d: .2 }, { k: 'shock', t: B1 + .01, x: 540, y: 920, r: 760, n: 2, col: '#FF4B4B' },
      { k: 'flash', t: B2 - .11, a: .4 }, { k: 'punch', t: B2, a: .08, sh: 16 }, { k: 'shock', t: B2 + .01, x: 540, y: 1130, r: 520, n: 1, col: '#FFD21F' },
      { k: 'glitch', t: HB - .05, d: .14 },
      { k: 'glitch', t: A.in2 - .12, d: .12 }, { k: 'punch', t: A.cenusa, a: .05 }, { k: 'glitch', t: A.in4 - .12, d: .12 }, { k: 'punch', t: A.blocat, a: .05 },
      { k: 'punch', t: A.deblocam, a: .04 }, { k: 'glitch', t: A.totodata - .12, d: .12 }, { k: 'punch', t: A.sparta, a: .07, sh: 10 },
      { k: 'punch', t: A.n24, a: .04 }, { k: 'glitch', t: A.turbina10 - .12, d: .12 },
    ],
    sfx: [[HB - .1, 'whoosh', .6], [A.gata, 'shimmer', .55]],
    bursts: [[B1 + .04, 540, 920, 8, 560, 1.7], [B2 + .04, 540, 1130, 4, 420, 1.2], [A.deblocam + .05, 540, 880, 6, 320, .8], [A.n24 + .1, 540, 1060, 6, 360, .9], [A.gata, 540, 520, 6, 330, .8]],
  };
};
