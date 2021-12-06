# Do some command line parsing at some point

from std_agent import StdAgent
from sim import Simulator
from call_market import CallMarket
import csv


def zero(_x):
    return 0


def carbon_p(_round):
    return 0.2  # keep constant


innovation_c = [0.001]
innovation_bump_c = [0.000015]


def renewable_p(round, total_bought):
    return 0.35 - round * innovation_c[0] - total_bought * innovation_bump_c[0]


def credit_value(round):
    return max(1 - 0.01 * round, 0.5)


prosecution_c = 3
prosection_normalization = 10.0
# prosecution chances = prosecution_c * misreport% / (prosecution_c * misreport% + 1)
fine_c = 0.45
# fine = misreport * fine_c
truthful_per = 0.0


def run():
    agents = [StdAgent.random_agent(truthful_per) for i in range(10)]
    call_market = CallMarket()
    simulator = Simulator(agents, credit_value, carbon_p,
                          renewable_p, prosecution_c, prosection_normalization, fine_c, call_market)

    max_len = 50
    history = simulator.run(max_len)
    util = 0
    total_carbon = 0
    for round in history.rounds:
        util += round.util
        for csm in round.consumption:
            total_carbon += csm.carbon
    truthful_util = 0
    lying_util = 0
    total_truthful = 0
    for agent in agents:
        if agent.truthful:
            total_truthful += 1
            truthful_util += agent.total_util + agent.budget
        else:
            lying_util += agent.total_util + agent.budget
    max_round_util = 0
    for agent in agents:
        amount = agent.demand_inv(carbon_p(0))
        max_round_util += agent.util(amount) - amount * carbon_p(0)
    max_util = max_round_util * len(history.rounds)
    completion = len(history.rounds) / max_len
    util_per = util / max_util * completion + (1 - completion)
    lying_util_avg = truthful_util / total_truthful if (len(
        agents) - total_truthful) == 0 else lying_util / (len(agents) - total_truthful)
    truthful_util_avg = truthful_util / \
        total_truthful if total_truthful > 0 else lying_util / \
        (len(agents) - total_truthful)
    return util / max_util, util_per, total_carbon, len(history.rounds), truthful_util_avg, lying_util_avg
    # return [agent.total_util + agent.budget for agent in agents]


def multi_run(num_rounds):
    results = [run() for _ in range(num_rounds)]
    total = results[0]
    for result in results[1:]:
        total = [sum(a) for a in zip(total, result)]
    return [a / num_rounds for a in total]


def main():
    global truthful_per
    results = []
    results.append(["", "eff%", "total eff%", "total carbon", "num rounds"])
    for i in range(10):
        truthful_per = i / 10
        result = [truthful_per]
        results.append(result + multi_run(300))
    return results


if __name__ == "__main__":
    res = main()
    print("done")
    print(res)
    with open("total_truthful.csv", "w+") as my_csv:
        csvWriter = csv.writer(my_csv, delimiter=',')
        csvWriter.writerows(res)
    print("Result: ")
    print(res)
