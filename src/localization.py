# THIS CODE IS AUTOGENERATED BY src/generate_locales.py
# DO NOT EDIT THIS FILE DIRECTLY.

from locales import it, en


SUPPORTED_LANGUAGES = {'it': 'it_IT', 'en': 'en_US'}


class Translator:
    def __init__(self, locale, locale_str) -> None:
        self.locale = locale
        self.locale_str = locale_str

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

    def description_search(self):
        return self.locale.DESCRIPTION_SEARCH

    def description_start(self):
        return self.locale.DESCRIPTION_START

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

    def error_search_result(
        self,
        query
    ):
        return self.locale.ERROR_SEARCH_RESULT.format(
            query=query
        )

    def error_team_result(self):
        return self.locale.ERROR_TEAM_RESULT

    def language(self):
        return self.locale.LANGUAGE

    def results_legends(
        self,
        total,
        current
    ):
        return self.locale.RESULTS_LEGENDS.format(
            total=total,
            current=current
        )

    def results_search(
        self,
        query,
        total,
        current
    ):
        return self.locale.RESULTS_SEARCH.format(
            query=query,
            total=total,
            current=current
        )

    def results_teams(
        self,
        total,
        current
    ):
        return self.locale.RESULTS_TEAMS.format(
            total=total,
            current=current
        )

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
        total,
        current,
        num,
        xp,
        date,
        id,
        name
    ):
        return self.locale.STATS_CLAN.format(
            total=total,
            current=current,
            num=num,
            xp=xp,
            date=date,
            id=id,
            name=name
        )

    def stats_general(
        self,
        level,
        totaldeath,
        xp,
        kosnowball,
        damagespikeball,
        loses,
        wins,
        most_used_legend,
        damagebomb,
        kobomb,
        hitsnowball,
        totalteamko,
        total_game_time,
        komine,
        totalko,
        clan,
        damagemine,
        kosidekick,
        kospikeball,
        games,
        damagesidekick,
        totalsuicide,
        winperc
    ):
        return self.locale.STATS_GENERAL.format(
            level=level,
            totaldeath=totaldeath,
            xp=xp,
            kosnowball=kosnowball,
            damagespikeball=damagespikeball,
            loses=loses,
            wins=wins,
            most_used_legend=most_used_legend,
            damagebomb=damagebomb,
            kobomb=kobomb,
            hitsnowball=hitsnowball,
            totalteamko=totalteamko,
            total_game_time=total_game_time,
            komine=komine,
            totalko=totalko,
            clan=clan,
            damagemine=damagemine,
            kosidekick=kosidekick,
            kospikeball=kospikeball,
            games=games,
            damagesidekick=damagesidekick,
            totalsuicide=totalsuicide,
            winperc=winperc
        )

    def stats_legend(
        self,
        weapon_two,
        defense,
        dexterity,
        strength,
        speed,
        legend_id,
        bio_aka,
        weapon_one,
        bio_name,
        legend_name_key
    ):
        return self.locale.STATS_LEGEND.format(
            weapon_two=weapon_two,
            defense=defense,
            dexterity=dexterity,
            strength=strength,
            speed=speed,
            legend_id=legend_id,
            bio_aka=bio_aka,
            weapon_one=weapon_one,
            bio_name=bio_name,
            legend_name_key=legend_name_key
        )

    def stats_player_legend(
        self,
        level,
        kogadgets,
        xp,
        kothrownitem,
        damageweapontwo,
        loses,
        damagethrownitem,
        wins,
        weaponone,
        weapontwo,
        matchtime,
        damageunarmed,
        id,
        ko,
        suicide,
        koweapontwo,
        damagegadgets,
        damagedealt,
        death,
        kounarmed,
        name,
        koweaponone,
        damagetaken,
        timeheldweaponone,
        games,
        damageweaponone,
        winperc,
        teamko,
        timeheldweapontwo
    ):
        return self.locale.STATS_PLAYER_LEGEND.format(
            level=level,
            kogadgets=kogadgets,
            xp=xp,
            kothrownitem=kothrownitem,
            damageweapontwo=damageweapontwo,
            loses=loses,
            damagethrownitem=damagethrownitem,
            wins=wins,
            weaponone=weaponone,
            weapontwo=weapontwo,
            matchtime=matchtime,
            damageunarmed=damageunarmed,
            id=id,
            ko=ko,
            suicide=suicide,
            koweapontwo=koweapontwo,
            damagegadgets=damagegadgets,
            damagedealt=damagedealt,
            death=death,
            kounarmed=kounarmed,
            name=name,
            koweaponone=koweaponone,
            damagetaken=damagetaken,
            timeheldweaponone=timeheldweaponone,
            games=games,
            damageweaponone=damageweaponone,
            winperc=winperc,
            teamko=teamko,
            timeheldweapontwo=timeheldweapontwo
        )

    def stats_ranked(
        self,
        rating,
        wins,
        peak,
        tier,
        region,
        games,
        elo_reset,
        glory,
        loses
    ):
        return self.locale.STATS_RANKED.format(
            rating=rating,
            wins=wins,
            peak=peak,
            tier=tier,
            region=region,
            games=games,
            elo_reset=elo_reset,
            glory=glory,
            loses=loses
        )

    def stats_ranked_team(
        self,
        rating,
        peak,
        wins,
        tier,
        region,
        games,
        teamname,
        loses
    ):
        return self.locale.STATS_RANKED_TEAM.format(
            rating=rating,
            peak=peak,
            wins=wins,
            tier=tier,
            region=region,
            games=games,
            teamname=teamname,
            loses=loses
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

    def usage_search(self):
        return self.locale.USAGE_SEARCH

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