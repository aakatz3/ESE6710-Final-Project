# Probe notes:
# all 10X/diff probe: connect via BNC U, also connect to scope channel 1
# For spec A: run through 1Meg resistor and through ZFL-500LN+
import pyvisa as visa
import time
from RsInstrument import RsInstrument as RS
import datetime as dtime
import numpy as np
import matplotlib.pyplot as plt
import os
import pathlib as p
import pandas as pd
import sys
from tkinter import messagebox as mb
import tkinter as tk
from tkinter import ttk
from sweep import Sweep
from playsound import playsound as play

# Flags
PLOT = False
SHOW_PLOT = False
CLEAR_PREVIOUS = False
DATASET = 'Spectrum'
SCREENSHOT = True


# NOTE: 10X probe = 20db attenuation
ANALOG_LABELS = ['', '', '', '']
DIGITAL_LABELS = ['CRTL_A', 'IN_A', 'CRTL_B', 'IN_B', 'nEN']

# Standard parameters
ROUT_STD = [50 * np.pi **2 / 8]
DUTY_STD = [0.32]
VIN_STD = [25]
FREQ_STD = [6.78e6]

# Make sure to include these globals

SIGNALS = ['V_DSA-V_DSB', 'V_MR', 'V_PRI', 'V_SEC', 'V_RECT', 'V_LOAD', 'V_LOAD_RF']
FETS = ['IGB070S10S1', 'IGB110S101', 'BSC065N06LS5', 'BSC096N10LS5', 'BSC160N15NS5']
# slice list to include only ones actually soldered
FETS = [FETS[1], FETS[3]]
DIODES = ['RB058LAM100TF', 'STPS360AF']

FREQS = np.unique(np.append(FREQ_STD, np.arange(6.0e6,7.501e6,0.1e6)))
DUTYS = np.unique(np.append(DUTY_STD, np.arange(0.3,0.4,0.01)))

SWEEPS = [
        Sweep('FREQ', FREQS, 'Hz'),
        Sweep('DUTY', DUTYS)
    ]

rm = visa.ResourceManager()

# Define the device handles
FPC1000 = RS('USB0::0x0AAD::0x01BB::101228::2::INSTR',  # Original resource string when using USB connection
                       reset=True, id_query=True, options="SelectVisa='rs'")
v33521A = rm.open_resource('USB0::2391::5639::MY50000944::0::INSTR')
v33510B = rm.open_resource('USB0::0x0957::0x2607::MY62003856::0::INSTR')
E3631A = rm.open_resource('ASRL12::INSTR', write_termination = '\r\n')
E3634A = rm.open_resource('ASRL14::INSTR', write_termination = '\r\n')
EL34143A = rm.open_resource('USB0::0x2A8D::0x3802::MY61001508::0::INSTR')
MSO7034B = rm.open_resource('USB0::2391::5949::MY50340240::0::INSTR')


# utility variables
# this isn't the best code practice but it works
global sweeppath
global wavepath
global sspath
global pltpath
global spectrumpath
global filename

#
# Define subroutines
#

def prompt_user():
    root = tk.Tk()
    root.withdraw()

    result = None

    dialog = tk.Toplevel(root)
    dialog.title("Select an option")
    dialog.resizable(False, False)

    tk.Label(dialog, text='FET Selection').pack(padx=10, pady=5)

    combo = ttk.Combobox(dialog, values=FETS, state="readonly")
    combo.pack(padx=10, pady=5)

    tk.Label(dialog, text='Signal Selection').pack(padx=10, pady=5)

    combo2 = ttk.Combobox(dialog, values=SIGNALS, state="readonly")
    combo2.pack(padx=10, pady=5)

    def submit():
        if (combo.get() != '') & (combo2.get() != ''):
            nonlocal result
            result = (combo.get(), combo2.get())
            dialog.destroy()
        else:
            mb.showerror(
                message='Please select a value for the FET and the signal', parent=dialog)

    ttk.Button(dialog, text="OK", command=submit).pack(pady=10)

    dialog.grab_set()
    dialog.wait_window()

    if result == None:
        raise ValueError('No selection made in configuration dialog')
    
    if result[1] == 'V_RECT':
        dialog = tk.Toplevel(root)
        dialog.title("Select an option")
        dialog.resizable(False, False)

        tk.Label(dialog, text='Rectifier Selection').pack(padx=10, pady=5)

        combo = ttk.Combobox(dialog, values=DIODES, state="readonly")
        combo.pack(padx=10, pady=5)

        def submit():
            if (combo.get() != ''):
                nonlocal result
                result[1] = result(1) + '_' + combo.get()
                dialog.destroy()
            else:
                mb.showerror(
                    message='Please select a value for the FET and the signal', parent=dialog)

    root.destroy()

    return result


