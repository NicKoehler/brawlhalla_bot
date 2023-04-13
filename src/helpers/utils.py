from keyboards import Keyboard, View
from brawlhalla_api.types import PlayerStats
from localization import Localization, Translator
from pyrogram.types import InlineKeyboardMarkup, CallbackQuery, Message


def make_progress_bar(level: int, xp_percentage: float) -> str:
    if level == 100:
        return level
    value = round(xp_percentage * 10)
    return f"\n{level} &gt; <code>▕{'█' * value}{'—' * (10 - value) }▏</code> &gt; {level + 1}"


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
