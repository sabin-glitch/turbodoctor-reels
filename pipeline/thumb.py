"""Render the DPF Doctor cover/thumbnail: python3 thumb.py <config.json> <out.jpg>
config: { bg: path to a 1080x1920 frame, zoom, ox, oy, tag, l1, l2, l2Col, l2Size, stamp }"""
import json, os, sys
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.abspath(__file__))
cfg = json.load(open(sys.argv[1])); out = sys.argv[2]
with sync_playwright() as pw:
    b = pw.chromium.launch(args=["--allow-file-access-from-files", "--force-color-profile=srgb", "--disable-gpu", "--hide-scrollbars"])
    pg = b.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.add_init_script("window.THUMB = " + json.dumps(cfg, ensure_ascii=False) + ";")
    pg.goto(f"file://{ROOT}/thumb.html"); pg.wait_for_function("window.READY === true", timeout=30000)
    pg.screenshot(path="/tmp/_thumb.png"); b.close()
    if errs: print("PAGE ERRORS:", errs)
import cv2
im = cv2.imread("/tmp/_thumb.png"); cv2.imwrite(out, im, [cv2.IMWRITE_JPEG_QUALITY, 92])
# grid preview (3:4 centre crop, as TikTok / Instagram profile grids show it)
cv2.imwrite(out.replace(".jpg", "_grila.jpg"), cv2.resize(im[240:1680], (360, 480), interpolation=cv2.INTER_AREA), [cv2.IMWRITE_JPEG_QUALITY, 90])
print("thumb ok", out)
