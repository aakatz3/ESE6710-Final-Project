from math import pi
from operating_conditions import OperatingConditions
from sweep import Sweep, SweepConfig
import jsonpickle

conditions = OperatingConditions(ROUT=50 * pi **2 / 8, DUTY=0.32, VIN=25, FREQ=6.78e6)

with open('OperatingConditions.json', 'w') as f:
    f.write(jsonpickle.encode(conditions))

with open("OperatingConditions.json", "r+") as f:
    written_instance = f.read()
    decoded_instance = jsonpickle.decode(written_instance)
print(decoded_instance)


SWEEP_CONFIGS = [
    SweepConfig('VIN', conditions.VIN, MinValue=18, MaxValue=28, StepValue=0.5, Unit='V'),
    SweepConfig('ROUT', conditions.ROUT, MinValue=50, MaxValue=75, StepValue=0.5),
    SweepConfig('FREQ', conditions.FREQ, MinValue=6.7e6, MaxValue=6.9e6, StepValue=10e3, Unit='Hz'),
    SweepConfig('DUTY', conditions.DUTY, MinValue=0.3, MaxValue=0.4, StepValue=0.01)
]

with open('Sweeps.json', 'w') as f:
    f.write(jsonpickle.encode(SWEEP_CONFIGS))

with open("Sweeps.json", "r+") as f:
    written_instance = f.read()
    decoded_instance = jsonpickle.decode(written_instance)
print(decoded_instance)
SWEEPS = [swp.get_sweep() for swp in decoded_instance]
print(SWEEPS)