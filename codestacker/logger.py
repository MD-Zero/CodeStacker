#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Logging utilities.
"""

####################################################################################################

_FG_DEFAULT = '\033[39m'
_BG_DEFAULT = '\033[49m'

####################################################################################################

def log_error(message):
    """
    Log an error message in the terminal, in light red.
    """
    red = '\033[91m'

    _log_label(red, 'ERROR')
    _log_message(red, message)

####################################################################################################

def log_warning(message):
    """
    Log a warning message in the terminal, in light yellow.
    """
    yellow = '\033[93m'

    _log_label(yellow, 'WARN ')
    _log_message(yellow, message)

####################################################################################################

def log_info(message):
    """
    Log an information message in the terminal, in light blue.
    """
    blue = '\033[94m'

    _log_label(blue, 'INFO ')
    _log_message(blue, message)

####################################################################################################

def log_ok(message):
    """
    Log an "OK" message in the terminal, in light green.
    """
    bg_green = '\033[42m'
    fg_green = '\033[92m'

    _log_label(bg_green, ' OK  ', 0)
    _log_message(fg_green, message)

####################################################################################################

def log_ko(message):
    """
    Log a "KO" message in the terminal, in light red.
    """
    bg_red = '\033[41m'
    fg_red = '\033[91m'

    _log_label(bg_red, ' KO  ', 0)
    _log_message(fg_red, message)

####################################################################################################

def _log_label(color, label, z_index=1):
    """
    Label logging.
    """
    if z_index == 1:
        print('[{}{}{}] '.format(color, label, _FG_DEFAULT), end='')
    elif z_index == 0:
        print('[{}{}{}] '.format(color, label, _BG_DEFAULT), end='')

####################################################################################################

def _log_message(color, message):
    """
    Message logging.
    """
    print('{}{}{}'.format(color, message, _FG_DEFAULT))
