import datetime
from dataclasses import dataclass


@dataclass
class Item:
    name: str = None
    price: float = None
    brand_name: str = None
    size: str = None
    color: str = None
    category: str = None
    description: str = None
    condition: str = None
    shipping: str = None
    seller: str = None
    url: str = None
    market_place: str = None
    date_added: datetime.datetime = None

    def __str__(self):
        return f'{self.name} - {self.price} - {self.size}'
