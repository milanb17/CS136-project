from dataclasses import dataclass


@dataclass
class MarketData:
    carbon_price: float
    renewable_price: float
