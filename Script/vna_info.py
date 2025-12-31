import pathlib as p
import datetime as dtime
import pyvisa as visa
import time
import datetime as dt
import os

DATASET = 'VNA'
dir = p.Path(f'data', DATASET)
sspath = p.Path(dir, 'screenshot')
os.makedirs(dir, exist_ok=True)
os.makedirs(sspath, exist_ok=True)


rm = visa.ResourceManager()
E5063A : visa.resources.USBInstrument = rm.open_resource('USB0::0x2A8D::0x5D01::MY54100949::0::INSTR')
E5063A.timeout = 30000


log = p.Path(dir, 'instruments.log').open('w', encoding='cp1252')
log.write('Timestamp: ' + dtime.datetime.now().astimezone().isoformat() + os.linesep)
print('Instruments Utilized:')
try:
    E5063A.write('*CLS')
    try:
        timenow = dt.datetime.now().astimezone()
        E5063A.write(':SYSTem:TIME %d,%d,%d' % (timenow.hour, timenow.minute, timenow.second))
        E5063A.write(':SYSTem:DATE %d,%d,%d' % (timenow.year, timenow.month, timenow.day))
        errors = E5063A.query_ascii_values(':SYSTem:ERRor?', converter='s')
        # print(f'{errors[0]}: {errors[1].strip('\r').strip('\n')}')
        # print( E5063A.query_ascii_values(':SYSTem:DATE?'))
        # print( E5063A.query_ascii_values(':SYSTem:TIME?'))
        # print(f'{errors[0]}: {errors[1].strip('\r').strip('\n')}')
    except BaseException:
        pass
    time.sleep(1)
    idn = E5063A.query('*IDN?').strip('\r').strip('\n')
    opt = E5063A.query('*OPT?').strip('\r').strip('\n')
    time.sleep(0.5)
    E5063A.write(':SENSe1:CORRection:COLLect:ECAL:SOLT2 1,2')
    time.sleep(3)
    E5063A.write(':SENSe1:CORRection:COLLect:ECAL:INFormation?')
    ecal_info = bytearray(E5063A.read_raw()).decode(encoding='cp1252',errors='ignore').strip('\r').strip('\n').strip('"')
    log.write(ecal_info + os.linesep)
    log.write(os.linesep)
    log.write('Options: ' + opt + os.linesep)
    print(' - ' + idn)
    print('   - '+ ecal_info)
    print('   - Options: '+ opt)

    E5063A.query('SYST:ERR?')
except BaseException as e:
    print(e)


E5063A.write(':HCOPy:SDUMp:DATA:FORMat %s' % ('PNG'))
img = E5063A.query_binary_values(':HCOPy:SDUMp:DATA:IMMediate?','B',False)

with open(p.Path(sspath, f'E5063A.png'), 'bw') as f:
    imagebytes = bytearray(img)
    f.write(imagebytes)

# E5063A.write(":SYST:POFF")
E5063A.close()
rm.close()

# end of Untitled

