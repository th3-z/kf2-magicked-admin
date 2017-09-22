import time
from subprocess import call
import re
import requests

login_url = "http://173.199.74.63:23002/ServerAdmin/"
players_url = "http://173.199.74.63:23002/ServerAdmin/current+gamesummary"

login_payload = {
    'password_hash': '',
    'username': 'chenbot',
    'password': '',
    'remember': '-1'
}

players_payload = {
    'ajax':'1'
}

players_ex = "rs\">(0\/6)<\/"

mins = 0

# Should probably just reset map when players=0 and map is not default

with requests.Session() as s:
    
    login_page_response = s.get(login_url)
    token_ex = "token\" value=\"(.*)\" \/"
    mo = re.search(token_ex, login_page_response.text)
    if mo:
        login_payload.update({'token':mo.group(1)})
    
    # Log me in
    print("Watchdog logging in...")
    p = s.post(login_url, data=login_payload)
    
    while True:
        players_response = s.post(players_url, players_payload)
        
        mo = re.search(players_ex, players_response.text)
        if mo:
            if mo.group(1) != "0/6":
                mins = 0
        else:
            mins = 0
        print("No players for: ", mins)
        # Sleep for a minute
        time.sleep(60)
        # Increment the minute total
        mins += 1
        
        if mins >= 15:
            print("Changing to a stock map...")
            exec(open("./reset_map.py").read())
            mins = 0
            time.sleep(120) # I should add exception handling to the requests instead
        
print("Watchdog logged out.")
