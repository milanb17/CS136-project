import heapq
from typing import List

from market import Market
from sim import BookAsk, BookBid, Trade


class CDA(Market):
    def run_round(self, bids: List[BookBid], asks: List[BookAsk]) -> List[Trade]:
        trades: List[Trade] = []

        heapq.heapify(bids)
        heapq.heapify(asks)

        while len(bids) != 0 and len(asks) != 0:
            top_bid = bids[0]
            top_ask = asks[0]
            if top_bid.price < top_ask.price:
                break

            traded_quantity = min(top_bid.quantity, top_ask.quantity)
            if top_bid.quantity >= top_ask.quantity:
                top_bid.quantity -= traded_quantity
                heapq.heappop(asks)
            if top_ask.quantity >= top_bid.quantity:
                top_ask.quantity -= traded_quantity
                heapq.heappop(bids)

            price = top_bid.price if top_bid.time < top_ask.time else top_ask.price
            trades.append(Trade(top_ask.agent_id,
                                top_bid.agent_id, traded_quantity, price))

        return trades
