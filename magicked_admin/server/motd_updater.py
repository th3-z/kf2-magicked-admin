import threading
import time
from os import path

import requests
from lxml import html

from utils import DEBUG, find_data_file, warning
from utils.text import millify, trim_string


class MotdUpdater(threading.Thread):

    def __init__(self, server, scoreboard_type):
        self.server = server
        self.motd_path = find_data_file(server.name + ".motd")

        self.scoreboard_type = scoreboard_type
        self.time_interval = 5*60

        if not path.exists(find_data_file(self.server.name + ".motd")):
            warning("No MOTD file for {} found, pulling from web admin!".format(self.server.name))
            
            with open(self.motd_path, "w+") as motd_file:
                motd_file.write(self.server.web_admin.get_motd())
                

        self.motd = self.load_motd()

        threading.Thread.__init__(self)

    def run(self):
        if not self.motd:
            return

        while True:
            self.server.write_all_players()

            motd = self.render_motd(self.motd)
            self.server.web_admin.set_motd(motd) 

            if DEBUG:
                print("Updated the MOTD!")

            time.sleep(self.time_interval)

    def load_motd(self):
        motd_f = open(find_data_file(self.server.name + ".motd"))
        motd = motd_f.read()
        motd_f.close()
        return motd

    def render_motd(self, src_motd):
        if self.scoreboard_type in ['kills', 'Kills', 'kill', 'Kill']:
            scores = self.server.database.top_kills()
        elif self.scoreboard_type in ['Dosh','dosh']:
            scores = self.server.database.top_dosh()
        else:
            warning("Scoreboard_type not recognised '{}' for {}. Options are: dosh, kills"
                    .format(self.scoreboard_type, self.server.name))
            return src_motd

        for player in scores:
            name = player[0].replace("<", "&lt;")
            name = trim_string(name, 12)
            score = player[1]

            src_motd = src_motd.replace("%PLR", name, 1)
            src_motd = src_motd.replace("%SCR", millify(score), 1)

        if "%SRV_K" in src_motd:
            server_kills = self.server.database.server_kills()
            src_motd = src_motd.replace("%SRV_K", millify(server_kills), 1)

        if "%SRV_D" in src_motd:
            server_dosh = self.server.database.server_dosh()
            src_motd = src_motd.replace("%SRV_D", millify(server_dosh), 1)

        return src_motd
