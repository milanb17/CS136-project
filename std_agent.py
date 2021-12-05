from dataclasses import make_dataclass
from agent import *
from consumption_data import ConsumptionData
import math


class StdAgent(Agent):

    def consumption_w_credits(self, market_data: MarketData, num_credits: int) -> ConsumptionData:
        carbon_free_q: float = self.demand_inv(market_data.carbon_p)
        if carbon_free_q < num_credits:
            return ConsumptionData(carbon_free_q, 0)
        else:
            return ConsumptionData(num_credits, self.demand_inv(market_data.renew_p) - num_credits)

    def consumption(self, market_data: MarketData) -> ConsumptionData:
        return self.consumption_w_credits(self, market_data, self.num_credits)

    def total_utility(self, market_data: MarketData, num_credits: int):
        consumption: ConsumptionData = self.consumption_w_credits(
            self, market_data, num_credits)
        cost: float = market_data.carbon_p * consumption.carbon + \
            market_data.renew_p * consumption.renewables
        quantity: float = market_data.carbon_p + market_data.renew_p
        return self.util(quantity) - cost

    def bid(self, market_data: MarketData) -> List[AgentBid]:
        q_buy = 1
        curr_util = self.total_utility(market_data, self.num_credits)
        on_buy_util = self.total_utility(market_data, self.num_credits + q_buy)
        return AgentBid(q_buy, (on_buy_util - curr_util) * 1/(1 - self.discount))
