import requests
import sys
import datetime
import threading
import time

from hashlib import sha1
from lxml import html
from time import sleep
from termcolor import colored

from server.chat.chat import ChatLogger
from database.database import ServerDatabase
from utils.logger import logger

import web_admin as api

import server.game as game
from server.game import Game
from server.game_map import GameMap
from server.player import Player


class Server:
    def __init__(self, name, address, username, password, ops=None):
        self.name = name

        print("Connecting to: {} ({})...".format(name, address))
        self.web_admin = api.web_admin(address, username, password, ops)
        message = "Connected to: {} ({})".format(name, address)
        print(colored(message, 'green'))

        self.game_password = None
        self.level_threshold = None

        self.game = Game(GameMap("kf-default"), api.MODE_UNKNOWN)
        self.trader_time = False
        self.players = []

        self.mapper = ServerMapper(self)
        self.mapper.start()

        self.database = ServerDatabase(name)

        logger.debug("Server " + name + " initialised")

    def close(self):
        self.mapper.stop()
        self.web_admin.close()

    def set_game_password(self, password):
        self.game_password = password

        self.web_admin.set_game_password(password)

    def new_wave(self):
        self.chat.handle_message("server",
                                 "!new_wave " + str(self.game.wave),
                                 admin=True)

        if int(self.game.wave) > int(self.game.game_map.highest_wave):
            self.game.game_map.highest_wave = int(self.game.wave)
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
        message = "New game on {}, map: {}, mode: {}"\
            .format(self.name, self.game.game_map.title,
                    self.game.gamemode)
        print(colored(message, 'magenta'))

        self.database.load_game_map(self.game.game_map)

        if self.game.gamemode == game.MODE_ENDLESS:
            self.game.game_map.plays_endless += 1
        elif self.game.gamemode == game.MODE_SURVIVAL:
            self.game.game_map.plays_survival += 1
        elif self.game.gamemode == game.MODE_SURVIVAL_VS:
            self.game.game_map.plays_survival_vs += 1
        elif self.game.gamemode == game.MODE_WEEKLY:
            self.game.game_map.plays_weekly += 1
        else:
            logger.debug("Unknown gamemode {}".format(self.game.gamemode))
            self.game.game_map.plays_other += 1


        self.web_admin.chat.handle_message("server", "!new_game", admin=True)

    def get_player(self, username):
        for player in self.players:
            if player.username == username:
                return player
        return None

    def player_join(self, player):
        self.database.load_player(player)
        player.total_logins += 1
        self.players.append(player)
        message = "Player {} joined {} from {}"\
            .format(player.username, self.name, player.country)
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
        logger.debug("Flushing players ({})".format(self.name))
        for player in self.players:
            self.database.save_player(player, final)

    def write_game_map(self):
        logger.debug("Writing to database ({})".format(self.name))
        self.database.save_game_map(self.game.game_map)

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
        # web_admin to forget settings
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
        self.web_admin.set_map(new_map)
        map_url = "http://" + self.address + "/ServerAdmin/current/change"
        payload = {
            "gametype": self.game.gamemode,
            "map": new_map,
            "mutatorGroupCount": "0",
            "urlextra": "?MaxPlayers={}".format(self.max_players),
            "action": "change"
        }

        try:
            self.session.post(map_url, payload)
        except requests.exceptions.RequestException:
            logger.warning("Couldn't set map on {} (RequestException)"
                           .format(self.name))
            sleep(3)

    def enforce_levels(self):
        for player in self.players:
            print(player.perk_level)
            if int(player.perk_level) < int(self.level_threshhold):
                self.kick_player(player.player_key)

    def kick_player(self, player_key):
        url = "http://" + self.address + "/ServerAdmin/current/players+data"
        payload = {
            'action': 'kick',
            'playerkey': player_key,
            'ajax': '1'
        }

        self.session.post(url, payload)
        print("REMOVED {}".format(player_key))
        return

    def restart_map(self):
        self.change_map(self.game.game_map.title)

    # Change the GameMode
    def change_gamemode(self, mode):
        url = "http://" + self.address + "/ServerAdmin/current/change"
        payload = {
            "gametype": mode,
            "map": self.game.game_map.title,
            "mutatorGroupCount": "0",
            "urlextra": "?MaxPlayers={}".format(self.max_players),
            "action": "change"
        }

        try:
            self.session.post(url, payload)
        except requests.exceptions.RequestException:
            logger.warning("Couldn't set GameMode on {} (RequestException)"
                           .format(self.name))
            sleep(3)


class ServerMapper(threading.Thread):

    def __init__(self, server):
        threading.Thread.__init__(self)

        self.server = server
        self.web_admin = server.web_admin

        self.__exit = False
        # TODO configuration option
        self.__refresh_rate = 20 if __debug__ else 5

        self.database = ServerDatabase(server.name)

    def run(self):
        while not self.__exit:
            self.__poll()
            time.sleep(self.__refresh_rate)

    def stop(self):
        self.__exit = True

    def __poll(self):
        game_now, players_now = self.web_admin.get_game_players()

        self.__update_players(players_now)
        self.__update_game(game_now)

    def __event_new_game(self):
        pass

    def __event_wave_start(self):
        pass

    def __event_wave_end(self):
        pass

    def __event_trader_open(self):
        pass

    def __event_trader_close(self):
        pass

    def __update_game(self, game_now):
        if game_now.wave < self.server.game.wave:
            self.__event_new_game()
        elif game_now.wave > self.server.game.wave:
            self.__event_wave_start()
        if game_now.zeds_dead == game_now.zeds_total:
            self.__event_wave_end()

        if game_now.trader_open and not self.server.trader_time:
            self.__event_trader_open()
        if not game_now.trader_open and self.server.trader_time:
            self.__event_trader_close()

        self.server.game.game_map.title = game_now.map_title
        self.server.game.game_map.name = game_now.map_name
        self.server.game.wave = game_now.wave
        self.server.game.length = game_now.length
        self.server.game.difficulty = game_now.difficulty
        self.server.game.zeds_dead = game_now.zeds_dead
        self.server.game.zeds_total = game_now.zeds_total
        self.server.game.game_type = game_now.game_type

    def __update_players(self, players_now):
        # Quitters
        for player in self.server.players:
            if player.username not in [p.username for p in players_now]:
                self.__event_player_quit(player)

        # Joiners
        for player in players_now:
            if player.username not in \
                    [p.username for p in self.server.players]:
                self.__event_player_join(player)

        for player in self.server.players:
            try:
                player_now = next(filter(
                    lambda p: p.username == player.username, players_now
                ))
            except StopIteration:
                self.server.players = []
                return

            player.ping = player_now.ping

            player.perk = player_now.perk
            player.total_kills += player_now.kills - player.kills

            player.wave_kills += player_now.kills - player.kills
            player.wave_dosh += player_now.dosh - player.dosh

            if player_now.dosh > player.dosh:
                player.game_dosh += player_now.dosh - player.dosh
                player.total_dosh += player_now.dosh - player.dosh
            else:
                player.total_dosh_spent += player.dosh - player_now.dosh

            player.kills = player_now.kills
            player.dosh = player_now.dosh
            player.health = player_now.health

    def __event_player_join(self, player):
        new_player = Player(player.username, player.perk)
        new_player.kills = player.kills
        new_player.dosh = player.dosh
        self.server.database.load_player(new_player)

        self.server.players.append(new_player)
        print(player.username + " joined")

    def __event_player_quit(self, player):
        self.server.players.remove(player)
        self.server.database.save_player(player)
        print(player.username + " left")