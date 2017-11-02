import threading
import time

from itertools import groupby
import requests
from lxml import html

from player import Player

class ServerMapper(threading.Thread):

    def __init__(self, server):
        self.server = server
        
        self.time_interval = 8
        self.last_wave = 0
        self.exit_flag = threading.Event()


        threading.Thread.__init__(self)
        print("Mapper for " + server.name + " initialised")

    def run(self):

        info_url = "http://" + self.server.address + "/ServerAdmin/current/info"

        while not self.exit_flag.wait(self.time_interval):
            info_page_response = self.server.session.post(info_url)

            info_tree = html.fromstring(info_page_response.content)
            dds = info_tree.xpath('//dd/text()')

            map_title = info_tree.xpath('//dl//dd/@title')[1]
            map_name = dds[0]
            wave, length = dds[7].split("/")
            difficulty = dds[8]

            if int(wave) < self.last_wave:
                self.new_game()
            elif int(wave) > self.last_wave:
                self.new_wave()
            self.last_wave = int(wave)

            self.server.game['map_title'] = map_title
            self.server.game['map_name'] = map_name
            self.server.game['wave'] = wave
            self.server.game['length'] = length
            self.server.game['difficulty'] = difficulty

            odds = info_tree.xpath('//tr[@class="odd"]//td/text()')
            evens = info_tree.xpath('//tr[@class="even"]//td/text()')
            players = odds + evens

            players = [list(group) for k, group in groupby(players, lambda x: x == "\xa0") if not k]

            # Remove players that have quit
            for player in self.server.players:
                print(player)
                if player.username not in [player[0] for player in players]:
                    print("DEBUG: Player " + player.username + " left.")
                    player.save()
                    self.server.players.remove(player)
            print("\n\n")
            # Find any new players
            for player in players:
                name, perk, dosh, health, kills, ping = player[:6]

                if name not in [player.username for player in self.server.players]:
                    player = Player(
                         name, perk, dosh, health, kills, ping,
                         record_file=self.name + ".players"
                    )
                    print("DEBUG: Player " + player.username + " joined.")

                    self.server.players.append(player)

                for player in self.server.players:
                    if player.username == name:
                        player.perk = perk
                        player.kills = kills
                        player.health = health
                        player.ping = ping
                        player.dosh = dosh

    def update_player(self):
        pass

    def save_player(self, player):
        pass

    def new_game(self):
        print("DEBUG: New game started")

    def new_wave(self):
        print("DEBUG: New wave started")

    def terminate(self):
        self.exit_flag.set()

