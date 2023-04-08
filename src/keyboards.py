from enum import Enum
from helpers.cache import Legends
from localization import Translator
from babel.dates import format_timedelta
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from brawlhalla_api.types import (
    PlayerStatsLegend,
    RankingResult,
    PlayerStats,
    Clan,
)


class View(Enum):
    CLAN = "clan"
    LEGEND = "legend"
    WEAPON = "weapon"
    GENERAL = "general"
    RANKED_SOLO = "rankedsolo"
    RANKED_TEAM = "rankedteam"
    RANKED_TEAM_DETAIL = "rankedteamdetail"

    def __str__(self):
        return self.value


class Keyboard:
    def close_buttons(translate: Translator) -> list[list[InlineKeyboardButton]]:
        return [[InlineKeyboardButton(translate.button_close(), callback_data="close")]]

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
        players: list[RankingResult],
        current: int,
        total_pages: int,
        limit: int,
        translate: Translator,
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
            + Keyboard.close_buttons(translate)
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
                        f"{comp.name} ({comp.rank})",
                        callback_data=f"{View.GENERAL}_{comp.brawlhalla_id}",
                    )
                ]
                for comp in clan.components[current * limit : (current + 1) * limit]
            ]
            + [buttons]
            + Keyboard.close_buttons(_)
        )

    async def legends(
        current: int,
        total_pages: int,
        limit: int,
        translator: Translator,
        legends: list[PlayerStatsLegend] | Legends,
        player: PlayerStats = None,
        rows: int = 2,
    ) -> InlineKeyboardMarkup:
        if player:
            buttons = Keyboard.navigation_buttons(
                current,
                total_pages,
                f"legend_prev_{player.brawlhalla_id}",
                f"legend_next_{player.brawlhalla_id}",
            )
        elif legends:
            buttons = Keyboard.navigation_buttons(
                current,
                total_pages,
                "legend_prev",
                "legend_next",
            )
        if player:
            iterator = player.legends[current * limit : (current + 1) * limit]

            keys = [
                InlineKeyboardButton(
                    "{} ({})".format(
                        (await legends.get(legend.legend_id)).bio_name,
                        format_timedelta(
                            legend.matchtime,
                            locale=translator.locale_str,
                        ),
                    ),
                    callback_data=f"{View.LEGEND}_{player.brawlhalla_id}_{legend.legend_id}",
                )
                for legend in iterator
            ]

        else:
            iterator = legends.all()[current * limit : (current + 1) * limit]
            keys = [
                InlineKeyboardButton(
                    legend.bio_name,
                    callback_data=f"{View.LEGEND}_stats_{legend.legend_id}",
                )
                for legend in iterator
            ]

        keys = [keys[i : i + rows] for i in range(0, len(keys), rows)]

        return InlineKeyboardMarkup(
            keys + [buttons] + Keyboard.close_buttons(translator)
        )

    def stats(
        brawlhalla_id_one: int,
        current_view: View,
        translate: Translator,
        brawlhalla_id_two: int = None,
        show_clan: bool = False,
        show_legends: bool = False,
    ) -> InlineKeyboardMarkup:
        buttons = [
            [
                InlineKeyboardButton(
                    translate.button_default_player(),
                    callback_data=f"set_{brawlhalla_id_one}",
                )
            ],
        ]

        if show_legends:
            buttons.append(
                [
                    InlineKeyboardButton(
                        translate.button_legends(),
                        callback_data=f"{View.LEGEND}_{brawlhalla_id_one}",
                    )
                ]
            )

        if current_view != View.GENERAL:
            buttons.append(
                [
                    InlineKeyboardButton(
                        translate.button_general(),
                        callback_data=f"{View.GENERAL}_{brawlhalla_id_one}",
                    )
                ]
            )
        if show_clan:
            buttons.append(
                [
                    InlineKeyboardButton(
                        translate.button_clan(),
                        callback_data=f"{View.CLAN}_{brawlhalla_id_one}",
                    )
                ]
            )

        if current_view != View.RANKED_SOLO:
            buttons.append(
                [
                    InlineKeyboardButton(
                        translate.button_ranked_solo(),
                        callback_data=f"{View.RANKED_SOLO}_{brawlhalla_id_one}",
                    )
                ]
            )
        buttons.append(
            [
                InlineKeyboardButton(
                    translate.button_ranked_team(),
                    callback_data=f"{View.RANKED_TEAM}_{brawlhalla_id_one}",
                )
            ]
        )
        if brawlhalla_id_two is not None:
            buttons.append(
                [
                    InlineKeyboardButton(
                        translate.button_teammate(),
                        callback_data=f"{View.GENERAL}_{brawlhalla_id_two}",
                    )
                ]
            )
        return InlineKeyboardMarkup(buttons)

    def legends_weapons(translate: Translator) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        translate.button_legends(),
                        callback_data=str(View.LEGEND),
                    )
                ],
                [
                    InlineKeyboardButton(
                        translate.button_weapons(),
                        callback_data=str(View.WEAPON),
                    )
                ],
            ]
            + Keyboard.close_buttons(translate)
        )

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

    def issues(translate: Translator) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        translate.button_issue(),
                        url="https://github.com/NicKoehler/brawlhalla_bot/issues",
                    )
                ]
            ]
            + Keyboard.close_buttons(translate)
        )
