# Reel „Eroarea P2002: ce înseamnă de cele mai multe ori pe 2.0 Euro 6 din gama VAG” (15.11.2026)

Reel făcut din filmul Blender „Eroare de eficiență DPF la EA288”, remontat pe vocea „Sabin” din ElevenLabs. Scripturile filmului sunt în `film/`;
cadrele randate de Blender (`pl.tar.xz`, 438 MB), fonturile și filmul sunt în /mnt/project-files/animatii/sursa/dpf-ea288/ (acolo e și o copie a acestui folder, în `reel/`).
Cerut de Sabin pe 15.11.2026: „Animația e bună, te rog, dă drumul și fă un reel cu hook puternic. Eroarea P2002, eficiență.
Ce înseamnă de cele mai multe ori pe motoarele 2.0 Euro 6 de pe gama VAG. Și după aia explicația cu vocea mea.”

Rezultat: `animatii/TurboDoctor_Reel_Eroare_P2002_EA288.mp4` (129,4 s = poveste 121,9 s + card de final 7,5 s), `_coperta.jpg` (cadrul de la 8,55 s)
și `_text_postare.txt`. **Stare: livrat spre aprobare pe 15.11, neprogramat.** La programare: etichetă AI pe TikTok și Instagram (voce generată),
Facebook ca POST cu titlu (peste 90 s), fără bifele de conținut comercial.

## Ce spune (16 rânduri, `vo_script.json`)

- **Hook (rândul 0), pe vorbele lui Sabin:** „Eroarea P2002, eficiență filtru de particule. Ce înseamnă, de cele mai multe ori, pe motoarele 2.0 Euro 6 de pe gama VAG?”
  („filtru de particule” e adăugat, ca să fie clar despre ce eficiență e vorba).
- **Răspunsul (rândul 1):** „De cele mai multe ori, filtrul nu are nimic. Problema e la EGR și la răcitorul de gaze. Hai să-ți arăt de ce.”
  Răspunsul e luat din reelul aprobat al lui Sabin „Ai motorul 2.0 Euro 6 din gama VAG?”; **de confirmat de el**.
- **Explicația (rândurile 2–15), în altă ordine decât filmul:** traseul gazelor (s01, s02) → filtrul (s03) → cum judecă calculatorul, calculat față de măsurat (s04, s05)
  → cauza 1, cea mai deasă: răcitorul de gaze înfundat, apoi fisurat (s07, s08, s09) → cauza 2: supapa EGR (s10) → cauza 3: furtunașele senzorului (s06)
  → cauza 4: aerul pierdut și debitmetrul (s16) → cauza 5: injecția (s11, s12) → cauza 6: uleiul ars, cenușa (s13, s14, s15) → lista de diagnoză (s17).
  Formulările sunt ale mele; baza tehnică e cea a filmului (`film/README.md` și documentul „Note de verificare”). Gramele din indicator sunt exemple.
- **Sunet:** doar vocea (`v2.json`: fără muzică, fără efecte), ca la ultimele reel-uri din animații.
- **Fără îndemn pe video sau în text:** se termină cu lista de diagnoză și cu cardul de final standard.

## Cum e făcut

Filmul nu e re-temporizat cu o hartă. Planurile lui sunt puse **în ordinea și în timpul vocii**: `reel_story.py` citește `reel_vo/cues.json`
(momentele pe cuvinte) și leagă de ele tăieturile dintre planuri, trecerile dintre stări, particulele, titlurile, etichetele și indicatorul
„funingine calculată / măsurată”. O voce nouă înseamnă momente noi și randarea cadrelor din nou (fără Blender: cadrele fixe rămân aceleași).

