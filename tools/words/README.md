# Timpii cuvintelor, verificați pe anvelopa vocii

Folosite la reelul „Probleme de eficiență DPF? Recondiționare DPF!” (17.11.2026), unde recunoașterea a ștampilat câteva cuvinte în liniștea dinaintea lor
și a auzit altfel câteva cuvinte („monolit ceramic”, „Carbura”).

- `env.py <wav> a b` — anvelopa vocii (150–4000 Hz), o cifră la 20 ms + momentele în care pornește vocea. Din ea se citesc începuturile de cuvânt
  pentru titlurile `boom`, `kin`, `scan` și pentru pașii schemelor (vocala cuvântului, nu timpul din ASR).
- `check_words.py <folder reel>` — listează cuvintele din `out/timeline.json` al căror început cade în liniște (ștampilate prea devreme) și momentul în care pornește de fapt vocea.
- `patch_words_dpf_eficienta.py <folder reel>` — exemplu: mută începuturile acelor cuvinte în `out/timeline.json` și `out/timeline_1x.json` (ritm natural, fără tăieturi).
  Se rulează după `retime.py`; lista `FIX` se scrie pentru fiecare reel.
- `slowasr.py <folder reel> <tempo> a-b …` — Whisper + Parakeet pe ferestre înguste, cu vocea încetinită (`atempo`), pentru cuvintele pe care transcrierea nu le prinde sigur.
