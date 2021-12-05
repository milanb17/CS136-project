from dataclasses import make_dataclass
from agent import *
from consumption_data import ConsumptionData
import math
import random

DISCOUNT = 0.9


class StdAgent(Agent):

    def consumption_w_credits(self, market_data: MarketData, num_credits: int) -> ConsumptionData:
        carbon_free_q: float = self.demand_inv(market_data.carbon_p)
        credited_carbon = market_data.credit_value(
            market_data.round) * num_credits
        if carbon_free_q < credited_carbon:
            return ConsumptionData(carbon_free_q, 0)
        else:
            return ConsumptionData(credited_carbon, max(self.demand_inv(market_data.renew_p) - credited_carbon, 0))

    def consumption(self, market_data: MarketData) -> ConsumptionData:
        return self.consumption_w_credits(self, market_data, self.num_credits)

    def total_utility(self, market_data: MarketData, num_credits: int):
        consumption: ConsumptionData = self.consumption_w_credits(
            market_data, num_credits)
        cost: float = market_data.carbon_p * consumption.carbon + \
            market_data.renew_p * consumption.renewables
        quantity: float = consumption.carbon + consumption.renewables
        return self.util(quantity) - cost

    def price_for(self, market_data: MarketData, q_buy: int):
        curr_util = self.total_utility(market_data, self.num_credits)
        on_buy_util = self.total_utility(market_data, self.num_credits + q_buy)
        return (on_buy_util - curr_util) / (1 - DISCOUNT)

    def bid(self, market_data: MarketData) -> List[AgentBid]:
        q_buy = 1
        return AgentBid(q_buy, self.price_for(market_data, q_buy))

    def ask(self, market_data: MarketData) -> List[AgentBid]:
        q_sell = 1
        return AgentAsk(q_sell, -1 * self.price_for(market_data, -1 * q_sell))

    @classmethod
    def random_agent(cls):
        alpha = random.uniform(1.0, 5.0)

        def util(energy: float):
            return math.sqrt(energy) * alpha

        def demand_inv(cost: float):
            return alpha * alpha / (4 * cost * cost)

        return StdAgent(12, 100000, util, demand_inv)
