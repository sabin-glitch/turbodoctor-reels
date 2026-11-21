# Desene 2D (SVG si cv2) pentru seria pompelor: pompa de la benzinarie, recipiente, proba de uzura, urma de pe bila, grafice.
# Desenele SVG devin sprite-uri (E.add(...)); cele cu cv2 se deseneaza pe cadru, in coordonate 1080x1920.
import math
import numpy as np, cv2
import i2d as D, ifx as F, fxlib as X
from fxlib import seg, ease

# ------------------------------------------------------------------ pompa de la benzinarie
def dispenser(w=300, plate='EN 590', top='MOTORINĂ', col='#FFD21F'):
    h = int(round(w * 470 / 320.0))
    return ('<svg width="%d" height="%d" viewBox="0 0 320 470">'
            '<defs><linearGradient id="dsb" x1="0" x2="1"><stop offset="0" stop-color="#1b242e"/><stop offset=".5" stop-color="#2c3743"/><stop offset="1" stop-color="#161d25"/></linearGradient></defs>'
            '<rect x="28" y="432" width="224" height="28" rx="6" fill="#39444f"/>'
            '<rect x="44" y="64" width="192" height="372" rx="16" fill="url(#dsb)" stroke="#9aa7b5" stroke-width="4"/>'
            '<rect x="36" y="30" width="208" height="52" rx="14" fill="%s"/>'
            '<text x="140" y="66" text-anchor="middle" style="font:800 27px Mont;letter-spacing:1px" fill="#0e1319">%s</text>'
            '<rect x="64" y="104" width="152" height="82" rx="8" fill="#0b1016" stroke="#5b6672" stroke-width="3"/>'
            '<rect x="78" y="120" width="92" height="12" rx="4" fill="#d9e0e7"/><rect x="78" y="141" width="124" height="12" rx="4" fill="#d9e0e7"/><rect x="78" y="162" width="64" height="10" rx="4" fill="#7d8894"/>'
            '<rect x="64" y="206" width="152" height="70" rx="8" fill="%s"/>'
            '<text x="140" y="254" text-anchor="middle" style="font:800 36px JB" fill="#0e1319">%s</text>'
            '<path d="M140 304 C128 324 114 338 114 354 a26 26 0 0 0 52 0 C166 338 152 324 140 304z" fill="#ffc02a"/>'
            '<path d="M236 348 C300 352 300 300 290 240 L286 196" fill="none" stroke="#0e1319" stroke-width="16" stroke-linecap="round"/>'
            '<path d="M236 348 C300 352 300 300 290 240 L286 196" fill="none" stroke="#3a4652" stroke-width="9" stroke-linecap="round"/>'
            '<rect x="236" y="150" width="22" height="88" rx="5" fill="#39444f"/>'
            '<path d="M252 150 L296 150 Q306 150 306 162 L306 186 Q306 196 296 196 L276 196 L270 228 L254 228 Z" fill="#111820" stroke="%s" stroke-width="5" stroke-linejoin="round"/>'
            '</svg>') % (w, h, col, top, col, plate, col)

# ------------------------------------------------------------------ recipiente (toate in caseta 200 x 260)
def _wrap(body, w, rot=None):
    """desenul in caseta 200x260; rot = unghi (grade, sens orar) -> caseta patrata 340x340, ca piesa rotita sa nu fie taiata"""
    if rot is None: return '<svg width="%d" height="%d" viewBox="0 0 200 260">%s</svg>' % (w, int(round(w * 1.3)), body)
    return '<svg width="%d" height="%d" viewBox="-70 -40 340 340"><g transform="rotate(%g 100 130)">%s</g></svg>' % (w, w, rot, body)

def jerry(w=200, col='#3ddc84', dark='#1c7a45', rot=None):
    """canistra de benzina"""
    b = ('<rect x="128" y="10" width="44" height="18" rx="6" fill="#0e1319"/><rect x="134" y="24" width="32" height="34" fill="%s"/>'
         '<path d="M40 62 V40 Q40 28 52 28 H104 Q116 28 116 40 V62" fill="none" stroke="%s" stroke-width="12" stroke-linejoin="round"/>'
         '<path d="M22 76 Q22 56 42 56 H160 Q180 56 180 76 V230 Q180 250 160 250 H42 Q22 250 22 230 Z" fill="%s" stroke="%s" stroke-width="6"/>'
         '<rect x="44" y="84" width="114" height="140" rx="12" fill="none" stroke="%s" stroke-width="6" opacity=".7"/>'
         '<path d="M50 90 L152 218 M152 90 L50 218" stroke="%s" stroke-width="7" opacity=".7" stroke-linecap="round"/>'
         '<path d="M34 80 V226" stroke="rgba(255,255,255,.35)" stroke-width="6" stroke-linecap="round"/>') % (dark, dark, col, dark, dark, dark)
    return _wrap(b, w, rot)

def tin(w=200, col='#8fb7d9', dark='#3f6182', rot=None):
    """bidon de tabla cu petrol lampant (semnul lampii)"""
    b = ('<rect x="80" y="12" width="40" height="16" rx="5" fill="#0e1319"/><rect x="86" y="26" width="28" height="26" fill="%s"/>'
         '<path d="M40 86 L72 50 H128 L160 86 V234 Q160 250 144 250 H56 Q40 250 40 234 Z" fill="%s" stroke="%s" stroke-width="6" stroke-linejoin="round"/>'
         '<path d="M40 86 H160" stroke="%s" stroke-width="5"/>'
         '<path d="M100 106 c8 16 22 22 22 42 a22 22 0 0 1 -44 0 c0 -12 8 -18 11 -27 3 8 8 11 11 11 0 -10 -3 -17 0 -26z" fill="#ff5a26"/>'
         '<path d="M100 144 c5 8 11 11 11 20 a11 11 0 0 1 -22 0 c0 -6 5 -11 11 -20z" fill="#FFD21F"/>'
         '<rect x="76" y="192" width="48" height="12" rx="4" fill="%s"/><rect x="66" y="206" width="68" height="18" rx="5" fill="%s"/>'
         '<path d="M50 96 V230" stroke="rgba(255,255,255,.4)" stroke-width="6" stroke-linecap="round"/>') % (dark, col, dark, dark, dark, dark)
    return _wrap(b, w, rot)