| Fișier | Rol |
|---|---|
| `reel_story.py` | planul reelului: cele 18 planuri (`RShot`), așezarea în cadru a fiecăruia (`KB(durată, zoom0, zoom1, pan0, pan1, rz, rx, ry)`), titlurile, etichetele (`LABELS`: text, punct 3D, poziție, cuvântul pe care apare), indicatorul, panourile și lista de final. Rulat, scrie `hud_reel_data.js` și tipărește planurile |
| `comp_reel.py` | compune cadrele: cadrul fix Blender + particule + texte → `<reel>/frames_base/NNNNN.jpg`. `--part i n` pentru procese în paralel, `--range f0 f1`, `--frames …`; sare peste cadrele care există. Cadre de probă: `--t 3 12.5 60 --out proba.jpg --sheet 4 [--guides] [--crop y0 y1]` |
| `hud_reel.html`, `hud_reel_render.js`, `hud_reel_data.js` | textele de pe ecran ca imagini transparente (`hudr/NNNNN.png`): `node hud_reel_render.js [f0 f1] [--part i n] [--out dir] [--t …]` |
| `../../pipeline/examples/reel_p2002_ea288_animatie.js` | `reel.js` al acestui reel, pentru compozitorul din pipeline v2: titlurile `boom` din hook, în două trepte, pe cuvintele lui Sabin; culorile din subtitrări (`tags`); `hideCap` pe hook; `bgFix` pe toată povestea |
| `film/` | scripturile filmului (modele Blender, camere, particule, montaj, texte) și `film/README.md`; `fxlib.py` are limita de nucleu reparată |
| `reel_out/` | `v2.json`, `cover_t.json`, `frames_meta.json` din dosarul `out/` al reelului |
| `vo_script.json`, `make_vo.py`, `vo_qc.py`, `asr2.py`, `run_iso.sh`, `mix_qc.py` | vocea rând cu rând, măsurată și verificată cu două recunoașteri (ca la reel-ul blow-off); scripturile rulează cu `run_iso.sh` (Python `-I`), fiindcă audio descărcat e dată străină |
| `map/` | `cues.json`, `timeline.json`, `picks.json` (variantele alese): momentele pe cuvinte cu care a fost randat reelul. Pista de voce nu e în repo; e în /mnt/project-files/animatii/sursa/dpf-ea288/reel/tools/vo/vo_track.flac |
| `rsheet.sh`, `plates_raw.py`, `probe.py`, `measure.cjs`, `psheet.py`, `sheet.py`, `rlib.cjs` | cadre de probă: foaie cu textele și cu ghidaje, planurile fără așezare, proiecția unui punct 3D (ancora unei etichete), lățimea unui titlu `boom` în fontul compozitorului, foaie de contact din cadre |
| `clipscan.py` | caută stropii de particule tăiați de limita de nucleu (vezi „Capcane”) |

Ca să ruleze, `reel_story.py`, `comp_reel.py` și `hud_reel.*` se pun în același dosar cu scripturile din `film/` (`fxlib.py`, `shots.py`, `comp.py`, `story.py`, `gas.py`,
`layout.py`, `out/meta.json`), cu `pl/` despachetat acolo din `pl.tar.xz` și cu `fonts/` un nivel mai sus; `map/cues.json` se copiază în `reel_vo/cues.json` (sau `P2002_CUES=<cale>`).
Căile scrise în uneltele de probă (`/home/claude/dpf/work`, `/home/claude/p2002/tools`) sunt cele de pe mașina pe care a fost făcut reelul.

## Pașii

Fluxul comun (voce, folderul reelului, `finish.sh`) e descris în `animatii/sursa/blow-off/reel/README_flux.md`, secțiunea „Pașii”. Aici:

1. **Vocea**: `eleven_v4`, vocea „Sabin”, fiecare rând generat separat în două variante, cu etichetele din `vo_script.json`
   (hook-ul: `[serious] [matter of fact] [conversational tone]`); fișierele vin prin `fetch-sources`, apoi `./run_iso.sh make_vo.py lines <dir>`
   → `vo/vo_track.wav`, `timeline.json`, `cues.json`. Povestea are 121,93 s.
