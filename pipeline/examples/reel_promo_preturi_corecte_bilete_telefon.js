// v2 – „Recondiționări perfecte la prețuri corecte” (14.11.2026, aprobat și publicat pe toate brandurile din Metricool) – promo prețuri recondiționare turbine, 2 clipuri lipite în ordinea filmării, fără tăieturi
// clipuri: 0 IMG_2481 (hook: turbinele recondiționate, vocea lui din spatele camerei) · 4.767 IMG_2482 (selfie, explicațiile)
// Cerut de Sabin: hook puternic din primul clip cu „Recondiționări perfecte la prețuri corecte”; cât explică, prețurile pe ecran
// (Volkswagen 1.9: 900–1000 lei · BMW 2.0: 1000–1300 lei · Mercedes 2.2 biturbo: 1000–1200 lei pe turbină · Logan Euro 3, Euro 4: doar 700 lei);
// când spune că prețul se vede direct pe site: un telefon care „se deschide” și rulează căutarea făcută de el pe turbodoctor.ro (înregistrarea lui de ecran,
// re-temporizată cu tools/phone/build_phone_frames.py -> assets/phone; partea cu Google e sărită: avea reclamele altor service-uri).
// Selfie filmat de aproape: grafica stă deasupra capului (biletele de preț la y 146–346), subtitrările cu 50 px mai jos (capTop), fără bara de etape.
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND, TOTAL }) => {
  const A = {
    da: aw(0, 'Da,'), am0: aw(0, 'Am'),
    pretul: aw(3, 'Prețul'), actuatorul: aw(3, 'actuatorul'), geometria: aw(3, 'geometria'), asa: aw(3, 'așa'), repede: aw(3, 'repede'), ca: aw(3, 'ca', 1), degeaba: aw(3, 'degeaba.'),
  };
  const CLIP = [0, 4.767];
  // HOOK – momentele sunt luate din sunet (anvelopa vocii), nu din ASR: „Recondiționări” .30 · „perfecte” 1.33 · „la prețuri” 2.64 · „corecte” 3.58
  const R1 = .30, R2 = 1.33, R3 = 2.64, R4 = 3.58, HEND = 4.72, Y1 = 262, Y2 = 522, Y3 = 1150, Y4 = 1398;   // între rândurile unei perechi rămâne loc pentru virgula lui Ț (altfel pare un accent pe rândul de jos)
  // „Am tăiat prețurile”: „Am” 6.90 · mâna taie aerul între cadrele 7.53 și 7.57 · „prețurile” 7.86, apoi titlul e tăiat în două
  const B1 = 6.90, HAND = 7.53, B2 = 7.86, TCUT = B2 + .32, BEND = 8.62, TY = 424;
  // biletele de preț, cât explică (unul odată, se întorc); prețul bubuie la +.32 s
  const PT = [8.95, 13.30, 17.60, 21.90], PEND = 26.30, PD = .32;
  // telefonul: intră pe „și le vedeți pe toate pe site-ul nostru”, iese după „…ansamblu central.”
  const P0 = 26.95, P1 = 39.85;
  return {
    hook: { tag: 'TURBO DOCTOR · PREȚURI NOI LA TURBINE', end: HEND, y: -76 },
    stages: null,
    capTop: 1340,
    hideCap: [[0, CLIP[1] - .02], [B1 - .08, BEND]],
    endSub: ['RECONDIȚIONĂRI PERFECTE', 'LA PREȚURI CORECTE'],
    tags: {
      0: { perfecte: 'g', corecte: 'y', preturi: 'y', taiat: 'g', preturile: 'y' },
      1: { buna: 'g', calitate: 'g', 5: 'y', ani: 'y', perfecte: 'g', reconditionari: 'c', corecte: 'y', preturi: 'y', taiat: 'g', preturile: 'y', toate: 'g', siteul: 'c' },
      2: { fara: 'g', ascunzisuri: 'g', talon: 'c', site: 'c', preturi: 'y', turbine: 'c', exact: 'g', costa: 'y', reconditionarea: 'c', intregului: 'g', ansamblu: 'c', central: 'c' },
      3: { pretul: 'y', creste: 'r', actuatorul: 'c', geometria: 'c', defecte: 'r', repede: 'g', problema: 'r', bani: 'y', plus: 'r', degeaba: 'r' },
    },
    items: [
      // ---- HOOK (IMG_2481, turbinele): titlul bubuie pe cuvinte – sus „RECONDIȚIONĂRI / PERFECTE”, jos „LA PREȚURI / CORECTE!”, turbina rămâne la vedere la mijloc
      { k: 'boom', t: R1, dur: HEND - R1, txt: 'RECONDIȚIONĂRI', y: Y1, size: 136, col: '#FFFFFF', from: 2.6, sh: 12, ca: 14, riser: false, bg: .55, glow: 'rgba(98,216,255,.5)' },
      { k: 'boom', t: R2, dur: HEND - R2, txt: 'PERFECTE', y: Y2, size: 250, col: '#4ADE80', from: 3.6, sh: 24, ca: 28, bg: .9, glow: 'rgba(74,222,128,.55)' },
      { k: 'boom', t: R3, dur: HEND - R3, txt: 'LA PREȚURI', y: Y3, size: 136, col: '#FFFFFF', from: 2.6, sh: 12, ca: 14, riser: false, bg: .5, glow: 'rgba(98,216,255,.5)' },
      { k: 'boom', t: R4, dur: HEND - R4, txt: 'CORECTE!', y: Y4, size: 250, col: '#FFD21F', from: 3.8, sh: 28, ca: 32, bg: 1 },

      // ---- IMG_2482: „Da, ați auzit bine. Am tăiat prețurile.”
      { k: 'chip', t0: A.da - .04, t1: B1 - .3, y: 330, ph: [[A.da - .04, 'exclamation', 'DA, AȚI AUZIT BINE!', 'yellow']] },
      { k: 'boom', t: B1, dur: BEND - B1, txt: 'AM TĂIAT', y: 256, size: 140, col: '#FFFFFF', from: 2.8, sh: 14, ca: 16, riser: false, bg: .6, glow: 'rgba(98,216,255,.5)' },
      { k: 'boom', t: B2, dur: BEND - B2, txt: 'PREȚURILE!', y: TY, size: 198, col: '#FFD21F', from: 3.8, sh: 26, ca: 30, riser: false, bg: 1, cut: [TCUT, -8, 15, 6] },
      { k: 'stk', ico: 'scissors', t0: B1 + .06, t1: BEND - .15, x: 902, y: 246, size: 122, rot: -18 },

      // ---- prețurile, cât explică: câte un bilet deasupra capului
      { k: 'ptag', t0: PT[0], t1: PEND, y: 246, pd: PD, kicker: 'RECONDIȚIONARE TURBINĂ', tags: [
        [PT[0], 'VOLKSWAGEN', 'MOTOR 1.9', '900–1000', '', 'PREȚ CORECT'],
        [PT[1], 'BMW', 'MOTOR 2.0', '1000–1300', '', 'PREȚ CORECT'],
        [PT[2], 'MERCEDES', '2.2 BITURBO', '1000–1200', '/ TURBINĂ', 'PREȚ CORECT'],
        [PT[3], 'LOGAN', 'EURO 3 · EURO 4', '700', '', 'DOAR', 116],
      ] },

      // ---- telefonul: căutarea lui pe site (momentele din înregistrare sunt tipărite de build_phone_frames.py)
      { k: 'phone', t0: P0, t1: P1, labY: 232,
        cam: [[P0, 590, 100], [30.22, 900, -405, .62], [31.32, 900, 40, .3], [32.78, 940, -80, .95], [33.78, 1000, -60, .4], [37.02, 1000, -300, .5], [38.36, 1060, -716, .85]],
        taps: [[28.43, 1205, 395], [29.58, 300, 1796], [30.95, 330, 1472], [33.32, 360, 1257], [34.70, 420, 1068], [35.25, 950, 704], [36.40, 560, 1396]],
        hl: [
          { t0: 27.72, t1: 28.72, box: [262, 2614, 796, 160], r: 78, col: '#62D8FF', sw: 12, silent: true },   // bara de adresă: turbodoctor.ro
          { t0: 30.30, t1: 30.88, box: [36, 1396, 1256, 752], r: 30, sw: 11, silent: true },                      // lista „Prețuri”
          { t0: 32.80, t1: 33.26, box: [66, 1150, 1194, 410], r: 34, sw: 11, silent: true },                      // marca · modelul · codul motorului · puterea
          { t0: 38.12, t1: P1, box: [22, 1388, 1276, 668], r: 34, dim: .86, sw: 13 },                             // rezultatul: Golf V 1.9 -> 900 lei
        ],
        lab: [[29.62, 'TOATE PREȚURILE PE SITE', 'FĂRĂ ASCUNZIȘURI', 'g'], [31.00, 'FĂRĂ SĂ TRIMIȚI', 'TALONUL', 'g'], [33.35, 'PASUL 1', 'ALEGI MARCA', 'c'], [35.28, 'PASUL 2', 'ALEGI MODELUL', 'c'],
          [36.50, 'PASUL 3', 'VEZI PREȚUL EXACT', 'y'], [38.12, 'VOLKSWAGEN GOLF V · 1.9 · 90 CP', '900 LEI', 'y', 116]],
        note: [[38.67, '✓ ANSAMBLU CENTRAL NOU']] },

      // ---- finalul: prețul poate crește -> vino repede
      { k: 'chip', t0: A.pretul - .02, t1: A.asa - .28, y: 330, ph: [[A.pretul - .02, 'warning', 'PREȚUL POATE CREȘTE', 'red'], [A.actuatorul - .05, 'gear', 'DACĂ ACTUATORUL…', 'red'], [A.geometria - .05, 'gear', '…ȘI GEOMETRIA SUNT DEFECTE', 'red']] },
      { k: 'chip', t0: A.asa - .04, t1: SEND - .12, y: 330, ph: [[A.asa - .04, 'stopwatch', 'VINO CU TURBINA CÂT MAI REPEDE', 'green'], [A.ca - .04, 'money_bag', 'NU DAI BANI ÎN PLUS', 'green']] },

      // ---- cardul de final: sloganul campaniei (endSub) + lista de prețuri ca „rețetă”, sub „Diagnoză gratuită”
      { k: 'prices', t0: TEND + 2.7, t1: TOTAL - .12, top: 1172, title: 'REȚETA TURBO DOCTOR', sub: 'RECONDIȚIONARE TURBINĂ', rows: [
        [TEND + 3.0, 'VOLKSWAGEN 1.9', '900–1000', 'LEI'], [TEND + 3.35, 'BMW 2.0', '1000–1300', 'LEI'],
        [TEND + 3.7, 'MERCEDES 2.2 BITURBO', '1000–1200', 'LEI/TURBINĂ'], [TEND + 4.05, 'LOGAN EURO 3 · EURO 4', '700', 'LEI']] },
    ],
    fx: [
      // hook
      { k: 'flash', t: R1 - .1, a: .35 }, { k: 'punch', t: R1, a: .07, sh: 14 }, { k: 'glitch', t: R1, d: .1 },
      { k: 'flash', t: R2 - .11, a: .6 }, { k: 'punch', t: R2, a: .13, sh: 26 }, { k: 'glitch', t: R2, d: .14 }, { k: 'shock', t: R2 + .01, x: 540, y: Y2, r: 700, n: 2, col: '#4ADE80', col2: '#FFFFFF' },
      { k: 'punch', t: R3, a: .06, sh: 12 },
      { k: 'flash', t: R4 - .11, a: .75 }, { k: 'punch', t: R4, a: .16, sh: 34 }, { k: 'glitch', t: R4, d: .18 }, { k: 'shock', t: R4 + .01, x: 540, y: Y4, r: 780, n: 2, col: '#FFD21F', col2: '#FFFFFF' },
      { k: 'glitch', t: CLIP[1] - .04, d: .12 },
      // „AM TĂIAT” · mâna taie aerul · „PREȚURILE!” · titlul tăiat
      { k: 'flash', t: B1 - .1, a: .4 }, { k: 'punch', t: B1, a: .08, sh: 16 }, { k: 'glitch', t: B1, d: .12 },
      { k: 'slash', t: HAND, x1: 1100, y1: 870, x2: 150, y2: 1780, w: 20, d: .05, hold: .24, lin: 1 }, { k: 'punch', t: HAND + .05, a: .04, sh: 12 },
      { k: 'flash', t: B2 - .11, a: .7 }, { k: 'punch', t: B2, a: .15, sh: 30 }, { k: 'glitch', t: B2, d: .16 }, { k: 'shock', t: B2 + .01, x: 540, y: TY, r: 720, n: 2, col: '#FFD21F', col2: '#FFFFFF' },
      { k: 'slash', t: TCUT - .07, x1: 1095, y1: TY - 104, x2: -15, y2: TY + 104, w: 17, d: .07, hold: .3 }, { k: 'punch', t: TCUT, a: .07, sh: 18 }, { k: 'flash', t: TCUT - .05, a: .3 },
      { k: 'glitch', t: BEND - .04, d: .12 },
      // prețurile
      ...PT.flatMap((t, i) => [{ k: 'flash', t: t + PD - .12, a: i === 3 ? .42 : .32 }, { k: 'punch', t: t + PD - .02, a: i === 3 ? .1 : .075, sh: i === 3 ? 20 : 15 }]),
      // telefonul: fundalul se estompează cât stă pe ecran
      { k: 'veil', t0: P0 + .35, t1: P1 + .08, in: .4, out: .34, a: .8 },
      { k: 'punch', t: 38.12, a: .05, sh: 10 },
      // finalul
      { k: 'punch', t: A.pretul, a: .05, sh: 10 }, { k: 'punch', t: A.repede, a: .05 }, { k: 'punch', t: A.degeaba, a: .04 },
    ],
    sfx: [[HAND - .03, 'slash', .8], [HAND - .12, 'whoosh', .5], [BEND - .08, 'whoosh', .5], [CLIP[1] - .1, 'whoosh', .6]],
    bursts: [[R2 + .04, 540, Y2 + 30, 5, 400, 1.3], [B2 + .04, 540, 300, 4, 240, 1.2]],   // scânteile stau pe titlu, nu pe față
  };
};
