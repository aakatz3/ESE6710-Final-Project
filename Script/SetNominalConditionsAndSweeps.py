from math import pi
from operating_conditions import OperatingConditions
from sweep import Sweep
import jsonpickle

conditions = OperatingConditions(ROUT=50 * pi **2 / 8, DUTY=0.32, VIN=25, FREQ=6.78e6)

with open('OperatingConditions.json', 'w') as f:
    f.write(jsonpickle.encode(conditions))

with open("OperatingConditions.json", "r+") as f:
    written_instance = f.read()
    decoded_instance = jsonpickle.decode(written_instance)
print(decoded_instance)



# VINS = np.unique(np.append(VIN_STD, np.arange(18,28.01, 0.5)))
# ROUTS = np.unique(np.append(ROUT_STD, np.arange(50,75,0.5)))
# FREQS = np.unique(np.append(FREQ_STD, np.arange(6.0e6,7.501e6,0.1e6)))
# DUTYS = np.unique(np.append(DUTY_STD, np.arange(0.3,0.4,0.01)))

# SWEEPS = [
#         Sweep('VIN', VINS, 'V'),
#         Sweep('ROUT', ROUTS, 'R'),
#         Sweep('FREQ', FREQS, 'Hz'),
#         Sweep('DUTY', DUTYS),
#         None
#     ]

