import requests
import re

default_map = "KF-HostileGrounds"

login_url = "http://173.199.74.63:23002/ServerAdmin/"
change_url = "http://173.199.74.63:23002/ServerAdmin/current/change"

login_payload = {
    'password_hash': '',
    'username': 'chenbot',
    'password': '',
    'remember': '-1'
}

change_payload = {
    'gametype': 'KFGameContent.KFGameInfo_Survival',
    'map': 'KF-HostileGrounds',
    'mutatorGroupCount': '0',
    'urlextra': '?MaxPlayers=6',
    'action': 'change'
}

# Use 'with' to ensure the session context is closed after use.
with requests.Session() as s:
    # Get the login page and extract the auth token, add it to the payload
    login_page_response = s.get(login_url)
    token_ex = "token\" value=\"(.*)\" \/"
    mo = re.search(token_ex, login_page_response.text)
    if mo:
        login_payload.update({'token':mo.group(1)})
    
    # Log me in
    print("Logging in...")
    p = s.post(login_url, data=login_payload)

    # Post the motd
    print("Changing map, wait 20s...")
    s.post(change_url, data=change_payload)
