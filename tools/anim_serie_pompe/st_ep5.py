# Episodul 5: particulele si filtrul neschimbat
import math
import numpy as np
import pser as S, ifx as F, i2d as D, ikit as K, pdraw as P, fxlib as X
from icomp import Shot
from fxlib import seg, ease
E = S.Ep(5); W, L, LE = E.W, E.L, E.LE; TOTAL = E.TOTAL; GLOB = S.glob(E)

# ------------------------------------------------------------------ carligul: sub lupa, un fir de par, un fir de praf si jocul pistonului, mai mic decat amandoua;
# firul de praf intra in joc si lasa o zgarietura (coperta, la 1,85 s: toate trei, cu etichete)
HX, HY, HR = 540, 958, 218
l_hair = E.lb('FIR DE PĂR', 'grey'); l_dust = E.lb('FIR DE PRAF', 'bad'); l_gap = E.lb('JOCUL PISTONULUI', 'lp')
T_IN = 1.98; _jx = (X.rnd(17, 14, 2) - 0.5) * 3.0
def ov_hook(C):
    t = C.t; te = E.T_S + 0.1; k = C.k
    F.lens(C, 'micro', 'mhair', HX, HY, HR, 0.1, te, kb=(0.45, 0, 14))
    a = F.pop(t, 0.4, te, 0.25, 0.3)
    u = float(ease(seg(t, T_IN, T_IN + 0.3))); v = float(seg(t, T_IN + 0.25, E.T_S + 0.1))
    gx = HX + 96 * (1 - u); gy = HY + 62 + 120 * v
    if v > 0:
        ys = np.linspace(HY + 62, gy, 14)
        for sx, j in ((-9, 0), (9, 1)): D.line2(C, [(HX + sx + _jx[i, j], ys[i]) for i in range(14)], (255, 75, 75), 4, a)
        S.sparks2(C, gx, gy, t, T_IN + 0.3, n=10, a=a, L=26.0, R=8.0)
    S.grain2(C, gx, gy, 15.0 - 3.0 * u, a)
    F.label(C, l_hair, ('px', HX - 118, HY - 126), (40, 744), 0.55, te)
    F.label(C, l_dust, ('px', gx + 12, gy - 6), (1040, 800), 0.95, te, anchor='tr')
    al = F.pop(t, 1.3, te)
    if al > 0.003:
        F._line(C, (HX * k, (HY + 192) * k), (HX * k, (HY + 246) * k), al)
        F.spr(C, l_gap, HX, HY + 244, 1.3, te, anchor='tc')
HOOK = [S.pump(E, 'ph', 0.0, E.T_S, kb=[(0.0, 1.0, 0, 0), (E.T_S, 1.04, 0, 0)], tr=None, dim=lambda t: 0.3, ov=ov_hook, fx=[])]

SIGNS = S.symptoms(E, 2, [(E.sym('power', 'TRAGE TOT MAI SLAB', cls='warn'), 'trage'), (E.sym('start', 'PORNEȘTE MAI GREU'), 'porneste'),
                          (E.sym('warn', 'EROARE DE PRESIUNE', 'În rampă'), 'eroarea')], cam='fl', st='ffull', fx=[S.fx_flt_fuel()], y0=740, dy=160)

# ------------------------------------------------------------------ peste 2.000 de bari, cu jocuri de cativa microni; un fir de par e de zeci de ori mai gros
T_3M = W(3, 'jocuri') - 0.1
KB_3 = [(L(3), 1.0, 0, 30), (T_3M, 1.22, 70, 190)]
l_2000 = E.lb('PESTE 2.000 BAR', 'num hp'); l_pis = E.lb('PISTON', 'grey'); l_cil = E.lb('CILINDRU', 'grey')
def ov_head(C):
    te = T_3M + 0.12
    F.label(C, l_2000, F.PR(10.0, 81.6), (536, 610), W(3, 'peste') - 0.25, te)
    F.label(C, l_pis, S.P_plunger(S.hC(C)), (330, 850), W(3, 'pistoanele') - 0.1, te, anchor='tr')
    F.label(C, l_cil, F.PR(8.0, 62.0), (650, 810), W(3, 'cilindri') - 0.1, te)
