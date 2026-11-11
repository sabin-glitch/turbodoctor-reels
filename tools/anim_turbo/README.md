# Reel animat „Nu schimba turbina defectă până nu vezi asta” (11.11.2026)

Reel explicativ din animația 3D a turbosuflantei pe motor (artifact „Turbosuflanta pe motor”), cu vocea lui Sabin din ElevenLabs:
axul care se rupe din lipsă de ungere (hook), cum funcționează turbina și filmul de ulei, cauzele (pompă de ulei slăbită, depuneri pe
turul turbinei), aceeași problemă la turbina nouă dacă nu se elimină cauza, apoi ungerea rezolvată. Același flux ca `tools/anim_injectie/`.

## Ce e nou față de anim_injectie

| Fișier | Rol |
|---|---|
| `index_src.html` | sursa animației, cu **stratul de defect** (`window.__FAIL` / `applyFail`): `starve` (filmele de ulei se golesc), `clog` (depuneri pe tur), `pump` (pompă slăbită), `heat` (lagăre și ax încinse), `wobble` (rotorul joacă în lagăre), `sparks`, `snap` (axul rupt la `FRAC_A`: jumătatea turbinei pleacă spre dreapta, a compresorului cade și încetinește) — refolosibil pentru alte animații cu defecte |
| `reel_tail.js` | regia: piste `TR` legate de cuvinte (`W(linie,'cuvânt')`), trei rupturi (`SNAP1` hook, `SNAP2` „rupe”, `SNAP3` „problemă”), dip la negru la fiecare „turbină nouă”, cadre de cameră pe zone (`SHOTS`) |
| `probe.js` + `make_bed.py` | sunetul din starea animației: șuieratul turbinei (scade după rupere), motorul, scrâșnetul lagărelor uscate, scântei, ruptura (crack + clang + zornăit) → `audio/bed_fx.wav`. `make_bed.py <out.wav> <sfârșitul hook-ului>`: șuieratul și fondul de motor rămân **doar în hook** (cerut de Sabin pe 11.11: fără zgomot de turbină pe tot parcursul); scrâșnetul și rupturile rămân |
| `../../pipeline/examples/reel_turbo_ungere_ax_rupt_animatie.js` | `reel.js`: hook `boom` „NU SCHIMBA” / „TURBINA DEFECTĂ” cu `cut` exact pe ruptura axului, apoi „SE STRICĂ DIN NOU!” |

Pașii sunt aceiași ca în `tools/anim_injectie/README.md` (voce: `python3 make_vo.py take vo/t1.mp4 vo/t2.mp4`; `fonts/` și `three.min.js` lângă fișiere).
`stills.js`, `render_frames.js`, `probe.js` cer `playwright` global (fără căi fixe); foaia de contact se face cu ffmpeg (`xstack`).

## Reguli de cadru

- zona sigură a animației: y 560–1280 (720 în hook, ca titlurile boom să stea deasupra); etichetele se opresc la 1250;
- planul larg cu motorul întreg nu încape pe înălțime: cadrele `wide`/`cause` taie de sus și de jos, centrul pe turbo + baia de ulei.
