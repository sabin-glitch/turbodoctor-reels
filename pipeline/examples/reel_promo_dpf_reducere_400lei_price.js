// v2 – PROMO plătit (Facebook + TikTok, 11.11.2026): reducere la curățarea filtrului de particule în noiembrie–decembrie · VARIANTA 500 → 400 LEI
// 2 clipuri lipite în ordinea filmării, fără tăieturi: 0 IMG_2345 (selfie, intro comun) · 21.333 IMG_2347 (selfie, oferta 400 lei + WhatsApp cu seria de șasiu)
// Cerut de Sabin: hook puternic pe „peste 200.000 de kilometri” / „acești martori aprins în bord”; deasupra lui martorii Check Engine și DPF;
// două variante de preț (400 și 450), făcute să oprească scroll-ul pe Facebook și TikTok. Promo plătit: WhatsApp-ul pe ecran când îl spune și pe final.
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND, TOTAL }) => {
  const WA = '0739 065 065';
  const A = {
    ai: aw(0, 'Ai'), peste: aw(0, 'peste'), k200: aw(0, '200.000'), km: aw(0, 'kilometri'), curatare0: aw(0, 'curățare'), particule0: aw(0, 'particule'),
    sau0: aw(0, 'Sau'), deja: aw(0, 'deja'), acesti: aw(0, 'acești'), martori: aw(0, 'martori'), aprins0: aw(0, 'aprins'), bord0: aw(0, 'bord'),
    ei: aw(1, 'Ei'), turbo1: aw(1, 'Turbo'), veste: aw(1, 'veste'), tine: aw(1, 'tine'), toata: aw(1, 'Toată'), noiembrie: aw(1, 'noiembrie'), decembrie: aw(1, 'decembrie'),
    avem1b: aw(1, 'avem', 1), reducere: aw(1, 'reducere'), curatarea1: aw(1, 'curățarea'), pentru1b: aw(1, 'pentru', 1), sezonul: aw(1, 'sezonul'),
    curatarea2: aw(2, 'Curățarea'), p500: aw(2, '500'), la2b: aw(2, 'la', 1), p400: aw(2, '400'), lei2b: aw(2, 'lei', 1), pentru2: aw(2, 'pentru'),
    autoturism: aw(2, 'autoturism'), cilindree: aw(2, 'cilindree'), iar2: aw(2, 'Iar'), afli: aw(2, 'afli'), trebuie: aw(2, 'trebuie'), trimiti: aw(2, 'trimiți'), whatsapp2: aw(2, 'WhatsApp'),
    seria: aw(2, 'seria'), acolo: aw(2, 'acolo'), cel: aw(2, 'cel'), cu2b: aw(2, 'cu', 2), demontare2b: aw(2, 'demontare', 1), montare2: aw(2, 'montare'),
    readaptare: aw(2, 'readaptare'),
    tot3: aw(3, 'tot'), dane: aw(3, 'Dă-ne'), whatsapp3: aw(3, 'WhatsApp'), ajuta: aw(3, 'ajuta'), intretine: aw(3, 'întreține'), sau3: aw(3, 'sau'),
    starea: aw(3, 'starea'), daca3: aw(3, 'dacă'), martor3: aw(3, 'martor'), aprins3: aw(3, 'aprins'), bord3: aw(3, 'bord'),
  };
  const CLIP = [0, 640 / 30];
  const T1 = .05, T2 = A.k200 - .04, T3 = A.curatare0 - .03;      // impacturile titlurilor din hook
  const HOOK_END = A.sau0 - .08;
  const RED_END = A.pentru1b - .3;
  return {
    hook: null,
    stages: null,
    hideCap: [[0, HOOK_END + .02], [A.reducere - .05, RED_END + .05], [A.p500 - .1, A.pentru2 - .1]],
    tags: {
      0: { peste: 'y', 200000: 'y', kilometri: 'y', curatare: 'g', filtrului: 'c', particule: 'c', martori: 'r', aprins: 'r', bord: 'r' },
      1: { veste: 'g', buna: 'g', noiembrie: 'y', decembrie: 'y', reducere: 'g', curatarea: 'g', sezonul: 'c', rece: 'c' },
      2: { redusa: 'g', 500: 'r', 400: 'g', lei: 'y', autoturism: 'c', cilindree: 'c', litri: 'y', pretul: 'y', demontare: 'c', montarea: 'c', montare: 'c',
        whatsapp: 'g', seria: 'y', sasiu: 'y', corect: 'g', pret: 'y', inclus: 'g', readaptare: 'c' },
      3: { whatsapp: 'g', intretine: 'g', corect: 'g', corecta: 'g', functionare: 'g', martor: 'r', aprins: 'r', bord: 'r' },
    },
    items: [
      // HOOK (IMG_2345, selfie): „AI PESTE / 200.000 KM?” → „CURĂȚARE DPF?”, deasupra capului; subtitrările ascunse cât stau titlurile
      { k: 'boom', t: T1, dur: T3 - .1 - T1, txt: 'AI PESTE', y: 212, size: 104, col: '#FFFFFF', from: 2.8, sh: 16, ca: 18, riser: false, bg: .7, glow: 'rgba(98,216,255,.5)' },
      { k: 'boom', t: T2, dur: T3 - .1 - T2, txt: '200.000 KM?', y: 370, size: 160, col: '#FFD21F', from: 3.6, sh: 28, ca: 30, bg: 1 },
      { k: 'boom', t: T3, dur: HOOK_END - T3, txt: 'CURĂȚARE DPF?', y: 300, size: 128, col: '#62D8FF', from: 3.0, sh: 18, ca: 20, riser: false, bg: .75, glow: 'rgba(98,216,255,.55)' },
      // „Sau chiar deja ai unul dintre acești martori aprins în bord?” → bordul cu Check Engine + DPF, deasupra capului
      { k: 'dash', t0: A.deja - .12, t1: A.ei - .12, y: 336, s: .96, gap: 300,
        lamps: [[A.acesti - .02, 'engine', 'CHECK ENGINE'], [A.martori - .02, 'dpf', 'DPF']], pulse: [A.aprins0 - .02, A.bord0 - .02] },

      // „Ei bine, la Turbo Doctor avem o veste foarte bună pentru tine.”
      { k: 'chip', t0: A.ei, t1: A.toata - .3, y: 300, s: 1.22, ph: [[A.ei, 'stethoscope', 'LA TURBO DOCTOR', 'blue'], [A.veste - .05, 'sparkles', 'AVEM O VESTE FOARTE BUNĂ', 'green']] },
      { k: 'chip', t0: A.toata - .05, t1: A.reducere - .35, y: 300, s: 1.22, ph: [[A.toata - .05, 'spiral_calendar', 'TOATĂ LUNA NOIEMBRIE', 'yellow'], [A.decembrie - .05, 'spiral_calendar', 'NOIEMBRIE + DECEMBRIE', 'yellow']] },
      // REDUCERE (boom) + la curățarea DPF
      { k: 'boom', t: A.reducere, dur: RED_END - A.reducere, txt: 'REDUCERE', y: 250, size: 150, col: '#FF4B4B', from: 3.4, sh: 26, ca: 28, bg: 1, glow: 'rgba(255,75,75,.55)' },
      { k: 'boom', t: A.curatarea1 - .02, dur: RED_END - A.curatarea1 + .02, txt: 'LA CURĂȚAREA DPF', y: 392, size: 78, col: '#FFFFFF', from: 2.4, sh: 10, ca: 12, riser: false, bg: .5, glow: 'rgba(98,216,255,.45)' },
      { k: 'chip', t0: A.pentru1b - .05, t1: CLIP[1] - .2, y: 300, s: 1.22, ph: [[A.pentru1b - .05, 'snowflake', 'PREGĂTEȘTE MAȘINA', 'blue'], [A.sezonul - .05, 'snowflake', 'PENTRU SEZONUL RECE', 'blue']] },

      // IMG_2347 (selfie): PREȚUL — 500 LEI tăiat, 400 LEI bubuie, −20%
      { k: 'price', t0: A.curatarea2 - .08, t1: A.autoturism - .3, top: 168, kicker: 'CURĂȚARE FILTRU DE PARTICULE', kIco: 'broom',
        old: '500', neu: '400', oldAt: A.p500 - .03, cutAt: A.la2b - .06, newAt: A.p400 - .02, badge: '−20%', badgeAt: A.lei2b },
      { k: 'chip', t0: A.autoturism - .05, t1: A.iar2 - .3, y: 300, s: 1.22, ph: [[A.autoturism - .05, 'automobile', 'ORICE AUTOTURISM', 'blue'], [A.cilindree - .05, 'gear', 'CILINDREE PÂNĂ ÎN 2,5 LITRI', 'yellow']] },
      { k: 'chip', t0: A.iar2 - .05, t1: A.trebuie - .35, y: 300, s: 1.22, ph: [[A.afli - .1, 'wrench', 'PREȚ CU DEMONTARE + MONTARE?', 'yellow']] },
      // WhatsApp + seria de șasiu
      { k: 'eq', t0: A.trebuie - .12, t1: A.acolo - .3, top: 168, ico: 'speech_balloon', title: 'OFERTA COMPLETĂ', sub: 'WHATSAPP',
        lines: [[A.trimiti - .08, 'MESAJ PE WHATSAPP', 'w'], [A.whatsapp2 - .05, WA, 'big g'], [A.seria - .05, 'CU SERIA DE ȘASIU A MAȘINII', 'y']] },
      { k: 'chip', t0: A.acolo - .05, t1: A.cu2b - .35, y: 300, s: 1.22, ph: [[A.acolo - .05, 'receipt', 'CEL MAI CORECT PREȚ', 'green']] },
      { k: 'pipe', t0: A.cu2b - .1, t1: A.dane - .3, top: 168, ico: 'receipt', title: 'PREȚUL CU TOTUL INCLUS', steps: [
        [A.demontare2b - .05, 'wrench', 'DEMONTARE'], [A.montare2 - .05, 'nutbolt', 'MONTARE'], [A.readaptare - .05, 'counterclockwise_arrows_button', 'READAPTARE<br>DUPĂ CURĂȚARE']] },
      // „Dă-ne acum un mesaj pe WhatsApp…”
      { k: 'eq', t0: A.dane - .12, t1: A.ajuta - .3, top: 168, ico: 'speech_balloon', title: 'SCRIE-NE PE WHATSAPP', sub: 'ACUM',
        lines: [[A.dane, 'DĂ-NE UN MESAJ ACUM', 'w'], [A.whatsapp3 - .05, WA, 'big g']] },
      { k: 'chip', t0: A.ajuta - .05, t1: A.daca3 - .3, y: 300, s: 1.22, ph: [[A.intretine - .1, 'wrench', 'ÎNTREȚINERE CORECTĂ', 'green'], [A.starea - .1, 'check_mark_button', 'STARE CORECTĂ DE FUNCȚIONARE', 'green']] },
      // „…dacă ai vreun martor aprins în bord” → bordul revine, cu martorii aprinși
      { k: 'dash', t0: A.daca3 - .1, t1: SEND - .12, y: 336, s: .96, gap: 300,
        lamps: [[A.martor3 - .02, 'engine', 'CHECK ENGINE'], [A.martor3 + .12, 'dpf', 'DPF']], pulse: [A.aprins3 - .02, A.bord3 - .02] },

      // cardul de final standard + oferta pe WhatsApp (doar pe promo)
      { k: 'eq', t0: TEND + 2.45, t1: TOTAL + 1, top: 1160, ico: 'speech_balloon', title: 'OFERTA PE WHATSAPP', sub: 'NOIEMBRIE–DECEMBRIE',
        lines: [[TEND + 2.65, 'CURĂȚARE DPF · 400 LEI', 'y'], [TEND + 2.95, WA, 'big g']] },
    ],
    fx: [
      // hook
      { k: 'punch', t: T1, a: .08, sh: 16 }, { k: 'glitch', t: T1, d: .12 },
      { k: 'flash', t: T2 - .11, a: .55 }, { k: 'punch', t: T2, a: .14, sh: 30 }, { k: 'glitch', t: T2, d: .18 },
      { k: 'shock', t: T2 + .01, x: 540, y: 370, r: 680, n: 2, col: '#FFD21F', col2: '#FFFFFF' },
      { k: 'flash', t: T3 - .1, a: .3 }, { k: 'punch', t: T3, a: .07, sh: 14 }, { k: 'glitch', t: T3, d: .12 },
      { k: 'punch', t: A.acesti, a: .05, sh: 8 }, { k: 'punch', t: A.martori, a: .06, sh: 10 }, { k: 'punch', t: A.aprins0, a: .05, sh: 8 },
      // reducere
      { k: 'flash', t: A.reducere - .11, a: .55 }, { k: 'punch', t: A.reducere, a: .12, sh: 26 }, { k: 'glitch', t: A.reducere, d: .16 },
      { k: 'shock', t: A.reducere + .01, x: 540, y: 250, r: 620, n: 2, col: '#FF4B4B', col2: '#FFFFFF' },
      // trecerea la al doilea clip
      { k: 'glitch', t: CLIP[1] - .04, d: .12 },
      // prețul
      { k: 'punch', t: A.p500, a: .05, sh: 10 }, { k: 'flash', t: A.p400 - .13, a: .6 }, { k: 'punch', t: A.p400, a: .14, sh: 30 }, { k: 'glitch', t: A.p400, d: .18 },
      { k: 'shock', t: A.p400 + .01, x: 540, y: 470, r: 700, n: 2, col: '#FFD21F', col2: '#4ADE80' }, { k: 'punch', t: A.lei2b, a: .05, sh: 10 },
      // WhatsApp
      { k: 'punch', t: A.whatsapp2, a: .05, sh: 8 }, { k: 'punch', t: A.whatsapp3, a: .06, sh: 10 }, { k: 'punch', t: A.martor3, a: .05, sh: 8 },
    ],
    sfx: [[CLIP[1] - .1, 'whoosh', .45]],
    bursts: [[T2 + .04, 540, 370, 8, 460, 1.4], [A.reducere + .04, 540, 250, 6, 420, 1.1], [A.p400 + .05, 540, 470, 9, 500, 1.5]],
  };
};
