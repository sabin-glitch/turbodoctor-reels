"""Hook-ul reel-ului piezo vs magnetic: pistonul urcă, injectorul injectează (animația din tools/anim_injectie),
apoi trecere prin negru spre comparație. Construiește hook/reel.html; cadrele 0..HK se randează cu hook/render_frames.js."""
import json, os, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); INJ = os.path.join(HERE, '..', 'anim_injectie'); H = os.path.join(HERE, 'hook')
os.makedirs(os.path.join(H, 'vo'), exist_ok=True)
cues = json.load(open(os.path.join(HERE, 'vo', 'cues.json'), encoding='utf-8'))
HK = cues['lines'][2]['start'] - 0.35                      # același moment ca în reel_tail.js / reel.js
L = [{'start': cues['lines'][0]['start'], 'end': 3.2}, {'start': cues['lines'][1]['start'], 'end': HK}, {'start': HK + 0.45, 'end': HK + 3}]
L += [{'start': 20 + 6 * i, 'end': 25 + 6 * i} for i in range(3, 24)]   # restul replicilor animației de injecție nu se folosesc
json.dump({'end': 200, 'lines': L, 'words': []}, open(os.path.join(H, 'vo', 'cues.json'), 'w'))
t = open(os.path.join(INJ, 'reel_tail.js'), encoding='utf-8').read()
def rep(a, b):
    global t
    i = t.index(a); j = t.index(b, i); return i, j
i, j = rep("  {t0:0,t1:fr(0,HK,.05)", "  {t0:HK,t1:W(3,'injectorul')")
t = t[:i] + """  {t0:0,t1:fr(0,HK,.30),u0:2.3,u1:6.6},{t0:fr(0,HK,.30),t1:fr(0,HK,.40),u0:6.6,u1:7.6},{t0:fr(0,HK,.40),t1:fr(0,HK,.45),u0:7.6,u1:8.55},
  {t0:fr(0,HK,.45),t1:fr(0,HK,.79),u0:8.55,u1:10.9},{t0:fr(0,HK,.79),t1:HK,u0:10.9,u1:13.5},
""" + t[j:]
i, j = rep("  [0,'noz'],[fr(0,HK,.58)", "  [HK,'wide']")
t = t[:i] + "  [0,'hkA'],[fr(0,HK,.20),'hkA'],[fr(0,HK,.42),'hkB'],[fr(0,HK,.74),'hkB'],[fr(0,HK,.95),'hkC'],[HK-.001,'hkC'],\n" + t[j:]
a = "const SHOTS={\n"; assert t.count(a) == 1
t = t.replace(a, a + "  hkA:{c:[3,-22],w:150,h:205,az:26,el:9,pb:470},hkB:{c:[2,8],w:104,h:124,az:12,el:11,pb:470},hkC:{c:[3,-24],w:150,h:175,az:20,el:10,pb:470},\n")
a = "top:[[0,720],[HK-.3,720],"; assert t.count(a) == 1
t = t.replace(a, "top:[[0,610],[HK-.3,610],")
open(os.path.join(H, 'reel_tail.js'), 'w', encoding='utf-8').write(t)
for n, src in (('three.min.js', os.path.join(HERE, 'three.min.js')), ('fonts', os.path.join(HERE, '..', '..', 'assets', 'fonts'))):
    p = os.path.join(H, n)
    if not os.path.lexists(p): os.symlink(os.path.relpath(src, H), p)
shutil.copy(os.path.join(HERE, 'render_frames.js'), os.path.join(H, 'render_frames.js'))
subprocess.check_call([sys.executable, os.path.join(INJ, 'build_reel.py')], cwd=H)
p = os.path.join(H, 'reel.html'); h = open(p, encoding='utf-8').read(); a = '<div id="dip"></div>'; assert h.count(a) == 1
h = h.replace(a, '<div style="position:absolute;left:0;top:0;width:1080px;height:660px;background:linear-gradient(#0b1016 0,rgba(11,16,22,.96) 70%,rgba(11,16,22,0))"></div><div style="position:absolute;left:0;top:1440px;width:1080px;height:480px;background:linear-gradient(rgba(11,16,22,0),#0b1016 30%)"></div>' + a)
open(p, 'w', encoding='utf-8').write(h)
print('HK', round(HK, 3), 'cadre 0..%d' % int(HK * 30))