def com_prep():
    """Preparation of the communication (termination, timeout, etc...)"""

    E3631A.read_termination = '\r\n'
    E3634A.read_termination = '\r\n'
    MSO7034B.timeout = 30000
    
    # Safety ops
    E3634A.write(':SYSTem:REMote')
    E3634A.write(':OUTPut:STATe %d' % (0))
    E3631A.write(':SYSTem:REMote')
    E3631A.write(':OUTPut:STATe %d' % (0))
    v33510B.write(':OUTPut1 %d' % (0))
    v33510B.write(':OUTPut2 %d' % (0))
    
    FPC1000.visa_timeout = 8000  # Timeout in ms for VISA Read Operations
    FPC1000.opc_timeout = 3000  # Timeout in ms for opc-synchronised operations
    FPC1000.instrument_status_checking = True  # Error check after each command
    FPC1000.clear_status()  # Clear status register
    FPC1000.write_str_with_opc('*RST')

    global dir
    
    with p.Path(dir, 'instruments.log').open('w', encoding='cp1252') as log:
            log.write('Timestamp: ' +
                    dtime.datetime.now().astimezone().isoformat() + os.linesep)
            print('Instruments Utilized:')
            for inst in [E3634A, E3631A, v33521A, v33510B, MSO7034B, EL34143A, FPC1000, ]:
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
    for inst in [v33510B, v33521A, MSO7034B, EL34143A, FPC1000]:
        time_now = dtime.datetime.now().astimezone()
        inst.write(':SYSTem:TIME %d,%d,%d' % (time_now.hour, time_now.minute, time_now.second))
        inst.write(':SYSTem:DATE %d,%d,%d' % (time_now.year, time_now.month, time_now.day))
        # errors = inst.query_ascii_values(':SYSTem:ERRor?', converter='s')
        # print(f'{errors[0]}: {errors[1].strip('\r').strip('\n')}')
        # print( inst.query_ascii_values(':SYSTem:DATE?'))
        # print( inst.query_ascii_values(':SYSTem:TIME?'))
        # print(f'{errors[0]}: {errors[1].strip('\r').strip('\n')}')


def close():
    """Close the VISA session"""
    E3634A.write(':OUTPut:STATe %d' % (0))
    E3631A.write(':OUTPut:STATe %d' % (0))
    v33510B.write(':OUTPut1 %d' % (0))
    v33510B.write(':OUTPut2 %d' % (0))
    v33521A.write(':OUTPut %d' % (0))
    FPC1000.write_str_with_opc('SYSTem:BNC:MODE TRIGger')
    time.sleep(0.5)
    v33510B.close()
    E3631A.close()
    E3634A.close()
    EL34143A.close()
    MSO7034B.close()
    v33521A.close()
    FPC1000.close()
    rm.close()


