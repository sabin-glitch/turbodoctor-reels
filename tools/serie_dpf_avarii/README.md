# Seria „De ce intră filtrul de particule în avarie” · scenariile (24.11.2026)

Sursa textelor pentru cele 16 episoade. Documentul pentru Sabin (lista celor 39 de cauze, explicațiile, partea Turbo Doctor, scenariile, sursele) este făcut din aceste fișiere: https://claude.ai/artifact/7EwJYdsfdA5NoXu7nP3nzB. Nota proiectului: `memorie/serie-dpf-avarii.md`.

Stare la 24.11.2026: scenariile sunt scrise și puse în document. Nu există încă voce, imagine sau montaj.

## Fișiere

- `episoade.py`: `EP` = lista episoadelor (din `ep_a.py` 1–5, `ep_b.py` 6–11, `ep_c.py` 12–16). Fiecare episod: `n`, `nume` (numele din formulă), `titlu` (titlul filmului), `rows` = rânduri `(text rostit, imagine, pe ecran, sursa)`. Textul `"@F"` = formula de început („Seria „De ce intră filtrul de particule în avarie”. Episodul X din 16: <nume>.”), `"@FF"` = formula episodului final. `C1`, `C2` = cele două rânduri ale formulei de final, adăugate la fiecare episod de `statx.rows_full`.
- `statx.py`: `rows_full(e)` și numărătoarea (rânduri, cuvinte, caractere, durată estimată = caractere / 13,6 + 6 s, rândurile de peste 30 de cuvinte, rândurile unice pentru voce). Rulare: `python3 statx.py`.
- `gen.py`: `md_ep(e)` = tabelul complet al unui episod (cu „Pe ecran”); `md_doc(e)` = tabelul fără „Pe ecran”. În document sunt doar primele 12 rânduri ale fiecărui episod (fără „Pe ecran” și fără cele două rânduri de final, care sunt aceleași peste tot). Rulare: `python3 gen.py <n>`.
- `note_surse.md`: notele studiului din 24.11.2026 (fapt · sursă · deschisă sau doar extras de căutare).
- `cauze.md`: cele 39 de cauze pe grupe și împărțirea lor pe episoade.

## Coduri în coloana „Imagine”

- F = filtrul din Blender (`tools/blender_dpf` în repo): F-ext exteriorul, F-sec secțiunea cu gazele, F-fata fața de intrare, F-can canalele de aproape, F-fun funinginea din canale, F-senz senzorii, F-dp senzorul de presiune diferențială cu prizele, țevile și barele de presiune, F-reg regenerarea, F-cen cenușa. Toate există în straturile randate (`layers.tar`) și în montajul `comp/comp.py`.
- M = motorul din Blender (`tools/blender_motor4`): M-A întreg, M-C pompa și baia de ulei, M-D camera de ardere, M-E supapele. T = turbina (`tools/blender_turbo_lagare`): T-sec, T-ext. I = injectorul CRI2.
- S = desen schematic 2D. „Stare simulată” = defect desenat peste randare, cu eticheta pe ecran. De făcut pe modelul filtrului: fisură și zonă topită, filtru îmbibat cu ulei, depuneri albe, fața catalizatorului înfundată, țeavă înfundată și furtunaș fisurat.

## Coduri în coloana „Sursa”

Codurile (VW1–VW6, GM1–GM2, H1–H4, DX1, G1 etc.) sunt explicate, cu linkuri, în secțiunea „Surse” din document. `[D]` = deducția mea. `[C]` = rândul spune ce face Turbo Doctor și trebuie confirmat de Sabin. TD1 = reelul lui Sabin din 17.11.2026 (recondiționare), TD2 = speța Radu Robert din 18.11.2026, TD3 = reelurile despre 2.0 TDI Euro 6 și P2002, TD4 = mesajul lui Sabin din 24.11.2026.

## Numere (24.11.2026)

16 filme, 224 de rânduri, 194 de rânduri unice de voce, circa 15.100 de caractere (o variantă pe rând = circa 15.100 de credite ElevenLabs; două variante = circa 30.200), circa 24 de minute în total. În cont, la 24.11.2026: 29.859 de credite libere, resetare pe 7.12.2026.
