# Filtrul de particule (DPF) cu catalizator de oxidare (DOC) în aceeași carcasă · Blender (24.11.2026, aprobat de Sabin pe 24.11)

Model 3D făcut în Blender pentru explicațiile video Turbo Doctor despre filtrele de particule: carcasa de inox cu **catalizatorul de oxidare** și **filtrul de particule** în ea, în secțiune, cu toți senzorii de pe carcasă și cu **senzorul de presiune diferențială** (prize, țevi, furtunașe, senzor).

- **Catalizatorul de oxidare (DOC):** monolit ceramic cu canale drepte, deschise la ambele capete.
- **Filtrul de particule (DPF):** carbură de siliciu, din segmente pătrate lipite cu ciment ceramic; canalele sunt închise alternativ cu dopuri (un canal la ieșire, vecinul lui la intrare), deci gazele trec prin pereții poroși.
- **Saltelele de fixare** dintre ceramică și carcasă, conurile de intrare și de ieșire, cotul cu flanșă spre turbină, cotul cu flanșă spre eșapament, cordoanele de sudură.
- **Senzorii:** sonda lambda (în cotul de intrare), trei senzori de temperatură (înainte de catalizator, înainte de filtru, după filtru), senzorul de presiune diferențială pe suport cu ecran termic, cu două furtunașe și două țevi metalice până la prizele de pe carcasă (una între catalizator și filtru, una în conul de ieșire).

## Fișiere

| Fișier | Ce e |
|---|---|
| `animatii/TurboDoctor_DPF_Filtru_de_particule_9x16.mp4` | filmul, vertical 1080×1920, 76 s, cu titlu, etichete, texte și cartonul Turbo Doctor |
| `animatii/TurboDoctor_DPF_Filtru_de_particule_coperta.jpg` | cadrul cu secțiunea întreagă și etichetele pieselor |
| `animatii/TurboDoctor_DPF_Filtru_de_particule_curat_9x16.mp4` | același film fără titlu, etichete, texte și carton (rămân marcajul pe fundal și „MODEL 3D RECONSTRUIT”), 70 s, pentru montaj cu vocea |
| `animatii/stills/*.jpg` | cadre statice fără texte: exterior, secțiune, fața filtrului, canalele cu gaze, cu funingine, senzorii, presiunea diferențială, regenerarea, cenușa |
| `dpf.py`, `kit.py` | modelul (Python pentru Blender 5.0, `bpy`), materialele, lumina, camera, randarea pe straturi; `kit.py` = ajutoarele de modelare din `tools/blender_turbo_lagare/turbo.py` |
| `queue.sh` | randează toate straturile care lipsesc (se poate reporni) |
| `comp/comp.py`, `comp/fk.py`, `comp/render_all.sh` | montajul (skia-python + numpy + OpenCV): straturile Blender, gazele, funinginea, regenerarea, cenușa, etichetele, textele |
| `out/dpf.blend` | scena Blender (Blender 5.0+, Cycles), colecții pe piese |
| `layers.tar` | toate straturile randate (PNG pe 8 biți) + fișierele json; despachetat în acest dosar (`tar xf layers.tar`), montajul se reface fără Blender |
| `pack_layers.py`, `crop_of.py` | fac `layers.tar`; decupajul unei zone 3D pentru probe |

## Cum e făcut

Modelul e construit din profile de revoluție, tuburi pe traseu și booleene (solverul MANIFOLD), 1 unitate = 1 mm. Axa carcasei e Z, gazele curg de sus în jos (intrarea de la turbină sus, ieșirea jos); secțiunea e în planul y = 0 și rămâne jumătatea din spate. Toți senzorii, țevile și furtunașele stau în jumătatea din spate, deci rămân întregi în secțiune.

Cele două ceramici nu sunt texturi: fiecare canal e geometrie (plasă generată direct, fără booleene). Planul de secțiune trece prin mijlocul unui rând de canale, deci în tăietură se văd canalele pe toată lungimea, cu dopurile lor, iar pe fața de intrare se vede tabla de șah a canalelor deschise și închise.

- Filtrul: Ø 144 × 178 mm, pas 1,8 mm, perete 0,38 mm (clasa 200 de canale pe țol pătrat), segmente de 34,3 mm cu rost de ciment de 1,6 mm, dopuri de 6 mm.
- Catalizatorul: Ø 144 × 76 mm, pas 1,27 mm, perete 0,17 mm (clasa 400 de canale pe țol pătrat).
- Saltea de 5 mm, carcasă de 1,5 mm, 20 mm între catalizator și filtru.

Randarea (Cycles pe procesor, fără placă video) e pe straturi, toate din aceeași cameră, deci zoomul din montaj nu pierde claritate: planșa întreagă (2160×2160), aceeași la densitate dublă, zona feței de intrare a filtrului la densitate ×8 și două planșe macro la densitate ×24 (capătul de intrare și capătul de ieșire al filtrului, circa 74 de pixeli pe milimetru). Pe lângă ele, jumătatea din față (pentru deschiderea secțiunii) și planșe-mască în canalele R / G / B (filtru, catalizator, saltele; canale de intrare, canale de ieșire, dopuri; senzori; țevi, furtunașe, senzorul de presiune), din care montajul face funinginea, culoarea canalelor, strălucirea de la regenerare și evidențierea senzorilor.

