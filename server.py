import requests
from hashlib import sha1
from lxml import html

from chat import ChatLogger
from server_mapper import ServerMapper

DIFF_NORM = "0.0000"
DIFF_HARD = "1.0000"
DIFF_SUI = "2.0000"
DIFF_HOE = "4.0000"

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

        """self.general_settings_payload = {
            settings_bUsedForTakeover:"0"
            settings_ServerName:"+!=UK=!+Killing+Floor+2+--+CUSTOM+MAPS++--+High+tick+server"
            settings_MaxIdleTime:"0.0000"
            settings_MaxPlayers:"6"
            settings_bAntiCheatProtected:"1"
            settings_GameDifficulty:"0.0000"
            settings_GameDifficulty_raw:"0.000000"
            settings_GameLength:"1"
            settings_bDisableTeamCollision:"1"
            settings_bAdminCanPause:"1"
            settings_bSilentAdminLogin:"1"
            settings_bDisableMapVote:"0"
            settings_MapVoteDuration:"60.0000"
            settings_bDisableKickVote:"1"
            settings_bDisableKickVote:"1"
            settings_MapVotePercentage:"0.0000"
            settings_KickVotePercentage:"0.6600"
            settings_bDisablePublicTextChat:"0"
            settings_bPartitionSpectators:"0"
            settings_bDisableVOIP:"0"
            liveAdjust:"1"
            action:"save"
        }"""


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

    def set_difficulty(self, difficulty):
       pass 

