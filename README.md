# Turbo Doctor – reels

Fluxul complet pentru reel-urile Turbo Doctor (TikTok, Facebook, Instagram, YouTube):

1. Sabin trimite videoclipul brut în conversația cu Claude.
2. Claude îl editează în stilul **v2 (ingineresc + medical)**, aprobat pe 18.10.2026: hook tehnic, scheme animate, fișa pacientului, carduri, subtitrări word-by-word, SFX, muzică discretă și cardul de final. **Fără stabilizare.**
3. Sabin aprobă videoclipul și textul postării.
4. Claude publică fișierul pe branch-ul `media` din acest repo (link public), apoi programează postările în Metricool pe ora de vârf a fiecărei rețele.

> Atenție: repo-ul este **public**. Tot ce e aici, inclusiv videoclipurile de pe branch-ul `media`, poate fi văzut de oricine are linkul.

Regulile lui Sabin și preferințele lui de editare sunt ținute în skill-ul `turbodoctor-reels` și au prioritate față de acest README.

## Stilul v2 (aprobat)

- **Hook tehnic:** tag „ANALIZĂ TEHNICĂ · CAZ #nnnn”, fraza cea mai tare din clip (cold open, fidel cu ce se spune), cuvântul-cheie colorat, scanare pe piesa defectă, chip cu mașina.
- **Bara de etape** sus: SIMPTOME → INVESTIGAȚIE → CAUZA → SOLUȚIA.
- **Temă medicală:** fișa pacientului (pacient, unitate, simptome, cu EKG), ștampile (GRAV, DEFECT, BETON!, TRANSPLANT, GATA DE PREDARE), tratament „în laboratorul Turbo Doctor”, listă „înainte de externare”.
- **Schemă animată** pentru mecanismul defectului (`schem.js`), plus scanări și săgeți care urmăresc piesa reală (`track_point.py`).
- **Final:** „Rețeta Turbo Doctor” (3 sfaturi de inginer) pe un cadru încetinit, apoi cardul de final neschimbat.
- **Culoare doar ca accent scurt** pe momente-cheie (roșu = problemă, „radiografie”, alb-negru, verde = rezolvare), niciodată filtru pe tot videoclipul.
- **Ritm natural (cerut de Sabin, 18.10.2026):** implicit nu se taie pauzele și nu se accelerează (`{"cuts": false, "speed": 1.0}`); tăierea tuturor pauzelor face videoclipul prea rapid și obositor. **Doar hook-ul (cold open) e montat**, din cea mai interesantă parte a clipului.
- Muzică procedurală discretă, cu ducking sub voce; loudnorm −14 LUFS.

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

## Structură

| Fișier | Rol |
|---|---|
| `setup.sh` | dependențe + modele offline (ASR Parakeet + Whisper, VAD; `--tts` pentru vocea Piper RO) |
| `new_reel.sh <nume> <video>` | creează `/home/claude/reels/<nume>` cu scripturile, compozitorul, `schem.js`, fonturile, sursa la 30 fps, audio și contact sheet |
| `publish_media.sh <mp4> <aaaa-ll-zz_slug>` | urcă videoclipul aprobat pe branch-ul `media` și afișează linkul public pentru Metricool |
| `pipeline/wm_remove.py` | scoate watermark-ul TikTok (`--probe` găsește momentul în care se mută logo-ul) |
| `pipeline/stab.sh` | dezactivat: imaginea rămâne cum a fost filmată |
| `pipeline/transcribe.py`, `transcribe2.py` | transcriere offline: VAD + Parakeet (timpi pe cuvânt) + Whisper (text) |
| `pipeline/wsn.py` | Whisper + Parakeet pe ferestre înguste, pentru cifre și nume nesigure |
| `pipeline/build_timeline.py` | aliniază `out/curated.json`, taie pauzele (sau nu, cu `"cuts": false`), cold open → `out/timeline.json` |
| `pipeline/retime.py` | ritmul (`speed`, implicit 1,1×) și segmentul pentru „Rețeta Turbo Doctor” (`tip`) |
| `pipeline/extract_frames.py` | cadrele în ordinea finală, upscale fără stabilizare, B-roll doar din același clip (`out/broll.json`) |
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
| `assets/` | fonturi Montserrat, Anton și JetBrains Mono (OFL), emoji Fluent 3D (MIT) |

## `reel.js`: piesele disponibile

Ancore pe cuvinte: `aw(fereastră, 'cuvânt', nth)` = începutul cuvântului, `ew(...)` = sfârșitul, `cw('cuvânt')` / `cwe(...)` în cold open. `S0` = începutul poveștii, `SEND` = sfârșitul ei, `TEND` = sfârșitul „Rețetei”.

- `hook`: `tag`, `l1`, `l2` (+ `l1At`, `l2At`, `l2Col`), `car`, `chips`.
- `stages`: `[[t, 'SIMPTOME'], [t, 'INVESTIGAȚIE'], [t, 'CAUZA'], [t, 'SOLUȚIA']]`.
- `items[].k`: `scan`, `file` (fișa pacientului, `ecg`), `schem` (`type` din `schem.js`), `ring`, `call` (săgeată pe piesă, `track`), `pipe` (tratament), `list`, `chip`, `kin` (text cinetic), `stamp`, `cmp`, `stat`, `bars`, `gauge`, `chain`, `def` (dicționar tehnic), `art`, `ecg`, `eq`, `stk`, `tip` (Rețeta Turbo Doctor).
- `fx[].k`: `red`, `green`, `xray`, `bw`, `punch`, `glitch`, `flash` — scurte, doar pe momente-cheie.
- Scheme (`schem.js`): `turboPlay`, `turboOil`, `injectorSpray`, `chainSkip`, `wastegate`, `pistonSeize`, `systemMap`, `oilPaths`, `railPressure`, `engineSwap`, `camTiming`, `coolingHybrid`, `oilFilter`, `camWear`, `route`.

Dacă o ancoră lipsește, compozitorul dezactivează scenele și randează doar subtitrările și finalul (`CFG_ERR` în `render.py`).

## Reguli fixe

- **Fără stabilizare.** Imaginea rămâne cum a fost filmată, chiar dacă e puțin mișcată.
- **Fiecare clip devine un reel separat**, cu hook, B-roll și CTA proprii. B-roll-ul se ia doar din același clip.
- **Hook-ul se extrage din fiecare clip** (cel mai tare moment al lui), nu se copiază de la alt reel.
- **Numerele de înmatriculare nu apar:** se acoperă cu B-roll din același clip.
- Dacă sunetul e prea slab pentru subtitrări sigure, reel-ul merge doar pe carduri, iar Sabin primește o notă.
- Subtitrări Montserrat Black, cuvântul activ cu galben; culori semantice: roșu = problemă, verde = soluție, cyan = componentă, galben = cifre.
- Elementele grafice stau în treimea de sus și nu acoperă fața prezentatorului.
- Cardul de final rămâne neschimbat: TURBO DOCTOR, „Distribuie acest video unui prieten care ar avea nevoie!”, harta cu Galați, București, Iași și Piatra Neamț, „Diagnoză gratuită”, 0739 065 065, turbodoctor.ro.
