import asyncio
import traceback
from os import environ
from plate import Plate
from cache import Cache
from html import escape
from functools import wraps
from dotenv import load_dotenv
from datetime import timedelta
from utils import get_current_page
from pyrogram import Client, filters
from keyboards import Keyboard, View
from brawlhalla_api import Brawlhalla
from user_settings import UserSettings
from pyrogram.methods.utilities.idle import idle
from pyrogram.types import Message, CallbackQuery, BotCommand
from callbacks import (
    handle_clan,
    handle_search,
    handle_general,
    handle_legend,
    handle_ranked_solo,
    handle_ranked_team,
    handle_legend_detail,
    handle_ranked_team_detail,
)

from scheduler.asyncio import Scheduler

SUPPORTED_LANGUAGES = {"it": "it_IT", "en": "en_US"}


plate = Plate("src/locales")

load_dotenv()

API_ID = environ.get("API_ID")
API_KEY = environ.get("API_KEY")
API_HASH = environ.get("API_HASH")
BOT_TOKEN = environ.get("BOT_TOKEN")

brawl = Brawlhalla(API_KEY)
bot = Client("Brawltool", API_ID, API_HASH, bot_token=BOT_TOKEN)

cache = Cache(180)

users_settings = UserSettings()


def user_language(f):
    @wraps(f)
    async def wrapped(bot: Client, update, *args, **kwargs):
        user_id = update.from_user.id
        lang = users_settings.get_user(
            user_id, "language", update.from_user.language_code
        )

        translate = plate.get_translator(SUPPORTED_LANGUAGES.get(lang, "en_US"))
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
                translate("generic_error", error=traceback.format_exc()),
                reply_markup=Keyboard.issues(translate),
            )

    return wrapped


@bot.on_message(filters.command("start"))
@user_language
async def start(_: Client, message: Message, translate: Plate):
    await message.reply(
        translate(
            "welcome",
            name=escape(message.from_user.first_name),
        ),
    )


@bot.on_message(filters.command(["search", "cerca"]))
@user_language
async def search_player(_: Client, message: Message, translate: Plate):
    await handle_search(brawl, cache, translate, message=message)


@bot.on_message(filters.command("id"))
@user_language
async def player_id(_: Client, message: Message, translate: Plate):
    if len(message.command) < 2 or not message.command[1].isnumeric():
        await message.reply(translate("player_id_usage"))
        return

    brawlhalla_id = int(message.command[1])

    await handle_general(brawl, brawlhalla_id, cache, translate, message=message)


@bot.on_message(filters.command("me"))
@user_language
async def player_me(_: Client, message: Message, translate: Plate):
    brawlhalla_id = users_settings.get_user(message.from_user.id, "me", None)
    if brawlhalla_id is None:
        await message.reply(translate("player_me_error"))
        return
    await handle_general(brawl, brawlhalla_id, cache, translate, message=message)


@bot.on_callback_query(filters.regex(r"^button_(next|prev)$"))
@user_language
async def search_player_page(_: Client, callback: CallbackQuery, translate: Plate):
    await handle_search(brawl, cache, translate, callback=callback)


@bot.on_callback_query(filters.regex(r"^legend_(next|prev)_(\d+)$"))
@user_language
async def search_legend_page(_: Client, callback: CallbackQuery, translate: Plate):
    current_page, brawlhalla_id = get_current_page(callback, brawlhalla_id=True)

    await handle_legend(
        brawl,
        brawlhalla_id,
        callback,
        cache,
        translate,
        current_page=current_page,
    )


@bot.on_callback_query(filters.regex(r"^team_(next|prev)_(\d+)$"))
@user_language
async def search_team_page(_: Client, callback: CallbackQuery, translate: Plate):
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


@bot.on_callback_query(filters.regex(r"^clan_(next|prev)_(\d+)$"))
@user_language
async def search_clan_page(_: Client, callback: CallbackQuery, translate: Plate):
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
async def player_general_callback(_: Client, callback: CallbackQuery, translate: Plate):
    brawlhalla_id = int(callback.matches[0].group(1))
    await handle_general(brawl, brawlhalla_id, cache, translate, callback=callback)


@bot.on_callback_query(filters.regex(f"^{View.RANKED_SOLO}_(\\d+)$"))
@user_language
async def player_ranked_solo_callback(
    _: Client, callback: CallbackQuery, translate: Plate
):
    brawlhalla_id = int(callback.matches[0].group(1))
    await handle_ranked_solo(brawl, brawlhalla_id, callback, cache, translate)


