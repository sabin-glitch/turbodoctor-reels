// v2 – „Am tăiat prețurile la Turbo Doctor!” (11.11.2026, aprobat și programat) – 6 clipuri selfie lipite în ordinea filmării, fără tăieturi
// clipuri: 0 IMG_2333 (hook) · 3.267 IMG_2336 (Volkswagen 1.9) · 16.433 IMG_2337 (BMW N47/M47) · 27.733 IMG_2338 (Logan 1.5 + condiții)
//          · 52.067 IMG_2340 (transport Cargus) · 64.5 IMG_2341 (mulțumiri)
// Cerut de Sabin: hook foarte puternic pe „am tăiat prețurile” + câte o mașină tăiată deasupra capului când vorbește de fiecare mașină
// (Volkswagen 1.9, BMW, Logan 1.5), tăiate de piesa `cut` (tools/cut_cars). VW = imagine AI generică, fără sigle. BMW și Logan = poze reale cerute de
// Sabin pe 11.11 („exact un Seria 3 E90 și un Logan”), luate de pe Wikimedia Commons doar cu licență liberă:
//   BMW   „2005-2008 BMW 320i (E90) sedan (2011-07-17) 01.jpg”, autor OSX, domeniu public (întoarsă spre stânga, plăcuța de înmatriculare acoperită)
//   Logan „2011 Renault Logan Silverline side.jpg”, autor Throwawayacc222, CC0 (Logan I, vedere laterală)
// Selfie filmat de aproape: toată grafica stă deasupra capului (y < ~390; chip-uri la y 236 unde capul urcă în cadru), fără bara de etape și fără `kin`
// sub bărbie (gura e la y 1060–1250, bărbia ajunge la y 1400) – de aceea și subtitrările sunt cu 50 px mai jos (capTop).
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND, TOTAL }) => {
  const A = {
    reparatia0: aw(0, 'Reparația'), vw: aw(0, 'Volkswagen'), n19: aw(0, '1.9'), codurile: aw(0, 'codurile'), n900: aw(0, '900'), functie0: aw(0, 'funcție'),
    ansamblu0: aw(0, 'ansamblu'), garantie0: aw(0, 'garanție'), n24a: aw(0, '24'),
    bmw: aw(1, 'BMW'), n47: aw(1, 'N47'), m47: aw(1, 'M47'), n1000b: aw(1, '1000'), functie1: aw(1, 'funcție'),
    cea: aw(2, 'cea'), ieftina: aw(2, 'ieftină'), logan: aw(2, 'Logan'), n15: aw(2, '1.5'), euro: aw(2, 'Euro'), n700: aw(2, '700'),
    toate: aw(2, 'Toate'), garantie2: aw(2, 'garanție'), schimbarea: aw(2, 'schimbarea'), ansamblu2: aw(2, 'ansamblu'),
    tineti: aw(2, 'Țineți'), pretul2: aw(2, 'prețul'), geometria: aw(2, 'geometria'), actuatorul: aw(2, 'actuatorul'), aduceti: aw(2, 'aduceți'), repede: aw(2, 'repede'),
    pretul3: aw(3, 'prețul'), daca3: aw(3, 'Dacă'), niciun: aw(3, 'niciun'), transportul: aw(3, 'Transportul'), doar3: aw(3, 'doar'), n40: aw(3, '40'), poti: aw(3, 'poți'),
    aceeasi: aw(4, 'Aceeași'), acum: aw(4, 'acum'), bun: aw(4, 'bun'), va4: aw(4, 'Vă'), in4: aw(4, 'în'),
  };
  const CLIP = [0, 3.267, 16.433, 27.733, 52.067, 64.5];
  // HOOK – momentele sunt luate din sunet și din imagine, nu din ASR: „Am” .49 · „tăiat” .80 · mâna taie aerul 1.00–1.07 · „prețurile” 1.36
  const B1 = .50, HAND = 1.0, B2 = 1.36, TCUT = 1.68, HEND = 3.15, TY = 446;
  // mașinile: apar pe numele mașinii, sunt tăiate la +.5 s, iar la preț se strâng în stânga și prețul bubuie în dreapta
  const VW0 = A.vw - .08, BM0 = A.bmw - .08, LG0 = A.logan - .08, CY = 268;
  return {
    hook: { tag: 'TURBO DOCTOR · REPARAȚII TURBINE', end: HEND, y: -64 },
    stages: null,
    capTop: 1340,
    hideCap: [[0, HEND - .05]],
    tags: {
      0: { preturile: 'y', volkswagen: 'c', 19: 'c', b: 'c', 900: 'y', 1000: 'y', lei: 'y', 24: 'y', luni: 'y' },
      1: { bmw: 'c', n47: 'c', m47: 'c', doar: 'g', 1000: 'y', 1300: 'y', lei: 'y' },
      2: { ieftina: 'g', logan: 'c', 15: 'c', doar: 'g', 700: 'y', lei: 'y', 24: 'y', luni: 'y', creste: 'r', distruse: 'r', repede: 'g', defecta: 'r' },
      3: { jos: 'g', problema: 'g', cargus: 'c', doar: 'g', 40: 'y', lei: 'y', oriunde: 'g', tara: 'g' },
      4: { calitate: 'g', bun: 'g', multumim: 'g', volum: 'c', bune: 'g', preturi: 'y' },
    },
    items: [
      // ---- HOOK: „AM TĂIAT” pe „Am tăiat”, „PREȚURILE!” pe „prețurile”, apoi titlul e tăiat în două (ca gestul lui cu mâna)
      { k: 'boom', t: B1, dur: HEND - B1, txt: 'AM TĂIAT', y: 276, size: 146, col: '#FFFFFF', from: 2.8, sh: 14, ca: 16, riser: false, bg: .6, glow: 'rgba(98,216,255,.5)' },
      { k: 'boom', t: B2, dur: HEND - B2, txt: 'PREȚURILE!', y: 446, size: 205, col: '#FFD21F', from: 3.8, sh: 26, ca: 30, riser: false, bg: 1, cut: [TCUT, -8, 15, 6] },

      { k: 'stk', ico: 'scissors', t0: .08, t1: HEND - .15, x: 905, y: 262, size: 128, rot: -18 },   // „tăiat” se vede din primul cadru, și fără sunet

      // ---- IMG_2336: Volkswagen 1.9
      { k: 'chip', t0: A.reparatia0 - .1, t1: VW0 - .3, y: 330, ph: [[A.reparatia0 - .1, 'wrench', 'REPARAȚIA UNEI TURBINE', 'blue']] },
      { k: 'cut', car: 'vw', t0: VW0, t1: CLIP[2] - .25, cutAt: VW0 + .5, y: CY,
        name: [[VW0, 'VOLKSWAGEN'], [A.n19 - .03, 'VOLKSWAGEN 1.9']], sub: [[A.codurile - .05, 'COD MOTOR: ÎNCEPE CU „B”']],
        price: [A.n900 - .03, '900–1000'], note: [[A.functie0 - .1, 'ÎN FUNCȚIE DE CODUL TURBINEI'], [A.ansamblu0 - .05, '✓ ANSAMBLU CENTRAL NOU', 'g'], [A.garantie0 - .05, '✓ GARANȚIE 24 DE LUNI', 'g']] },

      // ---- IMG_2337: BMW, motoare N47 și M47
      { k: 'cut', car: 'bmw', t0: BM0, t1: CLIP[3] - .25, cutAt: BM0 + .5, y: CY - 12, w: 520, s2: .62, dy2: 32,
        name: [[BM0, 'BMW']], sub: [[A.n47 - .05, 'COD MOTOR: N47'], [A.m47 - .05, 'COD MOTOR: N47 · M47']],
        price: [A.n1000b - .03, '1000–1300'], note: [[A.functie1 - .1, 'ÎN FUNCȚIE DE MODEL']] },

      // ---- IMG_2338: Logan 1.5 Euro 3, apoi condițiile
      { k: 'chip', t0: A.cea - .05, t1: LG0 - .3, y: 330, ph: [[A.cea - .05, 'money_bag', 'CEA MAI IEFTINĂ REPARAȚIE', 'green']] },
      { k: 'cut', car: 'logan', t0: LG0, t1: A.toate - .22, cutAt: LG0 + .5, y: CY, w: 640, s2: .58,
        name: [[LG0, 'LOGAN'], [A.n15 - .03, 'LOGAN 1.5']], sub: [[A.euro - .05, 'EURO 3']],
        price: [A.n700 - .03, '700'], prSize: 172, pry: -50, unDy: 114, note: [[A.n700 + .45, 'CEA MAI IEFTINĂ REPARAȚIE', 'y']] },
      { k: 'chip', t0: A.toate - .05, t1: A.tineti - .3, y: 236, ph: [[A.toate - .05, 'check_mark_button', 'TOATE PREȚURILE INCLUD:', 'blue'],
        [A.garantie2 - .05, 'shield', 'GARANȚIE 24 DE LUNI', 'green'], [A.schimbarea - .05, 'gear', 'ANSAMBLU CENTRAL NOU', 'green']] },
      { k: 'chip', t0: A.tineti - .05, t1: A.aduceti - .3, y: 236, ph: [[A.tineti - .05, 'exclamation', 'ȚINEȚI MINTE', 'yellow'], [A.pretul2 - .05, 'warning', 'PREȚUL POATE CREȘTE', 'red'],
        [A.geometria - .05, 'gear', 'DACĂ GEOMETRIA VARIABILĂ…', 'red'], [A.actuatorul - .05, 'gear', '…ȘI ACTUATORUL SUNT DISTRUSE', 'red']] },
      { k: 'chip', t0: A.aduceti - .05, t1: CLIP[4] - .25, y: 236, ph: [[A.aduceti - .05, 'stopwatch', 'ADU TURBINA CÂT MAI REPEDE', 'green'], [A.pretul3 - .05, 'chart_down', 'PREȚUL RĂMÂNE CÂT MAI JOS', 'green']] },

      // ---- IMG_2340: transportul
      { k: 'chip', t0: A.daca3 - .05, t1: A.transportul - .3, y: 330, ph: [[A.daca3 - .05, 'round_pushpin', 'NU EȘTI ÎN ORAȘELE NOASTRE?', 'yellow'], [A.niciun - .05, 'check_mark_button', 'NICIO PROBLEMĂ!', 'green']] },
      { k: 'chip', t0: A.transportul - .05, t1: CLIP[5] - .25, y: 330, ph: [[A.transportul - .05, 'package', 'TRANSPORT PRIN CARGUS', 'blue'], [A.poti - .05, 'globe', 'TRIMIȚI TURBINA DE ORIUNDE DIN ȚARĂ', 'green']] },
      { k: 'kin', t: A.n40 - .02, dur: 1.5, txt: 'DOAR 40 LEI', col: '#FFD21F', y: 204, size: 122, rot: -3 },   // sus, deasupra chip-ului

      // ---- IMG_2341: aceeași calitate, preț mai bun; la final, lista de prețuri
      { k: 'chip', t0: A.aceeasi - .05, t1: A.va4 - .3, y: 330, ph: [[A.aceeasi - .05, 'gem', 'ACEEAȘI CALITATE', 'blue'], [A.acum - .05, 'scissors', 'ACUM LA UN PREȚ MAI BUN', 'green']] },
      { k: 'chip', t0: A.va4 - .05, t1: A.in4 - .45, y: 330, ph: [[A.va4 - .05, 'handshake', 'VĂ MULȚUMIM!', 'blue']] },
      { k: 'eq', t0: A.in4 - .15, t1: SEND + .2, top: 130, ico: 'stethoscope', title: 'REȚETA TURBO DOCTOR', sub: 'PREȚURI NOI · GARANȚIE 24 LUNI',   // tema medicală: lista de prețuri ca „rețetă”
        lines: [[A.in4 + .1, 'VW 1.9 · 900–1000 LEI', 'y'], [A.in4 + .55, 'BMW N47·M47 · 1000–1300 LEI', 'y'], [A.in4 + 1.0, 'LOGAN 1.5 · 700 LEI', 'y']] },
    ],
    fx: [
      // hook: „AM TĂIAT” · mâna taie aerul · „PREȚURILE!” (impactul mare) · titlul tăiat
      { k: 'flash', t: B1 - .1, a: .4 }, { k: 'punch', t: B1, a: .08, sh: 16 }, { k: 'glitch', t: B1, d: .12 },
      { k: 'slash', t: HAND, x1: 1090, y1: 1134, x2: -20, y2: 1358, w: 20, d: .1, hold: .2, lin: 1 }, { k: 'punch', t: HAND + .05, a: .04, sh: 12 },   // vârful degetelor: (1075,1140) la 1.00 → (520,1250) la 1.067
      { k: 'flash', t: B2 - .11, a: .75 }, { k: 'punch', t: B2, a: .16, sh: 34 }, { k: 'glitch', t: B2, d: .18 }, { k: 'shock', t: B2 + .01, x: 540, y: TY, r: 760, n: 2, col: '#FFD21F', col2: '#FFFFFF' },
      { k: 'slash', t: TCUT - .07, x1: 1095, y1: TY - 108, x2: -15, y2: TY + 108, w: 17, d: .07, hold: .3 }, { k: 'punch', t: TCUT, a: .07, sh: 18 }, { k: 'flash', t: TCUT - .05, a: .3 },
      { k: 'glitch', t: HEND - .04, d: .12 },
      // schimbările de cadru
      { k: 'glitch', t: CLIP[2] - .04, d: .12 }, { k: 'glitch', t: CLIP[3] - .04, d: .12 }, { k: 'glitch', t: CLIP[4] - .04, d: .12 }, { k: 'glitch', t: CLIP[5] - .04, d: .12 },
      // mașinile tăiate și prețurile
      { k: 'punch', t: VW0 + .5, a: .05, sh: 12 }, { k: 'flash', t: A.n900 - .13, a: .35 }, { k: 'punch', t: A.n900 - .03, a: .09, sh: 18 },
      { k: 'punch', t: BM0 + .5, a: .05, sh: 12 }, { k: 'flash', t: A.n1000b - .13, a: .35 }, { k: 'punch', t: A.n1000b - .03, a: .09, sh: 18 },
      { k: 'punch', t: LG0 + .5, a: .05, sh: 12 }, { k: 'flash', t: A.n700 - .13, a: .4 }, { k: 'punch', t: A.n700 - .03, a: .11, sh: 22 },
      // restul: accente scurte
      { k: 'punch', t: A.n24a, a: .04 }, { k: 'punch', t: A.ieftina, a: .04 }, { k: 'punch', t: A.repede, a: .05 }, { k: 'punch', t: A.n40, a: .07, sh: 12 }, { k: 'punch', t: A.in4 + .1, a: .04 },
    ],
    sfx: [[HAND - .03, 'slash', .8], [HAND - .12, 'whoosh', .5], [HEND - .08, 'whoosh', .55]],
    bursts: [[B2 + .04, 540, TY, 5, 520, 1.4]],
  };
};
