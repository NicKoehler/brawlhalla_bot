import traceback

from time import time
from os import environ
from html import escape
from prisma import Prisma
from functools import wraps
from dotenv import load_dotenv
from itertools import combinations
from keyboards import Keyboard, View
from scheduler.asyncio import Scheduler
from datetime import datetime, timedelta

from brawlhalla_api import Brawlhalla
from brawlhalla_api.errors import ServiceUnavailable

from helpers.live import get_lives, schedule_lives, send_event
from helpers.cache import Cache
from helpers.legends_cache import LegendsCache
from helpers.utils import (
    is_query_invalid,
    get_localized_commands,
)

from pyrogram import Client, filters
from pyrogram.methods.utilities.idle import idle
from pyrogram.types import (
    Message,
    CallbackQuery,
    BotCommand,
    InlineQuery,
)
from pyrogram.errors import MessageNotModified, PeerIdInvalid, MessageIdInvalid

from localization import Localization, Translator, SUPPORTED_LANGUAGES
from handlers import (
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

load_dotenv()

API_ID = environ.get("API_ID")
API_KEY = environ.get("API_KEY")
API_HASH = environ.get("API_HASH")
BOT_TOKEN = environ.get("BOT_TOKEN")

FLOOD_WAIT_SECONDS = int(environ.get("FLOOD_WAIT_SECONDS"))
CLEAR_TIME_SECONDS = int(environ.get("CLEAR_TIME_SECONDS"))

db = Prisma()
cache = Cache(180)
brawl = Brawlhalla(API_KEY)
legends_cache = LegendsCache(brawl)
localization = Localization()
bot = Client("brawlhalla", API_ID, API_HASH, bot_token=BOT_TOKEN)

users = {}


def user_handling(f):
    @wraps(f)
    async def wrapped(bot: Client, update, *args, **kwargs):
        try:
            time_now = time()
            user_id = update.from_user.id
            is_message = isinstance(update, Message)

            if user_id not in users:
                users[user_id] = (await db.user.find_unique(where={"id": user_id})) or (
                    await db.user.create(
                        data={
                            "id": user_id,
                            "language": update.from_user.language_code,
                        }
                    )
                )
                users[user_id].__dict__["time_last_message"] = time_now

            user = users[user_id]

            translate = localization.get_translator(user.language)

            time_blocked = user.time_blocked
            if time_blocked:
                if time_now - time_blocked < FLOOD_WAIT_SECONDS:
                    return
                users[user_id] = await db.user.update(
                    where={"id": user_id}, data={"time_blocked": None}
                )

            time_last_message = user.__dict__.get("time_last_message", time_now)

            if (
                is_message
                and time_last_message != time_now
                and time_now - time_last_message < 1
            ):
                users[user_id] = await db.user.update(
                    where={"id": user_id}, data={"time_blocked": time_now}
                )
                await bot.send_message(
                    update.chat.id, translate.error_flood_wait(FLOOD_WAIT_SECONDS)
                )
                return

            users[user_id].__dict__["time_last_message"] = time_now

            return await f(
                bot,
                update,
                translate,
                *args,
                **kwargs,
            )
        except MessageNotModified:
            pass

        except Exception:
            try:
                return await bot.send_message(
                    update.from_user.id,
                    translate.error_generic(error=traceback.format_exc()),
                    reply_markup=Keyboard.issues(translate),
                )
            except (PeerIdInvalid, MessageIdInvalid):
                print(traceback.format_exc())

    return wrapped


@bot.on_message(filters.command("start"))
@user_handling
async def start(_: Client, message: Message, translate: Translator):
    args = message.text.split()[1:]

    if args and args[0] == "notifications":
        user_id = message.from_user.id
        new_status = not users[user_id].notify_live
        users[user_id] = await db.user.update(
            {"notify_live": new_status}, where={"id": user_id}
        )
        if new_status:
            await message.reply(
                translate.status_notifications_on(),
            )
        else:
            await message.reply(
                translate.status_notifications_off(),
            )
        return

    await message.reply(
        translate.welcome(
            name=escape(message.from_user.first_name),
        ),
        reply_markup=Keyboard.start(translate),
    )


@bot.on_message(filters.command(get_localized_commands("search", localization)))
@user_handling
async def search_player(_: Client, message: Message, translate: Translator):
    await message.reply(
        translate.usage_search(),
        reply_markup=Keyboard.search(translate),
    )


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
        legends_cache,
        translate,
        message,
    )


