#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Code cleaner: erase compilation results.
"""

####################################################################################################

def clean(config):
    """
    Clean any compilation results.
    """
    import os

    from .       import keys
    from .logger import Logger

    Logger.begin('Cleaning-up...')

    # Dereferenced for performance.
    root = config[keys.ROOT]

    # Clean-up "build" directory.
    _remove_files(config[keys.BUILD], root)

    # Clean-up "bin" directory.
    _remove_files(config[keys.BINARY], root)

    # Clean-up "*.gch" precompiled header files.
    _remove_files(config[keys.SOURCES], root, '.gch')

    Logger.end('Clean-up successful')

####################################################################################################

def _remove_files(directory, root, extension=''):
    """
    Remove all files within "directory" ending with "extension".
    """
    import os

    from .logger      import Logger
    from .file_system import get_files

    for file in get_files(directory, extension):
        Logger.info('Cleaning-up {}...'.format(os.path.relpath(file, root)))

        os.remove(file)
