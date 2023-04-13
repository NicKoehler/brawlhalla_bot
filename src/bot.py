import traceback

from time import time
from os import environ
from html import escape
from functools import wraps
from dotenv import load_dotenv
from datetime import timedelta
from itertools import combinations
from keyboards import Keyboard, View
from brawlhalla_api import Brawlhalla
from brawlhalla_api.errors import ServiceUnavailable

from helpers.cache import Cache, Legends
from helpers.user_settings import UserSettings
from helpers.utils import is_query_invalid, get_localized_commands

from pyrogram import Client, filters
from pyrogram.methods.utilities.idle import idle
from pyrogram.types import (
    Message,
    CallbackQuery,
    BotCommand,
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
)

from localization import Localization, Translator, SUPPORTED_LANGUAGES
from callbacks import (
    handle_clan,
    handle_search,
    handle_general,
    handle_weapons,
    handle_ranked_solo,
    handle_ranked_team,
    handle_legend_stats,
    handle_legend_details,
    handle_ranked_team_detail,
    handle_legend_personal_stats,
    handle_player_legend_details,
)

from scheduler.asyncio import Scheduler

load_dotenv()

API_ID = environ.get("API_ID")
API_KEY = environ.get("API_KEY")
API_HASH = environ.get("API_HASH")
BOT_TOKEN = environ.get("BOT_TOKEN")

FLOOD_WAIT_SECONDS = 60

bot = Client("brawlhalla", API_ID, API_HASH, bot_token=BOT_TOKEN)
brawl = Brawlhalla(API_KEY)
cache = Cache(180)
legends = Legends(brawl)
localization = Localization()
users_settings = UserSettings()


def user_handling(f):
    @wraps(f)
    async def wrapped(bot: Client, update, *args, **kwargs):
        time_now = time()
        user_id = update.from_user.id
        is_message = isinstance(update, Message)

        lang = users_settings.get_user(
            user_id, "language", update.from_user.language_code
        )
        translate = localization.get_translator(lang)

        time_blocked = users_settings.get_user(user_id, "time_blocked")

        if time_blocked:
            if time_now - time_blocked < FLOOD_WAIT_SECONDS:
                return
            users_settings.del_user(user_id, "time_blocked")

        time_last = users_settings.get_user(user_id, "time_last")
        if is_message and time_last and time_now - time_last < 1:
            users_settings.set_user(
                user_id,
                "time_blocked",
                time_now,
            )
            await bot.send_message(
                update.chat.id, translate.error_flood_wait(FLOOD_WAIT_SECONDS)
            )
            return

        users_settings.set_user(user_id, "time_last", time_now)

        try:
            return await f(
                bot,
                update,
                translate,
                *args,
                **kwargs,
            )
        except Exception:
            return await bot.send_message(
                update.from_user.id,
                translate.error_generic(error=traceback.format_exc()),
                reply_markup=Keyboard.issues(translate),
            )

    return wrapped


@bot.on_message(filters.command("start"))
@user_handling
async def start(_: Client, message: Message, translate: Translator):
    await message.reply(
        translate.welcome(
            name=escape(message.from_user.first_name),
        ),
        reply_markup=Keyboard.start(translate),
    )


@bot.on_message(filters.command(get_localized_commands("search", localization)))
@user_handling
async def search_player(_: Client, message: Message, translate: Translator):
    await handle_search(brawl, cache, legends, translate, message)


@bot.on_message(filters.command("id"))
@user_handling
async def player_id(_: Client, message: Message, translate: Translator):
    if len(message.command) < 2 or not message.command[1].isnumeric():
        await message.reply(translate.usage_id())
        return

    brawlhalla_id = message.command[1]

    await handle_general(
        brawl,
        brawlhalla_id,
        cache,
        legends,
        translate,
        message,
    )


