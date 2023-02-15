import re

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
    def parse(self, category: str) -> set[Item]:
        pass

    @abstractmethod
    def parse_details(self, url_item: str) -> ResultSet | None:
        pass

    @abstractmethod
    def _parse_category(self, url_category: str) -> ResultSet | None:
        pass

    @abstractmethod
    def _parse_size(self, size: str) -> str:
        pass

    @abstractmethod
    def _parse_price(self, *args) -> float:
        pass

    @abstractmethod
    def _parse_brand_name(self, brand_name: str) -> str:
        pass

    @abstractmethod
    def _parse_item(self, title: BeautifulSoup) -> Item:
        pass


class VintedParser(Parser):
    def __init__(self):
        super().__init__()

    def parse(self, category: str) -> list[Item]:
        """
        Parses url to a set of Items
        :param category: category string
        :return: set[Item]
        """
        url_category = category_url(category)
        soup = self._parse_category(url_category)
        result = [self._parse_item(item) for item in soup]
        return result

    def parse_details(self, url: str) -> ResultSet | None:
        """
        Not ready yet
        :param url: item url is primary key in db so it's unique
        :return: Item
        """
        self.driver.get(url)
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        result = soup.find('div', class_='web_ui__ItemDetails__content')
        return result

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

    def _parse_price(self, *price) -> float | None:
        """
        Parses price from string to float
        :param price: list of strings with price
        :return: float or None
        """
        match = re.search(r"\d+", price[0]), re.search(r"\d+", price[1])

        if match[0] and match[1]:
            numbers = int(match[0].group()), int(match[1].group())
            result = float(f'{numbers[0]}.{numbers[1]}')
            return result
        else:
            return None

    def _parse_size(self, size: str) -> str:
        """
        Brings size back to the normal view
        :param size: not parsed string with size
        :return: str
        """
        try:
            result = re.search(r'rozmiar:(.*)', size).group()
        except AttributeError:
            result = None
        return result

    def _parse_brand_name(self, brand_name: str) -> str:
        """
        Brings brand name back to the normal view
        :param brand_name: not parsed string with brand name
        :return:
        """
        try:
            result = re.search(r'marka:(.*)', brand_name).group()
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
            url=title.get('href'),
            market_place='Vinted',
        )
        return result

    def __del__(self):
        self.driver.quit()


vinted = VintedParser()
