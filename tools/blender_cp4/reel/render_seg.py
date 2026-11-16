# Randeaza cu compozitorul reelului (subtitrari, titluri, stampile) doar un interval de cadre, intr-un fisier separat:
#   python3 render_seg.py <start> <end>   -> <reel>/out/seg_SSSSS_EEEEE.mp4  (cadrele start .. end-1)
# Bucatile care nu depind de Blender se pot face cat inca randeaza Blender; finish_bl.sh le lipeste si face codarea finala.
# Intermediar de calitate mare (crf 14), ca fisierul livrat sa fie codat o singura data la debitul final.
import base64, os, subprocess, sys, time
R = os.environ.get('REEL_ROOT', '/home/claude/reels/amorsare_filtru'); os.environ['REEL_ROOT'] = R; sys.path.insert(0, R)
import render                     # render.py al reelului: write_data, open_compositor (face chdir in dosarul reelului)
from playwright.sync_api import sync_playwright
a, b = int(sys.argv[1]), int(sys.argv[2])
out = 'out/seg_%05d_%05d.mp4' % (a, b); part = out[:-4] + '.part.mp4'
if os.environ.get('WRITE_DATA', '1') != '0': render.write_data()
with sync_playwright() as pw:
    br, pg, errs = render.open_compositor(pw)
    ce = pg.evaluate("window.CFG_ERR || ''")
    if ce: print('CFG_ERR:', ce)
    cdp = pg.context.new_cdp_session(pg)
    enc = subprocess.Popen(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-f', 'image2pipe', '-framerate', '30', '-c:v', 'mjpeg', '-i', '-',
                            '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '14', '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-r', '30', part], stdin=subprocess.PIPE)
    t0 = time.time()
    for n in range(a, b):
        if n < 4123 and not os.path.exists('frames_base/%05d.jpg' % n): raise FileNotFoundError('frames_base/%05d.jpg' % n)
        pg.evaluate('window.renderFrame(%d)' % n)
        r = cdp.send('Page.captureScreenshot', {'format': 'jpeg', 'quality': 93, 'optimizeForSpeed': True})
        enc.stdin.write(base64.b64decode(r['data']))
        if (n - a) % 150 == 0:
            el = time.time() - t0; done = n - a + 1
            print('frame %d/%d %.1f fps' % (n, b, done / max(el, .01)), flush=True)
    enc.stdin.close(); rc = enc.wait(); br.close()
    if rc != 0: sys.exit('ffmpeg a iesit cu %d' % rc)
os.replace(part, out)
print('segment gata', out, '%.0f s' % (time.time() - t0), 'erori pagina:', errs)
