import logging
from time import time

logger = logging.getLogger("Cache")


class Cache:
    def __init__(self, validation_seconds: int) -> None:
        self._validation_seconds = validation_seconds
        self._cache = {}

    def add(self, key, data) -> None:
        logger.debug("Adding cache for key '%s'", key)
        self._cache[key] = (time(), data)

    def get(self, key):
        result = self._cache.get(key)
        if result is None:
            logger.debug("Nothing in cache for key '%s'", key)
            return
        if time() - result[0] < self._validation_seconds:
            logger.debug("Found valid cache for key '%s'", key)
            return result[1]
        logger.debug("Ivalid cache for key '%s'", key)

    def remove(self, key):
        logger.debug("Removing cache for key '%s'", key)
        self._cache.pop(key)
