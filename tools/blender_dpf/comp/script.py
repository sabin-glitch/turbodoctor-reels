"""Training film "Filtrul de particule (DPF)": the narration, line by line (one generated take per line).

`say` = the text sent to the voice (numbers and abbreviations written the way they are spoken);
`txt` = the same line the way it is written in documents.  Chapters: CH[i] = (first line, title).
"""
TAG = '[calm] [matter of fact] '
TAG0 = '[serious] [matter of fact] [conversational tone] '

L = [
    # ---- 0 intro
    ('Filtrul de particule: ce e în el, cum se încarcă, cum se regenerează și de ce dă erori.', None),
    ('Începem cu piesa. Imediat după turbină stă o carcasă de inox, cu senzorii prinși pe ea.', None),
    ('Înăuntru sunt două piese ceramice. Sus, catalizatorul de oxidare, pe scurt docul. Sub el, filtrul de particule.',
     'Înăuntru sunt două piese ceramice. Sus, catalizatorul de oxidare, pe scurt DOC-ul. Sub el, filtrul de particule.'),
    ('Amândouă stau în saltele din fibre, care le țin pe loc și preiau dilatarea.', None),
    # ---- 1 DOC
    ('Docul e un fagure cu canale drepte, deschise la ambele capete, acoperite cu platină și paladiu.',
     'DOC-ul e un fagure cu canale drepte, deschise la ambele capete, acoperite cu platină și paladiu.'),
    ('Are trei roluri. Primul: arde monoxidul de carbon și motorina nearsă din gaze.', None),
    ('Al doilea: transformă o parte din monoxidul de azot în dioxid de azot. Cu el, funinginea din filtru poate arde încet, la temperaturi obișnuite de drum.', None),
    ('Al treilea e cel mai important pentru noi. La regenerare, docul arde motorina trimisă special pe evacuare și încălzește gazele înainte de filtru.',
     'Al treilea e cel mai important pentru noi. La regenerare, DOC-ul arde motorina trimisă special pe evacuare și încălzește gazele înainte de filtru.'),
    ('Dar lucrează doar cald. Sub circa două sute de grade, motorina trece prin el nearsă.',
     'Dar lucrează doar cald. Sub circa 200 °C, motorina trece prin el nearsă.'),
    # ---- 2 filtrarea
    ('Filtrul e din carbură de siliciu. Canalele lui sunt închise alternativ: unul are dop la ieșire, vecinul lui are dop la intrare.', None),
    ('Gazele intră pe un canal și dau de dop. Singura cale e prin peretele poros, în canalul vecin.', None),
    ('Funinginea nu trece prin perete. Rămâne în canalul de intrare și se așază strat peste strat.', None),
    ('Un filtru întreg oprește peste nouăzeci și cinci la sută din particule. De aceea, la un filtru bun, țeava de evacuare e curată pe dinăuntru.',
     'Un filtru întreg oprește peste 95 % din particule. De aceea, la un filtru bun, țeava de evacuare e curată pe dinăuntru.'),
    # ---- 3 încărcarea
    ('Cu cât se adună mai multă funingine, cu atât gazele trec mai greu, iar presiunea dinaintea filtrului crește.', None),
    ('Calculatorul motorului socotește încărcarea pe două căi. Prima e funinginea măsurată: o scoate din presiunea diferențială și din debitul de gaze.', None),
    ('A doua e funinginea calculată. Un model adună cât a produs motorul, după injecție, aer și e-ge-re, și scade cât s-a ars pe drum.',
     'A doua e funinginea calculată. Un model adună cât a produs motorul, după injecție, aer și EGR, și scade cât s-a ars pe drum.'),
    ('Pe tester le vedeți pe amândouă, în grame. La un sistem sănătos, merg aproape una de alta.', None),
    # ---- 4 senzorii
    ('Acum, senzorii. Sonda lambda măsoară oxigenul din gaze. După ea, calculatorul corectează injecția și e-ge-re-ul.',
     'Acum, senzorii. Sonda lambda măsoară oxigenul din gaze. După ea, calculatorul corectează injecția și EGR-ul.'),
    ('Primul senzor de temperatură stă înainte de doc. Arată dacă docul e destul de cald ca să primească motorină.',
     'Primul senzor de temperatură stă înainte de DOC. Arată dacă DOC-ul e destul de cald ca să primească motorină.'),
    ('Al doilea stă între doc și filtru. După el se reglează regenerarea.',
     'Al doilea stă între DOC și filtru. După el se reglează regenerarea.'),
    ('Al treilea, după filtru, arată cum arde funinginea și păzește filtrul de supraîncălzire.', None),
    ('Senzorul de presiune diferențială e legat prin două țevi: una înainte de filtru, una după. Măsoară diferența dintre ele.', None),
    ('La unele modele are o singură țeavă, cea dinainte de filtru, și compară cu presiunea de afară.', None),
    ('Filtru curat înseamnă diferență mică. Filtru plin înseamnă diferență mare și tensiune mai mare spre calculator.', None),
    # ---- 5 regenerarea
    ('Regenerarea pasivă merge singură. Pe drum lung, la trei sute cincizeci până la cinci sute de grade, funinginea arde încet, fără nicio comandă.',
     'Regenerarea pasivă merge singură. Pe drum lung, la 350–500 °C, funinginea arde încet, fără nicio comandă.'),
    ('În oraș, asta nu ajunge. Când încărcarea trece de prag, calculatorul pornește regenerarea activă.', None),
    ('Închide e-ge-re-ul, strânge clapeta de admisie și întârzie injecția principală. Gazele ies din motor mai fierbinți.',
     'Închide EGR-ul, strânge clapeta de admisie și întârzie injecția principală. Gazele ies din motor mai fierbinți.'),
    ('Apoi adaugă post-injecții târzii. Motorina aceea nu mai arde în cilindru. Pleacă pe evacuare și arde în doc.',
     'Apoi adaugă post-injecții târzii. Motorina aceea nu mai arde în cilindru. Pleacă pe evacuare și arde în DOC.'),
    ('Înainte de filtru se ajunge la șase sute, șase sute cincizeci de grade. Funinginea se aprinde și arde în zece, cincisprezece minute.',
     'Înainte de filtru se ajunge la 600–650 °C. Funinginea se aprinde și arde în 10–15 minute.'),
    ('Presiunea diferențială scade, iar calculatorul oprește post-injecția.', None),
    ('Pentru asta îi trebuie condiții: motor cald, drum destul de lung și nicio eroare care blochează regenerarea.', None),
    ('Dacă regenerarea e întreruptă mereu, motorina din post-injecție ajunge în ulei. Nivelul uleiului crește, iar filtrul rămâne plin.', None),
    # ---- 6 cenușa
    ('Ce nu arde niciodată e cenușa. Vine din aditivii uleiului ars în motor și se strânge la capătul canalelor de intrare.', None),
    ('Filtrul rămâne cu tot mai puțin loc. Regenerările se îndesesc, iar la sfârșit filtrul trebuie curățat profesional sau înlocuit.', None),
    ('Un motor care consumă ulei, pe la turbină, pe la semeringurile de supape sau pe la epurator, îl umple de cenușă mult mai repede.', None),
    # ---- 7 erorile de încărcare
    ('Erorile de încărcare. Calculatorul spune: în filtru e mai multă funingine decât am voie. Întrebarea corectă e: de ce?', None),
    ('Prima variantă: regenerarea n-a putut merge. Drumuri scurte, termostat blocat deschis, bujii arse, un senzor de temperatură defect sau un doc obosit, care nu mai încălzește.',
     'Prima variantă: regenerarea n-a putut merge. Drumuri scurte, termostat blocat deschis, bujii arse, un senzor de temperatură defect sau un DOC obosit, care nu mai încălzește.'),
    ('A doua: motorul scoate prea multă funingine. Injectoare care picură, e-ge-re blocat deschis, pierderi de aer pe admisie, turbină care nu mai dă presiune.',
     'A doua: motorul scoate prea multă funingine. Injectoare care picură, EGR blocat deschis, pierderi de aer pe admisie, turbină care nu mai dă presiune.'),
    ('A treia: măsurătoarea minte. Furtunaș înfundat sau fisurat, apă în țevi, senzor decalibrat.', None),
    ('A patra: filtrul e plin de cenușă. Presiunea e mare, dar nu mai are ce să ardă. Regenerează des și degeaba.', None),
    ('Prima verificare: cu contactul pus și motorul oprit, senzorul de presiune trebuie să arate zero.', None),
    ('Apoi comparați valorile. Dacă funinginea măsurată e mult peste cea calculată, bănuiți măsurătoarea, cenușa sau un motor care scoate mai multă funingine decât crede calculatorul.', None),
    ('Dacă amândouă sunt mari și apropiate, filtrul chiar e plin. Regenerările n-au mers și trebuie aflat ce le-a oprit.', None),
    ('Atenție la limite. La doi litri TDI, peste vreo patruzeci de grame, regenerarea se mai face doar în service. Peste patruzeci și cinci, filtrul se înlocuiește: atâta funingine, arsă deodată, îl crapă sau îl topește.',
     'Atenție la limite. La 2.0 TDI, peste vreo 40 g, regenerarea se mai face doar în service. Peste 45 g, filtrul se înlocuiește: atâta funingine, arsă deodată, îl crapă sau îl topește.'),
    # ---- 8 erorile de eficiență
    ('Erorile de eficiență sunt invers. P două mii doi înseamnă: filtrul nu mai reține cât trebuie.',
     'Erorile de eficiență sunt invers. P2002 înseamnă: filtrul nu mai reține cât trebuie.'),
    ('Fără senzor de particule, calculatorul judecă tot după presiune. La un anumit debit de gaze, un filtru întreg trebuie să opună o anumită rezistență.', None),
    ('Dacă presiunea măsurată iese mult sub cea așteptată, mai multe drumuri la rând, concluzia lui e că gazele trec prea ușor.', None),
    ('Cauza poate fi chiar filtrul: crăpat sau topit după o regenerare scăpată de sub control, ori golit.', None),
    ('Dar la fel de des, presiunea e falsă: o scăpare pe evacuare înainte de filtru, furtunașul dinainte de filtru fisurat sau un senzor care arată prea puțin.', None),
    ('Sau debitul e socotit greșit. La motoarele de doi litri Euro șase din grupul VAG, cauza întâlnită cel mai des e răcitorul e-ge-re-ului de joasă presiune, înfundat.',
     'Sau debitul e socotit greșit. La motoarele 2.0 Euro 6 din grupul VAG, cauza întâlnită cel mai des e răcitorul EGR-ului de joasă presiune, înfundat.'),
    ('Prin filtru trece atunci mai puțin gaz decât crede calculatorul. Presiunea iese prea mică, deși filtrul e bun.', None),
    ('La mașinile cu senzor de particule, verdictul vine de la el. Funinginea scăpată se așază între doi electrozi. Dacă se adună prea repede, filtrul nu mai reține.', None),
    ('Proba cea mai simplă: uitați-vă în țeava de evacuare. Curată înseamnă că filtrul reține. Neagră de funingine înseamnă că nu.', None),
    # ---- 9 ordinea de lucru
    ('Ordinea de lucru, pe scurt. Unu: citiți toate erorile, nu doar pe cea a filtrului.', None),
    ('Doi: valorile măsurate. Funinginea măsurată și calculată, cenușa, presiunea diferențială, temperaturile și distanța de la ultima regenerare.', None),
    ('Trei: furtunașele, țevile, senzorul și etanșeitatea evacuării.', None),
    ('Patru: cauza din amonte. Injecția, e-ge-re-ul, turbina și admisia, consumul de ulei, termostatul, bujiile.',
     'Patru: cauza din amonte. Injecția, EGR-ul, turbina și admisia, consumul de ulei, termostatul, bujiile.'),
    ('Abia la urmă, filtrul: regenerare, curățare sau înlocuire, cu adaptările făcute corect.', None),
    ('De cele mai multe ori, filtrul de particule e victima, nu vinovatul. Întâi cauza, apoi filtrul.', None),
]
SAY = [a for a, b in L]
TXT = [b or a for a, b in L]
N = len(L)
CH = [(0, 'CE E ÎN CARCASĂ'), (4, 'ROLUL DOC-ULUI'), (9, 'CUM FILTREAZĂ'), (13, 'CUM SE ÎNCARCĂ'), (17, 'SENZORII'), (24, 'REGENERAREA'),
      (32, 'CENUȘA'), (35, 'ERORILE DE ÎNCĂRCARE'), (44, 'ERORILE DE EFICIENȚĂ'), (53, 'ORDINEA DE LUCRU')]


def prompt(i):
    return (TAG0 if i == 0 else TAG) + SAY[i]


if __name__ == '__main__':
    import json
    tot = sum(len(prompt(i)) for i in range(N)); raw = sum(len(s) for s in SAY)
    print(N, 'lines;', raw, 'chars spoken;', tot, 'with tags; longest', max(len(s) for s in SAY), '; est', round(raw / 15.0 + 0.4 * N), 's')
    for c, (i, t) in enumerate(CH):
        j = CH[c + 1][0] if c + 1 < len(CH) else N
        print(c, t, i, j - 1, sum(len(s) for s in SAY[i:j]))
    json.dump([prompt(i) for i in range(N)], open('/tmp/prompts.json', 'w'), ensure_ascii=False, indent=0)
