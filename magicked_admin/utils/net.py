from urllib.request import urlopen


def repair_address_scheme(address):
    address = address.strip()

    if len(address) < 9 or "://" not in address[:8]:
        address = "http://" + address

    return address

def is_valid_address(address):
    try:
        code = urlopen(address).getcode()
    except:
        return False

    return code < 400
