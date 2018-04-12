import threading
import requests
import time
import logging

from lxml import html
from lxml.html.clean import Cleaner

from server.player import Player

logger = logging.getLogger(__name__)
if __debug__:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)


class ServerMapper(threading.Thread):
    def __init__(self, server):
        self.server = server

        self.time_interval = 6
        self.last_wave = 0

        threading.Thread.__init__(self)
        logging.info("INFO: Mapper for " + server.name + " initialised")

    def run(self):
        info_url = "http://" + self.server.address + \
                   "/ServerAdmin/current/info"

        while True:
            try:
                info_page_response = self.server.session.post(info_url,
                                                              timeout=2)
            except requests.exceptions.RequestException:
                logging.debug("Couldn't get info page (RequestException)"
                              " on {} sleeping for 5 seconds"
                              .format(self.server.name))
                time.sleep(5)
                continue

            # Look into this encoding, pages are encoded in Windows 1252.
            info_tree = html.fromstring(info_page_response.content
                                        .decode('cp1252'))
            dds = info_tree.xpath('//dd/text()')

            z, zr = info_tree.xpath('//dd[@class="gs_wave"]/text()')[0]\
                .split("/")
            z, zr = int(z), int(zr)
            if z == zr and z > 1:
                # The if ensures
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

            self.server.game['map_title'] = map_title
            self.server.game['map_name'] = map_name
            self.server.game['wave'] = wave
            self.server.game['length'] = length
            self.server.game['difficulty'] = difficulty

            if int(wave) < self.last_wave:
                self.server.new_game()
            elif int(wave) > self.last_wave:
                self.server.new_wave()
            self.last_wave = int(wave)

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
                logging.error("Player is missing columns ({}) on {}"
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
                    logging.warning("Player row ({}) length did not "
                                    "match the table length on {}"
                                    .format(player_row[headings.index("Name")],
                                            self.server.name))
                else:
                    players_table += [values]

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
                    logger.debug("Null perk for {} on: ()".format(
                        player_row[headings.index("Name")]),
                        self.server.name)
                    new_perk = "N/A"
                try:
                    new_health = int(player_row[headings.index("Health")])
                except TypeError:
                    logger.debug("DEBUG: Null health on: " + player_row[headings.index("Name")])
                    new_health = 0
                new_kills = int(player_row[headings.index("Kills")])
                new_ping = int(player_row[headings.index("Ping")])
                new_dosh = int(player_row[headings.index("Dosh")])

                player = self.server.get_player(username)
                # New players
                if player is None:
                    player = Player(username, new_perk)
                    player.kills = new_kills
                    player.health = new_health
                    player.dosh = new_dosh
                    self.server.player_join(player)
                    continue

                if new_health == 0 and \
                        new_health < player.health and \
                        new_kills > 0:
                    logger.info("Player " + player.username + " died on {}"
                                .format(self.server.name))
                    player.total_deaths += 1

                player.perk = new_perk
                player.total_kills += new_kills - player.kills
                player.wave_kills += new_kills - player.kills
                player.wave_dosh += new_dosh - player.dosh
                player.kills = new_kills
                if new_health < player.health:
                    player.total_health_lost += player.health - new_health
                player.health = new_health
                player.ping = new_ping
                if new_dosh > player.dosh:
                    player.game_dosh += new_dosh - player.dosh
                    player.total_dosh += new_dosh - player.dosh

                else:
                    player.total_dosh_spent += player.dosh - new_dosh
                player.dosh = new_dosh

            time.sleep(self.time_interval)
