from math import ceil
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
    SEARCH = "search"
    RANKED_SOLO = "rankedsolo"
    RANKED_TEAM = "rankedteam"
    RANKED_TEAM_DETAIL = "rankedteamdetail"

    def __str__(self):
        return self.value


class Keyboard:
    def close_button(translate: Translator) -> list[list[InlineKeyboardButton]]:
        return [[InlineKeyboardButton(translate.button_close(), callback_data="close")]]

    def start(translate: Translator) -> list[list[InlineKeyboardButton]]:
        return InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        translate.button_inline(),
                        switch_inline_query_current_chat="",
                    )
                ]
            ]
        )

    def legend_button(translate: Translator):
        return [
            [
                InlineKeyboardButton(
                    translate.button_legends(),
                    callback_data=str(View.LEGEND),
                )
            ]
        ]

    def weapon_button(translate: Translator):
        return [
            [
                InlineKeyboardButton(
                    translate.button_weapons(),
                    callback_data=str(View.WEAPON),
                )
            ]
        ]

    def navigation_buttons(
        current_page: int,
        limit_page: int,
        data: str,
        lst: list,
    ) -> list[InlineKeyboardButton]:
        total_pages = ceil(len(lst) / limit_page) - 1

        if current_page > total_pages:
            current_page = total_pages

        buttons = []
        if current_page > 0:
            buttons.append(
                InlineKeyboardButton("◀️", callback_data=f"{current_page - 1}_{data}")
            )
        if current_page < total_pages:
            buttons.append(
                InlineKeyboardButton("▶️", callback_data=f"{current_page + 1}_{data}")
            )

        return buttons

    def search_player(
        players: list[RankingResult],
        query: str,
        current_page: int,
        limit: int,
        translate: Translator,
    ) -> InlineKeyboardMarkup:
        buttons = Keyboard.navigation_buttons(
            current_page,
            limit,
            f"{View.SEARCH}_{query}",
            players,
        )

        return InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        f"{player.name} ({player.rating})",
                        callback_data=f"{View.GENERAL}_{player.brawlhalla_id}",
                    )
                ]
                for player in players[current_page * limit : (current_page + 1) * limit]
            ]
            + [buttons]
            + Keyboard.close_button(translate)
        )

    def teams(
        player: RankingResult,
        current: int,
        limit: int,
    ) -> InlineKeyboardMarkup:
        buttons = Keyboard.navigation_buttons(
            current,
            limit,
            f"team_{player.brawlhalla_id}",
            player.teams,
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
        )

    def clan_components(
        clan: Clan, current_page: int, limit: int, _
    ) -> InlineKeyboardMarkup:
        total_pages = ceil(clan.components / limit) - 1

        if current_page > total_pages:
            current_page = total_pages

        buttons = Keyboard.navigation_buttons(
            current_page,
            limit,
            f"clan_{clan.clan_id}",
            clan.components,
        )

        return InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        f"{comp.name} ({comp.rank})",
                        callback_data=f"{View.GENERAL}_{comp.brawlhalla_id}",
                    )
                ]
                for comp in clan.components[
                    current_page * limit : (current_page + 1) * limit
                ]
            ]
            + [buttons]
        )

    async def legends(
        current: int,
        limit: int,
        translator: Translator,
        legends: list[PlayerStatsLegend] | Legends,
        weapon: str = None,
        player: PlayerStats = None,
        rows: int = 2,
    ) -> InlineKeyboardMarkup:
        if player:
            navigation_buttons = Keyboard.navigation_buttons(
                current,
                limit,
                f"legend_{player.brawlhalla_id}",
                player.legends,
            )
        else:
            iterator = legends if weapon else legends.all
            navigation_buttons = Keyboard.navigation_buttons(
                current,
                limit,
                f"legend_{weapon}" if weapon else "legend",
                iterator,
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
            iterator = iterator[current * limit : (current + 1) * limit]
            keys = [
                InlineKeyboardButton(
                    legend.bio_name,
                    callback_data=f"{View.LEGEND}_stats_{legend.legend_id}",
                )
                for legend in iterator
            ]

        keys = [keys[i : i + rows] for i in range(0, len(keys), rows)] + [
            navigation_buttons
        ]

        if not player:
            keys += Keyboard.weapon_button(translator)
            keys += Keyboard.close_button(translator)

        return InlineKeyboardMarkup(keys)

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
            Keyboard.legend_button(translate)
            + Keyboard.weapon_button(translate)
            + Keyboard.close_button(translate)
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

    def weapons(weapons: set[str], translate, row=3) -> InlineKeyboardMarkup:
        keys = [
            InlineKeyboardButton(
                weapon.capitalize(),
                callback_data=f"{View.WEAPON}_{weapon}",
            )
            for weapon in weapons
        ]

        keys = (
            [keys[i : i + row] for i in range(0, len(keys), row)]
            + Keyboard.legend_button(translate)
            + Keyboard.close_button(translate)
        )

        return InlineKeyboardMarkup(keys)

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
            + Keyboard.close_button(translate)
        )
