from dataclasses import dataclass
from collections.abc import Iterable

@dataclass
class Sweep:
    Name : str
    Points : Iterable
    Unit : str = ''
