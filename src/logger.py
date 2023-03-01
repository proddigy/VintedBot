"""
This module contains the logger class.
"""

import logging
import os
import sys
from src.settings import LOG_FILE_PATH, DEBUG

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


class Logger:
    """
    Logger class
    """

    def __init__(self):
        self._logger = logging.getLogger('vinted_parser')
        self._logger.setLevel(logging.DEBUG)
        self._logger.addHandler(logging.FileHandler(LOG_FILE_PATH))
        self._logger.addHandler(logging.StreamHandler())
        if DEBUG:
            self._logger.setLevel(logging.DEBUG)
            # clear log file every time the program is run
            with open(LOG_FILE_PATH, 'w', encoding='utf-8'):
                pass
        else:
            self._logger.setLevel(logging.INFO)

    def info(self, message: str) -> None:
        """
        Logs info message
        :param message:
        :return: None
        """
        self._logger.info(message)

    def error(self, message: str) -> None:
        """
        Logs error message
        :param message:
        :return: None
        """
        self._logger.error(message)

    def warning(self, message: str) -> None:
        """
        Logs warning message
        :param message:
        :return: None
        """
        self._logger.warning(message)

    def debug(self, message: str) -> None:
        """
        Logs debug message
        :param message:
        :return: None
        """
        self._logger.debug(message)

    def critical(self, message: str) -> None:
        """
        Logs critical message
        :param message:
        :return: None
        """
        self._logger.critical(message)


logger = Logger()
