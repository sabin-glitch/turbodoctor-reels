// v2 – DPF Doctor · „Europa schimbă DPF-ul, noi facem DPF OFF” (TikTok 7684636860261469462, târg, voce din off, 16.7 s)
// Footage exactly as filmed, natural pace, no separate hook. Short clip: no stage bar.
// The burned 3-line text („AVANTAJE-DPF OFF / Scrie-ne avantajele…”, 0–10.43 s) can't be inpainted cleanly over the honeycombs,
// so it is covered by our own question card glued to the same spot until the scene change; captions resume right after.
window.REEL_CFG = ({ S0, SEND, TEND, WORDS }) => {
  const nn = s => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]/g, '');
  const near = (x, t) => { const c = WORDS.filter(w => nn(w.text) === nn(x)); if (!c.length) throw new Error('anchor not found: ' + x);
    const b = c.reduce((a, w) => Math.abs(w.os - t) < Math.abs(a.os - t) ? w : a); if (Math.abs(b.os - t) > 1.5) throw new Error('anchor too far: ' + x + ' ' + t + ' -> ' + b.os.toFixed(2)); return b; };
  const W = (x, t) => near(x, t).os, WE = (x, t) => near(x, t).oe;
  const A = {
    toata: W('toată', .96), schimba: W('schimbă', 2.16), topite: W('topite', 4.2), noi: W('noi', 5.46), facem: W('facem', 6.48), offE: WE('OFF', 7.55),
    chiar: W('Chiar', 8.25), raspundeti: W('răspundeți', 10.56), cei: W('cei', 12.24), ce: W('ce', 13.92), avantaje: W('avantaje', 14.16),
  };
  const CUT = 10.43;              // scene change: the old burned text ends here
  const HOOK_OUT = A.noi - .1;
  return {
    hook: { tag: 'ANALIZĂ TEHNICĂ · DPF OFF', l1: 'TOATĂ <span class="c">EUROPA</span>', l1At: A.toata - .05, l2: 'SCHIMBĂ DPF-UL!', l2At: A.schimba - .04, l2Col: '#4ADE80',
      car: 'CÂND E TOPIT', carAt: A.topite - .05, end: HOOK_OUT },
    hideCap: [[0, CUT]],
    tags: { 0: { europa: 'c', schimba: 'g', topite: 'r', romanii: 'y', off: 'r' }, 1: { comentarii: 'c', off: 'r', avantaje: 'y' } },
    items: [
      // our card over the burned question (same place, same size), until the scene change
      { k: 'note', t0: 0, t1: CUT, hard: true, box: [128, 1286, 952, 1552], fs: 54, ico: 'speech_balloon', label: 'ÎNTREBARE PENTRU VOI',
        text: 'Avantaje DPF OFF? <span style="white-space:nowrap">Scrie-ne</span> avantajele acestei proceduri în comentarii.' },
      { k: 'cmp', t0: A.noi - .1, t1: CUT - .1, top: 262, title: 'DPF TOPIT. CE SE FACE?', ico: 'magnifying_glass_tilted_left', aCls: 'ok', bCls: 'bad', big: true,
        a: [A.noi, 'globe', 'EUROPA', 'ÎL SCHIMBĂ'], b: [A.facem - .05, 'scissors', 'ROMÂNIA', 'DPF OFF'] },
      { k: 'chip', t0: CUT, t1: SEND - .05, y: 330, ph: [[CUT, 'speech_balloon', 'RĂSPUNDE-NE ÎN COMENTARII', 'blue'], [A.cei - .05, 'scissors', 'CEI CU DPF OFF:', 'red'],
        [A.ce - .05, 'thinking_face', 'CE AVANTAJE AVEȚI?', 'yellow']] },
    ],
    fx: [
      { k: 'green', t0: A.schimba - .05, t1: A.schimba + .8, silent: true },
      { k: 'punch', t: A.facem, a: .05, sh: 6 }, { k: 'red', t0: A.facem - .05, t1: A.offE + .3, max: 1.4 },
    ],
    sfx: [],
    bursts: [],
  };
};
