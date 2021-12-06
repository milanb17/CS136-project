import heapq
import random
from typing import List

from market import Market
from bid import BookAsk, BookBid, Trade


class CDA(Market):
    def run_round(self, bids: List[BookBid], asks: List[BookAsk]) -> List[Trade]:
        random.shuffle(bids)
        random.shuffle(asks)

        trades: List[Trade] = []
        simulated_bids: List[BookBid] = []
        simulated_asks: List[BookAsk] = []

        while True:
            if len(bids) != 0:
                heapq.heappush(simulated_bids, bids.pop())
            if len(asks) != 0:
                heapq.heappush(simulated_asks, asks.pop())

            top_bid = simulated_bids[0]
            top_ask = simulated_asks[0]
            if top_bid.price < top_ask.price:
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
