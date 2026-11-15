# Reel animat „Diesel cu sunet de blow-off? Nu e tuning. Turbina se distruge” (15.11.2026, varianta 2)

Reel din animația 3D „Supapa blow-off: benzină vs. diesel” (artifact; sursa filmului în /mnt/project-files/animatii/sursa/blow-off/),
cu vocea „Sabin” din ElevenLabs. Cerut de Sabin pe 15.11: hook „dacă ai diesel și auzi sunetul ăsta, ca un suflat de blow-off, nu e tuning,
e semnul că turbina se va distruge”, apoi traseul.

**Varianta 2** (tot 15.11, după observațiile lui Sabin la varianta 1):
1. la început, motoarele pe benzină vin din fabrică cu **supapă de recirculare (diverter)**: ia aerul de după compresor și îl duce înapoi, înainte de compresor,
   așa că aerul deja măsurat rămâne captiv după **senzorul MAF** și motorul funcționează corect;
2. **blow-off-ul** se pune în special pe mașinile tunate și protejează turbina când se accelerează prea mult sau când pe admisie se adună presiune de care motorul nu mai are nevoie;
3. pe diesel se explică **doar de unde vine sunetul** (supraturare → pompaj), fără geometria variabilă („nu te lega de geometria variabilă”);
4. **cauzele abia la final**: geometrie variabilă blocată, problemă pe acționare (actuator), alte defecte din cauza cărora presiunea de pe admisie ajunge prea mare;
5. sunetul din hook este o **înregistrare reală** de blow-off (varianta 1 avea un efect generat, respins: „Ce ai luat tu nu e ok”).

Varianta 1 (16 rânduri, 132 s, geometria variabilă explicată pe larg) este în istoricul git al acestui folder (commit-urile de dinainte de varianta 2).

Rezultat: `animatii/TurboDoctor_Reel_Blow_Off_Diesel_Pompaj.mp4` (148,2 s = poveste 140,7 s + card de final 7,5 s), `_coperta.jpg` (cadrul de la 9,6 s) și `_text_postare.txt`.
**Stare: varianta 2 aprobată de Sabin pe 15.11.2026 („Programează-l pe toate platformele pe brandul Turbo Doctor, acum…”) și programată în aceeași zi în Metricool,
pe cele patru rețele ale brandului turbodoctoroficial, toate la 14:42** („acum” = aceeași oră pe toate rețelele, la ~10 minute de la programare):
YouTube (Short), Facebook (POST cu titlu, fiindcă are peste 90 s), Instagram (Reel), TikTok. Etichetă AI pe Instagram și TikTok (voce generată), nu pe YouTube;
fără bifele de conținut comercial. S-a urcat masterul din `finish.sh`, fără recomprimare, cu `publish_media_batch.sh` (commit normal pe `media`, ca să nu dispară
fișierele reelurilor programate de alte fire în aceeași zi); fișierul descărcat de pe linkul raw are același sha256 ca masterul.

Ce rămâne ca regulă din observațiile lui Sabin la acest reel:
- când reelul se sprijină pe un sunet („dacă auzi sunetul ăsta”), sunetul este o **înregistrare reală**, nu un efect generat; doar domeniu public sau CC0, cu sursa și licența spuse lui;
- se explică **fenomenul** („din ce cauză se aude zgomotul”), iar **cauzele posibile vin la final**, pe scurt, fără să fie legată toată povestea de una singură dintre ele;
- comparația cu benzina începe cu ce au mașinile **din fabrică** (supapa de recirculare, aerul captiv după MAF) și abia apoi cu ce se pune la tuning (blow-off).

## Diferența față de `anim_egr` / amorsare: regie pe cuvinte, nu re-temporizare

La EGR și la amorsare animația avea cronologia ei (U), iar vocea era legată de ea printr-o hartă U(t). Aici povestea reelului are altă ordine
decât filmul, așa că animația este **rescrisă direct în timpul vocii**:
`build_reel.py` citește `vo/cues.json` și calculează ancorele `K` (fiecare = începutul unui cuvânt, ex. `K.P_DV = W(3,'supapă')`),
iar `r_timeline.js`, `r_cam.js`, `r_labels.js`, `r_ui.js`, `r_apply.js` leagă de ele starea motorului, camera, etichetele și HUD-ul.
Cadrul i din reel = `__seek(i/30)`. **O voce nouă înseamnă ancore noi și randarea animației din nou.**
`W(i, cuvânt, occ)` ignoră diacriticele și majusculele („Supapa” = „supapă”), deci a doua apariție se cere cu `occ=1`.

