import heapq
from typing import List

from market import Market
from bid import BookAsk, BookBid, Trade


class CallMarket(Market):
    def run_round(self, bids: List[BookBid], asks: List[BookAsk]) -> List[Trade]:
        trades: List[Trade] = []

        heapq.heapify(bids)
        heapq.heapify(asks)

        midpoint_price: float = 0.0
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

            trades.append(Trade(top_ask.agent_id,
                                top_bid.agent_id, traded_quantity, 0))
            midpoint_price = (top_bid.price + top_ask.price) / 2

        return [Trade(trade.seller_id, trade.buyer_id, trade.quantity, midpoint_price) for trade in trades]
