#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Code cleaner: erase compilation results.
"""

####################################################################################################

def clean(config):
    """
    Clean the "build" and "bin" folders.
    """
    import os

    from .            import keys
    from .file_system import get_files
    from .logger      import log_info, log_ok

    # Dereferenced for performance.
    root = config[keys.ROOT]

    log_info('>> Cleaning-up')

    # Remove '*.o' object files.
    for file in get_files(config[keys.BUILD], '.o'):
        relative_file = os.path.relpath(file, root)

        log_info('Cleaning-up {}...'.format(relative_file))

        os.remove(file)

    # Remove the produced executable.
    executable_file = os.path.join(config[keys.BINARY], config[keys.OUTPUT])

    if os.path.exists(executable_file):
        log_info('Cleaning-up {}...'.format(os.path.relpath(executable_file, root)))

        os.remove(executable_file)

    log_ok('<< Clean-up successful')
