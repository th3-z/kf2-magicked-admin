import threading
import time

import requests
from lxml import html
from termcolor import colored

import server.game as game
import web_admin as api
from database.database import ServerDatabase
from server.game import Game, GameMap
from server.player import Player
from utils import DEBUG, debug
from web_admin.constants import *


class Server:
    def __init__(self, name, address, username, password, ops=None):
        self.name = name

        print("Connecting to: {} ({})...".format(name, address))
        self.web_admin = api.WebAdmin(address, username, password, ops)
        message = "Connected to: {} ({})".format(name, address)
        print(colored(message, 'green'))

        self.game_password = None

        self.level_threshold = None
        self.dosh_threshold = None

        self.game = Game(GameMap("kf-default"), GAME_TYPE_UNKNOWN)
        self.trader_time = False
        self.players = []

        # Initial game's record data is discarded because some may be missed
        self.record_games = True

        self.tracker = GameTracker(self)
        self.tracker.start()

        self.database = ServerDatabase(name)

    def close(self):
        self.tracker.stop()
        self.write_game_map()
        self.write_all_players()
        self.web_admin.close()

    def get_player_by_username(self, username):
        for player in self.players:
            if player.username == username:
                return player
        return None

    def get_player_by_key(self, player_key):
        for player in self.players:
            if player.player_key == player_key:
                return player
        return None

    def get_player_by_sid(self, sid):
        for player in self.players:
            if player.sid == sid:
                return player
        return None

    def set_game_password(self, password):
        self.game_password = password
        self.web_admin.set_game_password(password)

    def toggle_game_password(self):
        self.web_admin.toggle_game_password()

    def write_all_players(self):
        if DEBUG:
            debug("Flushing players on {}".format(self.name))
        for player in self.players:
            self.database.save_player(player)

    def write_game_map(self):
        if DEBUG:
            debug("Writing game to database ({})".format(self.name))
        self.database.save_game_map(self.game.game_map)

    def set_difficulty(self, difficulty):
        self.web_admin.set_difficulty(difficulty)

    def set_length(self, length):
        self.web_admin.set_length(length)

    def disable_password(self):
        self.web_admin.set_game_password()

    def enable_password(self, password=None):
        if password:
            self.web_admin.set_game_password(password)
        else:
            self.web_admin.set_game_password(self.game_password)

    def change_map(self, new_map):
        self.web_admin.set_map(new_map)

    def kick_player(self, username):
        player = self.get_player_by_username(username)
        self.web_admin.kick_player(player.player_key)

    def enforce_levels(self):
        if not self.level_threshold:
            return

        for player in self.players:
            print(player)
            if player.perk_level < self.level_threshold:
                self.web_admin.kick_player(player.player_key)

    def enforce_dosh(self):
        if not self.dosh_threshold:
            return

        for player in self.players:
            if player.dosh > self.dosh_threshold:
                self.web_admin.kick_player(player.player_key)

    def restart_map(self):
        self.change_map(self.game.game_map.title)

    def change_game_type(self, mode):
        self.web_admin.set_game_type(mode)

    def event_player_join(self, player):
        identity = self.web_admin.get_player_identity(player.username)

        new_player = Player(player.username, player.perk)
        new_player.kills = player.kills
        new_player.dosh = player.dosh

        new_player.ip = identity['ip']
        new_player.country = identity['country']
        new_player.country_code = identity['country_code']
        new_player.steam_id = identity['steam_id']
        new_player.player_key = identity['player_key']

        self.database.load_player(new_player)

        self.players.append(new_player)
        message = "Player {} joined {} from {}" \
            .format(new_player.username, self.name, new_player.country)
        print(colored(message, 'cyan'))
        self.web_admin.chat.handle_message("server",
                                           "!player_join " + new_player.username,
                                           USER_TYPE_SERVER)

    def event_player_quit(self, player):
        self.players.remove(player)
        self.database.save_player(player)

        message = "Player {} quit {}" \
            .format(player.username, self.name)
        print(colored(message, 'cyan'))
        self.web_admin.chat.handle_message("server",
                                           "!player_quit " + player.username,
                                           USER_TYPE_SERVER)

    def event_player_death(self, player):
        player.total_deaths += 1
        message = "Player {} died on {}".format(player.username, self.name)
        print(colored(message, 'red'))

    def event_new_game(self):
        message = "New game on {}, map: {}, mode: {}" \
            .format(self.name, self.game.game_map.title,
                    self.game.game_type)
        print(colored(message, 'magenta'))

        self.database.load_game_map(self.game.game_map)

        if self.game.game_type == GAME_TYPE_ENDLESS:
            self.game.game_map.plays_endless += 1
        elif self.game.game_type == GAME_TYPE_SURVIVAL:
            self.game.game_map.plays_survival += 1
        elif self.game.game_type == GAME_TYPE_SURVIVAL_VS:
            self.game.game_map.plays_survival_vs += 1
        elif self.game.game_type == GAME_TYPE_WEEKLY:
            self.game.game_map.plays_weekly += 1
        else:
            if DEBUG:
                print("Unknown game_type {}".format(self.game.game_type))
            self.game.game_map.plays_other += 1

        self.web_admin.chat.handle_message("server", "!new_game", USER_TYPE_SERVER)

    def event_end_game(self, win=False):
        if win and self.game.game_type == GAME_TYPE_SURVIVAL:
            self.database.save_map_record(self.game, len(self.players))
            print("Recorded game time: " + str(self.game.time))

    def event_wave_start(self):
        self.web_admin.chat.handle_message("server",
                                           "!new_wave " + str(self.game.wave),
                                           USER_TYPE_SERVER)

        if int(self.game.wave) > int(self.game.game_map.highest_wave):
            self.game.game_map.highest_wave = int(self.game.wave)
        for player in self.players:
            player.wave_kills = 0
            player.wave_dosh = 0

    def event_wave_end(self):
        pass

    def event_trader_open(self):
        self.trader_time = True
        self.web_admin.chat.handle_message("server", "!t_open", USER_TYPE_SERVER)

    def event_trader_close(self):
        self.trader_time = False
        self.web_admin.chat.handle_message("server", "!t_close", USER_TYPE_SERVER)


