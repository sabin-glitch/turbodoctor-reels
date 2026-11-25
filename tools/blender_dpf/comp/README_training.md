# Filmul de training „Filtrul de particule (DPF)” · 24.11.2026

Film explicativ pentru colegii din Turbo Doctor, făcut pe modelul Blender al filtrului de particule cu catalizator de oxidare (`sursa/dpf-doc-blender/`), cu voce generată (nu vocea lui Sabin).

- 59 de fraze, 10 capitole, 7 min 39 s: ce e în carcasă → rolul DOC-ului → cum filtrează → cum se încarcă → senzorii → regenerarea → cenușa → erorile de încărcare → erorile de eficiență → ordinea de lucru.
- Formate: 9:16 (1080×1920) și 16:9 (1920×1080), 30 de cadre pe secundă, din aceleași straturi Blender.
- Vocea: ElevenLabs, „Claudiu Mihai Ciobanu – Professional Romanian” (`voice_id HPdbgrGubKiBta6Pq21b`), `eleven_v4`, o variantă pe frază, `[calm] [matter of fact]` în față (prima frază: `[serious] [matter of fact] [conversational tone]`). Toate frazele sunt verificate cu transcriere (Scribe): rostite corect.

## Fișiere

| Fișier | Ce e |
|---|---|
| `script.py` | cele 59 de fraze (textul rostit și textul scris), capitolele |
| `eng.py` | motorul: straturile Blender, efectele din măști (funingine, cenușă, strălucire, evidențieri), gazele, stările simulate (fisuri, scăpări) |
| `film.py` | cadrele (câte unul pe frază), cronologia după durata reală a frazelor, texte, etichete, panouri, randarea pe segmente |
| `fk.py` | trusa de desen (din `tools/blender_turbo_lagare/comp/fk.py`) |
| `vo/gens.json` | id-urile generărilor ElevenLabs, ale pachetelor și ale pistei finale |
| `vo/meas.json`, `vo/words.json` | duratele măsurate ale frazelor (`sp` = cât durează vorbirea), momentul fiecărui cuvânt (din transcriere; frazele 52–58 lipsesc, acolo se folosesc fracții din frază) |
| `dpf.py` (în dosarul de sus) | modelul din `sursa/dpf-doc-blender/dpf.py`, cu stratul `TC` adăugat (vezi mai jos) |

Nesalvate aici, pentru că se refac ușor: `vo/cues.json` (`python3 film.py --cues vo/cues.json`), `pf.sh` / `sheet.py` / `vsheet.py` (planșe de probă din cadre și din film), `mux.sh` (comanda `ffmpeg` de mai jos), `vo_check.py` / `vo_words.py` (compară transcrierea Scribe cu scriptul și scot timpii cuvintelor) și transcrierile brute.

### Stratul `TC` în `dpf.py` (trei modificări față de `sursa/dpf-doc-blender/dpf.py`)

```
TIERS = {'T1': 1, 'T2': 2, 'T8': 8, 'TA': 24, 'TB': 24, 'TC': 8}
# în info():      C['TC'] = bbox(boxpts(xm - 36.0, xm + 36.0, 6.0, 122.0, 0.0, 30.0), 8, 16)
# în job_list():  buclele trec și prin 'TC'; la măști  `if tn == 'TC' and k == 'B': continue`  (doar TC_sec și TC_idA);
#                 eșantioane  {'T2': 64, 'T8': 48, 'TC': 48}.get(tn, 60)
```

`queue.sh` are grupurile `"T1_sec T1_front T1_id" "T2_" "T8_ TA_ TB_ TC_"` și sare peste ce e deja pe disc (se poate reporni).

## Cum se reface

