from math import ceil
from os import environ
from plate import Plate
from cache import Cache
from html import escape
from functools import wraps
from dotenv import load_dotenv
from datetime import timedelta
from pyrogram import Client, filters
from keyboards import Keyboard, View
from brawlhalla_api import Brawlhalla
from pyrogram.methods.utilities.idle import idle
from pyrogram.types import Message, CallbackQuery, BotCommand
from callbacks import (
    handle_clan,
    handle_general,
    handle_ranked_solo,
    handle_ranked_team,
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


def user_language(f):
    @wraps(f)
    async def wrapped(bot: Client, update, *args, **kwargs):
        translate = plate.get_translator(
            SUPPORTED_LANGUAGES.get(update.from_user.language_code, "en_US")
        )
        try:
            return await f(
                bot,
                update,
                translate,
                *args,
                **kwargs,
            )
        except Exception as e:
            if isinstance(update, CallbackQuery):
                update = update.message
            return await bot.send_message(
                update.chat.id,
                translate("generic_error", error=e),
                reply_markup=Keyboard.developer(translate("button_issue")),
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
    query = escape(" ".join(message.command[1:]))

    if not query:
        await message.reply(translate("search_usage"))
        return

    len_query = len(query)

    if len_query < 2 or len_query > 32:
        await message.reply(translate("length_error"))
        return

    results = cache.get(query)
    if results is None:
        results = await brawl.get_rankings(name=query)
        if not results:
            await message.reply(translate("search_results_error", query=query))
            return
        cache.add(query, results)

    if len(results) == 1:
        await handle_general(
            brawl, results[0].brawlhalla_id, None, message, cache, translate, bot
        )
        return

    page_limit = 10
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
    _, original_query, pages = callback.message.text.split("\n")
    results = cache.get(original_query)

    if results is None:
        results = await brawl.get_rankings(name=original_query)
        if not results:
            await callback.answer(
                translate("search_results_error", query=original_query), show_alert=True
            )
            await callback.message.delete()
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


@bot.on_callback_query(filters.regex(r"team_(next|prev)_(\d+)"))
@user_language
async def search_team_page(_: Client, callback: CallbackQuery, translate: Plate):
    page_limit = 10
    pages = callback.message.text.split("\n")[-1]
    current_page = int(pages.split("/")[0])
    current_page += 1 if callback.matches[0].group(1) == "next" else -1
    brawlhalla_id = int(callback.matches[0].group(2))

    player = cache.get(f"{View.RANKED_SOLO}_{brawlhalla_id}")
    if player is None:
        player = await brawl.get_ranked(brawlhalla_id)
        if not player or not player.teams:
            await callback.answer(
                translate("teams_results_error", team=brawlhalla_id),
                show_alert=True,
            )
            await callback.message.delete()
            return
        cache.add(f"{View.RANKED_SOLO}_{brawlhalla_id}", player)

    total_pages = ceil(len(player.teams) / page_limit)

    await callback.message.edit(
        translate(
            "teams_results",
            id=player.brawlhalla_id,
            name=player.name,
            current=current_page,
            total=total_pages,
        ),
        reply_markup=Keyboard.teams(
            player, current_page - 1, total_pages - 1, page_limit, translate
        ),
    )


@bot.on_callback_query(filters.regex(r"clan_(next|prev)_(\d+)"))
@user_language
async def search_clan_page(_: Client, callback: CallbackQuery, translate: Plate):
    page_limit = 10
    pages = callback.message.text.split("\n")[-1]
    current_page = int(pages.split("/")[0])
    current_page += 1 if callback.matches[0].group(1) == "next" else -1
    clan_id = int(callback.matches[0].group(2))

    clan = cache.get(f"{View.CLAN}_{clan_id}")
    if clan is None:
        clan = await brawl.get_clan(clan_id)
        cache.add(f"{View.CLAN}_{clan.clan_id}", clan)

    len_components = len(clan.components)
    total_pages = ceil(len_components / page_limit)

    await callback.message.edit(
        translate(
            "clan_stats",
            id=clan.clan_id,
            name=clan.clan_name,
            xp=clan.clan_xp,
            date=clan.clan_create_date,
            num=len_components,
            current=current_page,
            total=total_pages,
        ),
        reply_markup=Keyboard.clan_components(
            clan, current_page - 1, total_pages - 1, page_limit, translate
        ),
    )


@bot.on_callback_query(filters.regex(f"{View.GENERAL}_(\\d+)"))
@user_language
async def player_general_callback(_: Client, callback: CallbackQuery, translate: Plate):
    brawlhalla_id = int(callback.matches[0].group(1))
    player = cache.get(callback.data)

    await handle_general(
        brawl, brawlhalla_id, player, callback.message, cache, translate
    )


@bot.on_callback_query(filters.regex(f"{View.RANKED_SOLO}_(\\d+)"))
@user_language
async def player_ranked_solo_callback(
    _: Client, callback: CallbackQuery, translate: Plate
):
    brawlhalla_id = int(callback.matches[0].group(1))
    player = cache.get(callback.data)

    await handle_ranked_solo(brawl, brawlhalla_id, player, callback, cache, translate)


@bot.on_callback_query(filters.regex(f"{View.RANKED_TEAM}_(\\d+)"))
@user_language
async def player_ranked_team_callback(
    _: Client, callback: CallbackQuery, translate: Plate
):
    brawlhalla_id = int(callback.matches[0].group(1))
    player = cache.get(f"{View.RANKED_SOLO}_{brawlhalla_id}")
    await handle_ranked_team(brawl, brawlhalla_id, player, callback, cache, translate)


@bot.on_callback_query(filters.regex(f"{View.CLAN}_(\\d+)"))
@user_language
async def player_clan_callback(_: Client, callback: CallbackQuery, translate: Plate):
    brawlhalla_id = int(callback.matches[0].group(1))
    player = cache.get(f"{View.GENERAL}_{brawlhalla_id}")
    await handle_clan(brawl, brawlhalla_id, player, callback, cache, translate)


@bot.on_callback_query(filters.regex(f"{View.RANKED_TEAM_DETAIL}_(\\d+)_(\\d+)"))
@user_language
async def player_ranked_team_detail_callback(
    _: Client, callback: CallbackQuery, translate: Plate
):
    regex = callback.matches[0]
    brawlhalla_id_one = int(regex.group(1))
    brawlhalla_id_two = int(regex.group(2))
    player = cache.get(f"{View.RANKED_SOLO}_{brawlhalla_id_one}")

    await handle_ranked_team_detail(
        brawl, brawlhalla_id_one, brawlhalla_id_two, player, callback, cache, translate
    )


@bot.on_callback_query(filters.regex("close"))
async def close_callback(_: Client, callback: CallbackQuery):
    await callback.message.delete()


async def set_commands(bot: Client):
    for lang_code, lang_locale in SUPPORTED_LANGUAGES.items():
        translate = plate.get_translator(lang_locale)
        await bot.set_bot_commands(
            [
                BotCommand("start", translate("start_description")),
                BotCommand(translate("search"), translate("search_description")),
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
