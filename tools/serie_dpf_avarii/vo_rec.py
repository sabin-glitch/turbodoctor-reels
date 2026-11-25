import json, sys
p = json.load(open('vo/packs.json')); b, asset = sys.argv[1], sys.argv[2]; p['lens'][b] = json.loads(sys.argv[3]); p['assets'][b] = asset
json.dump(p, open('vo/packs.json', 'w'))
