"""QA for a finished v2 reel: python3 qa.py r0172 /path/to/video.mp4 -> /tmp/qa_<reel>.jpg + sync offsets"""
import sys, json, subprocess, unicodedata, os
import numpy as np, cv2, soundfile as sf, sherpa_onnx
from scipy.signal import resample_poly
reel, vid = sys.argv[1], sys.argv[2]; R = f"/home/claude/reels/{reel}"
tl = json.load(open(f"{R}/out/timeline.json")); D = tl["total"]
ts = list(np.linspace(0.15, D - 0.3, 18))
ims = []
for t in ts:
    p = f"/tmp/qa_{reel}_{t:.2f}.jpg"
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{t:.2f}", "-i", vid, "-frames:v", "1", "-vf", "scale=180:320", p], check=True)
    im = cv2.imread(p); cv2.putText(im, f"{t:.1f}", (4, 20), 0, .6, (0, 0, 0), 3); cv2.putText(im, f"{t:.1f}", (4, 20), 0, .6, (0, 255, 255), 1); ims.append(im); os.remove(p)
cv2.imwrite(f"/tmp/qa_{reel}.jpg", np.vstack([np.hstack(ims[:9]), np.hstack(ims[9:18])]), [cv2.IMWRITE_JPEG_QUALITY, 85])
M = "/home/claude/models/sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8"
rec = sherpa_onnx.OfflineRecognizer.from_transducer(encoder=f"{M}/encoder.int8.onnx", decoder=f"{M}/decoder.int8.onnx", joiner=f"{M}/joiner.int8.onnx", tokens=f"{M}/tokens.txt", num_threads=2, model_type="nemo_transducer")
x, sr = sf.read(f"{R}/audio/mix_final.wav", dtype="float32"); x = x.mean(1); x16 = resample_poly(x, 1, 3).astype(np.float32)
def nm(z): z = unicodedata.normalize('NFD', z.lower()); return ''.join(c for c in z if c.isalnum() and unicodedata.category(c) != 'Mn')
words = [(w['text'], w['os']) for w in tl['words']]; diffs = []
SE = tl['story_end']; S0 = tl['story_out0']
for a in np.arange(S0 + .5, SE - 4, max(6.0, (SE - S0) / 6)):
    b = a + 5.5; s = rec.create_stream(); s.accept_waveform(16000, x16[int(a*16000):int(b*16000)]); rec.decode_stream(s)
    for t, st in zip(s.result.tokens, s.result.timestamps):
        if not t.startswith(' '): continue
        hs = a + st; ht = nm(t)
        c = [(abs(os_ - hs), os_) for tx, os_ in words if a <= os_ < b and len(ht) >= 2 and nm(tx)[:2] == ht[:2]]
        if c:
            d, os_ = min(c)
            if d < .6: diffs.append(hs - os_)
print(f"{reel}: duration {D:.1f}s  sync matched {len(diffs)}  mean {np.mean(diffs):+.3f}s  p90 abs {np.percentile(np.abs(diffs), 90):.3f}s  max {np.max(np.abs(diffs)):.3f}s")
