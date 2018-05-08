import urllib.request
import urllib.error
from contextlib import closing
import json

def get_country(ip):
    url = "http://www.freegeoip.net/json/" + ip
    unknown = ("Unknown", "??")
    try:
        with closing(urllib.request.urlopen(url)) as response:
            location = json.loads(response.read())
            country = location['country_name']
            country_code = location['country_code']
            if not country:
                return unknown
            return country, country_code
    except urllib.error.HTTPError:
        return unknown
    except urllib.error.URLError:
        return unknown
