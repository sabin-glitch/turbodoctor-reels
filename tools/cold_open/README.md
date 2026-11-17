# Cold open fără repetare (hook-ul = o frază spusă mai târziu în clip)

Folosit la reel-ul „O nouă viață la doar 30–40% din costul unei turbine noi” (17.11.2026, aprobat și programat pe 18.11): Sabin a cerut ca hook fraza pe care o spune la sfârșitul celui de-al doilea clip, „și după aia” ce spune despre recondiționare.

Ce face `build_src_noua_viata.py`:

1. Mută fraza la început **cu imaginea și vocea ei** (o singură bucată continuă). Restul rulează în ordinea filmată, fără tăieturi. Fraza nu se mai repetă la final (cold open-ul din `out/cold.json` ar fi redat-o de două ori).
2. Estompează semnătura și scrisul de mână de pe fișa clientului care apare lângă piesa veche (cadre-cheie interpolate pe fiecare cadru, sigma 20, doar pe zona scrisă). Verificare: `sigcheck.py`.
3. Ia sunetul din filmările originale și pune fade de 12 ms la îmbinări.

În reel:

- Titlurile `boom` ale hook-ului cad pe cuvintele lui; momentele se iau din anvelopa vocii, nu din ASR.
- Ultimul rând de subtitrări al hook-ului se ascunde și după îmbinare (`hideCap` până la +0,45 s), altfel rămâne 0,3 s peste primul cadru al poveștii.
- La final, când camera se întoarce la turbina recondiționată, titlul hook-ului revine ca `kin` deasupra Rețetei, iar ultimul rând al Rețetei încheie fraza. Rețeta rulează pe continuarea firească a ultimului cadru (`"tip": {"src": 0.0}`).
- Începuturile de cuvinte greșite din ASR se corectează cu `pipeline/fix_words.py` (`out/word_fix.json`).
- Rupturile de rând din subtitrări se pot dirija cu virgule în `out/curated.json`: virgula de la sfârșitul unui cuvânt nu se afișează, dar începe un rând nou („un joc, destul de considerabil” → „UN JOC” / „DESTUL DE” / „CONSIDERABIL”).

Exemplu: `pipeline/examples/reel_noua_viata_30_40_cold_open_fara_repetare.js`, `word_fix_noua_viata_30_40.json`, `curated_noua_viata_30_40.json`.
