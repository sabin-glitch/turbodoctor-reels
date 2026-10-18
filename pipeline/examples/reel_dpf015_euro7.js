// v2 – DPF Doctor · „Euro 7: antipoluarea distruge motorul?” (TikTok 7686187533075664131, 2:45, răspuns la comentariu, la târg, sistemul Euro 7 expus)
// Footage exactly as filmed (exhaust after-treatment display + selfie parts), natural pace, no separate hook.
// The TikTok reply bubble is on screen the whole clip: our card covers it and, after the hook, becomes the „PE SCURT” panel synced with what he says.
// Hook lines in the caption zone (captions hidden meanwhile); nothing over his face, nothing in the bottom band.
window.REEL_CFG = ({ S0, SEND, TEND, WORDS }) => {
  const nn = s => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]/g, '');
  const near = (x, t) => { const c = WORDS.filter(w => nn(w.text) === nn(x)); if (!c.length) throw new Error('anchor not found: ' + x);
    const b = c.reduce((a, w) => Math.abs(w.os - t) < Math.abs(a.os - t) ? w : a); if (Math.abs(b.os - t) > 1.5) throw new Error('anchor too far: ' + x + ' ' + t + ' -> ' + b.os.toFixed(2)); return b; };
  const W = (x, t) => near(x, t).os, WE = (x, t) => near(x, t).oe;
  const A = {
    sistemul: W('Sistemul', 1.27), euro: W('Euro', 4.13), dieselE: WE('diesel', 4.72), nu5: W('nu', 5.92), decat: W('decât', 11.61), haideti: W('Haideți', 16.44), n10000: W('10.000', 22.0),
    nu25: W('Nu', 25.77), ignorarea: W('Ignorarea', 29.77), dpful37: W('DPF-ul', 37.24), daca44: W('Dacă', 44.25), asta55: W('Asta', 55.61), problema61: W('problema', 61.39), nu67: W('Nu', 67.55),
    sunt68: W('Sunt', 68.38), n400: W('400-500', 70.85), sunt76: W('Sunt', 76.31), au81: W('au', 81.43), trebuie84: W('Trebuie', 84.28), ele92: W('ele', 92.88), asta104: W('Asta', 104.79),
    in108: W('În', 108.62), dar128: W('Dar', 128.17), tapii: W('țapii', 132.37), si137: W('și', 137.61), si155: W('Și', 155.42),
  };
  const HOOK_OUT = A.nu5 - .1;
  const N = (t, txt, fs = 38, ico = 'stethoscope') => [t, 'PE SCURT', txt, fs, ico];
  return {
    hook: { tag: 'RĂSPUNS LA COMENTARIU', tagY: 1295, l1: 'SISTEMUL <span class="c">EURO 7</span>', l1At: A.sistemul - .05, l2: 'DISTRUGE MOTORUL?', l2At: A.euro - .04, l2Col: '#FF3B30',
      w: 900, l1Y: 1395, l2Y: 1515, end: HOOK_OUT },
    hideCap: [[0, HOOK_OUT - .05]],
    tags: {
      0: { euro: 'c', 7: 'c', diesel: 'c' }, 1: { nu: 'g', distruge: 'r', distrug: 'r' }, 2: { prost: 'r', intretinute: 'r', nereparate: 'r', 10000: 'y' },
      3: { nu: 'g', ignorarea: 'r', mentenantei: 'y', distruge: 'r' }, 4: { statica: 'c', regenerarea: 'g', corect: 'g', ok: 'g' }, 6: { infundarea: 'r' },
      7: { distruge: 'r', nu: 'g' }, 8: { active: 'g' }, 9: { distruse: 'r', motor: 'y' }, 11: { oul: 'y', gaina: 'y', n57le: 'c' }, 12: { tapii: 'y', ispasitori: 'y' },
      13: { complex: 'c' }, 15: { complicat: 'y', mistifici: 'r' },
    },
    items: [
      { k: 'note', t0: 0, t1: SEND, hard: true, box: [66, 308, 540, 550], fs: 38,
        ph: [[0, 'COMENTARIU', '„Să vedeți motoare picate la 20k km.”', 44, 'speech_balloon'],
          N(A.nu5 - .05, 'Euro 7 <b>nu va distruge motoare</b>, cum nici sistemele vechi nu distrug.', 36, 'check_mark_button'),
          N(A.decat - .05, 'Doar mașinile <b style="color:#C81E2C">prost întreținute</b>, nereparate la timp.', 36, 'warning'),
          N(A.haideti - .05, 'Din experiența a <b>10.000 de DPF-uri curățate</b>.', 38, 'soap'),
          N(A.nu25 - .05, 'Nu antipoluarea strică motorul, ci <b style="color:#C81E2C">ignorarea ei și a mentenanței</b>.', 34, 'wrench'),
          N(A.dpful37 - .05, 'DPF-ul e o piesă statică. <b style="color:#15803D">Regenerare corectă = totul OK.</b>', 36, 'gear'),
          N(A.daca44 - .05, 'Fără întreținere, <b>motorul iese din parametri</b>, apoi DPF-ul se înfundă.', 34, 'warning'),
          N(A.problema61 - .05, '„DPF-ul distruge motorul”? <b style="color:#C81E2C">NU.</b>', 42, 'cross_mark'),
          N(A.sunt68 - .05, 'Mașini la <b style="color:#15803D">400–500.000 km</b> cu antipoluarea activă.', 38, 'automobile'),
          N(A.sunt76 - .05, 'Cele „moarte” la 100.000 km <b>au mereu alte motive</b>.', 38, 'magnifying_glass_tilted_left'),
          N(A.trebuie84 - .05, 'Degradarea <b>pleacă de la motor</b>, nu de la DPF.', 40, 'gear'),
          N(A.asta104 - .05, 'Oul sau găina? <b>Întâi motorul</b>, apoi DPF-ul.', 40, 'thinking_face'),
          N(A.dar128 - .05, 'DPF-ul e <b>țapul ispășitor</b>: cel mai greu de înțeles sistem.', 36, 'thinking_face'),
          N(A.si155 - .05, 'Ce e complicat <b>e ușor de învinovățit</b>.', 40, 'brain')] },
    ],
    fx: [
      { k: 'punch', t: A.euro, a: .04, sh: 4 },
      { k: 'green', t0: A.nu5 - .05, t1: A.nu5 + .8, silent: true },
      { k: 'red', t0: A.ignorarea - .05, t1: A.ignorarea + 1.0, max: 1.0 },
      { k: 'punch', t: A.nu67, a: .06, sh: 8 }, { k: 'red', t0: A.problema61 - .05, t1: A.nu67, max: 1.4 },
      { k: 'green', t0: A.n400 - .05, t1: A.n400 + .9, silent: true },
      { k: 'punch', t: A.tapii, a: .04, sh: 5 },
    ],
    sfx: [],
    bursts: [],
  };
};
