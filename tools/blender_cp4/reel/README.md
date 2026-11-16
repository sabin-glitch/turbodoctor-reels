# Reelul „Un banal schimb de filtru de motorină…” cu pompa CP4 randată în Blender (15.11.2026)

> Copie din `/mnt/project-files/animatii/sursa/blender-cp4/reel/`. Randările Blender, trecerile paginii și măștile marcajului sunt în `work/` acolo; `director.json` se reface cu `python3 director.py`. Căile relative (`../README.md`, `../../amorsare-filtru/reel/work/`) se referă la dosarele din proiect.

Sabin a acceptat aspectul corectat al pompei din Blender (motorină colorată, hașură, claritate) și a cerut reelul final refăcut cu ea. Se refac doar cadrele cu pompa în secțiune: hook-ul (cadrele 0–173) și partea 1:13–1:41 (cadrele 2180–3038). Vocea, subtitrările, titlurile, ștampilele și restul animației sunt cele din varianta 2 (`../../amorsare-filtru/reel/work/`).

## Cum e făcut

1. **Camera din Blender = camera paginii three.js.** `reel_scene.py`: FOV vertical 30° (`sensor_fit='VERTICAL'`, `sensor_height=24`, `lens=12/tan(15°)`), `shift_y=-oy/1920` pentru `setViewOffset`, poziția din țintă + azimut/elevație/distanță. Două camere fixe: `W` (plan larg) și `C` (prim-plan). Suprapunerea cu pagina e sub 0,001 px, deci etichetele, panoul și particulele paginii cad exact pe pompa din Blender.
2. **Bucle pe regiuni.** Cama e dublă, deci mecanismul se repetă la o jumătate de tură: `NL=38` de cadre (≈2,5 rad/s, cât avea și reelul). Pentru fiecare cameră și stare se randează o placă fixă pe tot cadrul și, la fiecare cadru al buclei, doar regiunea pieselor în mișcare (`R1`: camă, tachet, rolă, piston, arc, supape, coloana de motorină) și pana arborelui (`R2`, perioadă de o tură întreagă = 76 de cadre). Zonele fixe nu pâlpâie între cadre (același seed, OIDN), așa că lipirea nu se vede. Fundal transparent, fără motion blur.
   Stări: `FUEL` (motorină), `AIR` (aer, rece), `HOT` (aer, rola încinsă), `ROT0`/`ROT1` (tachetul se rotește 0–90° în 90 de cadre, cu cama întreagă / tăiată), `CROSS` (rola de-a curmezișul, cama tăiată).
3. **Regia** (`director.py` → `director.json`): pentru fiecare cadru al reelului, timpul animației `U` (din `vo/uframes.json`, ca etichetele și panoul să rămână pe voce), camera, starea pompei pentru pagină și rețeta de compunere. Planul larg ține până la „Se blochează și freacă de camă” (cadrul 2658), apoi prim-planul până la capăt; rotirea tachetului începe la cadrul 2740 („Tachetul se rotește în alezaj”). Trecerile motorină → aer → rolă încinsă sunt amestecuri între bucle la aceeași fază; cama trece din întreagă în tăiată între cadrele 51–58 ale rotirii. Hook-ul refolosește cadrele rotirii și ale buclei `CROSS`.
4. **Trecerile paginii** (`anim/patch_reel.py` aplicat peste sursa animației, `anim/ovrender.cjs`): pagina primește camera și starea prin `window.__OV` și scoate cu `window.__grab()` două imagini pe cadru: `ovl` (bule, pilitură, etichete, panoul CP4, degrade-urile de sus și de jos, pe fond transparent; pompa rămâne doar ca mască de adâncime) și `add` (scântei și strălucirea de la contact, pe negru). Panoul „Bosch CP4 · secțiune” apare doar în planul larg (`panel` în regie, `window.__OV.panel` în pagină): în prim-plan acoperea supapele din capul hidraulic, exact zona despre care Sabin a întrebat de ce nu e clară, așa că acolo e scos (alegerea mea, spusă la livrare).
5. **Compunerea** (`compose.py`): fundal #111417 + marcajul din fundal → pompa din Blender (placă + R1 cu margine înmuiată + R2 cu mască) → `add` (adunat) → `ovl` (peste) → `frames_bl/NNNNN.jpg`.
6. **Marcajul „TURBO DOCTOR” din fundal** (cerut de Sabin pe 15.11.2026 pentru toate animațiile): `wm_pattern.py` face desenul identic cu cel din seria turbinelor (`tools/anim_serie_turbine`), `wm.py` îl mișcă (9 px/s, −20°). Stă pe fundal, în spatele scenei, în fiecare cadru. În cadrele Blender e sub pompă (alfa din randare). În restul cadrelor, `anim/amask.cjs` scoate din pagină masca a ceea ce acoperă fundalul (obiectele opace și HUD-ul, la 540×960), iar `wmapply.py` adaugă marcajul în rest: `cadru + (1 − mască) · delta`. Caroseria „raze X” și strălucirile sunt materiale aditive, deci fundalul se vede întreg prin ele și marcajul rămâne sub ele; podeaua se topește în fundal și nu se pune în mască. Măștile se randează rar (`mask2_list.json`: din 4 în 4 cadre, mai des la mișcări rapide, pe ambele părți ale tăieturii de la cadrul 174) și se interpolează. Când pagina stinge cadrul spre fundal (trecerile de la 54,5 s, 60,2 s și 78,7 s din animație), marcajul rămâne, cu profilul degrade-urilor de sus și de jos (`wm.GRAD`), ca zona subtitrărilor să rămână curată.
7. **Montajul**: `assemble.sh rest` pune cadrele neschimbate (cu marcaj) în `/home/claude/reels/amorsare_filtru/frames_base/`, `assemble.sh bl` pe cele cu pompa din Blender. `render_seg.py <start> <end>` trece compozitorul reelului (subtitrări, titluri, ștampile, card de final) peste un interval de cadre; bucățile care nu depind de Blender (174–2180 și 3039–4348) se fac cât încă randează Blender. `finish_bl.sh` lipește cele patru segmente, pune sunetul neschimbat al variantei 2 și codează o singură dată fișierul livrat. Fișierul livrat pe 15.11.2026 e făcut cu `CRF=18 MAXRATE=4.8M ./finish_bl.sh Reel_Amorsare_Filtru_Motorina_Blender` (74,6 MB, 3,93 Mbps video, cât varianta 2; cu valorile implicite, crf 20, ieșea 62,6 MB).

