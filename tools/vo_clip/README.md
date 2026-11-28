# Voice-over cu vocea „Sabin” peste un clip real, fără voce (28.11.2026)

Pentru clipuri filmate fără voce (sau cu o singură frază la început), când Sabin cere voice-over cu vocea lui („te poți folosi și de vocea mea”).
Folosit la trei reel-uri trimise pe 28.11.2026 (în așteptarea aprobării): pompa cu rugină, injectorul Denso i-ART, kitul de injecție N47.

## Pași
1. `new_reel.sh <slug> <clip>`; mă uit la cadre (`contact.py`) și la tăieturi (diferența dintre cadre) și scriu textul pe ce se vede, rând cu rând.
   Nu pun cifre sau cauze pe care nu le-a spus el; tot ce e al meu i-l spun la livrare, ca să confirme.
2. Vocea: ElevenLabs, vocea „Sabin” (`voice_id` din `creative_list_voices`), model `eleven_v4`, **fiecare rând generat separat**, cu `[calm] [matter of fact]` în față
   (hook: `[serious] [matter of fact] [conversational tone]`), câte 2 variante. Fișierele ajung în workspace prin `fetch-sources`, numite `<prefix>L<NN><a|b>.mp3`.
   Siglele se scriu cum le aude ASR-ul („BMW”, „N47”), iar un cuvânt care trebuie rostit altfel decât se scrie: `{i-ART.|ai-art.}`.
3. `<reel>/vo_script.json` (exemple în `examples/`): `lines` cu `n` (numărul rândului din numele fișierelor), `t` (momentul din reel) și `text`;
   `orig` dacă fraza din clip rămâne (cu cuvintele ei, pentru subtitrări); `end_card` (5.0 la un reel de ~10 s); `fix` = început de cuvânt corectat de mână.
4. `python3 build_vo_clip.py <reel> <folder variante> <prefix>`: alege varianta pe care o înțeleg ambele recunoașteri (Parakeet și Whisper), apoi tonul cel mai
   apropiat de vocea lui; aduce rândurile la același nivel; scrie `audio/vo_track.wav`, `audio/src48.wav` (sunetul clipului doar pe fraza păstrată, altfel mut),
   `out/timeline.json` (narator, povestea = clipul întreg) și `out/vo_picks.json`. Începuturile de cuvânt se mută pe începutul real al rostirii (anvelopa vocii).
5. `out/v2.json`: `{"cuts": false, "speed": 1.0, "music_gain": 0.5, "narrator": true, "orig_gain": 0.0 sau 1.0, "orig_duck": 0.0}`; apoi `retime.py`, `extract_frames.py`, `reel.js`.
6. După `finish.sh`: `loud2.py` + mux din nou (reel-urile scurte ies altfel sub −14 LUFS) și ASR pe mixul final, rând cu rând.

## Clipuri deja montate, cu text ars în imagine
- `caption_clean_tight.py`: scoate un text static (alb sau roșu) cu o mască strânsă, la rezoluția sursei. Pe fundal uniform și întunecat rămâne o urmă fină:
  peste zona textului pun un `band` opac (titlul lui, refăcut), subtitrările coboară sub el (`capTop`) și fundalul rămâne fix (`bgFix`).
- Text mare peste un cadru care se schimbă (fereastră CapCut pe fundal negru): nu îl șterg; îl acopăr pe toată durata cu un `lbl` opac al cărui rând mare
  urmărește vocea, cu `bgFix`. `endbg_fix.py` reface `assets/end_bg.jpg` fără pata colorată a titlului vechi (se rulează după `render.py --prep`).
- `slow_tail.py`: când ultimul rând de voce nu încape, coada clipului se întinde lin (viteză normală → aproape oprit), cu cadre intermediare interpolate.

## Exemple de scene
`pipeline/examples/reel_pompa_rugina_voiceover_peste_clip.js`, `reel_denso_iart_voiceover_lbl_peste_titlu.js`, `reel_kit_n47_voiceover_band_incetinire.js`.