@bot.on_message(filters.command("me"))
@user_handling
async def player_me(_: Client, message: Message, translate: Translator):
    brawlhalla_id = users_settings.get_user(message.from_user.id, "me", None)
    if brawlhalla_id is None:
        await message.reply(translate.error_missing_default_player())
        return
    await handle_general(
        brawl,
        brawlhalla_id,
        cache,
        legends,
        translate,
        message,
    )


@bot.on_message(filters.command("legend"))
@user_handling
async def legend(_: Client, message: Message, translate: Translator):
    if len(message.command) < 2:
        await handle_legend_stats(legends, translate, message)
        return
    query = escape(" ".join(message.command[1:]).lower())
    if await is_query_invalid(query, message, translate):
        return
    for legend in legends.all:
        if legend.legend_name_key == query:
            await handle_legend_details(legend, translate, message)
            return

    await message.reply(translate.error_legend_not_found(query))


@bot.on_message(filters.command(get_localized_commands("weapons", localization)))
@user_handling
async def weapon(_: Client, message: Message, translate: Translator):
    len_commands = len(message.command)

    if len_commands < 2:
        await handle_weapons(legends, message, translate)
        return

    if len_commands == 2:
        weapon = escape(message.command[1].lower())
        if await is_query_invalid(weapon, message, translate):
            return
        if weapon not in legends.weapons:
            await message.reply(translate.error_weapon_not_found(weapon))
            return
        await handle_weapons(legends, message, translate, weapon)
        return

    weapons = [
        escape(message.command[1].lower()),
        escape(message.command[2].lower()),
    ]

    weapons_set = set(weapons)

    for legend in legends.all:
        legend_weapons = set([legend.weapon_one, legend.weapon_two])
        if weapons_set.issubset(legend_weapons):
            await handle_legend_details(legend, translate, message)
            return
    await message.reply(translate.error_weapon_not_found(" ".join(weapons)))


@bot.on_message(filters.command(get_localized_commands("missing", localization)))
@user_handling
async def missing_weapons(_: Client, message: Message, translate: Translator):
    weapon = None
    if len(message.command) > 1:
        weapon = escape(message.command[1].lower())
        if await is_query_invalid(weapon, message, translate):
            return

    weapons = set(f"{legend.weapon_one}_{legend.weapon_two}" for legend in legends.all)
    missing = []
    for combination in combinations(legends.weapons, 2):
        w1, w2 = combination
        if f"{w1}_{w2}" in weapons or f"{w2}_{w1}" in weapons:
            continue
        if weapon is None or weapon == w1 or weapon == w2:
            missing.append(f"• {combination[0]} - {combination[1]}")

    if not missing:
        await message.reply(
            translate.error_missing_weapons_combination_not_found(weapon)
        )
        return

    text = "\n".join(missing)
    await message.reply(
        translate.results_missing_weapons_combination(text)
        if weapon is None
        else translate.results_missing_weapons_combination_with_weapon(
            weapon=weapon.capitalize(),
            weapons=text,
        )
    )


@bot.on_message(filters.command(get_localized_commands("language", localization)))
@user_handling
async def language_command(_: Client, message: Message, translate: Translator):
    await message.reply_text(
        translate.description_language(), reply_markup=Keyboard.languages()
    )


@bot.on_callback_query(filters.regex(f"^(\\d+)_{View.SEARCH}_(.+)$"))
@user_handling
async def search_player_page(_: Client, callback: CallbackQuery, translate: Translator):
    current_page, query = callback.matches[0].groups()
    await handle_search(
        brawl,
        cache,
        legends,
        translate,
        callback,
        query=query,
        current_page=int(current_page),
    )



@bot.on_callback_query(filters.regex(r"^(\d+)_team_(\d+)$"))
@user_handling
async def search_team_page(_: Client, callback: CallbackQuery, translate: Translator):
    current_page, brawlhalla_id = callback.matches[0].groups()
    await handle_ranked_team(
        brawl,
        brawlhalla_id,
        callback,
        cache,
        translate,
        current_page=int(current_page),
        is_page_view=True,
    )


