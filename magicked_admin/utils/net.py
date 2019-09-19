from urllib.parse import urlparse
from urllib.request import urlopen

import requests


# Add http scheme if no scheme
def __add_address_scheme(address):
    if len(address) < 9 or "://" not in address[:8]:
        address = "http://" + address
    return address


# Is the address responsive
def __is_valid_address(address):
    try:
        code = urlopen(address).getcode()
    except:
        return False
    return code == 200


# Returns redirected scheme+netloc if exists
def __follow_redirect(address):
    try:
        response = urlopen(address)
        redirect_url = urlparse(response.geturl())
        return redirect_url.scheme + "://" + redirect_url.netloc
    except:
        return address


# Resolve common address issues and test connection, returns None on fail
def resolve_address(address):
    address = __add_address_scheme(address.strip())

    if not __is_valid_address(address):
        return None
    else:
        return __follow_redirect(address)


# Ping home url
def phone_home():
    try:
        # See git.th3-z.xyz/www-th3-z-xyz/
        code = urlopen("https://www.th3-z.xyz/kf2-ma-ping")
    except:
        return False
    return code == 200


# Get geographical information for an ip address
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
