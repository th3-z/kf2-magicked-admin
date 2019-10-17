from settings import Settings

TEST_CONFIG_PATH = "magicked_admin/tests/test_data/conf/magicked_admin.conf"
SETTINGS = Settings(TEST_CONFIG_PATH)
ADDRESS = SETTINGS.setting("server_one", "address")

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


class MockSession:
    def __init__(self):
        self.urls = {
            'login': '{}/ServerAdmin/'.format(ADDRESS),
            'chat': '{}/ServerAdmin/current/chat+data'.format(ADDRESS),
            'info': '{}/ServerAdmin/current/info'.format(ADDRESS),
            'map': '{}/ServerAdmin/current/change'.format(ADDRESS),
            'players': '{}/ServerAdmin/current/players'.format(ADDRESS),
            'passwords': '{}/ServerAdmin/policy/passwords'.format(ADDRESS),
            'bans': '{}/ServerAdmin/policy/bans'.format(ADDRESS),
            'game_type': '{}/ServerAdmin/settings/gametypes'.format(ADDRESS),
            'maplist': '{}/ServerAdmin/settings/maplist'.format(ADDRESS),
            'welcome': '{}/ServerAdmin/settings/welcome'.format(ADDRESS),
            'console': '{}/ServerAdmin/console'.format(ADDRESS),
            'general_settings': '{}/ServerAdmin/settings/general'.format(
                ADDRESS
            ),
            'players_action': '{}/ServerAdmin/current/players+data'.format(
                ADDRESS
            )
        }

    def post(self, *args, **kwargs):
        if args[0] == self.urls['login']:
            return MockResponse("<!-- KF2-MA-INSTALLED-FLAG -->", 200)

        return MockResponse(None, 404)

    def get(self, *args, **kwargs):
        if args[0] == self.urls['login']:
            return MockResponse(LOGIN_TOKEN_RESP, 200)

        return MockResponse(None, 404)
