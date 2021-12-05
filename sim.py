from dataclasses import dataclass
from typing import List
import heapq

from agent import Agent


class CDAMarket:
    @dataclass
    class BookBid:
        quantity: int
        price: float
        agent_id: int
        round_num: int

        def __lt__(self, other) -> bool:
            return (self.price, -self.round_num) > (other.price, -other.round_num)

    @dataclass
    class BookAsk:
        quantity: int
        price: float
        agent_id: int
        round_num: int

        def __lt__(self, other) -> bool:
            return (self.price, self.round_num) < (other.price, other.round_num)

    @dataclass
    class Trade:
        seller_id: int
        buyer_id: int
        quantity: int

    def __init__(self, agents: List[Agent]) -> None:
        self.agents = agents
        self.bids: List[CDAMarket.BookBid] = []
        self.asks: List[CDAMarket.BookAsk] = []
        self.round = 0

    def run_round(self):
        for agent in self.agents:
            bids = [CDAMarket.BookBid(b.quantity, b.price, i, self.round)
                    for i, b in enumerate(agent.bid())]
            for bid in bids:
                heapq.heappush(self.bids, bid)

            asks = [CDAMarket.BookAsk(b.quantity, b.price, i, self.round)
                    for i, b in enumerate(agent.ask())]
            for ask in asks:
                heapq.heappush(self.asks, ask)

        trades: List[CDAMarket.Trade] = []
        midpoint_price = 0.0
        while len(self.bids) != 0 and len(self.asks) != 0:
            top_bid = self.bids[0]
            top_ask = self.asks[0]
            if top_bid.price < top_ask.price:
                break

            heapq.heappop(self.bids)
            heapq.heappop(self.asks)
            traded_quantity = abs(top_bid.quantity - top_ask.quantity)

            if top_bid.quantity > top_ask.quantity:
                new_bid = CDAMarket.BookBid(
                    top_bid.quantity - traded_quantity, top_bid.price, top_bid.agent_id, top_bid.round_num)
                heapq.heappush(self.bids, new_bid)
            if top_ask.quantity > top_bid.quantity:
                new_ask = CDAMarket.BookAsk(
                    top_ask.quantity - traded_quantity, top_ask.price, top_ask.agent_id, top_ask.round_num)
                heapq.heappush(self.asks, new_ask)

            trades.append(CDAMarket.Trade(top_ask.agent_id,
                                          top_bid.agent_id, traded_quantity))
            midpoint_price = (top_bid.price + top_ask.price) / 2

        for trade in trades:
            self.agents[trade.buyer_id].buy(midpoint_price, trade.quantity)
            self.agents[trade.seller_id].sell(midpoint_price, trade.quantity)
