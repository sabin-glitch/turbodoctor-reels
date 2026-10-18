// v2 – DPF Doctor #001 – „Așa îți omori DPF-ul” (3 greșeli zilnice: motor rece + blană, mers subturat, drumuri scurte)
// Talking-head clip: big cards run as short cutaways (fx 'focus': footage blurred + darkened), never on top of the face.
window.REEL_BRAND = { word: 'DPF <span class="y">DOCTOR</span>', sub: 'UN SERVICIU TURBO DOCTOR', wordTop: 150 };
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND }) => {
  const A = {
    zilnic: aw(0, 'zilnic'), omori: aw(0, 'omori'), dpf0: aw(0, 'DPF-ul'), fara: aw(0, 'fără'), stiiE: ew(0, 'știi'), unu: aw(0, '1'),
    pornesti: aw(1, 'Pornești'), incalz1: aw(1, 'încălzească'), nui: aw(1, 'Nu-i'), blana: aw(1, 'blană'), directE: ew(1, 'direct'),
    acest: aw(2, 'Acest'), afecteaza: aw(2, 'afectează'), indirect: aw(2, 'indirect'), uzura: aw(2, 'uzură'), componente: aw(2, 'componente'), infunde: aw(2, 'înfunde'), dpf2E: ew(2, 'DPF-ul', 1),
    doi: aw(3, '2'), subturat3: aw(3, 'subturat'), bine3: aw(3, 'Bine'), automata: aw(3, 'automată'), n1100: aw(3, '1100'), tureE: ew(3, 'ture'),
    ok4: aw(4, 'Ok'), daca4: aw(4, 'dacă'), subturat4: aw(4, 'subturat'), traseu: aw(4, 'traseu'), lungE4: ew(4, 'lung'),
    plecam: aw(5, 'Plecăm'), n100: aw(5, '100'), ruda: aw(5, 'rudă'), bunici: aw(5, 'bunici'), munte: aw(5, 'munte'), mare: aw(5, 'mare'), noiE5: ew(5, 'noi', 1),
    si6: aw(6, 'Și'), drum6: aw(6, 'drum'), turatie: aw(6, 'turație'), asta6: aw(6, 'Asta'), regen: aw(6, 'regenerarea'), curatarea: aw(6, 'curățarea'), recirc: aw(6, 'recirculare'), gazeleE: ew(6, 'gazelor'),
    numarul: aw(7, 'numărul'), trei: aw(7, '3'), condusul: aw(7, 'condusul'), scurteE7: ew(7, 'scurte'),
    auzit: aw(8, 'auzit'), biroul: aw(8, 'biroul'), doiMin: aw(8, '2'), naveti: aw(8, 'N-aveți'), vinaE: ew(8, 'vină', 1), dar8: aw(8, 'Dar', 1), comport8: aw(8, 'comportamente'),
    infundare: aw(8, 'înfundare'), particuleE8: ew(8, 'particule'), intelegem8: aw(8, 'înțelegem'),
    momentul9: aw(9, 'momentul'), subturat9: aw(9, 'subturat'), distante9: aw(9, 'distanțe'),
    daca10: aw(10, 'dacă'), incalzit10: aw(10, 'încălzit'), iarna: aw(10, 'iarna'), refer: aw(10, 'refer'), cinci: aw(10, '5'), vom: aw(10, 'vom'), premature: aw(10, 'premature'), particuleE10: ew(10, 'particule'),
    daca11: aw(11, 'Dacă'), ajutam: aw(11, 'ajutăm'), devreme11: aw(11, 'devreme'), trebuiE11: ew(11, 'trebui'),
    tineti12: aw(12, 'Țineți'), diagnoza: aw(12, 'diagnoza'), gratuita: aw(12, 'gratuită'), problema12: aw(12, 'problemă'), stadiu: aw(12, 'stadiu'), si12: aw(12, 'și'), alegeti: aw(12, 'alegeți'), nuE12: ew(12, 'nu'),
    dar13: aw(13, 'Dar'), moduri: aw(13, 'moduri'), aduce: aw(13, 'aduce'), noiE13: ew(13, 'noi'),
    tineti14: aw(14, 'Țineți'), mergeti: aw(14, 'mergeți'), vacanta: aw(14, 'vacanță'), succes: aw(14, 'succes'),
  };
  const FT = 420; // card top during cutaways
  return {
    hook: { tag: 'ANALIZĂ TEHNICĂ · DPF #001', l1: 'FACI ASTA <span class="y">ZILNIC</span>?', l1At: .05, l2: 'ÎȚI OMORI DPF-UL!', l2At: A.omori - .04, l2Col: '#FF3B30',
      chips: [['warning', '3 GREȘELI ZILNICE', A.fara]], chipsAt: A.fara - .1, end: A.unu - .02 },
    hideCap: [[0, A.unu - .03]],
    stages: [[A.unu - .05, 'GREȘEALA 1'], [A.doi - .05, 'GREȘEALA 2'], [A.trei - .1, 'GREȘEALA 3'], [A.daca11 - .1, 'SOLUȚIA']],
    tags: {
      0: { omori: 'r', dpful: 'c' }, 1: { incalzeasca: 'c', blana: 'r', direct: 'r', motorul: 'c' },
      2: { dpful: 'c', prematura: 'r', componente: 'c', infunde: 'r' },
      3: { subturat: 'r', automata: 'c', ture: 'y' }, 4: { subturat: 'r', traseu: 'g', lung: 'g' },
      5: { km: 'y' }, 6: { drum: 'g', lung: 'g', turatie: 'g', ridicata: 'g', regenerarea: 'g', eficienta: 'g', curatarea: 'g' },
      7: { distante: 'r', scurte: 'r' }, 8: { minute: 'y', infundare: 'r', prematura: 'r' },
      9: { subturat: 'r', distante: 'r', scurte: 'r' }, 10: { incalzit: 'c', iarna: 'c', minute: 'y', premature: 'r' },
      11: { ajutam: 'g', drag: 'g', devreme: 'y' }, 12: { diagnoza: 'g', complet: 'g', gratuita: 'g', dpful: 'c', stadiu: 'y', dpf: 'c' },
      13: { devreme: 'r' }, 14: { vacanta: 'g', succes: 'g' },
    },
    items: [
      // HOOK: scan on the DPF flange (B-roll), then the headline over the engine
      { k: 'scan', t0: .12, t1: 1.02, box: [130, 470, 820, 900], lab: 'SCANARE DPF...', lab2: 'RISC: ÎNFUNDARE', at2: .62, labBelow: true },
      { k: 'kin', t: A.unu - .02, dur: .95, txt: 'GREȘEALA #1', col: '#FFD21F', y: 340, size: 128, rot: -3 },
      // #1 – cold engine + full throttle (dashboard B-roll)
      { k: 'gauge', t0: A.pornesti - .05, t1: A.directE + .3, top: 300, ico: 'snowflake', title: 'MOTOR RECE', sub: 'TURAȚIE', ends: ['0', 'MAX'], mid: 'RPM',
        needle: [[A.pornesti, .05], [A.incalz1 + .3, .1], [A.blana - .08, .95]], read: [[A.pornesti + .1, 'MOTOR PORNIT · ULEI RECE', '#62D8FF'], [A.blana - .06, '„BLANĂ” DIRECT, LA RECE', '#FF4B4B']] },
      // cutaway (outdoor segment: also keeps the parked cars' plates unreadable)
      { k: 'chain', t0: A.acest - .1, t1: A.doi - .45, top: FT, title: 'ANALIZA CAUZEI', sub: 'CAUZĂ › EFECT', nodes: [
        [A.acest, 'snowflake', 'CAUZA', 'MOTOR RECE + „BLANĂ” DIRECT', 'y'], [A.afecteaza, 'warning', 'EFECT DIRECT', 'AFECTEAZĂ DPF-UL', 'r'],
        [A.indirect, 'gear', 'EFECT INDIRECT', 'UZURĂ PREMATURĂ A COMPONENTELOR', 'r'], [A.infunde - .05, 'dashing_away', 'ÎN FINAL', 'DPF ÎNFUNDAT', 'r']] },
      // #2 – driving at low revs
      { k: 'kin', t: A.doi - .02, dur: .95, txt: 'GREȘEALA #2', col: '#FFD21F', y: 340, size: 128, rot: -3 },
      { k: 'def', t0: A.subturat3 - .1, t1: A.automata - .45, top: 262, term: 'SUBTURAT', text: 'Turație mică, mult timp: gaze prea reci pentru DPF' },
      { k: 'chip', t0: A.automata - .3, t1: A.tureE + .2, y: 330, ph: [[A.automata - .3, 'speech_balloon', '„DAR E AUTOMATĂ!”', 'blue'], [A.n1100 - .05, 'counter', 'DOAR 1100 RPM', 'red']] },
      { k: 'schem', t0: A.daca4 - .15, t1: A.plecam - .3, top: FT, type: 'dpfSoot', title: 'SCHEMĂ · FILTRUL DE PARTICULE', sub: 'SECȚIUNE', stepNames: ['SUBTURAT', 'SOLUȚIA'],
        P: { loadLab: 'SUBTURAT: FUNINGINEA SE ADUNĂ', holdLab: 'NEVOIE DE UN TRASEU MAI LUNG', l0: .25, l1: .82 },
        steps: [[A.daca4 - .15, 'Turație mică: gazele rămân reci, funinginea nu arde', 'r', 1], [A.traseu - .05, 'Din când în când: un traseu mai lung', 'y', 8]] },
      { k: 'kin', t: A.n100 - .02, dur: 1.0, txt: '100 KM', col: '#4ADE80', y: 340, size: 150, rot: -3 },
      { k: 'chip', t0: A.ruda - .15, t1: A.noiE5 + .2, y: 330, ph: [[A.ruda - .15, 'round_pushpin', 'LA O RUDĂ', ''], [A.bunici - .1, 'round_pushpin', 'LA BUNICI', ''], [A.munte - .1, 'round_pushpin', 'LA MUNTE', ''], [A.mare - .1, 'round_pushpin', 'LA MARE', 'blue']] },
      { k: 'chip', t0: A.si6 - .05, t1: A.asta6 - .35, y: 330, ph: [[A.si6 - .05, 'automobile', 'DRUM LUNG', 'green'], [A.turatie - .05, 'counter', 'TURAȚIE MAI RIDICATĂ', 'green']] },
      { k: 'schem', t0: A.asta6 - .1, t1: A.gazeleE + .3, top: FT, type: 'dpfSoot', title: 'SCHEMĂ · REGENERAREA DPF', sub: 'DRUM LUNG', stepNames: ['DRUM LUNG', 'REGENERARE', 'REZULTAT'],
        P: { l1: .82, hotLab: 'TURAȚIE MAI MARE: GAZE FIERBINȚI', cleanLab: 'DPF CURAT · EGR CURAT' },
        steps: [[A.asta6 - .1, 'Drum lung, turație mai mare: gazele se încălzesc', 'y', 7], [A.regen - .05, 'Regenerare: funinginea arde, filtrul se curăță', 'g', 2], [A.curatarea - .05, 'Se curăță și evacuarea, și recircularea gazelor (EGR)', 'g', 6]] },
      // #3 – short trips
      { k: 'kin', t: A.trei - .02, dur: .95, txt: 'GREȘEALA #3', col: '#FFD21F', y: 340, size: 128, rot: -3 },
      { k: 'chip', t0: A.condusul - .1, t1: A.scurteE7 + .4, y: 330, ph: [[A.condusul - .1, 'stopwatch', 'DRUMURI SCURTE', 'red']] },
      { k: 'chip', t0: A.biroul - .15, t1: A.vinaE + .2, y: 330, ph: [[A.biroul - .15, 'speech_balloon', '„BIROUL E LA 2 MINUTE!”', 'blue'], [A.naveti - .05, 'handshake', 'NU E VINA TA', 'green']] },
      { k: 'schem', t0: A.dar8 - .1, t1: A.intelegem8 - .1, top: FT, type: 'dpfSoot', title: 'SCHEMĂ · DRUMURI SCURTE', sub: '2 MINUTE', stepNames: ['DRUM SCURT', 'REZULTAT'],
        P: { l1: .8, stopLab: 'MOTOR RECE: REGENERARE ÎNTRERUPTĂ', clogLab: 'ÎNFUNDARE PREMATURĂ' },
        steps: [[A.dar8 - .1, 'Drum de 2 minute: regenerarea nu apucă să se termine', 'r', 3], [A.infundare - .05, 'Înfundare prematură a filtrului de particule', 'r', 5]] },
      // summary = patient file
      { k: 'file', t0: A.momentul9 - .15, t1: A.iarna - .35, top: FT, no: 'DPF-001', ecg: 'crit', title: 'FIȘA PACIENTULUI · DPF', rows: [
        [A.subturat9 - .05, 'CAUZA 1', 'MERS SUBTURAT', 'r', 'counter'], [A.distante9 - .05, 'CAUZA 2', 'DRUMURI SCURTE', 'r', 'stopwatch'],
        [A.incalzit10 - .05, 'CAUZA 3', 'MOTOR NEÎNCĂLZIT', 'r', 'snowflake']] },
      { k: 'chip', t0: A.iarna - .2, t1: A.vom - .3, y: 330, ph: [[A.iarna - .2, 'snowflake', 'IARNA: ÎNCĂLZEȘTE-L PUȚIN', 'blue'], [A.cinci - .05, 'stopwatch', 'NU 5 MINUTE!', 'yellow']] },
      { k: 'stamp', t: A.premature - .05, t1: A.particuleE10 + .05, y: 330, txt: 'PROBLEME PREMATURE', col: 'red', s: .62, rot: -4 },
      // solution: help + free diagnosis
      { k: 'chip', t0: A.daca11 - .1, t1: A.trebuiE11 + .2, y: 330, ph: [[A.daca11 - .1, 'handshake', 'VĂ AJUTĂM CU DRAG', 'green'], [A.devreme11 - .1, 'hourglass', 'DAR NU MAI DEVREME!', 'yellow']] },
      { k: 'file', t0: A.tineti12 - .15, t1: A.si12 - .1, top: FT, no: 'DPF-001', title: 'TRIAJ DPF', ico: 'stethoscope', rows: [
        [A.diagnoza - .05, 'DIAGNOZĂ', 'COMPLET GRATUITĂ', 'g', 'stethoscope'], [A.problema12 - .05, 'CÂND', 'LA O PROBLEMĂ CU DPF-UL', 'c', 'warning'],
        [A.stadiu - .05, 'AFLI', 'STADIUL EXACT AL DPF-ULUI', 'y', 'magnifying_glass_tilted_left']], stamp: [A.gratuita + .1, 'GRATUIT', 'green'] },
      { k: 'chip', t0: A.alegeti - .15, t1: A.nuE12 + .25, y: 330, ph: [[A.alegeti - .15, 'handshake', 'DECIZIA E A TA', 'green']] },
      { k: 'chip', t0: A.moduri - .2, t1: A.noiE13 + .2, y: 330, ph: [[A.moduri - .2, 'warning', 'ACESTE OBICEIURI...', 'red'], [A.aduce - .1, 'automobile', '...TE ADUC MAI DEVREME LA NOI', 'red']] },
      { k: 'chip', t0: A.mergeti - .15, t1: A.vacanta - .3, y: 330, ph: [[A.mergeti - .15, 'automobile', 'MAI DES CU MAȘINA LA DRUM', 'green']] },
      { k: 'kin', t: A.vacanta - .02, dur: 1.2, txt: 'VACANȚĂ!', col: '#4ADE80', y: 340, size: 150, rot: -3 },
      { k: 'tip', t0: SEND + .1, t1: TEND - .15, top: 470, title: 'REȚETA DPF DOCTOR', sub: 'SFAT DE INGINER · DPF', ico: 'stethoscope',
        rows: [[SEND + .35, 'snowflake', 'La rece: încălzește-l puțin, fără „blană”'], [SEND + 1.15, 'automobile', 'Subturat sau drumuri scurte? Din când în când, ~100 km'], [SEND + 1.95, 'stethoscope', 'Probleme cu DPF-ul? Diagnoza e gratuită']] },
    ],
    fx: [
      { k: 'xray', t0: .18, t1: .9 }, { k: 'punch', t: A.omori, a: .06, sh: 8 }, { k: 'red', t0: A.omori - .05, t1: A.stiiE, max: 1.4 },
      { k: 'glitch', t: A.unu - .16, d: .14 }, { k: 'flash', t: A.unu - .06, a: .4 },
      { k: 'punch', t: A.blana, a: .07, sh: 10 }, { k: 'red', t0: A.blana - .05, t1: A.directE + .2, max: .9 },
      { k: 'focus', t0: 9.38, t1: A.dpf2E + .3, fi: .25, fo: .3 },
      { k: 'punch', t: A.infunde, a: .05, sh: 6 },
      { k: 'glitch', t: A.doi - .14, d: .12 },
      { k: 'focus', t0: A.daca4 - .15, t1: A.plecam - .3 },
      { k: 'punch', t: A.n100, a: .05, sh: 6 },
      { k: 'focus', t0: A.asta6 - .1, t1: A.gazeleE + .3 }, { k: 'green', t0: A.regen - .05, t1: A.regen + .9, silent: true },
      { k: 'glitch', t: A.trei - .14, d: .12 },
      { k: 'focus', t0: A.dar8 - .1, t1: A.intelegem8 - .1 }, { k: 'red', t0: A.infundare - .05, t1: A.particuleE8 + .2, max: 1.4 },
      { k: 'focus', t0: A.momentul9 - .15, t1: A.iarna - .35 },
      { k: 'punch', t: A.premature, a: .05, sh: 6 }, { k: 'red', t0: A.premature - .05, t1: A.particuleE10 + .2, max: 1.1, silent: true },
      { k: 'focus', t0: A.tineti12 - .15, t1: A.si12 - .1 }, { k: 'green', t0: A.gratuita - .05, t1: A.gratuita + .8 },
      { k: 'green', t0: A.vacanta - .05, t1: A.vacanta + .9, silent: true },
    ],
    sfx: [[A.succes, 'shimmer', .55]],
    bursts: [[A.gratuita + .1, 700, 760, 6, 260, .8], [A.vacanta, 540, 340, 6, 330, .8], [A.succes, 540, 520, 6, 300, .7]],
  };
};
