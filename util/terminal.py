""" """

from .config import config

TERMINAL_POOL = []

if config.has_section("terminal"):
    TERMINAL_POOL = [{'exe_path': t[0], 'data_path': t[1] } for t in [t.split('|') for t in config.get("terminal", "pool").split(",")]]