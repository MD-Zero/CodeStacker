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
    from .       import keys as K
    from .logger import Logger

    Logger.begin('Cleaning-up...')

    # Dereferenced for performance.
    root = config[K.ROOT]

    # Clean-up "build" directory.
    _remove_files(config[K.BUILD], root)

    # Clean-up "bin" directory.
    _remove_files(config[K.BINARY], root)

    # Clean-up "*.gch" precompiled header files.
    # _remove_files(config[keys.SOURCES], root, '.gch')

    Logger.end('Clean-up successful')

####################################################################################################

def _remove_files(directory, root):
    """
    Remove all files within "directory".
    """
    import os
    import shutil

    from .           import errors as E
    from .exceptions import TechnicalError
    from .logger     import Logger

    with os.scandir(directory) as entries:
        for entry in entries:
            abs_entry = os.path.join(directory, entry)

            Logger.info('Cleaning-up {}...'.format(os.path.relpath(abs_entry, root)))

            try:
                if os.path.isfile(abs_entry):
                    os.unlink(abs_entry)
                elif os.path.isdir(abs_entry):
                    shutil.rmtree(abs_entry)
                else:
                    Logger.warning('"{}" neither file nor directory: skipped'.format(abs_entry))
            except Exception as error:
                raise TechnicalError(E.REMOVAL_FAILED.format(abs_entry), error)
