import json
import requests
from loguru import logger


class RequestClient:
    def __init__(self, user_agent: str = None, proxy: str = None):
        self.user_agent = user_agent
        self.proxy = proxy
        self._session = requests.Session()

    @staticmethod
    def is_successful_request(response: requests.Response):
        return True if response.status_code == 200 else False

    @staticmethod
    def get_response_obj(response: requests.Response):
        try:
            data = response.json()
        except requests.JSONDecodeError:
            logger.warning("Failed to fetch raw JSON, trying to get text info...")
            if response.text.startswith("{"):
                data = json.loads(response.text)
        finally:
            return data

    def handle_request(self, response: requests.Response) -> dict:
        if self.is_successful_request(response=response):
            return self.get_response_obj(response=response)
        raise Exception(
            f"Request is not successful, status code: {response.status_code}, text: {response.text}"
        )

    def session_request(
        self,
        url: str,
        method: str = "GET",
        headers: dict | None = None,
        data: dict | None = None,
        json: dict | None = None,
        params: dict | None = None,
        timeout: int = 60,
    ):
        with self._session.request(
            method=method,
            url=url,
            headers={"User-Agent": self.user_agent} if headers is None else headers,
            data=data,
            params=params,
            json=json,
            proxies=(
                {"http": self.proxy, "https": self.proxy}
                if self.proxy is not None
                else None
            ),
            timeout=timeout,
        ) as response:
            return self.handle_request(response)

    def request(
        self,
        url: str,
        method: str = "GET",
        headers: dict | None = None,
        data: dict | None = None,
        json: dict | None = None,
        params: dict | None = None,
        timeout: int = 60,
    ):
        response = requests.request(
            url=url,
            method=method,
            headers={"User-Agent": self.user_agent} if headers is None else headers,
            data=data,
            params=params,
            json=json,
            proxies=(
                {"http": self.proxy, "https": self.proxy}
                if self.proxy is not None
                else None
            ),
            timeout=timeout,
        )

        return self.handle_request(response)
