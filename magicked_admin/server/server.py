import gettext

from server.player import Player
from server.level import Level
from server.match import Match

from events import (
    EVENT_SERVER_UPDATE, EVENT_PLAYERS_UPDATE, EVENT_MATCH_END,
    EVENT_PLAYER_JOIN, EVENT_PLAYER_QUIT
)

_ = gettext.gettext


class Server:
    def __init__(self, web_admin, event_manager, name):
        self.name = name
        self.web_admin = web_admin

        self.game_password = None

        self.match = None
        self.players = []
        self.rejected_players = []

        self.event_manager = event_manager

        self.capacity = 0

        event_manager.register_event(
            EVENT_SERVER_UPDATE, self.receive_update_data
        )
        event_manager.register_event(
            EVENT_PLAYERS_UPDATE, self.receive_player_updates
        )

    def _is_new_match(self, server_update_data):
        # Uninitialized (first match)
        if not self.match:
            return True

        # Game mode switched
        if self.match.game_type != server_update_data.game_type:
            return True

        # Level changed
        if self.match.level.title != server_update_data.map_title:
            return True

        # Wave counter decreased
        if server_update_data.wave < (self.match.wave or 0):
            return True

        return False
        
    def receive_update_data(self, event, sender, server_update_data):
        self.capacity = server_update_data.capacity

        new_match = self._is_new_match(server_update_data)

        # End current match unless its the first one
        if new_match and self.match:
            self.rejected_players = []
            self.event_manager.emit_event(
                EVENT_MATCH_END, self.__class__, match=self.match
            )
            self.match.close()

        # Set up next match
        if new_match:
            new_level = Level(
                server_update_data.map_title, server_update_data.map_name
            )
            new_match = Match(
                self, new_level, server_update_data.game_type,
                server_update_data.difficulty, server_update_data.length
            )
            self.match = new_match

        self.capacity = server_update_data.capacity

    def receive_player_updates(self, event, sender, players_update_data):
        # Quitters
        for player in self.players:
            if player.username not in [p.username for p in players_update_data]:
                self.event_manager.emit_event(
                    EVENT_PLAYER_QUIT, self.__class__, player=player
                )
                self.players.remove(player)
                player.close()

        # Joiners
        for player_update_data in players_update_data:
            # Filter pawns
            if "KFAIController" in player_update_data.username:
                continue
            if player_update_data.username in self.rejected_players:
                continue

            if player_update_data.username not in [p.username for p in self.players]:
                identity = self.web_admin.get_player_identity(
                    player_update_data.username
                )
                if not identity:
                    self.rejected_players.append(player_update_data.username)
                    continue

                player = Player(self, player_update_data.username, identity)
                self.players.append(player)
                self.event_manager.emit_event(
                    EVENT_PLAYER_JOIN, self.__class__, player=player
                )

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
        return self.web_admin.supported_game_type(self.match.game_type)

    def set_game_password(self, password):
        self.game_password = password
        self.web_admin.set_game_password(password)

    def toggle_game_password(self):
        self.web_admin.toggle_game_password()

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

    def close(self):
        if self.match:
            self.match.close()
        for player in self.players:
            player.close()
