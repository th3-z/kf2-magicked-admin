import requests
from hashlib import sha1
from lxml import html

from chat import ChatLogger
from server_mapper import ServerMapper

DIFF_NORM = "0.0000"
DIFF_HARD = "1.0000"
DIFF_SUI = "2.0000"
DIFF_HOE = "4.0000"

LEN_SHORT = "0"
LEN_NORM = "1"
LEN_LONG = "2"

class Server():
   
    def __init__(self, name, address, username, password, hashed=False):
        self.name = name
        self.address = address
        self.username = username
        if hashed:
            self.password_hash = "$sha1$" + \
                sha1(password.encode("iso-8859-1","ignore") + \
                    username.encode("iso-8859-1","ignore")) \
                .hexdigest()
        else:
            self.password_hash = password

        self.session = self.new_session()
        self.motd = self.load_motd()

        self.game = {
            'map_title': 'kf-default',
            'map_name': 'kf-default',
            'wave': 0,
            'length': 7,
            'difficulty':'normal'
        }

        self.general_settings = self.load_general_settings()

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

    def load_general_settings(self):
        settings = {}

        general_settings_url = "http://" + self.address + "/ServerAdmin/settings/general"
        general_settings_response = self.session.get(general_settings_url)
        general_settings_tree = html.fromstring(general_settings_response.content)

        settings_names = general_settings_tree.xpath('//input/@name')
        settings_vals = general_settings_tree.xpath('//input/@value')

        radio_settings_names = general_settings_tree.xpath('//input[@checked="checked"]/@name')
        radio_settings_vals = general_settings_tree.xpath('//input[@checked="checked"]/@value')
        length_val = general_settings_tree.xpath('//select[@id="settings_GameLength"]//option[@selected="selected"]/@value')[0]
        difficulty_val = general_settings_tree.xpath('//input[@name="settings_GameDifficulty_raw"]/@value')[0]
        

        settings['settings_GameLength'] = length_val
        settings['settings_GameDifficulty'] = difficulty_val
        settings['action'] = 'save'

        for i in range(0,len(settings_names)):
            settings[settings_names[i]] = settings_vals[i]

        for i in range(0,len(radio_settings_names)):
            settings[radio_settings_names[i]] = radio_settings_vals[i]

        return settings

    def event_new_wave(self):
        print("New Wave\n\n")

    def event_new_game(self):
        print("New game\n\n")

    def set_difficulty(self, difficulty):
        general_settings_url = "http://" + self.address + "/ServerAdmin/settings/general"

        self.general_settings['settings_GameDifficulty'] = difficulty
        self.general_settings['settings_GameDifficulty_raw'] = difficulty

        self.session.post(general_settings_url, self.general_settings)
        
        self.chat.submit_message("Difficulty change will take effect next game.")
    
    def set_length(self, length):
        general_settings_url = "http://" + self.address + "/ServerAdmin/settings/general"

        self.general_settings['settings_GameLength'] = length

        self.session.post(general_settings_url, self.general_settings)
        
        self.chat.submit_message("Length change will take effect next game.")

    def toggle_game_password(self, password):
        pass

    def set_map(self, map):
        pass

    def close(self):
        self.mapper.terminate()
        self.mapper.join()

        self.chat.terminate()
        self.chat.join()

