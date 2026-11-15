# Seria „De ce se strică turbinele” (15.11.2026): reel-uri animate în secțiune, câte unul pe cauză

Cerută de Sabin pe 15.11.2026, după documentul de research (13 cauze, din surse de producători: MAHLE, Garrett, BorgWarner, Holset, Melett).
Fiecare film: începe cu „Seria «De ce se strică turbinele». Astăzi prezentăm cauza X din 13: …” + „Vezi toate cauzele pe TikTok, Facebook și
YouTube-ul nostru”, explică mecanismul în secțiune, apoi „Cum eviți?”, și se încheie cu „La Turbo Doctor suntem experți în aceste probleme. Acum că
știi cum poți evita această problemă, ar trebui să ajungi cât mai târziu la noi. Iar dacă ai nevoie de noi, la noi diagnoza este gratuită.” și cu
ecranul de final cu diagnoză gratuită, **numărul de telefon** (`endPhone: true`, nou în compozitor) și pictogramele serviciilor (`endIcons: true`).
Sabin nu dă poze cu piese distruse: totul este simulat. Sunet: doar vocea (`"music": false, "sfx": false`).

Scena este cea din `tools/anim_turbo` (`index_src.html`, three.js r128, cu stratul `FAIL`), peste care vin:

| Fișier | Rol |
|---|---|
| `fx.js` | stratul de efecte al seriei, totul condus de numere din `FX`: ulei murdar (`dirty`, `dirt`), ax zgâriat (`score`), palete care ating carcasa (`rub`), filtru de ulei în secțiune cu supapă de ocolire (`showFilt`, `filt`, `bypass`), căldură care trece din evacuare în lagăre (`hotT`, `soak`), calamină (`coke`), fum (`smoke`), retur înfundat (`dclog`), ulei care se adună în carcasa lagărelor (`flood`), ulei pe lângă etanșări (`leak`, `leakSide`), fum albastru (`blue`), ulei în aerul de admisie și în intercooler (`oilAir`, `pool`), gaze scăpate în carter (`blowby`), depuneri la intrarea în turbină (`vcrust`), amorsare / frontul uleiului (`prime`), nivel scăzut în baie (`low`), ulei rece (`cold`) |
| `fx2.js` | al doilea strat de efecte, pentru cauzele 5–13: praf și corpuri străine pe admisie (`sand`, `sandB`, `sandMetal`, `window.FODS`, `window.HITC`), filtrul de aer rupt / înfundat / lipsă (`afTorn`, `afClog`, `afHide`), palete rupte (`chipC`, `chipT`), bucată venită din motor prin galerie (`window.FODT`, `window.HITT`), gaze prea fierbinți și funingine (`gasHot`, `sootGas`, `sootOut` = fum negru la ieșire, în `fx.js`), fisuri (`crack`, `crackW`), roata care crește la supraturare (`grow`, `rubSide`), lupa (`inset`, `insetKind`: 0 = inelul geometriei variabile cu `vgtPos`, `vgtSoot`, `vgtJit`, `vgtBent`; 1 = spatele roții compresorului cu `peel`, „coaja de portocală”), filtrul de particule / catalizatorul în secțiune după turbină (`showDpf`, `dpfClog`), gaze trecute pe lângă segmentul de etanșare (`gasIn`), scăpări (`hoseLeak` = furtun fisurat, `manLeak` = galerie crăpată), silicon în intrarea uleiului (`sil`), resturi rămase în admisie și în intercooler (`chips`), indicatorul de sus (`window.GAUGE`, cu `state` opțional pentru trei stări) |
| `dir_pre.js`, `dir_post.js` | regia comună: momente pe cuvinte `W(rând,'cuvânt')`, piste `TR` (inclusiv `eng` = turația motorului, `spn` = turația turbinei, `gas`, `airK`), cadre de cameră `SHOTS`, etichete, eticheta fixă „Cauza X din 13” (`#badge`, y 196–290) |
| `ep1.js` … `ep13.js` | câte un episod: pistele, etichetele și camera lui (1 lipsa ungerii, 2 uleiul murdar, 3 oprirea motorului la cald, 4 uleiul care nu se mai poate scurge, 5 corpuri străine pe admisie, 6 corpuri străine pe evacuare, 7 temperatura gazelor, 8 supraturarea, 9 geometria variabilă blocată, 10 filtrul de particule înfundat, 11 scăpări și înfundări pe traseu, 12 greșelile de montaj, 13 uzura motorului). De la 5 încolo momentele stau într-un obiect `Q={…}`, ca să nu se redeclare constantele scenei |
| `build_reel.py <epN>` | scrie `epN/reel.html` din `index_src.html` + `fx.js` + `fx2.js` + `dir_pre.js` + `epN.js` + `dir_post.js` + `epN/vo/cues.json` (lângă: `fonts/` și `three.min.js`) |
| `stills.js <epN> <prefix> t1,t2,… [coloane]` | cadre de probă + foaie de contact |
| `render_frames.js <epN> <dir> <primul> <ultimul> [pas]`, `render_all.sh` | randarea, 4 procese intercalate pe episod, cu reluare (≈ 0,4 s/cadru în total) |
| `render_queue.sh`, `finish_queue.sh` | coada de randare (episoadele scrise rând cu rând în `render_queue.txt`, pe măsură ce sunt gata; `END` o oprește) și coada de montaj (așteaptă `EPn DONE` în `render_status.txt`, apoi `render.py --prep` și `finish.sh` în folderul reel-ului) |
| `make_vo.py`, `vo_qc.py`, `asr2.py`, `run_iso.sh` | vocea rând cu rând (ca la blow-off): se copiază lângă `vo_script.json` al episodului și se rulează `bash run_iso.sh make_vo.py lines <dir cu L<NN><x>.mp4>` |
| `mk_reeljs.py` | scrie `reel.js` pentru fiecare episod (titlurile boom din hook pe cuvinte, `endPhone`, `endIcons`, culorile cuvintelor) |
| `epN/vo_script.json`, `epN/map/` | textul vocii și momentele pe cuvinte cu care a fost randat episodul |

