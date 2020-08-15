import pytest

from utils.net import (
    get_country, phone_home, resolve_address
)


def test_get_country():
    expected = ("United States", "US")
    unknown = ("Unknown", "??")
    c = get_country("8.8.8.8")
    assert c == expected or c == unknown


def test_resolve_address():
    tests = [
        {"address": "kf2.th3-z.xyz",
         "expected": "https://kf2.th3-z.xyz"},
        {"address": "https://kf2.th3-z.xyz",
         "expected": "https://kf2.th3-z.xyz"},
        {"address": "http://kf2.th3-z.xyz",
         "expected": "https://kf2.th3-z.xyz"},
        {"address": "kf2.th3-z.xyz:8090",
         "expected": "http://kf2.th3-z.xyz:8090"},
        {"address": "136.244.96.98:8090",
         "expected": "http://136.244.96.98:8090"}
    ]

    for test in tests:
        result = resolve_address(test["address"])
        assert result == test["expected"]
