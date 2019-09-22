import configparser
import os
from getpass import getpass

from utils import die, fatal, find_data_file, info
from utils.net import resolve_address

CONFIG_PATH = find_data_file("conf/magicked_admin.conf")
CONFIG_PATH_DISPLAY = "conf/magicked_admin.conf"

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
    'dosh_threshold': "0",
}

SETTINGS_REQUIRED = ['address', 'password', 'motd_scoreboard',
                     'scoreboard_type', 'dosh_threshold',
                     'max_players', 'enable_greeter']

CONFIG_DIE_MESG = "Please correct this manually  or delete '{}' to create a clean config next run.".format(
    CONFIG_PATH)


class Settings:
    def __init__(self, skip_setup=False):
        if not os.path.exists(CONFIG_PATH):
            info("No configuration was found, first time setup is required!")

            if not skip_setup:
                config = self.construct_config_interactive()
            else:
                config = self.construct_config_template()

            with open(CONFIG_PATH, 'w') as config_file:
                config.write(config_file)

            if skip_setup:
                info("Guided setup was skipped, a template has been generated.")
                die(
                    "Setup is not complete yet, please amend '{}' with your "
                    "server details.".format(CONFIG_PATH_DISPLAY)
                )

        try:
            self.config = configparser.ConfigParser()
            self.config.read(CONFIG_PATH)

        except configparser.DuplicateOptionError as e:
            fatal(
                "Configuration error(s) found!\nSection '{}' has a duplicate setting: '{}'."
                .format(e.section, e.option)
            )
            die(CONFIG_DIE_MESG, pause=True)

        config_errors = self.validate_config(self.config)

        if config_errors:
            fatal("Configuration error(s) found!")
            for error in config_errors:
                print("\t\t" + error)
            die(CONFIG_DIE_MESG, pause=True)

    def setting(self, section, setting):
        try:
            return self.config.get(section, setting)
        except configparser.NoOptionError:
            return None

    def sections(self):
        return self.config.sections()

    @staticmethod
    def construct_config_interactive():
        print("     Please input your web admin details below.")
        new_config = configparser.ConfigParser()
        new_config.add_section(SETTINGS_DEFAULT['server_name'])

        for setting in SETTINGS_DEFAULT:
            new_config.set(SETTINGS_DEFAULT['server_name'], setting,
                           SETTINGS_DEFAULT[setting])

        while True:
            address = input(
                "\nAddress [default - localhost:8080]: ") or "localhost:8080"
            resolved_address = resolve_address(address)
            if resolved_address:
                break
            else:
                print(
                    "Address not responding!\nAccepted formats are: 'ip:port', 'domain', or 'domain:port'")

        username = input("Username [default - Admin]: ") or "Admin"
        password = getpass(
            "Password (will not echo) [default - 123]: ") or "123"
        print()  # \n

        new_config.set(SETTINGS_DEFAULT['server_name'], 'address',
                       resolved_address)
        new_config.set(SETTINGS_DEFAULT['server_name'], 'username', username)
        new_config.set(SETTINGS_DEFAULT['server_name'], 'password', password)

        return new_config

    @staticmethod
    def construct_config_template():
        new_config = configparser.ConfigParser()
        new_config.add_section(SETTINGS_DEFAULT['server_name'])

        for setting in SETTINGS_DEFAULT:
            new_config.set(SETTINGS_DEFAULT['server_name'], setting,
                           SETTINGS_DEFAULT[setting])

        new_config.set(
            SETTINGS_DEFAULT['server_name'],
            'address',
            "http://localhost:8080"
        )
        new_config.set(SETTINGS_DEFAULT['server_name'], 'username', "Admin")
        new_config.set(SETTINGS_DEFAULT['server_name'], 'password', "123")
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
                    errors.append(
                        "Section '{}' is missing a required setting: '{}'.".format(
                            section, setting))

        return errors
