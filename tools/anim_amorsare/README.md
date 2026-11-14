# Reel animat „Un banal schimb de filtru de motorină te poate costa peste 2.000 de euro” (14.11.2026)

Reel din animația 3D „Amorsare filtru motorină” (sursa completă în /mnt/project-files/animatii/sursa/amorsare-filtru/, cu README), cu vocea „Sabin” din ElevenLabs.
Același flux ca `tools/anim_egr/`: animația are cronologia ei (U 0–97 s), `vo_script.json` dă pentru fiecare rând intervalul `u`,
`make_umap.py` leagă începutul fiecărui rând de `u0` (PCHIP între ancore) → `vo/uframes.json` (U pe fiecare cadru).
Hook-ul (rândul 0) arată pompa CP4 în secțiune mergând cu aer (U 69,3–74,6: tachetul se rotește, rola taie cama), apoi rândul 1 taie la U 0.

- **Vocea** (cerința lui Sabin din 14.11: calmă, directă, inginerească, nu „cinematică”): `eleven_multilingual_v2`, vocea „Sabin”, tot textul într-o generare.
  `eleven_v4`, cu sau fără tag-uri `[calm] [matter of fact]`, a ieșit cu intonație mai largă (măsurat: abaterea tonului 4,6–4,9 semitonuri față de 3,7 la varianta aleasă).
  Încheierea (rândurile 18–19) a fost generată separat și lipită după varianta aleasă, adusă la același nivel (`comb1/2.wav`), apoi
  `VO_PICK='{"19":0}' VO_GAPK=0.7 python3 make_vo.py take comb1.wav comb2.wav`. Fișierele audio vin prin `fetch-sources` (`nume=URL`).
- **Modul `vo` al animației**: `patch/80_hud.js` înlocuiește `src/80_hud.js` din sursa animației (`window.__vo(true)`): fără titlu, texte, bară de timp și card de final;
  testerul, bannerul „FĂRĂ AMORSARE” și panoul CP4 sunt mutate sus (y 250), legenda la y 1262, etichetele între y 560 și 1190, scena urcată ca subtitrările (de la 1290) să rămână libere.
  `window.__VOHOOK` ascunde panoul CP4 în hook (acolo stau titlurile boom).
- **Randare**: `OUT=<reel>/frames_base UF=vo/uframes.json HOOK_F=<cadrul tăieturii> ./vrender.sh` din folderul animației (lângă `out/amorsare.html`, `three/`, `fonts/`): 4 procese intercalate, ~105 cadre/min.
- `make_bed.py <out.wav>`: demarorul și frecarea metal pe metal din pompă, pe momentele din `uframes.json` (`beds` în `out/v2.json`).
- Folderul reel-ului ca la `anim_injectie` (pașii 4 și 7); `reel.js`: `pipeline/examples/reel_amorsare_filtru_motorina_animatie.js`.

Valorile din text (circa 2.000 de bari, peste 2.000 de euro) sunt generale, nu dintr-o fișă de producător.
