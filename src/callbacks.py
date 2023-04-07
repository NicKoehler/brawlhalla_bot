import utils
from math import ceil
from html import escape
from cache import Cache
from legends import Legends
from datetime import timedelta
from localization import Translator
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
    translate: Translator,
):
    player = cache.get(f"{View.RANKED_SOLO}_{brawlhalla_id}")

    if player is None:
        player = await brawl.get_ranked(brawlhalla_id)
        player.teams.sort(key=lambda x: x.rating, reverse=True)
        cache.add(f"{View.RANKED_SOLO}_{brawlhalla_id}", player)

    if player is None or player.games == 0:
        await callback.answer(translate.error_no_ranked_data(), show_alert=True)
        return

    return player


async def handle_search(
    brawl: Brawlhalla,
    cache: Cache,
    legends: Legends,
    translate: Translator,
    message: Message = None,
    callback: CallbackQuery = None,
    page_limit=10,
    current_page=0,
):
    if message:
        query = escape(" ".join(message.command[1:]))

        if not query:
            await message.reply(translate.usage_search())
            return

        if await utils.is_query_invalid(query, message, translate):
            return

    elif callback:
        current_page, query = utils.get_current_page(callback, query=True)

    else:
        return

    results = cache.get(query)

    if results is None:
        results = await brawl.get_rankings(name=query)
        if not results:
            if callback:
                await callback.answer(
                    translate.error_search_result(query),
                    show_alert=True,
                )
                await callback.message.delete()
                return
            elif message:
                await message.reply(
                    translate.error_search_result(query),
                )
                return

        cache.add(query, results)

    if len(results) == 1:
        await handle_general(
            brawl,
            results[0].brawlhalla_id,
            cache,
            legends,
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
    translate: Translator,
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
        "text": translate.results_search(
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
    legends: Legends,
    translate: Translator,
    message: Message = None,
    callback: CallbackQuery = None,
) -> None:
    player = await general_checks(brawl, brawlhalla_id, cache)

    if not player:
        if message:
            await message.reply(translate.error_player_not_found(id=brawlhalla_id))
        elif callback:
            await callback.answer(
                translate.error_player_not_found(id=brawlhalla_id), show_alert=True
            )
        return

    total_game_time = sum(
        (legend.matchtime for legend in player.legends),
        timedelta(seconds=0),
    ).total_seconds()

    total_game_time_list = make_played_time(translate, total_game_time)
    most_used_legend_name = "❌"

    if player.legends:
        most_used_id = player.legends[0].legend_id
        most_used_legend_name = (await legends.get(most_used_id)).bio_name

    to_send = {
        "text": translate.stats_base(
            id=player.brawlhalla_id,
            name=player.name,
        )
        + translate.stats_general(
            level=utils.make_progress_bar(player.level, player.xp_percentage),
            xp=player.xp,
            clan=player.clan.clan_name if player.clan else "❌",
            most_used_legend=most_used_legend_name,
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
        (translate.time_days(days), days),
        (translate.time_hours(hours), hours),
        (translate.time_minutes(minutes), minutes),
        (translate.time_seconds(seconds), seconds),
    ):
        if v == 0:
            continue

        translated_game_times.append(s)

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
    translate: Translator,
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
        translate.stats_clan(
            id=clan.clan_id,
            name=clan.clan_name,
            xp=clan.clan_xp,
            date=format_datetime(clan.clan_create_date, locale=translate.locale_str),
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
    translate: Translator,
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
        translate.stats_base(
            id=player.brawlhalla_id,
            name=player.name,
        )
        + translate.stats_ranked(
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
    translate: Translator,
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
            translate.error_no_team_data(),
            show_alert=True,
        )
        if is_page_view:
            await callback.message.delete()
        return

    total_pages = ceil(len(player.teams) / page_limit) - 1

    if current_page > total_pages:
        current_page = total_pages

    await callback.message.edit(
        translate.stats_base(
            id=player.brawlhalla_id,
            name=player.name,
        )
        + translate.results_teams(
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
    translate: Translator,
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
            translate.error_team_result(),
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
                translate.stats_base(
                    id=player.brawlhalla_id,
                    name=player.name,
                )
                + translate.stats_ranked_team(
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


async def handle_legend_personal_stats(
    brawl: Brawlhalla,
    brawlhalla_id: int,
    callback: CallbackQuery,
    cache: Cache,
    legends: Legends,
    translate: Translator,
    page_limit: int = 10,
    current_page: int = 0,
):
    player = await general_checks(brawl, brawlhalla_id, cache)

    if not player.legends:
        await callback.answer(
            translate.error_legend_result(team=brawlhalla_id),
            show_alert=True,
        )
        return

    len_legends = len(player.legends)
    total_pages = ceil(len_legends / page_limit) - 1

    if current_page > total_pages:
        current_page = total_pages

    await callback.message.edit(
        translate.stats_base(
            id=player.brawlhalla_id,
            name=player.name,
        )
        + translate.results_legends(
            current=current_page + 1,
            total=total_pages + 1,
        ),
        reply_markup=await Keyboard.legends(
            current_page,
            total_pages,
            page_limit,
            translate,
            legends,
            player,
        ),
    )


async def handle_legend_personal_details(
    brawl: Brawlhalla,
    brawlhalla_id: int,
    legend_obj: Legend,
    callback: CallbackQuery,
    cache: Cache,
    translate: Translator,
):
    player = await general_checks(brawl, brawlhalla_id, cache)

    if player.legends is None:
        await callback.answer(
            translate.error_legend_result(),
            show_alert=True,
        )
        return

    for legend in player.legends:
        if legend.legend_id == legend_obj.legend_id:
            game_time_list = make_played_time(
                translate, legend.matchtime.total_seconds()
            )

            await callback.message.edit(
                translate.stats_base(
                    id=player.brawlhalla_id,
                    name=player.name,
                )
                + translate.stats_legend(
                    id=legend.legend_id,
                    name=legend_obj.bio_name,
                    level=utils.make_progress_bar(legend.level, legend.xp_percentage),
                    xp=legend.xp,
                    weaponone=legend_obj.weapon_one,
                    weapontwo=legend_obj.weapon_two,
                    timeheldweaponone=format_timedelta(
                        legend.timeheldweaponone,
                        locale=translate.locale_str,
                    ),
                    timeheldweapontwo=format_timedelta(
                        legend.timeheldweapontwo,
                        locale=translate.locale_str,
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


async def handle_legend_stats(
    legends: Legends,
    translator: Translator,
    message=None,
    callback=None,
    current_page=0,
    limit=20,
):
    total_pages = ceil(len(legends) / limit) - 1

    if current_page > total_pages:
        current_page = total_pages

    text = translator.results_legends(current=current_page + 1, total=total_pages + 1)

    keyboard = await Keyboard.legends(
        current_page,
        total_pages,
        limit,
        translator,
        legends=legends,
        rows=3,
    )

    if message:
        await message.reply(
            text,
            reply_markup=keyboard,
        )
    elif callback:
        await callback.message.edit(
            text,
            reply_markup=keyboard,
        )


async def handle_legend_details(
    legend: Legend,
    callback,
    translator: Translator,
):
    await callback.message.edit(legend)
