SEARCH = "cerca"
LANGUAGE = "lingua"

# Descriptions
DESCRIPTION_LANGUAGE = "Cambia la lingua del bot"
DESCRIPTION_SEARCH = "Cerca un giocatore"
DESCRIPTION_START = "Mostra il messaggio di primo avvio"
DESCRIPTION_ID = "Mostra le statistiche di un giocatore con l'ID specificato"
DESCRIPTION_ME = "Mostra le statistiche del giocatore impostato come predefinito"

WELCOME = (
    "Benvenuto <b>{name}</b>.\n\n"
    "Ecco i comandi disponibili attualmente:\n\n"
    f"🔍 • /{SEARCH} - {DESCRIPTION_SEARCH}\n"
    f"🆔 • /id - {DESCRIPTION_ID}\n"
    f"👤 • /me - {DESCRIPTION_ME}\n"
    f"🌐 • /{LANGUAGE} - {DESCRIPTION_LANGUAGE}"
)

# Usages
USAGE_SEARCH = (
    "Usa il comando <b>/cerca</b> per ricercare un giocatore.\n\n"
    "Esempio: <code>/cerca nickoehler</code>"
)
USAGE_ID = (
    "Usa il comando <b>/id</b> per mostrare le statistiche di un giocatore l'ID specificato.\n\n"
    "Esempio: <code>/id 2316541</code>"
)
# Errors
ERROR_LENGTH = "La lunghezza della ricerca deve essere tra 2 e 32 caratteri"
ERROR_SEARCH_RESULT = "Nessun giocatore trovato cercando <b>{query}</b>"
ERROR_LEGEND_RESULT = "Nessuna legend trovata"
ERROR_TEAM_RESULT = "Nessuna squadra trovata"
ERROR_PLAYER_NOT_FOUND = "Giocatore con ID <b>{id}</b> non trovato"
ERROR_NO_CLAN_DATA = "Questo giocatore non è più in un clan"
ERROR_NO_RANKED_DATA = "Questo giocatore non ha ancora giocato partite classificate"
ERROR_NO_TEAM_DATA = (
    "Questo giocatore non ha ancora giocato partite classificate a squadre"
)
ERROR_MISSING_DEFAULT_PLAYER = (
    "Devi prima impostare un giocatore come predefinito per eseguire questo comando"
)
ERROR_GENERIC = (
    "Si è verificato un errore:\n\n"
    "<code>{error}</code>\n\n"
    "Se vuoi aiutare lo sviluppo, "
    "apri una issue dettagliata su come riprodurre l'errore che hai riscontrato.\n"
    "Prima di aprire una nuova issue assicurati che l'errore non sia già stato segnalato"
)

# Results
RESULTS_SEARCH = "Risultati della ricerca:\n<b>{query}</b>\n<b>{current}/{total}</b>"
RESULTS_TEAMS = "Squadre:\n<b>{current}/{total}</b>"
RESULTS_LEGENDS = "Legends:\n<b>{current}/{total}</b>"

# Status messages
STATUS_LANGUAGE_CHANGED = "La lingua è stata cambiata correttamente"
STATUS_LANGUAGE_UNCHANGED = "La lingua non è stata cambiata"
STATUS_DEFAULT_PLAYER_SET = "Giocatore impostato come predefinito"

# Buttons
BUTTON_GENERAL = "⚔️ • STATS GENERALI • ⚔️"
BUTTON_LEGEND = "🥷 • LEGENDS • 🥷"
BUTTON_DEFAULT_PLAYER = "👤 • IMPOSTA PREDEFINITO • 👤"
BUTTON_RANKED_SOLO = "🏆 • CLASSIFICATA 1V1 • 🏆"
BUTTON_RANKED_TEAM = "🏆 • CLASSIFICATA 2V2 • 🏆"
BUTTON_TEAMMATE = "🙋‍♂️ • COMPAGNO DI SQUADRA • 🙋‍♂️"
BUTTON_ISSUE = "🐙 • APRI UNA ISSUE • 🐱"
BUTTON_CLAN = "🎖 • CLAN • 🎖"
BUTTON_CLOSE = "❌ • CHIUDI • ❌"

# Time
TIME_DAYS = "Giorni: {t}"
TIME_HOURS = "Ore: {t}"
TIME_MINUTES = "Minuti: {t}"
TIME_SECONDS = "Secondi: {t}"

