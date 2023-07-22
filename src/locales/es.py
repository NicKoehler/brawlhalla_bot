# Comandos
SEARCH = "buscar"
LANGUAGE = "idioma"
WEAPONS = "armas"
MISSING = "faltante"

# Descripciones
DESCRIPTION_LANGUAGE = "Cambiar el idioma del bot"
DESCRIPTION_SEARCH = "Buscar un jugador"
DESCRIPTION_START = "Muestra el primer mensaje de inicio"
DESCRIPTION_ID = "Muestra las estadísticas de un jugador con el ID especificado"
DESCRIPTION_LEGEND = "Muestra las estadísticas de una leyenda"
DESCRIPTION_WEAPONS = "Buscar una leyenda a través de tipos de armas"
DESCRIPTION_MISSING = "Muestra combinaciones de armas faltantes"
DESCRIPTION_ME = "Muestra las estadísticas del jugador establecido como predeterminado"
DESCRIPTION_LIVE = "Muestra el tiempo restante para la próxima transmisión en vivo de Brawlhalla en Twitch"

WELCOME = (
    "Bienvenido <b>{name}</b>.\n\n"
    "Aquí están los comandos actualmente disponibles:\n\n"
    f"🔍 • /{SEARCH} - {DESCRIPTION_SEARCH}\n"
    f"🆔 • /id - {DESCRIPTION_ID}\n"
    f"👤 • /me - {DESCRIPTION_ME}\n"
    f"🥷 • /legend - {DESCRIPTION_LEGEND}\n"
    f"🗡️ • /{WEAPONS} - {DESCRIPTION_WEAPONS}\n"
    f"❓ • /{MISSING} - {DESCRIPTION_MISSING}\n"
    f"🎮 • /live - {DESCRIPTION_LIVE}\n"
    f"🌐 • /{LANGUAGE} - {DESCRIPTION_LANGUAGE}"
)

# Usos
USAGE_SEARCH = (
    "Toca uno de los botones a continuación para comenzar a buscar un jugador"
)
USAGE_ID = (
    "Use el comando <b>/id</b> para mostrar las estadísticas de un jugador con el ID especificado.\n\n"
    "Ejemplo: <code>/id 2316541</code>"
)
USAGE_INLINE = "Ingrese el nombre del jugador que desea buscar"

# Errores
ERROR_LENGTH = "La consulta de búsqueda debe tener entre 2 y 32 caracteres"
ERROR_SEARCH_RESULT = "No se encontró ningún jugador buscando <b>{query}</b>"
ERROR_LEGEND_RESULT = "No se encontró ninguna leyenda"
ERROR_TEAM_RESULT = "No se encontró ningún equipo"
ERROR_PLAYER_RESULT = "No se encontró ningún jugador"
ERROR_PLAYER_NOT_FOUND = "Jugador con ID <b>{id}</b> no encontrado"
ERROR_NO_CLAN_DATA = "Este jugador ya no está en un clan"
ERROR_NO_RANKED_DATA = "Este jugador aún no ha jugado ningún juego clasificado individuales"
ERROR_NO_TEAM_DATA = "Este jugador aún no ha jugado ningún juego de equipo clasificado"
ERROR_MISSING_DEFAULT_PLAYER = (
    "Necesita establecer un jugador como predeterminado para ejecutar este comando."
)
ERROR_LEGEND_NOT_FOUND = "No hay leyendas que coincidan con <b>{query}</b>"
ERROR_WEAPON_NOT_FOUND = "No hay armas que coincidan con <b>{query}</b>"
ERROR_MISSING_WEAPONS_COMBINATION_NOT_FOUND = (
    "No hay combinaciones de armas que coincidan con <b>{query}</b>"
)
ERROR_FLOOD_WAIT = (
    "Está enviando demasiadas solicitudes en un corto período de tiempo.\n"
    "Ha sido bloqueado por <b>{seconds}</b> segundos."
)
ERROR_API_OFFLINE = "Las API de Brawlhalla están temporalmente fuera de línea.\nInténtelo de nuevo más tarde."
ERROR_GENERIC = (
    "Ocurrió un error:\n\n"
    "<code>{error}</code>\n\n"
    "Si desea ayudar al desarrollo, "
    "abra un problema detallado sobre cómo reproducir el error que encontró.\n "
    "Antes de abrir un nuevo problema, asegúrese de que el error aún no haya sido informado."
)
ERROR_NO_LIVES = "No hay retransmisiones en directo de Brawlhalla en Twitch"

