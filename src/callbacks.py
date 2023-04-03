import utils
from cache import Cache
from plate import Plate
from datetime import timedelta
from keyboards import Keyboard, View
from brawlhalla_api.types import PlayerStats, PlayerRanked
from pyrogram.types import CallbackQuery


async def handle_general(
    brawl,
    brawlhalla_id: int,
    player: PlayerStats,
    callback: CallbackQuery,
    cache: Cache,
    translate: Plate,
):
    if player is None:
        player = await brawl.get_stats(brawlhalla_id)
        cache.add(callback.data, player)

    await callback.message.edit(
        translate(
            "general_stats",
            id=player.brawlhalla_id,
            name=player.name,
            level=utils.make_progress_bar(player.level, player.xp_percentage),
            xp=player.xp,
            clan=player.clan.clan_name if player.clan else "❌",
            most_used_legend=max(
                player.legends, key=lambda legend: legend.matchtime
            ).legend_name_key,
            total_game_time=sum(
                (legend.matchtime for legend in player.legends),
                timedelta(seconds=0),
            ),
            games=player.games,
            wins=player.wins,
            loses=player.games - player.wins,
            winperc=round(player.wins / player.games * 100, 2),
            totalko=sum(legend.kos for legend in player.legends),
            totaldeath=sum(legend.falls for legend in player.legends),
            totalsuicide=sum(legend.suicides for legend in player.legends),
            totalteamko=sum(legend.teamkos for legend in player.legends),
            kobomb=player.kobomb,
            damagebomb=player.damagebomb,
            komine=player.komine,
            damagemine=player.damagemine,
            kospikeball=player.kospikeball,
            damagespikeball=player.damagespikeball,
            kosidekick=player.kosidekick,
            damagesidekick=player.damagesidekick,
            kosnowball=player.kosnowball,
            hitsnowball=player.hitsnowball,
        ),
        reply_markup=Keyboard.stats(player.brawlhalla_id, View.GENERAL, translate),
    )


async def handle_rankedsolo(
    brawl,
    brawlhalla_id: int,
    player: PlayerRanked,
    callback: CallbackQuery,
    cache: Cache,
    translate: Plate,
):
    if player is None:
        player = await brawl.get_ranked(brawlhalla_id)
        cache.add(callback.data, player)

    if player is None:
        callback.answer(translate("no_ranked_data"), show_alert=True)
        return

    await callback.message.edit(
        translate(
            "ranked_stats",
            id=player.brawlhalla_id,
            name=player.name,
            rating=player.rating,
            peak=player.peak_rating,
            tier=player.tier,
            games=player.games,
            wins=player.wins,
            loses=player.games - player.wins,
            region=player.region,
            glory=player.estimated_glory,
            elo_reset=player.estimated_elo_reset,
        ),
        reply_markup=Keyboard.stats(player.brawlhalla_id, View.RANKED_SOLO, translate),
    )
