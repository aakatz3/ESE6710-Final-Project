import pyvisa as visa
import time
import datetime as dtime
import numpy as np
import matplotlib.pyplot as plt
import os
import pathlib as p
import pandas as pd
import shutil
import sys
import tkinter.messagebox as mb

from sweep import Sweep

# Flags
PLOT = True
SHOW_PLOT = False
CLEAR_PREVIOUS = False
SHORT = True
LONG = False
DATASET = 'VGS_VDS'

ANALOG_LABELS = ['VGS_A', 'VGS_B', 'VDS_A', 'VDS_B']
DIGITAL_LABELS = ['CRTL_A', 'IN_A', 'CRTL_B', 'IN_B', 'nEN']

# Standard parameters
ROUT_STD = [50 * np.pi **2 / 8]
DUTY_STD = [0.35]
VIN_STD = [25]
FREQ_STD = [6.78e6]

VINS = np.unique(np.append(VIN_STD, np.arange(18,28.01, 0.5)))
ROUTS = np.unique(np.append(ROUT_STD, np.arange(50,75,0.5)))
FREQS = np.unique(np.append(FREQ_STD, np.arange(6.0e6,7.501e6,0.1e6)))
DUTYS = np.unique(np.append(DUTY_STD, np.arange(0.3,0.4,0.01)))

SWEEPS = [
        Sweep('VIN', VINS, 'V'),
        Sweep('ROUT', ROUTS, 'R'),
        Sweep('FREQ', FREQS, 'Hz'),
        Sweep('DUTY', DUTYS)
    ]

rm = visa.ResourceManager()


# Instruments
v33510B = rm.open_resource('USB0::0x0957::0x2607::MY62003856::0::INSTR')
v34401A = rm.open_resource('ASRL13::INSTR', write_termination = '\r\n')
E3631A = rm.open_resource('ASRL12::INSTR', write_termination = '\r\n')
E3634A = rm.open_resource('ASRL14::INSTR', write_termination = '\r\n')
EDU34450A = rm.open_resource('USB0::0x2A8D::0x8E01::CN62180094::0::INSTR')
EL34143A = rm.open_resource('USB0::0x2A8D::0x3802::MY61001508::0::INSTR')
MSO7034B = rm.open_resource('USB0::2391::5949::MY50340240::0::INSTR')

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


dir = p.Path(f'data/{DATASET}')
wavepath = p.Path(dir, 'waveform')
sspath = p.Path(dir, 'scope')

if CLEAR_PREVIOUS and os.path.isdir(dir.resolve()):
    shutil.rmtree(dir.resolve())

os.makedirs(dir, exist_ok=True)



