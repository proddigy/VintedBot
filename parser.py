"""
This module contains parsers for vinted.pl and grailed.com
"""
import datetime
import re
import logging
import os
import sys
import urllib3
import urllib.request
from PIL import Image
from abc import ABC, abstractmethod

from bs4 import BeautifulSoup, ResultSet
from selenium import webdriver
from models import Item, DetailedItem
from helpers import vinted_category_url, grailed_category_url

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class Parser(ABC):
    """
    Abstract parser class
    """

    def __init__(self):
        self._driver = webdriver.Chrome()
        self._category = None

    @abstractmethod
    def get(self, category: str) -> list[Item, ...]:
        """
        Parses url to a list of Items
        :param category: category string (e.g. 'polo')
        :return: list[Item, ...] list of parsed items
        """
        return []

    @abstractmethod
    def get_details(self, item: Item) -> DetailedItem:
        """
        Gets details of parsed_item
        :param item: item with default values
        :return: Item dataclass
        """
        return DetailedItem()

    @abstractmethod
    def _parse_category(self, url_category: str) -> ResultSet | None:
        """
        Protected method for parsing category, returns bf4 ResultSet
        :param url_category:
        :return: bf4 ResultSet
        """
        return None

    @abstractmethod
    def _parse_item(self, bf4_object: BeautifulSoup) -> Item:
        """
        Protected method for parsing item, returns Item dataclass
        :param bf4_object: contains data about item
        :return: Item dataclass
        """
        return Item()

    def __del__(self):
        """
        Closes selenium driver
        :return: None
        """
        self._driver.close()


class VintedParser(Parser):
    """
    Parser for vinted.pl
    """

    def get(self, category: str) -> list[Item, ...]:
        """
        Parses url to a list of Items
        :param category: category string
        :return: set[Item]
        """
        self._category = category
        url_category = vinted_category_url(category)
        soup = self._parse_category(url_category)
        result = [self._parse_item(item) for item in soup]
        return result

    def get_details(self, item: Item) -> DetailedItem:
        """
        Not ready yet
        :param item: this function will saturate item with details
        :return: Item
        """
        item = DetailedItem(**item.__dict__)
        self._driver.get(item.url)
        soup = BeautifulSoup(self._driver.page_source, 'lxml')

        try:
            item.brand_name = soup.find('span', itemprop='name').text
        except AttributeError:
            item.brand_name = None

        try:
            item.condition = self._parse_condition(soup.find(
                'div',
                itemprop='itemCondition').text
                                                   )
        except AttributeError:
            item.condition = None

        try:
            item.color = soup.find('div', itemprop='color').text
        except AttributeError:
            item.color = None

        try:
            item.date_added = datetime.datetime.fromisoformat(
                soup.find(
                    'time',
                    class_='relative'
                ).get('datetime')
            )
        except AttributeError:
            item.date_added = None

        self._get_image(soup, item)

        return item

    def _parse_category(self, url_category: str) -> ResultSet | None:
        """
        Parses page with saved category
        :param url_category: url of category
        :return: ResultSet | None
        """
        self._driver.get(url_category)
        soup = BeautifulSoup(self._driver.page_source, 'lxml')
        result = soup.find_all('a', class_='web_ui__ItemBox__overlay')
        return result

    def _parse_item(self, bf4_object: BeautifulSoup) -> Item:
        """
        Parses soup iter obj to Item
        :param bf4_object: BeautifulSoup iter obj that contains Item info
        :return: Item without details
        """
        list_title = bf4_object.get('title').strip().split(',')
        if len(list_title) == 6:
            list_title.remove(list_title[1])

        result = Item(
            name=list_title[0],
            price=self._parse_price(list_title[1], list_title[2]),
            brand_name=self._parse_brand_name(list_title[3]),
            size=self._parse_size(list_title[4]),
            category=self._category,
            url=bf4_object.get('href'),
            market_place='vinted',
        )

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
            raise ValueError('Price should be a list of 2 elements')

        if match[0] and match[1]:
            numbers = int(match[0].group(0)), int(match[1].group(0))
            result = float(f'{numbers[0]}.{numbers[1]}')
            return result
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
    def _parse_brand_name(brand_name: str) -> str | None:
        """
        Brings brand name back to the normal view
        this function is used in _parse_item
        :param brand_name: not parsed string with brand name
        :return: brand name or None
        """
        try:
            result = re.search(r'marka:\s*(.*)', brand_name).group(1)
            if result:
                return result
        except AttributeError:
            pass
        return None

    @staticmethod
    def _parse_condition(condition: str) -> str | None:
        condition = condition.replace('\n', '').strip()
        condition = re.sub(r'\s+', ' ', condition)
        condition = re.match(r'(.*)\bCondition information\b', condition)
        if condition:
            return condition.group(1).strip()
        return None

    @staticmethod
    def _get_image(bs4_object: BeautifulSoup, item: DetailedItem) -> None:
        """
        Gets image from item url
        :param item: DetailedItem object containing item details
        :param bs4_object: BeautifulSoup object containing the HTML of the item's web page
        """
        # Extract the image URL from the HTML using bs4
        img_tag = bs4_object.find('img', itemprop='image')
        if not img_tag:
            return
        img_url = img_tag.get('data-src')

        # Download the image from the URL using urllib3
        http = urllib3.PoolManager()
        response = http.request('GET', img_url)
        img_data = response.data

        # Create a directory path for the item's market place, category, and ID
        dir_path = os.path.join('media', item.market_place, item.category, item.name.strip())
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        # Save the image to the file system under the directory path
        filename = os.path.join(
            dir_path,
            f'{item.name}-{item.date_added.date()}.jpg'
        )
        with open(filename, 'wb') as f:
            f.write(img_data)
        return


class GrailedParser(Parser):
    """
    Parser for grailed.com
    """

    def get(self, category: str) -> list[Item, ...]:
        """
        Parses url to a list of Items
        :param category:
        :return: list[Item, ...]
        """
        self._category = category
        url_category = grailed_category_url(category, self._driver)
        soup = self._parse_category(url_category)
        result = [self._parse_item(item) for item in soup]

        return result

    def get_details(self, item: Item) -> Item:
        pass

    def _parse_category(self, url_category: str) -> ResultSet | None:
        """
        Parses page with input category
        :param url_category:
        :return: ResultSet | None
        """

        self._driver.get(url_category)
        soup = BeautifulSoup(self._driver.page_source, 'lxml')
        result = soup.find_all('div', class_='feed-item')

        logging.warning('Parsed %s items from %s category', len(result), self._category)
        logging.shutdown()
        return result

    def _parse_item(self, bf4_object: BeautifulSoup) -> Item:
        """
        Parses soup iter obj to Item
        :param bf4_object: BeautifulSoup iter obj that contains Item info
        :return: Item without details
        """
        result = Item(
            name=bf4_object.find('div', class_='title').text.strip(),
            price=self._parse_price(bf4_object.find('div', class_='price').text),
            brand_name=self._parse_brand_name(bf4_object.find('div', class_='brand').text),
            size=self._parse_size(bf4_object.find('div', class_='size').text),
            category=self._category,
            url=bf4_object.find('a', class_='link').get('href'),
            market_place='grailed',
        )

        return result


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
