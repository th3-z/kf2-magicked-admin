import pytest

from magicked_admin.utils.net import get_country, phone_home, resolve_address


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
        {"address": "kf2.th3-z.xyz:8080",
         "expected": "http://kf2.th3-z.xyz:8080"},
        {"address": "45.32.187.80:8080",
         "expected": "http://45.32.187.80:8080"}
    ]

    for test in tests:
        result = resolve_address(test["address"])
        assert result == test["expected"]
