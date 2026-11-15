#!/usr/bin/env python3
"""Reduce o pagină Freesound (căutare, etichetă sau pagina unui sunet) la lista sunetelor din ea: id, titlu, autor,
durată, licență, link de preview. Pe branch-ul `sources` ajunge doar acest JSON, nu pagina (pagina are scripturi și
chei ale site-ului, care nu au ce căuta în repo).   python3 fs_extract.py <fișier html>  → îl rescrie ca JSON"""
import html, json, re, sys
p = sys.argv[1]
h = open(p, encoding='utf-8', errors='replace').read()
h = re.sub(r'(?is)<script.*?</script>|<style.*?</style>|<svg.*?</svg>|<!--.*?-->', ' ', h)
text = lambda s: re.sub(r'\s+', ' ', html.unescape(re.sub(r'(?s)<[^>]+>', ' ', s))).strip()
LIC = (('publicdomain/zero', 'cc0'), ('licenses/by-nc', 'by-nc'), ('licenses/by/', 'by'), ('sampling+', 'sampling+'))
ms = list(re.finditer(r'data-mp3="([^"]+)"', h)); out = []
for k, m in enumerate(ms):
    a = h.rfind('<', 0, m.start()); b = h.find('>', m.end())
    at = dict(re.findall(r'data-([a-z0-9-]+)="([^"]*)"', h[a:b + 1]))
    w = h[a:(h.rfind('<', 0, ms[k + 1].start()) if k + 1 < len(ms) else min(len(h), b + 6000))]
    link = re.search(r'href="(/people/([^/"]+)/sounds/(\d+)/)"', w)
    lic = sorted({n for s, n in LIC if s in w} | {x.lower() for x in re.findall(r'bw-icon-(zero|by-nc|by|sampling)', w)}
                 | {x.lower() for x in re.findall(r'(Creative Commons 0|Attribution NonCommercial|Attribution)', w)})
    out.append({'id': at.get('sound-id') or (link.group(3) if link else None), 'title': html.unescape(at.get('title', '')),
                'user': link.group(2) if link else None, 'url': 'https://freesound.org' + link.group(1) if link else None,
                'duration': at.get('duration'), 'mp3': m.group(1), 'license_marks': lic, 'text': text(w)[:500]})
tot = re.search(r'([\d,.]+)\s+(?:results|sounds)\b', text(h))
extra = {} if out else {'links': sorted(set(re.findall(r'/people/[^/"]+/sounds/\d+/', h)))[:200],
                         'previews': sorted(set(re.findall(r'https://cdn\.freesound\.org/previews/[\w/.-]+?\.mp3', h)))[:200], 'text': text(h)[:3000]}
json.dump({'n': len(out), 'total_text': tot.group(0) if tot else None, 'sounds': out, **extra}, open(p, 'w'), ensure_ascii=False, indent=1)
print(f'fs_extract: {len(out)} sunete')
