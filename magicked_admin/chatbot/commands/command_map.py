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
        wave_event_manager = CommandOnWaveManager(
            self.server, self.chatbot
        )
        trader_event_manager = CommandOnTraderManager(
            self.server, self.chatbot
        )
        time_event_manager = CommandOnTimeManager(
            self.server, self.chatbot
        )

        command_map = {
            'player_join': CommandGreeter(self.server),
            'stop_wc': wave_event_manager,
            'start_wc': wave_event_manager,
            'new_wave': wave_event_manager,
            'start_tc': time_event_manager,
            'stop_tc': time_event_manager,
            'start_trc': trader_event_manager,
            'stop_trc': trader_event_manager,
            't_close': trader_event_manager,
            't_open': trader_event_manager,
            'record_wave': CommandHighWave(self.server),
            'enforce_levels': CommandEnforceLevels(self.server),
            'enforce_dosh': CommandEnforceDosh(self.server),
            'say': CommandSay(self.server),
            'restart': CommandRestart(self.server),
            'load_map': CommandLoadMap(self.server),
            'password': CommandPassword(self.server),
            'silent': CommandSilent(self.server, self.chatbot),
            'run': CommandRun(self.server, self.chatbot),
            'length': CommandLength(self.server),
            'difficulty': CommandDifficulty(self.server),
            'game_mode': CommandGameMode(self.server),
            'players': CommandPlayers(self.server),
            'game': CommandGame(self.server),
            'help': CommandHelp(self.server),
            'kills': CommandKills(self.server),
            'kick': CommandKick(self.server),
            'ban': CommandBan(self.server),
            'dosh': CommandDosh(self.server),
            'top_kills': CommandTopKills(self.server),
            'top_dosh': CommandTopDosh(self.server),
            'top_time': CommandTopTime(self.server),
            'top_wave_kills': CommandTopWaveKills(self.server),
            'top_wave_dosh': CommandTopWaveDosh(self.server),
            'stats': CommandStats(self.server),
            'game_time': CommandGameTime(self.server),
            'server_kills': CommandServerKills(self.server),
            'server_dosh': CommandServerDosh(self.server),
            'op': CommandOp(self.server),
            'deop': CommandOp(self.server),
            'map': CommandGameMap(self.server),
            'maps': CommandGameMap(self.server),
            'lps': CommandLpsTest(self.server, self.chatbot),
            'player_count': CommandPlayerCount(self.server),
        }

        return command_map
