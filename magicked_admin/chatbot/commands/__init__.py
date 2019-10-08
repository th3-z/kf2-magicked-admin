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


def get_commands(server, chatbot, scheduler, motd_updater):
    return {
        # Operator commands
        _('start_jc'): CommandStartJoinCommand(server, scheduler),
        _('stop_jc'): CommandStopJoinCommands(server, scheduler),
        _('start_wc'): CommandStartWaveCommand(server, scheduler),
        _('stop_wc'): CommandStopWaveCommands(server, scheduler),
        _('start_tc'): CommandStartTimeCommand(server, scheduler),
        _('stop_tc'): CommandStopTimeCommands(server, scheduler),
        _('start_trc'): CommandStartTraderCommand(server, scheduler),
        _('stop_trc'): CommandStopTraderCommands(server, scheduler),
        _('enforce_dosh'): CommandEnforceDosh(server),
        _('say'): CommandSay(server),
        _('restart'): CommandRestart(server),
        _('load_map'): CommandLoadMap(server),
        _('password'): CommandPassword(server),
        _('silent'): CommandSilent(server, chatbot),
        _('run'): CommandRun(server, chatbot),
        _('marquee'): CommandMarquee(server, chatbot),
        _('length'): CommandLength(server),
        _('difficulty'): CommandDifficulty(server),
        _('game_mode'): CommandGameMode(server),
        _('players'): CommandPlayers(server),
        _('kick'): CommandKick(server),
        _('ban'): CommandBan(server),
        _('op'): CommandOp(server),
        _('deop'): CommandDeop(server),
        _('update_motd'): CommandMarquee(server, motd_updater),
        _('reload_motd'): CommandMarquee(server, motd_updater),

        # Player commands
        _('commands'): CommandCommands(server),
        _('record_wave'): CommandHighWave(server),
        _('game'): CommandGame(server),
        _('kills'): CommandKills(server),
        _('dosh'): CommandDosh(server),
        _('top_kills'): CommandTopKills(server),
        _('top_dosh'): CommandTopDosh(server),
        _('top_time'): CommandTopTime(server),
        _('top_wave_kills'): CommandTopWaveKills(server),
        _('top_wave_dosh'): CommandTopWaveDosh(server),
        _('stats'): CommandStats(server),
        _('game_time'): CommandGameTime(server),
        _('server_kills'): CommandServerKills(server),
        _('server_dosh'): CommandServerDosh(server),
        _('map'): CommandGameMap(server),
        _('maps'): CommandGameMaps(server),
        _('player_count'): CommandPlayerCount(server),
        _('scoreboard'): CommandScoreboard(server),
        _('sb'): CommandScoreboard(server)
    }
