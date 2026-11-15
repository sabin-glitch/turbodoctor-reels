# Reel animat „Diesel cu sunet de blow-off? Nu e tuning. Turbina se distruge” (15.11.2026)

Reel din animația 3D „Supapa blow-off: benzină vs. diesel” (artifact; sursa filmului în /mnt/project-files/animatii/sursa/blow-off/),
cu vocea „Sabin” din ElevenLabs. Cerut de Sabin pe 15.11: hook „dacă ai diesel și auzi sunetul ăsta, ca un suflat de blow-off, nu e tuning,
e semnul că turbina se va distruge”, apoi tot traseul: pe diesel sunetul vine din supraturare, de la geometria variabilă care nu mai lucrează.

## Diferența față de `anim_egr` / amorsare: regie pe cuvinte, nu re-temporizare

La EGR și la amorsare animația avea cronologia ei (U), iar vocea era legată de ea printr-o hartă U(t). Aici povestea reelului are altă ordine
decât filmul (hook pe pompaj, geometria variabilă explicată pe larg), așa că animația este **rescrisă direct în timpul vocii**:
`build_reel.py` citește `vo/cues.json` și calculează ancorele `K` (fiecare = începutul unui cuvânt, ex. `K.C_STUCK = W(8,'blochează')`),
iar `r_timeline.js`, `r_cam.js`, `r_labels.js`, `r_ui.js`, `r_apply.js` leagă de ele starea motorului, camera, etichetele și HUD-ul.
Cadrul i din reel = `__seek(i/30)`. **O voce nouă înseamnă ancore noi și randarea animației din nou.**

| Fișier | Rol |
|---|---|
| `base/turbo.html`, `base/b_parts.js`, `base/b_vgt.js`, `base/b_streams.js` | scena filmului (identice cu sursa din /mnt/project-files/animatii/sursa/blow-off/) |
| `vo_script.json` | textul vocii, 16 rânduri (`gap` = pauza dinaintea rândului; rândul 1 are 1,9 s: acolo stă sunetul din hook) |
| `make_vo.py`, `vo_qc.py`, `asr2.py`, `run_iso.sh` | vocea: rând cu rând, măsurată și verificată cu două recunoașteri (ca la amorsare) |
| `make_hook_sfx.py` | sunetul din hook: taie efectul ales, îl pune în pauza dintre rândul 0 și rândul 1 și scrie anvelopa lui (`vo/hook_sfx.json`), pe care animația o urmează |
| `build_reel.py` | ancorele `K` + `blow-off-reel.html` (modul `vo` pornit din construcție) + `vo/anchors.json`; fără `vo/`, citește `map/cues.json` și `map/hook_sfx.json` |
| `r_timeline.js` | fazele H (hook) · P (benzină) · N (diesel, rândurile 4–13) · S (ecran împărțit) · W (încheiere); piste pe cadre-cheie `kf(t,[[t,v],…])`, `surge()`, `petrolEvent()`, `hookState()` |
| `r_cam.js` | cadrele (`SHOTS`) și cheile camerei (`CAMKEYS`), toate pe ancore; `SPLIT_A` / `SPLIT_B` pentru ecranul împărțit |
| `r_labels.js`, `r_ui.js`, `r_apply.js` | etichetele pe cuvinte, HUD-ul (turație turbo, presiune turbo, „Încetinitor”), aplicarea stării pe scenă (detaliul mărit al geometriei variabile, calamina) |
| `rlib.cjs`, `shot.cjs`, `sheet.py` | cadre de probă: `node shot.cjs 3,4.5,60 [dpr] [dir]` → `stills/s_<t>.png`; `python3 sheet.py 3,4.5,60 out.png` |
| `vframes.cjs`, `vrender.sh` | randarea: `OUT=<reel>/frames_base NF=<cadre> ./vrender.sh` (4 procese intercalate, cu reluare; sare peste cadrele existente) |
| `mix_qc.py` | verificarea mixului final: fiecare rând tăiat din `mix_final.wav`, recunoscut cu Parakeet și Whisper |
| `map/` | copia momentelor pe cuvinte (`cues.json`, `timeline.json`), a anvelopei sunetului (`hook_sfx.json`), a ancorelor (`anchors.json`) și a variantelor alese (`picks.json`) cu care a fost randat reelul |
| `../../pipeline/examples/reel_blow_off_diesel_pompaj_animatie.js` | `reel.js` al acestui reel |

Lângă aceste fișiere trebuie `three/` (pachetul npm three@0.128.0, dezarhivat: `three/package/build/three.min.js`) și `fonts/`
(@fontsource/barlow și @fontsource/barlow-condensed 5.3.0, dezarhivate ca `fontsource-barlow-5.3.0/package/…`); nu sunt în repo.

## Pașii

