import requests
import re

class Server():
   
    def __init__(self, name, address, username, password):
        self.name = name
        self.address = address
        self.username = username
        self.password = password

        self.session = self.new_session()
        self.motd = self.load_motd()

        self.game = {
            'players_max': 6,
            'map': 'kf-default',
            'round': 0,
            'length': 7,
            'difficulty':'normal'
        }

        self.players = {}

    def __str__(self):
        return "I'm " + self.name + " at " + self.address +\
            ".\nThe admin is " + self.username + " (" + self.password\
            + ").\n" + "The game is currently: " + str(self.game)

    def new_session(self):
        login_url = self.address + "/ServerAdmin/"
        login_payload = {
            'password_hash': self.password,
            'username': self.username,
            'remember': '-1'
        }

        s = requests.Session()

        login_page_response = s.get(login_url)

        token_ex = "token\" value=\"(.*)\" \/"
        mo = re.search(token_ex, login_page_response.text)
        if mo:
            login_payload.update({'token':mo.group(1)})


        login_page_response = s.get(login_url)
        s.post(login_url, data=login_payload)
        
        return s
        
    def load_motd(self):
        motd_f = open(self.name + ".motd")
        motd = motd_f.read()
        motd_f.close()

        return motd.encode("iso-8859-1", "ignore")

