"""Compositor for the 4-cylinder engine animation (skia-python + ffmpeg).

  vsk/bin/python comp.py loops [shot ...]   -> out/video/TurboDoctor_Motor4_<shot>_bucla.mp4  (3 seamless cycles, fundal + marcaj fix)
                                               out/video/TurboDoctor_Motor4_<shot>_alfa.webm  (1 ciclu, VP9 cu transparenta, pentru montaje)
  vsk/bin/python comp.py film               -> out/video/TurboDoctor_Motor_4_cilindri_3D.mp4  (prezentare cu etichete, ~35 s)
  vsk/bin/python comp.py png 1.5,9.0        -> out/proof/film_<t>.png
Frames come from out/frames/<shot>/f%04d.png (render.py), anchors from out/info.json (build.py).
"""
import sys, os, json, math, subprocess
from functools import lru_cache
import numpy as np, skia
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from fk import *

M4 = os.path.dirname(HERE)
OUT = os.path.join(M4, 'out')
VID = os.path.join(OUT, 'video'); os.makedirs(VID, exist_ok=True)
INFO = json.load(open(os.path.join(OUT, 'info.json')))
Y, WHT, BG = '#ffc21a', '#ffffff', '#0a1220'
C_HP, C_LP, C_OIL, C_AIR, C_FLAME, C_EXH = '#ff6a3d', '#2f8cff', '#ffb52e', '#8cc8ff', '#ffc24d', '#8a7d72'
SAMP = skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kNone)


def nframes(shot):
    return len(INFO[shot]['thetas'])


@lru_cache(maxsize=48)
def frame_img(shot, k):
    p = os.path.join(OUT, 'frames', shot, f'f{k % nframes(shot):04d}.png')
    if not os.path.exists(p): return None
    return skia.Image.open(p)


# ------------------------------------------------------------------ background (same look as the CRI2 film) + watermark
def background(c, t, moving=True):
    c.drawRect(skia.Rect.MakeWH(W, H), P(shader=lin(0, 0, 0, H, ['#0e1a2c', '#060b14'])))
    c.drawCircle(540, 900, 860, P(shader=rad(540, 900, 860, [skia.Color4f(.13, .21, .34, .55).toColor(), skia.Color4f(0, 0, 0, 0).toColor()])))
    c.save(); c.rotate(-20, 540, 960)
    f = font('anton', 58); s = 'TURBO DOCTOR'; w = f.measureText(s) + 120
    off = (t * 9) % w if moving else 0.0
    for row in range(-14, 22):
        yy = row * 110; sh = (row % 2) * w / 2
        for k in range(-3, 7):
            x = -400 + k * w + sh + off
            col = (1, 1, 1, .04) if (row + k) % 3 else (1, .76, .1, .052)
            c.drawString(s, x, yy, f, P(col[:3], col[3]))
    c.restore()


def draw_frame(c, shot, k, alpha=1.0):
    im = frame_img(shot, k)
    if im is None or alpha <= 0.003: return
    p = skia.Paint(); p.setAlphaf(min(1.0, alpha))
    c.drawImage(im, 0, 0, SAMP, p)


# ------------------------------------------------------------------ UI pieces
def label(c, text, ax, ay, lx, ly, a, side='r', size=28, dot=Y):
    if a <= 0.01: return
    w_ = tw(text, size, 'm8')
    c.drawCircle(ax, ay, 6.5, P('#0b1424', a * 0.9)); c.drawCircle(ax, ay, 5, P(dot, a)); c.drawCircle(ax, ay, 11, P(dot, a * 0.35, stroke=2))
    ex = lx - 6 if side == 'r' else lx + 6
    c.drawPath(path_of([(ax, ay), (ex, ly)]), P('#0b1424', a * 0.7, stroke=5))
    c.drawPath(path_of([(ax, ay), (ex, ly)]), P(dot, a * 0.9, stroke=2.4))
    x0 = lx if side == 'r' else lx - w_ - 28
    rrect(c, x0, ly - size * 0.88, x0 + w_ + 28, ly + size * 0.50, 12, P('#0b1424', a * 0.9))
    rrect(c, x0, ly - size * 0.88, x0 + w_ + 28, ly + size * 0.50, 12, P(dot, a * 0.6, stroke=2))
    txt(c, text, x0 + 14, ly, size, 'm8', WHT, a)


def wrap_lines(text, size, name, maxw):
    out, cur = [], ''
    for wd in text.split():
        cand = (cur + ' ' + wd).strip()
        if tw(cand, size, name) > maxw and cur: out.append(cur); cur = wd
        else: cur = cand
    return out + [cur]


