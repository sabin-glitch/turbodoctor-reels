# Reel animat „Un banal schimb de filtru de motorină te poate costa peste 2.000 de euro” (14.11.2026)

Reel din animația 3D „Amorsare filtru motorină” (sursa completă în /mnt/project-files/animatii/sursa/amorsare-filtru/, cu README), cu vocea „Sabin” din ElevenLabs.
Același flux ca `tools/anim_egr/`: animația are cronologia ei (U 0–97 s), `vo_script.json` dă pentru fiecare rând intervalul `u`,
`make_umap.py` leagă începutul fiecărui rând de `u0` (PCHIP între ancore) → `vo/uframes.json` (U pe fiecare cadru).
Hook-ul (rândul 0) arată pompa CP4 în secțiune mergând cu aer (U 69,3–74,6: tachetul se rotește, rola taie cama), apoi rândul 1 taie la U 0.

- **Vocea** (cerințele lui Sabin din 14.11: calmă, directă, inginerească, nu „cinematică”; apoi „mult mai corectă, fără zgomot de fundal și pauze ciudate”):
  `eleven_v4`, vocea „Sabin”, **fiecare rând generat separat**, cu `[calm] [matter of fact]` în față (hook-ul: `[serious] [matter of fact] [conversational tone]`), câte 2 variante.
  Tag-urile v4 țin doar ~10 s de la începutul generării, de aceea nu merge tot textul într-o generare (tonul urcă înapoi spre ~200 Hz).
  Nu folosi `eleven_multilingual_v2` / `eleven_v3`: prima variantă a reelului a fost făcută cu v2 și respinsă (fâșâit constant la -53 dBFS, 20+ s de pauze în mijlocul propozițiilor).
  Fișierele vin prin `fetch-sources` (`nume=URL`), numite `…L<NN><x>.mp4` (rândul NN, varianta x), apoi
  `VO_GAPK=0.7 VO_PICK='{…}' python3 make_vo.py lines <dir>`: taie, verifică prin ASR, măsoară (`vo_qc.metrics`), alege varianta cea mai clară și cu tonul cel mai aproape de
  vocea lui reală (~168 Hz), egalizează nivelul rândurilor și atenuează blând fondul din pauzele din interiorul rândului. `vo/picks.json` ține ce s-a ales.
  `vo_qc.py <script.json> <fișier…>` măsoară orice variantă sau mixul final (fond, pauze, F0, ritm, potrivire ASR). Pronunția se verifică cu două recunoașteri
  (Parakeet + Whisper): o diferență semnalată de amândouă e reală. Așa a ieșit că „Tachetul” la început de propoziție e citit „Tașetul” → în script `{Tachetul|Taketul}`.
  Rezultat (14.11): F0 median 162 Hz, pauze doar între propoziții (0,25–0,6 s), potrivire ASR 0,98.
- **Sunetul: doar vocea** (cerut de Sabin: „să scoți zgomotul ăla enervant din hook, rămâne doar vocea pe fundal și explicația video”):
  `out/v2.json` = `{"narrator": true, "orig_gain": 0, "music": false, "sfx": false}`, fără `beds`. Zgomotul sintetizat de frecare și demaror din prima variantă (`make_bed.py`) a fost scos de tot.
- **Modul `vo` al animației**: `patch/80_hud.js` înlocuiește `src/80_hud.js` din sursa animației (`window.__vo(true)`): fără titlu, texte, bară de timp și card de final;
  testerul, bannerul „FĂRĂ AMORSARE” și panoul CP4 sunt mutate sus (y 250), legenda la y 1262, etichetele între y 560 și 1190, scena urcată ca subtitrările (de la 1290) să rămână libere.
  `window.__VOHOOK` ascunde panoul CP4 în hook (acolo stau titlurile boom).
- **Randare**: `OUT=<reel>/frames_base UF=vo/uframes.json HOOK_F=<cadrul tăieturii> ./vrender.sh` din folderul animației (lângă `out/amorsare.html`, `three/`, `fonts/`): 4 procese intercalate, 70–105 cadre/min (sare peste cadrele deja existente, deci se poate relua).
- Folderul reel-ului ca la `anim_injectie` (pașii 4 și 7); `reel.js`: `pipeline/examples/reel_amorsare_filtru_motorina_animatie.js`.

Valorile din text (circa 2.000 de bari, peste 2.000 de euro) sunt generale, nu dintr-o fișă de producător.

**Stare (16.11.2026):** reelul aprobat este cel refăcut cu pompa CP4 randată în Blender (`tools/blender_cp4/reel/`): hook-ul și partea cu pompa în secțiune au imagine nouă, iar vocea, subtitrările și titlurile sunt cele făcute aici. Sabin l-a aprobat pe 15.11 și e programat pe 16.11. Folderul de lucru al variantei de aici (voce, mix, timeline, cadrele animației) este în /mnt/project-files/animatii/sursa/amorsare-filtru/reel/work/.
