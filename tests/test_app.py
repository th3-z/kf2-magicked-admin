import pytest

from magicked_admin.utils.net import get_country


def test_true():
    assert True


def test_net():
    assert get_country("8.8.8.8")
