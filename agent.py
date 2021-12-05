from abc import ABC, abstractmethod
from typing import Callable, List
from dataclasses import dataclass
from market_data import MarketData
from consumption_data import ConsumptionData


@dataclass
class AgentBid:
    quantity: int
    price: float


@dataclass
class AgentAsk:
    quantity: int
    price: float


class Agent(ABC):
    def __init__(self, num_credits: int, budget: int, util: Callable[[float], float], demand_inv: Callable[[float], float]) -> None:
        self.num_credits = num_credits
        self.budget = budget
        self.util = util
        self.demand_inv = demand_inv
        self.discount = 0.9  # indicator of how much less we value profit in the next round

    @abstractmethod
    def bid(self, market_data: MarketData) -> List[AgentBid]:
        pass

    @abstractmethod
    def ask(self, market_data: MarketData) -> List[AgentAsk]:
        pass

    @abstractmethod
    def consumption(self, market_data: MarketData) -> ConsumptionData:
        pass

    def buy(self, price: float, quantity: int) -> None:
        self.budget -= (price * quantity)
        self.num_credits += quantity

    def sell(self, price: float, quantity: int) -> None:
        self.budget += (price * quantity)
        self.num_credits -= quantity
