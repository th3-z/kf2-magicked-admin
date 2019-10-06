import gettext

from chatbot.commands.event_commands import *
from chatbot.commands.info_commands import *
from chatbot.commands.player_commands import *
from chatbot.commands.server_commands import *

_ = gettext.gettext

# Internal command definitions
COMMAND_NEW_WAVE = "new_wave"  # Params: wave number
COMMAND_NEW_GAME = "new_game"
COMMAND_PLAYER_JOIN = "player_join"  # Params: username
COMMAND_TRADER_OPEN = "t_open"
COMMAND_TRADER_CLOSE = "t_close"


class CommandMap:
    def __init__(self, server, chatbot):
        self.server = server
        self.chatbot = chatbot
        self.command_map = self.generate_map()

    def generate_map(self):
        scheduler = self.chatbot.scheduler

        command_map = {
            # Operator commands
            _('start_jc'): CommandStartJoinCommand(self.server, scheduler),
            _('stop_jc'): CommandStopJoinCommands(self.server, scheduler),
            _('start_wc'): CommandStartWaveCommand(self.server, scheduler),
            _('stop_wc'): CommandStopWaveCommands(self.server, scheduler),
            _('start_tc'): CommandStartTimeCommand(self.server, scheduler),
            _('stop_tc'): CommandStopTimeCommands(self.server, scheduler),
            _('start_trc'): CommandStartTraderCommand(self.server, scheduler),
            _('stop_trc'): CommandStopTraderCommands(self.server, scheduler),
            _('enforce_dosh'): CommandEnforceDosh(self.server),
            _('say'): CommandSay(self.server),
            _('restart'): CommandRestart(self.server),
            _('load_map'): CommandLoadMap(self.server),
            _('password'): CommandPassword(self.server),
            _('silent'): CommandSilent(self.server, self.chatbot),
            _('run'): CommandRun(self.server, self.chatbot),
            _('length'): CommandLength(self.server),
            _('difficulty'): CommandDifficulty(self.server),
            _('game_mode'): CommandGameMode(self.server),
            _('players'): CommandPlayers(self.server),
            _('kick'): CommandKick(self.server),
            _('ban'): CommandBan(self.server),
            _('op'): CommandOp(self.server),
            _('deop'): CommandDeop(self.server),
            _('marquee'): CommandMarquee(self.server, self.chatbot),

            # Player commands
            _('commands'): CommandCommands(self.server),
            _('record_wave'): CommandHighWave(self.server),
            _('game'): CommandGame(self.server),
            _('kills'): CommandKills(self.server),
            _('dosh'): CommandDosh(self.server),
            _('top_kills'): CommandTopKills(self.server),
            _('top_dosh'): CommandTopDosh(self.server),
            _('top_time'): CommandTopTime(self.server),
            _('top_wave_kills'): CommandTopWaveKills(self.server),
            _('top_wave_dosh'): CommandTopWaveDosh(self.server),
            _('stats'): CommandStats(self.server),
            _('game_time'): CommandGameTime(self.server),
            _('server_kills'): CommandServerKills(self.server),
            _('server_dosh'): CommandServerDosh(self.server),
            _('map'): CommandGameMap(self.server),
            _('maps'): CommandGameMaps(self.server),
            _('player_count'): CommandPlayerCount(self.server),
            _('scoreboard'): CommandScoreboard(self.server),
            _('sb'): CommandScoreboard(self.server)
        }

        return command_map
