> Copie a README-ului din /mnt/project-files/animatii/sursa/dpf-ea288/. Acolo scripturile stau în `work/`; aici sunt în acest folder.

# Eroare de eficiență DPF la 2.0 TDI EA288 (film 3D, Blender)

Film vertical 1080×1920, 30 fps, 102,5 s, fără voce (texte pe ecran).
Rezultatul: `animatii/TurboDoctor_Animatie_3D_Eroare_Eficienta_DPF_EA288.mp4` și `_coperta.jpg`.
Ce e găsit în surse și ce e deducție: documentul „Note de verificare” din proiect.

## Ce e în acest dosar

| Loc | Ce conține |
|---|---|
| `work/` | toate scripturile, `hud.html`, `out/assets.blend` (scena Blender) și `out/meta.json` |
| `fonts/` | fonturile Barlow și Barlow Condensed folosite de `work/hud.html` (căi relative `../fonts/...`) |
| `pl.tar.xz` | tot ce a randat Blender: cadrele fixe, adâncimile, buclele de mișcare și rotirea de început. Se despachetează în `work/` (`tar -xJf pl.tar.xz -C work/`) și filmul se poate monta din nou fără nicio randare Blender |
| `reel/` | reelul „Eroarea P2002” făcut din acest film pe vocea lui Sabin (15.11.2026): planul pe cuvinte, compunerea cadrelor, textele, vocea, uneltele și README-ul lui |
| `arhiva/` | prima variantă a filmului (15.11.2026 dimineața), cu fumul de la furtunașul crăpat tăiat în pătrate (vezi „Capcane întâlnite”) |

## Cum e făcut

Imaginea 3D e randată în **Blender 5.0 (Cycles)**. Ca să încapă pe un calculator fără placă video, filmul e construit din straturi:

1. **Cadre fixe** (`pl/<camera>__<stare>.png`): fiecare unghi de cameră randat o dată la 1080×1920, 32 de eșantioane + denoise. Stările aceleiași camere (curat / cu funingine / cu fisură / radiografie / supapă deschisă sau închisă) sunt topite între ele la montaj.
2. **Adâncime** (`.z.npy`): pentru fiecare cadru, distanța până la prima suprafață opacă. Cu ea particulele trec corect prin spatele pieselor.
3. **Bucle de mișcare** (`pl/loop_*`): motorul în 4 timpi (60 de faze) și rotorul turbinei (12 faze), randate separat la 720×1280, cu restul scenei ca mască.
4. **Rotirea de început** (`pl/orbit/`): 150 de cadre randate unul câte unul la 900×1600.
5. **Particule** (gaze, funingine, depuneri, antigel, abur, ulei, motorină, cenușă, fisura filtrului): desenate peste cadre cu numpy, cu test de adâncime (`fxlib.py`, `story.py`). Sunt funcții de timp, deci se reglează fără randare nouă.
6. **Texte** (`hud.html`): titluri, etichete, indicatorul „funingine calculată / măsurată”, schema logicii și lista de la final, randate cu Playwright ca imagini transparente.

## Fișiere (în `work/`)

| Fișier | Rol |
|---|---|
| `kit.py`, `mats.py`, `layout.py`, `rig.py` | unelte de modelare, materiale, cote, lumini și cameră |
| `m_engine.py`, `m_turbo.py`, `m_module.py`, `m_egr.py`, `m_misc.py` | modelele: motor, turbină, catalizator + DPF în secțiune, răcitor și supapă EGR, senzori și furtunașe |
| `build.py` | construiește scena → `out/assets.blend` (+ `out/meta.json`) |
| `shots.py` | camerele, stările și lista de cadre de randat |
| `film.py`, `plates.py` | randarea în Blender (cadre fixe, bucle, rotire) |
| `gas.py`, `fxlib.py`, `story.py`, `comp.py` | traseele gazelor, particulele, scenariul (planuri, durate, texte) și montajul |
| `hud.html`, `hud_render.js`, `hud_probe.js`, `hud_data.js` | textele de pe ecran |
| `probe.sh`, `cover.py`, `assemble.sh`, `sheets.sh` | cadre de probă, coperta, asamblarea finală în paralel, planșe de contact din filmul codat |

