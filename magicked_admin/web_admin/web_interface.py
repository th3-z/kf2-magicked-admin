import logging
import time
from hashlib import sha1

import requests
from lxml import html

logger = logging.getLogger(__name__)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

class AuthorizationException(Exception):
    pass


class WebInterface(object):
    def __init__(self, address, username, password, server_name="unnamed"):
        self._address = address
        self._username = username
        self._password = password
        self._http_auth = False

        self.server_name = server_name
        self.ma_installed = False

        self._urls = {
            'login': '{}/ServerAdmin/'.format(address),
            'chat': '{}/ServerAdmin/current/chat+data'.format(address),
            'info': '{}/ServerAdmin/current/info'.format(address),
            'map': '{}/ServerAdmin/current/change'.format(address),
            'players': '{}/ServerAdmin/current/players'.format(address),
            'passwords': '{}/ServerAdmin/policy/passwords'.format(address),
            'bans': '{}/ServerAdmin/policy/bans'.format(address),
            'game_type': '{}/ServerAdmin/settings/gametypes'.format(address),
            'maplist': '{}/ServerAdmin/settings/maplist'.format(address),
            'welcome': '{}/ServerAdmin/settings/welcome'.format(address),
            'console': '{}/ServerAdmin/console'.format(address),
            'general_settings': '{}/ServerAdmin/settings/general'.format(
                address
            ),
            'players_action': '{}/ServerAdmin/current/players+data'.format(
                address
            )
        }

        self._timeout = 5

        # Setter event, disconnected
        self._sleeping = False

        self._session = self._new_session()

        # Event, connected
        logger.info("Connected to {} ({})".format(server_name, address))

    def _get(self, session, url, retry_interval=6, login=False):
        while True:
            try:
                if not self._http_auth:
                    response = session.get(url, timeout=self._timeout)
                else:
                    response = session.get(
                        url,
                        timeout=self._timeout,
                        auth=(self._username, self._password)
                    )

                if response.status_code > 401:
                    # Down/unavailable
                    self._sleep()
                    time.sleep(retry_interval)
                    continue
                else:
                    self._wake()

                if response.status_code == 401 and not self._http_auth:
                    logger.info(
                        "Trying to login with basic auth for '{}'".format(self.server_name)
                    )
                    self._http_auth = True
                    return self._get(
                        session, url, retry_interval, login
                    )
                elif response.status_code == 401 and self._http_auth:
                    # Dead, bad creds
                    logger.error("{}'s credentials were rejected".format(self.server_name))
                    raise AuthorizationException

                if not login:
                    if "hashAlg" in response.text:
                        logger.warning("{}'s session expired, attempting to renew".format(self.server_name))
                        try:
                            self._session = self._new_session()
                        except AuthorizationException:
                            logger.error("Couldn't renew session for '{}'".format(self.server_name))
                            # Dead, bad creds
                            """die(
                                _("Authorization error, credentials changed?"),
                                pause=True
                            )"""

                    else:
                        return response
                else:
                    return response

            except requests.exceptions.HTTPError:
                logger.warning("HTTPError getting {}. Retrying in {}s"
                               .format(url, retry_interval))
            except requests.exceptions.ConnectionError:
                logger.warning("ConnectionError getting {}. Retrying in {}s"
                               .format(url, retry_interval))
            except requests.exceptions.Timeout:
                logger.warning("Timeout getting {}. Retrying in {}s"
                               .format(url, retry_interval))
            except requests.exceptions.RequestException as err:
                logger.warning("None-specific RequestException getting {}, "
                               "{}. Retrying in {}s"
                               .format(url, str(err), retry_interval))

            time.sleep(retry_interval)

    def _post(self, session, url, payload, retry_interval=6, login=False):
        while True:
            try:
                if not self._http_auth:
                    response = session.post(
                        url, payload,
                        timeout=self._timeout
                    )
                else:
                    response = session.post(
                        url, payload,
                        timeout=self._timeout,
                        auth=(self._username, self._password)
                    )

                if response.status_code > 401:
                    self._sleep()
                    time.sleep(retry_interval)
                    continue
                else:
                    self._wake()

                if response.status_code == 401 and not self._http_auth:
                    logger.info(
                        "Trying to login with basic auth for '{}'".format(self.server_name)
                    )
                    self._http_auth = True
                    return self._post(
                        session, url, payload, retry_interval, login
                    )
                elif response.status_code == 401 and self._http_auth:
                    logger.error("{}'s credentials were rejected".format(self.server_name))
                    raise AuthorizationException

                if not login:
                    if "hashAlg" in response.text:
                        logger.warning("{}'s session expired, attempting to renew".format(self.server_name))
                        try:
                            self._session = self._new_session()
                        except AuthorizationException:
                            logger.error("Couldn't renew session for '{}'".format(self.server_name))
                            # Dead
                            """die(
                                _("Authorization error, credentials changed?"),
                                pause=True
                            )"""
                else:
                    return response
                return response

            except requests.exceptions.HTTPError:
                logger.warning("HTTPError getting {}. Retrying in {}s"
                               .format(url, retry_interval))
            except requests.exceptions.ConnectionError:
                logger.warning("ConnectionError getting {}. Retrying in {}s"
                               .format(url, retry_interval))
            except requests.exceptions.Timeout:
                logger.warning("Timeout getting {}. Retrying in {}s"
                               .format(url, retry_interval))
            except requests.exceptions.RequestException as err:
                logger.warning("None-specific RequestException getting {}, "
                               "{}. Retrying in {}s"
                               .format(url, str(err), retry_interval))

            time.sleep(retry_interval)

    def _sleep(self):
        if not self._sleeping:
            logger.info("{}'s web admin not responding, sleeping".format(self.server_name))
            self._sleeping = True

    def _wake(self):
        if self._sleeping:
            logger.info("{}'s web admin is back, resuming".format(self.server_name))
            self._sleeping = False

    def _new_session(self):
        login_payload = {
            'password_hash': '',
            'username': self._username,
            'password': '',
            'remember': '-1'
        }

        session = requests.Session()

        login_page_response = self._get(session, self._urls['login'],
                                        login=True)
        if self._http_auth:
            return session

        if "hashAlg = \"sha1\"" in login_page_response.text:
            hex_dig = "$sha1$" + sha1(
                self._password.encode("iso-8859-1", "ignore")
                + self._username.encode("iso-8859-1", "ignore")
            ).hexdigest()
            login_payload['password_hash'] = hex_dig
        else:
            login_payload['password'] = self._password
            login_payload['password_hash'] = self._password

        login_page_tree = html.fromstring(login_page_response.content)
        token_pattern = "//input[@name='token']/@value"
        token = login_page_tree.xpath(token_pattern)[0]
        login_payload.update({'token': token})

        response = self._post(session, self._urls['login'], login_payload,
                              login=True)

        if "hashAlg" in response.text \
                or "Exceeded login attempts" in response.text:
            raise AuthorizationException

        if "<!-- KF2-MA-INSTALLED-FLAG -->" in response.text:
            self.ma_installed = True

        return session

    def get_new_messages(self):
        payload = {
            'ajax': '1'
        }

        return self._post(
            self._session,
            self._urls['chat'],
            payload
        )

    def post_message(self, payload):
        return self._post(
            self._session,
            self._urls['chat'],
            payload,
        )

    def get_server_info(self):
        return self._get(
            self._session,
            self._urls['info']
        )

    def get_map(self):
        return self._get(
            self._session,
            self._urls['map']
        )

    def post_map(self, payload):
        return self._post(
            self._session,
            self._urls['map'],
            payload
        )

    def get_players(self):
        return self._get(
            self._session,
            self._urls['players']
        )

    def get_passwords(self):
        return self._get(
            self._session,
            self._urls['passwords']
        )

    def post_passwords(self, payload):
        return self._post(
            self._session,
            self._urls['passwords'],
            payload
        )

    def get_bans(self):
        return self._get(
            self._session,
            self._urls['bans']
        )

    def post_bans(self, payload):
        return self._post(
            self._session,
            self._urls['bans'],
            payload
        )

    def post_players_action(self, payload):
        return self._post(
            self._session,
            self._urls['players_action'],
            payload
        )

    def get_general_settings(self):
        return self._get(
            self._session,
            self._urls['general_settings']
        )

    def post_general_settings(self, payload):
        return self._post(
            self._session,
            self._urls['general_settings'],
            payload
        )

    def get_game_type(self):
        return self._get(
            self._session,
            self._urls['game_type']
        )

    def post_game_type(self, payload):
        return self._post(
            self._session,
            self._urls['game_type'],
            payload
        )

    def get_maplist(self):
        return self._get(
            self._session,
            self._urls['maplist']
        )

    def post_maplist(self, payload):
        return self._post(
            self._session,
            self._urls['maplist'],
            payload
        )

    def get_welcome(self):
        return self._get(
            self._session,
            self._urls['welcome']
        )

    def post_welcome(self, payload):
        return self._post(
            self._session,
            self._urls['welcome'],
            payload
        )

    def post_command(self, payload):
        return self._post(
            self._session,
            self._urls['console'],
            payload
        )

    def get_payload_general_settings(self):
        response = self.get_general_settings()
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
                "{} couldn't retrieve map information, please check that your "
                "KFMapSummary section is correctly configured for this map"
                .format(self.server_name)
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