bh3 = S.scr('ph', 'fuel', F.PR(3.25, 66.0), KB_3[-1][1:])
l_few = E.lb('CÂȚIVA MICRONI', 'num hp', 'Jocul dintre piston și cilindru'); l_hair2 = E.lb('FIR DE PĂR', 'grey big', 'De zeci de ori mai gros')
def ov_micro(C):
    te = L(4) + 0.15
    F.spr(C, l_pis, 258, 950, T_3M + 0.5, te, anchor='tc'); F.spr(C, l_cil, 822, 950, T_3M + 0.5, te, anchor='tc')
    x, y = S.pk(C, [(553, 1158)])[0]
    F.label(C, l_few, ('px', x, y), (596, 1070), W(3, 'cativa') - 0.15, te)
    F.spr(C, l_hair2, 60, 520, W(3, 'par') - 0.1, te)
SCALE = [
 S.pump(E, 'ph', L(3), T_3M, kb=KB_3, fx=[S.fx_fuel()], ov=ov_head,
        labs=[('POMPA RIDICĂ PRESIUNEA', 'hp big', L(3) + 0.2), ('PISTONUL LUCREAZĂ ÎN CILINDRU', 'grey', W(3, 'pistoanele') - 0.1)]),
 Shot('micro', T_3M, L(4), st='mclean', seq=[('mhair', W(3, 'un') - 0.05, W(3, 'un') + 0.5)], tr=('dive', 0.7, bh3, 3.0, 'full'),
      kb=[(T_3M, 1.05, 0, -40), (L(4), 1.08, 0, -40)], fx=[S.gap_fx(T_3M - 3.0)], ov=ov_micro, phase=False),
]

# ------------------------------------------------------------------ filtrul opreste particulele; unul vechi, ieftin sau nepotrivit le lasa sa treaca
T_4B = W(4, 'un') - 0.1
BL = [F.PR(41.4, z) for z in (120, 102, 84, 66, 48, 30)] + [F.PLf(-41.4, z) for z in (120, 102, 84, 66, 48, 30)]
l_paper = E.lb('HÂRTIA', 'grey', 'Reține particulele')
def ov_flt(C): F.label(C, l_paper, F.PLf(-30.0, 108.0), (24, 640), W(4, 'opreste') - 0.2, T_4B + 0.12)
def chip(col, text):
    return E.lb('<span style="display:inline-block;width:24px;height:24px;border-radius:50%%;background:%s;margin-right:12px;vertical-align:-2px;box-shadow:0 0 0 3px rgba(0,0,0,.55)"></span>%s' % (col, text), 'bad')
CH = [(chip('#b9844a', 'PRAF'), W(4, 'praf'), 226), (chip('#b3501e', 'RUGINĂ'), W(4, 'rugina'), 532), (chip('#e6cc8c', 'NISIP FIN'), W(4, 'nisip'), 846)]
def ov_flz(C):
    for sid, ti, x in CH: F.spr(C, sid, x, 1096, ti - 0.12, L(5) + 0.12, anchor='tc')
FLT = [
 Shot('fl', L(4), T_4B, st='ffull', kb=[(L(4),) + S.KB_FL, (T_4B, 0.94, 0, 62)], phase=False, tr=('xf', 0.3),
      fx=[S.fx_flt_fuel(), S.fx_grit(('flt_outR', 'flt_outL'), L(4) - 2.0, n=22, speed=24.0, size=1.25, lat=0.8), S.fx_blotch(BL, S.DUST3, L(4) + 0.5, T_4B - 0.3, R=3.6, n=16, soft=False)],
      ov=S.ovs(ov_flt, S.bl(E, [('FILTRUL OPREȘTE PARTICULELE', 'good big', L(4) + 0.25)], T_4B))),
 Shot('flz', T_4B, L(5), st='ffull', kb=[(T_4B, 1.0, 0, 0), (L(5), 1.05, 0, 0)], phase=False, tr=('xf', 0.3), pf=S.pf_paper(t0=T_4B + 0.3, t1=T_4B + 2.6, w=0.72),
      fx=[S.fx_flt_fuel(), S.fx_grit(('flt_outR', 'flt_outL'), T_4B - 3.0, n=22, speed=22.0, size=1.2, lat=0.8),
          S.fx_grit(('flt_inR', 'flt_inL'), W(4, 'lasa') - 0.4, n=26, speed=10.0, size=1.2, col=S.DUST3, seed=91),
          S.fx_grit(('flt_inR', 'flt_inL'), W(4, 'rugina') - 0.7, n=18, speed=10.0, size=1.2, col=S.RUST3, seed=95),
          S.fx_grit(('flt_inR', 'flt_inL'), W(4, 'nisip') - 0.7, n=18, speed=10.0, size=1.05, col=S.SAND3, seed=99),
          S.fx_grit(('flt_core', 'flt_coreL'), W(4, 'lasa') + 0.8, n=14, speed=30.0, size=1.2, seed=103)],
      ov=S.ovs(ov_flz, S.bl(E, [('FILTRU VECHI, IEFTIN SAU NEPOTRIVIT', 'bad', T_4B + 0.15), ('LASĂ PARTICULELE SĂ TREACĂ', 'bad big', W(4, 'lasa') - 0.15)], L(5)))),
]

