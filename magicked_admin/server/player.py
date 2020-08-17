import gettext
import time

_ = gettext.gettext


class Player:

    def __init__(self, username, perk):
        self.steam_id = None
        self.player_key = None
        self.ip = None
        self.country = _("Unknown")
        self.country_code = "??"
        self.op = False

        self.total_deaths = 0
        self.total_kills = 0
        self.total_dosh = 0

        self.sessions = 0
        self.total_time = 0
        self.__total_timer = time.time()
        self.session_start = time.time()

        # game_kills is equivalent to kills
        self.game_dosh = 0

        self.wave_kills = 0
        self.wave_dosh = 0

        self.session_id = None

        self.kills = 0
        self.dosh = 0
        self.dosh_spent = 0
        self.health = 0
        self.deaths = 0
        self.damage_taken = 0

        self.username = username
        self.perk = perk
        self.perk_level = 99
        self.ping = 0

        self.join_date = 0



    def update_time(self):
        now = time.time()
        elapsed_time = now - self.__total_timer
        self.total_time += elapsed_time
        self.__total_timer = now

    def reset_stats(self):
        pass

    def __str__(self):
        return _("Username: {}\nCountry: {} ({})\nOP: {}\nSteam ID:{}").format(
            self.username, self.country, self.ip, self.op, self.steam_id
        )
