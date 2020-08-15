import pytest
from utils import (
    banner, warning, fatal, die, debug, info
)


def test_banner():
    banner()


def test_logging():
    warning("something", log=True, display=True)
    debug("something", log=True, display=True)
    info("something", log=True, display=True)
    fatal("something", log=True, display=True)


def test_die():
    with pytest.raises(IOError):
        die("rip", pause=True)
    with pytest.raises(SystemExit):
        die("rip", pause=False)
