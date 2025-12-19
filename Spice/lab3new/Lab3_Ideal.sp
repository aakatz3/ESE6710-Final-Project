* Lab 3 - Ideal switch
.param FS      = 6.78e6
.param DUTY    = 0.5
.param VI      = 12
.param RL      = 5

.param QL      = 5

.param Ls = QL*RL/(2*pi*FS)+20n
.param LCHOKE  = 20*Ls
.param Cs = 1/(2*pi*FS*RL*(QL-1.1525))+0.05n
.param Cp_ideal = 1/(34.22*RL*FS)

.param NCYCLES = 300
.param SHCYCLES= 3
.param PPS     = 3000
.param TPER    = 1/FS
.param TSTOP   = NCYCLES*TPER
.param TMEAS   = (NCYCLES-SHCYCLES)*TPER
.param TSTEP   = TPER/PPS

.options method=Trap abstol=1n vntol=1e-3 reltol=0.001  solver=alt
.options nomarch maxord=1
.OPTIONS measdgt=99
.OPTIONS numdgt=99
.OPTIONS gmin=1e-15
.tran 0 {TSTOP} {TMEAS} {TSTEP} uic
.OPTIONS itl1=100000
.OPTIONS itl2=100000
.OPTIONS itl4=100000


V1 NVIN 0 {VI}
LCH NVIN NSW {LCHOKE}
XQ1 NSW 0 NG SWMOS   ; D=NSW, S=0, G=NG
;S1 NSW 0 NG 0 SWIDEAL
Cp NSW 0 {Cp_ideal};{Cp_ext}
Lser N_SER N_LOAD {Ls}
Cser NSW N_SER {Cs}
Rload N_LOAD 0 {RL}

;.step lin param C_oss 20p 1100p 10p
;.step lin param C_oss 50p 850p 10p
;.step param QL list 6 15 20 25

*DRIVE
.param VDRV   = 5
.param TRISE  = 1e-9
.param TFALL  = 1e-9
.param TON    = DUTY*TPER

Vg NG 0 PULSE(0 {VDRV} 0 {TRISE} {TFALL} {TON-2e-9} {TPER})



;.SUBCKT SWMOS D S G

;S1 D S G 0 SW_IDEAL
;Dbody S D D_IDEAL

;.model SW_IDEAL SW(Vt=2.5 Vh=0 Ron=5m Roff=1e9 Vser=1e-15)
;.model D_IDEAL D(Ron=1e-15 Vfwd=1e-15 Vrev=1e15)

;.ENDS SWMOS
.MODEL SWIDEAL SW(RON=0.1m ROFF=1G VT=2 VH=0)
.SUBCKT SWMOS D S G
DFWD D N1 DIDEAL
S1 N1 S G 0 SWIDEAL
DAP S D DVP
.MODEL DIDEAL D(RON=1m)
.MODEL DVP D(RON=5m VFWD=0.7)
.MODEL SWIDEAL SW(RON=1m ROFF=10MEG VT=0.5 VH=0.1)
.ENDS SWMOS

.meas M_LCHOKE param  {LCHOKE}
.meas M_LS param  {LS}
.meas M_CIDEAL param  {CP_IDEAL}
.meas M_Cs param  {Cs}
.meas POUT RMS I(Rload)* V(n_load)
.MEAS IOUT_RMS RMS I(Rload)
.meas V_DS_MAX max(V(nsw))
.meas V_DS_ON FIND V(nsw) AT 170n
.meas Q_L param QL
;.meas TRAN m_cds PARAM {xq1:x1:cds2 + xq1:x1:cds3 + xq1:x1:cds5 + xq1:x1:cds6 + xq1:x1:cds8} ;AT={TMEAS}


* Po = AVG( v_load * i_RL )
*.meas TRAN POUT AVG  V(N_LOAD)*I(Rload)

* Pin = -AVG( v_in * i_V1 )
*.meas TRAN PIN  AVG  -V(NVI)*I(V1)

*.meas TRAN EFF  param  POUT/PIN*100
.meas tran EO INTEG  (V(N_LOAD)*I(Rload)) FROM {TSTOP-20*TPER} TO {TSTOP}

* Pin = -AVG( v_in * i_V1 )
.meas tran EIN INTEG  (-V(NVIN)*I(V1)) FROM {TSTOP-20*TPER} TO {TSTOP}

.meas  EFF  PARAM  (EO/EIN*100)
.END
