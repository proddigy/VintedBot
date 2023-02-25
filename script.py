"""
This module contains functions that are used in main.py
"""

import time
from parser import VintedParser, GrailedParser
from tqdm import tqdm

from db_manager import VintedDBManager, GrailedDBManager
from helpers import get_marketplace

marketplaces = ('vinted', 'depop', 'ebay', 'mercari', 'grailed')

marketplace_to_dbmanager = {
    'vinted': VintedDBManager,
    'grailed': GrailedDBManager
}
marketplace_to_parser = {
    'vinted': VintedParser,
    'grailed': GrailedParser
}


def vinted_script(category: str):
    marketplace = 'vinted'
    db_m = marketplace_to_dbmanager[marketplace]()
    parser = marketplace_to_parser[marketplace]()
    items = parser.get(category)

    for item in tqdm(items,
                     desc='Inserting items into database',
                     unit='item',
                     total=len(items)):

        detailed_item = parser.get_details(item)
        if detailed_item.condition is None:
            time.sleep(10)
            detailed_item = parser.get_details(item)
            if detailed_item.condition is None:
                print(f'Item: {item} has no condition')
        try:
            db_m.insert_item(detailed_item)
        except Exception as e:
            print(e)
            print(f'Item: {item} not inserted into database')

        time.sleep(0.8)
