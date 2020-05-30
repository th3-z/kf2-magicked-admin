import gettext
from os import path

from utils import debug, find_data_file, warning
from utils.text import millify, trim_string

_ = gettext.gettext


class MotdUpdater:
    def __init__(self, server):
        self.server = server
        self.motd_path = find_data_file("conf/" + server.name + ".motd")

        self.motd = ""
        self.reload()

    def reload(self):
        if not path.exists(find_data_file(self.motd_path)):
            warning(
                _("No MOTD file for {} found, pulling from web admin!").format(
                    self.server.name
                )
            )

            with open(self.motd_path, "w+") as motd_file:
                motd_file.write(self.server.web_admin.get_motd())

        motd_f = open(find_data_file(self.motd_path))
        motd = motd_f.read()
        motd_f.close()
        self.motd = motd

    def update(self, score_type):
        if not self.motd:
            return

        self.server.web_admin.set_motd(self.render_motd(score_type))
        debug(_("Updated the MOTD!"))

    def render_motd(self, score_type):
        motd = self.motd

        if score_type in ['kills', 'Kills', 'kill', 'Kill']:
            scores = self.server.database.top_kills()
        elif score_type in ['Dosh', 'dosh']:
            scores = self.server.database.top_dosh()
        elif score_type in ['Time', 'time']:
            scores = self.server.database.top_time()
        else:
            warning(
                _("Scoreboard_type not recognised '{}'. Options are: "
                  "dosh, kills").format(score_type)
            )
            return motd

        for player in scores:
            if not player['username']:
                continue
            name = player['username'].replace("<", "&lt;")
            name = trim_string(name, 12)
            score = player['score']

            motd = motd.replace("%PLR", name, 1)
            motd = motd.replace("%SCR", millify(score), 1)

        if "%SRV_K" in motd:
            server_kills = self.server.database.server_kills()
            motd = motd.replace("%SRV_K", millify(server_kills), 1)

        if "%SRV_D" in motd:
            server_dosh = self.server.database.server_dosh()
            motd = motd.replace("%SRV_D", millify(server_dosh), 1)

        return motd
