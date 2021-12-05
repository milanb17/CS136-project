# Do some command line parsing at some point

from std_agent import StdAgent
from sim import Simulator
from call_market import CallMarket


def zero(_x):
    return 0


def main():
    agents = [StdAgent(0, 0, zero, zero, 0.0) for _ in range(10)]
    call_market = CallMarket()
    simulator = Simulator(agents, zero, zero, zero, call_market)

    history = simulator.run(10)
    print(history)


if __name__ == "__main__":
    main()