| Fișier | Rol |
|---|---|
| `base/turbo.html`, `base/b_parts.js`, `base/b_vgt.js`, `base/b_streams.js` | scena filmului (identice cu sursa din /mnt/project-files/animatii/sursa/blow-off/) |
| `vo_script.json` | textul vocii, 15 rânduri (`gap` = pauza dinaintea rândului; rândul 1 are 1,9 s: acolo stă sunetul din hook) |
| `make_vo.py`, `vo_qc.py`, `asr2.py`, `run_iso.sh` | vocea: rând cu rând, măsurată și verificată cu două recunoașteri (ca la amorsare) |
| `make_hook_sfx.py` | sunetul din hook: taie înregistrarea, o curăță (trece-sus, înalte, intrare lină), o pune în pauza dintre rândul 0 și rândul 1 și scrie anvelopa ei (`vo/hook_sfx.json`), pe care animația o urmează |
| `build_reel.py` | ancorele `K` + `blow-off-reel.html` (modul `vo` pornit din construcție) + `vo/anchors.json`; fără `vo/`, citește `map/cues.json` și `map/hook_sfx.json` |
| `r_parts.js` | piesele noi din varianta 2: senzorul MAF (tub + senzor cu film cald) în fața compresorului și supapa de recirculare (solenoid, taler, arc, racord lateral) pe conducta de aspirație, cu furtunul ei de la conducta de presiune |
| `r_streams.js`, `r_s1.js` | aerul recirculat (bucla verde-albăstruie: conducta de presiune → furtun → supapă → înapoi în fața compresorului) și aerul proaspăt care se oprește cât bucla e deschisă |
| `r_timeline.js` | fazele H (hook) · P1 (benzină, supapa de recirculare, rândurile 2–4) · P2 (benzină tunată, blow-off, rândul 5) · N (diesel, rândurile 6–11) · S (ecran împărțit, rândul 12) · W (cauzele și încheierea, rândurile 13–14); `petrolDV()`, `petrolEvent()`, `surge()`, `hookState()`, piste pe cadre-cheie |
| `r_cam.js` | cadrele (`SHOTS`) și cheile camerei (`CAMKEYS`), toate pe ancore; `SPLIT_A` / `SPLIT_B` pentru ecranul împărțit |
| `r_labels.js`, `r_ui.js`, `r_apply.js` | etichetele pe cuvinte, HUD-ul (turație turbo, presiune turbo, în faza P1 și „Aer măsurat · MAF”; „Încetinitor”), aplicarea stării pe scenă (supapa de recirculare, elementul MAF, detaliul mărit al geometriei variabile la cauze) |
| `rlib.cjs`, `shot.cjs`, `sheet.py` | cadre de probă: `node shot.cjs 3,4.5,60 [dpr] [dir]` → `<dir>/s_<t>.png`; `python3 sheet.py 3,4.5,60 out.png [dir] [coloane]` |
| `vframes.cjs`, `vrender.sh` | randarea: `N=2 OUT=<reel>/frames_base NF=<cadre> ./vrender.sh` (procese intercalate, cu reluare; sare peste cadrele existente) |
| `mix_qc.py` | verificarea mixului final: fiecare rând tăiat din `mix_final.wav`, recunoscut cu Parakeet și Whisper |
| `map/` | copia momentelor pe cuvinte (`cues.json`, `timeline.json`), a anvelopei sunetului (`hook_sfx.json`), a ancorelor (`anchors.json`) și a variantelor alese (`picks.json`) cu care a fost randat reelul |
| `../../pipeline/examples/reel_blow_off_diesel_pompaj_animatie.js` | `reel.js` al acestui reel |
| `../../sources/fs_extract.py`, `../../sources/web_extract.py` | folosite de `fetch-sources` la căutarea sunetului: reduc o pagină Freesound (nume `fsq_…`) sau orice pagină de catalog (nume `webq_…`) la lista sunetelor, cu licența fiecăruia |

