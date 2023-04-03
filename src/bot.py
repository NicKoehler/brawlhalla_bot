import asyncio
from math import ceil
from os import environ
from plate import Plate
from cache import Cache
from html import escape
from functools import wraps
from dotenv import load_dotenv
from datetime import timedelta
from keyboards import Keyboard, View
from pyrogram import Client, filters
from brawlhalla_api import Brawlhalla
from pyrogram.types import Message, CallbackQuery
from pyrogram.methods.utilities.idle import idle
from callbacks import handle_general, handle_rankedsolo

from scheduler.asyncio import Scheduler

plate = Plate("src/locales")

load_dotenv()

API_ID = environ.get("API_ID")
API_KEY = environ.get("API_KEY")
API_HASH = environ.get("API_HASH")
BOT_TOKEN = environ.get("BOT_TOKEN")

brawl = Brawlhalla(API_KEY)
bot = Client("Brawltool", API_ID, API_HASH, bot_token=BOT_TOKEN)

cache = Cache(180)


def user_language(f):
    @wraps(f)
    async def wrapped(bot: Client, update, *args, **kwargs):
        match update.from_user.language_code:
            case "it":
                lang = "it_IT"
            case "es":
                lang = "es_ES"
            case _:
                lang = "en_US"
        lang = plate.get_translator(lang)
        return await f(bot, update, lang, *args, **kwargs)

    return wrapped


@bot.on_message(filters.command(["search", "cerca"]))
@user_language
async def search_player(_: Client, message: Message, translate: Plate):
    query = escape(" ".join(message.command[1:]))

    if not query:
        await message.reply(translate("search_usage"))
        return

    page_limit = 10
    results = cache.get(query)
    if results is None:
        results = await brawl.get_rankings(name=query)
        if not results:
            await message.reply(translate("search_results_error", query=query))
            return
        cache.add(query, results)

    current_page = 0
    total_pages = ceil(len(results) / page_limit)

    await message.reply(
        translate(
            "search_results",
            query=query,
            current=current_page + 1,
            total=total_pages,
        ),
        reply_markup=Keyboard.search_player(
            results, current_page, total_pages - 1, page_limit, translate
        ),
    )


@bot.on_callback_query(filters.regex(r"button_(next|prev)"))
@user_language
async def search_player_page(_: Client, callback: CallbackQuery, translate: Plate):
    page_limit = 10
    n, original_query, pages = callback.message.text.split("\n")
    results = cache.get(original_query)

    if results is None:
        results = await brawl.get_rankings(name=original_query)
        if not results:
            await callback.message.reply(
                translate("search_results_error", query=original_query)
            )
            return
        cache.add(original_query, results)

    current_page = int(pages.split("/")[0])
    current_page += 1 if callback.matches[0].group(1) == "next" else -1

    total_pages = ceil(len(results) / page_limit)

    await callback.message.edit(
        translate(
            "search_results",
            query=original_query,
            current=current_page,
            total=total_pages,
        ),
        reply_markup=Keyboard.search_player(
            results, current_page - 1, total_pages - 1, page_limit, translate
        ),
    )


@bot.on_callback_query(
    filters.regex(f"({View.GENERAL}|{View.RANKED_SOLO}|{View.RANKED_TEAM})_(\d+)")
)
@user_language
async def player_callback(_: Client, callback: CallbackQuery, translate: Plate):
    callback.from_user.language_code
    regex = callback.matches[0]
    view_mode = View(regex.group(1))
    brawlhalla_id = regex.group(2)
    player = cache.get(callback.data)

    match view_mode:
        case View.GENERAL:
            await handle_general(
                brawl, brawlhalla_id, player, callback, cache, translate
            )
        case View.RANKED_SOLO:
            await handle_rankedsolo(
                brawl, brawlhalla_id, player, callback, cache, translate
            )


@bot.on_callback_query(filters.regex("close"))
async def close_callback(_: Client, callback: CallbackQuery):
    await callback.message.delete()


async def main():
    schedule = Scheduler()
    schedule.cyclic(timedelta(hours=1), cache.clear)
    await bot.start()
    await idle()
    await bot.stop()


bot.run(main())
