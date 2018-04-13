import requests
import sys
import logging

from hashlib import sha1
from lxml import html
from time import sleep

from server.chat.chat import ChatLogger
from server.managers.server_mapper import ServerMapper
from database.database import ServerDatabase

DIFF_NORM = "0.0000"
DIFF_HARD = "1.0000"
DIFF_SUI = "2.0000"
DIFF_HOE = "4.0000"

LEN_SHORT = "0"
LEN_NORM = "1"
LEN_LONG = "2"

logger = logging.getLogger(__name__)
if __debug__ and not hasattr(sys, 'frozen'):
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)


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
        print("Connecting to: {} ({})".format(self.name, self.address))
        self.session = self.new_session()

        self.general_settings = self.load_general_settings()
        self.game = {
            'map_title': 'kf-default',
            'map_name': 'kf-default',
            'wave': 0,
            'length': 7,
            'difficulty': 'normal'
        }
        self.zeds_killed = 0
        self.zeds_wave = 0
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
            logger.debug("Couldn't get settings " + self.name +
                         " (RequestException), sleeping for 3s")
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
                                 "!new_wave " + str(self.game['wave']),
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
        self.chat.handle_message("server",
                                 "!player_join " + player.username,
                                 admin=True)
        print("Player {} joined {}".format(player.username, self.name))

    def player_quit(self, quit_player):
        for player in self.players:
            if player.username == quit_player.username:
                print("Player {} quit {}".format(player.username,
                                                        self.name))
                self.chat.handle_message("server",
                                         "!p_quit " + player.username,
                                         admin=True)
                self.database.save_player(player, final=True)
                self.players.remove(player)

    def write_all_players(self, final=False):
        logger.debug("Flushing database")
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

    def toggle_game_password(self):
        passwords_url = "http://" + self.address + \
                        "/ServerAdmin/policy/passwords"
        payload = {
            'action': 'gamepassword'
        }

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
            payload['gamepw1'] = ""
            payload['gamepw2'] = ""

        try:
            self.session.post(passwords_url, payload)
        except requests.exceptions.RequestException:
            logger.warning("Couldn't set password on {} (RequestException)"
                           .format(self.name))
            sleep(3)
        if password_state == 'False':
            return True
        else:
            return False

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
        self.change_map(self.game['map_title'])
