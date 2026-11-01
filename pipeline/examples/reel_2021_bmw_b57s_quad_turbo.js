// v2 – Reel r2021 – „Quad Turbo BMW B57S recondiționat capital” (IMG_2021 + IMG_2024, filmate la un minut distanță, lipite în ordinea filmării, fără tăieturi)
// clipuri: 0 ansamblul biturbo pe banc, în laboratorul Turbo Doctor (IMG_2021) · 25.13 același ansamblu (IMG_2024) · fără fețe
// Sabin a cerut la început poză + logo BMW și o poză cu un X5 după 2020: logo-ul și pozele de pe internet nu le folosim (marcă / drepturi de autor);
// în loc, „BMW X5 · MOTOR B57S” scris în stilul nostru, pe chip-ul de mașină din hook. Dacă trimite o poză a lui cu un X5, intră la început.
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND }) => {
  const A = {
    quad: aw(0, 'Quad'), bmw0: aw(0, 'BMW'), cod: aw(0, 'cod'), b57s: aw(0, 'B57S'), reconditionat: aw(0, 'recondiționat'), capital: aw(0, 'capital'), la0: aw(0, 'la'),
    da1: aw(1, 'Da'), n30: aw(1, '3.0'), n4: aw(1, '4'), n400: aw(1, '400'), si1: aw(1, 'Și'), aducem: aw(1, 'aducem'), ladoar: aw(1, 'la', 3), n3040: aw(1, '30–40%'), costul: aw(1, 'costul'),
    aceasta2: aw(2, 'Această'), n1500: aw(2, '1.500'), per: aw(2, 'per'), garantie2: aw(2, 'garanție'), n24: aw(2, '24'), cu2b: aw(2, 'cu', 1), ansamblu: aw(2, 'ansamblu'),
  };
  // HOOK: „QUAD TURBO” bubuie pe „Quad”, „DE BMW” pe „BMW”; chip-ul cu mașina pe „cod motor”
  const B1 = A.quad - .03, B2 = A.bmw0 - .03, HB = A.reconditionat - .15;
  return {
    hook: { tag: 'ANALIZĂ TEHNICĂ · LABORATOR TURBO DOCTOR', car: 'BMW X5 · MOTOR B57S', carAt: A.cod - .02, end: HB },
    hideCap: [[0, HB - .05]],
    stages: [[A.da1 - .1, 'MOTORUL'], [A.si1 - .1, 'REZULTATUL'], [A.aceasta2 - .1, 'COSTUL'], [A.garantie2 - .1, 'GARANȚIA']],
    tags: {
      0: { quad: 'y', turbo: 'y', bmw: 'c', b57s: 'c', reconditionat: 'g', capital: 'g' },
      1: { diesel: 'c', bmw: 'c', turbine: 'c', cai: 'y', aducem: 'g', viata: 'g', noi: 'r' },
      2: { lei: 'y', turbina: 'c', garantie: 'g', luni: 'y', ansamblu: 'c', central: 'c' },
    },
    items: [
      // ---- hook: boom
      { k: 'boom', t: B1, dur: HB - B1, txt: 'QUAD TURBO', y: 860, size: 210, col: '#FFD21F', from: 3.8, sh: 24, ca: 30, bg: 1 },
      { k: 'boom', t: B2, dur: HB - B2, txt: 'DE BMW', y: 1080, size: 170, col: '#FFFFFF', from: 2.6, sh: 14, ca: 18, riser: false, bg: .7, glow: 'rgba(98,216,255,.55)' },
      // ---- fișa pacientului: recondiționat capital la Turbo Doctor
      { k: 'file', t0: HB + .02, t1: A.da1 - .3, no: 'B57S', ecg: 'ok', stamp: [A.capital, 'CAPITAL', 'green'],
        rows: [[A.reconditionat - .02, 'PACIENT', 'BMW X5', 'c', 'automobile'], [A.reconditionat + .15, 'MOTOR', 'B57S · 3.0 DIESEL', 'y', 'gear'],
          [A.reconditionat + .3, 'TRATAMENT', 'RECONDIȚIONAT', 'g', 'hammer_and_wrench'], [A.la0, 'LABORATOR', 'TURBO DOCTOR', 'y', 'test_tube']] },
      // ---- motorul: 3.0 diesel, 4 turbine, 400 CP
      { k: 'chip', t0: A.da1 - .05, t1: A.n30 - .3, y: 330, ph: [[A.da1 - .05, 'gear', 'MOTORUL B57S', 'blue']] },
      { k: 'eq', t0: A.n30 - .12, t1: A.si1 - .3, ico: 'gear', title: 'MOTORUL B57S', sub: 'BMW',
        lines: [[A.n30 - .02, '3.0 DIESEL', 'w'], [A.n4 - .02, '4 TURBINE', 'y'], [A.n400 - .02, '400 CP', 'big y']] },
      // ---- rezultatul: adus la viață, la 30–40% din costul unor turbine noi
      { k: 'ecg', t0: A.si1 - .05, t1: A.ladoar - .3, label: 'PULS QUAD TURBO', ico: 'stethoscope', states: [[A.si1 - .05, 'crit', 'ÎNAINTE'], [A.aducem, 'ok', 'ADUS LA VIAȚĂ']] },
      { k: 'bars', t0: A.ladoar - .05, t1: A.aceasta2 - .3, ico: 'euro_banknote', title: 'COSTUL', sub: 'RECONDIȚIONARE vs NOU',
        bars: [[A.n3040 - .02, 'RECONDIȚIONAT LA TURBO DOCTOR', .35, 'g', '30–40%'], [A.costul - .02, 'TURBINE NOI', 1, 'r', '100%']] },
      { k: 'kin', t: A.n3040 - .02, dur: 1.4, txt: 'DOAR 30–40%!', col: '#4ADE80', y: 1060, size: 130, rot: -4 },
      // ---- costul reparației și garanția
      { k: 'chip', t0: A.aceasta2 - .05, t1: A.n1500 - .3, y: 330, ph: [[A.aceasta2 - .05, 'euro_banknote', 'COSTUL REPARAȚIEI', 'blue']] },
      { k: 'eq', t0: A.n1500 - .12, t1: A.garantie2 - .3, ico: 'euro_banknote', title: 'COSTUL REPARAȚIEI', sub: 'TURBO DOCTOR',
        lines: [[A.n1500 - .02, '1.500 – 2.500 LEI', 'big y'], [A.per - .02, 'PER TURBINĂ', 'w']] },
      { k: 'chip', t0: A.garantie2 - .05, t1: A.cu2b - .3, y: 330, ph: [[A.garantie2 - .05, 'shield', 'GARANȚIE 24 DE LUNI', 'green']] },
      { k: 'kin', t: A.n24 - .02, dur: 1.0, txt: '24 LUNI GARANȚIE', col: '#FFD21F', y: 1060, size: 120, rot: -3 },
      { k: 'def', t0: A.cu2b - .05, t1: SEND - .2, term: 'ANSAMBLUL CENTRAL', text: 'Miezul turbinei: axul cu cele două roți, lagărele și carcasa centrală. Se schimbă întreg.' },
      { k: 'tip', t0: SEND + .1, t1: TEND - .15, top: 520, title: 'REȚETA TURBO DOCTOR', sub: 'SFAT DE INGINER · TURBO', ico: 'stethoscope',
        rows: [[SEND + .35, 'gear', 'Turbo defect? Întâi diagnoza, apoi decizi: nouă sau recondiționată'], [SEND + 1.15, 'euro_banknote', 'Recondiționarea: 30–40% din costul unor turbine noi'],
          [SEND + 1.95, 'shield', 'Cu ansamblul central schimbat: garanție 24 de luni']] },
    ],
    fx: [
      { k: 'flash', t: B1 - .11, a: .75 }, { k: 'punch', t: B1, a: .16, sh: 34 }, { k: 'glitch', t: B1, d: .2 }, { k: 'shock', t: B1 + .01, x: 540, y: 860, r: 760, n: 2, col: '#FFD21F' },
      { k: 'flash', t: B2 - .11, a: .45 }, { k: 'punch', t: B2, a: .08, sh: 16 }, { k: 'shock', t: B2 + .01, x: 540, y: 1080, r: 520, n: 1 },
      { k: 'glitch', t: HB - .05, d: .14 }, { k: 'punch', t: A.capital, a: .05 },
      { k: 'glitch', t: A.da1 - .12, d: .12 }, { k: 'punch', t: A.n4, a: .05 }, { k: 'punch', t: A.n400, a: .06, sh: 10 },
      { k: 'glitch', t: A.si1 - .12, d: .12 }, { k: 'punch', t: A.n3040, a: .05 }, { k: 'glitch', t: A.aceasta2 - .12, d: .12 }, { k: 'punch', t: A.n1500, a: .05 }, { k: 'punch', t: A.n24, a: .04 },
    ],
    sfx: [[HB - .1, 'whoosh', .6], [A.aducem, 'shimmer', .5]],
    bursts: [[B1 + .04, 540, 860, 8, 560, 1.7], [B2 + .04, 540, 1080, 4, 420, 1.2], [A.n400 + .05, 540, 600, 6, 340, .9], [A.n24 + .1, 540, 1060, 6, 360, .9]],
  };
};
