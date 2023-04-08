from localization import Translator
from pyrogram.types import InlineKeyboardMarkup, CallbackQuery, Message


def make_progress_bar(level: int, xp_percentage: float) -> str:
    if level == 100:
        return level
    value = round(xp_percentage * 10)
    return f"\n{level} &gt; <code>▕{'█' * value}{'—' * (10 - value) }▏</code> &gt; {level + 1}"


def get_current_page(
    callback: CallbackQuery, get_second_param=False, query=False
) -> int:
    splitted = callback.message.text.split("\n")
    pages = splitted[-1]
    current_page = int(pages.split("/")[0]) - 1
    current_page += 1 if callback.matches[0].group(1) == "next" else -1

    if get_second_param:
        return current_page, int(callback.matches[0].group(2))

    if query:
        return current_page, splitted[-2]

    return current_page


async def is_query_invalid(query, message: Message, translate: Translator) -> bool:
    len_query = len(query)

    if len_query < 2 or len_query > 32:
        await message.reply(translate.error_length())
        return True
    return False


async def send_or_edit_message(
    update: Message | CallbackQuery, text: str, keyboard: InlineKeyboardMarkup
) -> None:
    if isinstance(update, Message):
        send = getattr(update, "reply")
    elif isinstance(update, CallbackQuery):
        send = getattr(update.message, "edit")
    else:
        raise TypeError("update must be a Message or CallbackQuery")

    await send(text, reply_markup=keyboard)
