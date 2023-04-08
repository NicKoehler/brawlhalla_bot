import asyncio
import traceback

from os import environ
from html import escape
from functools import wraps
from dotenv import load_dotenv
from datetime import timedelta
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


localization = Localization()
brawl = Brawlhalla(API_KEY)
bot = Client("Brawltool", API_ID, API_HASH, bot_token=BOT_TOKEN)
cache = Cache(180)
legends = Legends(brawl)
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
    await handle_search(brawl, cache, legends, translate, message=message)


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
        message=message,
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
        message=message,
    )


@bot.on_message(filters.command("legend"))
@user_language
async def player_legend(_: Client, message: Message, translate: Translator):
    if len(message.command) < 2:
        await handle_legend_stats(legends, translate, message=message)
        return
    query = escape(" ".join(message.command[1:]).lower())
    if await is_query_invalid(query, message, translate):
        return
    for legend in legends.all():
        if legend.legend_name_key == query:
            await handle_legend_details(legend, translate, message=message)
            return

    await message.reply(translate.error_legend_not_found(query))


@bot.on_callback_query(filters.regex(r"^button_(next|prev)$"))
@user_language
async def search_player_page(_: Client, callback: CallbackQuery, translate: Translator):
    await handle_search(brawl, cache, legends, translate, callback=callback)


@bot.on_callback_query(filters.regex(f"^{View.LEGEND}_(next|prev)_(\\d+)$"))
@user_language
async def search_legend_personal_page(
    _: Client, callback: CallbackQuery, translate: Translator
):
    current_page, brawlhalla_id = get_current_page(callback, brawlhalla_id=True)

    await handle_legend_personal_stats(
        brawl,
        brawlhalla_id,
        callback,
        cache,
        legends,
        translate,
        current_page=current_page,
    )


@bot.on_callback_query(filters.regex(f"^{View.LEGEND}_(next|prev)$"))
@user_language
async def search_legend_page(_: Client, callback: CallbackQuery, translate: Translator):
    current_page = get_current_page(callback)
    await handle_legend_stats(
        legends, translate, callback=callback, current_page=current_page
    )


@bot.on_callback_query(filters.regex(r"^team_(next|prev)_(\d+)$"))
@user_language
async def search_team_page(_: Client, callback: CallbackQuery, translate: Translator):
    current_page, brawlhalla_id = get_current_page(callback, brawlhalla_id=True)

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
    current_page, clan_id = get_current_page(callback, clan_id=True)

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
    await handle_general(
        brawl,
        brawlhalla_id,
        cache,
        legends,
        translate,
        callback=callback,
    )


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
    await handle_legend_stats(legends, translate, callback=callback)


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
    await handle_legend_details(
        await legends.get(legend_id), translate, callback=callback
    )


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
        await callback.message.edit(translate.status_language_unchanged())
    else:
        users_settings.set_user(callback.from_user.id, "language", lang)
        translate = localization.get_translator(lang)
        await callback.message.edit(translate.status_language_changed())

    await asyncio.sleep(3)
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
