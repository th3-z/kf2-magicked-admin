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
        map = {
            'stop_wc':CommandOnWaveManager(self.server, self.chatbot),
            'start_wc':CommandOnWaveManager(self.server, self.chatbot),
            'new_wave':CommandOnWaveManager(self.server, self.chatbot),
            'start_tc':CommandOnTimeManager(self.server, self.chatbot),
            'stop_tc':CommandOnTimeManager(self.server, self.chatbot),
            'start_trc':CommandOnTraderManager(self.server, self.chatbot),
            'stop_trc':CommandOnTraderManager(self.server, self.chatbot),
            'say':CommandSay(self.server),
            'restart':CommandRestart(self.server),
            'toggle_pass':CommandTogglePassword(self.server),
            'silent':CommandSilent(self.server, self.chatbot),
            'length':CommandLength(self.server, adminOnly=False),
            'difficulty':CommandDifficulty(self.server, adminOnly=False),
            'players':CommandPlayers(self.server, adminOnly=False),
            'game':CommandGame(self.server, adminOnly=False),
            'help':CommandHelp(self.server, adminOnly=False),
            'kills':CommandKills(self.server, adminOnly=False),
            'dosh':CommandDosh(self.server, adminOnly=False),
            'top_kills':CommandTopKills(self.server, adminOnly=False),
            'top_dosh':CommandTopDosh(self.server, adminOnly=False)
        }
        
        return map
