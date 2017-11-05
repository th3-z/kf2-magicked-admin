class Player():
    
    def __init__(self, username, perk):
        self.total_deaths = 0
        self.total_kills = 0
        self.total_time = 0
        self.total_dosh = 0
        self.total_dosh_spent = 0
        self.total_health_lost = 0
        self.total_logins = 0
        self.last_login = 0

        self.session_start_time = 0

        self.dosh = 0
        self.dosh_spent = 0
        self.wave_kills = 0
        self.health_lost_wave = 0
        self.kills = 0
        self.health = 0
        self.username = username
        self.perk = perk
        self.ping = 0
        
        #self.steam_id = sid

    def __str__(self):
        return "username: " + self.username + "\nperk: " + self.perk + "\ndosh: " + str(self.dosh) + "\nhealth: " + str(self.health) + "\nping: " + str(self.ping)

