// v2 – „Un injector injectează de 3 ori”: explicație animată (preinjecție · injecție principală · postinjecție + regenerarea DPF)
// Sursa este animația 3D randată cadru cu cadru (reelwork/reel.html), nu o filmare: banda cu momentul injecției, etichetele de pe piese
// și citirea temperaturii sunt desenate în animație; compozitorul adaugă hook-ul, bara de etape, cardurile de capitol, accentele și subtitrările.
// Narator (fără prezentator în cadru) -> fundalul rămâne fix (bgFix), ca desenul tehnic să rămână clar.
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND }) => {
  const L = (i, w, k) => aw(i, w, k);
  const HK = aw(2, 'Prima') - .45;               // sfârșitul hook-ului = tăietura din animație
  const BEAT = { pre: .07 * HK, main: .34 * HK, post: .75 * HK };  // cele 3 pulverizări din hook (vo/info.json)
  const K1 = aw(7, 'bate,'), K2 = aw(20, 'bate.');  // „motorul bate”: aprinderea bruscă din animație pornește exact aici
  const TD = aw(21, 'nu') - .05;                 // bordul cu martorul DPF (banda din animație se stinge chiar înainte)
  const CY = 588;                                // rândul de chip-uri: sub banda „momentul injecției”, deasupra piesei
  const items = [], fx = [];

  // ---- capitolele: cele trei injecții
  [[aw(2, 'Prima'), 'INJECȚIA 1 / 3', 'PREINJECȚIA', 'PREGĂTEȘTE ARDEREA'],
   [aw(8, 'A'), 'INJECȚIA 2 / 3', 'INJECȚIA PRINCIPALĂ', 'DĂ PUTEREA'],
   [aw(12, 'A'), 'INJECȚIA 3 / 3', 'POSTINJECȚIA', 'CURĂȚĂ FILTRUL DE PARTICULE']].forEach(([t, k, title, sub]) => {
    const t0 = t - .35, D = 1.75;
    fx.push({ k: 'veil', t0, t1: t0 + D - .05, out: .2 }, { k: 'flash', t: t0, a: .35 }, { k: 'glitch', t: t0, d: .12 });
    items.push({ k: 'chap', t0, t1: t0 + D, kicker: k, title, sub, y: 880 });
  });

  // ---- 1 · preinjecția: ardere lină
  items.push({ k: 'chip', t0: L(5, 'arde') - .05, t1: aw(7, 'Când') - .35, y: CY,
    ph: [[L(5, 'arde') - .05, 'check_mark_button', 'ARDERE LINĂ', 'green'], [L(6, 'silențios') - .05, 'check_mark_button', 'MOTOR MAI SILENȚIOS', 'green'], [L(6, 'poluează') - .05, 'leaf', 'MAI PUȚINE NOXE', 'green']] });
  // ---- fără preinjecție: motorul bate
  items.push({ k: 'chip', t0: L(7, 'preinjecția') - .05, t1: K1 - .12, y: CY, ph: [[L(7, 'preinjecția') - .05, 'warning', 'PREINJECȚIE GREȘITĂ', 'red']] });
  items.push({ k: 'kin', t: K1, dur: .78, txt: 'BATE!', col: '#FF3B30', y: 660, size: 250, rot: -5 });
  items.push({ k: 'chip', t0: L(7, 'mai', 1) + .3, t1: aw(8, 'A') - .5, y: CY, ph: [[L(7, 'mai', 1) + .3, 'cold_face', 'MAI ALES LA RECE', 'blue']] });
  fx.push({ k: 'flash', t: K1, a: .55 }, { k: 'shock', t: K1, x: 540, y: 1130, r: 620, n: 2, col: '#FFD21F', col2: '#FF4B4B' });

  // ---- 2 · injecția principală: puterea
  items.push({ k: 'kin', t: L(11, 'împing') - .02, dur: 1.2, txt: 'PUTERE', col: '#FFD21F', y: 650, size: 210, rot: -4 });

  // ---- 3 · postinjecția și regenerarea
  items.push({ k: 'chip', t0: L(13, 'doar') - .05, t1: aw(14, 'Injectorul') - .3, y: 574, ph: [[L(13, 'doar') - .05, 'broom', 'DOAR LA CURĂȚAREA FILTRULUI', 'yellow']] });
  items.push({ k: 'chip', t0: L(15, 'nu') - .05, t1: ew(15, 'cilindru.') + .2, y: CY, ph: [[L(15, 'nu') - .05, 'cross_mark', 'NU ARDE ÎN CILINDRU', 'red']] });
  items.push({ k: 'kin', t: L(18, 'regenerarea.') - .02, dur: 1.2, txt: 'REGENERARE', col: '#4ADE80', y: 598, size: 150, rot: -3 });

  // ---- concluzia: ce se întâmplă cu un injector uzat
  items.push({ k: 'chip', t0: L(20, 'Fără') - .05, t1: K2 - .12, y: CY, ph: [[L(20, 'Fără') - .05, 'warning', 'FĂRĂ PREINJECȚIE CORECTĂ', 'red']] });
  items.push({ k: 'kin', t: K2, dur: .68, txt: 'BATE!', col: '#FF3B30', y: 660, size: 250, rot: -5 });
  fx.push({ k: 'flash', t: K2, a: .55 }, { k: 'shock', t: K2, x: 540, y: 1130, r: 620, n: 2, col: '#FFD21F', col2: '#FF4B4B' });
  items.push({ k: 'chip', t0: L(21, 'Fără') - .05, t1: TD - .4, y: CY, ph: [[L(21, 'Fără') - .05, 'warning', 'FĂRĂ POSTINJECȚIE CORECTĂ', 'red']] });
  items.push({ k: 'dash', t0: TD, t1: SEND - .2, x: 540, y: 410, s: .78, chime: .45,
    lamps: [[L(21, 'regenerează') + .3, 'dpf', 'FILTRU DPF'], [L(21, 'și') + .1, 'engine', 'MOTOR']] });
  items.push({ k: 'stamp', t: L(21, 'înfundă.') + .05, t1: SEND - .25, y: 985, txt: 'FILTRU ÎNFUNDAT', col: 'red', s: .86, rot: -7 });

  return {
    hook: { tag: 'LECȚIE DE ANATOMIE · INJECȚIA DIESEL', l1: 'UN INJECTOR INJECTEAZĂ', l1At: .05, l2: 'DE 3 ORI', l2At: aw(0, 'trei') - .02, l2Col: '#FFD21F',
      chips: [['droplet', '1 · PREINJECȚIE', BEAT.pre], ['fire', '2 · PRINCIPALĂ', BEAT.main], ['dashing_away', '3 · POSTINJECȚIE', BEAT.post]],
      chipsAt: .25, chipsY: 676, y: -22, end: HK },
    stages: [[HK + .45, 'PREINJECȚIE'], [aw(8, 'A'), 'PRINCIPALĂ'], [aw(12, 'A'), 'POSTINJECȚIE'], [aw(19, 'De'), 'UZURĂ']],
    bgFix: [[0, SEND]],
    sfx: [[L(18, 'regenerarea.'), 'shimmer', .5]],
    items, fx,
    tags: {
      0: { trei: 'y', ori: 'y', singura: 'y' },
      2: { preinjectia: 'y' }, 3: { foarte: 'y', mica: 'y' }, 4: { prima: 'y', incalzeste: 'y' },
      5: { lin: 'g', explozie: 'r' }, 6: { silentios: 'g', putin: 'g' },
      7: { preinjectia: 'y', bate: 'r', rece: 'c' },
      8: { principala: 'y' }, 9: { puterea: 'y' }, 10: { bari: 'y', microni: 'y' }, 11: { arde: 'y' },
      12: { postinjectia: 'y' }, 13: { curatat: 'g' }, 14: { tarziu: 'y', jos: 'y' }, 15: { nu: 'r' },
      16: { catalizator: 'c' }, 17: { grade: 'y', funinginea: 'r', arde: 'g' }, 18: { regenerarea: 'g' },
      19: { uzat: 'r', consum: 'y' }, 20: { preinjectie: 'y', bate: 'r' }, 21: { postinjectie: 'y', regenereaza: 'r', infunda: 'r' },
    },
  };
};
