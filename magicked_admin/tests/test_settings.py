import pytest
import configparser
from settings import Settings, CONFIG_PATH
from utils import find_data_file
from os.path import exists
from os import remove

TEST_CONFIG_PATH = "magicked_admin/tests/test_data/conf/magicked_admin.conf"
BROKEN_CONFIG_PATH = ("magicked_admin/tests/test_data/conf"
                      "/magicked_admin_broken.conf")
BAD_CONFIG_PATH = "junk"
SKIP_CONFIG_PATH = "magicked_admin/tests/test_data/conf/skip.conf"


def test_settings_test_config():
    settings = Settings(TEST_CONFIG_PATH)
    assert settings

    assert settings.setting("server_one", "username")
    assert len(settings.servers())


def test_settings_bad_config():
    with pytest.raises(IOError):
        Settings(BAD_CONFIG_PATH)


def test_settings_skip_config():
    try:
        remove(SKIP_CONFIG_PATH)
    except Exception:
        pass

    with pytest.raises(SystemExit):
        Settings(SKIP_CONFIG_PATH, skip_setup=True)
    assert exists(SKIP_CONFIG_PATH)

    config = configparser.ConfigParser()
    config.read(SKIP_CONFIG_PATH)

    remove(SKIP_CONFIG_PATH)


def test_settings_test_broken_config():
    config = configparser.ConfigParser()
    config.read(BROKEN_CONFIG_PATH)