```
# straturile Blender (o dată; pe 24.11.2026 au durat ~2 h 20 pe 2 nuclee: T1 6 min, T2 18, T8 22, TA 35, TB 20, TC 17, măștile sub 1 min fiecare)
# vezi sursa/dpf-doc-blender/README.md, cu dpf.py modificat ca mai sus (are și TC)
cd comp
python3 film.py --info                      # cronologia: fraze, cadre, segmente
python3 film.py --mid --only 9,10,28        # cadre de probă la mijlocul frazelor
CRF=26 python3 film.py --out final/DPF_training_V.mp4 --jobs 2            # 9:16; câte un fișier pe segment în .seg/, lipite fără recodare
FMT=H CRF=26 python3 film.py --out final/DPF_training_H.mp4 --jobs 2      # 16:9
python3 film.py --out final/DPF_training_V.mp4 --force 7,8                # reface doar segmentele 7 și 8
ffmpeg -i final/DPF_training_V.mp4 -i vo/DPF_training_voce.mp3 -map 0:v -map 1:a -c:v copy -c:a aac -b:a 128k -shortest out.mp4
```

Un cadru = o frază. Durata cadrului e durata frazei rostite (`vo/meas.json`), cu 0,42 s între fraze și 1,05 s între capitole. Listele din panouri apar pe cuvântul rostit (`vo/words.json`). Segmentele care au nevoie doar de planșele largi (T1, T2) se pot randa înainte ca prim-planurile (T8, TA, TB, TC) să fie gata.

Timpi și mărimi (2 nuclee, CRF 26): 13.772 de cadre; 24 de segmente; filmul 9:16 are 126 MB. Cu 2 procese, ~4–6 cadre pe secundă (întregul film în 45–60 de minute). Sesiunea se poate reporni singură în timpul unei randări lungi: tot ce rulează în fundal se oprește, fișierele rămân; `queue.sh` și `film.py --out` se reiau de unde au rămas (un `NN.tmp.mp4` rămas în `.seg/` se șterge).

## Vocea, pas cu pas (ElevenLabs)

1. Flow `zCKbdQBRenR06Seq6h00`, 20 de noduri `tts` refolosite în trei serii (`creative_update_flow_nodes` cu textele și vocea, `creative_run_flow_nodes` cu `generations_count=1`).
2. `creative_execute_sandbox` pe fiecare serie: măsoară fiecare frază (durată, pauze, nivel, ton) și scrie un pachet WAV cu felii de 16 s.
3. Verificare: `creative_transcribe_audio` (Scribe) pe pachete. Atenție: costă cam 5,5 credite pe secundă de sunet, cu tot cu liniște (estimarea uneltei arată mult mai puțin); pachetele se strâng înainte, fără liniști.
4. Pista finală se face tot în sandbox: fiecare frază pusă la momentul ei din `vo/cues.json`, nivel egalizat pe frază (−23 LUFS), apoi +7 dB cu limitator: −16,1 LUFS, vârf −1,5 dBFS. Rezultat: `DPF_training_voce.mp3` și `.wav` pe flow.
5. Sunetul nu se poate descărca direct în sesiunea de lucru (gazdele ElevenLabs sunt blocate): vine prin workflow-ul `fetch-sources` din repo (cere acces de scriere) sau atașat de Sabin în conversație.

Credite: 8.233 pentru voce (59 de fraze, o variantă), 3.546 pentru transcriere.

## Ce e reconstruit, ilustrativ sau dedus

- Modelul e un ansamblu generic, de tipul celor montate lângă turbină la 2.0 TDI common rail (vezi `memorie/dpf-doc-blender.md`).
- Marcat pe ecran „VALORI ILUSTRATIVE”: gramele de funingine, temperaturile de la cei trei senzori, tensiunea senzorului, barele de presiune, graficele.
- Marcat „STARE SIMULATĂ”: fisurile filtrului, scăpările, gazele cu multă funingine. Marcat „DESEN SCHEMATIC”: bucla EGR de joasă presiune, senzorul de particule, țeava de evacuare.
- Pragurile de 18 / 40 / 45 g sunt exemplul 2.0 TDI (regenerarea în mers pornește la 18,9 g: buletin VW pentru SUA; 40 g și 45 g: ca în filmul „De ce filtrul de particule nu se regenerează sau se topește”). Diferă de la motor la motor.
- Dedus, nu din documentația de fabrică: mecanismul prin care răcitorul EGR de joasă presiune înfundat dă P2002 (prin filtru trece mai puțin gaz decât în calcul); vezi `memorie/p2002-ea288-continut-tehnic.md`.
- Codurile de eroare sunt cele generice OBD (P2002, P2463, P242F, P2458, P2459, P244A, P244B, P2452–P2455); la VAG textele din tester diferă.
