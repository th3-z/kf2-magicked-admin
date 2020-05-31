import gettext
import sys

from termcolor import colored

from server.player import Player
from utils import debug, warning, info
from web_admin.constants import *

_ = gettext.gettext


class Server:
    def __init__(self, web_admin, database, game, name):
        self.name = name
        self.database = database
        self.web_admin = web_admin

        self.game_password = None

        self.game = game
        self.trader_time = False
        self.players = []

        # Initial game's record data is discarded because some may be missed
        self.record_games = True

    def supported_mode(self):
        return self.web_admin.supported_mode(self.game.game_type)

    def stop(self):
        self.write_game_map()
        self.write_all_players()

    def get_player_by_username(self, username):
        matched_players = 0
        matched_player = None

        for player in self.players:
            # Unidentifiable players have no steam_id
            if username in player.username and player.steam_id:
                matched_players += 1
                matched_player = player

        if matched_players != 1:
            return None

        return matched_player

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

        if matched_players != 1:
            return None

        return matched_player

    def set_game_password(self, password):
        self.game_password = password
        self.web_admin.set_game_password(password)

    def toggle_game_password(self):
        self.web_admin.toggle_game_password()

    def write_all_players(self):
        debug(_("Flushing players on {}").format(self.name))
        for player in self.players:
            self.database.save_player(player)

    def write_game_map(self):
        debug(_("Writing game to database ({})").format(
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
        if active_only:
            return self.web_admin.get_active_maps()
        else:
            return self.web_admin.get_maps()

    def find_map(self, search_title):
        matches = 0
        matched_title = None

        for map_title in self.get_maps():
            if search_title.upper() in map_title.upper():
                matches += 1
                matched_title = map_title

        if matches != 1:
            return None

        return matched_title

    def change_map(self, new_map):
        matched_title = self.find_map(new_map)

        if not matched_title:
            return None

        self.web_admin.set_map(matched_title)

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

        self.web_admin.ban_player(player.steam_id, player.player_key)
        return player.username

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
        message = _("Player {} joined {} from {}") \
            .format(new_player.username, self.name, new_player.country)
        print(colored(
            message.encode("utf-8").decode(sys.stdout.encoding), 'cyan'
        ))
        info(
            "{} (SteamID: {})".format(message, new_player.steam_id),
            display=False
        )
        self.web_admin.chat.handle_message(
            "internal_command",
            "!player_join " + new_player.username,
            USER_TYPE_INTERNAL
        )

    def event_player_quit(self, player):
        self.players.remove(player)
        self.database.save_player(player)

        message = _("Player {} left {}") \
            .format(player.username, self.name)
        print(colored(
            message.encode("utf-8").decode(sys.stdout.encoding), 'cyan'
        ))
        info(
            "{} (SteamID: {})".format(message, player.steam_id),
            display=False
        )
        self.web_admin.chat.handle_message("internal_command",
                                           "!player_quit " + player.username,
                                           USER_TYPE_INTERNAL)

    def event_player_death(self, player):
        player.total_deaths += 1
        message = _("Player {} died on {}").format(player.username, self.name)
        print(colored(
            message.encode("utf-8").decode(sys.stdout.encoding), 'red'
        ))

    def event_new_game(self):
        if self.game.game_type in GAME_TYPE_DISPLAY:
            display_name = GAME_TYPE_DISPLAY[self.game.game_type]
        else:
            display_name = GAME_TYPE_UNKNOWN
        message = _("New game on {}, map: {}, mode: {}") \
            .format(self.name, self.game.game_map.name, display_name)
        print(colored(
            message.encode("utf-8").decode(sys.stdout.encoding), 'magenta'
        ))

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
            warning(_("Unknown game_type {}").format(self.game.game_type))
            self.game.game_map.plays_other += 1

        self.web_admin.chat.handle_message("internal_command", "!new_game",
                                           USER_TYPE_INTERNAL)

    def event_end_game(self, victory=False):
        debug(_("End game on {}, map: {}, mode: {}, victory: {}").format(
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
        command = "!t_open {}".format(self.game.wave)
        self.web_admin.chat.handle_message("internal_command", command,
                                           USER_TYPE_INTERNAL)

    def event_trader_close(self):
        self.trader_time = False
        command = "!t_close {}".format(self.game.wave)
        self.web_admin.chat.handle_message("internal_command", command,
                                           USER_TYPE_INTERNAL)
