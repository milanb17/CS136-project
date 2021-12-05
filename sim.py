from dataclasses import dataclass
from typing import Callable, List

from agent import Agent
from consumption_data import ConsumptionData
from market import Market
from market_data import MarketData


@dataclass
class BookBid:
    quantity: int
    price: float
    agent_id: int
    time: int

    def __lt__(self, other: 'BookBid') -> bool:
        return (self.price, -self.time) > (other.price, -other.time)


@dataclass
class BookAsk:
    quantity: int
    price: float
    agent_id: int
    time: int

    def __lt__(self, other: 'BookAsk') -> bool:
        return (self.price, self.time) < (other.price, other.time)


@dataclass
class Trade:
    seller_id: int
    buyer_id: int
    quantity: int
    price: float


@dataclass
class History:
    consumption_per_agent_per_round: List[List[ConsumptionData]]


class Simulator:
    def __init__(
        self,
        agents: List[Agent],
        credit_value: Callable[[int], float],
        carbon_price: Callable[[int], float],
        ren_price: Callable[[int], float],
        market: Market
    ) -> None:
        self.agents = agents
        self.credit_value = credit_value
        self.carbon_price = carbon_price
        self.ren_price = ren_price
        self.market = market

    def run(self, num_rounds: int) -> List[List[ConsumptionData]]:
        consumption_data = List[List[ConsumptionData]]

        for r in num_rounds:
            bids: List[BookBid] = []
            asks: List[BookAsk] = []

            market_data = MarketData(self.carbon_price(
                r), self.ren_price(consumption_data.renewables))
            for i, agent in enumerate(self.agents):
                agent_bids = [BookBid(b.quantity, b.price, i, r)
                              for b in agent.bid(market_data)]
                bids.extend(agent_bids)

                agent_asks = [BookAsk(b.quantity, b.price, i, r)
                              for b in agent.ask(market_data)]
                asks.extend(agent_asks)

            trades = self.market.run_round(bids, asks, market_data)
            for trade in trades:
                self.agents[trade.buyer_id].buy(trade.price, trade.quantity)
                self.agents[trade.seller_id].sell(trade.price, trade.quantity)

            consumption_data.append(
                [agent.consumption(market_data) for agent in self.agents])

        return consumption_data
