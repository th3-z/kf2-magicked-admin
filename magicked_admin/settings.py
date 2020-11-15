import configparser
import gettext
import os
import sys
from collections import namedtuple
import logging

from utils import find_data_file

langs = [
    {
        "name": "English",
        "code": "en_GB"
    },
    {
        "name": "Español",
        "code": "es_ES"
    },
    {
        "name": "Deutsche",
        "code": "de_DE"
    },
    {
        "name": "Français",
        "code": "fr_FR"
    }
]

server_options = ['address', 'username', 'password', 'game_password', 'url_extras', 'refresh_rate']
ServerConfig = namedtuple('ServerConfig', server_options)
default_server_config = ServerConfig('127.0.0.1:8080', 'Admin', '123', '123', '', '1')

template_server_config = """
# [server_one]
# address = 127.0.0.1:8080
# username = Admin
# password = 123
# game_password = 123
# url_extras = 
# refresh_rate = 1
"""


class Settings:
    debug = __debug__ and not hasattr(sys, 'frozen')
    banner_url = "https://kf2-ma.th3-z.xyz/"
    config_path = find_data_file("conf/magicked_admin.conf")
    config_path_display = "conf/magicked_admin.conf"
    log_level = logging.DEBUG if debug else logging.INFO

    language = "en_GB"
    servers = {}

    @classmethod
    def load(cls):
        config = configparser.ConfigParser(strict=False)
        config.read(cls.config_path)

        try:
            cls.language = config.get('magicked_admin', 'language')
        except configparser.NoSectionError:
            config.add_section("magicked_admin")
            config.set("magicked_admin", "language", cls.language)
        except configparser.NoOptionError:
            config.set("magicked_admin", "language", cls.language)

        for section in config.sections():
            if section != "magicked_admin":
                options = {}
                for option in server_options:
                    try:
                        value = config.get(section, option)
                    except configparser.NoOptionError:
                        value = getattr(default_server_config, option)
                        config.set(section, option, value)
                    options[option] = value

                cls.servers[section] = ServerConfig(
                    *options.values()
                )

        with open(cls.config_path, 'w') as config_file:
            config.write(config_file)
        cls.set_language(cls.language)

    @classmethod
    def append_template(cls):
        with open(cls.config_path, 'a') as config_file:
            config_file.write(template_server_config[1:]+'\n')

    @classmethod
    def set_language(cls, lang_code):
        if lang_code not in [lang['code'] for lang in langs]:
            lang_code = cls.language

        config = configparser.ConfigParser(strict=False)
        config.read(cls.config_path)

        config.set('magicked_admin', 'language', lang_code)

        cls.language = lang_code

        lang = gettext.translation(
            'magicked_admin', find_data_file('locale'), [lang_code]
        )
        lang.install()
        os.environ['LANGUAGE'] = lang_code[:2]

        with open(cls.config_path, 'w') as config_file:
            config.write(config_file)

    @classmethod
    def add_server(cls, name, server_config):
        config = configparser.ConfigParser(strict=False)
        config.read(cls.config_path)

        config.add_section(name)
        config.set(name, 'address', server_config.address)
        config.set(name, 'username', server_config.username)
        config.set(name, 'password', server_config.password)
        config.set(name, 'game_password', server_config.game_password)
        config.set(name, 'url_extras', server_config.url_extras)
        config.set(name, 'refresh_rate', server_config.refresh_rate)

        cls.servers[name] = server_config

        with open(cls.config_path, 'w') as config_file:
            config.write(config_file)

    @classmethod
    def remove_server(cls, name):
        config = configparser.ConfigParser(strict=False)
        config.read(cls.config_path)

        config.remove_section(name)
        cls.servers.pop(name)

        with open(cls.config_path, 'w') as config_file:
            config.write(config_file)


# Autoload
Settings.load()
