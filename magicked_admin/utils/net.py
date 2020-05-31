import gettext
from urllib.parse import urlparse
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

import requests

_ = gettext.gettext


# Add http scheme if no scheme
def __add_address_scheme(address):
    if len(address) < 9 or "://" not in address[:8]:
        address = "http://" + address
    return address


# Is the address responsive
def __is_valid_address(address):
    try:
        code = urlopen(address).getcode()
    except HTTPError as err:
        return err.code == 401
    except URLError:
        return False
    return code == 200


# Returns redirected scheme+netloc if exists
def __follow_redirect(address):
    try:
        response = urlopen(address)
        redirect_url = urlparse(response.geturl())
        return redirect_url.scheme + "://" + redirect_url.netloc
    except Exception:
        return address


# Resolve common address issues and test connection, returns None on fail
def resolve_address(address):
    address = __add_address_scheme(address.strip())

    if not __is_valid_address(address):
        return None

    return __follow_redirect(address)


# Ping home url
def phone_home():
    try:
        # See git.th3-z.xyz/www-th3-z-xyz/
        code = urlopen("https://www.th3-z.xyz/kf2-ma-ping")
    except Exception:
        return False
    return code


# Get geographical information for an ip address
def get_country(ip):
    url = "https://freegeoip.app" + "/json/" + ip
    unknown = (_("Unknown"), "??")

    try:
        geo_data = requests.get(url).json()
    except Exception:
        return unknown

    if 'country_name' not in geo_data:
        return unknown

    country = geo_data['country_name']
    country_code = geo_data['country_code']
    return country, country_code
