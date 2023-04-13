import helpers.utils as utils

from html import escape
from datetime import timedelta
from localization import Translator
from keyboards import Keyboard, View
from brawlhalla_api import Brawlhalla
from brawlhalla_api.types import Legend
from helpers.cache import Cache, Legends
from brawlhalla_api.errors import ServiceUnavailable
from babel.dates import format_datetime, format_timedelta
from helpers.checkers import general_checks, ranked_checks
from pyrogram.types import (
    Message,
    CallbackQuery,
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
)


async def handle_general(
    brawl: Brawlhalla,
    brawlhalla_id: int,
    cache: Cache,
    legends: Legends,
    translate: Translator,
    update: Message | CallbackQuery | InlineQuery,
) -> None:
    try:
        player = await general_checks(brawl, brawlhalla_id, cache)
    except ServiceUnavailable:
        if isinstance(update, Message):
            await update.reply(translate.error_api_offline())
        if isinstance(update, CallbackQuery):
            await update.answer(translate.error_api_offline(), show_alert=True)
        if isinstance(update, InlineQuery):
            await update.answer(
                [
                    InlineQueryResultArticle(
                        title=translate.error_api_offline(),
                        input_message_content=InputTextMessageContent(
                            translate.error_api_offline()
                        ),
                    )
                ],
                is_personal=True,
            )
        return

    if not player:
        if isinstance(update, Message):
            await update.reply(translate.error_player_not_found(id=brawlhalla_id))
        elif isinstance(update, CallbackQuery):
            await update.answer(
                translate.error_player_not_found(id=brawlhalla_id), show_alert=True
            )
        elif isinstance(update, InlineQuery):
            await update.answer(
                [
                    InlineQueryResultArticle(
                        title=translate.error_player_result(),
                        input_message_content=InputTextMessageContent(
                            translate.error_player_result()
                        ),
                    )
                ],
                is_personal=True,
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

    text = translate.stats_base(
        id=player.brawlhalla_id,
        name=player.name,
    ) + translate.stats_general(
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
    )

    keyboard = Keyboard.stats(
        player.brawlhalla_id,
        current_view=View.GENERAL,
        translate=translate,
        show_clan=player.clan is not None,
        show_legends=len(player.legends) > 0,
    )

    if isinstance(update, InlineQuery):
        await update.answer(
            [
                InlineQueryResultArticle(
                    title=player.name,
                    input_message_content=InputTextMessageContent(
                        text,
                    ),
                    reply_markup=keyboard,
                )
            ]
        )
    else:
        await utils.send_or_edit_message(
            update,
            text,
            keyboard,
        )


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
        try:
            clan = await brawl.get_clan(clan_id)
        except ServiceUnavailable:
            await callback.answer(
                translate.error_api_offline(),
                show_alert=True,
            )
            return
        cache.add(f"{View.CLAN}_{clan_id}", clan)

    await callback.edit_message_text(
        translate.stats_clan(
            id=clan.clan_id,
            name=clan.clan_name,
            xp=clan.clan_xp,
            date=format_datetime(clan.clan_create_date, locale=translate.locale_str),
            num=len(clan.components),
        ),
        reply_markup=Keyboard.clan_components(
            clan, current_page, page_limit, translate
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
    await callback.edit_message_text(
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

    await callback.edit_message_text(
        translate.stats_base(
            id=player.brawlhalla_id,
            name=player.name,
        ),
        reply_markup=Keyboard.teams(player, current_page, page_limit),
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
            await callback.edit_message_text(
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
    try:
        player = await general_checks(brawl, brawlhalla_id, cache)
    except ServiceUnavailable:
        await callback.answer(
            translate.error_api_offline(),
            show_alert=True,
        )
        return
    if not player.legends:
        await callback.answer(
            translate.error_legend_result(team=brawlhalla_id),
            show_alert=True,
        )
        return

    await callback.edit_message_text(
        translate.stats_base(
            id=player.brawlhalla_id,
            name=player.name,
        )
        + translate.results_legends(),
        reply_markup=await Keyboard.legends(
            current_page,
            page_limit,
            translate,
            legends=legends,
            player=player,
        ),
    )


async def handle_player_legend_details(
    brawl: Brawlhalla,
    brawlhalla_id: int,
    legend_obj: Legend,
    callback: CallbackQuery,
    cache: Cache,
    translate: Translator,
):
    try:
        player = await general_checks(brawl, brawlhalla_id, cache)
    except ServiceUnavailable:
        await callback.answer(
            translate.error_api_offline(),
            show_alert=True,
        )
        return
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

            await callback.edit_message_text(
                translate.stats_base(
                    id=player.brawlhalla_id,
                    name=player.name,
                )
                + translate.stats_player_legend(
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
    update: Message | CallbackQuery,
    weapon: str = None,
    current_page=0,
    limit=20,
):
    if weapon:
        legends = legends.filter_weapon(weapon)

    await utils.send_or_edit_message(
        update,
        translator.results_legends_with_weapon(weapon=weapon.capitalize())
        if weapon
        else translator.results_legends(),
        await Keyboard.legends(
            current_page,
            limit,
            translator,
            legends=legends,
            weapon=weapon,
            rows=3,
        ),
    )


async def handle_weapons(
    legends: Legends,
    update: Message | CallbackQuery,
    translate: Translator,
    weapon: str = None,
):
    if weapon:
        await handle_legend_stats(legends, translate, update, weapon)
        return

    await utils.send_or_edit_message(
        update,
        translate.all_weapons(),
        Keyboard.weapons(legends.weapons, translate),
    )


async def handle_legend_details(
    legend: Legend,
    translator: Translator,
    update: Message | CallbackQuery,
):
    await utils.send_or_edit_message(
        update,
        translator.stats_legend(
            legend_id=legend.legend_id,
            bio_name=legend.bio_name,
            bio_aka=legend.bio_aka,
            weapon_one=legend.weapon_one.capitalize(),
            weapon_two=legend.weapon_two.capitalize(),
            strength=legend.strength,
            dexterity=legend.dexterity,
            defense=legend.defense,
            speed=legend.speed,
        ),
        Keyboard.legends_weapons(translator),
    )


async def handle_search(
    inline_query: InlineQuery,
    brawl: Brawlhalla,
    translate: Translator,
    cache: Cache,
):
    if not inline_query.query:
        text = translate.usage_inline()
        await inline_query.answer(
            [
                InlineQueryResultArticle(
                    title=text, input_message_content=InputTextMessageContent(text)
                )
            ]
        )
    query = escape(" ".join(inline_query.query.split()).lower())
    results = cache.get(query)

    if not results:
        try:
            results = await brawl.get_rankings(query)
        except ServiceUnavailable:
            text = translate.error_api_offline()
            await inline_query.answer(
                [
                    InlineQueryResultArticle(
                        title=text,
                        input_message_content=InputTextMessageContent(
                            text,
                        ),
                    )
                ],
                is_personal=True,
            )
            return
    if not results:
        await inline_query.answer(
            [
                InlineQueryResultArticle(
                    title=translate.error_player_result(),
                    input_message_content=InputTextMessageContent(
                        translate.error_player_result(),
                    ),
                )
            ],
            is_personal=True,
        )
        return

    cache.add(query, results)

    await inline_query.answer(
        [
            InlineQueryResultArticle(
                title=f"{result.name} ({result.rating})",
                description=f"🏆 {result.wins:<8} 🤬 {result.games - result.wins:<8}",
                input_message_content=InputTextMessageContent(
                    f"{result.name} ({result.rating})"
                ),
                reply_markup=Keyboard.stats(
                    result.brawlhalla_id,
                    None,
                    translate,
                    show_clan=False,
                    show_legends=False,
                ),
            )
            for result in results
        ],
        is_personal=True,
    )
