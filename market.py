from abc import ABC, abstractmethod
from typing import List

from call_market import BookAsk, BookBid
from sim import Trade


class Market(ABC):
    @abstractmethod
    def run_round(self, bids: List[BookBid], asks: List[BookAsk]) -> List[Trade]:
        pass
