"""
This module contains dataclasses for vinted.pl and grailed.com
"""

import datetime
from dataclasses import dataclass
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@dataclass
class Item:
    """
    Dataclass for parsed item
    """
    name: str = None
    price: float = None
    brand_name: str = None
    size: str = None
    category: str = None
    url: str = None
    market_place: str = None


@dataclass
class DetailedItem(Item):
    """
    Dataclass for detailed item
    """
    color: str = None
    condition: str = None
    date_added: datetime.datetime = None
