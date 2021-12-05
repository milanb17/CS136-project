from dataclasses import dataclass


@dataclass
class ConsumptionData:
    carbon: float
    renewables: float

    def __add__(self, other: 'ConsumptionData') -> 'ConsumptionData':
        return ConsumptionData(self.carbon + other.carbon, self.renewables + other.renewables)
