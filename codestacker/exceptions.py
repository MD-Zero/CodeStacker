#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
User-defined exceptions.
"""

####################################################################################################

class Error(Exception):
    """
    Base class for exceptions.
    """
    def __init__(self, message, details=None):
        """Initialization."""
        super().__init__()

        self.message = message
        self.details = details

    def get_message(self):
        """Return the error message (used for unit test [BAD])."""
        return self.message

    def print(self):
        """Log a formatted error message."""
        from .logger import log_error

        log_error(self.__class__.__name__ + ': ' + self.message)

        if self.details is not None:
            print(self.details)

####################################################################################################

class GraphError(Error):
    """
    Graph-related error.
    """
    pass

####################################################################################################

class FunctionalError(Error):
    """
    Functional error.
    """
    pass

####################################################################################################

class TechnicalError(Error):
    """
    Technical error.
    """
    pass
