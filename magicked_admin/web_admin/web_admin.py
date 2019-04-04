import logging
from itertools import groupby

from lxml import html

from utils import DEBUG
from utils.geolocation import get_country
from utils.text import str_to_bool
from web_admin.chat import Chat
from web_admin.constants import *
from web_admin.web_interface import WebInterface


class WebAdmin(object):
    def __init__(self, address, username, password, ops=None,
                 server_name="unnamed"):
        self.__web_interface = \
            WebInterface(address, username, password, server_name)
        self.chat = Chat(self.__web_interface, ops)
        self.chat.start()

        self.__general_settings = \
            self.__web_interface.get_payload_general_settings()
        self.__motd_settings = \
            self.__web_interface.get_payload_motd_settings()
        self.__map_settings = \
            self.__web_interface.get_payload_map_settings()

        self.__game_password = None

    def close(self):
        self.chat.stop()

    def __save_general_settings(self):
        self.__web_interface.post_general_settings(
            self.__general_settings
        )

    def set_general_setting(self, setting, value):
        self.__general_settings[setting] = value
        self.__save_general_settings()

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
            print("Tried to toggle game password before setting value")
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

        odds = info_tree.xpath('//tr[@class="odd"]//td/text()')
        evens = info_tree.xpath('//tr[@class="even"]//td/text()')
        player_rows = odds + evens

        player_rows = [list(group) for k, group in
                       groupby(player_rows, lambda x: x == "\xa0") if not k]

        for player_row in player_rows:
            if len(player_row) < 7:
                # Player is dead TODO
                username, perk, dosh = player_row[:3]
                health = 0
                kills, ping = player_row[3:5]
            else:
                # Player is alive
                username, perk, dosh, health, kills, ping \
                    = player_row[:6]

            player = ConstPlayer(username, perk, int(kills),
                                 int(health), int(dosh), int(ping))
            players.append(player)
        return players

    @staticmethod
    def __get_game(info_tree):
        zed_status_pattern = "//dd[@class=\"gs_wave\"]/text()"
        zeds_dead, zeds_total = \
            info_tree.xpath(zed_status_pattern)[0].split("/")
        zeds_dead, zeds_total = int(zeds_dead), int(zeds_total)

        if zeds_dead == zeds_total and zeds_total > 1:
            trader_open = True
        else:
            trader_open = False

        zeds_total = int(zeds_total)
        zeds_dead = int(zeds_dead)

        dds = info_tree.xpath('//dd/text()')
        game_type = info_tree.xpath('//dl//dd/@title')[0]
        map_title = info_tree.xpath('//dl//dd/@title')[1]
        map_name = dds[0]
        wave, length = [int(val) for val in dds[7].split("/")]
        difficulty = dds[8]

        return ConstGame(trader_open, zeds_total, zeds_dead, map_title,
                         map_name, wave, length, difficulty, game_type)

    def get_player_identity(self, username):
        response = self.__web_interface.get_players()
        player_tree = html.fromstring(response.content)

        odds = player_tree.xpath('//tr[@class="odd"]//td/text()')
        evens = player_tree.xpath('//tr[@class="even"]//td/text()')

        player_rows = odds + evens
        player_rows = [list(group) for k, group in
                       groupby(player_rows, lambda x: x == "\xa0") if not k]

        player_key = player_tree.xpath('//tr/td[text()="{}"]'
                                       '/following-sibling::td'
                                       '//input[@name="playerkey"]/@value'
        .format(username))

        for player in player_rows:
            if player[0] == username:
                ip = player[2]
                steam_id = player[4]
                country, country_code = get_country(ip)
                return {
                    'ip': ip,
                    'country': country,
                    'country_code': country_code,
                    'steam_id': steam_id,
                    'player_key': player_key
                }

        if DEBUG:
            ("ERROR: Couldn't find identify player: {}".format(username))
        return {
            'ip': "0.0.0.0",
            'country': "Unknown",
            'country_code': "??",
            'steam_id': "00000000000000000",
            'player_key': "0x0.00"
        }
