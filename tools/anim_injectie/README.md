# Reel animat „Un injector injectează de 3 ori” (10.11.2026)

Reel explicativ făcut dintr-o animație 3D (Three.js), nu dintr-o filmare: preinjecție → injecție principală → postinjecție și
regenerarea DPF, cu narator. Animația este o funcție pură de timp, legată de cuvintele din voce, așa că se randează cadru cu cadru
direct în `frames_base/` și trece apoi prin compozitorul obișnuit (hook, bară de etape, carduri de capitol, subtitrări, card de final).

## Fișiere

| Fișier | Rol |
|---|---|
| `index_src.html` | sursa paginii interactive publicate (artifact „Injecție diesel în 3D”): modelul injectorului, cilindrul, particulele |
| `vo_script.json` | textul naratorului, pe rânduri (`{afișat|rostit}` pentru cifre și cuvinte străine) |
| `make_vo.py` | `piper` = narator provizoriu (Piper RO); `take <t1> [t2]` = vocea reală (ElevenLabs): găsește fiecare rând în fiecare variantă (ASR + aliniere pe caractere), taie în punctul cel mai liniștit al pauzei și ia rândul mai clar. Scrie `vo/vo_track.wav`, `vo/timeline.json` (format narator), `vo/cues.json` |
| `build_reel.py` | face `reel.html` (1080×1920) din `index_src.html` + `reel_tail.js` + `vo/cues.json` |
| `reel_tail.js` | regia: segmente timp → ciclul motorului, camera, etichete, banda „momentul injecției”, postinjecția, linia de evacuare (DOC + DPF), temperatura |
| `stills.js` | cadre de probă: `node stills.js st/x 13.4,62.7 4 "0.6&aa=0&guides=1"` (`guides=1` desenează zona subtitrărilor și a butoanelor din aplicații) |
| `render_frames.js` | randarea: `node render_frames.js <reel>/frames_base 0 2453` (JPEG q92, reia de unde a rămas) |
| `probe.js` + `make_bed.py` | sunetul: starea animației la 200 Hz → șuierul pulverizării, clicul injectorului, arderea, bătaia, arderea din catalizator (`audio/bed_fx.wav`, intră prin `beds` din `out/v2.json`) |
| `tweak_sfx.py`, `finish_local.sh` | pașii din `finish.sh`, cu lovitura de la începutul hook-ului redusă la jumătate (cade pe primul cuvânt al naratorului) |
| `../../pipeline/examples/reel_injectie_3_timpi_animatie_narator.js` | `reel.js` al acestui reel |

## Pașii

1. Folder de lucru cu `fonts/` (din `assets/fonts`) și `three.min.js` (three@0.128.0, `build/three.min.js` din npm) lângă aceste fișiere.
2. Vocea. Provizoriu: `python3 make_vo.py piper`. Vocea lui Sabin: ElevenLabs, modelul `eleven_v4`, vocea „Sabin”, tot textul într-o singură
   generare (2 variante ≈ 2.300 de credite), scris normal („diesel”, „2.000 de bari”, „600 de grade”). Fișierele vin prin `fetch-sources`
   (`nume=URL`, apar pe `sources` ca `<nume>.mp4`, cu MP3 înăuntru), apoi `VO_PICK='{"1":1,"3":1}' python3 make_vo.py take t1.mp3 t2.mp3`
   (`VO_PICK` = rândurile luate din a doua variantă, alese după ce aude ASR-ul pe fiecare rând). → voce + momente pe cuvinte. Toată regia din `reel_tail.js` se leagă de aceste momente (`W(linie, 'cuvânt')`),
   deci **o voce nouă înseamnă randarea animației din nou**.
3. `python3 build_reel.py && node --check reel_check.js`, apoi cadre de probă cu `stills.js` (cu `guides=1`).
4. Folderul reel-ului: `new_reel.sh <slug> <un mp4 negru de durata poveștii>`, apoi `vo/vo_track.wav` → `audio/vo_track.wav`,
   `vo/timeline.json` → `out/timeline.json`, `out/v2.json` = `{"narrator": true, "orig_gain": 0, "music_gain": 0.5, "beds": [...]}`,
   `python3 retime.py`, `out/frames_meta.json` = `{"n_out": round(total × 30)}`. **Nu** se rulează `extract_frames.py`.
5. `node render_frames.js <reel>/frames_base 0 <ultimul cadru al poveștii>` în fundal (≈ 0,7 s/cadru, ~28 min la 82 s).
6. `node probe.js && python3 make_bed.py <reel>/audio/bed_fx.wav "<ferestre în care camera nu e pe cilindru>"`.
7. `reel.js` + `python3 render.py --test …` pe cadrele deja randate, apoi `bash finish_local.sh <Nume_Fisier>`.

## Reguli de așezare în cadru (verificate pe acest reel)

- subtitrările ocupă y 1290–1530: ce contează în animație stă deasupra (cadrul `inj` are marginea de jos la 1280);
- banda „momentul injecției” stă la y 300–506, sub bara de etape; citirea temperaturii îi ia locul în scenele cu filtrul;
- rândul de chip-uri din compozitor: y ≈ 588; etichetele din dreapta se opresc la 112 px de margine sub y 800 (butoanele aplicațiilor);
- fundal fix (`bgFix` pe toată povestea), ca desenul să rămână clar; zguduitura de la „motorul bate” este făcută în animație (camera).
