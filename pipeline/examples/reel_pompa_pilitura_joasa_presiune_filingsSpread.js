// v2 – Reel din vlogul „Pompa de înaltă a făcut pilitură” (08.11.2026) – #3 Pilitura ajunge și în joasa presiune: rezervor, pompe, conducte
// cold open din clip (fraza lui cea mai puternică) + titluri boom pe cuvinte, ca la Euro 7; cardul de final cu sloganul cerut de Sabin
// Seria de 9 reel-uri din vlogul „Pompa de înaltă a făcut pilitură” a fost aprobată de Sabin și programată pe 09.11.2026 (22–30.11). Schema `filingsSpread` și `endSub` (sloganul de pe cardul de final, fără telefon) sunt în pipeline din 09.11.2026.
window.REEL_CFG = ({ aw, ew, cw, cwe, S0, SEND, TEND }) => {
  const BOOMS = (B) => { const items = [], fx = [], bursts = [];
    B.forEach((b, i) => { const big = !!b.big;
      items.push({ k: 'boom', t: b.t, dur: b.end - b.t, txt: b.txt, y: b.y, size: b.size, col: b.col || '#FFFFFF', from: big ? 3.8 : 2.6, sh: big ? 24 : 14, ca: big ? 30 : 18, riser: i === 0, bg: big ? 1 : .7, glow: b.glow || (big ? undefined : 'rgba(98,216,255,.55)') });
      fx.push({ k: 'flash', t: b.t - .11, a: big ? .75 : .45 }, { k: 'punch', t: b.t, a: big ? .16 : .08, sh: big ? 34 : 16 }, { k: 'shock', t: b.t + .01, x: 540, y: b.y, r: big ? 720 : 500, n: big ? 2 : 1, col: b.col === '#FFD21F' ? '#FFD21F' : '#FFFFFF' });
      if (big) fx.push({ k: 'glitch', t: b.t, d: .2 });
      bursts.push([b.t + .04, 540, b.y, big ? 8 : 4, big ? 540 : 400, big ? 1.6 : 1.1]); });
    return { items, fx, bursts }; };
  const END_SUB = ['EXPERȚI ÎN DIAGNOSTICAREA', 'SISTEMELOR DE INJECȚIE'];
  const A = { ci0: aw(0, 'ci'), joasa: aw(0, 'joasă'), adica: aw(0, 'adică'), rezervor0: aw(0, 'rezervor'), rezervor0E: ew(0, 'rezervor'), pompele: aw(0, 'pompele'), inalta0: aw(0, 'înaltă', 1),
    conductele: aw(0, 'conductele'), comunicarea: aw(0, 'comunicarea'), rezervorEnd: ew(0, 'rezervor', 2),
    toate1: aw(1, 'Toate'), pilitura1: aw(1, 'pilitură'), da1: aw(1, 'da'), curata: aw(1, 'curăța'), curataE: ew(1, 'curăța'), punem: aw(1, 'punem'), pericol: aw(1, 'pericol'), reparatia: aw(1, 'reparația') };
  const HE = S0 - .05;
  const HB = BOOMS([
    { t: cw('pericol') - .03, end: HE, txt: 'ÎN PERICOL!', y: 700, size: 200, col: '#FF4B4B', big: true, glow: 'rgba(255,75,75,.6)' },
    { t: cw('reparația') - .03, end: HE, txt: 'TOATĂ REPARAȚIA', y: 480, size: 128, col: '#FFFFFF' },
  ]);
  return {
    hideCap: [[0, HE]],
    endSub: END_SUB,
    hook: { tag: 'ANALIZĂ TEHNICĂ · POMPĂ CU PILITURĂ', end: HE },
    stages: [[S0, 'ÎNALTĂ PRESIUNE'], [A.ci0 - .1, 'JOASĂ PRESIUNE'], [A.toate1 - .1, 'CURĂȚAREA'], [A.punem - .1, 'RISCUL']],
    items: [
      ...HB.items,
      { k: 'schem', t0: S0 + .05, t1: A.toate1 - .3, type: 'filingsSpread', title: 'SCHEMĂ · CIRCUITUL DE MOTORINĂ', sub: 'ÎNALTĂ + JOASĂ PRESIUNE', stepNames: ['ÎNALTĂ', 'JOASĂ', 'REZERVOR', 'POMPE', 'CONDUCTE'],
        P: { hpTxt: 'ÎNALTĂ PRESIUNE · PILITURĂ', lpTxt: 'JOASĂ PRESIUNE · PILITURĂ', heads: { hp: ['PILITURĂ ÎN ÎNALTĂ PRESIUNE', '#FF4B4B'], lp: ['PILITURĂ ȘI ÎN JOASĂ PRESIUNE', '#FF4B4B'] } },
        steps: [[S0 + .05, 'Pilitura nu a ajuns doar în sistemul de înaltă presiune...', 'r', 'hp'], [A.ci0 - .05, '...ci și în sistemul de joasă presiune', 'r', 'lp'],
          [A.rezervor0 - .05, 'Rezervorul', 'r', 'lp'], [A.pompele - .05, 'Pompele care ridică presiunea din rezervor spre pompa de înaltă', 'r', 'lp'], [A.conductele - .05, 'Conductele dintre rezervor și sistemul de înaltă presiune', 'r', 'lp']] },
      { k: 'list', t0: A.toate1 - .1, t1: A.punem - .3, ico: 'warning', title: 'TOATE AU PILITURĂ ÎN ELE', rows: [[A.toate1 + .1, 'REZERVOR · POMPE · CONDUCTE', 'bad'], [A.da1 - .05, 'DE DAT JOS'], [A.curata - .05, 'DE CURĂȚAT']] },
      { k: 'schem', t0: A.punem - .1, t1: SEND - .1, type: 'filingsSpread', title: 'SCHEMĂ · DACĂ NU SE CURĂȚĂ', sub: 'ÎNALTĂ PRESIUNE REPARATĂ', stepNames: ['RISCUL'],
        steps: [[A.punem - .1, 'Pilitura rămasă pune în pericol toată reparația', 'r', 'again']] },
      { k: 'kin', t: A.rezervor0 - .02, dur: Math.min(A.rezervor0E + .4, A.pompele - .1) - A.rezervor0, txt: 'REZERVORUL', col: '#FF4B4B', y: 1650, size: 120, rot: -3 },
      { k: 'kin', t: A.pompele - .02, dur: 1.6, txt: 'POMPELE DE JOASĂ', col: '#FF8A3D', y: 1650, size: 100, rot: -3 },
      { k: 'kin', t: A.conductele - .02, dur: 1.5, txt: 'CONDUCTELE', col: '#FF8A3D', y: 1650, size: 120, rot: -3 },
      { k: 'kin', t: A.curata - .02, dur: A.curataE + .5 - A.curata, txt: 'DE CURĂȚAT!', col: '#4ADE80', y: 1650, size: 120, rot: -3 },
      { k: 'kin', t: A.pericol - .02, dur: Math.max(.8, SEND - .05 - A.pericol), txt: 'REPARAȚIA, ÎN PERICOL!', col: '#FF4B4B', y: 1650, size: 80, rot: -4 },
    ],
    fx: [...HB.fx, { k: 'punch', t: A.joasa, a: .05 }, { k: 'glitch', t: A.ci0 - .05, d: .12 }, { k: 'punch', t: A.curata, a: .04 }, { k: 'punch', t: A.pericol, a: .07, sh: 9 }, { k: 'glitch', t: A.pericol - .03, d: .14 }],
    bursts: HB.bursts,
  };
};