Lângă aceste fișiere trebuie `three/` (pachetul npm three@0.128.0, dezarhivat: `three/package/build/three.min.js`) și `fonts/`
(@fontsource/barlow și @fontsource/barlow-condensed 5.3.0, dezarhivate ca `fontsource-barlow-5.3.0/package/…`); nu sunt în repo.

## Pașii

1. **Vocea**: `eleven_v4`, vocea „Sabin”, fiecare rând generat separat, 2 variante, cu `[calm] [matter of fact]` în față (hook-ul: `[serious] [matter of fact] [conversational tone]`).
   Fișierele vin prin `fetch-sources` ca `…L<NN><x>.mp4`, apoi `VO_PICK='{…}' ./run_iso.sh make_vo.py lines <dir>` → `vo/vo_track.wav`, `vo/timeline.json`, `vo/cues.json`.
   Varianta 2: rândurile 0–2 și 8–12 sunt cele din varianta 1 (aceleași fișiere: hook-ul, ridicarea piciorului, pompajul, uzura, ecranul împărțit), iar 3–7, 13 și 14 sunt generate din nou; povestea are 140,7 s. Scripturile rulează cu `run_iso.sh` (Python `-I`), fiindcă audio descărcat este dată străină.
2. **Sunetul din hook** („…și auzi sunetul ăsta”): o înregistrare reală, **Freesound 659544 „Turbo Spooling and Blow Off.WAV” de EwanPenman11, Creative Commons 0**
   (https://freesound.org/people/EwanPenman11/sounds/659544/; o mașină care trece, cu fâlfâit de turbină și blow-off). Regula pentru orice material luat de pe net: doar domeniu public sau CC0.
   Căutarea: Freesound cu filtrul CC0 nu are nimic la „blow off valve”, „blowoff”, „bov turbo”, „dump valve”, „turbo flutter”, „wastegate”, „diverter valve”; înregistrarea a ieșit la „turbo”.
   Pe Wikimedia Commons există un blow-off HKS pe Peugeot 406, dar e CC BY (nefolosit); Pixabay nu lasă accesul automat.
   ```
   ./run_iso.sh make_hook_sfx.py <fsr_659544.mp3> 0.40 1.80 --hp 800 --shelf 4000 5 --fadein 0.5 --pre -7 --tail 1.27 5 --t0off 0.25 \
       --event 0.925 --flutter 0.925 1.30 --acc 0.94,1.00,1.10,1.20 --psh 1.34
   ```
   → `vo/hook_bed.wav` (1,4 s, intră la 3,25 s, se termină cu 0,25 s înainte de rândul 1) și `vo/hook_sfx.json`. Ce se aude: mașina care se apropie (ținută cu 7 dB mai încet),
   fâlfâitul (7 pulsuri la 50 ms, începe la 0,925 s din înregistrare = `tb`, momentul ridicării piciorului în animație), apoi „pșș”-ul (1,3–1,65 s, ridicat cu 5 dB).
   Nu pot asculta sunetul: momentele sunt citite din spectrogramă și din nivelurile pe benzi. Sunetul stă **doar în pauza vocii**, niciodată sub ea (Sabin a respins pe 14.11 zgomotul de sub voce din hook-ul de la amorsare).
   Modul vechi (efect generat, `--shape`, `--comp`, `--lead`) a rămas în script.
3. `python3 build_reel.py`, apoi cadre de probă pe fiecare fază (`shot.cjs` + `sheet.py`).
4. Folderul reel-ului ca la `anim_injectie` (pasul 4): `new_reel.sh <slug> <mp4 negru de durata poveștii, cu o pistă audio mută>`, vocea și cronologia copiate,
   `audio/hook_bed.wav`, `out/v2.json` = `{"narrator": true, "orig_gain": 0, "music": false, "sfx": false, "beds": [{"wav": "audio/hook_bed.wav", "t": 3.25, "gain": 1.3, "duck": 0.6}]}`,
   `python3 retime.py`, `out/frames_meta.json` = `{"n_out": round(total × 30)}`.
   Nivelul sunetului (`gain` 1.3) e pus pe măsurători, nu după ureche: în mixul final sunetul ajunge la ≈ −15 LUFS (maxim momentan), cu vocea la ≈ −14, iar tot fișierul are −14,1 LUFS integrat.
5. Randarea: `N=2 OUT=<reel>/frames_base NF=<int(story_end × 30) + 1> ./vrender.sh` (aici 4.222 de cadre; 540×960 la DPR 2, JPEG q92). Viteza depinde de mașină: randarea e software (SwiftShader) și folosește toate nucleele.
   Pe o mașină cu 4 nuclee iese cam 1 cadru/s cu 1 sau 2 procese (70 de minute), iar cu 4 procese se sufocă (0,3 cadre/s și primul cadru trece de limita de timp a capturii); varianta 1 a mers cu 4 procese la 0,6 s/cadru pe o mașină mai mare.
   Compozitorul folosește cadrele doar până la sfârșitul poveștii (cardul de final are fundalul lui). Dacă se schimbă doar sunetul din hook, se refac doar cadrele hook-ului (t < `K.T_P`): se șterg și se rulează din nou `vrender.sh`.
6. `reel.js`, `python3 render.py --prep --test …`, `bash finish.sh <slug> <Nume_Fisier>`, `./run_iso.sh mix_qc.py <reel>/audio/mix_final.wav`.

## Așezarea în cadru

- Modul `vo`: scena utilă între 13% și 66% din înălțime (în hook de la 30%, ca titlurile `boom` să aibă loc sus); restul scenei continuă sub subtitrări, ca la reelul EGR.
- HUD dreapta sus, cu fond închis: „Turație turbo”, „Presiune turbo” și, cât se vorbește despre supapa de recirculare, „Aer măsurat · MAF” (310 kg/h → 10 kg/h cât clapeta e închisă); pastila „Încetinitor” apare la pompaj (nu și în hook).
- Hook: titluri `boom` la y 300–612, onomatopeea sunetului („TU” × 4 pe pulsurile fâlfâitului, apoi „PȘȘȘ”, pe momentele din `hook_sfx.json`) la y ≈ 1160, sub conducta de admisie; subtitrările sunt ascunse până la rândul 2.
- Pulsurile roșii de aer întors din hook urmează anvelopa sunetului (`K.HE`; în fereastra `K.HFL` pâlpâie la 10 Hz, ca fâlfâitul), apoi trec în încetinitor (1,5 Hz); în poveste pompajul merge la 1,2 Hz (`K.HZ`).
- Supapa de recirculare: bucla aerului recirculat e verde-albăstruie; partea din spatele planului de secțiune (conducta de presiune de sus) se vede „prin perete” (nor de particule fără test de adâncime).
- Ecranul împărțit (rândul 12): două cadre diferite, „Benzină · blow-off / Normal” și „Diesel · pompaj / Defect”; jumătatea despre care nu se vorbește este întunecată.
- Cauzele (rândul 13): vederea mărită a geometriei variabile cu „Geometrie variabilă blocată” și „Actuator · problemă pe acționare”, apoi „Alte defecte · presiune prea mare pe admisie”.
- Ștampile la y 1150; fără bară de etape; `bgFix` pe toată povestea.

## Conținut

Pe benzină, din fabrică: la ridicarea piciorului clapeta se închide, aerul comprimat nu mai are unde să se ducă, supapa de recirculare (diverter) îl ia de după compresor și îl duce înapoi,
înainte de compresor; aerul deja măsurat rămâne captiv după senzorul MAF, deci amestecul rămâne corect. Pe mașinile tunate se pune blow-off: aerul în plus e eliberat în atmosferă (de aici sunetul).
Pe diesel: clapeta rămâne deschisă, aerul trece prin motor, din fabrică nu există nici supapă de recirculare, nici blow-off. Sunetul de „blow-off” pe diesel: turbina supraturată trimite pe admisie
mai mult aer și mai multă presiune decât cere motorul → la ridicarea piciorului aerul se întoarce prin roata compresorului, în pulsuri (pompaj) → tensiune pe paletele compresorului,
lagărul axial lovit înainte-înapoi → joc pe ax → paletele ating carcasa. Cauze (la final): geometrie variabilă blocată, actuator, alte defecte care ridică presiunea de pe admisie.
Cifrele din HUD (rpm, bari, kg/h) sunt ilustrative, nu dintr-o fișă de producător.
