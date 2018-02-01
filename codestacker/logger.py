#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Logging utilities.
"""

_LOG_ERROR = '[ERROR]'
_LOG_INFO = '[INFO ]'
_LOG_KO = '[ KO  ]'
_LOG_OK = '[ OK  ]'
_LOG_WARNING = '[WARN ]'

_COL_BLUE = '\033[94m'
_COL_GREEN = '\033[92m'
_COL_NONE = '\033[0m'
_COL_RED = '\033[91m'
_COL_YELLOW = '\033[93m'

####################################################################################################

def log_error(message):
    """
    Log an error message in the terminal.
    """
    print('{}{} {}{}'.format(_COL_RED, _LOG_ERROR, message, _COL_NONE))

####################################################################################################

def log_info(message):
    """
    Log an information message in the terminal.
    """
    print('{}{} {}{}'.format(_COL_BLUE, _LOG_INFO, message, _COL_NONE))

####################################################################################################

def log_ko(message):
    """
    Log a "KO" message in the terminal.
    """
    print('{}{} {}{}'.format(_COL_RED, _LOG_KO, message, _COL_NONE))

####################################################################################################

def log_ok(message):
    """
    Log an "OK" message in the terminal.
    """
    print('{}{} {}{}'.format(_COL_GREEN, _LOG_OK, message, _COL_NONE))

####################################################################################################

def log_warning(message):
    """
    Log a warning message in the terminal.
    """
    print('{}{} {}{}'.format(_COL_YELLOW, _LOG_WARNING, message, _COL_NONE))
