# Turbo Doctor – reels

Fluxul complet pentru reel-urile Turbo Doctor (TikTok, Facebook, Instagram, YouTube):

1. Sabin trimite videoclipul brut în conversația cu Claude.
2. Claude îl editează: scoate watermark-ul TikTok dacă există, adaugă hook, B-roll (doar din același clip), elementele medicale (fișa pacientului, EKG, ștampile), subtitrări word-by-word, SFX și cardul de final. **Fără stabilizare.**
3. Sabin aprobă videoclipul și textul postării.
4. Claude publică fișierul pe branch-ul `media` din acest repo (link public), apoi programează postările în Metricool pe ora de vârf a fiecărei rețele.

> Atenție: repo-ul este **public**. Tot ce e aici, inclusiv videoclipurile de pe branch-ul `media`, poate fi văzut de oricine are linkul.

## Structură

| Fișier | Rol |
|---|---|
| `setup.sh` | instalează dependențele și descarcă modelele offline (ASR Parakeet + Whisper, VAD; `--tts` pentru vocea Piper RO) |
| `new_reel.sh <nume> <video>` | creează `/home/claude/reels/<nume>` cu scripturile, template-ul, sursa la 30 fps, audio și contact sheet |
| `publish_media.sh <mp4> <aaaa-ll-zz_slug>` | urcă videoclipul aprobat pe branch-ul `media` și afișează linkul public pentru Metricool |
| `pipeline/wm_remove.py` | scoate watermark-ul TikTok (`--probe` găsește momentul în care se mută logo-ul) |
| `pipeline/stab.sh` | dezactivat: imaginea rămâne cum a fost filmată (upscale-ul se face în `extract_frames.py`) |
| `pipeline/transcribe.py`, `transcribe2.py` | transcriere offline: VAD + Parakeet (timpi pe cuvânt) + Whisper (text) |
| `pipeline/build_timeline.py` | aliniază textul curat (`out/curated.json`), taie pauzele (VAD + energie, fără să taie cuvinte), cold open (`out/cold.json`) → `out/timeline.json` |
| `pipeline/extract_frames.py` | cadrele în ordinea finală (`frames_base/`), upscale fără stabilizare, plus B-roll din același clip (`out/broll.json`) |
| `pipeline/compositor_template.html` | compozitorul HTML/CSS (Chromium), cu tema medicală: hook, fișa pacientului, listă de tratament, monitor EKG, carduri cu ilustrații, comparații, contor, ștampile, cercuri urmărite, efecte de culoare doar pe momente-cheie |
| `reel.js` (per reel, exemplu în `pipeline/reel_example.js`) | configurația scenelor: ancore pe cuvinte, carduri, efecte, capitole Consultație → Diagnostic → Tratament → Externare |
| `pipeline/render.py` | `--test t1,t2` pentru previzualizări, `--full` pentru randare (~5 fps) |
| `pipeline/audio.py` | vocea pe EDL, curățată și egalizată, plus SFX sintetizate; loudnorm -14 LUFS |
| `pipeline/verify_sync.py` | re-transcrie mixul final și compară cu subtitrările |
| `pipeline/track_point.py` | urmărește un punct (optical flow) pentru cercuri pe piese reale |
| `pipeline/vo_build.py` | voiceover TTS (Piper ro_RO-mihai) din `vo_script.json`, când clientul cere voce nouă |
| `assets/` | fonturi Montserrat și Anton (OFL), emoji Fluent 3D (MIT) |

## Reguli de stil

- Elementele grafice sunt compacte, în treimea de sus, și nu acoperă imaginea. La cadrele cu prezentatorul stau deasupra capului, nu peste față.
- Subtitrări Montserrat Black, câte 3 cuvinte, cuvântul activ cu galben. Culori semantice: roșu = problemă, verde = soluție, cyan = componentă, galben = cifre. Poziție: `top:1290px`.
- Hook puternic în primele ~3 s. Poate fi un cold open cu cea mai tare frază din video, fidel cu ce se spune.
- Se păstrează vocea originală, cu excepția cazului în care se cere voiceover.
- Cardul de final: TURBO DOCTOR, „Distribuie acest video unui prieten care ar avea nevoie!”, harta cu Galați, București, Iași și Piatra Neamț, „Diagnoză gratuită”, 0739 065 065, turbodoctor.ro.

## Reguli noi (octombrie 2026)

- **Fără stabilizare.** Imaginea rămâne cum a fost filmată, chiar dacă e puțin mișcată.
- **Fără filtru de culoare permanent.** Culoarea se folosește doar ca accent scurt: roșu pe problemă (max ~2,4 s), „radiografie” albastră ~1 s la constatare, alb-negru scurt la „nu mai pornește / colmatat”, verde la rezolvare.
- **Temă medicală Turbo Doctor:** fișa pacientului (pacient, unitate, internat cu, diagnostic), monitor EKG pentru simptome, ștampile (GRAV, DEFECT, GATA DE PREDARE), capitole Consultație → Diagnostic → Tratament → Externare.
- **Fiecare clip devine un reel separat.** B-roll-ul se ia doar din același clip; nu se amestecă secvențe între reel-uri.
- **Numerele de înmatriculare nu apar:** se acoperă cu B-roll din același clip.
- Dacă sunetul e prea slab pentru subtitrări sigure, reel-ul merge doar pe carduri (fără subtitrări automate), iar Sabin primește o notă.
