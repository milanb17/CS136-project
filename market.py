from abc import ABC, abstractmethod
from typing import List

from bid import BookAsk, BookBid, Trade


class Market(ABC):
    @abstractmethod
    def run_round(self, bids: List[BookBid], asks: List[BookAsk]) -> List[Trade]:
        pass
