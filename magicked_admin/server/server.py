from termcolor import colored

import web_admin as api
from database.database import ServerDatabase
from server.game import Game, GameMap
from server.game_tracker import GameTracker
from server.player import Player
from utils import DEBUG, debug, info, warning
from web_admin.constants import *


class Server:
    def __init__(self, name, address, username, password):
        self.name = name

        info("Connecting to {} ({})...".format(name, address))
        self.web_admin = api.WebAdmin(address, username, password, name)
        info("Connected to {} ({})".format(name,address))

        self.database = ServerDatabase(name)

        self.game_password = None
        self.level_threshold = None
        self.dosh_threshold = None

        self.game = Game(GameMap(), GAME_TYPE_UNKNOWN)
        self.trader_time = False
        self.players = []

        # Initial game's record data is discarded because some may be missed
        self.record_games = True

        self.tracker = GameTracker(self)
        self.tracker.start()

    def supported_mode(self):
        return self.web_admin.supported_mode(self.game.game_type)

    def close(self):
        self.tracker.stop()
        self.write_game_map()
        self.write_all_players()
        self.web_admin.close()

    def get_player_by_username(self, username):
        matched_players = 0
        matched_player = None

        for player in self.players:
            # Unidentifiable players have no steam_id
            if username in player.username and player.steam_id:
                matched_players += 1
                matched_player = player

        if matched_players == 1:
            return matched_player
        else:
            return None

    def get_player_by_key(self, player_key):
        for player in self.players:
            if player.player_key == player_key:
                return player
        return None

    def get_player_by_sid(self, sid):
        matched_players = 0
        matched_player = None

        for player in self.players:
            if sid in player.steam_id:
                matched_players += 1
                matched_player = player

        if matched_players == 1:
            return matched_player
        else:
            return None

    def set_game_password(self, password):
        self.game_password = password
        self.web_admin.set_game_password(password)

    def toggle_game_password(self):
        self.web_admin.toggle_game_password()

    def write_all_players(self):
        debug("Flushing players on {}".format(self.name))
        for player in self.players:
            self.database.save_player(player)

    def write_game_map(self):
        debug("Writing game to database ({})".format(
              self.game.game_map.name
        ))
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
    
    def get_maps(self, active_only=False):
        return self.web_admin.get_maps()

    def find_map(self, search_title):
        matches = 0
        matched_title = None

        for map_title in self.get_maps():
            if search_title.upper() in map_title.upper():
                matches += 1
                matched_title = map_title

        if matched_title and matches == 1: 
            return matched_title
        else:
            return None

    def change_map(self, new_map):
        matched_title = self.find_map(new_map)

        if matched_title: 
            self.web_admin.set_map(matched_title)
        else:
            return None

    def kick_player(self, username):
        player = self.get_player_by_username(username)
        if not player:
            player = self.get_player_by_sid(username)
        if not player: 
            return False
        
        self.web_admin.kick_player(player.player_key)
        return player.username

    def ban_player(self, username):
        player = self.get_player_by_username(username)
        if not player:
            player = self.get_player_by_sid(username)
        if not player:
            return False

        self.web_admin.ban_player(player.player_key)
        return player.username

    def enforce_levels(self):
        if not self.level_threshold:
            return

        for player in self.players:
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
        new_player.sessions += 1

        self.players.append(new_player)
        message = "Player {} joined {} from {}" \
            .format(new_player.username, self.name, new_player.country)
        print(colored(message, 'cyan'))
        self.web_admin.chat.handle_message("internal_command",
                                           "!player_join " + new_player.username,
                                           USER_TYPE_INTERNAL)

    def event_player_quit(self, player):
        self.players.remove(player)
        self.database.save_player(player)

        message = "Player {} left {}" \
            .format(player.username, self.name)
        print(colored(message, 'cyan'))
        self.web_admin.chat.handle_message("internal_command",
                                           "!player_quit " + player.username,
                                           USER_TYPE_INTERNAL)

    def event_player_death(self, player):
        player.total_deaths += 1
        message = "Player {} died on {}".format(player.username, self.name)
        print(colored(message, 'red'))

    def event_new_game(self):
        message = "New game on {}, map: {}, mode: {}" \
            .format(self.name, self.game.game_map.name,
                    GAME_TYPE_NAME[self.game.game_type])
        print(colored(message, 'magenta'))

        self.database.load_game_map(self.game.game_map)
        self.game.new_game()

        if self.game.game_type == GAME_TYPE_ENDLESS:
            self.game.game_map.plays_endless += 1
        elif self.game.game_type == GAME_TYPE_SURVIVAL:
            self.game.game_map.plays_survival += 1
        elif self.game.game_type == GAME_TYPE_SURVIVAL_VS:
            self.game.game_map.plays_survival_vs += 1
        elif self.game.game_type == GAME_TYPE_WEEKLY:
            self.game.game_map.plays_weekly += 1
        else:
            warning("Unknown game_type {}".format(self.game.game_type))
            self.game.game_map.plays_other += 1

        self.web_admin.chat.handle_message("internal_command", "!new_game", USER_TYPE_INTERNAL)

    def event_end_game(self, victory=False):
        debug("End game on {}, map: {}, mode: {}, victory: {}".format(
              self.name, self.game.game_map.title, self.game.game_type, 
              str(victory)
        ))

        self.write_game_map()
        self.database.save_map_record(self.game, len(self.players), victory)

    def event_wave_start(self):
        self.web_admin.chat.handle_message("internal_command",
                                           "!new_wave " + str(self.game.wave),
                                           USER_TYPE_INTERNAL)

        if self.game.wave > self.game.game_map.highest_wave:
            self.game.game_map.highest_wave = self.game.wave
        for player in self.players:
            player.wave_kills = 0
            player.wave_dosh = 0

    def event_wave_end(self):
        pass

    def event_trader_open(self):
        self.trader_time = True
        self.web_admin.chat.handle_message("internal_command", "!t_open", USER_TYPE_INTERNAL)

    def event_trader_close(self):
        self.trader_time = False
        self.web_admin.chat.handle_message("internal_command", "!t_close", USER_TYPE_INTERNAL)
