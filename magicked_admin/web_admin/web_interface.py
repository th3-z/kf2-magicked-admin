import logging
from hashlib import sha1

import requests
from requests.exceptions import RequestException
from lxml import html
from PySide2.QtCore import QObject, Signal, QThread

from utils.net import resolve_address

logger = logging.getLogger(__name__)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

STATUS_CONNECTED = 0  # 200
STATUS_DISCONNECTED = 1
STATUS_NOT_AUTHORIZED = 2  # 401
STATUS_EXCEEDED_LOGIN_ATTEMPTS = 3  # 403
STATUS_SERVER_ERROR = 4  # 5xx
STATUS_NETWORK_ERROR = 5  # Requests exception
STATUS_NOT_FOUND = 6  # 404

URLS = {
    'login': '{}/ServerAdmin/',
    'chat': '{}/ServerAdmin/current/chat+data',
    'info': '{}/ServerAdmin/current/info',
    'map': '{}/ServerAdmin/current/change',
    'players': '{}/ServerAdmin/current/players',
    'passwords': '{}/ServerAdmin/policy/passwords',
    'bans': '{}/ServerAdmin/policy/bans',
    'game_type': '{}/ServerAdmin/settings/gametypes',
    'maplist': '{}/ServerAdmin/settings/maplist',
    'welcome': '{}/ServerAdmin/settings/welcome',
    'console': '{}/ServerAdmin/console',
    'general_settings': '{}/ServerAdmin/settings/general',
    'players_action': '{}/ServerAdmin/current/players+data'
}

class ConnectWorker(QThread):
    def __init__(self, web_interface):
        super(QThread, self).__init__()
        self.web_interface = web_interface

    def run(self):
        self.web_interface.connect()

    @property
    def result(self):
        return self.web_interface.status


class WebInterfaceSignals(QObject):
    status_change = Signal(int)


