// v2 – Reel „Ai motorul 2.0 Euro 6 din gama VAG? Stai până la final!” (IMG_2490 + IMG_2491, lipite în ordinea filmării, fără tăieturi, ritm natural)
// Cerut de Sabin pe 14.11.2026: problemele comune ale motoarelor 2.0 · 150 CP · Euro 6 din gama VAG (Passat, Golf, Skoda, Audi A4, A3…),
// interesant pentru posesor, cu animații și explicații și hook puternic cu textul dat de el: „Ai motorul 2.0 Euro 6 din gama VAG, stai până la final”.
// Filmare doar cu motorul (fără față, fără plăcuțe de înmatriculare) -> schemele și cardurile mari stau sus.
// Scheme noi: `vagEgrDpf` (tratarea gazelor: DPF + bucla EGR cu răcitor) și `waterCooler` (răcitorul de aer cu antigel care se crapă).
// Fără CTA pe imagine (25.10): „diagnoza gratuită” o spune el, pe ecran apare doar ce spune. Fără accente roșu/verde pe tot cadrul (neconfirmate).
// Aprobat de Sabin și programat pe 15.11.2026 (TikTok, Facebook, YouTube 18:00 · Instagram 19:00; Facebook ca postare video cu titlu, fiind peste 90 s).
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND }) => {
  const A = {
    audi: aw(0, 'Audi'), aceasta: aw(0, 'Această'), o0: aw(0, 'o'), gama: aw(0, 'gama'), vag: aw(0, 'VAG'), n20b: aw(0, '2.0', 1),
    euro1: aw(1, 'Euro'), a1: aw(1, 'A'), noi1: aw(1, 'noi'), probleme1: aw(1, 'probleme'), egr1: aw(1, 'EGR'),
    ce2: aw(2, 'Ce'), ele2: aw(2, 'ele'), zona2: aw(2, 'zona'), uneori2: aw(2, 'Uneori'), erori2: aw(2, 'erori'), dpf2: aw(2, 'DPF'), cauzate2: aw(2, 'cauzate'),
    si2: aw(2, 'și'), racitorul2: aw(2, 'răcitorul'), uneori2b: aw(2, 'Uneori', 1), serioase2: aw(2, 'serioase'), motoare2: aw(2, 'motoare'), distruse2: aw(2, 'distruse'), ignoram2: aw(2, 'ignorăm'),
    anumite3: aw(3, 'anumite'), recirculare3: aw(3, 'recirculare'), gazelor3e: ew(3, 'gazelor'),
    la4: aw(4, 'La'), sute4: aw(4, 'sute'), si4: aw(4, 'și'), problema4: aw(4, 'problema'), water4: aw(4, 'watercoolerelor'), crapa4: aw(4, 'crapă'), si4b: aw(4, 'și', 1),
    consume4: aw(4, 'consume'), pana4: aw(4, 'până'), evacuare4: aw(4, 'evacuare'),
    si5: aw(5, 'Și'), acest5: aw(5, 'acest'), atunci5: aw(5, 'atunci'), mana5: aw(5, 'mâna'), nu5: aw(5, 'nu'), sistemul5: aw(5, 'sistemul'),
    pe6: aw(6, 'pe'), va6: aw(6, 'va'), piese6: aw(6, 'piese'), pomana6: aw(6, 'pomană'), fara6: aw(6, 'fără'), desi6: aw(6, 'deși'), alta6: aw(6, 'altă'),
    de7: aw(7, 'De'), dpfuri7: aw(7, 'DPF-uri'), deoarece7: aw(7, 'deoarece'), eroare7: aw(7, 'eroare'), desi7: aw(7, 'deși'), racitorul7: aw(7, 'răcitorul'),
    de8: aw(8, 'De'), masini8: aw(8, 'mașini'), recond8: aw(8, 'recondiționate'), din8: aw(8, 'din'), exista8: aw(8, 'exista'), si8: aw(8, 'și'), din8b: aw(8, 'din', 1), spart8: aw(8, 'spart'),
    aveti9: aw(9, 'Aveți'), grija9: aw(9, 'grijă'), apelati9: aw(9, 'apelați'), service9: aw(9, 'service'), care9: aw(9, 'care'),
    complicate: aw(10, 'complicate'), in10: aw(10, 'în'), nu10: aw(10, 'nu'), tineti: aw(10, 'Țineți'), diagnoza10: aw(10, 'diagnoză'), atunci10: aw(10, 'atunci'),
    determinam: aw(10, 'determinăm'), cu10b: aw(10, 'cu', 1), la10b: aw(10, 'la', 1), pret: aw(10, 'preț'),
  };
  const CLIP = [0, 39.6];
  // HOOK: titlu boom în patru trepte, cu textul cerut de Sabin; impactul mare pe „2.0 EURO 6” (pe „Audi, 2.0”), ultimul rând = „STAI PÂNĂ LA FINAL!”.
  // Momentele sunt începuturile de cuvânt din anvelopa vocii (Audi .82 · 2.0 1.52 · 150 2.54); primul rând e pe ecran din primele cadre.
  const B1 = .12, B2 = .80, B3 = 1.50, B4 = 2.52, HB = 5.25;
  return {
    hook: { tag: 'ANALIZĂ TEHNICĂ · 2.0 · 150 CP · EURO 6', end: HB },
    hideCap: [[0, HB - .05]],
    stages: [[HB + .45, 'PACIENTUL'], [A.ce2 - .1, 'PROBLEMELE'], [A.si5 - .1, 'GREȘELILE'], [A.aveti9 - .1, 'SOLUȚIA']],
    tags: {
      0: { audi: 'c', 20: 'y', 150: 'y', gama: 'c', vag: 'c' },
      1: { euro: 'y', 6: 'y', probleme: 'r', egr: 'c' },
      2: { probleme: 'r', comune: 'r', tratarea: 'c', gazelor: 'c', esapament: 'c', erori: 'r', eficienta: 'r', dpf: 'c', egr: 'c', racitorul: 'c', serioase: 'r', motoare: 'r', distruse: 'r', ignoram: 'r' },
      3: { recirculare: 'c', gazelor: 'c' },
      4: { turbo: 'g', doctor: 'g', sute: 'y', watercoolerelor: 'c', crapa: 'r', consume: 'r', antigel: 'r', serioase: 'r', evacuare: 'c' },
      5: { motor: 'c', mana: 'r', intelege: 'r', tratarea: 'c', gazelor: 'c', esapament: 'c' },
      6: { euro: 'y', 6: 'y', piese: 'c', pomana: 'r', fara: 'r', sens: 'r', alta: 'y', parte: 'y' },
      7: { dpfuri: 'c', schimbate: 'r', eroare: 'r', eficienta: 'r', racitorul: 'c', gaze: 'c' },
      8: { reconditionate: 'r', antigel: 'r', antigelul: 'r', watercoolerul: 'c', spart: 'r' },
      9: { grija: 'y', service: 'g', specializat: 'g', intelege: 'g' },
      10: { complicate: 'c', serioase: 'r', diagnoza: 'g', gratuita: 'g', pret: 'y' },
    },
    items: [
      // ---- hook: boom în patru trepte
      { k: 'boom', t: B1, dur: HB - B1, txt: 'AI MOTORUL', y: 520, size: 138, col: '#FFFFFF', from: 2.4, sh: 12, ca: 14, riser: false, bg: .55, glow: 'rgba(98,216,255,.5)' },
      { k: 'boom', t: B2, dur: HB - B2, txt: '2.0 EURO 6', y: 748, size: 224, col: '#FFD21F', from: 3.8, sh: 24, ca: 30, bg: 1 },
      { k: 'boom', t: B3, dur: HB - B3, txt: 'DIN GAMA VAG?', y: 976, size: 150, col: '#FFFFFF', from: 2.6, sh: 14, ca: 18, riser: false, bg: .7, glow: 'rgba(98,216,255,.55)' },
      { k: 'boom', t: B4, dur: HB - B4, txt: 'STAI PÂNĂ LA FINAL!', y: 1222, size: 126, col: '#FF3B30', from: 2.8, sh: 16, ca: 20, riser: false, bg: .8, glow: 'rgba(255,75,75,.6)' },
      // ---- „o găsim pe toată gama VAG”: modelele (din mesajul lui Sabin)
      { k: 'list', t0: HB + .05, t1: A.euro1 - .3, top: 268, ico: 'automobile', title: 'O GĂSEȘTI PE TOATĂ GAMA VAG',
        rows: [[A.o0 + .02, 'VW PASSAT · VW GOLF'], [A.gama - .1, 'SKODA'], [A.vag - .02, 'AUDI A4 · AUDI A3 ȘI TOT AȘA']] },
      { k: 'kin', t: A.n20b - .08, dur: 1.5, txt: '2.0 · 150 CP', col: '#FFD21F', y: 1090, size: 170, rot: -4 },
      { k: 'kin', t: A.euro1, dur: 1.1, txt: 'EURO 6', col: '#62D8FF', y: 1090, size: 190, rot: -4 },
      // ---- fișa pacientului
      { k: 'file', t0: A.a1 - .1, t1: A.ce2 - .3, top: 268, no: '2490', ecg: 'crit',
        rows: [[A.a1 - .05, 'PACIENT', 'AUDI · 2.0 · 150 CP', 'c', 'automobile'], [A.noi1, 'NORMĂ', 'EURO 6', 'y', 'leaf'], [A.probleme1 - .02, 'SIMPTOME', 'PROBLEME LEGATE DE EGR', 'r', 'warning']] },
      // ---- problemele comune: tratarea gazelor de eșapament (schemă sus)
      { k: 'chip', t0: A.ce2 - .05, t1: A.ele2 - .35, y: 330, ph: [[A.ce2 - .05, 'exclamation', 'CE TREBUIE SĂ ȘTII', 'yellow']] },
      { k: 'schem', t0: A.ele2 - .1, t1: A.gazelor3e + .2, top: 268, h: 360, type: 'vagEgrDpf', title: 'SCHEMĂ · TRATAREA GAZELOR', sub: '2.0 · EURO 6',
        stepNames: ['SISTEMUL', 'EROAREA', 'CAUZA 1', 'CAUZA 2', 'RISCUL', 'ATENȚIE'],
        steps: [[A.ele2 - .1, 'Probleme comune pe zona de tratare a gazelor', '', 'ok'], [A.erori2 - .05, 'Erori de eficiență pe DPF', 'r', 'dpfErr'],
          [A.cauzate2 - .05, 'Cauzate de EGR...', 'y', 'egr'], [A.si2 - .03, '...și de răcitorul de EGR', 'y', 'cooler'],
          [A.motoare2 - .05, 'Probleme serioase, chiar motoare distruse', 'r', 'engine'], [A.ignoram2 - .05, 'Dacă ignorăm problemele de pe recircularea gazelor', 'y', 'ignore']],
        sfx: [[A.cauzate2, 'lock', .45], [A.racitorul2, 'lock', .5], [A.distruse2 - .02, 'impact', .6]] },
      { k: 'kin', t: A.distruse2 - .04, dur: 1.5, txt: 'MOTOARE DISTRUSE', col: '#FF3B30', y: 1090, size: 124, rot: -4 },
      // ---- clipul 2: sute de motorizări, watercoolerul
      { k: 'chip', t0: A.la4 - .02, t1: A.problema4 - .3, y: 330, ph: [[A.la4 - .02, 'stethoscope', 'LA TURBO DOCTOR', 'blue'], [A.sute4 - .05, 'automobile', 'SUTE DE ASTFEL DE MOTORIZĂRI', 'yellow'],
        [A.si4 - .02, 'check_mark_button', 'LE ȘTIM PROBLEMELE', 'green']] },
      { k: 'kin', t: A.sute4 - .02, dur: 1.5, txt: 'SUTE!', col: '#FFD21F', y: 1090, size: 230, rot: -4 },
      { k: 'schem', t0: A.problema4 - .1, t1: A.pana4 - .1, top: 268, h: 360, type: 'waterCooler', title: 'SCHEMĂ · WATERCOOLER', sub: 'RĂCIREA AERULUI', P: { fall: .85 },
        stepNames: ['CE FACE', 'DEFECTUL', 'EFECTUL'],
        steps: [[A.problema4 - .1, 'Watercoolerul: răcește aerul de la turbo cu antigel', '', 'ok'], [A.crapa4 - .05, 'Se crapă...', 'r', 'crack'], [A.si4b + .05, '...și motorul începe să consume antigel', 'r', 'consume']],
        sfx: [[A.crapa4, 'impact', .55]] },
      { k: 'chip', t0: A.pana4 - .02, t1: A.si5 - .25, y: 330, ph: [[A.pana4 - .02, 'warning', 'PÂNĂ LA PROBLEME SERIOASE PE EVACUARE', 'red']] },
      // ---- greșelile: pe mâna cui ajunge
      { k: 'chip', t0: A.si5 - .02, t1: A.pe6 - .3, y: 330, ph: [[A.si5 - .02, 'exclamation', 'CE TREBUIE SĂ ȘTII', 'yellow'], [A.atunci5 - .05, 'thinking_face', 'PE MÂNA CUI AJUNGE?', 'red'],
        [A.nu5 - .05, 'cross_mark', 'NU ÎNȚELEGE TRATAREA GAZELOR', 'red']] },
      { k: 'chip', t0: A.pe6 - .02, t1: A.de7 - .25, y: 330, ph: [[A.pe6 - .02, 'wrench', 'PE MOTORIZĂRILE EURO 6...', 'blue'], [A.va6 - .05, 'money_with_wings', 'SCHIMBĂ MULTE PIESE DE POMANĂ', 'red'],
        [A.desi6 - .05, 'magnifying_glass_tilted_left', 'PROBLEMA E ÎN ALTĂ PARTE', 'yellow']] },
      { k: 'kin', t: A.pomana6 - .16, dur: 1.5, txt: 'DE POMANĂ!', col: '#FF3B30', y: 1090, size: 190, rot: -4 },
      { k: 'stk', t0: A.pomana6 - .1, t1: A.desi6 - .1, ico: 'money_with_wings', x: 905, y: 930, size: 150 },
      // ---- DPF-uri schimbate degeaba: problema era pe răcitorul de gaze
      { k: 'schem', t0: A.de7 + .25, t1: A.de8 - .2, top: 268, h: 360, type: 'vagEgrDpf', title: 'SCHEMĂ · GREȘEALA CLASICĂ', sub: 'DPF SCHIMBAT',
        stepNames: ['GREȘEALA', 'MOTIVUL', 'CAUZA REALĂ'],
        steps: [[A.de7 + .25, 'DPF-uri schimbate la aceste motorizări', 'y', 'swap'], [A.deoarece7 - .05, 'Deoarece aveau eroare pe eficiență', 'r', 'swapErr'],
          [A.desi7 - .05, 'Deși problema era pe răcitorul de gaze', 'y', 'real']],
        sfx: [[A.dpfuri7 + .35, 'stamp', .5], [A.racitorul7, 'lock', .55]] },
      // ---- motoare recondiționate degeaba: antigelul venea din watercoolerul spart
      { k: 'schem', t0: A.masini8 - .1, t1: A.aveti9 - .2, top: 268, h: 360, type: 'waterCooler', title: 'SCHEMĂ · DE UNDE VINE ANTIGELUL', sub: 'WATERCOOLER',
        stepNames: ['GREȘEALA', 'MOTIVUL', 'ÎNTREBAREA', 'CAUZA REALĂ'],
        steps: [[A.masini8 - .1, 'Mașini sau motoare care au fost recondiționate', 'y', 'recon'], [A.din8 - .05, 'Pentru că exista antigel prin diferite locuri', 'y', 'where'],
          [A.si8 - .05, 'Și antigelul provenea...', '', 'trace'], [A.din8b - .1, '...din watercoolerul spart', 'r', 'source']],
        sfx: [[A.recond8, 'stamp', .5], [A.din8b - .05, 'impact', .6]] },
      { k: 'kin', t: A.spart8 - .04, dur: .8, txt: 'SPART!', col: '#FF3B30', y: 1090, size: 220, rot: -4 },
      // ---- soluția
      { k: 'list', t0: A.aveti9 - .05, t1: A.complicate - .25, top: 268, ico: 'shield', title: 'CA SĂ NU AI PROBLEME SERIOASE',
        rows: [[A.grija9 - .3, 'MARE GRIJĂ UNDE MERGI'], [A.service9 - .1, 'SERVICE SPECIALIZAT'], [A.care9 - .02, 'CARE ÎNȚELEGE ACESTE SISTEME']] },
      { k: 'chip', t0: A.complicate - .05, t1: A.tineti - .25, y: 330, ph: [[A.complicate - .05, 'gear', 'SISTEME COMPLICATE, ÎNTR-ADEVĂR', 'blue'], [A.in10 - .05, 'shield', 'CA SĂ NU AI PROBLEME SERIOASE', 'green']] },
      { k: 'chip', t0: A.tineti - .02, t1: A.determinam - .35, y: 330, ph: [[A.tineti - .02, 'stethoscope', 'TOTUL ÎNCEPE CU O DIAGNOZĂ GRATUITĂ', 'green']] },
      { k: 'kin', t: A.diagnoza10 - .02, dur: 1.4, txt: 'DIAGNOZĂ GRATUITĂ', col: '#FFD21F', y: 1090, size: 108, rot: -4 },
      { k: 'list', t0: A.determinam - .25, t1: SEND - .2, top: 268, ico: 'stethoscope', title: 'LA DIAGNOZA GRATUITĂ AFLĂM',
        rows: [[A.determinam + .3, 'CE PROBLEMĂ ARE MAȘINA TA'], [A.cu10b - .05, 'CU CE TE PUTEM AJUTA'], [A.la10b - .1, 'ȘI LA CE PREȚ']] },
      // ---- Rețeta (răsplata pentru „stai până la final”)
      { k: 'tip', t0: SEND + .1, t1: TEND - .15, top: 470, title: 'REȚETA TURBO DOCTOR', sub: 'SFAT DE INGINER · 2.0 EURO 6 VAG', ico: 'stethoscope',
        rows: [[SEND + .35, 'warning', 'Eroare de eficiență pe DPF? Verifică întâi EGR-ul și răcitorul de gaze'],
          [SEND + 1.45, 'droplet', 'Consumă antigel? Poate fi watercoolerul spart, nu motorul'],
          [SEND + 2.55, 'stethoscope', 'Mergi la un service care înțelege tratarea gazelor']] },
    ],
    fx: [
      // hook: patru impacturi (al doilea = cel mare)
      { k: 'flash', t: B1 - .08, a: .35 }, { k: 'punch', t: B1, a: .07, sh: 14 },
      { k: 'flash', t: B2 - .11, a: .75 }, { k: 'punch', t: B2, a: .16, sh: 34 }, { k: 'glitch', t: B2, d: .2 }, { k: 'shock', t: B2 + .01, x: 540, y: 748, r: 760, n: 2 },
      { k: 'flash', t: B3 - .11, a: .4 }, { k: 'punch', t: B3, a: .08, sh: 16 },
      { k: 'flash', t: B4 - .11, a: .5 }, { k: 'punch', t: B4, a: .1, sh: 20 }, { k: 'shock', t: B4 + .01, x: 540, y: 1226, r: 560, n: 1, col: '#FF4B4B' },
      { k: 'glitch', t: HB - .05, d: .14 },
      { k: 'punch', t: A.n20b - .06, a: .06, sh: 10 }, { k: 'punch', t: A.euro1 + .02, a: .07, sh: 12 }, { k: 'glitch', t: A.a1 - .2, d: .12 },
      { k: 'glitch', t: A.ele2 - .2, d: .12 }, { k: 'punch', t: A.erori2, a: .05 }, { k: 'punch', t: A.racitorul2, a: .05 },
      { k: 'flash', t: A.distruse2 - .13, a: .35 }, { k: 'punch', t: A.distruse2 - .02, a: .1, sh: 20 },
      { k: 'glitch', t: CLIP[1] - .06, d: .16 }, { k: 'punch', t: A.sute4, a: .07, sh: 12 },
      { k: 'glitch', t: A.problema4 - .2, d: .12 }, { k: 'punch', t: A.crapa4, a: .08, sh: 16 },
      { k: 'punch', t: A.pomana6 - .14, a: .09, sh: 18 }, { k: 'glitch', t: A.de7 + .15, d: .12 }, { k: 'punch', t: A.racitorul7, a: .06, sh: 10 },
      { k: 'glitch', t: A.masini8 - .2, d: .12 }, { k: 'flash', t: A.spart8 - .13, a: .3 }, { k: 'punch', t: A.spart8 - .02, a: .1, sh: 20 },
      { k: 'glitch', t: A.aveti9 - .15, d: .12 }, { k: 'punch', t: A.diagnoza10, a: .05 },
    ],
    sfx: [[HB - .1, 'whoosh', .6], [A.service9, 'shimmer', .45]],
    bursts: [[A.distruse2 + .02, 540, 1120, 6, 280, .9], [A.pomana6 - .1, 540, 1120, 6, 280, .9], [A.spart8, 540, 1120, 6, 280, .9]],
  };
};
