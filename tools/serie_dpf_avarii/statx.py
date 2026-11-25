# -*- coding: utf-8 -*-
import re
from episoade import EP, C1, C2, FF, formula

def rows_full(e):
    out = []
    for (v, i, s, src) in e['rows']:
        if v == '@F': v = formula(e['n'], e['nume'])
        if v == '@FF': v = FF
        out.append((v, i, s, src))
    out.append((C1, "Cartonul Turbo Doctor intră peste F-ext.", "CĂUTĂM ȘI CAUZA", "formula, TD4"))
    out.append((C2, "Ecranul de final: TURBO DOCTOR · Diagnoză gratuită · 0739 065 065 · Galați · București · Iași · Piatra Neamț.", "DIAGNOZĂ GRATUITĂ", "formula, TD4"))
    return out

def words(t): return len(re.findall(r"[\wăâîșțĂÂÎȘȚ]+", t))

if __name__ == '__main__':
    tot = 0; totc = 0
    for e in EP:
        r = rows_full(e)
        w = sum(words(x[0]) for x in r); c = sum(len(x[0]) for x in r)
        dur = c / 13.6 + 6
        tot += dur; totc += c
        long = [(k + 1, words(x[0])) for k, x in enumerate(r) if words(x[0]) > 30]
        print(f"EP{e['n']:>2} {e['nume'][:40]:40} rows={len(r):2} words={w:3} chars={c:4} ~{dur:4.0f}s long={long}")
        for k, x in enumerate(r): assert all(x), (e['n'], k, x)
    print('total chars', totc, '~min %.1f' % (tot / 60))
    uniq = set()
    for e in EP:
        for x in rows_full(e): uniq.add(x[0])
    u = sum(len(t) for t in uniq)
    print('unique rows', len(uniq), 'unique chars', u, '| o variantă =', u, 'credite · două variante =', 2 * u)
