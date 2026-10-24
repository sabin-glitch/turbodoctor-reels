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
- **Final:** „Rețeta Turbo Doctor” (3 sfaturi de inginer) pe un cadru încetinit, apoi cardul de final neschimbat.
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

## Structură

| Fișier | Rol |
|---|---|
| `setup.sh` | dependențe + modele offline (ASR Parakeet + Whisper, VAD; `--tts` pentru vocea Piper RO) |
| `new_reel.sh <nume> <video>` | creează `/home/claude/reels/<nume>` cu scripturile, compozitorul, `schem.js`, fonturile, sursa la 30 fps, audio și contact sheet |
| `.github/workflows/fetch-sources.yml`, `sources/queue.txt` | **clipuri de pe TikTok, fără laptopul lui Sabin:** URL-urile din `sources/queue.txt` (push pe `main`) sunt descărcate de GitHub Actions pe branch-ul `sources` (`<id>.mp4` + `<id>.json` + `manifest.json`) |
| `pipeline/caption_clean.py` | înainte de `new_reel.sh`: șterge textul vechi ars static (inpainting doar pe litere) și estompează numerele de înmatriculare (`--blur t0-t1:x0:y0:x1:y1`; estomparea crește cu mărimea plăcii; pentru o placă în mișcare, câte un `--blur` pe cadru); fără crop, fără zoom, cadrele rămân în ordinea filmată |
| `publish_media.sh <mp4> <aaaa-ll-zz_slug>` | urcă videoclipul aprobat pe branch-ul `media` și afișează linkul public pentru Metricool |
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
| `pipeline/audio.py` | vocea pe EDL + atempo, muzică discretă cu ducking, SFX sintetizate, loudnorm −14 LUFS |
| `pipeline/finish.sh` | randare completă, audio, mux, compresie sub 85 MB, copertă, `verify_sync.py` |
| `pipeline/runner.sh` | coadă serială de joburi de randare (`/home/claude/queue/todo/*.job`) |
| `pipeline/qa.py`, `qsheet.py`, `gridframe.py`, `csheet.sh`, `sheet.py`, `toks.py`, `wl.py` | control: foi de contact, grile de coordonate, cuvinte cu timpi |
| `pipeline/track_point.py` | urmărește un punct (optical flow) pentru cercuri, scanări și săgeți pe piese reale |
| `pipeline/vo_build.py` | voiceover TTS (Piper ro_RO-mihai), doar când se cere voce nouă |
| `pipeline/vo_narrator.py` | **narator peste clipul întreg** (cerut de Sabin pe 23.10.2026 la #0209, unde vocea originală nu se înțelegea): `vo_script.json` cu replici la timpi fixați pe imagine, voce Piper făcută mai gravă și calmă (Praat: formanți ×0,94, ~95 Hz), cea mai clară din 8 variante după ASR; sunetul original rămâne dedesubt (`out/v2.json`: `"narrator": true, "orig_gain": 0.32`). Apoi `retime.py`, `extract_frames.py`, ca de obicei. Se rulează după `setup.sh --tts` |
| `assets/` | fonturi Montserrat, Anton și JetBrains Mono (OFL), emoji Fluent 3D (MIT) |

## `reel.js`: piesele disponibile

Ancore pe cuvinte: `aw(fereastră, 'cuvânt', nth)` = începutul cuvântului, `ew(...)` = sfârșitul, `cw('cuvânt')` / `cwe(...)` în cold open. `S0` = începutul poveștii, `SEND` = sfârșitul ei, `TEND` = sfârșitul „Rețetei”.

- `hook`: `tag`, `l1`, `l2` (+ `l1At`, `l2At`, `l2Col`), `car`, `chips`.
- `stages`: `[[t, 'SIMPTOME'], [t, 'INVESTIGAȚIE'], [t, 'CAUZA'], [t, 'SOLUȚIA']]`.
- `comment`: card de comentariu ca sticker-ul TikTok (`name`, `text`, opțional `head`, `initial`/`col` pentru avatar, `y`, `mini` = momentul în care se micșorează în colț, `miniX/miniY/miniS`); hook-ul reel-urilor de răspuns la comentarii.
- `items[].k`: `scan`, `file` (fișa pacientului, `ecg`), `schem` (`type` din `schem.js`), `ring`, `call` (săgeată pe piesă, `track`), `pipe` (tratament), `list`, `chip`, `kin` (text cinetic), `stamp`, `cmp`, `stat`, `bars`, `gauge`, `chain`, `def` (dicționar tehnic), `art`, `ecg`, `eq`, `stk`, `tip` (Rețeta Turbo Doctor).
- `fx[].k`: `red`, `green`, `xray`, `bw`, `punch`, `glitch`, `flash` — scurte, doar pe momente-cheie.
- Scheme (`schem.js`), motor și turbo: `turboBlowby` (consum de ulei la o turbină bună din cauza motorului: segmenți, echilibrul presiunilor, gaze din carter pe retur; faze 0–7), `turboPlay`, `turboOil`, `wastegate`, `pistonSeize`, `chainSkip`, `camTiming`, `camWear`, `oilPaths`, `oilFilter`, `engineSwap`, `coolingHybrid`, `systemMap`, `route`.
- Scheme, injecție common-rail: `injectorSet` (de ce se uzează toate injectoarele împreună: aceeași motorină, temperatură, impulsuri; un singur injector reparat → factori de corecție mari; primul defect la km mulți → urmează celelalte; faze 0–10), `injectorSpray`, `railPressure`, `sensorFeedback`, `controlLoop`, `pressureLag`, `supplyChain`, `fuelFilterFlow`, `injectorReturn`, `tankCondens`, `liveData`, `scopeTrace`, `wearCurve`. Lista completă e în `return`-ul de la finalul `schem.js`.

Dacă o ancoră lipsește, compozitorul dezactivează scenele și randează doar subtitrările și finalul (`CFG_ERR` în `render.py`).

## Reguli fixe

- **Fără stabilizare.** Imaginea rămâne cum a fost filmată, chiar dacă e puțin mișcată.
- **Fiecare clip devine un reel separat**, cu hook, B-roll și CTA proprii. B-roll-ul se ia doar din același clip.
- **Hook-ul vine din fiecare clip:** textul intro-ului (hook B) descrie problemele din clipul respectiv, iar fundalul e primul lui cadru; nu se copiază de la alt reel.
- **Numerele de înmatriculare nu apar:** se acoperă cu B-roll din același clip.
- Dacă sunetul e prea slab pentru subtitrări sigure, reel-ul merge doar pe carduri, iar Sabin primește o notă.
- Subtitrări Montserrat Black, cuvântul activ cu galben; culori semantice: roșu = problemă, verde = soluție, cyan = componentă, galben = cifre.
- Elementele grafice stau în treimea de sus și nu acoperă fața prezentatorului.
- Cardul de final rămâne neschimbat: TURBO DOCTOR, „Distribuie acest video unui prieten care ar avea nevoie!”, harta cu Galați, București, Iași și Piatra Neamț, „Diagnoză gratuită”, 0739 065 065, turbodoctor.ro.
