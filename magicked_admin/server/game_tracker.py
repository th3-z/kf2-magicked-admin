import gettext
import threading
import time

from colorama import init
from termcolor import colored

from utils import BANNER_URL, warning
from web_admin.constants import *
from database.database import lock

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

        self.game_timer = time.time()

    def run(self):
        while not self.__exit:
            self.__poll()
            time.sleep(self.__refresh_rate)

    def stop(self):
        self.__exit = True

    def __poll(self):
        game_now, players_now = self.web_admin.get_game_players()

        self.__update_players(players_now)
        self.__update_game(game_now)

        lock.acquire(True)
        self.server.database.cur.execute("BEGIN TRANSACTION")
        lock.release()
        self.server.write_all_players()
        self.server.write_game_map()
        lock.acquire(True)
        self.server.database.cur.execute("COMMIT")
        lock.release()

    @staticmethod
    def __is_new_game(game_now, game_before):
        # Skip until a map name is available
        if game_now.map_title == GAME_MAP_TITLE_UNKNOWN:
            return False

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
            map_change = game_before.game_map.title != game_now.map_title
            wave_drop = game_now.wave < (game_before.wave or 0)
            wave_reset = game_before.wave is None or wave_drop

            if map_change or wave_reset:
                new_game = True

        return new_game

    def __update_game(self, game_now):
        new_game = self.__is_new_game(game_now, self.server.game)

        # End previous game before loading next game's info
        if new_game:
            # TODO: Victory detection
            # Skip event until map is initialised
            if self.server.game.game_map.title != GAME_MAP_TITLE_UNKNOWN:
                self.server.event_end_game(False)

        # Trader open/closed
        if game_now.trader_open and not self.server.trader_time:
            # End waves on trader close
            self.server.event_wave_end()
            self.server.event_trader_open()
        if not game_now.trader_open and self.server.trader_time:
            self.server.event_trader_close()

        # Game timer
        if game_now.wave is not None:
            # Not in lobby or boss wave
            is_zed_wave = 0 < game_now.wave <= game_now.length
            if not self.server.trader_time and is_zed_wave:
                now = time.time()
                self.server.game.time += now - self.game_timer
            self.game_timer = time.time()

        self.server.game.game_map.title = game_now.map_title
        self.server.game.game_map.name = game_now.map_name
        self.server.game.wave = game_now.wave
        self.server.game.length = game_now.length
        self.server.game.difficulty = game_now.difficulty

        self.server.game.zeds_dead = game_now.zeds_dead
        self.server.game.zeds_total = game_now.zeds_total
        self.server.game.game_type = game_now.game_type
        self.server.game.players_max = game_now.players_max

        # New game after loading next game's info
        if new_game:
            self.server.event_new_game()
            self.previous_wave = 0

        # And wave start
        if (game_now.wave or 0) > self.previous_wave:
            if self.server.game.wave > 0:
                self.server.event_wave_start()
            self.previous_wave = self.server.game.wave

    def __survival_boss_defeat(self):
        game_over = True

        for player in self.server.players:
            if player.health and player.kills and player.ping:
                game_over = False

        return game_over

    def __update_players(self, players_now):
        # Quitters
        for player in self.server.players:
            if player.username not in [p.username for p in players_now]:
                self.server.event_player_quit(player)

        # Joiners
        for player in players_now:
            if player.username not in \
                    [p.username for p in self.server.players]:

                # Filter pawns in KF-SantasWorkshop
                if "KFAIController" not in player.username:
                    self.server.event_player_join(player)

        for player in self.server.players:
            try:
                player_now = next(filter(
                    lambda p: p.username == player.username, players_now
                ))
            except StopIteration:
                self.server.players = []
                return

            player.ping = player_now.ping

            player.perk = player_now.perk
            player.total_kills += player_now.kills - player.kills

            player.wave_kills += player_now.kills - player.kills
            player.wave_dosh += player_now.dosh - player.dosh

            if not player_now.health and player_now.health < player.health:
                self.server.event_player_death(player)

            if player_now.dosh > player.dosh:
                player.game_dosh += player_now.dosh - player.dosh
                player.total_dosh += player_now.dosh - player.dosh

            player.kills = player_now.kills
            player.dosh = player_now.dosh
            player.health = player_now.health

            player.update_time()
