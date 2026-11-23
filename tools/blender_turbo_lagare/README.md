# Turbina în secțiune 3D: lagăre flotante și lagăr fix (semi-flotant) · Blender (22.11.2026, exterior refăcut 23.11.2026)

Două animații 3D făcute în Blender pentru explicațiile video Turbo Doctor, aceeași turbină de autoturism diesel (cu geometrie variabilă), în secțiune, cu cele două sisteme de lagăre:

- **A · lagăre flotante (hidrodinamice):** două bucșe de bronz care se rotesc cam la jumătate din turația axului, fiecare între două filme de ulei (spre carcasă și spre ax), siguranțe (inele elastice) de o parte și de alta, lagăr axial separat.
- **B · lagăr fix (semi-flotant):** un singur lagăr de bronz, dintr-o bucată, ținut pe loc de un știft din carcasă; filmul interior (ax – lagăr) e hidrodinamic, filmul exterior doar amortizează; același lagăr axial separat.

Carcasele, roțile, axul, lagărul axial, etanșările, ecranul termic și paletele geometriei variabile sunt aceleași în A și B, ca diferența dintre lagăre să se vadă direct.

## Exteriorul (v2, 23.11.2026): după un Garrett 753420 real

Exteriorul e refăcut după poze din toate unghiurile cu turbina **Garrett 753420-5006S** (GTA1544V / GT1544V, VNT, 1.6 HDi / TDCi 110 CP): poze de produs Garrett original (dencodiesel.com) și o turbină recondiționată (turbobaltic.com). Interiorul (lagărele, axul, roțile, uleiul, secțiunile transversale) a rămas cel aprobat.

- **Orientarea reală** (verificată pe toate pozele): cu intrarea de ulei sus, racordul de ieșire al compresorului pleacă de sus din melc și ambele flanșe, ieșirea de aer și intrarea de gaze, privesc spre aceeași parte (spre cameră); actuatorul pneumatic stă pe partea opusă, jos, cu tija spre maneta geometriei variabile.
- **Carcasa compresorului** (aluminiu turnat): gura de admisie e o țeavă dreaptă prelucrată, cu 6 nervuri spre capac; melcul e mai mare (A/R 0,33 turnat pe capacul real), are guler de prindere care urmează melcul, urechi cu șuruburi și racord de ieșire cu flanșă cu 2 urechi pe direcția axului.
- **Carcasa turbinei** (fontă, gri închis): e mai masivă, cu fața din spate lată și prelucrată, prinsă cu șuruburi a căror șaibă ține flanșa carcasei centrale. Are flanșa de admisie cu 4 găuri jos, spre cameră, ieșirea scurtă cu guler, urechea de lângă ieșire și talpa pentru suportul actuatorului.
- **Uleiul intră printr-un banjo** (ca la 1.6 HDi): șurub găurit cu găuri transversale, două șaibe de cupru, ochiul banjo și conducta de ulei; în secțiune uleiul se vede pe tot drumul: conductă → ochiul banjo → găurile transversale → prin șurub → galerie.
- **Carcasa centrală** e neagră la exterior (ca la piesa reală); în interior culorile au rămas cele de dinainte.
- **Actuatorul** (cutie cu membrană, scut termic, suport, tijă cu contrapiulițe și furcă pe manetă) apare doar în cadrul exterior; la deschiderea secțiunii pleacă odată cu jumătățile din față, ca să nu încurce secțiunea.
- **Diferența rămasă față de piesa reală:** corpul lagărelor (partea neagră dintre carcase) e cam de două ori mai lung decât la 753420, pentru că interiorul are lagărele depărtate, ca filmele de ulei să se vadă bine. Scurtarea lui la cota reală ar schimba secțiunea și ar cere refacerea tuturor randărilor.

## Fișiere

| Fișier | Ce e |
|---|---|
| `animatii/TurboDoctor_Turbina_Lagare_Flotante_9x16.mp4` | A, vertical 1080×1920, 51 s, cu titlu, etichete, texte și cartonul Turbo Doctor |
| `animatii/TurboDoctor_Turbina_Lagare_Flotante_16x9.mp4` | A, orizontal 1920×1080 |
| `animatii/TurboDoctor_Turbina_Lagar_Fix_9x16.mp4` | B, vertical |
| `animatii/TurboDoctor_Turbina_Lagar_Fix_16x9.mp4` | B, orizontal |
| `animatii/*_curat_*.mp4` | aceleași filme fără titlu, etichete, texte, săgeți și carton (rămân marcajul pe fundal și „MODEL 3D RECONSTRUIT · JOCURI MĂRITE”), pentru montaj cu vocea |
| `animatii/stills/*.jpg` | cadre statice fără texte, în ambele formate: exterior, secțiune, ulei, lagăr, secțiune transversală (și știftul la B) |
| `turbo.py` | modelul (Python pentru Blender 5.0, `bpy`), materialele, lumina, camerele, randarea pe straturi |
| `comp/comp.py`, `comp/fk.py`, `comp/render_all.sh` | montajul (skia-python + numpy + OpenCV): straturile Blender, uleiul colorat, curgerile, etichetele, textele; `render_all.sh` face cele 8 filme și imaginile |
| `out/turbo.blend` | scena Blender (Blender 5.0+, Cycles), colecții pe piese și variante |
| `layers.tar` | toate straturile randate (PNG pe 8 biți) + `info.json`; se despachetează în acest dosar (`tar xf layers.tar`) și montajul se reface fără Blender |
| `pack_layers.py` | face `layers.tar` din `out/*.png` |

## Cum e făcut