def meas_prep():
    

    # Reference setup
    v33521A.write(':OUTPut:LOAD %s' % ('INFinity'))
    v33521A.write(':SOURce:APPLy:SINusoid %G MHZ,%G VPP,%G' % (10.0, 4.5, 0.0))
    
    # Spectrum Analyzer Setup
    FPC1000.write_str_with_opc('SYSTem:BNC:MODE REFerence')
    FPC1000.write_str_with_opc('FREQ:STAR 0.6e6')
    FPC1000.write_str_with_opc('FREQ:STOP 60e6')
    FPC1000.write_str_with_opc('SENSe:BANDwidth:RESolution %G' % (10e3))
    FPC1000.write_str_with_opc('SENSe:BANDwidth:VIDeo:AUTO 1')
    FPC1000.write_str_with_opc('DISPlay:TRACe1:MODE WRITe')  # Trace to Write mode
    FPC1000.write_str_with_opc('SENSe:DETector1:FUNCtion RMS')
    
    
    # Wavegen Setup
    v33510B.write(':SOURce:ROSCillator:SOURce %s' % ('EXTernal'))
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

    time.sleep(0.5)

    # Logic Power Setup:
    E3631A.write(':SYSTem:REMote')
    E3631A.write(':INSTrument:SELect %s' % ('P6V'))
    E3631A.write(':SOURce:CURRent:LEVel:IMMediate:AMPLitude %G' % (0.5))
    E3631A.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G' % (5.0))
    E3631A.write(':OUTPut:STATe %d' % (1))
    E3631A.query_ascii_values(':MEASure:VOLTage:DC? %s' % ('P6V')) # To return to live measure
    time.sleep(0.5)
    
    # Technially inefficient but it doesn't matter
    # E-Load Setup
    EL34143A.write(':SOURce:VOLTage:SENSe:SOURce %s' % ('EXTernal'))
    EL34143A.write(':SOURce:MODE %s' % ('RESistance'))
    EL34143A.write(':SOURce:RESistance:LEVel:IMMediate:AMPLitude %G' % ROUT_STD[0])
    EL34143A.write(':OUTPut:STATe %d' % (1))
    time.sleep(0.5)

    # Main Power Setup
    E3634A.write(':SOURce:VOLTage:RANGe %s' % ('HIGH')) # or LOW
    E3634A.write(':SOURce:VOLTage:PROTection:STATe 0')
    E3634A.write(':SOURce:VOLTage:PROTection:CLEar')
    E3634A.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G' % VIN_STD[0])
    E3634A.write(':SOURce:CURRent:LEVel:IMMediate:AMPLitude %G' % (2.2))
    E3634A.query_ascii_values(':MEASure:VOLTage:DC?')
    E3634A.write(':OUTPut:STATe %d' % (0))
    time.sleep(0.5)
   

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
    MSO7034B.write(':DIGital4:DISPlay %d' % (0))
    MSO7034B.write(':DIGital3:DISPlay %d' % (1))
    MSO7034B.write(':DIGital2:DISPlay %d' % (0))
    MSO7034B.write(':DIGital1:DISPlay %d' % (1))
    MSO7034B.write(':DIGital0:DISPlay %d' % (0))
    MSO7034B.write(':POD1:SIZE %s' % ('SMALl'))
    MSO7034B.write(':DIGital0:LABel "%s"' % DIGITAL_LABELS[0])
    MSO7034B.write(':ACQuire:TYPE %s' % ('HRESolution'))
    MSO7034B.write(':CHANnel1:LABel "%s"' % ANALOG_LABELS[0])
    MSO7034B.write(':CHANnel2:LABel "%s"' % ANALOG_LABELS[1])
    MSO7034B.write(':CHANnel3:LABel "%s"' % ANALOG_LABELS[2])
    MSO7034B.write(':CHANnel4:LABel "%s"' % ANALOG_LABELS[3])
    MSO7034B.write(':CHANnel1:DISPlay %d' % (1))
    MSO7034B.write(':CHANnel2:DISPlay %d' % (0))
    MSO7034B.write(':CHANnel3:DISPlay %d' % (0))
    MSO7034B.write(':CHANnel4:DISPlay %d' % (0))
    MSO7034B.write(':TRIGger:EDGE:SOURce %s' % ('EXTernal'))
    MSO7034B.write(':TRIGger:EDGE:LEVel %G' % (0.5))
    MSO7034B.write(':TRIGger:EDGE:SLOPe %s' % ('POSitive'))
    MSO7034B.write(':TRIGger:SWEep %s' % ('NORMal'))
    MSO7034B.write(':TIMebase:MAIN:SCALe %G NS' % (50.0))
    time.sleep(0.5)