try:
    
    

    E3631A.read_termination = '\r\n'
    E3634A.read_termination = '\r\n'
    v34401A.read_termination = '\r\n'
    v34401A.timeout = 30000
    MSO7034B.timeout = 30000
    EDU34450A.timeout = 20000


    v34401A.write(':SYSTem:REMote')
    E3634A.write(':SYSTem:REMote')
    E3634A.write(':OUTPut:STATe %d' % (0))
    v33510B.write(':OUTPut1 %d' % (0))
    v33510B.write(':OUTPut2 %d' % (0))

    E3631A.write(':SYSTem:REMote')

    with p.Path(dir, 'instruments.log').open('w', encoding='cp1252') as log:
            log.write('Timestamp: ' +
                    dtime.datetime.now().astimezone().isoformat() + os.linesep)
            print('Instruments Utilized:')
            for inst in [E3634A, E3631A, v33510B, v34401A, EDU34450A, MSO7034B, EL34143A]:
                try:
                    inst.write('*CLS')
                    time.sleep(1)
                    idn = inst.query('*IDN?').strip('\r').strip('\n')
                    log.write(idn + os.linesep)
                    print(' - ' + idn)
                    inst.write('*RST')
                    time.sleep(1)
                    inst.query('SYST:ERR?')
                except BaseException as e:
                    print(e)
                finally:
                    if inst == MSO7034B:
                        inst.write('*CLS')


    # Wavegen Setup
    v33510B.write(':OUTPut1:LOAD %s' % ('INFinity'))
    v33510B.write(':OUTPut2:LOAD %s' % ('INFinity'))
    v33510B.write(':DISPlay:VIEW %s' % ('DUAL'))
    v33510B.write(':DISPlay:FOCus %s' % ('CH2'))
    v33510B.write(':DISPlay:UNIT:VOLTage %s' % ('HIGHlow'))
    v33510B.write(':DISPlay:FOCus %s' % ('CH1'))
    v33510B.write(':DISPlay:UNIT:VOLTage %s' % ('HIGHlow'))
    v33510B.write(':SOURce1:FUNCtion %s' % ('SQUare'))
    v33510B.write(':SOURce1:FUNCtion:SQUare:DCYCle %G' % (DUTY_STD[0] * 100))
    v33510B.write(':SOURce2:FUNCtion %s' % ('SQUare'))
    v33510B.write(':SOURce2:FUNCtion:SQUare:DCYCle %G' % (DUTY_STD[0] * 100))
    v33510B.write(':SOURce1:VOLTage:HIGH %G' % (5.0))
    v33510B.write(':SOURce1:VOLTage:LOW %G' % (0.0))
    v33510B.write(':SOURce2:VOLTage:HIGH %G' % (5.0))
    v33510B.write(':SOURce2:VOLTage:LOW %G' % (0.0))
    v33510B.write(':SOURce1:FREQuency %G HZ' % (FREQ_STD[0]))
    v33510B.write(':SOURce2:FREQuency %G HZ' % (FREQ_STD[0]))
    v33510B.write(':SOURce:PHASe:SYNChronize')
    v33510B.write(':SOURce2:PHASe:ADJust %G' % (180.0))
    v33510B.write(':DISPlay:FOCus %s' % ('CH2'))
    v33510B.write(':SOURce:FREQuency:COUPle:RATio %G' % (1.0))
    v33510B.write(':SOURce:FREQuency:COUPle:MODE %s' % ('RATio'))
    v33510B.write(':SOURce:FREQuency:COUPle:STATe %d' % (1))
    v33510B.write(':DISPlay:FOCus %s' % ('CH1'))
    

    # Logic Power Setup:
    E3631A.write(':SYSTem:REMote')
    E3631A.write(':INSTrument:SELect %s' % ('P6V'))
    E3631A.write(':SOURce:CURRent:LEVel:IMMediate:AMPLitude %G' % (0.5))
    E3631A.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G' % (5.0))
    E3631A.write(':OUTPut:STATe %d' % (1))
    E3631A.query_ascii_values(':MEASure:VOLTage:DC? %s' % ('P6V')) # To return to live measure
    # E-Load Setup
    EL34143A.write(':SOURce:VOLTage:SENSe:SOURce %s' % ('EXTernal'))
    EL34143A.write(':SOURce:MODE %s' % ('RESistance'))
    EL34143A.write(':SOURce:RESistance:LEVel:IMMediate:AMPLitude %G' % ROUT_STD[0])
    EL34143A.write(':OUTPut:STATe %d' % (1))


    # Main Power Setup
    E3634A.write(':SOURce:VOLTage:RANGe %s' % ('HIGH')) # or LOW
    E3634A.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G' % VIN_STD[0])
    E3634A.write(':SOURce:CURRent:LEVel:IMMediate:AMPLitude %G' % (2.2))
    E3634A.query_ascii_values(':MEASure:VOLTage:DC?')
    E3634A.write(':OUTPut:STATe %d' % (0))

 

    # Voltage DMM Setup
    vin_v = v34401A.query_ascii_values(':MEASure:VOLTage:DC? %s,%s' % ('DEF', 'MIN')) [0]

    # Current DMM Setup
    EDU34450A.write(':SENSe:PRIMary:CURRent:DC:RANGe %s' % ('MAX'))
    EDU34450A.write(':SENSe:PRIMary:CURRent:DC:RESolution %s' % ('MIN'))
    EDU34450A.write(':FORMat:OUTPut %d' % (1))

    Idc = EDU34450A.query_ascii_values(':MEASure:PRIMary:CURRent:DC?')

    # Scope Setup
    MSO7034B.write(':SYSTem:PRECision %d' % (1))
    MSO7034B.write(':HARDcopy:INKSaver %d' % (0))
    MSO7034B.write(':ACQuire:RSIGnal %s' % ('IN'))
    MSO7034B.write(':DISPlay:LABel %d' % (1))
    MSO7034B.write(':DIGital0:THReshold %s' % ('CMOS'))
    MSO7034B.write(':DIGital1:THReshold %s' % ('CMOS'))
    MSO7034B.write(':DIGital2:THReshold %s' % ('CMOS'))
    MSO7034B.write(':DIGital3:THReshold %s' % ('CMOS'))
    MSO7034B.write(':DIGital4:THReshold %s' % ('CMOS'))
    MSO7034B.write(':DIGital4:DISPlay %d' % (1))
    MSO7034B.write(':DIGital3:DISPlay %d' % (1))
    MSO7034B.write(':DIGital2:DISPlay %d' % (1))
    MSO7034B.write(':DIGital1:DISPlay %d' % (1))
    MSO7034B.write(':DIGital0:DISPlay %d' % (1))
    MSO7034B.write(':POD1:SIZE %s' % ('SMALl'))
    MSO7034B.write(':DIGital0:LABel "%s"' % DIGITAL_LABELS[0])
    MSO7034B.write(':DIGital1:LABel "%s"' % DIGITAL_LABELS[1])
    MSO7034B.write(':DIGital2:LABel "%s"' % DIGITAL_LABELS[2])
    MSO7034B.write(':DIGital3:LABel "%s"' % DIGITAL_LABELS[3])
    MSO7034B.write(':DIGital4:LABel "%s"' % DIGITAL_LABELS[4])
    MSO7034B.write(':ACQuire:TYPE %s' % ('HRESolution'))
    MSO7034B.write(':CHANnel1:LABel "%s"' % ANALOG_LABELS[0])
    MSO7034B.write(':CHANnel2:LABel "%s"' % ANALOG_LABELS[1])
    MSO7034B.write(':CHANnel3:LABel "%s"' % ANALOG_LABELS[2])
    MSO7034B.write(':CHANnel4:LABel "%s"' % ANALOG_LABELS[3])
    MSO7034B.write(':CHANnel1:DISPlay %d' % (1))
    MSO7034B.write(':CHANnel2:DISPlay %d' % (1))
    MSO7034B.write(':CHANnel3:DISPlay %d' % (1))
    MSO7034B.write(':CHANnel4:DISPlay %d' % (1))
    MSO7034B.write(':TRIGger:EDGE:SOURce %s' % ('EXTernal'))
    MSO7034B.write(':TRIGger:EDGE:LEVel %G' % (0.5))
    MSO7034B.write(':TRIGger:EDGE:SLOPe %s' % ('POSitive'))
    MSO7034B.write(':TRIGger:SWEep %s' % ('NORMal'))
    MSO7034B.write(':TIMebase:MAIN:SCALe %G NS' % (50.0))


    MSO7034B.write(':CHANnel1:SCALe %G V' % (2.0))
    MSO7034B.write(':CHANnel2:SCALe %G V' % (2.0))
    MSO7034B.write(':CHANnel3:SCALe %G V' % (20.0))
    MSO7034B.write(':CHANnel4:SCALe %G V' % (20.0))

    offset1 = -1.75
    offset2 = -1.75
    offset3 = 40
    offset4 = 40

    MSO7034B.write(':CHANnel1:OFFSet %G' % (offset1))
    MSO7034B.write(':CHANnel2:OFFSet %G' % (offset2))
    MSO7034B.write(':CHANnel3:OFFSet %G' % (offset3))
    MSO7034B.write(':CHANnel4:OFFSet %G' % (offset4))

    
    # General measurements Dataframe:

    v33510B.write(':OUTPut1 %d' % (1))
    v33510B.write(':OUTPut2 %d' % (1))
    # E3634A.write(':OUTPut:STATe %d' % (0))
    

    for swp in SWEEPS:
        sweeppath = p.Path(dir, swp.Name)
        wavepath = p.Path(sweeppath, 'waveform')
        sspath = p.Path(sweeppath, 'scope')
        os.makedirs(wavepath, exist_ok=True)
        os.makedirs(sspath, exist_ok=True)
        if (PLOT):
            pltpath = p.Path(sweeppath, 'plt')
            os.makedirs(pltpath, exist_ok=True)
        
        # Reset to std
        E3634A.write(':OUTPut:STATe %d' % (0))
        time.sleep(0.2)
        E3634A.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G' % VIN_STD[0])
        EL34143A.write(':SOURce:RESistance:LEVel:IMMediate:AMPLitude %G' % ROUT_STD[0])
        v33510B.write(':SOURce1:FUNCtion:SQUare:DCYCle %G' % (DUTY_STD[0] * 100))
        v33510B.write(':SOURce2:FUNCtion:SQUare:DCYCle %G' % (DUTY_STD[0] * 100))
        v33510B.write(':SOURce1:FREQuency %G HZ' % (FREQ_STD[0]))
        E3634A.query_ascii_values(':MEASure:VOLTage:DC?')
        E3634A.write(':OUTPut:STATe %d' % (1))
        df_measurements = pd.DataFrame(columns=[
                swp.Name, 'V_IN', 'I_IN', 'P_IN', 'V_OUT', 'I_OUT', 'P_OUT'
            ])
        

        for var in swp.Points:
            print(f'{swp.Name}:{var}')
            

            filename = f'{var}{swp.Unit}'

            match swp.Name:
                case 'VIN':
                    E3634A.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G' % var)
                    E3634A.query_ascii_values(':MEASure:VOLTage:DC?')
                case 'ROUT':
                    EL34143A.write(':SOURce:RESistance:LEVel:IMMediate:AMPLitude %G' % var)
                case 'FREQ':
                    v33510B.write(':SOURce1:FREQuency %G HZ' % (var))
                case 'DUTY':
                    v33510B.write(':OUTPut1 %d' % (0))
                    v33510B.write(':OUTPut2 %d' % (0))
                    E3634A.write(':OUTPut:STATe %d' % (0))
                    time.sleep(0.2)
                    v33510B.write(':SOURce1:FUNCtion:SQUare:DCYCle %G' % (var * 100))
                    v33510B.write(':SOURce2:FUNCtion:SQUare:DCYCle %G' % (var * 100))
                    time.sleep(0.1)
                    v33510B.write(':OUTPut1 %d' % (1))
                    v33510B.write(':OUTPut2 %d' % (1))
                    time.sleep(0.2)
                    E3634A.write(':OUTPut:STATe %d' % (1))
                case _:
                    print(swp.Name)
                    raise AssertionError
                
            time.sleep(0.5)
            # General Measurements
            MSO7034B.write(':RUN')
            


            vin = v34401A.query_ascii_values(':MEASure:VOLTage:DC? %s,%s' % ('DEF', 'MIN'))[0]
            iin = EDU34450A.query_ascii_values(':MEASure:PRIMary:CURRent:DC? %G,%s' % (3.0, 'MIN'))[0]
            vout = EL34143A.query_ascii_values(':MEASure:SCALar:VOLTage:ACDC?')[0]
            iout = EL34143A.query_ascii_values(':MEASure:SCALar:CURRent:ACDC?')[0]
            pout = EL34143A.query_ascii_values(':MEASure:SCALar:POWer:DC?')[0]

            # Scope measurements

            
            # newoffset1 = vin - 1
            # newoffset2 = iin - 2
            # newoffset3 = 
            # while True:
            #     MSO7034B.write(':MEASure:VPP %s' % ('CHANNEL1'))
            #     vinpp = MSO7034B.query_ascii_values(':MEASure:VPP? %s' % ('CHANNEL1')) [0]
            #     if (vinpp < 1e10):
            #         break
            #     else:
            #         newoffset = offset3 + 0.125
            #         MSO7034B.write(':CHANnel3:OFFSet %G' % (offset3))
            MSO7034B.write(':MEASure:CLEar')
            MSO7034B.write(':MEASure:VPP %s' % ('CHANNEL1'))
            MSO7034B.write(':MEASure:VPP %s' % ('CHANNEL2'))
            MSO7034B.write(':MEASure:Vpp %s' % ('CHANNEL3'))
            MSO7034B.write(':MEASure:VPP %s' % ('CHANNEL4'))

            vgsa_pp = MSO7034B.query_ascii_values(':MEASure:VPP? %s' % ('CHANNEL1')) [0]
            vgsa_amp = MSO7034B.query_ascii_values(':MEASure:VAMPlitude? %s' % ('CHANNEL1')) [0]
            vgsb_pp = MSO7034B.query_ascii_values(':MEASure:VPP? %s' % ('CHANNEL2')) [0]
            vgsb_amp = MSO7034B.query_ascii_values(':MEASure:VAMPlitude? %s' % ('CHANNEL2')) [0]
            vdsa_pp = MSO7034B.query_ascii_values(':MEASure:Vpp? %s' % ('CHANNEL3')) [0]
            vdsb_pp =  MSO7034B.query_ascii_values(':MEASure:VPP? %s' % ('CHANNEL4')) [0]


            

            new_row = {
                swp.Name: var,
                'V_IN': vin,
                'I_IN': iin,
                'P_IN': vin*iin,
                'V_OUT': vout,
                'I_OUT': iout,
                'P_OUT': pout,
                'V_GS_A_pp': vgsa_pp,
                'V_GS_A_amp': vgsa_amp,
                'V_GS_B_pp': vgsb_pp,
                'V_GS_B_amp': vgsb_amp,
                'V_DS_A_pp': vdsa_pp,
                'V_DS_B_pp': vdsb_pp,
            }
            df_measurements = df_measurements._append(new_row, ignore_index=True)

            # Scope captures
            MSO7034B.write(':STOP')
            if PLOT:
                plt.figure()
            for c in range(0, 3):
                MSO7034B.write(':WAVeform:SOURce %s' % ('CHANnel%d' % (c + 1)))
                MSO7034B.write(':WAVeform:POINts %s' % ('MAXimum'))
                MSO7034B.write(':WAVeform:FORMat %s' % ('WORD'))
                MSO7034B.write(':WAVeform:UNSigned %d' % (1))
                MSO7034B.write(':WAVeform:BYTeorder %s' % ('LSBFirst'))
                r = MSO7034B.query(':waveform:preamble?')
                xinc, xorg, xref, yinc, yorg, yref = [
                    float(i) for i in r.split(',')[4:]
                ]
                binary_block_data = MSO7034B.query_binary_values(':WAVeform:DATA?',
                                                                datatype='H')
                acq_data = np.array(binary_block_data)
                scaled_data = (acq_data - yref) * yinc + yorg
                if c == 0:
                    times = np.arange(0, xinc * len(acq_data), xinc)
                    dat_tmp = {
                        "Time (s)": times[0:min(len(times), len(scaled_data))],
                        ANALOG_LABELS[c]: scaled_data[0:min(len(times), len(scaled_data))]
                    }
                    dframe = pd.DataFrame(dat_tmp)
                else:
                    dframe.insert(c + 1, ANALOG_LABELS[c],
                                scaled_data[0:min(len(times), len(scaled_data))])
                if PLOT:
                    plt.plot(times[0:min(len(times), len(scaled_data))],
                            scaled_data[0:min(len(times), len(scaled_data))])
            if PLOT:
                    if SHOW_PLOT:
                        plt.show()
                    plt.savefig(p.Path(pltpath, f'{filename}.svg'), format='svg')
                    plt.close()
            dframe.to_csv(p.Path(wavepath, f'{filename}_MSO7034B.csv'),
                        index=False)
            


            # Screenshot
            MSO7034B.write(':RUN')
            time.sleep(3)

            succeed = False
            while not succeed:
                try:
                    time.sleep(0.25)
                    img = MSO7034B.query_binary_values(':DISPlay:DATA? %s,%s,%s' %
                                                        ('PNG', 'SCReen', 'COLor'),
                                                        datatype='c')
                    MSO7034B.write(':STOP')
                    
                    with open(p.Path(sspath, f'{filename}_MSO7034B.png'), 'wb') as f:
                        for b in img:
                            f.write(b)
                    succeed = True
                except BaseException as e:
                    print(e)
                    time.sleep(10)
        df_measurements.to_csv(p.Path(sweeppath, 'measurements.csv'), index=False)

except BaseException as e:
    print(e)
finally:
    E3634A.write(':OUTPut:STATe %d' % (0))
    E3631A.write(':OUTPut:STATe %d' % (0))
    v33510B.write(':OUTPut1 %d' % (0))
    v33510B.write(':OUTPut2 %d' % (0))
    time.sleep(0.5)
    v34401A.write(':SYSTem:LOCal')
    E3634A.write(':SYSTem:LOCal')
    E3631A.write(':SYSTem:LOCal')
    time.sleep(1)
    v33510B.close()
    v34401A.close()
    E3631A.close()
    E3634A.close()
    EDU34450A.close()
    EL34143A.close()
    MSO7034B.close()
    rm.close()