Modelul e construit din profile și booleene (solverul MANIFOLD), 1 unitate = 1 mm, axul pe X (compresorul la −X), secțiunea în planul y = 0 (rămâne jumătatea din spate). Roțile au palete generate din linii meridionale (butuc și vârf), cu înfășurare și grosime variabilă: compresorul 6 + 6 palete (principale și intermediare), turbina 10 palete, cu decupaje în discul din spate. Carcasele de compresor și de turbină au melcul generat ca tub cu secțiune variabilă pe spirală; racordurile tangențiale (ieșirea de aer, intrarea de gaze) sunt în jumătatea din față, spre cameră, ca la piesa reală, și dispar la deschiderea secțiunii. Jocurile sunt mărite: filmul interior 0,4 mm, filmul exterior 0,8 mm (A) / 0,5 mm (B), ca uleiul să se vadă.

Randarea (Cycles pe procesor, fără placă video) e pe straturi, ca la injectorul CRI2: planșa întreagă (2160×2160), planșa carcasei centrale la densitate dublă, planșa lagărelor la densitate cvadruplă (aceeași cameră, decupaje exacte, deci zoom fără pierdere), jumătățile din față pentru deschiderea secțiunii, uleiul pe zone (alb, colorat la montaj), buclele de rotație ale roților (compresor 10 cadre × 6°, turbină 6 cadre × 6°, cu motion blur) și vederile transversale prin lagăr (axul și bucșa se rotesc în montaj).

```
uv venv -p python3.11 venv && uv pip install -p venv/bin/python bpy==5.0.1 numpy==1.26.4
venv/bin/python turbo.py build          # out/turbo.blend (~6 s)
venv/bin/python turbo.py info           # out/info.json, out/crops.json (proiecții, decupaje, ancore)
venv/bin/python turbo.py queue          # toate straturile (~2 h pe 2 nuclee, fără placă video); sare peste ce există
# (sau: tar xf layers.tar  -> straturile gata randate, fără Blender)
venv/bin/python turbo.py prev main 1 "" shared,chra_A,int_A,rotor,rotor_c,rotor_t,rotor_cut 40 16 proba.png   # probă rapidă
venv/bin/python turbo.py look 0.2,0.65,0.73 -1,0,0 300 1000 48 unghi.png   # exteriorul din orice direcție (aici ca în poza Garrett)
cd comp
FMT=V VAR=A python3 comp.py --png 9,16,26,36      # cadre de probă (V = 9:16, H = 16:9; A = flotante, B = fix)
FMT=H VAR=B python3 comp.py --out B_16x9.mp4      # filmul (51 s)
CLEAN=1 FMT=V VAR=A python3 comp.py --out A_curat.mp4
```

Pe un calculator cu placă video, `out/turbo.blend` se deschide direct în Blender 5.0+ (Cycles → GPU Compute) și se poate randa orice cameră: `cam_main` (secțiunea), `cam_trA` (secțiune transversală prin lagărul dinspre turbină), `cam_trP` (prin mijlocul lagărului fix, cu știftul), `cam_hero` (exterior). Colecțiile: `shared` (carcase, palete, piese comune), `chra_A` / `chra_B` (carcasa centrală), `int_A` / `int_B` (lagărele), `rotor*` (axul și roțile), `front` (jumătățile din față), `oil*` (uleiul pe zone), `tr*` (vederile transversale).

## Cronologia (51 s, la fel în ambele formate)

0–3,2 exterior (753420) · 3,2–5 jumătatea din față și actuatorul se ridică (secțiunea) · 5–11,6 roțile se rotesc, aer (albastru) și gaze (portocaliu), etichetele pieselor · 11,6–13,4 zoom pe carcasa centrală · 13,4–21 uleiul (chihlimbar) umple conducta, banjo-ul, galeria, alimentările, filmele și lagărul axial, apoi se scurge spre retur · 21–30,8 prim-plan pe lagăr: filmele de ulei, inelele de rotație (A: bucșa la ~½ din turația axului; B: doar axul) · 30,8–41 secțiune transversală prin lagăr în cerc (A: axul și bucșa se rotesc, particule în filme; B: lagărul stă, apoi secțiunea prin știft) · 41–42,6 înapoi la planul larg · 42,8–47,5 „Pe scurt” · 47,6– cartonul Turbo Doctor.

## Surse și ce e reconstruit

Garrett, „Turbocharger Bearing Systems”: bucșele complet flotante se rotesc cam la jumătate din turația axului, cu două filme hidrodinamice (exterior carcasă–bucșă, interior bucșă–ax); majoritatea turbinelor mici, de turație mare, de autoturism au un lagăr semi-flotant dintr-o bucată care nu se rotește, la care filmul exterior lucrează mai ales ca film de amortizare și doar filmul interior e hidrodinamic; lagărul axial poate fi separat sau integrat. Cummins Turbo Technologies (lagăre semi-flotante dintr-o bucată, lagăr axial separat cu pante). Brevetul US 11415021 (știft anti-rotație fixat în carcasă). DieselNet, secțiunea BorgWarner (lagăr axial + două lagăre complet flotante; etanșare cu segmenți).

Exteriorul: după pozele Garrett 753420-5006S (dencodiesel.com, produs Garrett original) și 753420-5006S recondiționată (turbobaltic.com); cotele sunt estimate din poze, nu dintr-un desen Garrett.

Reconstruit, de confirmat cu poze din atelier: proporțiile pieselor interioare, știftul intrat de jos (din cavitatea de retur), găurile bucșelor la 45° și cele ale lagărului fix sus/jos, jocurile mărite, paletele geometriei variabile (11), forma exactă a suportului și a scutului termic de la actuator, traseul conductei de ulei și tubul de retur.
