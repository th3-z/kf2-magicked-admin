# Basically just moved the logging into here to use the same logger in very file.
# Now you can control the LOG-level via the Config-File

import logging
import sys

logging.basicConfig(stream=sys.stdout)

logger = logging.getLogger('')  # type: Logger

# This is the default log level but it will be overwritten in main.py
logger.setLevel(logging.DEBUG)
