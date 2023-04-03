from brawlhalla_api.types import RankingResult
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class Keyboard:
    def CLOSE(translate):
        return [
            [InlineKeyboardButton(translate("button_close"), callback_data="close")]
        ]

    def search_player(
        players: list[RankingResult], current: int, total_pages: int, limit: int, _
    ) -> InlineKeyboardMarkup:
        buttons = []
        if current > 0:
            buttons.append(InlineKeyboardButton("◀️", callback_data="button_prev"))
        if current < total_pages:
            buttons.append(InlineKeyboardButton("▶️", callback_data="button_next"))

        return InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        f"{player.name} ({player.rating})",
                        callback_data=f"general_{player.brawlhalla_id}",
                    )
                ]
                for player in players[current * limit : (current + 1) * limit]
            ]
            + [buttons]
            + Keyboard.CLOSE(_)
        )

    def stats(brawlhalla_id: int, current_view: str, _) -> InlineKeyboardMarkup:
        buttons = []
        if current_view != "general":
            buttons.append(
                [
                    InlineKeyboardButton(
                        _("button_general"), callback_data=f"general_{brawlhalla_id}"
                    )
                ]
            )
        if current_view != "ranked":
            buttons.append(
                [
                    InlineKeyboardButton(
                        _("button_ranked"), callback_data=f"ranked_{brawlhalla_id}"
                    )
                ]
            )
        return InlineKeyboardMarkup(buttons)
