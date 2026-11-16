#!/usr/bin/env python3
"""Reduce o pagină web oarecare (catalog de sunete) la titlu, text și lista fișierelor audio din ea, fiecare cu textul
dinaintea lui. Pe branch-ul `sources` ajunge doar acest JSON, nu pagina.   python3 web_extract.py <fișier html>"""
import html, json, re, sys
p = sys.argv[1]
raw = open(p, encoding='utf-8', errors='replace').read()
u = raw.replace('\\u002F', '/').replace('\\/', '/').replace('\\u0026', '&').replace('&amp;', '&')
clean = lambda s: re.sub(r'\S{48,}', '…', re.sub(r'\s+', ' ', html.unescape(re.sub(r'(?s)<[^>]+>', ' ', s)))).strip()
body = re.sub(r'(?is)<script.*?</script>|<style.*?</style>|<svg.*?</svg>|<!--.*?-->', ' ', raw)
t = re.search(r'(?is)<title[^>]*>(.*?)</title>', raw)
seen, audio = set(), []
for m in re.finditer(r'https?://[^"\'\s<>\\)]+?\.(?:mp3|ogg|wav|m4a|flac)(?:\?[^"\'\s<>\\)]*)?', u):
    url = m.group(0)
    if url in seen or len(url) > 400: continue
    seen.add(url); audio.append({'url': url, 'before': clean(u[max(0, m.start() - 500):m.start()])[-320:]})
json.dump({'title': clean(t.group(1)) if t else None, 'bytes': len(raw), 'n_audio': len(audio), 'audio': audio[:300], 'text': clean(body)[:6000]},
          open(p, 'w'), ensure_ascii=False, indent=1)
print(f'web_extract: {len(audio)} fișiere audio, {len(raw)} octeți')
