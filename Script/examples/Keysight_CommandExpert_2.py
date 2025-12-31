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
MSO7034B.close()
rm.close()

# end of Untitled
