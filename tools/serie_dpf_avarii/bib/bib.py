# -*- coding: utf-8 -*-
"""Textele din Biblioteca aplicației consilierilor pentru seria „De ce intră filtrul de particule în avarie”.
python3 bib.py N   -> pornește publica-biblioteca pentru episodul N (linkul video din push.log)."""
import sys, re, subprocess
S = 'De ce intră filtrul de particule în avarie: '
B = {
    1: ('filtrul nu se strică singur', 'Filtru de particule (DPF) în avarie, martor aprins. Cum lucrează filtrul și catalizatorul de oxidare, ce vede calculatorul (presiune diferențială, temperaturi), cele patru feluri de avarie: încărcare, regenerare, senzor, eficiență.',
        'Codul de eroare spune ce a observat calculatorul, nu ce piesă e stricată. De cele mai multe ori, cauza e în altă parte a mașinii. De aceea căutăm cauza, nu schimbăm filtrul după cod.'),
    2: ('avaria de încărcare', 'Eroare „filtru de particule plin”, încărcare cu funingine. Funingine calculată și măsurată, pragurile de regenerare (exemplu 2.0 TDI), regenerarea din service, regenerarea forțată.',
        'Filtrul plin este un rezultat: ori regenerarea n-a avut condiții, ori motorul face prea multă funingine, ori senzorul minte. Regenerarea forțată golește filtrul, dar cauza rămâne pe mașină.'),
    3: ('avaria de eficiență', 'Eroare de eficiență la filtrul de particule (P2002). Senzor de particule, presiune diferențială prea mică, filtru fisurat sau topit, filtru de schimb fără metale prețioase, filtru golit, senzor de presiune, EGR și răcitor EGR.',
        'Nu schimbăm filtrul după cod. Întâi aflăm cine are dreptate: filtrul sau măsurătoarea.'),
    4: ('regenerarea întreruptă', 'Drumuri scurte, mers prin oraș, regenerare întreruptă, autostradă la turație mică, rezerva de combustibil. Motorină în ulei, nivelul uleiului crește, martorul filtrului de particule.',
        'Din când în când, un drum întins la turație medie, până se stinge martorul. Dacă martorul rămâne aprins sau clipește, veniți la diagnoză: verificăm încărcarea, uleiul și dacă regenerarea mai poate porni.'),
    5: ('motorul rece', 'Termostat blocat deschis, motorul nu ajunge la temperatură, regenerarea nu pornește. Bujii incandescente și modulul lor. Filtru de particule care se umple deși motorul pare să meargă bine.',
        'La un filtru plin măsurăm temperatura reală a motorului și verificăm termostatul, bujiile și modulul lor. Altfel, filtrul curățat se umple repede la loc.'),
    6: ('erorile care blochează regenerarea', 'Eroare la EGR, clapeta de admisie, senzor de temperatură, debitmetru, presiune diferențială, presiune de supraalimentare, comanda turbinei. Calculatorul nu mai pornește regenerarea. Actualizare de soft.',
        'Eroarea de filtru este a doua, nu prima. Citim toate erorile, reparăm prima cauză și abia apoi curățăm filtrul.'),
    7: ('regenerarea rece', 'Regenerarea pornește, dar temperatura nu urcă. Catalizator de oxidare (DOC) înfundat pe față sau otrăvit cu ulei ori lichid de răcire, vaporizator sau injector pe evacuare înfundat, sistem cu aditiv.',
        'Comparăm temperaturile dinainte și de după catalizator în timpul regenerării. Dacă nu urcă, problema e în fața filtrului, nu în filtru.'),
    8: ('lipsa de aer', 'Furtun de intercooler crăpat, scăpări de aer pe admisie, filtru de aer înfundat, debitmetru murdar, turbină cu geometria blocată, EGR rămas deschis. Funingine multă, regenerări tot mai dese.',
        'La un filtru plin verificăm tot traseul de aer, cu fum sub presiune, și valorile debitmetrului.'),
    9: ('motorina arsă prost', 'Injectoare uzate sau care curg, motorină nearsă pe evacuare, filtru topit. Compresie mică, supape nereglate, motorină cu apă sau contaminată, modificări ale mașinii.',
        'La un filtru care se umple repede, injectoarele merg pe stand, iar motorul primește o probă de compresie înainte să dăm vina pe filtru.'),
    10: ('senzorul de presiune diferențială', 'Senzor de presiune diferențială, țevi înfundate cu funingine sau înghețate, furtunașe crăpate, scăpare pe evacuare înainte de filtru, cablaj rupt. Filtrul pare plin când e curat sau curat când e plin.',
         'Verificăm senzorul, suflăm țevile și căutăm scăpările înainte să spunem că filtrul e plin.'),
    11: ('senzorii de temperatură și de particule', 'Senzori de temperatură a gazelor de evacuare, fir rupt (−40 °C pe tester), regenerări prea scurte sau prea lungi, regenerare blocată. Senzorul de particule de după filtru.',
         'Comparăm senzorii între ei, cu motorul rece: trebuie să arate aproape la fel. Un senzor nu se schimbă pe ghicite. Și nici filtrul.'),
    12: ('cenușa și uleiul nepotrivit', 'Cenușă în filtrul de particule, ulei nepotrivit (fără specificația cu cenușă puțină), presiunea nu mai scade după regenerare, regenerări tot mai dese.',
         'Cenușa nu iese cu nicio regenerare. Iese doar cu filtrul demontat: asta e curățarea pe care o facem noi. Apoi verificăm ce ulei e în motor și cât ulei consumă.'),
    13: ('uleiul și lichidul de răcire', 'Motor care consumă ulei (semeringuri de supape, segmenți, epurator), turbină care scapă ulei pe evacuare, filtru îmbibat cu ulei. Lichid de răcire de la răcitorul EGR sau de la garnitura de chiulasă.',
         'Întrebăm mereu: consumă ulei? scade lichidul de răcire? Și verificăm turbina, epuratorul și răcitorul EGR înainte să montăm filtrul curat.'),
    14: ('regenerarea necontrolată', 'Filtru de particule fisurat sau topit după o regenerare pe filtru prea plin, motor căzut la ralanti în timpul regenerării, filtru îmbibat cu ulei sau motorină. Cordierită și carbură de siliciu.',
         'Un asemenea filtru nu mai poate fi salvat prin curățare. Îl recondiționăm: monolit nou, din carbură de siliciu, în carcasa originală. Și căutăm de ce s-a supraîncărcat.'),
    15: ('reparația făcută pe jumătate', 'Filtru nou și martorul aprins din nou: cauza nereparată, filtru de schimb fără destule metale prețioase, filtru golit (fără viză ITP), adaptări nefăcute, regenerare forțată pe filtru prea plin, aditivi în exces.',
         'Ordinea corectă: cauza, filtrul, apoi adaptările și proba de drum.'),
    16: ('ce facem noi la Turbo Doctor', 'Ce facem la Turbo Doctor cu un filtru de particule: diagnoză, verificare cu camera endoscopică, curățare sau recondiționare (monolit nou din carbură de siliciu) și căutarea cauzei pe mașină: aer, EGR, injectoare, turbină, ulei, senzori, termostat, bujii.',
         'Filtrul de particule este o piesă statică: altceva îl face să intre în avarie. Curățăm sau recondiționăm filtrul și căutăm cauza care l-a înfundat. Doar așa nu mai intră în eroare.'),
}
if __name__ == '__main__':
    n = int(sys.argv[1]); nume, sub, con = B[n]
    url = [re.search(r'(https://raw\S+)', l).group(1) for l in open('/home/claude/work/serie_dpf/bib/push.log') if l.startswith(f'#{n:02d} push_ok=1 HTTP 200')][0]
    r = subprocess.run(['gh', 'api', 'repos/sabin-glitch/turbodoctor-reels/actions/workflows/publica-biblioteca.yml/dispatches', '-f', 'ref=main', '-f', f'inputs[video_url]={url}',
                        '-f', f'inputs[titlu]={S}{nume}', '-f', f'inputs[subiect]={sub}', '-f', f'inputs[concluzie]={con}'] + (['-F', 'inputs[dry_run]=true'] if '--dry' in sys.argv else []), capture_output=True, text=True)
    print(n, r.returncode, r.stderr[:200], url)
