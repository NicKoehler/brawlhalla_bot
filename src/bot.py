import traceback

from os import environ
from html import escape
from functools import wraps
from dotenv import load_dotenv
from datetime import timedelta
from itertools import combinations
from pyrogram import Client, filters
from keyboards import Keyboard, View
from brawlhalla_api import Brawlhalla
from helpers.cache import Cache, Legends
from helpers.user_settings import UserSettings
from pyrogram.methods.utilities.idle import idle
from helpers.utils import get_current_page, is_query_invalid
from pyrogram.types import Message, CallbackQuery, BotCommand
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
    handle_legend_personal_details,
)

from scheduler.asyncio import Scheduler

load_dotenv()

API_ID = environ.get("API_ID")
API_KEY = environ.get("API_KEY")
API_HASH = environ.get("API_HASH")
BOT_TOKEN = environ.get("BOT_TOKEN")

bot = Client("Brawltool", API_ID, API_HASH, bot_token=BOT_TOKEN)
brawl = Brawlhalla(API_KEY)
cache = Cache(180)
legends = Legends(brawl)
localization = Localization()
users_settings = UserSettings()


def user_language(f):
    @wraps(f)
    async def wrapped(bot: Client, update, *args, **kwargs):
        user_id = update.from_user.id
        lang = users_settings.get_user(
            user_id, "language", update.from_user.language_code
        )
        translate = localization.get_translator(lang)
        try:
            return await f(
                bot,
                update,
                translate,
                *args,
                **kwargs,
            )
        except Exception:
            if isinstance(update, CallbackQuery):
                update = update.message
            return await bot.send_message(
                update.chat.id,
                translate.error_generic(error=traceback.format_exc()),
                reply_markup=Keyboard.issues(translate),
            )

    return wrapped


@bot.on_message(filters.command("start"))
@user_language
async def start(_: Client, message: Message, translate: Translator):
    await message.reply(
        translate.welcome(
            name=escape(message.from_user.first_name),
        )
    )


@bot.on_message(filters.command(["search", "cerca"]))
@user_language
async def search_player(_: Client, message: Message, translate: Translator):
    await handle_search(brawl, cache, legends, translate, message)


@bot.on_message(filters.command("id"))
@user_language
async def player_id(_: Client, message: Message, translate: Translator):
    if len(message.command) < 2 or not message.command[1].isnumeric():
        await message.reply(translate.usage_id())
        return

    brawlhalla_id = int(message.command[1])

    await handle_general(
        brawl,
        brawlhalla_id,
        cache,
        legends,
        translate,
        message,
    )


@bot.on_message(filters.command("me"))
@user_language
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
@user_language
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


@bot.on_message(filters.command(["weapons", "armi"]))
@user_language
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


@bot.on_message(filters.command(["missing", "mancanti"]))
@user_language
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


@bot.on_callback_query(filters.regex(r"^button_(next|prev)$"))
@user_language
async def search_player_page(_: Client, callback: CallbackQuery, translate: Translator):
    await handle_search(brawl, cache, legends, translate, callback)


@bot.on_callback_query(filters.regex(f"^{View.LEGEND}_(next|prev)_(\\d+)$"))
@user_language
async def search_legend_personal_page(
    _: Client, callback: CallbackQuery, translate: Translator
):
    current_page, brawlhalla_id = get_current_page(callback, get_second_param=True)

    await handle_legend_personal_stats(
        brawl,
        brawlhalla_id,
        callback,
        cache,
        legends,
        translate,
        current_page=current_page,
    )


@bot.on_callback_query(filters.regex(f"^{View.LEGEND}_(next|prev)_?(\\w+)?$"))
@user_language
async def search_legend_page(_: Client, callback: CallbackQuery, translate: Translator):
    current_page = get_current_page(callback)
    weapon = None
    if len(callback.matches[0].groups()) > 1:
        weapon = callback.matches[0].group(2)
    await handle_legend_stats(
        legends, translate, callback, weapon=weapon, current_page=current_page
    )


@bot.on_callback_query(filters.regex(r"^team_(next|prev)_(\d+)$"))
@user_language
async def search_team_page(_: Client, callback: CallbackQuery, translate: Translator):
    current_page, brawlhalla_id = get_current_page(callback, get_second_param=True)

    await handle_ranked_team(
        brawl,
        brawlhalla_id,
        callback,
        cache,
        translate,
        current_page=current_page,
        is_page_view=True,
    )


@bot.on_callback_query(filters.regex(f"^{View.CLAN}_(next|prev)_(\\d+)$"))
@user_language
async def search_clan_page(_: Client, callback: CallbackQuery, translate: Translator):
    current_page, clan_id = get_current_page(callback, get_second_param=True)

    await handle_clan(
        brawl,
        clan_id,
        callback,
        cache,
        translate,
        current_page=current_page,
    )


