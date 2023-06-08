import logging

from time import time

logger = logging.getLogger("Cache")


class Cache:
    def __init__(
        self,
        validation_seconds: int = None,
    ) -> None:
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
        if self._validation_seconds is not None:
            self._cache[key] = (time(), data)
        else:
            self._cache[key] = data

    def values(self) -> list:
        """
        :return: The values of the cache
        """
        return list(self._cache.values())

    def get(self, key):
        """
        :param key: The key of the entry
        :return: The data of the entry
        """
        result = self._cache.get(key)

        if result is None:
            logger.debug("Nothing in cache for key '%s'", key)
            return

        if self._validation_seconds is None:
            logger.debug("Found valid cache for key '%s'", key)
            return result

        if time() - result[0] > self._validation_seconds:
            logger.debug("Ivalid cache for key '%s'", key)
            return

        logger.debug("Found valid cache for key '%s'", key)
        return result[1]

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

    def __len__(self) -> int:
        return len(self._cache)
