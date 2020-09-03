from events.event import Event

EVENT_PLAYERS_UPDATE = 'event_players_update'

"""
player_update_data: web_admin.constants.PlayerUpdateData
"""
EVENT_PLAYER_UPDATE = 'event_player_update'

"""
server_update_data: web_admin.constants.ServerUpdateData
"""
EVENT_SERVER_UPDATE = 'event_server_update'

"""
match_update_data: web_admin.constants.MatchUpdateData
"""
EVENT_MATCH_UPDATE = 'event_match_update'

class EventManager:
    def __init__(self):
        self._events = {}

    def register_event(self, event, listener):
        if event not in self._events.keys():
            self._events[event] = Event(event)

        self._events[event].add_listener(listener)

    def unregister_event(self, event, listener):
        if event in self._events.keys() and listener in self._events[event]:
            self._events[event].remove_listener(listener)

    def emit_event(self, event, sender, **kwargs):
        if event not in [EVENT_MATCH_UPDATE, EVENT_PLAYER_UPDATE, EVENT_SERVER_UPDATE, EVENT_PLAYERS_UPDATE] and '0' not in event and '1' not in event:
            print("emission:", event, str(sender), kwargs)
        if event in self._events.keys():
            self._events[event].emit(sender, **kwargs)
