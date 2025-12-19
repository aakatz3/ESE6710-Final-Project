
.lib OptiMOS_OptiMOS5_60V_LTSpice.lib
.lib SN74LVC1G34.cir
.lib LM5114A_TRANS.lib

.param FS      = 6.78e6
.param DUTY    = 0.5
.param VI      = 12
.param RL      = 5

.param QL      = 5
.param Ls = 582n;QL*RL/(2*pi*FS);5.868545099258678e-07;QL*RL/(2*pi*FS)
.param LCHOKE  = 18.65u;1.173709019851736e-05;20*Ls
.param Cs = 1.24n;1/(2*pi*FS*RL*(QL-1.1525));1.220230300040791e-09;1/(2*pi*FS*RL*(QL-1.1525))
.param Cp_ideal = 1/(34.22*RL*FS);8.620258642240302e-10;1/(34.22*RL*FS)
.param C_oss=400p;650p;850p;390p;200p;650p
.param Cp_ext  = Cp_ideal-C_oss;2.120258642240302e-10;Cp_ideal-C_oss

.param NCYCLES = 150
.param SHCYCLES= 3
.param PPS     = 2000
.param TPER    = 1/FS
.param TSTOP   = NCYCLES*TPER
.param TMEAS   = (NCYCLES-SHCYCLES)*TPER
.param TSTEP   = TPER/PPS

.options method=Gear abstol=1n vntol=1e-3 reltol=0.001  solver=alt
.options nomarch maxord=1
.OPTIONS measdgt=99
.OPTIONS numdgt=99
.OPTIONS gmin=1e-15
.tran 0 {TSTOP} {TMEAS} {TSTEP} uic
.OPTIONS itl1=100000
.OPTIONS itl2=100000
.OPTIONS itl4=100000
;.op

V1 NVIN 0 {VI}
LCH NVIN NSW {LCHOKE} Rser=0.3
XQ1 NSW NG 0 BSC065N06LS5_L1
Cp NSW 0 {Cp_ext}
Lser N_SER N_LOAD {Ls} Rser=0.03
Cser NSW N_SER {Cs}
Rload N_LOAD 0 {RL}

;.step lin param C_oss 20p 1100p 10p
;.step lin param C_oss 50p 850p 10p
;.step param QL list 6 15 20 25

*DRIVE
.param VDRV   = 5
.param TRISE  = 8.4n ; From Keysight 35521A Datasheet
.param TFALL  = 8.4n
.param TON    = DUTY*TPER

;V2 VCC 0 {VDRV}
Vg NG 0 PULSE(0 {VDRV} 0 {TRISE} {TFALL} {TON} {TPER})
;XU1 INA CRTL VCC 0 SN74LVC1G34
;XU2 INA 0 VCC NGP NGN 0 LM5114A
;RGP NGP NG 1e-3
;RGN NGN NG 1.5

.SUBCKT SWMOS D S G

S1 D S G 0 SWMOD
Dbody S D DBD

.MODEL SWMOD SW( RON=10m ROFF=10Meg VT=5 VH=0 )
.MODEL DBD   D ( RS=10m VFWD=0.7 )

.ENDS SWMOS
.meas M_LCHOKE param  {LCHOKE}
.meas M_LS param  {LS}
.meas M_CEXT param  {CP_EXT}
.meas M_CIDEAL param  {CP_IDEAL}
.meas M_Cs param  {Cs}
.meas POUT AVG I(Rload)* V(n_load)
.MEAS IOUT_RMS RMS I(Rload)
.meas V_DS_MAX max(V(nsw))
.meas V_DS_ON FIND V(nsw) AT 170n
.meas Q_L param QL
;.meas TRAN m_cds PARAM {xq1:x1:cds2 + xq1:x1:cds3 + xq1:x1:cds5 + xq1:x1:cds6 + xq1:x1:cds8} ;AT={TMEAS}


* Po = AVG( v_load * i_RL )
.meas tran EO INTEG  (V(N_LOAD)*I(Rload))

* Pin = -AVG( v_in * i_V1 )
.meas tran EIN INTEG  (-V(NVIN)*I(V1))

.meas  EFF  PARAM  (EO/EIN*100)

.END
