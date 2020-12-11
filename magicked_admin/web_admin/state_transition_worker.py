import gettext
import time

from PySide2.QtCore import QObject, QThread, Signal, QCoreApplication

from web_admin.constants import MatchUpdateData, ServerUpdateData

_ = gettext.gettext


class StateTransitionSignals(QObject):
    poll = Signal()
    server_update = Signal(ServerUpdateData)


class StateTransitionWorker(QThread):
    def __init__(self, server, refresh_rate=1):
        super(StateTransitionWorker, self).__init__()

        self.server = server
        self.server_signals = server.signals
        self.signals = StateTransitionSignals()
        self.web_admin = server.web_admin

        self._exit = False
        self._refresh_rate = refresh_rate

        self.server_state_previous = None
        self.match_state_previous = None
        self.player_states_previous = []

    def run(self):
        while not self._exit:
            self._poll()
            self.signals.poll.emit()
            time.sleep(self._refresh_rate)

    def close(self):
        self._exit = True

    @staticmethod
    def _props_match(obj_a, obj_b, props):
        for prop in props:
            if getattr(obj_a, prop) != getattr(obj_b, prop):
                return False
        else:
            return True

    def _poll(self):
        server_state, match_state, player_states = self.web_admin.get_server_info()
        if not server_state:
            return

        if server_state != self.server_state_previous:
            self.signals.server_update.emit(server_state)
            self.server_state_previous = server_state

        if match_state != self.match_state_previous:
            self.server_signals.match_update.emit(match_state)
            self.match_state_previous = match_state

        if player_states != self.player_states_previous:
            # Only emit when someone joins or leaves
            usernames = [p.username for p in player_states]
            usernames_previous = [p.username for p in self.player_states_previous]
            if usernames != usernames_previous:
                self.server_signals.players_update.emit(player_states)

            # Individual players
            for player_state in player_states:
                for player_state_previous in self.player_states_previous:
                    if player_state_previous.username == player_state.username:
                        break
                else:
                    continue

                # Don't care about ping, already matched username
                trigger_props = ["dosh", "kills", "health", "perk"]
                if not self._props_match(
                        player_state, player_state_previous, trigger_props
                ):
                    player = self.server.get_player_by_username(player_state.username)
                    if player:
                        player.signals.player_update.emit(player_state)
                    # Else: Player was rejected or hasn't joined yet TODO: Check other calls to s.get_p_by_u

            self.player_states_previous = player_states
