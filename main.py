# Do some command line parsing at some point

from std_agent import StdAgent
from sim import Simulator
from call_market import CallMarket


def zero(_x):
    return 0


def carbon_p(round):
    return 0.2  # keep constant


def renewable_p(round, total_bought):
    return 0.35 - round * 0.001 - total_bought * 0.000015


def credit_value(round):
    return 1 - 0.01 * round


def run():
    agents = [StdAgent.random_agent() for _ in range(10)]
    call_market = CallMarket()
    simulator = Simulator(agents, credit_value, carbon_p,
                          renewable_p, call_market)

    max_len = 50
    history = simulator.run(max_len)
    util = 0
    total_carbon = 0
    for round in history.rounds:
        util += round.util
        for csm in round.consumption:
            total_carbon += csm.carbon
    max_round_util = 0
    for agent in agents:
        amount = agent.demand_inv(carbon_p(0))
        max_round_util += agent.util(amount) - amount * carbon_p(0)
    max_util = max_round_util * len(history.rounds)
    completion = len(history.rounds) / max_len
    util_per = util / max_util * completion + (1 - completion)
    return util / max_util, util_per, total_carbon, len(history.rounds)


def main():
    num_rounds = 100
    results = [run() for _ in range(num_rounds)]
    total = results[0]
    for result in results[1:]:
        total = [sum(a) for a in zip(total, result)]
    return [a / num_rounds for a in total]


if __name__ == "__main__":
    res = main()
    print("Result: ")
    print(res)
