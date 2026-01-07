import numpy as np
import jsonpickle
from operating_conditions import OperatingConditions
from sweep import Sweep
# Standard parameters
with open('OperatingConditions.json', 'r+') as f:
    NOMINAL = jsonpickle.decode(f.read())



VINS = np.unique(np.append(NOMINAL.VIN, np.arange(18,28.01, 0.5)))
ROUTS = np.unique(np.append(NOMINAL.ROUT, np.arange(50,75,0.5)))
FREQS = np.unique(np.append(NOMINAL.FREQ, np.arange(6.0e6,7.501e6,0.1e6)))
DUTYS = np.unique(np.append(NOMINAL.DUTY, np.arange(0.3,0.4,0.01)))

SWEEPS = [
        Sweep('VIN', VINS, 'V'),
        Sweep('ROUT', ROUTS, 'R'),
        Sweep('FREQ', FREQS, 'Hz'),
        Sweep('DUTY', DUTYS),
        None
    ]

with open('info.json', 'w') as f:
    f.write(jsonpickle.encode( (NOMINAL, SWEEPS) ))

