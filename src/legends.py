from cache import Cache
from brawlhalla_api import Brawlhalla
from brawlhalla_api.types import Legend


class Legends:
    def __init__(self, brawl: Brawlhalla) -> None:
        self._brawl = brawl
        self._cache = Cache()

    async def refresh_legends(self):
        legends = await self._brawl.get_legends()
        await self._cache.clear()
        for legend in legends:
            self._cache.add(legend.legend_id, legend)

    async def get(self, legend_id: int) -> Legend:
        legend = self._cache.get(legend_id)
        if legend is None:
            await self.refresh_legends()
            legend = self._cache.get(legend_id)
        return legend

    def all(self) -> Legend:
        return self._cache.values()

    def __contains__(self, key: int) -> bool:
        return key in self._cache

    def __getitem__(self, key: int) -> Legend:
        return self.get(key)

    def __len__(self) -> int:
        return len(self._cache)
