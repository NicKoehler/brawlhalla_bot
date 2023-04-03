from math import ceil
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
            ).legend_name_key.capitalize(),
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


async def ranked_checks(
    brawl,
    brawlhalla_id: int,
    player: PlayerRanked,
    callback: CallbackQuery,
    cache: Cache,
    translate: Plate,
    teamcheck=False,
):
    if player is None:
        player = await brawl.get_ranked(brawlhalla_id)
        cache.add(f"{View.RANKED_SOLO}_{brawlhalla_id}", player)

    if player is None:
        await callback.answer(translate("no_ranked_data"), show_alert=True)
        return

    if teamcheck and not player.teams:
        await callback.answer(translate("no_team_data"), show_alert=True)
        return

    return player


async def handle_ranked_solo(
    brawl,
    brawlhalla_id: int,
    player: PlayerRanked,
    callback: CallbackQuery,
    cache: Cache,
    translate: Plate,
):
    player = await ranked_checks(
        brawl, brawlhalla_id, player, callback, cache, translate
    )

    if player is None:
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


async def handle_ranked_team(
    brawl,
    brawlhalla_id: int,
    player: PlayerRanked,
    callback: CallbackQuery,
    cache: Cache,
    translate: Plate,
):
    player = await ranked_checks(
        brawl, brawlhalla_id, player, callback, cache, translate, True
    )

    if player is None:
        return

    page_limit = 10
    current_page = 0
    total_pages = ceil(len(player.teams) / page_limit)

    await callback.message.edit(
        translate(
            "teams_results",
            id=player.brawlhalla_id,
            name=player.name,
            current=current_page + 1,
            total=total_pages,
        ),
        reply_markup=Keyboard.search_team(
            player, current_page, total_pages - 1, page_limit, translate
        ),
    )


async def handle_ranked_team_detail(
    brawl,
    brawlhalla_id_one: int,
    brawlhalla_id_two: int,
    player: PlayerRanked,
    callback: CallbackQuery,
    cache: Cache,
    translate: Plate,
):
    player = await ranked_checks(
        brawl, brawlhalla_id_one, player, callback, cache, translate, True
    )
    if player is None:
        return

    for team in player.teams:
        if (
            team.brawlhalla_id_one == brawlhalla_id_one
            and team.brawlhalla_id_two == brawlhalla_id_two
        ) or (
            team.brawlhalla_id_one == brawlhalla_id_two
            and team.brawlhalla_id_two == brawlhalla_id_one
        ):
            await callback.message.edit(
                translate(
                    "ranked_team_stats",
                    id=player.brawlhalla_id,
                    name=player.name,
                    teamname=team.teamname,
                    rating=team.rating,
                    peak=team.peak_rating,
                    tier=team.tier,
                    games=team.games,
                    wins=team.wins,
                    loses=team.games - team.wins,
                    region=team.region,
                ),
                reply_markup=Keyboard.stats(
                    brawlhalla_id_one,
                    View.RANKED_TEAM_DETAIL,
                    translate,
                    brawlhalla_id_two,
                ),
            )
            break
