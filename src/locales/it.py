# Commands
SEARCH = "cerca"
LANGUAGE = "lingua"
WEAPONS = "armi"
MISSING = "mancanti"

# Descriptions
DESCRIPTION_LANGUAGE = "Cambia la lingua del bot"
DESCRIPTION_SEARCH = "Cerca un giocatore"
DESCRIPTION_START = "Mostra il messaggio di primo avvio"
DESCRIPTION_ID = "Mostra le statistiche di un giocatore con l'ID specificato"
DESCRIPTION_LEGEND = "Mostra le statistiche di una legend"
DESCRIPTION_WEAPONS = "Cerca una legend attraverso le tipologie di armi"
DESCRIPTION_ME = "Mostra le statistiche del giocatore impostato come predefinito"
DESCRIPTION_MISSING = "Mostra le combinazioni di armi mancanti"
DESCRIPTION_LIVE = "Mostra il tempo mancante alla prossima live di Brawlhalla su twitch"

WELCOME = (
    "Benvenuto <b>{name}</b>.\n\n"
    "Ecco i comandi disponibili attualmente:\n\n"
    f"🔍 • /{SEARCH} - {DESCRIPTION_SEARCH}\n"
    f"🆔 • /id - {DESCRIPTION_ID}\n"
    f"👤 • /me - {DESCRIPTION_ME}\n"
    f"🥷 • /legend - {DESCRIPTION_LEGEND}\n"
    f"🗡️ • /{WEAPONS} - {DESCRIPTION_WEAPONS}\n"
    f"❓ • /{MISSING} - {DESCRIPTION_MISSING}\n"
    f"🎤 • /live - {DESCRIPTION_LIVE}\n"
    f"🌐 • /{LANGUAGE} - {DESCRIPTION_LANGUAGE}"
)

# Usages
USAGE_SEARCH = (
    "Tocca uno dei pulsanti qui sotto per iniziare la ricerca di un giocatore"
)
USAGE_ID = (
    "Usa il comando <b>/id</b> per mostrare le statistiche di un giocatore l'ID specificato.\n\n"
    "Esempio: <code>/id 2316541</code>"
)
USAGE_INLINE = "Digita il nome del giocatore che stai cercando"

# Errors
ERROR_LENGTH = "La lunghezza della ricerca deve essere tra 2 e 32 caratteri"
ERROR_SEARCH_RESULT = "Nessun giocatore trovato cercando <b>{query}</b>"
ERROR_LEGEND_RESULT = "Nessuna legend trovata"
ERROR_TEAM_RESULT = "Nessuna squadra trovata"
ERROR_PLAYER_RESULT = "Nessun giocatore trovato"
ERROR_PLAYER_NOT_FOUND = "Giocatore con ID <b>{id}</b> non trovato"
ERROR_NO_CLAN_DATA = "Questo giocatore non è più in un clan"
ERROR_NO_RANKED_DATA = "Questo giocatore non ha ancora giocato partite classificate"
ERROR_NO_TEAM_DATA = (
    "Questo giocatore non ha ancora giocato partite classificate a squadre"
)
ERROR_MISSING_DEFAULT_PLAYER = (
    "Devi prima impostare un giocatore come predefinito per eseguire questo comando"
)
ERROR_LEGEND_NOT_FOUND = "La legenda <b>{query}</b> non è stata trovata"
ERROR_WEAPON_NOT_FOUND = "Non sono presenti armi cercando <b>{query}</b>"
ERROR_MISSING_WEAPONS_COMBINATION_NOT_FOUND = (
    "Non sono presenti combinazioni di armi mancanti cercando <b>{query}</b>"
)
ERROR_FLOOD_WAIT = (
    "Stai inviando troppe richieste in un breve periodo di tempo.\n"
    "Sei stato bloccato per <b>{seconds}</b> secondi."
)
ERROR_API_OFFLINE = (
    "Le API di Brawlhalla sono temporaneamente offline.\nRiprova più tardi."
)
ERROR_GENERIC = (
    "Si è verificato un errore:\n\n"
    "<code>{error}</code>\n\n"
    "Se vuoi aiutare lo sviluppo, "
    "apri una issue dettagliata su come riprodurre l'errore che hai riscontrato.\n"
    "Prima di aprire una nuova issue assicurati che l'errore non sia già stato segnalato"
)
ERROR_NO_LIVES = "Non sono previste live di Brawlhalla su twitch"

