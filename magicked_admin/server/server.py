import logging
import time

from chatbot.chatbot import Chatbot
from database import db_connector
from PySide2.QtCore import QObject, Signal, Slot
from server.level import Level
from server.match import Match
from server.player import Player
from web_admin.chat_worker import ChatWorker
from web_admin.constants import *  # FIXME
from web_admin.state_transition_worker import StateTransitionWorker

logger = logging.getLogger(__name__)


class ServerSignals(QObject):
    chat = Signal(str, str, int)
    post_chat = Signal(str, str, int)
    command = Signal(str, list, int)
    wave_start = Signal(Match)
    wave_end = Signal(Match)
    player_join = Signal(Player)
    player_quit = Signal(Player)
    player_death = Signal(Player)
    trader_open = Signal(Match)
    trader_close = Signal(Match)
    match_start = Signal(Match)
    match_end = Signal(Match)

    server_update = Signal(ServerUpdateData)
    players_update = Signal(list)  # Maybe this one should be moved/refactored
    match_update = Signal(MatchUpdateData)  # This too


class Server:
    def __init__(self, web_admin, name, game_password=None, url_extras=None):
        self.name = name
        self.web_admin = web_admin
        self.signals = ServerSignals()

        self.game_password = game_password
        self.url_extras = url_extras

        self.capacity = 0
        self.server_id = 0
        self.insert_date = 0

        self.players = []
        self.rejected_players = []

        self.init_db()

        self.match = Match(  # FIXME: Ugly
            self, Level(
                GAME_MAP_TITLE_UNKNOWN, GAME_MAP_TITLE_UNKNOWN, self
            ), GAME_TYPE_UNKNOWN, DIFF_UNKNOWN, LEN_UNKNOWN
        )

        self.chat_worker = ChatWorker(self)
        self.chat_worker.start()

        self.state_transition_worker = StateTransitionWorker(self)
        self.state_transition_worker.start()

        self.state_transition_worker.signals.server_update.connect(self.receive_update_data)
        self.signals.players_update.connect(self.receive_player_updates)

        self.chatbot = Chatbot(self)

    @db_connector
    def init_db(self, conn):
        sql = """
            INSERT OR IGNORE INTO server
                (name, insert_date)
            VALUES
                (?, ?)
        """
        cur = conn.cursor()
        cur.execute(sql, (self.name, int(time.time())))
        conn.commit()

        sql = """
            SELECT
                server_id, name, insert_date
            FROM
                server
            WHERE
                name = ?
        """
        cur.execute(sql, (self.name,))
        result, = cur.fetchall()

        self.server_id = result['server_id']
        self.insert_date = result['insert_date']

    @db_connector
    def record_players_online(self, conn):
        sql = """
            INSERT INTO server_players_date
                (server_id, players, date)
            VALUES
                (?, ?, ?)
        """

        cur = conn.cursor()
        cur.execute(sql, (self.server_id, len(self.players), int(time.time())))

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

    @Slot(ServerUpdateData)
    def receive_update_data(self, server_update_data):
        self.capacity = server_update_data.capacity

        new_match = self._is_new_match(server_update_data)

        # End current match unless its the first one
        if new_match and self.match:
            self.rejected_players = []

            logger.info("Match ended on {}, map: {}, mode: {}".format(
                self.name, self.match.level.name, self.match.game_type)
            )
            self.signals.wave_end.emit(self.match)
            self.match.close()

        # Set up next match
        if new_match:
            new_level = Level(
                server_update_data.map_title, server_update_data.map_name, self
            )
            new_match = Match(
                self, new_level, server_update_data.game_type,
                server_update_data.difficulty, server_update_data.length
            )
            self.match = new_match

        self.capacity = server_update_data.capacity

    @Slot(list)
    def receive_player_updates(self, players_update_data):
        # Quitters
        for player in self.players:
            if player.username not in [p.username for p in players_update_data]:
                self.players.remove(player)
                self.record_players_online()
                logger.info("Player, {}, left {}".format(player.username, self.name))
                self.signals.player_quit.emit(player)
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
                self.record_players_online()
                logger.info("Player, {}, joined {}".format(player.username, self.name))
                self.signals.player_join.emit(player)

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
        self.state_transition_worker.close()
        self.chat_worker.close()
        self.chatbot.close()

        if self.match:
            self.match.close()
        for player in self.players:
            player.close()

    @property
    def is_finished(self):
        return self.state_transition_worker.isFinished() \
               and self.chat_worker.isFinished() \
               and self.chatbot.is_finished()
