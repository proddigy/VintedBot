"""
Scheduler for running parsers
"""
import schedule
import time
import threading

from src.settings import PARSERS
from src.settings import PARSER_UPDATE_INTERVAL


def main():
    """
    Runs different scripts depending on marketplace in different threads
    """
    for parser in PARSERS:
        threading.Thread(target=parser().run).start()


if __name__ == '__main__':
    schedule.every(PARSER_UPDATE_INTERVAL).minutes.do(main)
