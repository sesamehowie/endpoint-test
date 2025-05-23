import json
from loguru import logger
from src.utils.rand_sleep import random_sleep
from config import RANDOM_SLEEP_RANGE, BASE_URL
from src.client.request_client import RequestClient


client = RequestClient()
test_data = [
    {
        "endpoint": "/api/monroll/biggest-win",
        "method": "GET",
    },
    {
        "endpoint": "/api/monroll/game-history/pages/2",
        "method": "GET",
    },
    {
        "endpoint": "/api/monroll/game-history/pages/3",
        "method": "GET",
    },
]


def test():
    i = 1
    for item in test_data:
        logger.info(f"Starting at item {i}")

        full_url = BASE_URL + item.get("endpoint")
        method = item.get("method")
        body = item.get("body")
        params = item.get("params")
        data = item.get("data")
        headers = item.get("headers")

        if all([i is None for i in [full_url, body, params, data, method]]):
            logger.warning(f"Item {i} - missing test data")
            continue

        res = client.request(full_url, method, headers, data, body, params)

        if res:
            logger.success(f"Item {i} | Got response:")
            print(json.dumps(res, indent=4))
        else:
            logger.warning(f"Item {i} | Empty response")

        i += 1

        random_sleep(RANDOM_SLEEP_RANGE)
