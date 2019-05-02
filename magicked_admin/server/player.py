import time


class Player:

    def __init__(self, username, perk):
        self.total_deaths = 0
        self.total_kills = 0
        self.total_dosh = 0
        self.total_dosh_spent = 0
        self.total_health_lost = 0
        self.total_logins = 0

        self.total_time = 0
        self.__total_timer = time.time()
        self.session_start = time.time()

        self.game_dosh = 0

        self.wave_kills = 0
        self.wave_dosh = 0

        self.kills = 0
        self.dosh = 0
        self.health = 0

        self.username = username
        self.perk = perk
        self.perk_level = 99
        self.ping = 0
        self.login_time = 0

        self.steam_id = None
        self.network_id = None
        self.player_key = None
        self.ip = None
        self.country = "Unknown"
        self.country_code = "??"
        self.op = False

    def update_time(self):
        now = time.time()
        elapsed_time = now - self.__total_timer
        self.total_time += elapsed_time
        self.__total_timer = now

    def reset_stats(self):
        self.total_deaths = 0
        self.total_kills = 0
        self.total_dosh = 0
        self.total_dosh_spent = 0
        self.total_health_lost = 0
        self.total_logins = 0
        self.total_time = 0


    def __str__(self):
        return "Username: " + self.username + \
               "\nCountry: " + str(self.country) + " (" + self.ip + ")"\
               "\nSteam ID: " + str(self.steam_id)
