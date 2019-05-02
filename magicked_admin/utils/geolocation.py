import json
import urllib.error
import urllib.request
from contextlib import closing

import requests


def get_country(ip):
    url = "https://ipapi.co/" + ip + "/json/"
    unknown = ("Unknown", "??")

    geo_data = requests.get(url).json()

    if 'country_name' in geo_data:
        country = geo_data['country_name']
        country_code = geo_data['country']
        return country, country_code
    else:
        return unknown

