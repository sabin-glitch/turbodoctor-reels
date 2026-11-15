# Probă Blender: pompa CP4 în secțiune (14–15.11.2026)

> Copie din `/mnt/project-files/animatii/sursa/blender-cp4/` (fără fișierele `.blend`, fără geometrie și fără cadre randate). Căile relative de mai jos (`../amorsare-filtru/…`, `../../TurboDoctor_…`) se referă la dosarul acela din proiect.

Aceeași geometrie ca „Amorsare filtru motorină” (`../amorsare-filtru/out/geo.bin` + `geo.json`), randată cu Blender 5.0.1 / Cycles pe CPU.

- Prima probă (`scene_v1.py`): `../../TurboDoctor_Proba_Blender_CP4.mp4` (5,2 s, 156 de cadre randate la 720×1280 și mărite la 1080×1920), copertă `_coperta.jpg`, comparație `_comparatie.jpg`, cadru de pornire pentru AI video `_cadru_pornire.png`.
- Varianta 2 (`scene.py`, 15.11.2026), după observația lui Sabin că în capul hidraulic s-au pierdut claritatea și elementele grafice: cadre `../../TurboDoctor_Proba_Blender_CP4_v2_cadru_larg.jpg`, `_v2_cap_hidraulic.jpg`, `_v2_comparatie.jpg` (three.js | prima probă | corectat).

## Ce s-a schimbat în varianta 2
- Motorina e lichid „grafic”, ca în animația three.js: Principled cu bază neagră și emisie în culoarea convenției (albastru 0x2f8cff joasă presiune, portocaliu 0xff6a3d înaltă presiune), amestecat cu Transparent. Culoarea și opacitatea au cheie la fiecare cadru, după formulele din `src/10_cp4.js` (camera de pompare trece din albastru în portocaliu cu presiunea, totul pălește când intră aerul). Lichidul fizic din prima probă (transmisie + absorbție) ieșea aproape incolor la scara 0,001.
- Hașura de pe fețele secționate e refăcută cu noduri (`hatch=(perioadă mm, intensitate, semnul lui y)` în `pbr()`), pe coordonate Object, cu aceeași formulă ca în `src/00_core.js`. Cele două plane de tăiere au tonuri diferite (`SEC_TONE`), ca muchia secțiunii să se citească.
- Fețele de secțiune sunt mate (metalic 0,5, asperitate 0,6) și închise la 0,42 din culoarea three.js (`SEC_K`), altfel lumina cheie le arde și hașura dispare.
- Fără estompare de profunzime (implicit; `DOF=1` o readuce) și randare directă la 1080×1920.
- Variabile de mediu pentru reglaj: `LIQ_EMIT`, `LIQ_OP`, `SEC_K`, `SEC_M`, `SEC_R`, `HATCH`, `SEC_TONE`, `MB` (obturator motion blur), `KEYK` (tăria luminii cheie), `FRAMES` (dosarul cadrelor), `VT`/`LOOK`/`EXPO` (culoare), `CAM="cx,cy,cz,azimut,elevație,distanță,focală"` (cameră fixă), `OUT` (numele cadrului).

## Refacere în cloud (fără placă video)
```
uv venv -p python3.11 venv && uv pip install -p venv/bin/python bpy==5.0.1 numpy   # bpy de pe PyPI; download.blender.org e blocat de proxy
mkdir src && cp ../amorsare-filtru/out/geo.* src/ && cp venv/lib/python3.11/site-packages/bpy/5.0/datafiles/studiolights/world/studio.exr src/
OUT=larg.png MB=0.2 venv/bin/python scene.py still 15 1080 96                                  # cadrul larg (lățime 1080, 96 de eșantioane) în out/
OUT=cap.png MB=0.2 CAM="18,62,4,40,12,340,60" venv/bin/python scene.py still 15 1080 96       # prim-plan pe capul hidraulic
FRAMES=frames_v2 WX=1080 SPP=32 venv/bin/python scene.py anim 0 79                           # cadrele în frames_v2/ (sare peste cele existente); pe bucăți: 0–79, 80–129, 130–179
venv/bin/python scene.py save                                                                  # out/cp4_proba.blend, cu HDRI-ul împachetat
python3 cmp2.py original_three.png blender_v1.png blender_v2.png comparatie.jpg                # comparația pe zona capului hidraulic
ffmpeg -framerate 30 -i frames_v2/f%04d.png -vf "format=yuv420p" -c:v libx264 -crf 17 -preset slow -movflags +faststart out.mp4
```

## Randare pe un calculator cu placă video (ex. laptop cu RTX)
`cp4_proba.blend` e de sine stătător: se deschide în Blender 5.0 sau mai nou. Edit → Preferences → System → Cycles Render Devices → OptiX (sau CUDA), apoi în Render Properties: Device = GPU Compute. Render → Render Animation scrie cadrele în `cadre/` lângă fișier (1080×1920, 64 de eșantioane, 180 de cadre).

## De știut
- Reperul three.js (mm, Y sus) e păstrat sub empty-ul `CP4` (rotit 90° pe X, scară 0,001); cinematica (`hPar`/`hCross`, ceasuri) e portată 1:1 din `src/10_cp4.js`.
- Arcul are două forme (shape keys): poziția spirelor e liniară în cursa tachetului.
- Toate obiectele au cheie la fiecare cadru, interpolare liniară, ca să meargă motion blur (scânteile devin dâre).
- Cronologia: `T_FUEL`, `T_HEAT`, `T_ROT`, `T_DAM`, `T_CHIP`, `T_SPARK`; camera în `SH`.
- Viteză în cloud (4 nuclee, fără GPU): la 720×1280 cu 32 de eșantioane + OIDN ~37 s/cadru la planul larg și ~57 s/cadru la prim-plan; un cadru fix la 1080×1920 cu 96 de eșantioane ~2,5 minute; în animație, la 1080×1920 cu 32 de eșantioane, ~70 s/cadru la planul larg.
- O comandă în fundal e oprită după 2 ore: randarea din 14.11 s-a oprit la cadrul 155 din 179. Pentru clipuri mai lungi, randează pe bucăți (`anim a b`), nu într-o singură comandă.
- AgX rămâne transformarea de culoare: cu Khronos PBR Neutral aluminiul turnat iese ars.