def barrel(w=200, col='#d06a2c', dark='#7a3712', rot=None):
    """butoi cu combustibil de incalzire (semnul casei cu flacara)"""
    b = ('<rect x="30" y="20" width="140" height="230" rx="18" fill="%s" stroke="%s" stroke-width="6"/>'
         '<path d="M30 84 H170 M30 190 H170" stroke="%s" stroke-width="9"/>'
         '<ellipse cx="100" cy="32" rx="52" ry="7" fill="%s" opacity=".6"/><circle cx="134" cy="32" r="5" fill="#0e1319"/>'
         '<path d="M68 156 L100 120 L132 156 V176 H68 Z" fill="none" stroke="#fff" stroke-width="6" stroke-linejoin="round"/>'
         '<path d="M100 140 c4 7 9 9 9 16 a9 9 0 0 1 -18 0 c0 -5 4 -8 9 -16z" fill="#FFD21F"/>'
         '<path d="M44 34 V238" stroke="rgba(255,255,255,.3)" stroke-width="7" stroke-linecap="round"/>') % (col, dark, dark, dark)
    return _wrap(b, w, rot)

def jug(w=200, liq='#a9792a', mark='?', cap='#ff4b4b', rot=None, uid='jg'):
    """bidon de plastic fara eticheta, cu lichid tulbure si semn de intrebare"""
    sh = 'M36 92 Q36 60 68 60 H132 Q164 60 164 92 V226 Q164 250 140 250 H60 Q36 250 36 226 Z'
    mk = ('<text x="100" y="212" text-anchor="middle" style="font:400 118px Anton" fill="#fff" stroke="#0e1319" stroke-width="6" paint-order="stroke">%s</text>' % mark) if mark else ''
    b = ('<defs><clipPath id="%s"><path d="%s"/></clipPath></defs>'
         '<rect x="74" y="12" width="52" height="18" rx="6" fill="%s"/><rect x="82" y="28" width="36" height="34" fill="#cfd6de"/>'
         '<path d="%s" fill="rgba(232,237,243,.2)"/><rect x="30" y="128" width="140" height="130" fill="%s" clip-path="url(#%s)" opacity=".92"/>'
         '<path d="%s" fill="none" stroke="#cfd6de" stroke-width="6"/>'
         '<path d="M160 86 Q196 92 188 138 Q184 156 164 158" fill="none" stroke="#cfd6de" stroke-width="10" stroke-linecap="round"/>%s'
         '<path d="M48 96 V224" stroke="rgba(255,255,255,.45)" stroke-width="6" stroke-linecap="round"/>') % (uid, sh, cap, sh, liq, uid, sh, mk)
    return _wrap(b, w, rot)

def item_card(svg, text, small=None, cls='bad', w=570, fs=34):
    """card lat cu un desen in stanga si numele in dreapta (ca la semne, dar cu desenul nostru)"""
    sm = '<small>%s</small>' % small if small else ''
    return ('<div class="sym %s" style="width:%dpx;padding:10px 22px 10px 14px;gap:18px"><div class="ic" style="width:112px;height:130px">%s</div>'
            '<div class="tx" style="font-size:%dpx">%s%s</div></div>') % (cls, w, svg, fs, text, sm)

# ------------------------------------------------------------------ proba de uzura (bila care freaca pe o placa, in baie de motorina)
def rig_bath(w=640):
    """baia cu placa de otel pe fund (fara lichid)"""
    return ('<svg width="%d" height="%d" viewBox="0 0 640 300">'
            '<defs><linearGradient id="rgp" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#eef2f6"/><stop offset=".5" stop-color="#aab4bf"/><stop offset="1" stop-color="#6c7783"/></linearGradient></defs>'
            '<rect x="26" y="36" width="588" height="240" fill="rgba(10,14,19,.55)"/>'
            '<rect x="150" y="246" width="340" height="26" rx="4" fill="#2b3642"/>'
            '<rect x="176" y="206" width="288" height="42" rx="6" fill="url(#rgp)" stroke="#4d5864" stroke-width="3"/>'
            '<path d="M20 30 V252 Q20 282 50 282 H590 Q620 282 620 252 V30" fill="none" stroke="#0e1319" stroke-width="20" stroke-linecap="round" stroke-linejoin="round"/>'
            '<path d="M20 30 V252 Q20 282 50 282 H590 Q620 282 620 252 V30" fill="none" stroke="#9aa7b5" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/></svg>') % (w, int(round(w * 300 / 640.0)))

def rig_fuel(w=640, col='255,192,42', a=0.6):
    """motorina din baie, desenata peste bila (partea scufundata se vede prin lichid)"""
    return ('<svg width="%d" height="%d" viewBox="0 0 640 300"><path d="M27 96 H613 V252 Q613 275 590 275 H50 Q27 275 27 252 Z" fill="rgba(%s,%g)"/>'
            '<path d="M27 96 H613" stroke="#ffe7a0" stroke-width="5"/></svg>') % (w, int(round(w * 300 / 640.0)), col, a)

