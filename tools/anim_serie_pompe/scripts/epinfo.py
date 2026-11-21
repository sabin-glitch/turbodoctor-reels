# epinfo.py N -> datele episodului din document (cadre, surse, deductii) si randurile vocii cu timpii cuvintelor
import sys, json, os
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, H)
import pdata_eps as P
n = int(sys.argv[1]); e = P.EP[n - 1]
for k in ('titlu', 'pompe', 'hook', 'ecran', 'semne', 'lant'):
    print('== %s: %s' % (k, e[k]))
print('== cadre:'); [print('  -', c) for c in e['cadre']]
for k in ('surse', 'site', 'deductie'):
    print('== %s: %s' % (k, e[k]))
Q = json.load(open(os.path.join(H, 'ep%d' % n, 'vo', 'cues.json'))); tl = json.load(open(os.path.join(H, 'ep%d' % n, 'vo', 'timeline.json')))
print('== total %.2f  story_end %.2f' % (tl['total'], tl['story_end']))
for l in Q['lines']:
    i = l['i']; print('%2d %6.2f-%6.2f' % (i, l['start'], l['end']))
    print('    ' + ' '.join('%s@%.2f' % (w['text'], w['s']) for w in Q['words'] if w['win'] == i))
