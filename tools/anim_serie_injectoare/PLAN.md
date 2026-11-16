# Seria injectoare: episoadele 1 și 2 (lucru, 15–16.11.2026)

Vocea gata: ep1/vo (story_end 92.2, total 99.7), ep2/vo (story_end 88.13, total 95.63; rândul 2 forțat pe varianta b).

## Unelte (în /home/claude/w/serinj)
- ishots.py: camerele și stările plăcilor (comun Blender + montaj)
- iplate.py: randează o placă (beauty PNG + .z.npy + .json camera) cu venv_bpy; `--preview` = 270x480, 8 spp
- micro.py: scena micro (joc ac/ghidaj + fir de păr), ballseat.py: bila pe scaun (adâncituri, canal), tank.py: rezervoare (ep2)
- sprites.js: etichete / insignă / fundal / marcaj ca PNG (Playwright, CSS-ul seriei turbine)
- icomp.py: montajul cadrelor (fundal + marcaj + plăci + particule + etichete) -> frames_base
- ep1_story.py / ep2_story.py: planurile pe voce

## Ep1 (particulele) – planuri
hook 0.25–8.0 injector întreg -> scanare -> secțiune, particule negre în canal | L1 secțiune, apropiere
L2 sursa Bosch, eticheta MOTORINĂ MURDARĂ | L3 micro: joc 1–4 µm vs fir de păr 50–70 µm | L4 particule mici intră, cele mari nu
L5 supapa: închisă/deschisă, apoi vârful: acul deschide / închide | L6 bila pe scaun: adâncituri -> canal
L7 scăpare spre retur + curba injecției (mai mult, mai târziu) | L8 duza erodată, jet stricat | L9 camera de ardere + simptome
L10 filtrul (prinde particulele) | L11–13 injectorul întreg, curat

## Ep2 (apa) – planuri
hook ca la ep1 cu picături albastre | L2 Bosch nr. 2 | L3 rugina pe ac | L4 micro: rugina macină / umple jocul -> blocat
L5 apa nu unge (film de motorină vs apă, contact metal pe metal) | L6 surse: rezervor cu condens, benzinărie, filtru nescurs
L7 filtrul: apa se adună în pahar, apoi trece mai departe | L8 camera de ardere + simptome | L9 golirea apei, martorul de apă
