import logging

from time import time
from brawlhalla_api import Brawlhalla
from brawlhalla_api.types import Legend

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


class Legends:
    def __init__(self, brawl: Brawlhalla) -> None:
        self._brawl = brawl
        self._cache = Cache()

    async def refresh_legends(self):
        legends = await self._brawl.get_legends()
        self.refresh_weapons(legends)
        self._cache.add("legends", {legend.legend_id: legend for legend in legends})

    async def get(self, legend_id: int) -> Legend:
        legend = self._cache.get("legends").get(legend_id)
        if legend is None:
            await self.refresh_legends()
            legend = self._cache.get("legends").get(legend_id)

        return legend

    def refresh_weapons(self, legends: list[Legend]) -> None:
        weapons = list(
            set(
                item
                for sublist in [
                    [legend.weapon_one, legend.weapon_two] for legend in legends
                ]
                for item in sublist
            )
        )
        self._cache.add("weapons", weapons)

    @property
    def all(self) -> Legend:
        return list(self._cache.get("legends").values())

    @property
    def weapons(self) -> list[str]:
        return self._cache.get("weapons")

    def __contains__(self, key: int) -> bool:
        return key in self._cache

    def __getitem__(self, key: int) -> Legend:
        return self.get(key)

    def __len__(self) -> int:
        return len(self._cache.get("legends"))
