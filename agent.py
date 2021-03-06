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
    def __init__(self, num_credits: int, budget: int, util: Callable[[float], float], demand: Callable[[float], float], demand_inv: Callable[[float], float], alpha: float, truthful: bool) -> None:
        self.num_credits = num_credits
        self.budget = budget
        self.util = util
        self.demand = demand
        self.demand_inv = demand_inv
        self.alpha = alpha
        self.truthful = truthful

    @abstractmethod
    def bid(self, market_data: MarketData) -> List[AgentBid]:
        pass

    @abstractmethod
    def ask(self, market_data: MarketData) -> List[AgentAsk]:
        pass

    @abstractmethod
    def consumption(self, market_data: MarketData) -> ConsumptionData:
        pass

    @abstractmethod
    def update_util(self, market_data: MarketData):
        pass

    def buy(self, price: float, quantity: int) -> None:
        self.budget -= (price * quantity)
        self.num_credits += quantity

    def sell(self, price: float, quantity: int) -> None:
        self.budget += (price * quantity)
        self.num_credits -= quantity
