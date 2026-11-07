"""Build the cut (1x) and accelerated sources from src/cfr.mp4: one encode per segment, then concat demuxer (low memory)."""
import subprocess, json, os
SRC = "/home/claude/reels/asamblare_turbina_timelapse/src/cfr.mp4"
V1 = [(5, 38), (46, 66), (71, 127), (127, 143), (163, 169), (179, 187), (197, 203), (207, 213), (217, 221), (231, 235), (235, 255), (261, 281), (297, 305), (313, 319), (325, 331)]
V2 = [(5, 21.5, 2.0), (21.5, 38, 2.0), (46, 66, 3.0), (71, 119, 3.0), (119, 143, 3.0), (163, 169, 4.0), (179, 187, 4.0), (197, 203, 4.0), (207, 213, 4.0), (217, 221, 4.0), (231, 235, 4.0),
      (235, 255, 2.5), (261, 267, 2.0), (267, 281, 3.0), (297, 305, 2.5), (313, 319, 2.0), (325, 331, 1.3)]
def build(name, segs):
    os.makedirs(name, exist_ok=True); out_t = 0.0; table = []; lst = []
    for i, s in enumerate(segs):
        a, b = s[0], s[1]; sp = s[2] if len(s) > 2 else 1.0; d = (b - a) / sp
        vf = f"setpts=(PTS-STARTPTS)/{sp},fps=30"
        af = f"afade=t=in:st=0:d=0.02,afade=t=out:st={d-0.02:.3f}:d=0.02" if sp == 1.0 else f"atempo={min(sp,2.0)}" + (f",atempo={sp/2.0}" if sp > 2 else "") + ",volume=0"
        f = f"{name}/seg{i:02d}.mp4"
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", str(a), "-to", str(b), "-i", SRC, "-vf", vf, "-af", af, "-t", f"{d:.3f}",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "10", "-pix_fmt", "yuv420p", "-g", "30", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2", f], check=True)
        lst.append(f"file '{os.path.abspath(f)}'"); table.append(dict(src_a=a, src_b=b, speed=sp, out_a=round(out_t, 3), out_b=round(out_t + d, 3))); out_t += d
    open(f"{name}/list.txt", "w").write("\n".join(lst) + "\n")
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{name}/list.txt", "-c", "copy", f"{name}.mp4"], check=True)
    json.dump(table, open(f"{name}_edl.json", "w"), indent=1); print(name, "total", round(out_t, 2), "s")
build("v1_cut", V1); build("v2_fast", V2)
