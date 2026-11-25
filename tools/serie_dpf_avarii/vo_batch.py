import json, sys
N = "4A0kNewFEKohUDWYn2DF wXXDLF3FmUfP7zALrY6l fql3ZDMWn6uiCVFIScVY b2dlAi70ZUu0UVsUwqng keJlMgluVLYsRDZrzOkD gcFSrpnI8Jx2MZNGqNCO QfeQPlO8fSQdTJkQdrgA gEjutHtWhXorNemKiKDB 1pjyNAcMQwc13U7WoWpn ujW9631l7FjBlUj3iSOp 4lvQbZHGevP6AIrWTors WVPNBlLjorsjt66kBzbX 2BvjTcrQlREbKlHtJcvw TJjRpuEFcc2nrgPgAVTv KB5AzkNShClRDlS7BN67 KnueOCb6jdyOuvSnGCR6 Q7NV5Kl1UzkEUCnsAdmD 3eF7WaYdq6B85JTdEWzK AdbLU2uT1ZYIYnoChD6S 5rdwtHzXN998mMFoxvsf".split()
L = json.load(open('vo/lines.json'))['lines']; b = int(sys.argv[1]); ls = L[b*20:(b+1)*20]
print(json.dumps([dict(node_id=N[k], prompt=u['prompt']) for k, u in enumerate(ls)], ensure_ascii=False, separators=(',', ':')))
print(len(ls), sum(len(u['prompt']) for u in ls))