@bot.on_callback_query(filters.regex(f"^{View.GENERAL}_(\\d+)$"))
@user_handling
async def player_general_callback(
    _: Client, callback: CallbackQuery, translate: Translator
):
    brawlhalla_id = int(callback.matches[0].group(1))
    await handle_general(brawl, brawlhalla_id, cache, legends, translate, callback)


@bot.on_callback_query(filters.regex(f"^{View.RANKED_SOLO}_(\\d+)$"))
@user_handling
async def player_ranked_solo_callback(
    _: Client, callback: CallbackQuery, translate: Translator
):
    brawlhalla_id = int(callback.matches[0].group(1))
    await handle_ranked_solo(brawl, brawlhalla_id, callback, cache, translate)


@bot.on_callback_query(filters.regex(f"^{View.RANKED_TEAM}_(\\d+)$"))
@user_handling
async def player_ranked_team_callback(
    _: Client, callback: CallbackQuery, translate: Translator
):
    brawlhalla_id = int(callback.matches[0].group(1))
    await handle_ranked_team(brawl, brawlhalla_id, callback, cache, translate)


@bot.on_callback_query(filters.regex(f"^{View.CLAN}_(\\d+)$"))
@user_handling
async def player_clan_callback(
    _: Client, callback: CallbackQuery, translate: Translator
):
    brawlhalla_id = callback.matches[0].group(1)
    player = cache.get(f"{View.GENERAL}_{brawlhalla_id}")

    if player is None:
        try:
            player = await brawl.get_stats(brawlhalla_id)
        except ServiceUnavailable:
            await callback.answer(translate.error_api_offline(), show_alert=True)
            return

    if player.clan is None:
        await callback.answer(translate.error_no_clan_data(), show_alert=True)
        return

    await handle_clan(brawl, player.clan.clan_id, callback, cache, translate)


@bot.on_callback_query(filters.regex(f"^(\\d+)_{View.CLAN}_(\\d+)$"))
@user_handling
async def search_clan_page(_: Client, callback: CallbackQuery, translate: Translator):
    regex = callback.matches[0]
    current_page = int(regex.group(1))
    clan_id = regex.group(2)

    await handle_clan(
        brawl,
        clan_id,
        callback,
        cache,
        translate,
        current_page=current_page,
    )


@bot.on_callback_query(filters.regex(f"^(\\d+)?_?{View.LEGEND}_(\\d+)$"))
@user_handling
async def search_legend_personal_page(
    _: Client, callback: CallbackQuery, translate: Translator
):
    current_page, brawlhalla_id = callback.matches[0].groups()

    await handle_legend_personal_stats(
        brawl,
        brawlhalla_id,
        callback,
        cache,
        legends,
        translate,
        current_page=int(current_page or "0"),
    )

@bot.on_callback_query(filters.regex(f"^{View.LEGEND}$"))
@user_handling
async def player_legend_list_callback(
    _: Client, callback: CallbackQuery, translate: Translator
):
    await handle_legend_stats(legends, translate, callback)


@bot.on_callback_query(filters.regex(f"^{View.LEGEND}_stats_(\\d+)$"))
@user_handling
async def player_legend_details_callback(
    _: Client, callback: CallbackQuery, translate: Translator
):
    legend_id = callback.matches[0].group(1)
    await handle_legend_details(await legends.get(legend_id), translate, callback)


@bot.on_callback_query(filters.regex(f"^(\\d+)_{View.LEGEND}_?([az]+)?$"))
@user_handling
async def search_legend_page(_: Client, callback: CallbackQuery, translate: Translator):
    current_page, weapon = callback.matches[0].groups()
    await handle_legend_stats(
        legends,
        translate,
        callback,
        weapon=weapon,
        current_page=int(current_page or "0"),
    )


