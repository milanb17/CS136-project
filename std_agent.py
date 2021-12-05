from agent import *
import math


class StdAgent(Agent):

    def total_utility(self, market_data: MarketData, num_credits: int):
        carbon_free_q: int = math.floor(
            self.marginal_utility_inv(market_data.carbon_price))
        only_carbon: bool = carbon_free_q < num_credits
        quantity: int = carbon_free_q if only_carbon else math.floor(
            self.marginal_utility_inv(market_data.renewable_price))
        cost: float = quantity * market_data.carbon_price if only_carbon else num_credits * \
            market_data.carbon_price + \
            (quantity - num_credits) * market_data.renewable_price

    def bid(self, market_data: MarketData) -> List[AgentBid]:
        return AgentBid(1, self.utility)