def rig_ball(w=300):
    """partea care se misca: greutatea, bratul, tija si bila de otel (fundul bilei la y = 422 din 430)"""
    return ('<svg width="%d" height="%d" viewBox="0 0 300 430">'
            '<defs><radialGradient id="rgb" cx=".36" cy=".3" r=".8"><stop offset="0" stop-color="#ffffff"/><stop offset=".45" stop-color="#b3bdc8"/><stop offset="1" stop-color="#5b6672"/></radialGradient>'
            '<linearGradient id="rgs" x1="0" x2="1"><stop offset="0" stop-color="#7d8894"/><stop offset=".45" stop-color="#e3e9ef"/><stop offset="1" stop-color="#69747f"/></linearGradient></defs>'
            '<rect x="98" y="4" width="104" height="66" rx="8" fill="#2b3642" stroke="#9aa7b5" stroke-width="4"/>'
            '<path d="M150 18 V50 M136 38 L150 54 L164 38" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>'
            '<rect x="4" y="84" width="292" height="28" rx="9" fill="#5b6672" stroke="#0e1319" stroke-width="3"/>'
            '<rect x="134" y="70" width="32" height="232" fill="url(#rgs)" stroke="#4d5864" stroke-width="3"/>'
            '<path d="M108 296 H192 V326 Q192 338 180 338 H120 Q108 338 108 326 Z" fill="#2b3642" stroke="#9aa7b5" stroke-width="3"/>'
            '<circle cx="150" cy="372" r="50" fill="url(#rgb)" stroke="#0e1319" stroke-width="3"/></svg>') % (w, int(round(w * 430 / 300.0)))

def scar_field(R=240, ring='#FFD21F'):
    """campul microscopului: suprafata bilei, intunecata, cu rama galbena (urma se deseneaza peste, cu scar())"""
    s = 2 * R + 24; c = R + 12
    return ('<svg width="%d" height="%d" viewBox="0 0 %d %d"><defs><radialGradient id="sfg" cx=".42" cy=".36" r=".8"><stop offset="0" stop-color="#5a6673"/><stop offset=".6" stop-color="#3b4551"/><stop offset="1" stop-color="#222a33"/></radialGradient></defs>'
            '<circle cx="%d" cy="%d" r="%d" fill="url(#sfg)"/><circle cx="%d" cy="%d" r="%d" fill="none" stroke="rgba(0,0,0,.55)" stroke-width="11"/>'
            '<circle cx="%d" cy="%d" r="%d" fill="none" stroke="%s" stroke-width="6"/></svg>') % (s, s, s, s, c, c, R, c, c, R, c, c, R, ring)

def scar(C, cx, cy, hw, a=1.0, red=0.0, ry_k=0.8, seed=23):
    """urma de uzura vazuta la microscop: elipsa mata cu zgarieturi pe directia frecarii; hw = jumatatea latimii (px 1080x1920), red = 0..1 (peste limita)"""
    if a <= 0.003 or hw < 3: return
    hh = hw * ry_k; red = float(np.clip(red, 0, 1))
    base = np.array([168, 178, 190.0]) * (1 - red) + np.array([226, 98, 90.0]) * red
    rim = np.array([226, 232, 240.0]) * (1 - red) + np.array([255, 150, 140.0]) * red
    r = X.rnd(seed, 46, 3)
    def draw(buf, P, k):
        c = P(cx, cy); ax = (int(hw * k * 16), int(hh * k * 16))
        cv2.ellipse(buf, c, ax, 0, 0, 360, tuple(int(v) for v in base) + (255,), -1, cv2.LINE_AA, shift=4)
        for i in range(46):
            yy = (r[i, 0] * 2 - 1) * hh * 0.93; full = hw * math.sqrt(max(0.0, 1 - (yy / hh) ** 2)) - 3
            if full < 4: continue
            half = full * (0.5 + 0.5 * r[i, 1]); x0 = (r[i, 2] * 2 - 1) * (full - half); sh = 0.62 + 0.6 * r[i, 1]
            col = tuple(int(min(255, v * sh)) for v in base) + (255,)
            cv2.line(buf, P(cx + x0 - half, cy + yy), P(cx + x0 + half, cy + yy), col, max(1, int(2.2 * k)), cv2.LINE_AA, shift=4)
        cv2.ellipse(buf, c, ax, 0, 0, 360, tuple(int(v) for v in rim) + (255,), max(1, int(3 * k)), cv2.LINE_AA, shift=4)
    D.canvas(C, cx - hw - 8, cy - hh - 8, 2 * hw + 16, 2 * hh + 16, draw, a)

# ------------------------------------------------------------------ grafic ilustrativ intr-un panou (debit in functie de presiune etc.)
def graph_panel(C, pid, x, y, w, h, curves, t_in, t_out, t_draw, dur=1.4, xlab='PRESIUNE', ylab='DEBIT', tags=(), note='GRAFIC ILUSTRATIV'):
    """panoul pid (sprite, ancorat sus-centru la (x, y), de latime w si inaltime h) cu un grafic desenat progresiv de la t_draw;
    curves = [(xs, ys, (r,g,b), grosime)]; tags = [(text, (r,g,b), u, v)] in coordonatele graficului (0..1)"""
    a = F.pop(C.t, t_in, t_out)
    if a <= 0.003: return
    F.spr(C, pid, x, y, t_in, t_out, anchor='tc')
    gx, gy, gw, gh = x - w / 2 + 50, y + 112, w - 96, h - 196
    pr = float(seg(C.t, t_draw, t_draw + dur))
    F.graph(C, gx, gy, gw, gh, curves, pr, a)
    D.text(C, ylab, gx - 4, gy - 10, 22, (182, 194, 207), a, font='mont', anchor='lb', shadow=False)
    D.text(C, xlab, gx + gw, gy + gh + 10, 22, (182, 194, 207), a, font='mont', anchor='rt', shadow=False)
    for tx, col, u, v in tags:
        D.text(C, tx, gx + u * gw, gy + (1 - v) * gh, 27, col, a * float(seg(pr, max(0.0, u - 0.25), u)), font='mont', anchor='rb', shadow=True)
    if note: D.text(C, note, x - w / 2 + 50, y + h - 30, 20, (125, 136, 148), a, font='mont7', anchor='lm', shadow=False)