# ------------------------------------------------------------------ particulele ajung intre piston si cilindru si intre cama si rola; zgarie, iar pompa pierde presiune pe langa piston
T_5B = W(5, 'si', 2) - 0.12; T_5C = W(5, 'iar') - 0.1
KB_P = (1.6, 168, 384); KB_M = S.kb_on('pm', 'fuel', S.P_contact(S.H0, -3.5), 1.45, 540, 800)
G_R = [(350, 316), (424, 316), (437, 392), (437, 470), (462, 540), (471, 568), (471, 800)]
G_L = [(350, 316), (424, 316), (435, 392), (435, 470), (410, 540), (401, 568), (401, 800)]
_sj = (X.rnd(23, 18, 2) - 0.5) * 3.0; _sy = np.linspace(574, 798, 18)
def scratches(C, t0, te):
    a = F.pop(C.t, t0, te); pr = float(seg(C.t, t0, t0 + 1.1))
    for x, j in ((401, 0), (471, 1)): D.line2(C, S.pk(C, [(x + _sj[i, j], _sy[i]) for i in range(18)]), (255, 75, 75), 5, a, prog=pr)
def ov_pgap(C):
    t0 = L(5) - 3.0; te = T_5B + 0.15
    S.flowp(C, G_R, 13, 170.0, S.DUST2, 4.4, t0=t0, seed=4, lat=2.0, dark=0.9); S.flowp(C, G_L, 13, 170.0, S.DUST2, 4.4, t0=t0, seed=5, lat=2.0, dark=0.9)
    scratches(C, W(5, 'piston') - 0.2, te)
    x, y = S.pk(C, [(471, 690)])[0]; S.sparks2(C, x, y, C.t, W(5, 'piston') - 0.2, n=12, L=30.0, R=150.0)
def fx_trap(t_on, n=14, seed=5):
    """graunte prinse pe linia de contact dintre cama si rola (apar pe rand si freamata)"""
    r = X.rnd(seed, n, 6)
    def f(C):
        t = C.t; e = np.clip((t - t_on - 1.1 * r[:, 0]) / 0.2, 0, 1)
        if e.max() <= 0: return
        y = -6.8 + 6.7 * r[:, 1] + 0.12 * np.sin(t * 23.0 + 40.0 * r[:, 2])
        Pp = np.stack([np.full(n, 0.06), y, S.H0 - 5.5 + 0.3 * (r[:, 3] - 0.5)], -1); sz = 0.7 + 0.6 * r[:, 4]
        F.dots3(C, Pp, 0.62 * sz, np.broadcast_to(np.array([0.13, 0.08, 0.04], np.float32), (n, 3)), e, shade=0, ztest=False)
        F.dots3(C, Pp, 0.45 * sz, np.broadcast_to(np.asarray(S.DUST3, np.float32), (n, 3)), e, shade=0.4, ztest=False)
    return f
l_pres = E.lb('PRESIUNE', 'hp')
def ov_leak(C):
    t = C.t; t0 = T_5C + 0.15; te = L(6) + 0.12
    scratches(C, T_5C - 5.0, te)
    S.flowp(C, [(466, 500), (471, 566), (471, 800), (482, 850)], 16, 200.0, S.HP2, 4.2, t0=t0, seed=7, lat=1.5, glow=0.5)
    S.flowp(C, [(406, 500), (401, 566), (401, 800), (390, 850)], 16, 200.0, S.HP2, 4.2, t0=t0, seed=8, lat=1.5, glow=0.5)
    a = F.pop(t, T_5C + 0.3, te); v = 0.86 - 0.52 * float(ease(seg(t, W(5, 'piarda') - 0.4, L(6) - 0.3)))
    S.gauge(C, 836, 800, 118, v, a, green=(0.72, 1.0)); F.spr(C, l_pres, 836, 940, T_5C + 0.3, te, anchor='tc')
