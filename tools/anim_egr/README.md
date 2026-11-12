# Reel animat „Admisia plină de depuneri îți poate distruge turbina” (12.11.2026)

Reel din animația 3D „Depuneri EGR în admisie” (artifact, sursa în /mnt/project-files/animatii/sursa/egr-admisie/: `build.py` pune `c_*.js`
peste animația turbo), cu vocea lui Sabin din ElevenLabs (vocea „Sabin”, eleven_v4, 2 variante ≈ 2.700 de credite, aduse prin `fetch-sources`).

Diferența față de `anim_injectie` / `anim_piezo`: animația are deja propria cronologie U (0–62 s), deci nu se rescrie regia pe cuvinte.
`vo_script.json` dă pentru fiecare rând intervalul de animație `u: [u0, u1]`; începutul fiecărui rând din voce se leagă de `u0`,
iar între ancore U merge pe o curbă monotonă (PCHIP), ca viteza să nu sară. Hook-ul (rândul 0) arată loviturile din geometria variabilă
(U 45,9–49,4), apoi rândul 1 taie la U 0 (fade din negru, din animație). Rezultatul: `vo/umap.json` (copie în `map/`), `vo/uframes.json` (U pe fiecare cadru). `egr-reel.html` = animația cu modul `vo`; `rlib.js` o încarcă cu `HTML=egr-reel.html` (lângă ea: `fonts/` @fontsource și `three/package` three@0.128.0).

Randarea: animația în modul `vo` (`window.__vo(true)`: fără titlu și legendă, HUD dreapta sus, scena între 13% și 66% din înălțime),
Playwright 540×960 DPR 2, `__seek(U[cadru])`, JPEG q92 în `<reel>/frames_base/NNNNN.jpg`, 3 procese cu reluare (`vchunk.sh`).

`make_bed.py <out.wav>`: clinchet metalic la fiecare lovitură în palete și zdrobire la bucata prinsă între piston și chiulasă,
pe momentele din `uframes.json` → `audio/bed_fx.wav` (`beds` în `out/v2.json`).

`reel.js`: `pipeline/examples/reel_egr_depuneri_admisie_animatie.js` (hook `boom` „ADMISIA” → „DISTRUGE TURBINA” → „SAU MOTORUL!”, ștampile, fără bară de etape).
