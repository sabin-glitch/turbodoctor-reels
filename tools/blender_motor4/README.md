# Motor diesel 4 cilindri common rail în secțiune (Blender) · 22.11.2026

Model 3D refolosibil, făcut din scripturi Python pentru Blender 5.3 (`bpy` de pe PyPI), randat cu Cycles. Arhitectura este cea a motorului VW 2.0 TDI common rail (familiile EA189 / EA288), cel mai des întâlnit la noi; proporțiile pe care VW nu le publică sunt reconstruite.

Ce se vede (toate piesele se mișcă sincron, după unghiul arborelui cotit):
- blocul, chiulasa, garnitura, capacul de culbutori și baia de ulei tăiate prin axa cilindrilor (hașură pe fețele secționate);
- arborele cotit forjat cu contragreutăți, bielele, pistoanele cu bol (cameră de ardere în piston), segmenți, bolțuri, volanta;
- 16 supape verticale, arcuri, culbutori cu rolă pe elemente hidraulice, doi arbori cu came cuplați prin roți dințate, camele calculate din mișcarea culbutorului;
- cureaua de distribuție cu dinți (se deplasează pe role), roata arborelui cu came (2:1), pompa de înaltă presiune (1:1), pompa de apă, întinzătorul și rola de ghidare;
- pompa de înaltă presiune tip Bosch CP4.1: camă dublă, tachet cu rolă, pistonaș, arc, supapă de admisie, supapă de refulare cu bilă, dozator (MeUn), motorina colorată după presiune;
- rampa comună tăiată (motorina portocalie), senzorul de presiune, regulatorul de presiune, conductele spre injectoare, returul;
- 4 injectoare Bosch CRI2 (același profil ca modelul CRI2 din proiect), cu clemele lor; 4 bujii incandescente (vârful se înroșește, proprietatea `g` 0..1);
- pompa de ulei cu palete și inel excentric, antrenată cu lanț de la arborele cotit, sorbul, uleiul din baie;
- efecte explicative: aer la admisie (albastru pal), jeturile de motorină (injecție pilot + principală), flacăra, gazele arse, aerul și gazele din porturi.

## Surse
- VW SSP 403 (2.0 TDI CR): pompa de înaltă presiune cu un piston, antrenată de cureaua de distribuție la turația motorului, două came decalate cu 180° pe arborele pompei, până la 1.800 bar; injectorul vertical, central, deasupra bolului din piston; doi arbori cu came cuplați prin roți dințate, cureaua antrenează arborele de evacuare; culbutori cu rolă și elemente hidraulice.
- VW SSP 820433 (EA288): alezaj 81 mm, cursă 95,5 mm, raport de compresie 16,2:1, pompă de ulei cu palete și inel excentric, bujii incandescente din oțel (peste 1.000 °C în cel mult 2 s), cureaua: arbore cotit → întinzător → arbore cu came → pompa de înaltă presiune → pompa de apă.
- Bosch (CP4): unul sau două elemente de pompare, fiecare cu arborele lui cu came, antrenat de curea, lanț sau roți dințate.

## Ce e reconstruit (nu din desene VW)
Cotele chiulasei, porturile, poziția bujiei (pe partea de admisie, înclinată 25°), rampa deasupra capacului cu conducte drepte (traseu simplificat), interiorul pompei CP4.1 (după descrierile Bosch), antrenarea pompei de ulei cu lanț (la EA288 e o curea în baie de ulei), fazele distribuției (valori tipice diesel: admisia 5° înainte de PMS → 35° după PMI, evacuarea 40° înainte de PMI → 5° după PMS, cursa supapelor 9 / 8,6 mm), culorile gazelor (explicative). Mișcarea este încetinită (40–60 rot/min în loc de 800+).

