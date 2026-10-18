"""Render pipeline: prep assets, preview frames, full render (Chromium compositor -> ffmpeg)."""
import argparse, base64, json, os, subprocess, sys, time
import cv2, numpy as np
from playwright.sync_api import sync_playwright

ROOT = os.environ.get("REEL_ROOT") or os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)


def write_data():
    tl = json.load(open("out/timeline.json"))
    tl["map"] = json.load(open("out/map.json"))
    import glob
    for f in glob.glob("out/track_*.json"): tl[os.path.basename(f)[:-5]] = json.load(open(f))
    if os.path.exists("out/broll_resolved.json"): tl["broll"] = json.load(open("out/broll_resolved.json"))
    open("data.js", "w").write("window.TL = " + json.dumps(tl, ensure_ascii=False) + ";\n")


def outline(png, border=20, shadow=24, off=16):
    im = cv2.imdecode(np.frombuffer(png, np.uint8), cv2.IMREAD_UNCHANGED)
    pad = border + shadow * 2 + off
    im = cv2.copyMakeBorder(im, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=(0, 0, 0, 0))
    art = im[..., :3].astype(np.float32) / 255; a = im[..., 3].astype(np.float32) / 255
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * border + 1, 2 * border + 1))
    dil = cv2.dilate((a > 0.03).astype(np.uint8) * 255, k).astype(np.float32) / 255
    dil = cv2.GaussianBlur(dil, (0, 0), 1.3)
    sh = cv2.GaussianBlur(dil, (0, 0), shadow / 2)
    sh = cv2.warpAffine(sh, np.float32([[1, 0, 0], [0, 1, off]]), (sh.shape[1], sh.shape[0])) * 0.55
    C = np.zeros_like(art); A = sh.copy()
    C = 1.0 * dil[..., None] + C * (1 - dil[..., None]); A = dil + A * (1 - dil)
    C = art * a[..., None] + C * (1 - a[..., None]); A = a + A * (1 - a)
    rgb = np.where(A[..., None] > 1e-4, C / np.maximum(A[..., None], 1e-4), 0)
    out = np.dstack([np.clip(rgb * 255, 0, 255), np.clip(A * 255, 0, 255)]).astype(np.uint8)
    ys, xs = np.where(out[..., 3] > 2)
    return out[max(0, ys.min() - 2):ys.max() + 3, max(0, xs.min() - 2):xs.max() + 3]


def prep(page):
    os.makedirs("assets/stickers", exist_ok=True)
    page.set_content("<html><body style='margin:0;background:transparent'><div id='s' style='display:inline-block'></div></body></html>")
    page.add_script_tag(path="art.js")
    for name, js in [("turbo", "ART.turbo('a')"), ("injector", "ART.injector('b')"), ("glowplug", "ART.glowplug('c')")]:
        page.evaluate(f"""() => {{ const s=document.getElementById('s'); s.innerHTML={js}; const v=s.querySelector('svg');
            v.setAttribute('width', v.viewBox.baseVal.width*2); v.setAttribute('height', v.viewBox.baseVal.height*2); }}""")
        png = page.locator("#s svg").screenshot(omit_background=True)
        cv2.imwrite(f"assets/stickers/{name}.png", outline(png))
    tl = json.load(open("out/timeline.json"))
    n_last = int(tl["story_end"] * tl["fps"]) - 1
    fr = cv2.imread(f"frames_base/{n_last:05d}.jpg")
    fr = cv2.GaussianBlur(fr, (0, 0), 24)
    fr = (fr.astype(np.float32) * 0.40).astype(np.uint8)
    cv2.imwrite("assets/end_bg.jpg", fr, [cv2.IMWRITE_JPEG_QUALITY, 92])


def open_compositor(pw):
    b = pw.chromium.launch(args=["--allow-file-access-from-files", "--disable-web-security", "--force-color-profile=srgb",
                                 "--disable-gpu", "--hide-scrollbars", "--font-render-hinting=none"])
    pg = b.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append("console: " + m.text) if m.type == "error" else None)
    pg.goto(f"file://{ROOT}/compositor.html")
    pg.wait_for_function("window.READY === true", timeout=60000)
    if errs:
        print("PAGE ERRORS:", errs, file=sys.stderr)
    return b, pg, errs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prep", action="store_true")
    ap.add_argument("--test", type=str, default="")
    ap.add_argument("--full", action="store_true")
    ap.add_argument("--start", type=int, default=0)
    ap.add_argument("--end", type=int, default=-1)
    args = ap.parse_args()
    write_data()
    with sync_playwright() as pw:
        if args.prep:
            b = pw.chromium.launch(); pg = b.new_page(); prep(pg); b.close(); print("prep done")
        b, pg, errs = open_compositor(pw)
        ce = pg.evaluate("window.CFG_ERR || ''")
        if ce: print("CFG_ERR:", ce)
        json.dump(pg.evaluate("window.SFX"), open("out/sfx.json", "w"), indent=0)
        json.dump(pg.evaluate("window.CHUNKS_DEBUG"), open("out/chunks.json", "w"), ensure_ascii=False, indent=0)
        cdp = pg.context.new_cdp_session(pg)
        if args.test:
            os.makedirs("preview", exist_ok=True)
            for tt in args.test.split(","):
                n = int(round(float(tt) * 30))
                pg.evaluate(f"window.renderFrame({n})")
                r = cdp.send("Page.captureScreenshot", {"format": "jpeg", "quality": 90})
                open(f"preview/t{float(tt):06.2f}.jpg", "wb").write(base64.b64decode(r["data"]))
            print("errors:", errs)
        if args.full:
            n_total = json.load(open("out/frames_meta.json"))["n_out"]
            end = n_total if args.end < 0 else args.end
            enc = subprocess.Popen(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "image2pipe", "-framerate", "30",
                                    "-c:v", "mjpeg", "-i", "-", "-c:v", "libx264", "-preset", "fast", "-crf", "19",
                                    "-maxrate", "11M", "-bufsize", "22M", "-profile:v", "high", "-pix_fmt", "yuv420p",
                                    "-r", "30", "out/video_noaudio.mp4"], stdin=subprocess.PIPE)
            t0 = time.time()
            for n in range(args.start, end):
                pg.evaluate(f"window.renderFrame({n})")
                r = cdp.send("Page.captureScreenshot", {"format": "jpeg", "quality": 93, "optimizeForSpeed": True})
                enc.stdin.write(base64.b64decode(r["data"]))
                if n % 150 == 0:
                    el = time.time() - t0; done = n - args.start + 1
                    print(f"frame {n}/{end} {done / el:.1f} fps, eta {(end - n) / max(.1, done / el) / 60:.1f} min", flush=True)
            enc.stdin.close(); enc.wait()
            print("render done", time.time() - t0, "errors:", errs)
        b.close()


if __name__ == "__main__":
    main()
