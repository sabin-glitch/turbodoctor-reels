// v2 – Reel din vlogul „Pompa de înaltă a făcut pilitură” (08.11.2026) – #1 De ce face pompa pilitură: lipsa de lubrifiere și amorsarea
// cold open din clip (fraza lui cea mai puternică) + titluri boom pe cuvinte, ca la Euro 7; cardul de final cu sloganul cerut de Sabin
// Seria de 9 reel-uri din vlogul „Pompa de înaltă a făcut pilitură” a fost aprobată de Sabin și programată pe 09.11.2026 (22–30.11). Schema `pumpLube` și `endSub` (sloganul de pe cardul de final, fără telefon) sunt în pipeline din 09.11.2026.
window.REEL_CFG = ({ aw, ew, cw, cwe, S0, SEND, TEND }) => {
  const BOOMS = (B) => { const items = [], fx = [], bursts = [];
    B.forEach((b, i) => { const big = !!b.big;
      items.push({ k: 'boom', t: b.t, dur: b.end - b.t, txt: b.txt, y: b.y, size: b.size, col: b.col || '#FFFFFF', from: big ? 3.8 : 2.6, sh: big ? 24 : 14, ca: big ? 30 : 18, riser: i === 0, bg: big ? 1 : .7, glow: b.glow || (big ? undefined : 'rgba(98,216,255,.55)') });
      fx.push({ k: 'flash', t: b.t - .11, a: big ? .75 : .45 }, { k: 'punch', t: b.t, a: big ? .16 : .08, sh: big ? 34 : 16 }, { k: 'shock', t: b.t + .01, x: 540, y: b.y, r: big ? 720 : 500, n: big ? 2 : 1, col: b.col === '#FFD21F' ? '#FFD21F' : '#FFFFFF' });
      if (big) fx.push({ k: 'glitch', t: b.t, d: .2 });
      bursts.push([b.t + .04, 540, b.y, big ? 8 : 4, big ? 540 : 400, big ? 1.6 : 1.1]); });
    return { items, fx, bursts }; };
  const END_SUB = ['EXPERȚI ÎN DIAGNOSTICAREA', 'SISTEMELOR DE INJECȚIE'];
  const A = { motiv0: aw(0, 'motiv'), de1: aw(1, 'De'), lipsa: aw(1, 'lipsa'), insuf1E: ew(1, 'insuficientă'),
    acest2: aw(2, 'Acest'), combustibil: aw(2, 'combustibilului'), rezervorE: ew(2, 'rezervor'),
    fie3: aw(3, 'fie'), schimbarea: aw(3, 'schimbarea'), motorinaE: ew(3, 'motorină'),
    amorsarea: aw(4, 'amorsarea'), amorsareaE: ew(4, 'sistemului'), daca4: aw(4, 'Dacă'),
    insuf5: aw(5, 'insuficient'), secunde: aw(5, 'câteva'), secundeE: ew(5, 'secunde'), aparitia: aw(5, 'apariția'), pilit5: aw(5, 'piliturii') };
  const HE = S0 - .05;
  const HB = BOOMS([
    { t: cw('amorsăm') - .03, end: HE, txt: 'FĂRĂ AMORSARE?', y: 400, size: 128, col: '#FFFFFF' },
    { t: cw('lubrifiată') - .03, end: HE, txt: 'LUBRIFIATĂ', y: 588, size: 190, col: '#FFD21F', big: true },
    { t: cw('insuficient') - .03, end: HE, txt: 'INSUFICIENT!', y: 776, size: 138, col: '#FF4B4B', glow: 'rgba(255,75,75,.6)' },
  ]);
  return {
    hideCap: [[0, HE]],
    endSub: END_SUB,
    hook: { tag: 'ANALIZĂ TEHNICĂ · POMPA DE ÎNALTĂ PRESIUNE', end: HE },
    stages: [[S0, 'CAUZA'], [A.acest2 - .1, 'COMBUSTIBIL'], [A.fie3 - .1, 'ÎNTREȚINERE'], [A.daca4 - .1, 'AMORSAREA']],
    items: [
      ...HB.items,
      { k: 'chip', t0: S0 + .05, t1: A.de1 - .3, y: 330, ph: [[S0 + .05, 'thinking_face', 'DE CE FACE POMPA PILITURĂ?', 'blue']] },
      { k: 'schem', t0: A.de1 - .1, t1: A.schimbarea - .3, type: 'pumpLube', title: 'SCHEMĂ · ELEMENTUL DE POMPARE', sub: 'POMPA DE ÎNALTĂ PRESIUNE', stepNames: ['UNGEREA', 'CAUZA', 'COMBUSTIBIL'],
        P: { heads: { water: ['PROBLEMĂ LA COMBUSTIBIL', '#FF8A3D'] } },
        steps: [[A.de1 - .1, 'Pistonul pompei lucrează într-un film de motorină', 'g', 'ok'], [A.lipsa - .05, 'Cauza: lipsa de lubrifiere sau lubrifiere insuficientă', 'r', 'dry'],
          [A.combustibil - .05, 'Fie o problemă la combustibilul din rezervor...', 'y', 'water']] },
      { k: 'def', t0: A.schimbarea - .1, t1: A.daca4 - .25, term: 'AMORSAREA SISTEMULUI', text: 'Umplerea circuitului cu motorină și scoaterea aerului, înainte de pornire. Necesară după schimbarea filtrului.' },
      { k: 'schem', t0: A.daca4 - .1, t1: SEND - .1, type: 'pumpLube', title: 'SCHEMĂ · ELEMENTUL DE POMPARE', sub: 'PORNIRE FĂRĂ AMORSARE', stepNames: ['FĂRĂ AMORSARE', 'SECUNDE CRITICE', 'PILITURA'],
        steps: [[A.daca4 - .1, 'Mașina pornită fără amorsarea sistemului', 'y', 'air'], [A.insuf5 - .05, 'Câteva secunde, pompa e lubrifiată insuficient', 'r', 'metal'], [A.aparitia - .05, 'Așa apare pilitura', 'r', 'flakes']] },
      { k: 'kin', t: A.lipsa - .02, dur: A.insuf1E + .5 - A.lipsa, txt: 'LIPSA DE LUBRIFIERE', col: '#FF4B4B', y: 1650, size: 88, rot: -3 },
      { k: 'kin', t: A.combustibil - .02, dur: A.rezervorE + .3 - A.combustibil, txt: 'COMBUSTIBILUL', col: '#FFD21F', y: 1650, size: 110, rot: -3 },
      { k: 'kin', t: A.schimbarea - .02, dur: A.motorinaE + .4 - A.schimbarea, txt: 'SCHIMBAREA FILTRULUI', col: '#62D8FF', y: 1650, size: 86, rot: -3 },
      { k: 'kin', t: A.amorsarea - .02, dur: A.amorsareaE + .5 - A.amorsarea, txt: 'AMORSAREA!', col: '#FFD21F', y: 1650, size: 120, rot: -4 },
      { k: 'kin', t: A.secunde - .02, dur: A.secundeE + .4 - A.secunde, txt: 'CÂTEVA SECUNDE...', col: '#FF8A3D', y: 1650, size: 100, rot: -3 },
      { k: 'kin', t: A.pilit5 - .02, dur: Math.max(.6, SEND - .05 - A.pilit5), txt: 'PILITURĂ!', col: '#FF4B4B', y: 1650, size: 140, rot: -4 },
    ],
    fx: [...HB.fx, { k: 'punch', t: A.lipsa, a: .05 }, { k: 'punch', t: A.amorsarea, a: .05 }, { k: 'glitch', t: A.insuf5 - .05, d: .12 }, { k: 'punch', t: A.pilit5, a: .07, sh: 9 }, { k: 'glitch', t: A.pilit5 - .03, d: .14 }],
    bursts: HB.bursts,
  };
};
