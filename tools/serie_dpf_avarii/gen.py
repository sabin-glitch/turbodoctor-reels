# -*- coding: utf-8 -*-
import sys
from episoade import EP
from statx import rows_full

def dur(e):
    c = sum(len(x[0]) for x in rows_full(e))
    s = round((c / 13.6 + 6) / 5) * 5
    return f"{int(s // 60)} min {int(s % 60):02d} s"

def md_ep(e):
    r = rows_full(e)
    h = f"### Episodul final · {e['titlu']}" if e.get('final') else f"### {e['n']} · {e['titlu']}"
    lead = (f"{len(r)} rânduri, durată estimată {dur(e)}." if e.get('final')
            else f"Numele din formulă: {e['nume']}. {len(r)} rânduri, durată estimată {dur(e)}.")
    out = [h, '', lead, '', '| # | Text rostit | Imagine | Pe ecran | Sursa |', '| --- | --- | --- | --- | --- |']
    for k, (v, i, s, src) in enumerate(r, 1):
        cells = [str(k), v, i, s, src]
        out.append('| ' + ' | '.join(c.replace('|', '/') for c in cells) + ' |')
    return '\n'.join(out)

if __name__ == '__main__':
    import json
    if sys.argv[1] == 'json':            # python3 gen.py json 1 3  -> un șir JSON cu tabelele episoadelor 1..3 (de lipit în document)
        a, b = int(sys.argv[2]), int(sys.argv[3])
        print(json.dumps('\n\n'.join(md_ep(EP[k - 1]) for k in range(a, b + 1)), ensure_ascii=False))
    else:
        print(md_ep(EP[int(sys.argv[1]) - 1]))

def md_doc(e):                            # tabelul din document: fără coloana „Pe ecran” (rămâne în episoade.py)
    r = rows_full(e)
    h = f"### Episodul final · {e['titlu']}" if e.get('final') else f"### {e['n']} · {e['titlu']}"
    out = [h, '', f"{len(r)} rânduri, durată estimată {dur(e)}.", '', '| # | Text rostit | Imagine | Sursa |', '| --- | --- | --- | --- |']
    for k, (v, i, s, src) in enumerate(r, 1):
        out.append('| ' + ' | '.join(c.replace('|', '/') for c in (str(k), v, i, src)) + ' |')
    return '\n'.join(out)
