# Do some command line parsing at some point

from std_agent import StdAgent
from sim import Simulator
from call_market import CallMarket


def zero(_x):
    return 0


def carbon_p(round):
    return 0.06


def renewable_p(round, total_bought):
    return 0.2 - round * 0.01 - total_bought * 0.001


def credit_value(round):
    return 1 - 0.0025 * round


def main():
    agents = [StdAgent.random_agent() for _ in range(10)]
    call_market = CallMarket()
    simulator = Simulator(agents, credit_value, carbon_p,
                          renewable_p, call_market)

    history = simulator.run(10)
    print(history)


if __name__ == "__main__":
    main()
