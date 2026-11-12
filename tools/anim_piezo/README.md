# Reel animat „Injectorul piezo versus injectorul magnetic” (12.11.2026)

Reel explicativ din animația 3D „Injector piezo vs. magnetic” (artifact, three.js r128 + canvas 2D), cu vocea lui Sabin din ElevenLabs.
Același flux ca `tools/anim_injectie/` (vezi README-ul de acolo pentru pași).

| Fișier | Rol |
|---|---|
| `index_src.html` | sursa artifactului: simularea (comandă → supapă → cameră de comandă → ac), modelele 3D tăiate pe jumătate (`rev()`), osciloscopul U/I/ac |
| `build_reel.py` | face `reel.html` din `index_src.html` (modelele, simularea, osciloscopul) + `reel_tail.js` + `vo/cues.json`; în reel piezo are 10 injecții pe ciclu |
| `reel_tail.js` | regia pe cuvinte (`Wd(linie,'cuvânt')`): starea fiecărui injector (`est`), cadrele camerei cu zona 3D pe rândurile `pt..pb`, etichete, tensiunile, cartonașele Bosch, contorul reprize/doze |
| `vo_script.json`, `make_vo.py` | textul și vocea (`python3 make_vo.py take vo/t1.mp4 vo/t2.mp4`) |
| `render_frames.js` | `node render_frames.js <reel>/frames_base 0 <ultimul cadru>` (~0,9 s/cadru; se pot porni două procese pe intervale diferite) |
| `../../pipeline/examples/reel_piezo_vs_magnetic_animatie.js` | `reel.js` |

Lângă fișiere: `fonts/` (Barlow și Barlow Condensed 500/600/700, latin + latin-ext, din @fontsource) și `three.min.js` (three@0.128.0).

Cifrele din partea „Bosch spune așa” sunt din fișa Bosch CRS3-27 (forță ~10× față de solenoid, interval minim 100 µs, până la 10 injecții, 2.700 bar).
Tensiunile (48 V, ~150 V) sunt valori tipice, nu din fișă.

Așezare: zona 3D y 250–950 când sunt grafice (958–1278), 250–1270 fără; în hook 560–1280 (titlurile boom deasupra); subtitrările de la 1290.
