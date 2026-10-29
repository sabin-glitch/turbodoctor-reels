// PROMO plătit (29.10.2026): REPARAȚII MOTOARE · compilație din secvențe deja publicate, fiecare cu vocea ei
// Sursa (all.mp4, vezi segs.json): 0 hook = clipul vechi „Reparații motoare” (GLE 2.0 biturbo desfăcut, titlul ars scos cu caption_clean)
// · 1 Mercedes C200 (#0193) · 2 Suzuki SX4 (#0172) · 3 Opel Combo (#0213) — reel-uri deja editate: subtitrările și grafica lor rămân,
// vocea e separată de muzica/SFX-urile lor (UVR), fundalul nu se mărește (bgFix), bara lor de etape e acoperită de `band`
// · 4–5 același clip vechi, selfie: „demontăm, verificăm…” + „diagnoza este complet gratuită” · 6 selfie: „Vă puteți programa…”.
// Revizia 29.10 (Sabin): fără coada scurtă „din Piatra Neamț” de la Opel și un singur „țineți minte” la final (fraza începe cu „Vă puteți programa”).
// Promo: telefonul apare când spune „numărul de telefon” și pe cardul de final (ca la promo injectoare).
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND, TOTAL }) => {
  const SEG = [{"name": "hook", "out_t0": 0.0, "out_t1": 11.2667, "src": "pre_clean.mp4", "src_t0": 0.0}, {"name": "merc", "out_t0": 11.2667, "out_t1": 15.9333, "src": "orig_mercedes_0193.mp4", "src_t0": 2.6333}, {"name": "suz", "out_t0": 15.9333, "out_t1": 28.6333, "src": "orig_suzuki_0172.mp4", "src_t0": 21.8667}, {"name": "opel", "out_t0": 28.6333, "out_t1": 37.8, "src": "orig_opel_0213.mp4", "src_t0": 5.0667}, {"name": "trust", "out_t0": 37.8, "out_t1": 59.2667, "src": "pre_clean.mp4", "src_t0": 108.3333}, {"name": "cta", "out_t0": 59.2667, "out_t1": 64.9667, "src": "pre_clean.mp4", "src_t0": 142.1}];  // din out/segs.json (build_promo_motoare.py)
  const at = n => SEG.find(s => s.name === n);
  const M = at('merc'), Z = at('suz'), O = at('opel'), T = at('trust'), C = at('cta');
  const CASES = [[M, '#1', 'MERCEDES C200', 'MOTOR PE BENZINĂ', 'MERCEDES C200 1.8 COMPRESOR', 'NU DOAR DIESEL'],
                 [Z, '#2', 'SUZUKI SX4 2.0', 'PISTON TOPIT', 'SUZUKI SX4 2.0', 'CAMERĂ ENDOSCOPICĂ'],
                 [O, '#3', 'OPEL COMBO 1.5', 'MOTOR DIN GERMANIA', 'MOTOR OPEL COMBO 1.5 DIESEL', 'DIN GERMANIA']];
  const VEIL = [.30, .30, .44];                          // cât stă estompat începutul fiecărui caz (acoperă finalul hook-ului vechi: #0193 până la src 2.87, #0213 până la 5.50)
  const A = {
    ai: aw(0, 'Ai'), probleme: aw(0, 'probleme'), motorul: aw(0, 'motorul'), blocul: aw(0, 'blocul'), dedicat: aw(0, 'dedicat'), rezolvarea: aw(0, 'rezolvarea'),
    corecta: aw(0, 'corectă'), tale: ew(0, 'tale', 1),
    tineti4: aw(4, 'Țineți'), demontam: aw(4, 'demontăm'), verificam: aw(4, 'verificăm'), diagnosticam: aw(4, 'diagnosticăm'), decidem: aw(4, 'decidem'), apucam: aw(4, 'apucăm'),
    doar: aw(5, 'doar'), sute: aw(5, 'sute'), motor5: aw(5, 'motor'), admisie5: aw(5, 'admisie'), injectie5: aw(5, 'injecție'), evacuare5: aw(5, 'evacuare'),
    diagnoza5: aw(5, 'diagnoza'), gratuita5: aw(5, 'gratuită'),
    programa: aw(6, 'programa'), numarul: aw(6, 'numărul'), site: aw(6, 'site-ul'),
  };
  const items = [], fx = [];
  // ---- HOOK (selfie 0–2.97, apoi motorul desfăcut): „AI PROBLEME” deasupra capului + „CU MOTORUL?” sub bărbie, fața rămâne liberă
  const HE = 89 / 30 - .02;                              // tăietura din clipul vechi: selfie -> motorul (cadrul 89)
  items.push({ k: 'boom', t: -.06, dur: HE + .06, txt: 'AI PROBLEME', y: 322, size: 162, col: '#FFFFFF', from: 3.6, sh: 28, riser: false, bg: 0, cg: 0 });
  items.push({ k: 'boom', t: A.motorul, dur: HE - A.motorul, txt: 'CU MOTORUL?', y: 1352, size: 150, col: '#FFD21F', from: 2.6, riser: false, bg: .75, ca: 18 });
  fx.push({ k: 'punch', t: 0, a: .16, sh: 34 }, { k: 'glitch', t: .02, d: .16 },
          { k: 'shock', t: .02, x: 540, y: 322, r: 760, n: 2 },
          { k: 'flash', t: A.motorul - .1, a: .4 }, { k: 'punch', t: A.motorul, a: .08, sh: 16 }, { k: 'shock', t: A.motorul + .01, x: 540, y: 1352, r: 560, n: 1, col: '#FFD21F' });
  items.push({ k: 'stamp', t: A.blocul, t1: A.dedicat - .25, txt: 'BLOC OPERATOR', y: 560, col: 'blue', s: .92, rot: -7 });
  // eticheta opacă peste locul titlului vechi „Reparații Motoare / Turbo Doctor” (scos cu caption_clean; inpainting-ul lasă urme pe motor și pe păr)
  items.push({ k: 'lbl', t0: HE, t1: M.out_t0, y: 333, ph: [[HE, 'TURBO DOCTOR', 'REPARAȚII MOTOARE', ''],
    [A.dedicat - .05, 'BLOC OPERATOR', 'DEDICAT MOTOARELOR', 'c'], [A.rezolvarea - .05, 'REZOLVARE', 'COMPLETĂ ȘI CORECTĂ', 'g']] });
  // ---- CAZURI (reel-uri deja editate): card de capitol peste fundalul estompat + bara „CAZ REAL” peste bara lor de etape
  CASES.forEach(([S, no, title, sub], i) => {
    fx.push({ k: 'veil', t0: S.out_t0, t1: S.out_t0 + VEIL[i], out: .14 }, { k: 'flash', t: S.out_t0, a: .5 });
    items.push({ k: 'chap', t0: S.out_t0, t1: S.out_t0 + VEIL[i] + .1, kicker: 'CAZ REAL ' + no, title, sub, y: 880 });
  });
  items.push({ k: 'band', t0: M.out_t0, t1: O.out_t1, y: 222, w: 980, h: 76, kicker: 'CAZ REAL',
    ph: CASES.map(([S, no, , , car, sub]) => [S.out_t0, car, sub]) });
  // ---- SELFIE: procesul, clienții mulțumiți, diagnoza gratuită
  fx.push({ k: 'flash', t: T.out_t0, a: .45 }, { k: 'glitch', t: T.out_t0, d: .12 });
  items.push({ k: 'lbl', t0: T.out_t0, t1: T.out_t1, y: 333, ph: [[T.out_t0, 'PROTOCOLUL TURBO DOCTOR', 'REPARAȚII MOTOARE', ''],
    [A.demontam - .08, 'PASUL 1', 'DEMONTĂM', ''], [A.verificam - .05, 'PASUL 2', 'VERIFICĂM', ''], [A.diagnosticam - .05, 'PASUL 3', 'DIAGNOSTICĂM', 'c'],
    [A.decidem - .05, 'PASUL 4', 'DECIDEM', 'c'], [A.apucam - .1, 'PASUL 5', 'ABIA APOI REPARĂM', 'g'],
    [A.sute - .08, 'REZULTATUL', 'SUTE DE CLIENȚI MULȚUMIȚI', 'g'],
    [A.motor5 - .08, 'PROBLEME PE', 'MOTOR', 'c'], [A.admisie5 - .05, 'PROBLEME PE', 'MOTOR · ADMISIE', 'c'],
    [A.injectie5 - .05, 'PROBLEME PE', 'MOTOR · ADMISIE · INJECȚIE', 'c'], [A.evacuare5 - .05, 'PROBLEME PE', 'MOTOR · ADMISIE · INJECȚIE · EVACUARE', 'c'],
    [A.diagnoza5 - .05, 'LA TURBO DOCTOR', 'DIAGNOZA ESTE', '']] });
  items.push({ k: 'stamp', t: A.gratuita5 - .05, t1: A.programa - .1, txt: 'DIAGNOZĂ GRATUITĂ', y: 333, col: 'green', s: 1, rot: -5 });  // până intră telefonul
  // ---- CTA: telefonul și site-ul exact când le spune
  fx.push({ k: 'flash', t: C.out_t0, a: .3 }, { k: 'punch', t: C.out_t0, a: .06, sh: 10 });
  items.push({ k: 'eq', t0: A.programa - .12, t1: SEND + .2, top: 196, ico: 'phone', title: 'PROGRAMEAZĂ-TE', sub: 'DIAGNOZĂ GRATUITĂ',
    lines: [[A.numarul - .02, '0739 065 065', 'big y'], [A.site - .02, 'TURBODOCTOR.RO', 'y']] });
  // ---- cardul de final standard + telefonul (doar pe promo)
  items.push({ k: 'eq', t0: TEND + 2.45, t1: TOTAL + 1, top: 1160, ico: 'phone', title: 'PROGRAMEAZĂ-TE', sub: 'TELEFON · SITE',
    lines: [[TEND + 2.7, '0739 065 065', 'big y'], [TEND + 3.1, 'TURBODOCTOR.RO', 'y']] });
  return {
    hook: null,
    stages: null,
    bgFix: [[M.out_t0, O.out_t1]],
    hideCap: [[0, HE], [M.out_t0, Math.max(O.out_t1 + .3, A.tineti4 - .06)]],  // + coada ultimei bucăți de subtitrare din cazul Opel
    tags: {
      0: { probleme: 'r', motorul: 'c', masinii: '', blocul: 'y', operator: 'y', motoarelor: 'c', completa: 'g', corecta: 'g' },
      4: { demontam: 'c', verificam: 'c', diagnosticam: 'c', decidem: 'c', treaba: 'g' },
      5: { multumiti: 'g', motor: 'c', admisie: 'c', injectie: 'c', evacuare: 'c', diagnoza: 'g', complet: 'g', gratuita: 'g' },
      6: { programa: 'g', numarul: 'y', telefon: 'y', site: 'y', turbodoctorro: 'y' },
    },
    items, fx, sfx: [[0, 'boom', 1], [.02, 'crack', .55]], bursts: [[.04, 540, 322, 10, 360, 1.1], [A.motorul, 540, 1352, 8, 300, 1]],
  };
};
