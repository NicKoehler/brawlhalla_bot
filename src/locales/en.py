# Commands
SEARCH = "search"
LANGUAGE = "language"
WEAPONS = "weapons"
MISSING = "missing"

# Descriptions
DESCRIPTION_LANGUAGE = "Change the language of the bot"
DESCRIPTION_SEARCH = "Search for a player"
DESCRIPTION_START = "Shows the first start message"
DESCRIPTION_ID = "Shows the statistics of a player with the specified ID"
DESCRIPTION_LEGEND = "Shows the statistics of a legend"
DESCRIPTION_WEAPONS = "Search for a legend through weapon types"
DESCRIPTION_MISSING = "Shows missing weapons combinations"
DESCRIPTION_ME = "Shows the statistics of the player set as default"

WELCOME = (
    "Welcome <b>{name}</b>.\n\n"
    "Here are the commands currently available:\n\n"
    f"🔍 • /{SEARCH} - {DESCRIPTION_SEARCH}\n"
    f"🆔 • /id - {DESCRIPTION_ID}\n"
    f"👤 • /me - {DESCRIPTION_ME}\n"
    f"🥷 • /legend - {DESCRIPTION_LEGEND}\n"
    f"🗡️ • /{WEAPONS} - {DESCRIPTION_WEAPONS}\n"
    f"🌐 • /{LANGUAGE} - {DESCRIPTION_LANGUAGE}"
)

# Usages
USAGE_SEARCH = "Tap one of the buttons bellow to start searching for a player"
USAGE_ID = (
    "Use the <b>/id</b> command to show the statistics of a player with the specified ID.\n\n"
    "Example: <code>/id 2316541</code>"
)
USAGE_INLINE = "Enter the name of the player you want to search"

# Errors
ERROR_LENGTH = "The search query must be between 2 and 32 characters"
ERROR_SEARCH_RESULT = "No player found searching <b>{query}</b>"
ERROR_LEGEND_RESULT = "No legend found"
ERROR_TEAM_RESULT = "No team found"
ERROR_PLAYER_RESULT = "No player found"
ERROR_PLAYER_NOT_FOUND = "Player with ID <b>{id}</b> not found"
ERROR_NO_CLAN_DATA = "This player is not in a clan anymore"
ERROR_NO_RANKED_DATA = "This player has not played any ranked games yet"
ERROR_NO_TEAM_DATA = "This player has not played any ranked team games yet"
ERROR_MISSING_DEFAULT_PLAYER = (
    "You need to set a player as default to execute this command."
)
ERROR_LEGEND_NOT_FOUND = "There are no legends matching <b>{query}</b>"
ERROR_WEAPON_NOT_FOUND = "There are no weapons matching <b>{query}</b>"
ERROR_MISSING_WEAPONS_COMBINATION_NOT_FOUND = (
    "There are no weapons combination matching <b>{query}</b>"
)
ERROR_FLOOD_WAIT = (
    "You are sending too many requests in a short period of time.\n"
    "You have been blocked for <b>{seconds}</b> seconds."
)
ERROR_API_OFFLINE = "Brawlhalla's API are temporarily offline.\nTry again later."
ERROR_GENERIC = (
    "An error occurred:\n\n"
    "<code>{error}</code>\n\n"
    "If you want to help development, "
    "open a detailed issue on how to reproduce the error you encountered.\n"
    "Before opening a new issue, make sure that the error has not already been reported"
)

# Results
RESULTS_TEAMS = "Teams:"
RESULTS_LEGENDS = "Legends:"
RESULTS_LEGENDS_WITH_WEAPON = "Legends with weapons <b>{weapon}</b>"
RESULTS_MISSING_WEAPONS_COMBINATION = (
    "Missing weapons combinations:\n\n<b>{weapons}</b>"
)
RESULTS_MISSING_WEAPONS_COMBINATION_WITH_WEAPON = (
    "Missing weapons combinations with <b>{weapon}</b>:\n\n<b>{weapons}</b>"
)

