import pytest
from helpers import depop_category_url
from helpers import grailed_category_url
from helpers import vinted_category_url
from selenium import webdriver


def test_depop_category_url():
    """
    Test case for Depop category url.
    """
    category = 'nike jackets'
    expected_result = 'https://www.depop.com/search/?q=nike%20jackets'
    assert depop_category_url(category) == expected_result

def test_grailed_category_url():
    """
    Test case for Grailed category url.
    """
    driver = webdriver.Chrome()
    category = 'nike jackets'
    expected_result = 'https://www.grailed.com/shop/gsg3jh5CsQ'
    assert grailed_category_url(category, driver) == expected_result
