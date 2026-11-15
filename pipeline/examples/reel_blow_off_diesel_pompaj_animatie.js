// „Diesel cu sunet de blow-off? Nu e tuning. Turbina se distruge” — reel animat 3D (animația „Supapa blow-off”, refăcută pe voce) cu vocea lui Sabin (ElevenLabs), 15.11.2026
// Hook: „Dacă ai diesel și auzi sunetul ăsta…” → sunetul (doar în pauza vocii, audio/hook_bed.wav) → „…nu e tuning. E semnul că turbina se va distruge.”
// Apoi traseul: benzină (blow-off normal) → diesel fără blow-off → geometria variabilă → calamină, palete blocate → supraturare → pompaj → lagăr axial, palete → turbină distrusă.
// Animația e randată direct pe voce (tools/anim_blowoff: fiecare mișcare e ancorată pe un cuvânt din vo/cues.json); etichetele, HUD-ul și ecranul împărțit sunt în animație.
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND }) => {
  const HK = aw(2, 'Hai') - .1;                       // de aici încep subtitrările
  const T1 = aw(0, 'diesel') - .03, T2 = aw(0, 'sunetul') - .03;
  const SX = 3.151, TU = [3.521, 3.721, 3.921, 4.121]; // accentele sunetului din hook (vo/hook_sfx.json → accents)
  const Q = aw(1, 'Ca') + .2;                         // titlurile întrebării și onomatopeea ies când vocea reia
  const T3 = aw(1, 'suflat') - .03, T4 = aw(1, 'nu') - .03, T5 = aw(1, 'turbina') - .03, HE = ew(1, 'distruge') + .32;
  const tu = (i) => ({ k: 'boom', t: TU[i], dur: Q - TU[i], txt: 'TU', x: 500 + i * 150, y: 1162 - i * 6, size: 108 - i * 9, col: '#FFD21F', from: 2.6, sh: 10, ca: 12, rot: -5, riser: false, bg: .3, cg: .2 });
  return {
    hideCap: [[0, HK - .05]],
    items: [
      { k: 'boom', t: T1, dur: Q - T1, txt: 'AI DIESEL', y: 300, size: 190, col: '#FFFFFF', from: 3.4, sh: 18, ca: 24, riser: false, bg: .55, cg: .3 },
      { k: 'boom', t: T2, dur: Q - T2, txt: 'ȘI SUNETUL ĂSTA?', y: 470, size: 128, col: '#FFD21F', from: 3.2, sh: 20, ca: 24, riser: false, bg: .5, cg: .3 },
      { k: 'boom', t: SX, dur: Q - SX, txt: 'PȘȘȘ', x: 250, y: 1168, size: 124, col: '#FFFFFF', from: 2.8, sh: 14, ca: 16, rot: -5, riser: false, bg: .3, cg: .2 },
      tu(0), tu(1), tu(2), tu(3),
      { k: 'boom', t: T3, dur: HE - T3, txt: 'BLOW-OFF PE DIESEL?', y: 300, size: 116, col: '#FFFFFF', from: 3.2, sh: 16, ca: 22, riser: false, bg: .5, cg: .3 },
      { k: 'boom', t: T4, dur: HE - T4, txt: 'NU E TUNING!', y: 456, size: 178, col: '#FFD21F', from: 3.6, sh: 26, ca: 26, riser: false, bg: .7, cg: .35 },
      { k: 'boom', t: T5, dur: HE - T5, txt: 'TURBINA SE DISTRUGE', y: 622, size: 114, col: '#FF4B3E', from: 3.4, sh: 22, ca: 24, riser: false, bg: .6, cg: .35, glow: 'rgba(255,75,62,.5)' },
      { k: 'stamp', t: aw(3, 'normal') - .03, t1: aw(3, 'piciorul') + .3, y: 1150, txt: 'PE BENZINĂ: NORMAL', col: 'green', s: .78 },
      { k: 'stamp', t: aw(9, 'supraturarea') - .03, t1: aw(10, 'ridici') - .1, y: 1150, txt: 'SUPRATURARE', col: 'red', s: .85 },
      { k: 'stamp', t: aw(11, 'pompajul') - .03, t1: aw(12, 'Fiecare') - .2, y: 1150, txt: 'POMPAJ', col: 'red', s: .9 },
      { k: 'stamp', t: aw(13, 'distruge') - .03, t1: ew(13, 'turbina') + .2, x: 600, y: 1212, txt: 'TURBINĂ DISTRUSĂ', col: 'red', s: .82 },
      { k: 'stamp', t: aw(15, 'nu') - .03, t1: aw(15, 'geometria') - .1, y: 1150, txt: 'NU E TUNING', col: 'red', s: .85 },
      { k: 'stamp', t: aw(15, 'geometria') - .03, t1: SEND - .25, y: 1228, rot: -5, txt: 'VERIFICĂ GEOMETRIA VARIABILĂ', col: 'green', s: .6 },
    ],
    fx: [
      { k: 'punch', t: T1, a: .08, sh: 14 }, { k: 'punch', t: T2, a: .08, sh: 14 },
      { k: 'flash', t: SX - .05, a: .5 }, { k: 'shock', t: SX + .02, x: 700, y: 925, r: 620, n: 2, col: '#FF4B3E', col2: '#F39237' },
      { k: 'punch', t: T4, a: .16, sh: 34 }, { k: 'glitch', t: T4, d: .16 }, { k: 'flash', t: T4 - .11, a: .75 },
      { k: 'shock', t: T4 + .01, x: 540, y: 900, r: 700, n: 2, col: '#FFD21F', col2: '#FF4B3E' },
      { k: 'punch', t: T5, a: .1, sh: 20 }, { k: 'glitch', t: T5, d: .12 },
    ],
    bgFix: [[0, SEND]],
    tags: {
      0: { diesel: 'c', sunetul: 'y' }, 1: { blowoff: 'y', tuning: 'r', turbina: 'c', distruge: 'r' }, 2: { sunetul: 'y' },
      3: { benzina: 'y', normal: 'g', clapeta: 'c', inchide: 'y', supapa: 'c', blowoff: 'c', elibereaza: 'g', presiune: 'y' },
      4: { diesel: 'y', altfel: 'y', clapeta: 'c', deschisa: 'g', aerul: 'c', motor: 'c', nici: 'r', nu: 'r', supapa: 'c', blowoff: 'c' },
      5: { sunetul: 'y', turbina: 'c', geometria: 'c', variabila: 'c' },
      6: { geometria: 'c', variabila: 'c', inel: 'c', palete: 'c', carcasa: '', turbinei: '', actuator: 'c' },
      7: { mici: 'y', paletele: 'c', inchid: 'y', gazele: '', roata: 'c', viteza: 'y', mare: 'y', mari: 'y', deschid: 'g', turbina: 'c', supratureze: 'r' },
      8: { calamina: 'r', depune: 'r', palete: 'c', blocheaza: 'r', inchis: 'r', actuatorul: 'c', nu: 'r', deschide: 'r' },
      9: { gazele: '', roata: 'c', turbinei: 'c', prea: 'r', mare: 'r', turbina: 'c', maxima: 'r', presiunea: 'y', peste: 'r', limita: 'r', supraturarea: 'r' },
      10: { ridici: 'y', piciorul: 'y', motorul: 'c', aerul: 'c', compresorul: 'c', supraturat: 'r', impinge: 'r' },
      11: { aerul: 'c', greu: 'r', intoarce: 'r', roata: 'c', compresorului: 'c', pulsuri: 'r', pompajul: 'r', blowoff: 'y' },
      12: { puls: 'r', tensiune: 'r', paletele: 'c', rotii: 'c', compresor: 'c', impinge: 'r', axul: 'c', lagarul: 'c', axial: 'c' },
      13: { lagarul: 'c', uzeaza: 'r', axul: 'c', joc: 'r', paletele: 'c', atinga: 'r', carcasa: 'c', distruge: 'r', turbina: 'c' },
      14: { sunet: 'y', doua: 'y', benzina: 'g', supapa: 'c', treaba: 'g', diesel: 'r', turbina: 'c', pompaj: 'r' },
      15: { dieselul: 'c', sufla: 'y', tuning: 'r', verifica: 'g', geometria: 'c', variabila: 'c', turbina: 'c', repara: 'g' },
    },
  };
};
