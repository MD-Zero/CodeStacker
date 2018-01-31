#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Helper functions.
"""

####################################################################################################

def print_and_die(message, exception=None):
    """
    Print a message (and associated error, if provided), then quit the program.
    """
    import sys

    from .logger import log_error

    log_error(message)

    if exception is not None:
        print(exception)

    log_error('Script stopped.')

    sys.exit()
