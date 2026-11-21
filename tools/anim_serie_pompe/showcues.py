import json, sys
def show(n):
    c = json.load(open(f'/home/claude/w/serpmp/ep{n}/vo/cues.json')); tl = json.load(open(f'/home/claude/w/serpmp/ep{n}/vo/timeline.json'))
    print('EP', n, 'total', tl['total'], 'story_end', round(tl['story_end'], 2))
    for l in c['lines'][2:len(c['lines']) - 3]:
        ws = [w for w in c['words'] if w['win'] == l['i']]
        print('L%d %.2f-%.2f | %s' % (l['i'], l['start'], l['end'], ' '.join('%s@%.1f' % (w['text'], w['s']) for w in ws)))
    print('OUT at %.2f' % c['lines'][len(c['lines']) - 3]['start'])
for a in sys.argv[1:]: show(int(a))
