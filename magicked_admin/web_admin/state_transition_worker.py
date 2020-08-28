import gettext
import threading
import time

from colorama import init

from events import (
    EVENT_SERVER_UPDATE, EVENT_MATCH_UPDATE, EVENT_PLAYERS_UPDATE,
    EVENT_PLAYER_UPDATE
)
from utils.alg import uuid

_ = gettext.gettext
init()


class StateTransitionWorker(threading.Thread):
    def __init__(self, web_admin, event_manager, refresh_rate=1):
        threading.Thread.__init__(self)

        self.event_manager = event_manager
        self.web_admin = web_admin

        self._exit = False
        self._refresh_rate = refresh_rate

        self.server_state_previous = None
        self.match_state_previous = None
        self.player_states_previous = []

    def run(self):
        while not self._exit:
            self._poll()
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

        if server_state != self.server_state_previous:
            self.event_manager.emit_event(
                EVENT_SERVER_UPDATE, self, server_update_data=server_state
            )
            self.server_state_previous = server_state

        if match_state != self.match_state_previous:
            self.event_manager.emit_event(
                EVENT_MATCH_UPDATE, self, match_update_data=match_state
            )
            self.match_state_previous = match_state

        if player_states != self.player_states_previous:
            # Only emit when someone joins or leaves
            usernames = [p.username for p in player_states]
            usernames_previous = [p.username for p in self.player_states_previous]
            if usernames != usernames_previous:
                self.event_manager.emit_event(
                    EVENT_PLAYERS_UPDATE, self, players_update_data=player_states
                )

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
                    self.event_manager.emit_event(
                        EVENT_PLAYER_UPDATE + "." + uuid(
                            player_state.username),
                        self.__class__, player_update_data=player_state
                    )

            self.player_states_previous = player_states
