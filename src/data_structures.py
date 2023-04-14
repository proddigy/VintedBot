"""
This module contains dataclasses for vinted.pl and grailed.com
"""
from dataclasses import dataclass


@dataclass
class Item:
    """
    Dataclass for parsed item
    """
    title: str = None
    unique_id: int = None
    price: float = None
    brand_name: str = None
    size: str = None
    url: str = None
    image_url: str = None
    category_id: int = None