# Resultados
RESULTS_TEAMS = "Equipos:"
RESULTS_LEGENDS = (
    "Todas las leyendas:\n\n "
    "<i>Nota: También puede escribir <code>/legend name</code> para ver las estadísticas de esa leyenda específica.</i>\n\n "
    "Por ejemplo: <code>/legend bodvar</code>"
)
RESULTS_LEGENDS_WITH_WEAPON = "Leyendas con <b>{weapon}</b>"
RESULTS_MISSING_WEAPONS_COMBINATION = (
    "Combinaciones de armas faltantes:\n\n<b>{weapons}</b>\n\n"
    f"<i>Nota: También puede escribir <code>/{MISSING} weapon</code> para ver todas las combinaciones de armas faltantes.</i>\n\n"
    f"Por ejemplo: <code>/{MISSING} sword</code>"
)
RESULTS_WEAPONS = (
    "Todas las armas:\n\n"
    f"<i>Nota: También puede escribir <code>/{WEAPONS} weapon</code> para ver todas las leyendas que usan esa arma específica.</i>\n\n"
    f"Por ejemplo: <code>/{WEAPONS} sword</code>\n\n"
    f"<i>Alternativamente, también puede escribir <code>/{WEAPONS} weapon1 weapon2</code> para ver directamente la leyenda que usa estas armas.</i>\n\n"
    f"Por ejemplo: <code>/{WEAPONS} sword hammer</code>"
)
RESULTS_MISSING_WEAPONS_COMBINATION_WITH_WEAPON = (
    "Combinaciones de armas faltantes con <b>{weapon}</b>:\n\n<b>{weapons}</b>"
)
RESULTS_LIVE = (
    "🎮 • <b>{title}</b> • 🎮\n\n"
    "Comienza en: <b>{start}</b>\n"
    "Duración: <b>{end}</b>"
)
RESULT_LIVE_NOTIFICATION = "🎮 • <b>{title}</b> • 🎮\n\nEstá a punto de comenzar"

# Mensajes de estado
STATUS_LANGUAGE_CHANGED = "Idioma cambiado con éxito"
STATUS_LANGUAGE_UNCHANGED = "Idioma sin cambios"
STATUS_DEFAULT_PLAYER_SET = "Jugador establecido como predeterminado"
STATUS_NOTIFICATIONS_ON = "<b>🔔 • Notificaciones habilitadas • 🔔</b>\n\nRecibirás una notificación poco antes de que comience el en vivo!"
STATUS_NOTIFICATIONS_OFF = (
    "<b>🔕 • Notificaciones deshabilitadas • 🔕</b>\n\nYa no recibirás notificaciones!"
)

