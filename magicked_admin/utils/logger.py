# Basically just moved the logging into here to use the same logger in very file.
# Now you can control the LOG-level via the Config-File

import logging
import sys

logging.basicConfig(stream=sys.stdout, format="%(levelname)s: %(message)s")

logger = logging.getLogger('')  # type: Logger

# This is the default log level but it will be overwritten in magicked_administrator.py
logger.setLevel(logging.DEBUG)

# urllib3 spams debug messages (reset connection) constantly
logging.getLogger("urllib3").setLevel(logging.INFO)


