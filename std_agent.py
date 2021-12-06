from dataclasses import make_dataclass
from agent import *
from consumption_data import ConsumptionData
import math
import random

discount = [0.9]


class StdAgent(Agent):

    def consumption_w_credits(self, market_data: MarketData, num_credits: int) -> ConsumptionData:
        carbon_free_q: float = self.demand_inv(market_data.carbon_p)
        credited_carbon = market_data.credit_value(
            market_data.round) * num_credits
        if carbon_free_q < credited_carbon:
            return ConsumptionData(carbon_free_q, 0)

        if credited_carbon == 0:
            return ConsumptionData(0, self.demand_inv(market_data.renew_p))

        # misreport where marginal cost of carbon is equal to that of renewable

        f = market_data.fine_c
        pr = market_data.prosecution_c
        x0 = credited_carbon
        if x0 == 0:
            x0 += 0.001
        p = market_data.renew_p - market_data.carbon_p
        # there's a plus or minus before the sqrt. I'm assuming + but we should take a look
        max_emissions = - ((pr - 1)*pr*x0*(p - f) - math.sqrt(f *
                                                              (f - p)*pr*pr*x0*x0)) / ((f - p) * pr * pr)

        def marginal_cost(x):
            return market_data.carbon_p + f * pr * (x - x0) * (
                pr * (x - x0) + 2 * x0) / (pr * (x - x0) + x0) ** 2
        d_prime = marginal_cost(max_emissions)
        demand = self.demand(max_emissions)

        if demand >= d_prime:
            #print(d_prime, market_data.renew_p)
            return ConsumptionData(max_emissions, max(self.demand_inv(market_data.renew_p) - max_emissions, 0))

        min_emissions = credited_carbon
        threshold = credited_carbon / 100
        if (threshold <= 0):
            print(threshold, credited_carbon, self.num_credits, market_data.credit_value(
                market_data.round))
            assert(False)
        while(max_emissions - min_emissions > threshold):
            to_check = (max_emissions + min_emissions) / 2
            if self.demand(to_check) >= marginal_cost(to_check):
                min_emissions = to_check
            else:
                max_emissions = to_check

            assert(max_emissions > min_emissions)
        # print("or here: ", max_emissions, min_emissions,
        #      credited_carbon, carbon_free_q)
        # print("on the margin: ", marginal_cost(
        #    min_emissions), market_data.renew_p, self.demand(min_emissions))
        return ConsumptionData(min_emissions, 0)

    def consumption(self, market_data: MarketData) -> ConsumptionData:
        return self.consumption_w_credits(market_data, self.num_credits)

    def fine_cost(self, market_data: MarketData, misreport: float):
        if misreport <= 0:
            return 0

        misreport_c = market_data.prosecution_c * \
            misreport / (self.num_credits + 0.00001)
        fine_chance = misreport_c / (misreport_c + 1)
        fine_size = market_data.fine_c * misreport
        fine = fine_chance * fine_size
        # print(misreport)
        return fine

    def total_utility(self, market_data: MarketData, num_credits: int):
        consumption: ConsumptionData = self.consumption_w_credits(
            market_data, num_credits)
        cost: float = market_data.carbon_p * consumption.carbon + \
            market_data.renew_p * consumption.renewables
        quantity: float = consumption.carbon + consumption.renewables
        return self.util(quantity) - cost - self.fine_cost(market_data, consumption.carbon - num_credits)

    def price_for(self, market_data: MarketData, q_buy: int):
        curr_util = self.total_utility(market_data, self.num_credits)
        on_buy_util = self.total_utility(market_data, self.num_credits + q_buy)
        val = (on_buy_util - curr_util) / (1 - discount[0])
        val = round(val * 1000) / 1000
        if(val * q_buy < 0):
            print(curr_util)
            print(on_buy_util)
            print(self.num_credits)
            assert(False)
        return val

    def bid(self, market_data: MarketData) -> List[AgentBid]:
        q_buy = 1
        return [AgentBid(q_buy, self.price_for(market_data, q_buy))]

    def ask(self, market_data: MarketData) -> List[AgentBid]:
        if self.num_credits == 0:
            return []
        q_sell = 1
        return [AgentAsk(q_sell, -1 * self.price_for(market_data, -1 * q_sell))]

    @classmethod
    def random_agent(cls):
        alpha = random.uniform(1.0, 5.0)

        def util(energy: float):
            return math.sqrt(energy) * alpha

        def demand(energy: float):
            return alpha / (2 * math.sqrt(energy))

        def demand_inv(cost: float):
            return alpha * alpha / (4 * cost * cost)

        return StdAgent(12, 0, util, demand, demand_inv, alpha)
