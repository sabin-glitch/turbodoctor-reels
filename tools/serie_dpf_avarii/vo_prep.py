# -*- coding: utf-8 -*-
# Rândurile unice de voce. Formula de început e ruptă în două: „Seria …” (o singură dată) + „Episodul X din șaisprezece: nume.”
import json, re
from episoade import EP, SERIA, C1, C2
from statx import rows_full
NUM = ['', 'unu', 'doi', 'trei', 'patru', 'cinci', 'șase', 'șapte', 'opt', 'nouă', 'zece', 'unsprezece', 'doisprezece', 'treisprezece', 'paisprezece', 'cincisprezece', 'șaisprezece']
REP = [('Am strâns 39 de', 'Am strâns treizeci și nouă de'), ('39 de cauze pot', 'Treizeci și nouă de cauze pot'),
       ('La un 2.0 TDI', 'La un doi litri te-de-i'), ('la 2.0 TDI Euro 6', 'la doi litri te-de-i Euro șase'),
       ('19 grame', 'nouăsprezece grame'), ('40 de grame', 'patruzeci de grame'), ('45 de grame', 'patruzeci și cinci de grame'),
       ('Euro 6', 'Euro șase'), ('VW', 'Volkswagen'), ('BMW-uri', 'be-em-ve-uri'), ('NGK', 'En-ge-ca'), ('GM', 'General Motors'),
       ('răcitor EGR', 'răcitor e-ge-re'), ('răcitorul EGR', 'răcitorul e-ge-re'), ('EGR-ul', 'e-ge-re-ul'), ('un EGR', 'un e-ge-re'), ('la EGR', 'la e-ge-re'),
       ('10 până la 20 de minute', 'zece până la douăzeci de minute'), ('75 de grade', 'șaptezeci și cinci de grade'), ('68 de grade', 'șaizeci și opt de grade'),
       ('peste 600 de grade', 'peste șase sute de grade'), ('circa 600 de grade', 'circa șase sute de grade'), ('din 2012', 'din două mii doisprezece'),
       ('Minus 40 de grade', 'Minus patruzeci de grade'), ('1.200 de grade', 'o mie două sute de grade'), ('100 de kilometri', 'o sută de kilometri'),
       ('viza ITP', 'viza i-te-pe'), ('30 până la 40 la sută', 'treizeci până la patruzeci la sută')]
def say(s):
    for a, b in REP: s = s.replace(a, b)
    return s.replace('„', '').replace('”', '')
INTRO = f"Seria „{SERIA}”."
uniq = []; shows = []; eps = {}
def add(show, v, kind):
    if show not in shows:
        shows.append(show); uniq.append(dict(id=len(uniq), show=show, v=v, kind=kind))
    return shows.index(show)
for e in EP:
    ids = []
    for i, r in enumerate(rows_full(e)):
        s = r[0]
        if i == 1 and s.startswith('Seria') and 'Episodul final' not in s:
            a = add(INTRO, say(INTRO), 'intro')
            t = f"Episodul {e['n']} din 16: {e['nume']}."
            b = add(t, f"Episodul {NUM[e['n']]} din șaisprezece: {e['nume']}.", 'ep')
            ids.append([a, b])
        else:
            ids.append([add(s, say(s), 'hook' if i == 0 else 'row')])
    eps[str(e['n'])] = ids
for u in uniq:
    u['prompt'] = ('[serious] ' if u['kind'] == 'hook' else '[calm] ') + u['v']
    assert not re.search(r'\d|[A-Z]{2,}', u['v'].replace('RAR', '').replace('Volkswagen', '')), u['v']
json.dump(dict(lines=uniq, eps=eps), open('vo/lines.json', 'w'), ensure_ascii=False, indent=1)
print(len(uniq), sum(len(u['prompt']) for u in uniq), sum(len(u['v']) for u in uniq), max(len(u['v']) for u in uniq))
