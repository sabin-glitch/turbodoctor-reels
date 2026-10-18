"""Print Parakeet words with absolute start times per context window: python3 toks.py [win ...]"""
import json, sys
ctx = json.load(open("out/transcript_ctx.json"))
sel = [int(a) for a in sys.argv[1:]] or range(len(ctx))
for i in sel:
    w = ctx[i]; words = []; cur = None
    for tok, ts in zip(w["tokens"], w["token_ts"]):
        if tok.startswith(" ") or cur is None:
            cur = [tok.strip(), ts]; words.append(cur)
        else: cur[0] += tok
    print(f"--- win {i} [{w['start']}-{w['end']}]")
    print("  ".join(f"{t:.2f}:{x}" for x, t in words))