class WebInterface(object):
    def __init__(self, address, username, password):
        self.signals = WebInterfaceSignals()

        self.address = address
        self.username = username
        self._password = password
        self._http_auth = False
        self.ma_installed = False

        self._urls = URLS

        self._timeout = 5
        self._status = STATUS_DISCONNECTED
        self.session = None

        self.connect_worker = ConnectWorker(self)
        self.connect_worker.start()

    @classmethod
    def connectivity_test(cls, address, username, password):
        return WebInterface(address, username, password).connect_worker

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        if status == self._status:
            return

        if status == STATUS_CONNECTED:
            logger.info("Connected to {}".format(self.address))
        elif status != STATUS_CONNECTED and self._status == STATUS_CONNECTED:
            logger.info("Lost connection to {}, code: {}".format(self.address, status))
        self._status = status
        self.signals.status_change.emit(status)

    def _get(self, session, url, login=False):
        if not login and self.status != STATUS_CONNECTED:
            return None
        try:
            response = session.get(
                url, timeout=self._timeout, auth=(self.username, self._password) if self._http_auth else None
            )
        except RequestException as err:
            # Connectivity issue
            logger.warning("RequestException getting {}, err: {}".format(url, str(err)))
            self.status = STATUS_NETWORK_ERROR
            return None

        if response.status_code == 401 and not self._http_auth:
            logger.info(
                "Trying HTTP basic auth for ({})".format(url)
            )
            self._http_auth = True
            return self._get(
                session, url, login
            )
        elif response.status_code == 401 and self._http_auth:
            logger.error("Bsic auth credentials rejected ({})".format(url))
            self.status = STATUS_NOT_AUTHORIZED
            self._http_auth = False
            self.session = None
            return None

        if response.status_code == 404:
            self.status = STATUS_NOT_FOUND
            self.session = None
            return None
        if response.status_code >= 500:
            self.status = STATUS_SERVER_ERROR
            return None

        if not login and "hashAlg" in response.text:
            logger.warning("Session expired ({})".format(url))
            self.status = STATUS_NOT_AUTHORIZED
            self.session = None
            return None
        else:
            return response

    def _post(self, session, url, payload, login=False):
        if not login and self.status != STATUS_CONNECTED:
            return None
        try:
            response = session.post(
                url, payload, timeout=self._timeout, auth=(self.username, self._password) if self._http_auth else None
            )
        except RequestException as err:
            # Connectivity issue
            logger.warning("RequestException posting {}, err: {}".format(url, str(err)))
            self.status = STATUS_NETWORK_ERROR
            return None

        if response.status_code == 401 and not self._http_auth:
            logger.info(
                "Trying HTTP basic auth for ({})".format(url)
            )
            self._http_auth = True
            return self._post(
                session, url, payload, login
            )
        elif response.status_code == 401 and self._http_auth:
            logger.error("Bsic auth credentials rejected ({})".format(url))
            self.status = STATUS_NOT_AUTHORIZED
            self._http_auth = False
            self.session = None
            return None

        if response.status_code == 404:
            self.status = STATUS_NOT_FOUND
            self.session = None
            return None
        if response.status_code >= 500:
            self.status = STATUS_SERVER_ERROR
            return None

        if not login and "hashAlg" in response.text:
            logger.warning("Session expired ({})".format(url))
            self.status = STATUS_NOT_AUTHORIZED
            self.session = None
            return None
        else:
            return response

    def connect(self):
        self.address = resolve_address(self.address)
        self._urls = {key: value.format(self.address) for key, value in URLS.items()}

        session = requests.Session()

        login_payload = {
            'password_hash': '',
            'username': self.username,
            'password': '',
            'remember': '-1'
        }

        login_page_response = self._get(session, self._urls['login'], login=True)
        if not login_page_response:
            return

        if self._http_auth:
            self.status = STATUS_CONNECTED
            self.session = session
            return

        if "hashAlg = \"sha1\"" in login_page_response.text:
            hex_dig = "$sha1$" + sha1(
                self._password.encode("iso-8859-1", "ignore")
                + self.username.encode("iso-8859-1", "ignore")
            ).hexdigest()
            login_payload['password_hash'] = hex_dig
        else:
            login_payload['password'] = self._password
            login_payload['password_hash'] = self._password

        login_page_tree = html.fromstring(login_page_response.content)
        token = login_page_tree.xpath("//input[@name='token']/@value")[0]
        login_payload.update({'token': token})

        response = self._post(session, self._urls['login'], login_payload, login=True)
        if not response:
            return
        if "Exceeded login attempts" in response.text:
            self.status = STATUS_EXCEEDED_LOGIN_ATTEMPTS
            return
        elif "hashAlg" in response.text:
            self.status = STATUS_NOT_AUTHORIZED
            return

        self.ma_installed = "<!-- KF2-MA-INSTALLED-FLAG -->" in response.text

        self.session = session
        self.status = STATUS_CONNECTED

    def disconnect(self):
        self.status = STATUS_DISCONNECTED
        self.session = None

    def reconnect(self):
        self.disconnect()
        self.connect_worker = ConnectWorker(self)
        self.connect_worker.start()

    def get_new_messages(self):
        payload = {
            'ajax': '1'
        }

        return self._post(
            self.session,
            self._urls['chat'],
            payload
        )

    def post_message(self, payload):
        return self._post(
            self.session,
            self._urls['chat'],
            payload,
        )

    def get_server_info(self):
        return self._get(
            self.session,
            self._urls['info']
        )

    def get_map(self):
        return self._get(
            self.session,
            self._urls['map']
        )

    def post_map(self, payload):
        return self._post(
            self.session,
            self._urls['map'],
            payload
        )

    def get_players(self):
        return self._get(
            self.session,
            self._urls['players']
        )

    def get_passwords(self):
        return self._get(
            self.session,
            self._urls['passwords']
        )

    def post_passwords(self, payload):
        return self._post(
            self.session,
            self._urls['passwords'],
            payload
        )

    def get_bans(self):
        return self._get(
            self.session,
            self._urls['bans']
        )

    def post_bans(self, payload):
        return self._post(
            self.session,
            self._urls['bans'],
            payload
        )

    def post_players_action(self, payload):
        return self._post(
            self.session,
            self._urls['players_action'],
            payload
        )

    def get_general_settings(self):
        return self._get(
            self.session,
            self._urls['general_settings']
        )

    def post_general_settings(self, payload):
        return self._post(
            self.session,
            self._urls['general_settings'],
            payload
        )

    def get_game_type(self):
        return self._get(
            self.session,
            self._urls['game_type']
        )

    def post_game_type(self, payload):
        return self._post(
            self.session,
            self._urls['game_type'],
            payload
        )

    def get_maplist(self):
        return self._get(
            self.session,
            self._urls['maplist']
        )

    def post_maplist(self, payload):
        return self._post(
            self.session,
            self._urls['maplist'],
            payload
        )

    def get_welcome(self):
        return self._get(
            self.session,
            self._urls['welcome']
        )

    def post_welcome(self, payload):
        return self._post(
            self.session,
            self._urls['welcome'],
            payload
        )

    def post_command(self, payload):
        return self._post(
            self.session,
            self._urls['console'],
            payload
        )

    def get_payload_general_settings(self):
        response = self.get_general_settings()
        if not response:
            return {}

        general_settings_tree = html.fromstring(response.content)

        settings_names = general_settings_tree.xpath('//input/@name')
        settings_vals = general_settings_tree.xpath('//input/@value')

        radio_settings_names = general_settings_tree.xpath(
            '//input[@checked="checked"]/@name'
        )
        radio_settings_vals = general_settings_tree.xpath(
            '//input[@checked="checked"]/@value'
        )

        if self.get_game_type() == "KFGameContent.KFGameInfo_Endless":
            length_val = None
        else:
            length_val = general_settings_tree.xpath(
                '//select[@id="settings_GameLength"]'
                + '//option[@selected="selected"]/@value'
            )[0]

        difficulty_val = general_settings_tree.xpath(
            '//input[@name="settings_GameDifficulty_raw"]/@value'
        )[0]

        settings = {'settings_GameLength': length_val,
                    'settings_GameDifficulty': difficulty_val,
                    'action': 'save'}

        for i, setting_name in enumerate(settings_names):
            settings[setting_name] = settings_vals[i]

        for i, radio_setting_name in enumerate(radio_settings_names):
            settings[radio_setting_name] = radio_settings_vals[i]

        return settings

    def get_payload_motd_settings(self):
        response = self.get_welcome()
        if not response:
            return {}

        motd_tree = html.fromstring(response.content)

        banner_link = motd_tree.xpath('//input[@name="BannerLink"]/@value')[0]
        web_link = motd_tree.xpath('//input[@name="WebLink"]/@value')[0]

        clan_motto = motd_tree.xpath('//textarea[@name="ClanMotto"]/text()')
        clan_motto = clan_motto[0] if clan_motto else ""

        motd = motd_tree.xpath('//textarea[@name="ServerMOTD"]/text()')
        motd = motd[0] if motd else ""

        return {
            'BannerLink': banner_link,
            'ClanMotto': clan_motto,
            'ClanMottoColor': '#FF0000',
            'ServerMOTDColor': '#FF0000',
            'ServerMOTD': motd,
            'WebLink': web_link,
            'WebLinkColor': '#FF0000',
            'liveAdjust': '1',
            'action': 'save'
        }

    def get_payload_map_settings(self):
        response = self.get_map()
        if not response:
            return {}

        map_tree = html.fromstring(response.content)

        game_type_pattern = "//select[@id=\"gametype\"]" \
                            "//option[@selected=\"selected\"]/@value"
        map_pattern = "//select[@id=\"map\"]" \
                      "//option[@selected=\"selected\"]/@value"
        url_extra_pattern = "//input[@id=\"urlextra\"]/@value"
        mutator_count_pattern = "//input[@name=\"mutatorGroupCount\"]/@value"

        game_type = map_tree.xpath(game_type_pattern)[0]
        map_results = map_tree.xpath(map_pattern)[0]
        if len(map_results):
            map_name = map_results[0]
        else:
            logger.warning(
                "Couldn't retrieve map information ({}), please check that your "
                "KFMapSummary section is correctly configured for this map"
                .format(self._urls['map'])
            )
            map_name = "KF-BioticsLab"
        url_extra = map_tree.xpath(url_extra_pattern)[0]
        mutator_count = map_tree.xpath(mutator_count_pattern)[0]

        return {
            "gametype": game_type,
            "map": map_name,
            "mutatorGroupCount": mutator_count,
            "urlextra": url_extra,
            "action": "change"
        }
