# Piese comune pentru episoadele seriei „De ce se strică pompele de înaltă presiune”: timpii episodului, proiectii, miscarea rolei,
# curgerile din pompa (motorina, bule, pilitura), scanteile contactului uscat, schema instalatiei, filtrul, atelierul, deschiderea si finalul.
import os, json, math
import numpy as np, cv2
import icomp as IC, ifx as F, ikit as K, i2d as D, pkin, pshots as PS
import fxlib as X
from icomp import Shot
from fxlib import seg, ease

FIRST = {1: 'aerul', 2: 'rezervorul', 3: 'benzina', 4: 'motorina', 5: 'particulele', 6: 'apa', 7: 'adblue', 8: 'motorina', 9: 'filtrul', 10: 'pompa',
         11: 'aerul', 12: 'regulatorul', 13: 'tachetul', 14: 'uzura', 15: 'greselile', 16: 'pompa', 17: 'pompa'}
METAL2 = (225, 230, 238); AIR2 = (235, 244, 255); LP2 = (255, 200, 60); HP2 = (255, 110, 50); RED2 = (255, 75, 75); GREEN2 = (61, 220, 132)
GREEN_HL = dict(col='#3ddc84', fill='rgba(61,220,132,.22)'); YEL_HL = dict(col='#ffd21f', fill='rgba(255,210,31,.18)')
WHITE_HL = dict(col='#e8f2ff', fill='rgba(232,242,255,.16)')
KB_PW = (1.0, 0, 46)          # pompa in plan larg, coborata sub insigna

class Ep:
    def __init__(s, n):
        s.n = n; s.ep = 'ep%d' % n
        s.Q = IC.Cues(os.path.join(IC.HERE, s.ep, 'vo', 'cues.json'))
        tl = json.load(open(os.path.join(IC.HERE, s.ep, 'vo', 'timeline.json')))
        s.TOTAL = tl['total']; s.END = tl['story_end']
        s.W, s.L, s.LE = s.Q.W, s.Q.L, s.Q.LE
        s.NL = len(s.Q.lines); s.OUT = s.NL - 3          # primul rand din formula de final
        s.T_S = s.L(0); s.T_C = s.W(0, 'cauza'); s.T_N = s.W(0, FIRST[n])
        tx = [l['text'] for l in s.Q.lines]
        s.I_EV = next((i for i, t in enumerate(tx) if t.startswith('Cum evi')), None)          # randul „Cum eviti”
        s.I_NOI = next((i for i, t in enumerate(tx) if t.startswith('Ce facem noi')), None)     # randul „Ce facem noi la Turbo Doctor”
        s.T_NOI = s.L(s.I_NOI) if s.I_NOI is not None else None
        s.SPR = dict(spr_common(n)); s.SPR['sys'] = D.sys_svg(); s._ids = {}
    # sprite-urile episodului: fiecare text se inregistreaza o singura data si primeste un nume scurt
    def add(s, html):
        if html not in s._ids:
            s._ids[html] = 'a%d' % (len(s._ids) + 1); s.SPR[s._ids[html]] = html
        return s._ids[html]
    def lb(s, text, cls='', small=None): return s.add(K.lb(text, cls, small))
    def sym(s, icon, text, small=None, cls='bad'):
        ic = K.ICON.get(icon) or D.ICON2[icon]; sm = '<small>%s</small>' % small if small else ''
        return s.add('<div class="sym %s"><div class="ic">%s</div><div class="tx">%s%s</div></div>' % (cls, ic, text, sm))
    def chk(s, text, ok=True): return s.add(K.chk(text, ok))
    def hl(s, names, style=None): return s.add(D.sys_hl(list(names), **(style or {})))
    def stop(s, text, small=None, icon='stop'):
        ic = K.ICON.get(icon) or D.ICON2[icon]; sm = '<small>%s</small>' % small if small else ''
        return s.add('<div class="stop" style="max-width:960px"><div class="ic">%s</div><div>%s%s</div></div>' % (ic, text, sm))
    def panel(s, title, w, h): return s.add(K.panel(title, w, h))

def scr(cam, st, P, kb=(1.0, 0, 0)):
    J = json.load(open(IC.find_plate('%s__%s' % (cam, st)) + '.json')); c = X.Cam(J, 1080, 1920); c.set2d(*kb)
    x, y, z = c.proj(np.asarray(P, float).reshape(-1, 3)); return float(x[0]), float(y[0])

def kb_on(cam, st, P, z, tx=540, ty=960, clip=True):
    """Ken Burns (zoom, dx, dy) care pune punctul 3D P la (tx, ty) pe ecran, cu zoom z"""
    x, y = scr(cam, st, P)
    dx, dy = tx - (x - 540) * z - 540, ty - (y - 960) * z - 960
    if clip:
        mx, my = 540 * (z - 1), 960 * (z - 1)                 # placa trebuie sa acopere tot cadrul
        dx, dy = float(np.clip(dx, -mx, mx)), float(np.clip(dy, -my, my))
    return (z, dx, dy)

def spr_common(n):
    return {'badge': K.badge_html(n)}

def glob(E): return K.make_glob(E.ep, E.n)

def shake_at(ta, dur=0.9, amp=4.0):
    def sh(t):
        e = float(seg(t, ta, ta + 0.08)) * (1 - float(seg(t, ta + dur * 0.6, ta + dur)))
        return (amp * e * math.sin(t * 57.0), 0.75 * amp * e * math.sin(t * 43.0 + 0.7))
    return sh

def shakes(*S):
    def sh(t):
        x = y = 0.0
        for f in S:
            a, b = f(t); x += a; y += b
        return (x, y)
    return sh

# ------------------------------------------------------------------ pompa: miscarea rolei si punctele de pe piese
def hph(ph):
    """inaltimea centrului rolei (mm) la faza ph (in curse), aceeasi cu a buclei randate (30 de cadre pe cursa)"""
    k = math.floor(ph * PS.NLOOP + 1e-6) % PS.NLOOP
    return pkin.state(PS.PHI0 + math.pi * k / PS.NLOOP)['h']
def hC(C, t=None):
    ph = C.shot.ph(C.t if t is None else t)
    return hph(ph if ph is not None else 0.0)
H0 = pkin.state(PS.PHI0)['h']
def P_contact(h, y=-6.95): return np.array([0.0, y, h - 5.5])
def P_roller(h): return np.array([0.0, -7.0, h])
def P_tappet(h): return np.array([9.0, -9.5, h + 9.0])
def P_plunger(h): return np.array([2.2, -2.4, h + 36.0])
P_CAM = np.array([13.0, -8.7, -6.0]); P_SHAFT = np.array([0.0, -40.0, 9.0]); P_CHAMBER = np.array([0.0, -0.1, 80.5]); P_INVALVE = np.array([0.0, -0.1, 85.5])
P_BALL = np.array([15.66, -0.1, 81.6]); P_HPPORT = np.array([50.0, -0.1, 81.6]); P_ZME = np.array([52.0, 8.0, 34.0]); P_LPBATH = np.array([24.0, -0.1, -8.0])

# trasee noi pe fetele de sectiune (peste cele din ifx.path)
def _mk_paths():
    P = F.PATHS; PR, PL = F.PR, F.PLf
    P['bath_R'] = F.IPath(F.ring(24.0, -86, 86, 28), 'R', 2.5, smooth=0, step=0.25)            # baia camei, sensul acelor (de jos in sus)
    P['bath_Rd'] = F.IPath(F.ring(24.0, 86, -86, 28), 'R', 2.5, smooth=0, step=0.25)           # de sus in jos
    P['bath_out'] = F.IPath(F.ring(24.0, -60, 40, 18) + [PR(27.5, 20.0), PR(33.0, 26.0)], 'R', 1.6, smooth=0, step=0.25)   # din baie spre regulator
    P['up_gal'] = F.IPath([PL(-17.5, 60.0), PL(-17.5, 88.3), PL(-6.0, 88.3), PL(-1.0, 87.0)], 'L', 1.4, smooth=3, step=0.25)  # urcarea spre galeria de admisie
_mk_paths()

def env(t, t_on=None, t_off=None, d=0.45):
    e = 1.0
    if t_on is not None: e *= float(seg(t, t_on, t_on + d))
    if t_off is not None: e *= 1.0 - float(seg(t, t_off, t_off + d))
    return e

