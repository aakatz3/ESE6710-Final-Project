from dataclasses import dataclass

@dataclass
class OperatingConditions:
    ROUT : float
    DUTY : float
    VIN : float
    FREQ : float

