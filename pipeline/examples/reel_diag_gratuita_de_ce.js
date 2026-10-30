// v2 – Reel r_diag – „De ce e gratuită diagnoza la Turbo Doctor?” (4 clipuri în ordinea filmării, fără tăieturi)
// clipuri: 0 turbina secționată + motor pe stand (IMG_1917) · 11.03 selfie (IMG_1919) · 59.70 motor pe stand (IMG_1920) · 68.27 selfie (IMG_1921)
// Cerut de Sabin 28.10: hook puternic cu „de ce e gratuită diagnoza la noi” (titlu boom, ca la Euro 7), apoi explicația cauză → efect
// (eroarea apare pe turbină, cauza e pe acționare / injectoare / DPF) și de ce diagnoza trebuie făcută corect ca reparația să reușească.
// Fără CTA pe imagine (25.10): telefonul / site-ul nu apar (întrebat pe 28.10; blocul PHONE de mai jos se activează doar dacă spune da).
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND }) => {
  const A = {
    diagnoza0: aw(0, 'diagnoza'), complet1: aw(1, 'complet'), gratuita1: aw(1, 'gratuită'), dar1: aw(1, 'Dar'),
    treaba: aw(2, 'Treaba'), noi2: aw(2, 'Noi'), experienta: aw(2, 'experiență'), pe2: aw(2, 'pe'), tocmai2: aw(2, 'Tocmai'), aceste: aw(2, 'aceste'),
    puteti3: aw(3, 'puteți'), eroare3: aw(3, 'eroare'), desi3: aw(3, 'deși'), altundeva: aw(3, 'altundeva,'), actionarea: aw(3, 'acționarea'),
    puteti4: aw(4, 'Puteți'), injectoarele4: aw(4, 'injectoarele'), sau4: aw(4, 'sau'), dpf4: aw(4, 'DPF-ul'), supra4: aw(4, 'supraîncărcat'), nu4b: aw(4, 'nu', 1),
    tocmai5: aw(5, 'Tocmai'), diagnoza5: aw(5, 'diagnoza'), gratuita5: aw(5, 'gratuită.'), in5: aw(5, 'În'), piesa5: aw(5, 'piesa'), noi5b: aw(5, 'noi', 1), stare5: aw(5, 'stare'),
    si6: aw(6, 'Și'), valoare6: aw(6, 'valoare'), corecta6: aw(6, 'corectă'), exact6: aw(6, 'exact'), nu6: aw(6, 'nu'),
    mecanica: aw(7, 'Mecanica'), grea7: aw(7, 'grea'), diagnosticarea7: aw(7, 'diagnosticarea'), cheia7: aw(7, 'cheia'),
    tocmai8: aw(8, 'Tocmai'), orice8: aw(8, 'Orice'), admisie8: aw(8, 'admisie,'), turbine8: aw(8, 'turbine,'), injectoare8: aw(8, 'injectoare,'), dpf8: aw(8, 'DPF-uri,'),
    noi8c: aw(8, 'noi', 1), si8b: aw(8, 'Și'), diagnoza8: aw(8, 'diagnoză'), gratuita8: aw(8, 'gratuită'), numarul8: aw(8, 'numărul'), site8: aw(8, 'site-ul'),
  };
  const CLIP = [0, 11.03, 59.70, 68.27];
  // HOOK 1 (turbina secționată): „DE CE E / GRATUITĂ / DIAGNOZA?” – trei titluri boom, al doilea e impactul mare
  const B1 = .16, B2 = .74, B3 = 1.22, HB = 3.9;
  // HOOK 2 (motor pe stand): „DAR DE CE?” pe întrebarea lui, până la „Treaba e simplă”
  const B4 = A.dar1 - .03, HEND = A.treaba - .15;
  return {
    hook: { tag: 'TURBO DOCTOR · DIAGNOZĂ GRATUITĂ', end: HEND },
    hideCap: [[0, HB - .12], [B4 - .05, HEND - .05]],
    stages: [[A.treaba - .05, 'DE CE GRATUIT?'], [A.puteti3 - .5, 'CAUZĂ › EFECT'], [A.tocmai5 - .1, 'DIAGNOZA'], [A.mecanica - .1, 'SUCCESUL']],
    tags: {
      0: { diagnoza: 'y' }, 1: { gratuita: 'g', complet: 'g' },
      2: { diagnosticarea: 'y', inselatoare: 'r', simpla: 'g' }, 3: { actionarea: 'c', altundeva: 'y' }, 4: { dpful: 'c', supraincarcat: 'r', corect: 'g' },
      5: { diagnoza: 'y', gratuita: 'g', piesa: 'c', stare: 'y' }, 6: { corecta: 'g', exact: 'g', crezi: 'r' },
      7: { grea: 'r', diagnosticarea: 'y', corecta: 'g', cheia: 'g', succesului: 'g' },
      8: { diagnoza: 'y', gratuita: 'g', alaturi: 'g', aici: 'g', dpfuri: 'c', pompe: 'c', motoare: 'c' },
    },
    items: [
      // ---- hook 1: boom
      { k: 'boom', t: B1, dur: HB - B1, txt: 'DE CE E', y: 640, size: 150, col: '#FFFFFF', from: 2.4, sh: 12, ca: 14, riser: false, bg: .5, glow: 'rgba(98,216,255,.5)' },
      { k: 'boom', t: B2, dur: HB - B2, txt: 'GRATUITĂ', y: 860, size: 245, col: '#FFD21F', from: 3.8, sh: 24, ca: 30, bg: 1 },
      { k: 'boom', t: B3, dur: HB - B3, txt: 'DIAGNOZA?', y: 1075, size: 185, col: '#FFFFFF', from: 2.6, sh: 14, ca: 18, riser: false, bg: .7, glow: 'rgba(98,216,255,.55)' },
      // ---- motorul pe stand: ce e gratuit, apoi „complet gratuită”
      { k: 'list', t0: HB, t1: B4 - .3, top: 268, ico: 'stethoscope', title: 'GRATUIT LA TURBO DOCTOR',
        rows: [[HB + .05, 'VERIFICAREA FIZICĂ A TURBINEI'], [A.diagnoza0 - .02, 'DIAGNOZA PE MOTOR']] },
      { k: 'kin', t: A.complet1 - .02, dur: 1.6, txt: 'COMPLET GRATUITĂ!', col: '#FFD21F', y: 1060, size: 118, rot: -4 },
      // ---- hook 2: „DAR DE CE?”
      { k: 'boom', t: B4, dur: HEND - B4, txt: 'DAR DE CE?', y: 900, size: 195, col: '#FF4B4B', from: 3.4, sh: 20, ca: 24, bg: .9, glow: 'rgba(255,75,75,.6)' },
      // ---- selfie 1 (IMG_1919): grafică compactă deasupra capului
      { k: 'chip', t0: A.treaba - .05, t1: A.tocmai2 - .3, y: 330, ph: [[A.treaba - .05, 'check_mark_button', 'TREABA E SIMPLĂ', 'green'],
        [A.noi2 - .05, 'stethoscope', 'EXPERIENȚĂ ÎN DIAGNOSTICARE', 'blue'], [A.pe2 - .05, 'gear', 'ADMISIE · INJECȚIE · EVACUARE', 'blue']] },
      { k: 'def', t0: A.tocmai2 - .05, t1: A.puteti3 - .8, top: 262, term: 'DEFECȚIUNI ÎNȘELĂTOARE', text: 'Simptomul apare pe o piesă, dar cauza reală e în altă parte.' },
      // cauză → efect 1: eroare pe turbină, cauza pe acționare
      { k: 'chip', t0: A.puteti3 - .5, t1: A.puteti4 - .3, y: 330, ph: [[A.puteti3 - .5, 'warning', 'EROARE PE TURBINĂ', 'red'],
        [A.desi3 - .05, 'magnifying_glass_tilted_left', 'DAR EROAREA NU E ACOLO', 'yellow'], [A.altundeva - .05, 'gear', 'E PE ACȚIONAREA TURBINEI', 'yellow']] },
      { k: 'kin', t: A.altundeva - .02, dur: 1.3, txt: 'CAUZA E ÎN ALTĂ PARTE!', col: '#FFD21F', y: 1185, size: 92, rot: -4 },
      // cauză → efect 2: injectoare sau DPF
      { k: 'chip', t0: A.puteti4 - .05, t1: A.tocmai5 - .3, y: 330, ph: [[A.puteti4 - .05, 'warning', 'EROARE PE TURBINĂ', 'red'],
        [A.injectoarele4 - .05, 'droplet', 'CAUZA: INJECTOARELE NU MERG CORECT', 'yellow'], [A.sau4 - .05, 'leaf', 'SAU: DPF-UL SUPRAÎNCĂRCAT', 'yellow'],
        [A.nu4b - .05, 'cross_mark', 'NU MAI EVACUEAZĂ CUM TREBUIE', 'red']] },
      { k: 'kin', t: A.supra4 - .02, dur: 1.3, txt: 'DPF SUPRAÎNCĂRCAT', col: '#FF3B30', y: 1185, size: 100, rot: -4 },
      // de asta: diagnoza gratuită
      { k: 'chip', t0: A.tocmai5 - .05, t1: A.in5 - .3, y: 330, ph: [[A.tocmai5 - .05, 'stethoscope', 'DE ASTA: DIAGNOZA GRATUITĂ', 'green']] },
      { k: 'kin', t: A.gratuita5 - .02, dur: 1.3, txt: 'DIAGNOZĂ GRATUITĂ', col: '#4ADE80', y: 1185, size: 108, rot: -4 },
      { k: 'chip', t0: A.in5 - .05, t1: A.si6 - .3, y: 330, ph: [[A.in5 - .05, 'package', 'VII LA NOI CU PIESA', 'blue'],
        [A.noi5b - .05, 'magnifying_glass_tilted_left', 'VEDEM ÎN CE STARE E PIESA', 'green']] },
      { k: 'chip', t0: A.si6 - .05, t1: A.mecanica - .3, y: 330, ph: [[A.si6 - .05, 'euro_banknote', 'VALOARE CORECTĂ DE REPARAȚIE', 'green'],
        [A.exact6 - .05, 'check_mark_button', 'EXACT PENTRU PROBLEMA TA', 'green'], [A.nu6 - .05, 'cross_mark', 'NU PENTRU CE CREZI TU CĂ AI', 'red']] },
      { k: 'kin', t: A.corecta6 - .02, dur: 1.3, txt: 'VALOARE CORECTĂ', col: '#4ADE80', y: 1185, size: 108, rot: -4 },
      // ---- motorul pe stand (IMG_1920): schema cauză → efect, sus
      { k: 'schem', t0: A.mecanica - .08, t1: CLIP[3] - .28, top: 268, h: 330, type: 'causeEffect', title: 'SCHEMĂ · CAUZĂ › EFECT', sub: 'DIAGNOZA TURBO DOCTOR',
        P: { sym: ['warning', 'EROARE PE TURBINĂ'], causes: [['gear', 'ACȚIONARE'], ['droplet', 'INJECTOARE'], ['leaf', 'DPF']], sweep: 1.9 },
        stepNames: ['SIMPTOM', 'DIAGNOZA', 'SUCCESUL'],
        steps: [[A.mecanica - .08, 'Mecanica pe motoarele noi e grea', 'r'], [A.diagnosticarea7 - .05, 'Diagnosticarea corectă: verificăm cauzele', ''], [A.cheia7 - .05, 'E cheia succesului reparației', 'g']] },
      { k: 'kin', t: A.cheia7 - .02, dur: 1.5, txt: 'CHEIA SUCCESULUI!', col: '#4ADE80', y: 1040, size: 112, rot: -4 },
      // ---- selfie 2 (IMG_1921): suntem alături de voi
      { k: 'chip', t0: A.tocmai8 - .05, t1: A.orice8 - .3, y: 330, ph: [[A.tocmai8 - .05, 'handshake', 'SUNTEM ALĂTURI DE VOI', 'green']] },
      { k: 'chip', t0: A.orice8 - .05, t1: A.si8b - .3, y: 330, ph: [[A.orice8 - .05, 'warning', 'ORICE PROBLEMĂ AI AVEA', 'yellow'],
        [A.admisie8 - .05, 'gear', 'ADMISIE · INJECȚIE · EVACUARE', 'blue'], [A.turbine8 - .05, 'gear', 'TURBINE · MOTOARE', 'blue'],
        [A.injectoare8 - .05, 'droplet', 'INJECTOARE · POMPE', 'blue'], [A.dpf8 - .05, 'leaf', 'DPF-URI', 'blue'], [A.noi8c - .05, 'round_pushpin', 'NOI SUNTEM AICI', 'green']] },
      { k: 'chip', t0: A.si8b - .05, t1: SEND - .2, y: 330, ph: [[A.si8b - .05, 'stethoscope', 'TOTUL PLEACĂ DE LA DIAGNOZA GRATUITĂ', 'green']] },
      { k: 'kin', t: A.gratuita8 - .02, dur: 1.4, txt: 'DIAGNOZĂ GRATUITĂ', col: '#FFD21F', y: 1185, size: 108, rot: -4 },
      // PHONE (doar dacă Sabin confirmă; regula din 25.10 = fără telefon / site pe video):
      // { k: 'chip', t0: A.numarul8 - .05, t1: SEND - .2, y: 330, ph: [[A.numarul8 - .05, 'phone', '0739 065 065', 'yellow'], [A.site8 - .05, 'globe', 'TURBODOCTOR.RO', 'blue']] },
    ],
    fx: [
      // hook 1: trei impacturi (al doilea = cel mare)
      { k: 'flash', t: B1 - .11, a: .35 }, { k: 'punch', t: B1, a: .07, sh: 14 }, { k: 'glitch', t: B1, d: .12 },
      { k: 'flash', t: B2 - .11, a: .75 }, { k: 'punch', t: B2, a: .16, sh: 34 }, { k: 'glitch', t: B2, d: .2 }, { k: 'shock', t: B2 + .01, x: 540, y: 860, r: 760, n: 2 },
      { k: 'flash', t: B3 - .11, a: .45 }, { k: 'punch', t: B3, a: .08, sh: 16 }, { k: 'shock', t: B3 + .01, x: 540, y: 1075, r: 520, n: 1, col: '#FFD21F' },
      { k: 'glitch', t: HB - .05, d: .14 }, { k: 'punch', t: A.complet1, a: .05 },
      // hook 2: „DAR DE CE?”
      { k: 'flash', t: B4 - .11, a: .6 }, { k: 'punch', t: B4, a: .12, sh: 26 }, { k: 'glitch', t: B4, d: .16 }, { k: 'shock', t: B4 + .01, x: 540, y: 900, r: 640, n: 2, col: '#FF4B4B' },
      { k: 'glitch', t: HEND - .05, d: .14 },
      // restul: accente scurte
      { k: 'glitch', t: A.tocmai2 - .1, d: .12 }, { k: 'punch', t: A.altundeva, a: .05 }, { k: 'punch', t: A.supra4, a: .05 },
      { k: 'glitch', t: A.tocmai5 - .1, d: .12 }, { k: 'punch', t: A.gratuita5, a: .05 }, { k: 'punch', t: A.corecta6, a: .04 },
      { k: 'glitch', t: A.mecanica - .12, d: .12 }, { k: 'punch', t: A.cheia7, a: .05 }, { k: 'glitch', t: A.tocmai8 - .1, d: .12 }, { k: 'punch', t: A.gratuita8, a: .05 },
    ],
    sfx: [[HB - .1, 'whoosh', .6], [HEND - .1, 'whoosh', .6]],
    bursts: [[B2 + .04, 540, 860, 8, 560, 1.7], [B3 + .04, 540, 1075, 4, 420, 1.2], [B4 + .04, 540, 900, 6, 480, 1.4], [A.cheia7 + .05, 540, 620, 6, 320, .8]],
  };
};
