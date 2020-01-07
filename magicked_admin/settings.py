import configparser
import gettext
import os

from utils import die, fatal, find_data_file, info
from utils.net import resolve_address

# if getch is available, implement getpass() with asterisks
try:
    import getch

    def getpass(prompt):
        print(prompt, end='', flush=True)
        buf = ''
        while True:
            ch = getch.getch()
            if ch == '\n':
                print('')
                break
            else:
                buf += ch
                print('*', end='', flush=True)
        return buf
except ImportError:
    from getpass import getpass

_ = gettext.gettext

CONFIG_PATH = find_data_file("conf/magicked_admin.conf")
CONFIG_PATH_DISPLAY = "conf/magicked_admin.conf"

SETTINGS_DEFAULT = {
    'server_name': 'server_one',
    # address = 127.0.0.1:8080
    # username = Admin
    # password = 123
    'game_password': '123',
}

SETTINGS_REQUIRED = ['address', 'username', 'password']

CONFIG_DIE_MESG = _("Please correct this manually  or delete '{}' to create "
                    "a clean config next run.").format(CONFIG_PATH_DISPLAY)


class Settings:
    def __init__(self, config_filename, skip_setup=False):
        if not os.path.exists(config_filename):
            info(_("No configuration was found, first time setup is "
                   "required!"))

            if not skip_setup:
                config = self.construct_config_interactive()
            else:
                config = self.construct_config_template()

            with open(config_filename, 'w') as config_file:
                config.write(config_file)

            if skip_setup:
                info(_("Guided setup was skipped, a template has been "
                       "generated."))
                die(_("Setup is not complete yet, please amend '{}' with your "
                      "server details.").format(CONFIG_PATH_DISPLAY))

        try:
            self.config = configparser.ConfigParser()
            self.config.read(config_filename)

        except configparser.DuplicateOptionError as e:
            fatal(_("Configuration error(s) found!\nSection '{}' has a "
                    "duplicate setting: '{}'.").format(e.section, e.option))
            die(CONFIG_DIE_MESG, pause=True)

        config_errors = self.validate_config(self.config)

        if config_errors:
            fatal(_("Configuration error(s) found!"))
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
        print(_("    Please input your web admin details below."))
        new_config = configparser.ConfigParser()
        new_config.add_section(SETTINGS_DEFAULT['server_name'])

        for setting in SETTINGS_DEFAULT:
            if setting == "server_name":
                continue
            new_config.set(SETTINGS_DEFAULT['server_name'], setting,
                           SETTINGS_DEFAULT[setting])

        while True:
            address = input(
                _("\nAddress [default - localhost:8080]: ")
            ) or "localhost:8080"
            resolved_address = resolve_address(address)
            if resolved_address:
                break
            else:
                print(_("Address not responding!\nAccepted formats are: "
                      "'ip:port', 'domain', or 'domain:port'"))

        username = input(_("Username [default - Admin]: ")) or "Admin"
        password = getpass(
            _("Password (will not echo) [default - 123]: ")) or "123"
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
            if setting == "server_name":
                continue
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
            errors.append(_("Config file has no sections."))
            return errors

        for section in sections:
            for setting in SETTINGS_REQUIRED:
                try:
                    config.get(section, setting)
                except configparser.NoOptionError:
                    errors.append(
                        _("Section '{}' is missing a required setting: "
                          "'{}'.").format(section, setting)
                    )

        return errors
