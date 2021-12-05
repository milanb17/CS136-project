from dataclasses import dataclass
from typing import Callable


@dataclass
class MarketData:
    carbon_p: float
    renew_p: float
    credit_value: Callable[[int], float]
    round: int
