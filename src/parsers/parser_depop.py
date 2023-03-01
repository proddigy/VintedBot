"""
Depop parser
Not ready yet
"""
import datetime
import os
import re

import urllib3
from bs4 import BeautifulSoup, ResultSet

from src.data_structures import Item, DetailedItem
from src.parsers.helpers import vinted_category_url
from src.parsers.parser_abc import Parser
from src.parsers.exceptions import InvalidPrice


class DepopParser(Parser):
    """
    Parser for depop.com
    """

    def get(self, category: str) -> list[Item, ...]:
        pass

    def get_details(self, item: Item) -> Item:
        pass

    def _parse_category(self, url_category: str) -> ResultSet | None:
        pass

    def _parse_item(self, bf4_object: BeautifulSoup) -> Item:
        pass