## Refacere

```
# 1. Blender (bpy 5.0.1 de pe PyPI, vezi ../README.md): în dosarul cu scene.py, reel_scene.py, src/
venv/bin/python reel_scene.py boxes W && venv/bin/python reel_scene.py boxes C
./qA1.sh        # prim-planul: placa, rotirea tachetului, bucla CROSS (~55 min pe 4 nuclee)
./qA2.sh        # bucla HOT din prim-plan, pana, planul larg (~45 min); fiecare coadă stă sub limita de 2 ore a unei comenzi în fundal
# 2. pagina: sursa animației + patch_reel.py + node build.mjs main; apoi
python3 director.py
node ovrender.cjs ovl director.json ov/ovl 0 1 && node ovrender.cjs add director.json ov/add 0 1
# 3. marcajul: python3 wm_pattern.py; lista de măști (mask2_list.json) + node amask.cjs uframes.json mask2_list.json mask2 0 1
# 4. ./assemble.sh rest && python3 render_seg.py 174 2180 && python3 render_seg.py 3039 4348      (cât randează Blender)
# 5. ./assemble.sh bl && python3 render_seg.py 0 174 && python3 render_seg.py 2180 3039 && CRF=18 MAXRATE=4.8M ./finish_bl.sh Reel_Amorsare_Filtru_Motorina_Blender
```

## De știut

- `page.addInitScript` nu rulează cu `setContent`; variabilele de pornire (`__ALPHA`, `__PASS`) intră ca `<script>` la începutul documentului (`rlib.cjs`).
- Procesele Chromium au prioritate peste Blender (nice −8): cât rulează trecerile paginii, randarea merge la jumătate de viteză.
- Cilindrul regulatorului de debit e `steelDark` (metal), deci iese gri deschis sub lumina cheie, ca în proba aprobată; în pagina three.js părea negru.
- Rola are un reper (`markDark`): în stările cu ungere (`FUEL`, `AIR`) se rostogolește două ture pe buclă, în rest stă blocată.
- Tăria marcajului din fundal: `WM_W` / `WM_Y` în `wm.py` (implicit alb 4% + galben 5,2%, cât în seria turbinelor după „Să fie mai discret”). Fără marcaj: `WM=0 ./assemble.sh rest` și `WM=0 ./assemble.sh bl`.
- Bara neagră de un cadru de la cadrul 120 al hook-ului e efectul de „glitch” al titlului din compozitorul reelului; e și în varianta 2.
- `qa_sheet.py <video> <out.jpg> <cadre,cu,virgulă>` face planșe de verificare din fișierul codat.

## Ce e salvat

- Aici: uneltele (scripturile de mai sus, `anim/`, `wm/`).
- `work/` (arhive tar fără compresie, făcute cu `save_work.sh` / `pack.py`): randările Blender (`bl_out_reel_01..03.tar`, se desfac în dosarul cu `reel_scene.py` și dau `out_reel/`: plăci, R1, R2, cele ~2 ore de calcul), trecerile paginii (`ov_ovl_01..03.tar` și `ov_add_01.tar`, se desfac în `ov/`) și măștile marcajului (`mask2_01.tar`, se desface lângă `wmapply.py`). Cadrele compuse (`frames_bl`, `frames_wm`) nu sunt salvate: se refac din acestea în ~5 minute (`assemble.sh`). Cadrele neschimbate ale variantei 2 sunt în `../../amorsare-filtru/reel/work/frames_base_parts/`.
- Pentru panoul CP4 înapoi în prim-plan: în `director.py` rândul `R['panel']` devine `1.0 if not hook else 0.0`, apoi trecerea `ovl` pentru cadrele 2658–3038 (~4 min), `assemble.sh bl`, `render_seg.py 2180 3039` și `finish_bl.sh`.
- Livrat: `/mnt/project-files/animatii/TurboDoctor_Reel_Amorsare_Filtru_Motorina_Blender.mp4` și `_coperta.jpg`. Textul postării e cel al variantei 2 (`TurboDoctor_Reel_Amorsare_Filtru_Motorina_text_postare.txt`).
