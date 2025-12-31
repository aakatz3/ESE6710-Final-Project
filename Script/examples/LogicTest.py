# NOTE: the default pyvisa import works well for Python 3.6+
# if you are working with python version lower than 3.6, use 'import visa' instead of import pyvisa as visa

import pyvisa as visa
import time
# start of Untitled

rm = visa.ResourceManager()
MSO7034B = rm.open_resource('USB0::2391::5949::MY50340240::0::INSTR')
MSO7034B.write('*RST')
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
MSO7034B.write(':DIGital0:LABel "%s"' % ('CRTL_A'))
MSO7034B.write(':DIGital1:LABel "%s"' % ('IN_A'))
MSO7034B.write(':DIGital2:LABel "%s"' % ('CRTL_B'))
MSO7034B.write(':DIGital3:LABel "%s"' % ('IN_B'))
MSO7034B.write(':DIGital4:LABel "%s"' % ('nEN'))
MSO7034B.write(':ACQuire:TYPE %s' % ('HRESolution'))
MSO7034B.write(':CHANnel1:LABel "%s"' % ('CH1'))
MSO7034B.write(':CHANnel2:LABel "%s"' % ('CH2'))
MSO7034B.write(':CHANnel3:LABel "%s"' % ('CH3'))
MSO7034B.write(':CHANnel4:LABel "%s"' % ('CH4'))
MSO7034B.write(':CHANnel1:DISPlay %d' % (1))
MSO7034B.write(':CHANnel2:DISPlay %d' % (1))
MSO7034B.write(':CHANnel3:DISPlay %d' % (1))
MSO7034B.write(':CHANnel4:DISPlay %d' % (1))
MSO7034B.write(':TRIGger:EDGE:SOURce %s' % ('EXTernal'))
MSO7034B.write(':TRIGger:EDGE:LEVel %G' % (0.5))
MSO7034B.write(':TRIGger:EDGE:SLOPe %s' % ('POSitive'))
MSO7034B.write(':TRIGger:SWEep %s' % ('NORMal'))
MSO7034B.write(':TIMebase:MAIN:SCALe %G NS' % (50.0))
MSO7034B.write(':SYSTem:PRECision %d' % (1))
MSO7034B.write(':AUToscale %s' % ('CHANNEL1'))
MSO7034B.write(':WAVeform:SOURce %s' % ('POD1'))
MSO7034B.write(':WAVeform:POINts:MODE %s' % ('MAXimum'))
MSO7034B.write(':WAVeform:FORMat %s' % ('WORD'))
MSO7034B.write(':WAVeform:UNSigned %d' % (1))
MSO7034B.write(':WAVeform:BYTeorder %s' % ('LSBFirst'))
# temp_values = MSO7034B.query_ascii_values(':WAVeform:PREamble?')
# format = int(temp_values[0])
# type = int(temp_values[1])
# points = int(temp_values[2])
# count = int(temp_values[3])
# xincrement = temp_values[4]
# xorigin = temp_values[5]
# xreference = int(temp_values[6])
# yincrement = temp_values[7]
# yorigin = temp_values[8]
# yreference = int(temp_values[9])

# binary_block_data = MSO7034B.query_binary_values(':WAVeform:DATA?','B',False)
import pandas as pd
import numpy as np
DIGITAL_LABELS = ['CRTL_A', 'IN_A', 'CRTL_B', 'IN_B', 'nEN']
r = MSO7034B.query(':waveform:preamble?')
xinc, xorg, xref, yinc, yorg, yref = [
    float(i) for i in r.split(',')[4:]
]
binary_block_data = MSO7034B.query_binary_values(':WAVeform:DATA?',
                                                datatype='H')
print(binary_block_data)
acq_data = np.array(binary_block_data)
scaled_data : np.ndarray = (acq_data - yref) * yinc + yorg

times = np.arange(0, xinc * len(acq_data), xinc)
dat_tmp = {
    "Time (s)": times[0:min(len(times), len(scaled_data))],
}
dframe = pd.DataFrame(dat_tmp)

digital = scaled_data.astype(np.int64)
import json
dframe.insert(1, json.dumps(DIGITAL_LABELS),
                digital[0:min(len(times), len(digital))])

import pathlib as p
wavepath = p.Path('.')
filename='test'

dframe.to_csv(p.Path(wavepath, f'{filename}_MSO7034B.csv'),
                        index=False)
MSO7034B.write(':DIGital5:DISPlay %d' % (0))
MSO7034B.write(':DIGital6:DISPlay %d' % (0))
MSO7034B.write(':DIGital7:DISPlay %d' % (0))

MSO7034B.close()
rm.close()

# end of Untitled
