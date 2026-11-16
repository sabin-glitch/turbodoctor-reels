# Seria „De ce se strică injectoarele” (13 episoade)

Cerută de Sabin pe 15.11.2026. Cauzele, sursele și lista de episoade sunt în documentul seriei din proiect; notele de cercetare (engleză, cu citate și linkuri) și plăcile randate (`pl.tar.xz`) sunt în folderul `animatii/sursa/serie-injectoare/` al proiectului.

Reel-urile: `/mnt/project-files/animatii/TurboDoctor_Reel_Serie_Injectoare_NN_<Nume>.mp4`, cu `_coperta.jpg` și `_text_postare.txt`. Pe 16.11.2026, episoadele 1 și 2 au vocea generată a lui Sabin; 3–13 sunt previzualizări (sufixul `_PREVIZUALIZARE`): vocea se aude doar la formula fixă de început și de final, refolosită din episodul 1, iar restul are subtitrări pe momente estimate. Nimic nu e publicat sau programat fără aprobarea lui Sabin.

## Cum e făcut

1. **Modelele** (Blender, `bpy` de pe PyPI în `/home/claude/w/venv_bpy`): injectorul electromagnetic generic de tip Bosch, modelat întreg și tăiat în secțiune (o pană de 120° spre cameră), filtrul cu separator de apă (`model/model.py`, `model/filter.py`, materialele în `model/imats.py`), plus scena micro cu jocul de 3 µm dintre ac și ghidaj și firul de păr (`micro.py`), rezervorul (`tank.py`), scaunul bilei cu adâncituri și canal (`seatdmg.py`) și calamina din puțul injectorului (`xsoot.py`).
2. **Plăcile**: fiecare cadru fix (cameră + stare) se randează o singură dată în Cycles, pe procesor: imaginea, adâncimea (`.z.npy`) și camera (`.json`). Camerele și stările sunt în `ishots.py`; randarea: `venv_bpy/bin/python iplate.py cam:stare … [--preview] [--force]` (fără `--force` sare peste plăcile existente). Plăcile gata sunt în `pl.tar.xz`, în folderul seriei din proiect.
3. **Montajul cadrelor**: `icomp.py` compune fiecare cadru din plăci, mișcarea camerei și efecte: particule, motorina care curge, apa, bulele, scânteile (`ifx.py`, `fxlib.py`), desene 2D (harta sistemului, grafice, săgeți: `i2d.py`), etichete HTML randate ca PNG (`ikit.py`, stilul în `hud/sprites.html`) și formula fixă a seriei (`iser.py`). Povestea fiecărui episod e în `st_epN.py`; fiecare moment e legat de un cuvânt al vocii: `W(rând, 'cuvânt')`, `L(rând)` = începutul rândului, `LE(rând)` = sfârșitul lui.
4. **Vocea**: `epN/vo_script.json` are textul; `make_vo.py` (copiat în `ep1/`, `ep2/`) alege și aliniază frazele generate cu ASR și scrie `epN/vo/vo_track.wav`, `timeline.json`, `cues.json`. Previzualizările vin din `scripts/prov_vo.py` (0,072 + 0,060 s pe literă, formula fixă cu vocea din ep1).
5. **Reel-ul**: `scripts/setup_reel.sh N` pregătește reel-ul în pipeline-ul `turbodoctor-reels` (cadrele + vocea, fără muzică); `scripts/finish_ep.sh N <Nume>` adaugă subtitrările, titlul din hook și ecranul de final (diagnoză gratuită, telefonul, pictogramele serviciilor) și copiază rezultatul în `/mnt/project-files/animatii/`.

## Comenzi

```
python3 ikit.py epN                                                  # etichetele episodului
python3 icomp.py epN --t 3 8.5 12 --sheet 6 --scale 0.25 --out p.jpg   # cadre de probă
bash scripts/render_ep.sh N 2 fresh                                  # validare + toate cadrele, în out/epN/frames_base
bash scripts/finish_ep.sh N <Nume>                                   # reel-ul, coperta, textul postării
```

Un episod se randează în ≈5 minute pe 4 nuclee; montajul mai ia ≈6 minute.

## Refacerea episoadelor 3–13 cu vocea reală

1. Copiezi `make_vo.py`, `asr2.py`, `vo_qc.py` și `run_iso.sh` din `ep1/` în `epN/`.
2. Generezi fiecare frază din `epN/vo_script.json` cu vocea lui Sabin (ElevenLabs, rețeta frază cu frază pe tonul ingineresc) și o pui în `epN/vo_in/` ca `iN_L<NN><a|b>.mp3`.
3. În `epN/`: `./run_iso.sh make_vo.py lines vo_in` (audio descărcat = date nesigure, de aceea Python rulează izolat).
4. Ștergi `epN/vo/PROVIZORIU`, apoi `ikit`, `render_ep.sh` și `finish_ep.sh` ca mai sus; fișierul iese fără sufixul `_PREVIZUALIZARE`. Dacă se schimbă un cuvânt-cheie din text, se schimbă și în `st_epN.py`.

## Căi și dependențe

Căile sunt scrise în cod: `/home/claude/w/serinj` (codul), `/home/claude/w/inj` (modelul), `/home/claude/turbodoctor-reels` (pipeline-ul), `/home/claude/reels` (reel-urile), `/home/claude/models` (ASR Parakeet, Piper). Python 3 cu opencv, numpy, scipy, soundfile, sherpa-onnx și Playwright (Chromium) pentru etichete. Ecranul de final cu telefonul folosește `CFG.endPhone` din `pipeline/compositor_template.html`, ca la seria turbinelor.
