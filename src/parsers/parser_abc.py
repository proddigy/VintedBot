"""
This module contains parsers for vinted.pl and grailed.com
"""

from abc import ABC, abstractmethod

from src.data_structures import Item


class Parser(ABC):
    """
    Abstract parser class
    """
    __instance = None

    def __init__(self):
        self._reference = None
        self._db_client = None

    @abstractmethod
    def get_items(self, category: str) -> list[Item, ...]:
        """
        Parses url to a list of Items
        :param category: category string (e.g. 'polo')
        :return: list[Item, ...] list of parsed items
        """
        return []

    @classmethod
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
