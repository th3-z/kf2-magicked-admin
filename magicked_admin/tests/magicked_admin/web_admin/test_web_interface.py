import pytest
from unittest import mock
from requests import Session

from web_admin.web_interface import WebInterface

from settings import Settings

TEST_CONFIG_PATH = "magicked_admin/tests/test_data/conf/magicked_admin.conf"
settings = Settings(TEST_CONFIG_PATH)

ADDRESS = settings.setting("server_one", "address")

LOGIN_TOKEN_RESP = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
 "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<body>
<div id="content">
<form id="loginform" method="post" action="/ServerAdmin/" autocomplete="off">
<fieldset>
<div class="section">
<input type="hidden" name="token" value="A67E6B0B"/>
</div>
</fieldset>
</form>
</div>
</body>
</html>"""


class MockResponse:
    def __init__(self, text, status_code):
        self.status_code = status_code
        self.text = text
        self.content = bytes(text, "utf-8")

    def text(self):
        return self.text

    def content(self):
        return self.content


def mock_session_post(*args, **kwargs):
    if args[0] == '{}/ServerAdmin/'.format(ADDRESS):
        return MockResponse("<!-- KF2-MA-INSTALLED-FLAG -->", 200)

    return MockResponse(None, 404)


def mock_session_get(*args, **kwargs):
    if args[0] == '{}/ServerAdmin/'.format(ADDRESS):
        return MockResponse(LOGIN_TOKEN_RESP, 200)

    return MockResponse(None, 404)


@pytest.fixture
@mock.patch.object(Session, 'get', side_effect=mock_session_get)
@mock.patch.object(Session, 'post', side_effect=mock_session_post)
def web_iface(mock_get, mock_post):
    web_iface = WebInterface(
        ADDRESS,
        settings.setting("server_one", "username"),
        settings.setting("server_one", "password"),
        server_name="server_one"
    )

    return web_iface


def test_get_server_info(web_iface):
    assert web_iface
