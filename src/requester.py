import time

import requests
from src.logger import logger

HEADERS = {
    "User-Agent": "PostmanRuntime/7.28.4",
    "Host": "www.vinted.pl",
}

DOMAIN = "pl"

VINTED_URL = f"https://www.vinted.{DOMAIN}"
VINTED_AUTH_URL = f"https://www.vinted.{DOMAIN}/auth/token_refresh"
VINTED_API_URL = f"https://www.vinted.{DOMAIN}/api/v2"
VINTED_PRODUCTS_ENDPOINT = "catalog/items"


class VintedRequester:
    """
    requester class used to perform http requests to vinted.pl
    """

    def __init__(self):
        self.vinted_url = VINTED_URL
        self.vinted_auth_url = VINTED_AUTH_URL
        self.vinted_api_url = VINTED_API_URL
        self.vinted_products_endpoint = VINTED_PRODUCTS_ENDPOINT
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.set_cookies()

    def get(self, url, data=None):
        """
        Perform a http get request.
        :param url: str
        :param data: dict, optional
        :return: dict
            Json format
        """
        try:
            response = self.session.get(url, params=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(e, exc_info=True)
            self.set_cookies()
            return self.get(url, data)

    def post(self, url, params=None):
        """
        Perform a http post request.
        :param url: url to post to
        :param params: params to post
        :return: none
        """
        response = self.session.post(url, params)
        try:
            response.raise_for_status()
        except Exception as e:
            logger.error(e, exc_info=True)
            self.set_cookies()

        return response

    def set_cookies(self, attempt=1):
        """used to set cookies"""
        if attempt > 3:
            logger.error("Failed to set cookies after 3 attempts")
            time.sleep(60)
            self.set_cookies()

        try:
            self.post(self.vinted_auth_url)
            logger.info("Cookies set!")
        except Exception as e:
            logger.error(
                f"There was an error fetching cookies for {self.vinted_url} on attempt {attempt}\n Error : {e}"
            )
            self.set_cookies(attempt + 1)


requester = VintedRequester()

