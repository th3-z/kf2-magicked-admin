import gettext
import sys

from termcolor import colored

from server.player import Player
from utils import debug, warning, info, DEBUG
from server.session import start_session, end_session
from web_admin.constants import *

_ = gettext.gettext


class Server:
    def __init__(self, web_admin, name):
        self.name = name
        self.web_admin = web_admin

        self.game_password = None

        self.match = None
        self.players = []
        self.rejected_players = []

        self.capacity = 0

    def get_player_by_username(self, username):
        matched_players = 0
        matched_player = None

        for player in self.players:
            if username in player.username and player.steam_id:
                matched_players += 1
                matched_player = player

        if matched_players != 1:
            return None

        return matched_player

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

    def supported_mode(self):
        return self.web_admin.supported_mode(self.match.game_type)

    def set_game_password(self, password):
        self.game_password = password
        self.web_admin.set_game_password(password)

    def toggle_game_password(self):
        self.web_admin.toggle_game_password()

    def write_game_map(self):
        pass

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
        self.change_map(self.match.level.title)

    def change_game_type(self, mode):
        self.web_admin.set_game_type(mode)

    def event_player_join(self, const_player):
        if const_player.username not in self.rejected_players:
            identity = self.web_admin.get_player_identity(const_player.username)
        else:
            return

        # Reject unidentifiable players
        if not identity['steam_id']:
            debug("Rejected player: {}".format(const_player.username))
            self.rejected_players.append(const_player.username)
            return

        player = Player(identity['steam_id'], const_player.username)
        player.ip = identity['ip']
        player.country = identity['country']
        player.country_code = identity['country_code']
        player.player_key = identity['player_key']
        player.username = const_player.username

        player.session_id = start_session(player.steam_id, self.match.match_id)

        self.players.append(player)

        if DEBUG:
            message = _("Player {} ({}) joined {} from {}").format(
                player.username, player.steam_id, self.name,
                player.country
            )
        else:
            message = _("Player {} joined {} from {}") \
                .format(player.username, self.name, player.country)

        print(colored(
            message.encode("utf-8").decode(sys.stdout.encoding), 'cyan'
        ))

        self.web_admin.chat.handle_message(
            "internal_command",
            "!player_join " + player.username,
            USER_TYPE_INTERNAL
        )

    def event_player_quit(self, player):
        self.players.remove(player)
        player.update_session()
        end_session(player.session_id)

        message = _("Player {} left {}") \
            .format(player.username, self.name)
        print(colored(
            message.encode("utf-8").decode(sys.stdout.encoding), 'cyan'
        ))

        self.web_admin.chat.handle_message("internal_command",
                                           "!player_quit " + player.username,
                                           USER_TYPE_INTERNAL)

    def event_player_death(self, player):

        message = _("Player {} died on {}").format(player.username, self.name)
        print(colored(
            message.encode("utf-8").decode(sys.stdout.encoding), 'red'
        ))

    def stop(self):
        pass

    def event_new_game(self):
        if self.match.game_type in GAME_TYPE_DISPLAY:
            display_name = GAME_TYPE_DISPLAY[self.match.game_type]
        else:
            display_name = GAME_TYPE_UNKNOWN
        message = _("New game on {}, map: {}, mode: {}") \
            .format(self.name, self.match.level.name, display_name)
        print(colored(
            message.encode("utf-8").decode(sys.stdout.encoding), 'magenta'
        ))

        # self.database.load_game_map(self.match.game_map)
        # self.game.new_game()

        self.rejected_players = []

        self.web_admin.chat.handle_message("internal_command", "!new_game",
                                           USER_TYPE_INTERNAL)

    def event_end_game(self, victory=False):
        debug(_("End game on {}, map: {}, mode: {}, victory: {}").format(
            self.name, self.game.game_map.title, self.game.game_type,
            str(victory)
        ))

        #self.write_game_map()
        #self.database.save_map_record(self.game, len(self.players), victory)

    def event_wave_start(self):
        self.web_admin.chat.handle_message("internal_command",
                                           "!new_wave " + str(self.game.wave),
                                           USER_TYPE_INTERNAL)

        if self.game.wave > self.game.game_map.highest_wave:
            self.game.game_map.highest_wave = self.game.wave

        for player in self.players:
            player.wave_kills = 0
            player.wave_dosh = 0
            player.wave_dosh_spent = 0
            player.wave_damage_taken = 0
            player.wave_deaths = 0

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
