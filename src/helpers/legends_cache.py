from helpers.cache import Cache

from lxml import html
from httpx import AsyncClient
from brawlhalla_api import Brawlhalla
from brawlhalla_api.types import Legend
from brawlhalla_api.errors import ServiceUnavailable

URL = "https://brawlhalla.fandom.com/wiki/Legends"


class LegendsCache:
    def __init__(self, 
    brawl: Brawlhalla,
    ) -> None:  # noqa: F821
        self._brawl = brawl
        self._cache = Cache()
        self._images = {}

    async def refresh_legends(self):
        try:
            legends = await self._brawl.get_legends()
        except ServiceUnavailable:
            if self._cache.get("legends"):
                return
            legends = []

        await self.refresh_all_images()

        for legend in legends:
            legend.weapon_one = legend.weapon_one.lower()
            legend.weapon_two = legend.weapon_two.lower()
            self._images[legend.legend_id] = self._images.get(legend.bio_name)

        self.refresh_weapons(legends)
        self._cache.add("legends", {legend.legend_id: legend for legend in legends})

    async def get(self, legend_id: int | str) -> Legend:
        if isinstance(legend_id, str):
            legend_id = int(legend_id)
        legend = self._cache.get("legends").get(legend_id)
        if legend is None:
            await self.refresh_legends()
            legend = self._cache.get("legends").get(legend_id)

        return legend

    
    async def get_image_by_id(self, legend_id: int | str) -> str:
        if legend_id not in self._images:
            await self.refresh_legends()
        return self._images.get(legend_id)

    def refresh_weapons(self, legends: list[Legend]) -> None:
        weapons = set(
            item
            for sublist in [
                [legend.weapon_one, legend.weapon_two] for legend in legends
            ]
            for item in sublist
        )

        self._cache.add("weapons", weapons)

    def filter_weapon(self, weapon: str) -> list[Legend]:
        return [
            legend
            for legend in self._cache.get("legends").values()
            if legend.weapon_one == weapon or legend.weapon_two == weapon
        ]

    async def refresh_all_images(self) -> dict[str]:
        self._images = {}
        async with AsyncClient() as client:
            response = await client.get(URL)
            tree = html.fromstring(response.text)
            elements = tree.xpath("//table[@style='text-align:center;']/tbody/tr[2]/td")
            for element in elements:
                link = element.xpath(".//a")[0].attrib
                img = element.xpath(".//img")[0].attrib
                self._images[link["title"]] = img["data-src"] if "data-src" in img else img["src"]
 
    @property
    def all(self) -> list[Legend]:
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
