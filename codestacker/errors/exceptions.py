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
    def __init__(self, message, details=None, error=None):
        """Constructor."""
        super().__init__(message, details, error)

    def print(self):
        """Log a formatted error message."""
        from codestacker.logger import Logger

        message = self.args[0]
        details = self.args[1]
        error = self.args[2]

        if details is not None:
            message += ' ({})'.format(details)

        Logger.error('{}: {}'.format(self.__class__.__name__, message))

        if error is not None:
            print(error.rstrip('\n'))

####################################################################################################

class FileSystemError(Error):
    """
    Technical error.
    """
    pass

####################################################################################################

class FunctionalError(Error):
    """
    Functional error.
    """
    pass

####################################################################################################

class GraphError(Error):
    """
    Graph-related error.
    """
    pass

####################################################################################################

class TechnicalError(Error):
    """
    Technical error.
    """
    pass
