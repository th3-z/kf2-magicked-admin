import pytest
from unittest import mock
from requests import Session
from tests.web_admin.mock_session import MockSession

from web_admin.web_interface import WebInterface

from settings import Settings

TEST_CONFIG_PATH = "magicked_admin/tests/test_data/conf/magicked_admin.conf"
settings = Settings(TEST_CONFIG_PATH)


@pytest.fixture
@mock.patch.object(Session, 'get', side_effect=MockSession().get)
@mock.patch.object(Session, 'post', side_effect=MockSession().post)
def web_iface(mock_get, mock_post):
    return WebInterface(
        settings.setting("server_one", "address"),
        settings.setting("server_one", "username"),
        settings.setting("server_one", "password"),
        settings.setting("server_one", "refresh_rate"),
        server_name="server_one"
    )


@pytest.mark.skip(reason="incomplete")
def test_get_server_info(web_iface):
    assert web_iface
