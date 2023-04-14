"""
This module contains functions that are used in other modules
"""
import sys
import time
from alive_progress import alive_bar
from functools import wraps
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from src.db_client.models import Category
from src.settings import VINTED_ITEMS_PER_PAGE

Url = str


def vinted_category_url(requested_category: Category) -> Url:
    """
    Returns url for vinted category
    :param requested_category: Category object from db
    :type requested_category: Category
    :return: Url
    :rtype: Url
    """
    title = requested_category.name.replace(' ', '+')
    brand_id = requested_category.brand_id if requested_category.brand_id else ''
    return f'https://www.vinted.pl/api/v2/catalog/items?search_text=' \
           f'{title}' \
           f'&catalog_ids=' \
           f'&color_ids=' \
           f'&brand_ids={brand_id}' \
           f'&size_ids=' \
           f'&material_ids=' \
           f'&video_game_rating_ids=' \
           f'&status_ids=' \
           f'&page=1&' \
           f'per_page={VINTED_ITEMS_PER_PAGE}'


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
