import requests
import sys
import datetime

from hashlib import sha1
from lxml import html
from time import sleep
from termcolor import colored

from server.chat.chat import ChatLogger
from server.managers.server_mapper import ServerMapper
from database.database import ServerDatabase
from utils.logger import logger

import server.game as game
from server.game import Game
from server.game_map import GameMap


class Server:
    def __init__(self, name, address, username, password, game_password):
        self.name = name
        self.address = address
        self.username = username
        self.password = password
        self.password_hash = "$sha1$" + \
                             sha1(password.encode("iso-8859-1", "ignore") +
                                  username.encode("iso-8859-1", "ignore"))\
                             .hexdigest()
        self.game_password = game_password

        self.database = ServerDatabase(name)
        print("\tConnecting to: {} ({})...".format(self.name, self.address))
        self.session = self.new_session()
        message = "\tConnected to: {} ({})".format(self.name, self.address)
        print(colored(message, 'green'))

        self.general_settings = self.load_general_settings()
        self.game = Game(GameMap("kf-default"), game.MODE_SURVIVAL)

        self.trader_time = False
        self.players = []

        self.chat = ChatLogger(self)
        self.chat.start()

        self.mapper = ServerMapper(self)
        self.mapper.start()

        logger.debug("Server " + name + " initialised")

    def new_session(self):
        login_url = "http://" + self.address + "/ServerAdmin/"
        login_payload = {
            'password_hash': self.password_hash,
            'username': self.username,
            'password': '',
            'remember': '-1'
        }

        try:
            s = requests.Session()

            login_page_response = s.get(login_url)

            if "hashAlg = \"sha1\"" not in login_page_response.text:
                login_payload['password_hash'] = self.password

            login_page_tree = html.fromstring(login_page_response.content)

            token = login_page_tree.xpath('//input[@name="token"]/@value')[0]
            login_payload.update({'token': token})

            login_response = s.post(login_url, data=login_payload)

            if "Invalid credentials" in login_response.text:
                logger.error("Bad credentials for server: " + self.name)
                input("Press enter to exit...")
                sys.exit()

        # Add in something to retry for X times.
        except requests.exceptions.RequestException:
            logger.error("Network error on: " + self.address +
                         " (" + self.name + "), bad address?")
            input("Press enter to exit...")
            sys.exit()

        return s

    def load_general_settings(self):
        settings = {}

        general_settings_url = "http://" + self.address + \
                               "/ServerAdmin/settings/general"

        try:
            general_settings_response = self.session.get(general_settings_url)
        except requests.exceptions.RequestException as e:
            logger.warning("Couldn't get settings " + self.name +
                         " (RequestException), sleeping for 3s")
            # This should retry, not continue to execute this function
            # general_settings_response may be unassigned.
            sleep(3)
        general_settings_tree = html.fromstring(
            general_settings_response.content
        )

        settings_names = general_settings_tree.xpath('//input/@name')
        settings_vals = general_settings_tree.xpath('//input/@value')

        radio_settings_names = general_settings_tree.xpath(
            '//input[@checked="checked"]/@name')
        radio_settings_vals = general_settings_tree.xpath(
            '//input[@checked="checked"]/@value')
        length_val = general_settings_tree.xpath(
            '//select[@id="settings_GameLength"]'
            '//option[@selected="selected"]/@value')[0]
        difficulty_val = general_settings_tree.xpath(
            '//input[@name="settings_GameDifficulty_raw"]/@value')[0]

        settings['settings_GameLength'] = length_val
        settings['settings_GameDifficulty'] = difficulty_val
        settings['action'] = 'save'

        for i in range(0,len(settings_names)):
            settings[settings_names[i]] = settings_vals[i]

        for i in range(0,len(radio_settings_names)):
            settings[radio_settings_names[i]] = radio_settings_vals[i]

        return settings

    def new_wave(self):
        self.chat.handle_message("server",
                                 "!new_wave " + str(self.game.wave),
                                 admin=True)
        for player in self.players:
            player.wave_kills = 0
            player.wave_dosh = 0

    def trader_open(self):
        self.trader_time = True
        self.chat.handle_message("server", "!t_open", admin=True)

    def trader_close(self):
        self.trader_time = False
        self.chat.handle_message("server", "!t_close", admin=True)

    def new_game(self):
        message = "New game on {}, map: {}"\
            .format(self.name, self.game.game_map.title)
        print(colored(message, 'magenta'))
        self.chat.handle_message("server", "!new_game", admin=True)

    def get_player(self, username):
        for player in self.players:
            if player.username == username:
                return player
        return None

    def player_join(self, player):
        self.database.load_player(player)
        player.total_logins += 1
        self.players.append(player)
        message = "Player {} joined {}".format(player.username, self.name)
        print(colored(message, 'cyan'))
        self.chat.handle_message("server",
                                 "!player_join " + player.username,
                                 admin=True)

    def player_quit(self, quit_player):
        for player in self.players:
            if player.username == quit_player.username:
                message = "Player {} quit {}"\
                    .format(quit_player.username, self.name)
                print(colored(message, 'cyan'))
                self.chat.handle_message("server",
                                         "!p_quit " + player.username,
                                         admin=True)
                self.database.save_player(player, final=True)
                self.players.remove(player)

    def write_all_players(self, final=False):
        logger.debug("Flushing database ({})".format(self.name))
        for player in self.players:
            self.database.save_player(player, final)

    def set_difficulty(self, difficulty):
        general_settings_url = "http://" + self.address + \
                               "/ServerAdmin/settings/general"

        self.general_settings['settings_GameDifficulty'] = difficulty
        self.general_settings['settings_GameDifficulty_raw'] = difficulty
        try:
            self.session.post(general_settings_url, self.general_settings)
        except requests.exceptions.RequestException:
            logger.warning("Couldn't set difficulty on {} (RequestException)"
                           .format(self.name))
            sleep(3)

    def set_length(self, length):
        general_settings_url = "http://" + self.address + \
                               "/ServerAdmin/settings/general"

        self.general_settings['settings_GameLength'] = length

        try:
            self.session.post(general_settings_url, self.general_settings)
        except requests.exceptions.RequestException:
            logger.warning("Couldn't set length on {} (RequestException)"
                           .format(self.name))
            sleep(3)

    def save_settings(self):
        # Addresses a problem where certain requests cause
        # webadmin to forget settings
        general_settings_url = "http://" + self.address + \
                               "/ServerAdmin/settings/general"
        try:
            self.session.post(general_settings_url, self.general_settings)
        except requests.exceptions.RequestException:
            logger.warning("Couldn't set general settings on {} "
                           "(RequestException)".format(self.name))
            sleep(3)

    # Re-write this to be enable and disbale password, that way when disabling
    # a password it will just straight up try and disable it and then when enabling it
    # It will check to see if it is already enabled. Also might look at how to pass parms
    # To this so that you can set a password not in the config.
    # This will need to be corrected elsewhere when done.
    def disable_password(self):
        passwords_url = "http://" + self.address + \
                        "/ServerAdmin/policy/passwords"
        payload = {
            'action': 'gamepassword'
        }

        payload['gamepw1'] = ""
        payload['gamepw2'] = ""

        self.mapper.inactive_timer = False

        try:
            self.session.post(passwords_url, payload)
        except requests.exceptions.RequestException:
            logger.warning("Could not disable password on {} (RequestException)"
                           .format(self.name))
            sleep(3)
            return False
        return True

    def enable_password(self, args):
        passwords_url = "http://" + self.address + \
                        "/ServerAdmin/policy/passwords"
        payload = {
            'action': 'gamepassword'
        }

        if args:
            self.mapper.inactive_timer = True
            self.mapper.inactive_time_start = datetime.datetime.now()
        else:
            self.mapper.inactive_timer = False

        try:
            passwords_response = self.session.get(passwords_url)
        except requests.exceptions.RequestException:
            logger.warning("Couldn't get password state on {} "
                           "(RequestException), returning".format(self.name))
            return
        passwords_tree = html.fromstring(passwords_response.content)

        password_state = passwords_tree.xpath(
            '//p[starts-with(text(),"Game password")]//em/text()')[0]

        if password_state == 'False':
            payload['gamepw1'] = self.game_password
            payload['gamepw2'] = self.game_password
        else:
            return True

        try:
            self.session.post(passwords_url, payload)
        except requests.exceptions.RequestException:
            logger.warning("Couldn't set password on {} (RequestException)"
                           .format(self.name))
            sleep(3)
            return False
        return True

    def change_map(self, new_map):
        map_url = "http://" + self.address + "/ServerAdmin/current/change"
        payload = {
            "gametype": "KFGameContent.KFGameInfo_Survival",
            "map": new_map,
            "mutatorGroupCount": "0",
            "urlextra": "?MaxPlayers=6",
            "action": "change"
        }

        try:
            self.session.post(map_url, payload)
        except requests.exceptions.RequestException:
            logger.warning("Couldn't set map on {} (RequestException)"
                           .format(self.name))
            sleep(3)

    def restart_map(self):
        self.change_map(self.game.game_map.title)