@bot.on_message(filters.command("me"))
@user_handling
async def player_me(_: Client, message: Message, translate: Translator):
    user = await db.user.find_first(where={"id": message.from_user.id})

    if user.brawlhalla_id is None:
        await message.reply(translate.error_missing_default_player())
        return

    await handle_general(
        brawl,
        user.brawlhalla_id,
        cache,
        legends_cache,
        translate,
        message,
    )


@bot.on_message(filters.command("legend"))
@user_handling
async def legend(_: Client, message: Message, translate: Translator):
    if len(message.command) < 2:
        await handle_legend_stats(legends_cache, translate, message)
        return
    query = escape(" ".join(message.command[1:]).lower())
    if await is_query_invalid(query, message, translate):
        return
    for legend in legends_cache.all:
        if legend.legend_name_key == query:
            await handle_legend_details(legend, translate, message)
            return

    await message.reply(translate.error_legend_not_found(query))


@bot.on_message(filters.command(get_localized_commands("weapons", localization)))
@user_handling
async def weapon(_: Client, message: Message, translate: Translator):
    len_commands = len(message.command)

    if len_commands < 2:
        await handle_weapons(legends_cache, message, translate)
        return

    if len_commands == 2:
        weapon = escape(message.command[1].lower())
        if await is_query_invalid(weapon, message, translate):
            return
        if weapon not in legends_cache.weapons:
            await message.reply(translate.error_weapon_not_found(weapon))
            return
        await handle_weapons(legends_cache, message, translate, weapon)
        return

    weapons = [
        escape(message.command[1].lower()),
        escape(message.command[2].lower()),
    ]

    weapons_set = set(weapons)

    for legend in legends_cache.all:
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

    weapons = set(
        f"{legend.weapon_one}_{legend.weapon_two}" for legend in legends_cache.all
    )
    missing = []
    for combination in combinations(legends_cache.weapons, 2):
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


@bot.on_message(filters.command("live"))
@user_handling
async def live_command(_: Client, message: Message, translate: Translator):
    lives = await get_lives()
    if not lives:
        await message.reply(
            translate.error_no_lives(),
            reply_markup=Keyboard.live(translate, False),
        )
        return
    await send_event(message, lives[0], translate, bot)


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
    await handle_general(
        brawl, brawlhalla_id, cache, legends_cache, translate, callback
    )


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
        legends_cache,
        translate,
        current_page=int(current_page or "0"),
    )


@bot.on_callback_query(filters.regex(f"^{View.LEGEND}$"))
@user_handling
async def player_legend_list_callback(
    _: Client, callback: CallbackQuery, translate: Translator
):
    await handle_legend_stats(legends_cache, translate, callback)


@bot.on_callback_query(filters.regex(f"^{View.LEGEND}_stats_(\\d+)$"))
@user_handling
async def player_legend_details_callback(
    _: Client, callback: CallbackQuery, translate: Translator
):
    legend_id = callback.matches[0].group(1)
    await handle_legend_details(await legends_cache.get(legend_id), translate, callback)


@bot.on_callback_query(filters.regex(f"^(\\d+)_{View.LEGEND}_?([az]+)?$"))
@user_handling
async def search_legend_page(_: Client, callback: CallbackQuery, translate: Translator):
    current_page, weapon = callback.matches[0].groups()
    await handle_legend_stats(
        legends_cache,
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
        legends_cache,
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
        await legends_cache.get(legend_id),
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
        brawl,
        int(brawlhalla_id_one),
        int(brawlhalla_id_two),
        callback,
        cache,
        translate,
    )


