DIFF_NORM = "0.0000"
DIFF_HARD = "1.0000"
DIFF_SUI = "2.0000"
DIFF_HOE = "3.0000"

LEN_SHORT = "0"
LEN_NORM = "1"
LEN_LONG = "2"

MODE_SURVIVAL = "KFGameContent.KFGameInfo_Survival"
MODE_WEEKLY = "KFGameContent.KFGameInfo_WeeklySurvival"
MODE_SURVIVAL_VS = "KFGameContent.KFGameInfo_VersusSurvival"
MODE_ENDLESS = "KFGameContent.KFGameInfo_Endless"


class Game:
    def __init__(self, game_map, gamemode):
        self.game_map = game_map
        self.gamemode = gamemode
        self.difficulty = DIFF_NORM
        self.wave = 0
        self.length = LEN_NORM

        self.zeds_wave_killed = 0
        self.zeds_wave_total = 0
        self.zeds_killed = 0

        self.dosh_wave_earned = 0
        self.dosh_earned = 0

        self.password = None
        self.password_enabled = False

    def __str__(self):
        return "Mode: {}\nMap: {}\nDifficulty: {}\nWave {}/{}".format(
            self.gamemode,
            self.game_map.title,
            self.difficulty,
            self.wave,
            self.length
        )
