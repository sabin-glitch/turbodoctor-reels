# Planse de verificare: cadre luate din fisierul video (dupa numarul cadrului), micsorate si puse una langa alta.
#   python3 qa_sheet.py <video> <iesire.jpg> <cadre separate prin virgula> [latime_cadru=432] [coloane=6]
import subprocess, sys
import numpy as np, cv2
vid, out, fs = sys.argv[1], sys.argv[2], [int(x) for x in sys.argv[3].split(',')]
w = int(sys.argv[4]) if len(sys.argv) > 4 else 432; cols = int(sys.argv[5]) if len(sys.argv) > 5 else 6
h = w * 16 // 9; ims = []
for f in fs:
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', '%.4f' % max(0.0, f / 30.0 - 0.005), '-i', vid, '-frames:v', '1', '-f', 'image2pipe', '-c:v', 'png', '-'], capture_output=True).stdout
    im = cv2.imdecode(np.frombuffer(raw, np.uint8), cv2.IMREAD_COLOR)
    im = cv2.resize(im, (w, h), interpolation=cv2.INTER_AREA)
    cv2.putText(im, '%d  %d:%05.2f' % (f, f // 1800, (f % 1800) / 30.0), (8, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 4); cv2.putText(im, '%d  %d:%05.2f' % (f, f // 1800, (f % 1800) / 30.0), (8, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    ims.append(im)
while len(ims) % cols: ims.append(np.zeros_like(ims[0]))
rows = [np.hstack(ims[i:i + cols]) for i in range(0, len(ims), cols)]
cv2.imwrite(out, np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 88]); print(out, len(fs), 'cadre')
