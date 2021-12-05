from dataclasses import dataclass
from typing import List
import heapq

from agent import Agent


@dataclass
class BookBid:
    quantity: int
    price: float
    agent_id: int
    time: int

    def __lt__(self, other: 'BookBid') -> bool:
        return (self.price, -self.time) > (other.price, -other.time)


@dataclass
class BookAsk:
    quantity: int
    price: float
    agent_id: int
    time: int

    def __lt__(self, other: 'BookAsk') -> bool:
        return (self.price, self.time) < (other.price, other.time)


@dataclass
class CallTrade:
    seller_id: int
    buyer_id: int
    quantity: int


@dataclass
class CDATrade:
    seller_id: int
    buyer_id: int
    quantity: int
    price: float


class CallMarket:
    def __init__(self, agents: List[Agent]) -> None:
        self.agents = agents
        self.bids: List[BookBid] = []
        self.asks: List[BookAsk] = []
        self._time: int = 0

    @property
    def time(self) -> int:
        t = self._time
        self._time += 1
        return t

    def run(self):
        for agent in self.agents:
            bids = [BookBid(b.quantity, b.price, i, self.time)
                    for i, b in enumerate(agent.bid())]
            for bid in bids:
                heapq.heappush(self.bids, bid)

            asks = [BookAsk(b.quantity, b.price, i, self.time)
                    for i, b in enumerate(agent.ask())]
            for ask in asks:
                heapq.heappush(self.asks, ask)

        trades: List[CallTrade] = []
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
                new_bid = BookBid(
                    top_bid.quantity - traded_quantity, top_bid.price, top_bid.agent_id, top_bid.time)
                heapq.heappush(self.bids, new_bid)
            if top_ask.quantity > top_bid.quantity:
                new_ask = BookAsk(
                    top_ask.quantity - traded_quantity, top_ask.price, top_ask.agent_id, top_ask.time)
                heapq.heappush(self.asks, new_ask)

            trades.append(CallTrade(top_ask.agent_id,
                                    top_bid.agent_id, traded_quantity))
            midpoint_price = (top_bid.price + top_ask.price) / 2

        for trade in trades:
            self.agents[trade.buyer_id].buy(midpoint_price, trade.quantity)
            self.agents[trade.seller_id].sell(midpoint_price, trade.quantity)


class CDAMarket:
    def __init__(self, agents: List[Agent]) -> None:
        self.agents = agents
        self.bids: List[BookBid] = []
        self.asks: List[BookAsk] = []
        self._time: int = 0

    @property
    def time(self):
        t = self._time
        self._time += 1
        return t

    def run(self):
        for agent in self.agents:
            bids = [BookBid(b.quantity, b.price, i, self.time)
                    for i, b in enumerate(agent.bid())]
            for bid in bids:
                heapq.heappush(self.bids, bid)

            asks = [BookAsk(b.quantity, b.price, i, self.time)
                    for i, b in enumerate(agent.ask())]
            for ask in asks:
                heapq.heappush(self.asks, ask)

        trades: List[CDATrade] = []
        while len(self.bids) != 0 and len(self.asks) != 0:
            top_bid = self.bids[0]
            top_ask = self.asks[0]
            if top_bid.price < top_ask.price:
                break

            heapq.heappop(self.bids)
            heapq.heappop(self.asks)
            traded_quantity = abs(top_bid.quantity - top_ask.quantity)

            if top_bid.quantity > top_ask.quantity:
                new_bid = BookBid(
                    top_bid.quantity - traded_quantity, top_bid.price, top_bid.agent_id, top_bid.time)
                heapq.heappush(self.bids, new_bid)
            if top_ask.quantity > top_bid.quantity:
                new_ask = BookAsk(
                    top_ask.quantity - traded_quantity, top_ask.price, top_ask.agent_id, top_ask.time)
                heapq.heappush(self.asks, new_ask)

            price = top_bid.price if top_bid.time < top_ask.time else top_ask.time
            trades.append(CDATrade(top_ask.agent_id,
                                   top_bid.agent_id, traded_quantity, price))

        for trade in trades:
            self.agents[trade.buyer_id].buy(trade.price, trade.quantity)
            self.agents[trade.seller_id].sell(trade.price, trade.quantity)