# ------------------------------------------------------------------ cartea de service a masinii (randul filtrului de motorina, evidentiat)
def book(w=300, title='CARTE SERVICE', row=('FILTRU', 'MOTORINĂ'), note='LA INTERVAL'):
    rows = ''
    for y in (94, 124):
        rows += ('<rect x="60" y="%d" width="20" height="18" rx="4" fill="none" stroke="#2fae69" stroke-width="3"/><path d="M64 %d l5 5 l8 -10" fill="none" stroke="#2fae69" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>'
                 '<rect x="92" y="%d" width="126" height="10" rx="5" fill="#b9c4d0"/>') % (y, y + 9, y + 4)
    for y in (268, 296):
        rows += '<rect x="60" y="%d" width="20" height="18" rx="4" fill="none" stroke="#9aa7b5" stroke-width="3"/><rect x="92" y="%d" width="%d" height="10" rx="5" fill="#b9c4d0"/>' % (y, y + 4, 126 if y == 268 else 92)
    return ('<svg width="%d" height="%d" viewBox="0 0 260 340"><rect x="18" y="14" width="232" height="320" rx="14" fill="#000" opacity=".35"/>'
            '<rect x="8" y="6" width="232" height="320" rx="14" fill="#eef2f6" stroke="#93a3b5" stroke-width="5"/>'
            '<path d="M22 6 h24 v320 h-24 a14 14 0 0 1 -14 -14 v-292 a14 14 0 0 1 14 -14 z" fill="#2c6fb6"/>'
            '<rect x="56" y="24" width="170" height="46" rx="8" fill="#1d2630"/>'
            '<text x="141" y="55" text-anchor="middle" style="font:800 19px Mont;letter-spacing:.6px" fill="#fff">%s</text>%s'
            '<rect x="52" y="152" width="178" height="102" rx="10" fill="#FFD21F" stroke="#11161c" stroke-width="3"/>'
            '<text x="141" y="184" text-anchor="middle" style="font:900 24px Mont" fill="#11161c">%s</text>'
            '<text x="141" y="211" text-anchor="middle" style="font:900 24px Mont" fill="#11161c">%s</text>'
            '<text x="141" y="238" text-anchor="middle" style="font:800 16px Mont;letter-spacing:1px" fill="#6b5600">%s</text></svg>'
            % (w, int(w * 340 / 260), title, rows, row[0], row[1], note))

# ------------------------------------------------------------------ AdBlue: bidonul, cele doua busoane din gura de umplere, tavile cu piese
def adblue_can(w=200, rot=None, text='AdBlue'):
    """bidon alb cu eticheta albastra si capac albastru (caseta 200x260, ca la celelalte recipiente)"""
    b = ('<rect x="118" y="8" width="50" height="20" rx="6" fill="#1f6fd0"/><rect x="126" y="26" width="34" height="30" fill="#cfd6de"/>'
         '<path d="M44 60 V42 Q44 30 56 30 H96 Q108 30 108 42 V60" fill="none" stroke="#b9c3ce" stroke-width="12" stroke-linejoin="round"/>'
         '<path d="M26 78 Q26 54 50 54 H152 Q176 54 176 78 V228 Q176 250 154 250 H48 Q26 250 26 228 Z" fill="#eef2f6" stroke="#9aa7b5" stroke-width="5"/>'
         '<rect x="28.5" y="112" width="145" height="84" fill="#1f6fd0"/>'
         '<text x="101" y="167" text-anchor="middle" style="font:800 37px Mont" fill="#fff">%s</text>'
         '<rect x="152" y="204" width="12" height="34" rx="6" fill="#8fd4ff"/><rect x="152" y="70" width="12" height="34" rx="6" fill="#8fd4ff"/>'
         '<path d="M40 82 V104 M40 204 V228" stroke="rgba(255,255,255,.9)" stroke-width="6" stroke-linecap="round"/>') % text
    return _wrap(b, w, rot)

def filler(w=640, hl=None):
    """gura de umplere cu cele doua busoane: negru (motorina) si albastru (AdBlue). Caseta 640x360; busonul negru la (200, 180), cel albastru la (470, 196).
    hl = 'diesel' / 'adblue': inel luminos in jurul unuia"""
    ribs = ''.join('<rect x="-7" y="-112" width="14" height="26" rx="5" fill="#2b343f" transform="rotate(%d)"/>' % a for a in range(0, 360, 30))
    ribs2 = ''.join('<rect x="-6" y="-80" width="12" height="20" rx="4" fill="#1857a8" transform="rotate(%d)"/>' % a for a in range(0, 360, 36))
    ring = ''
    if hl == 'diesel': ring = '<circle cx="200" cy="180" r="134" fill="none" stroke="#ff4b4b" stroke-width="9"/>'
    if hl == 'adblue': ring = '<circle cx="470" cy="196" r="100" fill="none" stroke="#3ddc84" stroke-width="9"/>'
    b = ('<rect x="6" y="6" width="628" height="348" rx="54" fill="#1a2129" stroke="#465463" stroke-width="6"/>'
         '<rect x="24" y="24" width="592" height="312" rx="40" fill="#10151b" stroke="#232c36" stroke-width="4"/>'
         '<g transform="translate(200 180)"><circle r="118" fill="#151a20" stroke="#394552" stroke-width="6"/>%s<circle r="82" fill="#0b0f13" stroke="#2b343f" stroke-width="5"/>'
         '<text y="13" text-anchor="middle" style="font:800 36px Mont;letter-spacing:1px" fill="#FFD21F">DIESEL</text></g>'
         '<g transform="translate(470 196)"><circle r="84" fill="#1f6fd0" stroke="#154f96" stroke-width="6"/>%s<circle r="56" fill="#2a7fe0" stroke="#154f96" stroke-width="4"/>'
         '<text y="11" text-anchor="middle" style="font:800 29px Mont" fill="#fff">AdBlue</text></g>%s') % (ribs, ribs2, ring)
    return '<svg width="%d" height="%d" viewBox="0 0 640 360">%s</svg>' % (w, int(round(w * 0.5625)), b)