## Refacerea filmului

Unelte: două medii Python (unul cu `bpy==5.0.1` și `numpy==1.26.4` pe Python 3.11, unul cu `numpy` 2, `opencv-python-headless` și `pillow`), Node cu Playwright (calea e scrisă în `hud_render.js` și `hud_probe.js`) și ffmpeg. Scripturile de montaj caută mediul al doilea la `../venv2/bin/python` (se schimbă cu `PY=...`).

```bash
# 1. scena (o singură dată)
python build.py
# 2. randarea Blender (sare peste ce există deja; se poate relua oricând). Cu pl.tar.xz despachetat, pasul nu mai e necesar.
SPP=32 WHAT=plates,loops,orbit python plates.py
# 3. textele
python story.py && node hud_render.js    # scrie hud_data.js și hud/00000.png ... (7 minute)
# 4. montajul
./assemble.sh film.mp4                   # câte o bucată pe plan în seg/, 4 în paralel, apoi lipire fără recodare
./assemble.sh film.mp4 s13 s14           # reface doar planurile numite și lipește din nou
```

Un singur cadru de probă: `python comp.py --scale 0.5 --t 47.6 --out proba.jpg`. O planșă cu texte: `./probe.sh sc/proba.jpg 6 47.5 48.5 49.5`.
Schimbarea unui text, a unei etichete, a unei durate sau a unui efect cu particule cere doar pașii 3 și 4 (cam 20–30 de minute), fără randare nouă în Blender. După o schimbare de text se randează din nou doar cadrele atinse: `node hud_render.js <primul cadru> <ultimul cadru + 1>`.

Capcane întâlnite:
- materialele translucide (lichidul de răcire) dau o adâncime „găurită”; `comp._z` o netezește cu o eroziune 5×5 pentru cadrele `cool__*`;
- particulele desenate în modul `over` nu țin cont de ordine (se face o medie ponderată), deci aburul alb peste depuneri negre se desenează în modul `add`;
- un punct de pondere 1 acoperă doar ~62%; masele pline se fac din multe puncte mici suprapuse.
- stropii mari erau tăiați în pătrate: `fxlib.Canvas.RMAX` limita jumătatea nucleului unui strop la 56 px, iar fumul scăpării de la furtunașul crăpat (s06) are stropi cu raza de până la ~200 px. Limita e acum 420. Filmul livrat a fost reparat pe 15.11.2026: au fost refăcute doar bucățile s06 și s07 (`./assemble.sh film.mp4 s06 s07`; s07 fiindcă începe cu trecerea din s06), restul filmului e neschimbat, pachet cu pachet. Celelalte bucăți din `seg/` sunt randate cu limita veche (acolo stropii tăiați nu se văd); la o refacere completă, s16 și s11 ies cu strălucirea puțin mai moale. `reel/tools/clipscan.py` arată plan cu plan stropii care ar fi tăiați.

## Timpi de randare (4 nuclee, fără placă video)

Cele 21 de cadre fixe: între 1 și 7,5 minute fiecare. Buclele: 5–19 s pe cadru. Rotirea de început: 20–40 s pe cadru. În total, cam o oră și trei sferturi de randare Blender, 7 minute pentru texte și 15–25 de minute pentru montaj.

## Randare pe un calculator cu placă video

`out/assets.blend` se deschide direct în Blender 5.0. Scripturile încearcă placa video dacă pornesc cu `DPF_GPU=1` (OptiX pe NVIDIA RTX, altfel CUDA): `DPF_GPU=1 SPP=64 WHAT=plates,loops,orbit python plates.py`. **Ramura aceasta nu a fost testată** (aici nu există placă video). Cu placă video, fiecare plan poate fi randat și cadru cu cadru, cu mișcare reală de cameră, în loc de cadre fixe.

## Conținut tehnic

Pe scurt: eroarea P2002 apare când funinginea „măsurată” (din presiunea pe filtru) iese mult sub cea „calculată”; legătura cu răcitorul EGR înfundat e raportată de proprietari de EA288, dar mecanismul intern arătat în film e dedus. Valorile în grame din indicator sunt exemple, nu date de fabrică. Detaliile și linkurile sunt în documentul „Note de verificare”.
