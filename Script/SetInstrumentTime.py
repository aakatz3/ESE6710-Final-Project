import pyvisa as visa
import datetime as dt
rm = visa.ResourceManager()

for resource in rm.list_resources():
    print('Resource: ' + resource)
    try:
        inst = rm.open_resource(resource)
        idn = inst.query('*IDN?').strip('\r').strip('\n')
        print('Trying ' + idn)
        time_now = dt.datetime.now().astimezone()
        
        inst.write(':SYSTem:TIME %d,%d,%d' % (time_now.hour, time_now.minute, time_now.second))
        inst.write(':SYSTem:DATE %d,%d,%d' % (time_now.year, time_now.month, time_now.day))
        errors = inst.query_ascii_values(':SYSTem:ERRor?', converter='s')
        print(f'{errors[0]}: {errors[1].strip('\r').strip('\n')}')
        print( inst.query_ascii_values(':SYSTem:DATE?'))
        print( inst.query_ascii_values(':SYSTem:TIME?'))
        print(f'{errors[0]}: {errors[1].strip('\r').strip('\n')}')
    except Exception as e:
        print(e)
    finally:
        if ('inst' in locals()) or ('inst' in globals()):
            inst.close()
rm.close()