def caption(c, title, body, a, y0=1630):
    if a <= 0.01: return
    dy = 16 * (1 - a)
    txt(c, title, 64, y0 + dy, 54, 'anton', Y, a, shadow=10)
    yy = y0 + 60 + dy
    for ln in wrap_lines(body, 34, 'm7', 950):
        txt(c, ln, 64, yy, 34, 'm7', WHT, a, shadow=8); yy += 46


def legend(c, items, a, y=1872):
    if a <= 0.01: return
    x = 64
    for col, s in items:
        c.drawRoundRect(skia.Rect.MakeXYWH(x, y - 22, 26, 26), 6, 6, P(col, a))
        txt(c, s, x + 38, y, 25, 'm7', WHT, a * 0.9); x += 38 + tw(s, 25, 'm7') + 30


def header(c, a=1.0):
    txt(c, 'MOTOR DIESEL 4 CILINDRI', 60, 108, 54, 'anton', WHT, a, shadow=8)
    txt(c, 'common rail · secțiune 3D', 62, 152, 28, 'm7', WHT, a * 0.82)
    txt(c, 'MODEL 3D RECONSTRUIT · MIȘCARE ÎNCETINITĂ', 1020, 62, 19, 'm8', WHT, 0.45, 'r')


def vignette(c):
    c.drawRect(skia.Rect.MakeLTRB(0, 1440, W, H), P(shader=lin(0, 1440, 0, 1640, [skia.Color4f(0.02, 0.04, 0.07, 0.0).toColor(), skia.Color4f(0.02, 0.04, 0.07, 0.86).toColor()])))
    c.drawRect(skia.Rect.MakeLTRB(0, 0, W, 240), P(shader=lin(0, 0, 0, 240, [skia.Color4f(0.02, 0.04, 0.07, 0.78).toColor(), skia.Color4f(0.02, 0.04, 0.07, 0.0).toColor()])))


def anch(shot, key):
    p = INFO[shot]['anch'][key]; return p[0], p[1]


# ------------------------------------------------------------------ film timeline
# (shot, start s, duration s, number of loops shown)
SEQ = [('A_motor', 0.0, 7.6), ('D_cilindru', 7.6, 6.4), ('E_supape', 14.0, 7.2), ('B_pompa_inalta', 21.2, 6.0), ('C_pompa_ulei', 27.2, 6.0)]
END = 33.2
DUR = END + 2.6
XF = 0.5   # crossfade

# world anchor points (mm) used by the labels (projected with each shot camera)
WA = {
    'curea': (-240.0, 113.0, 255.0), 'pompa_ip': (-205.0, -112.0, 235.0), 'ax_came': (75.0, -38.0, 378.0), 'rampa': (60.0, 0.0, 442.0),
    'injector': (44.0, 0.0, 345.0), 'piston': (44.0, -28.0, 175.0), 'arbore': (14.0, -20.0, -26.0), 'pompa_ulei': (-183.0, -30.0, -92.0),
    'volanta': (225.0, -70.0, -60.0), 'baie': (40.0, -60.0, -128.0),
    # cylinder close-up
    'D_inj': (-44.0, -6.0, 282.0), 'D_gp': (-44.0, -28.0, 278.0), 'D_vi': (-60.5, -18.0, 262.0), 'D_bol': (-44.0, -24.0, 228.0), 'D_duza': (-44.0, 0.0, 238.6),
    # valves (transverse section through x = -60.5)
    'E_cam': (-60.5, -38.0, 366.5), 'E_fol': (-60.5, -52.0, 340.0), 'E_hla': (-60.5, -64.0, 322.0), 'E_spr': (-60.5, -28.0, 300.0),
    'E_vi': (-60.5, -18.0, 262.0), 'E_ve': (-60.5, 18.0, 262.0), 'E_pi': (-60.5, -55.0, 275.0), 'E_pe': (-60.5, 55.0, 275.0),
    # HP pump (section x = -183, pump shaft at y=-112, z=210)
    'B_cam': (-183.0, -112.0, 214.0), 'B_rol': (-183.0, -112.0, 232.0), 'B_pl': (-183.0, -112.0, 280.0), 'B_out': (-183.0, -96.0, 294.0),
    'B_in': (-183.0, -112.0, 305.0), 'B_mu': (-183.0, -150.0, 256.0), 'B_spr': (-183.0, -103.0, 262.0),
    # oil pump (section x = -183, shaft at z=-92)
    'C_rot': (-183.0, 0.0, -92.0), 'C_van': (-183.0, 20.0, -86.0), 'C_out': (-183.0, -60.0, -50.0), 'C_sorb': (-183.0, 20.0, -140.0),
}

