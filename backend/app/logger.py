import logging
import sys

"""
Logging configuration module
Roles:
1. Logging configuration for the entire application
2. Manage log format and output level
3. Provide logs for debugging and monitoring
"""

# logging format
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

# create logger
logger = logging.getLogger("animal_lens")
logger.setLevel(logging.DEBUG)

# add console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# configure formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# add handler
logger.addHandler(console_handler)