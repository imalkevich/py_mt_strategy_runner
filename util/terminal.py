""" """

from .config import config

TERMINAL_POOL = config.get("terminal", "pool").split(",")