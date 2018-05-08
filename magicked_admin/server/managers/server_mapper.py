import threading
import requests
import time
import datetime
import sys, os

from lxml import html
from lxml.html.clean import Cleaner
from termcolor import colored
from server.player import Player
from utils.logger import logger
from utils.time import seconds_to_hhmmss
from utils.geolocation import get_country

from itertools import groupby

class ServerMapper(threading.Thread):
    """
    This class is responsible for gathering information from the web admin and
    ... other stuffs.
    """
    def __init__(self, server):
        self.server = server
        self.inactive_time_start = datetime.datetime.now()
        self.inactive_time = 0
        self.inactive_timer = False
        self.time_interval = 6
        self.last_wave = 0

        threading.Thread.__init__(self)
        logger.debug("Mapper for " + server.name + " initialised")

    def poll(self):
        info_url = "http://" + self.server.address + \
                   "/ServerAdmin/current/info"
        try:
            info_page_response = self.server.session.post(info_url,
                                                          timeout=2)
        except requests.exceptions.RequestException:
            logger.debug("Couldn't get info page (RequestException)"
                         " on {} sleeping for 5 seconds"
                         .format(self.server.name))
            time.sleep(5)
            return

        info_tree = html.fromstring(info_page_response.content)

        headings, players_table = self.get_current_players(info_tree)
        # This is working but can for sure be done better, look at it later.
        if not players_table and self.inactive_time < 30:
            now = datetime.datetime.now()
            elapsed_time = now - self.inactive_time_start
            self.inactive_time = elapsed_time.total_seconds()
        elif not players_table and self.inactive_time > 30:
            self.server.disable_password()
            # This needs to be reset?
            self.inactive_time_start = datetime.datetime.now()
            self.inactive_time = 0
            self.inactive_timer = False
        else:
            # Restart time if there are players?
            self.inactive_time_start = datetime.datetime.now()

        self.update_players(headings, players_table)
        self.update_game(info_tree)

    def get_current_players(self, info_tree):
        table_head_pat = '//table[@id="players"]//thead//tr//th'
        # Some but not all headers have an <a> for sorting columns
        # that needs to be removed
        cleaner = Cleaner()
        cleaner.remove_tags = ['a']

        headings = []
        required_headings = {'Name', 'Perk', 'Dosh', 'Health',
                             'Kills', 'Ping', 'Admin'}
        for heading in info_tree.xpath(table_head_pat):
            heading = cleaner.clean_html(heading)
            headings += heading.xpath('//th/text()')

        if not required_headings.issubset(set(headings)):
            logger.error("Player is missing columns ({}) on {}"
                         .format(required_headings - set(headings),
                                 self.server.name))

        player_rows_pat = '//table[@id="players"]//tbody//tr'
        player_rows_tree = info_tree.xpath(player_rows_pat)

        players_table = []

        for player_row in player_rows_tree:
            values = []
            for value in player_row:
                if not value.text_content():
                    values += [None]
                else:
                    values += [value.text_content()]

            if values[0] == "There are no players":
                logger.debug("No players on server {}"
                             .format(self.server.name))
            elif len(values) != len(headings):
                logger.warning("Player row ({}) length did not "
                               "match the table length on {}"
                               .format(player_row[headings.index("Name")],
                                       self.server.name))
            else:
                players_table += [values]

        return (headings, players_table)

    def update_players(self, headings, players_table):
        # Remove players that have quit
        for player in self.server.players:
            if player.username not in \
                    [player_row[headings.index("Name")]
                     for player_row in players_table]:
                self.server.player_quit(player)

        for player_row in players_table:
            username = player_row[headings.index("Name")]
            new_perk = player_row[headings.index("Perk")]
            if not new_perk:
                new_perk = "N/A"
            try:
                new_health = int(player_row[headings.index("Health")])
            except TypeError:
                new_health = 0
            new_kills = int(player_row[headings.index("Kills")])
            new_ping = int(player_row[headings.index("Ping")])
            new_dosh = int(player_row[headings.index("Dosh")])

            player = self.server.get_player(username)
            # If the player has just joined, inform the server and skip maths
            if player is None:
                player = Player(username, new_perk)
                player.kills = new_kills
                player.health = new_health
                player.dosh = new_dosh

                detail = self.get_player_details(player.username)
                player.country = detail["country"]
                player.country_code = detail["country_code"]
                player.ip = detail["ip"]
                player.sid = detail["steam_id"]

                self.server.player_join(player)
                continue

            # Players can also have 0 HP while in lobby, do additional checks
            if new_health == 0 and \
                    new_health < player.health and \
                    new_kills > 0:
                message = "Player {} died on {}"\
                    .format(player.username, self.server.name)
                print(colored(message, 'red'))
                player.total_deaths += 1

            player.perk = new_perk
            player.ping = new_ping

            if "Perk Level" in headings:
                player.perk_level = \
                    int(player_row[headings.index("Perk Level")])

            player.total_kills += new_kills - player.kills
            player.wave_kills += new_kills - player.kills
            player.kills = new_kills

            if new_dosh > player.dosh:
                player.wave_dosh += new_dosh - player.dosh
                player.game_dosh += new_dosh - player.dosh
                player.total_dosh += new_dosh - player.dosh
            else:
                player.total_dosh_spent += player.dosh - new_dosh
            player.dosh = new_dosh

            if new_health < player.health:
                player.total_health_lost += player.health - new_health
            player.health = new_health

    def update_game(self, info_tree):
        dds = info_tree.xpath('//dd/text()')

        try:
            z, zr = info_tree.xpath('//dd[@class="gs_wave"]/text()')[0]\
                .split("/")
        except:
            logger.error("Gamemode not supported without additional setup, "
                         "see documentation. Skipping update for {}."
                         .format(self.server.name))
            return
        z, zr = int(z), int(zr)
        if z == zr and z > 1:
            # The if ensures trader_open is only sent once
            if not self.server.trader_time:
                self.server.trader_open()
        else:
            if self.server.trader_time:
                self.server.trader_close()
        self.server.zeds_killed = z
        self.server.zeds_wave = zr

        map_title = info_tree.xpath('//dl//dd/@title')[1]
        map_name = dds[0]
        try:
            wave, length = dds[7].split("/")
            difficulty = dds[8]
        except ValueError:
            wave, length = dds[8].split("/")
            difficulty = dds[9]

        gamemode_pat = '//dl[@id="currentGame"]' \
                       '//dt[contains(text(), "Game type")]' \
                       '/following-sibling::dd/@title'
        gamemode = info_tree.xpath(gamemode_pat)[0]

        if int(wave) < self.last_wave:
            self.server.write_game_map()

        self.server.game.game_map.title = map_title
        self.server.game.game_map.name = map_name
        self.server.game.wave = wave
        self.server.game.length = length
        self.server.game.difficulty = difficulty
        self.server.game.gamemode = gamemode

        if int(wave) < self.last_wave:
            self.server.new_game()
        elif int(wave) > self.last_wave:
            self.server.new_wave()
        self.last_wave = int(wave)

    def get_player_details(self, username):
        response = self.server.session\
            .get("http://{0}/ServerAdmin/current/players"
                 .format(self.server.address))

        player_tree = html.fromstring(response.content)

        odds = player_tree.xpath('//tr[@class="odd"]//td/text()')
        evens = player_tree.xpath('//tr[@class="even"]//td/text()')

        player_rows = odds + evens

        player_rows = [list(group) for k, group in
                       groupby(player_rows, lambda x: x == "\xa0") if not k]

        for player in player_rows:
            if player[0] == username:
                ip = player[2]
                steam_id = player[4]
                country, country_code = get_country(ip)
                return {
                    'steam_id': steam_id,
                    'ip': ip,
                    'country': country,
                    'country_code': country_code
                }

        logger.warning("Couldn't find player details for: {}".format(username))
        return {
            'steam_id': "00000000000000000",
            'ip': "0.0.0.0",
            'country': "Unknown",
            'country_code': "??"
        }


    def run(self):
        while True:
            self.poll()
            time.sleep(self.time_interval)
