# Seria „De ce intră filtrul de particule în avarie” · producția (25.11.2026)

16 filme 9:16 (1080×1920, 30 cadre/s), câte unul pe episod, cu vocea „Sabin” din ElevenLabs, montate pe modelul Blender al filtrului de particule (`tools/blender_dpf` din repo). Scenariile sunt în `episoade.py` + `ep_a.py`, `ep_b.py`, `ep_c.py`.

## Fișiere

| Fișier | Ce face |
|---|---|
| `vo_prep.py` | rândurile unice de voce → `vo/lines.json` (cifrele și abrevierile scrise în litere; formula de început e ruptă în „Seria …”, o singură dată, + „Episodul X din șaisprezece: …”) |
| `vo_batch.py N` | tipărește lotul N (20 de rânduri) pentru nodurile `tts` din flow |
| `vo_rec.py`, `vo/packs.json` | lungimile fiecărui rând din pachet și id-ul pachetului |
| `vo_fetch.sh` | pornește workflow-ul `fetch-sources` din repo, care descarcă pachetele pe ramura `sources` |
| `vo_split.py` | taie pachetele în `vo/takes/L###.wav`, măsoară (`vo/meas.json`) și verifică fiecare rând cu recunoaștere de vorbire Parakeet (`vo/asr.json`, cu momentul fiecărui cuvânt) |
| `vo_ep.py N` | pista de voce a episodului (`vo/epNN/vo_track.wav`, −16,6 LUFS, vârf −4,5 dBFS) |
| `comp/eng.py` | motorul de imagine: straturile Blender, funingine, cenușă, regenerare, gaze, senzori + stările simulate (fisuri, topire, ulei, depuneri albe, fața catalizatorului astupată, filtru golit, țeavă înfundată, furtunaș crăpat, scăpare pe evacuare) |
| `comp/serie.py` | montajul: un plan pe rând rostit, cârlig, carton de titlu, texte, panouri (bord, tester, scale, lanțuri, liste), formula de final și ecranul de final |
| `comp/shots.py` | planurile celor 16 episoade |
| `render_ep.sh N`, `queue.sh N…` | randează episodul (două jumătăți în paralel), pune vocea, scoate coperta |

## Cum se reface

```
# straturile Blender: tools/blender_dpf din repo (layers.tar) + stratul TC (prim-plan pe catalizator; vezi sursa/dpf-training/README.md)
python3 vo_prep.py                          # vo/lines.json
# vocea: vezi mai jos; apoi
python3 vo_split.py                         # vo/takes, vo/meas.json, vo/asr.json   (cere sherpa-onnx + modelul Parakeet)
EP=3 python3 comp/serie.py --info           # cronologia episodului 3
EP=3 python3 comp/serie.py --mid            # câte un cadru de probă pe rând, în comp/proof/
./render_ep.sh 3                            # final/TurboDoctor_DPF_avarii_ep03_<nume>.mp4 + coperta
```

Un episod se randează în circa 5–6 minute pe 2 nuclee. Un text de pe ecran sau un plan se schimbă în `comp/shots.py`; se randează din nou doar episodul acela. Un rând rostit schimbat cere o nouă generare a acelui rând.

## Vocea (ElevenLabs)

- Vocea „Sabin” (`voice_id 2RuO79IWvD8wFKGk2vJi`), `eleven_v4`, o variantă pe rând; `[serious]` la cârlig, `[calm]` la restul.
- Flow `zCKbdQBRenR06Seq6h00`: cele 20 de noduri `tts` refolosite în 10 loturi (`creative_update_flow_nodes` cu textele, `creative_run_flow_nodes` cu `generations_count=1`), apoi `creative_execute_sandbox` lipește lotul într-un WAV (`sd_bNN.wav`, 0,5 s liniște între rânduri) și tipărește lungimile.
- Adusul în sesiune: `creative_get_available_assets` dă un link semnat spre copia MP3 a pachetului; `vo_fetch.sh "sdbNN=<link>"`; după circa 2 minute fișierul e la `raw.githubusercontent.com/sabin-glitch/turbodoctor-reels/sources/sdbNN.mp4` (este MP3).
- 195 de rânduri + 2 refăcute. Credite: circa 16.600. Formatele `.flac` nu devin fișiere pe flow (doar imagine, video, audio obișnuit).
- Rostiri: cifrele în litere; EGR → „e-ge-re”; VW → „Volkswagen”; GM → „General Motors”; NGK → „En-ge-ca”; BMW-uri → „be-em-ve-uri”; ITP → „i-te-pe”. „TDI” scris „te-de-i” a ieșit neclar; s-au refăcut cele două rânduri cu „TDI” scris ca atare.

## Ce e simulat, schematic sau ilustrativ

Pe ecran apare eticheta potrivită: „STARE SIMULATĂ” (fisuri, topire, ulei, depuneri, dopuri, scăpări), „DESEN SCHEMATIC” (lanțurile de casete, senzorul de particule), „VALORI ILUSTRATIVE” (grame, temperaturi, bare), „EXEMPLU · DIFERĂ DE LA MOTOR LA MOTOR” (pragurile 18,9 / 40 / 45 g, 75 °C, turațiile). Motorul, turbina și injectorul nu apar ca modele 3D: acolo unde scenariul le cerea sunt panouri schematice.
