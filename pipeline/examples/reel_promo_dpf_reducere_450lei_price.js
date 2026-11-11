// v2 – PROMO plătit (Facebook + TikTok, 11.11.2026): reducere la curățarea filtrului de particule în noiembrie–decembrie · VARIANTA 500 → 450 LEI
// 2 clipuri lipite în ordinea filmării, fără tăieturi: 0 IMG_2345 (selfie, intro comun) · 21.333 IMG_2349 (selfie, oferta 450 lei + poza cu talonul pe WhatsApp + garanție 24 luni)
// Cerut de Sabin: hook puternic pe „peste 200.000 de kilometri” / „acești martori aprins în bord”; deasupra lui martorii Check Engine și DPF;
// două variante de preț (400 și 450), făcute să oprească scroll-ul pe Facebook și TikTok. Promo plătit: WhatsApp-ul pe ecran când îl spune și pe final.
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND, TOTAL }) => {
  const WA = '0739 065 065';
  const A = {
    ai: aw(0, 'Ai'), peste: aw(0, 'peste'), k200: aw(0, '200.000'), km: aw(0, 'kilometri'), curatare0: aw(0, 'curățare'), particule0: aw(0, 'particule'),
    sau0: aw(0, 'Sau'), deja: aw(0, 'deja'), acesti: aw(0, 'acești'), martori: aw(0, 'martori'), aprins0: aw(0, 'aprins'), bord0: aw(0, 'bord'),
    ei: aw(1, 'Ei'), turbo1: aw(1, 'Turbo'), veste: aw(1, 'veste'), tine: aw(1, 'tine'), toata: aw(1, 'Toată'), noiembrie: aw(1, 'noiembrie'), decembrie: aw(1, 'decembrie'),
    reducere: aw(1, 'reducere'), curatarea1: aw(1, 'curățarea'), pentru1b: aw(1, 'pentru', 1), sezonul: aw(1, 'sezonul'),
    curatarea2: aw(2, 'Curățarea'), p450: aw(2, '450'), lei2: aw(2, 'lei'), p500: aw(2, '500'), lei2b: aw(2, 'lei', 1), pentru2: aw(2, 'pentru'),
    orice: aw(2, 'orice'), motorizare: aw(2, 'motorizare'), pana: aw(2, 'până'), pe2: aw(2, 'Pe', 1), pret2: aw(2, 'preț'), manopera: aw(2, 'manopera'), demontare2: aw(2, 'demontare'),
    iar3: aw(3, 'Iar'), afla: aw(3, 'afla'), trebuie3: aw(3, 'trebuie'), trimiti3: aw(3, 'trimiți'), poza: aw(3, 'poză'), talonul: aw(3, 'talonul'), whatsapp3: aw(3, 'WhatsApp'),
    solicitand: aw(3, 'solicitând'),
    in4: aw(4, 'În'), pretul4: aw(4, 'prețul'), demontare4: aw(4, 'demontare'), montare4: aw(4, 'montare'), reinit: aw(4, 'reinițializare'), probe: aw(4, 'probe'),
    absolut: aw(4, 'absolut'),
    sau5: aw(5, 'sau'), demonta5: aw(5, 'demonta'), poti5b: aw(5, 'poți', 1), doar: aw(5, 'doar'), garantia: aw(5, 'Garanția'), n24: aw(5, '24'), fara: aw(5, 'fără'),
  };
  const CLIP = [0, 640 / 30];
  const T1 = .05, T2 = A.k200 - .04, T3 = A.curatare0 - .03;      // impacturile titlurilor din hook
  const HOOK_END = A.sau0 - .08;
  const RED_END = A.pentru1b - .3;
  const G1 = A.garantia - .02, G2 = A.n24 - .02, G3 = A.fara - .02, G_END = SEND - .12;   // garanția, în trei trepte
  return {
    hook: null,
    stages: null,
    hideCap: [[0, HOOK_END + .02], [A.reducere - .05, RED_END + .05], [A.p450 - .1, A.pentru2 - .1], [G1 - .05, SEND]],
    tags: {
      0: { peste: 'y', 200000: 'y', kilometri: 'y', curatare: 'g', filtrului: 'c', particule: 'c', martori: 'r', aprins: 'r', bord: 'r' },
      1: { veste: 'g', buna: 'g', noiembrie: 'y', decembrie: 'y', reducere: 'g', curatarea: 'g', sezonul: 'c', rece: 'c' },
      2: { redusa: 'g', 450: 'g', 500: 'r', lei: 'y', curatarea: 'g', filtrului: 'c', particule: 'c', motorizare: 'c', litri: 'y', pret: 'y', redus: 'g',
        manopera: 'y', demontare: 'c', montare: 'c' },
      3: { oferta: 'y', poza: 'y', talonul: 'y', whatsapp: 'g', pret: 'y' },
      4: { pretul: 'y', complet: 'g', demontare: 'c', montare: 'c', reinitializare: 'c', probe: 'c', drum: 'c', absolut: 'g', tot: 'g' },
      5: { curatare: 'g', filtrul: 'c', particule: 'c', mecanicul: 'c', demontat: 'c', garantia: 'g', 24: 'g', luni: 'g', limita: 'y', kilometri: 'y' },
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

      // IMG_2349 (selfie): PREȚUL — spune întâi 450, apoi „de la 500”: 450 LEI bubuie, 500 LEI apare deasupra și e tăiat, −10%
      { k: 'price', t0: A.curatarea2 - .08, t1: A.orice - .35, top: 168, kicker: 'CURĂȚARE FILTRU DE PARTICULE', kIco: 'broom',
        old: '500', neu: '450', newAt: A.p450 - .02, oldAt: A.p500 - .03, cutAt: A.p500 + .3, badge: '−10%', badgeAt: A.lei2b },
      { k: 'chip', t0: A.orice - .05, t1: A.pe2 - .3, y: 300, s: 1.22, ph: [[A.orice - .05, 'automobile', 'ORICE MOTORIZARE', 'blue'], [A.pana - .05, 'gear', 'PÂNĂ ÎN 2,5 LITRI', 'yellow']] },
      { k: 'chip', t0: A.pe2 - .05, t1: A.iar3 - .3, y: 300, s: 1.22, ph: [[A.pe2 - .05, 'sparkles', 'PE LÂNGĂ ASTA:', 'green'], [A.pret2 - .05, 'money_bag', 'PREȚ REDUS ȘI LA MANOPERĂ', 'green'],
        [A.demontare2 - .05, 'wrench', 'DEMONTARE + MONTARE', 'blue']] },
      // oferta exactă: poza cu talonul pe WhatsApp
      { k: 'chip', t0: A.iar3 - .05, t1: A.trimiti3 - .3, y: 300, s: 1.22, ph: [[A.afla - .1, 'magnifying_glass_tilted_left', 'AFLĂ OFERTA EXACTĂ', 'yellow']] },
      { k: 'eq', t0: A.trimiti3 - .1, t1: A.in4 - .3, top: 168, ico: 'camera', title: 'OFERTA EXACTĂ', sub: 'WHATSAPP',
        lines: [[A.poza - .1, 'POZĂ CU TALONUL MAȘINII', 'w'], [A.whatsapp3 - .05, WA, 'big g'], [A.solicitand - .05, 'CERI O OFERTĂ DE PREȚ', 'y']] },
      // prețul complet: tot ce intră
      { k: 'pipe', t0: A.in4 - .1, t1: A.absolut - .3, top: 168, ico: 'receipt', title: 'PREȚUL COMPLET', steps: [
        [A.demontare4 - .05, 'wrench', 'DEMONTARE'], [A.montare4 - .05, 'nutbolt', 'MONTARE'], [A.reinit - .05, 'counterclockwise_arrows_button', 'REINIȚIALIZARE'],
        [A.probe - .05, 'chequered_flag', 'PROBE<br>DE DRUM']] },
      { k: 'chip', t0: A.absolut - .05, t1: A.sau5 - .3, y: 300, s: 1.22, ph: [[A.absolut - .05, 'check_mark_button', 'ABSOLUT TOT, LA CURĂȚAREA DPF', 'green']] },
      { k: 'chip', t0: A.sau5 - .05, t1: G1 - .3, y: 300, s: 1.22, ph: [[A.sau5 - .05, 'wrench', 'SAU ÎL DEMONTEZI LA MECANICUL TĂU', 'blue'], [A.poti5b - .05, 'round_pushpin', 'ȘI VII LA NOI DOAR CU FILTRUL', 'blue']] },
      // GARANȚIE 24 LUNI · FĂRĂ LIMITĂ DE KM (boom în trei trepte)
      { k: 'boom', t: G1, dur: G_END - G1, txt: 'GARANȚIE', y: 200, size: 84, col: '#FFFFFF', from: 2.6, sh: 12, ca: 14, riser: false, bg: .6, glow: 'rgba(74,222,128,.45)' },
      { k: 'boom', t: G2, dur: G_END - G2, txt: '24 LUNI', y: 322, size: 150, col: '#4ADE80', from: 3.4, sh: 26, ca: 28, bg: 1, glow: 'rgba(74,222,128,.6)' },
      { k: 'boom', t: G3, dur: G_END - G3, txt: 'FĂRĂ LIMITĂ DE KM', y: 446, size: 66, col: '#FFD21F', from: 2.4, sh: 10, ca: 12, riser: false, bg: .55 },

      // cardul de final standard + oferta pe WhatsApp (doar pe promo)
      { k: 'eq', t0: TEND + 2.45, t1: TOTAL + 1, top: 1160, ico: 'speech_balloon', title: 'OFERTA PE WHATSAPP', sub: 'NOIEMBRIE–DECEMBRIE',
        lines: [[TEND + 2.65, 'CURĂȚARE DPF · 450 LEI', 'y'], [TEND + 2.95, WA, 'big g']] },
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
      { k: 'flash', t: A.p450 - .13, a: .6 }, { k: 'punch', t: A.p450, a: .14, sh: 30 }, { k: 'glitch', t: A.p450, d: .18 },
      { k: 'shock', t: A.p450 + .01, x: 540, y: 500, r: 700, n: 2, col: '#FFD21F', col2: '#4ADE80' }, { k: 'punch', t: A.p500, a: .05, sh: 10 }, { k: 'punch', t: A.lei2b, a: .05, sh: 10 },
      // WhatsApp, garanția
      { k: 'punch', t: A.whatsapp3, a: .06, sh: 10 },
      { k: 'punch', t: G1, a: .06, sh: 12 }, { k: 'flash', t: G2 - .11, a: .55 }, { k: 'punch', t: G2, a: .13, sh: 28 }, { k: 'glitch', t: G2, d: .16 },
      { k: 'shock', t: G2 + .01, x: 540, y: 322, r: 640, n: 2, col: '#4ADE80', col2: '#FFFFFF' }, { k: 'punch', t: G3, a: .06, sh: 12 },
    ],
    sfx: [[CLIP[1] - .1, 'whoosh', .45]],
    bursts: [[T2 + .04, 540, 370, 8, 460, 1.4], [A.reducere + .04, 540, 250, 6, 420, 1.1], [A.p450 + .05, 540, 500, 9, 500, 1.5], [G2 + .04, 540, 322, 8, 460, 1.4]],
  };
};
