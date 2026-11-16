# Piesele comune ale episoadelor: insigna, cardurile de simptome, iconitele, finalul, sprite-urile.
import os, sys, json, math, subprocess, importlib
import numpy as np, cv2
HERE = os.path.dirname(os.path.abspath(__file__))
import icomp as IC, ifx as F
from fxlib import seg, win, ease

NAMES = {1: 'PARTICULELE DIN MOTORINĂ', 2: 'APA DIN MOTORINĂ', 3: 'DEPUNERILE DIN INTERIOR', 4: 'CALAMINA DIN GĂURILE DUZEI',
         5: 'ȘAIBA DE ETANȘARE', 6: 'MURDĂRIA ȘI GREȘELILE DE LA MONTAJ', 7: 'BENZINA PUSĂ DIN GREȘEALĂ', 8: 'ADBLUE ÎN REZERVORUL DE MOTORINĂ',
         9: 'MOTORINA CARE NU UNGE', 10: 'PILITURA DE LA POMPĂ', 11: 'FĂRĂ COD ȘI FĂRĂ STANDARD', 12: 'DEFECTELE ELECTRICE', 13: 'UZURA NORMALĂ'}

def badge_html(n):
    return '<div id="badge"><i>SERIA „DE CE SE STRICĂ INJECTOARELE”</i><b>CAUZA %d DIN 13</b><u>%s</u></div>' % (n, NAMES[n])

def lb(text, cls='', small=None):
    s = '<small>%s</small>' % small if small else ''
    return '<div class="lb %s">%s%s</div>' % (cls, text, s)

ICON = {
 'engine': '<svg width="78" height="78" viewBox="0 0 64 64"><path d="M9 27h5v-6h9v-5h14v5h7l5 6h6v15h-6l-5 6H21l-5-6h-7z" fill="none" stroke="#FFB224" stroke-width="4.5" stroke-linejoin="round"/><path d="M3 30v10M23 16h14" stroke="#FFB224" stroke-width="4.5" stroke-linecap="round"/></svg>',
 'power': '<svg width="80" height="80" viewBox="0 0 64 64"><path d="M8 46a24 24 0 0 1 48 0" fill="none" stroke="#5b6672" stroke-width="5" stroke-linecap="round"/><path d="M8 46a24 24 0 0 1 9-19" fill="none" stroke="#ff4b4b" stroke-width="5" stroke-linecap="round"/><path d="M32 46 L17 31" stroke="#fff" stroke-width="5" stroke-linecap="round"/><circle cx="32" cy="46" r="5" fill="#fff"/></svg>',
 'stall': '<svg width="78" height="78" viewBox="0 0 64 64"><circle cx="32" cy="32" r="25" fill="none" stroke="#ff4b4b" stroke-width="5"/><path d="M18 46 L46 18" stroke="#ff4b4b" stroke-width="5" stroke-linecap="round"/><path d="M22 34h6l3-7 4 12 3-5h5" fill="none" stroke="#fff" stroke-width="3.5" stroke-linejoin="round" stroke-linecap="round"/></svg>',
 'smoke': '<svg width="80" height="80" viewBox="0 0 64 64"><circle cx="24" cy="36" r="10" fill="#9aa7b5"/><circle cx="36" cy="28" r="12" fill="#b6c2cf"/><circle cx="44" cy="40" r="9" fill="#7d8894"/><rect x="6" y="48" width="18" height="8" rx="2" fill="#5b6672"/></svg>',
 'idle': '<svg width="80" height="80" viewBox="0 0 64 64"><path d="M4 34h8l4-10 6 20 6-26 6 30 5-18 4 8h17" fill="none" stroke="#FFB224" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/></svg>',
 'cold': '<svg width="80" height="80" viewBox="0 0 64 64"><g stroke="#6cc4ff" stroke-width="4.5" stroke-linecap="round"><path d="M32 6v52M9 19l46 26M9 45l46-26"/><path d="M26 10l6 6 6-6M26 54l6-6 6 6"/></g></svg>',
 'start': '<svg width="80" height="80" viewBox="0 0 64 64"><circle cx="32" cy="32" r="24" fill="none" stroke="#FFB224" stroke-width="5"/><path d="M32 14v18" stroke="#FFB224" stroke-width="5" stroke-linecap="round"/><path d="M20 22a16 16 0 1 0 24 0" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round"/></svg>',
 'fuel': '<svg width="80" height="80" viewBox="0 0 64 64"><rect x="10" y="12" width="26" height="42" rx="4" fill="none" stroke="#FFB224" stroke-width="5"/><rect x="15" y="18" width="16" height="10" fill="#FFB224"/><path d="M36 26h7l6 6v16a4 4 0 0 0 8 0V24l-6-6" fill="none" stroke="#FFB224" stroke-width="4.5" stroke-linejoin="round"/></svg>',
 'water': '<svg width="80" height="80" viewBox="0 0 64 64"><path d="M32 6C24 20 14 30 14 40a18 18 0 0 0 36 0C50 30 40 20 32 6z" fill="#2f9bff"/><path d="M24 40a8 8 0 0 0 8 8" fill="none" stroke="#cfe8ff" stroke-width="4" stroke-linecap="round"/></svg>',
 'warn': '<svg width="80" height="80" viewBox="0 0 64 64"><path d="M32 6 L60 56 H4 Z" fill="none" stroke="#FFB224" stroke-width="5" stroke-linejoin="round"/><path d="M32 24v16" stroke="#fff" stroke-width="5" stroke-linecap="round"/><circle cx="32" cy="48" r="3.4" fill="#fff"/></svg>',
 'stop': '<svg width="80" height="80" viewBox="0 0 64 64"><path d="M22 6h20l16 16v20L42 58H22L6 42V22z" fill="#ff4b4b"/><path d="M20 32h24" stroke="#fff" stroke-width="7" stroke-linecap="round"/></svg>',
 'check': '<svg width="44" height="44" viewBox="0 0 64 64"><path d="M14 33l12 12 24-26" fill="none" stroke="#0b1a10" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/></svg>',
 'cross': '<svg width="40" height="40" viewBox="0 0 64 64"><path d="M16 16l32 32M48 16L16 48" stroke="#fff" stroke-width="9" stroke-linecap="round"/></svg>',
}

