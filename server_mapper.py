import threading
import time

import requests
from lxml import html

from itertools import groupby

class ServerMapper(threading.Thread):

    def __init__(self, server):
        self.server = server
        
        self.time_interval = 20

        threading.Thread.__init__(self)

    def run(self):

        info_url = "http://" + self.server.address + "/ServerAdmin/current/info"


        while True:
            info_page_response = self.server.session.post(info_url)

            info_tree = html.fromstring(info_page_response.content)
            dds = info_tree.xpath('//dd/text()')

            #map_title = info_tree.xpath('//dd[starts-with(@title,\'kf\')]/@title')[0]
            map_name = dds[0]
            wave, length = dds[7].split("/")
            difficulty = dds[8]

            print("name: " + map_name + " wave: " + wave + " len: " + length + "diff: " + difficulty)
           
            odds = info_tree.xpath('//tr[@class="odd"]//td/text()')
            evens = info_tree.xpath('//tr[@class="even"]//td/text()')
            players = odds + evens

            players = [list(group) for k, group in groupby(players, lambda x: x == "\xa0") if not k]
            
            self.server.players = players
            self.server.game = [map_name, wave, length, difficulty]

            #print(str(dts))
            #print(str(dds))
            time.sleep(self.time_interval)


    def load_player(self):
        pass

    def update_player(self):
        pass

    def save_player(self):
        pass

