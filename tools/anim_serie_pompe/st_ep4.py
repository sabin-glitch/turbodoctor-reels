# Episodul 4: motorina care nu unge
import math
import numpy as np
import pser as S, ifx as F, i2d as D, ikit as K, pdraw as P
from icomp import Shot
from fxlib import seg, ease
E = S.Ep(4); W, L, LE = E.W, E.L, E.LE; TOTAL = E.TOTAL; GLOB = S.glob(E)
MIXT = S.pf_tint(S.MIX, w=0.55, rmin=0.62)             # motorina cu putina benzina: doar usor verzuie
def contact(C): return S.P_contact(S.hC(C))

# ------------------------------------------------------------------ carligul: doua pelicule sub lupa, una tine, cealalta se rupe; intre ele, 460
KB_H = S.kb_on('pc', 'fuel', S.P_contact(S.H0), 1.15, 540, 742)
c460 = E.add('<div class="stat y" style="padding:8px 22px 14px"><b style="font-size:112px;line-height:1">460</b><span style="font-size:27px;margin-top:0">MICRONI</span></div>')
def ov_hook(C): F.spr(C, c460, 540, 930, 1.4, E.T_S + 0.1, anchor='cc')
HOOK = [S.pump(E, 'pc', 0.0, E.T_S, kb=[(0.0,) + KB_H, (E.T_S, KB_H[0] * 1.04, KB_H[1], KB_H[2])], tr=None, dim=lambda t: 0.3,
               ov=S.ovs(S.film_pair(E, 0.1, E.T_S + 0.1, 0.95, y=930, R=165, xs=(250, 830), src=contact, t_chips=0.45), ov_hook))]

SIGNS = S.symptoms(E, 2, [(E.sym('part', 'SE UZEAZĂ ÎN TĂCERE', 'La început, fără semne', cls='warn'), 'pompa'), (E.sym('start', 'PORNEȘTE GREU'), 'porneste'),
                          (E.sym('power', 'PIERDE PUTERE'), 'pierde'), (E.sym('warn', 'EROARE DE PRESIUNE', 'Presiune mică în rampă'), 'eroarea')],
                  cam='pw', st='fuel', kb=S.KB_PW, fx=[S.fx_fuel()], y0=690, dy=140, phase=None)

# ------------------------------------------------------------------ motorina trebuie sa si unga; proba de uzura din standard
T_3B = W(3, 'standardul') - 0.2; T_4S = W(4, 'nu') - 0.3; T_4P = W(4, 'peste') - 0.15
RK = 1.1; rg_a = E.add(P.rig_bath(704)); rg_l = E.add(P.rig_fuel(704)); rg_b = E.add(P.rig_ball(330))
l_std = E.lb('STANDARDUL EUROPEAN EN 590', 'grey big'); l_ball = E.lb('BILĂ DE OȚEL', 'grey'); l_plate = E.lb('PLACĂ DE OȚEL', 'grey'); l_bath = E.lb('MOTORINA DE PROBĂ', 'lp')
BX, BY = 188, 790                                    # coltul baii (704 x 330, adica desenul de 640 x 300 marit cu RK)
def ov_rig(C):
    t = C.t; t0 = T_3B; te = T_4S + 0.15
    F.spr(C, l_std, 540, 372, t0 + 0.1, te, anchor='tc')
    F.spr(C, rg_a, BX, BY, t0 + 0.2, te)
    up = 110.0 * float(ease(seg(t, W(4, 'urma') + 0.5, W(4, 'urma') + 1.2)))                 # la final bila se ridica din baie
    amp = 50.0 * float(seg(t, t0 + 0.9, t0 + 1.4)) * (1.0 - float(seg(t, W(4, 'urma') + 0.2, W(4, 'urma') + 0.6)))
    dx = amp * math.sin((t - t0) * 2 * math.pi * 2.6)
    F.spr(C, rg_b, BX + (320 - 150) * RK + dx, BY + (206 - 422) * RK - up, t0 + 0.45, te, slide=(0, -30))
    F.spr(C, rg_l, BX, BY, t0 + 0.2, te)
    F.label(C, l_plate, ('px', BX + 440 * RK, BY + 226 * RK), (1036, 690), W(3, 'verifica') + 0.2, te, anchor='tr')
    F.label(C, l_bath, ('px', BX + 90 * RK, BY + 150 * RK), (44, 1124), W(3, 'verifica') + 0.6, te)
    F.label(C, l_ball, ('px', BX + 320 * RK + dx - 34, BY + (206 - 50) * RK - up), (44, 620), W(4, 'bila') - 0.5, te)
