from os import path
import threading
import requests

from lxml import html
from utils.text import millify
from utils.text import trim_string

class MotdUpdater(threading.Thread):

    def __init__(self, server):
        self.server = server

        self.time_interval = 8 * 60
        self.motd = self.load_motd()

        self.exit_flag = threading.Event()

        threading.Thread.__init__(self)
    
    def run(self):
        while not self.exit_flag.wait(self.time_interval):
            self.server.write_all_players()
            try:
                motd_payload = self.get_configuration()
            except requests.exceptions.ConnectionError as e:
                continue
            except requests.exceptions.Timeout as e:
                continue

            motd = self.render_motd(self.motd)
            motd_payload['ServerMOTD'] = motd.encode("iso-8859-1", "ignore")

            try:
                self.submit_motd(motd_payload)
            except requests.exceptions.ConnectionError as e:
                continue
            except requests.exceptions.Timeout as e:
                continue
    
    def submit_motd(self, payload):
        motd_url = "http://" + self.server.address + "/ServerAdmin/settings/welcome"

        print("INFO: Updating MOTD")
        try:
            self.server.session.post(motd_url, data=payload)
            self.server.save_settings()
        except requests.exceptions.ConnectionError as e:
            print("INFO: Couldn't submit MOTD (ConnectionError)")
            raise
        except requests.exceptions.Timeout as e:
            print("INFO: Couldn't submit MOTD (Timeout)")
            raise

    def load_motd(self):
        if not path.exists(self.server.name + ".motd"):
            print("WARNING: No motd file for " + self.server.name)
            return ""
 
        motd_f = open(self.server.name + ".motd")
        motd = motd_f.read()
        motd_f.close()
        return motd

    def render_motd(self, src_motd):
        scores = self.server.database.top_kills()

        for player in scores:
            name = player[0].replace("<","")
            name = trim_string(name, 12)
            score = player[1]

            src_motd = src_motd.replace("%PLR", name, 1)
            src_motd = src_motd.replace("%SCR", millify(score), 1)
        
        return src_motd

    def get_configuration(self):
        motd_url = "http://" + self.server.address + "/ServerAdmin/settings/welcome"

        try:
            motd_response = self.server.session.get(motd_url, timeout=2)
        except requests.exceptions.ConnectionError as e:
            print("INFO: Conecttion error in motd updater, could not retrieve configuration")
            raise
        except requests.exceptions.Timeout as e:
            print("INFO: Connection timed out, count not get motd configuration")
            raise

        motd_tree = html.fromstring(motd_response.content)

        banner_link = motd_tree.xpath('//input[@name="BannerLink"]/@value')[0] 
        web_link = motd_tree.xpath('//input[@name="WebLink"]/@value')[0]

        return {
                'BannerLink': banner_link,
                'ClanMotto': '',
                'ClanMottoColor': '#FF0000',
                'ServerMOTDColor': '#FF0000',
                'WebLink': web_link,
                'WebLinkColor': '#FF0000',
                'liveAdjust': '1',
                'action': 'save'
        }
    
    
    def terminate(self):
        self.exit_flag.set()
