from dataclasses import dataclass
from collections.abc import Iterable
import numpy as np

@dataclass
class Sweep:
    Name : str
    Points : Iterable
    Unit : str = ''

@dataclass
class SweepConfig:
    Name : str
    NominalValue : np.number
    MinValue : np.number
    MaxValue : np.number
    StepValue : np.number
    Unit : str = ''
    Enabled : bool = True
    def enable(self):
        self.Enabled = True
    def disable(self):
        self.Enabled = False
    def get_sweep(self):
        if self.Enabled:
            return Sweep(Name=self.Name,
                         Points=np.unique(np.append([self.NominalValue], np.arange(self.MinValue,self.MaxValue + 1e-12, self.StepValue))),
                         Unit=self.Unit)
        else:
            return Sweep(Name=self.Name, Points=[self.NominalValue], Unit=self.Unit)