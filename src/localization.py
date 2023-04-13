# THIS CODE IS AUTOGENERATED BY src/locales/generate_locales.py
# DO NOT EDIT THIS FILE DIRECTLY.

from typing import Iterator
from locales import it, en


SUPPORTED_LANGUAGES = {'it': 'it_IT', 'en': 'en_US'}


class Translator:
    def __init__(self, locale, locale_str) -> None:
        self.locale = locale
        self.locale_str = locale_str

    def all_weapons(self):
        return self.locale.ALL_WEAPONS

    def button_clan(self):
        return self.locale.BUTTON_CLAN

    def button_close(self):
        return self.locale.BUTTON_CLOSE

    def button_default_player(self):
        return self.locale.BUTTON_DEFAULT_PLAYER

    def button_general(self):
        return self.locale.BUTTON_GENERAL

    def button_issue(self):
        return self.locale.BUTTON_ISSUE

    def button_legends(self):
        return self.locale.BUTTON_LEGENDS

    def button_ranked_solo(self):
        return self.locale.BUTTON_RANKED_SOLO

    def button_ranked_team(self):
        return self.locale.BUTTON_RANKED_TEAM

    def button_search_all(self):
        return self.locale.BUTTON_SEARCH_ALL

    def button_search_aus(self):
        return self.locale.BUTTON_SEARCH_AUS

    def button_search_brz(self):
        return self.locale.BUTTON_SEARCH_BRZ

    def button_search_eu(self):
        return self.locale.BUTTON_SEARCH_EU

    def button_search_jpn(self):
        return self.locale.BUTTON_SEARCH_JPN

    def button_search_me(self):
        return self.locale.BUTTON_SEARCH_ME

    def button_search_sa(self):
        return self.locale.BUTTON_SEARCH_SA

    def button_search_sea(self):
        return self.locale.BUTTON_SEARCH_SEA

    def button_search_us_e(self):
        return self.locale.BUTTON_SEARCH_US_E

    def button_search_us_w(self):
        return self.locale.BUTTON_SEARCH_US_W

    def button_share(self):
        return self.locale.BUTTON_SHARE

    def button_teammate(self):
        return self.locale.BUTTON_TEAMMATE

    def button_weapons(self):
        return self.locale.BUTTON_WEAPONS

    def description_id(self):
        return self.locale.DESCRIPTION_ID

    def description_language(self):
        return self.locale.DESCRIPTION_LANGUAGE

    def description_legend(self):
        return self.locale.DESCRIPTION_LEGEND

    def description_me(self):
        return self.locale.DESCRIPTION_ME

    def description_missing(self):
        return self.locale.DESCRIPTION_MISSING

    def description_search(self):
        return self.locale.DESCRIPTION_SEARCH

    def description_start(self):
        return self.locale.DESCRIPTION_START

    def description_weapons(self):
        return self.locale.DESCRIPTION_WEAPONS

    def error_api_offline(self):
        return self.locale.ERROR_API_OFFLINE

    def error_flood_wait(
        self,
        seconds
    ):
        return self.locale.ERROR_FLOOD_WAIT.format(
            seconds=seconds
        )

    def error_generic(
        self,
        error
    ):
        return self.locale.ERROR_GENERIC.format(
            error=error
        )

    def error_legend_not_found(
        self,
        query
    ):
        return self.locale.ERROR_LEGEND_NOT_FOUND.format(
            query=query
        )

    def error_legend_result(self):
        return self.locale.ERROR_LEGEND_RESULT

    def error_length(self):
        return self.locale.ERROR_LENGTH

    def error_missing_default_player(self):
        return self.locale.ERROR_MISSING_DEFAULT_PLAYER

    def error_missing_weapons_combination_not_found(
        self,
        query
    ):
        return self.locale.ERROR_MISSING_WEAPONS_COMBINATION_NOT_FOUND.format(
            query=query
        )

    def error_no_clan_data(self):
        return self.locale.ERROR_NO_CLAN_DATA

    def error_no_ranked_data(self):
        return self.locale.ERROR_NO_RANKED_DATA

    def error_no_team_data(self):
        return self.locale.ERROR_NO_TEAM_DATA

    def error_player_not_found(
        self,
        id
    ):
        return self.locale.ERROR_PLAYER_NOT_FOUND.format(
            id=id
        )

    def error_player_result(self):
        return self.locale.ERROR_PLAYER_RESULT

    def error_search_result(
        self,
        query
    ):
        return self.locale.ERROR_SEARCH_RESULT.format(
            query=query
        )

    def error_team_result(self):
        return self.locale.ERROR_TEAM_RESULT

    def error_weapon_not_found(
        self,
        query
    ):
        return self.locale.ERROR_WEAPON_NOT_FOUND.format(
            query=query
        )

    def language(self):
        return self.locale.LANGUAGE

    def missing(self):
        return self.locale.MISSING

    def results_legends(self):
        return self.locale.RESULTS_LEGENDS

    def results_legends_with_weapon(
        self,
        weapon
    ):
        return self.locale.RESULTS_LEGENDS_WITH_WEAPON.format(
            weapon=weapon
        )

    def results_missing_weapons_combination(
        self,
        weapons
    ):
        return self.locale.RESULTS_MISSING_WEAPONS_COMBINATION.format(
            weapons=weapons
        )

    def results_missing_weapons_combination_with_weapon(
        self,
        weapon,
        weapons
    ):
        return self.locale.RESULTS_MISSING_WEAPONS_COMBINATION_WITH_WEAPON.format(
            weapon=weapon,
            weapons=weapons
        )

    def results_teams(self):
        return self.locale.RESULTS_TEAMS

    def search(self):
        return self.locale.SEARCH

    def stats_base(
        self,
        id,
        name
    ):
        return self.locale.STATS_BASE.format(
            id=id,
            name=name
        )

    def stats_clan(
        self,
        id,
        name,
        xp,
        num,
        date
    ):
        return self.locale.STATS_CLAN.format(
            id=id,
            name=name,
            xp=xp,
            num=num,
            date=date
        )

    def stats_general(
        self,
        clan,
        level,
        xp,
        most_used_legend,
        total_game_time,
        games,
        wins,
        loses,
        winperc,
        totalko,
        totaldeath,
        totalsuicide,
        totalteamko,
        kobomb,
        damagebomb,
        komine,
        damagemine,
        kospikeball,
        damagespikeball,
        kosidekick,
        damagesidekick,
        kosnowball,
        hitsnowball
    ):
        return self.locale.STATS_GENERAL.format(
            clan=clan,
            level=level,
            xp=xp,
            most_used_legend=most_used_legend,
            total_game_time=total_game_time,
            games=games,
            wins=wins,
            loses=loses,
            winperc=winperc,
            totalko=totalko,
            totaldeath=totaldeath,
            totalsuicide=totalsuicide,
            totalteamko=totalteamko,
            kobomb=kobomb,
            damagebomb=damagebomb,
            komine=komine,
            damagemine=damagemine,
            kospikeball=kospikeball,
            damagespikeball=damagespikeball,
            kosidekick=kosidekick,
            damagesidekick=damagesidekick,
            kosnowball=kosnowball,
            hitsnowball=hitsnowball
        )

    def stats_legend(
        self,
        legend_id,
        bio_name,
        bio_aka,
        weapon_one,
        weapon_two,
        strength,
        dexterity,
        defense,
        speed
    ):
        return self.locale.STATS_LEGEND.format(
            legend_id=legend_id,
            bio_name=bio_name,
            bio_aka=bio_aka,
            weapon_one=weapon_one,
            weapon_two=weapon_two,
            strength=strength,
            dexterity=dexterity,
            defense=defense,
            speed=speed
        )

    def stats_player_legend(
        self,
        id,
        name,
        level,
        xp,
        matchtime,
        games,
        wins,
        loses,
        winperc,
        ko,
        death,
        suicide,
        damagedealt,
        damagetaken,
        teamko,
        weaponone,
        timeheldweaponone,
        koweaponone,
        damageweaponone,
        weapontwo,
        timeheldweapontwo,
        koweapontwo,
        damageweapontwo,
        kounarmed,
        damageunarmed,
        kogadgets,
        damagegadgets,
        kothrownitem,
        damagethrownitem
    ):
        return self.locale.STATS_PLAYER_LEGEND.format(
            id=id,
            name=name,
            level=level,
            xp=xp,
            matchtime=matchtime,
            games=games,
            wins=wins,
            loses=loses,
            winperc=winperc,
            ko=ko,
            death=death,
            suicide=suicide,
            damagedealt=damagedealt,
            damagetaken=damagetaken,
            teamko=teamko,
            weaponone=weaponone,
            timeheldweaponone=timeheldweaponone,
            koweaponone=koweaponone,
            damageweaponone=damageweaponone,
            weapontwo=weapontwo,
            timeheldweapontwo=timeheldweapontwo,
            koweapontwo=koweapontwo,
            damageweapontwo=damageweapontwo,
            kounarmed=kounarmed,
            damageunarmed=damageunarmed,
            kogadgets=kogadgets,
            damagegadgets=damagegadgets,
            kothrownitem=kothrownitem,
            damagethrownitem=damagethrownitem
        )

    def stats_ranked(
        self,
        rating,
        peak,
        tier,
        games,
        wins,
        loses,
        region,
        glory,
        elo_reset
    ):
        return self.locale.STATS_RANKED.format(
            rating=rating,
            peak=peak,
            tier=tier,
            games=games,
            wins=wins,
            loses=loses,
            region=region,
            glory=glory,
            elo_reset=elo_reset
        )

    def stats_ranked_team(
        self,
        teamname,
        rating,
        peak,
        tier,
        games,
        wins,
        loses,
        region
    ):
        return self.locale.STATS_RANKED_TEAM.format(
            teamname=teamname,
            rating=rating,
            peak=peak,
            tier=tier,
            games=games,
            wins=wins,
            loses=loses,
            region=region
        )

    def status_default_player_set(self):
        return self.locale.STATUS_DEFAULT_PLAYER_SET

    def status_language_changed(self):
        return self.locale.STATUS_LANGUAGE_CHANGED

    def status_language_unchanged(self):
        return self.locale.STATUS_LANGUAGE_UNCHANGED

    def time_days(
        self,
        t
    ):
        return self.locale.TIME_DAYS.format(
            t=t
        )

    def time_hours(
        self,
        t
    ):
        return self.locale.TIME_HOURS.format(
            t=t
        )

    def time_minutes(
        self,
        t
    ):
        return self.locale.TIME_MINUTES.format(
            t=t
        )

    def time_seconds(
        self,
        t
    ):
        return self.locale.TIME_SECONDS.format(
            t=t
        )

    def usage_id(self):
        return self.locale.USAGE_ID

    def usage_inline(self):
        return self.locale.USAGE_INLINE

    def usage_search(self):
        return self.locale.USAGE_SEARCH

    def weapons(self):
        return self.locale.WEAPONS

    def welcome(
        self,
        name
    ):
        return self.locale.WELCOME.format(
            name=name
        )


class Localization:
    def __init__(self) -> None:
        self._strings = {
            "it": Translator(it, "it_IT"),
            "en": Translator(en, "en_US"),
        }

    def get_translator(self, lang: str) -> Translator:
        if lang not in self._strings:
            raise ValueError(f"Unsupported language: {lang}")
        return self._strings[lang]

    def __iter__(self) -> Iterator[Translator]:
        return iter(self._strings.values())
