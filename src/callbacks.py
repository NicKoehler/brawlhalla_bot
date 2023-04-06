import utils
from math import ceil
from html import escape
from cache import Cache
from plate import Plate
from datetime import timedelta
from keyboards import Keyboard, View
from brawlhalla_api import Brawlhalla
from brawlhalla_api.types import Legend
from pyrogram.types import Message, CallbackQuery
from babel.dates import format_datetime, format_timedelta


async def general_checks(
    brawl: Brawlhalla,
    brawlhalla_id: int,
    cache: Cache,
):
    player = cache.get(f"{View.GENERAL}_{brawlhalla_id}")

    if player is None:
        player = await brawl.get_stats(brawlhalla_id)
        player.legends.sort(key=lambda x: x.matchtime, reverse=True)
        cache.add(f"{View.GENERAL}_{brawlhalla_id}", player)

    return player


async def ranked_checks(
    brawl: Brawlhalla,
    brawlhalla_id: int,
    callback: Message,
    cache: Cache,
    translate: Plate,
):
    player = cache.get(f"{View.RANKED_SOLO}_{brawlhalla_id}")

    if player is None:
        player = await brawl.get_ranked(brawlhalla_id)
        player.teams.sort(key=lambda x: x.rating, reverse=True)
        cache.add(f"{View.RANKED_SOLO}_{brawlhalla_id}", player)

    if player is None or player.games == 0:
        await callback.answer(translate("no_ranked_data"), show_alert=True)
        return

    return player


async def handle_search(
    brawl: Brawlhalla,
    cache: Cache,
    translate: Plate,
    message: Message = None,
    callback: CallbackQuery = None,
    page_limit=10,
    current_page=0,
):
    if message:
        query = escape(" ".join(message.command[1:]))

        if not query:
            await message.reply(translate("search_usage"))
            return

        len_query = len(query)

        if len_query < 2 or len_query > 32:
            await message.reply(translate("length_error"))
            return

    elif callback:
        current_page = utils.get_current_page(callback)

    else:
        return

    results = cache.get(query)

    if results is None:
        results = await brawl.get_rankings(name=query)
        if not results:
            if callback:
                await callback.answer(
                    translate("search_results_error", query=query),
                    show_alert=True,
                )
                await callback.message.delete()
                return
            elif message:
                await message.reply(translate("search_results_error", query=query))
                return

        cache.add(query, results)

    if len(results) == 1:
        await handle_general(
            brawl,
            results[0].brawlhalla_id,
            cache,
            translate,
            message=message,
            callback=callback,
        )
        return

    await send_results(
        results,
        translate,
        query,
        message,
        callback,
        page_limit=page_limit,
        current_page=current_page,
    )


async def send_results(
    results,
    translate,
    query,
    message: Message = None,
    callback: CallbackQuery = None,
    page_limit=10,
    current_page=0,
):
    total_pages = ceil(len(results) / page_limit) - 1

    if current_page > total_pages:
        current_page = total_pages

    to_send = {
        "text": translate(
            "search_results",
            query=query,
            current=current_page + 1,
            total=total_pages + 1,
        ),
        "reply_markup": Keyboard.search_player(
            results, current_page, total_pages, page_limit, translate
        ),
    }

    if message:
        await message.reply(**to_send)
    elif callback:
        await callback.message.edit(**to_send)


