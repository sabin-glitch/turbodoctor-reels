# Turbo Doctor – reels

Fluxul complet pentru reel-urile Turbo Doctor (TikTok, Facebook, Instagram, YouTube):

1. Sabin trimite videoclipul brut în conversația cu Claude.
2. Claude îl editează în stilul **v2 (ingineresc + medical)**, aprobat pe 18.10.2026: hook tehnic, scheme animate, fișa pacientului, carduri, subtitrări word-by-word, SFX, muzică discretă și cardul de final. **Fără stabilizare.**
3. Sabin aprobă videoclipul și textul postării.
4. Claude publică fișierul pe branch-ul `media` din acest repo (link public), apoi programează postările în Metricool pe ora de vârf a fiecărei rețele.

> Atenție: repo-ul este **public**. Tot ce e aici, inclusiv videoclipurile de pe branch-ul `media`, poate fi văzut de oricine are linkul.

Regulile lui Sabin și preferințele lui de editare sunt ținute în skill-ul `turbodoctor-reels` și au prioritate față de acest README.

## Stilul v2 (aprobat)

- **Hook B (ales de Sabin pe 20.10.2026, pe toate reel-urile):** intro sintetic de ~8–10 s înaintea clipului: fundalul e primul cadru al aceluiași clip, estompat; 3 carduri cu problemele pe care le simte clientul se unesc într-o singură cauză, voce generată (Piper RO) cu subtitrări și „Ascultă mai departe pe Turbo Doctor!”, apoi clipul cu hook-ul lui vizual. Detalii în secțiunea „Hook B”.
- **Hook tehnic:** tag „ANALIZĂ TEHNICĂ · CAZ #nnnn”, fraza cea mai tare din clip (cold open, fidel cu ce se spune), cuvântul-cheie colorat, scanare pe piesa defectă, chip cu mașina.
- **Bara de etape** sus: SIMPTOME → INVESTIGAȚIE → CAUZA → SOLUȚIA.
- **Temă medicală:** fișa pacientului (pacient, unitate, simptome, cu EKG), ștampile (GRAV, DEFECT, BETON!, TRANSPLANT, GATA DE PREDARE), tratament „în laboratorul Turbo Doctor”, listă „înainte de externare”.
- **Schemă animată** pentru mecanismul defectului (`schem.js`), plus scanări și săgeți care urmăresc piesa reală (`track_point.py`).
- **Final:** „Rețeta Turbo Doctor” (3 sfaturi de inginer) pe un cadru încetinit, apoi cardul de final fără CTA (din 25.10.2026).
- **Culoare doar ca accent scurt** pe momente-cheie (roșu = problemă, „radiografie”, alb-negru, verde = rezolvare), niciodată filtru pe tot videoclipul.
- **Ritm natural (cerut de Sabin, 18.10.2026):** implicit nu se taie pauzele și nu se accelerează (`{"cuts": false, "speed": 1.0}`); tăierea tuturor pauzelor face videoclipul prea rapid și obositor. **Doar hook-ul (cold open) e montat**, din cea mai interesantă parte a clipului.
- Muzică procedurală discretă, cu ducking sub voce, la jumătate față de nivelul inițial (`music_gain` implicit 0,5, cerut de Sabin pe 18.10.2026); loudnorm −14 LUFS.

## Pașii pentru un reel

```bash
bash /home/claude/turbodoctor-reels/setup.sh                 # o dată pe sesiune, ~5 min (în background)
bash /home/claude/turbodoctor-reels/new_reel.sh <slug> <video>   # -> /home/claude/reels/<slug>
cd /home/claude/reels/<slug>
python3 wm_remove.py --probe && python3 wm_remove.py <SWITCH>   # doar dacă are watermark TikTok
python3 transcribe.py && python3 transcribe2.py               # -> out/wins.json, out/tr2.log
# scrii out/curated.json (un string pe fereastră, fidel) și out/cold.json (cold open)
# opțional out/v2.json: {"tip": {"dur": 3.4, "src": <s>, "speed": 0.7}, "music": true}  (implicit cuts false, speed 1.0 = ritm natural)
python3 build_timeline.py && python3 retime.py && python3 extract_frames.py
# scrii reel.js (pornește de la pipeline/examples/), opțional out/broll.json și out/track_*.json
python3 render.py --prep --test 0.4,1.5,6,12        # previzualizări în preview/
bash finish.sh <slug> <Nume_Fisier>                  # randare completă + audio + mux + copertă + verificare sincron
python3 qsheet.py /home/claude/deliver/TurboDoctor_<Nume>.mp4 /tmp/qs.jpg 12   # control rapid
```

