import threading
import time

from utils import DEBUG
from web_admin.constants import *


class GameTracker(threading.Thread):

    def __init__(self, server):
        threading.Thread.__init__(self)

        self.server = server
        self.web_admin = server.web_admin

        self.__exit = False
        # TODO configuration option
        self.__refresh_rate = 20 if DEBUG else 1
        self.__boss_reached = False

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

    def __update_game(self, game_now):
        # Game type specific code
        if game_now.game_type == GAME_TYPE_SURVIVAL:
            self.__update_game_survival(game_now)
        elif game_now.game_type == GAME_TYPE_ENDLESS:
            self.__update_game_survival_vs(game_now)
        elif game_now.game_type == GAME_TYPE_WEEKLY:
            self.__update_game_survival_vs(game_now)
        elif game_now.game_type == GAME_TYPE_SURVIVAL_VS:
            self.__update_game_survival_vs(game_now)

        if game_now.wave and (game_now.wave < self.server.game.wave):
            self.server.event_new_game()

        if game_now.trader_open and not self.server.trader_time:
            self.server.event_trader_open()
        if not game_now.trader_open and self.server.trader_time:
            self.server.event_trader_close()

        self.server.game.game_map.title = game_now.map_title
        self.server.game.game_map.name = game_now.map_name
        self.server.game.wave = game_now.wave
        self.server.game.length = game_now.length
        self.server.game.difficulty = game_now.difficulty
        self.server.game.zeds_dead = game_now.zeds_dead
        self.server.game.zeds_total = game_now.zeds_total
        self.server.game.game_type = game_now.game_type

        if not self.server.trader_time and 0 < int(
                self.server.game.wave) <= int(self.server.game.length):
            now = time.time()
            self.server.game.time += now - self.game_timer
            self.game_timer = time.time()
        else:
            self.game_timer = time.time()

    def __update_game_survival(self, game_now):
        # Boss wave
        if game_now.wave > self.server.game.length:
            # Attempt to identify game over on boss wave
            game_over = True
            for player in self.server.players:
                if player.health and player.kills and player.ping:
                    game_over = False

            if game_over:
                self.server.event_end_game(False)

    def __update_game_endless(self, game_now):
        pass

    def __update_game_weekly(self, game_now):
        pass

    def __update_game_survival_vs(self, game_now):
        pass

    def __update_players(self, players_now):
        # Quitters
        for player in self.server.players:
            if player.username not in [p.username for p in players_now]:
                self.server.event_player_quit(player)

        # Joiners
        for player in players_now:
            if player.username not in \
                    [p.username for p in self.server.players]:
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
            else:
                player.total_dosh_spent += player.dosh - player_now.dosh

            player.kills = player_now.kills
            player.dosh = player_now.dosh
            player.health = player_now.health

            player.update_time()
