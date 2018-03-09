from os import path
import threading
import requests

from lxml import html
from utils.text import millify
from utils.text import trim_string

class MotdUpdater(threading.Thread):

    def __init__(self, server, scoreboard_type):
        self.server = server

        self.scoreboard_type = scoreboard_type
        self.time_interval = 5 * 60
        self.motd = self.load_motd()

        self.exit_flag = threading.Event()

        threading.Thread.__init__(self)
    
    def run(self):
        while not self.exit_flag.wait(self.time_interval):
            self.server.write_all_players()
            try:
                motd_payload = self.get_configuration()
            except requests.exceptions.RequestException as e:
                continue

            motd = self.render_motd(self.motd)
            motd_payload['ServerMOTD'] = motd.encode("iso-8859-1", "ignore")

            try:
                self.submit_motd(motd_payload)
            except requests.exceptions.RequestException as e:
                continue
                
    def submit_motd(self, payload):
        motd_url = "http://" + self.server.address + "/ServerAdmin/settings/welcome"

        print("INFO: Updating MOTD")
        try:
            self.server.session.post(motd_url, data=payload)
            self.server.save_settings()
        except requests.exceptions.RequestException as e:
            print("INFO: Couldn't submit motd (RequestException)")
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
        if self.scoreboard_type in ['kills','Kills','kill','Kill']:
            scores = self.server.database.top_kills()
        elif self.scoreboard_type in ['Dosh','dosh']:
            scores = self.server.database.top_dosh()
        else:
            print("ERROR: Bad configuration, scoreboard_type. Options are: dosh, kills")
            return

        for player in scores:
            name = player[0].replace("<","&lt;")
            name = trim_string(name, 12)
            score = player[1]

            src_motd = src_motd.replace("%PLR", name, 1)
            src_motd = src_motd.replace("%SCR", millify(score), 1)
        
        return src_motd

    def get_configuration(self):
        motd_url = "http://" + self.server.address + "/ServerAdmin/settings/welcome"

        try:
            motd_response = self.server.session.get(motd_url, timeout=2)
        except requests.exceptions.RequestException as e:
            print("INFO: Couldn't get motd config(RequestException)")
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
