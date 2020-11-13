import gettext
import string
from os import path

from utils import find_data_file
from utils.text import millify, trim_string

from jinja2 import Template

_ = gettext.gettext


class MotdUpdater:
    def __init__(self, server):
        self.server = server
        self.motd_path = find_data_file("conf/" + server.name + ".motd")

        self.motd = ""
        self.reload()

    def reload(self):
        if not path.exists(find_data_file(self.motd_path)):
            """warning(
                _("No MOTD file for {} found, pulling from web admin!").format(
                    self.server.name
                )
            )"""

            with open(self.motd_path, "w+") as motd_file:
                motd_file.write(self.server.web_admin.get_motd())

        motd_f = open(find_data_file(self.motd_path))
        motd = motd_f.read()
        motd_f.close()
        self.motd = motd

    def update(self):
        if not self.motd:
            return

        self.server.web_admin.set_motd(self.render_motd())

    def render_motd(self):
        # https://jinja.palletsprojects.com/en/2.11.x/templates/
        motd = Template(self.motd)

        # Template functions
        motd.globals['millify'] = millify
        motd.globals['trimstr'] = trim_string

        # Template parameters
        top_kills = self.server.database.top_kills()
        top_dosh = self.server.database.top_dosh()
        top_time = self.server.database.top_time()
        server_dosh = self.server.database.server_dosh()
        server_kills = self.server.database.server_kills()

        return motd.render(
            top_kills=top_kills,
            top_dosh=top_dosh,
            top_time=top_time,
            server_kills=server_kills,
            server_dosh=server_dosh
        )
