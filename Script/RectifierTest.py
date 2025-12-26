import pyvisa as visa
import time
import datetime as dtime
import numpy as np
import matplotlib.pyplot as plt
import os
import pathlib as pl
import pandas as pd
import sys
from pint import UnitRegistry
import tkinter.messagebox as mb
import tkinter as tk
from tkinter import ttk

# Flags
PLOT = True
SHOW_PLOT = False
DATASET = 'RECTIFIER'

ANALOG_LABELS = ['V_IN', 'I_IN', 'V_OUT', 'I_OUT']
CONFIGURATIONS = ['RB058LAM100TF', 'STPS360AF']
CONFIGURATIONS.sort()


# Provided by ChatGPT. Not proud of that, but it was the simplest option.
def choose_option(prompt, options):
    root = tk.Tk()
    root.withdraw()

    result = None

    dialog = tk.Toplevel(root)
    dialog.title("Select an option")

    tk.Label(dialog, text=prompt).pack(padx=10, pady=5)

    combo = ttk.Combobox(dialog, values=options, state="readonly")
    combo.current(0)
    combo.pack(padx=10, pady=5)

    def submit():
        nonlocal result
        result = combo.get()
        dialog.destroy()

    ttk.Button(dialog, text="OK", command=submit).pack(pady=10)

    dialog.grab_set()
    dialog.wait_window()

    root.destroy()
    return result

# Stackoverflow
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# This is a script, it's OK to be messy. the point is hack it together so it works and do that quick

u = UnitRegistry(autoconvert_offset_to_baseunit=True)

rm = visa.ResourceManager()
v33521A = rm.open_resource('USB0::2391::5639::MY50000944::0::INSTR')
MSO7034B = rm.open_resource('USB0::2391::5949::MY50340240::0::INSTR')
MSO7034B.timeout = 15000
EL34143A = rm.open_resource('USB0::0x2A8D::0x3802::MY61001508::0::INSTR')

dir = pl.Path('data', DATASET)
wavepath = pl.Path(dir, 'waveform')
sspath = pl.Path(dir, 'scope')
for d in [dir, wavepath, sspath]:
    os.makedirs(d, exist_ok=True)
if (PLOT):
    pltpath = pl.Path(dir, 'plt')
    os.makedirs(pltpath, exist_ok=True)



