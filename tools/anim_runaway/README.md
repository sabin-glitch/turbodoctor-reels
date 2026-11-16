# „Turbina o ia pe ulei! Află de ce!” — reel animat cu hook AI realist (16.11.2026)

Aprobat de Sabin și publicat pe 16.11.2026 („postează-l pe toate canalele sociale acum, pe brandul Turbo Doctor”): Facebook, Instagram, TikTok, YouTube. 2:59, 1080×1920, 30 fps, 5391 de cadre.

## Structura

- **0–7,1 s: hook AI**, o singură filmare continuă: un Golf 5 care o ia pe ulei (fumul crește, motorul se turează), clientul sare de la volan și se ia cu mâinile de cap. Peste turare, vocea lui Sabin: „Turbina o ia pe ulei! Află de ce!” (0,30–3,45 s), apoi „Știi de ce se întâmplă asta? Hai să-ți explic inginerește.” (5,4–8,9 s).
- **de la 7,1 s: animația 3D** (three.js, motorul din `tools/anim_turbo`, regia pe cuvinte în `runaway_tail.js`, pagina asamblată de `build_runaway.py`) pe vocea lui din ElevenLabs (`vo_script.json`, `make_vo.py`).
- card de final standard, fără CTA.

## Ce a cerut Sabin, în ordine

1. Nu „ambalarea motorului/dieselului”, ci „turbina o ia pe ulei” / „a luat-o turbina pe ulei”.
2. Hook din Higgsfield: Golf 5, mult fum alb, motorul turat, clientul disperat care se dă jos de la volan; apoi „Știi de ce se întâmplă asta? Hai să-ți explic inginerește.”
3. Să se audă cum se turează motorul, fum pe eșapament, text mare.
4. „Exact așa cum este în realitate”: întâi mă uit la filmări reale; turația crește constant, fumul e continuu și corelat cu sunetul; clientul e în același cadru cu mașina, nu într-un cadru separat.
5. În timp ce se turează, vocea lui spune: „Turbina o ia pe ulei. Află de ce.”

## Hook-ul: imaginea

- Documentare pe filmări reale de diesel runaway (YouTube, prin vidIQ: `vidiq_youtube_search`, `vidiq_video_watch`): turația urcă încontinuu, fără salturi și fără limitator; fumul se îngroașă odată cu turația; omul sare din mașină.
- Higgsfield `kling3_0` (pro, 9:16, fără sunet): un clip de bază, apoi o **continuare generată din cadrul 54 al aceluiași clip** (`start_image`), ca fumul să crească fără întrerupere și omul să apară în același decor. 4 variante × 8 s = 56 de credite.
- `build_hook_v6b.py <continuare.mp4> 54 7.1`: lipește clipul de bază (cadrele 0–53) cu continuarea (fără primul ei cadru, care e dublură), redat la 1,25× (1,5× pe partea doar cu fum); potrivește claritatea și luminozitatea la îmbinare; scrie `frames_base/00000–00212`, `audio/hook_smoke.json` (cât fum e în fiecare cadru) și `audio/hook_map.json`.
- `tailgate_fix.py`: Kling a desenat litere fără sens pe hayon. Le scot cu zona curată din primul cadru, urmărită (translație + rotație) și potrivită la lumina cadrului; fumul și omul rămân deasupra.
- Fișierele locale ajung la Higgsfield cu `media_import_url`: imaginile de pe `raw.githubusercontent.com`, clipurile de pe `cdn.jsdelivr.net/gh/<owner>/<repo>@<branch>/<fișier>` (raw le servește ca octet-stream și sunt respinse).

## Hook-ul: sunetul

- `make_hook_bed7.py <T_voce> <AICUT>`: înregistrare reală de turbodiesel turat (Freesound 865222, CC0), re-eșantionată cu viteză variabilă ca să urmeze exact o țintă exponențială, 870 → 5.880 rpm (0,56 octave/s), de la apariția fumului (0,15 s) până înainte de voce. Nivelul e adus pe o dreaptă în dB (−26 → −14). Peste motor, un șuierat de turbină sintetizat (850 Hz → ~2,8 kHz, cu −13 dB sub motor, cu zgomot de aer). După vârf, turația maximă e ținută (granular). Sub voce, motorul coboară pe intervalele în care se vorbește.
- `analyze_bed.py`: verificare numerică independentă, fiindcă nu pot asculta sunetul: turația urmărită 899 → 5.711 rpm, monoton, abatere maximă 42 de cenți, fără pocnituri. Fumul din imagine față de turație: r ≈ 0,95.
- O descriere independentă a sunetului: Higgsfield `video_analysis_create` (gratuit). Prima variantă a fost descrisă „ca un aspirator”; după ce șuieratul a coborât și a primit zgomot de aer: turbină care se încarcă peste un diesel.

## Vocea din hook

- ElevenLabs, vocea „Sabin”, `eleven_v4`. În replica întreagă, „Află de ce.” ieșea cu ~7 dB mai încet și cu final slab, așa că am generat separat „[serious] [firm] Află de ce!” și am lipit-o după prima propoziție (`eval_takes.py`, `make_vo_lib.py` măsoară variantele: ASR, nivel pe propoziție, F0).
- `splice_hook_vo2.py <T_A> 0 1.0`: pune replica în pista de voce, aduce fiecare propoziție la nivelul narațiunii, corectează începuturile de cuvânt din anvelopă și rescrie `out/timeline.json` (propozițiile 0 și 1).

## Titlurile din hook

Trei rânduri `boom` care rămân împreună până la „Știi…”: „TURBINA O IA” (alb, din primele cadre), „PE ULEI!” (galben, impact pe „pe”), „AFLĂ DE CE!” (roșu, impact pe „Află”). Coperta: 4,85 s (toate rândurile, omul care sare, fumul). `reel.js`: `pipeline/examples/reel_turbina_o_ia_pe_ulei_hook_ai_animatie.js`.

## Sunetul final

- `v2.json`: `beds` cu `audio/hook_bed.wav` (fără ducking automat, fiindcă e deja în fișier) și `music_in` 7,1 (muzica intră odată cu animația).
- `tweak_sfx.py`, după fiecare randare: efectele titlurilor din timpul turării la ×0,15, ca să nu acopere motorul.
- `loudnorm` dinamic aplatizează crescendo-ul (14 dB → 7 dB, în trepte) și schimbă nivelul vocii în funcție de ce e înainte. De aceea `finish_hook_audio.py`: hook-ul (0–9,8 s) = `mix_pre` × câștig constant (vocea la −15 dBFS), limitare doar peste −1,5 dBTP, crossfade 9,2–9,8 s în mixul final al variantei dinainte. Restul reel-ului rămâne identic bit cu bit. (`fix_hook_dynamics.py` e varianta mai veche, de la v6.)

## Re-randare rapidă a hook-ului

`partial_hook_render.sh` randează doar cadrele 0–308; restul se copiază fără recodare din randarea dinainte (cadru-cheie la 10,3 s): ~49 s în loc de o randare completă. `finish_v7.sh` leagă toți pașii; `finish_runaway.sh` e calea cu randare completă.

## Text scris de mine, neconfirmat de Sabin

Scenariul e scris din documentare, nu sunt vorbele lui: „câțiva litri de ulei pe minut”, clapeta de admisie care „stă închisă doar câteva secunde”, „calculatorul taie motorina”, oprirea la cutia manuală (treapta cea mai mare, frână, ambreiaj eliberat) și stingătorul cu CO₂. I le-am semnalat la fiecare livrare; a cerut publicarea fără să le comenteze.
