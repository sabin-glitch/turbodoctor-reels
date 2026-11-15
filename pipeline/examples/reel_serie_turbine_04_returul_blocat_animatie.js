// v2 – Seria „De ce se strică turbinele”, cauza 4 din 13: uleiul care nu se mai poate scurge (15.11.2026)
// Reel animat 3D în secțiune (tools/anim_serie_turbine, episodul ep4), cu vocea „Sabin” din ElevenLabs, rând cu rând.
// Cerut de Sabin: fiecare film începe cu numele seriei și „cauza X din 13”, se termină cu „La Turbo Doctor suntem experți…”
// și cu ecranul de final cu diagnoză gratuită, numărul de telefon și pictogramele serviciilor (endPhone + endIcons).
// Etichetele de pe piese și eticheta „Cauza 4 din 13” sunt în animație; compozitorul pune titlurile boom din hook, subtitrările și ecranul de final.
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND }) => {
  const T1 = 0.27, T2 = 2.04, T3 = 4.04, T4 = 6.04, S1 = 8.76, HK = 12.83;
  return {
    hook: null,
    stages: null,
    endIcons: true,
    endPhone: true,
    hideCap: [[0, S1 - .1]],
    items: [
      { k: 'boom', t: T1, dur: T3 - .12 - T1, txt: 'DE CE SE STRICĂ', y: 448, size: 132, col: '#FFFFFF', from: 3.2, sh: 18, ca: 22, riser: false, bg: .6, cg: .3 },
      { k: 'boom', t: T2, dur: T3 - .12 - T2, txt: 'TURBINELE?', y: 612, size: 180, col: '#FFD21F', from: 3.0, sh: 20, ca: 24, riser: false, bg: .7, cg: .3 },
      { k: 'boom', t: T3, dur: HK - .1 - T3, txt: 'CAUZA 4 DIN 13', y: 455, size: 150, col: '#FFD21F', from: 3.2, sh: 18, ca: 22, riser: false, bg: .6, cg: .3 },
      { k: 'boom', t: T4, dur: HK - .1 - T4, txt: 'ULEIUL NU SE MAI SCURGE', y: 612, size: 96, col: '#FF4B4B', from: 3.0, sh: 20, ca: 24, riser: false, bg: .7, cg: .3, glow: 'rgba(255,75,75,.6)' },
      { k: 'chip', t0: S1 + .9, t1: HK - .15, y: 1226, ph: [[S1 + .9, 'eyes', 'TOATE CAUZELE: TIKTOK · FACEBOOK · YOUTUBE', 'yellow']] },
    ],
    fx: [
      { k: 'punch', t: T1, a: .08, sh: 16 }, { k: 'punch', t: T2, a: .1, sh: 22 }, { k: 'glitch', t: T2, d: .14 },
      { k: 'punch', t: T3, a: .08, sh: 16 }, { k: 'punch', t: T4, a: .14, sh: 30 }, { k: 'glitch', t: T4, d: .18 },
    ],
    bgFix: [[0, SEND]],
    tags: {"1": {"tiktok": "c", "facebook": "c", "youtubeul": "c"}, "2": {"presiune": "y", "singur": "y", "retur": "y"}, "3": {"infundat": "r", "calamina": "r", "indoit": "r"}, "4": {"carter": "y", "presiune": "r", "infundata": "r", "uzati": "r", "milibari": "y"}, "5": {"aduna": "r", "impins": "r", "etansari": "y", "admisie": "c", "evacuare": "r"}, "6": {"fum": "c", "albastru": "c", "intercooler": "c", "consum": "r", "cauza": "y"}, "7": {"ars": "r", "incleiaza": "r", "supraturari": "r", "necontrolate": "r"}, "8": {"problema": "r", "ramane": "r"}, "9": {"eviti": "g", "curat": "g", "corect": "g", "silicon": "y", "verificata": "g", "maxim": "g"}, "10": {"turbo": "y", "doctor": "y", "experti": "y"}, "11": {"evita": "g", "tarziu": "g"}, "12": {"diagnoza": "g", "gratuita": "g"}},
  };
};
