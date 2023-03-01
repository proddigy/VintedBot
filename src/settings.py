"""
This module contains functions that are used in other modules
"""
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

DEBUG = False

PARSERS = [
    'src.parsers.vinted_parser.VintedParser',
]

PARSER_UPDATE_INTERVAL = 20  # minutes

VINTED_ITEMS_PER_PAGE = 96

LOG_FILE_PATH = os.path.join(os.path.dirname(__file__), 'logs', 'log.txt')