def tray(title, col='#3ddc84', w=460, bad=False):
    """tava cu piese (rola, piston, arc), cu titlul deasupra: „se reconditioneaza” (verde) sau „se inlocuieste” (rosu, piese patate)"""
    met = '#cfd6de'; dk = '#7d8894'; st = '#b3501e' if bad else None
    spots = ('<circle cx="104" cy="142" r="9" fill="%s"/><circle cx="130" cy="160" r="6" fill="%s"/><circle cx="232" cy="118" r="7" fill="%s"/><circle cx="226" cy="170" r="9" fill="%s"/>'
             '<circle cx="330" cy="128" r="7" fill="%s"/><circle cx="352" cy="166" r="8" fill="%s"/>' % ((st,) * 6)) if bad else ''
    wh = ('<circle cx="118" cy="128" r="5" fill="#fff"/><circle cx="238" cy="146" r="5" fill="#fff"/><circle cx="342" cy="146" r="5" fill="#fff"/><circle cx="96" cy="164" r="4" fill="#fff"/>') if bad else ''
    b = ('<rect x="4" y="4" width="452" height="64" rx="14" fill="rgba(10,14,19,.92)" stroke="%s" stroke-width="4"/>'
         '<text x="230" y="48" text-anchor="middle" style="font:800 31px Mont;letter-spacing:.5px" fill="%s">%s</text>'
         '<path d="M22 92 H438 L416 222 Q414 234 400 234 H60 Q46 234 44 222 Z" fill="#27313c" stroke="#56636f" stroke-width="5" stroke-linejoin="round"/>'
         '<path d="M40 104 H420" stroke="#101519" stroke-width="10" opacity=".5"/>'
         '<circle cx="114" cy="150" r="36" fill="%s" stroke="%s" stroke-width="5"/><circle cx="114" cy="150" r="13" fill="#27313c" stroke="%s" stroke-width="4"/>'
         '<rect x="208" y="104" width="44" height="96" rx="8" fill="%s" stroke="%s" stroke-width="5"/><path d="M208 124 H252" stroke="%s" stroke-width="4"/>'
         '<path d="M314 112 H366 L314 132 H366 L314 152 H366 L314 172 H366 L314 192 H366" fill="none" stroke="%s" stroke-width="8" stroke-linejoin="round" stroke-linecap="round"/>%s%s'
         ) % (col, col, title, met, dk, dk, met, dk, dk, met, spots, wh)
    return '<svg width="%d" height="%d" viewBox="0 0 460 244">%s</svg>' % (w, int(round(w * 244 / 460.0)), b)


def straw(w=900):
    """paiul strans: plin de motorina inainte de strangulare, doar un fir subtire dupa ea; doua falci gri il strang la mijloc"""
    tube = 'M20 70 H330 C400 70 398 138 450 138 C502 138 500 70 570 70 H880 V230 H570 C500 230 502 162 450 162 C398 162 400 230 330 230 H20 Z'
    b = ('<defs><clipPath id="stc"><path d="%s"/></clipPath></defs>'
         '<path d="%s" fill="rgba(206,224,244,.16)"/>'
         '<g clip-path="url(#stc)"><rect x="20" y="70" width="432" height="160" fill="#f2b21d"/><rect x="450" y="141" width="330" height="18" rx="9" fill="#f2b21d"/>'
         '<rect x="20" y="70" width="432" height="26" fill="#ffd45e" opacity=".55"/></g>'
         '<circle cx="806" cy="150" r="9" fill="#f2b21d"/><circle cx="842" cy="150" r="6" fill="#f2b21d"/><circle cx="868" cy="150" r="4" fill="#f2b21d"/>'
         '<path d="%s" fill="none" stroke="#c3d0de" stroke-width="6" stroke-linejoin="round"/>'
         '<rect x="398" y="10" width="104" height="118" rx="16" fill="#3b4652" stroke="#7d8a98" stroke-width="5"/><rect x="398" y="172" width="104" height="118" rx="16" fill="#3b4652" stroke="#7d8a98" stroke-width="5"/>'
         '<path d="M450 34 V96 M430 78 L450 100 L470 78" fill="none" stroke="#ff4b4b" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>'
         '<path d="M450 266 V204 M430 222 L450 200 L470 222" fill="none" stroke="#ff4b4b" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>') % (tube, tube, tube)
    return '<svg width="%d" height="%d" viewBox="0 0 900 300">%s</svg>' % (w, int(round(w / 3.0)), b)


def plug(w=300, burnt=True):
    """mufa pompei electrice, vazuta din fata: patru contacte; unul innegrit, cu plasticul topit in jur si un fir de fum"""
    pins = ''
    for i, x in enumerate((70, 124, 178, 232)):
        bad = burnt and i == 2
        if bad: pins += '<ellipse cx="%d" cy="122" rx="38" ry="46" fill="#4a2c16"/><ellipse cx="%d" cy="122" rx="27" ry="36" fill="#150e08"/>' % (x, x)
        pins += '<rect x="%d" y="94" width="22" height="56" rx="4" fill="%s" stroke="%s" stroke-width="3"/>' % (x - 11, '#2a1d12' if bad else '#d9c070', '#0d0906' if bad else '#8a7430')
    b = ('<rect x="112" y="24" width="76" height="30" rx="8" fill="#2b323b" stroke="#5a6672" stroke-width="5"/>'
         '<rect x="12" y="44" width="276" height="156" rx="22" fill="#2b323b" stroke="#5a6672" stroke-width="6"/>'
         '<rect x="34" y="66" width="232" height="112" rx="12" fill="#12171c"/>%s') % pins
    if burnt: b += '<path d="M182 70 q-12 -16 0 -30 q12 -14 2 -30" fill="none" stroke="rgba(206,212,220,.6)" stroke-width="6" stroke-linecap="round"/>'
    return '<svg width="%d" height="%d" viewBox="0 0 300 212">%s</svg>' % (w, int(round(w * 212 / 300.0)), b)

