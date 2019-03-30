import os
import configparser

from utils import die

CONFIG_PATH = "./magicked_admin.conf"

SETTINGS_DEFAULT = {
    'server_name': 'server_one',
    # address = 127.0.0.1:8080
    # username = Admin
    # password = 123
    'game_password': '123',
    'motd_scoreboard': 'False',
    'scoreboard_type': 'Kills',
    'max_players': "6",
    'enable_greeter': "True",
    'level_threshold': "0",
}


class Settings:
    def __init__(self):
        if not os.path.exists(CONFIG_PATH):
            print("No configuration was found, first time setup is required!")
            print("Please input your web admin details.")
            config = self.construct_config_interactive()

            with open(CONFIG_PATH, 'w') as config_file:
                config.write(config_file)

        try:
            self.config = configparser.ConfigParser()
            self.config.read(CONFIG_PATH)

        except configparser.DuplicateOptionError as e:
            print("Duplicate key found in config, see: '{}', under '[{}]'."
                .format(e.option, e.section)
            )
            die("Please correct this manually  or delete '{}' to create a clean config next run."
                .format(CONFIG_PATH))

    def setting(self, section, setting):
        try:
            return self.config.get(section, setting)
        except configparser.NoOptionError:
            return None

    def sections(self):
        return self.config.sections()

    @staticmethod
    def construct_config_interactive():
        new_config = configparser.ConfigParser()
        new_config.add_section(SETTINGS_DEFAULT['server_name'])

        for setting in SETTINGS_DEFAULT:
            new_config.set(SETTINGS_DEFAULT['server_name'], setting, SETTINGS_DEFAULT[setting])

        address = input("Address (domain | domain:port | ip:port) [localhost:8080]: ") or "localhost:8080"
        username = input("Username [Admin]: ") or "Admin"
        password = input("Password [123]: ") or "123"

        new_config.set(SETTINGS_DEFAULT['server_name'], 'address', address)
        new_config.set(SETTINGS_DEFAULT['server_name'], 'username', username)
        new_config.set(SETTINGS_DEFAULT['server_name'], 'password', password)

        return new_config

    @staticmethod
    def validate_config(config):
        pass