# Results
RESULTS_TEAMS = "Squadre:"
RESULTS_LEGENDS = (
    "Tutti i legends:\n\n"
    "<i>NB: È anche possibile scrivere <code>/legend nome</code> per vedere direttamente le statistiche di una specifica legend.</i>\n\n"
    "Ad esempio: <code>/legend bodvar</code>"
)
RESULTS_LEGENDS_WITH_WEAPON = "Legends che utilizzano <b>{weapon}</b>:"
RESULTS_MISSING_WEAPONS_COMBINATION = (
    "Combinazioni di armi mancanti:\n\n<b>{weapons}</b>\n\n"
    f"<i>NB: È anche possibile scrivere <code>/{MISSING} arma</code> per vedere tutte le combinazioni di armi mancanti.</i>\n\n"
    f"Ad esempio: <code>/{MISSING} sword</code>"
)
RESULTS_WEAPONS = (
    "Tutte le armi:\n\n"
    f"<i>NB: È anche possibile scrivere <code>/{WEAPONS} arma</code> per vedere tutti i legends che utilizzano questa specifica arma.</i>\n\n"
    f"Ad esempio: <code>/{WEAPONS} sword</code>\n\n"
    f"<i>In alternativa è possibile anche scrivere <code>/{WEAPONS} arma1 arma2</code> per vedere direttamente la legend che utilizza queste armi.</i>\n\n"
    f"Ad esempio: <code>/{WEAPONS} sword hammer</code>"
)
RESULTS_MISSING_WEAPONS_COMBINATION_WITH_WEAPON = (
    "Combinazioni di armi mancanti che utilizzano <b>{weapon}</b>:\n\n<b>{weapons}</b>"
)

RESULTS_LIVE = (
    "Prossima stream: <b>{title}</b>\n\n"
    "Inizia tra: <b>{start}</b>\n"
    "Durata: <b>{end}</b>"
)

# Status messages
STATUS_LANGUAGE_CHANGED = "La lingua è stata cambiata correttamente"
STATUS_LANGUAGE_UNCHANGED = "La lingua non è stata cambiata"
STATUS_DEFAULT_PLAYER_SET = "Giocatore impostato come predefinito"

# Buttons
BUTTON_GENERAL = "⚔️ • STATS GENERALI • ⚔️"
BUTTON_LEGENDS = "🥷 • LEGENDS • 🥷"
BUTTON_DEFAULT_PLAYER = "👤 • IMPOSTA PREDEFINITO • 👤"
BUTTON_RANKED_SOLO = "🏆 • CLASSIFICATA 1V1 • 🏆"
BUTTON_RANKED_TEAM = "🏆 • CLASSIFICATA 2V2 • 🏆"
BUTTON_TEAMMATE = "🙋‍♂️ • COMPAGNO DI SQUADRA • 🙋‍♂️"
BUTTON_ISSUE = "🐙 • APRI UNA ISSUE • 🐱"
BUTTON_CLAN = "🎖 • CLAN • 🎖"
BUTTON_CLOSE = "❌ • CHIUDI • ❌"
BUTTON_WEAPONS = "🔫 • ARMI • 🔫"
BUTTON_SHARE = "💬 • CONDIVIDI • 💬"
BUTTON_SEARCH_ALL = "🌍 • RICERCA GLOBALE • 🌍"
BUTTON_SEARCH_AUS = "🇦🇺 • RICERCA IN AUS • 🇦🇺"
BUTTON_SEARCH_BRZ = "🇧🇷 • RICERCA IN BRZ • 🇧🇷"
BUTTON_SEARCH_EU = "🇪🇺 • RICERCA IN EU • 🇪🇺"
BUTTON_SEARCH_JPN = "🇯🇵 • RICERCA IN JPN • 🇯🇵"
BUTTON_SEARCH_ME = "🇦🇪 • RICERCA IN ME • 🇦🇪"
BUTTON_SEARCH_SA = "🇿🇦 • RICERCA IN SA • 🇿🇦"
BUTTON_SEARCH_SEA = "🇨🇳 • RICERCA IN SEA • 🇨🇳"
BUTTON_SEARCH_US_E = "🇺🇸 • RICERCA IN US-E • 🇺🇸"
BUTTON_SEARCH_US_W = "🇺🇸 • RICERCA IN US-W • 🇺🇸"

# Time
TIME_DAYS = "Giorni: {t}"
TIME_HOURS = "Ore: {t}"
TIME_MINUTES = "Minuti: {t}"
TIME_SECONDS = "Secondi: {t}"

# Stats
STATS_BASE = "🆔 • ID:<b> {id} </b>\n👤 • Nome: <b>{name}</b>"
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
🌎 • Regione: <b>{region}</b>"""

STATS_GLORY_ELO = """💎 • Glory stimata: <b>{glory}</b>
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
📅 • Data di creazione: <b>{date}</b>"""

STATS_PLAYER_LEGEND = """🥷 • <b>LEGEND</b> • 🥷

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

STATS_LEGEND = """🎮 • <b>STATISTICHE LEGEND</b> • 🎮

🆔 • ID: <b>{legend_id}</b>
🔖 • Nome: <a href="{url}"><b>{bio_name}</b></a>
🎖️ • Alias: <b>{bio_aka}</b>

🗡️ • Arma 1: <b>{weapon_one}</b>
🗡️ • Arma 2: <b>{weapon_two}</b>

💪 • Forza: <b>{strength}</b>
🏹 • Destrezza: <b>{dexterity}</b>
🛡️ • Difesa: <b>{defense}</b>
🏃 • Velocità: <b>{speed}</b>"""
