import re
import datetime

from abc import ABC, abstractmethod
from bs4 import BeautifulSoup, ResultSet
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from models import Item
from helpers import category_url


class Parser(ABC):
    """
    Abstract parser class
    """

    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    @abstractmethod
    def get(self, category: str) -> set[Item]:
        pass

    @abstractmethod
    def get_details(self, url_item: str) -> ResultSet | None:
        pass

    @abstractmethod
    def _parse_category(self, url_category: str) -> ResultSet | None:
        pass

    @abstractmethod
    def _parse_item(self, title: BeautifulSoup) -> Item:
        pass


class VintedParser(Parser):
    def __init__(self):
        super().__init__()
        self.category = None

    def get(self, category: str) -> list[Item, ...]:
        """
        Parses url to a list of Items
        :param category: category string
        :return: set[Item]
        """
        self.category = category
        url_category = category_url(category)
        soup = self._parse_category(url_category)
        result = [self._parse_item(item) for item in soup]
        return result

    def get_details(self, item: Item) -> Item:
        """
        Not ready yet
        :param item: this function will saturate item with details
        :return: Item
        """
        self.driver.get(item.url)
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        try:
            item.brand_name = soup.find('span', itemprop='name').text
        except AttributeError:
            item.brand_name = None

        try:
            item.condition = soup.find('div', itemprop='itemCondition').text
        except AttributeError:
            item.condition = None

        try:
            item.color = soup.find('div', itemprop='color').text
        except AttributeError:
            item.color = None

        try:
            item.date_added = datetime.datetime.fromisoformat(
                soup.find('time',
                          class_='relative'
                          ).get('datetime')
            )
        except AttributeError:
            item.date_added = None

        return item

    def _parse_category(self, url: str) -> ResultSet | None:
        """
        Parses page with saved category
        :param url: url of category
        :return: ResultSet | None
        """
        self.driver.get(url)
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        result = soup.find_all('a', class_='web_ui__ItemBox__overlay')
        return result

    @staticmethod
    def _parse_price(*price) -> float | None:
        """
        Parses price for category_parse from string to float
        this function is used in _parse_item
        :param price: list of strings with price
        :return: float or None
        """
        if len(price) == 2:
            match = re.search(r"\d+", price[0]), re.search(r"\d+", price[1])
        else:
            match = re.search(r"\d+", price[0]), None

        if match[0] and match[1]:
            numbers = int(match[0].group()), int(match[1].group())
            result = float(f'{numbers[0]}.{numbers[1]}')
            return result
        elif match[0]:
            return float(match[0].group())
        else:
            return None

    @staticmethod
    def _parse_size(size: str) -> str:
        """
        Brings size back to the normal view
        this function is used in _parse_item
        :param size: not parsed string with size
        :return: str
        """
        try:
            result = re.search(r'rozmiar:\s*(.*)', size).group(1)
        except AttributeError:
            result = None
        return result

    @staticmethod
    def _parse_brand_name(brand_name: str) -> str:
        """
        Brings brand name back to the normal view
        this function is used in _parse_item
        :param brand_name: not parsed string with brand name
        :return: brand name or None
        """
        try:
            result = re.search(r'marka:\s*(.*)', brand_name).group(1)
        except AttributeError:
            result = None
        return result

    def _parse_item(self, title: BeautifulSoup) -> Item:
        """
        Parses soup iter obj to Item
        :param title: BeautifulSoup iter obj that contains Item info
        :return: Item
        """
        list_title = title.get('title').strip().split(',')
        result = Item(
            name=list_title[0],
            price=self._parse_price(list_title[1], list_title[2]),
            brand_name=self._parse_brand_name(list_title[3]),
            size=self._parse_size(list_title[4]),
            category=self.category,
            url=title.get('href'),
            market_place='vinted',
        )
        return result

    def __del__(self):
        self.driver.quit()
