import configparser
import os
from getpass import getpass

from utils import die, find_data_file
from utils.net import is_valid_address, repair_address_scheme

CONFIG_PATH = find_data_file("./magicked_admin.conf")

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

SETTINGS_REQUIRED = ['address', 'password', 'motd_scoreboard', 'scoreboard_type', 'max_players', 'enable_greeter']

CONFIG_DIE_MESG = "Please correct this manually  or delete '{}' to create a clean config next run.".format(CONFIG_PATH)


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
            print("Configuration error(s) found!\nSection '{}' has a duplicate setting: '{}'."
                .format(e.section, e.option)
            )
            die(CONFIG_DIE_MESG)

        config_errors = self.validate_config(self.config)

        if config_errors:
            print("Configuration error(s) found!")
            for error in config_errors:
                print(error)
            die(CONFIG_DIE_MESG)

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

        while True: 
            address = input("\nAddress [default - localhost:8080]: ") or "localhost:8080"
            scheme_address = repair_address_scheme(address)
            if is_valid_address(scheme_address):
                break
            else:
                print("Address not responding!\nAccepted formats are: 'ip:port', 'domain', or 'domain:port'")

        username = input("Username [default - Admin]: ") or "Admin"
        password = getpass("Password (will not echo) [default - 123]: ") or "123"
        print() # \n

        new_config.set(SETTINGS_DEFAULT['server_name'], 'address', address)
        new_config.set(SETTINGS_DEFAULT['server_name'], 'username', username)
        new_config.set(SETTINGS_DEFAULT['server_name'], 'password', password)

        return new_config

    @staticmethod
    def validate_config(config):
        sections = config.sections()
        errors = []

        if len(sections) < 1:
            errors.append("Config file has no sections.")
            return errors

        for section in sections:
            for setting in SETTINGS_REQUIRED:
                try:
                    config.get(section, setting)
                except configparser.NoOptionError:
                    errors.append("Section '{}' is missing a required setting: '{}'.".format(section, setting))

        return errors
