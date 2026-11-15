// „Diesel cu sunet de blow-off? Nu e tuning. Turbina se distruge” — reel animat 3D (animația „Supapa blow-off”, refăcută pe voce) cu vocea lui Sabin (ElevenLabs)
// Varianta 2 (15.11.2026), după observațiile lui Sabin: la început supapa de recirculare (diverter) cu care vin din fabrică motoarele pe benzină și aerul
// care rămâne captiv după senzorul MAF; blow-off-ul pe mașinile tunate; pe diesel se explică doar de unde vine sunetul (supraturare → pompaj),
// fără geometria variabilă; cauzele (geometrie variabilă blocată, actuator, alte defecte) abia la final. Sunetul din hook e o înregistrare reală.
// Hook: „Dacă ai diesel și auzi sunetul ăsta…” → sunetul (doar în pauza vocii, audio/hook_bed.wav) → „…nu e tuning. E semnul că turbina se va distruge.”
// Animația e randată direct pe voce (tools/anim_blowoff: fiecare mișcare e ancorată pe un cuvânt din vo/cues.json); etichetele, HUD-ul și ecranul împărțit sunt în animație.
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND }) => {
  const HK = aw(2, 'Hai') - .1;                       // de aici încep subtitrările
  const T1 = aw(0, 'diesel') - .03, T2 = aw(0, 'sunetul') - .03;
  // sunetul din hook (vo/hook_sfx.json): TB = ridicarea piciorului (începe fâlfâitul), TU = pulsurile tari ale fâlfâitului, PSH = „pșș”-ul supapei
  const TB = 3.775, TU = [3.79, 3.85, 3.95, 4.05], PSH = 4.19;
  const Q = aw(1, 'Ca') + .2;                         // titlurile întrebării și onomatopeea ies când vocea reia
  const T3 = aw(1, 'suflat') - .03, T4 = aw(1, 'nu') - .03, T5 = aw(1, 'turbina') - .03, HE = ew(1, 'distruge') + .32;
  const tu = (i) => ({ k: 'boom', t: TU[i], dur: Q - TU[i], txt: 'TU', x: 140 + i * 138, y: 1166 - i * 5, size: 108, col: '#FFD21F', from: 2.4, sh: 9, ca: 12, rot: i % 2 ? -3 : -7, riser: false, bg: .3, cg: .2 });
  return {
    hideCap: [[0, HK - .05]],
    items: [
      { k: 'boom', t: T1, dur: Q - T1, txt: 'AI DIESEL', y: 300, size: 190, col: '#FFFFFF', from: 3.4, sh: 18, ca: 24, riser: false, bg: .55, cg: .3 },
      { k: 'boom', t: T2, dur: Q - T2, txt: 'ȘI SUNETUL ĂSTA?', y: 470, size: 128, col: '#FFD21F', from: 3.2, sh: 20, ca: 24, riser: false, bg: .5, cg: .3 },
      tu(0), tu(1), tu(2), tu(3),
      { k: 'boom', t: PSH, dur: Q - PSH, txt: 'PȘȘȘ', x: 835, y: 1150, size: 132, col: '#FFFFFF', from: 2.8, sh: 14, ca: 16, rot: -5, riser: false, bg: .3, cg: .2 },
      { k: 'boom', t: T3, dur: HE - T3, txt: 'BLOW-OFF PE DIESEL?', y: 300, size: 116, col: '#FFFFFF', from: 3.2, sh: 16, ca: 22, riser: false, bg: .5, cg: .3 },
      { k: 'boom', t: T4, dur: HE - T4, txt: 'NU E TUNING!', y: 456, size: 178, col: '#FFD21F', from: 3.6, sh: 26, ca: 26, riser: false, bg: .7, cg: .35 },
      { k: 'boom', t: T5, dur: HE - T5, txt: 'TURBINA SE DISTRUGE', y: 622, size: 114, col: '#FF4B3E', from: 3.4, sh: 22, ca: 24, riser: false, bg: .6, cg: .35, glow: 'rgba(255,75,62,.5)' },
      { k: 'stamp', t: aw(3, 'fabrică') - .03, t1: aw(3, 'supapă') + .1, y: 1150, txt: 'DIN FABRICĂ', col: 'green', s: .85 },
      { k: 'stamp', t: aw(5, 'tunate') - .03, t1: aw(5, 'Este') + .5, y: 1150, txt: 'PE MAȘINI TUNATE', col: 'blue', s: .78 },
      { k: 'stamp', t: aw(7, 'supraturează') - .03, t1: ew(7, 'motorul') + .1, y: 1150, txt: 'SUPRATURARE', col: 'red', s: .85 },
      { k: 'stamp', t: aw(9, 'pompajul') - .03, t1: ew(9, 'blow-off') + .15, y: 1150, txt: 'POMPAJ', col: 'red', s: .9 },
      { k: 'stamp', t: aw(11, 'distruge') - .03, t1: ew(11, 'turbina') + .2, x: 600, y: 1212, txt: 'TURBINĂ DISTRUSĂ', col: 'red', s: .82 },
      { k: 'stamp', t: aw(14, 'nu') - .03, t1: aw(14, 'Găsește') - .1, y: 1150, txt: 'NU E TUNING', col: 'red', s: .85 },
      { k: 'stamp', t: aw(14, 'Găsește') - .03, t1: SEND - .25, y: 1228, rot: -5, txt: 'GĂSEȘTE CAUZA', col: 'green', s: .85 },
    ],
    fx: [
      { k: 'punch', t: T1, a: .08, sh: 14 }, { k: 'punch', t: T2, a: .08, sh: 14 },
      { k: 'flash', t: TB - .05, a: .5 }, { k: 'shock', t: TB + .02, x: 700, y: 925, r: 620, n: 2, col: '#FF4B3E', col2: '#F39237' },
      { k: 'punch', t: T4, a: .16, sh: 34 }, { k: 'glitch', t: T4, d: .16 }, { k: 'flash', t: T4 - .11, a: .75 },
      { k: 'shock', t: T4 + .01, x: 540, y: 900, r: 700, n: 2, col: '#FFD21F', col2: '#FF4B3E' },
      { k: 'punch', t: T5, a: .1, sh: 20 }, { k: 'glitch', t: T5, d: .12 },
    ],
    bgFix: [[0, SEND]],
    tags: {
      0: { diesel: 'c', sunetul: 'y' }, 1: { blowoff: 'y', tuning: 'r', turbina: 'c', distruge: 'r' }, 2: { sunetul: 'y' },
      3: { benzina: 'y', fabrica: 'g', supapa: 'c', recirculare: 'c', diverter: 'c', ridici: 'y', piciorul: 'y', clapeta: 'c', inchide: 'y', aerul: 'c', comprimat: 'c', dupa: 'y', compresor: 'c', inapoi: 'g', inainte: 'y' },
      4: { aerul: 'c', masurat: 'y', captiv: 'y', senzorul: 'c', maf: 'c', motorul: 'c', corect: 'g' },
      5: { supapa: 'c', blowoff: 'c', tunate: 'y', protejeze: 'g', turbina: 'c', accelereaza: 'y', prea: 'r', mult: 'r', multa: 'r', presiune: 'y', admisie: 'c', motorul: 'c', aerul: 'c', eliberat: 'g', atmosfera: 'g', sunetul: 'y' },
      6: { diesel: 'y', altfel: 'y', clapeta: 'c', deschisa: 'g', aerul: 'c', motor: 'c', nici: 'r', nu: 'r', supapa: 'c', recirculare: 'c', blowoff: 'c' },
      7: { sunetul: 'y', turbina: 'c', supratureaza: 'r', admisie: 'c', mult: 'r', aer: 'c', multa: 'r', presiune: 'y', motorul: 'c' },
      8: { ridici: 'y', piciorul: 'y', motorul: 'c', aerul: 'c', compresorul: 'c', supraturat: 'r', impinge: 'r' },
      9: { aerul: 'c', greu: 'r', intoarce: 'r', roata: 'c', compresorului: 'c', pulsuri: 'r', pompajul: 'r', blowoff: 'y' },
      10: { puls: 'r', tensiune: 'r', paletele: 'c', rotii: 'c', compresor: 'c', impinge: 'r', axul: 'c', lagarul: 'c', axial: 'c' },
      11: { lagarul: 'c', uzeaza: 'r', axul: 'c', joc: 'r', paletele: 'c', atinga: 'r', carcasa: 'c', distruge: 'r', turbina: 'c' },
      12: { sunet: 'y', doua: 'y', benzina: 'g', supapa: 'c', treaba: 'g', diesel: 'r', turbina: 'c', pompaj: 'r' },
      13: { prea: 'r', mult: 'r', aer: 'c', admisie: 'c', diesel: 'y', geometria: 'c', variabila: 'c', blocata: 'r', actionare: 'y', actuator: 'c', defecte: 'r', presiunea: 'y', mare: 'r' },
      14: { dieselul: 'c', sufla: 'y', tuning: 'r', gaseste: 'g', cauza: 'g', turbina: 'c', repara: 'g' },
    },
  };
};
