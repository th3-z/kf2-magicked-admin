import gettext
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import urlopen

import requests

_ = gettext.gettext


# Add http scheme if no scheme
def _add_address_scheme(address):
    if len(address) < 9 or "://" not in address[:8]:
        address = "http://" + address
    return address


# Is the address responsive
def _is_valid_address(address):
    try:
        code = urlopen(address).getcode()
    except HTTPError as err:
        return err.code == 401
    except URLError:
        return False
    return code == 200


# Returns redirected scheme+netloc if exists
def _follow_redirect(address):
    try:
        response = urlopen(address)
        redirect_url = urlparse(response.geturl())
        return redirect_url.scheme + "://" + redirect_url.netloc
    except Exception:
        return address


# Resolve common address issues
def resolve_address(address):
    address = _add_address_scheme(address.strip())

    if not _is_valid_address(address):
        return address

    return _follow_redirect(address)


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
