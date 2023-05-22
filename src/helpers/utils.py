from localization import Localization, Translator
from pyrogram.types import InlineKeyboardMarkup, CallbackQuery, Message


def make_progress_bar(level: int, xp_percentage: float) -> str:
    if level == 100:
        return level
    value = round(xp_percentage * 10)
    return f"\n{level} &gt; <code>▕{'█' * value}{'—' * (10 - value) }▏</code> &gt; {level + 1}"


def get_translated_times(translate: Translator, total_game_time: int) -> list[str]:
    days = int(total_game_time // 86400)
    hours = int((total_game_time % 86400) // 3600)
    minutes = int((total_game_time % 3600) // 60)
    seconds = int(total_game_time % 60)

    to_send = []

    if days > 0:
        to_send.append((translate.time_days(days), days))
    if hours > 0:
        to_send.append((translate.time_hours(hours), hours))
    if minutes > 0:
        to_send.append((translate.time_minutes(minutes), minutes))
    if seconds > 0:
        to_send.append((translate.time_seconds(seconds), seconds))

    return to_send


def make_played_time(translate: Translator, total_game_time: int) -> list[str]:
    translated_game_times = get_translated_times(translate, total_game_time)

    total_game_time_list = []

    for n, time in enumerate(translated_game_times):
        (
            total_game_time_list.append(
                ("╰─► " if n == len(translated_game_times) - 1 else "├─► ") + time[0]
            )
        )

    return total_game_time_list


def make_emoji_from_tier(tier: str) -> str:
    """
    Valhallan 	Diamond players who won 100 matches or more and are in top of their region
    Diamond 	2000+ Elo
    Platinum 	1622-1999 Elo
    Gold 	1338-1679 Elo
    Silver 	1086-1389 Elo
    Bronze 	872-1129 Elo
    Tin 	200-909 Elo
    """
    match tier.split()[0]:
        case "Tin":
            return "🟢"
        case "Bronze":
            return "🟠"
        case "Silver":
            return "⚪️"
        case "Gold":
            return "🟡"
        case "Platinum":
            return "🔵"
        case "Diamond":
            return "🟣"
        case "Valhallan":
            return "🔴"
        case _:
            return "⚫"


async def is_query_invalid(query, message: Message, translate: Translator) -> bool:
    len_query = len(query)

    if len_query < 2 or len_query > 32:
        await message.reply(translate.error_length())
        return True
    return False


async def send_or_edit_message(
    update: Message | CallbackQuery, text: str, keyboard: InlineKeyboardMarkup = None
) -> None:
    if isinstance(update, Message):
        send = getattr(update, "reply")
    elif isinstance(update, CallbackQuery):
        send = getattr(update, "edit_message_text")
    else:
        raise TypeError("update must be a Message or CallbackQuery")

    await send(text, reply_markup=keyboard)


def get_localized_commands(string: str, localization: Localization) -> list[str]:
    return [getattr(translator, string)() for translator in localization]
