# Turbo Doctor – reels

Fluxul complet pentru reel-urile Turbo Doctor (TikTok, Facebook, Instagram, YouTube):

1. Sabin trimite videoclipul brut în conversația cu Claude.
2. Claude îl editează: scoate watermark-ul TikTok dacă există, stabilizează imaginea, adaugă hook, B-roll, infografice compacte, subtitrări word-by-word, SFX și cardul de final.
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
| `pipeline/stab.sh` | stabilizare vidstab + upscale 1080×1920 |
| `pipeline/transcribe.py`, `transcribe2.py` | transcriere offline: VAD + Parakeet (timpi pe cuvânt) + Whisper (text) |
| `pipeline/build_timeline.py` | aliniază textul curat (`out/curated.json`), taie pauzele, cold open (`out/cold.json`) → `out/timeline.json` |
| `pipeline/extract_frames.py` | cadrele în ordinea finală (`frames_base/`) |
| `pipeline/compositor_template.html` | compozitorul HTML/CSS (Chromium): baza reutilizabilă + scenele reel-ului Volvo 2.0 Biturbo ca exemplu |
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
