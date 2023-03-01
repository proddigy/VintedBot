"""
This module is used to perform http requests.
"""
import requests

HEADERS = {
    "User-Agent": "PostmanRuntime/7.28.4",
    "Host": "www.vinted.pl",
}

domain = "pl"

VINTED_URL = f"https://www.vinted.{domain}"
VINTED_AUTH_URL = f"https://www.vinted.{domain}/auth/token_refresh"
VINTED_API_URL = f"https://www.vinted.{domain}/api/v2"
VINTED_PRODUCTS_ENDPOINT = "catalog/items"


class VintedRequester:
    """
    requester class used to perform http requests to vinted.pl
    """

    def __init__(self):
        self.VINTED_URL = VINTED_URL
        self.VINTED_AUTH_URL = VINTED_AUTH_URL
        self.VINTED_API_URL = VINTED_API_URL
        self.VINTED_PRODUCTS_ENDPOINT = VINTED_PRODUCTS_ENDPOINT
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.setCookies()

    def get(self, url, data=None):
        """
        Perform a http get request.
        :param url: str
        :param data: dict, optional
        :return: dict
            Json format
        """
        response = self.session.get(url, params=data)

        response.raise_for_status()

        return response.json()

    def post(self, url, params=None):
        """
        Perform a http post request.
        :param url: url to post to
        :param params: params to post
        :return: none
        """
        response = self.session.post(url, params)
        response.raise_for_status()
        return response

    def setCookies(self, domain="pl"):
        """used to set cookies"""
        try:
            self.post(self.VINTED_AUTH_URL)
            print("Cookies set!")
        except Exception as e:
            print(
                f"There was an error fetching cookies for {self.VINTED_URL}\n Error : {e}"
            )


requester = VintedRequester()
