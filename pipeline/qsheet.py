"""quick contact sheet of a finished reel: python3 qsheet.py video.mp4 out.jpg [n]"""
import sys, subprocess, os, numpy as np, cv2
vid, out = sys.argv[1], sys.argv[2]; n = int(sys.argv[3]) if len(sys.argv) > 3 else 18
D = float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",vid]).decode().strip())
ts = list(np.linspace(0.15, D - 0.3, n)); ims = []
for t in ts:
    p = f"/tmp/qs_{os.getpid()}_{t:.2f}.jpg"
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-ss",f"{t:.2f}","-i",vid,"-frames:v","1","-vf","scale=200:356",p],check=True)
    im = cv2.imread(p); cv2.putText(im,f"{t:.1f}",(4,20),0,.6,(0,0,0),3); cv2.putText(im,f"{t:.1f}",(4,20),0,.6,(0,255,255),1); ims.append(im); os.remove(p)
h = n // 2
cv2.imwrite(out, np.vstack([np.hstack(ims[:h]), np.hstack(ims[h:2*h])]), [cv2.IMWRITE_JPEG_QUALITY, 85])
print(out, D)
