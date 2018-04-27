#!/usr/bin/env python

"""
Logging module.
"""
import sys

from datetime import datetime

TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S %Z'

def print_now(message, timestamp = True):
    if timestamp:
        message = '{}    {}'.format(datetime.now().strftime(TIMESTAMP_FORMAT), message)
    print(message)
    sys.stdout.flush()