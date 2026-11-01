// v2 – PROMO plătit pentru FLOTE (01.11.2026, varianta dinamică: pauzele și „regia” tăiate, 2:39): „Deții o flotă auto?” → turul Turbo Doctor: mecanică, laboratoare (injecție, turbo, DPF), motoare, contract
// Sursa (hook_src.mp4): 0 cadru AI „flotă” (dronă peste sute de dube albe aliniate, „ca la UMB”), peste „Deții o flotă auto?” · 2.5 IMG_2028 (la intrare, de la „Ei bine”)
// · 8.284 IMG_2030 (ușa) · 18.266 IMG_2034 (service, plăcile estompate) · 36.463 IMG_2035 + 61.613 IMG_2036 (laborator injecție, stand Bosch)
// · 80.235 IMG_2037 (quad turbo BMW) · 104.916 IMG_2038 (B-roll quad turbo, fără voce) · 113.0 IMG_2039 (DPF secționat) · 136.977 IMG_2052 + 162.11 IMG_2053 (motor pe stand)
// Cerut de Sabin: hook puternic cu multe mașini aliniate; mesajul „nu suntem doar un service, recondiționăm”; final = opis cu tot ce facem + mecanică generală + (0727) 345 459.
// Sunetul cadrului AI e în audio/hook_bed.wav (out/v2.json „beds”), muzica intră când apare el (music_in 2.5). Fiind reclamă: telefonul pe ecran când îl spune și pe opis.
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND, TOTAL }) => {
  const A = {
    ei0: aw(0, 'Ei'), turbo0: aw(0, 'Turbo'), partenerul: aw(0, 'partenerul'), reparatia0: aw(0, 'reparația'),
    haide: aw(1, 'Haide'), aratam: aw(1, 'arătăm'), inprimul: aw(1, 'În'), nu1: aw(1, 'nu'), un1: aw(1, 'un'),
    desigur: aw(2, 'Desigur'), aici: aw(2, 'aici'), demonteaza: aw(2, 'demontează'), monteaza: aw(2, 'montează'),
    inschimb3: aw(3, 'În'), magia: aw(3, 'magia'), fiecare3: aw(3, 'fiecare'), laboratorul3: aw(3, 'laboratorul'),
    hai4: aw(4, 'Hai'), injectoarele4: aw(4, 'injectoarele'), laborator4: aw(4, 'laborator'), sistemelor: aw(4, 'sistemelor'),
    o5: aw(5, 'O'), n1500: aw(5, '1.500'), inschimb5: aw(5, 'În'), recond5: aw(5, 'recondiționat'), n500: aw(5, '500'), iar5: aw(5, 'Iar'),
    aceeasi: aw(5, 'aceeași'), n12: aw(5, '12'), fara: aw(5, 'fără'),
    injectorul6: aw(6, 'Injectorul'), stand6: aw(6, 'stand'), adica: aw(6, 'Adică'), testat: aw(6, 'testat'), verificat: aw(6, 'verificat'),
    masina6: aw(6, 'mașina'), standul: aw(6, 'standul'),
    cazul: aw(7, 'În'), ganditi: aw(7, 'Gândiți-vă'), quad: aw(7, 'quad'),
    ar8: aw(8, 'ar'), n25000: aw(8, '25.000'), la9: aw(9, 'La'), n10000: aw(9, '10.000'), asta: aw(9, 'Asta'), acelasi9: aw(9, 'același'),
    garantie9: aw(9, 'garanție'), n24: aw(9, '24'), exact9: aw(9, 'exact'),
    sunt10: aw(10, 'Sunt'), probleme10: aw(10, 'probleme'), ei10: aw(10, 'Ei'), salvam: aw(10, 'salvăm'),
    daca11: aw(11, 'Dacă'), scapi: aw(11, 'scapi'), cateva: aw(11, 'câteva'), si11: aw(11, 'Și'), tot11: aw(11, 'tot'), nu11: aw(11, 'nu'),
    si12: aw(12, 'Și'), defectiuni: aw(12, 'defecțiuni'), distrugerea: aw(12, 'distrugerea'), turbo12: aw(12, 'Turbo'), un12: aw(12, 'un'),
    putem13: aw(13, 'Putem'), capital: aw(13, 'capital'), garantie13: aw(13, 'garanție'), si13: aw(13, 'și'), readucem: aw(13, 'readucem'),
    alaturi13: aw(13, 'alături'), turbine13: aw(13, 'turbine'), injectoare13: aw(13, 'injectoare'), pompe: aw(13, 'pompe'), dpfuri13: aw(13, 'DPF-uri'),
    la13: aw(13, 'la', 1), calitate: aw(13, 'calitate-preț'),
    pe14: aw(14, 'Pe'), intretinerea: aw(14, 'întreținerea'), distributii: aw(14, 'distribuții'), revizii: aw(14, 'revizii'), tot14: aw(14, 'tot'),
    totul: aw(15, 'Totul'), contract: aw(15, 'contract'), cele: aw(15, 'cele'), baza: aw(15, 'baza'),
    esti: aw(16, 'Ești'), suna: aw(16, 'Sună'), numarul: aw(16, 'numărul'), whatsapp: aw(16, 'WhatsApp'), hai16: aw(16, 'hai'),
  };
  // Varianta dinamică (cerută de Sabin doar pentru acest reel, 01.11.2026): pauzele tăiate (out/v2.json "cuts", "sil_local"), deci
  // începuturile de clip (timp-sursă) se mută în timpul final cu so(): un moment tăiat cade pe începutul segmentului păstrat următor.
  const SEGS = window.TL.segments.filter(s => s.kind === 'story');
  const so = t => { for (const s of SEGS) if (s.src_a - 1e-6 <= t && t <= s.src_b + 1e-6) return s.out_a + (t - s.src_a);
    for (const s of SEGS) if (s.src_a > t) return s.out_a; return SEND; };
  const CLIP = [0, 8.284, 18.266, 36.463, 61.613, 80.235, 104.916, 113.0, 136.977, 162.11].map(so);
  const CUT = 2.5;                       // cadrul AI → Sabin, chiar înainte de „Ei bine”
  const B1 = 1.31, B2 = 1.72;            // „Deții” · „flotă” (debutul real, din energia vocii)
  const N1 = A.nu1, N2 = A.un1 - .02;    // „nu suntem doar” · „un service”
  const BX = A.esti - .02;               // „Ești interesat?”
  // opisul de la final: [icon | null = titlu de secțiune, text]
  const RT = TEND + .55, RS = .26;
  const OPIS = [
    [null, 'RECONDIȚIONĂM ÎN LABORATOARELE NOASTRE'],
    ['fuel_pump', 'Injectoare și pompe de injecție'],
    ['dashing_away', 'Turbosuflante · garanție 24 luni'],
    ['leaf', 'DPF: curățare și recondiționare'],
    ['gear', 'Motoare: recondiționare capitală'],
    [null, 'ȘI TOATĂ MECANICA GENERALĂ'],
    ['oil_drum', 'Revizii periodice'],
    ['wrench', 'Kituri de distribuție'],
    ['nutbolt', 'Frâne, ambreiaj, suspensie'],
    ['stethoscope', 'Diagnoză gratuită'],
  ].map((r, i) => [RT + i * RS, r[0], r[1]]);
  const PH_AT = RT + OPIS.length * RS + .3;
  return {
    hook: null,
    stages: null,
    hideCap: [[0, CUT + .02], [N1 - .1, A.desigur - .08], [A.salvam - .1, A.daca11 - .06], [BX - .1, A.suna - .06]],
    tags: {
      0: { flota: 'y', turbo: 'c', doctor: 'c', partenerul: 'g', incredere: 'g', reparatia: 'g', profesionala: 'g' },
      1: { special: 'y', nu: 'r', doar: 'r', service: 'y' },
      2: { mecanica: 'c', demonteaza: 'y', monteaza: 'y' },
      3: { magia: 'y', laboratorul: 'g', dedicat: 'g', reparatii: 'g' },
      4: { injectoarele: 'c', laborator: 'g', dedicat: 'g', injectie: 'c' },
      5: { cutie: 'c', 1500: 'r', 2000: 'r', lei: 'y', reconditionat: 'g', 500: 'g', 800: 'g', garantia: 'g', aceeasi: 'g', 12: 'y', luni: 'y', kilometri: 'y' },
      6: { bosch: 'c', stand: 'c', testare: 'g', codare: 'g', testat: 'g', verificat: 'g', original: 'g' },
      7: { turbinelor: 'c', quad: 'y', turbo: 'y', bmw: 'c' },
      8: { 25000: 'r', lei: 'r', nou: 'r' },
      9: { 10000: 'g', lei: 'g', reduceri: 'g', substantiale: 'g', garantie: 'g', 24: 'y', luni: 'y' },
      10: { dpfuri: 'c', probleme: 'r', salvam: 'g' },
      11: { rapid: 'g', curatare: 'g', sute: 'y', tarziu: 'r', reconditionarea: 'g', profesionala: 'g', inlocuirea: 'r' },
      12: { defectiuni: 'r', catastrofale: 'r', distrugerea: 'r', motoarelor: 'r', partener: 'g', incredere: 'g' },
      13: { reconditiona: 'g', capital: 'g', motoarele: 'c', garantie: 'g', readucem: 'g', viata: 'g', turbine: 'c', injectoare: 'c', pompe: 'c', dpfuri: 'c', calitatepret: 'y' },
      14: { intretinerea: 'g', distributii: 'c', revizii: 'c', periodice: 'c' },
      15: { contract: 'y', bune: 'g', preturi: 'g', rulajelor: 'y' },
      16: { interesat: 'y', suna: 'g', telefon: 'y', whatsapp: 'g', detalii: 'g' },
    },
    items: [
      // ---------- HOOK (cadru AI: dronă peste flota de dube albe) ----------
      { k: 'chip', t0: .08, t1: CUT - .06, y: 300, ph: [[.08, 'automobile', 'PENTRU MANAGERII DE FLOTE', 'yellow']] },
      { k: 'boom', t: B1, dur: CUT - .04 - B1, txt: 'DEȚII O', y: 760, size: 150, col: '#FFFFFF', from: 3.0, sh: 18, ca: 22, bg: .8, glow: 'rgba(98,216,255,.55)' },
      { k: 'boom', t: B2, dur: CUT - .04 - B2, txt: 'FLOTĂ AUTO?', y: 985, size: 172, col: '#FFD21F', from: 3.6, sh: 30, ca: 30, riser: false, bg: 1 },

      // ---------- IMG_2028 (la intrare, cu cele trei firme pe perete) ----------
      { k: 'ring', t0: A.turbo0 - .05, t1: A.partenerul - .25, p: [248, 720], r: 195, col: '#62D8FF' },
      { k: 'chip', t0: A.ei0 + .05, t1: CLIP[1] - .2, y: 330, ph: [[A.ei0 + .05, 'stethoscope', 'LA TURBO DOCTOR', 'blue'],
        [A.partenerul - .05, 'handshake', 'PARTENERUL TĂU DE ÎNCREDERE', 'green'], [A.reparatia0 - .05, 'hammer_and_wrench', 'REPARAȚIA PROFESIONALĂ A FLOTEI', 'yellow']] },

      // ---------- IMG_2030 (ușa): „Haide cu mine…” ----------
      { k: 'chip', t0: A.haide - .05, t1: CLIP[2] - .25, y: 330, ph: [[A.haide - .05, 'pointing_right', 'HAI CU MINE!', 'yellow'],
        [A.aratam - .05, 'eyes', 'SĂ-ȚI ARĂTĂM CE FACEM SPECIAL', 'blue']] },

      // ---------- turul: bara de sus cu secția curentă ----------
      { k: 'band', t0: CLIP[2] + .15, t1: SEND - .1, y: 222, w: 980, h: 76, kicker: 'TUR PRIN CLINICĂ',
        ph: [[CLIP[2] + .15, 'ZONA DE MECANICĂ', 'SECȚIA 1/5'], [CLIP[3] + .05, 'LABORATOR INJECȚIE', 'SECȚIA 2/5'], [CLIP[5] + .05, 'LABORATOR TURBO', 'SECȚIA 3/5'],
          [CLIP[7] + .05, 'LABORATOR DPF', 'SECȚIA 4/5'], [CLIP[8] + .05, 'MOTOARE', 'SECȚIA 5/5'], [A.totul - .1, 'CONTRACT DE FLOTĂ', 'TURBO DOCTOR']] },

      // ---------- IMG_2034 (service): NU SUNTEM DOAR UN SERVICE ----------
      { k: 'boom', t: N1, dur: A.desigur - .1 - N1, txt: 'NU SUNTEM DOAR', y: 400, size: 118, col: '#FFFFFF', from: 2.8, sh: 14, ca: 18, bg: .7, glow: 'rgba(98,216,255,.5)' },
      { k: 'boom', t: N2, dur: A.desigur - .1 - N2, txt: 'UN SERVICE', y: 585, size: 185, col: '#FFD21F', from: 3.6, sh: 30, ca: 30, riser: false, bg: 1 },
      { k: 'chip', t0: A.desigur - .05, t1: A.inschimb3 - .25, y: 330, ph: [[A.desigur - .05, 'wrench', 'AICI: ZONA DE MECANICĂ', 'blue'],
        [A.demonteaza - .05, 'wrench', 'PIESELE SE DEMONTEAZĂ...', 'blue'], [A.monteaza - .05, 'nutbolt', '...ȘI SE MONTEAZĂ PE MAȘINĂ', 'blue']] },
      { k: 'kin', t: A.magia - .02, dur: 1.5, txt: 'MAGIA', col: '#FFD21F', y: 1185, size: 190, rot: -4 },
      { k: 'chip', t0: A.inschimb3 - .05, t1: CLIP[3] - .2, y: 330, ph: [[A.inschimb3 - .05, 'sparkles', 'ÎN SCHIMB, MAGIA ÎNCEPE...', 'yellow'],
        [A.laboratorul3 - .05, 'test_tube', '...ÎN LABORATORUL DEDICAT', 'green']] },

      // ---------- IMG_2035 (laborator injecție): cutia nouă vs recondiționat ----------
      { k: 'chip', t0: A.hai4 - .05, t1: A.o5 - .25, y: 330, ph: [[A.hai4 - .05, 'fuel_pump', 'EXEMPLU: INJECTOARELE', 'blue'],
        [A.laborator4 - .05, 'test_tube', 'LABORATOR PENTRU INJECȚIE', 'green']] },
      { k: 'chip', t0: A.o5 - .05, t1: A.iar5 - .25, y: 330, ph: [[A.o5 - .05, 'package', 'INJECTOR NOU, ÎN CUTIE', 'red'],
        [A.inschimb5 - .05, 'test_tube', 'INJECTOR RECONDIȚIONAT', 'green']] },
      { k: 'kin', t: A.n1500 - .02, dur: A.inschimb5 - .25 - A.n1500, txt: '1.500–2.000 LEI', col: '#FF4B4B', y: 1185, size: 104, rot: -4 },
      { k: 'kin', t: A.n500 - .02, dur: A.iar5 - .2 - A.n500, txt: '500–800 LEI', col: '#4ADE80', y: 1185, size: 140, rot: -4 },
      { k: 'chip', t0: A.iar5 - .05, t1: CLIP[4] - .2, y: 330, ph: [[A.iar5 - .05, 'shield', 'GARANȚIA E ACEEAȘI', 'green'],
        [A.fara - .05, 'counter', 'FĂRĂ LIMITĂ DE KILOMETRI', 'yellow']] },
      { k: 'kin', t: A.n12 - .02, dur: CLIP[4] - .25 - A.n12, txt: '12 LUNI GARANȚIE', col: '#FFD21F', y: 1185, size: 100, rot: -3 },

      // ---------- IMG_2036 (standul Bosch) ----------
      { k: 'chip', t0: A.injectorul6 - .05, t1: A.stand6 - .3, y: 330, ph: [[A.injectorul6 - .05, 'fuel_pump', 'INJECTOR BOSCH', 'blue']] },
      { k: 'scan', t0: A.stand6 - .05, t1: A.adica - .2, box: [690, 740, 390, 720], lab: 'STAND BOSCH...', lab2: 'TESTARE ȘI CODARE', at2: A.stand6 + .9, labBelow: false },
      { k: 'pipe', t0: A.adica - .1, t1: A.standul - .3, top: 262, ico: 'microscope', title: 'ÎNAINTE SĂ AJUNGĂ PE MAȘINA TA',
        steps: [[A.testat - .05, 'microscope', 'TESTAT'], [A.verificat - .05, 'check_mark_button', 'VERIFICAT'], [A.masina6 - .05, 'automobile', 'MONTAT PE<br>MAȘINA TA']] },
      { k: 'chip', t0: A.standul - .05, t1: CLIP[5] - .2, y: 330, ph: [[A.standul - .05, 'check_mark_button', 'PE STANDUL ORIGINAL AL PRODUCĂTORULUI', 'green']] },

      // ---------- IMG_2037 (laborator turbo): quad turbo BMW ----------
      { k: 'chip', t0: A.cazul - .05, t1: A.n25000 - .55, y: 330, ph: [[A.cazul - .05, 'dashing_away', 'TURBINELE: EXACT LA FEL', 'blue'],
        [A.quad - .05, 'gear', 'ACEST QUAD TURBO DE BMW', 'yellow'], [A.ar8 - .05, 'cross_mark', 'LUAT NOU AR FI COSTAT...', 'red']] },
      { k: 'cmp', t0: A.n25000 - .45, t1: A.asta - .3, top: 262, w: 780, big: true, ico: 'gear', title: 'QUAD TURBO BMW · COST', aCls: 'bad', bCls: 'ok', dimA: true,
        a: [A.n25000 - .05, 'cross_mark', 'LUAT NOU', 'PESTE 25.000 LEI'], b: [A.n10000 - .05, 'check_mark_button', 'LA TURBO DOCTOR', 'SUB 10.000 LEI'] },
      { k: 'chip', t0: A.asta - .05, t1: CLIP[6] - .2, y: 330, ph: [[A.asta - .05, 'chart_down', 'REDUCERI SUBSTANȚIALE', 'green'],
        [A.acelasi9 - .05, 'shield', 'ȘI GARANȚIE CA LA NOU', 'green']] },
      { k: 'stamp', t: A.n24 - .03, t1: CLIP[6] - .25, y: 520, txt: '24 LUNI GARANȚIE', col: 'green', s: .82, rot: -7 },

      // ---------- IMG_2038 (B-roll quad turbo, fără voce): doar 1,8 s, intrarea pe roata compresorului + ștampila ----------
      { k: 'stamp', t: CLIP[6] + .3, t1: CLIP[7] - .06, y: 560, txt: 'RECONDIȚIONAT', col: 'green', s: 1.0, rot: -8 },

      // ---------- IMG_2039 (laborator DPF) ----------
      { k: 'chip', t0: A.sunt10 - .05, t1: A.salvam - .3, y: 300, ph: [[A.sunt10 - .05, 'leaf', 'AI AUZIT DE DPF-URI?', 'blue'],
        [A.probleme10 - .05, 'warning', 'ȘI DE CÂTE PROBLEME FAC', 'red'], [A.ei10 - .05, 'stethoscope', 'LA TURBO DOCTOR...', 'blue']] },
      { k: 'boom', t: A.salvam - .02, dur: A.daca11 - .1 - A.salvam, txt: 'LE SALVĂM!', y: 900, size: 170, col: '#4ADE80', from: 3.2, sh: 22, ca: 24, riser: false, bg: .9, glow: 'rgba(74,222,128,.55)' },
      { k: 'chip', t0: A.daca11 - .05, t1: A.si11 - .25, y: 300, ph: [[A.daca11 - .05, 'stopwatch', 'AJUNGI LA TIMP?', 'green'], [A.scapi - .05, 'broom', 'SCAPI DOAR CU O CURĂȚARE', 'green']] },
      { k: 'kin', t: A.cateva - .02, dur: A.si11 - .25 - A.cateva, txt: 'CÂTEVA SUTE DE LEI', col: '#FFD21F', y: 900, size: 104, rot: -4 },
      { k: 'chip', t0: A.si11 - .05, t1: CLIP[8] - .2, y: 300, ph: [[A.si11 - .05, 'hourglass', 'AJUNGI PREA TÂRZIU?', 'red'],
        [A.tot11 - .05, 'hammer_and_wrench', 'RECONDIȚIONARE PROFESIONALĂ', 'green'], [A.nu11 - .05, 'cross_mark', 'NU ÎNLOCUIRE CU UNUL NOU', 'yellow']] },

      // ---------- IMG_2052 (motorul pe stand) ----------
      { k: 'stamp', t: A.defectiuni - .03, t1: A.turbo12 - .2, y: 430, txt: 'DEFECȚIUNI CATASTROFALE', col: 'red', s: .74, rot: -6 },
      { k: 'chip', t0: A.turbo12 - .05, t1: A.putem13 - .25, y: 330, ph: [[A.turbo12 - .05, 'stethoscope', 'TURBO DOCTOR RĂMÂNE ACOLO', 'blue'],
        [A.un12 - .05, 'handshake', 'UN PARTENER DE ÎNCREDERE', 'green']] },
      { k: 'scan', t0: A.putem13 - .05, t1: A.si13 - .2, box: [255, 1000, 420, 560], lab: 'MOTOR PE STAND...', lab2: 'RECONDIȚIONARE CAPITALĂ', at2: A.capital - .02, labBelow: false },
      { k: 'chip', t0: A.putem13 - .05, t1: A.si13 - .25, y: 330, ph: [[A.putem13 - .05, 'gear', 'MOTOARE RECONDIȚIONATE', 'blue'], [A.garantie13 - .05, 'shield', 'CU GARANȚIE', 'green']] },
      { k: 'ecg', t0: A.si13 - .1, t1: A.alaturi13 - .25, top: 262, label: 'PULS MOTOR', ico: 'stethoscope', states: [[A.si13 - .1, 'flat', 'OPRIT'], [A.readucem, 'ok', 'ADUS LA VIAȚĂ']] },
      { k: 'pipe', t0: A.alaturi13 - .1, t1: A.la13 - .25, top: 262, ico: 'hammer_and_wrench', title: 'ALĂTURI DE MOTOR, LA VIAȚĂ:',
        steps: [[A.turbine13 - .05, 'dashing_away', 'TURBINE'], [A.injectoare13 - .05, 'fuel_pump', 'INJECTOARE'], [A.pompe - .05, 'gear', 'POMPE'], [A.dpfuri13 - .05, 'leaf', 'DPF-URI']] },
      { k: 'stamp', t: A.calitate - .03, t1: CLIP[9] - .25, y: 430, txt: 'CEL MAI BUN RAPORT CALITATE-PREȚ', col: 'green', s: .62, rot: -5 },

      // ---------- IMG_2053: întreținere + contract + telefonul ----------
      { k: 'chip', t0: A.pe14 - .05, t1: A.contract - .4, y: 330, ph: [[A.pe14 - .05, 'handshake', 'ALĂTURI DE VOI ȘI LA ÎNTREȚINERE', 'blue'],
        [A.distributii - .05, 'wrench', 'DISTRIBUȚII', 'yellow'], [A.revizii - .05, 'oil_drum', 'REVIZII PERIODICE', 'yellow'], [A.tot14 - .05, 'check_mark_button', 'ȘI TOT AȘA', 'blue'],
        [A.totul - .05, 'handshake', 'TOTUL SE POATE FACE...', 'yellow']] },
      { k: 'eq', t0: A.contract - .35, t1: BX - .25, top: 236, ico: 'handshake', title: 'CONTRACT DE FLOTĂ', sub: 'TURBO DOCTOR',
        lines: [[A.contract - .12, '...ÎNTR-UN CONTRACT', 'w'], [A.cele - .05, 'CELE MAI BUNE PREȚURI', 'big g'], [A.baza - .05, 'PE BAZA RULAJULUI', 'y']] },
      { k: 'boom', t: BX, dur: A.suna - .12 - BX, txt: 'EȘTI INTERESAT?', y: 420, size: 128, col: '#FFD21F', from: 3.2, sh: 22, ca: 24, bg: .9 },
      { k: 'eq', t0: A.suna - .1, t1: SEND + .2, top: 236, ico: 'phone', title: 'SUNĂ SAU SCRIE-NE', sub: 'TELEFON · WHATSAPP',
        lines: [[A.numarul - .05, '0727 345 459', 'big y'], [A.whatsapp - .05, 'ȘI PE WHATSAPP', 'g']] },

      // ---------- FINAL: opisul cu tot ce facem + telefonul + locațiile, pe același ecran ----------
      { k: 'opis', t0: TEND + .22, t1: TOTAL + 1, top: 120, sub: 'CONTRACTE PENTRU FLOTE AUTO', subIco: 'handshake', kicker: 'OPIS · CE FACEM PENTRU FLOTA TA',
        head: 'NU DOAR SCHIMBĂM. RECONDIȚIONĂM.', ico: 'stethoscope', rows: OPIS, phoneLab: 'FLOTE · TELEFON ȘI WHATSAPP', phone: '0727 345 459', phoneAt: PH_AT,
        site: 'turbodoctor.ro', cities: ['GALAȚI', 'BUCUREȘTI', 'IAȘI', 'PIATRA NEAMȚ'], citiesAt: PH_AT + .5 },
    ],
    endCard: false,
    fx: [
      // hook
      { k: 'flash', t: B1 - .11, a: .6 }, { k: 'punch', t: B1, a: .12, sh: 24 }, { k: 'glitch', t: B1, d: .14 }, { k: 'shock', t: B1 + .01, x: 540, y: 760, r: 640, n: 1, col: '#FFFFFF' },
      { k: 'flash', t: B2 - .11, a: .75 }, { k: 'punch', t: B2, a: .16, sh: 34 }, { k: 'glitch', t: B2, d: .2 }, { k: 'shock', t: B2 + .01, x: 540, y: 985, r: 760, n: 2, col: '#FFD21F', col2: '#FFFFFF' },
      { k: 'glitch', t: CUT - .03, d: .14 },
      // NU SUNTEM DOAR UN SERVICE
      { k: 'flash', t: N1 - .1, a: .4 }, { k: 'punch', t: N1, a: .08, sh: 14 }, { k: 'shock', t: N1 + .01, x: 540, y: 400, r: 520, n: 1, col: '#FFFFFF' },
      { k: 'flash', t: N2 - .11, a: .7 }, { k: 'punch', t: N2, a: .16, sh: 32 }, { k: 'glitch', t: N2, d: .2 }, { k: 'shock', t: N2 + .01, x: 540, y: 585, r: 720, n: 2, col: '#FFD21F', col2: '#FFFFFF' },
      // prețuri, garanții
      { k: 'punch', t: A.magia, a: .05, sh: 8 }, { k: 'punch', t: A.n1500, a: .05, sh: 10 }, { k: 'punch', t: A.n500, a: .06, sh: 10 }, { k: 'punch', t: A.n12, a: .05, sh: 8 },
      { k: 'punch', t: A.n25000, a: .05, sh: 10 }, { k: 'punch', t: A.n10000, a: .06, sh: 12 }, { k: 'punch', t: A.n24, a: .05, sh: 8 },
      // LE SALVĂM
      { k: 'flash', t: A.salvam - .13, a: .55 }, { k: 'punch', t: A.salvam - .02, a: .12, sh: 26 }, { k: 'glitch', t: A.salvam - .02, d: .16 },
      { k: 'shock', t: A.salvam, x: 540, y: 900, r: 640, n: 2, col: '#4ADE80', col2: '#FFFFFF' },
      { k: 'punch', t: A.cateva, a: .05, sh: 8 }, { k: 'punch', t: A.defectiuni, a: .07, sh: 14 }, { k: 'punch', t: A.capital, a: .05, sh: 8 },
      // EȘTI INTERESAT? + telefonul
      { k: 'flash', t: BX - .11, a: .5 }, { k: 'punch', t: BX, a: .1, sh: 20 }, { k: 'glitch', t: BX, d: .14 }, { k: 'shock', t: BX + .01, x: 540, y: 420, r: 600, n: 1, col: '#FFD21F' },
      { k: 'punch', t: A.numarul, a: .06, sh: 12 },
      // schimbările de cadru
      ...CLIP.slice(1).map(c => ({ k: 'glitch', t: c - .04, d: .12 })),
    ],
    sfx: [[.02, 'whoosh', .55], [CUT - .12, 'whoosh', .6], ...CLIP.slice(1).map(c => [c - .1, 'whoosh', .45])],
    bursts: [[B2 + .04, 540, 985, 8, 520, .4],[N2 + .04, 540, 585, 8, 480, 1.4], [A.salvam + .02, 540, 900, 7, 440, 1.2], [BX + .04, 540, 420, 6, 380, 1.0]],
  };
};
