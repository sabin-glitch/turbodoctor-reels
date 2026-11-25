# -*- coding: utf-8 -*-
"""Seria „De ce intră filtrul de particule în avarie” (24.11.2026): textele celor 16 episoade.
EP = lista episoadelor: n, nume (din formulă), titlu (al filmului), rows = (text rostit, imagine, pe ecran, sursa).
"@F" = formula de început, "@FF" = formula episodului final; C1, C2 = cele două rânduri de final, puse de statx.rows_full."""
N = 16
SERIA = "De ce intră filtrul de particule în avarie"
def formula(n, nume):
    return f"Seria „{SERIA}”. Episodul {n} din {N}: {nume}."
FF = f"Seria „{SERIA}”. Episodul final: ce facem noi la Turbo Doctor."
C1 = "Filtrul de particule este o piesă statică: altceva îl face să intre în avarie."
C2 = "La Turbo Doctor curățăm sau recondiționăm filtrul și căutăm cauza care l-a înfundat. Doar așa nu mai intră în eroare."
from ep_a import A
from ep_b import B
from ep_c import C
EP = A + B + C
