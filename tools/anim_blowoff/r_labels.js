/* establishing */
const pv=(a,b)=>U=>pulse(U,a,a+0.4,b-0.4,b);
const dgA=(x,y,z)=>()=>[DGP.x+x,DGP.y+y,z||0];
const vaneAt=(k,z)=>()=>{const g=dgVanes[k];return [DGP.x+g.position.x,DGP.y+g.position.y,z||6];};
/* petrol engine with blow-off */
addLabel('Turbosuflantă',null,[-20,TY+46,-10],1,24,-26,pv(T_P+0.7,K.P_IN+0.6));
addLabel('Intercooler',null,[-245,196,0],1,30,6,pv(T_P+1.0,K.P_IN+0.6),'air');
addLabel('Supapă blow-off',null,[-322,143,-4],-1,10,28,pv(T_P+1.3,K.P_C-0.6),'big');
addLabel('Clapetă de accelerație',null,[-247,THR_Y,0],1,22,-4,pv(T_P+1.6,K.P_C-0.6),'air');
addLabel('Motor pe benzină','cu bujie',[EX-6,40,0],1,20,24,pv(T_P+1.9,K.P_IN+1.2),'fire');
addLabel('Clapetă închisă',null,[-266+12,THR_Y,0],1,24,-12,pv(K.P_C+0.35,T_D-0.25),'warn');
addLabel('Aer blocat','sub presiune',[-266,BOV_Y+30,0],1,22,10,pv(K.P_C+0.7,K.P_L+0.35),'warn');
addLabel('Aer eliberat','pșșșt',[-266-BOV_OUT,BOV_Y-60,8],1,22,-6,pv(K.P_L+0.35,T_D-0.25),'air');
/* diesel: nothing to vent */
addLabel('Motor diesel','cu injector',[EX+10,60,0],1,24,22,pv(T_D+0.6,K.D_LIFT+1.4),'fire');
addLabel('Clapeta rămâne deschisă',null,[-266+12,THR_Y,0],1,24,-12,pv(K.D_LIFT+0.2,K.D_NOBOV-0.3),'air');
addLabel('Aerul trece prin motor',null,[-252,48,0],1,24,-14,pv(K.D_AIR,K.D_NOBOV-0.3),'air');
addLabel('Fără supapă blow-off','din fabrică',[-277,BOV_Y,0],-1,14,20,pv(K.D_NOBOV+0.2,K.D_TURBO-0.2),'big');
/* where the sound comes from */
addLabel('Turbosuflantă',null,[-20,TY+46,-10],1,24,-26,pv(K.D_TURBO+0.2,K.G_IN+0.3));
addLabel('Geometrie variabilă','în carcasa turbinei',[61.5,TY+38,-4],1,20,-26,pv(K.G_IN,K.G_IN+2.3),'fire');
/* how the vanes work */
addLabel('Inel de palete',null,vaneAt(1),1,34,26,pv(K.G_RING,K.G_LOW+0.2));
addLabel('Gaze de evacuare',null,dgA(150,102,3),1,10,30,pv(K.G_RING+0.9,K.G_LOW+0.2),'fire');
addLabel('Roata turbinei',null,dgA(-12,10,8),-1,40,-52,pv(K.G_RING+1.3,K.G_LOW+0.2));
addLabel('Actuator',null,dgA(172,-112,10),1,6,26,pv(K.G_ACT,K.G_LOW+0.2));
addLabel('Turații mici','palete închise · gaze rapide',vaneAt(1),1,34,26,pv(K.G_CLOSE+0.5,K.G_HIGH+0.5),'fire');
addLabel('Turații mari','palete deschise · turația rămâne sub limită',vaneAt(1),1,34,26,pv(K.G_OPEN+0.5,K.C_LOW+0.4),'air');
/* soot blocks them */
addLabel('Calamină','depusă pe palete',vaneAt(5),-1,26,-30,pv(K.C_DEP+0.5,K.O_OUT+0.3),'warn');
addLabel('Palete blocate pe închis',null,vaneAt(1),1,34,26,pv(K.C_STUCK+0.2,K.O_OUT+0.3),'warn');
addLabel('Actuator','nu le mai poate deschide',dgA(172,-112,10),1,6,26,pv(K.C_TRY+0.1,K.O_0+0.6));
addLabel('Roata turbinei','lovită cu viteză prea mare',dgA(-12,10,8),-1,40,-52,pv(K.O_HIT,K.O_OUT+0.3),'warn');
/* overspeed, overboost */
addLabel('Turbină','peste turația maximă',[72,TY+22,8],1,14,46,pv(K.O_OUT+1.1,K.L_LIFT+0.2),'warn');
addLabel('Presiune peste limită',null,[-84,TY+72,-40],-1,26,-10,pv(K.O_PRES,K.L_LIFT+0.2),'warn');
/* lift-off: surge */
addLabel('Injecție tăiată',null,[EX+10,60,0],1,24,22,pv(K.L_LIFT+0.3,K.S_ON-1.6),'warn');
addLabel('Motorul cere mai puțin aer',null,[-252,48,0],1,24,-14,pv(K.L_ENG,K.S_ON-1.6),'air');
addLabel('Compresor supraturat','împinge în continuare',[-86,TY+16,8],-1,32,26,pv(K.L_COMP,K.S_ON-0.3),'warn');
addLabel('Aerul se întoarce','prin roata compresorului',[-150,TY+12,-4],-1,10,26,pv(K.S_ON+0.3,K.X_AX-0.3),'warn');
addLabel('Roata compresorului','tensiune pe palete',[-88,TY-16,8],-1,26,-34,pv(K.X_STR,K.X_AX+1.4),'warn');
addLabel('Lagăr axial','lovit înainte-înapoi',[-52,TY+22,0],-1,14,20,pv(K.X_BRG0-0.2,K.X_PAL+0.2),'warn');
addLabel('Axul capătă joc',null,[-22,TY-6,6],1,20,-30,pv(K.X_JOC,K.X_PAL+0.2),'warn');
addLabel('Paletele ating carcasa',null,[-80,TY-30,0],-1,24,-16,pv(K.X_SPK,T_S-0.3),'warn');
/* closing */
addLabel('Pompaj','aerul se întoarce în pulsuri',[-150,TY+12,-4],-1,10,26,pv(K.W_LIFT+0.6,K.W_DG+0.1),'warn');
addLabel('Geometrie variabilă','palete blocate de calamină',vaneAt(1),1,34,26,pv(K.W_DG+0.9,TU+1),'warn');
addLabel('Actuator',null,dgA(172,-112,10),1,6,26,pv(K.W_DG+1.3,TU+1));
let labelsOn=true;
