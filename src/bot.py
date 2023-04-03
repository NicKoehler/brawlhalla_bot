import utils
from math import ceil
from os import environ
from plate import Plate
from cache import Cache
from html import escape
from functools import wraps
from dotenv import load_dotenv
from keyboards import Keyboard
from pyrogram import Client, filters
from brawlhalla_api import Brawlhalla
from pyrogram.types import Message, CallbackQuery

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
                lang = "en_EN"
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


@bot.on_callback_query(filters.regex(r"(general|ranked)_(\d+)"))
@user_language
async def general_callback(_: Client, callback: CallbackQuery, translate: Plate):
    callback.from_user.language_code
    regex = callback.matches[0]
    mode = regex.group(1)
    brawlhalla_id = regex.group(2)
    player = cache.get(callback.data)

    match mode:
        case "general":
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
                    ).legend_name_key,
                    total_game_time=sum(legend.matchtime for legend in player.legends),
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
                reply_markup=Keyboard.stats(player.brawlhalla_id, "general", translate),
            )
        case "ranked":
            if player is None:
                player = await brawl.get_ranked(brawlhalla_id)
                cache.add(callback.data, player)

            if player is None:
                callback.answer(translate("no_ranked_data"), show_alert=True)
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
                ),
                reply_markup=Keyboard.stats(player.brawlhalla_id, "ranked", translate),
            )


@bot.on_callback_query(filters.regex("close"))
async def close_callback(_: Client, callback: CallbackQuery):
    await callback.message.delete()


bot.run()
