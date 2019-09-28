import pytest

from magicked_admin.utils.text import (
    str_to_bool, trim_string, pad_output, millify
)


def test_str_to_bool():
    tests = [
        {"str": "True",
         "expected": True},
        {"str": "1",
         "expected": True},
        {"str": "False",
         "expected": False},
        {"str": "0",
         "expected": False},
    ]

    for test in tests:
        result = str_to_bool(test["str"])
        assert result == test["expected"]


def test_trim_string():
    tests = [
        {"str": "test",
         "len": 8,
         "expected": "test"},
        {"str": "12345678",
         "len": 8,
         "expected": "12345678"},
        {"str": "123456789",
         "len": 8,
         "expected": "123456.."},
        {"str": "123456789",
         "len": 2,
         "expected": ".."}
    ]

    for test in tests:
        result = trim_string(test["str"], test["len"])
        assert result == test["expected"]


def test_millify():
    tests = [
        {"num": "1000",
         "expected": "1K"},
        {"num": 1000,
         "expected": "1K"},
        {"num": 1200,
         "expected": "1K"},
        {"num": 1000000,
         "expected": "1M"},
        {"num": 1000000000,
         "expected": "1B"},
        {"num": 1000000000000,
         "expected": "1T"},
        # TODO: This rounding is undesirable
        {"num": 1600000000000,
         "expected": "2T"},
        {"num": 0,
         "expected": "0"},
        {"num": "0",
         "expected": "0"},
    ]

    for test in tests:
        result = millify(test["num"])
        assert result == test["expected"]


def test_pad_output():
    tests = [
        {"str": "test",
         "expected": "\n\n\n\n\n\n\ntest"},
        {"str": "a\ntest",
         "expected": "\n\n\n\n\n\na\ntest"}
    ]

    for test in tests:
        result = pad_output(test["str"])
        assert result == test["expected"]
