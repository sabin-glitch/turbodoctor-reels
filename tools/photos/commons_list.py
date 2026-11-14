"""List Commons API results: title, size, license, artist. usage: python3 -I commons_list.py file.json [filter]"""
import json, sys, re, html
d = json.load(open(sys.argv[1]))
pages = (d.get("query") or {}).get("pages") or {}
flt = sys.argv[2].lower() if len(sys.argv) > 2 else ""
rows = []
for p in pages.values():
    ii = (p.get("imageinfo") or [{}])[0]; em = ii.get("extmetadata") or {}
    g = lambda k: re.sub(r"<[^>]+>", "", html.unescape((em.get(k) or {}).get("value", ""))).strip()
    rows.append((p.get("index", 0), p["title"], ii.get("width"), ii.get("height"), ii.get("mime"), g("LicenseShortName"), g("Artist")[:40], g("ImageDescription")[:110], ii.get("url")))
rows.sort()
for r in rows:
    if flt and flt not in (r[1] + " " + r[7]).lower(): continue
    print(f"{r[1]} | {r[2]}x{r[3]} {r[4]} | LIC={r[5]} | by {r[6]} | {r[7]}")
print(len(rows), "results")
