// v2 – Reel din vlogul „Pompa de înaltă a făcut pilitură” (08.11.2026) – #9 Am filtru cu decantare, deci sunt protejat? Logica e bună, dar în practică...
// cold open din clip (fraza lui cea mai puternică) + titluri boom pe cuvinte, ca la Euro 7; cardul de final cu sloganul cerut de Sabin
// Seria de 9 reel-uri din vlogul „Pompa de înaltă a făcut pilitură” a fost aprobată de Sabin și programată pe 09.11.2026 (22–30.11). Schema `decanterFilter` și `endSub` (sloganul de pe cardul de final, fără telefon) sunt în pipeline din 09.11.2026.
window.REEL_CFG = ({ aw, ew, cw, cwe, S0, SEND, TEND }) => {
  const BOOMS = (B) => { const items = [], fx = [], bursts = [];
    B.forEach((b, i) => { const big = !!b.big;
      items.push({ k: 'boom', t: b.t, dur: b.end - b.t, txt: b.txt, y: b.y, size: b.size, col: b.col || '#FFFFFF', from: big ? 3.8 : 2.6, sh: big ? 24 : 14, ca: big ? 30 : 18, riser: i === 0, bg: big ? 1 : .7, glow: b.glow || (big ? undefined : 'rgba(98,216,255,.55)') });
      fx.push({ k: 'flash', t: b.t - .11, a: big ? .75 : .45 }, { k: 'punch', t: b.t, a: big ? .16 : .08, sh: big ? 34 : 16 }, { k: 'shock', t: b.t + .01, x: 540, y: b.y, r: big ? 720 : 500, n: big ? 2 : 1, col: b.col === '#FFD21F' ? '#FFD21F' : '#FFFFFF' });
      if (big) fx.push({ k: 'glitch', t: b.t, d: .2 });
      bursts.push([b.t + .04, 540, b.y, big ? 8 : 4, big ? 540 : 400, big ? 1.6 : 1.1]); });
    return { items, fx, bursts }; };
  const END_SUB = ['EXPERȚI ÎN DIAGNOSTICAREA', 'SISTEMELOR DE INJECȚIE'];
  const A = { bun0: aw(0, 'Bun'), decantare0: aw(0, 'decantare'), decantare0E: ew(0, 'decantare'), apa0: aw(0, 'apa'),
    logica1: aw(1, 'Logica'), logica1E: ew(1, 'bună'), schimba1: aw(1, 'schimbă'), practica1: aw(1, 'practică'), practica1E: ew(1, 'practică'), exploatata1: aw(1, 'exploatată'), cand1: aw(1, 'când'), joasa1: aw(1, 'joasă'), presiune1E: ew(1, 'presiune'),
    anumite2: aw(2, 'Anumite'), pompa2: aw(2, 'pompă'), mizeria2: aw(2, 'mizeria'), mizeria2E: ew(2, 'mizeria'),
    trece3: aw(3, 'trece'), filtrare3E: ew(3, 'filtrare'), sunt3: aw(3, 'Sunt'), spete3: aw(3, 'spețe'),
    dar4: aw(4, 'Dar'), impuritati4: aw(4, 'impurități'), apa4b: aw(4, 'apă', 1), apare5: aw(5, 'apare'), rezervor5: aw(5, 'rezervor') };
  const HE = S0 - .05;
  const HB = BOOMS([
    { t: cw('trece') - .03, end: HE, txt: 'POT TRECE', y: 405, size: 170, col: '#FFFFFF', big: true },
    { t: cw('toate') - .03, end: HE, txt: 'DE TOATE SISTEMELE', y: 575, size: 100, col: '#FFFFFF' },
    { t: cw('filtrare') - .03, end: HE, txt: 'DE FILTRARE!', y: 745, size: 158, col: '#FF4B4B', big: true, glow: 'rgba(255,75,75,.6)' },
  ]);
  return {
    hideCap: [[0, HE]],
    endSub: END_SUB,
    hook: { tag: 'ANALIZĂ TEHNICĂ · FILTRUL CU DECANTARE', end: HE },
    stages: [[S0, 'ÎNTREBAREA'], [A.logica1 - .1, 'TEORIE VS PRACTICĂ'], [A.anumite2 - .1, 'CE TRECE'], [A.dar4 - .1, 'LA POMPĂ']],
    items: [
      ...HB.items,
      { k: 'chip', t0: S0 + .05, t1: A.bun0 - .25, y: 330, ph: [[S0 + .05, 'thinking_face', 'O SĂ VINĂ ÎNTREBAREA...', 'blue']] },
      { k: 'schem', t0: A.bun0 - .1, t1: A.sunt3 - .3, type: 'decanterFilter', title: 'SCHEMĂ · FILTRUL CU DECANTARE', sub: 'TEORIE VS PRACTICĂ', stepNames: ['FILTRUL', 'TEORIA', 'PRACTICA', 'LA POMPĂ'],
        steps: [[A.bun0, 'Bun, dar avem filtru de motorină cu decantare...', 'c', 'ok'], [A.apa0 - .05, '...care reține apa din combustibil', 'g', 'theory'],
          [A.schimba1 - .05, 'Logica e bună, dar în practică depinde de cum e exploatată mașina', 'r', 'practice'], [A.pompa2 - .05, 'Impurități, apă sau mizerie ajung în pompă', 'r', 'pump']] },
      { k: 'chip', t0: A.sunt3 - .1, t1: A.dar4 - .3, y: 330, ph: [[A.sunt3 - .1, 'speech_balloon', 'SUNT MULTE SPEȚE DE DISCUTAT', 'blue']] },
      { k: 'schem', t0: A.dar4 - .1, t1: SEND - .1, type: 'decanterFilter', title: 'SCHEMĂ · CE AJUNGE LA POMPĂ', sub: 'FILTRU CU DECANTARE', stepNames: ['IMPURITĂȚI', 'REZERVOR'],
        steps: [[A.dar4, 'Pot ajunge la pompă impurități sau apă...', 'r', 'pump'], [A.apa4b - .05, '...sau apa care apare în rezervor', 'o', 'condens']] },
      { k: 'kin', t: A.decantare0 - .02, dur: A.decantare0E + .6 - A.decantare0, txt: 'CU DECANTARE?', col: '#62D8FF', y: 1650, size: 115, rot: -3 },
      { k: 'kin', t: A.logica1 - .02, dur: Math.min(A.logica1E + .3, A.practica1 - .1) - A.logica1, txt: 'LOGICA E BUNĂ...', col: '#4ADE80', y: 1650, size: 105, rot: -3 },
      { k: 'kin', t: A.practica1 - .02, dur: A.practica1E + .6 - A.practica1, txt: '...DAR ÎN PRACTICĂ?', col: '#FF4B4B', y: 1650, size: 100, rot: -3 },
      { k: 'kin', t: A.mizeria2 - .02, dur: A.mizeria2E + .5 - A.mizeria2, txt: 'APA SAU MIZERIA', col: '#FF8A3D', y: 1650, size: 105, rot: -3 },
      { k: 'kin', t: A.trece3 - .02, dur: 2.2, txt: 'TREC DE FILTRARE!', col: '#FF4B4B', y: 1650, size: 100, rot: -4 },
      { k: 'kin', t: A.rezervor5 - .02, dur: Math.max(.8, SEND - .05 - A.rezervor5), txt: 'APA DIN REZERVOR', col: '#62D8FF', y: 1650, size: 100, rot: -3 },
    ],
    fx: [...HB.fx, { k: 'punch', t: A.decantare0, a: .04 }, { k: 'glitch', t: A.schimba1 - .05, d: .12 }, { k: 'punch', t: A.practica1, a: .05 }, { k: 'punch', t: A.pompa2, a: .05 }, { k: 'punch', t: A.trece3, a: .07, sh: 9 }, { k: 'glitch', t: A.dar4 - .05, d: .12 }],
    bursts: HB.bursts,
  };
};
