// v2 – Reel „Produs în România: turbinele de pe motorul 4.4 BMW M” (IMG_2486, un singur clip, fără tăieturi, ritm natural)
// Cerut de Sabin pe 14.11.2026: hook puternic pe prima frază („Unde sunteți, mă, ăia care spuneți că nu se mai produce nimic în România?”)
// și, când pomenește motorul 4.4 de BMW M (S63), motorul pus efectiv deasupra, sugestiv: fotografie reală cu licență liberă
// (Wikimedia Commons „BMW X5M Engine.JPG”, domeniu public, PD-user) într-un panou sus (`schem` cu `img` + `photoId`), cu zona din care vin turbinele marcată.
// Filmare doar cu piesele (fără față, fără plăcuțe de înmatriculare). Fără CTA pe imagine (25.10). Fără accente roșu/verde pe tot cadrul (neconfirmate).
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND }) => {
  const A = {
    unde: aw(0, 'Unde'), nu0: aw(0, 'nu'), nimic: aw(0, 'nimic'), in0: aw(0, 'în'), romania0: aw(0, 'România?'),
    turbinele: aw(0, 'Turbinele'), motorul: aw(0, 'motorul'), n44: aw(0, '4.4'), bmw: aw(0, 'BMW.'), motorizarile: aw(0, 'Motorizările'), variantele: aw(0, 'variantele'), m0: aw(0, 'M.'),
    produs1: aw(1, 'Produs'), romania1: aw(1, 'România.'), produs1b: aw(1, 'Produs', 1), sectorul: aw(1, 'Sectorul'), readus: aw(1, 'Readus'), viata1: aw(1, 'viață'), turbo1: aw(1, 'Turbo'), otopeni: aw(1, 'Otopeni.'),
    si2: aw(2, 'Și'), ingineria: aw(2, 'ingineria'), complexa: aw(2, 'complexă'),
    motorizarilor: aw(3, 'motorizărilor'), are3: aw(3, 'are'), radacina: aw(3, 'rădăcină'), romania3: aw(3, 'România.'), turbine3: aw(3, 'Turbine'), produse3: aw(3, 'produse'), romani: aw(3, 'români.'),
    din4: aw(4, 'Din'), ajuns: aw(4, 'ajuns'), datorita: aw(4, 'datorită'), pops: aw(4, 'pops'), apar: aw(4, 'Apar'), probleme: aw(4, 'probleme'), wastegate: aw(4, 'wastegate'),
    si4: aw(4, 'Și'), urmeaza: aw(4, 'urmează'), readucem: aw(4, 'readucem'), viata4: aw(4, 'viață'), cost: aw(4, 'cost'), minim: aw(4, 'minim.'),
  };
  // HOOK: titlu boom în patru trepte pe prima frază; impactul mare pe „NIMIC”, apoi „ÎN ROMÂNIA?” în tricolor.
  // Fără scântei pe titluri: coperta (out/cover_t.json, 3,87 s) e un cadru din hook cu toate rândurile, după ce inelele de șoc au dispărut.
  const B1 = A.unde - .03, B2 = A.nu0 - .03, B3 = A.nimic - .03, B4 = A.in0 - .02, HB = 4.5;
  return {
    hook: { tag: 'ANALIZĂ TEHNICĂ · LABORATOR TURBO DOCTOR', end: HB },
    hideCap: [[0, HB - .05]],
    stages: [[HB + .45, 'PACIENTUL'], [A.produs1 - .15, 'ORIGINEA'], [A.din4 - .1, 'PROBLEMA'], [A.si4 - .1, 'SOLUȚIA']],
    tags: {
      0: { nimic: 'r', romania: 'y', turbinele: 'c', motorul: 'c', bmw: 'c', variantele: 'y', m: 'y' },
      1: { produs: 'g', romania: 'y', sectorul: 'y', readus: 'g', viata: 'g', otopeni: 'y' },
      2: { ingineria: 'c', complexa: 'c' },
      3: { motorizarilor: 'c', m: 'y', radacina: 'g', romania: 'y', turbine: 'c', produse: 'g', romani: 'y' },
      4: { pacate: 'r', rapid: 'r', noi: '', turbine: 'c', softului: 'y', pops: 'r', bangs: 'r', normal: '', probleme: 'r', wastegate: 'c', readucem: 'g', viata: 'g', cost: 'g', minim: 'g' },
    },
    items: [
      // ---- hook: boom
      { k: 'boom', t: B1, dur: HB - B1, txt: 'UNDE SUNTEȚI, MĂ?', y: 560, size: 122, col: '#FFFFFF', from: 2.4, sh: 12, ca: 14, riser: false, bg: .55, glow: 'rgba(98,216,255,.5)' },
      { k: 'boom', t: B2, dur: HB - B2, txt: '„NU SE MAI PRODUCE', y: 716, size: 106, col: '#FFFFFF', from: 2.2, sh: 10, ca: 12, riser: false, bg: .4, cg: .3, glow: 'rgba(98,216,255,.45)' },
      { k: 'boom', t: B3, dur: HB - B3, txt: 'NIMIC', y: 950, size: 330, col: '#FF3B30', from: 3.8, sh: 24, ca: 30, bg: 1, glow: 'rgba(255,75,75,.6)' },
      { k: 'boom', t: B4, dur: HB - B4, txt: 'ÎN <span style="color:#3D8BFF">RO</span><span style="color:#FFD21F">MÂN</span><span style="color:#FF3B30">IA</span>”?', y: 1218, size: 160, col: '#FFFFFF', from: 2.6, sh: 14, ca: 18, riser: false, bg: .75 },
      // ---- motorul 4.4 BMW M, deasupra, exact când îl pomenește (fotografie reală, domeniu public)
      { k: 'schem', t0: A.motorul - .2, t1: A.produs1 - .8, top: 268, h: 430, type: 'photoId', img: 'assets/photos/s63_x5m.jpg',
        title: 'DE PE CE MOTOR VIN TURBINELE', sub: 'BMW M',
        P: { big: [A.n44 - .02, '4.4', 'LITRI · V8 BITURBO'], code: [A.bmw - .02, 'COD MOTOR', 'S63'], zone: [A.motorizarile - .05, 352, 40, 150, 250, 'DE AICI VIN TURBINELE'] },
        stepNames: ['MOTORUL', 'BMW M'],
        steps: [[A.motorul - .2, 'Turbinele vin de pe motorul 4.4 de BMW', ''], [A.motorizarile - .05, 'Motorizările care echipează variantele M', 'y']],
        sfx: [[A.n44 - .02, 'impact', .6], [A.bmw, 'type', .45], [A.motorizarile - .05, 'lock', .5]] },
      // ---- originea: plăcuța „MADE IN ROMANIA” de pe carcasă, apoi fișa pacientului
      { k: 'scan', t0: A.produs1 - .2, t1: A.produs1b - .12, track: 'track_plate', box: [0, 0, 440, 290], lab: 'CITIRE PLĂCUȚĂ...', lab2: 'MADE IN ROMANIA', at2: A.romania1 - .05, col2: '#4ADE80' },
      { k: 'stamp', t: A.romania1 - .02, t1: A.produs1b - .15, y: 640, txt: 'PRODUS ÎN ROMÂNIA', col: 'green', s: .95, rot: -6 },
      { k: 'file', t0: A.produs1b - .1, t1: A.si2 - .35, top: 268, no: '2486', ecg: 'ok',
        rows: [[A.produs1b - .1, 'PACIENT', 'TURBINE · BMW M 4.4', 'c', 'gear'], [A.sectorul - .02, 'LOCUL NAȘTERII', '<span style="font-size:30px;white-space:nowrap">ROMÂNIA · SECTORUL 6</span>', 'y', 'round_pushpin'],
          [A.readus - .02, 'TRATAMENT', 'READUS LA VIAȚĂ', 'g', 'stethoscope'], [A.turbo1 - .02, 'UNITATE', '<span style="font-size:26px;white-space:nowrap">TURBO DOCTOR OTOPENI</span>', 'y', 'test_tube']] },
      // ---- ingineria din spatele motorizărilor M are o rădăcină și în România
      { k: 'schem', t0: A.ingineria - .15, t1: A.din4 - .3, top: 268, h: 360, type: 'madeInRo', title: 'SCHEMĂ · RĂDĂCINA INGINERIEI', sub: 'BMW M › ROMÂNIA',
        P: { m: A.motorizarilor - .03, mLab: 'MOTORIZĂRILE M', root: A.are3 - .05, pin: A.romania3 - .03, pinLab: 'SECTORUL 6', go: A.turbine3 - .03 },
        stepNames: ['INGINERIA', 'RĂDĂCINA', 'ROMÂNIA'],
        steps: [[A.ingineria - .15, 'Ingineria complexă din spatele motorizărilor M', '', 0], [A.are3 - .05, 'Are o rădăcină și în România', 'y', 1], [A.turbine3 - .03, 'Turbine produse de români', 'g', 2]],
        sfx: [[A.motorizarilor - .03, 'pop', .5], [A.are3 - .05, 'data', .45], [A.romania3 - .03, 'lock', .55], [A.romania3, 'ding', .45]] },
      // ---- problema: soft de pops & bangs -> zona de wastegate
      { k: 'chip', t0: A.din4 - .05, t1: A.datorita - .35, y: 330, ph: [[A.din4 - .05, 'warning', 'DIN PĂCATE...', 'red'], [A.ajuns - .05, 'stopwatch', 'A AJUNS RAPID LA NOI', 'red']] },
      { k: 'schem', t0: A.datorita - .1, t1: A.si4 - .4, top: 268, h: 330, type: 'popsBangs', title: 'SCHEMĂ · POPS & BANGS', sub: 'TURBINĂ + WASTEGATE',
        stepNames: ['CAUZA', 'EFECTUL'],
        steps: [[A.datorita - .1, 'Soft de pops & bangs: pocnituri pe evacuare', 'y', 'pops'], [A.apar - .05, 'Apar probleme pe zona de wastegate', 'r', 'wg']] },
      { k: 'call', t0: A.apar + .1, t1: A.wastegate + .05, track: 'track_wg', p: [512, 1128], lab: [300, 1250], h: 'ZONA DE', v: 'WASTEGATE', col: 'red' },
      // ---- soluția
      { k: 'ecg', t0: A.si4 - .1, t1: SEND - .25, top: 268, label: 'PULS TURBINE', ico: 'stethoscope', states: [[A.si4 - .1, 'crit', 'URMEAZĂ TRATAMENTUL'], [A.viata4 - .02, 'ok', 'READUSE LA VIAȚĂ']] },
      { k: 'kin', t: A.cost - .02, dur: 1.5, txt: 'COST MINIM', col: '#4ADE80', y: 1080, size: 170, rot: -4 },
      { k: 'tip', t0: SEND + .1, t1: TEND - .15, top: 520, title: 'REȚETA TURBO DOCTOR', sub: 'SFAT DE INGINER · TURBO', ico: 'stethoscope',
        rows: [[SEND + .35, 'fire', 'Soft de pops & bangs? Turbinele ajung mai repede la reparat'], [SEND + 1.15, 'gear', 'Problemele apar pe zona de wastegate'],
          [SEND + 1.95, 'hammer_and_wrench', 'Se pot readuce la viață, la un cost minim']] },
    ],
    fx: [
      { k: 'flash', t: B1 - .08, a: .35 }, { k: 'punch', t: B1, a: .07, sh: 14 }, { k: 'punch', t: B2, a: .05, sh: 10 },
      { k: 'flash', t: B3 - .11, a: .75 }, { k: 'punch', t: B3, a: .16, sh: 34 }, { k: 'glitch', t: B3, d: .2 }, { k: 'shock', t: B3 + .01, x: 540, y: 950, r: 760, n: 2, col: '#FF4B4B' },
      { k: 'flash', t: B4 - .11, a: .45 }, { k: 'punch', t: B4, a: .09, sh: 18 }, { k: 'shock', t: B4 + .01, x: 540, y: 1218, r: 540, n: 1, col: '#FFD21F' },
      { k: 'glitch', t: HB - .05, d: .14 },
      { k: 'punch', t: A.n44, a: .06, sh: 10 }, { k: 'glitch', t: A.produs1 - .28, d: .12 }, { k: 'flash', t: A.romania1 - .12, a: .3 }, { k: 'punch', t: A.romania1, a: .08, sh: 14 },
      { k: 'glitch', t: A.ingineria - .25, d: .12 }, { k: 'punch', t: A.produse3, a: .06, sh: 8 },
      { k: 'glitch', t: A.din4 - .12, d: .12 }, { k: 'punch', t: A.apar, a: .05 }, { k: 'glitch', t: A.si4 - .15, d: .12 }, { k: 'punch', t: A.cost, a: .07, sh: 10 },
    ],
    sfx: [[HB - .1, 'whoosh', .6], [A.romania1 + .05, 'shimmer', .5], [A.produse3, 'impact', .55], [A.viata4, 'shimmer', .5]],
    bursts: [[A.romania1 + .05, 540, 640, 6, 420, 1.0], [A.produse3 + .05, 540, 560, 6, 380, .9], [A.cost + .1, 540, 1080, 6, 380, .9]],
  };
};