class GameTracker(threading.Thread):

    def __init__(self, server):
        threading.Thread.__init__(self)

        self.server = server
        self.web_admin = server.web_admin

        self.__exit = False
        # TODO configuration option
        self.__refresh_rate = 20 if DEBUG else 1
        self.__boss_reached = False

        self.game_timer = time.time()
        self.written_record = True  # Ignore records for first match

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

    def __update_game(self, game_now):
        # Game type specific code
        if game_now.game_type == GAME_TYPE_SURVIVAL:
            self.__update_game_survival(game_now)
        elif game_now.game_type == GAME_TYPE_ENDLESS:
            self.__update_game_survival_vs(game_now)
        elif game_now.game_type == GAME_TYPE_WEEKLY:
            self.__update_game_survival_vs(game_now)
        elif game_now.game_type == GAME_TYPE_SURVIVAL_VS:
            self.__update_game_survival_vs(game_now)

        if game_now.wave and (game_now.wave < self.server.game.wave):
            self.server.event_new_game()

        if game_now.trader_open and not self.server.trader_time:
            self.server.event_trader_open()
        if not game_now.trader_open and self.server.trader_time:
            self.server.event_trader_close()

        self.server.game.game_map.title = game_now.map_title
        self.server.game.game_map.name = game_now.map_name
        self.server.game.wave = game_now.wave
        self.server.game.length = game_now.length
        self.server.game.difficulty = game_now.difficulty
        self.server.game.zeds_dead = game_now.zeds_dead
        self.server.game.zeds_total = game_now.zeds_total
        self.server.game.game_type = game_now.game_type

        if not self.server.trader_time and 0 < int(
                self.server.game.wave) <= int(self.server.game.length):
            now = time.time()
            self.server.game.time += now - self.game_timer
            self.game_timer = time.time()
        else:
            self.game_timer = time.time()

    def __update_game_survival(self, game_now):
        # Boss wave
        if game_now.wave > self.server.game.length:
            # Attempt to identify game over on boss wave
            game_over = True
            for player in self.server.players:
                if player.health and player.kills and player.ping:
                    game_over = False

            if game_over:
                self.server.event_end_game(False)

    def __update_game_endless(self, game_now):
        pass

    def __update_game_weekly(self, game_now):
        pass

    def __update_game_survival_vs(self, game_now):
        pass

    def __update_players(self, players_now):
        # Quitters
        for player in self.server.players:
            if player.username not in [p.username for p in players_now]:
                self.server.event_player_quit(player)

        # Joiners
        for player in players_now:
            if player.username not in \
                    [p.username for p in self.server.players]:
                self.server.event_player_join(player)

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

            if not player_now.health and player_now.health < player.health:
                self.server.event_player_death(player)

            if player_now.dosh > player.dosh:
                player.game_dosh += player_now.dosh - player.dosh
                player.total_dosh += player_now.dosh - player.dosh
            else:
                player.total_dosh_spent += player.dosh - player_now.dosh

            player.kills = player_now.kills
            player.dosh = player_now.dosh
            player.health = player_now.health

            player.update_time()
