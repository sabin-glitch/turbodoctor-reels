const SHOTS={
  wide:{c:[-128,40],w:470,h:430,az:14,el:8},
  wide2:{c:[-128,40],w:470,h:430,az:-12,el:10},
  /* petrol with the recirculation valve */
  dvLoop:{c:[-160,228],w:220,h:200,az:6,el:6},
  dvWide:{c:[-196,186],w:310,h:300,az:10,el:6},
  dvMaf:{c:[-176,222],w:204,h:186,az:-8,el:6},
  /* petrol with the blow-off */
  bovT:{c:[-292,108],w:170,h:200,az:10,el:5},
  bov:{c:[-305,116],w:120,h:140,az:8,el:4},
  bovMid:{c:[-230,150],w:330,h:340,az:12,el:6},
  p2T:{c:[-176,196],w:330,h:300,az:2,el:6},
  /* diesel */
  intake:{c:[-215,70],w:300,h:300,az:12,el:6},
  noV:{c:[-205,178],w:330,h:320,az:8,el:6},
  comp:{c:[-120,TY+20],w:220,h:230,az:-28,el:9},
  compIn:{c:[-140,TY+4],w:200,h:170,az:-22,el:8},
  hookA0:{c:[-66,TY-6],w:350,h:250,az:-2,el:11},
  hookA:{c:[-78,TY+4],w:300,h:210,az:-10,el:9},
  hookB:{c:[-132,TY+2],w:210,h:170,az:-24,el:8},
  wheel:{c:[-84,TY-2],w:124,h:112,az:-14,el:5},
  cyl:{c:[EX+4,-6],w:180,h:215,az:14,el:5},
  turboAll:{c:[-50,TY+10],w:330,h:260,az:16,el:7},
  turboO:{c:[-24,TY+8],w:352,h:250,az:14,el:7},
  airPath:{c:[-185,100],w:340,h:330,az:10,el:6},
  chra:{c:[-60,TY+6],w:150,h:130,az:10,el:4},
  vgt:{c:[DGP.x+38,DGP.y-14],w:322,h:330,az:0,el:0}
};
const CAMKEYS=[[0,'hookA0'],[K.H_LIFT-0.55,'hookA'],[K.H_LIFT+0.35,'hookB'],[K.H_DMG-0.3,'hookB'],[K.H_DMG+0.9,'chra'],[K.H_SPK-0.2,'chra'],[K.H_SPK+0.8,'wheel'],[T_P,'wheel'],
  /* petrol, from the factory: recirculation valve + MAF */
  [T_P+0.01,'wide'],[K.P_IN+0.4,'wide'],[K.P_DV+0.9,'dvLoop'],[K.P_LIFT-0.2,'dvLoop'],[K.P_LIFT+1.1,'dvWide'],[K.P_L-0.5,'dvWide'],[K.P_L+0.9,'dvLoop'],
  [K.P_MAF-0.1,'dvLoop'],[K.P_MAF+1.2,'dvMaf'],[K.P_OK-0.3,'dvMaf'],[K.P_OK+1.0,'dvWide'],[T_B,'dvWide'],
  /* tuned petrol: blow-off */
  [T_B+0.01,'bovMid'],[K.B_PROT-0.3,'bovMid'],[K.B_PROT+1.0,'p2T'],[K.P2_C-0.7,'p2T'],[K.P2_C+0.5,'bovT'],[K.P2_L-0.6,'bovT'],[K.P2_L+0.5,'bov'],[T_D,'bov'],
  /* diesel */
  [T_D+0.01,'intake'],[K.D_NOBOV-0.4,'intake'],[K.D_NOBOV+0.9,'noV'],[K.D_TURBO-0.5,'noV'],[K.D_TURBO+0.8,'turboAll'],[K.O_PRES-0.6,'turboAll'],[K.O_PRES+0.8,'turboO'],
  [K.L_LIFT-0.6,'turboO'],[K.L_LIFT+0.9,'airPath'],[K.S_ON-1.9,'airPath'],[K.S_ON-0.5,'compIn'],[K.X_AX-0.5,'compIn'],[K.X_AX+0.8,'chra'],[K.X_PAL-0.4,'chra'],[K.X_PAL+0.8,'wheel'],[T_S,'wheel'],
  /* closing: the causes, then the surge once more */
  [T_W,'turboO'],[K.W_DG-0.2,'turboO'],[K.W_DG+1.0,'vgt'],[K.W_OTH-0.1,'vgt'],[K.W_OTH+1.1,'airPath'],[K.W_LIFT-0.5,'airPath'],[K.W_LIFT+0.8,'compIn'],[K.W_FIND+0.3,'compIn'],[K.W_FIND+1.8,'hookA'],[TU,'hookA']];
/* split screen: top = the blow-off and the compressor, bottom = the compressor inlet in surge (same scale) */
const SPLIT_A={c:[-212,138],w:330,h:150,az:6,el:5},SPLIT_B={c:[-150,172],w:330,h:150,az:-8,el:5};
