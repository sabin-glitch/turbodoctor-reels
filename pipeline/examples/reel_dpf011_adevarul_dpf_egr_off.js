// v2 – DPF Doctor · „Adevărul despre DPF OFF, EGR OFF” (TikTok 7677138986413985046, 2:18, răspuns la comentariu, selfie afară)
// Footage exactly as filmed, natural pace, no separate hook. The face fills the centre of the frame, the TikTok reply bubble the top-left
// for the whole clip: our card covers the bubble and, after the hook, the same card becomes the „PE SCURT” panel (summary of what he says).
// Hook lines in the caption zone (captions hidden meanwhile); nothing over the face, nothing in the bottom band.
window.REEL_CFG = ({ S0, SEND, TEND, WORDS }) => {
  const nn = s => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]/g, '');
  const near = (x, t) => { const c = WORDS.filter(w => nn(w.text) === nn(x)); if (!c.length) throw new Error('anchor not found: ' + x);
    const b = c.reduce((a, w) => Math.abs(w.os - t) < Math.abs(a.os - t) ? w : a); if (Math.abs(b.os - t) > 1.5) throw new Error('anchor too far: ' + x + ' ' + t + ' -> ' + b.os.toFixed(2)); return b; };
  const W = (x, t) => near(x, t).os, WE = (x, t) => near(x, t).oe;
  const A = {
    era: W('Era', .6), din: W('Din', 4.22), toti: W('toți', 6.27), ca: W('ca', 7.48), lipsa: W('Lipsa', 11.99), in23: W('În', 23.03), nu26: W('nu', 26.91), carpesti: W('cârpești', 28.03),
    problemele: W('problemele', 29.79), dar: W('Dar', 30.91), in37: W('În', 37.45), cel: W('cel', 39.69), dacaNai: W('Dacă', 42.01), strice: W('strice', 45.95), daca50: W('Dacă', 50.71),
    cand60: W('Când', 60.54), in66: W('În', 66.62), cadavre: W('cadavre', 75.81), rotiE: WE('roți', 77.01), cand80: W('Când', 80.37), cand87: W('Când', 87.01), si94: W('Și', 94.14),
    constiinta: W('conștiința', 96.6), nu102: W('nu', 102.51), si105: W('Și', 105.59), aerul: W('aerul', 110.94), asta116: W('Asta', 116.63), si123: W('și', 123.16), regulile: W('regulile', 123.95),
    si127: W('Și', 127.83), scurtaturi: W('scurtături', 129.31), inteligentE: WE('inteligent', 130.75), esti: W('Ești', 131.93), needucat: W('needucat', 134.0),
  };
  const HOOK_OUT = A.ca + .45;
  const NOTE = (t, txt, fs = 40, ico = 'stethoscope') => [t, 'PE SCURT', txt, fs, ico];
  return {
    hook: { tag: 'RĂSPUNS LA COMENTARIU', tagY: 1295, l1: 'ADEVĂRUL DESPRE', l1At: A.era - .05, l2: 'DPF OFF & EGR OFF', l2At: A.din - .04, l2Col: '#FF3B30',
      w: 900, l1Y: 1395, l2Y: 1515, end: HOOK_OUT },
    hideCap: [[0, HOOK_OUT - .05]],
    tags: {
      2: { anulezi: 'r', egr: 'r', dpf: 'r', rezolvi: 'r', nimic: 'r', carpesti: 'r' }, 3: { sanatos: 'g', vanzare: 'g' }, 4: { capat: 'y', lume: 'y' }, 5: { clasa: 'y' },
      6: { off: 'r', egr: 'r', dpf: 'r' }, 7: { cadavre: 'r', roti: 'r', diagnoza: 'r', stele: 'y' }, 9: { egrul: 'r', dpful: 'r', anulat: 'r', afecteaza: 'r' },
      10: { aerul: 'c', aglomerat: 'y' }, 12: { regulile: 'y', toti: 'y', scurtaturi: 'r', inteligent: 'r' }, 13: { needucat: 'r', simple: 'y' },
    },
    items: [
      { k: 'note', t0: 0, t1: SEND, hard: true, box: [80, 199, 580, 574], fs: 40,
        ph: [[0, 'COMENTARIU', '„EGR, DPF OFF... și fericire, bucurie, liniște... Conștientizare umană.”', 44, 'speech_balloon'],
          NOTE(A.in23 - .05, 'Anulezi EGR / DPF? <b>Nu rezolvi nimic</b>, doar <b style="color:#C81E2C">cârpești o problemă</b>.'),
          NOTE(A.problemele - .05, 'De multe ori, <b>problema e în altă parte</b>.', 44, 'magnifying_glass_tilted_left'),
          NOTE(A.cel - .05, 'Nu ai bani de piese? <b style="color:#15803D">Cel mai sănătos: vinde mașina.</b>', 40, 'automobile'),
          NOTE(A.strice - .05, 'Se vor strica și alte piese, <b>pe care n-ai cum să le anulezi</b>.', 40, 'warning'),
          NOTE(A.daca50 - .05, 'Nu e capătul lumii: <b>mai scazi o clasă</b>, apoi mai crești.', 40, 'handshake'),
          NOTE(A.in66 - .05, 'Cu DPF OFF, EGR OFF: <b style="color:#C81E2C">„cadavre pe roți”</b>.', 44, 'warning'),
          NOTE(A.cand80 - .05, 'Totul anulat: <b>nici diagnoza nu se mai poate face corect</b>.', 40, 'stethoscope'),
          NOTE(A.cand87 - .05, 'Alt mecanic <b>nu ghicește din stele</b> ce s-a făcut înainte.', 40, 'thinking_face'),
          NOTE(A.constiinta - .05, 'DPF / EGR anulat <b>nu te afectează doar pe tine</b>.', 42, 'leaf'),
          NOTE(A.si105 - .05, 'În orașe aglomerate contează mult <b>pentru aerul tuturor</b>.', 40, 'leaf'),
          NOTE(A.regulile - .05, '<b>Regulile sunt pentru toți</b>, nu numai pentru unii.', 42, 'handshake'),
          NOTE(A.si127 - .05, 'Scurtăturile <b style="color:#C81E2C">nu sunt inteligente</b>.', 46, 'cross_mark')] },
    ],
    fx: [
      { k: 'punch', t: A.din, a: .04, sh: 4 },
      { k: 'punch', t: A.carpesti, a: .04, sh: 5 }, { k: 'red', t0: A.carpesti - .05, t1: A.carpesti + 1.0, max: 1.0 },
      { k: 'green', t0: A.cel - .05, t1: A.cel + .9, silent: true },
      { k: 'punch', t: A.cadavre, a: .06, sh: 8 }, { k: 'red', t0: A.cadavre - .05, t1: A.rotiE + .4, max: 1.4 },
      { k: 'punch', t: A.needucat, a: .05, sh: 6 },
    ],
    sfx: [],
    bursts: [],
  };
};
