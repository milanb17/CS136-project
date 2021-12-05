from abc import ABC, abstractmethod
from typing import Callable, List
from dataclasses import dataclass


@dataclass
class AgentBid:
    quantity: int
    price: float


@dataclass
class AgentAsk:
    quantity: int
    price: float


class Agent(ABC):
    def __init__(self, num_credits: int, budget: int, demand: Callable[[float], float]) -> None:
        self.num_credits = num_credits
        self.budget = budget
        self.demand = demand

    @abstractmethod
    def bid(self) -> List[AgentBid]:
        pass

    @abstractmethod
    def ask(self) -> List[AgentAsk]:
        pass

    def buy(self, price: float, quantity: int) -> None:
        self.budget -= (price * quantity)
        self.num_credits += quantity

    def sell(self, price: float, quantity: int) -> None:
        self.budget += (price * quantity)
        self.num_credits -= quantity
