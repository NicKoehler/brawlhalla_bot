import logging
from time import time

logger = logging.getLogger("Cache")


class Cache:
    def __init__(self, validation_seconds: int) -> None:
        self._validation_seconds = validation_seconds
        self._cache = {}

    def add(self, key, data) -> None:
        """
        Adds the cache entry for the given key
        :param key: The key of the entry
        :param data: The data of the entry
        :return: None
        """

        logger.debug("Adding cache for key '%s'", key)
        self._cache[key] = (time(), data)

    def get(self, key):
        """
        :param key: The key of the entry
        :return: The data of the entry
        """
        result = self._cache.get(key)
        if result is None:
            logger.debug("Nothing in cache for key '%s'", key)
            return
        if time() - result[0] < self._validation_seconds:
            logger.debug("Found valid cache for key '%s'", key)
            return result[1]
        logger.debug("Ivalid cache for key '%s'", key)

    def remove(self, key) -> None:
        """
        Removes the cache entry for the given key
        :param key: The key of the entry
        :return: None
        """
        logger.debug("Removing cache for key '%s'", key)
        if key in self._cache:
            self._cache.pop(key)

    async def clear(self) -> None:
        """
        Clears the cache.
        :return: None
        """
        logger.debug("Clearing cache")
        self._cache.clear()
