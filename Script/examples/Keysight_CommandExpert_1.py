# NOTE: the default pyvisa import works well for Python 3.6+
# if you are working with python version lower than 3.6, use 'import visa' instead of import pyvisa as visa

import pyvisa as visa
import time
# start of Keysight_Setup

rm = visa.ResourceManager()
v33510B = rm.open_resource('%USB0::0x0957::0x2607::MY62003856::0::INSTR')
v34401A = rm.open_resource('%ASRL13::INSTR')
E3631A = rm.open_resource('%ASRL12::INSTR')
E3634A = rm.open_resource('%ASRL14::INSTR')
EDU34450A = rm.open_resource('USB0::0x2A8D::0x8E01::CN62180094::0::INSTR')
EL34143A = rm.open_resource('%USB0::0x2A8D::0x3802::MY61001508::0::INSTR')
MSO7034B = rm.open_resource('%USB0::2391::5949::MY50340240::0::INSTR')
v33521A = rm.open_resource('%USB0::2391::5639::MY50000944::0::INSTR')
string = v33510B.query('*IDN?')
v33510B.write('*RST')
v33510B.write(':DISPlay:FOCus %s' % ('CH1'))
v33510B.write(':OUTPut1:LOAD %s' % ('INFinity'))
v33521A.write(':SOURce1:PHASe:ADJust %G' % (180.0))
v33510B.write(':OUTPut2:LOAD %s' % ('INFinity'))
v33510B.write(':DISPlay:VIEW %s' % ('DUAL'))
v33510B.write(':DISPlay:FOCus %s' % ('CH2'))
v33510B.write(':DISPlay:UNIT:VOLTage %s' % ('HIGHlow'))
v33510B.write(':DISPlay:FOCus %s' % ('CH1'))
v33510B.write(':DISPlay:UNIT:VOLTage %s' % ('HIGHlow'))
v33510B.write(':SOURce1:FUNCtion %s' % ('SQUare'))
v33510B.write(':SOURce1:FUNCtion:SQUare:DCYCle %G' % (30.0))
v33510B.write(':SOURce1:VOLTage:HIGH %G' % (5.0))
v33510B.write(':SOURce1:VOLTage:LOW %G' % (0.0))
v33510B.write(':SOURce2:VOLTage:HIGH %G' % (5.0))
v33510B.write(':SOURce2:VOLTage:LOW %G' % (0.0))
v33510B.write(':SOURce1:FREQuency %G MHZ' % (6.78))
v33510B.write(':SOURce2:FREQuency %G MHZ' % (6.78))
v33510B.write(':SOURce:PHASe:SYNChronize')
v33510B.write(':OUTPut1 %d' % (1))
v33510B.write(':OUTPut2 %d' % (1))
v33510B.write(':SOURce:FREQuency:COUPle:RATio %G' % (1.0))
v33510B.write(':SOURce:FREQuency:COUPle:MODE %s' % ('RATio'))
v33510B.write(':SOURce:FREQuency:COUPle:STATe %d' % (1))
EL34143A.write('*RST')
EL34143A.write(':SOURce:VOLTage:SENSe:SOURce %s' % ('EXTernal'))
EL34143A.write(':SOURce:MODE %s' % ('RESistance'))
EL34143A.write(':SOURce:RESistance:LEVel:IMMediate:AMPLitude %G' % (63.525))
EL34143A.write(':OUTPut:STATe %d' % (1))
E3631A.write(':SYSTem:REMote')
E3631A.write(':INSTrument:SELect %s' % ('P6V'))
E3631A.write(':SOURce:CURRent:LEVel:IMMediate:AMPLitude %G' % (0.5))
E3631A.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G' % (5.0))
E3631A.write(':OUTPut:STATe %d' % (1))
temp_values = E3631A.query_ascii_values(':MEASure:VOLTage:DC? %s' % ('P6V'))
voltage = temp_values[0]

E3634A.write('*RST')
E3634A.write(':SOURce:VOLTage:RANGe %s' % ('LOW'))
E3634A.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G' % (25.0))
E3634A.write(':SOURce:CURRent:LEVel:IMMediate:AMPLitude %G' % (2.2))
E3634A.write(':OUTPut:STATe %d' % (1))
temp_values = E3634A.query_ascii_values(':MEASure:VOLTage:DC?')
dc = temp_values[0]

EDU34450A.write('*RST')
EDU34450A.write(':SENSe:PRIMary:CURRent:DC:RANGe %s' % ('MAX'))
EDU34450A.write(':SENSe:PRIMary:CURRent:DC:RESolution %s' % ('MIN'))
EDU34450A.write(':FORMat:OUTPut %d' % (1))
temp_values = EDU34450A.query_ascii_values(':MEASure:PRIMary:CURRent:DC?')
dcCurrent = temp_values[0]

v34401A.write('*RST')
# measure
#
temp_values = v34401A.query_ascii_values(':MEASure:VOLTage:DC? %s,%s' % ('DEF', 'MIN'))
measurement = temp_values[0]

temp_values = EDU34450A.query_ascii_values(':MEASure:PRIMary:CURRent:DC?')
dcCurrent1 = temp_values[0]

temp_values = EDU34450A.query_ascii_values(':MEASure:PRIMary:CURRent:DC? %G,%s' % (3.0, 'MIN'))
dcCurrent2 = temp_values[0]

temp_values = EL34143A.query_ascii_values(':MEASure:SCALar:CURRent:ACDC?')
current = temp_values[0]

temp_values = EL34143A.query_ascii_values(':MEASure:SCALar:POWer:DC?')
power = temp_values[0]

temp_values = EL34143A.query_ascii_values(':MEASure:SCALar:VOLTage:ACDC?')
voltage1 = temp_values[0]

v33510B.close()
v34401A.close()
E3631A.close()
E3634A.close()
EDU34450A.close()
EL34143A.close()
MSO7034B.close()
v33521A.close()
rm.close()

# end of Keysight_Setup