rows = list()
try:
    with pl.Path(dir, 'instruments.log').open('w', encoding='cp1252') as log:
            log.write('Timestamp: ' +
                    dtime.datetime.now().astimezone().isoformat() + os.linesep)
            print('Instruments Utilized:')
            for inst in [v33521A, MSO7034B, EL34143A]:
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
                        probes = list()
                        for i in range(0,4):
                            probes.append(MSO7034B.query(':CHANnel%g:PROBe:ID?' % (i+1)).strip('\r').strip('\n'))
                        print(f'    - Probes: {", ".join(probes)}')
                        log.write('REPORTED PROBES: ' + ", ".join(probes))
    
    

    

    VIN = 10 * u.volt
    RF_LOAD = 50 * u.ohm
    DC_LOAD = 50 * np.pi **2 / 8 * u.ohm

    P_IN_SET = (VIN ** 2 / RF_LOAD).to('W')

    # Initialize everything
    EL34143A.write(':SOURce:VOLTage:SENSe:SOURce %s' % ('EXTernal'))
    EL34143A.write(':SOURce:MODE %s' % ('RESistance'))
    EL34143A.write(':SOURce:RESistance:LEVel:IMMediate:AMPLitude %G' % (DC_LOAD.magnitude))
    EL34143A.write(':OUTPut:STATe %d' % (1))

    MSO7034B.write(':HARDcopy:INKSaver %d' % (0))
    MSO7034B.write(':ACQuire:TYPE %s' % ('HRESolution'))
    MSO7034B.write(':TRIGger:SWEep %s' % ('NORMal'))
    MSO7034B.write(':TRIGger:MODE %s' % ('EDGE'))
    MSO7034B.write(':TRIGger:EDGE:SOURce %s' % ('EXTernal'))
    MSO7034B.write(':TRIGger:EDGE:LEVel %G' % (0.5))
    MSO7034B.write(':TRIGger:EDGE:SLOPe %s' % ('POSitive'))
    MSO7034B.write(':CHANnel1:LABel "%s"' % ANALOG_LABELS[0])
    MSO7034B.write(':CHANnel2:LABel "%s"' % ANALOG_LABELS[1])
    MSO7034B.write(':CHANnel3:LABel "%s"' % ANALOG_LABELS[2])
    MSO7034B.write(':CHANnel4:LABel "%s"' % ANALOG_LABELS[3])
    MSO7034B.write(':CHANnel1:PROBe %s' % ('X10'))
    MSO7034B.write(':CHANnel3:PROBe %s' % ('X10'))
    MSO7034B.write(':CHANnel1:DISPlay %d' % (1))
    MSO7034B.write(':CHANnel2:DISPlay %d' % (1))
    MSO7034B.write(':CHANnel3:DISPlay %d' % (1))
    MSO7034B.write(':CHANnel4:DISPlay %d' % (1))
    MSO7034B.write(':DISPlay:LABel %d' % (1))
    MSO7034B.write(':TIMebase:MAIN:SCALe %G NS' % (50.0))
    MSO7034B.write(':CHANnel1:SCALe %G V' % (10.0))
    MSO7034B.write(':CHANnel2:SCALe %G V' % (0.2))
    MSO7034B.write(':CHANnel3:SCALe %G V' % (0.2))
    MSO7034B.write(':CHANnel4:SCALe %G V' % (0.02))
   

    v33521A.write(':SOURce:FUNCtion:SHAPe %s' % ('SINusoid'))
    v33521A.write(':SOURce:VOLTage:LEVel:UNIT %s' % ('DBM'))
    v33521A.write(':OUTPut:LOAD %G' % (50.0))
    v33521A.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G VPP' % (VIN.magnitude))
    v33521A.write(':SOURce:FREQuency:CW %G MHZ' % (6.78))
    

    time.sleep(2)
    rows = list()
    stop = False
    while len(CONFIGURATIONS) > 0:
        MSO7034B.write(':RUN')
        MSO7034B.write(':CHANnel4:OFFSet %G' % (0.050))
        # Get config
        if(len(CONFIGURATIONS) == 1):
            selected = CONFIGURATIONS[0]
        else:
            selected = choose_option('Select diode part number', CONFIGURATIONS)
        if selected == None:
            break
        
        CONFIGURATIONS.remove(selected)

        v33521A.write(':OUTPut:STATe %d' % (0))
        
        # Check if measurement is OK
        while not mb.askyesno("Ready?", f"Is {selected} connected and ready for measurement?"):
            if not mb.askretrycancel("Continue", f"Please connect {selected}"):
                stop = True
                break
        if stop:
            break
        # Do measurement and save screenshot

        v33521A.write(':OUTPut:STATe %d' % (1))

        MSO7034B.write(':RUN')
        VOUT = EL34143A.query_ascii_values(':MEASure:SCALar:VOLTage:ACDC?')[0]
        IOUT = EL34143A.query_ascii_values(':MEASure:SCALar:CURRent:ACDC?')[0]
        POUT = EL34143A.query_ascii_values(':MEASure:SCALar:POWer:DC?')[0]
        
        MSO7034B.write(':CHANnel1:OFFSet %G' % (-28.875))
        MSO7034B.write(':CHANnel2:OFFSet %G' % (-0.1))
        MSO7034B.write(':CHANnel3:OFFSet %G' % (0.2 + VOUT))
        MSO7034B.write(':CHANnel4:OFFSet %G' % (0.050 + IOUT))

        MSO7034B.write(':MEASure:CLEar')
        MSO7034B.write(':MEASure:VPP %s' % ('CHANNEL1'))
        MSO7034B.write(':MEASure:VPP %s' % ('CHANNEL2'))
        MSO7034B.write(':MEASure:VPP %s' % ('CHANNEL3'))
        MSO7034B.write(':MEASure:VPP %s' % ('CHANNEL4'))

        MSO7034B.write(':STOP')

        VIN_PP = MSO7034B.query_ascii_values(':MEASure:VPP? %s' % ('CHANNEL1')) [0]
        VIN_AVG = MSO7034B.query_ascii_values(':MEASure:VAVerage? %s' % ('CHANNEL1')) [0]
        VIN_RMS = MSO7034B.query_ascii_values(':MEASure:VRMS? %s' % ('CHANNEL1')) [0]
        IIN_PP = MSO7034B.query_ascii_values(':MEASure:VPP? %s' % ('CHANNEL2')) [0]
        IIN_AVG = MSO7034B.query_ascii_values(':MEASure:VAVerage? %s' % ('CHANNEL2')) [0]
        IIN_RMS = MSO7034B.query_ascii_values(':MEASure:VRMS? %s' % ('CHANNEL2')) [0]
        VOUT_PP = MSO7034B.query_ascii_values(':MEASure:VPP? %s' % ('CHANNEL3')) [0]
        VOUT_AVG = MSO7034B.query_ascii_values(':MEASure:VAVerage? %s' % ('CHANNEL3')) [0]
        VOUT_RMS = MSO7034B.query_ascii_values(':MEASure:VRMS? %s' % ('CHANNEL3')) [0]
        IOUT_PP = MSO7034B.query_ascii_values(':MEASure:VPP? %s' % ('CHANNEL4')) [0]
        IOUT_AVG = MSO7034B.query_ascii_values(':MEASure:VAVerage? %s' % ('CHANNEL4')) [0]
        IOUT_RMS = MSO7034B.query_ascii_values(':MEASure:VRMS? %s' % ('CHANNEL4')) [0]

        
        
        rows.append({
            'CONFIG': selected,
            'P_IN_SET': P_IN_SET.magnitude,
            'V_IN_PP': VIN_PP,
            'V_IN_AVG': VIN_AVG,
            'V_IN_RMS': VIN_RMS,
            'I_IN_PP': IIN_PP,
            'I_IN_AVG': IIN_AVG,
            'I_IN_RMS': IIN_RMS,
            'PIN_AVG': VIN_RMS * IIN_RMS,
            'V_OUT_DC': VOUT,
            'I_OUT_DC': IOUT,
            'P_OUT_DC': POUT,
            'V_OUT_PP': VOUT_PP,
            'V_OUT_AVG': VOUT_AVG,
            'V_OUT_RMS': VOUT_RMS,
            'I_OUT_PP': IOUT_PP,
            'I_OUT_AVG': IOUT_AVG,
            'I_OUT_RMS': IOUT_RMS,
            'POUT_AVG': IOUT_RMS * VOUT_RMS
        })



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
                plt.savefig(pl.Path(pltpath, f'{selected}.svg'), format='svg')
                plt.close()
        dframe.to_csv(pl.Path(wavepath, f'{selected}_MSO7034B.csv'),
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
                
                with open(pl.Path(sspath, f'{selected}_MSO7034B.png'), 'wb') as f:
                    for b in img:
                        f.write(b)
                succeed = True
            except BaseException as e:
                print(e)
                time.sleep(10)
            
    measurements = pd.DataFrame(rows)
    measurements.to_csv(pl.Path(dir, 'measurements.csv'), index=False)
    

except BaseException as e:
    print(e)
finally:
    v33521A.write(':OUTPut %d' % (0))
    time.sleep(0.5)
    v33521A.close()
    EL34143A.close()
    MSO7034B.close()
    rm.close()





