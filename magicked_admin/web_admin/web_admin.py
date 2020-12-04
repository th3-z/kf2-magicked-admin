import logging
from itertools import groupby

from lxml import html
from utils.net import get_country
from utils.text import str_to_bool
from web_admin.constants import *

logger = logging.getLogger(__name__)


class WebAdmin(object):
    def __init__(self, web_interface):
        self.web_interface = web_interface

        self._message_buffer = ""
        self._silent = False

        self._general_settings = None
        self._motd_settings = None
        self._map_settings = None

        self._game_password = None

    @property
    def general_settings(self):
        return self._general_settings or self.web_interface.get_payload_general_settings()

    @property
    def motd_settings(self):
        return self._motd_settings or self.web_interface.get_payload_motd_settings()

    @property
    def map_settings(self):
        return self._map_settings or self.web_interface.get_payload_map_settings()

    def supported_game_type(self, game_type):
        # The other modes have various bits of data omitted!
        return self.web_interface.ma_installed or game_type == GAME_TYPE_SURVIVAL

    def _save_general_settings(self):
        self.web_interface.post_general_settings(
            self.general_settings
        )

    def submit_message(self, message):
        if self._silent:
            return

        message_payload = {
            'ajax': '1',
            'message': message.encode("iso-8859-1", "ignore"),
            'teamsay': '-1'
        }

        response = self.web_interface.post_message(message_payload)
        self._message_buffer += response.text

        return True

    def get_new_messages(self):
        response = self.web_interface.get_new_messages().text + self._message_buffer
        self._message_buffer = ""

        if not response:
            return []

        username_pattern = ".//span[starts-with(@class,\'username\')]/text()"
        user_type_pattern = ".//span[starts-with(@class,\'username\')]/@class"
        message_pattern = ".//span[@class=\'message\']/text()"

        message_roots = html.fromstring(response).find_class("chatmessage")

        messages = []

        for message_root in message_roots:
            try:
                username = message_root.xpath(username_pattern)[0]
                user_type = message_root.xpath(user_type_pattern)[0]
                message = message_root.xpath(message_pattern)[0]
            except IndexError:
                # Not sure how but players can send messages with no content
                continue

            user_flags = USER_TYPE_NONE
            if 'admin' in user_type:
                user_flags += USER_TYPE_ADMIN
            if 'spectator' in user_type:
                user_flags += USER_TYPE_SPECTATOR

            messages.append({
                'username': username,
                'user_flags': user_flags,
                'message': message
            })

        return messages

    def set_general_setting(self, setting, value):
        self.general_settings[setting] = value
        self._save_general_settings()

    def kick_player(self, player_key):
        payload = {
            "ajax": "1",
            "action": "kick",
            "playerkey": player_key
        }
        self.web_interface.post_players_action(payload)

    def ban_player(self, steam_id, player_key):
        payload = {
            "uniqueid": "",
            "action": "add",
            "steamint64": steam_id
        }
        self.web_interface.post_bans(payload)
        self.kick_player(player_key)

    def unban_player(self, steam_id):
        payload = {
            "uniqueid": "",
            "action": "delete",
            "steamint64": steam_id
        }
        self.web_interface.post_bans(payload)

    def set_game_password(self, password=""):
        payload = {
            'action': 'gamepassword',
            'gamepw1': password,
            'gamepw2': password
        }
        self._game_password = password
        self.web_interface.post_passwords(payload)

    def _has_game_password(self):
        response = self.web_interface.get_passwords()
        passwords_tree = html.fromstring(response.content)

        password_state_pattern = "//p[starts-with(text(),'Game password')]" \
                                 "/em/text()"
        password_state = passwords_tree.xpath(password_state_pattern)[0]
        return str_to_bool(password_state)

    def toggle_game_password(self):
        if not self._game_password:
            logger.warning("Tried to toggle game password before setting value")
            return False

        if self._has_game_password():
            self.set_game_password("")
            return False
        else:
            self.set_game_password(self._game_password)
            return True

    def set_length(self, length):
        self.set_general_setting("settings_GameLength", length)

    def set_difficulty(self, difficulty):
        self.set_general_setting("settings_GameDifficulty", difficulty)

    def set_max_players(self, players):
        self.set_general_setting("settings_MaxPlayers", str(players))

    def toggle_map_voting(self):
        if self.general_settings["settings_bDisableMapVote"] == "1":
            self.set_general_setting("settings_bDisableMapVote", "0")
            return False
        else:
            self.set_general_setting("settings_bDisableMapVote", "1")
            return True

    def get_maps(self):
        response = self.web_interface.get_maplist()
        maplist_tree = html.fromstring(response.content)

        available_path = "//textarea[@id='allmaps']/text()"
        maps = maplist_tree.xpath(available_path)[0].split('\n')

        return maps

    def get_active_maps(self):
        response = self.web_interface.get_maplist()
        maplist_tree = html.fromstring(response.content)

        mapcycle_path = "//textarea[@id='mapcycle']/text()"
        maps = maplist_tree.xpath(mapcycle_path)[0].split('\n')

        return maps

    def set_server_name(self, name):
        self.set_general_setting("settings_ServerName", name)

    def set_map(self, new_map):
        self.map_settings['map'] = new_map
        self.web_interface.post_map(self.map_settings)

    def restart_map(self):
        self.web_interface.post_map(self.map_settings)

    def set_game_type(self, game_type):
        self.map_settings['gametype'] = game_type
        self.web_interface.post_map(self.map_settings)

    def activate_map_cycle(self, index):
        payload = {
            "maplistidx": str(index),
            "mapcycle": "KF-Default",
            "activate": "activate"
        }
        self.web_interface.post_map_cycle(payload)

    def set_map_cycle(self, index, maplist):
        payload = {
            "maplistidx": str(index),
            "mapcycle": maplist,
            "action": "save"
        }
        self.web_interface.post_map_cycle(payload)

    def set_motd(self, motd):
        self.motd_settings["ServerMOTD"] = motd \
            .encode("iso-8859-1", "ignore")
        self.web_interface.post_welcome(self.motd_settings)

        # Setting the MOTD resets changes to general settings
        self._save_general_settings()

    def get_motd(self):
        return self.motd_settings['ServerMOTD']

    def set_banner(self, banner_link):
        self.motd_settings["BannerLink"] = banner_link
        self.web_interface.post_welcome(self.motd_settings)

    def set_web_link(self, web_link):
        self.motd_settings["WebLink"] = web_link
        self.web_interface.post_welcome(self.motd_settings)

    def get_server_info(self):
        response = self.web_interface.get_server_info()
        info_tree = html.fromstring(response.content)

        server_update_data = self._parse_server_update(info_tree)
        match_update_data = self._parse_match_update(info_tree)
        players_update_data = self._parse_player_updates(info_tree)

        return server_update_data, match_update_data, players_update_data

    @staticmethod
    def _parse_player_updates(info_tree):
        player_updates = []

        # Empty servers only have a single <td> with an empty server message
        is_empty_path = "//table[@id=\"players\"]/tbody//td"
        is_empty_result = info_tree.xpath(is_empty_path)
        if len(is_empty_result) == 1:
            return player_updates

        theads_path = "//table[@id=\"players\"]/thead//th//text()"
        theads_result = [head.lower() for head in info_tree.xpath(theads_path)]

        if theads_result:
            name_col = theads_result.index("name") \
                if "name" in theads_result else None
            perk_col = theads_result.index("perk") \
                if "perk" in theads_result else None
            dosh_col = theads_result.index("dosh") \
                if "dosh" in theads_result else None
            health_col = theads_result.index("health") \
                if "health" in theads_result else None
            kills_col = theads_result.index("kills") \
                if "kills" in theads_result else None
            ping_col = theads_result.index("ping") \
                if "ping" in theads_result else None
            # admin_col = theads_result.index("admin")
            #     if "admin" in theads_result else None
        else:
            logger.info("Couldn't find server info headings")
            return player_updates

        # xpath to <td>s and retrieve text manually to catch empty cells
        trows_path = "//table[@id=\"players\"]/tbody/tr"
        trows_result = info_tree.xpath(trows_path)

        for player_row in trows_result:
            player_columns = player_row.xpath("td")
            player_updates.append(PlayerUpdateData(
                str(
                    (player_columns[name_col].text if name_col else "Unknown")
                    or "Unknown"
                ),
                str(
                    (player_columns[perk_col].text if perk_col else "Unknown")
                    or "Unknown"
                ),
                int(
                    (player_columns[kills_col].text if kills_col else 0)
                    or 0
                ),
                int(
                    (player_columns[health_col].text if health_col else 0)
                    or 0
                ),
                int(
                    (player_columns[dosh_col].text if dosh_col else 0)
                    or 0
                ),
                int(
                    (player_columns[ping_col].text if ping_col else 0)
                    or 0
                )
            ))
        return player_updates

    @staticmethod
    def _parse_match_update(info_tree):
        zeds_path = "//dd[@class=\"gs_wave\"]/text()"
        zeds_result = info_tree.xpath(zeds_path)

        if zeds_result:
            zeds_dead, zeds_total = map(int, zeds_result[0].split("/"))
            trader_open = bool(zeds_dead == zeds_total and zeds_total > 1)
        else:
            zeds_dead, zeds_total = None, None
            trader_open = False

        wave_path = "//dl[@id=\"currentRules\"]/dt[text()=\"Wave\"]" \
                    "/following-sibling::dd[1]/text()"
        wave_result = info_tree.xpath(wave_path)

        if wave_result:
            wave, _ = map(int, wave_result[0].split("/"))
        else:
            wave = None

        return MatchUpdateData(
            trader_open, zeds_total, zeds_dead, wave
        )

    @staticmethod
    def _parse_server_update(info_tree):
        # Difficulty
        difficulty_path = "//dl[@id=\"currentRules\"]" \
                          "/dt[text()=\"Difficulty\"]" \
                          "/following-sibling::dd[1]/text()"
        difficulty_result = info_tree.xpath(difficulty_path)

        if difficulty_result:
            difficulty_name = difficulty_result[0]
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

        # Game type
        game_type_path = "//dl[@id=\"currentGame\"]/dt[text()=\"Game type\"]" \
                         "/following-sibling::dd[1]/@title"
        game_type_result = info_tree.xpath(game_type_path)

        if game_type_result:
            game_type = game_type_result[0]
        else:
            game_type = GAME_TYPE_UNKNOWN

        # Map title and name
        map_title_path = "//dl[@id=\"currentGame\"]/dt[text()=\"Map\"]" \
                         "/following-sibling::dd[1]/@title"
        map_title_result = info_tree.xpath(map_title_path)
        map_name_path = "//dl[@id=\"currentGame\"]/dt[text()=\"Map\"]" \
                        "/following-sibling::dd[1]/text()"
        map_name_result = info_tree.xpath(map_name_path)

        if map_title_result and map_name_result:
            map_title, map_name = map_title_result[0], map_name_result[0]
        else:
            map_title, map_name = None, None

        # Capacity
        capacity_path = "//dl[@id=\"currentRules\"]/dt[text()=\"Players\"]" \
                        "/following-sibling::dd[1]/text()"
        capacity_result = info_tree.xpath(capacity_path)

        if capacity_result:
            _, capacity = map(int, capacity_result[0].split("/"))
        else:
            capacity = None

        # Length
        length_path = "//dl[@id=\"currentRules\"]/dt[text()=\"Wave\"]" \
                      "/following-sibling::dd[1]/text()"
        length_result = info_tree.xpath(length_path)

        if length_result:
            wave, length = map(int, length_result[0].split("/"))
        else:
            wave = None
            length = LEN_UNKNOWN

        return ServerUpdateData(
            map_title, map_name, length, difficulty, game_type, wave, capacity
        )

    def get_player_identity(self, username):
        response = self.web_interface.get_players()
        player_tree = html.fromstring(response.content)

        theads_path = "//table[@id=\"players\"]/thead//th[position()>1]" \
                      "//text()"
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

        player_keys_path = "//table[@id=\"players\"]/tbody" \
                           "//input[@name=\"playerkey\"]//@value"
        player_keys_result = player_tree.xpath(player_keys_path)
        for i, player_key in enumerate(player_keys_result):
            trows_result[i][player_key_col] = player_key

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

        if players_found != 1:
            logger.warning("Couldn't find identify player: {}".format(username))
            return None

        return PlayerIdentityData(
            ip, country, country_code, sid, nid, player_key
        )
