"""
This module contains functions that are used in other modules
"""
import sys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from src.settings import VINTED_ITEMS_PER_PAGE

Url = str


def vinted_category_url(requested_category: str) -> Url:
    """
    Returns url for vinted category
    :param requested_category:
    :return: Url
    """
    requested_category = requested_category.strip().replace(' ', '+')
    return f'https://www.vinted.pl/api/v2/catalog/items?search_text=' \
           f'{requested_category}' \
           f'&catalog_ids=2050&color_ids=&brand_ids=&size_ids=&material_ids=&video_game_rating_ids=&status_ids=&page=1&' \
           f'per_page={VINTED_ITEMS_PER_PAGE}'


def grailed_category_url(search_request: str, driver_selenium) -> Url:
    """
    Returns url for grailed category
    :param search_request: usually category
    :param driver_selenium: selenium driver used by parser class
    :return:
    """
    driver_selenium.get('https://www.grailed.com/')
    search = driver_selenium.find_element(by=By.ID, value='header_search-input')
    search.send_keys(Keys.ENTER)
    search.send_keys(search_request)
    search.send_keys(Keys.ENTER)
    time.sleep(3)
    return driver_selenium.current_url


def depop_category_url(search_request: str) -> Url:
    """
    Returns url for depop category
    :param search_request: usually category
    :return:
    """
    search_request = search_request.strip().replace(" ", "%20")
    depop_url = 'https://www.depop.com/search/'
    return f'{depop_url}?q={search_request}'


def get_marketplace():
    """
    Gets marketplace from user input
    :return: returns marketplace if exists
    """
    marketplace = 'vinted'  # input('Enter marketplace: ').strip().lower()
    match marketplace:
        case 'vinted':
            return 'vinted'
        case 'exit':
            sys.exit()
        case _:
            print('Marketplace not supported')

    get_marketplace()

def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} took {end_time - start_time} seconds to run.")
        return result
    return wrapper