@bot.on_callback_query(filters.regex(f"^{View.RANKED_TEAM}_(\\d+)$"))
@user_language
async def player_ranked_team_callback(
    _: Client, callback: CallbackQuery, translate: Plate
):
    brawlhalla_id = int(callback.matches[0].group(1))
    await handle_ranked_team(brawl, brawlhalla_id, callback, cache, translate)


@bot.on_callback_query(filters.regex(f"^{View.CLAN}_(\\d+)$"))
@user_language
async def player_clan_callback(_: Client, callback: CallbackQuery, translate: Plate):
    brawlhalla_id = int(callback.matches[0].group(1))
    player = cache.get(f"{View.GENERAL}_{brawlhalla_id}")

    if player is None:
        player = await brawl.get_stats(brawlhalla_id)

    if player.clan is None:
        await callback.answer(translate("no_clan_data"), show_alert=True)
        return

    await handle_clan(brawl, player.clan.clan_id, callback, cache, translate)


@bot.on_callback_query(filters.regex(f"^{View.LEGEND}_(\\d+)$"))
@user_language
async def player_legend_callback(_: Client, callback: CallbackQuery, translate: Plate):
    brawlhalla_id = int(callback.matches[0].group(1))
    await handle_legend(brawl, brawlhalla_id, callback, cache, translate)


@bot.on_callback_query(filters.regex(f"^{View.LEGEND}_(\\d+)_(\\d+)$"))
@user_language
async def player_legend_detail_callback(
    _: Client, callback: CallbackQuery, translate: Plate
):
    regex = callback.matches[0]
    brawlhalla_id = int(regex.group(1))
    legend_id = int(regex.group(2))

    await handle_legend_detail(
        brawl, brawlhalla_id, legend_id, callback, cache, translate
    )


@bot.on_callback_query(filters.regex(f"^{View.RANKED_TEAM_DETAIL}_(\\d+)_(\\d+)$"))
@user_language
async def player_ranked_team_detail_callback(
    _: Client, callback: CallbackQuery, translate: Plate
):
    regex = callback.matches[0]
    brawlhalla_id_one = int(regex.group(1))
    brawlhalla_id_two = int(regex.group(2))

    await handle_ranked_team_detail(
        brawl, brawlhalla_id_one, brawlhalla_id_two, callback, cache, translate
    )


@bot.on_callback_query(filters.regex(r"^set_(\d+)$"))
@user_language
async def set_default_callback(_: Client, callback: CallbackQuery, translate: Plate):
    brawlhalla_id = int(callback.matches[0].group(1))
    users_settings.set_user(callback.from_user.id, "me", brawlhalla_id)
    await callback.answer(translate("player_me"), show_alert=True)


@bot.on_message(filters.command(["lingua", "language"]))
@user_language
async def language_command(_: Client, message: Message, translate: Plate):
    await message.reply_text(
        translate("language_description"), reply_markup=Keyboard.languages()
    )


@bot.on_callback_query(filters.regex("en|it"))
@user_language
async def language_callback(_: Client, callback: CallbackQuery, translate: Plate):
    lang = callback.data

    if lang == users_settings.get_user(callback.from_user.id, "language"):
        await callback.message.edit(translate("language_unchanged"))
    else:
        users_settings.set_user(callback.from_user.id, "language", lang)
        translate = plate.get_translator(
            SUPPORTED_LANGUAGES.get(lang, "en_US"),
        )
        await callback.message.edit(translate("language_changed"))

    await asyncio.sleep(3)
    await callback.message.delete()


@bot.on_callback_query(filters.regex("^close$"))
async def close_callback(_: Client, callback: CallbackQuery):
    await callback.message.delete()


async def set_commands(bot: Client):
    for lang_code, lang_locale in SUPPORTED_LANGUAGES.items():
        translate = plate.get_translator(lang_locale)
        await bot.set_bot_commands(
            [
                BotCommand("start", translate("start_description")),
                BotCommand(translate("search"), translate("search_description")),
                BotCommand("id", translate("id_description")),
                BotCommand("me", translate("me_description")),
                BotCommand(translate("language"), translate("language_description")),
            ],
            language_code=lang_code,
        )


async def main():
    schedule = Scheduler()
    schedule.cyclic(timedelta(hours=1), cache.clear)

    await bot.start()
    await set_commands(bot)
    await idle()
    await bot.stop()


bot.run(main())
