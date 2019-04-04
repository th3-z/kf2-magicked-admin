import json
import urllib.error
import urllib.request
from contextlib import closing

import requests


def get_country(ip):
    url = "https://ipapi.co/" + ip + "/json/"
    unknown = ("Unknown", "??")

    geo_data = requests.get(url).json()
    country = geo_data['country_name']
    country_code = geo_data['country']

    if not country:
        return unknown
    else:
        return country, country_code