# ------------------------------------------------------------------ eticheta de carton de la dezmembrari (episodul 17)
def tag(w=420, title='POMPĂ FOLOSITĂ', rows=('KILOMETRI', 'MOTORINĂ', 'DE CE E AICI'), nq=0):
    """eticheta de carton legata cu sfoara: trei randuri fara date; nq = cate semne de intrebare rosii sunt deja puse (0..3)"""
    b = ('<path d="M84 62 C56 30 38 22 6 8" fill="none" stroke="#c9b48a" stroke-width="5" stroke-linecap="round"/>'
         '<g transform="rotate(-4 220 240)">'
         '<path d="M70 44 H366 Q384 44 384 62 V408 Q384 426 366 426 H56 Q38 426 38 408 V94 Z" fill="#000" opacity=".35" transform="translate(8 10)"/>'
         '<path d="M70 44 H366 Q384 44 384 62 V408 Q384 426 366 426 H56 Q38 426 38 408 V94 Z" fill="#dcc79d" stroke="#8c744b" stroke-width="5" stroke-linejoin="round"/>'
         '<circle cx="80" cy="76" r="12" fill="#11161c" stroke="#8c744b" stroke-width="5"/>'
         '<text x="238" y="100" text-anchor="middle" style="font:900 26px Mont;letter-spacing:.4px" fill="#3b2f1b">%s</text>'
         '<path d="M62 122 H360" stroke="#8c744b" stroke-width="4"/>') % title
    for i, r in enumerate(rows):
        y = 190 + i * 92
        b += '<text x="62" y="%d" style="font:800 25px Mont;letter-spacing:.5px" fill="#5d4a2b">%s</text>' % (y - 18, r)
        b += '<path d="M62 %d H300" stroke="#8c744b" stroke-width="4" stroke-dasharray="3 11" stroke-linecap="round"/>' % (y + 16)
        if i < nq:
            b += ('<circle cx="334" cy="%d" r="31" fill="#ff4b4b" stroke="#7d1717" stroke-width="4"/>'
                  '<text x="334" y="%d" text-anchor="middle" style="font:900 44px Mont" fill="#fff">?</text>') % (y - 6, y + 10)
    b += '</g>'
    return '<svg width="%d" height="%d" viewBox="0 0 420 450">%s</svg>' % (w, int(round(w * 450 / 420.0)), b)

def odo(km, w=560, title='KILOMETRAJ'):
    """kilometrajul de la bord: sase tamburi cu cifre si „km”"""
    s = '%06d' % int(km); g = []
    for i, ch in enumerate(s):
        x = 34 + i * 72 + (18 if i >= 3 else 0)
        g.append('<rect x="%d" y="64" width="62" height="94" rx="8" fill="#0d1218" stroke="#3a434d" stroke-width="3"/>' % x)
        g.append('<rect x="%d" y="64" width="62" height="30" rx="8" fill="#ffffff" opacity=".05"/>' % x)
        g.append('<text x="%d" y="136" text-anchor="middle" style="font:800 62px JB" fill="#ffffff">%s</text>' % (x + 31, ch))
    b = ('<rect x="3" y="3" width="554" height="184" rx="22" fill="rgba(8,12,17,.93)" stroke="rgba(232,237,243,.28)" stroke-width="3"/>'
         '<text x="34" y="46" style="font:800 25px Mont;letter-spacing:2px" fill="#b6c2cf">%s</text>%s'
         '<text x="508" y="136" text-anchor="middle" style="font:800 34px Mont" fill="#b6c2cf">km</text>') % (title, ''.join(g))
    return '<svg width="%d" height="%d" viewBox="0 0 560 190">%s</svg>' % (w, int(round(w * 190 / 560.0)), b)

def seals(w=460, title='GARNITURI NOI', col='#3ddc84'):
    """setul de garnituri noi: inele O de cauciuc si simeringul axului, pe o tava"""
    rings = ''.join('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="#111418" stroke-width="%d"/><path d="M%d %d a%d %d 0 0 1 %d %d" fill="none" stroke="#6f7a86" stroke-width="3"/>'
                    % (x, y, r, t, x - r, y, r, r, r, -r) for x, y, r, t in ((96, 156, 34, 11), (176, 186, 22, 8), (338, 150, 30, 10), (392, 196, 18, 7)))
    lip = ('<circle cx="254" cy="160" r="52" fill="#3a2214" stroke="#1a0f08" stroke-width="4"/><circle cx="254" cy="160" r="38" fill="#cfd6de" stroke="#7d8894" stroke-width="4"/>'
           '<circle cx="254" cy="160" r="26" fill="#27313c" stroke="#1a0f08" stroke-width="5"/><path d="M216 140 a40 40 0 0 1 30 -20" fill="none" stroke="#7a4a2a" stroke-width="4"/>')
    b = ('<rect x="4" y="4" width="452" height="64" rx="14" fill="rgba(10,14,19,.92)" stroke="%s" stroke-width="4"/>'
         '<text x="230" y="48" text-anchor="middle" style="font:800 31px Mont;letter-spacing:.5px" fill="%s">%s</text>'
         '<path d="M22 92 H438 L416 222 Q414 234 400 234 H60 Q46 234 44 222 Z" fill="#a7b1bc" stroke="#dfe5eb" stroke-width="5" stroke-linejoin="round"/>'
         '<path d="M40 104 H420" stroke="#6c7783" stroke-width="8" opacity=".5"/>%s%s') % (col, col, title, rings, lip)
    return '<svg width="%d" height="%d" viewBox="0 0 460 244">%s</svg>' % (w, int(round(w * 244 / 460.0)), b)

