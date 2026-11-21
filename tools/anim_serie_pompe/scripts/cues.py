# cues.py N -> randurile vocii episodului N, cu timpul fiecarui cuvant (pentru regie)
import sys, json, os
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
n = int(sys.argv[1]); Q = json.load(open(os.path.join(H, 'ep%d' % n, 'vo', 'cues.json'))); tl = json.load(open(os.path.join(H, 'ep%d' % n, 'vo', 'timeline.json')))
print('total %.2f  story_end %.2f' % (tl['total'], tl['story_end']))
for l in Q['lines']:
    i = l['i']; print('%2d %6.2f-%6.2f' % (i, l['start'], l['end']))
    print('    ' + ' '.join('%s@%.2f' % (w['text'], w['s']) for w in Q['words'] if w['win'] == i))
