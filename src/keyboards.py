from brawlhalla_api.types import RankingResult
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from enum import Enum


class View(Enum):
    GENERAL = "general"
    RANKED_SOLO = "rankedsolo"
    RANKED_TEAM = "rankedteam"

    def __str__(self):
        return self.value


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
                        callback_data=f"{View.GENERAL}_{player.brawlhalla_id}",
                    )
                ]
                for player in players[current * limit : (current + 1) * limit]
            ]
            + [buttons]
            + Keyboard.CLOSE(_)
        )

    def stats(brawlhalla_id: int, current_view: View, _) -> InlineKeyboardMarkup:
        buttons = []
        if current_view != View.GENERAL:
            buttons.append(
                [
                    InlineKeyboardButton(
                        _("button_general"),
                        callback_data=f"{View.GENERAL}_{brawlhalla_id}",
                    )
                ]
            )
        if current_view != View.RANKED_SOLO:
            buttons.append(
                [
                    InlineKeyboardButton(
                        _("button_rankedsolo"),
                        callback_data=f"{View.RANKED_SOLO}_{brawlhalla_id}",
                    )
                ]
            )
        if current_view != View.RANKED_TEAM:
            buttons.append(
                [
                    InlineKeyboardButton(
                        _("button_rankedteam"),
                        callback_data=f"{View.RANKED_TEAM}_{brawlhalla_id}",
                    )
                ]
            )
        return InlineKeyboardMarkup(buttons)
