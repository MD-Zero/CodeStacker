#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Helper functions.
"""

WITHOUT_EXCEPTION = '[ERROR] {}'
WITH_EXCEPTION = '[ERROR] {} --'

def print_and_die(message, exception=None):
    """
    Print a message (and associated error, if provided), then quit the program.
    """
    import sys

    if exception is None:
        print(WITHOUT_EXCEPTION.format(message))
    else:
        print(WITH_EXCEPTION.format(message), exception)

    sys.exit()