@bot.on_callback_query(lambda _, x: x.data[7:] in legends_cache.weapons)
@user_handling
async def legend_weapon_callback(
    _: Client, callback: CallbackQuery, translate: Translator
):
    weapon = callback.data[7:]
    await handle_weapons(legends_cache, callback, translate, weapon)


@bot.on_callback_query(filters.regex(f"^{View.WEAPON}$"))
@user_handling
async def legend_weapon_list_callback(
    _: Client, callback: CallbackQuery, translate: Translator
):
    await handle_weapons(legends_cache, callback, translate)


@bot.on_callback_query(filters.regex(r"^set_(\d+)$"))
@user_handling
async def set_default_callback(
    _: Client, callback: CallbackQuery, translate: Translator
):
    user_id = callback.from_user.id
    brawlhalla_id = int(callback.matches[0].group(1))
    users[user_id] = await db.user.update(
        {"brawlhalla_id": brawlhalla_id}, where={"id": user_id}
    )
    await callback.answer(translate.status_default_player_set(), show_alert=True)


@bot.on_callback_query(
    filters.regex(r"^(" + "|".join(SUPPORTED_LANGUAGES.keys()) + r")$")
)
@user_handling
async def language_callback(_: Client, callback: CallbackQuery, translate: Translator):
    lang = callback.data
    user_id = callback.from_user.id
    user = users[user_id]

    if lang == user.language:
        await callback.answer(translate.status_language_unchanged(), show_alert=True)
    else:
        users[user_id] = await db.user.update({"language": lang}, where={"id": user_id})
        translate = localization.get_translator(lang)
        await callback.answer(translate.status_language_changed(), show_alert=True)
        await callback.message.delete()


@bot.on_callback_query(filters.regex(r"^close$"))
async def close_callback(_: Client, callback: CallbackQuery):
    await callback.message.delete()


@bot.on_inline_query(filters.regex(r"^.id\s+(\d+)$"))
@user_handling
async def inline_query_id_handler(
    _: Client,
    inline_query: InlineQuery,
    translate: Translator,
):
    brawlhalla_id = inline_query.matches[0].group(1)
    await handle_general(
        brawl, brawlhalla_id, cache, legends_cache, translate, inline_query
    )


@bot.on_inline_query()
@user_handling
async def inline_query_handler(
    _: Client,
    inline_query: InlineQuery,
    translate: Translator,
):
    await handle_search(inline_query, brawl, translate, cache, legends_cache)


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
                BotCommand("live", translate.description_live()),
                BotCommand(translate.language(), translate.description_language()),
            ],
            language_code=lang_code,
        )


async def clear_inactive_users():
    """
    clear users that are not active for more than CLEAR_TIME_SECONDS from ram
    """

    time_now = time()
    to_delete = set()

    for user_id, user in users.items():
        if (
            "time_last_message" in user.__dict__
            and time_now - user.__dict__["time_last_message"] > CLEAR_TIME_SECONDS
        ):
            to_delete.add(user_id)

    for user_id in to_delete:
        del users[user_id]


async def main():
    schedule = Scheduler()

    schedule.cyclic(timedelta(hours=1), cache.clear)
    schedule.cyclic(timedelta(hours=1), clear_inactive_users)

    for t, s in [
        (datetime.now(), schedule.once),
        (timedelta(hours=1), schedule.cyclic),
    ]:
        s(
            t,
            schedule_lives,
            args=(
                bot,
                db,
                schedule,
                localization,
            ),
        )

    await legends_cache.refresh_legends()
    await db.connect()
    await bot.start()

    await set_commands(bot)
    await idle()

    await db.disconnect()
    await bot.stop()


bot.run(main())
