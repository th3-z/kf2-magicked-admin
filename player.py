class Player():
    
    def __init__(self, username, perk, dosh, health, kills, ping):
        self.total_deaths = 0
        self.total_kills = 0
        self.total_time = 0
        self.total_dosh = 0
        self.total_dosh_spent = 0
        self.total_health_lost = 0
        self.total_logins = 0
        self.last_login = 0

        self.session_kills = 0
        self.session_start_time = 0
        self.session_dosh = 0
        self.session_dosh_spent = 0
        self.session_health_lost = 0

        self.dosh = dosh
        self.dosh_spent = 0
        self.wave_kills = 0
        self.health_lost_wave = 0
        self.kills = kills
        self.health = health
        self.username = username
        self.perk = perk
        self.ping = ping
        
        #self.steam_id = sid

    def __str__(self):
        return "username: " + self.username + "\nperk: " + self.perk + "\ndosh: " + self.dosh + "\nhealth: " + self.health + "\nping: " + self.ping