c460b = E.add('<div class="dim" style="font-size:92px">460 µm<small style="font-size:27px">LIMITA DIN STANDARDUL EN 590</small></div>')
fld = E.add(P.scar_field(222)); src09 = E.lb('DECLARAȚIA PRODUCĂTORILOR, <b>2009</b>', 'src')
def ov_scar(C):
    t = C.t; t0 = T_4S; te = L(5) + 0.15; cx, cy = 540, 826; a = F.pop(t, t0, te, 0.3, 0.3); lim = 110.0
    F.spr(C, fld, cx, cy, t0, te, anchor='cc')
    hw = 96.0 * float(ease(seg(t, t0 + 0.1, t0 + 1.3))) + 64.0 * float(ease(seg(t, T_4P + 0.2, T_4P + 2.6)))
    P.scar(C, cx, cy, hw, a, float(seg(t, T_4P + 0.4, T_4P + 1.6)))
    al = F.pop(t, W(4, 'patru') - 0.3, te)
    S.dash2(C, (cx - lim, cy - 168), (cx - lim, cy + 150), (255, 210, 31), 4, al, n=13); S.dash2(C, (cx + lim, cy - 168), (cx + lim, cy + 150), (255, 210, 31), 4, al, n=13)
    F.bracket(C, (cx - lim, cy - 170), (cx + lim, cy - 170), al, th=4.0)
    F.spr(C, c460b, 540, 436, W(4, 'patru') - 0.3, te, anchor='tc')
    F.spr(C, src09, 540, 1072, W(4, 'spun') - 0.15, te, anchor='tc')
WEAR = [
 S.pump(E, 'pc', L(3), T_3B, labs=[('MOTORINA TREBUIE SĂ ȘI UNGĂ', 'lp big', L(3) + 0.2), ('NU DOAR SĂ ARDĂ', 'grey big', W(3, 'nu') - 0.15)], fx=[S.fx_fuel(n=60, a=0.6)]),
 S.plain(E, T_3B, T_4S, S.ovs(ov_rig, S.bl(E, [('PROBA DE UZURĂ', 'lp big', W(3, 'proba') - 0.5), ('URMA LĂSATĂ PE BILĂ', 'grey big', W(4, 'urma') - 0.1)], T_4S))),
 S.plain(E, T_4S, L(5), S.ovs(ov_scar, S.bl(E, [('URMA DE PE BILĂ, LA MICROSCOP', 'grey', T_4S + 0.15), ('PESTE LIMITĂ', 'bad big', T_4P + 0.1, 'Viața oricărei piese mecanice scade')], L(5)))),
]

# ------------------------------------------------------------------ motorina de la pompa respecta limita; problema e ce se pune in loc sau peste ea
T_5P = W(5, 'problema') - 0.2; T_6F = W(6, 'pelicula') - 0.2; T_6S = W(6, 'iar') - 0.1
dsp = E.add(P.dispenser(380)); c_ok = E.chk('RESPECTĂ LIMITA')
ITEMS = [(E.add(P.item_card(P.jerry(86), 'BENZINĂ')), W(5, 'benzina')), (E.add(P.item_card(P.tin(86), 'PETROL LAMPANT')), W(5, 'petrol')),
         (E.add(P.item_card(P.barrel(86), 'COMBUSTIBIL DE ÎNCĂLZIRE')), W(5, 'combustibil')), (E.add(P.item_card(P.jug(86), 'MOTORINĂ DIN SURSE NESIGURE', cls='warn')), W(5, 'motorina', 2))]
CY = (446, 610, 774, 938)
def ov_fuels(C):
    t = C.t; te = T_6F + 0.15; mv = float(ease(seg(t, T_5P - 0.1, T_5P + 0.5)))
    x = 350 - 318 * mv; y = 474
    F.spr(C, dsp, x, y, L(5) + 0.05, te)
    F.spr(C, c_ok, x + 178, y + 574, W(5, 'respecte') - 0.2, T_5P, anchor='tc')
    for (sid, ti), cy in zip(ITEMS, CY): F.spr(C, sid, 470, cy, ti - 0.12, te, slide=(24, 0))
    D.rbox(C, 458, CY[0] - 12, 594, CY[2] - CY[0] + 166, (255, 75, 75), F.pop(t, L(6) + 0.1, te), th=5, r=18)