1. **Vocea**: `eleven_v4`, vocea „Sabin”, fiecare rând generat separat, 2 variante, cu `[calm] [matter of fact]` în față (hook-ul: `[serious] [matter of fact] [conversational tone]`).
   Fișierele vin prin `fetch-sources` ca `…L<NN><x>.mp4`, apoi `VO_PICK='{…}' ./run_iso.sh make_vo.py lines <dir>` → `vo/vo_track.wav`, `vo/timeline.json`, `vo/cues.json`.
   Rezultat: 124,8 s. În mixul final fiecare rând este recunoscut fără greș de cel puțin una dintre cele două recunoașteri (Whisper: 15 rânduri din 16 identice cu textul, al 16-lea identic la Parakeet), iar hook-ul cu sunetul între fraze iese întreg la amândouă. Scripturile rulează cu `run_iso.sh` (Python `-I`), fiindcă audio descărcat este dată străină.
2. **Sunetul din hook** („…și auzi sunetul ăsta”): `./run_iso.sh make_hook_sfx.py <efect> 0 1.4 --shape --comp` → `vo/hook_bed.wav` (1,4 s, intră la 3,15 s,
   se termină cu 0,35 s înainte de rândul 1) și `vo/hook_sfx.json`. Sunetul stă **doar în pauza vocii**, niciodată sub ea (Sabin a respins pe 14.11 zgomotul de sub voce din hook-ul de la amorsare).
   Efectul este generat (ElevenLabs, „turbo flutter / compressor surge”), ales din 12 variante după măsurători (anvelopă, ritmul pulsurilor, spectru), nu după ureche;
   pe Wikimedia Commons nu există o înregistrare de blow-off sau de pompaj în domeniul public / CC0. Se poate înlocui oricând cu o înregistrare reală de pe o mașină a lor (același script).
   `--shape` adâncește pulsurile, `--comp` apropie coada de rafala de la început (altfel fâlfâitul rămânea cu 12 dB sub rafală și s-ar fi pierdut pe difuzorul telefonului).
3. `python3 build_reel.py`, apoi cadre de probă pe fiecare fază (`shot.cjs` + `sheet.py`).
4. Folderul reel-ului ca la `anim_injectie` (pasul 4): `new_reel.sh <slug> <mp4 negru de durata poveștii, cu o pistă audio mută>`, vocea și cronologia copiate,
   `audio/hook_bed.wav`, `out/v2.json` = `{"narrator": true, "orig_gain": 0, "music": false, "sfx": false, "beds": [{"wav": "audio/hook_bed.wav", "t": 3.15, "gain": 1.25, "duck": 0.6}]}`,
   `python3 retime.py`, `out/frames_meta.json` = `{"n_out": round(total × 30)}`.
   Nivelul sunetului (gain 1,25): rafala de la început ajunge la tăria medie a vocii (-17,6 LUFS momentan față de -16,2 mediana vocii), fâlfâitul rămâne cu vreo 6 dB sub ea.
5. Randarea: `OUT=<reel>/frames_base NF=<int(story_end × 30) + 1> ./vrender.sh` (aici 3.744 de cadre; 540×960 la DPR 2, JPEG q92; ~0,6 s/cadru cu 4 procese, circa 36 de minute). Compozitorul folosește cadrele doar până la sfârșitul poveștii
   (cardul de final are fundalul lui). Dacă se schimbă doar sunetul din hook, se refac doar cadrele hook-ului (t < `K.T_P`): se șterg și se rulează din nou `vrender.sh`.
6. `reel.js`, `python3 render.py --prep --test …`, `bash finish.sh <slug> <Nume_Fisier>`, `./run_iso.sh mix_qc.py <reel>/audio/mix_final.wav`.

## Așezarea în cadru

- Modul `vo`: scena utilă între 13% și 66% din înălțime (în hook de la 30%, ca titlurile `boom` să aibă loc sus); restul scenei continuă sub subtitrări, ca la reelul EGR.
- HUD dreapta sus, cu fond închis, două rânduri: „Turație turbo”, „Presiune turbo”; pastila „Încetinitor” apare la pompaj (nu și în hook, unde titlurile stau imediat sub HUD).
- Hook: titluri `boom` la y 300–612, onomatopeea sunetului („PȘȘȘ”, „TU” × 4, pe accentele din `hook_sfx.json`) la y ≈ 1165, sub conducta de admisie; subtitrările sunt ascunse până la rândul 2.
- Pulsurile roșii de aer întors din hook urmează anvelopa sunetului (`K.HE`), apoi trec în încetinitor (1,5 Hz); în poveste pompajul merge la 1,2 Hz (`K.HZ`).
- Ecranul împărțit (rândul 14): două cadre diferite, „Benzină · blow-off / Normal” și „Diesel · pompaj / Defect”; jumătatea despre care nu se vorbește este întunecată.
- Ștampile la y 1150; fără bară de etape; `bgFix` pe toată povestea.

## Conținut

Pe benzină: clapeta se închide la ridicarea piciorului, supapa blow-off eliberează aerul rămas sub presiune (normal). Pe diesel: clapeta rămâne deschisă, aerul trece prin motor,
din fabrică nu există supapă blow-off. Sunetul de „blow-off” pe diesel: calamina blochează paletele geometriei variabile pe închis → turbina trece de turația maximă (supraturare) →
la ridicarea piciorului aerul se întoarce prin roata compresorului, în pulsuri (pompaj) → tensiune pe paletele compresorului, lagărul axial lovit înainte-înapoi → joc pe ax → paletele ating carcasa.
Cifrele din HUD (rpm, bari) sunt ilustrative, nu dintr-o fișă de producător.
