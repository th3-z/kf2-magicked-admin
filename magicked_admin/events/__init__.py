from events.event_manager import EventManager

"""
players_update_data: List[web_admin.constants.PlayerUpdateData]
"""
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

"""
player: server.player.Player
"""
EVENT_PLAYER_JOIN = 'event_player_join'
EVENT_PLAYER_QUIT = 'event_player_quit'
EVENT_PLAYER_DEATH = "event_player_death"

"""
username: str
message: str
user_flags: int
"""
EVENT_CHAT = 'event_chat'

"""
args: List
message: str
user_flags: int
"""
EVENT_COMMAND = 'event_command'

"""
match: server.match.Match
"""
EVENT_TRADER_OPEN = "event_trader_open"
EVENT_TRADER_CLOSE = "event_trader_close"
EVENT_WAVE_START = "event_wave_start"
EVENT_WAVE_END = "event wave end"
EVENT_MATCH_START = "event_match_start"
EVENT_MATCH_END = "event_match_end"