def tube(w=960, fill=1.0):
    """conducta transparenta de joasa presiune, culcata: motorina galbena de la stanga pana la fill (0..1), aer dupa ea, cu meniscul frontului; canalul pe y 34..166 (din 200)"""
    x0, x1 = 44.0, 916.0; xf = x0 + (x1 - x0) * max(0.0, min(1.0, fill))
    front = '' if fill >= 0.999 else 'M%.1f 34 Q%.1f 100 %.1f 166 L%.1f 166 L%.1f 34 Z' % (xf, xf + 34, xf, xf - 1, xf - 1)
    b = ('<defs><clipPath id="tbc"><rect x="44" y="34" width="872" height="132" rx="16"/></clipPath></defs>'
         '<rect x="44" y="34" width="872" height="132" rx="16" fill="rgba(206,224,244,.12)"/>'
         '<g clip-path="url(#tbc)"><rect x="44" y="34" width="%.1f" height="132" fill="#f2b21d"/><path d="%s" fill="#f2b21d"/>'
         '<rect x="44" y="34" width="%.1f" height="26" fill="#ffd45e" opacity=".55"/></g>'
         '<rect x="40" y="28" width="880" height="144" rx="20" fill="none" stroke="#c3d0de" stroke-width="6"/>'
         '<rect x="56" y="40" width="848" height="12" rx="6" fill="#ffffff" opacity=".18"/>'
         '<rect x="4" y="14" width="54" height="172" rx="12" fill="#56636f" stroke="#8d99a6" stroke-width="4"/>'
         '<rect x="902" y="14" width="54" height="172" rx="12" fill="#56636f" stroke="#8d99a6" stroke-width="4"/>') % (xf - 44.0, front, xf - 44.0)
    return '<svg width="%d" height="%d" viewBox="0 0 960 200">%s</svg>' % (w, int(round(w * 200 / 960.0)), b)

def lpside(w=1000):
    """partea de joasa presiune, verticala: rezervorul jos, furtun, cupla rapida, para de amorsare, filtrul cu capac, a doua cupla, pompa de inalta presiune sus.
    viewBox 1000x800; lantul pe x=300 (puncte slabe: cupla de sus y 190, capacul filtrului y 258, carcasa filtrului y 353, para y 528, cupla de jos y 630)"""
    def hose(y0, y1):
        return ('<path d="M300 %d V%d" stroke="#141a20" stroke-width="30" stroke-linecap="butt"/><path d="M300 %d V%d" stroke="#3b444e" stroke-width="22"/>'
                '<path d="M300 %d V%d" stroke="#f2b21d" stroke-width="9" opacity=".9"/>') % (y0, y1, y0, y1, y0, y1)
    def coupling(yc):
        return ('<rect x="268" y="%d" width="64" height="40" rx="9" fill="#b9c3ce" stroke="#e6ecf2" stroke-width="3"/>'
                '<rect x="262" y="%d" width="76" height="10" rx="4" fill="#7d8996"/><rect x="330" y="%d" width="22" height="18" rx="4" fill="#d8dfe6" stroke="#6c7884" stroke-width="2"/>'
                ) % (yc - 20, yc - 5, yc - 9)
    b = ['<rect x="40" y="680" width="560" height="110" rx="26" fill="rgba(20,26,33,.94)" stroke="#9aa7b5" stroke-width="5"/>',
         '<rect x="48" y="722" width="544" height="60" rx="16" fill="#ffc02a" opacity=".5"/>',
         '<path d="M300 680 V760" stroke="#9aa7b5" stroke-width="7"/><rect x="284" y="756" width="32" height="18" rx="5" fill="#9aa7b5"/>',
         hose(648, 690), coupling(630), hose(586, 612),
         '<rect x="282" y="466" width="36" height="16" rx="4" fill="#3b444e"/><rect x="282" y="574" width="36" height="16" rx="4" fill="#3b444e"/>',
         '<ellipse cx="300" cy="528" rx="48" ry="58" fill="#20262d" stroke="#6b7783" stroke-width="5"/>',
         '<path d="M262 502 Q300 492 338 502 M256 528 Q300 518 344 528 M262 554 Q300 544 338 554" fill="none" stroke="#4c5661" stroke-width="4"/>',
         '<ellipse cx="284" cy="506" rx="10" ry="18" fill="#ffffff" opacity=".12"/>',
         hose(430, 468),
         '<rect x="244" y="276" width="112" height="154" rx="14" fill="rgba(20,26,33,.94)" stroke="#9aa7b5" stroke-width="5"/>',
         '<path d="M262 292v122M276 292v122M290 292v122M304 292v122M318 292v122M332 292v122M346 292v122" stroke="#e8edf3" stroke-width="3" opacity=".5"/>',
         '<rect x="232" y="240" width="136" height="38" rx="10" fill="#56636f" stroke="#a9b5c1" stroke-width="4"/>',
         '<path d="M248 248v22M262 248v22M276 248v22M324 248v22M338 248v22M352 248v22" stroke="#3a434d" stroke-width="4"/>',
         hose(208, 242), coupling(190), hose(130, 172),
         '<rect x="186" y="16" width="228" height="118" rx="24" fill="rgba(20,26,33,.94)" stroke="#9aa7b5" stroke-width="5"/>',
         '<ellipse cx="300" cy="80" rx="48" ry="32" fill="none" stroke="#e8edf3" stroke-width="5" opacity=".75"/><circle cx="300" cy="80" r="9" fill="#e8edf3" opacity=".75"/>']
    return '<svg width="%d" height="%d" viewBox="0 0 1000 800">%s</svg>' % (w, int(round(w * 0.8)), ''.join(b))

def calendar(month, w=280, n_cross=0):
    """filă de calendar de perete: banda rosie cu inele, luna mare (3 litere), grila zilelor; n_cross zile taiate"""
    cells = ''
    for r in range(4):
        for c in range(7):
            x = 34 + c * 30; y = 170 + r * 26; k = r * 7 + c
            cells += '<rect x="%d" y="%d" width="22" height="18" rx="3" fill="%s"/>' % (x, y, '#c9d2dc' if k >= n_cross else '#8b96a2')
            if k < n_cross: cells += '<path d="M%d %d l18 14 M%d %d l-18 14" stroke="#ff4b4b" stroke-width="3"/>' % (x + 2, y + 2, x + 20, y + 2)
    b = ('<rect x="14" y="20" width="252" height="290" rx="14" fill="#000" opacity=".35"/>'
         '<rect x="6" y="12" width="252" height="290" rx="14" fill="#eef2f6" stroke="#93a3b5" stroke-width="4"/>'
         '<path d="M6 26 a14 14 0 0 1 14 -14 h224 a14 14 0 0 1 14 14 v44 h-252 z" fill="#d8443a"/>'
         '<rect x="62" y="0" width="12" height="30" rx="6" fill="#56636f"/><rect x="190" y="0" width="12" height="30" rx="6" fill="#56636f"/>'
         '<text x="132" y="150" text-anchor="middle" style="font:900 74px Mont;letter-spacing:2px" fill="#1d2630">%s</text>%s') % (month, cells)
    return '<svg width="%d" height="%d" viewBox="0 0 264 310">%s</svg>' % (w, int(round(w * 310 / 264.0)), b)

