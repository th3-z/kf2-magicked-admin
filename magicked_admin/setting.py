import os
import configparser

from utils import die

CONFIG_PATH = "./magicked_admin.conf"

class Setting:
    def __init__(self):
        if not os.path.exists(CONFIG_PATH):
            die("Configuration file ['{}'] not found".format(CONFIG_PATH))

        try:
            self.config = configparser.SafeConfigParser()
            self.config.read(CONFIG_PATH)

        except configparser.DuplicateOptionError as e:
            die("Duplicate key found in config, please check options: "
                "\"{}\", on server \"{}\"."
                .format(e.option, e.section)
            )

    def setting(self, section, setting):
        try:
            return self.config.get(section, setting)
        except configparser.NoOptionError:
            return None

    def sections(self):
        return self.config.sections()