FUELS = S.plain(E, L(5), T_6F, S.ovs(ov_fuels, S.bl(E, [('MOTORINA DE LA POMPĂ: ÎN LIMITĂ', 'good big', W(5, 'trebuie') - 0.3), ('PROBLEMA: CE SE PUNE ÎN LOC SAU PESTE EA', 'bad', T_5P + 0.1),
                                                         ('PRIMELE TREI: MAI SUBȚIRI DECÂT MOTORINA', 'bad', L(6) + 0.1), ('UNG MAI SLAB', 'bad big', W(6, 'ung') - 0.15)], T_6F)))

# ------------------------------------------------------------------ pelicula dintre cama si rola se rupe; suprafetele incep sa se roada
KB_F = S.kb_on('pc', 'fuel', S.P_contact(S.H0), 1.3, 540, 500)
bh6 = S.scr('pc', 'fuel', S.P_contact(S.H0), (KB_F[0] * 1.03, KB_F[1], KB_F[2]))
BREAK = [
 S.pump(E, 'pc', T_6F, T_6S, kb=[(T_6F,) + KB_F, (T_6S, KB_F[0] * 1.03, KB_F[1], KB_F[2])], dim=lambda t: 0.3, fx=[S.fx_fuel(n=40, a=0.4)],
        ov=S.film_pair(E, T_6F + 0.1, T_6S + 0.1, W(6, 'rupe') - 0.35, y=830, R=200, xs=(285, 795), src=contact),
        labs=[('PELICULA DINTRE CAMĂ ȘI ROLĂ', 'grey big', T_6F + 0.15), ('SE RUPE', 'bad big', W(6, 'rupe') - 0.15)]),
 Shot('pm', T_6S, L(7), st='fuel', seq=[('damf', T_6S + 0.3, T_6S + 1.5)], tr=('dive', 0.6, bh6, 2.4, 'full'), kb=[(T_6S, 1.0, 0, 0), (L(7), 1.06, 0, 0)],
      fx=[S.fx_dry(T_6S - 0.1, rate=9.0, amp=0.75, size=0.2, speed=30.0), S.fx_flakes(T_6S + 0.9)], phase=False,
      ov=S.bl(E, [('SUPRAFEȚELE ÎNCEP SĂ SE ROADĂ', 'bad big', T_6S + 0.1)], L(7)), shake=S.shake_at(T_6S, L(7) - T_6S + 0.3, 2.0)),
]

# ------------------------------------------------------------------ sfatul vechi: benzina turnata iarna in motorina
T_7M = W(7, 'la') - 0.15
jc = E.add(P.jerry(300, rot=118)); snow = E.add('<div style="zoom:1.9;line-height:0">%s</div>' % K.ICON['cold'])
def ov_winter(C):
    t = C.t; te = T_7M + 0.15
    x, y = S.pk(C, [(24, 730)])[0]
    F.spr(C, jc, x - 232, y - 262, L(7) + 0.15, te, slide=(-20, -26))
    S.xmark(C, x - 82, y - 112, 104, F.pop(t, W(7, 'era') - 0.1, te), th=18)
    F.spr(C, snow, 900, 520, L(7) + 0.3, te, anchor='cc')
WINTER = [
 S.tank(E, L(7), T_7M, kb=[(L(7), 0.8, 170, 60), (T_7M, 0.83, 164, 54)], pf=S.pf_tint(S.MIX, L(7) + 0.8, W(7, 'era'), w=0.55),
        ov=S.ovs(S.tank_in(L(7) + 0.5, W(7, 'era') - 0.2), ov_winter),
        labs=[('SFATUL VECHI: BENZINĂ ÎN MOTORINĂ, IARNA', 'grey', L(7) + 0.2), ('DOAR LA MOTOARELE VECHI', 'grey big', W(7, 'era') - 0.1, 'De dinainte de common rail')]),
 # placa damf nu are bucla de miscare: pompa se opreste (la o faza para, aceeasi cu a placii fixe) chiar inainte sa apara zgarieturile, iar scanteile raman pe contact
 S.pump(E, 'pc', T_7M, L(8), seq=[('damf', W(7, 'inseamna') - 0.2, W(7, 'uzura') + 0.3)], pf=MIXT, kb=[(T_7M, 1.0, 0, 0), (L(8), 1.07, 0, 0)],
        phase=lambda t: 72.0 + min(t - (W(7, 'inseamna') - 0.3), 0.0),
        labs=[('LA O POMPĂ MODERNĂ', 'bad big', T_7M + 0.15, 'Înseamnă uzură')],
        fx=[S.fx_fuel(col=S.MIXS, n=50, a=0.5), S.fx_dry(W(7, 'inseamna') - 0.2)], shake=S.shake_at(W(7, 'inseamna') - 0.1, 1.2, 2.5)),
]

