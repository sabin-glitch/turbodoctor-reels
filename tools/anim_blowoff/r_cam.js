const SHOTS={
  wide:{c:[-128,40],w:470,h:430,az:14,el:8},
  wide2:{c:[-128,40],w:470,h:430,az:-12,el:10},
  bovT:{c:[-292,108],w:170,h:200,az:10,el:5},
  bov:{c:[-305,116],w:120,h:140,az:8,el:4},
  bovMid:{c:[-230,150],w:330,h:340,az:12,el:6},
  intake:{c:[-215,70],w:300,h:300,az:12,el:6},
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
  vgt:{c:[DGP.x+38,DGP.y-14],w:322,h:330,az:0,el:0},
  vgtIn:{c:[DGP.x+6,DGP.y+4],w:262,h:262,az:0,el:0}
};
const CAMKEYS=[[0,'hookA0'],[K.H_LIFT-0.55,'hookA'],[K.H_LIFT+0.35,'hookB'],[K.H_DMG-0.3,'hookB'],[K.H_DMG+0.9,'chra'],[K.H_SPK-0.2,'chra'],[K.H_SPK+0.8,'wheel'],[T_P,'wheel'],
  [T_P+0.01,'wide'],[K.P_IN,'wide'],[K.P_IN+1.4,'bovMid'],[K.P_C-1.9,'bovMid'],[K.P_C-0.7,'bovT'],[K.P_L-0.6,'bovT'],[K.P_L+0.5,'bov'],[T_D,'bov'],
  [T_D+0.01,'intake'],[K.D_NOBOV-0.7,'intake'],[K.D_NOBOV+0.5,'bovT'],[K.D_ACC+0.2,'bovT'],[K.D_TURBO-0.4,'bovMid'],[K.D_TURBO+0.9,'turboAll'],[K.G_IN+0.5,'turboAll'],[K.G_IN+1.7,'vgt'],
  [K.G_LOW-0.3,'vgt'],[K.G_LOW+1.0,'vgtIn'],[K.C_TRY-0.5,'vgtIn'],[K.C_TRY+0.7,'vgt'],[K.O_0-0.2,'vgt'],[K.O_0+1.0,'vgtIn'],[K.O_OUT,'vgtIn'],[K.O_OUT+1.2,'turboO'],
  [K.L_LIFT-0.6,'turboO'],[K.L_LIFT+0.9,'airPath'],[K.S_ON-1.9,'airPath'],[K.S_ON-0.5,'compIn'],[K.X_AX-0.5,'compIn'],[K.X_AX+0.8,'chra'],[K.X_PAL-0.4,'chra'],[K.X_PAL+0.8,'wheel'],[T_S,'wheel'],
  [T_W,'compIn'],[K.W_DG-0.2,'compIn'],[K.W_DG+1.1,'vgt'],[TU,'vgt']];
/* split screen: top = the blow-off and the compressor, bottom = the compressor inlet in surge (same scale) */
const SPLIT_A={c:[-212,138],w:330,h:150,az:6,el:5},SPLIT_B={c:[-150,172],w:330,h:150,az:-8,el:5};
