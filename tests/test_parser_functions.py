"""
Test cases for parser functions.
"""

from parser import VintedParser

import pytest


@pytest.fixture
def vinted_parser():
    return VintedParser()


def test_vinted_parser_parse_price(vinted_parser):
    parser = vinted_parser

    # Test case: with two prices
    price_1 = "50"
    price_2 = "99"
    expected_result = 50.99
    assert parser._parse_price(price_1, price_2) == expected_result

    # Test case: with one price
    price_1 = "30"
    with pytest.raises(ValueError) as e:
        parser._parse_price(price_1)
    assert str(e.value) == 'Price should be a list of 2 elements'

    # Test case: with no price
    price_1 = "Free"
    with pytest.raises(ValueError) as e:
        parser._parse_price(price_1)
    assert str(e.value) == 'Price should be a list of 2 elements'


def test_vinted_parser_parse_size(vinted_parser):
    parser = vinted_parser

    # Test case: with valid size
    size = "rozmiar: L"
    expected_result = "L"
    assert parser._parse_size(size) == expected_result

    # Test case: with no size
    size = "size: -"
    expected_result = None
    assert parser._parse_size(size) == expected_result


def test_vinted_parser_parse_brand_name(vinted_parser):
    parser = vinted_parser

    # Test case: with valid brand name
    brand_name = "marka: Nike"
    expected_result = "Nike"
    assert parser._parse_brand_name(brand_name) == expected_result

    # Test case: with no brand name
    brand_name = "marka:"
    expected_result = None
    assert parser._parse_brand_name(brand_name) == expected_result


def test_vinted_parser_parse_condition(vinted_parser):
    parser = vinted_parser

    # Test case: with valid condition
    condition = " \n     Great condition        \nCondition information\n"
    expected_result = "Great condition"
    assert parser._parse_condition(condition) == expected_result

    # Test case: with no condition
    condition = ""
    expected_result = None
    assert parser._parse_condition(condition) == expected_result

