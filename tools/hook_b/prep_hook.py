"""Retrofit hook B (synthetic intro) into an existing reel folder: prep_hook.py <slug> [--stage prep|post]
prep: back up the pre-intro files, copy the intro pipeline files, write out/intro_script.json and the intro block in reel.js.
post (after intro_vo.py + build_timeline + retime): shift track_*.json by the intro frames, set the cover in the intro."""
import json, os, re, shutil, sys, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hook_specs import SPECS
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.normpath(f"{HERE}/../../pipeline"); CTA = os.path.normpath(f"{HERE}/../../assets/cta_turbo_doctor.wav")
slug, stage = sys.argv[1], (sys.argv[3] if len(sys.argv) > 3 else "prep")
R = f"/home/claude/reels/{slug}"; S = SPECS[slug]; B = f"{R}/bak"


def js(v): return json.dumps(v, ensure_ascii=False).replace('"', "'")


if stage == "prep":
    if not os.path.exists(B):
        os.makedirs(B)
        for f in ["reel.js", "out/timeline.json", "out/timeline_1x.json", "out/cover_t.json", "out/frames_meta.json"] + [os.path.relpath(p, R) for p in glob.glob(f"{R}/out/track_*.json")]:
            if os.path.exists(f"{R}/{f}"): os.makedirs(os.path.dirname(f"{B}/{f}"), exist_ok=True); shutil.copy2(f"{R}/{f}", f"{B}/{f}")
    shutil.copy2(f"{REPO}/compositor_template.html", f"{R}/compositor.html")
    for f in ["intro.js", "intro_vo.py", "audio.py", "build_timeline.py", "retime.py", "extract_frames.py"]: shutil.copy2(f"{REPO}/{f}", f"{R}/{f}")
    shutil.copy2(CTA, f"{R}/out/cta_turbo_doctor.wav")
    tl = json.load(open(f"{B}/out/timeline.json")); bg = next(s["src_a"] for s in tl["segments"] if s["kind"] == "story")
    ph = [dict(text=p[0], gap=p[1], **({"say": p[2]} if len(p) > 2 else {})) for p in S["phrases"]] + [dict(text="Ascultă mai departe pe Turbo Doctor!", wav="cta_turbo_doctor.wav")]
    json.dump(dict(speed=1.15, tail=.5, bg_src=bg, takes=8, phrases=ph), open(f"{R}/out/intro_script.json", "w"), ensure_ascii=False, indent=1)
    cards = []
    for c in S["cards"]:
        t0 = c[3] if len(c) > 3 and c[3] else "null"; mk = js(c[4]) if len(c) > 4 else None
        cards.append(f"[{js(c[0])},{js(c[1])},{js(c[2])}" + (f",{t0},{mk}" if mk else (f",{t0}" if t0 != "null" else "")) + "]")
    extra = "".join(f", {k}: {js(S[k])}" for k in ("q", "mark") if k in S)
    block = (f"    intro: {{ type: 'board', tag: {js(S['tag'])}, ctaPh: {len(ph) - 1}, mergeAt: {js(S['mergeAt'])}, causeAt: {js(S['causeAt'])}, causeTxt: {js(S['causeTxt'])}{extra},\n"
             f"      cards: [{', '.join(cards)}] }},\n"
             f"    tags: {{ '-1': {{ {', '.join(f'{k}: {js(v)}' for k, v in S['tags'].items())} }} }},\n")
    src = open(f"{B}/reel.js").read(); assert src.count("\n  return {\n") == 1, "return { not found once"
    # the clip now starts at S0 (= intro end): bare-number times were written from the clip's start, so they become S0 + n
    TK = r"(?<![\w.])(t0|t|t1|at|at2|l1At|l2At|carAt|chipsAt|end)(\s*:\s*)(\d*\.?\d+)(?=\s*[,}\]])"
    src, n1 = re.subn(TK, r"\1\2S0 + \3", src)
    src, n2 = re.subn(r"(const\s+HE\s*=\s*)(\d*\.?\d+)(\s*;)", r"\1S0 + \2\3", src)
    assert re.search(r"REEL_CFG = \(\{[^}]*\bS0\b", src), "S0 not passed to REEL_CFG"
    src = src.replace("\n  return {\n", "\n  return {\n" + block, 1)
    src = re.sub(r"^// v2 – ", "// v2 (hook B: intro sintetic cu 3 probleme ale clientului) – ", src, count=1)
    open(f"{R}/reel.js", "w").write(src); print(slug, "prep ok, bg_src", bg, "| times moved after the intro:", n1 + n2)
else:
    tl = json.load(open(f"{R}/out/timeline.json")); d = round(tl["intro"]["dur"] * 30); ij = json.load(open(f"{R}/out/intro.json"))
    for p in glob.glob(f"{B}/out/track_*.json"):
        old = json.load(open(p)); json.dump({str(int(k) + d): v for k, v in old.items()}, open(f"{R}/out/{os.path.basename(p)}", "w"))
        print("shifted", os.path.basename(p), "+", d)
    from unicodedata import normalize, category
    n = lambda s: "".join(ch for ch in normalize("NFD", s.lower()) if category(ch) != "Mn" and ch.isalnum())
    ca = next(w["s"] for w in ij["words"] if n(w["text"]) == n(S["causeAt"])); ct = min(ca + .55, ij["phrases"][-1]["t0"] - .3)  # label fully in, before the CTA
    json.dump(dict(t=round(ct, 2)), open(f"{R}/out/cover_t.json", "w")); print(slug, "intro", tl["intro"]["dur"], "cover", round(ct, 2))
