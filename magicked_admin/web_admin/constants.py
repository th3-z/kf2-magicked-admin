from collections import namedtuple

CHAT_MAX_ROWS       = 7
CHAT_MAX_COLUMNS    = 21

DIFF_UNKNOWN    = "-1.0000"
DIFF_NORM       = "0.0000"
DIFF_HARD       = "1.0000"
DIFF_SUI        = "2.0000"
DIFF_HOE        = "3.0000"

LEN_UNKNOWN     = 0
LEN_SHORT       = 4
LEN_NORM        = 7
LEN_LONG        = 10

GAME_TYPE_UNKNOWN       = "kfgamecontent.KFGameInfo_Unknown"
GAME_TYPE_SURVIVAL      = "kfgamecontent.KFGameInfo_Survival"
GAME_TYPE_WEEKLY        = "kfgamecontent.KFGameInfo_Weekly"
GAME_TYPE_SURVIVAL_VS   = "kfgamecontent.KFGameInfo_VersusSurvival"
GAME_TYPE_ENDLESS       = "kfgamecontent.KFGameInfo_Endless"
GAME_TYPE_NAME = {
    GAME_TYPE_UNKNOWN       : "Unknown",
    GAME_TYPE_SURVIVAL      : "Survival",
    GAME_TYPE_WEEKLY        : "Weekly",
    GAME_TYPE_SURVIVAL_VS   : "Versus Survival",
    GAME_TYPE_ENDLESS       : "Endless"
}

GAME_MAP_TITLE_UNKNOWN = "kf-default"

USER_TYPE_NONE      = 0  # Enumerated ^2s for bitwise ops
USER_TYPE_ADMIN     = 1
USER_TYPE_SPECTATOR = 2
USER_TYPE_SERVER    = 4

ConstGame = namedtuple('Game', ['trader_open', 'zeds_total', 'zeds_dead',
                                'map_title', 'map_name', 'wave', 'length',
                                'difficulty', 'game_type'])


ConstPlayer = namedtuple('Player', ['username', 'perk', 'kills', 'health',
                                    'dosh', 'ping'])
