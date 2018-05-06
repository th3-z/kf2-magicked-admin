class GameMap:
    def __init__(self, name, title="Unnamed"):
        self.name = name
        self.title = title

        self.plays_survival = 0
        self.plays_weekly = 0
        self.plays_endless = 0
        self.plays_survival_vs = 0
        self.highest_wave = 0
        self.votes = 0

    def reset_stats(self):
        self.plays_survival = 0
        self.plays_weekly = 0
        self.plays_endless = 0
        self.plays_survival_vs = 0
        self.highest_wave = 0
        self.votes = 0

    def __str__(self):
        return self.title