## Fișiere
- `dims.py` cotele, ordinea de aprindere 1-3-4-2, fazele, legile de mișcare (piston, supape).
- `lib.py` (primitive, booleene MANIFOLD, materiale), `mats.py` (biblioteca de materiale), `scene.py` (studio, lumini, camere, setări Cycles), `anim.py` (chei rapide pe acțiunile Blender 5).
- `parts_core.py` bloc, arbore cotit, biele, pistoane, baie · `parts_head.py` chiulasă, supape, culbutori, came · `parts_fuel.py` injectoare, bujii, rampă, conducte · `parts_drive.py` curea, role, pompa de înaltă presiune, pompa de ulei, lanț · `parts_fx.py` gaze, jeturi.
- `build.py` construiește tot, pune cheile pe un ciclu de 720° (cadrul N = N grade de arbore cotit), face variantele de secțiune și cele 5 cadre, salvează `out/motor4.blend` și `out/info.json` (camerele, unghiurile buclelor, ancore pentru etichete).
- `render.py` randează cadrele unui plan (sare peste cele existente), `queue.sh` coada de randare.
- `comp/comp.py` montajul (skia): fundalul Turbo Doctor cu marcajul, buclele curate și filmul de prezentare cu etichete; `comp/fk.py` trusa de desen.

## Planurile (view layer + cameră `CAM_<plan>` în `motor4.blend`)
| Plan | Ce arată | Secțiune | Buclă |
|---|---|---|---|
| `A_motor` | motorul întreg, 3/4 față-stânga | longitudinală prin axa cilindrilor | 720° în 72 de cadre (2,4 s) |
| `D_cilindru` | camera de ardere: injectorul, bujia incandescentă (încinsă), supapele, bolul pistonului, injecția și flacăra | longitudinală, pistoanele tăiate | 720° în 91 de cadre, încetinit în jurul injecției |
| `E_supape` | secțiune transversală prin supapele cilindrului 2: came, culbutori, arcuri, porturi | transversală | 720° în 72 de cadre |
| `B_pompa_inalta` | pompa de înaltă presiune în secțiune | longitudinală + frontală prin camă | 720° în 72 de cadre (4 curse) |
| `C_pompa_ulei` | pompa de ulei cu palete în secțiune, sorbul | longitudinală + frontală prin rotor | 360° în 60 de cadre |

## Comenzi (în cloud, fără placă video)
```
uv venv -p python3.13 vbpy && uv pip install --python vbpy/bin/python bpy==5.3.0 numpy pillow
vbpy/bin/python build.py                                   # ~35 s -> out/motor4.blend + out/info.json
vbpy/bin/python render.py A_motor 0 999 100 8               # cadrele în out/frames/A_motor/ (8 eșantioane + OIDN)
vbpy/bin/python render.py still D_cilindru 57 50 8 x.png    # un cadru de probă la 50%
uv venv -p python3.12 vsk && uv pip install --python vsk/bin/python skia-python numpy pillow
vsk/bin/python comp/comp.py loops                           # buclele: MP4 cu fundal + WebM cu transparență
vsk/bin/python comp/comp.py film                            # filmul de prezentare cu etichete
```
Timpi pe 2 nuclee, 1080×1920: ~23 s/cadru planul general, ~60 s/cadru camera de ardere.

## Randare pe laptopul cu placă video (RTX)
Deschide `motor4.blend` în Blender 5.3 sau mai nou. Edit → Preferences → System → Cycles Render Devices → OptiX. În Render Properties: Device = GPU Compute, mărește Samples (ex. 64). Alege view layer-ul planului (sus-dreapta) și camera `CAM_<plan>` (Scene → Camera). Timeline: cadrul = unghiul arborelui cotit; pentru o buclă de 720° randează cadrele 0–719 cu pasul dorit (Output → Frame Step, ex. 6 → 120 de cadre). Lumea și luminile se reglează pentru fiecare cameră din `render.py` (`setup_shot`).

## Refolosire
- Cadrele cu transparență se scot din WebM: `ffmpeg -c:v libvpx-vp9 -i TurboDoctor_Motor4_A_motor_alfa.webm -pix_fmt rgba f%04d.png`.
- Bujia: proprietatea `g` pe obiectele `glowplug1..4` (0 rece, 1 încinsă). Gazele: proprietățile `col`, `e`, `a` (cu chei) pe `gas0..3`, `gasbowl0..3`; jeturile: `spray0..3` (scara = lungimea jetului în mm, `a` = opacitatea).
- Defecte pentru filme noi se adaugă în `parts_fx.py` / materiale (ex. jet strâmb, picurare, depuneri) și se randează doar planul afectat.
- Convenții: fără profunzime de câmp, hașură pe secțiuni, motorina albastru = joasă presiune / portocaliu = înaltă presiune, uleiul chihlimbar, marcajul „TURBO DOCTOR” pe fundal (pus la montaj), sus „MODEL 3D RECONSTRUIT · MIȘCARE ÎNCETINITĂ”.