# ------------------------------------------------------------------ cum eviti
dsp2 = E.add(P.dispenser(330)); c_known = E.chk('ALIMENTEAZĂ LA BENZINĂRII CUNOSCUTE')
c_stop = E.stop('NU TURNA NIMIC ÎN REZERVOR', 'Fără acordul producătorului mașinii')
MINI = [E.add(P.jerry(132)), E.add(P.tin(132)), E.add(P.barrel(132)), E.add(P.jug(132, mark=''))]
def ov_avoid(C):
    t = C.t; te = L(9) + 0.1; tn = W(8, 'nu') - 0.15
    F.spr(C, dsp2, 96, 446, L(8) + 0.1, te)
    for i, sid in enumerate(MINI):
        x = 590 + (i % 2) * 200; y = 452 + (i // 2) * 232
        F.spr(C, sid, x, y, tn + 0.08 * i, te); S.xmark(C, x + 66, y + 92, 62, F.pop(t, tn + 0.35 + 0.08 * i, te), th=13)
    F.spr(C, c_known, 540, 958, W(8, 'alimenteaza') - 0.1, te, anchor='tc')
    F.spr(C, c_stop, 540, 1062, tn, te, anchor='tc')
AVOID = S.plain(E, L(8), L(9), S.ovs(S.hd(E, 'CUM EVIȚI', L(8), L(9) + 0.1, 'good big'), ov_avoid))

# ------------------------------------------------------------------ ce facem noi
T_10 = L(10) - 0.1; T_10T = W(10, 'si') - 0.1
gp = E.panel('DEBIT LA PRESIUNE MARE', 500, 392)
_u = np.linspace(0, 1, 40)
CURVES = [(_u, 0.86 - 0.10 * _u ** 2, (61, 220, 132), 5), (_u, 0.80 - 0.55 * _u ** 1.6, (255, 75, 75), 5)]
def ov_graph(C):
    P.graph_panel(C, gp, 786, 452, 500, 392, CURVES, W(9, 'vedem') - 0.5, T_10 + 0.15, W(9, 'vedem'), dur=2.0,
                  tags=[('POMPĂ BUNĂ', (61, 220, 132), 0.98, 0.9), ('POMPĂ UZATĂ', (255, 120, 120), 0.6, 0.1)])
l_worn = E.lb('PIESĂ ROASĂ', 'bad'); l_new = E.lb('PIESĂ NOUĂ', 'good')
def ov_parts(C):
    te = T_10T + 0.15; t1 = W(10, 'inlocuim') - 0.3; t2 = W(10, 'piese', 2) - 0.25
    F.lens(C, 'pc', 'dam', 262, 660, 158, t1, te, kb=S.LENS_KB, src=S.WM_OBJ, ring=(255, 75, 75))
    F.lens(C, 'pc', 'dry', 818, 660, 158, t2, te, kb=S.LENS_KB, src=S.WM_OBJ, ring=(61, 220, 132))
    F.spr(C, l_worn, 262, 832, t1 + 0.2, te, anchor='tc'); F.spr(C, l_new, 818, 832, t2 + 0.2, te, anchor='tc')
NOI = [
 S.wk_bench(E, L(9), T_10, labs=[('TESTĂM POMPA PE BANC', 'good big', W(9, 'testam') - 0.15), ('CÂT DEBIT MAI DĂ LA PRESIUNE MARE', 'grey', W(9, 'cat') - 0.15)], ov=ov_graph),
 S.wk(E, 'wm', T_10, T_10T, [('DACĂ E UZATĂ, O DESFACEM', 'grey', W(10, 'daca') + 0.1), ('PIESELE ROASE, ÎNLOCUITE CU PIESE NOI', 'good', W(10, 'inlocuim') - 0.1)],
      st='wkdam', seq=[('wk', W(10, 'piese', 2) - 0.2, W(10, 'piese', 2) + 0.4)], ov=ov_parts),
 S.wk_bench(E, T_10T, L(E.OUT), labs=[('TESTATĂ DIN NOU PE BANC', 'good big', W(10, 'testam') - 0.15)],
            rows=[('DEBIT', W(10, 'primesti') - 0.1), ('PRESIUNE', W(10, 'primesti') + 0.3), ('ETANȘEITATE', W(10, 'fisa'))], t_sheet=W(10, 'primesti') - 0.5),
]

SHOTS = S.opening(E, HOOK) + [SIGNS] + WEAR + [FUELS] + BREAK + WINTER + [AVOID] + NOI + [S.ending(E)]
SPR = E.SPR
