from chatbot.commands.player_commands import *
from chatbot.commands.info_commands import *
from chatbot.commands.server_commands import *
from chatbot.commands.event_commands import *

class CommandMap():
    
    def __init__(self, server, chatbot):
        self.server = server
        self.chatbot = chatbot
        self.command_map = self.generate_map()

    def generate_map(self):
        wave_event_manager = CommandOnWaveManager(self.server, self.chatbot)
        trader_event_manager = CommandOnTraderManager(self.server, self.chatbot)
        time_event_manager = CommandOnTimeManager(self.server, self.chatbot)
        
        map = {
            'stop_wc':wave_event_manager,
            'start_wc':wave_event_manager,
            'new_wave':wave_event_manager,
            'start_tc':time_event_manager,
            'stop_tc':time_event_manager,
            'start_trc':trader_event_manager,
            'stop_trc':trader_event_manager,
            't_close':trader_event_manager,
            't_open':trader_event_manager,
            'say':CommandSay(self.server),
            'restart':CommandRestart(self.server),
            'toggle_pass':CommandTogglePassword(self.server),
            'silent':CommandSilent(self.server, self.chatbot),
            'length':CommandLength(self.server, adminOnly=False),
            'difficulty':CommandDifficulty(self.server, adminOnly=False),
            'players':CommandPlayers(self.server, adminOnly=False),
            'game':CommandGame(self.server, adminOnly=False),
            'help':CommandHelp(self.server, adminOnly=False),
            'info':CommandInfo(self.server, adminOnly=False),
            'kills':CommandKills(self.server, adminOnly=False),
            'dosh':CommandDosh(self.server, adminOnly=False),
            'top_kills':CommandTopKills(self.server, adminOnly=False),
            'top_dosh':CommandTopDosh(self.server, adminOnly=False),
            'me':CommandMe(self.server, adminOnly=False),
            'stats':CommandStats(self.server, adminOnly=False)
        }
        
        return map