import json; tl=json.load(open('out/timeline.json'))
print('S0', tl['story_out0'], 'SEND', tl['story_end'], 'TOTAL', tl['total'])
print('COLD:', ' '.join(f"{w['text']}@{w['os']:.2f}" for w in tl['cold_words']))
cur=None
for w in tl['words']:
    if w['win']!=cur: cur=w['win']; print(f"\n[w{cur}]", end=' ')
    print(f"{w['text']}@{w['os']:.2f}", end=' ')
print()
