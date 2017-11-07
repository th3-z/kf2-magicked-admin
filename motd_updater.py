from os import path
import threading
import math
import requests

from lxml import html

class MotdUpdater(threading.Thread):

    def __init__(self, server):
        self.server = server

        self.time_interval = 8 * 60
        self.motd = self.load_motd()

        self.exit_flag = threading.Event()

        threading.Thread.__init__(self)
    
    def run(self):
        while not self.exit_flag.wait(self.time_interval):
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

        print("INFO: Submitting motd")
        try:
            self.server.session.post(motd_url, data=payload)
        except requests.exceptions.ConnectionError as e:
            print("INFO: Connection error while submitting motd")
            raise
        except requests.exceptions.Timeout as e:
            print("INFO: Connection timed out while submitting motd")
            raise

    def millify(self,n):
        millnames = ['','K','M','B','T']
        
        n = float(n)
        millidx = max(0,min(len(millnames)-1,
            int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

        return '{:.0f}{}'.format(n / 10**(3 * millidx), millnames[millidx])
        
    def load_motd(self):
        if not path.exists(self.server.name + ".motd"):
            print("WARNING: No motd file for " + self.server.name)
            return ""
 
        motd_f = open(self.server.name + ".motd")
        motd = motd_f.read()
        motd_f.close()
        return motd

    def render_motd(self, src_motd):
        name_len = 11

        scores = self.server.database.top_kills()

        for player in scores:
            name = player[0]
            name = (name[:name_len-2] + '..') if len(name) > name_len else name
            score = player[1]

            src_motd = src_motd.replace("%PLR", name, 1)
            src_motd = src_motd.replace("%SCR", self.millify(score), 1)
        
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
