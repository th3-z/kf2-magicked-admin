import gettext
import threading
import time

from colorama import init
from termcolor import colored

from utils import BANNER_URL, warning, DEBUG
from server.level import Level
from server.match import Match

_ = gettext.gettext
init()


class GameTracker(threading.Thread):
    def __init__(self, server, refresh_rate=1):
        threading.Thread.__init__(self)

        self.server = server
        self.web_admin = server.web_admin

        self.__exit = False
        self.__refresh_rate = refresh_rate
        self.__boss_reached = False

        self.previous_wave = 0
        self.previous_time = time.time()

    def run(self):
        while not self.__exit:
            self._poll()
            time.sleep(self.__refresh_rate)

    def close(self):
        self.__exit = True

    def _poll(self):
        game_now, players_now = self.web_admin.get_game_players()
        self._update_game(game_now)
        self._update_players(players_now)

    @staticmethod
    def _is_new_game(game_now, game_before):
        # Uninitialized
        if not game_before:
            return True

        new_game = False
        # An unsupported game mode wont have a wave counter
        if game_now.wave is None:
            # Initial mode change
            if game_before.game_type != game_now.game_type:
                message = (_("Game type ({}) support not installed, please "
                             "patch your webadmin to correct this! Guidance is"
                             " available at: {}"))
                warning(message.format(
                    game_now.game_type, colored(BANNER_URL, 'magenta')
                ))

                # This new game is the last that will be detected because it
                # depends on the wave counter being present
                new_game = True

        # Supported mode always has a valid wave, try to detect a game change
        else:
            map_change = game_before.level.title != game_now.map_title
            wave_drop = game_now.wave < (game_before.wave or 0)
            wave_reset = game_before.wave is None or wave_drop

            if map_change or wave_reset:
                new_game = True

        return new_game

    def _update_game(self, game_now):
        new_game = self._is_new_game(game_now, self.server.match)

        # End current game
        if new_game:
            # Don't end the game if it wasn't initialized
            if self.server.match:
                self.server.event_match_end()

        # Start next game
        if new_game:
            new_level = Level(game_now.map_title, game_now.map_name)
            new_match = Match(
                new_level, game_now.game_type, game_now.difficulty,
                game_now.length
            )
            self.server.match = new_match
            self.server.event_match_start()

        new_wave = not self.server.match or game_now.wave > self.server.match.wave

        # Trader open/closed
        if game_now.trader_open and not self.server.match.trader_time:
            # Waves are considered over once the trader opens
            self.server.event_wave_end()
            self.server.event_trader_open()
        if not game_now.trader_open and self.server.match.trader_time:
            # Wave start is further down
            self.server.event_trader_close()

        # Start time at wave 1, wave 0 is lobby
        if game_now.wave and not self.server.match.start_date:
            self.server.match.start_date = time.time()

        self.server.match.wave = game_now.wave
        self.server.match.zeds_dead = game_now.zeds_dead
        self.server.match.zeds_total = game_now.zeds_total
        self.server.capacity = game_now.players_max

        if new_wave:
            self.server.event_wave_start()

    def _update_players(self, players_now):
        # Quitters
        for player in self.server.players:
            if player.username not in [p.username for p in players_now]:
                self.server.event_player_quit(player)

        # Joiners
        for player in players_now:
            if player.username not in \
                    [p.username for p in self.server.players]:
                # Filter pawns
                if "KFAIController" not in player.username:
                    self.server.event_player_join(player)

        # Update player models
        for player in self.server.players:
            try:
                player_now = next(filter(
                    lambda p: p.username == player.username, players_now
                ))
            except StopIteration:  # players_now empty
                self.server.players = []
                return

            player.session_kills += player_now.kills - player.kills
            player.session_dosh += max(player_now.dosh - player.dosh, 0)
            player.session_dosh_spent += max(player.dosh - player_now.dosh, 0)
            player.session_damage_taken += max(player.health - player_now.health, 0)

            player.wave_kills += player_now.kills - player.kills
            player.wave_dosh += max(player_now.dosh - player.dosh, 0)
            player.wave_dosh_spent += max(player.dosh - player_now.dosh, 0)
            player.wave_damage_taken += max(player.health - player_now.health, 0)

            if not player_now.health and player_now.health < player.health:
                player.session_deaths += 1
                player.wave_deaths += 1
                self.server.event_player_death(player)

            player.kills = player_now.kills
            player.dosh = player_now.dosh
            player.health = player_now.health
            player.ping = player_now.ping
            player.perk = player_now.perk

            # TODO: Move this
            if DEBUG:
                player.update_session()
