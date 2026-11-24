# Montaj din cele mai bune momente („Echipa Turbo Doctor la Bosch Budapesta”, aprobat și programat pe 25.11.2026)

Pentru cazul în care Sabin cere explicit o **selecție de cadre** dintr-un set de clipuri, nu clipurile lipite întregi. Exemplu: un reel de prezentare
fără o voce care să curgă tot timpul (curs de formare, eveniment, vizită). Cererea lui a fost: „selectează cadrele cele mai interesante și fă o selecție faină”.

- `build_montage_bosch_budapesta.py` face sursa reel-ului din momentele alese (`SPEC`: clip, început, sfârșit, tip), **în ordinea filmării**.
  Tăieturile cad pe bătaia muzicii din `audio.py` (104 bpm, `('beat', k)`), deci montajul „bate” cu muzica. Fiecare bucată își păstrează imaginea.
- Tipuri de bucăți: `voice` = vorbirea în română, pe pista vocii (e transcrisă, subtitrată și trece prin lanțul vocii); `bed` = sunetul real, separat
  în `amb_bed.wav` (`beds` în `out/v2.json`); `mute` = doar imaginea, cu muzica dedesubt.
- **Varianta aprobată nu are vorbe pe fundal.** Prima versiune avea sunetul real al cursului (instructorul în maghiară/engleză, discuțiile din atelier)
  ca `bed`. Sabin a cerut să scot „cuvintele de pe fundal” din bucățile în care colegii lucrează, apoi și fraza unui coleg de la final, spusă slab, din spatele camerei.
  Acum toate bucățile sunt `mute`, cu excepția frazei de hook și a replicii clare „Un CP4 și un CP5. Ce diferență!”, iar `out/v2.json` are `"beds": []`.
- Clipurile de pe iPhone trec întâi prin tone mapping (`pipeline/sdr.sh`). Pista audio bună e cea AAC; pista APAC spațială nu se poate decoda.
- Mesajul de final cerut de Sabin („INVESTIM CONSTANT / ÎN PREGĂTIREA ECHIPEI / CA SĂ-ȚI OFERIM / CELE MAI BUNE REPARAȚII”) stă pe ultimul cadru,
  aproape înghețat (`"tip": {"dur": 3.6, "src": <sfârșit − 0,07>, "speed": 0.02}`), cu `bgFix`, ca sigla TURBO DOCTOR de pe spatele colegului să rămână întreagă.
- Etichetele (`chip`) stau pe zonele libere ale fiecărui cadru: jos peste banc unde fața e sus, sus unde mâinile sunt jos. Cardul `def` cu ce explică
  instructorul a fost traducerea mea din maghiară; i-am spus lui Sabin la livrare.

Exemplu de scene: `pipeline/examples/reel_bosch_budapesta_curs_formare_montaj.js`.