# Botones
BUTTON_GENERAL = "⚔️ • ESTADÍSTICAS GENERALES • ⚔️"
BUTTON_LEGENDS = "🥷 • LEYENDAS • 🥷"
BUTTON_DEFAULT_PLAYER = "👤 • ESTABLECER COMO PREDETERMINADO • 👤"
BUTTON_RANKED_SOLO = "🏆 • CLASIFICADO 1V1 • 🏆"
BUTTON_RANKED_TEAM = "🏆 • CLASIFICADO 2V2 • 🏆"
BUTTON_TEAMMATE = "🙋‍♂️ • COMPAÑERO DE EQUIPO • 🙋‍♂️"
BUTTON_ISSUE = "🐙 • ABRIR UN PROBLEMA • 🐱"
BUTTON_START = "🌟 • PONME UNA ESTRELLA EN GITHUB • 🌟"
BUTTON_CLAN = "🎖 • CLAN • 🎖"
BUTTON_CLOSE = "❌ • CERRAR • ❌"
BUTTON_WEAPONS = "🔫 • ARMAS • 🔫"
BUTTON_SHARE = "💬 • COMPARTIR • 💬"
BUTTON_LIVE = "🎮 • MIRA LA TRANSMISIÓN EN VIVO • 🎮"
BUTTON_LIVE_NOTIFICATIONS = "🔔 • ACTIVAR/DESACTIVAR NOTIFICACIONES • 🔔"
BUTTON_SEARCH_ALL = "🌍 • BUSCAR TODO • 🌍"
BUTTON_SEARCH_AUS = "🇦🇺 • BUSCAR AUS • 🇦🇺"
BUTTON_SEARCH_BRZ = "🇧🇷 • BUSCAR BRZ • 🇧🇷"
BUTTON_SEARCH_EU = "🇪🇺 • BUSCAR EU • 🇪🇺"
BUTTON_SEARCH_JPN = "🇯🇵 • BUSCAR JPN • 🇯🇵"
BUTTON_SEARCH_ME = "🇦🇪 • BUSCAR ME • 🇦🇪"
BUTTON_SEARCH_SA = "🇿🇦 • BUSCAR SA • 🇿🇦"
BUTTON_SEARCH_SEA = "🇨🇳 • BUSCAR SEA • 🇨🇳"
BUTTON_SEARCH_US_E = "🇺🇸 • BUSCAR US-E • 🇺🇸"
BUTTON_SEARCH_US_W = "🇺🇸 • BUSCAR US-W • 🇺🇸"

# Tiempo
TIME_DAYS = "Días: {t}"
TIME_HOURS = "Horas: {t}"
TIME_MINUTES = "Minutos: {t}"
TIME_SECONDS = "Segundos: {t}"

# Estadísticas
STATS_BASE = "🆔 • ID:<b> {id} </b>\n👤 • Nombre: <b>{name}</b>"
STATS_GENERAL = """⚔ • <b>ESTADÍSTICAS GENERALES</b> • ⚔

🎖 • Clan: <b>{clan}</b>
🆙 • Nivel: <b>{level}</b>
🔺 • XP: <b>{xp}</b>
⌚ • Leyenda más utilizada: <b>{most_used_legend}</b>
⌛ • Tiempo total de juego:
<b>{total_game_time}</b>

🎮 • Juegos jugados: <b>{games}</b>
🥇 • Juegos ganados: <b>{wins}</b>
🥉 • Juegos perdidos: <b>{loses}</b>
⚖ • Porcentaje de victorias: <b>{winperc}%</b>
👊 • Total de KOs: <b>{totalko}</b>
⚰ • Total de muertes: <b>{totaldeath}</b>
💀 • Total de suicidios: <b>{totalsuicide}</b>
😐 • KOs de equipo: <b>{totalteamko}</b>

💣 <b>BOMBAS</b> 💣
├─► KOs: <b>{kobomb}</b>
╰─► Daño: <b>{damagebomb}</b>

💥 <b>MINAS</b> 💥
├─► KOs: <b>{komine}</b>
╰─► Daño: <b>{damagemine}</b>

☀️ <b>BOLAS DE PINCHOS</b> ☀️
├─► KOs: <b>{kospikeball}</b>
╰─► Daño: <b>{damagespikeball}</b>

👟 <b>PATADA LATERAL</b> 👟
├─► KOs: <b>{kosidekick}</b>
╰─► Daño: <b>{damagesidekick}</b>

❄️ <b>BOLAS DE NIEVE</b> ❄️
├─► KOs: <b>{kosnowball}</b>
╰─► Golpes: <b>{hitsnowball}</b>"""

