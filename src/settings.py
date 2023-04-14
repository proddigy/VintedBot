"""
This module contains settings that are used in other modules
"""
import os
import pathlib


BASE_DIR = pathlib.Path(__file__).parent

DEBUG = True


PARSER_UPDATE_INTERVAL = 5  # minutes


VINTED_ITEMS_PER_PAGE = 96


# LOGGING
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

LOG_DEBUG_FILE_PATH = os.path.join(
    BASE_DIR, 'logs', 'log_debug.log'
)

LOG_INFO_FILE_PATH = os.path.join(
    BASE_DIR, 'logs', 'log_info.log'
)

LOG_WARNING_FILE_PATH = os.path.join(
    BASE_DIR, 'logs', 'log_warning.log'
)

LOG_ERROR_FILE_PATH = os.path.join(
    BASE_DIR, 'logs', 'log_error.log'
)


LOG_LEVEL = 'debug'