df_measurements = None

def do_sweep(swp : Sweep):
    global spectrumpath
    global wavepath
    global sspath
    sweeppath = p.Path(dir, swp.Name)
    wavepath = p.Path(sweeppath, 'waveform')
    sspath = p.Path(sweeppath, 'scope')
    spectrumpath = p.Path(sweeppath, 'spectrum')
   
    os.makedirs(wavepath, exist_ok=True)
    os.makedirs(sspath, exist_ok=True)
    os.makedirs(spectrumpath, exist_ok=True)
    if (PLOT):
        pltpath = p.Path(sweeppath, 'plt')
        os.makedirs(pltpath, exist_ok=True)
    
    # Reset to std
    E3634A.write(':OUTPut:STATe %d' % (0))
    time.sleep(0.2)
    E3634A.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G' % VIN_STD[0])
    E3634A.write(':OUTPut:STATe %d' % (0))
    # E3634A.write(':SOURce:VOLTage:PROTection:CLEar')
    E3634A.write(':SOURce:VOLTage:PROTection:STATe 0')

    EL34143A.write(':SOURce:RESistance:LEVel:IMMediate:AMPLitude %G' % ROUT_STD[0])
    v33510B.write(':SOURce1:FUNCtion:SQUare:DCYCle %G' % (DUTY_STD[0] * 100))
    v33510B.write(':SOURce2:FUNCtion:SQUare:DCYCle %G' % (DUTY_STD[0] * 100))
    v33510B.write(':SOURce1:FREQuency %G HZ' % (FREQ_STD[0]))
    v33510B.write(':OUTPut1 %d' % (1))
    v33510B.write(':OUTPut2 %d' % (1))
    time.sleep(0.5)
    E3634A.query_ascii_values(':MEASure:VOLTage:DC?')
    time.sleep(0.5)
    E3634A.write(':OUTPut:STATe %d' % (1))
    E3634A.write(':SOURce:VOLTage:PROTection:STATe 0')
    # E3634A.write(':SOURce:VOLTage:PROTection:CLEar')
    time.sleep(1)
    for var in swp.Points:
        print(f'{swp.Name}:{var}')
            
        global filename
        filename = f'{var}{swp.Unit}'
        match swp.Name:
            case 'FREQ':
                v33510B.write(':SOURce1:FREQuency %G HZ' % (var))
            case 'DUTY':
                E3634A.write(':OUTPut:STATe %d' % (0))
                v33510B.write(':OUTPut1 %d' % (0))
                v33510B.write(':OUTPut2 %d' % (0))
                
                time.sleep(1)
                v33510B.write(':SOURce1:FUNCtion:SQUare:DCYCle %G' % (var * 100))
                v33510B.write(':SOURce2:FUNCtion:SQUare:DCYCle %G' % (var * 100))
                time.sleep(0.1)
                v33510B.write(':OUTPut1 %d' % (1))
                v33510B.write(':OUTPut2 %d' % (1))
                time.sleep(1)
                E3634A.write(':OUTPut:STATe %d' % (1))
            case _:
                print(swp.Name)
                raise AssertionError
        time.sleep(1)
        E3634A.write(':SOURce:VOLTage:PROTection:STATe 0')
        # E3634A.write(':SOURce:VOLTage:PROTection:CLEar')
        E3634A.query_ascii_values(':MEASure:VOLTage:DC?')
        time.sleep(1)
        trace_get()
        screen_copy()
        time.sleep(0.5)
    
    pass

