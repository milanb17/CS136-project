from agent import *
import math


class StdAgent(Agent):

    def total_utility(self, market_data: MarketData, num_credits: int):
        carbon_free_q: int = math.floor(
            self.demand_inv(market_data.carbon_p))
        only_carbon: bool = carbon_free_q < num_credits
        quantity: int = carbon_free_q if only_carbon else math.floor(
            self.demand_inv(market_data.renew_p))
        cost: float = quantity * market_data.carbon_p if only_carbon else num_credits * \
            market_data.carbon_p + \
            (quantity - num_credits) * market_data.renew_p
        return self.util(quantity) - cost

    def bid(self, market_data: MarketData) -> List[AgentBid]:
        q_buy = 1
        curr_util = self.total_utility(market_data, self.num_credits)
        on_buy_util = self.total_utility(market_data, self.num_credits + q_buy)
        return AgentBid(q_buy, on_buy_util - curr_util)
