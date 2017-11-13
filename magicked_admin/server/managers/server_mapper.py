import threading
import time
from itertools import groupby
import datetime

import requests
from lxml import html

from server.player import Player

class ServerMapper(threading.Thread):

    def __init__(self, server):
        self.server = server
        
        self.time_interval = 6
        self.last_wave = 0
        self.exit_flag = threading.Event()

        threading.Thread.__init__(self)
        print("INFO: Mapper for " + server.name + " initialised")

    def run(self):
        info_url = "http://" + self.server.address + "/ServerAdmin/current/info"

        while not self.exit_flag.wait(self.time_interval):
            try:
                info_page_response = self.server.session.post(info_url, timeout=2)
            except requests.exceptions.ConnectionError as e:
                print("INFO: Connection error while reloading web-admin, \
                        retrying in " + str(self.time_interval) + " seconds")
                continue
            except requests.exceptions.Timeout as e:
                print("INFO: Connection timed out while reloading web-admin \
                        retrying in " + str(self.time_interval) + " seconds")
                continue

            info_tree = html.fromstring(info_page_response.content)
            dds = info_tree.xpath('//dd/text()')

            z, zr = info_tree.xpath('//dd[@class="gs_wave"]/text()')[0].split("/")
            z, zr = int(z), int(zr)
            if z == zr and z > 1:
                if self.server.trader_time != True:
                    self.server.trader_open()
            else:
                if self.server.trader_time != False:
                    self.server.trader_close()
            self.server.zeds_killed = z
            self.server.zeds_wave = zr
            
            map_title = info_tree.xpath('//dl//dd/@title')[1]
            map_name = dds[0]
            wave, length = dds[7].split("/")
            difficulty = dds[8]

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

            odds = info_tree.xpath('//tr[@class="odd"]//td/text()')
            evens = info_tree.xpath('//tr[@class="even"]//td/text()')
            player_rows = odds + evens

            # Break them up by the &nbs; between columns
            player_rows = [list(group) for k, group in groupby(player_rows, lambda x: x == "\xa0") if not k]
            # Remove players that have quit
            for player in self.server.players:
                if player.username not in [player_row[0] for player_row in player_rows]:
                    self.server.player_quit(player)

            for player_row in player_rows:
                if len(player_row) < 7:
                    username, new_perk, new_dosh = player_row[:3]
                    new_health = 0
                    new_kills, new_ping = player_row[3:5]
                else:
                    username, new_perk, new_dosh, new_health, \
                    new_kills, new_ping = player_row[:6]
                new_health, new_kills, new_dosh, new_ping = \
                    int(new_health), int(new_kills), int(new_dosh), int(new_ping) 
                player = self.server.get_player(username)
                # New players
                if player == None:
                    player = Player(username, new_perk)
                    player.kills = new_kills
                    player.health = new_health
                    player.dosh = new_dosh
                    self.server.player_join(player)
                    continue

                if new_health == 0 and new_health < player.health and new_kills > 0:
                    print("INFO: Player " + player.username + " died")
                    player.total_deaths += 1
               
                player.perk = new_perk
                player.total_kills += new_kills - player.kills
                player.wave_kills += new_kills - player.kills
                player.wave_dosh += new_dosh - player.dosh
                player.kills = new_kills
                if new_health < player.health:
                    player.total_health_lost += player.health - new_health
                    if player.username == "the_z":
                        print("LOST: " + str(player.health - new_health))
                player.health = new_health
                player.ping = new_ping
                if new_dosh > player.dosh:
                    player.game_dosh += new_dosh - player.dosh
                    player.total_dosh += new_dosh - player.dosh
                    
                else:
                    player.total_dosh_spent += player.dosh - new_dosh
                player.dosh = new_dosh
               
    def terminate(self):
        self.exit_flag.set()

