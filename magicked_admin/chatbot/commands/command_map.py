import gettext

from .event_commands import *
from .info_commands import *
from .player_commands import *
from .server_commands import *

_ = gettext.gettext


class CommandMap:
    @classmethod
    def get_commands(cls, server, chatbot, motd_updater):
        return {
            # Operator commands
            'lua': CommandLua(server, chatbot),
            'on_join': CommandOnJoin(server),
            'on_time': CommandOnTime(server),
            'on_trader': CommandOnTrader(server),
            'on_death': CommandOnDeath(server),
            'on_wave': CommandOnWave(server),
            'enforce_dosh': CommandEnforceDosh(server),
            'say': CommandSay(server),
            'restart': CommandRestart(server),
            'load_map': CommandLoadMap(server),
            'password': CommandPassword(server),
            'silent': CommandSilent(server, chatbot),
            'run': CommandRun(server, chatbot),
            'length': CommandLength(server),
            'difficulty': CommandDifficulty(server),
            'game_mode': CommandGameMode(server),
            'players': CommandPlayers(server),
            'kick': CommandKick(server),
            'ban': CommandBan(server),
            'op': CommandOp(server),
            'deop': CommandDeop(server),
            'update_motd': CommandUpdateMotd(server, motd_updater),
            'reload_motd': CommandReloadMotd(server, motd_updater),
            'alias': CommandAlias(server, chatbot),

            # Player commands
            'commands': CommandCommands(server),
            'record_wave': CommandHighWave(server),
            'game': CommandGame(server),
            'kills': CommandKills(server),
            'dosh': CommandDosh(server),
            'top_kills': CommandTopKills(server),
            'top_dosh': CommandTopDosh(server),
            'top_time': CommandTopTime(server),
            'top_wave_kills': CommandTopWaveKills(server),
            'top_wave_dosh': CommandTopWaveDosh(server),
            'stats': CommandStats(server),
            'game_time': CommandGameTime(server),
            'server_kills': CommandServerKills(server),
            'server_dosh': CommandServerDosh(server),
            'map': CommandGameMap(server),
            'maps': CommandGameMaps(server),
            'player_count': CommandPlayerCount(server),
            'scoreboard': CommandScoreboard(server)
        }
