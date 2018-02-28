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
    __RED = 1
    __GREEN = 2
    __YELLOW = 3
    __BLUE = 4

    __INDENT = 0

    @staticmethod
    def begin(message):
        """Log the beginning of a sequence in the terminal, in blue."""
        Logger.__log_label(Logger.__BLUE, 'INFO ', Logger.__indent() + '╭')
        Logger.__log_message(Logger.__BLUE, message)

        Logger.__INDENT += 1

    @staticmethod
    def info(message):
        """Log an information message in the terminal, in blue."""
        Logger.__log_label(Logger.__BLUE, 'INFO ', Logger.__indent(True) + '├')
        Logger.__log_message(Logger.__BLUE, message)

    @staticmethod
    def end(message):
        """Log the end of a sequence in the terminal, in blue and green."""
        Logger.__INDENT -= 1

        Logger.__log_label(Logger.__BLUE, 'INFO ', Logger.__indent() + '╰')
        Logger.__log_message(Logger.__GREEN, message)

    @staticmethod
    def error(message):
        """Log an error message in the terminal, in red."""
        Logger.__log_label(Logger.__RED, 'ERROR', Logger.__indent(True) + '╳')
        Logger.__log_message(Logger.__RED, message)

    @staticmethod
    def warning(message):
        """Log a warning message in the terminal, in yellow."""
        Logger.__log_label(Logger.__YELLOW, 'WARN ', Logger.__indent(True) + '!')
        Logger.__log_message(Logger.__YELLOW, message)

    @staticmethod
    def __indent(overwrite=False):
        """Indent the message with the input prefix."""
        return '│' * (Logger.__INDENT - int(overwrite))

    @staticmethod
    def __log_label(color_number, label, prefix):
        """Label logging."""
        code = '\033[{}m'

        color = code.format(90 + color_number)
        default = code.format(39)

        print('[{}{}{}] '.format(color, label, default), end='')
        print('{}{}{} '.format(color, prefix, default), end='')

    @staticmethod
    def __log_message(color_number, message):
        """Message logging."""
        code = '\033[{}m'

        print('{}{}{}'.format(code.format(90 + color_number), message, code.format(39)))
