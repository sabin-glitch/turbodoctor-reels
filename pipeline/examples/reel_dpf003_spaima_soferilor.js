// v2 – DPF Doctor · „Filtrul de particule, spaima șoferilor” (TikTok 7679786234343918850, 4 min)
// Footage exactly as filmed: selfie (DPF photo inset top, 0–8 s), office selfie, cut-open DPF, engine, office selfie. Natural pace, no separate hook.
// Selfie parts: compact chips above the head (y 300); cards only over the DPF / engine shots (wall + stand at the top).
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND, WORDS }) => {
  const nn = s => s.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/[^a-z0-9]/g, '');
  const near = (x, t) => { const c = WORDS.filter(w => nn(w.text) === nn(x)); if (!c.length) throw new Error('anchor not found: ' + x);
    const b = c.reduce((a, w) => Math.abs(w.os - t) < Math.abs(a.os - t) ? w : a); if (Math.abs(b.os - t) > 1.5) throw new Error('anchor too far: ' + x + ' ' + t + ' -> ' + b.os.toFixed(2)); return b; };
  const W = (x, t) => near(x, t).os, WE = (x, t) => near(x, t).oe;
  const A = {
    filtrul: W('Filtrul', .54), spaima: W('spaima', 2.13), soferilor: W('șoferilor', 3.09), dieselE: WE('diesel', 5.09),
    stati: W('Stați', 8.89), rolul: W('rolul', 11.2), mai2: W('mai', 13.04), ce1: W('ce', 15.12), luiE: WE('lui', 19.92),
    cam: W('Cam', 20.89), si2: W('Și', 23.12), burete: W('burete', 26.16), care2: W('care', 31.6),
    este2: W('Este', 34.24), n25: W('2,5', 37.36), suficient: W('suficient', 39.28),
    dar3: W('dar', 44.3), plamanii: W('plămânii', 48.22), nostriE: WE('noștri', 49.1), el: W('El', 50.14), momentul3: W('momentul', 54.62),
    arderea: W('arderea', 61.02), cenusa: W('cenușă', 65.66), cenusaE: WE('cenușă', 65.66),
    sistemul: W('Sistemul', 67.29), sute: W('sute', 70.32), intretinute: W('întreținute', 72.63), dar4: W('Dar', 73.68), si4: W('Și', 79.6), cand: W('Când', 85.12),
    masina5: W('mașina', 89.17), problema5: W('problemă', 91.17), arderii5E: WE('arderii', 92.37), ce5: W('Ce', 93.17), filtreaza: W('filtrează', 99.33), orice5: W('Orice', 103.57),
    admisie5: W('admisie', 105.33), injectie5: W('injecție', 105.89), evacuare5: W('evacuare', 106.37), motor5: W('motor', 107.25), senzor: W('senzor', 108.13),
    si6: W('Și', 116.33), incarcare: W('încărcare', 119.77), particule6E: WE('particule', 123.29), in6: W('În', 124.17), ai1: W('ai', 129.93), cauto: W('Caut-o', 133.45), rezolvo: W('rezolv-o', 134.33),
    curatama: W('curăță-mă', 135.29), trebuie7E: WE('trebuie', 138.73), problema7: W('Problema', 139.53), anuleze: W('anuleze', 148.97), tai: W('Tai', 150.97), revedereE: WE('revedere', 151.69),
    de7: W('De', 152.41), masiniE: WE('mașini', 157.21),
    totusi: W('Totuși', 157.73), anularea: W('anularea', 158.37), dezechilibru: W('dezechilibru', 162.05), distruge: W('distruge', 165.97), componenteE: WE('componente', 166.93),
    tocmai: W('Tocmai', 168.41), diagnosticarea9: W('diagnosticarea', 171.52), reparatia: W('reparația', 176.96), noi9: W('Noi', 179.68), neam2: W('ne-am', 184.24), de9: W('De', 192.5),
    cutii: W('cutii', 195.79), facem: W('Facem', 200.11), si10: W('Și', 206.99), diagnoza10: W('diagnoză', 211.71), restabilirea: W('restabilirea', 213.71), fiecare: W('fiecare', 216.03), parteE: WE('parte', 217.15),
    nu11: W('Nu', 218.01), gratuita: W('gratuită', 221.44), pentru11: W('Pentru', 224.56), iar11: W('Iar', 230.96), reparatieE: WE('reparație', 237.76),
    va12: W('Vă', 238.49), bucuresti: W('București', 240.33), iasi: W('Iași', 241.0), galati: W('Galați', 241.29), piatra: W('Piatra', 241.93),
  };
  const HOOK_OUT = A.dieselE + .2;
  return {
    // DPF photo inset (top, 0–8 s) + face in the middle → hook lines sit in the caption zone, the tag right under them
    hook: { tag: 'ANALIZĂ TEHNICĂ · DPF', l1: 'FILTRUL DE <span class="y">PARTICULE</span>', l1At: A.filtrul - .05, l2: 'SPAIMA ȘOFERILOR!', l2At: A.spaima - .04, l2Col: '#FF3B30',
      y: 950, tagY: 1612, end: HOOK_OUT },
    hideCap: [[0, HOOK_OUT - .05]],
    stages: [[A.cam - .05, 'CE ESTE'], [A.sistemul - .1, 'DE CE SE STRICĂ'], [A.totusi - .1, 'ANULAREA?'], [A.tocmai - .1, 'SOLUȚIA']],
    tags: {
      0: { spaima: 'r' }, 1: { benzina: 'c', reparatii: 'r', costisitoare: 'r' }, 2: { pm25: 'y', burete: 'c', adanc: 'r', respirator: 'r' },
      3: { plamanii: 'r', urban: 'r', extraurban: 'g', regenereaza: 'g', regenerarea: 'g', funingine: 'r', cenusa: 'g' },
      4: { gandit: 'g', bine: 'g', corect: 'g', anulat: 'r', plang: 'r' }, 5: { arderii: 'r', senzor: 'c', depunere: 'r', restrictioneaza: 'r' },
      6: { anormala: 'r', grija: 'r', cauto: 'g', rezolvo: 'g' }, 7: { curatama: 'g', complicata: 'y', anuleze: 'r', tai: 'r', revedere: 'r' },
      8: { anularea: 'r', dezechilibru: 'r', reaparea: 'r', distruge: 'r', componente: 'r' }, 9: { specializat: 'g', diagnosticarea: 'g', profesionala: 'g', curatarea: 'g' },
      10: { diagnosticam: 'g', reparam: 'g', completa: 'g' }, 11: { gratuita: 'g', gratuit: 'g', aiurea: 'r', devizul: 'g' },
      12: { bucuresti: 'y', iasi: 'y', galati: 'y', piatra: 'y', neamt: 'y' },
    },
    items: [
      // office selfie: what's coming
      { k: 'chip', t0: A.stati - .1, t1: A.luiE + .3, y: 300, ph: [[A.stati - .1, 'magnifying_glass_tilted_left', 'ROLUL DPF PE DIESEL', 'blue'], [A.mai2 - .05, 'fuel_pump', '...ȘI PE BENZINĂ', 'blue'],
        [A.ce1 - .05, 'money_with_wings', 'CUM EVIȚI REPARAȚII SCUMPE', 'green']] },
      // cut-open DPF
      { k: 'call', t0: A.cam + .1, t1: A.si2 + 1.2, p: [330, 960], lab: [600, 600], h: 'ASTA E', v: 'FILTRUL DE PARTICULE', cps: 38 },
      { k: 'def', t0: A.burete - .1, t1: A.n25 - .9, top: 262, term: 'PM2.5', text: 'Particule fine rezultate în urma arderii. DPF-ul le reține, ca un burete.' },
      { k: 'stat', t0: A.n25 - .6, t1: A.suficient - .3, top: 262, title: 'DIMENSIUNEA PARTICULELOR', ico: 'microscope', to: 25, at: A.n25 - .15, dur: .6, fmt: v => (v / 10).toFixed(1).replace('.', ','), unit: 'MICRONI', sub: 'PM2.5' },
      { k: 'chip', t0: A.suficient - .1, t1: A.nostriE + .3, y: 330, ph: [[A.suficient - .1, 'warning', 'DESTUL DE MICI: AJUNG ADÂNC', 'red'], [A.dar3 - .05, 'warning', 'DESTUL DE MARI: AFECTEAZĂ PLĂMÂNII', 'red']] },
      { k: 'schem', t0: A.el - .15, t1: A.cenusaE + .4, top: 262, type: 'dpfFlow', P: { burn: 4.0 }, title: 'SCHEMĂ · FILTRUL DE PARTICULE', sub: 'SECȚIUNE', stepNames: ['ORAȘ', 'EXTRAURBAN', 'REZULTAT'],
        steps: [[A.el - .15, 'În oraș, filtrul se încarcă cu funingine', 'r', 'load'], [A.momentul3 - .05, 'Extraurban: se regenerează', 'y', 'regen'], [A.arderea - .05, 'Funinginea arde și devine cenușă', 'g', 'ash']] },
      // why it fails
      { k: 'chip', t0: A.sistemul - .1, t1: A.dar4 - .2, y: 300, ph: [[A.sistemul - .1, 'check_mark_button', 'SISTEM GÂNDIT BINE', 'green'], [A.sute - .05, 'automobile', 'SUTE DE MII DE KM', 'green'], [A.intretinute - .1, 'wrench', 'DACĂ E ÎNTREȚINUT CORECT', 'green']] },
      { k: 'chip', t0: A.dar4 - .1, t1: A.si4 - .2, y: 300, ph: [[A.dar4 - .1, 'thinking_face', 'ATUNCI DE CE SE STRICĂ?', 'yellow']] },
      { k: 'chip', t0: A.si4 - .1, t1: A.cand - .2, y: 300, ph: [[A.si4 - .1, 'speech_balloon', '„ANULEAZĂ-L, DOM\'LE!”', 'blue']] },
      { k: 'chip', t0: A.cand - .1, t1: A.problema5 - .25, y: 300, ph: [[A.cand - .1, 'magnifying_glass_tilted_left', 'ÎN REALITATE...', ''], [A.masina5 - .05, 'warning', 'MAȘINA ÎȚI SEMNALEAZĂ', 'red']] },
      { k: 'stamp', t: A.problema5 - .03, t1: A.arderii5E + .4, y: 320, txt: 'PROBLEMĂ LA ARDERE', col: 'red', s: .55, rot: -4 },
      { k: 'schem', t0: A.ce5 - .1, t1: A.particule6E + .35, top: 262, type: 'systemMap', title: 'SCHEMĂ · DE UNDE VINE PROBLEMA', sub: 'ARDEREA', stepNames: ['MONTAJ', 'ROL', 'CAUZE', 'EFECT'],
        P: { nodes: [[150, 70, 'ADMISIE', 'dashing_away'], [457, 70, 'INJECȚIE', 'droplet'], [764, 70, 'SENZORI', 'counter'], [457, 215, 'ARDERE', 'fire'], [250, 360, 'EVACUARE', 'dashing_away'], [664, 360, 'DPF', 'warning']],
          links: [[0, 3], [1, 3], [2, 3, true], [3, 4], [4, 5]],
          events: [[A.admisie5, 0, 'bad'], [A.injectie5, 1, 'bad'], [A.evacuare5, 4, 'bad'], [A.motor5, 3, 'bad'], [A.senzor, 2, 'bad'], [A.incarcare, 5, 'bad']] },
        steps: [[A.ce5 - .1, 'DPF-ul e montat pe evacuarea motorului', ''], [A.filtreaza - .05, 'Filtrează tot ce rezultă din ardere', ''],
          [A.orice5 - .05, 'Orice defect înaintea lui strică arderea', 'r'], [A.si6 - .05, 'Ardere proastă: încărcare și regenerare anormale', 'r']] },
      { k: 'list', t0: A.in6 - .1, t1: A.trebuie7E + .3, top: 292, ico: 'speech_balloon', title: 'CE ÎȚI SPUNE DPF-UL', rows: [[A.ai1 - .05, 'AI O PROBLEMĂ PE MOTOR', 'bad'], [A.cauto - .05, 'CAUT-O'], [A.rezolvo - .05, 'REZOLV-O'], [A.curatama - .05, 'CURĂȚĂ-MĂ']] },
      { k: 'chip', t0: A.problema7 - .1, t1: A.tai - .25, y: 330, ph: [[A.problema7 - .1, 'magnifying_glass_tilted_left', 'DIAGNOZA CORECTĂ E COMPLICATĂ', 'yellow'], [A.anuleze - .1, 'scissors', 'MULȚI PREFERĂ ANULAREA', 'red']] },
      { k: 'stamp', t: A.tai - .03, t1: A.revedereE + .35, y: 330, txt: 'TAI ȘI LA REVEDERE', col: 'red', s: .55, rot: -4 },
      { k: 'chip', t0: A.de7 - .1, t1: A.masiniE + .3, y: 330, ph: [[A.de7 - .1, 'thinking_face', '„DE CE SĂ TE CHINUI?”', '']] },
      { k: 'chain', t0: A.totusi - .1, t1: A.componenteE + .5, top: 262, title: 'ANULAREA DPF', sub: 'CAUZĂ › EFECT', ico: 'scissors',
        nodes: [[A.anularea, 'scissors', 'ANULARE', 'REZOLVĂ DOAR DE MOMENT', 'y'], [A.dezechilibru - .05, 'warning', 'DEZECHILIBRUL', 'REAPARE ÎN SCURT TIMP', 'r'], [A.distruge - .05, 'collision', 'REZULTAT', 'ALTE COMPONENTE DISTRUSE', 'r']] },
      // the solution (office selfie)
      { k: 'chip', t0: A.tocmai - .1, t1: A.noi9 - .25, y: 300, ph: [[A.tocmai - .1, 'stethoscope', 'NE-AM SPECIALIZAT ÎN DIAGNOZĂ', 'green'], [A.diagnosticarea9 - .05, 'magnifying_glass_tilted_left', 'ADMISIE · INJECȚIE · EVACUARE', 'blue'],
        [A.reparatia - .05, 'hammer_and_wrench', 'ȘI REPARAȚIE PROFESIONALĂ', 'green']] },
      { k: 'chip', t0: A.noi9 - .1, t1: A.de9 - .25, y: 300, ph: [[A.noi9 - .1, 'soap', 'AM ÎNCEPUT CU CURĂȚAREA DPF', ''], [A.neam2 - .05, 'magnifying_glass_tilted_left', 'APOI: VERIFICĂM TOT SISTEMUL', 'green']] },
      { k: 'chip', t0: A.de9 - .1, t1: A.facem - .25, y: 300, ph: [[A.de9 - .1, 'gear', 'DOAR ACESTE SERVICII', 'blue'], [A.cutii - .05, 'cross_mark', 'NU: CUTII, BUCȘE, PLĂCUȚE', 'red']] },
      { k: 'chip', t0: A.facem - .1, t1: A.si10 - .25, y: 300, ph: [[A.facem - .1, 'handshake', 'SISTEME ÎN STRÂNSĂ LEGĂTURĂ', 'blue']] },
      { k: 'pipe', t0: A.si10 - .1, t1: A.parteE + .4, top: 252, ico: 'stethoscope', title: 'REPARAȚIA CORECTĂ',
        steps: [[A.diagnoza10 - .05, 'stethoscope', 'DIAGNOZĂ<br>COMPLETĂ'], [A.restabilirea - .05, 'gear', 'PARAMETRI<br>RESTABILIȚI'], [A.fiecare - .05, 'check_mark_button', 'PE FIECARE<br>SISTEM']] },
      { k: 'chip', t0: A.nu11 - .1, t1: A.reparatieE + .3, y: 300, ph: [[A.nu11 - .1, 'stethoscope', 'DIAGNOZĂ GRATUITĂ', 'green'], [A.pentru11 - .05, 'money_with_wings', 'NU PLĂTEȘTI DIAGNOZA AIUREA', 'red'],
        [A.iar11 - .05, 'check_mark_button', 'INFORMAȚIE + DEVIZ, GRATUIT', 'green']] },
      { k: 'chip', t0: A.va12 - .1, t1: SEND - .05, y: 300, ph: [[A.va12 - .1, 'round_pushpin', 'VĂ AȘTEPTĂM!', ''], [A.bucuresti - .05, 'round_pushpin', 'BUCUREȘTI', ''], [A.iasi - .05, 'round_pushpin', 'IAȘI', ''],
        [A.galati - .05, 'round_pushpin', 'GALAȚI', ''], [A.piatra - .05, 'round_pushpin', 'PIATRA NEAMȚ', 'blue']] },
    ],
    fx: [
      { k: 'punch', t: A.spaima, a: .05, sh: 6 }, { k: 'red', t0: A.spaima - .05, t1: A.soferilor + .8, max: 1.3 },
      { k: 'red', t0: A.plamanii - .05, t1: A.nostriE + .2, max: 1.2 },
      { k: 'green', t0: A.cenusa - .05, t1: A.cenusaE + .5, silent: true },
      { k: 'punch', t: A.problema5, a: .05, sh: 6 }, { k: 'red', t0: A.problema5 - .05, t1: A.arderii5E + .3, max: 1.3 },
      { k: 'punch', t: A.tai, a: .05, sh: 7 },
      { k: 'punch', t: A.distruge, a: .05, sh: 6 }, { k: 'red', t0: A.distruge - .05, t1: A.componenteE + .3, max: 1.2 },
      { k: 'green', t0: A.gratuita - .05, t1: A.gratuita + .9 },
    ],
    sfx: [],
    bursts: [[A.gratuita, 540, 300, 6, 300, .7]],
  };
};