# Stats
STATS_BASE = "🆔 • ID:<b> {id} </b>\n🙋‍♂️ • Nome: <b>{name}</b>\n\n"
STATS_GENERAL = """⚔ • <b>GENERICHE</b> • ⚔

🎖 • Clan: <b>{clan}</b>
🆙 • Lv: <b>{level}</b>
🔺 • XP: <b>{xp}</b>
⌚ • Legend più usata: <b>{most_used_legend}</b>
⌛ • Tempo di gioco:
<b>{total_game_time}</b>

🎮 • Partite Giocate: <b>{games}</b>
🥇 • Partite Vinte: <b>{wins}</b>
🥉 • Partite Perse: <b>{loses}</b>
⚖️ • Perc. di Vincita: <b>{winperc}%</b>
👊 • KO totali: <b>{totalko}</b>
⚰ • Morti totali: <b>{totaldeath}</b>
💀 • Suicidi totali: <b>{totalsuicide}</b>
😐 • KO al compagno di squadra: <b>{totalteamko}</b>

💣 <b>BOMBE</b> 💣
├─► KO: <b>{kobomb}</b>
╰─► Danni: <b>{damagebomb}</b>

💥 <b>MINE</b> 💥
├─► KO: <b>{komine}</b>
╰─► Danni: <b>{damagemine}</b>

☀️ <b>PALLE CHIODATE</b> ☀️
├─► KO: <b>{kospikeball}</b>
╰─► Danni: <b>{damagespikeball}</b>

👟 <b>SIDE KICK</b> 👟
├─► KO: <b>{kosidekick}</b>
╰─► Danni: <b>{damagesidekick}</b>

❄️ <b>PALLE DI NEVE</b> ❄️
├─► KO: <b>{kosnowball}</b>
╰─► Colpi: <b>{hitsnowball}</b>"""

STATS_RANKED = """🏆 • <b>CLASSIFICATA 1v1</b> • 🏆

🔶 • Elo Attuale: <b>{rating}</b>
🔷 • Elo Massimo: <b>{peak}</b>
👑 • Tier: <b>{tier}</b>

🎮 • Partite Giocate: <b>{games}</b>
🥇 • Partite Vinte: <b>{wins}</b>
🥉 • Partite Perse: <b>{loses}</b>
🌎 • Regione: <b>{region}</b>

💎 • Glory stimata: <b>{glory}</b>
👑 • Reset elo stimato: <b>{elo_reset}</b>"""

STATS_RANKED_TEAM = """🏆 • <b>CLASSIFICATA 2v2</b> • 🏆

👥 • Team: <b>{teamname}</b>

🔶 • Elo Attuale: <b>{rating}</b>
🔷 • Elo Massimo: <b>{peak}</b>
👑 • Tier: <b>{tier}</b>

🎮 • Partite Giocate: <b>{games}</b>
🥇 • Partite Vinte: <b>{wins}</b>
🥉 • Partite Perse: <b>{loses}</b>
🌎 • Regione: <b>{region}</b>"""

STATS_CLAN = """🆔 • Clan ID: <b>{id}</b>
👑 • Nome del clan: <b>{name}</b>

🔺 • XP: <b>{xp}</b>
👥 • Membri: <b>{num}</b>
📅 • Data di creazione: <b>{date}</b>

<b>{current}/{total}</b>"""

STATS_LEGEND = """🥷 • <b>LEGEND</b> • 🥷

🆔 • Legend ID: <b>{id}</b>
🥷 • Nome del legend: <b>{name}</b>

🆙 • Lv: <b>{level}</b>
🔺 • XP: <b>{xp}</b>
⌚ • Tempo di gioco:
<b>{matchtime}</b>

🎮 • Partite Giocate: <b>{games}</b>
🥇 • Partite Vinte: <b>{wins}</b>
🥉 • Partite Perse: <b>{loses}</b>
⚖️ • Perc. di Vincita: <b>{winperc}%</b>
👊 • KO totali: <b>{ko}</b>
⚰ • Morti totali: <b>{death}</b>
💀 • Suicidi totali: <b>{suicide}</b>
💥 • Danni totali inflitti: <b>{damagedealt}</b>
💢 • Danni totali reicevuti: <b>{damagetaken}</b>
😐 • KO al compagno di squadra: <b>{teamko}</b>

🔫 <b>ARMI</b> 🔫
├─► Tempo {weaponone}: <b>{timeheldweaponone}</b>
├─► KO {weaponone}: <b>{koweaponone}</b>
├─► Danni {weaponone}: <b>{damageweaponone}</b>
├─► Tempo {weapontwo}: <b>{timeheldweapontwo}</b>
├─► KO con {weapontwo}: <b>{koweapontwo}</b>
╰─► Danni {weapontwo}: <b>{damageweapontwo}</b>

👊 <b>SENZA ARMI</b> 👊
├─► KO: <b>{kounarmed}</b>
╰─► Danni: <b>{damageunarmed}</b>

📱 <b>GADGETS</b>📱
├─► KO: <b>{kogadgets}</b>
╰─► Danni: <b>{damagegadgets}</b>

🎯 <b>LANCIO OGGETTI</b> 🎯
├─► KO: <b>{kothrownitem}</b>
╰─► Danni: <b>{damagethrownitem}</b>"""
