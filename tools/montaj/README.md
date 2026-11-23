# Montaj din cele mai bune momente („Echipa Turbo Doctor la Bosch Budapesta”, 24.11.2026)

Când Sabin cere explicit o **selecție de cadre** dintr-un set de clipuri (nu clipurile lipite întregi), de exemplu pentru un reel de prezentare
fără o voce care să curgă tot timpul (curs de formare, eveniment, vizită):

- `build_montage_bosch_budapesta.py [țintă dBFS]` face sursa reel-ului din momentele alese (`SPEC`: clip, început, sfârșit), **în ordinea filmării**.
  Tăieturile cad pe bătaia muzicii din `audio.py` (104 bpm, `('beat', k)`), deci montajul „bate” cu muzica. Fiecare bucată are imaginea și sunetul ei.
- Vorbirea în română (fraza de hook, replicile colegilor) merge pe pista vocii a sursei: e transcrisă, subtitrată și trece prin lanțul vocii din `audio.py`.
- Sunetul real al celorlalte bucăți (instructorul în altă limbă, atelierul) merge separat în `amb_bed.wav`, adus la același nivel pe bucată
  (implicit −24 dBFS pe partea activă, cel mult +8 dB) și pus în `out/v2.json` ca `beds`; așa nu e transcris, nu primește subtitrări și nu coboară muzica.
- Clipurile de pe iPhone trec întâi prin tone mapping (`pipeline/sdr.sh`); pista audio bună e cea AAC (pista APAC spațială nu se poate decoda).
- Mesajul de final stă pe ultimul cadru aproape înghețat (`"tip": {"dur": 3.6, "src": <sfârșit − 0,07>, "speed": 0.02}`) cu `bgFix`, ca sigla
  de pe spatele colegului să rămână întreagă în cadru.
- Subtitrările mutate doar pe un interval: `capTopAt: [[t0, t1, top]]` în `reel.js` (aici deasupra siglei TURBO DOCTOR de pe spate).

Exemplu de scene: `pipeline/examples/reel_bosch_budapesta_curs_formare_montaj.js`.