async def handle_general(
    brawl: Brawlhalla,
    brawlhalla_id: int,
    cache: Cache,
    translate: Plate,
    message: Message = None,
    callback: CallbackQuery = None,
) -> None:
    player = await general_checks(brawl, brawlhalla_id, cache)

    if not player:
        if message:
            await message.reply(translate("player_not_found", id=brawlhalla_id))
        elif callback:
            await callback.answer(
                translate("player_not_found", id=brawlhalla_id), show_alert=True
            )
        return

    total_game_time = sum(
        (legend.matchtime for legend in player.legends),
        timedelta(seconds=0),
    ).total_seconds()

    total_game_time_list = make_played_time(translate, total_game_time)

    to_send = {
        "text": translate(
            "base_stats",
            id=player.brawlhalla_id,
            name=player.name,
        )
        + translate(
            "general_stats",
            level=utils.make_progress_bar(player.level, player.xp_percentage),
            xp=player.xp,
            clan=player.clan.clan_name if player.clan else "❌",
            most_used_legend=max(
                player.legends, key=lambda legend: legend.matchtime
            ).legend_name_key.capitalize()
            if player.legends
            else "❌",
            total_game_time="\n".join(total_game_time_list) or "❌",
            games=player.games,
            wins=player.wins,
            loses=player.games - player.wins,
            winperc=round(player.wins / player.games * 100, 2) if player.games else 0,
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
        "reply_markup": Keyboard.stats(
            player.brawlhalla_id,
            current_view=View.GENERAL,
            translate=translate,
            show_clan=player.clan is not None,
            show_legends=len(player.legends) > 0,
        ),
    }

    if message:
        await message.reply(**to_send)
    elif callback:
        await callback.message.edit(**to_send)

    return True


def make_played_time(translate, total_game_time):
    days = int(total_game_time // 86400)
    hours = int((total_game_time % 86400) // 3600)
    minutes = int((total_game_time % 3600) // 60)
    seconds = int(total_game_time % 60)

    translated_game_times = []

    for s, v in (
        ("days", days),
        ("hours", hours),
        ("minutes", minutes),
        ("seconds", seconds),
    ):
        if v == 0:
            continue

        translated_game_times.append(translate(s, t=v))

    total_game_time_list = []

    for n, time in enumerate(translated_game_times):
        (
            total_game_time_list.append(
                ("╰─► " if n == len(translated_game_times) - 1 else "├─► ") + time
            )
        )

    return total_game_time_list


async def handle_clan(
    brawl: Brawlhalla,
    clan_id: int,
    callback: CallbackQuery,
    cache: Cache,
    translate: Plate,
    page_limit=10,
    current_page=0,
):
    clan = cache.get(f"{View.CLAN}_{clan_id}")
    if clan is None:
        clan = await brawl.get_clan(clan_id)
        cache.add(f"{View.CLAN}_{clan_id}", clan)

    len_components = len(clan.components)
    total_pages = ceil(len_components / page_limit) - 1

    if current_page > total_pages:
        current_page = total_pages

    await callback.message.edit(
        translate(
            "clan_stats",
            id=clan.clan_id,
            name=clan.clan_name,
            xp=clan.clan_xp,
            date=format_datetime(
                clan.clan_create_date, locale=translate.keywords.get("locale")
            ),
            num=len_components,
            current=current_page + 1,
            total=total_pages + 1,
        ),
        reply_markup=Keyboard.clan_components(
            clan, current_page, total_pages, page_limit, translate
        ),
    )


async def handle_ranked_solo(
    brawl: Brawlhalla,
    brawlhalla_id: int,
    callback: CallbackQuery,
    cache: Cache,
    translate: Plate,
):
    player = await ranked_checks(
        brawl,
        brawlhalla_id,
        callback,
        cache,
        translate,
    )

    if player is None:
        return

    await callback.message.edit(
        translate(
            "base_stats",
            id=player.brawlhalla_id,
            name=player.name,
        )
        + translate(
            "ranked_stats",
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
        reply_markup=Keyboard.stats(
            player.brawlhalla_id,
            current_view=View.RANKED_SOLO,
            translate=translate,
        ),
    )


async def handle_ranked_team(
    brawl: Brawlhalla,
    brawlhalla_id: int,
    callback: CallbackQuery,
    cache: Cache,
    translate: Plate,
    page_limit: int = 10,
    current_page: int = 0,
    is_page_view: bool = False,
):
    player = await ranked_checks(
        brawl,
        brawlhalla_id,
        callback,
        cache,
        translate,
    )

    if player is None or not player.teams:
        await callback.answer(
            translate("no_team_data"),
            show_alert=True,
        )
        if is_page_view:
            await callback.message.delete()
        return

    total_pages = ceil(len(player.teams) / page_limit) - 1

    if current_page > total_pages:
        current_page = total_pages

    await callback.message.edit(
        translate(
            "base_stats",
            id=player.brawlhalla_id,
            name=player.name,
        )
        + translate(
            "teams_results",
            current=current_page + 1,
            total=total_pages + 1,
        ),
        reply_markup=Keyboard.teams(
            player, current_page, total_pages, page_limit, translate
        ),
    )


async def handle_ranked_team_detail(
    brawl: Brawlhalla,
    brawlhalla_id_one: int,
    brawlhalla_id_two: int,
    callback: CallbackQuery,
    cache: Cache,
    translate: Plate,
):
    player = await ranked_checks(
        brawl,
        brawlhalla_id_one,
        callback,
        cache,
        translate,
    )
    if player is None or not player.teams:
        await callback.answer(
            translate("teams_results_error"),
        )
        await callback.message.delete()
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
                    "base_stats",
                    id=player.brawlhalla_id,
                    name=player.name,
                )
                + translate(
                    "ranked_team_stats",
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
                    brawlhalla_id_one=player.brawlhalla_id,
                    brawlhalla_id_two=brawlhalla_id_two,
                    current_view=View.RANKED_SOLO,
                    translate=translate,
                ),
            )
            break


async def handle_legend(
    brawl: Brawlhalla,
    brawlhalla_id: int,
    callback: CallbackQuery,
    cache: Cache,
    translate: Plate,
    page_limit: int = 10,
    current_page: int = 0,
):
    player = await general_checks(brawl, brawlhalla_id, cache)

    if not player.legends:
        await callback.answer(
            translate("legend_results_error", team=brawlhalla_id),
            show_alert=True,
        )
        return

    len_legends = len(player.legends)
    total_pages = ceil(len_legends / page_limit) - 1

    if current_page > total_pages:
        current_page = total_pages

    await callback.message.edit(
        translate(
            "base_stats",
            id=player.brawlhalla_id,
            name=player.name,
        )
        + translate(
            "legend_results",
            current=current_page + 1,
            total=total_pages + 1,
        ),
        reply_markup=Keyboard.legends(
            player, current_page, total_pages, page_limit, translate
        ),
    )


async def handle_legend_detail(
    brawl: Brawlhalla,
    brawlhalla_id: int,
    legend_obj: Legend,
    callback: CallbackQuery,
    cache: Cache,
    translate: Plate,
):
    player = await general_checks(brawl, brawlhalla_id, cache)

    if player.legends is None:
        await callback.answer(
            translate("legend_results_error"),
            show_alert=True,
        )
        return

    for legend in player.legends:
        if legend.legend_id == legend_obj.legend_id:
            game_time_list = make_played_time(
                translate, legend.matchtime.total_seconds()
            )

            await callback.message.edit(
                translate(
                    "base_stats",
                    id=player.brawlhalla_id,
                    name=player.name,
                )
                + translate(
                    "legend_stats",
                    id=legend.legend_id,
                    name=legend.legend_name_key.capitalize(),
                    level=utils.make_progress_bar(legend.level, legend.xp_percentage),
                    xp=legend.xp,
                    weaponone=legend_obj.weapon_one,
                    weapontwo=legend_obj.weapon_two,
                    timeheldweaponone=format_timedelta(
                        legend.timeheldweaponone,
                        locale=translate.keywords.get("locale"),
                    ),
                    timeheldweapontwo=format_timedelta(
                        legend.timeheldweapontwo,
                        locale=translate.keywords.get("locale"),
                    ),
                    matchtime="\n".join(game_time_list) or "❌",
                    games=legend.games,
                    wins=legend.wins,
                    loses=legend.games - legend.wins,
                    winperc=round(legend.wins / legend.games * 100, 2)
                    if legend.games
                    else 0,
                    ko=legend.kos,
                    death=legend.falls,
                    suicide=legend.suicides,
                    teamko=legend.teamkos,
                    damagedealt=legend.damagedealt,
                    damagetaken=legend.damagetaken,
                    koweaponone=legend.koweaponone,
                    damageweaponone=legend.damageweaponone,
                    koweapontwo=legend.koweapontwo,
                    damageweapontwo=legend.damageweapontwo,
                    kogadgets=legend.kogadgets,
                    damagegadgets=legend.damagegadgets,
                    kothrownitem=legend.kothrownitem,
                    damagethrownitem=legend.damagethrownitem,
                    kounarmed=legend.kounarmed,
                    damageunarmed=legend.damageunarmed,
                ),
                reply_markup=Keyboard.stats(
                    brawlhalla_id,
                    current_view=View.LEGEND,
                    translate=translate,
                    show_clan=player.clan is not None,
                    show_legends=len(player.legends) > 0,
                ),
            )
            break