## Hook B: intro sintetic

1. `out/intro_script.json`: `{"speed": 1.15, "tail": .5, "bg_src": <sursa primului cadru>, "takes": 8, "phrases": [{"text": "Pornește greu,", "gap": .08}, …, {"text": "Ascultă mai departe pe Turbo Doctor!", "wav": "cta_turbo_doctor.wav"}]}` (clipul verificat din `assets/`, copiat în `out/`). Trei fraze scurte cu problema clientului + o frază-răspuns; `say` = forma rostită când diferă de subtitrare (cifre).
2. În `reel.js`: `intro: { type: 'board', tag, ctaPh, mergeAt, causeAt, causeTxt, cards: [[emoji, titlu, subtitlu, t0?, 'x'|'q'|'none']] }` și `tags: { '-1': { cuvânt: 'r'|'y'|'c'|'g' } }`.
3. `python3 intro_vo.py` (cea mai bună din 8 variante pe frază, verificată cu ASR; linia `whole intro heard` trebuie să sune ca textul), apoi `build_timeline.py`, `retime.py`, `extract_frames.py`. Cheile din `out/track_*.json` se mută cu numărul de cadre ale intro-ului.
4. Timpii din `reel.js` se scriu cu ancore sau `S0 + n`: clipul începe după intro.
5. Pe reel-uri deja făcute: `tools/hook_b/` (scenariile în `hook_specs.py`, apoi `hook_all.sh <slug…>` și `render_all.sh <slug…>`, care randează și verifică vocea intro-ului cu ASR, LUFS și o foaie de cadre).
6. Vocea TTS pierde consoanele de la începutul frazei (T, C, V, „Și nu”, „Știi”): frazele încep cu vocală, „Iar”, „Însă”, „dar”.

## Hook cu cadre AI (promo injectoare, 28.10.2026)

Când Sabin cere în hook imagini care nu există în clipurile lui (ex. „un motor care pornește greu și după aia un motor care trepidează”):

1. Generez cadrele cu vidIQ (`vidiq_generate_video`, `gemini-omni-flash`, 9:16, 720p, **cu sunet**; ~20 credite/s) și îi spun lui Sabin costul. Promptul cere „vertical smartphone footage, no music, no voices, no text”.
2. Le aduc prin `fetch-sources`: linii `nume=URL` în `sources/queue.txt`, push pe `main`, apoi `git show origin/sources:<nume>.mp4` (după aceea șterg ref-ul `origin/sources` și rulez `git gc`: branch-ul are sute de MB).
3. `tools/hook_ai/build_hook_promo_injectoare.py` construiește sursa: cadrele AI peste prima frază (vocea lui rămâne întreagă, întârziată cu `PRE`), apoi clipurile lui de la fraza următoare. Demarorul e pus în buclă, tăiat pe golurile dintre compresii, până motorul „prinde” imediat după cuvântul-cheie („greu”); imaginea merge înainte-înapoi pe partea statică, ca momentul în care prinde să cadă pe sunet. Motorul care trepidează primește o vibrație a cadrului sincronizată cu sunetul lui (anvelopa 20–150 Hz). Sunetul real al cadrelor AI merge separat în `audio/hook_bed.wav`.
4. `out/v2.json`: `"beds": [{"wav": "audio/hook_bed.wav", "t": 0, "gain": 1.0, "duck": 0.5}]` (sunetul nu trece prin lanțul de curățare a vocii și coboară sub voce) și `"music_in": <s>` (muzica intră abia când apare el).
5. Transcrierea făcută pe clipurile lui se mută cu `PRE` (`out/transcript.json`, `out/transcript_ctx.json`, `out/wins.json`), fără o nouă transcriere.
6. Titlurile hook-ului: `boom` pe cuvintele-cheie, sus, peste zona fără acțiune (parbrizul înghețat, capota); subtitrările ascunse cât durează hook-ul (`hideCap`). Exemplu: `pipeline/examples/reel_promo_injectoare_hook_ai.js`.
7. La postare: `isAiGenerated: true` pe Instagram și `isAigc: true` pe TikTok.

