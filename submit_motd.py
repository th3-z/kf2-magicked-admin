import requests
import re

login_url = "http://173.199.74.63:23002/ServerAdmin/"
motd_url = "http://173.199.74.63:23002/ServerAdmin/settings/welcome"

banner_url = "http://i.imgur.com/ilf97xg.png"
clan_motto = "kf.znel.org:2300     ::     173.199.74.63:23000     ::     United Kingdom"
web_link = "http://znel.org/kf"

motd_f = open("motd.txt", "r")
motd = motd_f.read()

login_payload = {
    'password_hash': '',
    'username': 'Admin',
    'password': '',
    'remember': '-1'
}

motd_payload = {
    'BannerLink': banner_url,
    'ClanMotto': clan_motto,
    'ClanMottoColor': '#FF0000',
    'ServerMOTD': motd.encode("iso-8859-1", "ignore"),
    'ServerMOTDColor': '#FF0000',
    'WebLink': web_link,
    'WebLinkColor': '#FF0000',
    'liveAdjust': '1',
    'action': 'save'
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
    print("Uploading motd...")
    s.post(motd_url, data=motd_payload)

motd_f.close()
