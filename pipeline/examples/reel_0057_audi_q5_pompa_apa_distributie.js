// v2 – Reel r0057 – „Audi Q5 2.0 diesel: pierde antigel → pompa de apă de pe distribuție” (IMG_0057, un singur clip, fără tăieturi)
// clip: 0–3 vasul de expansiune · 4–30 compartimentul motor (Piatra Neamț) · 30–35 vasul de expansiune (testul de presiune) · 41–51 kitul nou de distribuție în cutie · 52–78 motorul · fără fețe
// Hook: titlu boom pe cuvântul-cheie din prima frază („AI OBSERVAT” + „LIPSĂ” + „LICHID DE RĂCIRE?”), ca la Ford Focus #0046. Fără CTA pe imagine (25.10).
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND }) => {
  const A = {
    lipsa0: aw(0, 'lipsă'), lichid: aw(0, 'lichid'), noi0: aw(0, 'Noi'), constatare0: aw(0, 'constatare'), identificare0: aw(0, 'identificare'), diagnoza0: aw(0, 'diagnoză'), rezolvarea: aw(0, 'rezolvarea'),
    audi: aw(1, 'Audi'), n20: aw(1, '2.0'), piatra: aw(1, 'Piatra'),
    unde2: aw(2, 'unde'), lipsa2: aw(2, 'lipsă'), pierderi: aw(2, 'pierderi'), si2: aw(2, 'și'),
    problema3: aw(3, 'problemă'), distributie3: aw(3, 'distribuție'), bine3: aw(3, 'Bineînțeles'), cu3: aw(3, 'cu'), vasul: aw(3, 'vasul'),
    si4: aw(4, 'și'), pompa4: aw(4, 'pompă'), bine4: aw(4, 'Bineînțeles'), optat: aw(4, 'optat'), completa4: aw(4, 'completă'), curea4: aw(4, 'curea'), pompa4b: aw(4, 'pompă', 1), role: aw(4, 'role'),
    si5: aw(5, 'Și'), cureaua5: aw(5, 'cureaua'), masina5: aw(5, 'Mașina'),
    urmand6: aw(6, 'urmând'), demonta6: aw(6, 'demonta'),
    inlocui7: aw(7, 'înlocui'), nou7: aw(7, 'nou'), constatare7: aw(7, 'constatare'),
    iar8: aw(8, 'Iar'), remontare8: aw(8, 'remontare'), adaptarile8: aw(8, 'adaptările'), probe8: aw(8, 'probe'), gata8: aw(8, 'gata'),
  };
  // HOOK: „AI OBSERVAT” → „LIPSĂ” bubuie pe cuvânt → „LICHID DE RĂCIRE?” pe „lichid”
  const B0 = .28, B1 = A.lipsa0 - .03, B2 = A.lichid - .03, HB = A.noi0 - .1;
  const KIT0 = 41.3;  // apare cutia cu kitul nou de distribuție
  return {
    hook: { tag: 'ANALIZĂ TEHNICĂ · CAZ #0057', end: HB },
    hideCap: [[0, HB - .05]],
    stages: [[A.unde2 - .1, 'SIMPTOME'], [A.si2 - .1, 'INVESTIGAȚIE'], [A.si4 - .1, 'CAUZA'], [A.bine4 - .1, 'SOLUȚIA']],
    tags: {
      0: { lipsa: 'r', lichid: 'c', racire: 'c' }, 2: { lipsa: 'r', antigel: 'c', pierderi: 'r' }, 3: { distributie: 'c', presiune: 'y', vasul: 'c', expansiune: 'c' },
      4: { pompa: 'c', apa: 'c', completa: 'g', kitului: 'g', curea: 'g', role: 'g' }, 5: { cureaua: 'c', pompa: 'c', ulei: 'c', demontare: 'y' },
      6: { distributie: 'c' }, 7: { nou: 'g', kitul: 'g', admisie: 'c' }, 8: { gata: 'g', predare: 'g' },
    },
    items: [
      // ---- hook: boom
      { k: 'boom', t: B0, dur: HB - B0, txt: 'AI OBSERVAT', y: 590, size: 104, col: '#FFFFFF', from: 2.2, sh: 10, ca: 12, riser: false, bg: .45, glow: 'rgba(98,216,255,.5)' },
      { k: 'boom', t: B1, dur: HB - B1, txt: 'LIPSĂ', y: 875, size: 300, col: '#FF4B4B', from: 3.8, sh: 24, ca: 30, bg: 1, glow: 'rgba(255,75,75,.6)' },
      { k: 'boom', t: B2, dur: HB - B2, txt: 'LICHID DE RĂCIRE?', y: 1115, size: 116, col: '#62D8FF', from: 2.6, sh: 14, ca: 18, riser: false, bg: .7, glow: 'rgba(98,216,255,.6)' },
      // ---- ce face Turbo Doctor
      { k: 'list', t0: A.noi0 - .05, t1: A.audi - .3, ico: 'stethoscope', title: 'TURBO DOCTOR TE POATE AJUTA',
        rows: [[A.constatare0, 'CONSTATARE'], [A.identificare0, 'IDENTIFICARE'], [A.diagnoza0, 'DIAGNOZĂ'], [A.rezolvarea, 'REZOLVAREA PROBLEMEI']] },
      // ---- fișa pacientului
      { k: 'file', t0: A.audi - .1, t1: A.si2 - .3, no: '0057', ecg: 'crit', rows: [[A.audi, 'PACIENT', 'AUDI Q5', 'c', 'automobile'], [A.n20, 'MOTOR', '2.0 DIESEL', 'y', 'gear'],
        [A.piatra, 'UNITATE', 'PIATRA NEAMȚ', 'y', 'round_pushpin'], [A.lipsa2, 'SIMPTOME', 'LIPSĂ DE ANTIGEL', 'r', 'droplet'], [A.pierderi, '', 'PIERDERI', 'r', 'warning']] },
      // ---- investigația: problemă pe distribuție, test de presiune pe vasul de expansiune
      { k: 'chip', t0: A.si2 - .05, t1: A.bine3 - .3, y: 330, ph: [[A.si2 - .05, 'magnifying_glass_tilted_left', 'CONSTATARE', 'blue'], [A.problema3 - .05, 'gear', 'PROBLEMĂ PE PARTEA DE DISTRIBUȚIE', 'yellow']] },
      { k: 'def', t0: A.bine3 - .05, t1: A.cu3 - .15, term: 'TESTUL DE PRESIUNE', text: 'Circuitul de răcire e pus sub presiune prin vasul de expansiune. Dacă presiunea scade, există o pierdere.' },
      { k: 'ring', t0: A.cu3 - .05, t1: 35.85, track: 'track_tank', p: [625, 520], r: 150, col: '#62D8FF' },
      // ---- cauza: pompa de apă (antrenată de cureaua de distribuție) → soluția: kit complet
      { k: 'schem', t0: A.si4 - .05, t1: KIT0 - .2, top: 268, h: 410, type: 'timingKit', title: 'SCHEMĂ · DISTRIBUȚIA', sub: 'POMPA DE APĂ',
        stepNames: ['CUM FUNCȚIONEAZĂ', 'CAUZA', 'SOLUȚIA'],
        steps: [[A.si4 - .05, 'Pompa de apă e antrenată de cureaua de distribuție', '', 0], [A.pompa4 - .05, 'Problema: pompa de apă pierde antigel', 'r', 1],
          [A.bine4 - .05, 'Soluția: kit complet de distribuție', 'g', 2]] },
      { k: 'chip', t0: KIT0, t1: A.si5 - .3, y: 330, ph: [[KIT0, 'package', 'KIT COMPLET DE DISTRIBUȚIE', 'green'], [A.curea4 - .05, 'check_mark_button', 'CUREA', 'green'],
        [A.pompa4b - .05, 'check_mark_button', 'CUREA · POMPĂ DE APĂ', 'green'], [A.role - .05, 'check_mark_button', 'CUREA · POMPĂ DE APĂ · ROLE', 'green']] },
      { k: 'chip', t0: A.si5 - .05, t1: A.masina5 - .3, y: 330, ph: [[A.si5 - .05, 'wrench', 'ȘI TOTODATĂ...', 'blue'], [A.cureaua5 - .05, 'oil_drum', 'ȘI CUREAUA DE LA POMPA DE ULEI', 'yellow']] },
      { k: 'chip', t0: A.masina5 - .05, t1: A.urmand6 - .3, y: 330, ph: [[A.masina5 - .05, 'wrench', 'MAȘINA: ÎN DEMONTARE', 'yellow']] },
      { k: 'pipe', t0: A.urmand6 - .1, t1: A.iar8 - .3, ico: 'hammer_and_wrench', title: 'PLANUL DE LUCRU · TURBO DOCTOR',
        steps: [[A.demonta6, 'wrench', 'DEMONTARE<br>KIT VECHI'], [A.inlocui7, 'package', 'KIT NOU<br>DE DISTRIBUȚIE'], [A.constatare7, 'magnifying_glass_tilted_left', 'CONSTATARE<br>ADMISIE']] },
      // ---- externarea
      { k: 'list', t0: A.iar8 - .1, t1: A.gata8 - .25, ico: 'test_tube', title: 'ÎNAINTE DE EXTERNARE', rows: [[A.remontare8, 'REMONTARE COMPLETĂ'], [A.adaptarile8, 'ADAPTĂRI NECESARE'], [A.probe8, 'PROBE DE DRUM']] },
      { k: 'stamp', t: A.gata8 - .05, t1: SEND - .1, y: 520, txt: 'GATA DE PREDARE', col: 'green', s: .85 },
      { k: 'tip', t0: SEND + .1, t1: TEND - .15, top: 520, title: 'REȚETA TURBO DOCTOR', sub: 'SFAT DE INGINER · RĂCIRE', ico: 'stethoscope',
        rows: [[SEND + .35, 'droplet', 'Pierzi antigel? Cere un test de presiune pe circuit'], [SEND + 1.15, 'gear', 'Pompa de apă e pe distribuție: se schimbă împreună cu kitul'],
          [SEND + 1.95, 'warning', 'Nivelul de antigel scade? Nu amâna diagnoza']] },
    ],
    fx: [
      { k: 'punch', t: B0, a: .05, sh: 10 },
      { k: 'flash', t: B1 - .11, a: .75 }, { k: 'punch', t: B1, a: .16, sh: 34 }, { k: 'glitch', t: B1, d: .2 }, { k: 'shock', t: B1 + .01, x: 540, y: 875, r: 760, n: 2, col: '#FF4B4B' },
      { k: 'flash', t: B2 - .11, a: .45 }, { k: 'punch', t: B2, a: .08, sh: 16 }, { k: 'shock', t: B2 + .01, x: 540, y: 1115, r: 520, n: 1 },
      { k: 'glitch', t: HB - .05, d: .14 },
      { k: 'glitch', t: A.si2 - .12, d: .12 }, { k: 'punch', t: A.distributie3, a: .05 }, { k: 'glitch', t: A.si4 - .12, d: .12 }, { k: 'punch', t: A.pompa4, a: .06, sh: 10 },
      { k: 'punch', t: A.completa4, a: .04 }, { k: 'glitch', t: A.urmand6 - .12, d: .12 }, { k: 'glitch', t: A.iar8 - .12, d: .12 },
    ],
    sfx: [[HB - .1, 'whoosh', .6], [A.gata8, 'shimmer', .55]],
    bursts: [[B1 + .04, 540, 875, 8, 560, 1.7], [B2 + .04, 540, 1115, 4, 420, 1.2], [A.gata8, 540, 520, 6, 330, .8]],
  };
};
