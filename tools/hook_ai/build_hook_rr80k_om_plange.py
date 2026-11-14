"""Range Rover Velar 3.0 biturbo, „revizia de 80.000 km” (14.11.2026): hook = AI clip of a man crying at the service
reception (Veo 3.1 Fast via ElevenLabs, 9:16, with his sobbing), over Sabin's first phrase („Range Rover, 3.0, Velar,
biturbo”); Sabin's footage takes over just before „Venit la revizie”. His voice is untouched (PRE = 0: the clip already
starts with ~1 s of silence before „Range Rover”, now filled by the sobbing).
Writes:
  <W>/hook_src.mp4    video 1080x1920/30 fps (AI hook + clip from CUT), audio = the clip's own audio, unchanged
  <W>/hook_bed.wav    48 kHz stereo sobbing for the hook only (mixed by audio.py as a 'bed', ducked under the voice)
  <W>/hook_meta.json  markers for reel.js
Run: python3 -I build_hook_rr80k_om_plange.py <W> (W holds all.mp4 and ai/ai_rr80k_om_plange_v1.mp4/.wav)"""
import json, subprocess, sys
import numpy as np, soundfile as sf, cv2

W = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/work"
AI_V = f"{W}/ai/ai_rr80k_om_plange_v1.mp4"; AI_A = f"{W}/ai/ai_rr80k_om_plange_v1.wav"; ALL = f"{W}/all.mp4"
FPS = 30; SR = 48000
CUT_F = 156                      # 5.200 s: Sabin's footage from here („Venit” starts at 5.29)
CUT = CUT_F / FPS
AI_OFF = 0.0                     # AI 0.0 = crying over the invoice (best first frame), then hand to mouth, then looks up
Z0, Z1, ZC = 1.0, 1.075, (540, 720)   # slow push-in on his face over the hook

# ---------------- audio bed: his sobbing, -24 dBFS RMS on the sobs, fade-out at the cut ----------------
a, sr = sf.read(AI_A, dtype="float64"); assert sr == SR
if a.ndim == 1: a = np.stack([a, a], 1)
bed = a[int(AI_OFF * SR):int((AI_OFF + CUT + .02) * SR)].copy()
env = np.sqrt(np.convolve(bed.mean(1) ** 2, np.ones(int(.05 * SR)) / int(.05 * SR), mode="same"))
loud = bed[env > np.percentile(env, 70)]
g = 10 ** ((-24 - 20 * np.log10(np.sqrt(np.mean(loud ** 2)) + 1e-12)) / 20); bed *= g
# +6 dB on the sobbing before his first word („Range Rover” at 1.02 s), so the crying carries the first second of the hook
VO1 = 1.0; tt = np.arange(len(bed)) / SR; bed *= np.interp(tt, [0, VO1 - .08, VO1 + .04], [2.0, 2.0, 1.0])[:, None]
pk = np.abs(bed).max(); bed *= min(1.0, .89 / pk)
fo = int(.06 * SR); bed[int(CUT * SR) - fo:int(CUT * SR)] *= np.linspace(1, 0, fo)[:, None]; bed[int(CUT * SR):] = 0
bed[:int(.004 * SR)] *= np.linspace(0, 1, int(.004 * SR))[:, None]
sf.write(f"{W}/hook_bed.wav", bed.astype(np.float32), SR, subtype="FLOAT")

# ---------------- video: AI frames for [0, CUT), nearest frame at 30 fps, slow push-in ----------------
cap = cv2.VideoCapture(AI_V); afps = cap.get(cv2.CAP_PROP_FPS) or 24; fr = []
while True:
    ok, im = cap.read()
    if not ok: break
    fr.append(im)
ease = lambda p: p * p * (3 - 2 * p)
enc = subprocess.Popen(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "1080x1920",
                        "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "10", "-pix_fmt", "yuv420p",
                        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", f"{W}/hook_video.mp4"], stdin=subprocess.PIPE)
for f in range(CUT_F):
    t = AI_OFF + f / FPS; im = fr[max(0, min(len(fr) - 1, int(round(t * afps))))]
    if im.shape[:2] != (1920, 1080): im = cv2.resize(im, (1080, 1920), interpolation=cv2.INTER_LANCZOS4)
    z = Z0 + (Z1 - Z0) * ease(f / max(1, CUT_F - 1))
    M = np.float32([[z, 0, (1 - z) * ZC[0]], [0, z, (1 - z) * ZC[1]]])
    enc.stdin.write(cv2.warpAffine(im, M, (1080, 1920), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT).tobytes())
enc.stdin.close(); assert enc.wait() == 0

# hook + Sabin's clip from CUT (frame-exact), with the clip's own audio from 0 (no delay)
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", f"{W}/hook_video.mp4", "-i", ALL,
                "-filter_complex", f"[0:v]setsar=1[h];[1:v]trim=start_frame={CUT_F},setpts=PTS-STARTPTS,setsar=1[c];[h][c]concat=n=2:v=1:a=0[v]",
                "-map", "[v]", "-map", "1:a", "-c:v", "libx264", "-preset", "veryfast", "-crf", "10", "-pix_fmt", "yuv420p",
                "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
                f"{W}/hook_src.mp4"], check=True)
meta = dict(CUT=CUT, CUT_F=CUT_F, AI_OFF=AI_OFF, ai_frames=len(fr), ai_fps=afps, zoom=[Z0, Z1, ZC])
json.dump(meta, open(f"{W}/hook_meta.json", "w"), indent=1); print(json.dumps(meta))
