from lxml import html
import logging

from api.web_interface import WebInterface
from api.chat import Chat

from utils.text import str_to_bool

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class WebAdmin(object):
    def __init__(self, address, username, password, ops=None):

        self.__web_interface = WebInterface(address, username, password)
        self.__chat = Chat(self.__web_interface, ops)

        self.__general_settings = \
            self.__web_interface.get_payload_general_settings()
        self.__motd_settings = \
            self.__web_interface.get_payload_motd_settings()
        self.__map_settings = \
            self.__web_interface.get_payload_map_settings()

        self.__game_password = None

    def __save_general_settings(self):
        self.__web_interface.post_general_settings(
            self.__general_settings
        )

    def set_general_setting(self, setting, value):
        self.__general_settings[setting] = value
        self.__save_general_settings()

    def set_game_password(self, password):
        payload = {
            'action': 'gamepassword',
            'gamepw1': password,
            'gamepw2': password
        }
        self.__game_password = password
        self.__web_interface.post_passwords(payload)

    def has_game_password(self):
        response = self.__web_interface.get_passwords
        passwords_tree = html.fromstring(response.content)

        password_state_pattern = "//p[starts-with(text(),\"Game password\")]" \
                                 "//em/text()'"
        password_state = passwords_tree.xpath(password_state_pattern)[0]
        return str_to_bool(password_state)

    def toggle_game_password(self):
        if not self.__game_password:
            logger.info("Tried to toggle game password before setting value")
            return False

        if self.has_game_password():
            self.set_game_password("")
            return False
        else:
            self.set_game_password(self.__game_password)
            return True

    def set_length(self, length):
        self.set_general_setting("settings_GameLength", length)

    def set_difficulty(self, difficulty):
        self.set_general_setting("settings_GameDifficulty", difficulty)

    def set_max_players(self, players):
        self.set_general_setting("settings_MaxPlayers", str(players))

    def toggle_map_voting(self):
        if self.__general_settings["settings_bDisableMapVote"] == "1":
            self.set_general_setting("settings_bDisableMapVote", "0")
            return False
        else:
            self.set_general_setting("settings_bDisableMapVote", "1")
            return True

    def set_server_name(self, name):
        self.set_general_setting("settings_ServerName", name)

    def set_map(self, new_map):
        self.__map_settings['map'] = new_map
        self.__web_interface.post_map(self.__map_settings)

    def restart_map(self):
        self.__web_interface.post_map(self.__map_settings)

    def set_game_type(self, game_type):
        self.__map_settings['gametype'] = game_type
        self.__web_interface.post_map(self.__map_settings)

    def activate_map_cycle(self, index):
        payload = {
            "maplistidx": str(index),
            "mapcycle": "KF-Default",
            "activate": "activate"
        }
        self.__web_interface.post_map_cycle(payload)

    def set_map_cycle(self, index, maplist):
        payload = {
            "maplistidx": str(index),
            "mapcycle": maplist,
            "action": "save"
        }
        self.__web_interface.post_map_cycle(payload)

    def set_motd(self, motd):
        self.__motd_settings["ServerMOTD"] = motd\
            .encode("iso-8859-1", "ignore")
        self.__web_interface.post_motd(self.__motd_settings)
        # Setting the MOTD resets changes to general settings
        self.__save_general_settings()

    def set_banner(self, banner_link):
        self.__motd_settings["BannerLink"] = banner_link
        self.__web_interface.post_motd(self.__motd_settings)

    def set_web_link(self, web_link):
        self.__motd_settings["WebLink"] = web_link
        self.__web_interface.post_motd(self.__motd_settings)