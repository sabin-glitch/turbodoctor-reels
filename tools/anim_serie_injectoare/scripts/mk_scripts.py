# Textele episoadelor 3-13 -> epN/vo_script.json (rândul 0 = „Seria...” refolosit din ep1, rândul 2 = „Vezi toate cauzele...”, ultimele 3 = finalul comun)
import json, os
HERE = '/home/claude/w/serinj'
HOOK = '[serious] [matter of fact] [conversational tone]'
INTRO = 'Seria „De ce se strică injectoarele”.'
VEZI = 'Vezi toate cauzele pe TikTok, Facebook și YouTube-ul nostru.'
END = ['La Turbo Doctor suntem experți în aceste probleme.',
       'Acum că știi cum poți evita această problemă, ar trebui să ajungi cât mai târziu la noi.',
       'Iar dacă ai nevoie de noi, la noi diagnoza este gratuită.']
NUM = {3: 'trei', 4: 'patru', 5: 'cinci', 6: 'șase', 7: 'șapte', 8: 'opt', 9: 'nouă', 10: 'zece', 11: 'unsprezece', 12: 'douăsprezece', 13: 'treisprezece'}
EP = {
 3: ('depunerile din interior', [
   'În interior, pe ac și pe pistonul de comandă, se depune în timp o peliculă subțire, ca un lac.',
   'Apare când urme de sodiu din motorină reacționează cu unii aditivi. În teste, au fost de ajuns câteva părți la un milion.',
   'Jocurile sunt de câțiva microni, iar forțele care mișcă piesele sunt mici, așa că pelicula le frânează.',
   'Acul răspunde mai târziu decât comanda, sau rămâne lipit.',
   'La mașină: pornire grea sau imposibilă la rece, mers neregulat și pierdere de putere.',
   'Un semn tipic: testele electrice ies bune, dar injectorul tot nu lucrează cum trebuie.',
   'Cum eviți? Motorină cu aditivi detergenți, de la benzinării serioase. Aditivii buni previn depunerile și le pot chiar curăța.']),
 4: ('calamina din găurile duzei', [
   'Găurile duzei au în jur de o zecime de milimetru.',
   'Motorina rămasă în vârful fierbinte se descompune și lasă calamină în găuri și în jurul lor.',
   'Peste aproximativ {300|trei sute} de grade la vârful duzei, depunerile cresc mult mai repede.',
   'Iar după oprire, căldura rămasă coace motorina din injector.',
   'Puterea o fură depunerea din interiorul găurii, nu crusta de afară. Jetul se strică.',
   'La mașină: fum, putere mai mică, consum mai mare și probleme repetate cu filtrul de particule.',
   'Cum eviți? Motorină cu aditivi detergenți. În teste, detergenții au recuperat peste trei sferturi din puterea pierdută, cam într-un plin.']),
 5: ('șaiba de etanșare', [
   'Între injector și chiulasă stă o șaibă de cupru, care ține gazele de ardere în cilindru.',
   'Dacă lipsește, e refolosită sau nepotrivită, ori clema e strânsă greșit, gazele scapă pe lângă injector.',
   'La fiecare ardere urcă în puțul injectorului și lasă o calamină foarte tare. Mercedes-Benz îi spune „moartea neagră”.',
   'Injectorul se blochează în chiulasă, iar motorul merge prost.',
   'La mașină: funingine în jurul injectorului, mers neregulat, iar la demontare injectorul nu mai iese.',
   'Cum eviți? La orice demontare: șaibă nouă, scaunul curățat și strângere cu cuplul și unghiul din fabrică.']),
 6: ('murdăria și greșelile de la montaj', [
   'Denso avertizează: murdăria intrată în sistem la montaj poate distruge injectorul imediat.',
   'De aceea, racordurile deschise se acoperă cu capace, iar locul de muncă trebuie să fie curat.',
   'Țevile de înaltă presiune nu se refolosesc: conul se deformează la strângere și se pot desprinde așchii.',
   'Contează și cuplurile de strângere, returul liber și aerisirea: aerul lăsat după reparație împiedică ungerea.',
   'Bosch pune montajul greșit printre cele trei cauze cheie ale defectării injectoarelor.',
   'Cum eviți? Injectoarele se montează în service, cu curățenie de laborator, țevi noi și cupluri după fabricant.']),
 7: ('benzina pusă din greșeală', [
   'Benzina spală pelicula de ungere din pompa de înaltă presiune.',
   'Pompa ajunge să meargă metal pe metal și trimite pilitură în tot sistemul, până în injectoare.',
   'Dacă motorul a mers, reparația poate cuprinde pompa, injectoarele, rampa, țevile, filtrul și rezervorul.',
   'ADAC avertizează că pot face rău și cantitățile mici de benzină.',
   'Ce faci? Nu pui contactul și nu pornești motorul. Chemi tractarea, iar rezervorul se golește.',
   'Iar iarna, nu amesteca motorina cu benzină.']),
 8: ('AdBlue în rezervorul de motorină', [
   'AdBlue e uree dizolvată în apă: {32,5|treizeci și doi virgulă cinci} la sută uree, restul apă.',
   'Ajuns în sistemul de motorină, corodează piesele și lasă cristale albe.',
   'Cristalele și coroziunea ajung în pompă și în injectoare, unde jocurile sunt de câțiva microni.',
   'Dacă motorul a fost pornit, General Motors cere înlocuirea întregului sistem de alimentare.',
   'Ce faci? Nu pui contactul. Rezervorul se golește și se spală.']),
 9: ('motorina care nu unge', [
   'Motorina e singurul lubrifiant al pompei de înaltă presiune și al injectoarelor.',
   'Producătorii de echipamente de injecție cer o motorină care unge suficient și cel mult {7|șapte} la sută biodiesel.',
   'Biodieselul vechi sau prost face acizi și depuneri: filtrele se înfundă și piesele se lipesc.',
   'Uleiul de încălzire nu unge destul, iar uleiul vegetal e prea vâscos și lasă depuneri.',
   'Și când rămâi fără motorină, aerul intrat în sistem împiedică ungerea.',
   'Fără pelicula de motorină, piesele freacă metal pe metal, duzele se lipesc și supapele cedează.',
   'Cum eviți? Motorină standard de la benzinării serioase, fără amestecuri, și nu mergi până la ultima picătură.']),
 10: ('pilitura de la pompă', [
   'Când pompa de înaltă presiune se macină, pilitura pleacă prin rampă în toate injectoarele.',
   'Se depune mai ales la supapa de comandă, în zona bilei.',
   'Buletinele constructorilor spun la fel: dacă găsești metal în pompă, se schimbă pompa, rampa, toate injectoarele, țevile și filtrul.',
   'Rezervorul și conductele se golesc și se spală, iar niciun buletin nu permite curățarea și refolosirea injectoarelor.',
   'Pe scurt: pompa schimbată singură înseamnă injectoare noi, distruse de pilitura rămasă.']),
 11: ('injectorul fără cod și recondiționarea fără standard', [
   'Fiecare injector are un cod de corecție, scris pe corp, care se introduce în calculator la montaj.',
   'Fără el, calculatorul nu știe cât dă acel injector, iar motorul merge prost.',
   'Al doilea risc e recondiționarea fără stand de testare și fără piese bune.',
   'Bosch a testat injectoare recondiționate în afara rețelei autorizate: în {2013|două mii treisprezece}, {70|șaptezeci} la sută au picat testele.',
   'Cum eviți? Injector testat pe stand, cu piese bune, și codat în calculator la montaj.']),
 12: ('defectele electrice', [
   'La injectorul electromagnetic, o bobină ridică ancora și deschide supapa de comandă.',
   'Bobina se poate întrerupe, poate face scurtcircuit sau își poate pierde izolația față de corp.',
   'La injectorul piezo, teancul de sute de straturi ceramice poate face scurtcircuit sau își pierde capacitatea. Și nu se schimbă separat.',
   'Defectele electrice sunt rare față de cele hidraulice, iar uneori vina e la mufă sau la cablaj.',
   'Cum eviți? Înainte să schimbi injectoare, verifică mufele și cablajul.']),
 13: ('uzura normală', [
   'Bosch proiectează sistemul de injecție pentru {300.000|trei sute de mii} de kilometri la autoturisme.',
   'Delphi dă o durată medie în service de {130|o sută treizeci} până la {160.000|o sută șaizeci de mii} de kilometri.',
   'Cu timpul apare cavitația la scaunul supapei și la duză, iar arcurile slăbesc.',
   'Returul crește, iar preinjecțiile se pierd.',
   'La mașină: pornire grea, ralanti neregulat și fum. Iar o duză care curge poate topi pistonul.',
   'Cum eviți? La kilometraj mare, test de retur și verificare pe stand, înainte să cedeze un injector.']),
}
tot = {}
for n, (name, body) in EP.items():
    rows = [dict(text=INTRO, gap=0.25, id='intro'),
            dict(text='Astăzi prezentăm cauza {%d|%s} din {13|treisprezece}: %s.' % (n, NUM[n], name), gap=0.3, tags=HOOK, id='i%dh' % n),
            dict(text=VEZI, gap=0.35, id='s1')]
    for k, b in enumerate(body): rows.append(dict(text=b, gap=0.6 if k == 0 else 0.45, id='i%db%d' % (n, k)))
    rows += [dict(text=END[0], gap=0.8, id='o1'), dict(text=END[1], gap=0.4, id='o2'), dict(text=END[2], gap=0.4, id='o3')]
    d = os.path.join(HERE, 'ep%d' % n); os.makedirs(d, exist_ok=True)
    json.dump(rows, open(os.path.join(d, 'vo_script.json'), 'w'), ensure_ascii=False, indent=1)
    import re
    def spoken(t): return re.sub(r'\{([^|}]*)\|([^}]*)\}', r'\2', t)
    gen = [rows[1]] + rows[3:-3]
    chars = sum(len(spoken(r['text'])) + len(r.get('tags', '[calm] [matter of fact]')) + 1 for r in gen)
    tot[n] = (len(gen), chars)
    print(n, len(gen), 'randuri noi', chars, 'caractere')
c = 0
for n in sorted(tot):
    c += tot[n][1]; print('pana la ep%d: %d' % (n, c))