STATS_RANKED = """🏆 • <b>CLASIFICADO 1v1</b> • 🏆

🔶 • Elo actual: <b>{rating}</b>
🔷 • Pico de elo: <b>{peak}</b>
👑 • Nivel: <b>{tier}</b>

🎮 • Juegos jugados: <b>{games}</b>
🥇 • Juegos ganados: <b>{wins}</b>
🥉 • Juegos perdidos: <b>{loses}</b>
🌎 • Región: <b>{region}</b>"""

STATS_GLORY_ELO = """💎 • Gloria estimada: <b>{glory}</b>
👑 • Reinicio de elo estimado: <b>{elo_reset}</b>"""

STATS_RANKED_TEAM = """🏆 • <b>CLASIFICADO 2v2</b> • 🏆

👥 • Equipo: <b>{teamname}</b>

🔶 • Elo actual: <b>{rating}</b>
🔷 • Pico de elo: <b>{peak}</b>
👑 • Nivel: <b>{tier}</b>

🎮 • Juegos jugados: <b>{games}</b>
🥇 • Juegos ganados: <b>{wins}</b>
🥉 • Juegos perdidos: <b>{loses}</b>
🌎 • Región: <b>{region}</b>"""

STATS_CLAN = """🆔 • ID de clan:<b> {id} </b>
👑 • Nombre del clan: <b>{name}</b>

🔺 • XP: <b>{xp}</b>
👥 • Miembros: <b>{num}</b>
📅 • Fecha de creación: <b>{date}</b>"""

STATS_PLAYER_LEGEND = """🥷 • <b>LEYENDA</b> • 🥷

🆔 • ID de leyenda: <b>{id}</b>
🥷 • Nombre de leyenda: <b>{name}</b>

🆙 • Nivel: <b>{level}</b>
🔺 • XP: <b>{xp}</b>
⌚ • Tiempo de juego:
<b>{matchtime}</b>

🎮 • Partidas jugadas: <b>{games}</b>
🥇 • Partidas ganadas: <b>{wins}</b>
🥉 • Partidas perdidas: <b>{loses}</b>
⚖️ • Porcentaje de victorias: <b>{winperc}%</b>
👊 • Total de KOs: <b>{ko}</b>
⚰ • Total de muertes: <b>{death}</b>
💀 • Total de suicidios: <b>{suicide}</b>
💥 • Daño total infligido: <b>{damagedealt}</b>
💢 • Daño total recibido: <b>{damagetaken}</b>
😐 • KOs de equipo: <b>{teamko}</b>

🔫 <b>ARMAS</b> 🔫
├─► {weaponone} Tiempo sostenido: <b>{timeheldweaponone}</b>
├─► {weaponone} KOs: <b>{koweaponone}</b>
├─► {weaponone} Daño: <b>{damageweaponone}</b>
├─►{weapontwo} Tiempo sostenido: <b>{timeheldweapontwo}</b>
├─►{weapontwo} KOs: <b>{koweapontwo}</b>
╰─►{weapontwo} Daño: <b>{damageweapontwo}</b>

👊 <b>SIN ARMAS</b> 👊
├─► KOs: <b>{kounarmed}</b>
╰─► Daño: <b>{damageunarmed}</b>

📱 <b>GADGETS</b>📱
├─► KOs: <b>{kogadgets}</b>
╰─► Daño: <b>{damagegadgets}</b>

🎯 <b>OBJETOS LANZADOS</b> 🎯
├─► KOs: <b>{kothrownitem}</b>
╰─► Daño: <b>{damagethrownitem}</b>"""

STATS_LEGEND = """🎮 • <b>ESTADÍSTICAS DE LEYENDA</b> • 🎮

🆔 • ID: <b>{legend_id}</b>
🔖 • Nombre: <a href="{url}"><b>{bio_name}</b></a>
🎖️ • Alias: <b>{bio_aka}</b>

🗡️ • Arma 1: <b>{weapon_one}</b>
🗡️ • Arma 2: <b>{weapon_two}</b>

💪 • Fuerza: <b>{strength}</b>
🏹 • Destreza: <b>{dexterity}</b>
🛡️ • Defensa: <b>{defense}</b>
🏃 • Velocidad: <b>{speed}</b>"""
