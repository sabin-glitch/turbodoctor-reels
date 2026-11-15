/* establishing */
const pv=(a,b)=>U=>pulse(U,a,a+0.4,b-0.4,b);
const dgA=(x,y,z)=>()=>[DGP.x+x,DGP.y+y,z||0];
const vaneAt=(k,z)=>()=>{const g=dgVanes[k];return [DGP.x+g.position.x,DGP.y+g.position.y,z||6];};
/* petrol engine as it leaves the factory: recirculation (diverter) valve, MAF */
addLabel('Motor pe benzină','cu bujie',[EX-6,40,0],1,20,24,pv(T_P+0.6,K.P_DV+0.2),'fire');
addLabel('Turbosuflantă',null,[-20,TY+46,-10],1,24,-26,pv(T_P+0.9,K.P_DV+0.2));
addLabel('Intercooler',null,[-245,196,0],1,30,6,pv(T_P+1.2,K.P_DV+0.2),'air');
addLabel('Clapetă de accelerație',null,[-247,THR_Y,0],1,22,-4,pv(T_P+1.5,K.P_DV+0.2),'air');
addLabel('Supapă de recirculare','diverter valve · din fabrică',[DV_X+14,DV_Y+60,0],1,10,22,pv(K.P_DV+0.3,K.P_LIFT+0.5),'big');
addLabel('Clapetă închisă',null,[-266+12,THR_Y,0],1,24,-12,pv(K.P_C+0.35,K.P_L+0.3),'warn');
addLabel('Aer comprimat','nu mai are unde să se ducă',[-266+10,BOV_Y+16,0],1,22,14,pv(K.P_TRAP,K.P_L+0.3),'warn');
addLabel('Supapa se deschide',null,[DV_X+14,DV_Y+54,0],1,18,-30,pv(K.P_L+0.5,K.P_BACK),'air');
addLabel('Aerul se întoarce','înainte de compresor',[DV_X+8,TY+6,0],1,26,-34,pv(K.P_BACK,K.P_MAF+0.2),'air');
addLabel('Senzor MAF','aici se măsoară aerul',[MAF_X,TY+40,-4],-1,10,-36,pv(K.P_MAF1,K.P_OK+0.6),'big');
addLabel('Aer deja măsurat','rămâne captiv în circuit',[DV_X-24,TY-6,0],1,8,-36,pv(K.P_CAP-0.4,K.P_OK-0.1),'air');
addLabel('Motorul funcționează corect',null,[EX-6,40,0],1,20,24,pv(K.P_OK+0.35,T_B-0.2),'air');
/* tuned petrol engine: blow-off */
addLabel('Supapă blow-off','pe mașinile tunate',[-322,143,-4],-1,10,28,pv(T_B+0.6,K.P2_C-0.5),'big');
addLabel('Turbina se accelerează prea mult',null,[-84,TY+34,6],1,26,-40,pv(K.B_ACC+0.2,K.P2_C+0.2),'warn');
addLabel('Clapetă închisă',null,[-266+12,THR_Y,0],1,24,-12,pv(K.P2_C+0.35,T_D-0.25),'warn');
addLabel('Presiune în plus','motorul nu mai are nevoie de ea',[-266,BOV_Y+30,0],1,22,10,pv(K.P2_NEED-0.5,K.P2_L+0.35),'warn');
addLabel('Aer eliberat în atmosferă','de aici vine sunetul',[-266-BOV_OUT,BOV_Y-60,8],1,22,-6,pv(K.P2_L+0.35,T_D-0.25),'air');
/* diesel: nothing to recirculate, nothing to vent */
addLabel('Motor diesel','cu injector',[EX+10,60,0],1,24,22,pv(T_D+0.6,K.D_LIFT+1.4),'fire');
addLabel('Clapeta rămâne deschisă',null,[-266+12,THR_Y,0],1,24,-12,pv(K.D_LIFT+0.2,K.D_NOBOV-0.2),'air');
addLabel('Aerul trece prin motor',null,[-252,48,0],1,24,-14,pv(K.D_AIR,K.D_NOBOV-0.2),'air');
addLabel('Fără supapă de recirculare',null,[DV_X,DV_Y+4,0],1,16,-46,pv(K.D_NODV,K.D_TURBO-0.3),'big');
addLabel('Fără blow-off','din fabrică',[-279,BOV_Y,0],-1,12,24,pv(K.D_NOBO,K.D_TURBO-0.3),'big');
/* where the sound comes from: overspeed */
addLabel('Turbosuflantă',null,[-20,TY+46,-10],1,24,-26,pv(K.D_TURBO+0.3,K.O_R0+0.6));
addLabel('Turbină supraturată','peste turația maximă',[72,TY+22,8],1,14,46,pv(K.O_R0+0.9,K.L_LIFT+0.2),'warn');
addLabel('Prea mult aer și presiune','mai mult decât cere motorul',[-84,TY+72,-40],-1,26,-10,pv(K.O_AIR,K.L_LIFT+0.2),'warn');
/* lift-off: surge */
addLabel('Injecție tăiată',null,[EX+10,60,0],1,24,22,pv(K.L_LIFT+0.3,K.S_ON-1.6),'warn');
addLabel('Motorul cere mai puțin aer',null,[-252,48,0],1,24,-14,pv(K.L_ENG,K.S_ON-1.6),'air');
addLabel('Compresor supraturat','împinge în continuare',[-86,TY+16,8],-1,32,26,pv(K.L_COMP,K.S_ON-0.3),'warn');
addLabel('Aerul se întoarce','prin roata compresorului',[-150,TY+12,-4],-1,10,26,pv(K.S_ON+0.3,K.X_AX-0.3),'warn');
addLabel('Roata compresorului','tensiune pe palete',[-88,TY-16,8],-1,26,-34,pv(K.X_STR,K.X_AX+1.4),'warn');
addLabel('Lagăr axial','lovit înainte-înapoi',[-52,TY+22,0],-1,14,20,pv(K.X_BRG0-0.2,K.X_PAL+0.2),'warn');
addLabel('Axul capătă joc',null,[-22,TY-6,6],1,20,-30,pv(K.X_JOC,K.X_PAL+0.2),'warn');
addLabel('Paletele ating carcasa',null,[-80,TY-30,0],-1,24,-16,pv(K.X_SPK,T_S-0.3),'warn');
/* closing: why there is too much air on the intake of a diesel */
addLabel('Prea mult aer pe admisie','de ce?',[-84,TY+72,-40],-1,26,-10,pv(K.W_Q,K.W_DG+0.2),'warn');
addLabel('Geometrie variabilă blocată',null,vaneAt(1),1,34,26,pv(K.W_DG+0.9,K.W_OTH+0.2),'warn');
addLabel('Actuator','problemă pe acționare',dgA(172,-112,10),1,6,26,pv(K.W_ACT,K.W_OTH+0.2),'warn');
addLabel('Alte defecte','presiune prea mare pe admisie',[-266+12,150,0],1,24,14,pv(K.W_OTH+0.9,K.W_LIFT+0.1),'warn');
addLabel('Pompaj','aerul se întoarce în pulsuri',[-150,TY+12,-4],-1,10,26,pv(K.W_LIFT+0.7,TU+1),'warn');
let labelsOn=true;
