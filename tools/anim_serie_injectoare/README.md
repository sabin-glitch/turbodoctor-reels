# Seria „De ce se strică injectoarele” (13 episoade)

Cerută de Sabin pe 15.11.2026. Cauzele, sursele și lista de episoade sunt în documentul seriei: https://claude.ai/artifact/VM3hYyAsn2TFCGdUH4RK4o. Notele de cercetare (engleză, cu citate și linkuri) sunt în `/mnt/project-files/animatii/sursa/serie-injectoare/cercetare/`.

Reel-urile: `/mnt/project-files/animatii/TurboDoctor_Reel_Serie_Injectoare_NN_<Nume>.mp4`, cu `_coperta.jpg` și `_text_postare.txt`. Toate cele 13 au vocea generată a lui Sabin (1 și 2 pe 15.11.2026, 3–13 pe 16.11.2026; previzualizările de peste noapte sunt mutate în `previzualizari/`, în folderul seriei din proiect). Nimic nu e publicat sau programat fără aprobarea lui Sabin.

## Cum e făcut

1. **Modelele** (Blender, `bpy` de pe PyPI în `/home/claude/w/venv_bpy`): injectorul electromagnetic generic de tip Bosch, modelat întreg și tăiat în secțiune (o pană de 120° spre cameră), filtrul cu separator de apă (`model/model.py`, `model/filter.py`, materialele în `model/imats.py`), plus scena micro cu jocul de 3 µm dintre ac și ghidaj și firul de păr (`micro.py`), rezervorul (`tank.py`), scaunul bilei cu adâncituri și canal (`seatdmg.py`) și calamina din puțul injectorului (`xsoot.py`).
2. **Plăcile**: fiecare cadru fix (cameră + stare) se randează o singură dată în Cycles, pe procesor: imaginea, adâncimea (`.z.npy`) și camera (`.json`). Camerele și stările sunt în `ishots.py`; randarea: `venv_bpy/bin/python iplate.py cam:stare … [--preview] [--force]` (fără `--force` sare peste plăcile existente). Plăcile gata sunt în `pl.tar.xz`, în folderul seriei din proiect.
3. **Montajul cadrelor**: `icomp.py` compune fiecare cadru din plăci, mișcarea camerei și efecte: particule, motorina care curge, apa, bulele, scânteile (`ifx.py`, `fxlib.py`), desene 2D (harta sistemului, grafice, săgeți: `i2d.py`), etichete HTML randate ca PNG (`ikit.py`, stilul în `hud/sprites.html`) și formula fixă a seriei (`iser.py`). Povestea fiecărui episod e în `st_epN.py`; fiecare moment e legat de un cuvânt al vocii: `W(rând, 'cuvânt')`, `L(rând)` = începutul rândului, `LE(rând)` = sfârșitul lui.
4. **Vocea**: `epN/vo_script.json` are textul; `make_vo.py` (copiat în fiecare `epN/`) alege și aliniază frazele generate cu ASR și scrie `epN/vo/vo_track.wav`, `timeline.json`, `cues.json`, `picks.json` (secțiunea „Vocea” de mai jos). Previzualizările de peste noapte veneau din `scripts/prov_vo.py`; vocea lor provizorie e păstrată în `epN/vo_prov/`.
5. **Reel-ul**: `scripts/setup_reel.sh N` pregătește reel-ul în pipeline-ul `turbodoctor-reels` (cadrele + vocea, fără muzică); `scripts/finish_ep.sh N <Nume>` adaugă subtitrările, titlul din hook și ecranul de final (diagnoză gratuită, telefonul, pictogramele serviciilor) și copiază rezultatul în `/mnt/project-files/animatii/`.

## Comenzi

```
python3 ikit.py epN                                                  # etichetele episodului
python3 icomp.py epN --t 3 8.5 12 --sheet 6 --scale 0.25 --out p.jpg   # cadre de probă
bash scripts/render_ep.sh N 2 fresh                                  # validare + toate cadrele, în out/epN/frames_base
bash scripts/finish_ep.sh N <Nume>                                   # reel-ul, coperta, textul postării
```

Un episod se randează în ≈5 minute pe 4 nuclee; montajul mai ia ≈6 minute.

## Vocea (cum a fost făcută la 3–13, pe 16.11.2026)

1. Fiecare rând generat din `epN/vo_script.json` (hook-ul și corpul; formula fixă se refolosește) a plecat la ElevenLabs separat, cu rețeta pe tonul ingineresc: `eleven_v4`, vocea „Sabin”, `[calm] [matter of fact]` în față (hook-ul: tag-urile din câmpul `tags`), 2 variante, textul rostit din `{afișat|rostit}`.
2. Descărcarea: CDN-ul ElevenLabs e blocat din container, așa că fișierele vin prin workflow-ul `fetch-sources` din `turbodoctor-reels`, cu nume `si<N>L<NN><a|b>` (`scripts/mk_fetch.py` face lista din rezultatele generărilor), apoi `git show FETCH_HEAD:si…mp4 > epN/vo_in/iN_L<NN><a|b>.mp3`. Un ID deja prezent pe branch-ul `sources` se sare, deci o frază refăcută primește altă literă (ex. `c`, `d`).
3. Rândurile refolosite, în `epN/vo_in/`: introducerea (`iN_L00a.wav` = primele 3,05 s din `ep1/vo/vo_track.wav`, până înainte de „Astăzi”), „Vezi toate cauzele…” (`ep1/vo_in/i1_L01a.mp4`) și cele trei fraze de final (`i1_L11a`–`i1_L13a`).
4. În `epN/`: `./run_iso.sh make_vo.py lines vo_in` (audio descărcat = date nesigure, Python izolat). `VO_PICK='{"7":"d"}'` impune o variantă.
5. Verificarea: `python3 -I scripts/asr_picked.py epN` trece varianta aleasă prin Parakeet și Whisper și arată diferențele față de textul rostit; `scripts/ctx.py epN <rând>` ascultă începutul unui rând în context. O diferență prinsă de amândouă e reală (ex. „Jetul” la început de propoziție ieșea englezește; la 4 a devenit „…, iar jetul se strică”).
6. Montajul: `scripts/queue_final.sh 3 4 … 13` randează și montează pe rând (fiecare episod așteaptă `logs/vo_ok_epN`, pus după verificarea vocii); `scripts/qc_final.sh N` dă durata, sunetul și o foaie de contact. Dacă se schimbă un cuvânt-cheie din text, se schimbă și în `st_epN.py`.

## Căi și dependențe

Căile sunt scrise în cod: `/home/claude/w/serinj` (codul), `/home/claude/w/inj` (modelul), `/home/claude/turbodoctor-reels` (pipeline-ul), `/home/claude/reels` (reel-urile), `/home/claude/models` (ASR Parakeet, Piper). Python 3 cu opencv, numpy, scipy, soundfile, sherpa-onnx și Playwright (Chromium) pentru etichete. Ecranul de final cu telefonul folosește `CFG.endPhone` din `pipeline/compositor_template.html`, ca la seria turbinelor.
