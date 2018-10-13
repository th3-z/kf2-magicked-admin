from collections import namedtuple

CHAT_MAX_ROWS = 7
CHAT_MAX_COLUMNS = 21

DIFF_UNKNOWN = "-1.0000"
DIFF_NORM = "0.0000"
DIFF_HARD = "1.0000"
DIFF_SUI = "2.0000"
DIFF_HOE = "3.0000"

LEN_UNKNOWN = "-1"
LEN_SHORT = "0"
LEN_NORM = "1"
LEN_LONG = "2"

MODE_UNKNOWN = "UnknownGameMode"
MODE_SURVIVAL = "KFGameContent.KFGameInfo_Survival"
MODE_WEEKLY = "KFGameContent.KFGameInfo_WeeklySurvival"
MODE_SURVIVAL_VS = "KFGameContent.KFGameInfo_VersusSurvival"
MODE_ENDLESS = "KFGameContent.KFGameInfo_Endless"


ConstGame = namedtuple('Game', ['trader_open', 'zeds_total', 'zeds_dead',
                                'map_title', 'map_name', 'wave', 'length',
                                'difficulty', 'game_type'])


ConstPlayer = namedtuple('Player', ['username', 'perk', 'kills',
'health', 'dosh', 'ping'])