def trace_get():
    """Initialize continuous measurement, stop it after the desired time, query trace data"""
    FPC1000.write_str_with_opc('FORMat:DATA ASCii')
    swptime = FPC1000.query_float_with_opc('SENSE:SWEEP:TIME?')
    FPC1000.write_str_with_opc(
        'INITiate:CONTinuous Off')  # Single measurement on trace 1 ON
    FPC1000.write_str('INITiate:IMMediate')
    print(f'Please wait for sweep; this will take {swptime} seconds')
    time.sleep(int(swptime) + 1)  # Wait for preset record time
    FPC1000.write(
        'DISPlay:TRACe1:MODE VIEW')  # Continuous measurement on trace 1 OFF
    FPC1000.query_opc()
    time.sleep(0.5)

    # Get y data (amplitude for each point)
    trace_data = FPC1000.query('Trace:DATA? TRACe1')  # Read y data of trace 1
    csv_trace_data = trace_data.split(",")  # Slice the amplitude list
    trace_len = len(csv_trace_data)  # Get number of elements of this list

    # Reconstruct x data (frequency for each point) as it can not be directly read from the instrument
    start_freq = FPC1000.query_float('FREQuency:STARt?')
    span = FPC1000.query_float('FREQuency:SPAN?')
    step_size = span / (trace_len - 1)
    global spectrumpath
    # Now write values into file
    with p.Path(spectrumpath, f'{filename}.csv').open('w') as f:
        f.write("Frequency in Hz;Power in dBm\n")  # Write the headline
        x = 0  # Set counter to 0 as list starts with 0
        while x < int(
                trace_len):  # Perform loop until all sweep points are covered
            f.write(f'{(start_freq + x * step_size):.1f}'
                    )  # Write adequate frequency information
            f.write(";")
            amp = float(csv_trace_data[x])
            f.write(f'{amp:.2f}')  # Write adequate amplitude information
            f.write("\n")
            x = x + 1
    MSO7034B.write(':SINGLE')
    time.sleep(0.2)
    for c in range(0, 1):
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
    MSO7034B.write(':RUN')

   

    dframe.to_csv(p.Path(wavepath, f'{filename}_MSO7034B.csv'),
                        index=False)
    
    

    

def screen_copy():
    inst_filename = r'"\Public\Screen Shots\screenshot.png"'
    """Prepare and perform screenshot, transfer data to local PC"""
    time.sleep(1)
    for i in range(0,6):
        FPC1000.write_str_with_opc(f'CALCulate:MARKer{i+1}:X:SLIMits:LEFT 4e6')
        FPC1000.write_str_with_opc(f'CALCulate:MARKer{i+1}:MAXimum:PEAK')
        for j in range(0,i):
            FPC1000.write_str_with_opc(f'CALCulate:MARKer{i+1}:MAXimum:NEXT')
    time.sleep(2)
    FPC1000.write('HCOPy:DEVice:LANGuage PNG')  # Select file format for screenshot (possible: PNG or JPG)
    FPC1000.write(f'MMEMory:NAME {inst_filename}')  # Define path and name for the screenshot on the instrument
    FPC1000.write('HCOPy:IMMediate')  # Perform screenshot and save it on the analyzer
    # Transfer file to PC
    FPC1000.data_chunk_size = 10000
    FPC1000.query_bin_block_to_file(f'MMEMory:DATA? {inst_filename}', f'{p.Path(spectrumpath, f"{filename}.png")}', append=False)
    FPC1000.write(f'MMEMory:DELete {inst_filename}')  # And delete it on the instrument

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

def measure_get():
    # General Measurements
    MSO7034B.write(':RUN')

    MSO7034B.write(':RUN')
    MSO7034B.write(':AUToscale CHANNEL1')
    time.sleep(1)
    MSO7034B.write(':TIMebase:MAIN:SCALe %G NS' % (50.0))
    pass

#
# -------------------------
# Main Program begins here
# -------------------------
#

try:
    
    fet, signal = prompt_user()
    ANALOG_LABELS[0] = signal
    global dir
    dir = p.Path('data', DATASET, fet, signal)
    
    os.makedirs(dir, exist_ok=True)
    com_prep()
    meas_prep()
    for swp in SWEEPS:
        do_sweep(swp)
        
    # screen_copy()
    print('Program successfully ended.')
    print('Wrote trace data into', filename)
    # print('Wrote screenshot data into', pc_filename)
    play(p.Path('sound','Success.wav'))
except BaseException as e:
    print(e)
    play(p.Path('sound','Error.wav'))
finally:
    close()


