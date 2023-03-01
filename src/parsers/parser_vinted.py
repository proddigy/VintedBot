"""
This module contains parser for vinted.pl
"""

import datetime
import os
import re

import urllib3
from bs4 import BeautifulSoup, ResultSet

from src.data_structures import Item
from src.parsers.helpers import vinted_category_url
from src.parsers.parser_abc import Parser
from src.requester import requester as http
from src.logger import logger
from src.parsers.helpers import timer_decorator
from src.db_client.db_client_vinted import VintedDbClient


class VintedParser(Parser):
    """
    Parser for vinted.pl
    """

    def __init__(self):
        super().__init__()
        self._db_client = VintedDbClient()
        self._reference = 'vinted'
        self._requester = http

    def get_items(self, category: str) -> list[Item, ...]:
        """
        Parses url to a list of Items
        :param category: category string
        :return: list[Item, ...] list of parsed items
        """
        api_url = vinted_category_url(category)
        search_response = http.get(api_url)
        items = search_response['items']
        unique_ids = self._db_client.get_unique_ids()
        logger.debug(f'Found {len(unique_ids)} unique ids in database')
        result = [
            Item(
                title=item['title'],
                unique_id=item['id'],
                price=item['price'],
                brand_name=item['brand_title'],
                size=item['size_title'],
                url=item['url'],
                image_path=self._get_image(item)
            ) for item in items
            if item['id'] not in unique_ids
        ]
        logger.info(f'Found {len(result)} new items')
        logger.debug(f'Starting to insert items to database')
        return result

    def _get_image(self, item: dict) -> str:
        """
        Gets image from item url
        :param item: Item object
        :param bs4_object: BeautifulSoup object containing the HTML of the item's web page
        :return str: path to the image file
        """
        # Download the image from the URL using urllib3
        http_ = urllib3.PoolManager()
        response = http_.request('GET', item['photo']['url'])
        img_data = response.data

        # Create a directory path for the item's marketplace, category, and ID
        dir_path = os.path.join(
            '../../media',
            self._reference,
            item['brand_title'],
            str(item['id']))

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        # Save the image to the file system under the directory path
        normalized_title = re.sub(r"[^\w\s]", " ", item['title'])
        filename = os.path.join(
            dir_path,
            f'{normalized_title}-{item["id"]}.jpg'
        )
        try:
            with open(filename, 'wb') as image_file:
                image_file.write(img_data)
        except Exception as e:
            logger.error(e)
            logger.error(f'Failed to save image for {item["url"]}')
        return filename

    def insert_items(self, items: list[Item, ...]) -> None:
        """
        Inserts items to database
        :param items: list of items
        :return: None
        """
        self._db_client.insert_items(items)


if __name__ == '__main__':
    logger.debug(f'Starting at {datetime.datetime.now()}')
    VintedParser().get_items('nike kurtki')
    logger.debug(f'Done at {datetime.datetime.now()}')
