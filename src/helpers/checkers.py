from keyboards import View
from helpers.cache import Cache
from localization import Translator
from brawlhalla_api import Brawlhalla
from pyrogram.types import CallbackQuery
from brawlhalla_api.types import PlayerStats
from brawlhalla_api.errors import ServiceUnavailable


async def general_checks(
    brawl: Brawlhalla,
    brawlhalla_id: int,
    cache: Cache,
) -> PlayerStats | None:
    player = cache.get(f"{View.GENERAL}_{brawlhalla_id}")

    if player is None:
        player = await brawl.get_stats(brawlhalla_id)
        if player is None:
            return None
        player.legends.sort(key=lambda x: x.matchtime, reverse=True)
        cache.add(f"{View.GENERAL}_{brawlhalla_id}", player)

    return player


async def ranked_checks(
    brawl: Brawlhalla,
    brawlhalla_id: int,
    callback: CallbackQuery,
    cache: Cache,
    translate: Translator,
    ensure_ranked_games: bool = False,
):
    player = cache.get(f"{View.RANKED_SOLO}_{brawlhalla_id}")

    if player is None:
        try:
            player = await brawl.get_ranked(brawlhalla_id)
        except ServiceUnavailable:
            await callback.answer(translate.error_api_offline(), show_alert=True)
            return
        player.teams.sort(key=lambda x: x.rating, reverse=True)
        cache.add(f"{View.RANKED_SOLO}_{brawlhalla_id}", player)

    if player is None or player.games == 0 and ensure_ranked_games:
        await callback.answer(translate.error_no_ranked_data(), show_alert=True)
        return

    return player
