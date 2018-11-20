import datetime

class Player:

    def __init__(self, username, perk):
        self.total_deaths = 0
        self.total_kills = 0
        self.total_time = 0
        self.total_dosh = 9999
        self.total_dosh_spent = 0
        self.total_health_lost = 0
        self.total_logins = 0

        self.session_start = datetime.datetime.now()

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

        self.sid = "00000000000000000"
        self.player_key = "0x0.00"
        self.ip = "0.0.0.0"
        self.country = "Unknown"
        self.country_code = "??"

    def __str__(self):
        return "username: " + self.username + "\nperk: " + self.perk + \
               "\ndosh: " + str(self.dosh) + "\nhealth: " + str(self.health) +\
               "\nkills: " + str(self.kills)
