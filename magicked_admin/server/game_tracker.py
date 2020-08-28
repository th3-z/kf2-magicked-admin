import gettext
import threading
import time

from colorama import init
from termcolor import colored

from utils import BANNER_URL, warning
from server.level import Level
from server.match import Match

_ = gettext.gettext
init()


class GameTracker(threading.Thread):
    def __init__(self, server, refresh_rate=1):
        threading.Thread.__init__(self)

        self.server = server
        self.web_admin = server.web_admin

        self._exit = False
        self._refresh_rate = refresh_rate

        self.previous_time = time.time()

    def run(self):
        while not self._exit:
            self._poll()
            time.sleep(self._refresh_rate)

    def close(self):
        self._exit = True

    def _poll(self):
        match_now, players_now = self.web_admin.get_server_info()
        self._update_match(match_now)
        self._update_players(players_now)

    @staticmethod
    def _is_new_match(match_now, match_before):
        # Uninitialized match
        if not match_before:
            return True

        new_match = False
        # An unsupported game types wont have a wave counter
        if match_now.wave is None:
            # Initial mode change
            if match_before.game_type != match_now.game_type:
                message = (_("Game type ({}) support not installed, please "
                             "patch your webadmin to correct this! Guidance is"
                             " available at: {}"))
                warning(message.format(
                    match_now.game_type, colored(BANNER_URL, 'magenta')
                ))

                # This new match is the last that will be detected because it
                # depends on the wave counter being present
                new_match = True

        # Supported mode always has a valid wave, try to detect a match change
        else:
            map_change = match_before.level.title != match_now.map_title
            wave_drop = match_now.wave < (match_before.wave or 0)
            wave_reset = match_before.wave is None or wave_drop

            if map_change or wave_reset:
                new_match = True

        return new_match

    def _update_match(self, match_now):
        new_match = self._is_new_match(match_now, self.server.match)

        # End current match unless its the first one
        if new_match and self.server.match:
            self.server.event_match_end()

        # Start next match
        if new_match:
            new_level = Level(match_now.map_title, match_now.map_name)
            new_match = Match(
                new_level, match_now.game_type, match_now.difficulty,
                match_now.length
            )
            self.server.match = new_match
            self.server.event_match_start()

        new_wave = match_now.wave > self.server.match.wave

        # Trader open/close
        if match_now.trader_open and not self.server.match.trader_time:
            # Waves are considered over once the trader opens
            self.server.event_wave_end()
            self.server.match.trader_time = True
            self.server.event_trader_open()
        if not match_now.trader_open and self.server.match.trader_time:
            # Wave start is further down so the new wave data is available
            self.server.match.trader_time = False
            self.server.event_trader_close()

        # Start time at wave 1, wave 0 is lobby
        if match_now.wave and not self.server.match.start_date:
            self.server.match.start_date = time.time()

        self.server.match.wave = match_now.wave
        self.server.match.zeds_dead = match_now.zeds_dead
        self.server.match.zeds_total = match_now.zeds_total
        self.server.capacity = match_now.players_max

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

            player.update_session()
