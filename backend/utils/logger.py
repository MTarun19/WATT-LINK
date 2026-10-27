"""
logger.py
-----------------------------------
WATT LINK Logging Configuration
"""

import logging
import os
from logging.handlers import RotatingFileHandler

# =====================================================
# Create Logs Directory
# =====================================================

LOG_DIR = "logs"

os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "watt_link.log")

# =====================================================
# Logger Configuration
# =====================================================

logger = logging.getLogger("WATT_LINK")

logger.setLevel(logging.INFO)

if not logger.handlers:

    formatter = logging.Formatter(

        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

    )

    # Console Logger
    console_handler = logging.StreamHandler()

    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    # File Logger (5 MB × 5 backups)
    file_handler = RotatingFileHandler(

        LOG_FILE,

        maxBytes=5 * 1024 * 1024,

        backupCount=5

    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

# =====================================================
# Helper Functions
# =====================================================

def info(message: str):
    logger.info(message)


def warning(message: str):
    logger.warning(message)


def error(message: str):
    logger.error(message)


def critical(message: str):
    logger.critical(message)


def debug(message: str):
    logger.debug(message)


def exception(message: str):
    logger.exception(message)