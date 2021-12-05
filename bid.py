from dataclasses import dataclass


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
class Trade:
    seller_id: int
    buyer_id: int
    quantity: int
    price: float