LABELS = {
    # shot: [(text, world anchor, (lx, ly), side, t_in)]
    'A_motor': [('Curea de distribuție', 'curea', (64, 250), 'r', 0.8), ('Pompa de înaltă presiune', 'pompa_ip', (64, 330), 'r', 1.2),
                ('Ax cu came', 'ax_came', (590, 250), 'r', 1.6), ('Rampa comună', 'rampa', (590, 330), 'r', 2.0),
                ('Injector', 'injector', (840, 420), 'r', 2.4), ('Pompa de ulei', 'pompa_ulei', (64, 1430), 'r', 2.8),
                ('Arbore cotit', 'arbore', (420, 1430), 'r', 3.2), ('Volantă', 'volanta', (790, 1430), 'r', 3.6)],
    'D_cilindru': [('Injector', 'D_inj', (760, 820), 'r', 0.4), ('Bujie incandescentă', 'D_gp', (64, 760), 'r', 0.8),
                   ('Supapă de admisie', 'D_vi', (64, 1380), 'r', 1.2), ('Camera de ardere', 'D_bol', (650, 1440), 'r', 1.6)],
    'E_supape': [('Ax cu came', 'E_cam', (720, 300), 'r', 0.4), ('Culbutor cu rolă', 'E_fol', (720, 380), 'r', 0.8),
                 ('Element hidraulic', 'E_hla', (720, 460), 'r', 1.2), ('Arcul supapei', 'E_spr', (720, 540), 'r', 1.6),
                 ('Supapă de admisie', 'E_vi', (720, 900), 'r', 2.0), ('Supapă de evacuare', 'E_ve', (64, 900), 'r', 2.0)],
    'B_pompa_inalta': [('Spre rampă', 'B_out', (64, 380), 'r', 0.4), ('Pistonaș', 'B_pl', (760, 560), 'r', 0.8),
                       ('Dozator', 'B_mu', (760, 900), 'r', 1.2), ('Tachet cu rolă', 'B_rol', (64, 1250), 'r', 1.6), ('Camă dublă', 'B_cam', (64, 1340), 'r', 2.0)],
    'C_pompa_ulei': [('Rotor cu palete', 'C_rot', (690, 1270), 'r', 0.4), ('Spre galeria de ulei', 'C_out', (64, 460), 'r', 0.8),
                     ('Sorb', 'C_sorb', (690, 1370), 'r', 1.2)],
}
CAPS = {
    'A_motor': ('MOTORUL ÎN SECȚIUNE', 'Ordinea de aprindere 1-3-4-2: la fiecare jumătate de tură a arborelui cotit, alt cilindru e în timpul motor.'),
    'D_cilindru': ('INJECȚIA ȘI ARDEREA', 'Pilot, apoi injecția principală în bolul pistonului; motorina se aprinde în aerul comprimat. Bujia ajută pornirea la rece.'),
    'E_supape': ('SUPAPELE', 'Cama apasă culbutorul cu rolă, supapa se deschide; arcul o închide la loc. Elementul hidraulic preia jocul.'),
    'B_pompa_inalta': ('POMPA DE ÎNALTĂ PRESIUNE', 'Antrenată de curea, la turația motorului. Cama dublă împinge pistonașul de două ori pe tură; motorina pleacă spre rampă.'),
    'C_pompa_ulei': ('POMPA DE ULEI', 'Paletele aspiră uleiul din baie prin sorb și îl împing sub presiune spre galeria de ungere a motorului.'),
}
LEG = {
    'A_motor': [(C_HP, 'motorină înaltă presiune'), (C_OIL, 'ulei')],
    'D_cilindru': [(C_HP, 'motorină'), (C_FLAME, 'flacără'), (C_AIR, 'aer')],
    'E_supape': [(C_AIR, 'aer admisie'), (C_EXH, 'gaze evacuare')],
    'B_pompa_inalta': [(C_LP, 'joasă presiune'), (C_HP, 'înaltă presiune')],
    'C_pompa_ulei': [(C_OIL, 'ulei aspirat'), ('#ff8a1c', 'ulei sub presiune')],
}


def shot_at(t):
    """list of (shot, local time, alpha) active at film time t"""
    out = []
    for i, (s, t0, d) in enumerate(SEQ):
        t1 = t0 + d
        a_in = 1.0 if i == 0 else ramp(t, t0 - XF / 2, XF)
        a_out = 1.0 - (ramp(t, t1 - XF / 2, XF) if i < len(SEQ) - 1 else ramp(t, END - 0.2, 0.6))
        if t0 - XF / 2 <= t <= t1 + XF / 2 and a_in * a_out > 0.003:
            out.append((s, t - t0, a_in * a_out))
    return out


def endcard(c, a):
    if a <= 0.01: return
    c.drawRect(skia.Rect.MakeWH(W, H), P('#060b14', a * 0.94))
    txt(c, 'TURBO', 540, 820, 170, 'anton', WHT, a, 'c')
    txt(c, 'DOCTOR', 540, 995, 170, 'anton', Y, a, 'c')
    txt(c, 'Diagnoză · Turbo · Injectoare · Pompe', 540, 1090, 36, 'm7', WHT, a * 0.9, 'c')
    txt(c, 'GALAȚI · BUCUREȘTI · IAȘI · PIATRA NEAMȚ', 540, 1180, 30, 'm8', WHT, a * 0.85, 'c')


