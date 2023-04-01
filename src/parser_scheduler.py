import threading
import time
import schedule
from settings import PARSER_UPDATE_INTERVAL, DEBUG
from consts import PARSERS
from logger import logger


def start_parser(parser):
    try:
        threading.Thread(target=parser()()).start()
        logger.info(f'Successfully started parser thread for {parser}')
    except Exception as e:
        logger.error(f'Failed to start parser thread for {parser}: {e}')


def main():
    for parser in PARSERS:
        schedule.every(PARSER_UPDATE_INTERVAL).minutes.do(start_parser, parser)
        time.sleep(10)


if __name__ == '__main__':
    main()
    while True:
        schedule.run_pending()
        time.sleep(1)

