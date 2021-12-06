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
        prosection_c: float,
        prosection_normalization: float,
        fine_c: float,
        market: Market
    ) -> None:
        self.agents = agents
        self.credit_value = credit_value
        self.carbon_price = carbon_price
        self.ren_price = ren_price
        self.market = market
        self.prosecution_c = prosection_c
        self.fine_c = fine_c
        self.prosection_normalization = prosection_normalization

    def run(self, num_rounds: int) -> History:
        history: History = History([])
        total_renewables = 0
        avg_last_misreport = 0

        for r in range(num_rounds):
            bids: List[BookBid] = []
            asks: List[BookAsk] = []

            prosecution_c = self.prosecution_c / \
                (self.prosection_normalization * avg_last_misreport + 1)

            market_data = MarketData(self.carbon_price(
                r), self.ren_price(r, total_renewables), self.credit_value, r, prosecution_c, self.fine_c)

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
            truthful_util = 0
            round_consumption_data = []
            total_misreport = 0
            total_reported = 0
            for agent in self.agents:
                agent.update_util(market_data)
                agent_csm = agent.consumption(market_data)
                total_renewables += agent_csm.renewables
                this_util = agent.util(agent_csm.renewables + agent_csm.carbon)
                util += this_util
                util -= agent_csm.renewables * market_data.renew_p + \
                    agent_csm.carbon * market_data.carbon_p
                if agent.truthful:
                    truthful_util += this_util
                reported = min(agent_csm.carbon,
                               agent.num_credits * self.credit_value(r))
                total_misreport += agent_csm.carbon - reported
                total_reported += reported

                round_consumption_data.append(agent_csm)

            avg_last_misreport = total_misreport / total_reported

            round_info = RoundInfo(
                round_consumption_data, ren_price, trades, util, truthful_util)

            history.rounds.append(round_info)

        return history
