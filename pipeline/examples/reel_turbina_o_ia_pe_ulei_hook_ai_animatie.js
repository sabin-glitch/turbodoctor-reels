// v3 – „A luat-o turbina pe ulei” (diesel runaway; Sabin: „e incorect spus ambalarea, ci faptul că ia turbina pe ulei”), 16.11.2026
// Hook (v7): scenă Higgsfield într-un singur cadru: un Golf 5 la ralanti începe singur să se tureze, fumul alb iese neîntrerupt pe țeavă și se îngroașă,
// șoferul sare de la volan și se ia cu mâinile de cap. Cât se turează, vocea lui Sabin (ElevenLabs „Sabin”) spune „Turbina o ia pe ulei! Află de ce.”,
// cu textul mare pe aceleași cuvinte; apoi „Știi de ce se întâmplă asta? Hai să-ți explic inginerește.” și explicația animată 3D.
// Sursa: animația turbosuflantei pe motor (tools/anim_turbo) cu regie nouă (runaway_tail.js): motorul care a luat-o pe ulei, autoaprinderea,
// etanșarea turbinei prin presiune, cele 4 cauze, uleiul pe admisie, bucla, cheia și clapeta, ce cedează, cum îl oprești.
// Etichetele de pe piese, săgețile de presiune, turometrul și blitzurile sunt în animație; compozitorul pune hook-ul boom, bara de etape,
// chip-urile (doar ideea principală, nu repetă etichetele), listele, ștampila, Rețeta (vorbită) și subtitrările.
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND }) => {
  const L = (i, w, k) => aw(i, w, k);
  const HK = aw(2, 'Dieselul') - .22;                 // tăietura din animație (dip la negru)
  const D2 = aw(24, 'Dacă') - .22, D4 = ew(26, 'mâna.') + .30;
  // hook v6 (16.11, refăcut după filmări reale: Jetta 1.9 TDI, Golf 4 TDI, „mad run away diesel”): un singur cadru, fără tăietură (build_hook_v6b.py):
  // Golf 5 la ralanti → fumul apare la 0,15 s și crește neîntrerupt (Higgsfield Kling 3.0: clipul hf4_k0 + continuarea hf7_e0 din cadrul lui 54, la 1,25×);
  // ușa șoferului se deschide la 3,66 s, omul e jos la ~4,7 s și se ia cu mâinile de cap la ~5,9 s, în același decor, cu fumul în spate;
  // sunet (make_hook_bed7.py): turația urcă ÎNCONTINUU 870 → ~5.800 rpm (0,56 octave/s), fără salturi și fără limitator, cu șuieratul turbinei
  // care urcă odată cu ea; motorul coboară sub voce și revine după ea, rămâne în fundal sub „Știi de ce se întâmplă asta?”, apoi motorul 3D până la HK
  // hook v7 (16.11, cerut de Sabin: „în momentul în care se turează, tu să spui: turbina o ia pe ulei, află de ce”): rândul 0 al vocii e
  // „Turbina o ia pe ulei! Află de ce.” (splice_hook_vo2.py), cu titlurile pe începuturile de cuvânt din anvelopa vocii; imaginea e cea din v6
  const AICUT = 7.1;                                  // 0–AICUT: cadrul cu mașina, fumul și șoferul
  const B1 = .12, B2 = aw(0, 'pe') - .02;             // „TURBINA O IA” din primele cadre, impactul pe „PE ULEI!”
  const B3 = aw(0, 'Află') - .03;                     // „AFLĂ DE CE!” (impact); cele trei rânduri rămân împreună până la „Știi…” (hook în trepte)
  const OUT2 = aw(1, 'Știi') - .12;
  const HAI = aw(1, 'Hai'), ING = aw(1, 'inginerește.');
  const CA = 410, CB = 562;                           // chip-uri: sus (fără turometru) / sub turometru (bucla, cheia, clapeta)
  const items = [], fx = [];

  // ---- HOOK: textul mare cerut de Sabin, pe vocea lui: „Turbina o ia pe ulei! Află de ce.” – trei rânduri care se adună și rămân pe ecran
  items.push({ k: 'boom', t: B1, dur: OUT2 - B1, txt: 'TURBINA O IA', y: 259, size: 118, col: '#FFFFFF', from: 3.0, sh: 14, ca: 18, riser: false, bg: .4, cg: .2, glow: 'rgba(255,255,255,.3)' });
  items.push({ k: 'boom', t: B2, dur: OUT2 - B2, txt: 'PE ULEI!', y: 415, size: 182, col: '#FFD21F', from: 3.4, sh: 26, ca: 24, riser: false, bg: .75, cg: .3, glow: 'rgba(255,210,31,.5)' });
  fx.push({ k: 'flash', t: B2 - .11, a: .6 }, { k: 'punch', t: B2, a: .14, sh: 28 }, { k: 'shock', t: B2 + .01, x: 540, y: 1080, r: 700, n: 2, col: '#FFD21F', col2: '#FFFFFF' }, { k: 'glitch', t: B2, d: .16 });
  items.push({ k: 'boom', t: B3, dur: OUT2 - B3, txt: 'AFLĂ DE CE!', y: 585, size: 146, col: '#FF4B4B', from: 3.6, sh: 36, ca: 30, riser: false, bg: .85, cg: .35, glow: 'rgba(255,75,75,.6)' });
  fx.push({ k: 'flash', t: B3 - .11, a: .75 }, { k: 'punch', t: B3, a: .18, sh: 36 }, { k: 'shock', t: B3 + .01, x: 540, y: 1080, r: 760, n: 2, col: '#FF4B4B', col2: '#FFFFFF' }, { k: 'glitch', t: B3, d: .2 });
  // ---- trecerea în motor: „Hai să-ți explic inginerește.” peste animația 3D (turometrul e pe rândul subtitrărilor, deci titluri)
  fx.push({ k: 'flash', t: AICUT - .08, a: .8 }, { k: 'glitch', t: AICUT, d: .22 });
  items.push({ k: 'boom', t: HAI, dur: HK - .05 - HAI, txt: 'HAI SĂ-ȚI EXPLIC', y: 330, size: 112, col: '#FFFFFF', from: 3.0, sh: 14, ca: 18, riser: false, bg: .4, cg: .2 });
  items.push({ k: 'boom', t: ING, dur: HK - .05 - ING, txt: 'INGINEREȘTE', y: 505, size: 150, col: '#FFD21F', from: 3.4, sh: 22, ca: 24, riser: false, bg: .65, cg: .3, glow: 'rgba(255,210,31,.45)' });
  fx.push({ k: 'punch', t: ING, a: .12, sh: 24 }, { k: 'shock', t: ING + .01, x: 540, y: 980, r: 700, n: 2, col: '#FFD21F', col2: '#FFFFFF' });

  // ---- FIZICA · de ce poate arde uleiul
  items.push({ k: 'chip', t0: L(2, 'aprinde') - .1, t1: ew(4, 'motorină.') + .25, y: CA,
    ph: [[L(2, 'aprinde') - .1, 'fire', 'DIESELUL SE APRINDE SINGUR', 'yellow'], [L(3, 'ci') - .05, 'fuel_pump', 'PUTEREA = CÂTĂ MOTORINĂ INJECTEZI', 'yellow'],
         [L(4, 'Dacă') - .05, 'oil_drum', 'ULEIUL DEVINE COMBUSTIBIL', 'red']] });
  // ---- FIZICA · cum ține turbina uleiul
  items.push({ k: 'chip', t0: L(6, 'segmenți') - .1, t1: ew(8, 'baie.') + .2, y: CA,
    ph: [[L(6, 'segmenți') - .1, 'shield', 'SEGMENȚII NU ȚIN ULEIUL', 'yellow'], [L(7, 'Etanșarea') - .05, 'dashing_away', 'PRESIUNEA ȚINE ULEIUL ÎNĂUNTRU', 'yellow']] });

  // ---- CAUZA · cele 4 situații
  items.push({ k: 'list', t0: L(9, 'Echilibrul') - .05, t1: ew(13, 'DPF.') + .3, top: 268, ico: 'warning', title: 'ECHILIBRUL SE STRICĂ',
    rows: [[L(10, 'Unu:'), 'BUCȘE UZATE: AXUL JOACĂ', 'bad'], [L(11, 'Doi:'), 'RETUR ÎNFUNDAT / CARTER CU PRESIUNE', 'bad'],
           [L(12, 'Trei:'), 'FILTRU DE AER ÎMBÂCSIT', 'bad'], [L(13, 'Patru:'), 'PREA MULT ULEI ÎN BAIE', 'bad']] });
  items.push({ k: 'chip', t0: L(14, 'Uleiul') - .05, t1: ew(14, 'cilindri.') + .25, y: CA, ph: [[L(14, 'Uleiul') - .05, 'oil_drum', 'ULEI › INTERCOOLER › CILINDRI', 'red']] });

  // ---- BUCLA (turometrul e sus, în animație)
  items.push({ k: 'chip', t0: L(15, 'bucla.') - .1, t1: aw(19, 'Calculatorul') - .25, y: CB,
    ph: [[L(15, 'bucla.') - .1, 'warning', 'ÎNCEPE BUCLA', 'red'], [L(16, 'Pompa') - .05, 'oil_drum', 'TURAȚIE MAI MARE › MAI MULT ULEI', 'red'],
         [L(17, 'Crește') - .05, 'dashing_away', 'PRESIUNE MARE ÎN CARTER', 'red'], [L(18, 'Mai') - .05, 'rocket', 'MAI MULT ULEI › TURAȚIE MAI MARE', 'red']] });
  items.push({ k: 'kin', t: L(19, 'degeaba:') - .02, dur: .95, txt: 'DEGEABA!', col: '#FF3B30', y: 760, size: 190, rot: -5 });
  fx.push({ k: 'punch', t: L(19, 'degeaba:'), a: .1, sh: 20 });

  // ---- de ce nu se oprește de la cheie · clapeta
  items.push({ k: 'chip', t0: L(20, 'cheia') - .1, t1: ew(20, 'ele.') + .2, y: CB,
    ph: [[L(20, 'cheia') - .1, 'key', 'CHEIA TAIE DOAR MOTORINA', 'yellow'], [L(20, 'uleiul') - .05, 'oil_drum', 'ULEIUL NU TRECE PRIN INJECTOARE', 'red']] });
  items.push({ k: 'chip', t0: L(22, 'stă') - .1, t1: ew(22, 'departe.') + .2, y: CB, ph: [[L(22, 'stă') - .1, 'stopwatch', 'CLAPETA STĂ ÎNCHISĂ DOAR CÂTEVA SECUNDE', 'yellow']] });

  // ---- ce cedează
  items.push({ k: 'stamp', t: L(23, 'gripează.') + .1, t1: D2 - .12, y: 900, txt: 'MOTOR DISTRUS', col: 'red', s: .82, rot: -7 });

  // ---- SOLUȚIA · cum îl oprești
  items.push({ k: 'list', t0: L(24, 'Dacă') - .02, t1: D4 - .12, top: 268, ico: 'police_light', title: 'DACĂ ȚI SE ÎNTÂMPLĂ',
    rows: [[L(24, 'apăsa'), 'NU AMBREIAJ, NU NEUTRU', 'bad'],
           [L(25, 'treapta'), 'TREAPTA MAXIMĂ + FRÂNĂ TARE'], [L(25, 'brusc'), 'ELIBEREZI BRUSC AMBREIAJUL'],
           [L(26, 'aerul:'), 'TAI AERUL: PLACĂ / STINGĂTOR CO2'], [L(26, 'niciodată'), 'NICIODATĂ CU MÂNA', 'bad']] });

  // ---- Rețeta (vorbită: „Ca să nu ajungi aici…”), rândurile intră pe cuvinte; animația trece prin baie, filtrul de aer, intercooler
  items.push({ k: 'tip', t0: L(27, 'Ca') - .1, t1: SEND - .15, top: 268, title: 'REȚETA TURBO DOCTOR', sub: 'SFAT DE INGINER · TURBO DIESEL', ico: 'stethoscope',
    rows: [[L(27, 'urmărește') - .05, 'oil_drum', 'Nivelul uleiului urcă pe jojă? E semnal de alarmă.'],
           [L(27, 'schimbă') - .05, 'dashing_away', 'Schimbă filtrul de aer la timp.'],
           [L(27, 'când') - .05, 'wrench', 'Turbină cedată? Curăță intercoolerul și țevile înainte de montaj.']] });

  return {
    hideCap: [[0, aw(1, 'Știi') - .1], [AICUT, HK]],     // rândul 0 e pe titlurile mari; „Știi de ce se întâmplă asta?” cu subtitrări peste omul care se ia cu mâinile de cap; în 3D turometrul stă pe rândul subtitrărilor
    stages: [[HK + .45, 'FIZICA'], [aw(9, 'Echilibrul') - .1, 'CAUZA'], [aw(15, 'Și') - .1, 'BUCLA'], [aw(24, 'Dacă') - .1, 'SOLUȚIA'], [aw(27, 'Ca') - .1, 'PREVENȚIE']],
    bgFix: [[0, SEND]],
    items, fx,
    tags: {
      0: { turbina: 'c', ulei: 'y', afla: 'r' }, 1: { stii: 'y', intampla: 'y', asta: 'r', explic: 'y', inginereste: 'y' },
      2: { scanteie: 'y', comprima: 'c', aerul: 'c', '700900': 'y', grade: 'y', aprinde: 'r', singura: 'r' }, 3: { aer: 'c', motorina: 'y', injectata: 'y' },
      4: { uleiul: 'y', arde: 'r', admisie: 'c', motorina: 'y' }, 5: { uleiul: 'y', turbina: 'c' },
      6: { ulei: 'y', presiune: 'y', litri: 'y', segmenti: 'c', simeringuri: 'c' }, 7: { presiune: 'y', etansarea: 'c' },
      8: { compresor: 'c', turbina: 'c', corpul: 'c', central: 'c', baie: 'g' }, 9: { patru: 'y', situatii: 'y' },
      10: { bucsele: 'r', uzate: 'r', axul: 'c', joaca: 'r', segmentii: 'c' }, 11: { returul: 'r', infundat: 'r', presiunea: 'r', carter: 'c' },
      12: { filtrul: 'c', imbacsit: 'r', depresiune: 'r', trage: 'r' }, 13: { prea: 'r', mult: 'r', motorina: 'y', dpf: 'c' },
      14: { compresorului: 'c', intercooler: 'c', cilindri: 'c' }, 15: { bucla: 'r', arde: 'r', turatia: 'y', creste: 'r' },
      16: { pompa: 'c', ulei: 'y', stricata: 'r' }, 17: { presiunea: 'r', carter: 'c', intercooler: 'c' }, 18: { ulei: 'y', turatie: 'y' },
      19: { calculatorul: 'c', taie: 'y', degeaba: 'r', propriul: 'r', ulei: 'y' }, 20: { cheie: 'y', cheia: 'y', injectoarele: 'c', uleiul: 'y' },
      21: { clapeta: 'c', admisie: 'c', inchide: 'g', salveaza: 'g' }, 22: { urgente: 'r', secunde: 'y', galerie: 'c', arde: 'r' },
      23: { supapele: 'r', pistoanele: 'r', rupe: 'r', biela: 'r', gripeaza: 'r' }, 24: { ambreiajul: 'r', neutru: 'r', sarcina: 'y' },
      25: { treapta: 'g', franezi: 'g', brusc: 'g', ambreiajul: 'g' }, 26: { aerul: 'g', placa: 'g', rigida: 'g', stingator: 'g', co2: 'g', mana: 'r' },
      27: { nivelul: 'y', uleiului: 'y', filtrul: 'c', aer: 'c', timp: 'g', turbina: 'c', curata: 'g', intercoolerul: 'c' },
    },
  };
};
