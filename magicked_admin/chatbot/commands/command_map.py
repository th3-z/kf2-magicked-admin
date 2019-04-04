from chatbot.commands.event_commands import *
from chatbot.commands.info_commands import *
from chatbot.commands.player_commands import *
from chatbot.commands.server_commands import *


class CommandMap:
    def __init__(self, server, chatbot):
        self.server = server
        self.chatbot = chatbot
        self.command_map = self.generate_map()

    def generate_map(self):
        """
        Generates the command mapping (key/value pairs) that are used by the (chat bot was it?)
        """
        wave_event_manager = CommandOnWaveManager(self.server, self.chatbot)
        trader_event_manager = CommandOnTraderManager(self.server, self.chatbot)
        time_event_manager = CommandOnTimeManager(self.server, self.chatbot)
        greeter = CommandGreeter(self.server)

        command_map = {
            'new_game': greeter,
            'player_join': greeter,
            'stop_wc': wave_event_manager,
            'start_wc': wave_event_manager,
            'new_wave': wave_event_manager,
            'start_tc': time_event_manager,
            'stop_tc': time_event_manager,
            'start_trc': trader_event_manager,
            'stop_trc': trader_event_manager,
            't_close': trader_event_manager,
            't_open': trader_event_manager,
            'record_wave': CommandHighWave(self.server, admin_only=False),
            'enforce_levels': CommandEnforceLevels(self.server),
            'say': CommandSay(self.server),
            'restart': CommandRestart(self.server),
            'load_map': CommandLoadMap(self.server),
            'password': CommandPassword(self.server),
            'silent': CommandSilent(self.server, self.chatbot),
            'run': CommandRun(self.server, self.chatbot),
            'length': CommandLength(self.server),
            'difficulty': CommandDifficulty(self.server),
            'game_mode': CommandGameMode(self.server),
            'players': CommandPlayers(self.server, admin_only=False),
            'game': CommandGame(self.server, admin_only=False),
            'map': CommandGameMap(self.server, admin_only=False),
            'help': CommandHelp(self.server, admin_only=False),
            'kills': CommandKills(self.server, admin_only=False),
            'dosh': CommandDosh(self.server, admin_only=False),
            'top_kills': CommandTopKills(self.server, admin_only=False),
            'top_dosh': CommandTopDosh(self.server, admin_only=False),
            'me': CommandMe(self.server, admin_only=False),
            'stats': CommandStats(self.server, admin_only=False),
            'game_time': CommandGameTime(self.server, admin_only=False),
            'server_kills': CommandServerKills(self.server, admin_only=False),
            'server_dosh': CommandServerDosh(self.server, admin_only=False),
        }

        return command_map
