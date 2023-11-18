import logging
import logging.config

logging.config.fileConfig("log.ini")

# Create the logger
logger = logging.getLogger(__name__)
