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

    from .       import cache_builder, keys
    from .logger import Logger

    Logger.begin('Cleaning-up')

    # Dereferenced for performance.
    root = config[keys.ROOT]
    build_dir = config[keys.BUILD]

    # Remove '*.o' object files.
    _remove_files(build_dir, '.o', root)

    # Remove '*.gch' precompiled header files.
    _remove_files(config[keys.SOURCES], '.gch', root)

    # Remove the produced executable.
    _remove_file(os.path.join(config[keys.BINARY], config[keys.OUTPUT]), root)

    # Remove the cache file.
    _remove_file(os.path.join(build_dir, cache_builder.CACHE_FILENAME), root)

    Logger.end('Clean-up successful')

####################################################################################################

def _remove_files(directory, extension, root):
    """
    Remove all files within "directory" ending with "extension".
    """
    import os

    from .logger      import Logger
    from .file_system import get_files

    for file in get_files(directory, extension):
        Logger.info('Cleaning-up {}...'.format(os.path.relpath(file, root)))

        os.remove(file)

####################################################################################################

def _remove_file(file, root):
    """
    Remove "file" in input.
    """
    import os

    from .logger import Logger

    if os.path.exists(file):
        Logger.info('Cleaning-up {}...'.format(os.path.relpath(file, root)))

        os.remove(file)
