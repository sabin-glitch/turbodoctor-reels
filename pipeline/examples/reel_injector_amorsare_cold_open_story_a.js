// v2 – Reel #5 din vlogul „Top 3 simptome injector defect” – Cauza #2: amorsarea după schimbarea filtrului de motorină (sursa 414.80–492.30)
// Hook: cold open din același clip (sursa 474.65–480.80, „În cel mai rău caz, pompa de înaltă presiune poate genera pilitură…”), apoi povestea
// de la „Haideți să discutăm…” (out/v2.json story_a 3.955: am scos doar începutul „Am vorbit despre lucrurile stupide…”, care trimite la partea anterioară a vlogului).
// Eticheta veche arsă („NEAMORSAREA SISTEMULUI”) e acoperită de cardul nostru lbl. Card de final cu telefon (excepție cerută de Sabin doar la seria asta).
// cardul de final al seriei „simptome injector” (cerut de Sabin pe 08.11.2026, doar pentru această serie): cardul standard + „Experți în diagnosticarea sistemelor de injecție” + telefonul
// Telefonul de pe cardul de final (ENDCARD) a fost cerut DOAR pentru seria asta; implicit nu se pune (regula din 25.10.2026). Seria a fost aprobată și programată pe 09.11.2026.
const ENDCARD = (TEND, TOTAL) => [
  { k: 'lbl', t0: TEND + .12, t1: TOTAL + 1, x: 540, y: 236, w: 960, h: 176, ph: [[TEND + .12, '', '<span style="color:#fff">EXPERȚI ÎN DIAGNOSTICAREA</span><br>SISTEMELOR DE INJECȚIE', 'y']] },
  { k: 'eq', t0: TEND + 2.45, t1: TOTAL + 1, top: 1172, ico: 'phone', title: 'PROGRAMĂRI', sub: '', lines: [[TEND + 2.7, '0739 065 065', 'big y']] },
];
window.REEL_CFG = ({ aw, ew, cw, cwe, S0, SEND, TEND, TOTAL }) => {
  const A = {
    stupid: aw(0, 'stupid'), amorsarea: aw(0, 'amorsarea'), in0: aw(0, 'În'), schimbam: aw(0, 'schimbăm'),
    dezamorsam: aw(1, 'dezamorsăm'), procedura: aw(1, 'procedură'),
    daca: aw(2, 'Dacă'), fortam: aw(2, 'forțăm'), aerisire: aw(2, 'aerisire'), aducem: aw(2, 'aducem'),
    ne: aw(3, 'ne'), lipsa: aw(3, 'lipsa'), lubrifiere: aw(3, 'lubrifiere'), difera: aw(3, 'diferă'), altul: ew(3, 'altul'),
    in4: aw(4, 'În'), rau: aw(4, 'rău'), pilitura: aw(4, 'pilitură'), distruge: aw(4, 'distruge'), injectie4: ew(4, 'injecție'),
    bun: aw(5, 'bun'), ce5: aw(5, 'ce'), rezolvate: aw(5, 'rezolvate'), dar: aw(5, 'dar'), importante: aw(6, 'importante'),
  };
  const T1 = cw('În') + .02, T2 = cw('pilitură') - .02, TD = cw('distruge') - .02;
  return {
    stages: [[S0, 'GREȘEALA'], [A.amorsarea - .1, 'AMORSAREA'], [A.daca - .1, 'DACĂ NU'], [A.in4 - .1, 'EFECTELE']],
    items: [
      // HOOK (cold open din același clip)
      { k: 'chip', t0: .05, t1: S0, y: 172, ph: [[.05, 'warning', 'DUPĂ SCHIMBAREA FILTRULUI DE MOTORINĂ', 'red']] },
      { k: 'boom', t: T1, dur: S0 - T1, txt: 'ÎN CEL MAI RĂU CAZ', y: 372, size: 100, col: '#FFFFFF', from: 3.0, sh: 18, ca: 20, bg: .8 },
      { k: 'boom', t: T2, dur: S0 - T2, txt: 'PILITURĂ', y: 600, size: 230, col: '#FFD21F', from: 3.6, sh: 26, ca: 30, bg: 1 },
      { k: 'kin', t: TD, dur: S0 - TD + .05, txt: 'DISTRUGE TOT SISTEMUL!', col: '#FF3B30', y: 1640, size: 80, rot: -3 },
      // greșeala mecanicului
      { k: 'chip', t0: S0 + .05, t1: A.amorsarea - .3, y: 330, ph: [[S0 + .05, 'wrench', 'CÂND MECANICUL…', 'yellow'], [A.stupid - .05, 'warning', '…FACE CEVA STUPID', 'red']] },
      // eticheta veche a vlogului, acoperită
      { k: 'lbl', t0: 12.595, t1: 17.095, x: 290, y: 937, w: 540, h: 108, ph: [[12.595, 'TOP 3 CAUZE · #2', 'NEAMORSAREA SISTEMULUI']] },
      { k: 'def', t0: A.amorsarea - .1, t1: A.in0 - .3, term: 'AMORSAREA SISTEMULUI', text: 'Umplerea circuitului de alimentare cu motorină și scoaterea aerului, ca pompa să primească imediat combustibil.' },
      { k: 'pipe', t0: A.in0 - .1, t1: A.daca - .3, top: 268, ico: 'wrench', title: 'SCHIMBAREA FILTRULUI DE MOTORINĂ', steps: [
        [A.schimbam - .05, 'wrench', 'SCHIMBI<br>FILTRUL'], [A.dezamorsam - .05, 'dashing_away', 'SISTEMUL SE<br>DEZAMORSEAZĂ'], [A.procedura - .05, 'check_mark_button', 'PROCEDURA<br>PRODUCĂTORULUI']] },
      { k: 'kin', t: A.dezamorsam - .02, dur: 2.2, txt: 'SE DEZAMORSEAZĂ', col: '#FFD21F', y: 1640, size: 104, rot: -3 },
      { k: 'kin', t: A.procedura - .02, dur: A.daca - A.procedura - .25, txt: 'PROCEDURA PRODUCĂTORULUI', col: '#4ADE80', y: 1640, size: 76, rot: -3 },
      // dacă nu respectăm procedura
      { k: 'list', t0: A.daca - .1, t1: A.ne - .3, top: 268, ico: 'warning', title: 'DACĂ NU RESPECȚI PROCEDURA', rows: [
        [A.fortam - .05, 'Forțezi pornirea motorului', 'bad'], [A.aerisire - .05, 'Fără aerisire din diagnoză', 'bad'], [A.aducem - .05, 'Motorina nu ajunge la timp la pompă', 'bad']] },
      { k: 'chip', t0: A.ne - .05, t1: A.lipsa - .3, y: 330, ph: [[A.ne - .05, 'warning', 'O ANUMITĂ PROBLEMĂ…', 'yellow']] },
      { k: 'def', t0: A.lipsa - .1, t1: A.in4 - .3, term: 'LIPSA DE LUBRIFIERE', text: 'Pompa de înaltă presiune și injectoarele sunt unse chiar de motorină. Fără ea, piesele lor lucrează fără ungere.' },
      { k: 'kin', t: A.lubrifiere - .02, dur: 2.3, txt: 'LIPSĂ DE LUBRIFIERE', col: '#FF3B30', y: 1640, size: 96, rot: -3 },
      { k: 'kin', t: A.difera - .02, dur: A.altul + .4 - A.difera, txt: 'DIFERĂ DE LA SISTEM LA SISTEM', col: '#62D8FF', y: 1640, size: 70, rot: -3 },
      // efectele: cel mai rău caz / caz bun
      { k: 'cmp', t0: A.in4 - .1, t1: A.ce5 - .3, top: 268, w: 780, ico: 'magnifying_glass_tilted_left', title: 'CE SE POATE ÎNTÂMPLA',
        a: [A.rau - .05, 'warning', 'CEL MAI RĂU CAZ', 'POMPA FACE<br>PILITURĂ'], b: [A.bun - .05, 'wrench', 'CAZ BUN', 'BLOCAREA<br>INJECTOARELOR'], aCls: 'bad', bCls: 'bad' },
      { k: 'kin', t: A.pilitura - .02, dur: A.distruge - A.pilitura - .05, txt: 'PILITURĂ!', col: '#FFD21F', y: 1640, size: 130, rot: -4 },
      { k: 'kin', t: A.distruge - .02, dur: A.injectie4 + .5 - A.distruge, txt: 'DISTRUGE TOT SISTEMUL!', col: '#FF3B30', y: 1640, size: 80, rot: -3 },
      { k: 'eq', t0: A.ce5 - .1, t1: SEND - .15, top: 268, ico: 'wrench', title: 'CAZUL BUN', sub: 'BLOCAREA INJECTOARELOR',
        lines: [[A.rezolvate - .05, 'SE REZOLVĂ MAI IEFTIN', 'g'], [A.dar - .05, 'DAR TOT CU INTERVENȚII', 'w'], [A.importante - .05, 'IMPORTANTE', 'big y']] },
      ...ENDCARD(TEND, TOTAL),
    ],
    fx: [
      { k: 'flash', t: .01, a: .5 }, { k: 'punch', t: T1, a: .08, sh: 16 }, { k: 'glitch', t: T1, d: .14 }, { k: 'shock', t: T1 + .01, x: 540, y: 372, r: 560, n: 1 },
      { k: 'flash', t: T2 - .11, a: .75 }, { k: 'punch', t: T2, a: .16, sh: 34 }, { k: 'glitch', t: T2, d: .2 }, { k: 'shock', t: T2 + .01, x: 540, y: 600, r: 780, n: 2, col: '#FFD21F', col2: '#FFFFFF' },
      { k: 'punch', t: TD, a: .08, sh: 16 }, { k: 'glitch', t: S0 - .02, d: .14 },
      { k: 'punch', t: A.stupid, a: .05, sh: 10 }, { k: 'punch', t: A.dezamorsam, a: .05, sh: 10 }, { k: 'punch', t: A.procedura, a: .04, sh: 8 },
      { k: 'punch', t: A.fortam, a: .04, sh: 8 }, { k: 'punch', t: A.lubrifiere, a: .07, sh: 14 }, { k: 'glitch', t: A.lubrifiere - .03, d: .12 },
      { k: 'punch', t: A.pilitura, a: .1, sh: 22 }, { k: 'glitch', t: A.pilitura - .03, d: .16 }, { k: 'punch', t: A.distruge, a: .06, sh: 12 }, { k: 'punch', t: A.importante, a: .05, sh: 10 },
    ],
    bursts: [[T2 + .04, 540, 600, 8, 460, 1.3]],
  };
};
