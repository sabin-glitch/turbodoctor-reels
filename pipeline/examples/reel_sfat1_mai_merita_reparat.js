// v2 – Reel r_sfat – „Sfatul #1 la reparația motorului: mai merită reparat?” (2 clipuri în ordinea filmării, fără tăieturi)
// clipuri: 0 motor demontat (IMG_1741) · 30.55 selfie (1742)
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND }) => {
  const A = {
    pont: aw(0, 'pont'), mare0: aw(0, 'mare'), primul: aw(0, 'Primul'), sa1: aw(1, 'să'), merita1: aw(1, 'merită'),
    sunt2: aw(2, 'Sunt'), reparatia2: aw(2, 'reparația'), anumite2: aw(2, 'anumite', 1),
    vedem: aw(3, 'Vedem'), in4: aw(4, 'În'), dorinta: aw(4, 'dorința'), cand5: aw(5, 'Când'), sunt5: aw(5, 'Sunt'),
    cel6: aw(6, 'Cel'), domnule: aw(7, 'Domnule'), orice: aw(7, 'Orice'), rata: aw(9, 'rata'), si10: aw(10, 'Și'), eliminam: aw(10, 'eliminăm'),
  };
  const CLIP = [0, 30.55];
  return {
    hook: { tag: 'SFATUL #1 · REPARAȚIA MOTORULUI', l1: 'ÎNAINTE SĂ REPARI UN MOTOR:', l1At: .1, l2: 'MAI MERITĂ REPARAT?', l2At: A.pont - .04, l2Col: '#FF3B30',
      car: 'CEL MAI IMPORTANT SFAT', carAt: A.mare0, stk1: 'thinking_face', end: A.primul - .12 },
    hideCap: [[0, A.primul - .1]],
    stages: [[A.primul - .05, 'SFATUL'], [CLIP[1] + .15, 'ȚEAPA?'], [A.in4 - .1, 'REALITATEA'], [A.cel6 - .1, 'TURBO DOCTOR']],
    items: [
      { k: 'scan', t0: .12, t1: A.primul - .3, box: [120, 760, 840, 700], lab: 'ANALIZĂ MOTOR...', lab2: 'VERDICT?', at2: A.pont - .04 },
      // indicatorul stării motorului, sus, peste motorul demontat
      { k: 'gauge', t0: A.primul - .05, t1: CLIP[1] - .25, top: 268, title: 'DIAGNOSTIC · STAREA MOTORULUI', sub: 'SFATUL #1', ico: 'stethoscope',
        needle: [[A.primul, .14], [A.sa1, .16], [A.merita1, .48], [A.sunt2, .62], [A.reparatia2 + .3, .9]],
        zones: [[0, .5, '#4ADE80'], [.5, .75, '#FFD21F'], [.75, 1, '#FF4B4B']], ends: ['BUN', 'DEGRADAT'], mid: 'MAI MERITĂ?',
        read: [[A.primul, 'PRIMUL PAS: EVALUEZI MOTORUL', '#FFFFFF'], [A.sa1, 'MAI MERITĂ REPARAT?', '#FFD21F'], [A.reparatia2, 'REPARAȚIA NU AR MAI TREBUI FĂCUTĂ', '#FF4B4B'],
          [A.anumite2, 'COMPONENTE CARE NU MAI TREBUIE REUTILIZATE', '#FF4B4B']] },
      // selfie: chip-uri compacte deasupra capului
      { k: 'chip', t0: CLIP[1] + .15, t1: A.in4 - .3, y: 330, ph: [[CLIP[1] + .15, 'phone', 'PE TIKTOK: „MI-A DAT ȚEAPĂ MECANICUL”', 'red']] },
      { k: 'chip', t0: A.in4 - .05, t1: A.cand5 - .3, y: 330, ph: [[A.in4 - .05, 'magnifying_glass_tilted_left', 'DIN PRACTICĂ: PROBLEMA E DECIZIA', 'blue'], [A.dorinta - .05, 'money_bag', '„SĂ IES CÂT MAI IEFTIN”', 'red']] },
      { k: 'chip', t0: A.cand5 - .05, t1: A.cel6 - .3, y: 330, ph: [[A.cand5 - .05, 'warning', 'BLOC SAU COMPONENTE PREA AFECTATE', 'red'], [A.sunt5 - .05, 'cross_mark', 'NU MAI DUC LA O REPARAȚIE CORECTĂ', 'red']] },
      { k: 'chip', t0: A.cel6 - .05, t1: A.orice - .3, y: 330, ph: [[A.cel6 - .05, 'stethoscope', 'LA TURBO DOCTOR: ÎȚI SPUNEM SINCER', 'green'], [A.domnule - .05, 'speech_balloon', '„NU MAI E CE SĂ REPARI”', 'yellow']] },
      { k: 'chip', t0: A.orice - .05, t1: A.si10 - .3, y: 330, ph: [[A.orice - .05, 'hammer_and_wrench', 'ORICE SE POATE REPARA...', 'blue'], [A.rata - .05, 'chart_down', 'DAR RATA DE SUCCES SCADE', 'red']] },
      { k: 'chip', t0: A.si10 - .05, t1: SEND - .2, y: 330, ph: [[A.si10 - .05, 'handshake', 'SUNTEM DESCHIȘI CU CLIENȚII', 'green'], [A.eliminam - .05, 'check_mark_button', 'ELIMINĂM PROBLEMA DE LA ÎNCEPUT', 'green']] },
    ],
    fx: [ { k: 'punch', t: A.pont, a: .05 }, { k: 'glitch', t: A.vedem, d: .12 } ],
    sfx: [],
    bursts: [],
  };
};
