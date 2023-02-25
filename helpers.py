"""
This module contains functions that are used in other modules
"""
import sys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

Url = str


def vinted_category_url(requested_category: str) -> Url:
    """
    Returns url for vinted category
    :param requested_category:
    :return:
    """
    return f'https://www.vinted.pl/vetements?search_text=' \
           f'{requested_category.strip().replace(" ", "+")}' \
           f'&order=newest_first'


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
