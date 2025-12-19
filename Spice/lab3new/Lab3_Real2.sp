
.lib OptiMOS_OptiMOS5_60V_LTSpice.lib
.lib SN74LVC1G34.cir
.lib LM5114A_TRANS.lib

.param FS      = 6.78e6
.param DUTY    = 0.5
.param VI      = 12

.param NCYCLES = 300
.param SHCYCLES= 4
.param PPS     = 3000
.param TPER    = 1/FS
.param TSTOP   = NCYCLES*TPER
.param TMEAS   = (NCYCLES-SHCYCLES)*TPER
.param TSTEP   = TPER/PPS

.options method=Trap abstol=1n vntol=1e-3 reltol=0.001  solver=alt
.options nomarch maxord=1 list logparams logopinfo
.OPTIONS measdgt=99
.OPTIONS numdgt=99
.OPTIONS gmin=1e-15
.tran 0 {TSTOP} {TMEAS} {TSTEP} uic
.OPTIONS itl1=100000
.OPTIONS itl2=100000
.OPTIONS itl4=100000
;.op

V1 NVIN 0 {VI}
LCH NVIN NSW 18644.305e-9 Rser=0.520
XQ1 NSW NG 0 BSC065N06LS5_L1
Cp NSW 0 340260.190e-15
Lser N_SER N_LOAD 582.565e-9 Rser = 0.05
Cser NSW N_SER 1227665.346e-15
Rload N_LOAD 0 5.187

;.step lin param C_oss 20p 1100p 10p
;.step lin param C_oss 50p 850p 10p
;.step param QL list 6 15 20 25

*DRIVE
.param VDRV   = 5
.param TRISE  = 8.4n ; From Keysight 35521A Datasheet
.param TFALL  = 8.4n
.param TON    = DUTY*TPER

V2 VCC 0 {VDRV}
Vg CRTL 0 PULSE(0 {VDRV} 0 {TRISE} {TFALL} {TON} {TPER})
XU1 INA CRTL VCC 0 SN74LVC1G34
XU2 INA 0 VCC NGP NGN 0 LM5114A
RGP NGP NG 1e-3
RGN NGN NG 1.5


.meas VOUT_RMS RMS  V(n_load)
.meas POUT_AAVG param {VOUT_RMS} * {IOUT_RMS}
.MEAS IOUT_RMS RMS I(Rload)
.meas V_DS_MAX max(V(nsw))
.meas V_DS_ON FIND V(nsw) AT 170n

.END
