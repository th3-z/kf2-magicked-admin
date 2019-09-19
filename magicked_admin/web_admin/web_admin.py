from itertools import groupby

from lxml import html

from utils import warning
from utils.net import get_country
from utils.text import str_to_bool
from web_admin.chat import Chat
from web_admin.constants import *
from web_admin.web_interface import WebInterface


class WebAdmin(object):
    def __init__(self, address, username, password, server_name="unnamed"):
        self.__web_interface = \
            WebInterface(address, username, password, server_name)
        self.chat = Chat(self.__web_interface)
        self.chat.start()

        self.__general_settings = \
            self.__web_interface.get_payload_general_settings()
        self.__motd_settings = \
            self.__web_interface.get_payload_motd_settings()
        self.__map_settings = \
            self.__web_interface.get_payload_map_settings()

        self.__game_password = None

    def supported_mode(self, mode):
        # The other modes have various bits of data omitted!
        return self.__web_interface.ma_installed or mode == GAME_TYPE_SURVIVAL

    def close(self):
        self.chat.stop()

    def __save_general_settings(self):
        self.__web_interface.post_general_settings(
            self.__general_settings
        )

    def set_general_setting(self, setting, value):
        self.__general_settings[setting] = value
        self.__save_general_settings()

    def kick_player(self, player_key):
        payload = {
            "ajax": "1",
            "action": "kick",
            "playerkey": player_key
        }
        self.__web_interface.post_players_action(payload)

    def ban_player(self, player_key):
        payload = {
            "ajax": "1",
            "action": "ban",
            "playerkey": player_key
        }
        self.__web_interface.post_players_action(payload)

    def set_game_password(self, password=""):
        payload = {
            'action': 'gamepassword',
            'gamepw1': password,
            'gamepw2': password
        }
        self.__game_password = password
        self.__web_interface.post_passwords(payload)

    def has_game_password(self):
        response = self.__web_interface.get_passwords()
        passwords_tree = html.fromstring(response.content)

        password_state_pattern = "//p[starts-with(text(),'Game password')]" \
                                 "/em/text()"
        password_state = passwords_tree.xpath(password_state_pattern)[0]
        return str_to_bool(password_state)

    def toggle_game_password(self):
        if not self.__game_password:
            warning("Tried to toggle game password before setting value")
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

    def get_maps(self):
        response = self.__web_interface.get_maplist()
        maplist_tree = html.fromstring(response.content)

        available_path = "//textarea[@id='allmaps']/text()"
        return maplist_tree.xpath(available_path)[0].split('\n')

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
        self.__motd_settings["ServerMOTD"] = motd \
            .encode("iso-8859-1", "ignore")
        self.__web_interface.post_welcome(self.__motd_settings)

        # Setting the MOTD resets changes to general settings
        self.__save_general_settings()

    def get_motd(self):
        return self.__motd_settings['ServerMOTD']

    def set_banner(self, banner_link):
        self.__motd_settings["BannerLink"] = banner_link
        self.__web_interface.post_welcome(self.__motd_settings)

    def set_web_link(self, web_link):
        self.__motd_settings["WebLink"] = web_link
        self.__web_interface.post_welcome(self.__motd_settings)

    def get_players(self):
        response = self.__web_interface.get_server_info()
        info_tree = html.fromstring(response.content)
        return self.__get_players(info_tree)

    def get_game(self):
        response = self.__web_interface.get_server_info()
        info_tree = html.fromstring(response.content)
        return self.__get_game(info_tree)

    def get_game_players(self):
        response = self.__web_interface.get_server_info()
        info_tree = html.fromstring(response.content)
        return self.__get_game(info_tree), self.__get_players(info_tree)

    @staticmethod
    def __get_players(info_tree):
        players = []
        theads_path = "//table[@id=\"players\"]/thead//th[position()>1]//text()"
        theads_result = info_tree.xpath(theads_path)

        if len(theads_result):
            name_col = theads_result.index("Name")
            perk_col = theads_result.index("Perk")
            dosh_col = theads_result.index("Dosh")
            health_col = theads_result.index("Health")
            kills_col = theads_result.index("Kills")
            ping_col = theads_result.index("Ping")
        else:
            return players

        # xpath to <td>s and retrieve text manually to catch empty text()
        trows_path = "//table[@id=\"players\"]/tbody//td"
        trows_result = info_tree.xpath(trows_path)
        trows_result = [
            trow.text if trow.text else ""
            for trow in trows_result
        ]

        # If players in game, a lone message is left in the table
        if len(trows_result) == 1:
            return players

        # Group rows in the table by the non-breaking space in first cell
        trows_result = [
            list(group)
            for k, group in groupby(
                trows_result, lambda x: x == "\xa0"
            )
            if not k
        ]

        for player_row in trows_result:
            player = ConstPlayer(
                player_row[name_col],
                player_row[perk_col],
                int(player_row[kills_col] or 0),
                int(player_row[health_col] or 0),
                int(player_row[dosh_col] or 0),
                int(player_row[ping_col] or 0)
            )
            players.append(player)

        return players

    @staticmethod
    def __get_game(info_tree):
        zeds_path = "//dd[@class=\"gs_wave\"]/text()"
        zeds_result = info_tree.xpath(zeds_path)

        if len(zeds_result):
            zeds_dead, zeds_total = map(int, zeds_result[0].split("/"))
            if zeds_dead == zeds_total and zeds_total > 1:
                trader_open = True
            else:
                trader_open = False
        else:
            zeds_dead, zeds_total = None, None
            trader_open = False

        players_path = "//dl[@id=\"currentRules\"]/dt[text()=\"Players\"]/following-sibling::dd[1]/text()"
        players_result = info_tree.xpath(players_path)

        if len(players_result):
            players, players_max = map(int, players_result[0].split("/"))
        else:
            players, players_max = None, None

        wave_path = "//dl[@id=\"currentRules\"]/dt[text()=\"Wave\"]/following-sibling::dd[1]/text()"
        wave_result = info_tree.xpath(wave_path)

        if len(wave_result):
            wave, length = map(int, wave_result[0].split("/"))
        else:
            wave, length = None, LEN_UNKNOWN

        difficulty_path = "//dl[@id=\"currentRules\"]/dt[text()=\"Difficulty\"]/following-sibling::dd[1]/text()"
        difficulty_result = info_tree.xpath(difficulty_path)

        if len(difficulty_result):
            difficulty_name = map(int, wave_result[0].split("/"))
            if difficulty_name == "Normal":
                difficulty = DIFF_NORM
            elif difficulty_name == "Hard":
                difficulty = DIFF_HARD
            elif difficulty_name == "Suicidal":
                difficulty = DIFF_SUI
            elif difficulty_name == "Hell on Earth":
                difficulty = DIFF_HOE
            else:
                difficulty = DIFF_UNKNOWN
        else:
            difficulty = DIFF_UNKNOWN

        game_type_path = "//dl[@id=\"currentGame\"]/dt[text()=\"Game type\"]/following-sibling::dd[1]/@title"
        game_type_result = info_tree.xpath(game_type_path)

        if len(game_type_result):
            game_type = game_type_result[0]
        else:
            game_type = GAME_TYPE_UNKNOWN

        map_title_path = "//dl[@id=\"currentGame\"]/dt[text()=\"Map\"]/following-sibling::dd[1]/@title"
        map_title_result = info_tree.xpath(map_title_path)
        map_name_path = "//dl[@id=\"currentGame\"]/dt[text()=\"Map\"]/following-sibling::dd[1]/text()"
        map_name_result = info_tree.xpath(map_name_path)

        if len(map_title_result) and len(map_name_result):
            map_title, map_name = map_title_result[0], map_name_result[0]
        else:
            map_title, map_name = None, None

        return ConstGame(trader_open, zeds_total, zeds_dead, map_title,
                         map_name, wave, length, difficulty, game_type,
                         players_max)

    def get_player_identity(self, username):
        response = self.__web_interface.get_players()
        player_tree = html.fromstring(response.content)

        theads_path = "//table[@id=\"players\"]/thead//th[position()>1]//text()"
        theads_result = player_tree.xpath(theads_path)

        name_col = theads_result.index("Player name")
        ip_col = theads_result.index("IP")
        sid_col = theads_result.index("Steam ID")
        nid_col = theads_result.index("Unique Net ID")
        player_key_col = 5

        trows_path = "//table[@id=\"players\"]/tbody//td"
        trows_result = player_tree.xpath(trows_path)
        trows_result = [trow.text if trow.text else "" for trow in
                        trows_result]
        trows_result = [list(group) for k, group in
                        groupby(trows_result, lambda x: x == "\xa0") if not k]

        player_keys_path = "//table[@id=\"players\"]/tbody//input[@name=\"playerkey\"]//@value"
        player_keys_result = player_tree.xpath(player_keys_path)
        for i in range(0, len(player_keys_result)):
            trows_result[i][player_key_col] = player_keys_result[i]

        # Duplicate usernames cannot be identified reliably
        players_found = 0

        for player_row in trows_result:
            if player_row[name_col] == username:
                players_found += 1
                ip = player_row[ip_col]
                sid = player_row[sid_col]
                nid = player_row[nid_col]
                player_key = player_row[player_key_col]
                country, country_code = get_country(ip)

        if players_found == 1:
            return {
                'ip': ip,
                'country': country,
                'country_code': country_code,
                'steam_id': sid,
                'network_id': nid,
                'player_key': player_key
            }
        else:
            warning("Couldn't find identify player: {}".format(username))
            return {
                'ip': None,
                'country': "Unknown",
                'country_code': "??",
                'steam_id': None,
                'network_id': None,
                'player_key': None
            }
