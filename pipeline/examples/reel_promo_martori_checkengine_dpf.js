// v2 – PROMO plătit (Facebook + TikTok, 28.10.2026): „Ai martorul Check Engine sau DPF aprins în bord?” → diagnoză gratuită la Turbo Doctor
// 3 clipuri lipite în ordinea filmării, fără tăieturi: 0 IMG_1861 (selfie, hook) · 6.72 IMG_1862 (DPF secționat, motor, turbo) · 30.62 IMG_1863 (selfie, oferta)
// Hook cerut de Sabin: martorii Check Engine și DPF se aprind în bord exact pe „acești martori aprinși în bord”.
// Promo cu programare (cerut explicit): site + telefon pe video când le spune și pe cardul de final (reel-urile organice rămân fără CTA).
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND, TOTAL }) => {
  const A = {
    acesti: aw(0, 'acești'), martori: aw(0, 'martori'), aprinsi: aw(0, 'aprinși'), ei: aw(0, 'Ei'), dpful: aw(0, 'DPF-ul'),
    cam: aw(1, 'Cam'), un1: aw(1, 'un'), dpf1: aw(1, 'DPF'), functionarea: aw(1, 'Funcționarea'), motorului: aw(1, 'motorului'), filtrul: aw(1, 'filtrul'),
    defectiuni: aw(2, 'defecțiuni'), catastrofale: aw(2, 'catastrofale'), in2: aw(2, 'În'), suferit: aw(2, 'suferit'), iar2: aw(2, 'iar'),
    motorul: aw(2, 'motorul'), distruge: aw(2, 'distruge'), cauza: aw(2, 'cauza'), contra: aw(2, 'contrapresiunii'), supra: aw(2, 'supraîncălzirii'), generate: aw(2, 'generate'),
    turbo3: aw(3, 'Turbo'), catastrofe: aw(3, 'catastrofe'), mersul: aw(3, 'mersul'), tocmai: aw(3, 'Tocmai'), diagnoza3: aw(3, 'diagnoza'), gratuita3: aw(3, 'gratuită'),
    va3: aw(3, 'va'),
    pentru4: aw(4, 'Pentru'), profesionist: aw(4, 'profesionist'), diagnosticare: aw(4, 'diagnosticare'), oferita: aw(4, 'oferită'), clar: aw(4, 'clar'), costul: aw(4, 'costul'),
    daca5: aw(5, 'Dacă'), programezi: aw(5, 'programezi'), site: aw(5, 'site'), numarul: aw(5, 'numărul'), si5: aw(5, 'și'),
    ce5: aw(5, 'ce'), cat5: aw(5, 'cât'), cat5b: aw(5, 'cât', 1),
  };
  const CLIP = [0, 6.72, 30.62];
  const BOOM_END = A.diagnoza3 + 2.95;
  return {
    hook: null,
    stages: null,
    tags: {
      0: { martori: 'r', aprinsi: 'r', bord: 'y', dpful: 'c' },
      1: { dpf: 'c', incarcat: 'r', sectiune: 'c' },
      2: { catastrofale: 'r', suferit: 'r', distruge: 'r', contrapresiunii: 'r', supraincalzirii: 'r' },
      3: { catastrofe: 'r', diagnoza: 'g', complet: 'g', gratuita: 'g' },
      4: { profesionist: 'g', diagnosticare: 'g', profesionala: 'g', gratuit: 'g', vizibilitate: 'y', costul: 'y', reparatii: 'y' },
      5: { diagnoza: 'g', gratuita: 'g', programezi: 'g', site: 'y', telefon: 'y', dureaza: 'y', costa: 'y' },
    },
    items: [
      // HOOK (IMG_1861): bordul cu martorii Check Engine + DPF, deasupra capului, unde arată cu degetul
      { k: 'dash', t0: -.3, t1: CLIP[1] - .3, y: 338, s: .96, shrink: [A.ei - .1, .9, -8], gap: 300,
        lamps: [[A.acesti - .02, 'engine', 'CHECK ENGINE'], [A.martori - .02, 'dpf', 'DPF']], pulse: [A.aprinsi - .02], focus: [A.dpful - .03, 1, 'FILTRU DE PARTICULE'] },

      // IMG_1862: DPF-ul tăiat în secțiune
      { k: 'scan', t0: CLIP[1] + .2, t1: 9.25, track: 'track_dpf', box: [0, -25, 430, 690], lab: 'SECȚIUNE PRIN DPF', labBelow: true },
      { k: 'def', t0: A.un1 - .05, t1: A.functionarea - .35, top: 205, term: 'DPF · FILTRUL DE PARTICULE', text: 'Reține funinginea din gazele de evacuare, apoi o arde la regenerare.' },
      // motorul cu DPF încărcat → fișa pacientului
      { k: 'file', t0: A.functionarea - .1, t1: A.in2 - .35, top: 205, ecg: 'crit', rows: [
        [A.functionarea, 'PACIENT', 'Motor diesel cu DPF', 'c', 'automobile'],
        [A.motorului + .35, 'SIMPTOME', 'Check Engine + DPF', 'r', 'warning'],
        [A.filtrul, 'DIAGNOSTIC', 'DPF încărcat', 'r', 'magnifying_glass_tilted_left'],
        [A.defectiuni, 'RISC', 'Defecțiuni catastrofale', 'r', 'collision']], stamp: [A.catastrofale + .05, 'GRAV', 'red'] },
      // riscul 1: turbosuflanta (turbo secționat pe masă)
      { k: 'chip', t0: A.in2 - .05, t1: A.iar2 - .3, y: 330, ph: [[A.in2 - .05, 'warning', 'RISCUL 1: TURBOSUFLANTA', 'yellow'], [A.suferit - .05, 'collision', 'TURBO AVARIAT', 'red']] },
      { k: 'scan', t0: 19.55, t1: 21.35, track: 'track_turbo', box: [90, -25, 680, 560], lab: 'SCANARE TURBO...', lab2: 'TURBO ÎN PERICOL', at2: A.suferit - .04 },
      // riscul 2: motorul
      { k: 'chip', t0: A.iar2 - .05, t1: A.distruge - .25, y: 330, ph: [[A.iar2 - .05, 'warning', 'RISCUL 2: ÎN CAZURI EXTREME', 'yellow'], [A.motorul - .05, 'gear', 'MOTORUL', 'red']] },
      { k: 'stamp', t: A.distruge - .03, t1: A.cauza - .45, y: 380, txt: 'MOTOR DISTRUS', col: 'red', s: .92, rot: -8 },
      // de ce: contrapresiune + supraîncălzire pe evacuare
      { k: 'schem', t0: A.cauza - .1, t1: CLIP[2] - .2, top: 200, h: 370, type: 'dpfBackpressure', title: 'CE SE ÎNTÂMPLĂ PE EVACUARE', sub: 'DPF ÎNFUNDAT',
        stepNames: ['CAUZA', 'EFECT 1', 'EFECT 2', 'REZULTAT'],
        steps: [[A.cauza - .1, 'DPF înfundat: gazele nu mai pot ieși', 'r', 0], [A.contra, 'Contrapresiune: gazele apasă înapoi', 'r', 1],
          [A.supra, 'Supraîncălzire pe evacuare', 'y', 2], [A.generate, 'Turbo și motor în pericol', 'r', 3]] },

      // IMG_1863 (selfie): ce am văzut la Turbo Doctor
      { k: 'chip', t0: A.turbo3 - .05, t1: A.tocmai - .3, y: 330, ph: [[A.turbo3 - .05, 'stethoscope', 'LA TURBO DOCTOR', 'blue'], [A.catastrofe - .05, 'collision', 'AM VĂZUT CATASTROFE', 'red'],
        [A.mersul - .05, 'warning', 'MERS EXCESIV CU PROBLEME LA DPF', 'red']] },
      // oferta: DIAGNOZĂ ... GRATUITĂ! (boom pe fiecare cuvânt)
      { k: 'boom', t: A.diagnoza3, dur: BOOM_END - A.diagnoza3, txt: 'DIAGNOZĂ', y: 224, size: 112, col: '#FFFFFF', from: 2.8, sh: 14, ca: 18, riser: false, bg: .6, glow: 'rgba(98,216,255,.5)' },
      { k: 'boom', t: A.gratuita3, dur: BOOM_END - A.gratuita3, txt: 'GRATUITĂ!', y: 380, size: 142, col: '#4ADE80', from: 3.6, sh: 26, ca: 28, bg: 1, glow: 'rgba(74,222,128,.6)' },
      { k: 'chip', t0: BOOM_END + .05, t1: A.pentru4 - .3, y: 330, ph: [[BOOM_END + .05, 'calendar', 'GRATUITĂ DE ANI DE ZILE', 'green'], [Math.max(BOOM_END + .6, A.va3 - .05), 'check_mark_button', 'ȘI DE ACUM ÎNCOLO', 'green']] },
      { k: 'chip', t0: A.pentru4 - .05, t1: A.daca5 - .3, y: 330, ph: [[A.pentru4 - .05, 'person_raising_hand', 'VII LA UN PROFESIONIST', 'blue'], [A.diagnosticare - .05, 'stethoscope', 'DIAGNOZĂ PROFESIONALĂ', 'blue'],
        [A.oferita - .05, 'check_mark_button', 'OFERITĂ GRATUIT', 'green'], [A.clar - .05, 'eyes', 'VEZI CLAR CE AI DE FĂCUT', 'blue'], [A.costul - .05, 'money_bag', 'ȘI COSTUL REPARAȚIEI', 'yellow']] },
      { k: 'chip', t0: A.daca5 - .05, t1: A.site - .62, y: 330, ph: [[A.daca5 - .05, 'stethoscope', 'VREI O DIAGNOZĂ GRATUITĂ?', 'green'], [A.programezi - .05, 'calendar', 'PROGRAMEAZĂ-TE', 'green']] },
      // programare: site + telefon, mari, exact când le spune
      { k: 'eq', t0: A.site - .32, t1: A.si5 - .3, top: 196, ico: 'calendar', title: 'PROGRAMEAZĂ-TE', sub: 'DIAGNOZĂ GRATUITĂ',
        lines: [[A.site - .15, 'turbodoctor.ro', 'c'], [A.numarul - .1, '0739 065 065', 'big y']] },
      // ce afli la diagnoză
      { k: 'chip', t0: A.si5 - .05, t1: SEND - .15, y: 330, ph: [[A.si5 - .05, 'magnifying_glass_tilted_left', 'AFLI EXACT:', 'blue'], [A.ce5 - .05, 'magnifying_glass_tilted_left', 'CE PROBLEMĂ ARE MAȘINA', 'blue'],
        [A.cat5 - .05, 'stopwatch', 'CÂT DUREAZĂ', 'blue'], [A.cat5b - .05, 'money_bag', 'CÂT COSTĂ REPARAȚIA', 'yellow']] },
      // cardul de final standard + programarea (doar pe acest promo)
      { k: 'eq', t0: TEND + 2.55, t1: TOTAL + 1, top: 1160, ico: 'calendar', title: 'PROGRAMEAZĂ-TE ACUM', sub: 'DIAGNOZĂ GRATUITĂ',
        lines: [[TEND + 2.75, 'turbodoctor.ro', 'c'], [TEND + 3.05, '0739 065 065', 'big y']] },
    ],
    fx: [
      { k: 'punch', t: A.aprinsi, a: .05, sh: 8 }, { k: 'punch', t: A.dpful, a: .06, sh: 10 },
      { k: 'glitch', t: CLIP[1] - .04, d: .12 }, { k: 'glitch', t: CLIP[2] - .04, d: .12 },
      { k: 'flash', t: A.catastrofale - .06, a: .3 }, { k: 'punch', t: A.catastrofale + .05, a: .08, sh: 16 },
      { k: 'punch', t: A.suferit, a: .06, sh: 10 },
      { k: 'flash', t: A.distruge - .14, a: .45 }, { k: 'punch', t: A.distruge, a: .12, sh: 26 }, { k: 'glitch', t: A.distruge, d: .16 },
      { k: 'shock', t: A.distruge + .01, x: 540, y: 380, r: 560, n: 1, col: '#FF4B4B' },
      { k: 'flash', t: A.diagnoza3 - .1, a: .35 }, { k: 'punch', t: A.diagnoza3, a: .06, sh: 12 },
      { k: 'flash', t: A.gratuita3 - .11, a: .65 }, { k: 'punch', t: A.gratuita3, a: .14, sh: 30 }, { k: 'glitch', t: A.gratuita3, d: .2 },
      { k: 'shock', t: A.gratuita3 + .01, x: 540, y: 372, r: 640, n: 2, col: '#4ADE80', col2: '#FFFFFF' },
    ],
    sfx: [[CLIP[1] - .1, 'whoosh', .45], [17.55, 'whoosh', .5], [21.45, 'whoosh', .5], [CLIP[2] - .1, 'whoosh', .45], [A.programezi, 'ding', .4],
      [A.numarul - .1, 'impact', .4], [TEND + 3.05, 'impact', .4]],
    bursts: [[A.gratuita3 + .04, 540, 372, 8, 460, 1.4], [A.distruge + .03, 540, 380, 5, 360, .9]],
  };
};
