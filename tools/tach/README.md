# Hook cu turometru care accelerează („Audi A7 biturbo, în reparație la Turbo Doctor”, 17.11.2026)

Cerut de Sabin: „hook puternic, Audi A7 biturbo și cu un turometru care se accelerează puternic, în reparație la Turbo Doctor”.

## Ideea

Acul turometrului **nu e animat de mână**. Se aude o turare reală de turbodiesel, iar turația afișată e calculată din sunetul acela,
deci acul urcă și coboară exact odată cu motorul.

- Sursa: Freesound 865222, „3008gtrevving.wav” (CC0), o turare până la limitator (822 → 3.918 rpm). E pe branch-ul `sources`
  (`fsr_865222.mp4`, de fapt un MP3): `curl -o fsr_865222.bin https://raw.githubusercontent.com/sabin-glitch/turbodoctor-reels/sources/fsr_865222.mp4`,
  apoi `ffmpeg -i fsr_865222.bin -ar 48000 -ac 2 fsr_865222.wav`.
- `revtrack.py`: urmărește frecvența de aprindere a înregistrării (însumare de subarmonice + Viterbi).
- `build_tach_bed.py <folder reel> <T_top1> <T_top2> <T_end>`: redă turarea cu viteză variabilă (fără time-stretch), ca urcarea să dureze
  ~0,8 s prima dată și ~0,63 s a doua oară, cu înălțimea crescând continuu. Scrie `audio/hook_bed.wav` și `out/track_tach.json`
  (turația afișată la 120 Hz: funcție afină de frecvența de aprindere care se aude, ralanti 850 → limitator 5.300).
  `TACH_SRC` = calea către WAV, `TACH_DUCK='[[t0,t1,dB],…]'` = motorul coboară sub cuvintele lui (ducking-ul e în fișier, deci în
  `out/v2.json`: `"beds": [{"wav": "audio/hook_bed.wav", "t": 0, "gain": 1.0, "duck": 0}]` și `"music_in"` la sfârșitul hook-ului).
- Verificare, fiindcă nu pot asculta: urmăresc din nou înălțimea în fișierul rezultat și o compar cu curba acului (abatere mediană 5 cenți),
  caut pocnituri la îmbinări și verific cu ASR pe `mix_final.wav` că fiecare cuvânt din hook se înțelege.

## Piesa `tach` din compozitor

`{k:'tach', t0, t1, x, y, s, kick: [t…], max: 6000, warn: 4500, red: 5000, turbos: 2}`: cadran original, generic (fără siglă și fără bordul
vreunui producător): 0–6 ×1000, zonă roșie, afișaj digital, două pictograme de turbină care se aprind și se învârt odată cu turația.
Peste 4.500 rpm cadranul strălucește roșu și tremură; `kick` îl face să sară odată cu impactul titlurilor. Se pune înaintea titlurilor
`boom` în `items`, ca titlurile să stea deasupra lui.

## Hook-ul reel-ului (4,85 s)

| Moment | Ce se vede | Ce se aude |
|---|---|---|
| 0,12 s | „AUDI A7” | bubuitură; motorul la ralanti |
| 0,22 → 1,00 s | acul urcă de la 850 la 5.300 | prima turare (cele 1,5 s de la început sunt fără voce) |
| 1,00 s | „BITURBO” (galben, uriaș), undă de șoc | bubuitura mare, motorul pe limitator |
| 1,55 / 2,35 s | „ÎN REPARAȚIE LA” / „TURBO DOCTOR” | pe cuvintele lui „Audi” / „3.0”; motorul coboară sub voce |
| 3,02 → 3,66 s | acul urcă din nou | a doua turare, în pauza dinaintea cuvântului |
| 3,68 s | „BITURBO” mai bubuie o dată | cuvântul lui „Biturbo”; motorul rămâne sus, cu 11 dB mai încet |

Coperta: 4,1 s (toate rândurile, acul în zona roșie). Exemplu: `pipeline/examples/reel_audi_a7_biturbo_hook_turometru.js`.

## Tot din acest reel

- `pipeline/fixwords.py` (între `build_timeline.py` și `retime.py`): timpii Parakeet vin cu până la ~0,3 s mai devreme după o pauză;
  primul cuvânt al fiecărei rostiri e mutat pe începutul ei real din anvelopa vocii. Corecturi manuale: `index=timp`.
  Consoanele slabe (s, f, ș) se caută în banda 3,5–9 kHz.
- `tags` pe apariție: `'noi#0': ''` colorează doar prima apariție a cuvântului din fereastră („la noi” față de „ansamble centrale noi”).
- Rețeta pe ultimele cadre ale clipului, aproape înghețate (`"tip": {"dur": 3.4, "src": <sfârșit − 0,25>, "speed": 0.07}`): fără salt înapoi în filmare.
- Un card care pornește cu alarmă (EKG `crit`) intră în pauza dinaintea frazei, nu peste primul ei cuvânt.
