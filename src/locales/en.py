SEARCH = "search"
LANGUAGE = "language"

# Descriptions
DESCRIPTION_LANGUAGE = "Change the language of the bot"
DESCRIPTION_SEARCH = "Search for a player"
DESCRIPTION_START = "Shows the first start message"
DESCRIPTION_ID = "Shows the statistics of a player with the specified ID"
DESCRIPTION_ME = "Shows the statistics of the player set as default"

WELCOME = (
    "Welcome <b>{name}</b>.\n\n"
    "Here are the commands currently available:\n\n"
    f"🔍 • /{SEARCH} - {DESCRIPTION_SEARCH}\n"
    f"🆔 • /id - {DESCRIPTION_ID}\n"
    f"👤 • /me - {DESCRIPTION_ME}\n"
    f"🌐 • /{LANGUAGE} - {DESCRIPTION_LANGUAGE}"
)


# Usages
USAGE_SEARCH = (
    "Use the <b>/search</b> command to search for a player.\n\n"
    "Example: <code>/search nickoehler</code>"
)
USAGE_ID = (
    "Use the <b>/id</b> command to show the statistics of a player with the specified ID.\n\n"
    "Example: <code>/id 2316541</code>"
)

# Errors
EERROR_LENGTH = "The search query must be between 2 and 32 characters"
ERROR_SEARCH_RESULT = "No player found searching <b>{query}</b>"
ERROR_LEGEND_RESULT = "No legend found"
ERROR_TEAM_RESULT = "No team found"
ERROR_PLAYER_NOT_FOUND = "Player with ID <b>{id}</b> not found"
ERROR_NO_CLAN_DATA = "This player is not in a clan anymore"
ERROR_NO_RANKED_DATA = "This player has not played any ranked games yet"
ERROR_NO_TEAM_DATA = "This player has not played any ranked team games yet"
ERROR_MISSING_DEFAULT_PLAYER = (
    "You need to set a player as default to execute this command."
)
ERROR_GENERIC = (
    "An error occurred:\n\n"
    "<code>{error}</code>\n\n"
    "If you want to help development, "
    "open a detailed issue on how to reproduce the error you encountered.\n"
    "Before opening a new issue, make sure that the error has not already been reported"
)
# Results
RESULTS_SEARCH = "Search results:\n<b>{query}</b>\n<b>{current}/{total}</b>"
RESULTS_TEAMS = "Teams:\n<b>{current}/{total}</b>"
RESULTS_LEGENDS = "Legends:\n<b>{current}/{total}</b>"

# Status messages
STATUS_LANGUAGE_CHANGED = "Language changed successfully"
STATUS_LANGUAGE_UNCHANGED = "Language unchanged"
STATUS_DEFAULT_PLAYER_SET = "Player set as default"

# Buttons
BUTTON_GENERAL = "⚔️ • GENERAL STATS • ⚔️"
BUTTON_LEGEND = "🥷 • LEGENDS • 🥷"
BUTTON_DEFAULT_PLAYER = "👤 • SET AS DEFAULT • 👤"
BUTTON_RANKED_SOLO = "🏆 • RANKED 1V1 • 🏆"
BUTTON_RANKED_TEAM = "🏆 • RANKED 2V2 • 🏆"
BUTTON_TEAMMATE = "🙋‍♂️ • TEAM MATE • 🙋‍♂️"
BUTTON_ISSUE = "🐙 • OPEN AN ISSUE • 🐱"
BUTTON_CLAN = "🎖 • CLAN • 🎖"
BUTTON_CLOSE = "❌ • CLOSE • ❌"

# Time
TIME_DAYS = "Days : {t}"
TIME_HOURS = "Hours : {t}"
TIME_MINUTES = "Minutes : {t}"
TIME_SECONDS = "Seconds : {t}"

# Stats
STATS_BASE = "🆔 • ID:<b> {id} </b>\n🙋‍♂️ • Name: <b>{name}</b>\n\n"
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
🌎 • Region: <b>{region}</b>

💎 • Estimated glory: <b>{glory}</b>
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
📅 • Creation date: <b>{date}</b>

<b>{current}/{total}</b>"""

STATS_LEGEND = """🥷 • <b>LEGEND</b> • 🥷

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