## Structură

| Fișier | Rol |
|---|---|
| `setup.sh` | dependențe + modele offline (ASR Parakeet + Whisper, VAD; `--tts` pentru vocea Piper RO; `--sep` pentru modelul UVR de separare a vocii) |
| `pipeline/sdr.sh <in> <out.mp4>` | **clipurile de pe iPhone sunt HDR (HLG/Dolby Vision): le normalizez mereu cu `sdr.sh` (1080×1920, 30 fps, tone mapping la SDR BT.709) înainte să le lipesc.** Fără tone mapping, fața iese palidă și „arsă”, ca un filtru de lumină (respins de Sabin pe 24.10.2026). `new_reel.sh` face același tone mapping dacă primește direct un clip HDR |
| `new_reel.sh <nume> <video>` | creează `/home/claude/reels/<nume>` cu scripturile, compozitorul, `schem.js`, fonturile, sursa la 30 fps, audio și contact sheet |
| `.github/workflows/fetch-sources.yml`, `sources/queue.txt` | **clipuri de pe TikTok, fără laptopul lui Sabin:** URL-urile din `sources/queue.txt` (push pe `main`) sunt descărcate de GitHub Actions pe branch-ul `sources` (`<id>.mp4` + `<id>.json` + `manifest.json`) |
| `pipeline/caption_clean.py` | înainte de `new_reel.sh`: șterge textul vechi ars static (inpainting doar pe litere) și estompează numerele de înmatriculare (`--blur t0-t1:x0:y0:x1:y1`; estomparea crește cu mărimea plăcii; pentru o placă în mișcare, câte un `--blur` pe cadru); fără crop, fără zoom, cadrele rămân în ordinea filmată |
| `publish_media.sh <mp4> <aaaa-ll-zz_slug>` | urcă videoclipul aprobat pe branch-ul `media` și afișează linkul public pentru Metricool, legat de commit (`raw.githubusercontent.com/<owner>/<repo>/<sha>/<fișier>`), ca să meargă și dacă alt chat face push pe `media` între timp |
| `pipeline/wm_remove.py` | scoate watermark-ul TikTok (`--probe` găsește momentul în care se mută logo-ul) |
| `pipeline/stab.sh` | dezactivat: imaginea rămâne cum a fost filmată |
| `pipeline/transcribe.py`, `transcribe2.py` | transcriere offline: VAD + Parakeet (timpi pe cuvânt) + Whisper (text) |
| `pipeline/wsn.py` | Whisper + Parakeet pe ferestre înguste, pentru cifre și nume nesigure |
| `pipeline/build_timeline.py` | aliniază `out/curated.json`, păstrează pauzele (implicit; `"cuts": true` le taie), cold open → `out/timeline.json` |
| `pipeline/retime.py` | ritmul (`speed`, implicit 1,0 = natural) și segmentul pentru „Rețeta Turbo Doctor” (`tip`) |
| `pipeline/extract_frames.py` | cadrele în ordinea finală, upscale fără stabilizare, B-roll doar din același clip (`out/broll.json`) |
| `pipeline/intro.js`, `pipeline/intro_vo.py` | hook B: grafica intro-ului (carduri, eticheta-cauză, CTA) și vocea lui (Piper RO, cea mai bună variantă pe frază după ASR) |
| `pipeline/vlog_vertical.py` | vlog orizontal 16:9 → 1080×1920: cadrul întreg pe lățime, fundal din același cadru estompat; etichetele arse se scot cu inpainting sau dintr-un cadru curat al aceleiași filmări (`t0-t1:x0,y0,x1,y1@tref`) |
| `pipeline/compositor_template.html` | compozitorul v2 (Chromium): hook, bara de etape, toate cardurile și efectele |
| `pipeline/schem.js` | schemele animate ale defectelor |
| `pipeline/examples/*.js` | configurații reale de scene (`reel.js`) din reel-urile aprobate |
| `pipeline/render.py` | `--prep`, `--test t1,t2` pentru previzualizări, `--full` pentru randare (~4–5 fps) |
| `pipeline/audio.py` | vocea pe EDL + atempo, muzică discretă cu ducking, SFX sintetizate, sunet real de hook (`beds`, cu ducking sub voce), loudnorm −14 LUFS |
| `pipeline/finish.sh` | randare completă, audio, mux, compresie sub 85 MB, copertă, `verify_sync.py` |
| `pipeline/runner.sh` | coadă serială de joburi de randare (`/home/claude/queue/todo/*.job`) |
| `pipeline/qa.py`, `qsheet.py`, `gridframe.py`, `csheet.sh`, `sheet.py`, `toks.py`, `wl.py` | control: foi de contact, grile de coordonate, cuvinte cu timpi |
| `pipeline/track_point.py` | urmărește un punct (optical flow) pentru cercuri, scanări și săgeți pe piese reale |
| `tools/hook_ai/` | hook din cadre AI cu sunet (vezi „Hook cu cadre AI”) |
| `pipeline/vo_build.py` | voiceover TTS (Piper ro_RO-mihai), doar când se cere voce nouă |
| `pipeline/sep_voice.py <in.wav 44,1 kHz> <voce.wav> [<rest.wav>]` | separă vocea de muzica și SFX-urile unui reel deja editat (UVR MDX-Net prin sherpa-onnx; după `setup.sh --sep`) |
| `tools/compilatie/` | promo din istoric (29.10.2026): `build_promo_motoare.py` construiește sursa din secvențe (`nume, fișier, t0, t1, 'sep'\|'orig', text, {mute_until, fade_in}`), `setup_reel_promo_motoare.sh` face folderul reel-ului și transcrierea pe câte o fereastră pe secvență |
| `pipeline/vo_narrator.py` | **narator peste clipul întreg** (cerut de Sabin pe 23.10.2026 la #0209, unde vocea originală nu se înțelegea): `vo_script.json` cu replici la timpi fixați pe imagine, voce Piper făcută mai gravă și calmă (Praat: formanți ×0,94, ~95 Hz), cea mai clară din 8 variante după ASR; sunetul original rămâne dedesubt (`out/v2.json`: `"narrator": true, "orig_gain": 0.32`). Apoi `retime.py`, `extract_frames.py`, ca de obicei. Se rulează după `setup.sh --tts` |
| `assets/` | fonturi Montserrat, Anton și JetBrains Mono (OFL), emoji Fluent 3D (MIT) |

## `reel.js`: piesele disponibile

Ancore pe cuvinte: `aw(fereastră, 'cuvânt', nth)` = începutul cuvântului, `ew(...)` = sfârșitul, `cw('cuvânt')` / `cwe(...)` în cold open. `S0` = începutul poveștii, `SEND` = sfârșitul ei, `TEND` = sfârșitul „Rețetei”.

- `hook`: `tag`, `l1`, `l2` (+ `l1At`, `l2At`, `l2Col`), `car`, `chips`.
- `stages`: `[[t, 'SIMPTOME'], [t, 'INVESTIGAȚIE'], [t, 'CAUZA'], [t, 'SOLUȚIA']]`.
- `comment`: card de comentariu ca sticker-ul TikTok (`name`, `text`, opțional `head`, `initial`/`col` pentru avatar, `y`, `mini` = momentul în care se micșorează în colț, `miniX/miniY/miniS`); hook-ul reel-urilor de răspuns la comentarii.
- `items[].k`: `scan`, `file` (fișa pacientului, `ecg`), `schem` (`type` din `schem.js`), `ring`, `call` (săgeată pe piesă, `track`), `pipe` (tratament), `list`, `chip`, `kin` (text cinetic), `stamp`, `cmp`, `stat`, `bars`, `gauge`, `chain`, `def` (dicționar tehnic), `art`, `ecg`, `eq`, `stk`, `tip` (Rețeta Turbo Doctor), `boom` (titlu de hook care „bubuie”: intră din blur de la scara `from` ≈ 3,6, cu RGB split `ca`, tremur `sh`, strălucire `glow`; sunet: riser scurt + `boom` + crack; `{k:'boom', t, dur, txt, y, size, col, riser?, bg?}`, aprobat pe 26.10.2026 la reel-ul Euro 7).
- `fx[].k`: `red`, `green`, `xray`, `bw`, `punch` (`a` zoom, `sh` tremur), `glitch`, `flash` (`a`), `shock` (undă de șoc: inele care pleacă din punctul de impact, `{k:'shock', t, x, y, r, n, col}`) — scurte, doar pe momente-cheie. Hook-ul „boom” de la Euro 7: `flash` .75 cu 0,11 s înainte de impact + `punch` .16/34 + `glitch` + `shock` + `bursts`.
- SFX sintetizate noi (`audio.py`): `boom` (bubuitură cinematică: sub saturat + thud + rumble, se aude și pe difuzoarele de telefon) și `rise` (riser scurt de 0,62 s care se termină pe impact).
- **Compilații din reel-uri deja publicate** (promo reparații motoare, 29.10.2026): clipurile brute din chat-urile vechi nu se păstrează, așa că secvențele se iau din reel-urile publicate (originalul din Metricool, `static.metricool.com`, adus cu `fetch-sources` ca `nume=URL`), fiecare cu imaginea și vocea lui. Vocea se separă de muzica și SFX-urile vechi cu UVR MDX-Net (`sherpa_onnx.OfflineSourceSeparation`, modelul `UVR-MDX-NET-Voc_FT.onnx` din release-ul `source-separation-models` al sherpa-onnx), apoi fiecare secvență se aduce la aceeași tărie (−20 LUFS). Subtitrările și grafica lor arsă rămân: în `reel.js` intervalele lor intră în `hideCap` și în `bgFix` (fundalul nu se mărește și nu primește vigneta a doua), iar bara lor de etape se acoperă cu `band`. Fiecare caz începe cu `chap` peste `fx` `veil`, care ascunde și finalul hook-ului vechi. Exemplu: `pipeline/examples/reel_promo_reparatii_motoare_compilatie.js`.
- `band` (29.10.2026): bară opacă, plină din primul cadru, peste bara de etape arsă a unui reel deja editat; arată cazul curent (`{k:'band', t0, t1, y: 222, w: 980, h: 76, kicker: 'CAZ REAL', ph: [[t, text, sub]]}`), textul se schimbă pe faze.
- `chap` (29.10.2026): card de capitol (`{k:'chap', t0, t1, kicker, title, sub, y}`), cu `fx` `veil` (`{k:'veil', t0, t1, out}` = fundal estompat și întunecat, plin din primul cadru).
- `lbl` (29.10.2026): etichetă opacă pe 2 rânduri (`{k:'lbl', t0, t1, y: 333, w: 660, h: 168, ph: [[t, kicker, text, 'g'|'c'|'y'|'r']]}`), plină din primul cadru, peste locul unui titlu vechi ars scos cu `caption_clean.py` (inpainting-ul lasă urme pe motoare și pe păr); rândul mare urmează ce spune (pașii, rezultatul), textul lung se micșorează singur.
- `bgFix: [[t0, t1], ...]` în `reel.js`: fundalul rămâne fix (fără zoom, fără vigneta compozitorului) pe secvențele care au deja grafica lor arsă.
- Scheme (`schem.js`), motor și turbo: `turboBlowby` (consum de ulei la o turbină bună din cauza motorului: segmenți, echilibrul presiunilor, gaze din carter pe retur; faze 0–7), `turboPlay`, `turboOil`, `wastegate`, `pistonSeize`, `chainSkip`, `camTiming`, `camWear`, `oilPaths`, `oilFilter`, `engineSwap`, `coolingHybrid`, `systemMap`, `route`.
- Scheme, costuri: `valueVsLabor` (valoarea mașinii scade, manopera e la prețul de azi → reparația nu mai merită; km pe an atunci vs. acum).
- Scheme, injecție common-rail: `injectorSet` (de ce se uzează toate injectoarele împreună: aceeași motorină, temperatură, impulsuri; un singur injector reparat → factori de corecție mari; primul defect la km mulți → urmează celelalte; faze 0–10), `injectorSpray`, `railPressure`, `sensorFeedback`, `controlLoop`, `pressureLag`, `supplyChain`, `fuelFilterFlow`, `injectorReturn`, `tankCondens`, `liveData`, `scopeTrace`, `wearCurve`.
- Scheme, DPF și admisie: `dpfFlow` (funingine → regenerare → cenușă), `regenModes` (pasivă / activă / forțată), `postInject` (post-injecție care încinge DPF-ul), `egrLoop` (recircularea gazelor). Lista completă e în `return`-ul de la finalul `schem.js`.
- Scheme, diagnoză: `causeEffect` (hartă cauză › efect: simptomul sus, ex. „eroare pe turbină”, cauzele posibile jos cu „?”; faza 1 = fasciculul de diagnoză le verifică pe rând, faza 2 = cauza găsită, totul verde; `P = {sym: [emoji, eticheta], causes: [[emoji, eticheta], …] (2–4), sweep: s}`), aprobată pe 30.10.2026 la reel-ul „De ce e gratuită diagnoza?”, cu hook-ul `boom` în trei trepte (`pipeline/examples/reel_diag_gratuita_de_ce.js`).
- Scheme, Euro 7: `euro7Line` (traseul gazelor turbo → încălzitor electric → AdBlue 1 + NOx → SCR 1 → DOC → DPF → AdBlue 2 → SCR 2 → tobă, cu senzori NOx / temperatură / O2; piesa curentă galbenă, faze 0–9) și `euro7Kit` (inventarul în 8 plăci care se umplu pe ce enumeră, `P.items = [[t, nr, eticheta, sub, icon, culoare]]`, `P.all` = momentul în care pulsează toate).
- **Clipuri cu cameră duală (PiP cu fața sus-dreapta):** fără bara de etape; chip-urile la y ≈ 590, sub PiP. Schemele și cardurile mari stau SUS (`top` ≈ 230), chiar dacă acoperă fața din PiP, ca mijlocul ecranului, unde e piesa arătată, să rămână liber (cerut de Sabin pe 26.10.2026). Exemplu: `pipeline/examples/reel_euro7_traseu_evacuare_pip.js`.

Cold open (hook din clip, aprobat 2026-10-24): `out/cold.json` = `{"audio":[[a,b]],"video_src":a,"extra":0.25}`, o singură bucată continuă de 4–8 s; peste ea `l1`/`l2` legate de cuvântul-cheie, un `kin` mare la y 1620 (mărime ≤ 1600/nr. caractere), `punch` + `glitch` + accent scurt `red`/`green`. Fără voce AI.

Dacă o ancoră lipsește, compozitorul dezactivează scenele și randează doar subtitrările și finalul (`CFG_ERR` în `render.py`).

## Reguli fixe

- **Fără stabilizare.** Imaginea rămâne cum a fost filmată, chiar dacă e puțin mișcată.
- **Fiecare clip devine un reel separat**, cu hook, B-roll și CTA proprii. B-roll-ul se ia doar din același clip.
- **Hook-ul vine din fiecare clip:** textul intro-ului (hook B) descrie problemele din clipul respectiv, iar fundalul e primul lui cadru; nu se copiază de la alt reel.
- **Numerele de înmatriculare nu apar:** se acoperă cu B-roll din același clip.
- Dacă sunetul e prea slab pentru subtitrări sigure, reel-ul merge doar pe carduri, iar Sabin primește o notă.
- Subtitrări Montserrat Black, cuvântul activ cu galben; culori semantice: roșu = problemă, verde = soluție, cyan = componentă, galben = cifre.
- Elementele grafice stau în treimea de sus și nu acoperă fața prezentatorului.
- Cardul de final (din 25.10.2026, fără CTA): TURBO DOCTOR, harta cu Galați, București, Iași și Piatra Neamț și „Diagnoză gratuită”. Fără „Distribuie acest video…”, fără 0739 065 065 și fără turbodoctor.ro — nici pe video, nici în textul postării (clipurile care arată a reclamă primesc mai puțin reach pe TikTok). Pe TikTok, postările nu se mai bifează ca „Commercial content”.
