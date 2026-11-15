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
| `dir_pre.js`, `dir_post.js` | regia comună: momente pe cuvinte `W(rând,'cuvânt')`, piste `TR` (inclusiv `eng` = turația motorului, `spn` = turația turbinei, `gas`, `airK`), cadre de cameră `SHOTS`, etichete, eticheta fixă „Cauza X din 13” (`#badge`, y 196–290) |
| `ep1.js` … `ep4.js` | câte un episod: pistele, etichetele și camera lui (1 lipsa ungerii, 2 uleiul murdar, 3 oprirea motorului la cald, 4 uleiul care nu se mai poate scurge) |
| `build_reel.py <epN>` | scrie `epN/reel.html` din `index_src.html` + `fx.js` + `dir_pre.js` + `epN.js` + `dir_post.js` + `epN/vo/cues.json` (lângă: `fonts/` și `three.min.js`) |
| `stills.js <epN> <prefix> t1,t2,… [coloane]` | cadre de probă + foaie de contact |
| `render_frames.js <epN> <dir> <primul> <ultimul> [pas]`, `render_all.sh` | randarea, 4 procese intercalate pe episod, cu reluare (≈ 0,4 s/cadru în total) |
| `make_vo.py`, `vo_qc.py`, `asr2.py`, `run_iso.sh` | vocea rând cu rând (ca la blow-off): se copiază lângă `vo_script.json` al episodului și se rulează `bash run_iso.sh make_vo.py lines <dir cu L<NN><x>.mp4>` |
| `mk_reeljs.py` | scrie `reel.js` pentru fiecare episod (titlurile boom din hook pe cuvinte, `endPhone`, `endIcons`, culorile cuvintelor) |
| `epN/vo_script.json`, `epN/map/` | textul vocii și momentele pe cuvinte cu care a fost randat episodul |

Pașii pentru un episod nou: text în `epN/vo_script.json` (rândul 0 = formula seriei, rândul 1 = „Vezi toate cauzele…”, ultimele 3 = încheierea comună,
care se refolosesc: `sdt2_s1_b`, `sdt2_o1_a`, `sdt2_o2_a`, `sdt2_o3_a` pe ramura `sources`), vocea, `epN.js`, `build_reel.py`, `stills.js`, randare,
apoi folderul reel-ului ca la `tools/anim_injectie` (pasul 4) și `finish.sh`.

Ce este din surse și ce este ilustrativ: cifrele spuse (până la 300.000 rot/min, „câțiva milibari”, ralanti 1–3 minute) sunt din sursele de producători;
filtrul de ulei, geometria variabilă și ventilația carterului sunt desenate schematic (scena nu are aceste piese modelate).
