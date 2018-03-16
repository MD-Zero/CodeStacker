#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Logging utilities.
"""

####################################################################################################

class Logger():
    """
    Simple logging class.
    """
    __RED = '\033[91m'
    __GREEN = '\033[92m'
    __YELLOW = '\033[93m'
    __BLUE = '\033[94m'
    __NONE = '\033[39m'

    __INDENT = 0

    @staticmethod
    def begin(message):
        """Log the beginning of a sequence in the terminal, in blue."""
        Logger.__INDENT += 1

        Logger.__log_label(Logger.__BLUE, 'INFO ', Logger.__indent() + '╭'' ')
        Logger.__log_message(Logger.__BLUE, message)

    @staticmethod
    def info(message):
        """Log an information message in the terminal, in blue."""
        prefix = '•'' ' if Logger.__INDENT == 0 else Logger.__indent() + '├'' '

        Logger.__log_label(Logger.__BLUE, 'INFO ', prefix)
        Logger.__log_message(Logger.__BLUE, message)

    @staticmethod
    def end(message):
        """Log the end of a sequence in the terminal, in blue and green."""
        Logger.__log_label(Logger.__BLUE, 'INFO ', Logger.__indent() + '╰'' ')
        Logger.__log_message(Logger.__GREEN, message)

        Logger.__INDENT -= 1

    @staticmethod
    def error(message):
        """Log an error message in the terminal, in red."""
        Logger.__log_label(Logger.__RED, 'ERROR', Logger.__indent('╵') + '╰'' ')
        Logger.__log_message(Logger.__RED, message)

    @staticmethod
    def warning(message):
        """Log a warning message in the terminal, in yellow."""
        Logger.__log_label(Logger.__YELLOW, 'WARN ', Logger.__indent() + '!'' ')
        Logger.__log_message(Logger.__YELLOW, message)

    @staticmethod
    def abort(message):
        """Log a special message for aborting the flow in the terminal, in red."""
        Logger.__log_label(Logger.__RED, 'ERROR', Logger.__indent('─') + '─'' ')
        Logger.__log_message(Logger.__RED, message)

    @staticmethod
    def close(message):
        """Log a special message for aborting the flow in the terminal, in red."""
        Logger.__log_label(Logger.__BLUE, 'INFO ', '×'' ')
        Logger.__log_message(Logger.__BLUE, message)

    @staticmethod
    def __indent(symbol='│'):
        """Indent the message with the input symbol."""
        return symbol * (Logger.__INDENT - 1)

    @staticmethod
    def __log_label(color_number, label, prefix):
        """Label logging."""
        print('[{}{}{}] '.format(color_number, label, Logger.__NONE), end='')
        print('{}{}{}'.format(color_number, prefix, Logger.__NONE), end='')

    @staticmethod
    def __log_message(color_number, message):
        """Message logging."""
        print('{}{}{}'.format(color_number, message, Logger.__NONE))
