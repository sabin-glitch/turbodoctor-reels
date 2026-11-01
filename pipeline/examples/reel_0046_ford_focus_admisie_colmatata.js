// v2 – Reel r0046 – „Ford Focus 2.0 diesel: lipsă de putere → admisia colmatată complet” (IMG_0046, un singur clip, fără tăieturi)
// clip: 0–23 motorul fără galeria de admisie (Piatra Neamț) · 24–38 galeria de admisie demontată, cu depuneri masive · 39–51 motorul · fără fețe
// Hook: titlu boom pe cuvântul-cheie din prima frază („LIPSĂ” + „DE PUTERE?”), apoi ce face Turbo Doctor. Fără CTA pe imagine (25.10).
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND }) => {
  const A = {
    lipsa0: aw(0, 'lipsă'), putere0: aw(0, 'putere'), noi0: aw(0, 'Noi'), constatare: aw(0, 'constatare'),
    diagnoza1: aw(1, 'diagnoză'), rezolvarea: aw(1, 'rezolvarea'), ford: aw(1, 'Ford'), n2: aw(1, '2'), piatra: aw(1, 'Piatra'),
    unde2: aw(2, 'unde'), lipsa2: aw(2, 'lipsă'), bine2: aw(2, 'Bineînțeles'), diagnozei: aw(2, 'diagnozei'), probelor: aw(2, 'probelor'),
    am3: aw(3, 'am'), flow: aw(3, 'flow'), insuficient: aw(3, 'insuficient'), admisie3: aw(3, 'admisie'), acesta3: aw(3, 'acesta'),
    colmatat: aw(3, 'colmatat'), complet3: aw(3, 'complet'), depuneri: aw(3, 'depuneri'), masive: aw(3, 'masive'),
    bine4: aw(4, 'Bineînțeles'), sistemul4: aw(4, 'sistemul'), curatat4: aw(4, 'curățat'), laboratorul4: aw(4, 'laboratorul'), se4: aw(4, 'Se'), garniturile: aw(4, 'garniturile'),
    iar5: aw(5, 'Iar'), probe5: aw(5, 'probe'), adaptarile5: aw(5, 'adaptările'), beneficia: aw(5, 'beneficia'), refresh: aw(5, 'refresh'),
  };
  // HOOK: „LIPSĂ” bubuie pe cuvânt, „DE PUTERE?” vine pe „putere”
  const B0 = .25, B1 = A.lipsa0 - .03, B2 = A.putere0 - .03, HB = A.noi0 - .1;
  return {
    hook: { tag: 'ANALIZĂ TEHNICĂ · CAZ #0046', end: HB },
    hideCap: [[0, HB - .05]],
    stages: [[A.unde2 - .1, 'SIMPTOME'], [A.bine2 - .1, 'INVESTIGAȚIE'], [A.am3 - .1, 'CAUZA'], [A.bine4 - .1, 'SOLUȚIA']],
    tags: {
      0: { lipsa: 'r', putere: 'r' }, 2: { lipsa: 'r', putere: 'r', diagnozei: 'c', probelor: 'c', drum: 'c' },
      3: { flow: 'r', insuficient: 'r', admisie: 'c', colmatat: 'r', complet: 'r', depuneri: 'r', masive: 'r' },
      4: { admisie: 'c', curatat: 'g', laboratorul: 'g', garniturile: 'g' }, 5: { refresh: 'g' },
    },
    items: [
      // ---- hook: boom
      { k: 'boom', t: B0, dur: HB - B0, txt: 'AI IDENTIFICAT O', y: 590, size: 96, col: '#FFFFFF', from: 2.2, sh: 10, ca: 12, riser: false, bg: .45, glow: 'rgba(98,216,255,.5)' },
      { k: 'boom', t: B1, dur: HB - B1, txt: 'LIPSĂ', y: 875, size: 300, col: '#FF4B4B', from: 3.8, sh: 24, ca: 30, bg: 1, glow: 'rgba(255,75,75,.6)' },
      { k: 'boom', t: B2, dur: HB - B2, txt: 'DE PUTERE?', y: 1115, size: 175, col: '#FFFFFF', from: 2.6, sh: 14, ca: 18, riser: false, bg: .7, glow: 'rgba(98,216,255,.55)' },
      // ---- ce face Turbo Doctor
      { k: 'list', t0: A.noi0 - .05, t1: A.ford - .3, ico: 'stethoscope', title: 'TURBO DOCTOR TE POATE AJUTA',
        rows: [[A.constatare, 'CONSTATARE'], [A.diagnoza1, 'DIAGNOZĂ'], [A.rezolvarea, 'REZOLVAREA PROBLEMEI']] },
      // ---- fișa pacientului
      { k: 'file', t0: A.ford - .1, t1: A.bine2 - .3, no: '0046', ecg: 'crit', rows: [[A.ford, 'PACIENT', 'FORD FOCUS', 'c', 'automobile'], [A.n2, 'MOTOR', '2.0 DIESEL', 'y', 'gear'],
        [A.piatra, 'UNITATE', 'PIATRA NEAMȚ', 'y', 'round_pushpin'], [A.lipsa2, 'SIMPTOME', 'LIPSĂ DE PUTERE', 'r', 'warning']] },
      // ---- investigația
      { k: 'chip', t0: A.bine2 - .05, t1: A.am3 - .3, y: 330, ph: [[A.bine2 - .05, 'stethoscope', 'DIAGNOZĂ', 'blue'], [A.probelor - .05, 'racing_car', 'DIAGNOZĂ + PROBE DE DRUM', 'blue']] },
      // ---- cauza: flow insuficient pe admisie (schemă), apoi depunerile reale
      { k: 'schem', t0: A.am3 - .05, t1: A.acesta3 - .25, top: 268, type: 'intakeFlow', title: 'SCHEMĂ · SISTEMUL DE ADMISIE', sub: 'CAUZA',
        stepNames: ['NORMAL', 'DEFECT'], steps: [[A.am3 - .05, 'Aerul trebuie să intre liber spre cilindri', '', 0], [A.flow - .05, 'Flow insuficient pe sistemul de admisie', 'r', 1]] },
      { k: 'scan', t0: A.colmatat - .1, t1: 31.0, box: [0, 0, 330, 330], track: 'track_dep', lab: 'SCANARE GALERIE ADMISIE...', lab2: 'COLMATAT COMPLET', at2: A.complet3 - .04, labBelow: true },
      { k: 'kin', t: A.masive - .02, dur: 1.3, txt: 'DEPUNERI MASIVE!', col: '#FF3B30', y: 420, size: 112, rot: -4 },
      // ---- soluția
      { k: 'pipe', t0: A.bine4 - .1, t1: A.iar5 - .3, ico: 'test_tube', title: 'TRATAMENT ÎN LABORATORUL TURBO DOCTOR',
        steps: [[A.sistemul4, 'dashing_away', 'SISTEMUL<br>DE ADMISIE'], [A.curatat4, 'broom', 'CURĂȚAT<br>ÎN LABORATOR'], [A.garniturile, 'nutbolt', 'GARNITURI<br>NOI']] },
      { k: 'list', t0: A.iar5 - .1, t1: SEND - .2, ico: 'test_tube', title: 'ÎNAINTE DE EXTERNARE',
        rows: [[A.probe5, 'PROBE DE DRUM'], [A.adaptarile5, 'ADAPTĂRI NECESARE'], [A.refresh, 'REFRESH NOU']] },
      { k: 'tip', t0: SEND + .1, t1: TEND - .15, top: 520, title: 'REȚETA TURBO DOCTOR', sub: 'SFAT DE INGINER · ADMISIE', ico: 'stethoscope',
        rows: [[SEND + .35, 'warning', 'Lipsă de putere? Verifică și sistemul de admisie'], [SEND + 1.15, 'racing_car', 'Diagnoză + probe de drum înainte de orice piesă'],
          [SEND + 1.95, 'broom', 'Depunerile se curăță în laborator, cu garnituri noi']] },
    ],
    fx: [
      { k: 'punch', t: B0, a: .05, sh: 10 },
      { k: 'flash', t: B1 - .11, a: .75 }, { k: 'punch', t: B1, a: .16, sh: 34 }, { k: 'glitch', t: B1, d: .2 }, { k: 'shock', t: B1 + .01, x: 540, y: 875, r: 760, n: 2, col: '#FF4B4B' },
      { k: 'flash', t: B2 - .11, a: .45 }, { k: 'punch', t: B2, a: .08, sh: 16 }, { k: 'shock', t: B2 + .01, x: 540, y: 1115, r: 520, n: 1 },
      { k: 'glitch', t: HB - .05, d: .14 },
      { k: 'glitch', t: A.am3 - .12, d: .12 }, { k: 'punch', t: A.insuficient, a: .05 }, { k: 'punch', t: A.colmatat, a: .06, sh: 10 }, { k: 'punch', t: A.masive, a: .05 },
      { k: 'glitch', t: A.bine4 - .12, d: .12 }, { k: 'punch', t: A.curatat4, a: .04 }, { k: 'glitch', t: A.iar5 - .12, d: .12 },
    ],
    sfx: [[HB - .1, 'whoosh', .6], [A.refresh, 'shimmer', .5]],
    bursts: [[B1 + .04, 540, 875, 8, 560, 1.7], [B2 + .04, 540, 1115, 4, 420, 1.2], [A.curatat4 + .05, 540, 400, 6, 320, .8]],
  };
};
