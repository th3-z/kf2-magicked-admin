import logging
import time
from hashlib import sha1

import requests
from lxml import html

from utils import DEBUG, die, warning
from web_admin.constants import *


class WebInterface(object):
    def __init__(self, address, username, password, server_name="unnamed"):
        self.__address = address
        self.__username = username
        self.__password = password

        self.server_name = server_name
        self.ma_installed = False

        self.__urls = {
            'login': '{}/ServerAdmin/'
                .format(address),
            'chat': '{}/ServerAdmin/current/chat+data'
                .format(address),
            'info': '{}/ServerAdmin/current/info'
                .format(address),
            'map': '{}/ServerAdmin/current/change'
                .format(address),
            'players': '{}/ServerAdmin/current/players'
                .format(address),
            'players_action': '{}/ServerAdmin/current/players+data'
                .format(address),
            'passwords': '{}/ServerAdmin/policy/passwords'
                .format(address),
            'bans': '{}/ServerAdmin/policy/bans'
                .format(address),
            'general_settings': '{}/ServerAdmin/settings/general'
                .format(address),
            'game_type': '{}/ServerAdmin/settings/gametypes'
                .format(address),
            'map_cycle': '{}/ServerAdmin/settings/maplist'
                .format(address),
            'welcome': '{}/ServerAdmin/settings/welcome'
                .format(address),
            'console': '{}/ServerAdmin/console'
                .format(address)
        }

        self.__timeout = 5
        self.__sleeping = False

        self.__session = self.__new_session()

    def __get(self, session, url, retry_interval=6, login=False):
        while True:
            try:
                response = session.get(url, timeout=self.__timeout)
                if response.status_code > 400:
                    self.__sleep()
                    time.sleep(retry_interval)
                    continue
                else:
                    self.__wake()

                if not login:
                    if "hashAlg" in response.text:
                        print("Session killed, renewing!")
                        self.__session = self.__new_session()
                    else:
                        return response
                else:
                    return response

            except requests.exceptions.HTTPError:
                if DEBUG:
                    print("HTTPError getting {}. Retrying in {}s"
                          .format(url, retry_interval))
            except requests.exceptions.ConnectionError:
                if DEBUG:
                    print("ConnectionError getting {}. Retrying in {}s"
                          .format(url, retry_interval))
            except requests.exceptions.Timeout:
                if DEBUG:
                    print("Timeout getting {}. Retrying in {}s"
                          .format(url, retry_interval))
            except requests.exceptions.RequestException as err:
                if DEBUG:
                    print("None-specific RequestException getting {}, "
                          "{}. Retrying in {}s"
                          .format(url, str(err), retry_interval))

            time.sleep(retry_interval)

    def __post(self, session, url, payload, retry_interval=6, login=False):
        while True:
            try:
                response = session.post(
                    url, payload,
                    timeout=self.__timeout
                )
                if response.status_code > 400:
                    self.__sleep()
                    time.sleep(retry_interval)
                    continue
                else:
                    self.__wake()

                if not login:
                    if "hashAlg" in response.text:
                        print("Session killed, renewing!")
                        self.__session = self.__new_session()
                else:
                    return response
                return response
            except requests.exceptions.HTTPError:
                if DEBUG:
                    print("HTTPError posting {}. Retrying in {}s"
                          .format(url, retry_interval))
            except requests.exceptions.ConnectionError:
                if DEBUG:
                    print("ConnectionError posting {}. Retrying in {}s"
                          .format(url, retry_interval))
            except requests.exceptions.Timeout:
                if DEBUG:
                    print("Timeout posting {}. Retrying in {}s"
                          .format(url, retry_interval))
            except requests.exceptions.RequestException as err:
                if DEBUG:
                    print("None-specific RequestException posting {}, "
                          "{}. Retrying in {}s"
                          .format(url, str(err), retry_interval))

            time.sleep(retry_interval)

    def __sleep(self):
        if not self.__sleeping:
            print("Web admin not responding, sleeping")
            self.__sleeping = True

    def __wake(self):
        if self.__sleeping:
            print("Web admin is back, resuming")
            self.__sleeping = False


    def __new_session(self):
        login_payload = {
            'password_hash': '',
            'username': self.__username,
            'password': '',
            'remember': '-1'
        }

        session = requests.Session()
        login_page_response = self.__get(session, self.__urls['login'], login=True)

        if "hashAlg = \"sha1\"" in login_page_response.text:
            hash = "$sha1$" + sha1(
                self.__password.encode("iso-8859-1", "ignore")
                + self.__username.encode("iso-8859-1", "ignore")
            ).hexdigest()
            login_payload['password_hash'] = hash
        else:
            login_payload['password'] = self.__password
            login_payload['password_hash'] = self.__password

        login_page_tree = html.fromstring(login_page_response.content)
        token_pattern = "//input[@name='token']/@value"
        token = login_page_tree.xpath(token_pattern)[0]
        login_payload.update({'token': token})

        response = self.__post(session, self.__urls['login'], login_payload, login=True)

        if "hashAlg" in response.text or "Exceeded login attempts" in response.text and DEBUG:
            # TODO Expand on handling here, should gracefully terminate
            die("Login failure, bad credentials or login attempts exceeded.")

        if "<!-- KF2-MA-INSTALLED-FLAG -->" in response.text:
            self.ma_installed = True
            print("Detected KF2-MA install on server.")
        else:
            warning("KF2-MA install not detect on server.")

        return session

    def get_new_messages(self):
        payload = {
            'ajax': '1'
        }

        return self.__post(
            self.__session,
            self.__urls['chat'],
            payload
        )

    def post_message(self, payload):
        return self.__post(
            self.__session,
            self.__urls['chat'],
            payload,
        )

    def get_server_info(self):
        return self.__get(
            self.__session,
            self.__urls['info']
        )

    def get_map(self):
        return self.__get(
            self.__session,
            self.__urls['map']
        )

    def post_map(self, payload):
        return self.__post(
            self.__session,
            self.__urls['map'],
            payload
        )

    def get_players(self):
        return self.__get(
            self.__session,
            self.__urls['players']
        )

    def get_passwords(self):
        return self.__get(
            self.__session,
            self.__urls['passwords']
        )

    def post_passwords(self, payload):
        return self.__post(
            self.__session,
            self.__urls['passwords'],
            payload
        )

    def get_bans(self):
        return self.__get(
            self.__session,
            self.__urls['bans']
        )

    def post_bans(self, payload):
        print(str(payload))
        return self.__post(
            self.__session,
            self.__urls['bans'],
            payload
        )

    def post_players_action(self, payload):
        return self.__post(
            self.__session,
            self.__urls['players_action'],
            payload
        )

    def get_general_settings(self):
        return self.__get(
            self.__session,
            self.__urls['general_settings']
        )

    def post_general_settings(self, payload):
        return self.__post(
            self.__session,
            self.__urls['general_settings'],
            payload
        )

    def get_game_type(self):
        return self.__get(
            self.__session,
            self.__urls['game_type']
        )

    def post_game_type(self, payload):
        return self.__post(
            self.__session,
            self.__urls['game_type'],
            payload
        )

    def get_map_cycle(self):
        return self.__get(
            self.__session,
            self.__urls['map_cycle']
        )

    def post_map_cycle(self, payload):
        return self.__post(
            self.__session,
            self.__urls['map_cycle'],
            payload
        )

    def get_welcome(self):
        return self.__get(
            self.__session,
            self.__urls['welcome']
        )

    def post_welcome(self, payload):
        return self.__post(
            self.__session,
            self.__urls['welcome'],
            payload
        )

    def post_command(self, payload):
        return self.__post(
            self.__session,
            self.__urls['console'],
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
                '//select[@id="settings_GameLength"]' +
                '//option[@selected="selected"]/@value'
            )[0]


        difficulty_val = general_settings_tree.xpath(
            '//input[@name="settings_GameDifficulty_raw"]/@value'
        )[0]

        settings = {'settings_GameLength': length_val,
                    'settings_GameDifficulty': difficulty_val,
                    'action': 'save'}

        for i in range(0, len(settings_names)):
            settings[settings_names[i]] = settings_vals[i]

        for i in range(0, len(radio_settings_names)):
            settings[radio_settings_names[i]] = radio_settings_vals[i]

        return settings

    def get_payload_motd_settings(self):
        response = self.get_welcome()
        motd_tree = html.fromstring(response.content)

        banner_link = motd_tree.xpath('//input[@name="BannerLink"]/@value')[0]
        web_link = motd_tree.xpath('//input[@name="WebLink"]/@value')[0]
        clan_motto = motd_tree.xpath('//textarea[@name="ClanMotto"]/text()')[0]
        motd = motd_tree.xpath('//textarea[@name="ServerMOTD"]/text()')[0]

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
        print(game_type)
        map_name = map_tree.xpath(map_pattern)[0]
        url_extra = map_tree.xpath(url_extra_pattern)[0]
        mutator_count = map_tree.xpath(mutator_count_pattern)[0]

        return {
            "gametype": game_type,
            "map": map_name,
            "mutatorGroupCount": mutator_count,
            "urlextra": url_extra,
            "action": "change"
        }