Marcajul din fundal (cerut de Sabin pe 15.11.2026, ca imaginile să nu poată fi preluate de alții): în spatele scenei, pe toată durata fiecărui film,
alunecă încet rânduri estompate „TURBO DOCTOR”. Este un strat DOM `#wm` pus în `#stage` înaintea canvasului (canvasul este transparent, deci marcajul
se vede doar unde nu sunt piese; grila rămâne). CSS-ul este în `build_reel.py` (Anton 58 px, −20°, alb 4% + galben 5,2%, după ce prima probă, la 8,5% + 11,5%, i s-a părut lui Sabin prea vizibilă; tăria se schimbă cu
variabilele de mediu `WM_W` și `WM_Y`, de exemplu `WM_W=.06 WM_Y=.08 python3 build_reel.py ep1`), iar mișcarea (9 px/s, rânduri decalate) în `placeWM`
din `dir_post.js`. Fiind în animație, nu la montaj, orice schimbare a lui cere randarea din nou a cadrelor.

Pașii pentru un episod nou: text în `epN/vo_script.json` (rândul 0 = formula seriei, rândul 1 = „Vezi toate cauzele…”, ultimele 3 = încheierea comună,
care se refolosesc: `sdt2_s1_b`, `sdt2_o1_a`, `sdt2_o2_a`, `sdt2_o3_a` pe ramura `sources`), vocea, `epN.js`, `build_reel.py`, `stills.js`, randare,
apoi folderul reel-ului ca la `tools/anim_injectie` (pasul 4) și `finish.sh`.

Capcane întâlnite la 5–13: `W(rând,'cuvânt',n)` numără toate aparițiile cuvântului normalizat (fără diacritice și majuscule), deci „De” le numără și pe „de”;
obiectele care zboară și exploziile de așchii se dau pe timp (`window.FODS`, `HITC`…), nu pe piste, fiindcă pistele sunt netezite și încetinesc înainte de impact;
cadrul se potrivește pe înălțime în zona 560–1280 px (720–1280 în hook), deci un cadru înalt iese mic: până în ~230 mm înălțime; verificarea de sintaxă a lui
`epN/reel_check.js` cere `})();` adăugat la final.

Deducțiile mele din filmele 5–13 (de confirmat cu Sabin): 5 „lagărele nu mai rezistă mult”; 6 turbina ca victimă și resturile din galerie; 9 când se închid / deschid
paletele și „un drum mai lung”; 10 sfatul de la final; 11 vidul care trage ulei și turbina care se învârte mai repede la o scăpare; 13 funinginea adusă de gazele scăpate.

Ce este din surse și ce este ilustrativ: cifrele spuse (până la 300.000 rot/min, „câțiva milibari”, ralanti 1–3 minute) sunt din sursele de producători;
filtrul de ulei, geometria variabilă, ventilația carterului, filtrul de particule / catalizatorul, „coaja de portocală”, fisurile, siliconul și indicatoarele de sus
sunt desenate schematic (scena nu are aceste piese modelate, iar indicatoarele nu arată valori reale).