GRIT = [
 S.pump(E, 'ph', L(5), T_5B, kb=[(L(5),) + KB_P, (T_5B, KB_P[0] * 1.04, KB_P[1], KB_P[2])], fx=[], ov=ov_pgap,
        labs=[('ÎNTRE PISTON ȘI CILINDRU', 'bad big', L(5) + 0.3)]),
 Shot('pm', T_5B, T_5C, st='fuel', seq=[('damf', W(5, 'zgarie') - 0.1, W(5, 'zgarie') + 1.3)], kb=[(T_5B,) + KB_M, (T_5C, KB_M[0] * 1.05, KB_M[1], KB_M[2])], phase=False, tr=('xf', 0.3),
      fx=[fx_trap(T_5B + 0.05, n=16), S.fx_dry(T_5B + 0.9, rate=8.0, amp=0.75, size=0.2, speed=30.0)], shake=S.shake_at(W(5, 'zgarie'), 1.4, 2.0),
      ov=S.bl(E, [('ÎNTRE CAMĂ ȘI ROLĂ', 'bad big', T_5B + 0.1), ('ZGÂRIE SUPRAFEȚELE CA UN ȘMIRGHEL', 'bad', W(5, 'zgarie') - 0.1)], T_5C)),
 S.pump(E, 'ph', T_5C, L(6), kb=[(T_5C,) + KB_P, (L(6), KB_P[0] * 1.04, KB_P[1], KB_P[2])], fx=[], ov=ov_leak,
        labs=[('POMPA PIERDE PRESIUNE PE LÂNGĂ PISTON', 'bad', T_5C + 0.2)]),
]

# ------------------------------------------------------------------ din zgarieturi se desprinde metal; uzura se hraneste singura si merge spre injectoare
T_6B = W(6, 'adica') - 0.1; T_6C = W(6, 'uzura') - 0.1
MORE = [
 Shot('pm', L(6), T_6B, st='damf', kb=[(L(6), 1.04, 0, 0), (T_6B, 1.1, 0, 0)], phase=False, tr=('xf', 0.3),
      fx=[fx_trap(L(6) - 5.0), S.fx_dry(L(6), rate=8.0, amp=0.7, size=0.2, speed=30.0), S.fx_flakes(L(6) + 0.1)],
      ov=S.bl(E, [('DIN ZGÂRIETURI SE DESPRINDE METAL', 'bad', L(6) + 0.15)], T_6B)),
 S.pump(E, 'pw', T_6B, T_6C, kb=[(T_6B,) + S.KB_PW, (T_6C, 1.05, 0, 40)],
        fx=[S.fx_fuel(), S.fx_filings(T_6B - 3.0, n=40), S.fx_grit(('bath_R', 'cam_Ldn'), T_6B - 3.0, n=18, size=0.6)],
        labs=[('ȘI MAI MULTE PARTICULE', 'bad big', T_6B + 0.1)]),
 S.sysm(E, T_6C, L(7), hl=[(['pump'], None, T_6C), (['rail'], None, W(6, 'merge') - 0.1), (['inj'], None, W(6, 'spre') - 0.15)],
        flows=[('lp', S.DUST2, 12, 200.0, 5.0, None), ('to_rail', S.METAL2, 12, 170.0, 4.5, T_6C + 0.3), (['to_rail'], S.DUST2, 8, 170.0, 4.5, T_6C + 0.5),
               ('rail_inj', S.METAL2, 16, 170.0, 4.5, W(6, 'merge') - 0.2), (['rail_inj'], S.DUST2, 10, 170.0, 4.5, W(6, 'merge'))],
        labs=[('UZURA SE HRĂNEȘTE SINGURĂ', 'bad big', T_6C + 0.1), ('ȘI MERGE SPRE INJECTOARE', 'bad big', W(6, 'merge') - 0.1)]),
]