def sym(icon, text, small=None, cls='bad'):
    s = '<small>%s</small>' % small if small else ''
    return '<div class="sym %s"><div class="ic">%s</div><div class="tx">%s%s</div></div>' % (cls, ICON[icon], text, s)

def chk(text, ok=True):
    return '<div class="chk%s"><div class="dot">%s</div>%s</div>' % ('' if ok else ' no', ICON['check'] if ok else ICON['cross'], text)

def panel(title, w=700, h=330):
    return '<div class="panel" style="width:%dpx;height:%dpx"><div class="tl">%s</div></div>' % (w, h, title)

def make_glob(ep, n):
    def glob(t, img):
        a = float(seg(t, 0.5, 1.0))
        if a > 0.003:
            s = IC.sprite(ep, 'badge'); k = IC.W / 1080.0
            if k != 1.0: s = cv2.resize(s, (max(1, int(s.shape[1] * k)), max(1, int(s.shape[0] * k))), interpolation=cv2.INTER_AREA)
            IC.blit(img, s, 44 * k, 196 * k, a)
        return img
    return glob

# ------------------------------------------------------------------ fragmente de regie
def inj_pulses(t0, t1, period=0.62, on=0.16, phase=0.0):
    """momentele injectiilor (ton, toff) intre t0 si t1"""
    out = []; t = t0 + phase
    while t < t1: out.append((t, t + on)); t += period
    return out

def spray_pulses(C, pulses, **kw):
    for ton, toff in pulses:
        if ton - 0.05 <= C.t <= toff + 0.6: F.spray(C, ton, toff, **kw)

if __name__ == '__main__':
    # python3 ikit.py epN  -> sprite-urile episodului in hud/epN
    ep = sys.argv[1]; sys.path.insert(0, HERE)
    st = importlib.import_module('st_' + ep)
    out = os.path.join(HERE, 'hud', ep); os.makedirs(out, exist_ok=True)
    spec = [{'id': k, 'html': v} for k, v in st.SPR.items()]
    json.dump(spec, open(os.path.join(out, 'spec.json'), 'w'), ensure_ascii=False)
    subprocess.run(['node', os.path.join(HERE, 'hud', 'sprites.js'), os.path.join(out, 'spec.json'), out], check=True)
