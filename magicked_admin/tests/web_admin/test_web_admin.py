import pytest
from unittest import mock
from requests import Session
from tests.web_admin.mock_session import MockSession

from web_admin.web_interface import WebInterface
from web_admin.web_admin import WebAdmin
from web_admin.chat_worker import Chat

from settings import Settings

TEST_CONFIG_PATH = "magicked_admin/tests/test_data/conf/magicked_admin.conf"
settings = Settings(TEST_CONFIG_PATH)


@pytest.fixture
@mock.patch.object(Session, 'get', side_effect=MockSession().get)
@mock.patch.object(Session, 'post', side_effect=MockSession().post)
def web_admin(mock_get, mock_post):
    web_iface = WebInterface(
        settings.setting("server_one", "address"),
        settings.setting("server_one", "username"),
        settings.setting("server_one", "password"),
        settings.setting("server_one", "refresh_rate"),
        server_name="server_one"
    )

    chat = Chat(web_iface)

    return WebAdmin(web_iface, chat)


@pytest.mark.skip(reason="incomplete")
def test_web_admin(web_admin):
    assert web_admin