def film_frame(t):
    surf = skia.Surface(W, H); c = surf.getCanvas()
    background(c, t, moving=True)
    act = shot_at(t)
    for s, lt, a in act:
        k = int(math.floor(lt * FPS + 1e-6))
        if lt < 0: k = 0
        draw_frame(c, s, k, a)
    vignette(c)
    header(c)
    for s, lt, a in act:
        d = dict((q[0], q[2]) for q in SEQ)[s]
        for (text, key, (lx, ly), side, tin) in LABELS.get(s, []):
            la = a * win(lt, tin, d - 0.3, 0.35, 0.3)
            if la > 0.01:
                ax, ay = project(s, WA[key]) if key in WA else anch(s, key)
                label(c, text, ax, ay, lx, ly, la, side, size=27)
        ttl, body = CAPS[s]
        caption(c, ttl, body, a * win(lt, 0.2, d - 0.1, 0.4, 0.3))
        legend(c, LEG[s], a * win(lt, 0.5, d - 0.1, 0.4, 0.3))
    endcard(c, ramp(t, END, 0.6))
    return surf.makeImageSnapshot()


# ------------------------------------------------------------------ outputs
def ffmpeg_writer(out, fps=30):
    return subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{W}x{H}', '-r', str(fps), '-i', '-',
                             '-vf', 'scale=out_color_matrix=bt709:out_range=tv', '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p',
                             '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-movflags', '+faststart', out], stdin=subprocess.PIPE)


def loops(shots, reps=3):
    for s in shots:
        n = nframes(s)
        if frame_img(s, n - 1) is None:
            print('missing frames for', s); continue
        out = os.path.join(VID, f'TurboDoctor_Motor4_{s}_bucla.mp4')
        p = ffmpeg_writer(out)
        for r in range(reps):
            for k in range(n):
                surf = skia.Surface(W, H); c = surf.getCanvas()
                background(c, 0.0, moving=False)
                draw_frame(c, s, k)
                p.stdin.write(surf.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType).tobytes())
        p.stdin.close(); p.wait()
        alfa = os.path.join(VID, f'TurboDoctor_Motor4_{s}_alfa.webm')
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', '30', '-i', os.path.join(OUT, 'frames', s, 'f%04d.png'),
                        '-c:v', 'libvpx-vp9', '-pix_fmt', 'yuva420p', '-crf', '18', '-b:v', '0', '-row-mt', '1', '-auto-alt-ref', '0', alfa], check=True)
        print('loop', s, n, 'frames ->', out)


def film(out=None, f0=0, f1=None):
    out = out or os.path.join(VID, 'TurboDoctor_Motor_4_cilindri_3D.mp4')
    n = int(round(DUR * FPS)); f1 = n if f1 is None else min(f1, n)
    p = ffmpeg_writer(out)
    for fi in range(f0, f1):
        p.stdin.write(film_frame(fi / FPS).toarray(colorType=skia.kRGBA_8888_ColorType).tobytes())
    p.stdin.close(); p.wait()
    print('film ->', out)


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[0] == 'loops':
        loops(a[1:] or [s for s, _, _ in SEQ])
    elif a[0] == 'film':
        film()
    elif a[0] == 'png':
        os.makedirs(os.path.join(OUT, 'proof'), exist_ok=True)
        for ts in a[1].split(','):
            film_frame(float(ts)).save(os.path.join(OUT, 'proof', f'film_{float(ts):05.1f}.png'), skia.kPNG)
    elif a[0] == 'still':
        # clean still of one shot frame on the background (no UI)
        s, k = a[1], int(a[2])
        surf = skia.Surface(W, H); cc = surf.getCanvas(); background(cc, 0.0, moving=False); draw_frame(cc, s, k)
        surf.makeImageSnapshot().save(a[3], skia.kJPEG if a[3].endswith('.jpg') else skia.kPNG)


# ------------------------------------------------------------------ projection of world points (mm) with the stored shot cameras
def project(shot, p):
    I = INFO[shot]
    Mw = np.array(I['matrix'])
    R = Mw[:3, :3]; tvec = Mw[:3, 3]
    pc = R.T @ (np.array(p, float) - tvec)
    f = I['lens'] / 24.0 * 1920.0
    u = 540.0 + f * pc[0] / (-pc[2]) - I['shift'][0] * 1920.0
    v = 960.0 - f * pc[1] / (-pc[2]) + I['shift'][1] * 1920.0
    return float(u), float(v)