# Status messages
STATUS_LANGUAGE_CHANGED = "Language changed successfully"
STATUS_LANGUAGE_UNCHANGED = "Language unchanged"
STATUS_DEFAULT_PLAYER_SET = "Player set as default"

# Buttons
BUTTON_GENERAL = "⚔️ • GENERAL STATS • ⚔️"
BUTTON_LEGENDS = "🥷 • LEGENDS • 🥷"
BUTTON_DEFAULT_PLAYER = "👤 • SET AS DEFAULT • 👤"
BUTTON_RANKED_SOLO = "🏆 • RANKED 1V1 • 🏆"
BUTTON_RANKED_TEAM = "🏆 • RANKED 2V2 • 🏆"
BUTTON_TEAMMATE = "🙋‍♂️ • TEAM MATE • 🙋‍♂️"
BUTTON_ISSUE = "🐙 • OPEN AN ISSUE • 🐱"
BUTTON_CLAN = "🎖 • CLAN • 🎖"
BUTTON_CLOSE = "❌ • CLOSE • ❌"
BUTTON_WEAPONS = "🔫 • WEAPONS • 🔫"
BUTTON_SHARE = "💬 • SHARE • 💬"
BUTTON_SEARCH_ALL = "🌍 • SEARCH ALL • 🌍"
BUTTON_SEARCH_AUS = "🇦🇺 • SEARCH AUS • 🇦🇺"
BUTTON_SEARCH_BRZ = "🇧🇷 • SEARCH BRZ • 🇧🇷"
BUTTON_SEARCH_EU = "🇪🇺 • SEARCH EU • 🇪🇺"
BUTTON_SEARCH_JPN = "🇯🇵 • SEARCH JPN • 🇯🇵"
BUTTON_SEARCH_ME = "🇦🇪 • SEARCH ME • 🇦🇪"
BUTTON_SEARCH_SA = "🇿🇦 • SEARCH SA • 🇿🇦"
BUTTON_SEARCH_SEA = "🇨🇳 • SEARCH SEA • 🇨🇳"
BUTTON_SEARCH_US_E = "🇺🇸 • SEARCH US-E • 🇺🇸"
BUTTON_SEARCH_US_W = "🇺🇸 • SEARCH US-W • 🇺🇸"

# Time
TIME_DAYS = "Days : {t}"
TIME_HOURS = "Hours : {t}"
TIME_MINUTES = "Minutes : {t}"
TIME_SECONDS = "Seconds : {t}"

# Stats
STATS_BASE = "🆔 • ID:<b> {id} </b>\n🙋‍♂️ • Name: <b>{name}</b>"
STATS_GENERAL = """⚔ • <b>GENERAL STATS</b> • ⚔

🎖 • Clan: <b>{clan}</b>
🆙 • Lv: <b>{level}</b>
🔺 • XP: <b>{xp}</b>
⌚ • Most used legend: <b>{most_used_legend}</b>
⌛ • Total Playtime:
<b>{total_game_time}</b>

🎮 • Games played: <b>{games}</b>
🥇 • Games won: <b>{wins}</b>
🥉 • Games lost: <b>{loses}</b>
⚖ • Win percentage: <b>{winperc}%</b>
👊 • Total KOs: <b>{totalko}</b>
⚰ • Total Deaths: <b>{totaldeath}</b>
💀 • Total Suicides: <b>{totalsuicide}</b>
😐 • Team KOs: <b>{totalteamko}</b>

💣 <b>BOMBS</b> 💣
├─► KOs: <b>{kobomb}</b>
╰─► Damage: <b>{damagebomb}</b>

💥 <b>MINES</b> 💥
├─► KOs: <b>{komine}</b>
╰─► Damage: <b>{damagemine}</b>

☀️ <b>SPIKEBALLS</b> ☀️
├─► KOs: <b>{kospikeball}</b>
╰─► Damage: <b>{damagespikeball}</b>

👟 <b>SIDE KICK</b> 👟
├─► KOs: <b>{kosidekick}</b>
╰─► Damage: <b>{damagesidekick}</b>

❄️ <b>SNOWBALLS</b> ❄️
├─► KOs: <b>{kosnowball}</b>
╰─► Hits: <b>{hitsnowball}</b>"""

