// v2 – „Injectorul piezo versus injectorul magnetic”: reel animat 3D cu vocea lui Sabin (ElevenLabs), 12.11.2026
// Sursa: animația 3D a celor două injectoare (tools/anim_piezo/reel.html), randată cadru cu cadru pe voce: diferența de funcționare
// (48 V în bobină vs ~150 V în stiva piezo), apoi ce spune Bosch (forță ×10, 100 µs, 10 injecții, 2.700 bar) și varianta pe înțelesul tuturor.
// Etichetele, graficele semnalului și cartonașele Bosch sunt în animație; compozitorul pune hook-ul boom, bara de etape și subtitrările.
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND }) => {
  const HK = aw(2, 'Amândouă') - .35;
  const T1 = aw(0, 'piezo') - .03, T2 = aw(0, 'versus') - .03, T3 = aw(1, 'Pariu') - .03;
  return {
    hideCap: [[0, HK - .05]],
    items: [
      { k: 'boom', t: T1, dur: T3 - .1 - T1, txt: 'PIEZO', y: 285, size: 200, col: '#B98CFF', from: 3.4, sh: 20, ca: 26, riser: false, bg: .7, cg: .35, glow: 'rgba(185,140,255,.55)' },
      { k: 'boom', t: T2, dur: T3 - .1 - T2, txt: 'VS MAGNETIC', y: 470, size: 132, col: '#F39237', from: 3.0, sh: 16, ca: 22, riser: false, bg: .5, cg: .3 },
      { k: 'boom', t: T3, dur: HK - T3, txt: 'PARIU CĂ', y: 300, size: 150, col: '#FFFFFF', from: 3.0, sh: 16, ca: 22, riser: false, bg: .5, cg: .3 },
      { k: 'boom', t: aw(1, 'nu') - .03, dur: HK - aw(1, 'nu'), txt: 'NU ȘTIAI ASTA!', y: 460, size: 128, col: '#FFD21F', from: 2.8, sh: 14, ca: 20, riser: false, bg: .3, cg: 0, glow: 'rgba(255,210,31,.5)' },
    ],
    fx: [
      { k: 'punch', t: T1, a: .14, sh: 30 }, { k: 'glitch', t: T1, d: .16 }, { k: 'flash', t: T1 - .11, a: .6 },
      { k: 'shock', t: T1 + .01, x: 540, y: 900, r: 700, n: 2, col: '#B98CFF', col2: '#F39237' },
      { k: 'punch', t: T2, a: .08, sh: 16 },
      { k: 'punch', t: T3, a: .1, sh: 20 }, { k: 'punch', t: aw(1, 'nu') - .03, a: .08, sh: 14 },
    ],
    stages: [[HK + .5, 'CUM FUNCȚIONEAZĂ'], [aw(4, 'La') - .05, 'DIFERENȚA'], [aw(9, 'De') - .05, 'CE SPUNE BOSCH'], [aw(14, 'Mai') - .05, 'PE ÎNȚELES']],
    bgFix: [[0, SEND]],
    tags: {
      0: { piezo: 'c', magnetic: 'y' }, 1: { pariu: 'y', stiai: 'y' },
      2: { rail: 'c', supapa: 'y', camera: 'c', comanda: 'c' }, 3: { diferenta: 'y', supapa: 'y' },
      4: { magnetic: 'y', '48': 'y', volti: 'y', bobina: 'c' }, 5: { bobina: 'c', armatura: 'c', bila: 'c' },
      6: { piezo: 'c', '150': 'y', volti: 'y', stiva: 'c', placute: 'c', ceramice: 'c' }, 7: { lungesc: 'g', imping: 'g' },
      8: { piezo: 'c', mult: 'g', mai: 'g', repede: 'g' }, 9: { superior: 'g', bosch: 'y' },
      10: { zece: 'y', ori: 'y', forta: 'y' }, 11: { '100': 'y', microsecunde: 'y' },
      12: { zece: 'y', injectii: 'y', '2700': 'y', bari: 'y' }, 13: { consum: 'g', emisii: 'g', zgomot: 'g' },
      14: { simplu: 'y', doua: 'r', trei: 'r', reprize: 'r' }, 15: { zece: 'g', doze: 'g', exact: 'g' },
      16: { lin: 'g', silentios: 'g', putin: 'g' },
    },
  };
};
