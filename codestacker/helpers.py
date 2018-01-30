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

    print(red('[ERROR] {}'.format(message)))

    if exception is not None:
        print(exception)

    sys.exit()


def green(message):
    """
    Color the input in green, for terminal printing.
    """
    return '{}{}{}'.format('\033[92m', message, '\033[0m')


def red(message):
    """
    Color the input in red, for terminal printing.
    """
    return '{}{}{}'.format('\033[91m', message, '\033[0m')
