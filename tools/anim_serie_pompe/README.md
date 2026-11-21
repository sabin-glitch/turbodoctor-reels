# Seria „De ce se strică pompele de înaltă presiune” (17 filme 3D)

Codul de producție al seriei (21.11.2026). Aceeași metodă ca la `tools/anim_serie_injectoare` (branch `claude/serie-injectoare`): plăci Blender Cycles randate o dată, compozitor în Python, apoi linia de reel-uri pentru titluri, subtitrări și ecranul de final.

Documentul cu scenariile: https://claude.ai/artifact/MKSWKnaxhBas19TGtj5TsN. Plăcile randate, vocea montată (FLAC) și fișierele Blender sunt în fișierele proiectului, `animatii/sursa/serie-pompe/` (`placi/`, `voce/`, `model/`).

## Ce e aici

- Modelele și plăcile: `pmodel.py` (pompa CP4 în secțiune), `paux.py`, `preg.py`, `pconn.py`, `pshelf.py` (piesele din jur, regulatorul, racordurile, raftul cu pompe), `pplate.py` + `pshots.py` (camere, stări, bucle). Se rulează cu Blender din PyPI (`bpy`): `venv_bpy/bin/python pplate.py cam:stare [--loop --lspp 16]`.
- Regia: `pser.py` (deschiderea, finalul, semnele pe carduri, schema instalației, efectele) și câte un `st_epN.py` pe episod; desenele 2D în `pdraw.py`.
- Compozitorul: `icomp.py` (cadre 1080×1920, 30 fps), `ifx.py`, `i2d.py`, `ikit.py` (etichete și carduri randate din HTML), `fxlib.py`.
- Vocea: `make_vo.py`, `vo_qc.py`, `asr2.py`, `wchk.py`; textele și timpii cuvintelor în `epN/vo_script.json` și `epN/vo/` (`cues.json`, `timeline.json`, `picks.json`).
- Montajul: `scripts/make_ep.sh N 3 [validate]` (randare, titluri și subtitrări cu `scripts/mk_reeljs_pmp.py`, sunet, copertă, text de postare, foaie de control).

## Ecranul

Insigna seriei acoperă y 196–351; subtitrările stau la y 1290–1530; subiectul și etichetele între 351 și 1280; titlul de sus la y 372, etichetele de jos la y 1150–1196. Carligul are 3 secunde fără voce; coperta e la 1,85 s (titlu pe două rânduri) sau 2,25 s (trei rânduri).
