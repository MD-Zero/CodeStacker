#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Code cleaner: erase compilation results.
"""

####################################################################################################

def clean(dir_root, config):
    """
    Clean the "build" and "bin" folders.
    """
    import os

    from .            import constants as keys
    from .file_system import get_absolute_path, get_files_with_extension
    from .logger      import log_info, log_ok

    # Dereferenced for performance.
    dir_bin = config[keys.KEY_DIR_BIN]
    dir_build = config[keys.KEY_DIR_BUILD]

    log_info('>> Cleaning-up')

    object_files = get_files_with_extension(dir_build, '.o')

    for file in object_files:
        os.remove(file)

    log_ok('<< Clean-up successful')