def fx_fuel(t_on=None, t_off=None, n=46, a=0.5, hp=True, speed=16.0, col=None):
    """motorina vie: licariri galbene in baia camei, portocalii spre rampa (doar pe cursa de refulare)"""
    def f(C):
        e = env(C.t, t_on, t_off)
        if e <= 0.003: return
        cl = np.array([1.0, 0.86, 0.5] if col is None else col)
        F.flow(C, 'bath_R', n, speed, cl, 0.55, lat=0.9, seed=11, mode='add', shape='g', shade=0, a=a * e)
        F.flow(C, 'cam_Ldn', n // 4, speed * 0.5, cl, 0.5, lat=0.8, seed=12, mode='add', shape='g', shade=0, a=a * e)
        if hp:
            ph = C.shot.ph(C.t); pr = pkin.state(PS.PHI0 + math.pi * (ph or 0.0))['press']
            if pr > 0.02:
                F.flow(C, 'hp_out', 26, 70.0, np.array([1.0, 0.62, 0.35]), 0.5, lat=0.7, seed=13, mode='add', shape='g', shade=0, a=0.75 * pr * e)
    return f

def fx_bubbles(t_on, t_off=None, n=34, speed=13.0, size=1.05, a=0.95, paths=('bath_R', 'cam_Ldn', 'cam_Lup'), seed=41):
    """bule de aer in baia camei (inele albe)"""
    def f(C):
        e = env(C.t, None, t_off)
        if e <= 0.003: return
        for i, pn in enumerate(paths):
            F.bubbles(C, pn, n if i == 0 else max(4, n // 5), speed, size, seed=seed + i, a=a * e, t0=t_on, sz_var=0.55, minpx=1.6)
    return f

def fx_filings(t_on, t_off=None, n=30, speed=15.0, size=0.5, a=1.0, paths=('bath_R', 'cam_Ldn'), seed=61, glow=0.5):
    """pilitura argintie dusa de motorina prin baia camei"""
    def f(C):
        e = env(C.t, None, t_off)
        if e <= 0.003: return
        for i, pn in enumerate(paths):
            m = n if i == 0 else max(4, n // 5)
            F.flow(C, pn, m, speed, np.array([0.16, 0.17, 0.19]), size * 1.35, lat=0.9, seed=seed + i, t0=t_on, mode='over', shape='d', shade=0, sz_var=0.6, a=0.8 * a * e, minpx=1.6)
            F.flow(C, pn, m, speed, np.array([0.93, 0.95, 0.98]), size, lat=0.9, seed=seed + i, t0=t_on, mode='over', shape='d', shade=0.55,
                   sz_var=0.6, glow=glow, a=a * e, minpx=1.3)
    return f

def fx_dry(t_on, t_off=None, rate=9.0, amp=1.0, size=0.34, speed=62.0, seed=0, hot=True, n=20):
    """contact uscat: scantei la linia rola - cama (urmaresc rola) si o dunga incinsa pe contact"""
    def f(C):
        t = C.t
        if t < t_on - 0.05 or (t_off is not None and t > t_off + 0.7): return
        k1 = int(math.floor((t - t_on) * rate)); k0 = max(0, int(math.floor((t - 0.75 - t_on) * rate)))
        for k in range(k0, k1 + 1):
            tb = t_on + k / rate
            if t_off is not None and tb > t_off: break
            r = X.rnd(900 + seed + k, 1, 6)[0]
            y = -6.95 if r[0] < 0.62 else -6.95 + 13.0 * r[1]
            p = P_contact(hC(C, tb), y) + np.array([0.9 * (r[2] - 0.5), -0.25, 0.0])
            sg = 1.0 if (k % 3) else -1.0
            F.sparks(C, p, tb, n=n, life=0.34, speed=speed * amp * (0.7 + 0.6 * r[3]), size=size * amp, seed=300 + seed + k,
                     up=np.array([0.9 * sg, -0.55, 0.22]), spread=0.85)
            u = t - tb
            if 0 <= u < 0.12: F.glow(C, p, 46 * C.k * amp, np.array([1.0, 0.85, 0.55]), 0.8 * (1 - u / 0.12))
        if hot:
            e = env(t, t_on, t_off, 0.5)
            if e > 0.01:
                h = hC(C); fl = 0.75 + 0.25 * math.sin(t * 31.0)
                for y in (-6.6, -4.4, -2.2):
                    F.glow(C, P_contact(h, y), 34 * C.k * amp, np.array([1.0, 0.42, 0.12]), 0.4 * e * fl)
    return f

def fx_flakes(t_on, t_off=None, n=70, size=0.21, seed=71, fall=26.0, a=1.0):
    """pilitura care se desprinde de la contact si cade pe langa cama (aschii mici, argintii)"""
    def f(C):
        t = C.t
        if t < t_on: return
        r = X.rnd(seed, n, 8); life = 1.5
        age = (t - t_on - r[:, 0] * life) % life; birth = t - age
        ok = (birth >= t_on) & ((birth <= t_off) if t_off is not None else True)
        if not ok.any(): return
        hb = np.array([hC(C, float(b)) for b in birth])
        sg = np.where(r[:, 1] < 0.5, -1.0, 1.0)
        x = sg * (1.2 + (6.0 + 9.0 * r[:, 2]) * age + 2.0 * r[:, 3])
        y = -6.95 - (0.6 + 2.4 * r[:, 4]) * age - 0.5
        z = hb - 5.5 + 2.0 * r[:, 5] * age - 0.5 * fall * age * age
        P = np.stack([x, y, z], -1); al = ok * np.clip(1.6 - age / life * 1.6, 0, 1) * a
        xx, yy, zz = C.cam.proj(P); rp = C.cam.px(size * (0.6 + 0.9 * r[:, 6]), zz)
        C.cv.dots(xx, yy, zz, np.maximum(rp, 1.2 * C.k), np.broadcast_to(F.METAL, (n, 3)), al, mode='over', shape='d', zbias=F.zb_for(C, zz), shade=0.8)
        C.cv.dots(xx, yy, zz, np.maximum(rp, 1.2 * C.k) * 2.6, np.broadcast_to(np.array([0.9, 0.95, 1.0]), (n, 3)), al * 0.35, mode='add', shape='g', zbias=F.zb_for(C, zz))
    return f

def lab_parts(C, items, t_out, h=None):
    """etichete pe piesele pompei: items = [(sprite, 'cam'|'roller'|'plunger'|'tappet'|punct, (x, y), t_in[, ancora])]"""
    h = hC(C) if h is None else h
    for it in items:
        sid, what, box, t_in = it[:4]; anc = it[4] if len(it) > 4 else 'tl'
        p = {'cam': P_CAM, 'roller': P_roller(h), 'plunger': P_plunger(h), 'tappet': P_tappet(h), 'contact': P_contact(h)}.get(what, what) if isinstance(what, str) else what
        F.label(C, sid, p, box, t_in, t_out, anchor=anc)

# ------------------------------------------------------------------ schema instalatiei (sprite 'sys' la D.SYS_X, D.SYS_Y)
SP = D.sys_paths()
def sysmap(C, t0, t1, hl=()):
    """schema + evidentieri [(sprite, t_in[, t_out])]; intoarce opacitatea pentru particule"""
    F.spr(C, 'sys', D.SYS_X, D.SYS_Y, t0, t1, popk=1.0, slide=(0, 0))
    for h in hl:
        F.spr(C, h[0], D.SYS_X, D.SYS_Y, h[1], h[2] if len(h) > 2 else t1, popk=1.0, slide=(0, 0))
    return F.pop(C.t, t0, t1)

def sys_flow(C, names, n, speed, col, r, a, t0=None, t1=None, seed=1, glow=0.4, ring=False, lat=0.0):
    polys = []
    for nm in names:
        p = SP[nm]; polys += p if isinstance(p, list) else [p]
    D.flow2(C, polys, n, speed, col, r, t0=t0, t1=t1, a=a, seed=seed, glow=glow, ring=ring, lat=lat)

def sys_shot(E, t0, t1, ov, tr=('xf', 0.3)):
    return Shot('blank', t0, t1, st='none', tr=tr, ov=ov, phase=False)

# ------------------------------------------------------------------ filtrul de motorina (camera 'fl', aux.blend)
KB_FL = (0.9, 0, 66)
def _flt_paths():
    P = F.PATHS; PR, PL = F.PR, F.PLf
    P['flt_core'] = F.IPath([PR(5.5, 22.0), PR(5.5, 150.0)], 'R', 4.6, smooth=0, step=0.5)        # tubul central, in sus
    P['flt_coreL'] = F.IPath([PL(-5.5, 22.0), PL(-5.5, 150.0)], 'L', 4.6, smooth=0, step=0.5)
    P['flt_outR'] = F.IPath([PR(43.2, 132.0), PR(43.2, 8.0)], 'R', 1.5, smooth=0, step=0.5)        # pe langa hartie, in jos
    P['flt_outL'] = F.IPath([PL(-43.2, 132.0), PL(-43.2, 8.0)], 'L', 1.5, smooth=0, step=0.5)
    P['flt_inR'] = F.IPath([PR(41.0, 70.0), PR(13.0, 70.0)], 'R', 50.0, smooth=0, step=0.5)        # prin hartie, spre centru
    P['flt_inL'] = F.IPath([PL(-41.0, 70.0), PL(-13.0, 70.0)], 'L', 50.0, smooth=0, step=0.5)
_flt_paths()

def fx_flt_air(t_on=None, t_off=None, n=30, speed=30.0, size=2.3, a=0.95):
    """aerul din filtrul gol: bule albe care urca prin tubul central spre iesire"""
    def f(C):
        F.bubbles(C, 'flt_core', n, speed, size, seed=45, a=a, t0=t_on, t1=t_off, sz_var=0.5, minpx=2.0, lat=0.8)
        F.bubbles(C, 'flt_coreL', n, speed, size, seed=46, a=a, t0=t_on, t1=t_off, sz_var=0.5, minpx=2.0, lat=0.8)
    return f

def fx_flt_fuel(t_on=None, t_off=None, n=36, a=0.55):
    """motorina prin filtru: coboara pe langa hartie, trece prin ea si urca prin tubul central"""
    def f(C):
        col = np.array([1.0, 0.86, 0.5])
        for i, (pn, sp, m) in enumerate((('flt_outR', 26.0, n // 2), ('flt_outL', 26.0, n // 2), ('flt_inR', 9.0, n), ('flt_inL', 9.0, n), ('flt_core', 34.0, n), ('flt_coreL', 34.0, n))):
            F.flow(C, pn, m, sp, col, 1.5, lat=0.9, seed=21 + i, t0=t_on, t1=t_off, mode='add', shape='g', shade=0, a=a)
    return f

# ------------------------------------------------------------------ atelierul (desene schematice): microscopul, bancul, standul de injectoare
WM_OBJ = np.array([-45.0, 70.0, 62.0])               # sub obiectivul microscopului (cama arborelui)
WI_TIP = np.array([0.0, 0.0, 262.0])                 # varful duzei pe standul de injectoare
def fx_spray(t_on, t_off=None, per=0.7, dur=0.2, L=92.0, cone=0.23, n=150, a=0.8):
    """jetul fin al injectorului pe stand (impulsuri scurte, ceata galbuie in camera de sticla)"""
    r = X.rnd(83, n, 8)
    def f(C):
        t = C.t
        if t < t_on or (t_off is not None and t > t_off + 0.5): return
        for j in range(3):
            k = math.floor((t - t_on) / per) - j
            if k < 0: continue
            tb = t_on + k * per
            if t_off is not None and tb > t_off: continue
            u = t - tb
            if u > 0.62: continue
            age = u - r[:, 0] * dur; ok = age > 0
            if not ok.any(): continue
            v = L / 0.36
            dist = np.minimum(L, v * age * (0.55 + 0.45 * r[:, 1]))
            ang = 2 * math.pi * r[:, 2]; rad = cone * dist * np.sqrt(r[:, 3])
            P = WI_TIP[None, :] + np.stack([rad * np.cos(ang), rad * np.sin(ang), -dist], -1)
            al = ok * np.clip(1.0 - age / 0.6, 0, 1) * a
            x, y, z = C.cam.proj(P); rp = C.cam.px(1.6 + 3.2 * dist / L, z)
            C.cv.dots(x, y, z, np.maximum(rp, 1.4 * C.k), np.broadcast_to(np.array([1.0, 0.9, 0.62]), (n, 3)), al * 0.5, mode='add', shape='g', ztest=False)
    return f

def test_sheet(C, x, y, t_in, t_out, rows, title='sheet'):
    """fisa de test: panoul (sprite) si randurile bifate [(sprite, t_in)]"""
    F.spr(C, title, x, y, t_in, t_out, anchor='tc')
    for i, (sid, tr) in enumerate(rows):
        F.spr(C, sid, x, y + 84 + i * 84, tr, t_out, anchor='tc')

# ------------------------------------------------------------------ planuri standard
def opening(E, hook, fx_open=()):
    """carligul (planurile date, pana la T_S), apoi pompa intreaga care se deschide in sectiune la cuvantul „cauza”"""
    t1 = E.L(2)
    return list(hook) + [
        Shot('pw', E.T_S, t1, st='full', wipe=('fuel', E.T_C - 0.05, E.T_C + 0.9, 60), tr=('xf', 0.35),
             kb=[(E.T_S, 1.0, 0, 46), (t1, 1.08, 0, 30)], fx=[fx_fuel(E.T_C + 0.5)] + list(fx_open)),
    ]

def ending(E, tr=('xf', 0.4)):
    t0 = E.L(E.OUT)
    return Shot('pw', t0, E.TOTAL + 1, st='fuel', tr=tr, kb=[(t0, 1.0, 0, 46), (E.TOTAL, 1.1, 0, 20)], fx=[fx_fuel()])

def symptoms(E, i, cards, cam='fl', st='fempty', kb=KB_FL, fx=(), x=220, y0=760, dy=145, t0=None, t1=None, dimk=0.3, phase=False, tr=('xf', 0.3), **kw):
    """planul cu semnele: carduri [(sprite, cuvant[, n])] peste un plan estompat"""
    W, L, LE = E.W, E.L, E.LE
    t0 = L(i) if t0 is None else t0; t1 = L(i + 1) if t1 is None else t1
    def ov(C):
        for k, cd in enumerate(cards):
            F.spr(C, cd[0], x, y0 + k * dy, W(i, cd[1], cd[2] if len(cd) > 2 else 1) - 0.1, LE(i) + 0.3)
    tc = W(i, cards[0][1], cards[0][2] if len(cards[0]) > 2 else 1) - 0.1
    return Shot(cam, t0, t1, st=st, kb=[(t0,) + tuple(kb), (t1, kb[0] * 1.04, kb[1], kb[2])], fx=list(fx), ov=ov, tr=tr, phase=phase,
                dim=lambda t: dimk * F.pop(t, tc, LE(i) + 0.3), **kw)

# ====================================================================================================================
# Trusa a doua: etichete pe timp, lichide recolorate, pete care cresc, placi ca sprite-uri, instrumente 2D, planuri standard
# ====================================================================================================================
def ovs(*fs):
    fs = [f for f in fs if f is not None]
    def ov(C):
        for f in fs: f(C)
    return ov

def bl(E, labs, t_end, y=None, x=540, anchor='tc'):
    """etichete de jos, una dupa alta: labs = [(text, clasa, t_in[, text mic])]; fiecare sta pana la urmatoarea"""
    ids = [(E.lb(l[0], l[1], l[3] if len(l) > 3 else None), l[2], len(l) > 3 and l[3]) for l in labs]
    def ov(C):
        for i, (sid, ti, two) in enumerate(ids):
            to = ids[i + 1][1] - 0.14 if i + 1 < len(ids) else t_end + 0.15
            F.spr(C, sid, x, (1150 if two else 1186) if y is None else y, ti - 0.1, to, anchor=anchor)
    return ov

def tl(E, labs, t_end, y=384, x=540):
    """etichete de sus (sub insigna), una dupa alta; pentru schema instalatiei, unde jos e desenul"""
    return bl(E, labs, t_end, y=y, x=x)

def hd(E, text, t0, t1, cls='big', y=372):
    sid = E.lb(text, cls)
    def ov(C): F.spr(C, sid, 540, y, t0 - 0.05, t1, anchor='tc')
    return ov

# ------------------------------------------------------------------ lichidul din placa, recolorat (benzina, AdBlue, apa, motorina veche)
BENZ = (0.42, 0.82, 0.36); ADB = (0.66, 0.88, 1.0); WATER = (0.2, 0.56, 0.9); OLD = (0.5, 0.3, 0.1); MIX = (0.66, 0.8, 0.26); LPY = (0.8, 0.61, 0.19)
BENZ2 = (120, 225, 105); ADB2 = (175, 228, 255); WATER2 = (70, 160, 245); OLD2 = (150, 95, 40); RUST2 = (170, 78, 34); WHITE2 = (245, 250, 255)
def liq_mask(c, which='lp', soft=False):
    """masca lichidului dintr-o imagine RGB nepremultiplicata: galben (joasa presiune), portocaliu (inalta) sau amandoua;
    soft = ia si galbenul spalacit de langa lichid (piese vazute prin motorina, reflexii pe otel), dar nu bronzul si cuprul aflate mai departe"""
    r = np.maximum(c[..., 0], 1e-3); sat = 1.0 - c[..., 2] / r; gr = c[..., 1] / r
    def mk(s0, g0, gw):
        m = np.clip((sat - s0) / 0.1, 0, 1) * np.clip((c[..., 0] - 0.25) / 0.15, 0, 1) * np.clip((1.02 - gr) / 0.06, 0, 1)
        if which == 'lp': m = m * np.clip((gr - g0) / gw, 0, 1)
        elif which == 'hp': m = m * np.clip((0.62 - gr) / 0.12, 0, 1)
        return m
    m = mk(0.6, 0.5, 0.12)
    if soft and which != 'hp':
        wk = mk(0.26, 0.6, 0.1)                                   # galben spalacit: se ia doar daca se tine de lichidul adevarat (aceeasi pata)
        n, lab = cv2.connectedComponents((np.maximum(wk, m) > 0.5).astype(np.uint8), connectivity=4)
        if n > 1:
            has = np.bincount(lab.ravel(), weights=(m > 0.5).ravel().astype(np.float32), minlength=n) > 40
            has[0] = False; m = np.maximum(m, wk * has[lab])
    return m
def pf_tint(col, t0=None, t1=None, w=1.0, which='lp', band=None, ref=0.79, rmin=None, soft=True):
    """recoloreaza lichidul din placa spre culoarea col (pastreaza umbrele); t0..t1 = trecerea; band = (y0, y1) px la 1080: de la 0 la tot, pe verticala"""
    col = np.asarray(col, np.float32)
    def f(rgba, t):
        ww = w * (1.0 if t0 is None else float(seg(t, t0, t1)))
        if ww <= 0.003: return rgba
        al = np.maximum(rgba[..., 3:4], 1e-4); c = np.clip(rgba[..., :3] / al, 0, 1)
        m = liq_mask(c, which, soft) * ww
        if rmin is not None: m = m * np.clip((c[..., 0] - rmin) / 0.1, 0, 1)          # lasa pe dinafara maroul inchis (cama zgariata)
        if band is not None:
            k = rgba.shape[1] / 1080.0; y = np.arange(rgba.shape[0], dtype=np.float32)[:, None]
            m = m * np.clip((y - band[0] * k) / max((band[1] - band[0]) * k, 1e-3), 0, 1)
        ys = np.where(m.max(1) > 0.003)[0]; xs = np.where(m.max(0) > 0.003)[0]
        if len(ys) == 0: return rgba
        sl = (slice(ys[0], ys[-1] + 1), slice(xs[0], xs[-1] + 1)); cc = c[sl]; mm = m[sl][..., None]          # doar dreptunghiul in care e lichid
        mx = cc.max(-1, keepdims=True); new = np.clip(col[None, None, :] * (mx / ref), 0, 1)
        if soft and which != 'hp':                                                       # galbenul spalacit ramane spalacit: verde deschis, nu verde plin
            kk = np.clip(1.0 - (1.0 - cc[..., 2:3] / np.maximum(cc[..., 0:1], 1e-3)) / 0.72, 0, 1); new = new * (1 - kk) + mx * 0.97 * kk
        out = rgba.copy(); out[sl][..., :3] = (cc * (1 - mm) + new * mm) * rgba[sl][..., 3:4]
        return out
    return f
def pfs(*fs):
    fs = [f for f in fs if f is not None]
    def f(rgba, t):
        for g in fs: rgba = g(rgba, t)
        return rgba
    return f

# ------------------------------------------------------------------ pete care cresc pe piese (rugina, cristale, lac, mal)
def fx_blotch(pts, col, t_on, t_full, R=3.0, n=30, seed=5, a=0.9, soft=True, spark=0.0, t_off=None, sq=0.8):
    """pts = puncte 3D (mm) pe suprafete vizibile (sau ('px', x, y) pe placa); R = raza petei (mm sau px); cresc intre t_on si t_full"""
    P3 = [p for p in pts]; r = X.rnd(seed, len(P3) * n, 8).reshape(len(P3), n, 8); col = np.asarray(col, np.float32)
    def f(C):
        e = float(seg(C.t, t_on, t_full)) * (1.0 if t_off is None else 1.0 - float(seg(C.t, t_off, t_off + 0.5)))
        if e <= 0.003: return
        for i, p in enumerate(P3):
            if isinstance(p, tuple) and p[0] == 'px':
                z, dx, dy = C.shot.kbat(C.t); k = C.k
                x0 = ((p[1] - 540) * z + 540 + dx) * k; y0 = ((p[2] - 960) * z + 960 + dy) * k; Rp = R * z * k; z0 = 0.0
            else:
                xx, yy, zz = C.cam.proj(np.asarray(p, float)[None, :]); x0, y0, z0 = float(xx[0]), float(yy[0]), float(zz[0]); Rp = float(C.cam.px(R, zz)[0])
            ri = r[i]; ang = 2 * math.pi * ri[:, 0]; rad = np.sqrt(ri[:, 1]) * (0.35 + 0.65 * e)
            g = np.clip((e - 0.75 * ri[:, 2]) / 0.25, 0, 1)
            x = x0 + np.cos(ang) * rad * Rp; y = y0 + np.sin(ang) * rad * Rp * sq
            sz = Rp * (0.16 + 0.3 * ri[:, 3]) * (0.5 + 0.5 * g)
            cc = np.clip(col[None, :] * (0.72 + 0.5 * ri[:, 4:5]), 0, 1)
            C.cv.dots(x, y, np.full(n, z0), np.maximum(sz, 1.0 * C.k), cc, a * g, mode='over', shape='g' if soft else 'd', ztest=False)
            if spark > 0:
                tw = 0.5 + 0.5 * np.sin(C.t * 7.0 + 40.0 * ri[:, 5])
                C.cv.dots(x, y, np.full(n, z0), np.maximum(sz * 0.55, 1.0 * C.k), np.broadcast_to(np.array([1.0, 1.0, 1.0], np.float32), (n, 3)), spark * g * tw, mode='add', shape='g', ztest=False)
    return f

# ------------------------------------------------------------------ o placa desenata ca sprite (micsorata), peste cadru
def plate_spr(C, cam, st, cx, cy, sc, a=1.0, crop=None, pf=None, tag=''):
    if a <= 0.003: return
    k = C.k; key = ('pspr', cam, st, round(sc, 4), crop, IC.W, tag)
    im = IC._cache.get(key)
    if im is None:
        p = IC.plate(cam, st)[0]
        if pf is not None: p = pf(p, 1e9)
        if crop is not None: p = p[int(crop[1] * k):int(crop[3] * k), int(crop[0] * k):int(crop[2] * k)]
        im = IC.keep(key, cv2.resize(p, (max(1, int(p.shape[1] * sc)), max(1, int(p.shape[0] * sc))), interpolation=cv2.INTER_AREA), cap=80)
    IC.blit(C.ov, im, cx * k - im.shape[1] / 2, cy * k - im.shape[0] / 2, a); C.used = True

# ------------------------------------------------------------------ instrumente 2D (coordonate 1080x1920)
def gauge(C, cx, cy, R, v, a=1.0, a0=150.0, a1=390.0, red=(0.0, 0.16), green=None, th=10, nt=9, col=(232, 237, 243)):
    """cadran cu ac: v in 0..1 intre unghiurile a0 si a1 (grade pe ecran, sens orar, 0 = dreapta)"""
    if a <= 0.003: return
    D.arc(C, cx, cy, R, a0, a1, (96, 106, 118), th, a)
    if red: D.arc(C, cx, cy, R, a0 + (a1 - a0) * red[0], a0 + (a1 - a0) * red[1], (255, 75, 75), th, a)
    if green: D.arc(C, cx, cy, R, a0 + (a1 - a0) * green[0], a0 + (a1 - a0) * green[1], (61, 220, 132), th, a)
    an = math.radians(a0 + (a1 - a0) * float(np.clip(v, -0.03, 1.03)))
    def draw(buf, P, k):
        for i in range(nt):
            t = math.radians(a0 + (a1 - a0) * i / (nt - 1)); c, s_ = math.cos(t), math.sin(t)
            cv2.line(buf, P(cx + c * (R - 26), cy + s_ * (R - 26)), P(cx + c * (R - 10), cy + s_ * (R - 10)), (*col, 200), max(1, int(3 * k)), cv2.LINE_AA, shift=4)
        cv2.line(buf, P(cx - math.cos(an) * R * 0.14, cy - math.sin(an) * R * 0.14), P(cx + math.cos(an) * (R - 30), cy + math.sin(an) * (R - 30)), (255, 210, 31, 255), max(2, int(7 * k)), cv2.LINE_AA, shift=4)
        cv2.circle(buf, P(cx, cy), int(R * 0.09 * k * 16), (*col, 255), -1, cv2.LINE_AA, shift=4)
    D.canvas(C, cx - R - 8, cy - R - 8, 2 * R + 16, 2 * R + 16, draw, a)

def thermo(C, x, y, h, v, a=1.0, w=34, cold=(70, 160, 245), hot=(255, 90, 50)):
    """termometru vertical: (x, y) = centrul bulbului de jos, h = inaltimea tubului, v in 0..1"""
    if a <= 0.003: return
    v = float(np.clip(v, 0, 1)); col = tuple(int(c0 + (c1 - c0) * v) for c0, c1 in zip(cold, hot))
    def draw(buf, P, k):
        r = int(w * 0.5 * k * 16)
        cv2.line(buf, P(x, y), P(x, y - h), (20, 26, 33, 240), max(2, int(w * k)), cv2.LINE_AA, shift=4)
        cv2.circle(buf, P(x, y), int(w * 0.95 * k * 16), (20, 26, 33, 240), -1, cv2.LINE_AA, shift=4)
        cv2.circle(buf, P(x, y), int(w * 0.95 * k * 16), (200, 208, 218, 255), max(1, int(3 * k)), cv2.LINE_AA, shift=4)
        cv2.line(buf, P(x - w / 2, y - h), P(x - w / 2, y - w * 0.8), (200, 208, 218, 255), max(1, int(3 * k)), cv2.LINE_AA, shift=4)
        cv2.line(buf, P(x + w / 2, y - h), P(x + w / 2, y - w * 0.8), (200, 208, 218, 255), max(1, int(3 * k)), cv2.LINE_AA, shift=4)
        cv2.ellipse(buf, P(x, y - h), (r, r), 0, 180, 360, (200, 208, 218, 255), max(1, int(3 * k)), cv2.LINE_AA, shift=4)
        cv2.circle(buf, P(x, y), int(w * 0.68 * k * 16), (*col, 255), -1, cv2.LINE_AA, shift=4)
        cv2.line(buf, P(x, y), P(x, y - (h - 6) * (0.08 + 0.92 * v)), (*col, 255), max(2, int((w - 18) * k)), cv2.LINE_AA, shift=4)
        for i in range(1, 6):
            yy = y - w - (h - w) * i / 6.0
            cv2.line(buf, P(x + w / 2 + 6, yy), P(x + w / 2 + (22 if i % 2 else 14), yy), (200, 208, 218, 230), max(1, int(2.5 * k)), cv2.LINE_AA, shift=4)
    D.canvas(C, x - w * 1.2, y - h - w, w * 2.4 + 30, h + 2.2 * w, draw, a)

def xmark(C, cx, cy, R, a=1.0, th=14, col=(255, 75, 75)):
    if a <= 0.003: return
    D.line2(C, [(cx - R, cy - R), (cx + R, cy + R)], col, th, a); D.line2(C, [(cx + R, cy - R), (cx - R, cy + R)], col, th, a)

def arrow2(C, p0, p1, col, th=8, a=1.0, prog=1.0, head=22):
    """sageata 2D desenata progresiv"""
    if a <= 0.003 or prog <= 0.02: return
    x0, y0 = p0; x1, y1 = p0[0] + (p1[0] - p0[0]) * min(1.0, prog), p0[1] + (p1[1] - p0[1]) * min(1.0, prog)
    D.line2(C, [(x0, y0), (x1, y1)], col, th, a)
    dx, dy = x1 - x0, y1 - y0; L = math.hypot(dx, dy) + 1e-6; ux, uy = dx / L, dy / L
    D.line2(C, [(x1 - ux * head - uy * head * 0.6, y1 - uy * head + ux * head * 0.6), (x1, y1), (x1 - ux * head + uy * head * 0.6, y1 - uy * head - ux * head * 0.6)], col, th, a)

def dash2(C, p0, p1, col, th=5, a=1.0, n=14):
    """linie intrerupta"""
    if a <= 0.003: return
    for i in range(n):
        u0, u1 = i / n, (i + 0.55) / n
        D.line2(C, [(p0[0] + (p1[0] - p0[0]) * u0, p0[1] + (p1[1] - p0[1]) * u0), (p0[0] + (p1[0] - p0[0]) * u1, p0[1] + (p1[1] - p0[1]) * u1)], col, th, a)

# ------------------------------------------------------------------ planuri standard
def pump(E, cam, t0, t1, st='fuel', labs=(), fx=None, ov=None, kb=None, tr=('xf', 0.3), y=None, **kw):
    """plan cu pompa (pw, pc, ph, pm): motorina vie daca nu se dau alte particule, etichete de jos pe timp"""
    if fx is None: fx = [fx_fuel()] if st in ('fuel', 'damf') and cam in ('pw', 'pc') else []
    if kb is None: kb = [(t0, 1.0, 0, 46 if cam == 'pw' else 0), (t1, 1.06, 0, 36 if cam == 'pw' else 0)]
    return Shot(cam, t0, t1, st=st, kb=kb, fx=list(fx), ov=ovs(bl(E, labs, t1, y=y) if labs else None, ov), tr=tr, **kw)

def sysm(E, t0, t1, hl=(), flows=(), labs=(), ov=None, tr=('xf', 0.3)):
    """schema instalatiei: hl = [(componente, stil sau None, t_in[, t_out])]; flows = [(trasee, culoare 0-255, n, viteza, raza, t_on[, t_off[, inel]])];
    labs = etichete de sus [(text, clasa, t_in[, mic])]"""
    H = [(E.hl(h[0] if isinstance(h[0], (list, tuple)) else [h[0]], h[1]),) + tuple(h[2:]) for h in hl]
    lo = tl(E, labs, t1) if labs else None; te = t1 + 0.2
    def o(C):
        a = sysmap(C, t0 - 0.1, te, H)
        for fl in flows:
            names, col, n, sp, r = fl[:5]; t_on = fl[5] if len(fl) > 5 else None; t_off = fl[6] if len(fl) > 6 else None; ring = fl[7] if len(fl) > 7 else False
            sys_flow(C, list(names) if isinstance(names, (list, tuple)) else [names], n, sp, col, r, a, t0=t_on, t1=t_off, seed=7 + len(str(names)), glow=0.0 if ring else 0.45, ring=ring, lat=6.0 if ring else 4.0)
        if lo: lo(C)
        if ov: ov(C)
    return Shot('blank', t0, t1, st='none', tr=tr, ov=o, phase=False)

def plain(E, t0, t1, ov, tr=('xf', 0.3)):
    """plan fara placa (doar fundalul), pentru desenele 2D"""
    return Shot('blank', t0, t1, st='none', tr=tr, ov=ov, phase=False)

def cards(E, items, t_end, ys=None, x=540):
    """carduri bifate, pe cuvinte: items = [(text, t_in[, ok])]"""
    n = len(items); ys = ys or {1: (1182,), 2: (1096, 1182), 3: (1010, 1096, 1182), 4: (924, 1010, 1096, 1182)}[n]
    ids = [(E.chk(it[0], it[2] if len(it) > 2 else True), it[1]) for it in items]
    def ov(C):
        for (sid, ti), y in zip(ids, ys): F.spr(C, sid, x, y, ti - 0.1, t_end, anchor='tc')
    return ov

def avoid(E, cam, st, t0, t1, items, kb=None, fx=(), head='CUM EVIȚI', ov=None, tr=('xf', 0.3), dim=0.22, t_head=None, hend=None, **kw):
    """planul „Cum eviti”: titlul verde sus si cardurile bifate jos, peste un plan usor estompat"""
    th = E.L(E.I_EV) if t_head is None else t_head; he = (E.L(E.I_NOI) if hend is None else hend) + 0.1
    o = ovs(hd(E, head, th, he, 'good big'), cards(E, items, t1 + 0.1) if items else None, ov)
    tc = min([it[1] for it in items]) if items else t0
    kw.setdefault('phase', False)
    return Shot(cam, t0, t1, st=st, kb=kb or [(t0, 1.0, 0, 0), (t1, 1.05, 0, 0)], fx=list(fx), ov=o, tr=tr, dim=(lambda t: dim * F.pop(t, tc - 0.1, t1 + 0.1)) if dim else None, **kw)

# ------------------------------------------------------------------ atelierul
LENS_KB = (1.6, -128, 128)               # cama zgariata de sub rola, in lupa (placa pc:dam)
def wk(E, cam, t0, t1, labs=(), st='wk', seq=(), fx=(), ov=None, kb=None, tr=('xf', 0.35), y=1196):
    """plan din atelier, cu titlul „Ce facem noi la Turbo Doctor” sus si etichetele de jos"""
    hid = E.lb('CE FACEM NOI LA TURBO DOCTOR', 'big'); lo = bl(E, labs, t1, y=y) if labs else None; he = E.L(E.OUT) + 0.2
    def o(C):
        F.spr(C, hid, 540, 372, E.T_NOI - 0.05, he, anchor='tc')
        if lo: lo(C)
        if ov: ov(C)
    return Shot(cam, t0, t1, st=st, seq=list(seq), tr=tr, kb=kb or [(t0, 1.0, 0, 0), (t1, 1.06, 0, 0)], fx=list(fx), ov=o, phase=False)

def wk_mic(E, t0, t1, labs=(), lens=None, t_new=None, lens_src=('pc', 'dam', LENS_KB), dam=True, ov=None, **kw):
    """microscopul: lens = (t_in, t_out) pentru lupa cu piesa marita; t_new = momentul in care piesele roase devin piese noi"""
    def o(C):
        if lens: F.lens(C, lens_src[0], lens_src[1], 770, 650, 200, lens[0], lens[1], kb=lens_src[2], src=WM_OBJ)
        if ov: ov(C)
    return wk(E, 'wm', t0, t1, labs, st='wkdam' if dam else 'wk', seq=[('wk', t_new, t_new + 0.5)] if (t_new is not None and dam) else (), ov=o, **kw)

def wk_bench(E, t0, t1, labs=(), rows=(), t_sheet=None, title='FIȘA DE TEST', ov=None, **kw):
    """bancul de proba, cu fisa de test: rows = [(text, t_in[, ok])]"""
    pid = E.panel(title, 440, 92 + 84 * len(rows)) if rows else None
    ids = [(E.chk(r[0], r[2] if len(r) > 2 else True), r[1]) for r in rows]
    def o(C):
        if rows:
            ts = (rows[0][1] - 0.45) if t_sheet is None else t_sheet
            test_sheet(C, 800, 470, ts, t1 + 0.15, [(sid, ti - 0.1) for sid, ti in ids], title=pid)
        if ov: ov(C)
    return wk(E, 'wb', t0, t1, labs, ov=o, **kw)

def wk_usb(E, t0, t1, labs=(), t_dip=None, **kw):
    """baia cu ultrasunete: cosul cu piese coboara in baie la t_dip"""
    return wk(E, 'wu', t0, t1, labs, st='wkup' if t_dip is not None else 'wk', seq=[('wk', t_dip, t_dip + 0.7)] if t_dip is not None else (), **kw)

def wk_inj(E, t0, t1, labs=(), spray=True, **kw):
    return wk(E, 'wi', t0, t1, labs, fx=[fx_spray(t0 + 0.4)] if spray else [], **kw)

def seal(E, big, text, small=None, cls='y'):
    """card mare cu cifra (garantia de 12 luni etc.)"""
    sm = '<small>%s</small>' % small if small else ''
    return E.add('<div class="stat %s" style="padding:10px 34px 16px"><b style="font-size:130px">%s</b><span style="font-size:34px">%s</span>%s</div>' % (cls, big, text, sm))

# ------------------------------------------------------------------ desene 2D legate de placa (urmaresc zoomul si deplasarea planului)
def pk(C, pts):
    """puncte din coordonatele placii (1080x1920, fara zoom) -> coordonatele cadrului la momentul C.t"""
    z, dx, dy = C.shot.kbat(C.t)
    if C.shot.shake is not None:
        sx, sy = C.shot.shake(C.t); dx += sx; dy += sy
    return [((x - 540) * z + 540 + dx, (y - 960) * z + 960 + dy) for x, y in pts]

def flowp(C, pts, n, speed, col, r, t0=None, t1=None, a=1.0, seed=1, glow=0.0, ring=False, lat=0.0, jit=0.25, dark=0.0):
    """particule 2D pe un traseu dat in coordonatele placii (bule in conducta, murdarie pe fundul rezervorului); dark = disc inchis sub inel (bule pe piese deschise)"""
    z = C.shot.kbat(C.t)[0]
    if dark: D.flow2(C, [D.Poly(pk(C, pts))], n, speed * z, (16, 22, 30), (r + 1.5) * z, t0=t0, t1=t1, a=a * dark, seed=seed, jit=jit, lat=lat * z)
    D.flow2(C, [D.Poly(pk(C, pts))], n, speed * z, col, r * z, t0=t0, t1=t1, a=a, seed=seed, glow=glow, jit=jit, lat=lat * z, ring=ring)

# rezervorul din seria injectoarelor (camera 'tank'): peretii x 105..985, y 800..1195; motorina de la y 985 in jos; sorbul la (695, 1150); conducta iese pe sus
TANK_TOP, TANK_BOT, TANK_SORB = 985, 1175, (695, 1150)
TANK_OUT = [(695, 1140), (697, 1040), (700, 830), (725, 790), (725, 712), (760, 690), (1075, 684)]        # din sorb, prin modul, pe conducta
def slosh(t0, amp=0.07, per=1.7, t1=None):
    def f(t):
        e = float(seg(t, t0, t0 + 0.4)) * (1.0 if t1 is None else 1.0 - float(seg(t, t1 - 0.5, t1)))
        return amp * e * math.sin((t - t0) * 2 * math.pi / per)
    return f

MIX2 = (176, 214, 84); MIXS = (0.86, 1.0, 0.55)          # amestecul de motorina cu benzina: particule 2D si licariri
TANK_IN = [(-30, 655), (30, 745), (85, 815), (135, 866), (166, 912), (182, 992)]          # de la gura de umplere pana la luciul motorinei
def tank_in(t_on, t_off=None, col=BENZ2, n=30, r=7.5, speed=300.0):
    """suvoiul care intra pe gura de umplere (benzina, AdBlue, apa)"""
    def ov(C): flowp(C, TANK_IN, n, speed, col, r, t0=t_on, t1=t_off, lat=5.0, seed=3, glow=0.35, jit=0.1)
    return ov
def tank(E, t0, t1, st='dry', labs=(), ov=None, kb=None, y=1200, tr=('xf', 0.3), **kw):
    """plan cu rezervorul in sectiune (camera 'tank'): etichetele de jos la y=1200, sub rezervor"""
    kw.setdefault('phase', False)
    return Shot('tank', t0, t1, st=st, kb=kb or [(t0, 1.0, 0, -20), (t1, 1.06, 0, -30)], ov=ovs(ov, bl(E, labs, t1, y=y) if labs else None), tr=tr, **kw)
def film(E, t0, t1, st='mclean', labs=(), ov=None, kb=None, flow=None, tr=('xf', 0.3), head='VEDERE MĂRITĂ', sides=('CAMA', 'ROLA'), t_sides=None, **kw):
    """pelicula dintre doua piese, marita (camera 'microf' din seria injectoarelor: banda verticala intre doua blocuri hasurate);
    flow = (culoare 0-255, t_on, t_off) pentru licaririle care curg prin pelicula"""
    kw.setdefault('phase', False)
    hid = E.lb(head, 'grey') if head else None; sl = [E.lb(x, 'grey') for x in sides] if sides else []
    def o(C):
        if flow: flowp(C, [(540, -40), (540, 1960)], 34, 260.0, flow[0], 4.5, t0=flow[1], t1=flow[2] if len(flow) > 2 else None, lat=52.0, seed=6, glow=0.3, a=0.8)
        if hid: F.spr(C, hid, 540, 372, t0 + 0.05, t1 + 0.1, anchor='tc')
        ts = t0 + 0.4 if t_sides is None else t_sides
        for sid, x in zip(sl, (236, 844)): F.spr(C, sid, x, 700, ts, t1 + 0.1, anchor='tc')
    return Shot('microf', t0, t1, st=st, kb=kb or [(t0, 1.0, 0, 0), (t1, 1.06, 0, 0)], ov=ovs(o, ov, bl(E, labs, t1) if labs else None), tr=tr, **kw)

# ------------------------------------------------------------------ pistolul de la pompa si busonul, la gura de umplere a rezervorului (desen 2D peste placa 'tank')
def nozzle_html(col='#3ddc84', dark='#1f9d4d'):
    return ('<svg width="340" height="330" viewBox="0 0 340 330"><path d="M-10 -8 L84 60" stroke="#0e1319" stroke-width="44" stroke-linecap="round"/>'
            '<path d="M-10 -8 L84 60" stroke="#27313c" stroke-width="30" stroke-linecap="round"/>'
            '<path d="M112 132 Q92 196 150 202 Q204 202 194 150" fill="none" stroke="%s" stroke-width="17" stroke-linecap="round"/>'
            '<path d="M70 48 L172 124" stroke="%s" stroke-width="82" stroke-linecap="round"/><path d="M70 48 L172 124" stroke="%s" stroke-width="60" stroke-linecap="round"/>'
            '<path d="M84 44 L150 93" stroke="rgba(255,255,255,.35)" stroke-width="10" stroke-linecap="round"/>'
            '<path d="M180 130 L300 300" stroke="#6c7884" stroke-width="32" stroke-linecap="round"/><path d="M180 130 L300 300" stroke="#dfe6ee" stroke-width="18" stroke-linecap="round"/></svg>'
            % (dark, dark, col))
def cap_html(text='DIESEL', col='#FFD21F'):
    return ('<div style="width:156px;height:156px;border-radius:50%%;background:#10161d;border:7px solid #2f3b47;box-shadow:inset 0 0 0 9px #1a222b;display:flex;'
            'align-items:center;justify-content:center"><span style="font:800 31px/1 Mont;letter-spacing:.04em;color:%s">%s</span></div>' % (col, text))
def tank_nozzle(E, t_in, t_out=None, col='#3ddc84', dark='#1f9d4d', cap='DIESEL', cap_col='#FFD21F', cap_at=(96, -214)):
    """pistolul in gura de umplere (varful lui la capatul taiat al tevii) si busonul cu inscriptie alaturi"""
    nid = E.add(nozzle_html(col, dark)); cid = E.add(cap_html(cap, cap_col)) if cap else None
    def ov(C):
        x, y = pk(C, [(24, 730)])[0]
        F.spr(C, nid, x - 300, y - 300, t_in, t_out, slide=(-26, -34))
        if cid: F.spr(C, cid, x + cap_at[0], y + cap_at[1], t_in + 0.15, t_out)
    return ov

# ------------------------------------------------------------------ doua lupe: pelicula care tine si pelicula care se rupe
def film_pair(E, t_in, t_out, t_break, y=930, R=170, xs=(250, 830), src=None, chips=True, t_chips=None, thin=(0.93, 0.86, 0.56),
              good=('MOTORINĂ', 'Pelicula ține'), bad=('AMESTEC SUBȚIRE', 'Pelicula se rupe')):
    """stanga: pelicula groasa de motorina (placa microf:mclean, in galbenul seriei); dreapta: pelicula subtire, care la t_break se rupe (microf:mdry) si scanteiaza.
    src = punctul de pe placa de care sunt legate lupele (3D, ('px', x, y) sau functie C -> punct)"""
    pf_y = pf_tint(LPY, which='hp'); pf_t = pf_tint(thin, which='hp')
    cg = E.lb(good[0], 'good', good[1]) if chips else None; cb = E.lb(bad[0], 'bad', bad[1]) if chips else None
    def ov(C):
        t = C.t; a = F.pop(t, t_in, t_out, 0.3, 0.3)
        if a <= 0.003: return
        sp = src(C) if callable(src) else src
        F.lens(C, 'microf', 'mclean', xs[0], y, R, t_in, t_out, src=sp, ring=(61, 220, 132), pf=pf_y, tag='filmY')
        F.lens(C, 'microf', 'mclean', xs[1], y, R, t_in + 0.12, t_out, src=sp, ring=(255, 75, 75), pf=pf_t, tag='filmT')
        F.lens(C, 'microf', 'mdry', xs[1], y, R, t_break, t_out, ring=(255, 75, 75), grow=False, din=0.45)
        D.flow2(C, [D.Poly([(xs[0], y - R + 16), (xs[0], y + R - 16)])], 12, 150.0, (255, 242, 180), 4.0, t0=t_in + 0.3, a=0.85 * a, seed=6, glow=0.3, lat=38.0)
        D.flow2(C, [D.Poly([(xs[1], y - R + 16), (xs[1], y + R - 16)])], 7, 170.0, (255, 246, 200), 3.2, t0=t_in + 0.4, t1=t_break, a=0.7 * a, seed=9, glow=0.2, lat=30.0)
        e = float(seg(t, t_break + 0.15, t_break + 0.45)) * a
        if e > 0.003:                                                          # scantei pe linia pe care piesele se ating
            r = X.rnd(31, 16, 4)
            for i in range(16):
                ph = (t * (2.0 + 2.2 * r[i, 0]) + r[i, 1]) % 1.0
                if ph < 0.42:
                    u = ph / 0.42; yy = y + (r[i, 2] * 2 - 1) * (R - 34); xx = xs[1] + (r[i, 3] * 2 - 1) * 6 + u * 30 * (1 if i % 2 else -1)
                    D.dots2(C, np.array([[xx, yy + u * 26]]), 5.5 * (1 - u) + 1.5, (255, 214, 130), e, glow=0.9)
        if chips:
            tc = t_in + 0.4 if t_chips is None else t_chips
            F.spr(C, cg, xs[0], y + R + 16, tc, t_out, anchor='tc'); F.spr(C, cb, xs[1], y + R + 16, t_break - 0.05, t_out, anchor='tc')
    return ov

# ------------------------------------------------------------------ particule dure: fire de praf 2D, pulbere colorata pe traseele 3D, hartia de filtru incarcata
DUST2 = (186, 132, 72); DUSTD = (62, 38, 18); SAND2 = (232, 204, 140); DUST3 = (0.56, 0.37, 0.18); RUST3 = (0.66, 0.27, 0.09); SAND3 = (0.9, 0.78, 0.5)
def grain2(C, x, y, r, a=1.0, seed=3, col=DUST2, dark=DUSTD):
    """un fir de praf desenat 2D (coordonate 1080x1920): cateva pete suprapuse, cu contur inchis si o lumina mica"""
    if a <= 0.003: return
    rr = X.rnd(seed, 5, 3)
    pts = np.stack([x + (rr[:, 0] - 0.5) * r * 1.0, y + (rr[:, 1] - 0.5) * r * 0.8], -1)
    D.dots2(C, pts, r * 0.74, dark, a); D.dots2(C, pts, r * 0.56, col, a)
    D.dots2(C, pts[:2] - np.array([r * 0.16, r * 0.2]), r * 0.2, tuple(min(255, int(c * 1.32)) for c in col), 0.85 * a)

def fx_grit(paths, t_on=None, t_off=None, n=24, speed=15.0, size=0.5, a=1.0, col=DUST3, seed=81, lat=0.9, minpx=1.5):
    """pulbere colorata (praf, rugina, nisip) dusa de motorina pe trasee 3D: graunte cu contur inchis, ca sa se vada pe galben"""
    cl = np.asarray(col, np.float32)
    def f(C):
        e = env(C.t, None, t_off)
        if e <= 0.003: return
        for i, pn in enumerate(paths):
            F.flow(C, pn, n, speed, np.array([0.13, 0.08, 0.04]), size * 1.42, lat=lat, seed=seed + i, t0=t_on, mode='over', shape='d', shade=0, sz_var=0.6, a=0.9 * a * e, minpx=minpx * 1.3)
            F.flow(C, pn, n, speed, cl, size, lat=lat, seed=seed + i, t0=t_on, mode='over', shape='d', shade=0.4, sz_var=0.6, a=a * e, minpx=minpx)
    return f

def pf_paper(col=(0.6, 0.42, 0.24), t0=None, t1=None, w=0.8, box=None):
    """hartia filtrului (alb mat) incarcata cu murdarie: se inchide spre maro; box = (x0, y0, x1, y1) px la 1080 = zona in care se cauta hartia"""
    col = np.asarray(col, np.float32)
    def f(rgba, t):
        ww = w * (1.0 if t0 is None else float(seg(t, t0, t1)))
        if ww <= 0.003: return rgba
        k = rgba.shape[1] / 1080.0
        x0, y0, x1, y1 = [int(v * k) for v in (box or (0, 0, 1080, 1920))]
        sub = rgba[y0:y1, x0:x1]; al = np.maximum(sub[..., 3:4], 1e-4); c = np.clip(sub[..., :3] / al, 0, 1)
        mx = c.max(-1); mn = c.min(-1); sat = (mx - mn) / np.maximum(mx, 1e-3)
        m = (np.clip((mx - 0.6) / 0.12, 0, 1) * np.clip((0.2 - sat) / 0.08, 0, 1) * np.clip((c[..., 0] - c[..., 2] + 0.012) / 0.02, 0, 1))[..., None] * ww
        new = col[None, None, :] * (0.35 + 0.75 * mx[..., None])
        out = rgba.copy(); out[y0:y1, x0:x1, :3] = (c * (1 - m) + new * m) * sub[..., 3:4]
        return out
    return f

def gap_fx(t_on=None, grit=None, hits=(), col=(1.0, 0.75, 0.5)):
    """placa 'micro' / 'microz' (jocul dintre doua piese, vertical): licariri de motorina prin joc; grit = momentul din care trec si particule; hits = momentele scanteilor"""
    gp = F.IPath([[0, -0.1, 170], [0, -0.1, -170]], None, 1.0, smooth=0, step=1.0)
    gp.L = np.tile(np.array([1.0, 0, 0]), (gp.n, 1))
    def f(C):
        F.flow(C, gp, 30, 46.0, np.asarray(col), 0.25, lat=0.9, seed=5, t0=t_on, mode='add', shape='g', shade=0, a=0.5)
        if grit is not None: F.grit(C, gp, 9, 38.0, size=1.15, seed=8, t0=grit, lat=0.25, sz_var=0.35)
        for i, tb in enumerate(hits):
            zz = 80 - (i * 37) % 160
            F.sparks(C, np.array([1.5 if i % 2 else -1.5, -0.2, zz]), tb, n=18, life=0.28, speed=26.0, size=0.45, seed=60 + i)
    return f

def sparks2(C, x, y, t, t_on, t_off=None, n=12, a=1.0, L=30.0, R=40.0, seed=31, col=(255, 214, 130)):
    """scantei 2D in jurul unui punct (sau de-a lungul unei verticale de inaltime R), pornite la t_on"""
    e = float(seg(t, t_on, t_on + 0.2)) * (1.0 if t_off is None else 1.0 - float(seg(t, t_off, t_off + 0.3))) * a
    if e <= 0.003: return
    r = X.rnd(seed, n, 4)
    for i in range(n):
        ph = (t * (2.0 + 2.2 * r[i, 0]) + r[i, 1]) % 1.0
        if ph < 0.42:
            u = ph / 0.42; yy = y + (r[i, 2] * 2 - 1) * R; xx = x + (r[i, 3] * 2 - 1) * 6 + u * L * (1 if i % 2 else -1)
            D.dots2(C, np.array([[xx, yy + u * 0.8 * L]]), 5.5 * (1 - u) + 1.5, col, e, glow=0.9)

# ------------------------------------------------------------------ apa: picaturi pe traseele 3D, condensul din rezervor, filtrul cu separator (placile 'tank' si 'filter' din seria injectoarelor)
WATER3 = np.array([0.18, 0.61, 1.0])
TJ = json.load(open('/home/claude/w/serinj/blend/tank.json')); TD = TJ['dims']
FJ = json.load(open('/home/claude/w/inj/out/filter.json'))
def fx_drops(paths, t_on=None, t_off=None, n=12, speed=15.0, size=0.9, a=1.0, col=WATER3, seed=27, lat=0.7):
    """picaturi (apa, AdBlue) duse de motorina pe trasee 3D: sfere colorate cu o lumina mica"""
    def f(C):
        e = env(C.t, None, t_off)
        if e <= 0.003: return
        for i, pn in enumerate(paths):
            F.flow(C, pn, n, speed, np.asarray(col), size, lat=lat, seed=seed + i, t0=t_on, mode='over', shape='d', shade=0.55, sz_var=0.45, a=a * e, minpx=1.6)
            F.flow(C, pn, n, speed, np.array([0.85, 0.95, 1.0]), size * 0.35, lat=lat, seed=seed + i, t0=t_on, mode='add', shape='g', shade=0, a=0.6 * a * e, sz_var=0.45)
    return f

def fx_tank_cond(t_cond, t_fall, n=14):
    """condensul din rezervor: picaturi care cad din tavan, trec prin motorina si se aduna pe fund"""
    T, ZW, ZF, LZ = TD['T'], TD['ZW'], TD['ZF'], TD['LZ']
    r = X.rnd(55, n, 5)
    def f(C):
        t = C.t
        for i in range(n):
            ta = t_fall + i * 0.42
            if t < ta: continue
            x = -200 + r[i, 0] * 260; y = 40 + r[i, 1] * 90; z0 = LZ - T - 6
            u = t - ta; zf = z0 - 0.5 * 2600 * u * u
            if zf < ZF:
                tf = math.sqrt(2 * (z0 - ZF) / 2600); zf = ZF - 34 * (u - tf)
            if zf < ZW + 3: continue
            F.dots3(C, np.array([x, y, zf]), 5.0 + 2.0 * r[i, 2], WATER3, 1.0, shade=0.6, ztest=False)
            F.dots3(C, np.array([x - 1.5, y - 2, zf + 1.5]), 1.8, np.array([0.9, 0.97, 1.0]), 0.8, mode='add', shape='g', shade=0, ztest=False)
        a = float(seg(t, t_cond, t_cond + 1.0)) * (0.5 + 0.5 * math.sin(t * 2.2) ** 2)
        F.glow(C, np.array([0, 60, (T + ZW) / 2]), 260 * C.k, WATER3, 0.18 * a)
    return f

UR_F = np.array(FJ['uR'], float) if not isinstance(FJ['uR'], (int, float)) else None; UL_F = np.array(FJ['uL'], float) if not isinstance(FJ['uL'], (int, float)) else None
def fx_sep(t_on, t_out=None, water=True):
    """filtrul cu separator: motorina intra, picaturile de apa coboara spre pahar; dupa t_out (paharul plin) apa urca spre iesire"""
    pup = F.IPath(FJ['paths']['up'], None, 2.0, smooth=6, step=0.5)
    pin = F.IPath(FJ['paths']['in'][1:], 'L', 3.0, smooth=6, step=0.5)
    r = X.rnd(81, 30, 4); EZ = np.array([0.0, 0.0, 1.0])
    def f(C):
        t = C.t
        F.flow(C, pin, 40, 70.0, np.array([1.0, 0.85, 0.5]), 0.9, lat=0.7, seed=12, mode='add', shape='g', shade=0, a=0.5)
        if water:
            F.flow(C, pin, 12, 60.0, WATER3, 2.2, lat=0.7, seed=13, mode='over', shape='d', shade=0.55, t1=None if t_out is None else t_out + 0.5)
            for i in range(30):                      # picaturile coboara printre straturi spre pahar
                ta = t_on + (i * 0.23) % 6.0 + int(i * 0.23 / 6.0) * 6.0
                u = (t - ta) % 3.2
                if t < ta: continue
                z = 60 - 14 * u; rr = 12 + r[i, 0] * 15
                if z < 18: continue
                Pp = (UR_F if i % 2 else UL_F) * rr + EZ * z + (F.NR if i % 2 else F.NL) * 0.6
                F.dots3(C, Pp, 1.6 + r[i, 1] * 1.0, WATER3, 1.0, shade=0.55)
        if t_out is not None and t > t_out:
            if water: F.flow(C, pup, 30, 70.0, WATER3, 2.0, lat=0.6, seed=14, t0=t_out, mode='over', shape='d', shade=0.55)
        F.flow(C, pup, 50, 90.0, np.array([1.0, 0.85, 0.5]), 0.9, lat=0.6, seed=15, mode='add', shape='g', shade=0, a=0.5)
    return f

def fx_drain(t_on, dur=4.0, z1=-70.0, n=40, size=2.2):
    """apa care curge pe surubul de golire al separatorului (z1 = pana unde cade, mm)"""
    pd = F.IPath([[0.0, 0, 6.0], [0.0, 0, -9.0], [0.0, 0, z1]], None, 1.5, smooth=4, step=0.5)
    def f(C):
        F.flow(C, pd, n, 42.0, WATER3, size, lat=0.5, seed=16, t0=t_on, t1=t_on + dur, mode='over', shape='d', shade=0.55, ztest=False)
    return f

WATER_HL = dict(col='#46a0f5', fill='rgba(70,160,245,.22)'); RUST_HL = dict(col='#c4602a', fill='rgba(196,96,42,.24)')
def pf_front(col, t0, t1, y0=-120.0, y1=2040.0, curve=70.0, which='lp', ref=0.79, xc=540.0, hw=76.0):
    """lichidul din placa se recoloreaza de sus in jos, cu un front rotunjit care coboara intre t0 si t1 (apa care ia locul motorinei in pelicula marita)"""
    col = np.asarray(col, np.float32)
    def f(rgba, t):
        u = float(seg(t, t0, t1))
        if u <= 0: return rgba
        h, w = rgba.shape[:2]; k = w / 1080.0
        yf = (y0 + (y1 - y0) * u) * k
        al = np.maximum(rgba[..., 3:4], 1e-4); c = np.clip(rgba[..., :3] / al, 0, 1)
        m = liq_mask(c, which, False)
        y = np.arange(h, dtype=np.float32)[:, None]; x = np.arange(w, dtype=np.float32)[None, :]
        fr = yf - curve * k * np.clip(((x - xc * k) / (hw * k)) ** 2, 0, 1.5)
        m = (m * np.clip((fr - y) / (4.0 * k) + 0.5, 0, 1))[..., None]
        mx = c.max(-1, keepdims=True); new = np.clip(col[None, None, :] * (mx / ref), 0, 1)
        out = rgba.copy(); out[..., :3] = (c * (1 - m) + new * m) * rgba[..., 3:4]
        return out
    return f

# ------------------------------------------------------------------ AdBlue: cristale albe pe piese (pe placa, pentru lupe si planuri fixe)
ADBS = (0.8, 0.94, 1.0); CRY3 = (0.95, 0.97, 1.0)
def pf_cryst(n=70, seed=3, box=(0, 0, 1080, 1920), r=(4.0, 11.0), col=(0.96, 0.98, 1.0), t0=None, t1=None, amin=0.6, liq=False, only_liq=False, edge=(200, 214, 232)):
    """cristale albe, colturoase, presarate pe piesele din placa, in dreptunghiul box (px la 1080); cresc pe rand intre t0 si t1.
    liq=False: nu se aseaza pe lichid (galben sau portocaliu), doar pe metal si pe hartie"""
    rr = X.rnd(seed, n, 8); cache = {}
    def f(rgba, t):
        e = 1.0 if t0 is None else float(seg(t, t0, t1))
        if e <= 0.003: return rgba
        h, w = rgba.shape[:2]; k = w / 1080.0
        if (h, w) not in cache:
            Lp = []
            for i in range(n):
                x = (box[0] + rr[i, 0] * (box[2] - box[0])) * k; y = (box[1] + rr[i, 1] * (box[3] - box[1])) * k
                R = (r[0] + (r[1] - r[0]) * rr[i, 2] ** 2) * k; m = 4 + int(rr[i, 3] * 2.99); a0 = rr[i, 4] * 6.283
                pts = [(x + R * (0.55 + 0.45 * ((i * 7 + j * 3) % 5) / 4.0) * math.cos(a0 + j * 6.283 / m), y + R * (0.55 + 0.45 * ((i * 5 + j * 2) % 5) / 4.0) * math.sin(a0 + j * 6.283 / m)) for j in range(m)]
                Lp.append(((np.array(pts) * 16).astype(np.int32), rr[i, 5], rr[i, 6]))
            cache[(h, w)] = Lp
        ov = np.zeros((h, w, 4), np.uint8)
        for pts, thr, sh in cache[(h, w)]:
            g = float(np.clip((e - 0.8 * thr) / 0.2, 0, 1))
            if g <= 0: continue
            c = 0.8 + 0.2 * sh
            cv2.fillPoly(ov, [pts], (int(255 * col[0] * c), int(255 * col[1] * c), int(255 * col[2] * c), int(255 * g)), cv2.LINE_AA, shift=4)
            cv2.polylines(ov, [pts], True, (int(edge[0] * c), int(edge[1] * c), int(edge[2] * c), int(255 * g)), max(1, int(1.5 * k)), cv2.LINE_AA, shift=4)
        a = ov[..., 3:4].astype(np.float32) / 255.0 * np.clip((rgba[..., 3:4] - amin) / 0.2, 0, 1)
        if not liq:
            al = np.maximum(rgba[..., 3:4], 1e-4); c3 = np.clip(rgba[..., :3] / al, 0, 1)
            a = a * (1.0 - np.clip(liq_mask(c3, 'all', False), 0, 1))[..., None]
        if only_liq:
            al = np.maximum(rgba[..., 3:4], 1e-4); c3 = np.clip(rgba[..., :3] / al, 0, 1)
            a = a * np.clip(liq_mask(c3, 'all', False), 0, 1)[..., None]
        out = rgba.copy(); out[..., :3] = rgba[..., :3] * (1 - a) + ov[..., :3].astype(np.float32) / 255.0 * a * rgba[..., 3:4]
        return out
    return f

# ------------------------------------------------------------------ modelele noi (regulator, cupla rapida, capatul conductei, raftul): puncte si trasee 3D din blend/<nume>.json
def mj(name):
    """punctele si traseele unui model nou: (pts, paths), ca vectori numpy (mm)"""
    J = json.load(open('/home/claude/w/serpmp/blend/%s.json' % name))
    return ({k: np.array(v, float) for k, v in J.get('pts', {}).items()}, {k: [np.array(p, float) for p in v] for k, v in J.get('paths', {}).items()})
def p3(C, pts):
    """puncte 3D (mm, in modelul placii curente) -> coordonatele cadrului (1080x1920) la momentul C.t"""
    out = []
    for p in pts:
        x, y = C.P(np.asarray(p, float)); out.append((x / C.k, y / C.k))
    return out
def flow3(C, pts, n, speed, col, r, t0=None, t1=None, a=1.0, seed=1, glow=0.0, ring=False, lat=0.0, jit=0.25, dark=0.0):
    """ca flowp, dar traseul e dat in 3D (mm), in modelul placii curente; viteza si raza in px la zoom 1"""
    z = C.shot.kbat(C.t)[0]; poly = [D.Poly(p3(C, pts))]
    if dark: D.flow2(C, poly, n, speed * z, (16, 22, 30), (r + 1.5) * z, t0=t0, t1=t1, a=a * dark, seed=seed, jit=jit, lat=lat * z)
    D.flow2(C, poly, n, speed * z, col, r * z, t0=t0, t1=t1, a=a, seed=seed, glow=glow, jit=jit, lat=lat * z, ring=ring)
def lab3(C, items, t_out):
    """etichete pe puncte 3D ale placii curente: items = [(sprite, punct, (x, y), t_in[, ancora])]"""
    for it in items:
        F.label(C, it[0], np.asarray(it[1], float), it[2], it[3], t_out, anchor=it[4] if len(it) > 4 else 'tl')
