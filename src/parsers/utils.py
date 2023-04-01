"""
This module contains functions that are used in other modules
"""
import sys
import time
from alive_progress import alive_bar
from functools import wraps
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
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
           f'&catalog_ids=2050' \
           f'&color_ids=' \
           f'&brand_ids=' \
           f'&size_ids=' \
           f'&material_ids=' \
           f'&video_game_rating_ids=' \
           f'&status_ids=' \
           f'&page=1&' \
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
    """
    Decorator that prints function execution time
    :param func:
    :return: str: time in seconds
    """

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} took {end_time - start_time} seconds to run.")
        return result

    return wrapper


def progress_bar(func):
    """
    wrapper for progress bar
    :param func: function to wrap
    :return: wrapped function
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        iterations = kwargs.pop("iterations", 100)
        with alive_bar(iterations) as bar:
            result = func(*args, **kwargs, bar=bar)
        return result

    return wrapper