@bot.on_callback_query(filters.regex(f"^(\\d+)_{View.LEGEND}_(\\d+)$"))
@user_handling
async def player_legend_stats_callback(
    _: Client, callback: CallbackQuery, translate: Translator
):
    current_page, brawlhalla_id = callback.matches[0].groups()

    await handle_legend_personal_stats(
        brawl,
        brawlhalla_id,
        callback,
        cache,
        legends,
        translate,
        current_page=int(current_page),
    )


@bot.on_callback_query(filters.regex(f"^{View.LEGEND}_(\\d+)_(\\d+)$"))
@user_handling
async def player_legend_detail_callback(
    _: Client, callback: CallbackQuery, translate: Translator
):
    brawlhalla_id, legend_id = callback.matches[0].groups()

    await handle_player_legend_details(
        brawl,
        brawlhalla_id,
        await legends.get(legend_id),
        callback,
        cache,
        translate,
    )


@bot.on_callback_query(filters.regex(f"^{View.RANKED_TEAM_DETAIL}_(\\d+)_(\\d+)$"))
@user_handling
async def player_ranked_team_detail_callback(
    _: Client, callback: CallbackQuery, translate: Translator
):
    brawlhalla_id_one, brawlhalla_id_two = callback.matches[0].groups()

    await handle_ranked_team_detail(
        brawl, int(brawlhalla_id_one), int(brawlhalla_id_two), callback, cache, translate
    )


@bot.on_callback_query(lambda _, x: x.data[7:] in legends.weapons)
@user_handling
async def legend_weapon_callback(
    _: Client, callback: CallbackQuery, translate: Translator
):
    weapon = callback.data[7:]
    await handle_weapons(legends, callback, translate, weapon)


@bot.on_callback_query(filters.regex(f"^{View.WEAPON}$"))
@user_handling
async def legend_weapon_list_callback(
    _: Client, callback: CallbackQuery, translate: Translator
):
    await handle_weapons(legends, callback, translate)


@bot.on_callback_query(filters.regex(r"^set_(\d+)$"))
@user_handling
async def set_default_callback(
    _: Client, callback: CallbackQuery, translate: Translator
):
    brawlhalla_id = int(callback.matches[0].group(1))
    users_settings.set_user(callback.from_user.id, "me", brawlhalla_id)
    await callback.answer(translate.status_default_player_set(), show_alert=True)


@bot.on_callback_query(filters.regex(r"^(en|it)$"))
@user_handling
async def language_callback(_: Client, callback: CallbackQuery, translate: Translator):
    lang = callback.data

    if lang == users_settings.get_user(callback.from_user.id, "language"):
        await callback.answer(translate.status_language_unchanged(), show_alert=True)
    else:
        users_settings.set_user(callback.from_user.id, "language", lang)
        translate = localization.get_translator(lang)
        await callback.answer(translate.status_language_changed(), show_alert=True)
        await callback.message.delete()


@bot.on_callback_query(filters.regex(r"^close$"))
async def close_callback(_: Client, callback: CallbackQuery):
    await callback.message.delete()


@bot.on_inline_query()
@user_handling
async def inline_query_handler(
    _: Client,
    inline_query: InlineQuery,
    translate: Translator,
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


async def set_commands(bot: Client):
    for lang_code in SUPPORTED_LANGUAGES:
        translate = localization.get_translator(lang_code)
        await bot.set_bot_commands(
            [
                BotCommand("start", translate.description_start()),
                BotCommand(translate.search(), translate.description_search()),
                BotCommand("id", translate.description_id()),
                BotCommand("me", translate.description_me()),
                BotCommand("legend", translate.description_legend()),
                BotCommand(translate.weapons(), translate.description_weapons()),
                BotCommand(translate.missing(), translate.description_missing()),
                BotCommand(translate.language(), translate.description_language()),
            ],
            language_code=lang_code,
        )


async def main():
    schedule = Scheduler()
    schedule.cyclic(timedelta(hours=1), cache.clear)

    await legends.refresh_legends()
    await bot.start()
    await set_commands(bot)
    await idle()
    await bot.stop()


bot.run(main())
