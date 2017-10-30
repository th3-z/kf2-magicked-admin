import requests
from hashlib import sha1
from lxml import html

from chat import ChatLogger
from server_mapper import ServerMapper

class Server():
   
    def __init__(self, name, address, username, password):
        self.name = name
        self.address = address
        self.username = username
        self.password_hash = "$sha1$" + \
            sha1(password.encode("iso-8859-1","ignore") + \
                username.encode("iso-8859-1","ignore")) \
            .hexdigest()

        self.session = self.new_session()
        self.motd = self.load_motd()

        self.game = {
            'map_title': 'kf-default',
            'map_name': 'kf-default',
            'wave': 0,
            'length': 7,
            'difficulty':'normal'
        }


        self.players = []

        self.chat = ChatLogger(self)
        self.chat.start()

        self.mapper = ServerMapper(self)
        self.mapper.start()

        print("Server " + name + " initialised")

    def __str__(self):
        return "I'm " + self.name + " at " + self.address +\
            ".\nThe admin is " + self.username + ". The game is currently:\n\t" + str(self.game)

    def new_session(self):
        login_url = "http://" + self.address + "/ServerAdmin/"
        login_payload = {
            'password_hash': self.password_hash,
            'username': self.username,
            'password': '',
            'remember': '-1'
        }

        s = requests.Session()

        login_page_response = s.get(login_url)
        login_page_tree = html.fromstring(login_page_response.content)
        
        token = login_page_tree.xpath('//input[@name="token"]/@value')[0]
        login_payload.update({'token':token})

        s.post(login_url, data=login_payload)
        
        return s
        
    def load_motd(self):
        motd_f = open(self.name + ".motd")
        motd = motd_f.read()
        motd_f.close()

        return motd.encode("iso-8859-1", "ignore")

    def event_new_wave(self):
        print("New Wave\n\n")

    def event_new_game(self):
        print("New game\n\n")

