# Fotografii reale în reel-uri (motor, piesă, model exact)

Când Sabin cere „pune efectiv deasupra un motor X” (14.11.2026, motorul 4.4 BMW M / S63), fotografia vine **doar de pe Wikimedia Commons, domeniu public sau CC0**
(fără obligație de atribuire și fără share-alike). Nu folosim o poză oarecare de pe net și nici pozele CC BY / CC BY-SA.

Din workspace nu se ajunge la Wikimedia, așa că și căutarea, și descărcarea merg prin workflow-ul `fetch-sources` (fișierele ajung pe branch-ul `sources` cu extensia `.mp4`, indiferent de conținut):

```bash
B='https://commons.wikimedia.org/w/api.php?action=query&format=json'
II='&prop=imageinfo&iiprop=url%7Csize%7Cmime%7Cextmetadata&iiextmetadatafilter=LicenseShortName%7CArtist%7CImageDescription%7CAttributionRequired%7CCredit&iiurlwidth=1600'
# 1) căutare doar printre fișierele fără restricții (PD / CC0): haslicense:unrestricted
U1="cm_free_s63=${B}&generator=search&gsrsearch=BMW%20S63%20haslicense:unrestricted&gsrnamespace=6&gsrlimit=50${II}"
# 2) categoria subiectului, cu licența fiecărui fișier
U2="cm_cat_s63=${B}&generator=categorymembers&gcmtitle=Category:BMW_S63_engine&gcmtype=file&gcmlimit=200${II}"
gh api -X POST repos/sabin-glitch/turbodoctor-reels/actions/workflows/fetch-sources.yml/dispatches -f ref=main -f "inputs[urls]=$U1 $U2"
# ~2 minute, apoi:
curl -sS -o cm_free_s63.json https://raw.githubusercontent.com/sabin-glitch/turbodoctor-reels/sources/cm_free_s63.mp4
python3 -I tools/photos/commons_list.py cm_free_s63.json        # titlu | dimensiune | LIC=… | autor | descriere
```

Apoi, pentru fișierul ales: metadatele complete (`titles=File:…&prop=imageinfo%7Ccategories%7Ctemplates&iiprop=url%7Csize%7Cextmetadata%7Cuser%7Ctimestamp`, trebuie să apară
`License: pd` / `cc0` și șablonul `PD-user` / `PD-self` / `Cc-zero`) și originalul de pe `upload.wikimedia.org`, tot prin `fetch-sources` (`nume=URL`, cel mult ~10 fișiere pe rulare).

Decuparea la mărimea panoului (`schem` cu `img`, 914 × h):

```bash
python3 -I tools/photos/prep_photo.py <original.jpg> assets/photos/<nume>.jpg x0 y0 x1 y1 914 430
```

În `reel.js`: `{ k: 'schem', type: 'photoId', img: 'assets/photos/<nume>.jpg', h: 430, P: { big, code, zone }, steps, … }` (vezi README-ul principal).

## Ce avem

| Fișier | Subiect | Sursă | Licență |
|---|---|---|---|
| `assets/photos/s63_x5m.jpg` | motorul BMW S63 (4.4 V8 biturbo) în X5 M E70, capacul cu dungile M | Commons, „File:BMW X5M Engine.JPG”, autor Dabombazzz, 2009 | domeniu public (PD-user) |

Pentru S63 nu există altă fotografie liberă pe Commons (verificat pe 14.11.2026: categoria „BMW S63 engine” are 8 fișiere, restul CC BY-SA).
