"""
This module contains parser for vinted.pl
"""

import os
import re
import urllib3

from typing import List
from src.data_structures import Item
from src.db_client.db_client_vinted import VintedDbClient
from src.logger import logger
from src.requester import requester as http
from src.settings import BASE_DIR
from src.parsers.utils import vinted_category_url
from src.parsers.parser_abc import Parser


class VintedParser(Parser):
    """
    Parser for vinted.pl
    """

    def __init__(self):
        super().__init__()
        self._db_client = VintedDbClient()
        self._reference = 'vinted'
        self._requester = http

    def __str__(self):
        return 'Vinted Parser'

    def __call__(self, *args, **kwargs):
        logger.debug('Starting Vinted Parser')
        for category_id in self._db_client.category_ids:
            logger.debug(f'Parsing {category_id}')
            new_items = self._get_new_items(category_id)
            if new_items:
                self._insert_items(new_items)
            else:
                logger.debug('No new items')
        logger.debug(f'Done parsing f{category_id}')

    def _get_new_items(self, category_id: int) -> List[Item]:
        category_name = self._db_client.get_category_name(category_id)
        api_url = vinted_category_url(category_name)
        search_response = http.get(api_url)
        items = search_response['items']
        unique_ids = self._db_client.unique_ids
        logger.debug(f'Found {len(unique_ids)} unique ids in database')
        result = [self._get_item(item, category_id) for item in items]
        logger.debug(f'Fetched {len(items)} items from API for category_id {category_id}')
        return result

    def _get_item(self, item: dict, category_id: int) -> Item:
        return Item(
            title=item['title'],
            unique_id=item['id'],
            price=item['price'],
            brand_name=item['brand_title'],
            size=item['size_title'],
            url=item['url'],
            image_path=self._get_image(item),
            category_id=category_id,
        )

    def _get_image(self, item: dict) -> str:
        http_ = urllib3.PoolManager()
        response = http_.request('GET', item['photo']['url'])
        img_data = response.data

        dir_path = os.path.join(
            BASE_DIR.parent,
            'images',
            self._reference,
            item['brand_title'],
            str(item['id']))

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

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
            logger.error(f'Failed to save image for {item["url"]}', exc_info=True)
        return filename

    def _insert_items(self, items: list[Item, ...]) -> None:
        logger.debug(f'Inserting {len(items)} items to database')
        try:
            self._db_client.insert_items(items)
            logger.debug(f'Inserted {len(items)} items to the database')
            logger.debug('Database updated')
        except Exception as e:
            logger.error(e)
            logger.error('Failed to insert items to database', exc_info=True)


vinted = VintedParser()


if __name__ == '__main__':
    vinted()
