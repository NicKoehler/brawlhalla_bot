from enum import Enum
from brawlhalla_api.types import RankingResult, Clan
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class View(Enum):
    GENERAL = "general"
    CLAN = "clan"
    RANKED_SOLO = "rankedsolo"
    RANKED_TEAM = "rankedteam"
    RANKED_TEAM_DETAIL = "rankedteamdetail"

    def __str__(self):
        return self.value


class Keyboard:
    def close_buttons(translate) -> list[list[InlineKeyboardButton]]:
        return [
            [InlineKeyboardButton(translate("button_close"), callback_data="close")]
        ]

    def navigation_buttons(
        current: int,
        total_pages: int,
        prev_data: str,
        next_data: str,
    ) -> list[InlineKeyboardButton]:
        buttons = []
        if current > 0:
            buttons.append(InlineKeyboardButton("◀️", callback_data=prev_data))
        if current < total_pages:
            buttons.append(InlineKeyboardButton("▶️", callback_data=next_data))

        return buttons

    def search_player(
        players: list[RankingResult], current: int, total_pages: int, limit: int, _
    ) -> InlineKeyboardMarkup:
        buttons = Keyboard.navigation_buttons(
            current,
            total_pages,
            "button_prev",
            "button_next",
        )

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
            + Keyboard.close_buttons(_)
        )

    def teams(
        player: RankingResult, current: int, total_pages: int, limit: int, _
    ) -> InlineKeyboardMarkup:
        buttons = Keyboard.navigation_buttons(
            current,
            total_pages,
            f"team_prev_{player.brawlhalla_id}",
            f"team_next_{player.brawlhalla_id}",
        )

        get_real_id = (
            lambda p_id, team_id_one, team_id_two: (team_id_one, team_id_two)
            if team_id_one == p_id
            else (team_id_two, team_id_one)
        )

        return InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        f"{team.teamname} ({team.rating})",
                        callback_data="{}_{}_{}".format(
                            View.RANKED_TEAM_DETAIL,
                            *get_real_id(
                                player.brawlhalla_id,
                                team.brawlhalla_id_one,
                                team.brawlhalla_id_two,
                            ),
                        ),
                    )
                ]
                for team in player.teams[current * limit : (current + 1) * limit]
            ]
            + [buttons]
            + Keyboard.close_buttons(_)
        )

    def clan_components(
        clan: Clan, current: int, total_pages: int, limit: int, _
    ) -> InlineKeyboardMarkup:
        buttons = Keyboard.navigation_buttons(
            current,
            total_pages,
            f"clan_prev_{clan.clan_id}",
            f"clan_next_{clan.clan_id}",
        )

        return InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        f"{comp.name} - {comp.rank}",
                        callback_data=f"{View.GENERAL}_{comp.brawlhalla_id}",
                    )
                ]
                for comp in clan.components[current * limit : (current + 1) * limit]
            ]
            + [buttons]
            + Keyboard.close_buttons(_)
        )

    def stats(
        brawlhalla_id_one: int,
        current_view: View,
        _,
        brawlhalla_id_two: int = None,
        has_clan: bool = False,
    ) -> InlineKeyboardMarkup:
        buttons = [
            [
                InlineKeyboardButton(
                    _("button_set_player"),
                    callback_data=f"set_{brawlhalla_id_one}",
                )
            ]
        ]
        if current_view != View.GENERAL:
            buttons.append(
                [
                    InlineKeyboardButton(
                        _("button_general"),
                        callback_data=f"{View.GENERAL}_{brawlhalla_id_one}",
                    )
                ]
            )
        if has_clan:
            buttons.append(
                [
                    InlineKeyboardButton(
                        _("button_clan"),
                        callback_data=f"{View.CLAN}_{brawlhalla_id_one}",
                    )
                ]
            )
        if current_view != View.RANKED_SOLO:
            buttons.append(
                [
                    InlineKeyboardButton(
                        _("button_rankedsolo"),
                        callback_data=f"{View.RANKED_SOLO}_{brawlhalla_id_one}",
                    )
                ]
            )
        buttons.append(
            [
                InlineKeyboardButton(
                    _("button_rankedteam"),
                    callback_data=f"{View.RANKED_TEAM}_{brawlhalla_id_one}",
                )
            ]
        )
        if brawlhalla_id_two is not None:
            buttons.append(
                [
                    InlineKeyboardButton(
                        _("button_teammate"),
                        callback_data=f"{View.GENERAL}_{brawlhalla_id_two}",
                    )
                ]
            )
        return InlineKeyboardMarkup(buttons)

    def languages() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🇺🇸 • ENGLISH • 🇺🇸",
                        callback_data="en",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "🇮🇹 • ITALIANO • 🇮🇹",
                        callback_data="it",
                    ),
                ],
            ]
        )

    def issues(text: str) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text,
                        url="https://github.com/NicKoehler/brawlhalla_bot/issues",
                    )
                ]
            ]
        )
