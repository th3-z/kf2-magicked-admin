import web_admin as api

class Game:
    def __init__(self, game_map, gamemode):
        self.game_map = game_map
        self.gamemode = gamemode
        self.difficulty = api.DIFF_NORM
        self.wave = 0
        self.length = api.LEN_NORM

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
