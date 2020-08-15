import pytest

from utils.time import seconds_to_hhmmss


def test_seconds_to_hhmmss():
    tests = [
        {"seconds": 12,
         "expected": "00:00:12"},
        {"seconds": 0,
         "expected": "00:00:00"},
        {"seconds": 60 * 60 * 3,
         "expected": "03:00:00"},
        {"seconds": 71237934,
         "expected": "19788:18:54"}
    ]

    for test in tests:
        result = seconds_to_hhmmss(test["seconds"])
        assert result == test["expected"]