STATS_RANKED = """🏆 • <b>RANKED 1v1</b> • 🏆

🔶 • Current elo: <b>{rating}</b>
🔷 • Elo peak: <b>{peak}</b>
👑 • Tier: <b>{tier}</b>

🎮 • Games played: <b>{games}</b>
🥇 • Games won: <b>{wins}</b>
🥉 • Games lost: <b>{loses}</b>
🌎 • Region: <b>{region}</b>"""

STATS_GLORY_ELO = """💎 • Estimated glory: <b>{glory}</b>
👑 • Estimated elo reset: <b>{elo_reset}</b>"""

STATS_RANKED_TEAM = """🏆 • <b>RANKED 2v2</b> • 🏆

👥 • Team: <b>{teamname}</b>

🔶 • Current elo: <b>{rating}</b>
🔷 • Elo peak: <b>{peak}</b>
👑 • Tier: <b>{tier}</b>

🎮 • Games played: <b>{games}</b>
🥇 • Games won: <b>{wins}</b>
🥉 • Games lost: <b>{loses}</b>
🌎 • Region: <b>{region}</b>"""

STATS_CLAN = """🆔 • Clan ID:<b> {id} </b>
👑 • Clan name: <b>{name}</b>

🔺 • XP: <b>{xp}</b>
👥 • Members: <b>{num}</b>
📅 • Creation date: <b>{date}</b>"""

STATS_PLAYER_LEGEND = """🥷 • <b>LEGEND</b> • 🥷

🆔 • Legend ID: <b>{id}</b>
🥷 • Legend Name: <b>{name}</b>

🆙 • Level: <b>{level}</b>
🔺 • XP: <b>{xp}</b>
⌚ • Playtime:
<b>{matchtime}</b>

🎮 • Matches Played: <b>{games}</b>
🥇 • Matches Won: <b>{wins}</b>
🥉 • Matches Lost: <b>{loses}</b>
⚖️ • Win Percentage: <b>{winperc}%</b>
👊 • Total KOs: <b>{ko}</b>
⚰ • Total Deaths: <b>{death}</b>
💀 • Total Suicides: <b>{suicide}</b>
💥 • Total damage dealt: <b>{damagedealt}</b>
💢 • Total damage taken: <b>{damagetaken}</b>
😐 • Team KOs: <b>{teamko}</b>

🔫 <b>WEAPONS</b> 🔫
├─► {weaponone} Time Held: <b>{timeheldweaponone}</b>
├─► {weaponone} KOs: <b>{koweaponone}</b>
├─► {weaponone} Damage: <b>{damageweaponone}</b>
├─►{weapontwo} Time Held: <b>{timeheldweapontwo}</b>
├─►{weapontwo} KOs: <b>{koweapontwo}</b>
╰─►{weapontwo} Damage: <b>{damageweapontwo}</b>

👊 <b>UNARMED</b> 👊
├─► KOs: <b>{kounarmed}</b>
╰─► Damage: <b>{damageunarmed}</b>

📱 <b>GADGETS</b>📱
├─► KOs: <b>{kogadgets}</b>
╰─► Damage: <b>{damagegadgets}</b>

🎯 <b>THROWN ITEMS</b> 🎯
├─► KOs: <b>{kothrownitem}</b>
╰─► Damage: <b>{damagethrownitem}</b>"""

STATS_LEGEND = """🎮 • <b>LEGEND STATS</b> • 🎮

🆔 • ID: <b>{legend_id}</b>
🔖 • Name: <b>{bio_name}</b>
🎖️ • Alias: <b>{bio_aka}</b>

🗡️ • Weapon 1: <b>{weapon_one}</b>
🗡️ • Weapon 2: <b>{weapon_two}</b>

💪 • Strength: <b>{strength}</b>
🏹 • Dexterity: <b>{dexterity}</b>
🛡️ • Defense: <b>{defense}</b>
🏃 • Speed: <b>{speed}</b>"""


# Other
ALL_WEAPONS = "All Weapons:"
