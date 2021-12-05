from dataclasses import dataclass
from bid import Trade
from consumption_data import ConsumptionData
from typing import List, Any


@dataclass
class RoundInfo:
    consumption: List[ConsumptionData]
    renewable_p: float
    trades: List[Trade]
    util: float


@dataclass
class History:
    rounds: List[RoundInfo]
