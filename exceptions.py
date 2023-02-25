"""
This module contains the exceptions used by the parser
"""


class InvalidPrice(Exception):  #
    """    Raised when the price of an item is invalid, probably because it is not a number    """
    pass