2. **Textele**: `python reel_story.py && node hud_reel_render.js` (3.658 de imagini în `hudr/`; cu `--part i 4` în patru procese).
3. **Cadrele**: `python comp_reel.py --out <reel>/frames_base --part i 4`, de patru ori în paralel (i = 0…3; cam 3–4 cadre pe secundă în total, deci în jur de 20 de minute pentru tot reelul).
4. **Reelul**: `new_reel.sh p2002_ea288 <mp4 negru de durata poveștii>`, vocea în `audio/vo_track.wav`, cronologia în `out/timeline.json`,
   `out/v2.json` = `{"narrator": true, "orig_gain": 0, "music": false, "sfx": false}`, `python3 retime.py`, `out/frames_meta.json` = `{"n_out": 3883}`,
   `out/cover_t.json` = `{"t": 8.55}`, `reel.js`; apoi `python3 render.py --prep` și, din folderul reelului, `bash finish.sh p2002_ea288 Reel_Eroare_P2002_EA288`
   (randarea finală durează cam 5 minute și jumătate).
5. **Verificarea**: `./run_iso.sh mix_qc.py <reel>/audio/mix_final.wav` (fiecare rând recunoscut din mix), `out/verify.log`, cadre scoase din MP4-ul final.

## Așezarea în cadru

- Subtitrările stau între y 1290 și 1530. Sus: titlul la y 196, pastila („FILTRUL E BUN” / „FILTRUL E VICTIMA”) la 318, indicatorul în dreapta (x 680–1030, y 196–446).
  Scena utilă e între y ≈ 330 și 1280; etichetele din dreapta se opresc înainte de x ≈ 968.
- Fiecare plan are deplasarea lui pe verticală (`ry`), aleasă din planșa cu planurile fără așezare (`plates_raw.py`) și din proiecția punctelor (`probe.py`):
  cu o singură deplasare pentru toate, subiectul ajungea sub titlu (turbina în s01, senzorul în s04, dopurile filtrului în s03).
- Un plan urcat în cadru își topește marginea de jos în fundal (altfel rămâne o linie sub subtitrări). Motorul din hook e micșorat (zoom 0,86–0,90)
  și are marginile topite (`edge_mask`), ca titlurile să aibă loc.
- Hook: titluri `boom` între y 350 și 940 (în afara zonelor acoperite de aplicații și de decupajele de grilă 4:5 și 3:4), cardul de tester
  „P2002 / FILTRU DE PARTICULE: EFICIENȚĂ SUB PRAG” la y 1420, vizibil din primul cadru; subtitrările ascunse până la răspuns.

## Capcane

- **Stropii mari tăiați în pătrate.** `fxlib.Canvas.RMAX` limita jumătatea nucleului unui strop la 56 px. Fumul scăpării de la furtunașul crăpat (s06)
  are stropi cu raza de până la ~200 px, deci gaussianul lor era tăiat și rămâneau pătrate vizibile în jurul fisurii. Limita e acum 420 (în `film/fxlib.py`).
  Defectul era și în filmul lung livrat pe 15.11 dimineața; planurile s06 și s07 ale filmului au fost refăcute tot pe 15.11 (varianta veche e în /mnt/project-files/animatii/sursa/dpf-ea288/arhiva/).
  `clipscan.py` arată, plan cu plan, câți stropi ar fi tăiați și cât de înaltă ar fi treapta de la margine.
- Efectul `glitch` al compozitorului de reel-uri scoate dreptunghiuri negre pe cadrele închise ale animației: în hook sunt doar `flash` și `shock`.
- `punch` nu are efect sub `bgFix`: loviturile de zoom din hook sunt făcute în cadre (`PUNCH` în `reel_story.py`).
- `render.py --prep` are nevoie de cadrul `int(tip_end × 30) − 1` (aici 3656) pentru fundalul cardului de final.
- Pe mașina din cloud, procesele lăsate în fundal înaintează doar cât rulează o comandă: randările lungi se așteaptă cu o buclă în prim-plan.
