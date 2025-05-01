import random
import time
from loguru import logger


def random_sleep(range: list):
    t = random.randint(*range)
    logger.debug(f'Sleeping for {t} {"seconds" if t > 1 else "second"}...')
    time.sleep(t)
