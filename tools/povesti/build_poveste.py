#!/usr/bin/env python3
"""Poveste #01 v2: source built from lip-synced single-speaker shots (Kling 4 + Sync 3, exact ElevenLabs lines).
Each shot is trimmed around its line, normalized to 1080x1920 / 30 fps; a short freeze-frame after shots A and B
hosts the chapter cards; s6 (signing + leaving) closes the story without dialogue. Output: build2/all.mp4 + timeline_src.json.
"""
import json, os, subprocess
L = "/home/claude/povesti/lipsync"; SH = "/home/claude/povesti/shots"; S = "/home/claude/povesti/src"
OUT = "/home/claude/povesti/build2"; os.makedirs(OUT, exist_ok=True)
def run(cmd): subprocess.run(cmd, check=True)

# (name, file, in, out, freeze_after, line_start_in_file, line_end_in_file, speaker, text)
SHOTS = [
  ("A", f"{L}/sync_A.mp4", 0.00, 8.00, 0.80, 3.25, 7.96, "client", "Iar nu trage. A treia oară luna asta. Gata, mă duc la Turbo Doctor."),
  ("B", f"{L}/sync_B.mp4", 0.05, 9.04, 0.80, 0.40, 8.76, "mecanic", "Ți-am pus turbină de la dezmembrări, 800 de lei. Merge brici. Ce să dai 1.200 pe una recondiționată?"),
  ("C", f"{L}/sync3_d1cu.mp4", 0.15, 5.57, 0.0, 0.50, 5.12, "doctor", "Deci pacientul vine cu aceeași problemă a treia oară. Ce i-ai făcut între timp?"),
  ("D", f"{L}/sync_D.mp4", 0.25, 3.13, 0.0, 0.60, 2.68, "client", "Am reparat ieftin. Era chilipir."),
  ("E", f"{L}/sync_E.mp4", 0.10, 7.91, 0.0, 0.45, 7.46, "doctor", "Ax cu joc, iar cauza n-a atins-o nimeni. 800 de lei de trei ori fac 2.400."),
  ("F", f"{L}/sync_F.mp4", 0.05, 8.96, 0.0, 0.40, 8.51, "doctor", "O turbină recondiționată corect era 1.200, o singură dată. Ieftin te-a costat dublu. Și tot nu merge."),
  ("G", f"{L}/sync_G.mp4", 0.20, 4.86, 0.0, 0.55, 4.41, "client", "Da, ai dreptate. Sunt prea sărac ca să-mi permit lucruri ieftine."),
  ("H", f"{L}/sync_H.mp4", 0.15, 3.77, 0.0, 0.50, 3.32, "doctor", "Exact. Ca la carte, o singură dată."),
  ("I", f"{L}/sync_I.mp4", 0.15, 3.76, 0.0, 0.50, 3.31, "client", "Fă-o cum trebuie. M-am săturat de stresul ăsta."),
  ("Z", f"{S}/s6.mp4", 0.00, 8.00, 0.0, None, None, None, ""),
]
parts_v, parts_a, tl, t = [], [], [], 0.0
for name, f, a, b, frz, ls, le, who, txt in SHOTS:
    dur = b - a
    v = f"{OUT}/{name}_v.mp4"; au = f"{OUT}/{name}_a.wav"
    vf = (f"trim={a}:{b},setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos:force_original_aspect_ratio=increase,crop=1080:1920,"
          f"fps=30,format=yuv420p" + (f",tpad=stop_mode=clone:stop_duration={frz}" if frz else ""))
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", f, "-an", "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "12", v])
    total = dur + frz
    if ls is not None:  # dialogue = the exact track that Sync 3 muxed into its output
        af = f"atrim={a}:{b},asetpts=PTS-STARTPTS,aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=mono,apad=whole_dur={total}"
        run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", f, "-vn", "-af", af, "-c:a", "pcm_s16le", au])
    else:
        run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i", f"anullsrc=r=48000:cl=mono", "-t", f"{total}", "-c:a", "pcm_s16le", au])
    parts_v.append(v); parts_a.append(au)
    tl.append({"shot": name, "start": round(t, 3), "end": round(t + total, 3), "speaker": who, "text": txt,
               "line_start": None if ls is None else round(t + ls - a, 3), "line_end": None if le is None else round(t + le - a, 3)})
    t += total
with open(f"{OUT}/v.txt", "w") as fh: fh.writelines(f"file '{p}'\n" for p in parts_v)
with open(f"{OUT}/a.txt", "w") as fh: fh.writelines(f"file '{p}'\n" for p in parts_a)
run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{OUT}/v.txt", "-c", "copy", f"{OUT}/video.mp4"])
run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{OUT}/a.txt", "-c", "pcm_s16le", f"{OUT}/dialog.wav"])
run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", f"{OUT}/video.mp4", "-i", f"{OUT}/dialog.wav", "-map", "0:v", "-map", "1:a",
     "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", f"{OUT}/all.mp4"])
json.dump({"total": round(t, 3), "shots": tl}, open(f"{OUT}/timeline_src.json", "w"), ensure_ascii=False, indent=1)
for s in tl: print(s["shot"], s["start"], s["end"], s["line_start"], s["line_end"], s["speaker"])
print("total", round(t, 3))
