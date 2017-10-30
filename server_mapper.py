import threading
import time

from itertools import groupby
import requests
from lxml import html

from player import Player

class ServerMapper(threading.Thread):

    def __init__(self, server):
        self.server = server
        
        self.time_interval = 20
        self.last_wave = 0

        threading.Thread.__init__(self)

    def run(self):

        info_url = "http://" + self.server.address + "/ServerAdmin/current/info"


        while True:
            info_page_response = self.server.session.post(info_url)
            print(info_page_response.text)

            info_tree = html.fromstring(info_page_response.content)
            dds = info_tree.xpath('//dd/text()')

            map_title = info_tree.xpath('//dl//dd/@title')[1]
            map_name = dds[0]
            wave, length = dds[7].split("/")
            difficulty = dds[8]

            if int(wave) < self.last_wave:
                self.new_game()
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

            for player in players:
                name, perk, dosh, health, kills, ping = player[:6]

                if name not in [player.username for player in self.server.players]:
                    player = Player(
                         name, perk, dosh, health, kills, ping,
                         record_file=self.name + ".players"
                    )

                    self.server.players.append(player)
            

            time.sleep(self.time_interval)

    def update_player(self):
        pass

    def save_player(self, player):
        pass

    def new_game(self):
        print("New game started, saving last game data..")

