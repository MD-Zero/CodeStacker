#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Logging utilities.
"""

LOG_INFO = '[INFO ]'
LOG_WARNING = '[WARN ]'
LOG_ERROR = '[ERROR]'

COL_BLUE = '\033[94m'
COL_NONE = '\033[0m'
COL_RED = '\033[91m'
COL_YELLOW = '\033[93m'

####################################################################################################

def log_info(message):
    """
    Log an information message in the terminal.
    """
    print('{}{} {}{}'.format(COL_BLUE, LOG_INFO, message, COL_NONE))

####################################################################################################

def log_warning(message):
    """
    Log a warning message in the terminal.
    """
    print('{}{} {}{}'.format(COL_YELLOW, LOG_WARNING, message, COL_NONE))

####################################################################################################

def log_error(message):
    """
    Log an error message in the terminal.
    """
    print('{}{} {}{}'.format(COL_RED, LOG_ERROR, message, COL_NONE))
