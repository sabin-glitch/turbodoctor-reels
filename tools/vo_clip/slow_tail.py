"""Încetinire lină a finalului unui clip (fără cadru înghețat și fără sacadare), ca ultimul rând de voice-over să încapă:
  python3 slow_tail.py <clip.mp4> <out.mp4> --from 6.8 --dur 2.0
Coada clipului (de la --from până la sfârșit) e întinsă pe --dur secunde: pornește la viteza normală și încetinește liniar spre oprire.
Cadrele intermediare vin din ffmpeg minterpolate (240 fps, compensare de mișcare), nu din repetarea cadrelor. Restul clipului rămâne neatins.
Ieșirea are 30 fps, crf 10 și o pistă audio mută (new_reel.sh citește durata din audio). Verific pe câteva cadre intermediare că nu apar deformări.
Folosit la „Kit sistem injecție N47” (28.11.2026): --from 6.8 --dur 2.0 pe un clip de 8 s -> 8,8 s."""
import argparse, os, subprocess, tempfile, glob
import cv2
ap = argparse.ArgumentParser(); ap.add_argument("src"); ap.add_argument("out"); ap.add_argument("--from", dest="t0", type=float, required=True); ap.add_argument("--dur", type=float, required=True)
a = ap.parse_args(); FPS, HI = 30, 240
cap = cv2.VideoCapture(a.src); W, H, N = int(cap.get(3)), int(cap.get(4)), int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); n0 = int(round(a.t0 * FPS))
tmp = tempfile.mkdtemp(prefix="tail_")
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{n0 / FPS:.4f}", "-i", a.src, "-an",
                "-vf", f"minterpolate=fps={HI}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1", "-q:v", "1", "-qmin", "1", f"{tmp}/%04d.jpg"], check=True)
M = len(glob.glob(f"{tmp}/*.jpg")); span = (M - 1) / HI          # secunde de sursă acoperite de cadrele interpolate
k = 2 - 2 * span / a.dur                                         # viteza scade liniar de la 1 la 1 - k: s(t) = t - k t² / (2 dur), s(dur) = span
assert 0 < k <= 1, f"--dur trebuie să fie între {span:.2f} și {2 * span:.2f} s pentru această coadă"
enc = subprocess.Popen(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                        "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-shortest", "-c:v", "libx264", "-preset", "slow", "-crf", "10", "-pix_fmt", "yuv420p",
                        "-c:a", "aac", "-b:a", "128k", a.out], stdin=subprocess.PIPE)
for i in range(n0):
    ok, im = cap.read(); assert ok; enc.stdin.write(im.tobytes())
for j in range(int(round(a.dur * FPS))):
    t = j / FPS; s = t - k * t * t / (2 * a.dur); enc.stdin.write(cv2.imread(f"{tmp}/{min(M, 1 + int(round(s * HI))):04d}.jpg").tobytes())
enc.stdin.close(); enc.wait()
print(f"{a.out}: {n0 / FPS + a.dur:.2f} s (coada {span:.2f} s -> {a.dur:.2f} s, viteza finală {1 - k:.2f}x, {M} cadre interpolate)")
