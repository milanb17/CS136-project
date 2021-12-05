from dataclasses import dataclass
from typing import Callable, List

from agent import Agent
from bid import BookBid, BookAsk
from consumption_data import ConsumptionData
from market import Market
from market_data import MarketData
from history import History, RoundInfo


class Simulator:
    def __init__(
        self,
        agents: List[Agent],
        credit_value: Callable[[int], float],
        carbon_price: Callable[[int], float],
        ren_price: Callable[[int, int], float],
        market: Market
    ) -> None:
        self.agents = agents
        self.credit_value = credit_value
        self.carbon_price = carbon_price
        self.ren_price = ren_price
        self.market = market

    def run(self, num_rounds: int) -> History:
        history: History = History([])
        total_renewables = 0

        for r in range(num_rounds):
            bids: List[BookBid] = []
            asks: List[BookAsk] = []

            market_data = MarketData(self.carbon_price(
                r), self.ren_price(r, total_renewables), self.credit_value, r)

            if market_data.carbon_p >= market_data.renew_p:
                break

            for i, agent in enumerate(self.agents):
                agent_bids = [BookBid(b.quantity, b.price, i, r)
                              for b in agent.bid(market_data)]
                bids.extend(agent_bids)

                agent_asks = [BookAsk(b.quantity, b.price, i, r)
                              for b in agent.ask(market_data)]
                asks.extend(agent_asks)

            trades = self.market.run_round(bids, asks)
            for trade in trades:
                self.agents[trade.buyer_id].buy(trade.price, trade.quantity)
                self.agents[trade.seller_id].sell(trade.price, trade.quantity)

            ren_price = self.ren_price(r, total_renewables)

            util = 0
            round_consumption_data = []
            for agent in self.agents:
                agent_csm = agent.consumption(market_data)
                total_renewables += agent_csm.renewables
                util += agent.util(agent_csm.renewables + agent_csm.carbon)
                util -= agent_csm.renewables * market_data.renew_p + \
                    agent_csm.carbon * market_data.carbon_p

                round_consumption_data.append(agent_csm)

            round_info = RoundInfo(
                round_consumption_data, ren_price, trades, util)

            history.rounds.append(round_info)

        return history