```
uv venv -p python3.11 venv && uv pip install -p venv/bin/python bpy==5.0.1 numpy==1.26.4
venv/bin/python dpf.py build          # out/dpf.blend (~2 s)
venv/bin/python dpf.py info           # out/info.json, out/crops.json (proiecții, decupaje, ancore, trasee)
PY=venv/bin/python ./queue.sh         # toate straturile (~1 h 05 pe 2 nuclee, fără placă video); sare peste ce există
# (sau: tar xf layers.tar  -> straturile gata randate, fără Blender)
venv/bin/python dpf.py prev 1 "" shell,mats,doc,dpf,acc 40 24 proba.png          # probă rapidă a secțiunii
venv/bin/python dpf.py look 0.3,0.9,-0.3 0,0,1 760 1000 48 unghi.png               # exteriorul din orice direcție
cd comp                                # montajul: pip install skia-python opencv-python-headless numpy
python3 comp.py --png 10.5,24,46       # cadre de probă (secunde)
python3 comp.py --out film.mp4         # filmul cu texte (76 s, ~6 min): câte un fișier pe capitol în film.mp4.seg/, lipite fără recodare
python3 comp.py --out film.mp4 --force 8,9   # reface doar capitolele 8 și 9 (de exemplu după o schimbare de text), restul rămân
CLEAN=1 python3 comp.py --out curat.mp4
CLEAN=1 python3 comp.py --stills
```

Pe un calculator cu placă video, `out/dpf.blend` se deschide direct în Blender 5.0+ (Cycles → GPU Compute), camera `cam_main`. Colecțiile: `shell` (carcasa, conurile, coturile, sudurile; jumătatea din spate), `front` (jumătatea din față, cu plăcuța de tip), `mats` (saltelele), `doc`, `dpf` (ceramicile, pe obiecte: pereți, canale de intrare, canale de ieșire, dopuri, ciment), `acc` (senzorii, țevile, furtunașele, suporturile).

## Cronologia (76 s)

0–3,4 exteriorul · 3,4–5,2 jumătatea din față se ridică (secțiunea) · 5,2–12 secțiunea întreagă, gazele trec prin catalizator și prin filtru (portocaliu = cu funingine, albastru = filtrate) · 13,6–19,6 fața de intrare a filtrului: canale închise alternativ · 21,2–25,6 macro: gazele trec prin pereții poroși · 25,6–29,8 funinginea se așază în canalele de intrare · 32,2–38,6 senzorii de pe carcasă (sonda lambda, cei trei senzori de temperatură) · 40–50,4 senzorul de presiune diferențială: prizele, țevile, furtunașele, senzorul, diferența de presiune · 52–58,6 regenerarea (catalizatorul încălzește gazele, funinginea arde, diferența de presiune scade) · 60,6–65,8 macro la capătul de ieșire: cenușa rămâne · 68,3–72,7 „Pe scurt” · 72,9– cartonul Turbo Doctor. Varianta curată se oprește la 69,8 s, pe secțiunea întreagă.

## Surse și ce e reconstruit

- Construcția cu pereți filtranți (canale pătrate, închise alternativ la capete, gazele trec prin pereții poroși): DieselNet, „Diesel Filter Materials”. Filtrele din carbură de siliciu sunt făcute din segmente lipite cu ciment: brevetul US 6508852; exemplu de geometrie (perete 0,38 mm, 31 de canale pe cm²): brevetul NGK US 7087286.
- Filtrul cu catalizator de oxidare în aceeași piesă, sonda lambda G39, senzorii de temperatură G495 (înainte de filtru) și G648 (după filtru), senzorul de presiune cu țevi de presiune spre filtru, ecranul lui: manualele de reparații VW / Audi / Seat pentru 2.0 TDI common rail (workshop-manuals.com); Hella Tech World, „Checking the exhaust gas temperature sensor” (temperatura e urmărită înainte de catalizator, înainte de turbină, înainte și după filtrul de particule).
- Senzorul de presiune diferențială cu două racorduri (înainte și după filtru), ce face calculatorul cu semnalul, regenerarea pasivă 350–500 °C și activă 600–650 °C: VW SSP 336 (vezi `memorie/senzor-presiune-diferentiala.md` din proiect). Cenușa din ulei nu arde și rămâne în filtru: Castrol, Hella (vezi `memorie/film-semeringuri-supape.md`).

Reconstruit, de confirmat cu poze din atelier sau cu un cod de piesă: forma exactă a carcasei (e un ansamblu generic, de tipul celor montate lângă turbină la 2.0 TDI common rail; cotele sunt alese de mine), poziția exactă a bosajelor, forma senzorului de presiune și a suportului, traseul țevilor, numărul și locul senzorilor de temperatură (diferă de la model la model: la 2.0 TDI Euro 5 primul senzor stă înainte de turbină, nu pe con; la unele modele, de la sfârșitul lui 2010, senzorul de presiune are o singură țeavă, cea dinainte de filtru). Culorile gazelor, grosimea stratului de funingine, înălțimea cenușii și barele de presiune sunt ilustrative.
