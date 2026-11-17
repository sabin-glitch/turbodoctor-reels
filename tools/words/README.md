# Timpii cuvintelor, citiți din anvelopa vocii

Folosite la reelul „Probleme de eficiență DPF? Recondiționare DPF!” (17.11.2026, aprobat și programat pe 20.11). Completează `pipeline/fix_words.py`
(care mută începuturile de cuvânt din `out/word_fix.json`, între `build_timeline.py` și `retime.py`).

- `env.py <wav> a b` — anvelopa vocii (150–4000 Hz), o cifră la 20 ms, plus momentele în care pornește vocea. Din ea se citesc începuturile de cuvânt
  pentru titlurile `boom`, `kin`, `scan` și pentru pașii schemelor: vocala cuvântului, nu timpul din ASR (ex. „spart” 6,40 · „topit” 6,76 · „crăpat” 7,24).
- `check_words.py <folder reel>` — listează cuvintele din `out/timeline.json` al căror început cade în liniște (ștampilate prea devreme) și momentul
  în care pornește de fapt vocea: candidații pentru `out/word_fix.json`. Lista acestui reel: `pipeline/examples/word_fix_dpf_eficienta.json`
  (27 de cuvinte; include și cuvintele pe care recunoașterea le-a auzit altfel, ex. „monolit ceramic”, „Carbura”).
- `slowasr.py <folder reel> <tempo> [fișier.wav] a-b …` — Whisper + Parakeet pe ferestre înguste, cu vocea încetinită (`atempo`), pentru cuvintele pe care
  transcrierea nu le prinde sigur. Rulat și pe `audio/mix_final.wav` (tempo 1.0), arată dacă vocea se înțelege peste bubuituri și muzică.
- `snap_words.py <folder reel> [index=timp …]` — detecția și mutarea într-un singur pas, fără `out/word_fix.json` (reelul „Audi A7 biturbo, în reparație
  la Turbo Doctor”, 17.11.2026): primul cuvânt al fiecărei rostiri e mutat pe începutul ei real din anvelopa vocii (180–3800 Hz), iar `index=timp` corectează
  de mână cuvântul cu acel număr din `out/timeline.json` (consoanele slabe, s / f / ș, se caută în banda 3,5–9 kHz). Se rulează între `build_timeline.py` și
  `retime.py`, în locul lui `fix_words.py`, și merge doar fără tăieturi și fără cold open. Scrie și `out/speech_runs.json` (rostirile găsite).

Dacă un cuvânt rămâne nesigur și după asta (aici: „deoarece” / „dar ce” la 58,9 s), se lasă afară din `out/curated.json` și i se spune lui Sabin la livrare.