def tester(prog=0.0, w=440, title='ADAPTARE', sub='POMPĂ / REGULATOR NOU', done=False):
    """testerul de diagnoza tinut in mana: ecran cu titlul, bara de progres (prog 0..1) si, la final, bifa verde; cablul pleaca in jos (desen ilustrativ)"""
    pw = 300.0 * max(0.0, min(1.0, prog))
    ok = ('<circle cx="220" cy="300" r="30" fill="#3ddc84"/><path d="M205 300 l11 11 l20 -24" fill="none" stroke="#0e1319" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'
          if done else '<text x="220" y="312" text-anchor="middle" style="font:800 30px JB" fill="#FFD21F">%d%%</text>' % int(round(100 * prog)))
    b = ('<path d="M220 560 C220 610 260 640 330 650" fill="none" stroke="#0e1319" stroke-width="18" stroke-linecap="round"/>'
         '<path d="M220 560 C220 610 260 640 330 650" fill="none" stroke="#39444f" stroke-width="10" stroke-linecap="round"/>'
         '<rect x="44" y="24" width="352" height="548" rx="44" fill="#000" opacity=".35" transform="translate(8 10)"/>'
         '<rect x="44" y="24" width="352" height="548" rx="44" fill="#1f2731" stroke="#9aa7b5" stroke-width="5"/>'
         '<rect x="70" y="58" width="300" height="300" rx="14" fill="#0b1016" stroke="#56636f" stroke-width="4"/>'
         '<text x="220" y="118" text-anchor="middle" style="font:900 38px Mont;letter-spacing:1px" fill="#e8edf3">%s</text>'
         '<text x="220" y="156" text-anchor="middle" style="font:800 19px Mont;letter-spacing:.5px" fill="#9aa7b5">%s</text>'
         '<rect x="70" y="214" width="300" height="34" rx="8" fill="#27313c"/><rect x="70" y="214" width="%.1f" height="34" rx="8" fill="#FFD21F"/>%s'
         '<circle cx="150" cy="440" r="34" fill="#2c3743" stroke="#56636f" stroke-width="4"/><circle cx="290" cy="440" r="34" fill="#2c3743" stroke="#56636f" stroke-width="4"/>'
         '<rect x="186" y="404" width="68" height="72" rx="14" fill="#2c3743" stroke="#56636f" stroke-width="4"/>'
         '<rect x="120" y="506" width="200" height="22" rx="11" fill="#2c3743"/>') % (title, sub, pw, ok)
    return '<svg width="%d" height="%d" viewBox="0 0 440 660">%s</svg>' % (w, int(round(w * 660 / 440.0)), b)

def tappet_top(ang=0.0, w=620, bad=False, uid='tt'):
    """tachetul vazut de sus, rotund in locasul lui (desen 2D, 620x620): rola de deasupra camei, rotita cu ang grade fata de pozitia buna
    (axa rolei orizontala = rola se rostogoleste pe cama, care trece de sus in jos); bad = conturul rolei rosu"""
    col = '#ff4b4b' if bad else '#0e1319'
    b = ('<defs><radialGradient id="%(u)sg" cx="42%%" cy="38%%" r="70%%"><stop offset="0" stop-color="#e3e9ef"/><stop offset=".7" stop-color="#a9b4bf"/><stop offset="1" stop-color="#7b8692"/></radialGradient>'
         '<linearGradient id="%(u)sr" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8d98a4"/><stop offset=".35" stop-color="#f2f6f9"/><stop offset=".6" stop-color="#c3ccd5"/><stop offset="1" stop-color="#6d7884"/></linearGradient>'
         '<pattern id="%(u)sh" width="22" height="22" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="22" height="22" fill="#56616d"/><rect width="9" height="22" fill="#66717d"/></pattern></defs>'
         '<rect x="20" y="20" width="580" height="580" rx="40" fill="url(#%(u)sh)" stroke="#2a323b" stroke-width="6"/>'
         '<circle cx="310" cy="310" r="226" fill="#0b1016"/><circle cx="310" cy="310" r="226" fill="none" stroke="#1d252e" stroke-width="10"/>'
         '<circle cx="310" cy="310" r="206" fill="url(#%(u)sg)" stroke="#59646f" stroke-width="5"/>'
         '<circle cx="310" cy="310" r="176" fill="none" stroke="#8a95a1" stroke-width="3" opacity=".7"/>'
         '<g transform="rotate(%(a).2f 310 310)">'
         '<rect x="150" y="248" width="320" height="124" rx="10" fill="#0b1016" opacity=".55"/>'
         '<rect x="176" y="256" width="268" height="108" rx="16" fill="url(#%(u)sr)" stroke="%(c)s" stroke-width="%(cw)d"/>'
         '<line x1="206" y1="262" x2="206" y2="358" stroke="#55606b" stroke-width="3"/><line x1="414" y1="262" x2="414" y2="358" stroke="#55606b" stroke-width="3"/>'
         '<rect x="140" y="292" width="40" height="36" rx="6" fill="#9aa5b1" stroke="#0e1319" stroke-width="4"/><rect x="440" y="292" width="40" height="36" rx="6" fill="#9aa5b1" stroke="#0e1319" stroke-width="4"/>'
         '</g>') % dict(u=uid, a=ang, c=col, cw=7 if bad else 4)
    return '<svg width="%d" height="%d" viewBox="0 0 620 620">%s</svg>' % (w, w, b)
