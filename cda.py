import heapq
import random
from typing import List

from market import Market
from bid import BookAsk, BookBid, Trade


class CDA(Market):
    def __init__(self) -> None:
        super().__init__()
        self._time = 0

    def time(self):
        t = self._time
        self._time += 1
        return t

    def run_round(self, bids: List[BookBid], asks: List[BookAsk]) -> List[Trade]:
        bids_and_asks = bids + asks
        random.shuffle(bids_and_asks)
        for item in bids_and_asks:
            item.time = self.time()

        trades: List[Trade] = []
        simulated_bids: List[BookBid] = []
        simulated_asks: List[BookAsk] = []

        while True:
            if len(bids_and_asks) != 0:
                item = bids_and_asks.pop()
                if isinstance(item, BookBid):
                    heapq.heappush(simulated_bids, item)
                elif isinstance(item, BookAsk):
                    heapq.heappush(simulated_asks, item)

            if len(simulated_bids) == 0 or len(simulated_asks) == 0:
                if len(bids_and_asks) != 0:
                    continue
                else:
                    break

            top_bid = simulated_bids[0]
            top_ask = simulated_asks[0]
            if top_bid.price < top_ask.price:
                if len(bids_and_asks) != 0:
                    continue
                else:
                    break

            traded_quantity = min(top_bid.quantity, top_ask.quantity)
            if top_bid.quantity >= top_ask.quantity:
                top_bid.quantity -= traded_quantity
                heapq.heappop(simulated_asks)
            if top_ask.quantity >= top_bid.quantity:
                top_ask.quantity -= traded_quantity
                heapq.heappop(simulated_bids)

            price = top_bid.price if top_bid.time < top_ask.time else top_ask.price
            trades.append(Trade(top_ask.agent_id,
                                top_bid.agent_id, traded_quantity, price))

        return trades