# ------------------------------------------------------------------ cum eviti: filtrul nou in locul celui vechi, la intervalul din cartea masinii
bk = E.add(P.book(300)); c_int = E.chk('LA INTERVALUL DIN CARTEA MAȘINII'); c_q = E.chk('DE CALITATE, POTRIVIT MOTORULUI')
c_st = E.stop('NU-L LĂSA DESFĂCUT ÎN PRAF', 'La montaj')
l_old = E.lb('VECHI', 'bad'); l_new = E.lb('NOU', 'good')
CROP = (228, 186, 868, 1462); PF_OLD = S.pf_paper(w=0.85)
def ov_avoid(C):
    t = C.t; te = L(8) + 0.1; tn = W(7, 'schimba') - 0.1
    S.plate_spr(C, 'fl', 'ffull', 196, 654, 0.33, F.pop(t, L(7) + 0.1, te), crop=CROP, pf=PF_OLD, tag='old')
    S.plate_spr(C, 'fl', 'ffull', 470, 654, 0.33, F.pop(t, tn + 0.3, te), crop=CROP, tag='new')
    S.xmark(C, 196, 654, 70, F.pop(t, tn + 0.1, te), th=15)
    S.arrow2(C, (300, 654), (366, 654), (61, 220, 132), 10, F.pop(t, tn + 0.2, te), prog=float(seg(t, tn + 0.2, tn + 0.5)))
    F.spr(C, l_old, 196, 874, L(7) + 0.3, te, anchor='tc'); F.spr(C, l_new, 470, 874, tn + 0.4, te, anchor='tc')
    F.spr(C, bk, 668, 458, W(7, 'intervalul') - 0.6, te)
    F.spr(C, c_int, 540, 962, W(7, 'intervalul') - 0.1, te, anchor='tc'); F.spr(C, c_q, 540, 1046, W(7, 'calitate') - 0.3, te, anchor='tc')
    F.spr(C, c_st, 540, 1134, W(7, 'nu') - 0.15, te, anchor='tc')
AVOID = S.plain(E, L(7), L(8), S.ovs(S.hd(E, 'CUM EVIȚI', L(7), L(8) + 0.1, 'good big'), ov_avoid))

# ------------------------------------------------------------------ ce facem noi
T_9N = W(9, 'si') - 0.1; T_10I = W(10, 'iar') - 0.1
FIND = [(E.lb('PILITURĂ', 'bad'), W(8, 'pilitura')), (E.lb('MIZERIE', 'bad'), W(8, 'mizerie')), (E.lb('FISURI', 'bad'), W(8, 'fisuri'))]
def ov_mic(C):
    te = L(9) + 0.12
    F.lens(C, 'pc', 'dam', 770, 650, 200, W(8, 'microscop') - 0.3, te, kb=S.LENS_KB, src=S.WM_OBJ)
    for i, (sid, ti) in enumerate(FIND): F.spr(C, sid, 56, 560 + 84 * i, ti - 0.1, te)
l_worn = E.lb('PIESĂ ZGÂRIATĂ', 'bad'); l_newp = E.lb('PIESĂ NOUĂ', 'good')
def ov_parts(C):
    te = L(10) + 0.12; t1 = W(9, 'inlocuim') - 0.2; t2 = W(9, 'piese', 2) - 0.25
    F.lens(C, 'pc', 'dam', 262, 660, 158, t1, te, kb=S.LENS_KB, src=S.WM_OBJ, ring=(255, 75, 75))
    F.lens(C, 'pc', 'dry', 818, 660, 158, t2, te, kb=S.LENS_KB, src=S.WM_OBJ, ring=(61, 220, 132))
    F.spr(C, l_worn, 262, 832, t1 + 0.2, te, anchor='tc'); F.spr(C, l_newp, 818, 832, t2 + 0.2, te, anchor='tc')
NOI = [
 S.wk(E, 'wm', L(8), L(9), [('LA DEMONTARE: POMPA, LA MICROSCOP', 'good', W(8, 'demontare') - 0.2)], st='wkdam', ov=ov_mic),
 S.wk_usb(E, L(9), T_9N, labs=[('CURĂȚĂM PIESELE CU ULTRASUNETE', 'good', L(9) + 0.15)], t_dip=W(9, 'ultrasunete') - 0.6),
 S.wk(E, 'wm', T_9N, L(10), [('PIESELE ZGÂRIATE: ÎNLOCUITE CU NOI', 'good', T_9N + 0.15)], st='wkdam', seq=[('wk', W(9, 'piese', 2) - 0.2, W(9, 'piese', 2) + 0.4)], ov=ov_parts),
 S.wk_bench(E, L(10), T_10I, labs=[('TESTĂM POMPA PE BANC', 'good big', W(10, 'testam') - 0.15)],
            rows=[('DEBIT', W(10, 'testam') + 0.1), ('PRESIUNE', W(10, 'testam') + 0.5), ('ETANȘEITATE', W(10, 'banc'))], t_sheet=L(10) + 0.1),
 S.wk_inj(E, T_10I, L(E.OUT), labs=[('PARTICULELE AJUNG ȘI LA INJECTOARE', 'bad', T_10I + 0.15), ('INJECTOARELE, VERIFICATE PE STAND', 'good', W(10, 'le') - 0.1)]),
]

SHOTS = S.opening(E, HOOK) + [SIGNS] + SCALE + FLT + GRIT + MORE + [AVOID] + NOI + [S.ending(E)]
SPR = E.SPR