@bot.on_callback_query(filters.regex(f"^{View.GENERAL}_(\\d+)$"))
@user_language
async def player_general_callback(
    _: Client, callback: CallbackQuery, translate: Translator
):
    brawlhalla_id = int(callback.matches[0].group(1))
    await handle_general(brawl, brawlhalla_id, cache, legends, translate, callback)


@bot.on_callback_query(filters.regex(f"^{View.RANKED_SOLO}_(\\d+)$"))
@user_language
async def player_ranked_solo_callback(
    _: Client, callback: CallbackQuery, translate: Translator
):
    brawlhalla_id = int(callback.matches[0].group(1))
    await handle_ranked_solo(brawl, brawlhalla_id, callback, cache, translate)


@bot.on_callback_query(filters.regex(f"^{View.RANKED_TEAM}_(\\d+)$"))
@user_language
async def player_ranked_team_callback(
    _: Client, callback: CallbackQuery, translate: Translator
):
    brawlhalla_id = int(callback.matches[0].group(1))
    await handle_ranked_team(brawl, brawlhalla_id, callback, cache, translate)


@bot.on_callback_query(filters.regex(f"^{View.CLAN}_(\\d+)$"))
@user_language
async def player_clan_callback(
    _: Client, callback: CallbackQuery, translate: Translator
):
    brawlhalla_id = int(callback.matches[0].group(1))
    player = cache.get(f"{View.GENERAL}_{brawlhalla_id}")

    if player is None:
        player = await brawl.get_stats(brawlhalla_id)

    if player.clan is None:
        await callback.answer(translate.error_no_clan_data(), show_alert=True)
        return

    await handle_clan(brawl, player.clan.clan_id, callback, cache, translate)


@bot.on_callback_query(filters.regex(f"^{View.LEGEND}$"))
@user_language
async def player_legend_list_callback(
    _: Client, callback: CallbackQuery, translate: Translator
):
    await handle_legend_stats(legends, translate, callback)


@bot.on_callback_query(filters.regex(f"^{View.LEGEND}_(\\d+)$"))
@user_language
async def player_legend_stats_callback(
    _: Client, callback: CallbackQuery, translate: Translator
):
    brawlhalla_id = int(callback.matches[0].group(1))
    await handle_legend_personal_stats(
        brawl, brawlhalla_id, callback, cache, legends, translate
    )


@bot.on_callback_query(filters.regex(f"^{View.LEGEND}_(\\d+)_(\\d+)$"))
@user_language
async def player_legend_detail_callback(
    _: Client, callback: CallbackQuery, translate: Translator
):
    regex = callback.matches[0]
    brawlhalla_id = int(regex.group(1))
    legend_id = int(regex.group(2))
    await handle_legend_personal_details(
        brawl, brawlhalla_id, await legends.get(legend_id), callback, cache, translate
    )


@bot.on_callback_query(filters.regex(f"^{View.LEGEND}_stats_(\\d+)$"))
@user_language
async def player_legend_details_callback(
    _: Client, callback: CallbackQuery, translate: Translator
):
    regex = callback.matches[0]
    legend_id = int(regex.group(1))
    await handle_legend_details(await legends.get(legend_id), translate, callback)


@bot.on_callback_query(filters.regex(f"^{View.RANKED_TEAM_DETAIL}_(\\d+)_(\\d+)$"))
@user_language
async def player_ranked_team_detail_callback(
    _: Client, callback: CallbackQuery, translate: Translator
):
    regex = callback.matches[0]
    brawlhalla_id_one = int(regex.group(1))
    brawlhalla_id_two = int(regex.group(2))

    await handle_ranked_team_detail(
        brawl, brawlhalla_id_one, brawlhalla_id_two, callback, cache, translate
    )


@bot.on_callback_query(lambda _, x: x.data[7:] in legends.weapons)
@user_language
async def legend_weapon_callback(
    _: Client, callback: CallbackQuery, translate: Translator
):
    weapon = callback.data[7:]
    await handle_weapons(legends, callback, translate, weapon)


@bot.on_callback_query(filters.regex(f"^{View.WEAPON}$"))
@user_language
async def legend_weapon_list_callback(
    _: Client, callback: CallbackQuery, translate: Translator
):
    await handle_weapons(legends, callback, translate)


@bot.on_callback_query(filters.regex(r"^set_(\d+)$"))
@user_language
async def set_default_callback(
    _: Client, callback: CallbackQuery, translate: Translator
):
    brawlhalla_id = int(callback.matches[0].group(1))
    users_settings.set_user(callback.from_user.id, "me", brawlhalla_id)
    await callback.answer(translate.status_default_player_set(), show_alert=True)


@bot.on_message(filters.command(["lingua", "language"]))
@user_language
async def language_command(_: Client, message: Message, translate: Translator):
    await message.reply_text(
        translate.description_language(), reply_markup=Keyboard.languages()
    )


@bot.on_callback_query(filters.regex(r"^(en|it)$"))
@user_language
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
