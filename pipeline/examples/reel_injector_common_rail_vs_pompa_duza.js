// v2 – Reel #7 din vlogul „Top 3 simptome injector defect” – Pompă-duză vs common rail (sursa 141.45–199.90)
// Vlog orizontal pus pe vertical (cadrul la y 868–1476). Hook: titlul care bubuie peste prima frază. Schemă nouă `commonRail` (în pipeline/schem.js din 09.11.2026):
// pas 0 = injectorul pompă-duză, pașii 1–6 = common rail (pompa, rampa sub presiune, conductele, calculatorul, tipurile de injectoare).
// Etichetele vechi arse („INJ. PUMPE DÜSE”, „INJ. COMMON RAIL”) sunt acoperite de cardurile noastre lbl; imaginile din vlog rămân.
// cardul de final al seriei „simptome injector” (cerut de Sabin pe 08.11.2026, doar pentru această serie): cardul standard + „Experți în diagnosticarea sistemelor de injecție” + telefonul
// Telefonul de pe cardul de final (ENDCARD) a fost cerut DOAR pentru seria asta; implicit nu se pune (regula din 25.10.2026). Seria a fost aprobată și programată pe 09.11.2026.
const ENDCARD = (TEND, TOTAL) => [
  { k: 'lbl', t0: TEND + .12, t1: TOTAL + 1, x: 540, y: 236, w: 960, h: 176, ph: [[TEND + .12, '', '<span style="color:#fff">EXPERȚI ÎN DIAGNOSTICAREA</span><br>SISTEMELOR DE INJECȚIE', 'y']] },
  { k: 'eq', t0: TEND + 2.45, t1: TOTAL + 1, top: 1172, ico: 'phone', title: 'PROGRAMĂRI', sub: '', lines: [[TEND + 2.7, '0739 065 065', 'big y']] },
];
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND, TOTAL }) => {
  const A = {
    n2000: aw(0, '2000'), in1: aw(1, 'în'), sistemul: aw(1, 'sistemul'), pd: aw(1, 'pompă-duză'), pompa1: aw(1, 'pompă'), injector1: aw(1, 'injector', 1),
    si2: aw(2, 'și'), folosit: aw(2, 'folosit'), common2: aw(2, 'common'),
    inalta: aw(3, 'înaltă'), rampa: aw(4, 'rampă'), conducte: aw(4, 'conducte'),
    aceste: aw(5, 'Aceste'), calculatorul: aw(5, 'calculatorul'), magnetice: aw(5, 'magnetice'),
  };
  const T1 = .12, T2 = .62, HEND = A.in1 - .1;
  return {
    hideCap: [[0, HEND]],
    stages: [[HEND, '2 SISTEME'], [A.sistemul - .1, 'POMPĂ-DUZĂ'], [A.si2 - .1, 'COMMON RAIL'], [A.aceste - .1, 'INJECTOARELE']],
    items: [
      // HOOK
      { k: 'chip', t0: .05, t1: HEND, y: 172, ph: [[.05, 'gear', 'SISTEME DE INJECȚIE DIESEL', 'blue']] },
      { k: 'boom', t: T1, dur: HEND - T1, txt: 'POMPĂ-DUZĂ', y: 372, size: 150, col: '#FFFFFF', from: 3.6, sh: 26, ca: 30, bg: 1 },
      { k: 'boom', t: T2, dur: HEND - T2, txt: 'SAU COMMON RAIL?', y: 600, size: 108, col: '#FFD21F', from: 2.6, sh: 14, ca: 18, riser: false, bg: .7 },
      { k: 'kin', t: A.n2000 - .02, dur: HEND - A.n2000 + .1, txt: 'PESTE 2000 DE BARI', col: '#FF3B30', y: 1640, size: 92, rot: -3 },
      { k: 'chip', t0: HEND, t1: A.sistemul - .3, y: 330, ph: [[HEND, 'gear', '2 TIPURI DE SISTEME', 'yellow']] },
      // etichetele vechi ale vlogului, acoperite
      { k: 'lbl', t0: 9.6, t1: 18.0, x: 262, y: 937, w: 470, h: 108, ph: [[9.6, 'SISTEMUL #1', 'POMPĂ-DUZĂ']] },
      { k: 'lbl', t0: 22.7, t1: 47.8, x: 290, y: 937, w: 520, h: 108, ph: [[22.7, 'SISTEMUL #2', 'COMMON RAIL']] },
      // schema: pompă-duză, apoi common rail pe ce spune
      { k: 'schem', t0: A.sistemul - .1, t1: SEND - .15, top: 268, h: 400, type: 'commonRail', title: 'SCHEMĂ · SISTEME DE INJECȚIE', sub: 'POMPĂ-DUZĂ VS COMMON RAIL',
        stepNames: ['POMPĂ-DUZĂ', 'COMMON RAIL', 'POMPA', 'RAMPA', 'CONDUCTE', 'CALCULATOR', 'INJECTOARE'],
        steps: [[A.sistemul - .1, 'Injectorul joacă rolul de pompă și de injector', 'y', 0],
                [A.folosit - .05, 'Cel mai folosit sistem în prezent', 'g', 1],
                [A.inalta - .05, 'Nu mai avem pompă de injecție, ci pompă de înaltă presiune', 'y', 2],
                [A.rampa - .05, 'Rampa comună: aici stă combustibilul sub presiune', 'y', 3],
                [A.conducte - .05, 'Câte o conductă către fiecare injector', 'y', 4],
                [A.calculatorul - .05, 'Injectoarele sunt comandate de calculatorul de injecție', 'y', 5],
                [A.magnetice - .05, 'Două feluri: magnetice și piezoelectrice', 'y', 6]] },
      { k: 'kin', t: A.pompa1 - .02, dur: A.injector1 + .9 - A.pompa1, txt: 'POMPĂ + INJECTOR', col: '#FFD21F', y: 1640, size: 100, rot: -3 },
      { k: 'kin', t: A.folosit - .02, dur: 2.4, txt: 'CEL MAI FOLOSIT', col: '#4ADE80', y: 1640, size: 104, rot: -3 },
      { k: 'kin', t: A.magnetice - .02, dur: SEND - A.magnetice + .2, txt: 'MAGNETICE SAU PIEZO', col: '#FFD21F', y: 1640, size: 88, rot: -3 },
      ...ENDCARD(TEND, TOTAL),
    ],
    fx: [
      { k: 'flash', t: .01, a: .7 }, { k: 'punch', t: T1, a: .16, sh: 34 }, { k: 'glitch', t: T1, d: .2 }, { k: 'shock', t: T1 + .01, x: 540, y: 372, r: 760, n: 2 },
      { k: 'flash', t: T2 - .11, a: .4 }, { k: 'punch', t: T2, a: .08, sh: 16 }, { k: 'shock', t: T2 + .01, x: 540, y: 600, r: 520, n: 1, col: '#FFD21F', col2: '#FFFFFF' },
      { k: 'punch', t: A.n2000, a: .08, sh: 16 }, { k: 'glitch', t: HEND, d: .12 }, { k: 'punch', t: A.pd, a: .05, sh: 10 }, { k: 'punch', t: A.common2, a: .06, sh: 12 },
      { k: 'punch', t: A.rampa, a: .04, sh: 8 }, { k: 'punch', t: A.calculatorul, a: .04, sh: 8 }, { k: 'punch', t: A.magnetice, a: .06, sh: 12 },
    ],
    bursts: [[T1 + .04, 540, 372, 8, 460, 1.3]],
  };
};
