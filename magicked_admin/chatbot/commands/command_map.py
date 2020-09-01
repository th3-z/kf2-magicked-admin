import gettext

from .event_commands import *
from .info_commands import *
from .player_commands import *
from .server_commands import *

_ = gettext.gettext


class CommandMap:
    @staticmethod
    def get_commands(server, chatbot, motd_updater):
        return {
            # Operator commands
            _('lua'): CommandLua(server, chatbot),
            ('on_join'): CommandOnJoin(server),
            ('on_time'): CommandOnTime(server),
            ('on_trader'): CommandOnTrader(server),
            ('on_wave'): CommandOnWave(server),
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
            _('update_motd'): CommandUpdateMotd(server, motd_updater),
            _('reload_motd'): CommandReloadMotd(server, motd_updater),
            _('alias'): CommandAlias(server, chatbot),

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
